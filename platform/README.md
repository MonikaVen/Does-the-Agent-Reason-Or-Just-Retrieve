# Investigation lab

Python FastAPI app plus a frontend that treats the C0–C7 architecture as
the interface.

## Setup

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000

## Models

- **Reference investigator** — offline structured baseline
- **Ollama** — local, set base URL (default `http://127.0.0.1:11434`)
- **GPT / Claude / Grok / Groq** — save an API key in the lab; keys are stored locally and never written into trajectories

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

## Experiment code

**Generate experiment code** downloads a pinned Python runner for the current
condition, provider, model, dataset, and budgets.

## Tests

```bash
python3 -m pytest tests
```
