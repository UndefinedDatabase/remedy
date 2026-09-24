// Drives headless Chrome over CDP (native WebSocket, node v22) to measure
// ForceBrainGraph's real rAF frame rate for the harness built under dist/.
// Runs SIZES x REPEATS measurements in one Chrome session, printing each
// result object as one JSON line, then one BUDGET verdict line for the
// stage-1 (200-node) budget: PASS means every 200-node run had p95 <= 17.0 ms
// and mean fps >= 59 (acceptance_criteria.md §5: "60fps p95 at 200 nodes").
// Exits 0 on PASS, 1 otherwise — measure.py (the caller) also stops Chrome
// and the server by their recorded pids, this script's own Browser.close is
// best-effort cleanup, not the only path.

const CDP_HOST = "127.0.0.1";
const CDP_PORT = 9333;
const SERVER_PORT = 8971;
const SIZES = [200, 500];
const REPEATS = 3;
const WAIT_MS = 11000; // 2s warmup + 8s measure + 1s slack
const STAGE1_P95_BUDGET_MS = 17.0;
const STAGE1_MEAN_FPS_BUDGET = 59;

async function jsonList() {
  const res = await fetch(`http://${CDP_HOST}:${CDP_PORT}/json/list`);
  return res.json();
}

function connect(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    ws.addEventListener("open", () => resolve(ws));
    ws.addEventListener("error", (e) => reject(e));
  });
}

function makeClient(ws) {
  let nextId = 1;
  const pending = new Map();
  ws.addEventListener("message", (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id !== undefined && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(new Error(JSON.stringify(msg.error)));
      else resolve(msg.result);
    }
  });
  function send(method, params = {}) {
    const id = nextId++;
    return new Promise((resolve, reject) => {
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
    });
  }
  return { send };
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function measureOnce(client, n, runIndex) {
  const url = `http://127.0.0.1:${SERVER_PORT}/index.html?n=${n}`;
  await client.send("Page.navigate", { url });
  await sleep(WAIT_MS);
  const evalResult = await client.send("Runtime.evaluate", {
    expression: "JSON.stringify(window.__brainPerfResult || null)",
    returnByValue: true,
  });
  const raw = evalResult.result.value;
  const parsed = raw ? JSON.parse(raw) : null;
  return { requestedN: n, runIndex, url, result: parsed };
}

async function main() {
  const list = await jsonList();
  const page = list.find((t) => t.type === "page");
  if (!page) throw new Error("no page target found in /json/list");

  const pageWs = await connect(page.webSocketDebuggerUrl);
  const client = makeClient(pageWs);
  await client.send("Page.enable");
  await client.send("Runtime.enable");
  await client.send("Emulation.setDeviceMetricsOverride", {
    width: 1280,
    height: 800,
    deviceScaleFactor: 1,
    mobile: false,
  });

  const results = [];
  for (const n of SIZES) {
    for (let i = 0; i < REPEATS; i++) {
      const r = await measureOnce(client, n, i + 1);
      console.log(JSON.stringify(r));
      results.push(r);
    }
  }

  const stage1Runs = results.filter((r) => r.requestedN === 200 && r.result);
  const stage1P95 = stage1Runs.map((r) => r.result.p95Ms);
  const stage1Mean = stage1Runs.map((r) => r.result.meanFps);
  const worstP95 = stage1Runs.length ? Math.max(...stage1P95) : Infinity;
  const worstMean = stage1Runs.length ? Math.min(...stage1Mean) : 0;
  const stage1Pass =
    stage1Runs.length === REPEATS &&
    stage1P95.every((v) => v <= STAGE1_P95_BUDGET_MS) &&
    stage1Mean.every((v) => v >= STAGE1_MEAN_FPS_BUDGET);
  console.log(
    `BUDGET stage1 200 nodes: p95 ${worstP95} ms, mean ${worstMean} fps, ${stage1Pass ? "PASS" : "FAIL"}`,
  );

  // Ask Chrome to close cleanly over CDP (browser-level endpoint) —
  // best-effort; measure.py stops Chrome by its recorded pid regardless.
  try {
    const version = await (await fetch(`http://${CDP_HOST}:${CDP_PORT}/json/version`)).json();
    const browserWs = await connect(version.webSocketDebuggerUrl);
    const browserClient = makeClient(browserWs);
    await browserClient.send("Browser.close");
  } catch (e) {
    console.error("Browser.close failed (measure.py will fall back to pid kill):", String(e));
  }

  process.exit(stage1Pass ? 0 : 1);
}

main().catch((e) => {
  console.error("FATAL:", e);
  process.exit(1);
});
