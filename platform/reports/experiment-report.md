# Experiment report

- Generated: `2026-11-12T16:25:22.409Z`
- Incident: `incident-0042`
- Model: `ollama:qwen2.5:3b`
- Dataset: `ds-sample-0042`

## Results

| Model | Condition | Status | Verdict | Confidence | Evidence IDs | Tool observations | Knowledge |
|---|---|---|---|---|---|---|---|
| ollama:qwen2.5:3b | C0 | completed | malicious | 0.93 | `event-1021, event-1028, event-1024, event-1026` | 0 | 0 |
| ollama:qwen2.5:3b | C1 | completed | malicious | 0.93 | `event-1021, event-1028, event-1024, event-1033` | 0 | 1 |
| ollama:qwen2.5:3b | C2 | completed | malicious | 0.93 | `event-1021, event-1028, event-1024` | 6 | 0 |
| ollama:qwen2.5:3b | C3 | completed | malicious | 0.93 | `event-1021, event-1028, event-1024` | 6 | 0 |
| ollama:qwen2.5:3b | C4 | completed | malicious | 0.93 | `event-1021, event-1028, event-1024, event-1009` | 2 | 1 |
| ollama:qwen2.5:3b | C5 | completed | malicious | 0.93 | `event-1008` | 0 | 1 |
| ollama:qwen2.5:3b | C6 | completed | malicious | 0.92 | `event-1021, event-1024` | 0 | 1 |
| ollama:qwen2.5:3b | C7 | completed | malicious | 0.93 | `event-1021, event-1028, event-1024` | 6 | 0 |

## Setup

Local Ollama was the model gateway. The reference investigator was not used as a silent fallback. Disabled interfaces returned `SERVICE_DISABLED`. Knowledge passages were not treated as evidence IDs. Ground truth stayed sealed.

- Completed: 8
- Failed: 0
- Skipped: 0
- Conditions that observed telemetry: C2, C3, C4, C7
- Conditions that retrieved knowledge: C1, C4, C5, C6

## Notes

### C0
Encoded PowerShell execution detected on workstation-17, likely part of a malicious campaign.

### C1
Encoded PowerShell execution detected on workstation-17 with suspicious network activity and registry persistence.

### C2
The alert represents malicious execution as evidenced by the encoded PowerShell execution detected on workstation-17.
Tools: query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events

### C3
The alert represents malicious execution as evidenced by the encoded PowerShell execution detected on workstation-17.
Tools: query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events

### C4
Encoded PowerShell execution detected on workstation-17 with suspicious parent process and network activity, indicative of malicious intent.
Tools: query_events, query_events

### C5
Encoded PowerShell execution detected and suspicious activity following execution.

### C6
Encoded PowerShell execution detected and followed by an outbound connection to an uncommon IP, raising suspicion of malicious activity.

### C7
The alert represents malicious execution as evidenced by the encoded PowerShell execution detected on workstation-17.
Tools: query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events, query_events

## Reading the matrix

C0/C1 cannot search telemetry. C2 searches without a knowledge service. C3 is the full adaptive loop. C4 uses a fixed query pack instead of agent-chosen tools. C5 receives C3's evidence without C3's search order. C6 is given oracle evidence; C7 is given an oracle plan. A small local model may stop early, cite poorly, or return inconclusive after validation — that is a measured outcome, not a reason to swap in the reference investigator.
