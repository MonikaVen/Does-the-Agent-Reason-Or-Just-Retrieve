#!/usr/bin/env python3
"""Run C0–C7 suite on every converted cyber pack; checkpoint + aggregate.

Example:
  LAB_STEP_DELAY=0 python3 scripts/run_converted_packs_suite.py \\
    --provider ollama --model qwen2.5:3b --tools 4 --quiet
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import traceback
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.lab import Lab  # noqa: E402

CONDITIONS = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"]


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def pack_result_path(out_dir: Path, incident_id: str) -> Path:
    return out_dir / "packs" / f"{incident_id}.json"


def summarize_suite(suite: dict[str, Any], pack_meta: dict[str, Any]) -> dict[str, Any]:
    runs = []
    for row in suite.get("runs") or []:
        runs.append(
            {
                "condition": row.get("condition"),
                "status": row.get("status"),
                "error": row.get("error"),
                "verdict": row.get("verdict"),
                "confidence": row.get("confidence"),
                "tool_observations": row.get("tool_observations"),
                "knowledge_retrievals": row.get("knowledge_retrievals"),
                "run_id": row.get("run_id"),
                "started_at": row.get("started_at"),
                "completed_at": row.get("completed_at"),
            }
        )
    return {
        "incident_id": suite.get("incident_id") or pack_meta.get("incident_id"),
        "dataset": pack_meta.get("dataset"),
        "scenario": pack_meta.get("scenario"),
        "path": pack_meta.get("path"),
        "provider": suite.get("provider"),
        "model": suite.get("model"),
        "generated_at": suite.get("generated_at") or utcnow(),
        "runs": runs,
        "completed": sum(1 for r in runs if r.get("status") == "completed"),
        "skipped": sum(1 for r in runs if r.get("status") == "skipped"),
        "failed": sum(1 for r in runs if r.get("status") == "failed"),
    }


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    by_cond: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for pack in results:
        for run in pack.get("runs") or []:
            by_cond[run["condition"]].append({**run, "incident_id": pack["incident_id"], "dataset": pack.get("dataset")})

    table = []
    for condition in CONDITIONS:
        rows = by_cond.get(condition) or []
        completed = [r for r in rows if r.get("status") == "completed"]
        confs = [float(r["confidence"]) for r in completed if r.get("confidence") is not None]
        verdicts = Counter((r.get("verdict") or "unknown") for r in completed)
        tools = [int(r.get("tool_observations") or 0) for r in completed]
        kb = [int(r.get("knowledge_retrievals") or 0) for r in completed]
        mean_conf = (sum(confs) / len(confs)) if confs else None
        median_conf = sorted(confs)[len(confs) // 2] if confs else None
        table.append(
            {
                "condition": condition,
                "n": len(rows),
                "completed": len(completed),
                "skipped": sum(1 for r in rows if r.get("status") == "skipped"),
                "failed": sum(1 for r in rows if r.get("status") == "failed"),
                "mean_confidence": round(mean_conf, 3) if mean_conf is not None else None,
                "median_confidence": round(median_conf, 3) if median_conf is not None else None,
                "mean_tools": round(sum(tools) / len(tools), 2) if tools else None,
                "mean_kb": round(sum(kb) / len(kb), 2) if kb else None,
                "verdicts": dict(verdicts),
            }
        )

    return {
        "generated_at": utcnow(),
        "packs_total": len(results),
        "condition_runs": sum(len(p.get("runs") or []) for p in results),
        "completed_runs": sum(p.get("completed", 0) for p in results),
        "skipped_runs": sum(p.get("skipped", 0) for p in results),
        "failed_runs": sum(p.get("failed", 0) for p in results),
        "by_dataset": dict(Counter(p.get("dataset") or "unknown" for p in results)),
        "table": table,
        "model": next((p.get("model") for p in results if p.get("model")), None),
        "provider": next((p.get("provider") for p in results if p.get("provider")), None),
    }


def render_markdown(agg: dict[str, Any]) -> str:
    lines = [
        "# C0–C7 converted-pack suite",
        "",
        f"Generated: `{agg['generated_at']}`",
        f"Model: `{agg.get('provider')}:{agg.get('model')}`",
        f"Packs: **{agg['packs_total']}** · condition-runs: **{agg['condition_runs']}** "
        f"(completed {agg['completed_runs']}, skipped {agg['skipped_runs']}, failed {agg['failed_runs']})",
        "",
        "| Condition | n | Completed | Skipped | Failed | Mean conf. | Median conf. | Mean tools | Mean KB | Top verdicts |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in agg["table"]:
        verdicts = row.get("verdicts") or {}
        top = ", ".join(f"{k}={v}" for k, v in sorted(verdicts.items(), key=lambda kv: (-kv[1], kv[0])))
        mean_c = f"{row['mean_confidence']:.3f}".replace(".", ",") if row.get("mean_confidence") is not None else "—"
        med_c = f"{row['median_confidence']:.3f}".replace(".", ",") if row.get("median_confidence") is not None else "—"
        mean_t = "—" if row.get("mean_tools") is None else f"{row['mean_tools']:.2f}".replace(".", ",")
        mean_k = "—" if row.get("mean_kb") is None else f"{row['mean_kb']:.2f}".replace(".", ",")
        lines.append(
            f"| {row['condition']} | {row['n']} | {row['completed']} | {row['skipped']} | {row['failed']} | "
            f"{mean_c} | {med_c} | {mean_t} | {mean_k} | {top or '—'} |"
        )
    lines.append("")
    lines.append("Confidence uses a comma decimal (paper style). Source: converted SecOps-ES + AIT-ADS packs.")
    lines.append("")
    return "\n".join(lines)


def write_aggregate(out_dir: Path) -> dict[str, Any]:
    results = []
    for path in sorted((out_dir / "packs").glob("*.json")):
        results.append(json.loads(path.read_text()))
    agg = aggregate(results)
    (out_dir / "aggregate.json").write_text(json.dumps(agg, indent=2) + "\n")
    (out_dir / "c0c7-table.md").write_text(render_markdown(agg))
    # Also mirror primary experiment-report style for the canvas/PR consumers.
    (out_dir / "experiment-report.md").write_text(render_markdown(agg))
    (out_dir / "experiment-report.json").write_text(json.dumps(agg, indent=2) + "\n")
    return agg


async def run_one(
    lab: Lab,
    pack_meta: dict[str, Any],
    *,
    provider: str,
    model: str,
    tools: int | None,
    records: int | None,
    seed: int,
    quiet: bool,
) -> dict[str, Any]:
    dataset = lab.load_pack_file(pack_meta["path"])
    budgets: dict[str, Any] = {}
    if tools is not None:
        budgets["max_tool_calls"] = tools
    if records is not None:
        budgets["max_records_per_call"] = records
    if not quiet:
        print(f"suite  {pack_meta['incident_id']}  ({pack_meta.get('dataset')})", flush=True)
    suite = await lab.run_suite(
        dataset["id"],
        provider=provider,
        model=model,
        budgets=budgets or None,
        seed=seed,
        report_dir=None,
    )
    return summarize_suite(suite, pack_meta)


async def main_async(args: argparse.Namespace) -> int:
    manifest = load_manifest(Path(args.manifest))
    packs = list(manifest["packs"])
    if args.datasets:
        wanted = {item.strip() for item in args.datasets.split(",") if item.strip()}
        packs = [p for p in packs if (p.get("dataset") or "") in wanted]
    if args.limit and args.limit > 0:
        packs = packs[: args.limit]
    out_dir = Path(args.out)
    (out_dir / "packs").mkdir(parents=True, exist_ok=True)

    pending = []
    for meta in packs:
        dest = pack_result_path(out_dir, meta["incident_id"])
        if args.resume and dest.exists() and not args.force:
            continue
        pending.append(meta)

    workers = max(1, int(args.workers))
    print(
        json.dumps(
            {
                "total_packs": len(packs),
                "pending": len(pending),
                "already_done": len(packs) - len(pending),
                "provider": args.provider,
                "model": args.model,
                "tools": args.tools,
                "workers": workers,
                "out": str(out_dir),
            },
            indent=2,
        ),
        flush=True,
    )

    # One Lab/SQLite per worker — sqlite connections are not share-safe across tasks.
    queue: asyncio.Queue[tuple[int, dict[str, Any]] | None] = asyncio.Queue()
    for index, meta in enumerate(pending, start=1):
        queue.put_nowait((index, meta))
    for _ in range(workers):
        queue.put_nowait(None)

    failures: list[dict[str, Any]] = []
    failures_lock = asyncio.Lock()
    progress_lock = asyncio.Lock()
    done_count = 0

    async def worker(worker_id: int) -> None:
        nonlocal done_count
        lab = Lab(db_path=out_dir / f"lab-w{worker_id}.sqlite3")
        while True:
            item = await queue.get()
            if item is None:
                return
            index, meta = item
            started = utcnow()
            print(
                f"[w{worker_id} {index}/{len(pending)}] {meta['incident_id']} start {started}",
                flush=True,
            )
            try:
                summary = await run_one(
                    lab,
                    meta,
                    provider=args.provider,
                    model=args.model,
                    tools=args.tools,
                    records=args.records,
                    seed=args.seed,
                    quiet=args.quiet,
                )
                pack_result_path(out_dir, meta["incident_id"]).write_text(
                    json.dumps(summary, indent=2) + "\n"
                )
                print(
                    f"[w{worker_id} {index}/{len(pending)}] {meta['incident_id']} "
                    f"done completed={summary['completed']} failed={summary['failed']}",
                    flush=True,
                )
            except Exception as exc:  # noqa: BLE001 — keep batch alive
                async with failures_lock:
                    failures.append({"incident_id": meta["incident_id"], "error": str(exc)})
                err_path = out_dir / "packs" / f"{meta['incident_id']}.error.json"
                err_path.write_text(
                    json.dumps(
                        {
                            "incident_id": meta["incident_id"],
                            "error": str(exc),
                            "traceback": traceback.format_exc(),
                            "at": utcnow(),
                        },
                        indent=2,
                    )
                    + "\n"
                )
                print(
                    f"[w{worker_id} {index}/{len(pending)}] {meta['incident_id']} ERROR {exc}",
                    flush=True,
                )
            async with progress_lock:
                done_count += 1
                agg = write_aggregate(out_dir)
                print(
                    f"progress done={done_count}/{len(pending)} "
                    f"packs_on_disk={agg['packs_total']} "
                    f"runs={agg['completed_runs']}/{agg['condition_runs']}",
                    flush=True,
                )

    await asyncio.gather(*(worker(i + 1) for i in range(workers)))

    agg = write_aggregate(out_dir)
    (out_dir / "failures.json").write_text(json.dumps(failures, indent=2) + "\n")
    print(render_markdown(agg), flush=True)
    print(f"wrote {out_dir / 'c0c7-table.md'}", flush=True)
    return 0 if not failures else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        default=str(ROOT / "data" / "packs" / "manifest.json"),
    )
    parser.add_argument(
        "--out",
        default=str(ROOT / "reports" / "c0c7-converted"),
    )
    parser.add_argument("--provider", default="ollama")
    parser.add_argument("--model", default="qwen2.5:3b")
    parser.add_argument("--tools", type=int, default=4, help="max tool calls per condition")
    parser.add_argument("--records", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--workers", type=int, default=1, help="parallel pack suites")
    parser.add_argument("--limit", type=int, default=0, help="optional pack cap for smoke runs")
    parser.add_argument(
        "--datasets",
        default="",
        help="Comma-separated dataset filters (e.g. SOC-AgentBench,ExCyTIn-Bench)",
    )
    parser.add_argument("--resume", action="store_true", default=True)
    parser.add_argument("--no-resume", action="store_false", dest="resume")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--quiet", action="store_true", default=True)
    args = parser.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
