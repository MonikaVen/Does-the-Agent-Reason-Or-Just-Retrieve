# Multi-benchmark report

- Generated: `2026-11-11T12:07:21.394Z`
- Model: `ollama:qwen2.5:3b`
- Queued: `1256`
- Completed rows: `1256`

## Dataset scores

| Model | Dataset | Scenarios | Completed | Mean score |
|---|---|---|---|---|
| qwen2.5:3b | Cyber-SecOps-ES | 54 | 54 | 0.5569 |
| qwen2.5:3b | Cyber-AIT-ADS | 79 | 79 | 0.4937 |
| qwen2.5:3b | DiscoveryBench | 439 | 417 | 0.4605 |
| qwen2.5:3b | DiscoveryWorld | 684 | 326 | 0.1155 |

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
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_0_2/metadata_1/q731 | completed | 0.5455 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_0_2/metadata_2/q734 | completed | 0.4211 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_0_2/metadata_4/q743 | completed | 0.3684 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_0_3/metadata_0/q720 | completed | 0.4 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_0_3/metadata_1/q727 | completed | 0.5294 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_0_3/metadata_2/q728 | completed | 0.5283 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_0_3/metadata_3/q729 | completed | 0.3636 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_0_3/metadata_4/q732 | completed | 0.76 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_0_3/metadata_5/q738 | completed | 0.375 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_0_3/metadata_6/q741 | completed | 0.549 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_1_0/metadata_0/q718 | completed | 0.5312 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_1_1/metadata_0/q724 | completed | 0.5758 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_1_2/metadata_0/q721 | completed | 0.4737 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_1_2/metadata_3/q739 | completed | 0.4478 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_2_1/metadata_1/q735 | completed | 0.4615 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/digital-artistry_2_1/metadata_2/q744 | completed | 0.4789 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/futuristic-technology_0_0/metadata_0/q647 | completed | 0.1918 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/futuristic-technology_0_2/metadata_2/q657 | completed | 0.5915 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/futuristic-technology_0_3/metadata_0/q648 | completed | 0.4103 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/futuristic-technology_0_3/metadata_1/q651 | completed | 0.6875 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/futuristic-technology_1_1/metadata_1/q658 | completed | 0.4557 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/futuristic-technology_1_2/metadata_0/q649 | completed | 0.5 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/futuristic-technology_1_2/metadata_1/q652 | completed | 0.3556 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/futuristic-technology_2_1/metadata_0/q654 | completed | 0.7143 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_0/metadata_0/q999 | completed | 0.1846 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_2/metadata_0/q1002 | completed | 0.4898 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_2/metadata_1/q1007 | completed | 0.1702 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_2/metadata_3/q1019 | completed | 0.3488 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_2/metadata_4/q1025 | completed | 0.5075 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_2/metadata_5/q1028 | completed | 0.5366 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_3/metadata_0/q1000 | completed | 0.4783 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_3/metadata_1/q1003 | completed | 0.3404 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_3/metadata_10/q1026 | completed | 0.375 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_3/metadata_2/q1004 | completed | 0.4407 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_3/metadata_3/q1005 | completed | 0.4561 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_3/metadata_4/q1011 | completed | 0.3889 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_3/metadata_5/q1012 | completed | 0.6216 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_3/metadata_6/q1013 | completed | 0.4706 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_3/metadata_7/q1016 | completed | 0.5246 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_3/metadata_8/q1017 | completed | 0.5556 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_0_3/metadata_9/q1023 | completed | 0.5278 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_1_1/metadata_0/q1009 | completed | 0.3913 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_1_1/metadata_2/q1030 | completed | 0.3944 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_1_2/metadata_2/q1014 | completed | 0.6429 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/impressionist-art_2_1/metadata_1/q1020 | completed | 0.4348 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_0_0/metadata_0/q372 | completed | 0.4828 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_0_1/metadata_0/q373 | completed | 0.5574 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_0_1/metadata_1/q388 | completed | 0.7407 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_0_2/metadata_0/q378 | completed | 0.7463 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_0_2/metadata_1/q379 | completed | 0.48 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_0_2/metadata_2/q380 | completed | 0.2 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_0_2/metadata_3/q381 | completed | 0.2857 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_0_3/metadata_0/q374 | completed | 0.3077 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_0_3/metadata_1/q375 | completed | 0.1395 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_0_3/metadata_2/q376 | completed | 0.4615 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_0_3/metadata_3/q382 | completed | 0.7857 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_0_3/metadata_4/q383 | completed | 0.6087 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/machine-learning_1_2/metadata_1/q384 | completed | 0.4 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_0_0/metadata_0/q808 | completed | 0.4667 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_0_2/metadata_0/q812 | completed | 0.48 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_0_3/metadata_0/q809 | completed | 0.5507 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_0_3/metadata_1/q810 | completed | 0.5517 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_0_3/metadata_2/q816 | completed | 0.4308 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_0_3/metadata_3/q820 | completed | 0.8333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_0_3/metadata_4/q826 | completed | 0.3077 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_0_3/metadata_5/q829 | completed | 0.4935 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_1_1/metadata_2/q824 | completed | 0.7719 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_1_2/metadata_1/q821 | completed | 0.4483 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_1_2/metadata_2/q827 | completed | 0.3929 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_1_2/metadata_3/q830 | completed | 0.5333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_2_1/metadata_0/q813 | completed | 0.5116 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_2_1/metadata_1/q817 | completed | 0.4727 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/molecular-gastronomy_2_1/metadata_3/q832 | completed | 0.4 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/neuroscience_0_0/metadata_0/q390 | completed | 0.4615 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/neuroscience_0_1/metadata_0/q391 | completed | 0.5652 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/neuroscience_0_1/metadata_1/q397 | completed | 0.3462 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/neuroscience_0_2/metadata_0/q394 | completed | 0.5618 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/neuroscience_0_3/metadata_0/q392 | completed | 0.4074 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/philosophical-debates_0_0/metadata_0/q284 | completed | 0.65 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/philosophical-debates_0_3/metadata_0/q285 | completed | 0.5106 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/philosophical-debates_0_3/metadata_1/q286 | completed | 0.4 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/philosophical-debates_0_3/metadata_2/q292 | completed | 0.4783 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/philosophical-debates_0_3/metadata_3/q298 | completed | 0.6 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/philosophical-debates_1_2/metadata_0/q287 | completed | 0.4333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/philosophical-debates_1_2/metadata_1/q293 | completed | 0.5588 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/philosophical-debates_1_2/metadata_2/q299 | completed | 0.6207 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/philosophical-debates_2_1/metadata_0/q289 | completed | 0.4375 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/philosophical-debates_2_1/metadata_1/q295 | completed | 0.5333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/robotics_0_1/metadata_0/q325 | completed | 0.2903 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/robotics_0_1/metadata_1/q326 | completed | 0.386 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/robotics_0_2/metadata_0/q322 | completed | 0.4533 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/robotics_0_2/metadata_1/q329 | completed | 0.386 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/robotics_0_3/metadata_0/q319 | completed | 0.3662 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/robotics_0_3/metadata_1/q320 | completed | 0.3582 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/robotics_0_3/metadata_2/q327 | completed | 0.3333 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/robotics_1_0/metadata_0/q317 | completed | 0.3636 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryBench | synth/robotics_2_1/metadata_1/q330 | completed | 0.1455 | token_f1 vs gold hypothesis |
| qwen2.5:3b | DiscoveryWorld | Tutorial/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Tutorial/Normal/seed0/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Tutorial/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Tutorial/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed0 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed1 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed2 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed3 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed4 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Easy/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Combinatorial Chemistry/Challenge/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed0 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed0/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed1 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed1/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed2 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed2/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed3 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed3/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed4 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed4/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Easy/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed0/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed0/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed1/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed1/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed2/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed2/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed3/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed3/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed4/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed4/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed0 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed0/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed0/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed1 | completed | 0.5 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed1/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed1/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed2 | completed | 0.5 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed2/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed2/cq2 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed3 | completed | 0.5 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed3/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed3/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed4/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Archaeology Dating/Challenge/seed4/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed4 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Easy/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed0 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed4 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed1 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Plant Nutrients/Challenge/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed0 | completed | 0.4286 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed0/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed0/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed1 | completed | 0.5714 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed1/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed2 | completed | 0.5714 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed2/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed3/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed3/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed4 | completed | 0.1429 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed4/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Easy/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed0/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed0/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed1/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed1/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed2/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed2/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed3/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed3/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed4/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed0/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed0/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed1/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed1/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed2 | completed | 0.4545 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed2/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed2/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed3/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed3/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed4/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed4/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Reactor Lab/Challenge/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed0/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed1/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed2/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed3/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Easy/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed0/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed1/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed2/cq1 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed3/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed4/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed4/cq1 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed0/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed0/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed1/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed1/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed2/cq1 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed2/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed3/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed3/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed4/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Lost in Translation/Challenge/seed4/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed0/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed1/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed2/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed3/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed4/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Easy/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed0 | completed | 0.5 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed0/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed0/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed1/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed1/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed2/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed2/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed3/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed3/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed4/cq1 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Normal/seed4/cq2 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed0/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed4/cq0 | completed | 0.5 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Space Sick/Challenge/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Easy/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed0/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed1/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed2/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed3/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed4/cq0 | completed | 0.0 | critical-question yes/no + keyword support |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Proteomics/Challenge/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed0/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed0/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed0/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed1/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed1/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed1/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed2/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed2/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed2/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed3 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed3/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed3/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed3/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed4 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed4/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed4/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Easy/seed4/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed0/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed0/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed0/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed1/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed1/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed1/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed2/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed2/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed2/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed3 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed3/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed3/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed3/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed4 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed4/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed4/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Normal/seed4/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed0/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed0/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed0/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed1/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed1/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed1/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed2/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed2/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed2/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed3 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed3/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed3/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed3/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed4 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed4/cq0 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed4/cq1 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | It's (not) Rocket Science!/Challenge/seed4/cq2 | failed | 0.0 | 'float' object cannot be interpreted as an integer |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed0/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed1/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed2/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed3/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed4/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Dialog Test/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed0/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed1/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed2/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed3/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed4/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Place Test/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed0/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed1/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed2/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed3/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed4/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Pick and Give Test/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed0/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed1/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed2/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed3/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed4/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Instrument Measurement Test/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed0/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed1/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed2/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed3/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed4/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors Test/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed0/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed1/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed2/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed3/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed4/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Doors with Keys Test/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed0/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed1/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed2/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed3/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed4/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Navigation in a House Test/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed0 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed0/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed1 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed1/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed2 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed2/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed3 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed3/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed4 | completed | 1.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed4/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Search Test/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed0/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed1/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed2/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed3/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed4/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Discovery Feed Test/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed0 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed0/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed0/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed0/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed1 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed1/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed1/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed1/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed2 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed2/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed2/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed2/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed3 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed3/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed3/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed3/cq2 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed4 | completed | 0.0 | critical-hypothesis keyword coverage |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed4/cq0 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed4/cq1 | skipped | 0.0 | no critical question at index |
| qwen2.5:3b | DiscoveryWorld | Small Skills: Moving Agents Test/Normal/seed4/cq2 | skipped | 0.0 | no critical question at index |

## Notes

- DiscoveryBench: token-F1 of hypothesis vs gold answer key (real + synth test).
- DiscoveryWorld: discovery statements plus critical-question probes from theme/difficulty/seed inventory.
- Cyber-SecOps-ES: evidence-grounded extraction against sealed answer key (unsealed locally).
- Cyber-AIT-ADS: attack-stage classification from AMiner alert windows across hosts.
- Confidence is not used; scores are deterministic graders.
- Long runs checkpoint to `multi-benchmark-checkpoint.json` every N scenarios.
