// F044 R5's render driver (evidence, not product): drives headless Chrome over CDP (node's global
// WebSocket) through the real `RemedyShell` mounted by main.tsx, and proves the keymap's keys as a
// person meets them (DECISION F044 D5):
//   R-a "/" pressed on the page puts the focus in the bar and opens its sheet;
//   R-b "/" and "?" typed in the bar stay text: the bar holds them, the focus stays, no terms open;
//   R-c Ctrl+K from the steering note's field moves the focus to the bar, and the field keeps
//       what was typed in it;
//   R-d Cmd+K from the page puts the focus in the bar;
//   R-e "?" on the page opens the terms panel, and Escape closes it;
//   R-f "g" then "p" on the page asks for the projects' home once;
//   R-g "g", another key, then "p" asks for nothing;
//   R-h no console error and no uncaught exception was logged in the whole run.
// Screenshots once, after R-a. Prints "RENDER: <n> of 8 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f044-r5-render-keys.png";

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
const NOTE_INPUT = '[data-ui="right-live-panel"] input';

const SNAPSHOT = `(function(){
  var input = document.querySelector('${BAR_INPUT}');
  var note = document.querySelector('${NOTE_INPUT}');
  return {
    barFocused: document.activeElement === input,
    noteFocused: document.activeElement === note,
    value: input.value,
    noteValue: note ? note.value : null,
    sheet: document.querySelector('[data-ui="palette-sheet"]') !== null,
    terms: document.querySelector('[data-ui="term-panel"]') !== null,
    home: window.__home,
  };
})()`;

// 1 Alt, 2 Ctrl, 4 Meta, 8 Shift, as CDP's Input.dispatchKeyEvent reads them.
async function press(client, name, code, vk, text, modifiers) {
  const common = { key: name, code, windowsVirtualKeyCode: vk, modifiers };
  await client.send("Input.dispatchKeyEvent", { type: "keyDown", ...common, ...(text ? { text } : {}) });
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", ...common });
  await sleep(200);
}

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
  await sleep(2000);
  await blur();

  await press(client, "/", "Slash", 191, "/", 0);
  const a = await snap();
  check("R-a / on the page focuses the bar and opens its sheet", a.barFocused === true && a.sheet === true
    && a.value === "", { focused: a.barFocused, sheet: a.sheet, value: a.value });
  console.log(`screenshot bytes: ${writeScreenshot(await client.send("Page.captureScreenshot", { format: "png" }))}`);

  await press(client, "/", "Slash", 191, "/", 0);
  await press(client, "?", "Slash", 191, "?", 8);
  const b = await snap();
  check("R-b / and ? typed in the bar stay text", b.barFocused === true && b.value === "/?" && b.terms === false,
    { focused: b.barFocused, value: b.value, terms: b.terms });
  await press(client, "Escape", "Escape", 27, null, 0);
  await blur();

  await click(client, NOTE_INPUT);
  await type(client, "hi");
  const c1 = await snap();
  await press(client, "k", "KeyK", 75, null, 2);
  const c2 = await snap();
  check("R-c Ctrl+K from the note's field moves the focus to the bar", c1.noteFocused === true && c2.barFocused === true
    && c2.noteValue === "hi", { before: c1.noteFocused, after: c2.barFocused, note: c2.noteValue });
  await blur();

  await press(client, "k", "KeyK", 75, null, 4);
  const d = await snap();
  check("R-d Cmd+K from the page focuses the bar", d.barFocused === true, { focused: d.barFocused });
  await blur();

  await press(client, "?", "Slash", 191, "?", 8);
  const e1 = await snap();
  await press(client, "Escape", "Escape", 27, null, 0);
  const e2 = await snap();
  check("R-e ? on the page opens the terms, and Escape closes them", e1.terms === true && e2.terms === false,
    { open: e1.terms, afterEscape: e2.terms });
  await blur();

  await press(client, "g", "KeyG", 71, "g", 0);
  await press(client, "p", "KeyP", 80, "p", 0);
  const f = await snap();
  check("R-f g then p asks for the projects' home once", f.home === 1, { home: f.home });

  await press(client, "g", "KeyG", 71, "g", 0);
  await press(client, "x", "KeyX", 88, "x", 0);
  await press(client, "p", "KeyP", 80, "p", 0);
  const g = await snap();
  check("R-g g, another key, then p asks for nothing", g.home === 1, { home: g.home });

  await sleep(300);
  check("R-h no console error", problems.length === 0, problems);
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
