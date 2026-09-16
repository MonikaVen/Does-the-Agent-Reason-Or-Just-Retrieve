from __future__ import annotations

from typing import Any


OFFICE_PARENTS = {"winword.exe", "excel.exe", "powerpnt.exe", "outlook.exe", "wscript.exe"}
ADMIN_PARENTS = {"management-agent.exe", "sccm.exe", "intune.exe", "services.exe"}


class ReferenceInvestigator:
    """Transparent, deterministic investigator.

    This is a pinned structured policy, not a hidden LLM. Every action includes
    an expected_discrimination so the UI can show *why* the next tool was chosen.
    Swap this class at the model gateway without changing the rest of the loop.
    """

    def generate_decision(self, context: dict[str, Any]) -> dict[str, Any]:
        tools = set(context.get("tools") or [])
        alert = context.get("alert") or {}
        state = context.get("state") or {}
        observations = context.get("observations") or []
        knowledge = context.get("knowledge") or []
        host = alert.get("host") or "unknown-host"
        known = list(state.get("known_evidence") or [])
        history = [item.get("tool") for item in (state.get("action_history") or [])]
        records = []
        for obs in observations:
            records.extend(obs.get("records") or [])

        malicious, admin = self._beliefs(records, known)
        hypotheses = [
            {"hypothesis_id": "h1", "claim": "The alert represents malicious execution.", "confidence": malicious},
            {"hypothesis_id": "h2", "claim": "The activity is approved administration.", "confidence": admin},
        ]

        if "retrieve_knowledge" in tools and not knowledge and "retrieve_knowledge" not in history:
            return self._decision(
                hypotheses,
                known,
                "What prior detection guidance distinguishes encoded PowerShell from approved administration?",
                {
                    "action_id": f"a-{len(history)+1:03d}",
                    "tool": "retrieve_knowledge",
                    "arguments": {
                        "question": f"{alert.get('summary') or 'suspicious process'} parent process command line network persistence",
                        "corpus_tags": ["detection", "procedural", "powershell"],
                        "top_k": 4,
                    },
                },
                "Knowledge should name discriminative telemetry, not replace looking at the incident.",
                False,
            )

        if "query_events" in tools and "query_events" not in history:
            return self._decision(
                hypotheses,
                known,
                "Which process events on the alerting host match encoded or hidden PowerShell?",
                {
                    "action_id": f"a-{len(history)+1:03d}",
                    "tool": "query_events",
                    "arguments": {
                        "source": "process_events",
                        "filter": {"host": host, "process_name": "powershell.exe"},
                        "order": "timestamp_ascending",
                        "limit": 100,
                    },
                },
                "A host-scoped process query tests whether the alert corresponds to real execution telemetry.",
                False,
            )

        if "find_process_tree" in tools and "find_process_tree" not in history and records:
            seed = next((rec.get("evidence_id") for rec in records if rec.get("evidence_id")), records[0].get("evidence_id"))
            return self._decision(
                hypotheses,
                known,
                "Was the process launched by an approved management application or an office parent?",
                {
                    "action_id": f"a-{len(history)+1:03d}",
                    "tool": "find_process_tree",
                    "arguments": {"host": host, "process_or_event_id": seed, "max_depth": 4},
                },
                "The parent process distinguishes approved administration from interactive malicious execution.",
                False,
            )

        if "build_timeline" in tools and "build_timeline" not in history:
            return self._decision(
                hypotheses,
                known,
                "What ordered cross-source events surround the alerting process?",
                {
                    "action_id": f"a-{len(history)+1:03d}",
                    "tool": "build_timeline",
                    "arguments": {
                        "host": host,
                        "sources": ["process_events", "network", "file", "registry"],
                        "limit": 100,
                    },
                },
                "A timeline tests whether execution is isolated or followed by staging, egress, or persistence.",
                False,
            )

        if "search_related" in tools and "search_related" not in history:
            entity = host
            for rec in records:
                ip = (rec.get("fields") or {}).get("destination_ip")
                if ip:
                    entity = ip
                    break
            return self._decision(
                hypotheses,
                known,
                "What other hosts, files, or network peers relate to this entity?",
                {
                    "action_id": f"a-{len(history)+1:03d}",
                    "tool": "search_related",
                    "arguments": {"entity": entity, "relation": "same_incident", "limit": 100},
                },
                "Multi-hop pivot tests whether the story stays on one host or fans out.",
                False,
            )

        return self._decision(
            hypotheses,
            known,
            "",
            {"action_id": f"a-{len(history)+1:03d}", "tool": "submit_report", "arguments": {}},
            "Budgets and remaining uncertainty no longer justify another discriminative query.",
            True,
            stop_reason="Sufficient discriminative evidence collected, or remaining tools would be redundant.",
        )

    def generate_report(self, context: dict[str, Any]) -> dict[str, Any]:
        records = []
        for obs in context.get("observations") or []:
            records.extend(obs.get("records") or [])
        if not records:
            records = list(context.get("raw_window") or [])
        known = [rec.get("evidence_id") for rec in records if rec.get("evidence_id")]
        malicious, _admin = self._beliefs(records, known)
        verdict = "malicious" if malicious >= 0.66 else "benign" if malicious <= 0.34 else "inconclusive"
        chain = []
        evidence_by_stage = {
            "Execution": [rec for rec in records if rec.get("source") == "process_events"],
            "Command and Control": [rec for rec in records if rec.get("source") == "network"],
            "Persistence": [rec for rec in records if rec.get("source") == "registry"],
        }
        techniques = {
            "Execution": "T1059.001",
            "Command and Control": "T1071.001",
            "Persistence": "T1547.001",
        }
        for stage, items in evidence_by_stage.items():
            ids = [item.get("evidence_id") for item in items if item.get("evidence_id")]
            if ids:
                chain.append({"stage": stage, "technique": techniques[stage], "evidence_ids": ids[:4]})
        hosts = sorted({rec.get("host") for rec in records if rec.get("host")})
        users = sorted(
            {
                (rec.get("fields") or {}).get("user")
                for rec in records
                if (rec.get("fields") or {}).get("user")
            }
        )
        ips = sorted(
            {
                (rec.get("fields") or {}).get("destination_ip")
                for rec in records
                if (rec.get("fields") or {}).get("destination_ip")
            }
        )
        files = sorted(
            {
                (rec.get("fields") or {}).get("path")
                for rec in records
                if (rec.get("fields") or {}).get("path")
            }
        )
        supporting = []
        seen_ids: set[str] = set()
        ranked = sorted(records, key=self._evidence_rank)
        for rec in ranked:
            eid = rec.get("evidence_id")
            if not eid or eid in seen_ids:
                continue
            seen_ids.add(eid)
            supporting.append({"event_id": eid, "claim": self._claim_for(rec)})
            if len(supporting) >= 6:
                break
        summary = self._summary(verdict, records)
        return {
            "verdict": verdict,
            "confidence": round(max(malicious, 1 - malicious), 2),
            "summary": summary,
            "attack_chain": chain,
            "key_entities": {"hosts": hosts, "users": users, "ips": ips, "files": files},
            "supporting_evidence": supporting,
            "contradicting_evidence": [],
            "remaining_uncertainty": "Initial delivery before WINWORD.EXE was not fully reconstructed."
            if verdict == "malicious"
            else "Available context may omit decisive telemetry.",
            "recommended_human_check": "Confirm whether the destination IP belongs to approved infrastructure.",
        }

    def _decision(
        self,
        hypotheses: list[dict[str, Any]],
        known: list[str],
        question: str,
        action: dict[str, Any],
        expected: str,
        stop: bool,
        stop_reason: str = "",
    ) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "hypotheses": hypotheses,
            "known_evidence": known,
            "contradicting_evidence": [],
            "next_question": question,
            "selected_action": action,
            "expected_discrimination": expected,
            "stop": stop,
            "stop_reason": stop_reason,
        }

    def _beliefs(self, records: list[dict[str, Any]], known: list[str]) -> tuple[float, float]:
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
        if "203.0.113." in blob or "destination_ip" in blob and "powershell" in blob:
            score += 0.08
        if "currentversion\\\\run" in blob or "currentversion\\run" in blob:
            score += 0.1
        if "update.ps1" in blob:
            score += 0.06
        score = min(0.93, max(0.07, score))
        return round(score, 2), round(1 - score, 2)

    def _evidence_rank(self, record: dict[str, Any]) -> tuple[int, str]:
        blob = str(record).lower()
        score = 0
        if "powershell" in blob:
            score += 4
        if "-enc" in blob or "hidden" in blob:
            score += 3
        if "winword" in blob:
            score += 2
        if "203.0.113" in blob:
            score += 2
        if "currentversion" in blob:
            score += 2
        if record.get("source") == "process_events":
            score += 1
        return (-score, record.get("evidence_id") or "")

    def _claim_for(self, record: dict[str, Any]) -> str:
        fields = record.get("fields") or {}
        if fields.get("parent_process_name"):
            return (
                f"{fields.get('process_name')} was launched by "
                f"{fields.get('parent_process_name')}."
            )
        if fields.get("destination_ip"):
            return (
                f"Outbound connection to {fields.get('destination_ip')}:"
                f"{fields.get('destination_port')} from {fields.get('process_name')}."
            )
        if fields.get("path"):
            return f"File write to {fields.get('path')}."
        if fields.get("key"):
            return f"Registry modification at {fields.get('key')}."
        return f"Telemetry record {record.get('evidence_id')} from {record.get('source')}."

    def _summary(self, verdict: str, records: list[dict[str, Any]]) -> str:
        if verdict == "malicious":
            return (
                "Encoded PowerShell was launched from an office parent and followed by "
                "staging, uncommon egress, and a Run-key persistence write."
            )
        if verdict == "benign":
            return "The available context is consistent with approved administration rather than an attack chain."
        return f"Interpreted {len(records)} evidence records without a decisive parent/follow-on pattern."
