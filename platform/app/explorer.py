"""Local read-only browser for suite pack files and SQLite trajectories."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .artifacts import ArtifactError, list_packs, list_suites, pack_detail, run_detail

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Artifact explorer</title>
<style>
  :root { color-scheme: light; --line: #d7d7d4; --ink: #1c1c1a; --muted: #5c5c57; --bg: #f6f6f4; --panel: #fff; --accent: #1f4b99; }
  * { box-sizing: border-box; }
  body { margin: 0; font: 14px/1.45 ui-sans-serif, system-ui, sans-serif; color: var(--ink); background: var(--bg); }
  header { padding: 16px 20px 8px; }
  h1 { font-size: 20px; margin: 0 0 4px; }
  p.note { margin: 0; color: var(--muted); }
  .layout { display: grid; grid-template-columns: 320px 1fr; gap: 16px; padding: 8px 20px 24px; }
  .panel { background: var(--panel); border: 1px solid var(--line); padding: 12px; }
  label { display: block; font-size: 12px; color: var(--muted); margin-bottom: 4px; }
  select, input { width: 100%; padding: 6px 8px; border: 1px solid var(--line); background: #fff; color: inherit; }
  ul.packs { list-style: none; margin: 12px 0 0; padding: 0; max-height: calc(100vh - 180px); overflow: auto; }
  ul.packs button { width: 100%; text-align: left; border: 0; border-bottom: 1px solid var(--line); background: transparent; padding: 8px 4px; cursor: pointer; color: inherit; }
  ul.packs button.active { background: #e8eef8; }
  .meta { color: var(--muted); font-size: 12px; }
  table { width: 100%; border-collapse: collapse; }
  th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--line); vertical-align: top; }
  th { font-size: 12px; color: var(--muted); font-weight: 600; }
  tr.clickable { cursor: pointer; }
  tr.clickable.active { background: #e8eef8; }
  pre { white-space: pre-wrap; word-break: break-word; background: #f3f3f1; padding: 8px; margin: 4px 0 0; font-size: 12px; }
  .status { font-size: 12px; }
  .failed { color: #8a2b2b; }
  .running { color: var(--accent); }
  h2 { font-size: 16px; margin: 0 0 8px; }
  h3 { font-size: 14px; margin: 16px 0 8px; }
  .error { color: #8a2b2b; }
</style>
</head>
<body>
<header>
  <h1>Artifact explorer</h1>
  <p class="note">Read-only view of pack summaries and SQLite trajectories. Ground truth stays in the pack files and is not shown.</p>
</header>
<div class="layout">
  <aside class="panel">
    <label for="suite">Suite</label>
    <select id="suite"></select>
    <label for="query" style="margin-top:10px">Incident</label>
    <input id="query" placeholder="Filter incident id" />
    <ul class="packs" id="packs"></ul>
  </aside>
  <main class="panel" id="detail">
    <p class="note">Choose a suite.</p>
  </main>
</div>
<script>
const suiteEl = document.querySelector("#suite");
const queryEl = document.querySelector("#query");
const packsEl = document.querySelector("#packs");
const detailEl = document.querySelector("#detail");
let catalog = null;
let selected = null;
let selectedRun = null;

function esc(value) {
  return String(value ?? "").replace(/[&<>"]/g, ch => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[ch]));
}

async function loadSuites() {
  const data = await fetch("/api/suites").then(r => r.json());
  suiteEl.innerHTML = data.suites.map(s => `<option value="${esc(s.name)}">${esc(s.name)} · ${s.pack_files} packs</option>`).join("");
  if (data.suites.length) loadPacks();
  else detailEl.innerHTML = "<p class='note'>No suite directories under reports/.</p>";
}

async function loadPacks() {
  const suite = suiteEl.value;
  catalog = await fetch("/api/packs?suite=" + encodeURIComponent(suite)).then(r => r.json());
  selected = catalog.packs.find(p => p.incident_id === selected) ? selected : (catalog.running_incident || (catalog.packs[0] && catalog.packs[0].incident_id));
  renderPacks();
  if (selected) showPack(selected);
}

function renderPacks() {
  const q = queryEl.value.trim().toLowerCase();
  const rows = catalog.packs.filter(p => !q || p.incident_id.toLowerCase().includes(q));
  packsEl.innerHTML = rows.map(p => {
    const verdicts = p.runs.map(r => r.verdict ? r.verdict[0] : (r.status === "running" ? "…" : "·")).join("");
    return `<li><button class="${p.incident_id === selected ? "active" : ""}" data-id="${esc(p.incident_id)}"><strong>${esc(p.incident_id)}</strong><div class="meta">${esc(p.model || "")} · ${p.completed || 0} done${p.failed ? " · " + p.failed + " failed" : ""}${p.on_disk ? "" : " · in progress"}</div><div class="meta">${esc(verdicts)}</div></button></li>`;
  }).join("") || "<li class='meta'>No packs</li>";
}

function showPack(id) {
  selected = id;
  selectedRun = null;
  renderPacks();
  const pack = catalog.packs.find(p => p.incident_id === id);
  if (!pack) return;
  const rows = pack.runs.map(run => `<tr class="clickable" data-run="${esc(run.run_id || "")}"><td>${esc(run.condition)}</td><td class="status ${esc(run.status)}">${esc(run.status)}</td><td>${esc(run.verdict || "")}</td><td>${run.confidence ?? ""}</td><td>${run.tool_observations ?? ""}</td><td>${run.knowledge_retrievals ?? ""}</td><td>${esc(run.error || "")}</td></tr>`).join("");
  detailEl.innerHTML = `
    <h2>${esc(pack.incident_id)}</h2>
    <p class="note">${esc(pack.dataset || "")} ${esc(pack.scenario || "")} · ${esc(pack.model || pack.provider || "")}</p>
    ${pack.pack_error ? `<p class="error">${esc(pack.pack_error)}</p>` : ""}
    <table>
      <thead><tr><th>Condition</th><th>Status</th><th>Verdict</th><th>Conf.</th><th>Tools</th><th>KB</th><th>Error</th></tr></thead>
      <tbody>${rows || "<tr><td colspan='7'>No condition rows yet.</td></tr>"}</tbody>
    </table>
    <div id="run"></div>`;
}

async function showRun(runId) {
  if (!runId) return;
  selectedRun = runId;
  detailEl.querySelectorAll("tr.clickable").forEach(row => row.classList.toggle("active", row.dataset.run === runId));
  const box = document.querySelector("#run");
  box.innerHTML = "<p class='note'>Loading trajectory…</p>";
  const res = await fetch("/api/run?suite=" + encodeURIComponent(suiteEl.value) + "&run_id=" + encodeURIComponent(runId));
  const data = await res.json();
  if (!res.ok) {
    box.innerHTML = `<p class="error">${esc(data.error)}</p>`;
    return;
  }
  const report = data.report ? `<h3>Report</h3><pre>${esc(JSON.stringify(data.report, null, 2))}</pre>` : "";
  const events = (data.events || []).map(ev => `<h3>${esc(ev.sequence)} · ${esc(ev.kind)} · ${esc(ev.service)}</h3><p class="meta">${esc(ev.timestamp)} ${esc(ev.stage || "")}${ev.truncated ? " · payload truncated" : ""}</p><pre>${esc(JSON.stringify(ev.payload, null, 2))}</pre>`).join("");
  box.innerHTML = `<p class="note">${esc(data.database)} · ${esc(data.status)} · ${esc(data.model_profile || "")}</p>${data.error ? `<p class="error">${esc(data.error)}</p>` : ""}${report}<h3>Trajectory</h3>${events || "<p class='note'>No events.</p>"}`;
}

suiteEl.addEventListener("change", () => { selected = null; loadPacks(); });
queryEl.addEventListener("input", renderPacks);
packsEl.addEventListener("click", ev => {
  const button = ev.target.closest("button");
  if (button) showPack(button.dataset.id);
});
detailEl.addEventListener("click", ev => {
  const row = ev.target.closest("tr.clickable");
  if (row && row.dataset.run) showRun(row.dataset.run);
});
loadSuites();
</script>
</body>
</html>
"""


class ExplorerHandler(BaseHTTPRequestHandler):
    reports_root: Path

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/":
                self._send(200, PAGE.encode(), "text/html; charset=utf-8")
                return
            if parsed.path == "/api/suites":
                self._json(200, {"suites": list_suites(self.reports_root)})
                return
            query = parse_qs(parsed.query)
            suite = _one(query, "suite")
            if parsed.path == "/api/packs":
                self._json(200, list_packs(suite, self.reports_root))
                return
            if parsed.path == "/api/pack":
                self._json(200, pack_detail(suite, _one(query, "incident"), self.reports_root))
                return
            if parsed.path == "/api/run":
                self._json(200, run_detail(suite, _one(query, "run_id"), self.reports_root))
                return
            self._json(404, {"error": "not found"})
        except ArtifactError as exc:
            self._json(400, {"error": str(exc)})
        except Exception as exc:  # noqa: BLE001 — surface a message, keep the server up
            self._json(500, {"error": str(exc)})

    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        self._send(status, json.dumps(payload).encode(), "application/json")

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _one(query: dict[str, list[str]], key: str) -> str:
    values = query.get(key) or []
    if not values or not values[0]:
        raise ArtifactError(f"missing {key}")
    return values[0]


def serve(host: str = "127.0.0.1", port: int = 8765, reports_root: Path | None = None) -> ThreadingHTTPServer:
    root = (reports_root or Path(__file__).resolve().parents[1] / "reports").resolve()
    handler = type("BoundExplorerHandler", (ExplorerHandler,), {"reports_root": root})
    server = ThreadingHTTPServer((host, port), handler)
    return server
