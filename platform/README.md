# Investigation lab

Python C0–C7 experiment runner. Experiments run from the terminal against a
**locally deployed Ollama** LLM (default) or the offline reference
investigator. `python3 -m app explore` opens a read-only browser for saved
pack files and trajectories.

## Install

Python 3.10 or newer. Commands below run from `platform/`. Ollama is local:
the lab calls `http://127.0.0.1:11434` and does not use an API key. Point at
another server with `--ollama-url` or `OLLAMA_HOST`.

```bash
# Ollama. https://ollama.com/download — on Linux:
# curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull llama3.2:1b
# any tag already on disk works; names must match `ollama list`

# Lab
python3 -m pip install -r requirements.txt
python3 -m app health --provider ollama --model llama3.2:1b
```

`health` prints the models Ollama is serving. The run fails if that list does
not include the `--model` tag.

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

# Run each new dataset in its own session/output dir (preferred)
LAB_STEP_DELAY=0 python3 scripts/run_converted_packs_suite.py \
  --provider ollama --model llama3.2:1b --tools 2 --workers 2 \
  --datasets SOC-AgentBench --out reports/c0c7-soc

LAB_STEP_DELAY=0 python3 scripts/run_converted_packs_suite.py \
  --provider ollama --model llama3.2:1b --tools 2 --workers 2 \
  --datasets ExCyTIn-Bench --out reports/c0c7-excytin
```

DiscoveryBench/DiscoveryWorld are not converted.

## Test a local Ollama model

Unit tests stay offline. They do not call Ollama:

```bash
python3 -m pytest tests
```

A live check uses a model from `ollama list`. One condition on the sample
incident:

```bash
python3 -m app run C3 --provider ollama --model llama3.2:1b \
  --pack data/sample_incident.json --tools 2
```

All eight conditions on that same pack. This writes
`reports/experiment-report.md`. Read it with `python3 -m app report`.

```bash
python3 -m app suite --provider ollama --model llama3.2:1b \
  --pack data/sample_incident.json --tools 2
```

One converted pack, written as a suite directory the result explorer can open.
Convert the benchmarks first (Converted cyber packs, above). `--tools 2` caps C2, C3, and C7.
`--workers 1` keeps a single local model from running two packs at once.
`--limit 1` stops after the first pack.

```bash
LAB_STEP_DELAY=0 python3 scripts/run_converted_packs_suite.py \
  --provider ollama --model llama3.2:1b --tools 2 --workers 1 \
  --runtime 1800 --limit 1 --datasets SOC-AgentBench \
  --out reports/smoke-ollama
```

Swap in `qwen2.5:14b`, `qwen2.5:3b`, or another pulled tag the same way.
`python3 -m app … --provider ollama` with no `--model` uses `qwen2.5:14b`.
The converted-pack script defaults to `qwen2.5:3b`.

## Result explorer

Read-only browser over a suite directory. It does not start runs or write the
lab database.

```bash
python3 -m app explore
# http://127.0.0.1:8765
# python3 -m app explore --host 127.0.0.1 --port 8765
```

Open that URL, pick a suite (the smoke above is `smoke-ollama`), pick an
incident, then click a condition. The table is the pack summary: status,
verdict, confidence, tool count, knowledge count. The click loads that run's
report and event trail from `lab-w*.sqlite3`. An in-progress pack is listed
from the database before its summary file exists. Ground truth stays in the
pack file and is not shown. Stop the server with Ctrl-C.

A directory under `reports/` is listed when it contains `packs/*.json`,
`lab-w*.sqlite3`, or `c0c7-table.md`. `run_converted_packs_suite.py` writes
those. `python3 -m app suite` writes `experiment-report.md` and stores the
trajectory in `var/lab.sqlite3` (or `LAB_DB`); read that report with
`python3 -m app report`.

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
