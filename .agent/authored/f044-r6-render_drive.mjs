// F044 R6's render driver (evidence, not product): drives headless Chrome over CDP (node's global
// WebSocket) through the real `RemedyShell` mounted by main.tsx, and proves the graph's keys and the
// keymap's overlay as a person meets them (DECISION F044 D6):
//   R-a "j" on the page zooms the graph to its first task and selects it;
//   R-b "j" steps to the next task, "k" back, and "k" again wraps to the last;
//   R-c Escape walks the zoom back to the whole job;
//   R-d "j" typed in the bar stays text and moves nothing;
//   R-e "?" held past the hold time shows the keymap's overlay, every binding listed and no terms
//       panel, and letting go closes it without opening the terms;
//   R-f the overlay is a fixed card centred on the overlay layer;
//   R-g "?" tapped opens the terms panel and shows no overlay;
//   R-h Escape with the terms panel open, and the focus on no field, closes the panel and leaves
//       the zoom where it was;
//   R-i no console error and no uncaught exception was logged in the whole run.
// Screenshots once, while R-e's overlay is shown. Prints "RENDER: <n> of 9 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f044-r6-render-overlay.png";

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
  const evaluated = await client.send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
  if (evaluated.exceptionDetails) {
    throw new Error(`evaluate failed: ${JSON.stringify(evaluated.exceptionDetails).slice(0, 300)}`);
  }
  return evaluated.result.value;
}

async function click(client, selector) {
  const at = await evalJson(client, `(function(){
    var el = document.querySelector(${JSON.stringify(selector)});
    if (!el) return null;
    var box = el.getBoundingClientRect();
    return { x: Math.round(box.left + box.width / 2), y: Math.round(box.top + box.height / 2) };
  })()`);
  if (at === null) return false;
  for (const type of ["mouseMoved", "mousePressed", "mouseReleased"]) {
    await client.send("Input.dispatchMouseEvent", { type, x: at.x, y: at.y, button: "left", clickCount: 1 });
  }
  await sleep(250);
  return true;
}

async function key(client, name, code, vk, text) {
  const common = { key: name, code, windowsVirtualKeyCode: vk };
  await client.send("Input.dispatchKeyEvent", { type: "keyDown", ...common, ...(text ? { text } : {}) });
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", ...common });
  await sleep(200);
}

async function type(client, text) {
  await client.send("Input.insertText", { text });
  await sleep(250);
}

const BAR_INPUT = '[data-ui="command-bar"] input';

const SNAPSHOT = `(function(){
  var stage = document.querySelector('[data-ui="brain-graph-stage"]');
  var input = document.querySelector('${BAR_INPUT}');
  var overlay = document.querySelector('[data-ui="keymap-overlay"]');
  var style = overlay ? getComputedStyle(overlay) : null;
  var box = overlay ? overlay.getBoundingClientRect() : null;
  return {
    level: stage ? stage.getAttribute('data-zoom-level') : null,
    picked: window.__picked.slice(),
    value: input.value,
    barFocused: document.activeElement === input,
    overlay: overlay !== null,
    rows: overlay ? Array.from(overlay.querySelectorAll('[data-keymap-action]')).map(function(el){ return el.getAttribute('data-keymap-action'); }) : [],
    position: style ? style.position : null,
    zIndex: style ? style.zIndex : null,
    dx: box ? Math.round(Math.abs(box.left + box.width / 2 - document.documentElement.clientWidth / 2)) : null,
    dy: box ? Math.round(Math.abs(box.top + box.height / 2 - document.documentElement.clientHeight / 2)) : null,
    terms: document.querySelector('[data-ui="term-panel"]') !== null,
  };
})()`;

// 1 Alt, 2 Ctrl, 4 Meta, 8 Shift, as CDP's Input.dispatchKeyEvent reads them.
async function down(client, name, code, vk, text, modifiers) {
  await client.send("Input.dispatchKeyEvent", { type: "keyDown", key: name, code, windowsVirtualKeyCode: vk, modifiers, ...(text ? { text } : {}) });
}
async function up(client, name, code, vk, modifiers) {
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: name, code, windowsVirtualKeyCode: vk, modifiers });
}
async function press(client, name, code, vk, text, modifiers) {
  await down(client, name, code, vk, text, modifiers);
  await up(client, name, code, vk, modifiers);
  await sleep(250);
}

const ALL_ACTIONS = ["open-bar", "open-terms", "go-projects", "next-sibling", "previous-sibling", "zoom-in", "walk-back"];

async function main() {
  const targets = await (await fetch(`${CDP}/json/list`)).json();
  const page = targets.find((t) => t.type === "page");
  const ws = await connect(page.webSocketDebuggerUrl);
  const problems = [];
  const client = makeClient(ws, (msg) => {
    if (msg.method === "Runtime.exceptionThrown") problems.push(`exception: ${JSON.stringify(msg.params).slice(0, 200)}`);
    if (msg.method === "Runtime.consoleAPICalled" && msg.params.type === "error") {
      problems.push(`console.error: ${JSON.stringify(msg.params.args).slice(0, 200)}`);
    }
  });
  await client.send("Page.enable");
  await client.send("Runtime.enable");
  const results = [];
  const check = (label, ok, detail) => { results.push(ok); console.log(`${ok ? "PASS" : "FAIL"} ${label} ${JSON.stringify(detail)}`); };
  const snap = () => evalJson(client, SNAPSHOT);
  const blur = () => evalJson(client, "(document.activeElement && document.activeElement.blur(), true)");

  await client.send("Page.navigate", { url: PAGE });
  await sleep(2500);
  await blur();

  await press(client, "j", "KeyJ", 74, "j", 0);
  const a = await snap();
  check("R-a j zooms to the first task and selects it", a.level === "1" && JSON.stringify(a.picked) === '["node-t1"]',
    { level: a.level, picked: a.picked });

  await press(client, "j", "KeyJ", 74, "j", 0);
  await press(client, "k", "KeyK", 75, "k", 0);
  await press(client, "k", "KeyK", 75, "k", 0);
  const b = await snap();
  check("R-b j steps forward, k back, and k wraps to the last", b.level === "1"
    && JSON.stringify(b.picked) === '["node-t1","node-t2","node-t1","node-t3"]', { level: b.level, picked: b.picked });

  await press(client, "Escape", "Escape", 27, null, 0);
  const c = await snap();
  check("R-c Escape walks back to the whole job", c.level === "0", { level: c.level });

  await click(client, BAR_INPUT);
  await press(client, "j", "KeyJ", 74, "j", 0);
  const d = await snap();
  check("R-d j typed in the bar stays text", d.value === "j" && d.level === "0" && d.picked.length === 4,
    { value: d.value, level: d.level, picks: d.picked.length });
  await press(client, "Escape", "Escape", 27, null, 0);
  await evalJson(client, `(function(){
    var input = document.querySelector('${BAR_INPUT}');
    var setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
    setter.call(input, '');
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.blur();
    return true;
  })()`);

  await down(client, "?", "Slash", 191, "?", 8);
  await sleep(800);
  const e1 = await snap();
  console.log(`screenshot bytes: ${writeScreenshot(await client.send("Page.captureScreenshot", { format: "png" }))}`);
  await up(client, "?", "Slash", 191, 8);
  await sleep(300);
  const e2 = await snap();
  check("R-e a held ? shows every binding, and letting go closes it without the terms", e1.overlay === true
    && JSON.stringify(e1.rows) === JSON.stringify(ALL_ACTIONS) && e1.terms === false && e2.overlay === false
    && e2.terms === false, { held: [e1.overlay, e1.rows.length, e1.terms], released: [e2.overlay, e2.terms] });

  check("R-f the overlay is a fixed card centred on the overlay layer", e1.position === "fixed" && e1.zIndex === "80"
    && e1.dx <= 1 && e1.dy <= 1, { position: e1.position, zIndex: e1.zIndex, dx: e1.dx, dy: e1.dy });

  await press(client, "?", "Slash", 191, "?", 8);
  const g = await snap();
  check("R-g a tapped ? opens the terms and no overlay", g.terms === true && g.overlay === false,
    { terms: g.terms, overlay: g.overlay });
  await press(client, "Escape", "Escape", 27, null, 0);
  await blur();

  await press(client, "j", "KeyJ", 74, "j", 0);
  await press(client, "?", "Slash", 191, "?", 8);
  const h1 = await snap();
  // The panel puts the focus in its search field; with the focus off every field, only the
  // dialog rule keeps Escape from walking the zoom back.
  await blur();
  await press(client, "Escape", "Escape", 27, null, 0);
  const h2 = await snap();
  check("R-h Escape closes the open terms panel and leaves the zoom", h1.terms === true && h1.level === "1"
    && h2.terms === false && h2.level === "1", { before: [h1.terms, h1.level], after: [h2.terms, h2.level] });

  await sleep(300);
  check("R-i no console error", problems.length === 0, problems);
  const passed = results.filter(Boolean).length;
  console.log(`RENDER: ${passed} of ${results.length} checks pass`);
  ws.close();
  process.exit(passed === results.length ? 0 : 1);
}

function writeScreenshot({ data }) {
  const bytes = Buffer.from(data, "base64");
  writeFileSync(SCREENSHOT_PNG, bytes);
  return bytes.length;
}

main().catch((err) => { console.error(err); process.exit(1); });
