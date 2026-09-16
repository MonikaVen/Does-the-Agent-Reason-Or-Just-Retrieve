from __future__ import annotations

import re
from typing import Any

VERDICTS = {"malicious", "benign", "inconclusive"}
ATTACK_RE = re.compile(r"^T\d{4}(?:\.\d{3})?$")


def validate_report(report: dict[str, Any], known_ids: set[str]) -> dict[str, Any]:
    errors: list[str] = []
    if report.get("verdict") not in VERDICTS:
        errors.append(f"invalid verdict '{report.get('verdict')}'")
    confidence = report.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0 <= float(confidence) <= 1:
        errors.append("confidence must be in [0, 1]")
    if not report.get("summary"):
        errors.append("summary is required")
    cited: list[str] = []
    for item in report.get("supporting_evidence") or []:
        eid = item.get("event_id")
        if eid:
            cited.append(eid)
            if known_ids and eid not in known_ids:
                errors.append(f"supporting evidence {eid} was not observed in this run")
    for stage in report.get("attack_chain") or []:
        tech = stage.get("technique")
        if tech and not ATTACK_RE.match(str(tech)):
            errors.append(f"invalid ATT&CK id {tech}")
        for eid in stage.get("evidence_ids") or []:
            cited.append(eid)
            if known_ids and eid not in known_ids:
                errors.append(f"attack-chain evidence {eid} was not observed in this run")
    if report.get("verdict") in {"malicious", "benign"} and not cited:
        errors.append("factual verdict requires at least one evidence citation")
    return {
        "ok": not errors,
        "errors": errors,
        "cited_evidence": sorted(set(cited)),
        "unsupported_claim_rate": 0.0 if not errors else round(len(errors) / max(1, len(cited) + len(errors)), 2),
    }
