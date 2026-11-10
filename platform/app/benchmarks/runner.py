from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from ..store import ROOT, utcnow
from . import ait_ads_eval, cyber_secops_eval, discoverybench_eval, discoveryworld_eval


def run_benchmarks(
    *,
    model: str = "qwen2.5",
    base_url: str = "http://127.0.0.1:11434",
    out_dir: Path | None = None,
    include: list[str] | None = None,
) -> dict[str, Any]:
    include = include or ["discoverybench", "discoveryworld", "cyber_secops", "ait_ads"]
    loaders = {
        "discoverybench": discoverybench_eval.load_scenarios,
        "discoveryworld": discoveryworld_eval.load_scenarios,
        "cyber_secops": cyber_secops_eval.load_scenarios,
        "ait_ads": ait_ads_eval.load_scenarios,
    }
    runners = {
        "discoverybench": discoverybench_eval.run_scenario,
        "discoveryworld": discoveryworld_eval.run_scenario,
        "cyber_secops": cyber_secops_eval.run_scenario,
        "ait_ads": ait_ads_eval.run_scenario,
    }

    rows: list[dict[str, Any]] = []
    for key in include:
        scenarios = loaders[key]()
        print(f"benchmark  {key}  scenarios={len(scenarios)}  model={model}", flush=True)
        for scenario in scenarios:
            print(f"  run  {scenario['scenario']}", flush=True)
            row = runners[key](scenario, model=model, base_url=base_url)
            print(f"  score {row['score']}  status={row['status']}", flush=True)
            rows.append(row)

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

    report = {
        "generated_at": utcnow(),
        "model": model,
        "provider": "ollama",
        "datasets": dataset_scores,
        "scenarios": rows,
    }
    out = out_dir or (ROOT / "reports" / "benchmarks")
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "multi-benchmark-report.json"
    md_path = out / "multi-benchmark-report.md"
    json_path.write_text(json.dumps(report, indent=2))
    md_path.write_text(render_markdown(report))
    report["files"] = {"json": str(json_path), "markdown": str(md_path)}
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Multi-benchmark report",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Model: `{report['provider']}:{report['model']}`",
        "",
        "## Dataset scores",
        "",
        "| Model | Dataset | Scenarios | Completed | Mean score |",
        "|---|---|---|---|---|",
    ]
    for row in report["datasets"]:
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
    for row in report["scenarios"]:
        detail = (row.get("detail") or "").replace("|", "/")
        lines.append(
            f"| {row['model']} | {row['dataset']} | {row['scenario']} | {row['status']} | "
            f"{row['score']} | {detail} |"
        )
    lines += [
        "",
        "## Notes",
        "",
        "- DiscoveryBench: token-F1 of hypothesis vs gold answer key.",
        "- DiscoveryWorld: keyword coverage of critical hypotheses from Easy scenarios (offline observation evidence).",
        "- Cyber-SecOps-ES: evidence-grounded extraction against sealed answer key (unsealed locally).",
        "- Cyber-AIT-ADS: attack-stage classification from AMiner alert windows (russellmitchell).",
        "- Confidence is not used; scores are deterministic graders.",
        "",
    ]
    return "\n".join(lines)
