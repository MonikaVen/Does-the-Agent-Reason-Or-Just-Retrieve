# Experiment report

- Generated: `2026-11-13T16:47:51.578Z`
- Incident: `soc-soc-000010`
- Model: `ollama:qwen2.5:14b`
- Dataset: `ds-fe0e6148ab`

## Results

| Model | Condition | Status | Verdict | Confidence | Evidence IDs | Tool observations | Knowledge |
|---|---|---|---|---|---|---|---|
| ollama:qwen2.5:14b | C0 | failed | — | — | `—` | 0 | 0 |
| ollama:qwen2.5:14b | C1 | failed | — | — | `—` | 0 | 1 |
| ollama:qwen2.5:14b | C2 | failed | — | — | `—` | 1 | 0 |
| ollama:qwen2.5:14b | C3 | completed | malicious | 0.58 | `soc-000010-log-003, soc-ioc-0001-79d8a1fe` | 2 | 0 |
| ollama:qwen2.5:14b | C4 | completed | malicious | 0.58 | `soc-000010-log-001, soc-ioc-0001-79d8a1fe, soc-000010-log-003` | 2 | 1 |
| ollama:qwen2.5:14b | C5 | completed | malicious | 0.58 | `soc-ioc-0001-79d8a1fe, soc-000010-log-003, soc-000010-log-001, soc-000010-log-001` | 0 | 1 |
| ollama:qwen2.5:14b | C6 | completed | benign | 0.58 | `soc-ioc-rep-0001-765db0f5` | 0 | 1 |
| ollama:qwen2.5:14b | C7 | completed | malicious | 0.58 | `soc-000010-log-003, soc-ioc-0001-79d8a1fe` | 2 | 0 |

## Setup

Local Ollama was the model gateway. The reference investigator was not used as a silent fallback. Disabled interfaces returned `SERVICE_DISABLED`. Knowledge passages were not treated as evidence IDs. Ground truth stayed sealed.

- Completed: 5
- Failed: 3
- Skipped: 0
- Conditions that observed telemetry: C3, C4, C7
- Conditions that retrieved knowledge: C4, C5, C6

## Notes

### C0
Failed: timed out

### C1
Failed: timed out

### C2
Failed: timed out

### C3
Large outbound data transfer detected from WS-167 to an external IP, suggesting potential exfiltration.
Tools: query_events, query_events, query_events, query_events

### C4
Encoded PowerShell execution followed by an outbound connection to an uncommon IP address indicates potential malicious activity.
Tools: query_events, query_events

### C5
Large outbound data transfer detected from WS-167 to an uncommon IP shortly after suspicious encoded PowerShell activity.

### C6
Large outbound data transfer detected but no suspicious encoded PowerShell execution or persistence activity observed.

### C7
Large outbound data transfer detected from WS-167 to an external IP, suggesting potential exfiltration.
Tools: query_events, query_events, query_events, query_events

## Reading the matrix

C0/C1 cannot search telemetry. C2 searches without a knowledge service. C3 is the full adaptive loop. C4 uses a fixed query pack instead of agent-chosen tools. C5 receives C3's evidence without C3's search order. C6 is given oracle evidence; C7 is given an oracle plan. A small local model may stop early, cite poorly, or fail validation and fall back to an evidence-based malicious/benign verdict — that is a measured outcome, not a reason to swap in the reference investigator.
