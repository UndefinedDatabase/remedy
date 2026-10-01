// F292 R2's render driver (evidence, not product): drives headless Chrome over CDP (node's global
// WebSocket) through the real `RemedyShell` mounted by main.tsx, and proves the plan view as a
// person meets it (DECISION F292 D2):
//   P-a the right panel's Plan button opens a dialog named Plan;
//   P-b it shows the version, the approval and the open edit window in words;
//   P-c it lists the three planned tasks in plan order, each with what it waits for, and numbers
//       each task's criteria from 0;
//   P-d the sheet is fixed on the overlay layer, right-anchored 24px in, with the glass surface,
//       the 26px radius and the 14px blur its stylesheet names;
//   P-e the open window's pill wears the blue tint and border of a chosen pill;
//   P-f each task tile is a 14px-radius tile on the second background with a 1px line;
//   P-g the criteria's index and the task id are set in the mono face;
//   P-h the task list scrolls inside the sheet and the sheet stays inside the viewport;
//   P-i Escape closes the view;
//   P-j no console error and no uncaught exception was logged in the whole run.
// Every expected colour and face is read from a probe element styled with the same token, so the
// checks compare computed values with computed values. Screenshots once, while the view is open.
// Prints "RENDER: <n> of 10 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f292-r2-render-plan.png";

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
    el.scrollIntoView({ block: "center" });
    var box = el.getBoundingClientRect();
    return { x: Math.round(box.left + box.width / 2), y: Math.round(box.top + box.height / 2) };
  })()`);
  if (at === null) return false;
  for (const type of ["mouseMoved", "mousePressed", "mouseReleased"]) {
    await client.send("Input.dispatchMouseEvent", { type, x: at.x, y: at.y, button: "left", clickCount: 1 });
  }
  await sleep(300);
  return true;
}

async function press(client, name, code, vk) {
  await client.send("Input.dispatchKeyEvent", { type: "keyDown", key: name, code, windowsVirtualKeyCode: vk });
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: name, code, windowsVirtualKeyCode: vk });
  await sleep(300);
}

const SNAPSHOT = `(function(){
  function probe(prop, value) {
    var el = document.createElement('div');
    el.style.setProperty(prop, value);
    document.body.appendChild(el);
    var out = getComputedStyle(el).getPropertyValue(prop);
    el.remove();
    return out;
  }
  var view = document.querySelector('[data-ui="plan-view"]');
  if (!view) return { open: false };
  var s = getComputedStyle(view);
  var box = view.getBoundingClientRect();
  var pill = view.querySelector('[data-ui="plan-window"]');
  var ps = getComputedStyle(pill);
  var tile = view.querySelector('[data-plan-task]');
  var ts = getComputedStyle(tile);
  // ':scope' keeps each selector inside the tile: a bare 'ol li span' also matches through the
  // tile's own place in the task list and would read the task id instead of the index.
  var index = tile.querySelector(':scope > ol > li > span:first-child');
  var taskId = tile.querySelector(':scope > div > span:first-child');
  var list = view.querySelector('ol[aria-label="Planned tasks"]');
  var body = list.parentElement;
  return {
    open: true,
    role: view.getAttribute('role'), label: view.getAttribute('aria-label'),
    headline: view.querySelector('[data-ui="plan-headline"]').textContent,
    windowText: pill.textContent,
    tasks: Array.from(view.querySelectorAll('[data-plan-task]')).map(function(li){
      return {
        id: li.getAttribute('data-plan-task'),
        meta: li.querySelector('p:last-of-type').textContent,
        criteria: Array.from(li.querySelectorAll('ol li')).map(function(c){ return c.textContent; }),
      };
    }),
    position: s.position, zIndex: s.zIndex, backdrop: s.backdropFilter, radius: s.borderTopLeftRadius,
    background: s.backgroundColor, glass: probe('background-color', 'var(--remedy-glass-bg-strong)'),
    right: Math.round(document.documentElement.clientWidth - box.right), top: Math.round(box.top),
    bottom: Math.round(document.documentElement.clientHeight - box.bottom),
    pillBg: ps.backgroundColor, pillBorder: ps.borderTopColor,
    blue50: probe('background-color', 'var(--remedy-blue-50)'),
    blueStrong: probe('color', 'var(--remedy-blue-strong)'),
    tileRadius: ts.borderTopLeftRadius, tileBg: ts.backgroundColor, tileBorder: ts.borderTopWidth,
    bg2: probe('background-color', 'var(--remedy-bg-2)'),
    indexFont: getComputedStyle(index).fontFamily, taskIdFont: getComputedStyle(taskId).fontFamily,
    mono: probe('font-family', 'var(--remedy-font-mono)'),
    bodyOverflow: getComputedStyle(body).overflowY,
    bodyScrolls: body.scrollHeight >= body.clientHeight,
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
  await sleep(2500);
  const closed = await evalJson(client, SNAPSHOT);
  const clicked = await click(client, '[data-ui="plan-button"]');
  const v = await evalJson(client, SNAPSHOT);
  check("P-a the Plan button opens a dialog named Plan", closed.open === false && clicked && v.open
    && v.role === "dialog" && v.label === "Plan", { before: closed.open, clicked, role: v.role, label: v.label });
  if (!v.open) { finish(ws, results, problems); return; }
  console.log(`screenshot bytes: ${writeScreenshot(await client.send("Page.captureScreenshot", { format: "png" }))}`);

  check("P-b version, approval and the open window in words", v.headline === "Version 2 · waiting for approval"
    && v.windowText === "Open for editing while its approval is open.", { headline: v.headline, window: v.windowText });

  const expected = [
    { id: "T1", meta: "Waits for nothing · pending · spec version 1", criteria: ["0reads a file", "1reports a missing file"] },
    { id: "T2", meta: "Waits for T1 · pending · spec version 1", criteria: ["0rejects an unknown key"] },
    { id: "T3", meta: "Waits for T2 and T1 · pending · spec version 1",
      criteria: ["0covers both paths", "1runs in under a second", "2names each case"] },
  ];
  check("P-c the tasks in plan order with their dependencies and numbered criteria",
    JSON.stringify(v.tasks) === JSON.stringify(expected), v.tasks);

  check("P-d a fixed glass sheet on the overlay layer, right-anchored", v.position === "fixed" && v.zIndex === "80"
    && v.backdrop === "blur(14px)" && v.radius === "26px" && v.background === v.glass && v.right === 24 && v.top === 24,
    { position: v.position, zIndex: v.zIndex, backdrop: v.backdrop, radius: v.radius, background: v.background,
      glass: v.glass, right: v.right, top: v.top });

  check("P-e the open window's pill is tinted and bordered blue", v.pillBg === v.blue50 && v.pillBorder === v.blueStrong,
    { pillBg: v.pillBg, blue50: v.blue50, pillBorder: v.pillBorder, blueStrong: v.blueStrong });

  check("P-f each task is a 14px tile on the second background with a 1px line", v.tileRadius === "14px"
    && v.tileBg === v.bg2 && v.tileBorder === "1px", { radius: v.tileRadius, bg: v.tileBg, bg2: v.bg2, border: v.tileBorder });

  check("P-g the index and the task id use the mono face", v.indexFont === v.mono && v.taskIdFont === v.mono,
    { index: v.indexFont, taskId: v.taskIdFont, mono: v.mono });

  check("P-h the list scrolls inside a sheet that stays in the viewport", v.bodyOverflow === "auto" && v.bodyScrolls
    && v.bottom === 24, { overflow: v.bodyOverflow, scrolls: v.bodyScrolls, bottom: v.bottom });

  await press(client, "Escape", "Escape", 27);
  const after = await evalJson(client, SNAPSHOT);
  check("P-i Escape closes the view", after.open === false, { open: after.open });

  finish(ws, results, problems);
}

function finish(ws, results, problems) {
  setTimeout(() => {
    results.push(problems.length === 0);
    console.log(`${problems.length === 0 ? "PASS" : "FAIL"} P-j no console error ${JSON.stringify(problems)}`);
    const passed = results.filter(Boolean).length;
    console.log(`RENDER: ${passed} of ${results.length} checks pass`);
    ws.close();
    process.exit(passed === results.length ? 0 : 1);
  }, 300);
}

function writeScreenshot({ data }) {
  const bytes = Buffer.from(data, "base64");
  writeFileSync(SCREENSHOT_PNG, bytes);
  return bytes.length;
}

main().catch((err) => { console.error(err); process.exit(1); });
