// Drives headless Chrome over CDP (node's global WebSocket) to load the
// render harness page built under dist/, then proves the prompt list, its
// keys and the synapses ForceBrainGraph is handed (DECISION F288 D6):
//   C-a the layout holds four synapse nodes and the page four list buttons;
//   C-b before any key, the nav's bounding box is at most 1x1 pixel;
//   C-c one Tab puts focus on the first list button;
//   C-d with focus inside, the nav's bounding box is wider and taller than
//       40 pixels;
//   C-e Enter sets window.__selected to the first entry's prompt id and its
//       button's aria-pressed to true;
//   C-f Tab then Space set window.__selected to the second entry's prompt id.
// Saves Page.captureScreenshot PNGs before C-c and after C-f, and prints
// their byte counts. Prints one line per check and exits 0 only when every
// one passed and no page exception was thrown.
// f288-r6-render_measure.py, the caller, stops Chrome and the server by pid.
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9363";
const PAGE = "http://127.0.0.1:8993/index.html";
const BEFORE_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f288-r6-worker/render-before.png";
const AFTER_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f288-r6-worker/render-after.png";

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

async function evalJson(client, expression) {
  const evaluated = await client.send("Runtime.evaluate", { expression, returnByValue: true });
  if (evaluated.exceptionDetails) {
    throw new Error(`evaluate failed: ${JSON.stringify(evaluated.exceptionDetails).slice(0, 300)}`);
  }
  return evaluated.result.value;
}

async function pressKey(client, { key, code, windowsVirtualKeyCode, text }) {
  const base = { key, code, windowsVirtualKeyCode, nativeVirtualKeyCode: windowsVirtualKeyCode };
  await client.send("Input.dispatchKeyEvent", { type: "keyDown", ...base, ...(text ? { text } : {}) });
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", ...base });
  await sleep(150);
}

async function screenshot(client, path) {
  const { data } = await client.send("Page.captureScreenshot", { format: "png" });
  const bytes = Buffer.from(data, "base64");
  writeFileSync(path, bytes);
  return bytes.length;
}

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

  const checks = [];
  const fail = (label, why) => checks.push({ label, ok: false, why });
  const pass = (label) => checks.push({ label, ok: true });

  // C-a — four synapse nodes in the layout, four list buttons on the page.
  const counts = await evalJson(
    client,
    "JSON.stringify({synapses: (window.__layout && window.__layout.nodes ? window.__layout.nodes : []).filter(n => n.kind === 'synapse').length, buttons: document.querySelectorAll('[data-ui=\"prompt-node-list\"] button').length})",
  );
  const countsParsed = counts ? JSON.parse(counts) : { synapses: -1, buttons: -1 };
  if (countsParsed.synapses === 4 && countsParsed.buttons === 4) pass("C-a four synapse nodes and four list buttons");
  else fail("C-a four synapse nodes and four list buttons", JSON.stringify(countsParsed));

  // The synapse layout nodes IN LIST ORDER (buildBrainLayout preserves model
  // order for an unclustered model) — each node's own id is `prompt:<promptId>`
  // (promptNodes.ts's promptNodeId), so the expected prompt ids are read off
  // the SAME layout the page built, never retyped here.
  const synapseIdsJson = await evalJson(
    client,
    "JSON.stringify((window.__layout && window.__layout.nodes ? window.__layout.nodes : []).filter(n => n.kind === 'synapse').map(n => n.id))",
  );
  const synapseIds = synapseIdsJson ? JSON.parse(synapseIdsJson) : [];
  const promptIdOf = (nodeId) => (typeof nodeId === "string" && nodeId.startsWith("prompt:") ? nodeId.slice("prompt:".length) : null);
  const firstPromptId = promptIdOf(synapseIds[0]);
  const secondPromptId = promptIdOf(synapseIds[1]);

  // Screenshot BEFORE any key.
  const beforeBytes = await screenshot(client, BEFORE_PNG);

  // C-b — before any key, the nav's bounding box is at most 1x1 pixel.
  const boxBefore = JSON.parse(await evalJson(
    client,
    "JSON.stringify((function(){var r=document.querySelector('[data-ui=\"prompt-node-list\"]').getBoundingClientRect();return {width:r.width,height:r.height};})())",
  ));
  if (boxBefore.width <= 1 && boxBefore.height <= 1) pass("C-b nav at most 1x1 before any key");
  else fail("C-b nav at most 1x1 before any key", JSON.stringify(boxBefore));

  // C-c — one Tab puts focus on the first list button.
  await pressKey(client, { key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 });
  const focusedFirst = await evalJson(
    client,
    "document.activeElement === document.querySelectorAll('[data-ui=\"prompt-node-list\"] button')[0]",
  );
  if (focusedFirst === true) pass("C-c Tab focuses the first list button");
  else fail("C-c Tab focuses the first list button", String(focusedFirst));

  // C-d — with focus inside, the nav's bounding box exceeds 40x40.
  const boxFocused = JSON.parse(await evalJson(
    client,
    "JSON.stringify((function(){var r=document.querySelector('[data-ui=\"prompt-node-list\"]').getBoundingClientRect();return {width:r.width,height:r.height};})())",
  ));
  if (boxFocused.width > 40 && boxFocused.height > 40) pass("C-d nav wider and taller than 40px while focused");
  else fail("C-d nav wider and taller than 40px while focused", JSON.stringify(boxFocused));

  // C-e — Enter selects the first entry and presses its button.
  await pressKey(client, { key: "Enter", code: "Enter", windowsVirtualKeyCode: 13, text: "\r" });
  const selectedAfterEnter = await evalJson(client, "window.__selected");
  const pressedAfterEnter = await evalJson(
    client,
    "document.querySelectorAll('[data-ui=\"prompt-node-list\"] button')[0].getAttribute('aria-pressed')",
  );
  if (selectedAfterEnter === firstPromptId && pressedAfterEnter === "true") {
    pass("C-e Enter selects the first prompt and presses its button");
  } else {
    fail("C-e Enter selects the first prompt and presses its button", `selected=${selectedAfterEnter} expected=${firstPromptId} pressed=${pressedAfterEnter}`);
  }

  // C-f — Tab then Space select the second entry.
  await pressKey(client, { key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 });
  await pressKey(client, { key: " ", code: "Space", windowsVirtualKeyCode: 32, text: " " });
  const selectedAfterSpace = await evalJson(client, "window.__selected");
  if (selectedAfterSpace === secondPromptId) pass("C-f Tab then Space select the second prompt");
  else fail("C-f Tab then Space select the second prompt", `selected=${selectedAfterSpace} expected=${secondPromptId}`);

  // Screenshot AFTER C-f.
  const afterBytes = await screenshot(client, AFTER_PNG);

  for (const e of exceptions) console.log(`EXCEPTION ${e}`);
  for (const c of checks) console.log(c.ok ? `PASS ${c.label}` : `FAILED ${c.label}: ${c.why}`);
  console.log(`SCREENSHOT before ${BEFORE_PNG} ${beforeBytes} bytes`);
  console.log(`SCREENSHOT after ${AFTER_PNG} ${afterBytes} bytes`);
  const allPassed = checks.every((c) => c.ok);
  console.log(`RENDER: ${checks.filter((c) => c.ok).length} of ${checks.length} checks pass`);
  const ok = exceptions.length === 0 && allPassed;
  process.exit(ok ? 0 : 1);
}

main().catch((e) => {
  console.error("FATAL:", e);
  process.exit(1);
});
