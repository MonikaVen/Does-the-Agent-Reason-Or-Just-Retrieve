# Multi-benchmark report

- Generated: `2026-11-11T11:31:13.204Z`
- Model: `ollama:qwen2.5:3b`
- Queued: `1256`
- Completed rows: `475`

## Dataset scores

| Model | Dataset | Scenarios | Completed | Mean score |
|---|---|---|---|---|
| qwen2.5:3b | Cyber-SecOps-ES | 54 | 54 | 0.5569 |
| qwen2.5:3b | Cyber-AIT-ADS | 79 | 79 | 0.4937 |
| qwen2.5:3b | DiscoveryBench | 342 | 320 | 0.4579 |

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
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_24/q0 | completed | 0.2909 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_25/q0 | completed | 0.283 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_26/q0 | completed | 0.1522 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_27/q0 | completed | 0.2278 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_28/q0 | completed | 0.3692 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_29/q0 | completed | 0.2376 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_3/q0 | completed | 0.12 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_30/q0 | completed | 0.25 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_31/q0 | completed | 0.2529 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_32/q0 | completed | 0.1111 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_33/q0 | completed | 0.1556 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_34/q0 | completed | 0.26 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_35/q0 | completed | 0.1316 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_36/q0 | completed | 0.2 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_37/q0 | completed | 0.2933 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_4/q0 | completed | 0.1842 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_5/q0 | completed | 0.0857 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_6/q0 | completed | 0.05 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_7/q0 | completed | 0.12 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_8/q0 | completed | 0.1368 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/archaeology/metadata_9/q0 | completed | 0.1205 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_0/q0 | completed | 0.4737 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_0/q1 | completed | 0.4706 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_0/q2 | completed | 0.2381 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_1/q0 | completed | 0.5143 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_1/q1 | completed | 0.5 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_2/q0 | completed | 0.3158 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_2/q1 | completed | 0.2051 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_3/q0 | completed | 0.3404 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_3/q1 | completed | 0.2727 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_3/q2 | completed | 0.4186 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_4/q0 | completed | 0.4 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_4/q1 | completed | 0.2979 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_4/q2 | completed | 0.3333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_5/q0 | completed | 0.3333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_5/q1 | completed | 0.1935 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/introduction_pathways_non-native_plants/metadata_5/q2 | completed | 0.3 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_0/q0 | completed | 0.6122 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_0/q1 | completed | 0.5217 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_0/q2 | completed | 0.4889 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_0/q3 | completed | 0.566 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_1/q0 | completed | 0.5652 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_1/q1 | completed | 0.5333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_10/q0 | completed | 0.45 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_10/q1 | completed | 0.4583 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_11/q0 | completed | 0.6897 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_11/q1 | completed | 0.7097 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_12/q0 | completed | 0.7391 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_12/q1 | completed | 0.36 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_13/q0 | completed | 0.2105 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_13/q1 | completed | 0.3182 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_13/q2 | completed | 0.2857 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_13/q3 | completed | 0.5714 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_14/q0 | completed | 0.6087 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_15/q0 | completed | 0.4255 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_15/q1 | completed | 0.4194 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_15/q2 | completed | 0.3673 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_16/q0 | completed | 0.4865 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_16/q1 | completed | 0.5714 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_17/q0 | completed | 0.5385 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_17/q1 | completed | 0.4138 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_17/q2 | completed | 0.4062 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_18/q0 | completed | 0.5532 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_18/q1 | completed | 0.4 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_18/q2 | completed | 0.4103 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_19/q0 | completed | 0.6071 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_19/q1 | completed | 0.5517 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_19/q2 | completed | 0.5882 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_19/q3 | completed | 0.5333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_19/q4 | completed | 0.5714 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_2/q0 | completed | 0.4444 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_2/q1 | completed | 0.5238 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_3/q0 | completed | 0.4615 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_3/q1 | completed | 0.4 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_3/q2 | completed | 0.3913 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_4/q0 | completed | 0.5532 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_5/q0 | completed | 0.6087 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_5/q1 | completed | 0.5217 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_5/q2 | completed | 0.4091 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_6/q0 | completed | 0.6087 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_6/q1 | completed | 0.386 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_6/q2 | completed | 0.5417 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_7/q0 | completed | 0.6829 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_7/q1 | completed | 0.4231 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_8/q0 | completed | 0.6667 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_8/q1 | completed | 0.5106 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression/metadata_9/q0 | completed | 0.4082 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_0/q0 | completed | 0.4615 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_0/q1 | completed | 0.5106 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_0/q2 | completed | 0.4783 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_0/q3 | completed | 0.5769 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_1/q0 | completed | 0.5217 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_1/q1 | completed | 0.4889 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_10/q0 | completed | 0.4 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_10/q1 | completed | 0.3673 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_11/q0 | completed | 0.7857 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_11/q1 | completed | 0.6486 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_12/q0 | completed | 0.7442 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_12/q1 | completed | 0.2703 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_13/q0 | completed | 0.4118 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_13/q1 | completed | 0.4118 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_13/q2 | completed | 0.35 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_13/q3 | completed | 0.5714 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_14/q0 | completed | 0.3721 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_15/q0 | completed | 0.4545 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_15/q1 | completed | 0.4444 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_15/q2 | completed | 0.4444 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_16/q0 | completed | 0.4211 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_16/q1 | completed | 0.3529 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_17/q0 | completed | 0.5455 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_17/q1 | completed | 0.4528 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_17/q2 | completed | 0.4167 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_18/q0 | completed | 0.6667 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_18/q1 | completed | 0.5 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_18/q2 | completed | 0.3333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_19/q0 | completed | 0.6909 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_19/q1 | completed | 0.4906 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_19/q2 | completed | 0.5556 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_19/q3 | completed | 0.5556 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_19/q4 | completed | 0.5424 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_2/q0 | completed | 0.4 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_2/q1 | completed | 0.5946 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_3/q0 | completed | 0.4878 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_3/q1 | completed | 0.3636 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_3/q2 | completed | 0.439 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_4/q0 | completed | 0.5833 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_5/q0 | completed | 0.6222 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_5/q1 | completed | 0.5217 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_5/q2 | completed | 0.3462 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_6/q0 | completed | 0.6087 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_6/q1 | completed | 0.5455 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_6/q2 | completed | 0.5417 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_7/q0 | completed | 0.75 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_7/q1 | completed | 0.449 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_8/q0 | completed | 0.5769 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_8/q1 | completed | 0.4528 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/meta_regression_raw/metadata_9/q0 | completed | 0.4 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_0/q0 | completed | 0.4 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_0/q1 | completed | 0.7027 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_0/q2 | completed | 0.5581 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_1/q0 | completed | 0.7273 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_10/q0 | completed | 0.5366 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_11/q0 | completed | 0.6154 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_12/q0 | completed | 0.4074 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_12/q1 | completed | 0.2727 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_12/q2 | completed | 0.4255 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_13/q0 | completed | 0.3019 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_14/q0 | completed | 0.6047 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_14/q1 | completed | 0.5581 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_14/q2 | completed | 0.7179 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_15/q0 | completed | 0.459 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_2/q0 | completed | 0.6275 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_2/q1 | completed | 0.6122 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_3/q0 | completed | 0.3774 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_3/q1 | completed | 0.48 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_3/q2 | completed | 0.4364 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_3/q3 | completed | 0.7925 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_3/q4 | completed | 0.4912 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_3/q5 | completed | 0.3077 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_4/q0 | completed | 0.2927 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_5/q0 | completed | 0.3333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_6/q0 | completed | 0.375 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_7/q0 | completed | 0.3415 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_8/q0 | completed | 0.3784 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_incarceration/metadata_9/q0 | completed | 0.4651 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_raw/metadata_2/q0 | completed | 0.4727 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_raw/metadata_3/q0 | completed | 0.2963 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_raw/metadata_4/q0 | completed | 0.2222 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_raw/metadata_5/q0 | completed | 0.4583 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_raw/metadata_6/q0 | completed | 0.4706 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_raw/metadata_7/q0 | completed | 0.25 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_raw/metadata_8/q0 | completed | 0.4762 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_0/q0 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_0/q1 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_1/q0 | completed | 0.0 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_10/q0 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_10/q1 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_10/q2 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_10/q3 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_11/q0 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_2/q0 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_3/q0 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_4/q0 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_4/q1 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_5/q0 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_5/q1 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_6/q0 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_6/q1 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_6/q2 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_7/q0 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_7/q1 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_8/q0 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_8/q1 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_9/q0 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/nls_ses/metadata_9/q1 | failed | 0.0 | Ollama call failed: HTTP Error 500: Internal Server Error |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_0/q0 | completed | 0.8387 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_1/q0 | completed | 0.3729 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_10/q0 | completed | 0.5556 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_11/q0 | completed | 0.6182 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_12/q0 | completed | 0.5556 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_13/q0 | completed | 0.7 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_14/q0 | completed | 0.4932 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_2/q0 | completed | 0.7143 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_3/q0 | completed | 0.8571 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_4/q0 | completed | 0.5079 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_5/q0 | completed | 0.7143 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_6/q0 | completed | 0.5231 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_7/q0 | completed | 0.2642 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_8/q0 | completed | 0.6316 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/requirements_engineering_for_ML_enabled_systems/metadata_9/q0 | completed | 0.6182 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/worldbank_education_gdp/metadata_0/q0 | completed | 0.1856 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/worldbank_education_gdp/metadata_0/q1 | completed | 0.2366 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/worldbank_education_gdp/metadata_1/q0 | completed | 0.3239 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/worldbank_education_gdp/metadata_2/q0 | completed | 0.281 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/worldbank_education_gdp/metadata_3/q0 | completed | 0.1575 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/worldbank_education_gdp/metadata_4/q0 | completed | 0.2051 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/worldbank_education_gdp_indicators/metadata_0/q0 | completed | 0.2745 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/worldbank_education_gdp_indicators/metadata_0/q1 | completed | 0.48 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/worldbank_education_gdp_indicators/metadata_1/q0 | completed | 0.3733 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/worldbank_education_gdp_indicators/metadata_2/q0 | completed | 0.5574 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/worldbank_education_gdp_indicators/metadata_3/q0 | completed | 0.3 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | real/worldbank_education_gdp_indicators/metadata_4/q0 | completed | 0.386 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_0_0/metadata_0/q189 | completed | 0.8276 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_0_1/metadata_2/q210 | completed | 0.4583 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_0_2/metadata_0/q190 | completed | 0.6786 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_0_2/metadata_3/q203 | completed | 0.4762 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_0_2/metadata_4/q208 | completed | 0.449 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_0_3/metadata_0/q191 | completed | 0.7037 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_0_3/metadata_1/q192 | completed | 0.5614 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_0_3/metadata_2/q195 | completed | 0.5823 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_0_3/metadata_3/q201 | completed | 0.7308 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_0_3/metadata_4/q207 | completed | 0.5417 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_0_3/metadata_5/q211 | completed | 0.6667 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_1_1/metadata_3/q215 | completed | 0.8116 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_1_2/metadata_0/q193 | completed | 0.5116 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_1_2/metadata_1/q196 | completed | 0.6897 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_1_2/metadata_3/q212 | completed | 0.4727 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_2_1/metadata_0/q198 | completed | 0.6154 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/ancient-languages_2_1/metadata_1/q204 | completed | 0.4528 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_0/metadata_0/q932 | completed | 0.4658 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_1/metadata_1/q957 | completed | 0.5405 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_2/metadata_1/q940 | completed | 0.5172 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_2/metadata_4/q954 | completed | 0.5862 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_2/metadata_5/q960 | completed | 0.5867 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_2/metadata_6/q966 | completed | 0.7018 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_2/metadata_7/q967 | completed | 0.6102 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_3/metadata_0/q933 | completed | 0.5574 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_3/metadata_1/q934 | completed | 0.4932 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_3/metadata_10/q964 | completed | 0.6122 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_3/metadata_2/q937 | completed | 0.5 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_3/metadata_3/q938 | completed | 0.6038 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_3/metadata_4/q941 | completed | 0.3607 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_3/metadata_5/q942 | completed | 0.3125 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_3/metadata_6/q945 | completed | 0.4561 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_3/metadata_7/q946 | completed | 0.6923 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_3/metadata_8/q952 | completed | 0.5417 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_0_3/metadata_9/q958 | completed | 0.5424 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_1_1/metadata_3/q969 | completed | 0.4932 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_1_2/metadata_0/q935 | completed | 0.7037 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_1_2/metadata_2/q943 | completed | 0.4375 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_1_2/metadata_3/q947 | completed | 0.25 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_2_1/metadata_0/q949 | completed | 0.4507 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/artificial-ecosystems_2_1/metadata_2/q961 | completed | 0.6102 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_0/metadata_0/q771 | completed | 0.8119 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_1/metadata_0/q788 | completed | 0.6939 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_2/metadata_1/q777 | completed | 0.4839 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_2/metadata_3/q785 | completed | 0.5161 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_2/metadata_5/q796 | completed | 0.3729 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_2/metadata_7/q804 | completed | 0.3333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_0/q772 | completed | 0.6667 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_1/q775 | completed | 0.5714 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_10/q797 | completed | 0.4068 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_11/q798 | completed | 0.4918 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_12/q801 | completed | 0.4528 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_13/q802 | completed | 0.5 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_2/q778 | completed | 0.5938 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_3/q779 | completed | 0.4058 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_4/q782 | completed | 0.5625 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_5/q783 | completed | 0.383 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_6/q789 | completed | 0.0816 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_7/q790 | completed | 0.5 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_8/q791 | completed | 0.5 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_0_3/metadata_9/q794 | completed | 0.5283 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_1_2/metadata_0/q773 | completed | 0.4783 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_1_2/metadata_2/q780 | completed | 0.3404 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_1_2/metadata_4/q792 | completed | 0.5574 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_1_2/metadata_6/q799 | completed | 0.48 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/astronomy_2_1/metadata_1/q805 | completed | 0.4167 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_0/metadata_0/q3 | completed | 0.6027 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_1/metadata_0/q13 | completed | 0.3288 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_1/metadata_2/q27 | completed | 0.5424 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_1/metadata_3/q35 | completed | 0.4267 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_2/metadata_1/q10 | completed | 0.2963 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_2/metadata_2/q16 | completed | 0.3704 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_2/metadata_3/q17 | completed | 0.36 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_3/metadata_0/q4 | completed | 0.4 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_3/metadata_1/q5 | completed | 0.3103 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_3/metadata_2/q8 | completed | 0.3265 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_3/metadata_3/q14 | completed | 0.4528 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_3/metadata_4/q21 | completed | 0.459 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_3/metadata_5/q22 | completed | 0.566 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_3/metadata_6/q28 | completed | 0.4912 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_3/metadata_7/q29 | completed | 0.5357 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_0_3/metadata_8/q30 | completed | 0.5 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_1_1/metadata_1/q19 | completed | 0.3421 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_1_2/metadata_0/q6 | completed | 0.4407 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_1_2/metadata_3/q23 | completed | 0.4082 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/board-games_1_2/metadata_4/q31 | completed | 0.6667 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_0/metadata_0/q529 | completed | 0.6154 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_1/metadata_1/q552 | completed | 0.1408 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_2/metadata_0/q533 | completed | 0.5429 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_2/metadata_3/q549 | completed | 0.4737 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_3/metadata_0/q530 | completed | 0.6207 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_3/metadata_1/q531 | completed | 0.6538 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_3/metadata_2/q534 | completed | 0.7188 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_3/metadata_3/q535 | completed | 0.7105 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_3/metadata_4/q538 | completed | 0.72 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_3/metadata_5/q539 | completed | 0.5185 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_3/metadata_6/q540 | completed | 0.8 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_3/metadata_7/q544 | completed | 0.4643 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_0_3/metadata_8/q547 | completed | 0.4583 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_1_2/metadata_1/q536 | completed | 0.5763 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_1_2/metadata_2/q545 | completed | 0.3333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/coding-competitions_2_1/metadata_0/q541 | completed | 0.3714 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_0_1/metadata_1/q726 | completed | 0.4407 | token_f1 vs gold hypothesis |

## Notes

- DiscoveryBench: token-F1 of hypothesis vs gold answer key (real + synth test).
- DiscoveryWorld: discovery statements plus critical-question probes from theme/difficulty/seed inventory.
- Cyber-SecOps-ES: evidence-grounded extraction against sealed answer key (unsealed locally).
- Cyber-AIT-ADS: attack-stage classification from AMiner alert windows across hosts.
- Confidence is not used; scores are deterministic graders.
- Long runs checkpoint to `multi-benchmark-checkpoint.json` every N scenarios.
