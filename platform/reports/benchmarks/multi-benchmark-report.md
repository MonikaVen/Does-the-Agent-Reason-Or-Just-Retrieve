# Multi-benchmark report

- Generated: `2026-11-10T17:18:37.684Z`
- Model: `ollama:qwen2.5`

## Dataset scores

| Model | Dataset | Scenarios | Completed | Mean score |
|---|---|---|---|---|
| qwen2.5 | DiscoveryBench | 3 | 3 | 0.3327 |
| qwen2.5 | DiscoveryWorld | 3 | 3 | 0.3333 |
| qwen2.5 | Cyber-SecOps-ES | 5 | 5 | 0.92 |
| qwen2.5 | Cyber-AIT-ADS | 3 | 3 | 0.6667 |

## Scenario scores

| Model | Dataset | Scenario | Status | Score | Detail |
|---|---|---|---|---|---|
| qwen2.5 | DiscoveryBench | archaeology/metadata_0/q0 | completed | 0.1714 | token_f1 vs gold hypothesis |
| qwen2.5 | DiscoveryBench | nls_incarceration/metadata_0/q0 | completed | 0.6667 | token_f1 vs gold hypothesis |
| qwen2.5 | DiscoveryBench | worldbank_education_gdp/metadata_0/q0 | completed | 0.16 | token_f1 vs gold hypothesis |
| qwen2.5 | DiscoveryWorld | Space Sick/Easy/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5 | DiscoveryWorld | Combinatorial Chemistry/Easy/seed0 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5 | DiscoveryWorld | Archaeology Dating/Easy/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5 | Cyber-SecOps-ES | case-01-recon/q-c01-root-cause | completed | 1.0 | grading=exact_ci; attck=T1105,T1071.001 |
| qwen2.5 | Cyber-SecOps-ES | case-01-recon/q-c01-c2-ip | completed | 1.0 | grading=exact_ci; attck=T1071.001 |
| qwen2.5 | Cyber-SecOps-ES | case-02-collection-exfil/q-c02-archive | completed | 1.0 | grading=exact_ci; attck=T1560.001 |
| qwen2.5 | Cyber-SecOps-ES | case-02-collection-exfil/q-c02-exfil-dest | completed | 1.0 | grading=exact_ci; attck=T1041 |
| qwen2.5 | Cyber-SecOps-ES | case-03-web-exploit-revshell/q-c03-webtools | completed | 0.6 | grading=set_f1; attck=T1595,T1190 |
| qwen2.5 | Cyber-AIT-ADS | russellmitchell/network_scans | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5 | Cyber-AIT-ADS | russellmitchell/webshell | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5 | Cyber-AIT-ADS | russellmitchell/dirb | completed | 0.0 | exact_ci attack-stage label |

## Notes

- DiscoveryBench: token-F1 of hypothesis vs gold answer key.
- DiscoveryWorld: keyword coverage of critical hypotheses from Easy scenarios (offline observation evidence).
- Cyber-SecOps-ES: evidence-grounded extraction against sealed answer key (unsealed locally).
- Cyber-AIT-ADS: attack-stage classification from AMiner alert windows (russellmitchell).
- Confidence is not used; scores are deterministic graders.
