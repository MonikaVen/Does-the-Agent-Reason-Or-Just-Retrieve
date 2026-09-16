from __future__ import annotations

import json
from typing import Any


def generate_experiment(spec: dict[str, Any]) -> dict[str, Any]:
    condition = spec["condition"]
    dataset_id = spec["dataset_id"]
    provider = spec.get("provider") or "reference"
    model = spec.get("model") or "reference-investigator-v1"
    budgets = spec.get("budgets") or {
        "max_tool_calls": 12,
        "max_records_per_call": 100,
        "max_runtime_seconds": 300,
    }
    matched = spec.get("matched_run_id")
    seed = int(spec.get("seed") or 42)
    base_url = (spec.get("lab_url") or "http://127.0.0.1:8000").rstrip("/")
    filename = f"experiment_{condition.lower()}_{provider}.py"
    body = {
        "dataset_id": dataset_id,
        "condition": condition,
        "provider": provider,
        "model": model,
        "seed": seed,
        "budgets": budgets,
        "matched_run_id": matched,
    }
    python = f'''#!/usr/bin/env python3
"""Generated C0-C7 experiment. Pins condition, model, dataset, and budgets."""
from __future__ import annotations

import json
import time
import urllib.request

LAB = {base_url!r}
BODY = {json.dumps(body, indent=2)}


def api(method: str, path: str, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(
        LAB + path,
        data=data,
        method=method,
        headers={{"Content-Type": "application/json"}} if payload is not None else {{}},
    )
    with urllib.request.urlopen(req) as response:
        return json.load(response)


def main() -> None:
    run = api("POST", "/api/runs", BODY)
    run_id = run["id"]
    print(f"started {{run_id}} condition={{run['condition']}} provider={provider} model={model}")
    while True:
        detail = api("GET", f"/api/runs/{{run_id}}")
        status = detail["status"]
        print(f"status={{status}} events={{len(detail.get('events') or [])}}")
        if status in {{"completed", "failed"}}:
            report = detail.get("report") or {{}}
            print(json.dumps({{"verdict": report.get("verdict"), "confidence": report.get("confidence"), "error": detail.get("error")}}, indent=2))
            if status == "failed":
                raise SystemExit(1)
            return
        time.sleep(0.5)


if __name__ == "__main__":
    main()
'''
    return {
        "filename": filename,
        "spec": {
            "schema_version": "1.0",
            "lab_url": base_url,
            **body,
        },
        "python": python,
    }
