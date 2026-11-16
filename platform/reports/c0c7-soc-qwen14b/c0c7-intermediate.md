# C0–C7 intermediate results — SOC-AgentBench / qwen2.5:14b

- Packs completed: **73/120**
- Packs failed: **1** (`soc-soc-000045`)
- Model: `ollama:qwen2.5:14b` · tools=2 · workers=1 · num_ctx=4096
- Accuracy = match to sealed `ground_truth.label` (scored offline; labels never reach non-C6 model context)

| Condition | n | Acc. | Malicious | Benign | Mean conf. | Med. conf. | Mean tools | Mean KB |
|-----------|--:|-----:|----------:|-------:|-----------:|-----------:|-----------:|--------:|
| C0 | 73 | 50.7% | 32 (44%) | 41 (56%) | 0.61 | 0.58 | 0.00 | 0.00 |
| C1 | 73 | 56.2% | 40 (55%) | 33 (45%) | 0.61 | 0.58 | 0.00 | 1.00 |
| C2 | 73 | 80.8% | 60 (82%) | 13 (18%) | 0.61 | 0.58 | 2.00 | 0.00 |
| C3 | 73 | 82.2% | 59 (81%) | 14 (19%) | 0.61 | 0.58 | 2.00 | 0.00 |
| C4 | 73 | 93.2% | 73 (100%) | 0 (0%) | 0.60 | 0.58 | 2.00 | 1.00 |
| C5 | 73 | 84.9% | 67 (92%) | 6 (8%) | 0.61 | 0.58 | 0.00 | 1.00 |
| C6 | 73 | 56.2% | 36 (49%) | 37 (51%) | 0.61 | 0.58 | 0.00 | 1.00 |
| C7 | 73 | 83.6% | 58 (79%) | 15 (21%) | 0.61 | 0.58 | 2.00 | 0.00 |

**Ground-truth mix in completed packs:** benign=5, malicious=68

## Per-condition accuracy vs ablation ladder

| | C0 Raw | C1 KB | C2 Search | C3 Full | C4 Fixed | C5 Matched | C6 Oracle evid. | C7 Oracle plan |
|--|------:|------:|----------:|--------:|---------:|-----------:|----------------:|---------------:|
| Acc. | 50.7% | 56.2% | 80.8% | 82.2% | 93.2% | 84.9% | 56.2% | 83.6% |
| % mal | 44% | 55% | 82% | 81% | 100% | 92% | 49% | 79% |

## Notes
- Intermediate snapshot; suite still running.
- Pack `soc-soc-000045` failed at C5 (`Matched C3 run has zero evidence`) and is excluded from n.
