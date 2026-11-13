# Investigation lab

Python C0–C7 experiment runner. There is no frontend. Experiments run from
the terminal against a **locally deployed Ollama** LLM (default) or the
offline reference investigator.

## Setup

```bash
# 1. Local model (skip if using --provider reference)
ollama serve
ollama pull llama3.2:1b

# 2. Lab
python3 -m pip install -r requirements.txt
```

## Run experiments

From `platform/`:

```bash
# Full C0–C7 matrix on the sample incident; writes reports/
python3 -m app suite --provider ollama --model llama3.2:1b

# One condition
python3 -m app run C3 --provider ollama --model llama3.2:1b

# Offline baseline (no Ollama)
python3 -m app suite --provider reference

# Your own pack
python3 -m app suite --pack data/sample_incident.json --provider ollama

# Typed parts
python3 -m app load --pack data/sample_incident.json
python3 -m app load --kind telemetry --file telemetry.json --dataset ds-...

# Inspect isolation
python3 -m app architecture C0
python3 -m app architecture C3
python3 -m app conditions
python3 -m app health
python3 -m app report
```

C5 uses the completed C3 run from the same suite. There is no silent
fallback from Ollama to the reference investigator.

## Models

- **Ollama** — default. Local, no cloud key.
- **Reference investigator** — deterministic offline baseline.
- **GPT / Claude / Grok / Groq** — `python3 -m app key openai --api-key sk-...`

Keys stay in the local SQLite store and never enter trajectories.

## Typed packs

| Pack | Used by | CLI |
|---|---|---|
| Alert | all conditions | `--kind alert` |
| Telemetry | C0–C5 | `--kind telemetry` |
| Knowledge corpus | C1, C3–C7 | `--kind knowledge` |
| C4 query pack | C4 | `--kind query_pack` |
| C6 oracle evidence | C6 | `--kind oracle_evidence` |
| C7 oracle plan | C7 | `--kind oracle_plan` |
| Ground truth | sealed | `--kind ground_truth` |

### Converted cyber packs (C0–C7 dataset points)

After downloading benchmarks, convert SecOps-ES, AIT-ADS, SOC-AgentBench, and
ExCyTIn-Bench scenarios into incident packs the suite can load:

```bash
python3 scripts/download_benchmarks.py
python3 scripts/convert_benchmarks_to_packs.py
# packs → data/packs/{secops,ait_ads,soc_agent,excytin}/ + data/packs/manifest.json

# Example: run the full C0–C7 matrix on one converted pack
python3 -m app suite --pack data/packs/secops/secops-q-c01-root-cause.json --provider ollama --model qwen2.5:3b

# Run only the newly added datasets
LAB_STEP_DELAY=0 python3 scripts/run_converted_packs_suite.py \
  --provider ollama --model llama3.2:1b --tools 2 --workers 2 \
  --datasets SOC-AgentBench,ExCyTIn-Bench \
  --out reports/c0c7-soc-excytin
```

DiscoveryBench/DiscoveryWorld are not converted.

## Experiment report

`python3 -m app suite` writes `reports/experiment-report.md` and `.json`.

Report `confidence` is **evidence-derived** (telemetry heuristics on the
records available in that run). Model self-reported confidence is ignored.
Result tables include a **Model** column.

## Multi-dataset benchmarks

Download DiscoveryBench, DiscoveryWorld, SecOps-ES, and AIT-ADS, then score
`qwen2.5` (or another Ollama model) per scenario:

```bash
python3 scripts/download_benchmarks.py
# All unique scenarios (no replica tiling). Use --limit N to cap or tile.
python3 -m app bench --provider ollama --model qwen2.5:3b --limit 0 --out reports/benchmarks
```

`--limit 0` runs the full unique inventory (~1256 after download). Positive
`--limit` values larger than the inventory tile `repN` replicas.

Writes `reports/benchmarks/multi-benchmark-report.md` with Model, Dataset,
Scenario, and Score.

## Generated runners

`python3 -m app generate C3 --provider ollama` prints an in-process script
that pins condition, pack, model, and budgets. It does not call HTTP.

## Tests

```bash
python3 -m pytest tests
```
