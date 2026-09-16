from __future__ import annotations

from typing import Any


def initial_state(run_id: str, budgets: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "step": 0,
        "hypotheses": [
            {
                "hypothesis_id": "h1",
                "claim": "The alert represents malicious execution.",
                "confidence": 0.5,
            },
            {
                "hypothesis_id": "h2",
                "claim": "The activity is approved administration.",
                "confidence": 0.5,
            },
        ],
        "known_evidence": [],
        "contradicting_evidence": [],
        "unresolved_questions": ["What launched the alerting process, and what happened next?"],
        "entities": {"hosts": [], "users": [], "ips": [], "files": [], "processes": []},
        "timeline": [],
        "knowledge_references": [],
        "action_history": [],
        "budget_state": {
            "tool_calls_used": 0,
            "tool_calls_remaining": budgets.get("max_tool_calls", 12),
            "runtime_ms": 0,
            "model_tokens_used": 0,
        },
        "stop_state": {"stop": False, "reason": ""},
        "state_version": 1,
        "confidence_history": [],
    }


def apply_observation(state: dict[str, Any], observation: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
    next_state = dict(state)
    next_state["step"] = int(state.get("step") or 0) + 1
    next_state["state_version"] = int(state.get("state_version") or 1) + 1
    known = list(state.get("known_evidence") or [])
    entities = {
        "hosts": list((state.get("entities") or {}).get("hosts") or []),
        "users": list((state.get("entities") or {}).get("users") or []),
        "ips": list((state.get("entities") or {}).get("ips") or []),
        "files": list((state.get("entities") or {}).get("files") or []),
        "processes": list((state.get("entities") or {}).get("processes") or []),
    }
    timeline = list(state.get("timeline") or [])
    for record in observation.get("records") or []:
        eid = record.get("evidence_id")
        if eid and eid not in known:
            known.append(eid)
        host = record.get("host")
        if host and host not in entities["hosts"]:
            entities["hosts"].append(host)
        fields = record.get("fields") or {}
        user = fields.get("user")
        if user and user not in entities["users"]:
            entities["users"].append(user)
        ip = fields.get("destination_ip")
        if ip and ip not in entities["ips"]:
            entities["ips"].append(ip)
        path = fields.get("path")
        if path and path not in entities["files"]:
            entities["files"].append(path)
        proc = fields.get("process_name")
        if proc and proc not in entities["processes"]:
            entities["processes"].append(proc)
        timeline.append(
            {
                "timestamp": record.get("timestamp"),
                "evidence_id": eid,
                "source": record.get("source"),
                "summary": _record_summary(record),
            }
        )
    history = list(state.get("action_history") or [])
    history.append(
        {
            "tool": action.get("tool"),
            "arguments": action.get("arguments"),
            "record_count": observation.get("record_count", 0),
        }
    )
    budget = dict(state.get("budget_state") or {})
    budget["tool_calls_used"] = int(budget.get("tool_calls_used") or 0) + 1
    remaining = int(budget.get("tool_calls_remaining") or 0)
    budget["tool_calls_remaining"] = max(0, remaining - 1)
    next_state["known_evidence"] = known
    next_state["entities"] = entities
    next_state["timeline"] = timeline
    next_state["action_history"] = history
    next_state["budget_state"] = budget
    return next_state


def apply_knowledge(state: dict[str, Any], passages: list[dict[str, Any]]) -> dict[str, Any]:
    next_state = dict(state)
    refs = list(state.get("knowledge_references") or [])
    for passage in passages:
        pid = passage.get("passage_id")
        if pid and pid not in refs:
            refs.append(pid)
    next_state["knowledge_references"] = refs
    next_state["state_version"] = int(state.get("state_version") or 1) + 1
    return next_state


def apply_beliefs(state: dict[str, Any], hypotheses: list[dict[str, Any]], question: str | None = None) -> dict[str, Any]:
    next_state = dict(state)
    previous = {item["hypothesis_id"]: item.get("confidence") for item in state.get("hypotheses") or []}
    history = list(state.get("confidence_history") or [])
    for item in hypotheses:
        hid = item["hypothesis_id"]
        history.append(
            {
                "hypothesis_id": hid,
                "previous": previous.get(hid),
                "new": item.get("confidence"),
            }
        )
    next_state["hypotheses"] = hypotheses
    next_state["confidence_history"] = history
    if question:
        next_state["unresolved_questions"] = [question]
    next_state["state_version"] = int(state.get("state_version") or 1) + 1
    return next_state


def mark_stop(state: dict[str, Any], reason: str) -> dict[str, Any]:
    next_state = dict(state)
    next_state["stop_state"] = {"stop": True, "reason": reason}
    return next_state


def _record_summary(record: dict[str, Any]) -> str:
    fields = record.get("fields") or {}
    if fields.get("process_name"):
        parent = fields.get("parent_process_name")
        extra = f" via {parent}" if parent else ""
        return f"{fields.get('process_name')}{extra}"
    if fields.get("destination_ip"):
        return f"egress {fields.get('destination_ip')}:{fields.get('destination_port', '')}"
    if fields.get("path"):
        return f"file {fields.get('path')}"
    if fields.get("key"):
        return f"registry {fields.get('key')}"
    return record.get("source") or "event"
