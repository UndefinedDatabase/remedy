// F043 R2's render driver (evidence, not product): drives headless Chrome over CDP (node's
// global WebSocket) through the real `TopMetricsBar` and `RightLivePanel` mounted by main.tsx,
// and proves the terms this round adds as a person meets them (DECISIONS F043 D1 and D2):
//   R-a the page carries exactly the terms of the two surfaces, in document order, and no
//       tooltip;
//   R-b a pointer resting on the "Decision inbox" heading opens its tooltip, which reads the
//       catalog's title and body, is a child of `document.body`, and lies inside the viewport
//       although the panel sits against its right edge;
//   R-c a pointer resting on a task row's "Blocked" opens that state's tooltip, and no element
//       inside any task row's button takes focus of its own;
//   R-d a pointer resting on the "Open" metric's label opens its tooltip and not the token
//       tile's breakdown;
//   R-e a pointer resting on the token tile opens its own breakdown and no term's tooltip;
//   R-s a pointer resting on the scrubbed stage's SCRUBBED badge opens its tooltip;
//   R-f keyboard focus on the "Tasks" heading opens its tooltip at once;
//   R-g a card heading's term keeps the heading's own size and colour, and the NowCard's Live
//       badge draws exactly one dot, its word in the badge's own size (the header's and the
//       badge's descendant rules must not reach a term's span);
//   R-h no console error and no uncaught exception was logged in the whole run.
// Each target is scrolled into view before the pointer moves to it. Screenshots once, while
// R-b's tooltip is open. Prints "RENDER: <n> of 9 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f043-r2-render-tooltip.png";
const TERMS = [
  "metric.open", "metric.planned", "metric.done", "metric.progress", "metric.tests", "metric.proof",
  "graph.scrubbed", "status.live", "panel.agent_now", "agent.live", "panel.decisions", "panel.activity", "panel.tasks",
  "task.done", "task.in_progress", "blocked.task", "task.planned", "task.partially_applied",
];
const INBOX_TEXT = "Decision inbox" + "Questions Remedy cannot answer for itself, waiting for you. Open ones come first, "
  + "the most urgent at the top: a question grows more urgent the longer it waits and the more tasks it holds up.";

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
  return {
    terms: Array.from(document.querySelectorAll('[data-term]')).map(function(el){ return el.getAttribute('data-term'); }),
    tips: tips.length,
    term: tip ? tip.getAttribute('data-term-tip') : null,
    text: tip ? tip.textContent : null,
    inBody: tip ? tip.parentElement === document.body : null,
    inside: box ? box.left >= 8 && box.top >= 0 && box.right <= width - 8 && box.bottom <= height : null,
    focused: document.activeElement ? document.activeElement.getAttribute('data-term') : null,
    tokenTip: document.querySelectorAll('[data-testid="token-tooltip"]').length,
    focusableInRows: document.querySelectorAll('[data-ui="task-checklist-card"] button [tabindex]').length,
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
  await sleep(1200);
  await rest(client);
  const a = await evalJson(client, SNAPSHOT);
  check("R-a the surfaces' terms and no tooltip", a.tips === 0 && JSON.stringify(a.terms) === JSON.stringify(TERMS), a);

  await hover(client, '[data-term="panel.decisions"]');
  const b = await evalJson(client, SNAPSHOT);
  check("R-b the inbox heading's tooltip", b.tips === 1 && b.term === "panel.decisions" && b.text === INBOX_TEXT
    && b.inBody === true && b.inside === true, b);
  console.log(`screenshot bytes: ${writeScreenshot(await client.send("Page.captureScreenshot", { format: "png" }))}`);
  await rest(client);

  await hover(client, '[data-term="blocked.task"]');
  const c = await evalJson(client, SNAPSHOT);
  check("R-c a task state's tooltip, and no focus inside the rows", c.tips === 1 && c.term === "blocked.task"
    && c.inside === true && c.focusableInRows === 0, c);
  await rest(client);

  await hover(client, '[data-term="metric.open"]');
  const d = await evalJson(client, SNAPSHOT);
  check("R-d the Open metric's tooltip and no breakdown", d.tips === 1 && d.term === "metric.open"
    && d.tokenTip === 0 && d.inside === true, d);
  await rest(client);

  await hover(client, '[data-ui="top-metrics-bar"] article:last-child');
  const e = await evalJson(client, SNAPSHOT);
  check("R-e the token tile's own breakdown and no term tooltip", e.tokenTip === 1 && e.tips === 0, e);
  await rest(client);

  await hover(client, '[data-term="graph.scrubbed"]');
  const sc = await evalJson(client, SNAPSHOT);
  check("R-s the SCRUBBED badge's tooltip", sc.tips === 1 && sc.term === "graph.scrubbed" && sc.inside === true
    && sc.inBody === true, sc);

  await rest(client);

  await evalJson(client, `(document.querySelector('[data-term="panel.tasks"]').focus(), true)`);
  await sleep(60);
  const f = await evalJson(client, SNAPSHOT);
  check("R-f focus opens the Tasks heading's tooltip at once", f.tips === 1 && f.term === "panel.tasks"
    && f.focused === "panel.tasks" && f.inside === true, f);

  const g = await evalJson(client, `(function(){
    function css(el){ var s = getComputedStyle(el); return s.fontSize + " " + s.color; }
    var term = document.querySelector('[data-term="panel.decisions"]');
    var live = document.querySelector('[data-term="agent.live"]');
    var badge = live.parentElement;
    var dots = Array.from(badge.children).filter(function(el){ return getComputedStyle(el).width === "7px"; }).length;
    return { term: css(term), heading: css(term.closest("h2")), dots: dots,
      liveSize: getComputedStyle(live).fontSize, badgeSize: getComputedStyle(badge).fontSize };
  })()`);
  check("R-g headings and the Live badge keep their own type", g.term === g.heading && g.dots === 1
    && g.liveSize === g.badgeSize, g);

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
