from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .common import ollama_generate, scenario_row, token_f1

ROOT = Path(__file__).resolve().parents[2] / "data" / "benchmarks" / "discoverybench"
TEST = ROOT / "discoverybench" / "real" / "test"
ANSWER_KEY = ROOT / "answer_key" / "answer_key_real.csv"

# Small, diverse real-test scenarios with available CSVs.
SELECTED = [
    ("archaeology", "0", "0"),
    ("nls_incarceration", "0", "0"),
    ("worldbank_education_gdp", "0", "0"),
]


def _load_answers() -> dict[tuple[str, str, str], str]:
    out: dict[tuple[str, str, str], str] = {}
    with ANSWER_KEY.open() as fh:
        for row in csv.DictReader(fh):
            out[(row["dataset"], row["metadataid"], row["query_id"])] = row["gold_hypo"]
    return out


def _csv_preview(path: Path, max_rows: int = 12) -> str:
    if not path.exists():
        return f"(missing {path.name})"
    lines = path.read_text(errors="replace").splitlines()
    return "\n".join(lines[: max_rows + 1])


def load_scenarios(limit: int = 3) -> list[dict[str, Any]]:
    answers = _load_answers()
    scenarios: list[dict[str, Any]] = []
    for dataset, metadata_id, query_id in SELECTED[:limit]:
        meta_path = TEST / dataset / f"metadata_{metadata_id}.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text())
        raw_queries = meta.get("queries") or []
        # Real-test metadata stores queries as a list of groups.
        flat: list[dict[str, Any]] = []
        for item in raw_queries:
            if isinstance(item, list):
                flat.extend([q for q in item if isinstance(q, dict)])
            elif isinstance(item, dict):
                flat.append(item)
        qid = int(query_id)
        query = next((q for q in flat if int(q.get("qid", -1)) == qid), flat[0] if flat else None)
        if not query:
            continue
        gold = answers.get((dataset, metadata_id, query_id)) or query.get("true_hypothesis") or ""
        previews = []
        for ds in (meta.get("datasets") or [])[:2]:
            name = ds.get("name")
            if name:
                previews.append(f"### {name}\n" + _csv_preview(TEST / dataset / name))
        scenarios.append(
            {
                "id": f"discoverybench:{dataset}:m{metadata_id}:q{query_id}",
                "dataset": "DiscoveryBench",
                "scenario": f"{dataset}/metadata_{metadata_id}/q{query_id}",
                "domain": meta.get("domain"),
                "domain_knowledge": meta.get("domain_knowledge") or "",
                "question": query.get("question") or "",
                "gold": gold,
                "data_preview": "\n\n".join(previews)[:6000],
            }
        )
    return scenarios


def run_scenario(scenario: dict[str, Any], *, model: str, base_url: str) -> dict[str, Any]:
    system = (
        "You are a careful scientific discovery assistant. "
        "Use only the supplied tables and domain knowledge. "
        "Reply with one concise hypothesis sentence. No preamble."
    )
    user = (
        f"Domain: {scenario.get('domain')}\n"
        f"Domain knowledge:\n{scenario.get('domain_knowledge')}\n\n"
        f"Data previews:\n{scenario.get('data_preview')}\n\n"
        f"Question: {scenario['question']}\n"
        "Hypothesis:"
    )
    try:
        pred = ollama_generate(model=model, system=system, user=user, base_url=base_url, num_predict=256)
        score = token_f1(pred, scenario["gold"])
        return scenario_row(
            dataset=scenario["dataset"],
            scenario=scenario["scenario"],
            model=model,
            score=score,
            detail="token_f1 vs gold hypothesis",
            prediction=pred,
            gold=scenario["gold"],
        )
    except Exception as exc:  # noqa: BLE001
        return scenario_row(
            dataset=scenario["dataset"],
            scenario=scenario["scenario"],
            model=model,
            score=0.0,
            status="failed",
            detail=str(exc),
            gold=scenario["gold"],
        )
