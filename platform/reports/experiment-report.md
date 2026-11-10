# Experiment report

- Generated: `2026-11-10T17:03:49.821Z`
- Incident: `incident-0042`
- Model: `ollama:qwen2.5`
- Dataset: `ds-sample-0042`

## Results

| Condition | Status | Verdict | Confidence | Evidence IDs | Tool observations | Knowledge |
|---|---|---|---|---|---|---|
| C0 | completed | malicious | 0.93 | `event-1021, event-1028, event-1026` | 0 | 0 |
| C1 | completed | malicious | 0.93 | `event-1021, event-1028, event-1024` | 0 | 1 |
| C2 | completed | inconclusive | 0.93 | `event-1021, event-1028, event-1024` | 6 | 0 |
| C3 | completed | malicious | 0.93 | `event-1021, event-1028, event-1024` | 6 | 0 |
| C4 | completed | malicious | 0.93 | `event-1021, event-1028, event-1024` | 2 | 1 |
| C5 | completed | malicious | 0.93 | `event-1008` | 0 | 1 |
| C6 | completed | malicious | 0.92 | `event-1021, event-1024` | 0 | 1 |
| C7 | completed | benign | 0.93 | `event-1021, event-1028, event-1024` | 6 | 0 |

## Setup

Local Ollama was the model gateway. The reference investigator was not used as a silent fallback. Disabled interfaces returned `SERVICE_DISABLED`. Knowledge passages were not treated as evidence IDs. Ground truth stayed sealed.

- Completed: 8
- Failed: 0
- Skipped: 0
- Conditions that observed telemetry: C2, C3, C4, C7
- Conditions that retrieved knowledge: C1, C4, C5, C6

## Notes

### C0
Encoded PowerShell execution detected, with network activity and registry changes.

### C1
Encoded PowerShell execution with network activity suggests malicious intent.

### C2
Insufficient evidence to determine if the PowerShell execution is malicious or benign.
Tools: query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events

### C3
Encoded PowerShell execution detected on workstation-17, indicating potential malicious activity.
Tools: query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events

### C4
Encoded PowerShell execution detected with suspicious parent process and network activity.
Tools: query_events, query_events

### C5
Encoded PowerShell execution detected, indicative of malicious activity.

### C6
Encoded PowerShell execution detected, followed by network activity, indicating potential malicious intent.

### C7
The PowerShell execution detected on workstation-17 appears to be benign as it is part of a legitimate workflow involving multiple processes.
Tools: query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events

## Reading the matrix

C0/C1 cannot search telemetry. C2 searches without a knowledge service. C3 is the full adaptive loop. C4 uses a fixed query pack instead of agent-chosen tools. C5 receives C3's evidence without C3's search order. C6 is given oracle evidence; C7 is given an oracle plan. A small local model may stop early, cite poorly, or return inconclusive after validation — that is a measured outcome, not a reason to swap in the reference investigator.
