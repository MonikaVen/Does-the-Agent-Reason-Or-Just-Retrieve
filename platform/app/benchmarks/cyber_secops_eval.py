from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import exact_ci, ollama_generate, scenario_row, token_f1

ROOT = Path(__file__).resolve().parents[2] / "data" / "benchmarks" / "secops-es-benchmark"
KEYS = ROOT / ".keys"
PUBLIC_Q = ROOT / "benchmark" / "questions"

# Evidence-based extraction questions across the first three cases.
SELECTED = [
    ("case-01.json", 0),
    ("case-01.json", 1),
    ("case-02.json", 0),
    ("case-02.json", 1),
    ("case-03.json", 0),
]


def _merge_question(public: dict[str, Any], sealed: dict[str, Any] | None) -> dict[str, Any]:
    row = dict(public)
    if sealed:
        for key in ("answer", "accept", "attck", "source", "evidence_query"):
            if key in sealed:
                row[key] = sealed[key]
    return row


def _evidence_for_case(case: str) -> str:
    case_dir = KEYS / "corpus" / "cases" / case
    chunks: list[str] = []
    for path in sorted(case_dir.glob("evidence*.json")):
        data = json.loads(path.read_text())
        chunks.append(f"## {path.name}\n{json.dumps(data, indent=2)[:5000]}")
    gt = case_dir / "groundtruth.md"
    if gt.exists():
        chunks.append("## groundtruth notes\n" + gt.read_text()[:2500])
    return "\n\n".join(chunks)[:9000]


def load_scenarios(limit: int = 5) -> list[dict[str, Any]]:
    scenarios: list[dict[str, Any]] = []
    for filename, idx in SELECTED[:limit]:
        public_path = PUBLIC_Q / filename
        sealed_path = KEYS / "benchmark" / "questions" / filename
        public_rows = json.loads(public_path.read_text())
        sealed_rows = json.loads(sealed_path.read_text()) if sealed_path.exists() else []
        sealed_by_id = {row.get("id"): row for row in sealed_rows}
        if idx >= len(public_rows):
            continue
        public = public_rows[idx]
        row = _merge_question(public, sealed_by_id.get(public.get("id")))
        case = row.get("case") or filename.replace(".json", "")
        answer = row.get("answer") or ""
        accept = row.get("accept")
        if accept is None:
            accept = answer if isinstance(answer, list) else [answer]
        elif isinstance(accept, str):
            accept = [accept]
        scenarios.append(
            {
                "id": f"cyber:{row.get('id')}",
                "dataset": "Cyber-SecOps-ES",
                "scenario": f"{case}/{row.get('id')}",
                "prompt": row.get("prompt") or "",
                "answer": answer,
                "accept": list(accept),
                "grading": row.get("grading") or "exact_ci",
                "evidence": _evidence_for_case(case),
                "attck": row.get("attck") or [],
            }
        )
    return scenarios


def run_scenario(scenario: dict[str, Any], *, model: str, base_url: str) -> dict[str, Any]:
    system = (
        "You are a SOC investigator. Answer using only the supplied evidence. "
        "Reply with the shortest exact answer string (path, IP, hostname, or short phrase). "
        "No explanation."
    )
    user = (
        f"Evidence:\n{scenario['evidence']}\n\n"
        f"Question: {scenario['prompt']}\n"
        "Answer:"
    )
    try:
        pred = ollama_generate(model=model, system=system, user=user, base_url=base_url, num_predict=128)
        accept = list(scenario.get("accept") or [])
        answer = scenario.get("answer") or ""
        if isinstance(answer, list):
            accept = list(accept) + [str(x) for x in answer]
            gold = ", ".join(str(x) for x in answer)
        else:
            accept = list(accept) + [str(answer)]
            gold = str(answer)
        if scenario["grading"] == "exact_ci":
            score = exact_ci(pred, accept)
        else:
            score = max(exact_ci(pred, accept), token_f1(pred, gold))
        return scenario_row(
            dataset=scenario["dataset"],
            scenario=scenario["scenario"],
            model=model,
            score=score,
            detail=f"grading={scenario['grading']}; attck={','.join(scenario.get('attck') or [])}",
            prediction=pred,
            gold=gold,
        )
    except Exception as exc:  # noqa: BLE001
        answer = scenario.get("answer") or ""
        gold = ", ".join(str(x) for x in answer) if isinstance(answer, list) else str(answer)
        return scenario_row(
            dataset=scenario["dataset"],
            scenario=scenario["scenario"],
            model=model,
            score=0.0,
            status="failed",
            detail=str(exc),
            gold=gold,
        )
