from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .common import exact_ci, ollama_generate, scenario_row

ROOT = Path(__file__).resolve().parents[2] / "data" / "benchmarks"
LABELS = ROOT / "ait_labels.csv"
AMINER = ROOT / "ait-ads" / "russellmitchell_aminer.json"

SELECTED_ATTACKS = ["network_scans", "webshell", "dirb"]


def _load_labels() -> list[dict[str, str]]:
    with LABELS.open() as fh:
        return [row for row in csv.DictReader(fh) if row.get("scenario") == "russellmitchell"]


def _iter_alerts(path: Path):
    text = path.read_text(errors="replace").strip()
    if text.startswith("["):
        raw = json.loads(text)
        if isinstance(raw, dict):
            alerts = raw.get("alerts") or raw.get("events") or raw.get("data") or []
            if isinstance(alerts, dict):
                alerts = list(alerts.values())
        else:
            alerts = raw
        for item in alerts:
            if isinstance(item, dict):
                yield item
        return
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            yield item


def _sample_alerts(path: Path, start: float, end: float, limit: int = 40) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    fallback: list[dict[str, Any]] = []
    for item in _iter_alerts(path):
        log = item.get("LogData") if isinstance(item.get("LogData"), dict) else {}
        analysis = item.get("AnalysisComponent") if isinstance(item.get("AnalysisComponent"), dict) else {}
        ts = None
        for candidate in (
            item.get("timestamp"),
            item.get("@timestamp"),
            (log.get("Timestamps") or [None])[0],
            (log.get("DetectionTimestamp") or [None])[0],
        ):
            if candidate is not None:
                ts = candidate
                break
        raw_logs = log.get("RawLogData") or []
        message = raw_logs[0] if raw_logs else str(log or item)[:300]
        detector = (
            analysis.get("AnalysisComponentName")
            or item.get("AnalysisComponentName")
            or item.get("detector")
            or item.get("rule")
        )
        try:
            tsf = float(ts)
        except (TypeError, ValueError):
            if len(fallback) < limit:
                fallback.append({"timestamp": ts, "detector": detector, "message": message})
            continue
        row = {"timestamp": tsf, "detector": detector, "message": message}
        if start <= tsf <= end:
            out.append(row)
            if len(out) >= limit:
                break
        elif len(fallback) < limit:
            fallback.append(row)
    return out or fallback


def load_scenarios(limit: int = 3) -> list[dict[str, Any]]:
    if not AMINER.exists() or not LABELS.exists():
        return []
    labels = _load_labels()
    by_attack = {row["attack"]: row for row in labels}
    scenarios: list[dict[str, Any]] = []
    for attack in SELECTED_ATTACKS[:limit]:
        row = by_attack.get(attack)
        if not row:
            continue
        start, end = float(row["start"]), float(row["end"])
        evidence = _sample_alerts(AMINER, start, end)
        scenarios.append(
            {
                "id": f"ait-ads:russellmitchell:{attack}",
                "dataset": "Cyber-AIT-ADS",
                "scenario": f"russellmitchell/{attack}",
                "prompt": (
                    "Based on the AMiner alerts in the evidence window, which multi-step attack stage "
                    "is occurring? Reply with one attack label only "
                    f"(one of: {', '.join(SELECTED_ATTACKS + ['service_scans', 'wpscan', 'webshell'])})."
                ),
                "answer": attack,
                "accept": [attack, attack.replace("_", " ")],
                "evidence": json.dumps(evidence, indent=2)[:8000],
            }
        )
    return scenarios


def run_scenario(scenario: dict[str, Any], *, model: str, base_url: str) -> dict[str, Any]:
    system = (
        "You classify multi-step cyber attacks from IDS alert evidence. "
        "Reply with only the attack stage label."
    )
    user = f"Evidence alerts:\n{scenario['evidence']}\n\nQuestion: {scenario['prompt']}\nAnswer:"
    try:
        pred = ollama_generate(model=model, system=system, user=user, base_url=base_url, num_predict=64)
        score = exact_ci(pred, scenario["accept"])
        return scenario_row(
            dataset=scenario["dataset"],
            scenario=scenario["scenario"],
            model=model,
            score=score,
            detail="exact_ci attack-stage label",
            prediction=pred,
            gold=scenario["answer"],
        )
    except Exception as exc:  # noqa: BLE001
        return scenario_row(
            dataset=scenario["dataset"],
            scenario=scenario["scenario"],
            model=model,
            score=0.0,
            status="failed",
            detail=str(exc),
            gold=scenario["answer"],
        )
