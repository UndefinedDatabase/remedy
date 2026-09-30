// F044 R2's render driver (evidence, not product): drives headless Chrome over CDP (node's global
// WebSocket) through the real `RemedyShell` mounted by main.tsx, and proves the command bar's
// dropdown sheet as a person meets it (DECISION F044 D2):
//   R-a the bar is a closed combobox and no sheet is on the page;
//   R-b a click into the bar opens the sheet: every task under Jump, then the two help rows;
//   R-c typing "err" ranks Errata first, then the task whose label holds "error", then the help
//       row that holds its letters, with the match marked;
//   R-d the sheet is fixed under the bar, as wide as the bar, on the popover layer, 14px round,
//       its rows 13px, the mark coloured and bold on no background, the active row tinted;
//   R-e ArrowDown moves the active row to the second, which the combobox names;
//   R-f Enter chooses it: the shell is asked to select that task's node, the sheet closes and
//       the bar empties;
//   R-g the arrow reopens the blank sheet with that task first under Recent, as stored;
//   R-h Escape closes the sheet and leaves the focus in the bar;
//   R-i a click on the "Take the tour" row starts the first-run tour;
//   R-j "term" and Enter open the Terms panel;
//   R-k no console error and no uncaught exception was logged in the whole run.
// Screenshots once, while R-d's sheet is open. Prints "RENDER: <n> of 11 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f044-r2-render-sheet.png";

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
  var input = document.querySelector('${BAR_INPUT}');
  var bar = document.querySelector('[data-ui="command-bar"]');
  var sheet = document.querySelector('[data-ui="palette-sheet"]');
  var options = sheet ? Array.from(sheet.querySelectorAll('[role="option"]')) : [];
  var active = options.find(function(el){ return el.getAttribute('aria-selected') === 'true'; }) || null;
  var first = options[0] || null;
  var mark = first ? first.querySelector('mark') : null;
  var sheetStyle = sheet ? getComputedStyle(sheet) : null;
  var barBox = bar.getBoundingClientRect();
  var sheetBox = sheet ? sheet.getBoundingClientRect() : null;
  return {
    shell: document.querySelector('[data-ui="remedy-visual-v2"]') !== null,
    role: input.getAttribute('role'),
    expanded: input.getAttribute('aria-expanded'),
    descendant: input.getAttribute('aria-activedescendant'),
    value: input.value,
    focused: document.activeElement === input,
    sheet: sheet !== null,
    groups: sheet ? Array.from(sheet.querySelectorAll('[role="group"]')).map(function(el){ return el.getAttribute('aria-label'); }) : [],
    rows: options.map(function(el){ return el.getAttribute('data-palette-row'); }),
    activeId: active ? active.id : null,
    activeIndex: active ? options.indexOf(active) : -1,
    markText: mark ? mark.textContent : null,
    markBg: mark ? getComputedStyle(mark).backgroundColor : null,
    markWeight: mark ? getComputedStyle(mark).fontWeight : null,
    markColor: mark ? getComputedStyle(mark).color : null,
    rowFont: first ? getComputedStyle(first).fontSize : null,
    activeBg: active ? getComputedStyle(active).backgroundColor : null,
    position: sheetStyle ? sheetStyle.position : null,
    zIndex: sheetStyle ? sheetStyle.zIndex : null,
    radius: sheetStyle ? sheetStyle.borderTopLeftRadius : null,
    gap: sheetBox ? Math.round((sheetBox.top - barBox.bottom) * 10) / 10 : null,
    leftDelta: sheetBox ? Math.round(Math.abs(sheetBox.left - barBox.left) * 10) / 10 : null,
    widthDelta: sheetBox ? Math.round(Math.abs(sheetBox.width - barBox.width) * 10) / 10 : null,
    inside: sheetBox ? sheetBox.bottom <= window.innerHeight : null,
    picked: window.__picked.slice(),
    stored: window.localStorage.getItem('remedy:palette-recent'),
    tour: document.querySelector('[data-ui="first-run-tour"]') !== null,
    terms: document.querySelector('[data-ui="term-panel"]') !== null,
  };
})()`;

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
  const a = await evalJson(client, SNAPSHOT);
  check("R-a a closed combobox and no sheet", a.shell === true && a.role === "combobox" && a.expanded === "false"
    && a.sheet === false, { role: a.role, expanded: a.expanded, sheet: a.sheet });

  await click(client, BAR_INPUT);
  const b = await evalJson(client, SNAPSHOT);
  check("R-b a click opens every task and the help rows", b.expanded === "true" && b.focused === true
    && JSON.stringify(b.groups) === JSON.stringify(["Jump", "Help"])
    && JSON.stringify(b.rows) === JSON.stringify(["jump:t1", "jump:t2", "jump:t3", "jump:t4", "jump:t5", "help:terms", "help:tour"]),
  { expanded: b.expanded, groups: b.groups, rows: b.rows });

  await type(client, "err");
  const c = await evalJson(client, SNAPSHOT);
  check("R-c err ranks Errata, then the error task, then the help row", JSON.stringify(c.rows)
    === JSON.stringify(["jump:t4", "jump:t1", "help:terms"]) && c.markText === "Err", { rows: c.rows, mark: c.markText });

  const d = c;
  check("R-d fixed under the bar, on the popover layer, as the reference draws it", d.position === "fixed"
    && d.zIndex === "40" && d.radius === "14px" && d.gap === 6 && d.leftDelta <= 0.5 && d.widthDelta <= 0.5
    && d.inside === true && d.rowFont === "13px" && d.markBg === "rgba(0, 0, 0, 0)" && d.markWeight === "700"
    && d.markColor === "rgb(47, 111, 255)" && d.activeIndex === 0 && d.activeBg === "rgb(238, 244, 255)",
  { position: d.position, zIndex: d.zIndex, radius: d.radius, gap: d.gap, leftDelta: d.leftDelta, widthDelta: d.widthDelta,
    inside: d.inside, rowFont: d.rowFont, markBg: d.markBg, markWeight: d.markWeight, markColor: d.markColor,
    activeIndex: d.activeIndex, activeBg: d.activeBg });
  console.log(`screenshot bytes: ${writeScreenshot(await client.send("Page.captureScreenshot", { format: "png" }))}`);

  await key(client, "ArrowDown", "ArrowDown", 40);
  const e = await evalJson(client, SNAPSHOT);
  check("R-e ArrowDown makes the second row active", e.activeIndex === 1 && e.descendant === e.activeId
    && e.activeId !== null, { activeIndex: e.activeIndex, descendant: e.descendant, activeId: e.activeId });

  await key(client, "Enter", "Enter", 13, "\r");
  const f = await evalJson(client, SNAPSHOT);
  check("R-f Enter jumps to that task", JSON.stringify(f.picked) === JSON.stringify(["node-t1"]) && f.sheet === false
    && f.value === "" && f.expanded === "false", { picked: f.picked, sheet: f.sheet, value: f.value, expanded: f.expanded });

  await key(client, "ArrowDown", "ArrowDown", 40);
  const g = await evalJson(client, SNAPSHOT);
  check("R-g the blank sheet puts it first under Recent", g.sheet === true && g.groups[0] === "Recent"
    && g.rows[0] === "recent:jump:t1" && g.stored === '["jump:t1"]', { groups: g.groups, first: g.rows[0], stored: g.stored });

  await key(client, "Escape", "Escape", 27);
  const h = await evalJson(client, SNAPSHOT);
  check("R-h Escape closes the sheet and keeps the focus", h.sheet === false && h.expanded === "false"
    && h.focused === true, { sheet: h.sheet, expanded: h.expanded, focused: h.focused });

  await type(client, "tour");
  const clicked = await click(client, '[data-palette-row="help:tour"]');
  const i = await evalJson(client, SNAPSHOT);
  check("R-i a click on Take the tour starts it", clicked === true && i.tour === true && i.sheet === false,
    { clicked, tour: i.tour, sheet: i.sheet });
  await key(client, "Escape", "Escape", 27);

  await click(client, BAR_INPUT);
  await type(client, "term");
  await key(client, "Enter", "Enter", 13, "\r");
  const j = await evalJson(client, SNAPSHOT);
  check("R-j term and Enter open the Terms panel", j.terms === true && j.sheet === false, { terms: j.terms, sheet: j.sheet });

  await sleep(300);
  check("R-k no console error", problems.length === 0, problems);
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
