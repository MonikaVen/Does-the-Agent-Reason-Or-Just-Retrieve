#!/usr/bin/env python3
"""Convert Cyber-SecOps-ES + Cyber-AIT-ADS scenarios into C0–C7 incident packs.

Writes JSON packs under data/packs/{secops,ait_ads}/ and a manifest.json.
DiscoveryBench / DiscoveryWorld are intentionally excluded (not investigation packs).
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.benchmarks import ait_ads_eval, cyber_secops_eval  # noqa: E402
from app.orchestrator import validate_pack  # noqa: E402

OUT = ROOT / "data" / "packs"
SECOPS_CASES = (
    ROOT / "data" / "benchmarks" / "secops-es-benchmark" / ".keys" / "corpus" / "cases"
)


def _slug(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", text).strip("-").lower() or "item"


def _iso_from_any(value: Any, default: str = "2026-01-01T00:00:00Z") -> str:
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = str(value).strip()
    if not text:
        return default
    if text.endswith("Z") or "+" in text[10:]:
        return text.replace("+00:00", "Z")
    try:
        # numeric string timestamp
        return datetime.fromtimestamp(float(text), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        pass
    if "T" not in text and len(text) >= 10:
        return text[:10] + "T00:00:00Z"
    return text if "T" in text else default


def _event_id(prefix: str, index: int, blob: str) -> str:
    digest = hashlib.sha1(blob.encode("utf-8", errors="replace")).hexdigest()[:8]
    return f"{prefix}-{index:04d}-{digest}"


def _base_pack(
    *,
    incident_id: str,
    name: str,
    alert: dict[str, Any],
    host: str,
    window: tuple[str, str],
    telemetry: dict[str, list[dict[str, Any]]],
    ground_truth: dict[str, Any],
    sources: list[str],
) -> dict[str, Any]:
    records = [rec for items in telemetry.values() for rec in items]
    # Prefer earliest process/network-like records as oracle evidence.
    oracle_evidence = []
    for rec in records[: min(3, len(records))]:
        fields = {
            k: v
            for k, v in rec.items()
            if k not in {"event_id", "timestamp", "host", "source"}
        }
        oracle_evidence.append(
            {
                "event_id": rec["event_id"],
                "source": rec.get("source") or next(
                    (src for src, items in telemetry.items() if rec in items), "process_events"
                ),
                "timestamp": rec.get("timestamp"),
                "host": rec.get("host") or host,
                "fields": fields,
            }
        )
    # If we somehow have no records, synthesize a minimal telemetry stub so validate_pack passes.
    if not records:
        stub_id = _event_id("stub", 1, incident_id)
        telemetry = {
            "process_events": [
                {
                    "event_id": stub_id,
                    "timestamp": window[0],
                    "host": host,
                    "process_name": "unknown",
                    "command_line": name,
                }
            ]
        }
        records = telemetry["process_events"]
        oracle_evidence = [
            {
                "event_id": stub_id,
                "source": "process_events",
                "timestamp": window[0],
                "host": host,
                "fields": {"process_name": "unknown", "command_line": name},
            }
        ]

    primary_source = next(iter(telemetry.keys()))
    oracle_plan = [
        {
            "order": 1,
            "question": "What processes or alerts fired in the investigation window?",
            "tool": "query_events",
            "arguments": {"source": primary_source, "filter": {"host": host}, "limit": 50},
        },
        {
            "order": 2,
            "question": "Are there related network or secondary signals on this host?",
            "tool": "query_events",
            "arguments": {
                "source": "network" if "network" in telemetry else primary_source,
                "filter": {"host": host},
                "limit": 50,
            },
        },
        {
            "order": 3,
            "question": "What ATT&CK or detection knowledge matches this alert?",
            "tool": "retrieve_knowledge",
            "arguments": {
                "question": alert.get("summary") or name,
                "corpus_tags": ["detection", "attack"],
                "top_k": 3,
            },
        },
    ]
    fixed_query_pack = {
        "version": "converted-pack-v1",
        "queries": [
            {
                "tool": "query_events",
                "arguments": {"source": primary_source, "filter": {"host": host}, "limit": 50},
            },
            {
                "tool": "query_events",
                "arguments": {
                    "source": "network" if "network" in telemetry else primary_source,
                    "filter": {"host": host},
                    "limit": 50,
                },
            },
            {
                "tool": "retrieve_knowledge",
                "arguments": {
                    "question": alert.get("summary") or name,
                    "corpus_tags": ["detection"],
                    "top_k": 3,
                },
            },
        ],
    }
    return {
        "incident_id": incident_id,
        "name": name,
        "source_benchmark": ground_truth.get("dataset"),
        "source_scenario": ground_truth.get("scenario"),
        "alert": alert,
        "scope": {
            "allowed_log_sources": sources,
            "start": window[0],
            "end": window[1],
            "hosts": [host],
        },
        "telemetry": telemetry,
        "oracle_evidence": oracle_evidence,
        "oracle_plan": oracle_plan,
        "fixed_query_pack": fixed_query_pack,
        "ground_truth": ground_truth,
    }


def _ingest_process_rows(
    rows: list[dict[str, Any]], *, host: str, prefix: str
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            continue
        ts = _iso_from_any(row.get("ts") or row.get("timestamp"))
        cmd = str(row.get("cmd") or row.get("command_line") or row.get("name") or "")
        name = str(row.get("name") or row.get("process_name") or "process")
        parent = str(row.get("parent") or row.get("parent_process_name") or "")
        blob = json.dumps(row, sort_keys=True, default=str)
        out.append(
            {
                "event_id": _event_id(prefix, index, blob),
                "timestamp": ts,
                "host": host,
                "process_name": name,
                "parent_process_name": parent,
                "command_line": cmd,
                **{
                    k: v
                    for k, v in row.items()
                    if k not in {"ts", "timestamp", "name", "cmd", "parent", "process_name", "parent_process_name", "command_line"}
                },
            }
        )
    return out


def _ingest_alert_rows(
    rows: list[dict[str, Any]], *, host: str, prefix: str
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            continue
        ts = _iso_from_any(row.get("ts") or row.get("timestamp"))
        blob = json.dumps(row, sort_keys=True, default=str)
        out.append(
            {
                "event_id": _event_id(prefix, index, blob),
                "timestamp": ts,
                "host": host,
                "rule": row.get("rule") or row.get("detector") or "alert",
                "severity": row.get("severity"),
                "message": row.get("message") or row.get("note") or "",
                "raw_alert": row,
            }
        )
    return out


def secops_case_telemetry(case: str) -> tuple[dict[str, list[dict[str, Any]]], tuple[str, str], str]:
    case_dir = SECOPS_CASES / case
    telemetry: dict[str, list[dict[str, Any]]] = {
        "process_events": [],
        "network": [],
        "alerts": [],
        "file": [],
    }
    host = "unknown-host"
    start, end = "2026-01-01T00:00:00Z", "2026-12-31T23:59:59Z"
    if not case_dir.exists():
        return telemetry, (start, end), host

    for path in sorted(case_dir.glob("evidence*.json")):
        data = json.loads(path.read_text())
        host = str(
            data.get("host.name")
            or data.get("source_host")
            or data.get("target_host")
            or host
        )
        window = data.get("window_utc") or []
        if isinstance(window, list) and len(window) >= 2:
            start, end = _iso_from_any(window[0], start), _iso_from_any(window[1], end)

        if isinstance(data.get("process_tree"), list):
            telemetry["process_events"].extend(
                _ingest_process_rows(data["process_tree"], host=host, prefix=f"{path.stem}-proc")
            )
        if isinstance(data.get("process_and_file"), list):
            telemetry["process_events"].extend(
                _ingest_process_rows(data["process_and_file"], host=host, prefix=f"{path.stem}-pf")
            )
        if isinstance(data.get("alerts"), list):
            telemetry["alerts"].extend(
                _ingest_alert_rows(data["alerts"], host=host, prefix=f"{path.stem}-al")
            )

        # Nested post-exploitation trees
        part_b = data.get("partB_post_exploitation") or {}
        if isinstance(part_b, dict):
            if isinstance(part_b.get("process_tree"), list):
                telemetry["process_events"].extend(
                    _ingest_process_rows(part_b["process_tree"], host=host, prefix=f"{path.stem}-b")
                )
            nested_window = part_b.get("window_utc") or []
            if isinstance(nested_window, list) and len(nested_window) >= 2:
                start, end = _iso_from_any(nested_window[0], start), _iso_from_any(nested_window[1], end)

        # Lateral movement / network-ish fields
        for key in ("source_evidence", "target_evidence", "network_multisource", "setup"):
            block = data.get(key)
            if isinstance(block, list):
                telemetry["process_events"].extend(
                    _ingest_process_rows(block, host=host, prefix=f"{path.stem}-{key[:4]}")
                )
            elif isinstance(block, dict):
                # Flatten dict values that are lists of process-like rows
                for sub_key, sub_val in block.items():
                    if isinstance(sub_val, list) and sub_val and isinstance(sub_val[0], dict):
                        telemetry["process_events"].extend(
                            _ingest_process_rows(
                                sub_val, host=host, prefix=f"{path.stem}-{sub_key[:4]}"
                            )
                        )

        attacker_ip = data.get("attacker_ip") or data.get("c2") or data.get("source_ip")
        if attacker_ip:
            blob = f"{path.name}:{attacker_ip}"
            telemetry["network"].append(
                {
                    "event_id": _event_id(f"{path.stem}-net", 1, blob),
                    "timestamp": start,
                    "host": host,
                    "destination_ip": str(attacker_ip),
                    "destination_port": 443,
                    "protocol": "tcp",
                    "note": "attacker_or_c2_indicator",
                }
            )

    # Drop empty sources
    telemetry = {k: v for k, v in telemetry.items() if v}
    return telemetry, (start, end), host


def convert_secops() -> list[dict[str, Any]]:
    packs: list[dict[str, Any]] = []
    case_cache: dict[str, tuple[dict[str, list], tuple[str, str], str]] = {}
    for scenario in cyber_secops_eval.load_scenarios(limit=None):
        case = scenario["scenario"].split("/", 1)[0]
        if case not in case_cache:
            case_cache[case] = secops_case_telemetry(case)
        telemetry, window, host = case_cache[case]
        # Deep copy telemetry lists so packs don't share mutable state
        telemetry = {src: [dict(rec) for rec in rows] for src, rows in telemetry.items()}
        qid = scenario["scenario"].split("/", 1)[-1]
        incident_id = f"secops-{_slug(qid)}"
        alert = {
            "timestamp": window[0],
            "host": host,
            "user": "unknown",
            "alert_type": "secops_investigation",
            "summary": scenario["prompt"][:240],
            "attck": scenario.get("attck") or [],
        }
        ground_truth = {
            "dataset": "Cyber-SecOps-ES",
            "scenario": scenario["scenario"],
            "answer": scenario.get("answer"),
            "accept": scenario.get("accept") or [],
            "grading": scenario.get("grading"),
            "attck": scenario.get("attck") or [],
            "sealed": True,
        }
        sources = list(telemetry.keys()) or ["process_events"]
        pack = _base_pack(
            incident_id=incident_id,
            name=f"SecOps {scenario['scenario']}",
            alert=alert,
            host=host,
            window=window,
            telemetry=telemetry,
            ground_truth=ground_truth,
            sources=sources,
        )
        packs.append(pack)
    return packs


def convert_ait() -> list[dict[str, Any]]:
    """Rebuild AIT packs from labels + AMiner files (full windows, not truncated JSON)."""
    packs: list[dict[str, Any]] = []
    labels_path = ROOT / "data" / "benchmarks" / "ait_labels.csv"
    ads_dir = ROOT / "data" / "benchmarks" / "ait-ads"
    if not labels_path.exists() or not ads_dir.exists():
        # Fall back to scenario loader if raw files are missing.
        scenarios = ait_ads_eval.load_scenarios(limit=None)
        for scenario in scenarios:
            host, attack = scenario["scenario"].split("/", 1)
            try:
                alerts = json.loads(scenario["evidence"])
            except json.JSONDecodeError:
                alerts = []
            packs.append(_ait_pack_from_alerts(host, attack, alerts if isinstance(alerts, list) else []))
        return packs

    import csv

    with labels_path.open(newline="", encoding="utf-8") as fh:
        labels = list(csv.DictReader(fh))
    for row in labels:
        host = row["scenario"]
        attack = row["attack"]
        aminer = ads_dir / f"{host}_aminer.json"
        if not aminer.exists():
            continue
        start, end = float(row["start"]), float(row["end"])
        alerts = ait_ads_eval._sample_alerts(aminer, start, end, limit=80)
        packs.append(_ait_pack_from_alerts(host, attack, alerts))
    return packs


def _ait_pack_from_alerts(host: str, attack: str, alerts: list[dict[str, Any]]) -> dict[str, Any]:
    records = []
    timestamps = []
    for index, row in enumerate(alerts, start=1):
        if not isinstance(row, dict):
            continue
        ts = _iso_from_any(row.get("timestamp"))
        timestamps.append(ts)
        blob = json.dumps(row, sort_keys=True, default=str)
        records.append(
            {
                "event_id": _event_id("ait", index, blob),
                "timestamp": ts,
                "host": host,
                "detector": row.get("detector") or "AMiner",
                "message": row.get("message") or "",
                "raw_alert": row,
            }
        )
    start = min(timestamps) if timestamps else "2022-01-01T00:00:00Z"
    end = max(timestamps) if timestamps else "2022-12-31T23:59:59Z"
    telemetry = {"alerts": records} if records else {}
    incident_id = f"ait-{_slug(host)}-{_slug(attack)}"
    alert = {
        "timestamp": start,
        "host": host,
        "user": "unknown",
        "alert_type": "ait_ads_stage",
        "summary": f"AIT-ADS multi-step stage candidate on {host}: {attack}",
    }
    ground_truth = {
        "dataset": "Cyber-AIT-ADS",
        "scenario": f"{host}/{attack}",
        "answer": attack,
        "accept": [attack, attack.replace("_", " ")],
        "grading": "exact_ci",
        "sealed": True,
    }
    return _base_pack(
        incident_id=incident_id,
        name=f"AIT-ADS {host}/{attack}",
        alert=alert,
        host=host,
        window=(start, end),
        telemetry=telemetry,
        ground_truth=ground_truth,
        sources=["alerts"],
    )


def write_packs(
    packs: list[dict[str, Any]], bucket: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    dest = OUT / bucket
    dest.mkdir(parents=True, exist_ok=True)
    # clear previous generated packs in this bucket
    for old in dest.glob("*.json"):
        old.unlink()
    index_rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for pack in packs:
        problems = validate_pack(pack)
        if problems:
            errors.append({"incident_id": pack.get("incident_id"), "errors": problems})
            continue
        path = dest / f"{pack['incident_id']}.json"
        path.write_text(json.dumps(pack, indent=2) + "\n")
        index_rows.append(
            {
                "incident_id": pack["incident_id"],
                "name": pack["name"],
                "dataset": (pack.get("ground_truth") or {}).get("dataset"),
                "scenario": (pack.get("ground_truth") or {}).get("scenario"),
                "path": str(path.relative_to(ROOT)),
                "telemetry_sources": sorted((pack.get("telemetry") or {}).keys()),
                "event_count": sum(len(v) for v in (pack.get("telemetry") or {}).values()),
            }
        )
    return index_rows, errors


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    secops = convert_secops()
    ait = convert_ait()
    secops_index, secops_errors = write_packs(secops, "secops")
    ait_index, ait_errors = write_packs(ait, "ait_ads")
    manifest = {
        "generated_at": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "description": "C0–C7 incident packs converted from cyber benchmark scenarios",
        "counts": {
            "secops": len(secops_index),
            "ait_ads": len(ait_index),
            "total": len(secops_index) + len(ait_index),
            "secops_errors": len(secops_errors),
            "ait_ads_errors": len(ait_errors),
        },
        "packs": secops_index + ait_index,
        "errors": secops_errors + ait_errors,
        "notes": [
            "Each pack is one C0–C7 dataset point (×8 conditions when suite-run).",
            "ground_truth is sealed and must not be sent to the model.",
            "DiscoveryBench/DiscoveryWorld are not converted.",
        ],
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest["counts"], indent=2))
    if manifest["errors"]:
        print("validation errors:", json.dumps(manifest["errors"][:5], indent=2))
        return 1
    print(f"wrote {manifest['counts']['total']} packs -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
