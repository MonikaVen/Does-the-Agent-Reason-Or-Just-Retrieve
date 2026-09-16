from __future__ import annotations

import json
from typing import Any


def generate_experiment(spec: dict[str, Any]) -> dict[str, Any]:
    condition = spec["condition"]
    dataset_id = spec.get("dataset_id") or ""
    provider = spec.get("provider") or "ollama"
    model = spec.get("model") or "llama3.2:1b"
    budgets = spec.get("budgets") or {
        "max_tool_calls": 6,
        "max_records_per_call": 100,
        "max_runtime_seconds": 300,
    }
    matched = spec.get("matched_run_id")
    seed = int(spec.get("seed") or 42)
    pack_path = spec.get("pack_path") or "data/sample_incident.json"
    filename = f"experiment_{condition.lower()}_{provider}.py"
    body = {
        "condition": condition,
        "pack_path": pack_path,
        "dataset_id": dataset_id,
        "provider": provider,
        "model": model,
        "seed": seed,
        "budgets": budgets,
        "matched_run_id": matched,
    }
    python = f'''#!/usr/bin/env python3
"""Generated C0-C7 experiment. Pins condition, model, pack, and budgets."""
from __future__ import annotations

import asyncio
import os

from app.lab import Lab, format_architecture, format_summary

SPEC = {json.dumps(body, indent=4)}


async def main() -> None:
    os.environ.setdefault("LAB_STEP_DELAY", "0")
    lab = Lab()
    lab.set_provider(SPEC["provider"], SPEC["model"])
    dataset = lab.load_pack_file(SPEC["pack_path"])
    print(format_architecture(lab.architecture(SPEC["condition"], SPEC["provider"], dataset["id"])))
    summary = await lab.run_condition(
        SPEC["condition"],
        dataset["id"],
        provider=SPEC["provider"],
        model=SPEC["model"],
        matched_run_id=SPEC["matched_run_id"],
        budgets=SPEC["budgets"],
        seed=SPEC["seed"],
    )
    print(format_summary(summary))
    if summary.get("status") != "completed":
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
'''
    return {
        "filename": filename,
        "spec": {
            "schema_version": "1.0",
            **body,
        },
        "python": python,
    }
