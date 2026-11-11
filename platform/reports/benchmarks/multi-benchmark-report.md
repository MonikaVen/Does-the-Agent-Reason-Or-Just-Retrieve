# Multi-benchmark report

- Generated: `2026-11-11T10:43:36.762Z`
- Model: `ollama:qwen2.5:3b`
- Queued: `1256`
- Completed rows: `150`

## Dataset scores

| Model | Dataset | Scenarios | Completed | Mean score |
|---|---|---|---|---|
| qwen2.5:3b | Cyber-SecOps-ES | 54 | 54 | 0.5569 |
| qwen2.5:3b | Cyber-AIT-ADS | 79 | 79 | 0.4937 |
| qwen2.5:3b | DiscoveryBench | 17 | 17 | 0.2913 |

## Scenario scores

| Model | Dataset | Scenario | Status | Score | Detail |
|---|---|---|---|---|---|
| qwen2.5:3b | Cyber-SecOps-ES | case-01-recon/q-c01-root-cause | completed | 1.0 | grading=exact_ci; attck=T1105,T1071.001 |
| qwen2.5:3b | Cyber-SecOps-ES | case-01-recon/q-c01-c2-ip | completed | 1.0 | grading=exact_ci; attck=T1071.001 |
| qwen2.5:3b | Cyber-SecOps-ES | case-01-recon/q-c01-c2-port | completed | 1.0 | grading=exact_ci; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-01-recon/q-c01-credaccess-file | completed | 1.0 | grading=exact_ci; attck=T1003.008 |
| qwen2.5:3b | Cyber-SecOps-ES | case-01-recon/q-c01-persistence | completed | 0.0 | grading=exact_ci; attck=T1053.003 |
| qwen2.5:3b | Cyber-SecOps-ES | case-01-recon/q-c01-delivery | completed | 1.0 | grading=mcq; attck=T1105,T1059.004 |
| qwen2.5:3b | Cyber-SecOps-ES | case-01-recon/q-c01-iocs | completed | 0.6667 | grading=set_f1; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-01-recon/q-c01-attck | completed | 0.5333 | grading=set_f1; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-01-recon/q-c01-timeline | completed | 1.0 | grading=ordering; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-01-recon/q-c01-neg-zeekcron | completed | 0.0 | grading=boolean; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-01-recon/q-c01-disc-8080 | completed | 0.0 | grading=mcq; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-02-collection-exfil/q-c02-archive | completed | 1.0 | grading=exact_ci; attck=T1560.001 |
| qwen2.5:3b | Cyber-SecOps-ES | case-02-collection-exfil/q-c02-exfil-dest | completed | 1.0 | grading=exact_ci; attck=T1041 |
| qwen2.5:3b | Cyber-SecOps-ES | case-02-collection-exfil/q-c02-exfil-happened | completed | 0.0 | grading=boolean; attck=T1041 |
| qwen2.5:3b | Cyber-SecOps-ES | case-02-collection-exfil/q-c02-decoy-or-real | completed | 0.0 | grading=mcq; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-02-collection-exfil/q-c02-timestomp | completed | 0.0 | grading=exact_ci; attck=T1070.006 |
| qwen2.5:3b | Cyber-SecOps-ES | case-02-collection-exfil/q-c02-ti-match | completed | 0.0 | grading=boolean; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-02-collection-exfil/q-c02-portscan | completed | 0.0 | grading=mcq; attck=T1046 |
| qwen2.5:3b | Cyber-SecOps-ES | case-02-collection-exfil/q-c02-attck | completed | 0.9231 | grading=set_f1; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-02-collection-exfil/q-c02-same-actor | completed | 0.0 | grading=boolean; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-03-web-exploit-revshell/q-c03-webtools | completed | 0.4 | grading=set_f1; attck=T1595,T1190 |
| qwen2.5:3b | Cyber-SecOps-ES | case-03-web-exploit-revshell/q-c03-log4shell | completed | 0.0 | grading=mcq; attck=T1190 |
| qwen2.5:3b | Cyber-SecOps-ES | case-03-web-exploit-revshell/q-c03-webshell | completed | 1.0 | grading=exact_ci; attck=T1505.003 |
| qwen2.5:3b | Cyber-SecOps-ES | case-03-web-exploit-revshell/q-c03-revshell-dest | completed | 1.0 | grading=exact_ci; attck=T1059.004,T1071.001 |
| qwen2.5:3b | Cyber-SecOps-ES | case-03-web-exploit-revshell/q-c03-revshell-mechanism | completed | 1.0 | grading=mcq; attck=T1059.004 |
| qwen2.5:3b | Cyber-SecOps-ES | case-03-web-exploit-revshell/q-c03-handsonkbd | completed | 0.8333 | grading=set_f1; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-03-web-exploit-revshell/q-c03-initial-access | completed | 1.0 | grading=exact_ci; attck=T1190 |
| qwen2.5:3b | Cyber-SecOps-ES | case-03-web-exploit-revshell/q-c03-attck | completed | 0.8 | grading=set_f1; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-03-web-exploit-revshell/q-c03-neg-benign-ua | completed | 0.0 | grading=boolean; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-04-privesc/q-c04-suid-artifact | completed | 1.0 | grading=exact_ci; attck=T1548.001 |
| qwen2.5:3b | Cyber-SecOps-ES | case-04-privesc/q-c04-suid-how | completed | 1.0 | grading=mcq; attck=T1548.001 |
| qwen2.5:3b | Cyber-SecOps-ES | case-04-privesc/q-c04-gtfobins | completed | 0.25 | grading=set_f1; attck=T1548.003 |
| qwen2.5:3b | Cyber-SecOps-ES | case-04-privesc/q-c04-binary-copy-alert | completed | 1.0 | grading=exact_ci; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-04-privesc/q-c04-severity-calibration | completed | 0.0 | grading=mcq; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-04-privesc/q-c04-antiforensics | completed | 0.0 | grading=boolean; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-04-privesc/q-c04-already-root | completed | 1.0 | grading=mcq; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-04-privesc/q-c04-attck | completed | 0.6667 | grading=set_f1; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-05-lateral-movement/q-c05-source-host | completed | 1.0 | grading=exact_ci; attck=T1021.004 |
| qwen2.5:3b | Cyber-SecOps-ES | case-05-lateral-movement/q-c05-target-host | completed | 1.0 | grading=exact_ci; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-05-lateral-movement/q-c05-cred | completed | 1.0 | grading=exact_ci; attck=T1552.004 |
| qwen2.5:3b | Cyber-SecOps-ES | case-05-lateral-movement/q-c05-access-method | completed | 1.0 | grading=mcq; attck=T1021.004,T1552.004 |
| qwen2.5:3b | Cyber-SecOps-ES | case-05-lateral-movement/q-c05-correlation-ip | completed | 1.0 | grading=exact_ci; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-05-lateral-movement/q-c05-discriminator | completed | 0.0 | grading=mcq; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-05-lateral-movement/q-c05-recon | completed | 1.0 | grading=set_f1; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-05-lateral-movement/q-c05-scope | completed | 1.0 | grading=exact_ci; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-05-lateral-movement/q-c05-attck | completed | 1.0 | grading=set_f1; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | case-05-lateral-movement/q-c05-neg-scannoise | completed | 0.0 | grading=boolean; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | cross-case/q-x-attacker-ip | completed | 0.0 | grading=exact_ci; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | cross-case/q-x-implant | completed | 0.0 | grading=exact_ci; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | cross-case/q-x-iocs-full | completed | 0.0 | grading=set_f1; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | cross-case/q-x-hosts | completed | 0.0 | grading=set_f1; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | cross-case/q-x-killchain-order | completed | 1.0 | grading=ordering; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | cross-case/q-x-single-intrusion | completed | 0.0 | grading=boolean; attck= |
| qwen2.5:3b | Cyber-SecOps-ES | cross-case/q-x-containment | completed | 0.0 | grading=set_f1; attck= |
| qwen2.5:3b | Cyber-AIT-ADS | russellmitchell/network_scans | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | russellmitchell/service_scans | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | russellmitchell/dirb | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | russellmitchell/wpscan | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | russellmitchell/webshell | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | russellmitchell/cracking | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | russellmitchell/reverse_shell | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | russellmitchell/privilege_escalation | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | russellmitchell/service_stop | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | russellmitchell/dnsteal | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | fox/network_scans | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | fox/service_scans | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | fox/wpscan | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | fox/dirb | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | fox/webshell | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | fox/cracking | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | fox/reverse_shell | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | fox/privilege_escalation | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | fox/service_stop | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | fox/dnsteal | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | harrison/network_scans | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | harrison/service_scans | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | harrison/wpscan | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | harrison/dirb | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | harrison/webshell | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | harrison/cracking | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | harrison/reverse_shell | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | harrison/privilege_escalation | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | harrison/service_stop | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | harrison/dnsteal | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | santos/network_scans | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | santos/service_scans | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | santos/dirb | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | santos/wpscan | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | santos/webshell | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | santos/cracking | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | santos/reverse_shell | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | santos/privilege_escalation | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | santos/service_stop | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | santos/dnsteal | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | shaw/network_scans | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | shaw/service_scans | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | shaw/wpscan | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | shaw/dirb | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | shaw/webshell | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | shaw/cracking | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | shaw/reverse_shell | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | shaw/privilege_escalation | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | shaw/service_stop | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | shaw/dnsteal | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wardbeck/network_scans | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wardbeck/service_scans | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wardbeck/wpscan | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wardbeck/dirb | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wardbeck/webshell | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wardbeck/cracking | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wardbeck/reverse_shell | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wardbeck/privilege_escalation | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wardbeck/service_stop | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wardbeck/dnsteal | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wheeler/network_scans | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wheeler/service_scans | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wheeler/wpscan | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wheeler/dirb | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wheeler/webshell | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wheeler/reverse_shell | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wheeler/privilege_escalation | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wheeler/service_stop | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wheeler/dnsteal | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wilson/network_scans | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wilson/service_scans | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wilson/wpscan | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wilson/dirb | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wilson/webshell | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wilson/cracking | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wilson/reverse_shell | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wilson/privilege_escalation | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wilson/service_stop | completed | 1.0 | exact_ci attack-stage label |
| qwen2.5:3b | Cyber-AIT-ADS | wilson/dnsteal | completed | 0.0 | exact_ci attack-stage label |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_0/q0 | completed | 0.169 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_1/q0 | completed | 0.3438 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_10/q0 | completed | 0.2083 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_11/q0 | completed | 0.1316 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_12/q0 | completed | 0.1091 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_13/q0 | completed | 0.1682 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_14/q0 | completed | 0.2353 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_15/q0 | completed | 0.3802 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_16/q0 | completed | 0.4194 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_17/q0 | completed | 0.3692 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_18/q0 | completed | 0.3537 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_19/q0 | completed | 0.3385 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_2/q0 | completed | 0.1443 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_20/q0 | completed | 0.3571 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_21/q0 | completed | 0.4667 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_22/q0 | completed | 0.3944 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_23/q0 | completed | 0.3636 | token_f1 vs gold hypothesis |

## Notes

- DiscoveryBench: token-F1 of hypothesis vs gold answer key (real + synth test).
- DiscoveryWorld: discovery statements plus critical-question probes from theme/difficulty/seed inventory.
- Cyber-SecOps-ES: evidence-grounded extraction against sealed answer key (unsealed locally).
- Cyber-AIT-ADS: attack-stage classification from AMiner alert windows across hosts.
- Confidence is not used; scores are deterministic graders.
- Long runs checkpoint to `multi-benchmark-checkpoint.json` every N scenarios.
