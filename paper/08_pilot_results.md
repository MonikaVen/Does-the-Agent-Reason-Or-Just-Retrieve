# 8 Results and planned analyses

> **Manuscript update (pilot upload).** The original draft stated that no agent experiments had been run and that Tables 6–10 were blank templates. This section now records **measured pilot runs** from the companion C0–C7 lab and open-dataset scorers. Confirmatory tables for conditions **R / A / P / H / AS / HS** remain unfilled: those require the preregistered AIT V0 cohort, frozen ESR rubrics, and both backbones. Do not treat the pilots below as substitutes for Table 6.

Pilot sources:

| Artifact | Model | Generated |
|---|---|---|
| Companion C0–C7 suite (`incident-0042`) | `ollama:qwen2.5` | 2026-11-10T17:03:49Z |
| Earlier C0–C7 suite (same incident) | `ollama:llama3.2:1b` | 2026-09-16T20:01:55Z |
| Multi-benchmark open-dataset scores | `ollama:qwen2.5` | 2026-11-10T17:18:37Z |

Confidence is shown with three digits after the comma (e.g. `0,930`).

## 8.0 Pilot status summary

| Stream | Cases / conditions | Completed | Failed | Notes |
|---|---:|---:|---:|---|
| C0–C7 investigation suite | 8 conditions × 1 sample incident | 8 | 0 | Not the confirmatory A/H/AS/HS grid |
| DiscoveryBench | 3 | 3 | 0 | token-F1 vs gold hypothesis |
| DiscoveryWorld | 3 | 3 | 0 | critical-hypothesis keyword coverage |
| Cyber-SecOps-ES | 5 | 5 | 0 | evidence-grounded extraction |
| Cyber-AIT-ADS (russellmitchell) | 3 | 3 | 0 | attack-stage label; AIT-aligned pilot |

## 8.1 Companion C0–C7 outcomes (qwen2.5)

These conditions come from the companion lab (`Architecture.md` / `platform/`), not from Table 3 of the manuscript. They answer the same research question on one sealed sample incident with local Ollama.

**Table P1.** C0–C7 pilot on `incident-0042`, model `ollama:qwen2.5` (evidence-derived confidence).

| Condition | Name | Status | Verdict | Confidence | Evidence IDs | Tool obs. | Knowledge |
|---|---|---|---|---:|---|---:|---:|
| C0 | Raw LLM | completed | malicious | 0,930 | event-1021, event-1028, event-1026 | 0 | 0 |
| C1 | Knowledge-only | completed | malicious | 0,930 | event-1021, event-1028, event-1024 | 0 | 1 |
| C2 | Search-only agent | completed | inconclusive | 0,930 | event-1021, event-1028, event-1024 | 6 | 0 |
| C3 | Full agent | completed | malicious | 0,930 | event-1021, event-1028, event-1024 | 6 | 0 |
| C4 | Fixed retrieval | completed | malicious | 0,930 | event-1021, event-1028, event-1024 | 2 | 1 |
| C5 | Passive matched evidence | completed | malicious | 0,930 | event-1008 | 0 | 1 |
| C6 | Oracle evidence | completed | malicious | 0,920 | event-1021, event-1024 | 0 | 1 |
| C7 | Oracle plan | completed | benign | 0,930 | event-1021, event-1028, event-1024 | 6 | 0 |

Reading notes:

- Completed 8 / failed 0 / skipped 0.
- Telemetry search observed on **C2, C3, C4, C7**.
- Knowledge retrieval observed on **C1, C4, C5, C6**.
- Adaptive / oracle-plan arms are mixed: **C3** malicious, **C2** and **C7** disagree (inconclusive / benign) despite overlapping evidence IDs.
- Mean confidence across C0–C7: **0,928**.

### Earlier backbone (llama3.2:1b)

**Table P2.** Same incident and harness; model `ollama:llama3.2:1b` (model-reported confidence in that run).

| Condition | Status | Verdict | Confidence | Tool obs. | Knowledge |
|---|---|---|---:|---:|---:|
| C0 | completed | malicious | 0,800 | 0 | 0 |
| C1 | completed | malicious | 0,900 | 0 | 1 |
| C2 | completed | malicious | 0,800 | 1 | 0 |
| C3 | completed | malicious | 0,900 | 3 | 0 |
| C4 | completed | malicious | 0,800 | 2 | 1 |
| C5 | completed | malicious | 0,800 | 0 | 1 |
| C6 | completed | malicious | 0,800 | 0 | 1 |
| C7 | completed | malicious | 0,800 | 3 | 0 |

Mean confidence: **0,838**. All eight conditions returned **malicious**; this does not imply ESR under the manuscript rubric.

### Confirmatory Table 6 (still blank)

| Condition | ESR ↑ | CPS ↑ | Unsupported claims ↓ | Calls ↓ | Cost / run ↓ |
|---|---|---|---|---|---|
| R Fixed retrieval | — | — | — | — | — |
| A Standard agent | — | — | — | — | — |
| P Fixed playbook | — | — | — | — | — |
| H Hypothesis agent | — | — | — | — | — |
| AS Agent + scripts | — | — | — | — | — |
| HS Full method | — | — | — | — | — |

## 8.2 Open-dataset pilot scores (qwen2.5)

**Table P3.** Dataset-level means from the companion multi-benchmark harness.

| Model | Dataset | Scenarios | Completed | Mean score |
|---|---|---:|---:|---:|
| qwen2.5 | DiscoveryBench | 3 | 3 | 0,333 |
| qwen2.5 | DiscoveryWorld | 3 | 3 | 0,333 |
| qwen2.5 | Cyber-SecOps-ES | 5 | 5 | 0,920 |
| qwen2.5 | Cyber-AIT-ADS | 3 | 3 | 0,667 |

**Table P4.** Cyber-AIT-ADS scenario detail (russellmitchell development environment; attack-stage exact match).

| Scenario | Status | Score | Prediction | Gold |
|---|---|---:|---|---|
| russellmitchell/network_scans | completed | 1,000 | network_scans | network_scans |
| russellmitchell/webshell | completed | 1,000 | webshell | webshell |
| russellmitchell/dirb | completed | 0,000 | webshell | dirb |

These AIT-ADS scores are **label-classification pilots**, not ESR investigations with provenance rubrics. They do not satisfy Appendix C case-construction rules and must not be pooled into the confirmatory AIT primary estimate.

## 8.3 What remains unmeasured

Tables 7–10 in the manuscript (robustness, common-evidence interpretation, ablations, script reliability) stay templates (`—` = not measured). No V1–V5 interventions, no paired CPS, no blinded ESR adjudication, and no second frozen backbone were run for this upload.

## 8.4 Provenance

Numeric inputs are archived under `paper/data/`:

- `c0-c7-qwen25-experiment-report.json`
- `c0-c7-llama321b-experiment-report.json`
- `multi-benchmark-report.json`

Original pre-results PDF: `paper/Beyond_Retrieval_Open_Dataset_Experiments.pdf`.
