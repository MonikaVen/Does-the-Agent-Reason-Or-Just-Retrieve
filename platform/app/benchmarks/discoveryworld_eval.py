from __future__ import annotations

import json
from typing import Any

from .common import ollama_generate, scenario_row, tokenize, yes_no_match


def _slim_obs(obs: dict[str, Any]) -> dict[str, Any]:
    ui = obs.get("ui") or {}
    nearby = ((ui.get("nearbyObjects") or {}).get("objects")) or {}
    names: list[str] = []
    for bucket in nearby.values():
        if not isinstance(bucket, list):
            continue
        for obj in bucket:
            if isinstance(obj, dict) and obj.get("name"):
                names.append(str(obj["name"]))
            elif isinstance(obj, str) and obj not in {".", "..."}:
                names.append(obj)
    accessible = []
    for obj in ui.get("accessibleEnvironmentObjects") or []:
        if isinstance(obj, dict):
            accessible.append({"name": obj.get("name"), "description": obj.get("description")})
    return {
        "task_hint_objects": sorted(set(names))[:40],
        "accessible": accessible[:20],
        "inventory": ui.get("inventoryObjects") or [],
    }


def _keywords_from_hypothesis(text: str) -> list[str]:
    stop = {
        "the", "a", "an", "and", "or", "of", "to", "with", "that", "is", "are", "can", "be",
        "which", "one", "for", "from", "this", "it", "on", "in",
    }
    toks = [t for t in tokenize(text) if len(t) > 2 and t not in stop]
    return toks[:12]


def _enumerate_specs(limit: int | None = None) -> list[dict[str, Any]]:
    from discoveryworld.DiscoveryWorldAPI import DiscoveryWorldAPI

    api = DiscoveryWorldAPI()
    valid = api.getValidScenarios()
    specs: list[dict[str, Any]] = []
    for name, info in valid.items():
        difficulties = info.get("difficulty") or ["Normal"]
        variations = info.get("variations") or ["1"]
        for difficulty in difficulties:
            for variation in variations:
                # API exposes variation via randomSeed (1..5 → seeds 0..4).
                try:
                    seed = max(0, int(variation) - 1)
                except ValueError:
                    seed = 0
                specs.append(
                    {
                        "id": f"discoveryworld:{name}:{difficulty}:seed{seed}",
                        "dataset": "DiscoveryWorld",
                        "scenario": f"{name}/{difficulty}/seed{seed}",
                        "theme": name,
                        "difficulty": difficulty,
                        "seed": seed,
                        "kind": "discovery",
                    }
                )
                if limit is not None and len(specs) >= limit:
                    return specs
    return specs


def _materialize(spec: dict[str, Any]) -> dict[str, Any]:
    if spec.get("task_description") is not None and spec.get("evidence") is not None:
        return spec
    from discoveryworld.DiscoveryWorldAPI import DiscoveryWorldAPI

    api = DiscoveryWorldAPI()
    ok = api.loadScenario(
        scenarioName=spec["theme"],
        difficultyStr=spec["difficulty"],
        randomSeed=int(spec["seed"]),
        numUserAgents=1,
    )
    if not ok:
        raise RuntimeError(f"failed to load DiscoveryWorld scenario {spec['scenario']}")
    scorecard = api.getTaskScorecard() or []
    task = scorecard[0] if scorecard else {}
    obs = api.getAgentObservation(agentIdx=0)
    spec = dict(spec)
    spec["task_description"] = task.get("taskDescription") or ""
    spec["critical_hypotheses"] = task.get("criticalHypotheses") or []
    spec["critical_questions"] = task.get("criticalQuestions") or []
    spec["evidence"] = _slim_obs(obs if isinstance(obs, dict) else {})
    # Expand critical questions as additional scenarios on first materialization callers.
    return spec


def load_scenarios(limit: int | None = None) -> list[dict[str, Any]]:
    """Return lightweight DiscoveryWorld specs; worlds load lazily during run_scenario."""
    base = _enumerate_specs(limit=None)
    expanded: list[dict[str, Any]] = []
    for spec in base:
        expanded.append(spec)
        # Placeholder CQ slots — concrete questions filled during run after world load.
        # We reserve up to 3 CQ scenarios per theme so inventory can reach ~1000.
        for idx in range(3):
            expanded.append(
                {
                    "id": f"{spec['id']}:cq{idx}",
                    "dataset": "DiscoveryWorld",
                    "scenario": f"{spec['scenario']}/cq{idx}",
                    "theme": spec["theme"],
                    "difficulty": spec["difficulty"],
                    "seed": spec["seed"],
                    "kind": "critical_question",
                    "cq_index": idx,
                }
            )
        if limit is not None and len(expanded) >= limit:
            return expanded[:limit]
    return expanded if limit is None else expanded[:limit]


def run_scenario(scenario: dict[str, Any], *, model: str, base_url: str) -> dict[str, Any]:
    try:
        # Materialize parent world once per theme/difficulty/seed via API.
        parent = {
            "theme": scenario["theme"],
            "difficulty": scenario["difficulty"],
            "seed": scenario["seed"],
            "scenario": f"{scenario['theme']}/{scenario['difficulty']}/seed{scenario['seed']}",
        }
        world = _materialize(parent)
        hyps = world.get("critical_hypotheses") or []
        questions = world.get("critical_questions") or []
        evidence = world.get("evidence") or {}
        task_description = world.get("task_description") or ""

        if scenario.get("kind") == "critical_question":
            idx = int(scenario.get("cq_index") or 0)
            if idx >= len(questions):
                return scenario_row(
                    dataset="DiscoveryWorld",
                    scenario=scenario["scenario"],
                    model=model,
                    score=0.0,
                    status="skipped",
                    detail="no critical question at index",
                )
            question = questions[idx]
            hyp = hyps[idx] if idx < len(hyps) else (hyps[0] if hyps else "")
            system = (
                "You answer scientific discovery questions from observed lab evidence only. "
                "Reply YES or NO, then one short justification sentence."
            )
            user = (
                f"Task: {task_description}\n"
                f"Observed evidence:\n{json.dumps(evidence, indent=2)}\n"
                f"Question: {question}\n"
                "Answer:"
            )
            pred = ollama_generate(model=model, system=system, user=user, base_url=base_url, num_predict=160)
            # Gold knowledge questions are framed so a correct discovery answers YES.
            score = yes_no_match(pred, True)
            keys = _keywords_from_hypothesis(hyp)
            if keys:
                covered = sum(1 for k in keys if k in pred.lower()) / len(keys)
                score = round(0.5 * score + 0.5 * (1.0 if covered >= 0.25 else 0.0), 4)
            return scenario_row(
                dataset="DiscoveryWorld",
                scenario=scenario["scenario"],
                model=model,
                score=score,
                detail="critical-question yes/no + keyword support",
                prediction=pred,
                gold=f"YES — {hyp}",
            )

        system = (
            "You are a scientific discovery agent in a simulated lab. "
            "Using only the task description and observed objects, state the key discovery "
            "in 2-4 sentences. Do not mention game UI."
        )
        user = (
            f"Task: {task_description}\n"
            f"Observed evidence:\n{json.dumps(evidence, indent=2)}\n"
            "Discovery statement:"
        )
        pred = ollama_generate(model=model, system=system, user=user, base_url=base_url, num_predict=320)
        if not hyps:
            score = 0.0
        else:
            hits = 0
            total = 0
            pred_l = pred.lower()
            for hyp in hyps:
                keys = _keywords_from_hypothesis(hyp)
                if not keys:
                    continue
                total += 1
                matched = sum(1 for k in keys if k in pred_l)
                if matched / max(1, len(keys)) >= 0.35:
                    hits += 1
            score = round(hits / max(1, total), 4)
        return scenario_row(
            dataset="DiscoveryWorld",
            scenario=scenario["scenario"],
            model=model,
            score=score,
            detail="critical-hypothesis keyword coverage",
            prediction=pred,
            gold="; ".join(hyps),
        )
    except Exception as exc:  # noqa: BLE001
        return scenario_row(
            dataset=scenario.get("dataset") or "DiscoveryWorld",
            scenario=scenario.get("scenario") or "unknown",
            model=model,
            score=0.0,
            status="failed",
            detail=str(exc),
        )
