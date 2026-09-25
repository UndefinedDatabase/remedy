// F024 R5: drive the scrub budget harness over CDP — three runs on the 500-node fixture's
// ledger — and print one JSON line per run and a BUDGET line (DECISION F024 D5). The frame
// budget is the stage-1 figure F023 applied at 500 nodes: a 95th-percentile frame of at most
// 17.0 ms and at least 59 frames a second while the handle sweeps one event per frame. The
// scrub budget is the snapshot arithmetic's: once the snapshots exist, a position's memo state,
// phases and view cost at most a quarter frame at the 95th percentile, and no position ever
// costs more than one frame, even cold. argv[2] is the red control's busy-wait in ms.
const CDP_HOST = "127.0.0.1";
const CDP_PORT = 9373;
const SERVER_PORT = 9003;
const REPEATS = 3;
const WAIT_MS = 12500; // 3s settle + 8s measure + slack
const P95_BUDGET_MS = 17.0;
const MEAN_FPS_BUDGET = 59;
const WARM_P95_BUDGET_MS = 4.0;
const COLD_MAX_BUDGET_MS = 16.7;
const SLOW_MS = Number(process.argv[2] ?? "0");

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
  return {
    send(method, params = {}) {
      const id = nextId++;
      return new Promise((resolve, reject) => {
        pending.set(id, { resolve, reject });
        ws.send(JSON.stringify({ id, method, params }));
      });
    },
  };
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
  const list = await (await fetch(`http://${CDP_HOST}:${CDP_PORT}/json/list`)).json();
  const page = list.find((t) => t.type === "page");
  if (!page) throw new Error("no page target found");
  const client = makeClient(await connect(page.webSocketDebuggerUrl));
  await client.send("Page.enable");
  await client.send("Runtime.enable");
  await client.send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });

  const results = [];
  for (let i = 1; i <= REPEATS; i++) {
    await client.send("Page.navigate", { url: `http://127.0.0.1:${SERVER_PORT}/index.html?slow=${SLOW_MS}` });
    await sleep(WAIT_MS);
    const value = (await client.send("Runtime.evaluate", {
      expression: "JSON.stringify(window.__scrubPerfResult || null)", returnByValue: true,
    })).result.value;
    const line = { run: i, result: value ? JSON.parse(value) : null };
    console.log(JSON.stringify(line));
    results.push(line);
  }

  const ok = (r) => r.result && r.result.done && r.result.nodeCount === 500 && r.result.mode === "scrubbed"
    && r.result.p95Ms <= P95_BUDGET_MS && r.result.meanFps >= MEAN_FPS_BUDGET
    && r.result.bench.warmP95Ms <= WARM_P95_BUDGET_MS && r.result.bench.coldMaxMs <= COLD_MAX_BUDGET_MS;
  const worst = (key, pick) => pick(...results.map((r) => (r.result ? key(r.result) : NaN)));
  console.log(`FRAMES: worst p95 ${worst((r) => r.p95Ms, Math.max)} ms, worst mean ${worst((r) => r.meanFps, Math.min)} fps`);
  console.log(`SCRUB: worst warm p95 ${worst((r) => r.bench.warmP95Ms, Math.max)} ms, worst cold max ${worst((r) => r.bench.coldMaxMs, Math.max)} ms`);
  const pass = results.length === REPEATS && results.every(ok);
  console.log(`BUDGET 500 nodes, scrubbed one event per frame: ${pass ? "PASS" : "FAIL"}`);

  try {
    const version = await (await fetch(`http://${CDP_HOST}:${CDP_PORT}/json/version`)).json();
    await makeClient(await connect(version.webSocketDebuggerUrl)).send("Browser.close");
  } catch (e) {
    console.error("Browser.close failed (measure.py falls back to its pid kill):", String(e));
  }
  process.exit(pass ? 0 : 1);
}

main().catch((e) => {
  console.error("FATAL:", e);
  process.exit(1);
});
