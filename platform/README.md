# Investigation lab

Python FastAPI app plus a frontend that treats the C0–C7 architecture as
the interface: upload incident telemetry, select a condition, run, and
watch services fire.

## Setup

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000

## Incident pack schema

JSON file with:

- `incident_id`
- `alert` (host, timestamp, summary, …)
- `scope` (allowed log sources, time window, hosts)
- `telemetry` — map of source name → list of records, each with `event_id`
- optional `fixed_query_pack` (C4), `oracle_evidence` (C6), `oracle_plan` (C7)

See `data/sample_incident.json`.

## Tests

```bash
python3 -m pip install pytest pytest-asyncio
python3 -m pytest tests
```
