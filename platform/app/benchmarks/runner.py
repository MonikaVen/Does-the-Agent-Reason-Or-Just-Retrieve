from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

from ..store import ROOT, utcnow
from . import ait_ads_eval, cyber_secops_eval, discoverybench_eval, discoveryworld_eval

Loader = Callable[..., list[dict[str, Any]]]
Runner = Callable[..., dict[str, Any]]


def _summarize(rows: list[dict[str, Any]], model: str) -> list[dict[str, Any]]:
    by_dataset: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_dataset[row["dataset"]].append(row)
    dataset_scores = []
    for dataset, items in by_dataset.items():
        completed = [r for r in items if r["status"] == "completed"]
        mean = round(sum(r["score"] for r in completed) / max(1, len(completed)), 4) if completed else 0.0
        dataset_scores.append(
            {
                "dataset": dataset,
                "model": model,
                "scenarios": len(items),
                "completed": len(completed),
                "mean_score": mean,
            }
        )
    return dataset_scores


def _write_report(report: dict[str, Any], out: Path) -> dict[str, str]:
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "multi-benchmark-report.json"
    md_path = out / "multi-benchmark-report.md"
    json_path.write_text(json.dumps(report, indent=2))
    md_path.write_text(render_markdown(report))
    return {"json": str(json_path), "markdown": str(md_path)}


def run_benchmarks(
    *,
    model: str = "qwen2.5",
    base_url: str = "http://127.0.0.1:11434",
    out_dir: Path | None = None,
    include: list[str] | None = None,
    limit: int | None = 1000,
    checkpoint_every: int = 10,
) -> dict[str, Any]:
    include = include or ["discoverybench", "discoveryworld", "cyber_secops", "ait_ads"]
    loaders: dict[str, Loader] = {
        "discoverybench": discoverybench_eval.load_scenarios,
        "discoveryworld": discoveryworld_eval.load_scenarios,
        "cyber_secops": cyber_secops_eval.load_scenarios,
        "ait_ads": ait_ads_eval.load_scenarios,
    }
    runners: dict[str, Runner] = {
        "discoverybench": discoverybench_eval.run_scenario,
        "discoveryworld": discoveryworld_eval.run_scenario,
        "cyber_secops": cyber_secops_eval.run_scenario,
        "ait_ads": ait_ads_eval.run_scenario,
    }

    out = out_dir or (ROOT / "reports" / "benchmarks")
    out.mkdir(parents=True, exist_ok=True)
    checkpoint_path = out / "multi-benchmark-checkpoint.json"

    # Prefer cyber evidence tasks first, then DiscoveryBench, then DiscoveryWorld fill.
    preferred = [k for k in ["cyber_secops", "ait_ads", "discoverybench", "discoveryworld"] if k in include]
    preferred += [k for k in include if k not in preferred]
    unique: list[tuple[str, dict[str, Any]]] = []
    for key in preferred:
        scenarios = loaders[key](limit=None)
        print(f"benchmark  {key}  available={len(scenarios)}  model={model}", flush=True)
        for scenario in scenarios:
            unique.append((key, scenario))
    print(f"unique  total={len(unique)}", flush=True)

    # If the caller asks for more than the unique inventory, tile with decoding
    # replicas (rep0, rep1, ...) so long runs can estimate variance.
    queue: list[tuple[str, dict[str, Any]]] = []
    target = limit if limit is not None else len(unique)
    if target <= len(unique):
        queue = unique[:target]
    else:
        replica = 0
        while len(queue) < target:
            for key, scenario in unique:
                if len(queue) >= target:
                    break
                cloned = dict(scenario)
                if replica > 0:
                    cloned["scenario"] = f"{scenario.get('scenario')}/rep{replica}"
                    cloned["id"] = f"{scenario.get('id')}/rep{replica}"
                    cloned["replica"] = replica
                else:
                    cloned["replica"] = 0
                queue.append((key, cloned))
            replica += 1
    print(f"queue  total={len(queue)}  limit={limit}  replicas~{max(1, (len(queue) + len(unique) - 1) // max(1, len(unique)))}", flush=True)

    # Resume from checkpoint if present.
    done_ids: set[str] = set()
    rows: list[dict[str, Any]] = []
    if checkpoint_path.exists():
        prior = json.loads(checkpoint_path.read_text())
        if prior.get("model") == model:
            rows = list(prior.get("scenarios") or [])
            done_ids = {f"{r.get('dataset')}::{r.get('scenario')}" for r in rows}
            print(f"resume  checkpoint_rows={len(rows)}", flush=True)

    total = len(queue)
    for idx, (key, scenario) in enumerate(queue, start=1):
        sid = f"{scenario.get('dataset')}::{scenario.get('scenario')}"
        if sid in done_ids:
            continue
        print(f"[{idx}/{total}] run  {scenario['scenario']}", flush=True)
        row = runners[key](scenario, model=model, base_url=base_url)
        print(f"[{idx}/{total}] score {row['score']}  status={row['status']}", flush=True)
        rows.append(row)
        done_ids.add(sid)
        if idx % checkpoint_every == 0 or idx == total:
            partial = {
                "generated_at": utcnow(),
                "model": model,
                "provider": "ollama",
                "limit": limit,
                "queued": total,
                "completed_rows": len(rows),
                "datasets": _summarize(rows, model),
                "scenarios": rows,
            }
            checkpoint_path.write_text(json.dumps(partial, indent=2))
            _write_report(partial, out)
            print(f"checkpoint  rows={len(rows)}/{total}", flush=True)

    report = {
        "generated_at": utcnow(),
        "model": model,
        "provider": "ollama",
        "limit": limit,
        "queued": total,
        "datasets": _summarize(rows, model),
        "scenarios": rows,
    }
    report["files"] = _write_report(report, out)
    checkpoint_path.write_text(json.dumps(report, indent=2))
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Multi-benchmark report",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Model: `{report['provider']}:{report['model']}`",
        f"- Queued: `{report.get('queued', len(report.get('scenarios') or []))}`",
        f"- Completed rows: `{len(report.get('scenarios') or [])}`",
        "",
        "## Dataset scores",
        "",
        "| Model | Dataset | Scenarios | Completed | Mean score |",
        "|---|---|---|---|---|",
    ]
    for row in report.get("datasets") or []:
        lines.append(
            f"| {row['model']} | {row['dataset']} | {row['scenarios']} | {row['completed']} | {row['mean_score']} |"
        )
    lines += [
        "",
        "## Scenario scores",
        "",
        "| Model | Dataset | Scenario | Status | Score | Detail |",
        "|---|---|---|---|---|---|",
    ]
    for row in report.get("scenarios") or []:
        detail = (row.get("detail") or "").replace("|", "/")
        lines.append(
            f"| {row['model']} | {row['dataset']} | {row['scenario']} | {row['status']} | "
            f"{row['score']} | {detail} |"
        )
    lines += [
        "",
        "## Notes",
        "",
        "- DiscoveryBench: token-F1 of hypothesis vs gold answer key (real + synth test).",
        "- DiscoveryWorld: discovery statements plus critical-question probes from theme/difficulty/seed inventory.",
        "- Cyber-SecOps-ES: evidence-grounded extraction against sealed answer key (unsealed locally).",
        "- Cyber-AIT-ADS: attack-stage classification from AMiner alert windows across hosts.",
        "- Confidence is not used; scores are deterministic graders.",
        "- Long runs checkpoint to `multi-benchmark-checkpoint.json` every N scenarios.",
        "",
    ]
    return "\n".join(lines)
