# Experiment report

- Generated: `2026-09-16T20:01:55.315Z`
- Incident: `incident-0042`
- Model: `ollama:llama3.2:1b`
- Dataset: `ds-sample-0042`

## Results

| Condition | Status | Verdict | Confidence | Evidence IDs | Tool observations | Knowledge |
|---|---|---|---|---|---|---|
| C0 | completed | malicious | 0.8 | `event-1008, event-1019, event-1021, event-1024, event-1009, event-1026, event-1033` | 0 | 0 |
| C1 | completed | malicious | 0.9 | `event-1008, event-1019, event-1021, event-1024, event-1026, event-1033` | 0 | 1 |
| C2 | completed | malicious | 0.8 | `event-1008, event-1019, event-1021, event-1028, event-1024, event-1009` | 1 | 0 |
| C3 | completed | malicious | 0.9 | `event-1008, event-1019, event-1021, event-1028, event-1024, event-1009` | 3 | 0 |
| C4 | completed | malicious | 0.8 | `event-1021, event-1028, event-1009` | 2 | 1 |
| C5 | completed | malicious | 0.8 | `event-1008, event-1009` | 0 | 1 |
| C6 | completed | malicious | 0.8 | `event-1021, event-1024` | 0 | 1 |
| C7 | completed | malicious | 0.8 | `event-1008, event-1019, event-1021, event-1028, event-1024, event-1009` | 3 | 0 |

## Setup

Local Ollama was the model gateway. The reference investigator was not used as a silent fallback. Disabled interfaces returned `SERVICE_DISABLED`. Knowledge passages were not treated as evidence IDs. Ground truth stayed sealed.

- Completed: 8
- Failed: 0
- Skipped: 0
- Conditions that observed telemetry: C2, C3, C4, C7
- Conditions that retrieved knowledge: C1, C4, C5, C6

## Notes

### C0
Encoded PowerShell execution detected on workstation-17, suggesting a potential attack.

### C1
The presence of encoded PowerShell execution and suspicious network activity suggests a malicious attack.

### C2
The alerting process appears to have been launched by the execution of PowerShell on workstation-17.
Tools: query_events, query_events

### C3
The ATT&CK technique T1059.001 was used to launch the alerting process.
Tools: query_events, query_events, query_events, query_events, query_events, query_events

### C4
Encoded PowerShell execution detected on workstation-17, suggesting malicious activity.
Tools: query_events, query_events

### C5
Encoded PowerShell execution detected on workstation-17, suggesting malicious activity.

### C6
The presence of encoded PowerShell execution on workstation-17 suggests malicious activity.

### C7
The ATT&CK technique T1059.001 was used to launch the alerting process.
Tools: query_events, query_events, query_events, query_events, query_events, query_events

## Reading the matrix

C0/C1 cannot search telemetry. C2 searches without a knowledge service. C3 is the full adaptive loop. C4 uses a fixed query pack instead of agent-chosen tools. C5 receives C3's evidence without C3's search order. C6 is given oracle evidence; C7 is given an oracle plan. A small local model may stop early, cite poorly, or return inconclusive after validation — that is a measured outcome, not a reason to swap in the reference investigator.
