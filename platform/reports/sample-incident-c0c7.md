# Experiment report

- Generated: `2026-11-12T22:27:14.622Z`
- Incident: `ait-wilson-dnsteal`
- Model: `ollama:llama3.2:1b`
- Dataset: `ds-f023a721d3`

## Results

| Model | Condition | Status | Verdict | Confidence | Evidence IDs | Tool observations | Knowledge |
|---|---|---|---|---|---|---|---|
| ollama:llama3.2:1b | C0 | completed | benign | 0.56 | `event-id` | 0 | 0 |
| ollama:llama3.2:1b | C1 | completed | benign | 0.56 | `event-id` | 0 | 1 |
| ollama:llama3.2:1b | C2 | completed | benign | 0.56 | `event-id` | 2 | 0 |
| ollama:llama3.2:1b | C3 | completed | benign | 0.56 | `event-id` | 2 | 0 |
| ollama:llama3.2:1b | C4 | completed | benign | 0.56 | `event-id, event-id, event-id` | 2 | 1 |
| ollama:llama3.2:1b | C5 | completed | benign | 0.56 | `event-id, event-id` | 0 | 1 |
| ollama:llama3.2:1b | C6 | completed | benign | 0.56 | `event-id, event-id` | 0 | 1 |
| ollama:llama3.2:1b | C7 | completed | benign | 0.56 | `event-id` | 2 | 0 |

## Setup

Local Ollama was the model gateway. The reference investigator was not used as a silent fallback. Disabled interfaces returned `SERVICE_DISABLED`. Knowledge passages were not treated as evidence IDs. Ground truth stayed sealed.

- Completed: 8
- Failed: 0
- Skipped: 0
- Conditions that observed telemetry: C2, C3, C4, C7
- Conditions that retrieved knowledge: C1, C4, C5, C6

## Notes

### C0
The T1059.001 attack chain was detected.
Validator: supporting evidence event-id was not observed in this run; attack-chain evidence event-id was not observed in this run

### C1
The execution of a T1059.001 technique was observed on a host with suspicious activity.
Validator: supporting evidence event-id was not observed in this run; attack-chain evidence event-id was not observed in this run

### C2
The alert represents malicious execution.
Tools: query_events, query_events, query_events, query_events
Validator: supporting evidence event-id was not observed in this run; attack-chain evidence event-id was not observed in this run

### C3
The alert represents malicious execution.
Tools: query_events, query_events, query_events, query_events
Validator: supporting evidence event-id was not observed in this run; attack-chain evidence event-id was not observed in this run

### C4
The analysis of the provided observations suggests that the T1059.001 ATT&CK technique was successfully exploited to execute malicious code on the target system.
Tools: query_events, query_events
Validator: supporting evidence event-id was not observed in this run; supporting evidence event-id was not observed in this run; supporting evidence event-id was not observed in this run; attack-chain evidence event-id was not observed in this run

### C5
The analysis of the AIT-ADS multi-step stage candidate on wilson indicates the presence of encoded PowerShell (T1059.001), suggesting a malicious attack.
Validator: supporting evidence event-id was not observed in this run; supporting evidence event-id was not observed in this run; attack-chain evidence event-id was not observed in this run

### C6
The presence of T1059.001 in the observed events suggests a malicious attack.
Validator: supporting evidence event-id was not observed in this run; supporting evidence event-id was not observed in this run; attack-chain evidence event-id was not observed in this run

### C7
The alert represents malicious execution.
Tools: query_events, query_events, query_events, query_events
Validator: supporting evidence event-id was not observed in this run; attack-chain evidence event-id was not observed in this run

## Reading the matrix

C0/C1 cannot search telemetry. C2 searches without a knowledge service. C3 is the full adaptive loop. C4 uses a fixed query pack instead of agent-chosen tools. C5 receives C3's evidence without C3's search order. C6 is given oracle evidence; C7 is given an oracle plan. A small local model may stop early, cite poorly, or fail validation and fall back to an evidence-based malicious/benign verdict — that is a measured outcome, not a reason to swap in the reference investigator.
