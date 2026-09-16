from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .store import ROOT, utcnow


def summarize_run(run: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    report = run.get("report") or {}
    kinds = [event["kind"] for event in events]
    tools = [
        (event.get("payload") or {}).get("tool")
        for event in events
        if event["kind"] in {"tool_requested", "tool_observation"}
    ]
    tools = [name for name in tools if name]
    evidence = report.get("supporting_evidence") or []
    return {
        "run_id": run.get("id"),
        "condition": run.get("condition"),
        "status": run.get("status"),
        "error": run.get("error"),
        "model": ((run.get("manifest") or {}).get("model_profile")),
        "verdict": report.get("verdict"),
        "confidence": report.get("confidence"),
        "summary": report.get("summary"),
        "evidence_ids": [item.get("event_id") for item in evidence if item.get("event_id")],
        "event_count": len(events),
        "tool_observations": kinds.count("tool_observation"),
        "knowledge_retrievals": kinds.count("knowledge_retrieved"),
        "tools": tools,
        "started_at": run.get("started_at"),
        "completed_at": run.get("completed_at"),
        "validation": ((run.get("manifest") or {}).get("validation")),
    }


def render_markdown(suite: dict[str, Any]) -> str:
    lines = [
        f"# Experiment report",
        "",
        f"- Generated: `{suite['generated_at']}`",
        f"- Incident: `{suite['incident_id']}`",
        f"- Model: `{suite['provider']}:{suite['model']}`",
        f"- Dataset: `{suite['dataset_id']}`",
        "",
        "## Results",
        "",
        "| Condition | Status | Verdict | Confidence | Evidence IDs | Tool observations | Knowledge |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in suite["runs"]:
        evidence = ", ".join(row.get("evidence_ids") or []) or "—"
        lines.append(
            f"| {row['condition']} | {row['status']} | {row.get('verdict') or '—'} | "
            f"{row.get('confidence') if row.get('confidence') is not None else '—'} | `{evidence}` | "
            f"{row.get('tool_observations', 0)} | {row.get('knowledge_retrievals', 0)} |"
        )
    completed = [row for row in suite["runs"] if row.get("status") == "completed"]
    failed = [row for row in suite["runs"] if row.get("status") == "failed"]
    skipped = [row for row in suite["runs"] if row.get("status") == "skipped"]
    searched = [row for row in completed if row.get("tool_observations")]
    knowledge = [row for row in completed if row.get("knowledge_retrievals")]
    lines += [
        "",
        "## Setup",
        "",
        "Local Ollama was the model gateway. The reference investigator was not used as a silent fallback. "
        "Disabled interfaces returned `SERVICE_DISABLED`. Knowledge passages were not treated as evidence IDs. "
        "Ground truth stayed sealed.",
        "",
        f"- Completed: {len(completed)}",
        f"- Failed: {len(failed)}",
        f"- Skipped: {len(skipped)}",
        f"- Conditions that observed telemetry: {', '.join(row['condition'] for row in searched) or 'none'}",
        f"- Conditions that retrieved knowledge: {', '.join(row['condition'] for row in knowledge) or 'none'}",
        "",
        "## Notes",
        "",
    ]
    for row in suite["runs"]:
        lines.append(f"### {row['condition']}")
        if row.get("error"):
            lines.append(f"Failed: {row['error']}")
        else:
            lines.append(row.get("summary") or "No summary.")
            if row.get("tools"):
                lines.append(f"Tools: {', '.join(row['tools'])}")
            validation = row.get("validation") or {}
            if validation.get("errors"):
                lines.append("Validator: " + "; ".join(validation["errors"]))
        lines.append("")
    lines.append("## Reading the matrix")
    lines.append("")
    lines.append(
        "C0/C1 cannot search telemetry. C2 searches without a knowledge service. "
        "C3 is the full adaptive loop. C4 uses a fixed query pack instead of agent-chosen tools. "
        "C5 receives C3's evidence without C3's search order. C6 is given oracle evidence; C7 is given an oracle plan. "
        "A small local model may stop early, cite poorly, or return inconclusive after validation — "
        "that is a measured outcome, not a reason to swap in the reference investigator."
    )
    return "\n".join(lines) + "\n"


def write_report(suite: dict[str, Any], directory: Path | None = None) -> dict[str, str]:
    out = directory or (ROOT / "reports")
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "experiment-report.json"
    md_path = out / "experiment-report.md"
    json_path.write_text(json.dumps(suite, indent=2))
    md_path.write_text(render_markdown(suite))
    return {"json": str(json_path), "markdown": str(md_path)}
