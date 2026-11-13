from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .common import ollama_generate, scenario_row, token_f1

ROOT = Path(__file__).resolve().parents[2] / "data" / "benchmarks" / "discoverybench"
REAL_TEST = ROOT / "discoverybench" / "real" / "test"
SYNTH_TEST = ROOT / "discoverybench" / "synth" / "test"
ANSWER_REAL = ROOT / "answer_key" / "answer_key_real.csv"
ANSWER_SYNTH = ROOT / "answer_key" / "answer_key_synth.csv"


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    return list(csv.DictReader(text.splitlines()))


def _flatten_queries(raw: Any) -> list[dict[str, Any]]:
    flat: list[dict[str, Any]] = []
    for item in raw or []:
        if isinstance(item, list):
            flat.extend([q for q in item if isinstance(q, dict)])
        elif isinstance(item, dict):
            flat.append(item)
    return flat


def _csv_preview(path: Path, max_rows: int = 10) -> str:
    if not path.exists():
        return f"(missing {path.name})"
    lines = path.read_text(errors="replace").splitlines()
    return "\n".join(lines[: max_rows + 1])


def _build_from_answer_key(
    rows: list[dict[str, str]],
    *,
    root: Path,
    split: str,
    limit: int | None,
) -> list[dict[str, Any]]:
    scenarios: list[dict[str, Any]] = []
    for row in rows:
        if limit is not None and len(scenarios) >= limit:
            break
        dataset = row["dataset"]
        metadata_id = row["metadataid"]
        query_id = row["query_id"]
        gold = row.get("gold_hypo") or ""
        # Synth folders are named like ancient-languages_0_0; real folders are domain names.
        meta_path = root / dataset / f"metadata_{metadata_id}.json"
        if not meta_path.exists():
            # Some synth metadata ids differ; try any metadata in folder.
            folder = root / dataset
            candidates = sorted(folder.glob("metadata_*.json")) if folder.exists() else []
            meta_path = candidates[0] if candidates else meta_path
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text(errors="replace"))
        flat = _flatten_queries(meta.get("queries"))
        qid = int(query_id)
        query = next((q for q in flat if int(q.get("qid", -1)) == qid), flat[0] if flat else None)
        if not query:
            # Synth answer keys sometimes use opaque query ids; fall back to first question text.
            query = flat[0] if flat else {"question": f"Derive the main discovery hypothesis for {dataset}."}
        previews = []
        data_csv = meta_path.parent / "data.csv"
        if data_csv.exists():
            previews.append(f"### data.csv\n{_csv_preview(data_csv)}")
        for ds in (meta.get("datasets") or [])[:2]:
            name = ds.get("name")
            if name:
                previews.append(f"### {name}\n{_csv_preview(meta_path.parent / name)}")
        scenarios.append(
            {
                "id": f"discoverybench:{split}:{dataset}:m{metadata_id}:q{query_id}",
                "dataset": "DiscoveryBench",
                "scenario": f"{split}/{dataset}/metadata_{metadata_id}/q{query_id}",
                "domain": meta.get("domain") or split,
                "domain_knowledge": meta.get("domain_knowledge") or "",
                "question": query.get("question") or "",
                "gold": gold,
                "data_preview": "\n\n".join(previews)[:6000],
            }
        )
    return scenarios


def load_scenarios(limit: int | None = None) -> list[dict[str, Any]]:
    real = _build_from_answer_key(
        _read_csv_rows(ANSWER_REAL),
        root=REAL_TEST,
        split="real",
        limit=limit,
    )
    remaining = None if limit is None else max(0, limit - len(real))
    synth = _build_from_answer_key(
        _read_csv_rows(ANSWER_SYNTH),
        root=SYNTH_TEST,
        split="synth",
        limit=remaining,
    )
    return real + synth


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
