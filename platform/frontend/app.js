const state = {
  conditions: [],
  architecture: null,
  datasets: [],
  runs: [],
  c3Runs: [],
  providers: [],
  selected: { provider: "ollama", model: "llama3.2:1b" },
  selectedCondition: "C3",
  selectedDataset: null,
  selectedRun: null,
  seenStages: new Set(),
  seenSequences: new Set(),
  stream: null,
  generated: null,
  suiteTimer: null,
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

function currentProviderMeta() {
  return state.providers.find((item) => item.id === state.selected.provider) || state.providers[0];
}

function renderOllamaChip(health) {
  const chip = $("ollama-chip");
  const ollama = health.ollama || {};
  if (ollama.ok) {
    chip.className = "ollama-chip on";
    chip.textContent = `Ollama online · ${(ollama.models || []).join(", ") || "no models"}`;
  } else {
    chip.className = "ollama-chip off";
    chip.textContent = `Ollama offline · ${ollama.error || "start ollama serve"}`;
  }
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

function renderProviders() {
  $("provider").innerHTML = state.providers
    .map((item) => {
      const mark = item.configured ? "" : item.needs_key ? " · key needed" : "";
      const live = item.id === "ollama" && item.online === false ? " · offline" : "";
      return `<option value="${item.id}">${item.label}${mark}${live}</option>`;
    })
    .join("");
  $("provider").value = state.selected.provider;
  $("model-name").value = state.selected.model;
  const meta = currentProviderMeta();
  const models = meta?.models || [];
  $("model-options").innerHTML = models.map((name) => `<option value="${name}"></option>`).join("");
  $("ollama-url-wrap").hidden = meta?.id !== "ollama";
  $("key-form").hidden = !meta?.needs_key && meta?.id !== "ollama";
  $("api-key").placeholder = meta?.hint || "paste key";
  $("save-key").textContent = meta?.id === "ollama" ? "Save URL" : "Save key";
  if (meta?.id === "ollama") $("ollama-url").value = meta.base_url || "http://127.0.0.1:11434";
}

function renderUploadKinds() {
  const kinds = state.architecture?.data_kinds || [];
  $("upload-kinds").innerHTML = kinds
    .map((kind) => {
      const active = kind.active_for_condition ? "active-kind" : "";
      const loaded = kind.loaded ? "loaded-kind" : "";
      return `<label class="kind-btn ${active} ${loaded}" title="${kind.hint}">
        <input type="file" accept="application/json,.json" data-kind="${kind.id}" />
        <strong>${kind.label}</strong>
        <span>${kind.loaded ? "loaded" : kind.active_for_condition ? "needed for this condition" : "optional / sealed"}</span>
      </label>`;
    })
    .join("");
  for (const input of $("upload-kinds").querySelectorAll("input")) {
    input.addEventListener("change", () => uploadKind(input.dataset.kind, input.files[0]));
  }
}

async function uploadKind(kind, file) {
  if (!file) return;
  $("upload-status").textContent = `Uploading ${kind}…`;
  try {
    const body = new FormData();
    body.append("file", file);
    const query = state.selectedDataset ? `?dataset_id=${encodeURIComponent(state.selectedDataset)}` : "";
    const dataset = await api(`/api/datasets/parts/${kind}${query}`, { method: "POST", body });
    await refreshLists();
    await selectDataset(dataset.id);
    $("upload-status").textContent = `Loaded ${kind} onto ${dataset.incident_id}.`;
    await regenerateArchitecture();
  } catch (error) {
    $("upload-status").textContent = error.message;
  }
}

async function selectCondition(id) {
  state.selectedCondition = id;
  renderConditions();
  $("matched-run").disabled = id !== "C5";
  await regenerateArchitecture();
}

async function regenerateArchitecture() {
  const provider = state.selected.provider;
  const dataset = state.selectedDataset ? `&dataset_id=${encodeURIComponent(state.selectedDataset)}` : "";
  state.architecture = await api(
    `/api/architecture?condition=${state.selectedCondition}&provider=${encodeURIComponent(provider)}${dataset}`
  );
  renderArchitecture();
  renderUploadKinds();
}

function renderArchitecture() {
  const view = state.architecture;
  const profile = view.profile;
  $("canvas-title").textContent = `${view.condition_id} · ${profile.name} · ${view.provider || "ollama"}`;
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
            .map((svc) => {
              const classes = [
                "svc",
                svc.enabled ? "on" : "off",
                svc.selected ? "selected" : "",
                svc.loaded ? "loaded" : "",
              ].join(" ");
              const badge = svc.selected ? "pinned" : svc.loaded ? "data" : svc.enabled ? "on" : "off";
              return `
            <div class="${classes}" data-service="${svc.id}">
              <div class="name">${svc.label}</div>
              <div class="role">${svc.role}</div>
              <div class="badge">${badge}</div>
            </div>`;
            })
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
  const counts = Object.entries(passport.record_counts || {})
    .map(([source, count]) => `<span>${source} ${count}</span>`)
    .join("");
  const present = passport.packs_present || {};
  $("passport").classList.remove("empty");
  $("passport").innerHTML = `
    <dl>
      <dt>Incident</dt><dd class="mono">${passport.incident_id}</dd>
      <dt>Host</dt><dd>${passport.alert.host || "—"}</dd>
      <dt>Alert</dt><dd>${passport.alert.summary || passport.alert.alert_type || "—"}</dd>
      <dt>Packs</dt>
      <dd>${Object.entries(present).filter(([, on]) => on).map(([name]) => name).join(" · ") || "none"}</dd>
    </dl>
    <div class="counts">${counts}</div>`;
  await regenerateArchitecture();
}

function renderRuns() {
  $("run-list").innerHTML = state.runs
    .slice(0, 12)
    .map((run) => {
      const active = run.id === state.selectedRun ? "active" : "";
      const model = run.manifest?.model_profile || "";
      return `<button class="run-chip ${active}" data-id="${run.id}">
        ${run.condition} · ${run.status}
        <small>${run.id} ${model}</small>
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
    event.payload?.model ||
    event.payload?.stage ||
    "";
  return `<li>
    <div class="meta">${String(event.sequence ?? 0).padStart(3, "0")} · ${event.service} · ${event.kind}</div>
    <div class="why">${why}</div>
  </li>`;
}

function pushEvent(event) {
  if (event.kind === "eof") return;
  if (event.sequence != null) {
    if (state.seenSequences.has(event.sequence)) return;
    state.seenSequences.add(event.sequence);
  }
  $("events").insertAdjacentHTML("afterbegin", eventLine(event));
  markStage(event.stage);
  markService(event.service, event.kind === "run_failed" || event.kind === "service_disabled" ? "fail" : "live");
  setSignal(event.stage ? `${event.service} · ${event.stage}` : `${event.service} · ${event.kind}`);
  if (event.kind === "state_updated" || event.kind === "state_initialized") renderState(event.payload);
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

function renderSuite(suite) {
  if (!suite || !suite.runs || !suite.runs.length) {
    $("suite-table").className = "suite-table empty";
    $("suite-table").textContent = "No suite results yet.";
    $("download-report").hidden = true;
    return;
  }
  const current = suite.current ? `Now: ${suite.current.condition}` : suite.status;
  $("suite-meta").textContent = `${suite.provider || ""}:${suite.model || ""} · ${current}`;
  $("suite-table").className = "suite-table";
  $("suite-table").innerHTML = `
    <table>
      <thead>
        <tr><th>C</th><th>Status</th><th>Verdict</th><th>Conf</th><th>Tools</th><th>KB</th></tr>
      </thead>
      <tbody>
        ${suite.runs
          .map(
            (row) => `<tr>
              <td>${row.condition}</td>
              <td>${row.status}</td>
              <td>${row.verdict || "—"}</td>
              <td>${row.confidence ?? "—"}</td>
              <td>${row.tool_observations ?? 0}</td>
              <td>${row.knowledge_retrievals ?? 0}</td>
            </tr>`
          )
          .join("")}
      </tbody>
    </table>`;
  $("download-report").hidden = suite.status !== "completed";
}

function showGenerated(generated) {
  state.generated = generated;
  $("code-view").hidden = false;
  $("code-view").classList.remove("empty");
  $("code-view").textContent = generated.python;
  $("download-code").hidden = false;
}

async function attachRun(runId) {
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
  renderUploadKinds();
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

function runPayload() {
  return {
    dataset_id: state.selectedDataset,
    condition: state.selectedCondition,
    provider: state.selected.provider,
    model: $("model-name").value,
    matched_run_id: state.selectedCondition === "C5" ? $("matched-run").value || null : null,
    budgets: {
      max_tool_calls: Number($("budget-tools").value),
      max_records_per_call: Number($("budget-records").value),
    },
  };
}

async function pinProvider() {
  await api("/api/providers/select", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      provider: state.selected.provider,
      model: $("model-name").value,
      base_url: $("ollama-url").value,
    }),
  });
}

async function pollSuite() {
  const suite = await api("/api/experiments/suite");
  renderSuite(suite);
  $("suite-status").textContent = suite.status === "running"
    ? `Suite running${suite.current ? ` · ${suite.current.condition}` : ""}…`
    : suite.status === "completed"
      ? "Suite complete."
      : suite.status === "failed"
        ? `Suite failed: ${suite.error || ""}`
        : "";
  if (suite.current?.run_id && suite.current.run_id !== state.selectedRun) {
    await refreshLists();
    await attachRun(suite.current.run_id);
  }
  if (suite.status === "completed" || suite.status === "failed") {
    clearInterval(state.suiteTimer);
    state.suiteTimer = null;
    await refreshLists();
  }
}

$("regen-arch").addEventListener("click", () => regenerateArchitecture());

$("provider").addEventListener("change", async () => {
  const provider = $("provider").value;
  const meta = state.providers.find((item) => item.id === provider);
  state.selected.provider = provider;
  state.selected.model = meta.default_model;
  $("model-name").value = meta.default_model;
  await pinProvider();
  renderProviders();
  await regenerateArchitecture();
});

$("key-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const provider = $("provider").value;
    const result = await api("/api/secrets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        provider,
        api_key: $("api-key").value,
        base_url: $("ollama-url").value,
      }),
    });
    $("api-key").value = "";
    $("key-status").textContent = `${provider} ${result.hint || "saved"}`;
    const providers = await api("/api/providers");
    state.providers = providers.providers;
    renderProviders();
    await regenerateArchitecture();
  } catch (error) {
    $("key-status").textContent = error.message;
  }
});

$("generate-code").addEventListener("click", async () => {
  $("run-error").hidden = true;
  try {
    if (!state.selectedDataset) throw new Error("Select a dataset first.");
    const generated = await api("/api/experiments/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(runPayload()),
    });
    showGenerated(generated);
    if (generated.architecture) {
      state.architecture = generated.architecture;
      renderArchitecture();
      renderUploadKinds();
    }
  } catch (error) {
    $("run-error").hidden = false;
    $("run-error").textContent = error.message;
  }
});

$("download-code").addEventListener("click", () => {
  if (!state.generated) return;
  const blob = new Blob([state.generated.python], { type: "text/x-python" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = state.generated.filename;
  link.click();
  URL.revokeObjectURL(url);
});

$("start-run").addEventListener("click", async () => {
  $("run-error").hidden = true;
  try {
    if (!state.selectedDataset) throw new Error("Select a dataset first.");
    await pinProvider();
    const run = await api("/api/runs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(runPayload()),
    });
    await refreshLists();
    await attachRun(run.id);
  } catch (error) {
    $("run-error").hidden = false;
    $("run-error").textContent = error.message;
  }
});

$("start-suite").addEventListener("click", async () => {
  $("run-error").hidden = true;
  try {
    if (!state.selectedDataset) throw new Error("Select a dataset first.");
    await pinProvider();
    await api("/api/experiments/suite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        dataset_id: state.selectedDataset,
        provider: state.selected.provider,
        model: $("model-name").value,
        budgets: runPayload().budgets,
      }),
    });
    $("suite-status").textContent = "Suite started…";
    if (state.suiteTimer) clearInterval(state.suiteTimer);
    state.suiteTimer = setInterval(pollSuite, 1500);
    await pollSuite();
  } catch (error) {
    $("run-error").hidden = false;
    $("run-error").textContent = error.message;
  }
});

async function boot() {
  const [conditions, providers, health] = await Promise.all([
    api("/api/conditions"),
    api("/api/providers"),
    api("/api/health"),
  ]);
  state.conditions = conditions.conditions;
  state.providers = providers.providers;
  state.selected = providers.selected;
  renderOllamaChip(health);
  renderConditions();
  renderProviders();
  await refreshLists();
  if (state.datasets[0]) await selectDataset(state.datasets[0].id);
  else await selectCondition("C3");
  try {
    const suite = await api("/api/experiments/suite");
    renderSuite(suite);
    if (suite.status === "running") {
      state.suiteTimer = setInterval(pollSuite, 1500);
    } else if (suite.status === "completed") {
      renderSuite(suite);
    } else {
      const report = await api("/api/experiments/report").catch(() => null);
      if (report) renderSuite({ ...report, status: "completed" });
    }
  } catch {
    /* no suite yet */
  }
}

boot();
