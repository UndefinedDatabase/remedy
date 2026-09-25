// F023 R7: drive the zoom perf harness over CDP — three runs at each zoom level
// on the 500-node fixture — and print one JSON line per run and a BUDGET line.
// The budget is the stage-1 frame budget T5_F023.md applies at 500 nodes: a
// 95th-percentile frame of at most 17.0 ms and at least 59 frames a second.
const CDP_HOST = "127.0.0.1";
const CDP_PORT = 9363;
const SERVER_PORT = 8993;
const LEVELS = [0, 1, 2, 3];
const REPEATS = 3;
const WAIT_MS = 12500; // 3s settle + 8s measure + slack
const P95_BUDGET_MS = 17.0;
const MEAN_FPS_BUDGET = 59;

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
  for (const level of LEVELS) {
    for (let i = 1; i <= REPEATS; i++) {
      await client.send("Page.navigate", { url: `http://127.0.0.1:${SERVER_PORT}/index.html?level=${level}` });
      await sleep(WAIT_MS);
      const value = (await client.send("Runtime.evaluate", {
        expression: "JSON.stringify(window.__zoomPerfResult || null)", returnByValue: true,
      })).result.value;
      const result = value ? JSON.parse(value) : null;
      const line = { level, run: i, result };
      console.log(JSON.stringify(line));
      results.push(line);
    }
  }

  const ok = (r) => r.result && r.result.done && r.result.reachedLevel === r.level
    && r.result.p95Ms <= P95_BUDGET_MS && r.result.meanFps >= MEAN_FPS_BUDGET;
  for (const level of LEVELS) {
    const runs = results.filter((r) => r.level === level);
    const worstP95 = Math.max(...runs.map((r) => (r.result ? r.result.p95Ms : Infinity)));
    const worstMean = Math.min(...runs.map((r) => (r.result ? r.result.meanFps : 0)));
    console.log(`LEVEL L${level}: worst p95 ${worstP95} ms, worst mean ${worstMean} fps, ${runs.every(ok) ? "PASS" : "FAIL"}`);
  }
  const pass = results.length === LEVELS.length * REPEATS && results.every(ok);
  console.log(`BUDGET 500 nodes, every zoom level: ${pass ? "PASS" : "FAIL"}`);

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
