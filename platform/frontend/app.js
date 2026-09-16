const state = {
  conditions: [],
  architecture: null,
  datasets: [],
  runs: [],
  c3Runs: [],
  selectedCondition: "C3",
  selectedDataset: null,
  selectedRun: null,
  seenStages: new Set(),
  seenSequences: new Set(),
  liveService: null,
  stream: null,
};

const $ = (id) => document.getElementById(id);

async function api(path, options) {
  const response = await fetch(path, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = data.detail;
    const message = typeof detail === "string" ? detail : JSON.stringify(detail || data);
    throw new Error(message || response.statusText);
  }
  return data;
}

function renderConditions() {
  $("condition-rail").innerHTML = state.conditions
    .map(
      (item) => `
      <button class="cond ${item.id === state.selectedCondition ? "active" : ""}" data-id="${item.id}">
        <strong>${item.id}</strong>
        <span>${item.name}</span>
      </button>`
    )
    .join("");
  for (const button of $("condition-rail").querySelectorAll(".cond")) {
    button.addEventListener("click", () => selectCondition(button.dataset.id));
  }
}

async function selectCondition(id) {
  state.selectedCondition = id;
  renderConditions();
  state.architecture = await api(`/api/architecture?condition=${id}`);
  renderArchitecture();
  $("matched-run").disabled = id !== "C5";
}

function renderArchitecture() {
  const view = state.architecture;
  const profile = view.profile;
  $("canvas-title").textContent = `${view.condition_id} · ${profile.name}`;
  $("canvas-summary").textContent = profile.summary;
  $("stages").innerHTML = view.stages
    .map((stage) => `<li data-stage="${stage.id}">${stage.label}</li>`)
    .join("");
  $("planes").innerHTML = view.planes
    .map(
      (plane) => `
      <article class="plane ${plane.id}">
        <header>
          <strong>${plane.label}</strong>
        </header>
        <p>${plane.blurb}</p>
        <div class="services">
          ${plane.services
            .map(
              (svc) => `
            <div class="svc ${svc.enabled ? "on" : "off"}" data-service="${svc.id}">
              <div class="name">${svc.label}</div>
              <div class="role">${svc.role}</div>
              <div class="badge">${svc.enabled ? "on" : "off"}</div>
            </div>`
            )
            .join("")}
        </div>
      </article>`
    )
    .join("");
}

function renderDatasets() {
  $("dataset-list").innerHTML = state.datasets
    .map((dataset) => {
      const active = dataset.id === state.selectedDataset ? "active" : "";
      return `<button class="chip ${active}" data-id="${dataset.id}">
        ${dataset.name}
        <small>${dataset.incident_id} · ${dataset.record_total} records</small>
      </button>`;
    })
    .join("");
  for (const button of $("dataset-list").querySelectorAll(".chip")) {
    button.addEventListener("click", () => selectDataset(button.dataset.id));
  }
}

async function selectDataset(id) {
  state.selectedDataset = id;
  renderDatasets();
  const dataset = await api(`/api/datasets/${id}`);
  const passport = dataset.passport;
  const counts = Object.entries(passport.record_counts)
    .map(([source, count]) => `<span>${source} ${count}</span>`)
    .join("");
  $("passport").classList.remove("empty");
  $("passport").innerHTML = `
    <dl>
      <dt>Incident</dt><dd class="mono">${passport.incident_id}</dd>
      <dt>Host</dt><dd>${passport.alert.host || "—"}</dd>
      <dt>Alert</dt><dd>${passport.alert.summary || passport.alert.alert_type || "—"}</dd>
      <dt>Window</dt><dd>${(passport.scope.start || "?").slice(11, 16)}–${(passport.scope.end || "?").slice(11, 16)}</dd>
      <dt>Packs</dt>
      <dd>
        ${passport.has_fixed_query_pack ? "C4 query pack · " : ""}
        ${passport.has_oracle_evidence ? "C6 oracle evidence · " : ""}
        ${passport.has_oracle_plan ? "C7 oracle plan" : ""}
        ${!passport.has_fixed_query_pack && !passport.has_oracle_evidence && !passport.has_oracle_plan ? "none" : ""}
      </dd>
    </dl>
    <div class="counts">${counts}</div>`;
}

function renderRuns() {
  $("run-list").innerHTML = state.runs
    .slice(0, 12)
    .map((run) => {
      const active = run.id === state.selectedRun ? "active" : "";
      return `<button class="run-chip ${active}" data-id="${run.id}">
        ${run.condition} · ${run.status}
        <small>${run.id}</small>
      </button>`;
    })
    .join("");
  for (const button of $("run-list").querySelectorAll(".run-chip")) {
    button.addEventListener("click", () => attachRun(button.dataset.id));
  }
  $("matched-run").innerHTML =
    `<option value="">Select a completed C3 run</option>` +
    state.c3Runs
      .map((run) => `<option value="${run.id}">${run.id} · ${run.report?.verdict || "done"}</option>`)
      .join("");
}

function setSignal(text) {
  $("signal").textContent = text;
}

function markStage(stage) {
  if (!stage) return;
  state.seenStages.add(stage);
  for (const item of $("stages").children) {
    item.classList.toggle("current", item.dataset.stage === stage);
    item.classList.toggle("done", state.seenStages.has(item.dataset.stage) && item.dataset.stage !== stage);
  }
}

function markService(serviceId, mode) {
  if (!serviceId) return;
  for (const node of document.querySelectorAll(".svc")) {
    if (mode === "live" && node.dataset.service === serviceId) {
      node.classList.add("live");
      node.querySelector(".badge").textContent = "live";
    } else {
      node.classList.remove("live");
      if (node.classList.contains("on") && node.querySelector(".badge").textContent === "live") {
        node.querySelector(".badge").textContent = "on";
      }
    }
    if (mode !== "live" && node.dataset.service === serviceId) {
      node.classList.add("done");
      node.querySelector(".badge").textContent = mode === "fail" ? "fail" : "fired";
      if (mode === "fail") node.classList.add("fail");
    }
  }
}

function eventLine(event) {
  const why =
    event.payload?.expected_discrimination ||
    event.payload?.reason ||
    event.payload?.summary ||
    event.payload?.message ||
    (event.payload?.record_count != null ? `${event.payload.record_count} records` : "") ||
    (event.payload?.passages ? `${event.payload.passages.length} passages` : "") ||
    event.payload?.stage ||
    "";
  return `<li>
    <div class="meta">${String(event.sequence).padStart(3, "0")} · ${event.service} · ${event.kind}</div>
    <div class="why">${why}</div>
  </li>`;
}

function pushEvent(event) {
  if (event.kind === "eof") return;
  if (event.sequence != null) {
    if (state.seenSequences.has(event.sequence)) return;
    state.seenSequences.add(event.sequence);
  }
  const list = $("events");
  list.insertAdjacentHTML("afterbegin", eventLine(event));
  markStage(event.stage);
  markService(event.service, event.kind === "run_failed" || event.kind === "service_disabled" ? "fail" : "live");
  const hop = event.stage ? `${event.service} · ${event.stage}` : `${event.service} · ${event.kind}`;
  setSignal(hop);
  if (event.kind === "state_updated" || event.kind === "state_initialized") {
    renderState(event.payload);
  }
  if (event.kind === "decision") {
    renderState({
      hypotheses: event.payload.hypotheses,
      unresolved_questions: event.payload.next_question ? [event.payload.next_question] : [],
      known_evidence: event.payload.known_evidence,
    });
  }
  if (event.kind === "report_generated") renderReport(event.payload);
}

function renderState(payload) {
  if (!payload) return;
  const hyps = (payload.hypotheses || [])
    .map((item) => `<div>${item.hypothesis_id}: ${item.claim} <strong>${item.confidence}</strong></div>`)
    .join("");
  const evidence = (payload.known_evidence || []).map((id) => `<span class="pill">${id}</span>`).join("") || "—";
  const entities = payload.entities || {};
  $("state-view").classList.remove("empty");
  $("state-view").innerHTML = `
    <div class="card"><h3>Hypotheses</h3>${hyps || "—"}</div>
    <div class="card"><h3>Evidence ledger</h3>${evidence}</div>
    <div class="card"><h3>Question</h3>${(payload.unresolved_questions || [])[0] || "—"}</div>
    <div class="card"><h3>Budgets</h3>
      tool calls ${payload.budget_state?.tool_calls_used ?? "—"} /
      remaining ${payload.budget_state?.tool_calls_remaining ?? "—"}
    </div>
    <div class="card"><h3>Entities</h3>
      ${(entities.hosts || []).map((x) => `<span class="pill">${x}</span>`).join("")}
      ${(entities.ips || []).map((x) => `<span class="pill">${x}</span>`).join("")}
    </div>
    <div class="card"><h3>Stop</h3>${payload.stop_state?.stop ? payload.stop_state.reason : "running"}</div>`;
}

function renderReport(report) {
  if (!report) {
    $("report-view").className = "report empty";
    $("report-view").textContent = "The validator only accepts citations that exist in this run’s evidence ledger.";
    return;
  }
  $("report-view").className = "report";
  const cites = (report.supporting_evidence || [])
    .map((item) => `<div class="pill">${item.event_id}</div> ${item.claim}`)
    .join("");
  $("report-view").innerHTML = `
    <div class="verdict ${report.verdict}">${report.verdict} · ${report.confidence}</div>
    <p>${report.summary}</p>
    <p class="hint">${report.remaining_uncertainty || ""}</p>
    <div>${cites}</div>`;
}

async function attachRun(runId, fromHistory = true) {
  if (state.stream) {
    state.stream.close();
    state.stream = null;
  }
  state.selectedRun = runId;
  state.seenStages = new Set();
  state.seenSequences = new Set();
  $("events").innerHTML = "";
  renderRuns();
  const detail = await api(`/api/runs/${runId}`);
  state.selectedCondition = detail.condition;
  state.architecture = detail.architecture;
  renderConditions();
  renderArchitecture();
  renderState(detail.state);
  renderReport(detail.report);
  for (const event of detail.events || []) pushEvent(event);
  if (detail.status === "queued" || detail.status === "running") {
    const source = new EventSource(`/api/runs/${runId}/stream`);
    state.stream = source;
    source.onmessage = (message) => {
      const event = JSON.parse(message.data);
      if (event.kind === "eof") {
        source.close();
        refreshLists();
        return;
      }
      pushEvent(event);
    };
  }
}

async function refreshLists() {
  const [datasets, runs, c3] = await Promise.all([
    api("/api/datasets"),
    api("/api/runs"),
    api("/api/runs/c3"),
  ]);
  state.datasets = datasets.datasets;
  state.runs = runs.runs;
  state.c3Runs = c3.runs;
  renderDatasets();
  renderRuns();
}

$("upload-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const file = $("file-input").files[0];
  if (!file) return;
  const body = new FormData();
  body.append("file", file);
  const dataset = await api("/api/datasets", { method: "POST", body });
  await refreshLists();
  await selectDataset(dataset.id);
});

$("start-run").addEventListener("click", async () => {
  $("run-error").hidden = true;
  try {
    if (!state.selectedDataset) throw new Error("Select a dataset first.");
    const payload = {
      dataset_id: state.selectedDataset,
      condition: state.selectedCondition,
      matched_run_id: state.selectedCondition === "C5" ? $("matched-run").value || null : null,
      budgets: {
        max_tool_calls: Number($("budget-tools").value),
        max_records_per_call: Number($("budget-records").value),
      },
    };
    const run = await api("/api/runs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    await refreshLists();
    await attachRun(run.id, false);
  } catch (error) {
    $("run-error").hidden = false;
    $("run-error").textContent = error.message;
  }
});

async function boot() {
  const conditions = await api("/api/conditions");
  state.conditions = conditions.conditions;
  await selectCondition("C3");
  await refreshLists();
  if (state.datasets[0]) await selectDataset(state.datasets[0].id);
}

boot();
