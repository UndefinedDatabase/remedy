// Drives headless Chrome over CDP (node's global WebSocket) to load the
// conformance page built under dist/, then prints the page's own verdict:
// the missing tokens, every failed probe, a per-mark tally and one summary
// line. Exits 0 only when no token is missing and every probe passed.
// conformance_measure.py, the caller, stops Chrome and the server by pid.

const CDP = "http://127.0.0.1:9353";
const PAGE = "http://127.0.0.1:8991/index.html";

function connect(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    ws.addEventListener("open", () => resolve(ws));
    ws.addEventListener("error", (e) => reject(e));
  });
}

function makeClient(ws, onEvent) {
  let nextId = 1;
  const pending = new Map();
  ws.addEventListener("message", (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id !== undefined && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(new Error(JSON.stringify(msg.error)));
      else resolve(msg.result);
    } else if (msg.method) onEvent(msg);
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
  const list = await (await fetch(`${CDP}/json/list`)).json();
  const page = list.find((t) => t.type === "page");
  if (!page) throw new Error("no page target");
  const exceptions = [];
  const client = makeClient(await connect(page.webSocketDebuggerUrl), (m) => {
    if (m.method === "Runtime.exceptionThrown") exceptions.push(JSON.stringify(m.params.exceptionDetails).slice(0, 300));
  });
  await client.send("Page.enable");
  await client.send("Runtime.enable");
  await client.send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
  await client.send("Page.navigate", { url: PAGE });
  await sleep(3000);
  const evaluated = await client.send("Runtime.evaluate", {
    expression: "JSON.stringify(window.__conformance || null)", returnByValue: true,
  });
  const result = evaluated.result.value ? JSON.parse(evaluated.result.value) : null;
  for (const e of exceptions) console.log(`EXCEPTION ${e}`);
  if (!result) {
    console.log("CONFORMANCE: the page produced no result");
    process.exit(1);
  }
  console.log(`MISSING TOKENS: ${result.missing.length ? result.missing.join(" ") : "none"}`);
  for (const key of Object.keys(result.byMark).sort()) {
    const t = result.byMark[key];
    console.log(`PASSED ${key}: ${t.present} present, ${t.absent} absent`);
  }
  for (const f of result.failures) console.log(`FAILED ${f}`);
  console.log(`CONFORMANCE: ${result.passed} of ${result.total} probes pass`);
  const ok = exceptions.length === 0 && result.missing.length === 0 && result.passed === result.total;
  process.exit(ok ? 0 : 1);
}

main().catch((e) => {
  console.error("FATAL:", e);
  process.exit(1);
});
