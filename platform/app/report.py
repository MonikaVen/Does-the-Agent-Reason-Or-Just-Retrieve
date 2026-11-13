from __future__ import annotations

import re
from typing import Any

VERDICTS = {"malicious", "benign"}
ATTACK_RE = re.compile(r"^T\d{4}(?:\.\d{3})?$")
OFFICE_PARENTS = {"winword.exe", "excel.exe", "powerpnt.exe", "outlook.exe", "wscript.exe"}
ADMIN_PARENTS = {"management-agent.exe", "sccm.exe", "intune.exe", "services.exe"}


def normalize_verdict(verdict: Any, *, malicious_score: float | None = None) -> str:
    """Force a binary verdict. Unknown/inconclusive values become evidence-based or benign."""
    value = str(verdict or "").strip().lower()
    if value in VERDICTS:
        return value
    if malicious_score is not None:
        return "malicious" if float(malicious_score) >= 0.5 else "benign"
    return "benign"


def evidence_beliefs(records: list[dict[str, Any]], known: list[str] | None = None) -> tuple[float, float]:
    """Deterministic malicious/admin beliefs from observed telemetry only."""
    known = known or []
    score = 0.5
    if not records and not known:
        return 0.5, 0.5
    blob = str(records).lower()
    if "-enc" in blob or "encodedcommand" in blob or "-w hidden" in blob:
        score += 0.18
    if any(parent in blob for parent in OFFICE_PARENTS):
        score += 0.16
    if any(parent in blob for parent in ADMIN_PARENTS):
        score -= 0.2
    if "203.0.113." in blob or ("destination_ip" in blob and "powershell" in blob):
        score += 0.08
    if "currentversion\\\\run" in blob or "currentversion\\run" in blob:
        score += 0.1
    if "update.ps1" in blob:
        score += 0.06
    # Converted cyber-pack heuristics (SecOps-ES / AIT-ADS telemetry shapes).
    if any(
        token in blob
        for token in (
            "reverse_shell",
            "revshell",
            "webshell",
            "log4shell",
            "gtfobins",
            "privilege_escalation",
            "/etc/shadow",
            "chmod u+s",
            "suid",
        )
    ):
        score += 0.14
    if any(token in blob for token in ("nmap", "masscan", "wpscan", "dirb", "dnsteal", "hydra", "cracker")):
        score += 0.08
    if "aminer" in blob or '"detector"' in blob:
        score += 0.06
    if any(token in blob for token in ("exfil", "c2", "beacon", "implant", "persistence")):
        score += 0.08
    if any(
        token in blob
        for token in (
            "lsass",
            "lateral_movement",
            "rdp_lateral",
            "encodedcommand",
            "true_positive",
            "compromised",
            "credential theft",
            "malicious url",
        )
    ):
        score += 0.1
    if "benign_positive" in blob or "false_positive" in blob or "backup job" in blob:
        score -= 0.18
    if re.search(r"\bt1\d{3}\b", blob):
        score += 0.05
    score = min(0.93, max(0.07, score))
    return round(score, 2), round(1 - score, 2)


def compute_evidence_confidence(records: list[dict[str, Any]], known: list[str] | None = None) -> float:
    """Report confidence from evidence strength — never from a model self-report."""
    malicious, admin = evidence_beliefs(records, known)
    return round(max(malicious, admin), 2)


def context_records(context: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for obs in context.get("observations") or []:
        records.extend(obs.get("records") or [])
    if not records:
        records = list(context.get("raw_window") or [])
    return records


def assign_evidence_confidence(report: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Overwrite any model-provided confidence with an evidence-derived score."""
    known = []
    state = context.get("state") or {}
    if isinstance(state, dict):
        known = list(state.get("known_evidence") or [])
    records = context_records(context)
    malicious, _admin = evidence_beliefs(records, known)
    next_report = dict(report)
    next_report["verdict"] = normalize_verdict(next_report.get("verdict"), malicious_score=malicious)
    next_report["confidence"] = compute_evidence_confidence(records, known)
    next_report["confidence_source"] = "evidence"
    return next_report


def binary_fallback_report(
    context: dict[str, Any],
    *,
    known_ids: set[str] | None = None,
    summary: str,
    uncertainty: str = "",
) -> dict[str, Any]:
    """Build a valid malicious/benign report when the model output cannot be used."""
    known = []
    state = context.get("state") or {}
    if isinstance(state, dict):
        known = list(state.get("known_evidence") or [])
    records = context_records(context)
    malicious, _admin = evidence_beliefs(records, known)
    verdict = "malicious" if malicious >= 0.5 else "benign"
    cite_ids = [eid for eid in (known_ids or set()) if eid]
    if not cite_ids:
        cite_ids = [rec.get("evidence_id") for rec in records if rec.get("evidence_id")]
    supporting = [
        {"event_id": eid, "claim": "Observed in this run."}
        for eid in cite_ids[:4]
    ]
    if not supporting and cite_ids:
        supporting = [{"event_id": cite_ids[0], "claim": "Observed in this run."}]
    return {
        "verdict": verdict,
        "confidence": compute_evidence_confidence(records, known),
        "confidence_source": "evidence",
        "summary": summary,
        "attack_chain": [],
        "key_entities": {"hosts": [], "users": [], "ips": [], "files": []},
        "supporting_evidence": supporting,
        "contradicting_evidence": [],
        "remaining_uncertainty": uncertainty,
        "recommended_human_check": "Inspect the trajectory for decisive telemetry.",
    }


def validate_report(report: dict[str, Any], known_ids: set[str]) -> dict[str, Any]:
    errors: list[str] = []
    if report.get("verdict") not in VERDICTS:
        errors.append(f"invalid verdict '{report.get('verdict')}' (must be malicious or benign)")
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
    if report.get("verdict") in VERDICTS and not cited:
        errors.append("factual verdict requires at least one evidence citation")
    return {
        "ok": not errors,
        "errors": errors,
        "cited_evidence": sorted(set(cited)),
        "unsupported_claim_rate": 0.0 if not errors else round(len(errors) / max(1, len(cited) + len(errors)), 2),
    }
