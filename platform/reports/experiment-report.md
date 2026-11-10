# Experiment report

- Generated: `2026-11-10T16:25:49.687Z`
- Incident: `incident-0042`
- Model: `ollama:qwen2.5`
- Dataset: `ds-sample-0042`

## Results

| Condition | Status | Verdict | Confidence | Evidence IDs | Tool observations | Knowledge |
|---|---|---|---|---|---|---|
| C0 | completed | malicious | 0.95 | `event-1021, event-1028, event-1026, event-1024` | 0 | 0 |
| C1 | completed | malicious | 0.8 | `event-1021, event-1028, event-1024` | 0 | 1 |
| C2 | completed | malicious | 0.9 | `event-1024` | 6 | 0 |
| C3 | completed | inconclusive | 0.5 | `event-1021, event-1028, event-1024` | 6 | 0 |
| C4 | completed | malicious | 0.8 | `event-1021, event-1028, event-1024` | 2 | 1 |
| C5 | completed | inconclusive | 0.0 | `event-1008` | 0 | 1 |
| C6 | completed | malicious | 0.75 | `event-1021, event-1024` | 0 | 1 |
| C7 | completed | inconclusive | 0.5 | `event-1021, event-1028, event-1024` | 6 | 0 |

## Setup

Local Ollama was the model gateway. The reference investigator was not used as a silent fallback. Disabled interfaces returned `SERVICE_DISABLED`. Knowledge passages were not treated as evidence IDs. Ground truth stayed sealed.

- Completed: 8
- Failed: 0
- Skipped: 0
- Conditions that observed telemetry: C2, C3, C4, C7
- Conditions that retrieved knowledge: C1, C4, C5, C6

## Notes

### C0
Execution of PowerShell with suspicious activity and network communication.

### C1
Encoded PowerShell execution followed by network activity to an uncommon IP address suggests malicious intent.

### C2
The PowerShell process communicated with an external IP address, indicating potential malicious activity.
Tools: query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events

### C3
Insufficient evidence to determine if the PowerShell execution is malicious.
Tools: query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events

### C4
Encoded PowerShell execution detected with suspicious parent process and network activity.
Tools: query_events, query_events

### C5
Insufficient evidence to determine if the detected PowerShell execution is malicious.

### C6
Encoded PowerShell execution detected, followed by network activity, indicating potential malicious intent.

### C7
The PowerShell execution detected on workstation-17 is suspicious but lacks definitive evidence of malicious intent.
Tools: query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events

## Reading the matrix

C0/C1 cannot search telemetry. C2 searches without a knowledge service. C3 is the full adaptive loop. C4 uses a fixed query pack instead of agent-chosen tools. C5 receives C3's evidence without C3's search order. C6 is given oracle evidence; C7 is given an oracle plan. A small local model may stop early, cite poorly, or return inconclusive after validation — that is a measured outcome, not a reason to swap in the reference investigator.
