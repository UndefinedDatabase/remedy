// F043 R3's render driver (evidence, not product): drives headless Chrome over CDP (node's
// global WebSocket) through the real `RemedyShell` mounted by main.tsx, and proves the token and
// cost tiles' move onto the term's tooltip and the '?' panel as a person meets them (DECISION
// F043 D3):
//   R-a the shell is on the page with no tooltip and no panel open;
//   R-b a pointer resting on the Tokens label opens its term's tooltip: the catalog's title and
//       body, then the tile's breakdown by role under its own test id, inside the viewport;
//   R-c a pointer resting on the Cost label opens its tooltip, which names the estimate basis;
//   R-d keyboard focus on the Tokens label opens the breakdown at once, which is how the
//       keyboard reaches it now that the tile itself takes no focus;
//   R-e the "?" key pressed on the page opens the Terms panel with its search field focused and
//       every catalog entry listed;
//   R-f typing "urgent" into the search leaves exactly the decision inbox's entry;
//   R-g Escape closes the panel;
//   R-h "?" typed into the steering note's field opens nothing;
//   R-i the right panel's Terms button opens the panel;
//   R-j no console error and no uncaught exception was logged in the whole run.
// Each target is scrolled into view before the pointer moves to it. Screenshots once, while
// R-e's panel is open. Prints "RENDER: <n> of 10 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f043-r3-render-panel.png";
const CATALOG_SIZE = 30;
const TOKENS_TEXT = "Tokens" + "How many tokens this job's model calls have used so far, by role. The count is an estimate."
  + "builder" + "1.2k";

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

async function moveMouse(client, x, y) {
  await client.send("Input.dispatchMouseEvent", { type: "mouseMoved", x, y });
}

async function hover(client, selector) {
  const at = await evalJson(client, `(function(){
    var el = document.querySelector(${JSON.stringify(selector)});
    el.scrollIntoView({ block: "center" });
    var box = el.getBoundingClientRect();
    return { x: Math.round(box.left + box.width / 2), y: Math.round(box.top + box.height / 2) };
  })()`);
  await moveMouse(client, at.x, at.y);
  await sleep(400);
}

async function rest(client) {
  await moveMouse(client, 5, 790);
  await sleep(250);
}

const SNAPSHOT = `(function(){
  var tips = Array.from(document.querySelectorAll('[data-ui="term-tip"]'));
  var tip = tips[0] || null;
  var width = document.documentElement.clientWidth;
  var height = document.documentElement.clientHeight;
  var box = tip ? tip.getBoundingClientRect() : null;
  var panel = document.querySelector('[data-ui="term-panel"]');
  var active = document.activeElement;
  return {
    shell: document.querySelector('[data-ui="remedy-visual-v2"]') !== null,
    tips: tips.length,
    term: tip ? tip.getAttribute('data-term-tip') : null,
    text: tip ? tip.textContent : null,
    breakdown: tip ? tip.querySelectorAll('[data-testid="token-tooltip"]').length : 0,
    inside: box ? box.left >= 8 && box.top >= 0 && box.right <= width - 8 && box.bottom <= height : null,
    focused: active ? (active.getAttribute('data-term') || active.getAttribute('aria-label')) : null,
    panel: panel !== null,
    rows: panel ? Array.from(panel.querySelectorAll('[data-term-entry]')).map(function(el){ return el.getAttribute('data-term-entry'); }) : [],
  };
})()`;

async function key(client, name, code, vk, text, modifiers) {
  const common = { key: name, code, windowsVirtualKeyCode: vk, modifiers };
  await client.send("Input.dispatchKeyEvent", { type: "keyDown", ...common, ...(text ? { text } : {}) });
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", ...common });
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

  await client.send("Page.navigate", { url: PAGE });
  await sleep(2000);
  await rest(client);
  const a = await evalJson(client, SNAPSHOT);
  check("R-a the shell and nothing open", a.shell === true && a.tips === 0 && a.panel === false, a);

  await hover(client, '[data-term="metric.tokens"]');
  const b = await evalJson(client, SNAPSHOT);
  check("R-b the Tokens tooltip with its breakdown", b.tips === 1 && b.term === "metric.tokens"
    && b.text === TOKENS_TEXT && b.breakdown === 1 && b.inside === true, b);
  await rest(client);

  await hover(client, '[data-term="metric.cost"]');
  const c = await evalJson(client, SNAPSHOT);
  check("R-c the Cost tooltip names the basis", c.tips === 1 && c.term === "metric.cost"
    && typeof c.text === "string" && c.text.startsWith("Cost") && c.text.includes("Figures are an estimate")
    && c.inside === true, c);
  await rest(client);

  await evalJson(client, `(document.querySelector('[data-term="metric.tokens"]').focus(), true)`);
  await sleep(60);
  const d = await evalJson(client, SNAPSHOT);
  check("R-d focus opens the breakdown at once", d.tips === 1 && d.term === "metric.tokens"
    && d.breakdown === 1 && d.focused === "metric.tokens", d);
  await evalJson(client, `(document.activeElement.blur(), true)`);
  await sleep(100);

  await key(client, "?", "Slash", 191, "?", 8);
  await sleep(300);
  const e = await evalJson(client, SNAPSHOT);
  check("R-e the ? key opens the Terms panel", e.panel === true && e.focused === "Search the terms"
    && e.rows.length === CATALOG_SIZE, { panel: e.panel, focused: e.focused, rows: e.rows.length });
  console.log(`screenshot bytes: ${writeScreenshot(await client.send("Page.captureScreenshot", { format: "png" }))}`);

  await evalJson(client, `(function(){
    var input = document.querySelector('[data-ui="term-panel"] input');
    var setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
    setter.call(input, 'urgent');
    input.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  })()`);
  await sleep(200);
  const f = await evalJson(client, SNAPSHOT);
  check("R-f the search keeps the inbox's entry", JSON.stringify(f.rows) === JSON.stringify(["panel.decisions"]), f.rows);

  await key(client, "Escape", "Escape", 27, null, 0);
  await sleep(200);
  const g = await evalJson(client, SNAPSHOT);
  check("R-g Escape closes it", g.panel === false, { panel: g.panel });

  const typed = await evalJson(client, `(function(){
    var input = document.querySelector('[data-ui="right-live-panel"] input');
    input.scrollIntoView({ block: "center" });
    input.focus();
    return document.activeElement === input;
  })()`);
  await key(client, "?", "Slash", 191, "?", 8);
  await sleep(300);
  const h = await evalJson(client, SNAPSHOT);
  check("R-h ? typed into a field opens nothing", typed === true && h.panel === false, { typed, panel: h.panel });
  await evalJson(client, `(document.activeElement.blur(), true)`);

  await evalJson(client, `(function(){
    var button = Array.from(document.querySelectorAll('[data-ui="right-live-panel"] button')).find(function(el){ return el.textContent === 'Terms'; });
    button.click();
    return true;
  })()`);
  await sleep(300);
  const i = await evalJson(client, SNAPSHOT);
  check("R-i the Terms button opens it", i.panel === true && i.rows.length === CATALOG_SIZE, { panel: i.panel, rows: i.rows.length });

  await sleep(300);
  check("R-j no console error", problems.length === 0, problems);
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
