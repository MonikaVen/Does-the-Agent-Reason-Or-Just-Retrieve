# Investigation lab

Python FastAPI app plus a frontend that treats the C0–C7 architecture as
the interface. The default model is a **locally deployed Ollama** LLM.

## Setup

```bash
# 1. Local model
ollama serve
ollama pull llama3.2:1b

# 2. Lab
python3 -m pip install -r requirements.txt
LAB_STEP_DELAY=0 python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000

The lab probes `http://127.0.0.1:11434` on startup. If Ollama is up it pins
`ollama` + the pulled model (prefers `llama3.2:1b`). There is no silent
fallback to the reference investigator.

## Models

- **Ollama** — default. Local, no cloud key. Set the base URL if needed.
- **Reference investigator** — deterministic offline baseline.
- **GPT / Claude / Grok / Groq** — save an API key in the lab; keys are stored locally and never written into trajectories.

## Typed uploads

Each button merges one pack onto the selected dataset:

| Pack | Used by |
|---|---|
| Alert | all conditions |
| Telemetry | C0–C5 |
| Knowledge corpus | C1, C3–C7 |
| C4 query pack | C4 |
| C6 oracle evidence | C6 |
| C7 oracle plan | C7 |
| Ground truth | sealed; never sent to the model |

## C0–C7 suite and experiment report

**Run C0–C7 suite** executes the matrix sequentially against the pinned
model (C5 uses the completed C3 run from the same suite). Results are
written to `platform/reports/experiment-report.md` and `.json`.

```bash
curl -X POST http://127.0.0.1:8000/api/experiments/suite \
  -H 'Content-Type: application/json' \
  -d '{"dataset_id":"ds-sample-0042","provider":"ollama","model":"llama3.2:1b","wait":true}'
```

## Experiment code

**Generate experiment code** downloads a pinned Python runner for the current
condition, provider, model, dataset, and budgets.

## Tests

```bash
python3 -m pytest tests
```
