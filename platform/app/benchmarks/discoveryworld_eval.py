from __future__ import annotations

import json
import re
from typing import Any

from .common import ollama_generate, scenario_row, tokenize

SELECTED = [
    ("Space Sick", "Easy", 0),
    ("Combinatorial Chemistry", "Easy", 0),
    ("Archaeology Dating", "Easy", 0),
]


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
            accessible.append(
                {
                    "name": obj.get("name"),
                    "description": obj.get("description"),
                }
            )
    return {
        "task_hint_objects": sorted(set(names))[:40],
        "accessible": accessible[:20],
        "inventory": ui.get("inventoryObjects") or [],
    }


def _keywords_from_hypothesis(text: str) -> list[str]:
    stop = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "of",
        "to",
        "with",
        "that",
        "is",
        "are",
        "can",
        "be",
        "which",
        "one",
        "for",
        "from",
        "this",
        "it",
        "on",
        "in",
    }
    toks = [t for t in tokenize(text) if len(t) > 2 and t not in stop]
    # Keep distinctive tokens / multi-digit species-like ids.
    return toks[:12]


def load_scenarios(limit: int = 3) -> list[dict[str, Any]]:
    from discoveryworld.DiscoveryWorldAPI import DiscoveryWorldAPI

    scenarios: list[dict[str, Any]] = []
    for name, difficulty, seed in SELECTED[:limit]:
        api = DiscoveryWorldAPI()
        ok = api.loadScenario(
            scenarioName=name,
            difficultyStr=difficulty,
            randomSeed=seed,
            numUserAgents=1,
        )
        if not ok:
            continue
        scorecard = api.getTaskScorecard() or []
        task = scorecard[0] if scorecard else {}
        obs = api.getAgentObservation(agentIdx=0)
        scenarios.append(
            {
                "id": f"discoveryworld:{name}:{difficulty}:seed{seed}",
                "dataset": "DiscoveryWorld",
                "scenario": f"{name}/{difficulty}/seed{seed}",
                "task_description": task.get("taskDescription") or "",
                "critical_hypotheses": task.get("criticalHypotheses") or [],
                "critical_questions": task.get("criticalQuestions") or [],
                "evidence": _slim_obs(obs if isinstance(obs, dict) else {}),
            }
        )
    return scenarios


def run_scenario(scenario: dict[str, Any], *, model: str, base_url: str) -> dict[str, Any]:
    system = (
        "You are a scientific discovery agent in a simulated lab. "
        "Using only the task description and observed objects, state the key discovery "
        "in 2-4 sentences: what is contaminated/special, and which instrument detects it "
        "or which relation holds. Do not mention game UI."
    )
    user = (
        f"Task: {scenario['task_description']}\n"
        f"Observed evidence:\n{json.dumps(scenario['evidence'], indent=2)}\n"
        "Discovery statement:"
    )
    try:
        pred = ollama_generate(model=model, system=system, user=user, base_url=base_url, num_predict=320)
        # Lexical coverage of critical hypotheses — evidence-grounded proxy for knowledge score.
        hyps = scenario.get("critical_hypotheses") or []
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
            dataset=scenario["dataset"],
            scenario=scenario["scenario"],
            model=model,
            score=score,
            detail="critical-hypothesis keyword coverage",
            prediction=pred,
            gold="; ".join(hyps),
        )
    except Exception as exc:  # noqa: BLE001
        return scenario_row(
            dataset=scenario["dataset"],
            scenario=scenario["scenario"],
            model=model,
            score=0.0,
            status="failed",
            detail=str(exc),
            gold="; ".join(scenario.get("critical_hypotheses") or []),
        )
