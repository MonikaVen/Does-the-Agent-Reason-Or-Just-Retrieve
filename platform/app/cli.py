from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from .codegen import generate_experiment
from .conditions import CONDITIONS, condition_ids, get_condition
from .lab import Lab, LabError, SUITE_CONDITIONS, format_architecture, format_event, format_summary
from .llm import PROVIDER_INDEX
from .packs import DATA_KINDS
from .store import ROOT


def _print_event(event: dict[str, Any]) -> None:
    if event.get("kind") in {"stage"}:
        print(f"  {format_event(event)}", flush=True)
        return
    if event.get("kind") in {
        "decision",
        "tool_observation",
        "tool_requested",
        "knowledge_retrieved",
        "service_disabled",
        "report_generated",
        "report_validated",
        "run_completed",
        "run_failed",
        "action_rejected",
    }:
        print(f"  {format_event(event)}", flush=True)


def _lab(verbose: bool) -> Lab:
    return Lab(on_event=_print_event if verbose else None)


def _budgets(args: argparse.Namespace) -> dict[str, int]:
    budgets: dict[str, int] = {}
    if args.tools is not None:
        budgets["max_tool_calls"] = args.tools
    if args.records is not None:
        budgets["max_records_per_call"] = args.records
    return budgets


def cmd_health(args: argparse.Namespace) -> int:
    lab = Lab()
    if args.provider:
        lab.set_provider(args.provider, args.model, args.ollama_url)
    else:
        lab.prefer_ollama()
    print(json.dumps(lab.health(), indent=2))
    return 0


def cmd_conditions(_args: argparse.Namespace) -> int:
    for cid in condition_ids():
        profile = get_condition(cid)
        print(f"{cid}  {profile['name']}")
        print(f"    {profile['summary']}")
    return 0


def cmd_architecture(args: argparse.Namespace) -> int:
    lab = Lab()
    dataset = None
    if args.pack or args.dataset:
        dataset = lab.ensure_dataset(args.pack, args.dataset)
    provider = args.provider or lab.store.get_setting("provider", "ollama")
    print(format_architecture(lab.architecture(args.condition, provider, dataset["id"] if dataset else None)))
    return 0


def cmd_load(args: argparse.Namespace) -> int:
    lab = Lab()
    if args.kind:
        if not args.file:
            raise LabError("--file is required with --kind")
        payload = json.loads(Path(args.file).read_text())
        dataset = lab.merge_kind(args.kind, payload, dataset_id=args.dataset)
    elif args.pack:
        dataset = lab.load_pack_file(args.pack)
    else:
        dataset = lab.seed_sample() or lab.store.list_datasets()[0]
    passport = dataset_brief(dataset)
    print(json.dumps(passport, indent=2))
    return 0


def dataset_brief(dataset: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in dataset.items() if k != "pack"}


def cmd_key(args: argparse.Namespace) -> int:
    lab = Lab()
    lab.set_secret(args.name, args.api_key or "", args.ollama_url)
    public = next((item for item in lab.store.list_secret_public() if item["provider"] == args.name), None)
    print(json.dumps(public or {"provider": args.name, "status": "saved"}, indent=2))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    lab = _lab(not args.quiet)
    if args.provider:
        lab.set_provider(args.provider, args.model, args.ollama_url)
    else:
        lab.prefer_ollama()
        if args.model:
            lab.store.set_setting("model", args.model)
    dataset = lab.ensure_dataset(args.pack, args.dataset)
    print(format_architecture(lab.architecture(args.condition, args.provider, dataset["id"])))
    print(f"dataset {dataset['id']}  {dataset['incident_id']}", flush=True)
    summary = asyncio.run(
        lab.run_condition(
            args.condition,
            dataset["id"],
            provider=args.provider,
            model=args.model,
            matched_run_id=args.matched_run,
            budgets=_budgets(args),
            seed=args.seed,
        )
    )
    print(format_summary(summary))
    if summary.get("summary"):
        print(summary["summary"])
    return 0 if summary.get("status") == "completed" else 1


def cmd_suite(args: argparse.Namespace) -> int:
    lab = _lab(not args.quiet)
    if args.provider:
        lab.set_provider(args.provider, args.model, args.ollama_url)
    else:
        lab.prefer_ollama()
        if args.model:
            lab.store.set_setting("model", args.model)
    dataset = lab.ensure_dataset(args.pack, args.dataset)
    conditions = SUITE_CONDITIONS if args.conditions == "all" else [item.strip().upper() for item in args.conditions.split(",")]
    for cid in conditions:
        if cid not in CONDITIONS:
            raise LabError(f"unknown condition {cid}")
    print(f"suite  dataset={dataset['id']}  {dataset['incident_id']}", flush=True)
    print(f"model  {lab.store.get_setting('provider')} {lab.store.get_setting('model')}", flush=True)
    report_dir = Path(args.out) if args.out else (ROOT / "reports")
    suite = asyncio.run(
        lab.run_suite(
            dataset["id"],
            provider=args.provider,
            model=args.model,
            conditions=conditions,
            budgets=_budgets(args),
            seed=args.seed,
            report_dir=report_dir,
        )
    )
    print()
    for row in suite["runs"]:
        print(format_summary(row))
    print()
    print(f"report  {suite['files']['markdown']}")
    print(f"json    {suite['files']['json']}")
    failed = any(row.get("status") == "failed" for row in suite["runs"])
    return 1 if failed else 0


def cmd_report(args: argparse.Namespace) -> int:
    path = Path(args.out) / "experiment-report.md" if args.out else ROOT / "reports" / "experiment-report.md"
    if not path.exists():
        raise LabError("No experiment report yet. Run: python -m app suite")
    sys.stdout.write(path.read_text())
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    lab = Lab()
    dataset = lab.ensure_dataset(args.pack, args.dataset)
    generated = generate_experiment(
        {
            "condition": args.condition,
            "dataset_id": dataset["id"],
            "pack_path": str(Path(args.pack).resolve()) if args.pack else str((ROOT / "data" / "sample_incident.json").resolve()),
            "provider": args.provider or lab.store.get_setting("provider", "ollama"),
            "model": args.model or lab.store.get_setting("model") or PROVIDER_INDEX["ollama"]["default_model"],
            "matched_run_id": args.matched_run,
            "seed": args.seed,
            "budgets": _budgets(args),
        }
    )
    if args.write:
        dest = Path(args.write)
        dest.write_text(generated["python"])
        print(dest)
    else:
        sys.stdout.write(generated["python"])
    return 0


def _common_flags() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--quiet", action="store_true", help="hide per-event trajectory")
    common.add_argument("--provider", choices=list(PROVIDER_INDEX), help="model provider (default: ollama if reachable)")
    common.add_argument("--model", help="model name, e.g. llama3.2:1b")
    common.add_argument("--ollama-url", default=os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434"))
    common.add_argument("--pack", help="incident pack JSON")
    common.add_argument("--dataset", help="existing dataset id")
    common.add_argument("--tools", type=int, help="max tool calls")
    common.add_argument("--records", type=int, help="max records per tool call")
    common.add_argument("--seed", type=int, default=42)
    common.add_argument("--out", help="directory for experiment-report.md/json")
    return common


def build_parser() -> argparse.ArgumentParser:
    common = _common_flags()
    parser = argparse.ArgumentParser(
        prog="python -m app",
        description="Run C0–C7 investigation experiments from the terminal. No frontend.",
        parents=[common],
    )
    sub = parser.add_subparsers(dest="command")

    health = sub.add_parser("health", parents=[common], help="probe Ollama and print lab status")
    health.set_defaults(func=cmd_health)

    conditions = sub.add_parser("conditions", parents=[common], help="list C0–C7")
    conditions.set_defaults(func=cmd_conditions)

    arch = sub.add_parser("architecture", parents=[common], help="print enabled/disabled services for a condition")
    arch.add_argument("condition", choices=list(CONDITIONS), nargs="?", default="C3")
    arch.set_defaults(func=cmd_architecture)

    load = sub.add_parser("load", parents=[common], help="load a full pack or one typed part")
    load.add_argument("--kind", choices=[item["id"] for item in DATA_KINDS])
    load.add_argument("--file", help="JSON file for --kind")
    load.set_defaults(func=cmd_load)

    key = sub.add_parser("key", parents=[common], help="save a cloud API key or Ollama URL")
    key.add_argument("name", choices=[name for name in PROVIDER_INDEX if name != "reference"])
    key.add_argument("--api-key", default="")
    key.set_defaults(func=cmd_key)

    run = sub.add_parser("run", parents=[common], help="run one condition")
    run.add_argument("condition", choices=list(CONDITIONS))
    run.add_argument("--matched-run", help="completed C3 run id (C5 only)")
    run.set_defaults(func=cmd_run)

    suite = sub.add_parser("suite", parents=[common], help="run C0–C7 and write the experiment report")
    suite.add_argument("--conditions", default="all", help="comma-separated list, or 'all'")
    suite.set_defaults(func=cmd_suite)

    report = sub.add_parser("report", parents=[common], help="print the latest experiment-report.md")
    report.set_defaults(func=cmd_report)

    generate = sub.add_parser("generate", parents=[common], help="print a pinned in-process runner script")
    generate.add_argument("condition", choices=list(CONDITIONS), nargs="?", default="C3")
    generate.add_argument("--matched-run")
    generate.add_argument("--write", help="write the script to this path")
    generate.set_defaults(func=cmd_generate)

    parser.set_defaults(func=None, conditions="all")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.func is None or args.command is None:
        parser.print_help()
        return 2
    try:
        return args.func(args)
    except LabError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
