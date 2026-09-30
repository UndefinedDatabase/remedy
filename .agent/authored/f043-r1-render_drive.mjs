// F043 R1's render driver (evidence, not product): drives headless Chrome over CDP (node's
// global WebSocket) through the real `LiveStatusPill` and `PhaseTimeline` mounted by main.tsx,
// and proves the explanation layer's tooltip as a person meets it (DECISION F043 D1):
//   R-a the page carries exactly the seven terms of its two surfaces and no tooltip;
//   R-b a pointer resting on LIVE opens its tooltip after the hover delay and not before: the
//       tooltip is a child of `document.body`, is named by the term's `aria-describedby`, reads
//       the catalog's title and body, is placed and visible, lies inside the viewport, and
//       reaches below the clipping glass card the pill sits in;
//   R-c the pointer leaving closes it;
//   R-d a pointer that only passes through opens nothing;
//   R-e keyboard focus on the Finalized term opens its tooltip at once, above the term, since the
//       timeline sits on the bottom edge, and inside the viewport;
//   R-f Escape closes it and leaves the focus on the term;
//   R-g no console error and no uncaught exception was logged in the whole run.
// Screenshots once, while R-b's tooltip is open. Prints "RENDER: <n> of 7 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f043-r1-render-tooltip.png";
const LIVE_BODY = "This job is running, and the cockpit receives its events the moment they happen.";
const FINALIZED_BODY = "Reached when every task has passed, and held only while that stays true.";

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

async function centreOf(client, term) {
  return evalJson(client, `(function(){
    var el = document.querySelector('[data-term="${term}"]');
    var box = el.getBoundingClientRect();
    return { x: Math.round(box.left + box.width / 2), y: Math.round(box.top + box.height / 2) };
  })()`);
}

const SNAPSHOT = `(function(){
  var tip = document.querySelector('[data-ui="term-tip"]');
  var terms = Array.from(document.querySelectorAll('[data-term]')).map(function(el){ return el.getAttribute('data-term'); });
  var focused = document.activeElement ? document.activeElement.getAttribute('data-term') : null;
  if (!tip) return { terms: terms, tips: 0, focused: focused };
  var box = tip.getBoundingClientRect();
  var term = document.querySelector('[data-term="' + tip.getAttribute('data-term-tip') + '"]');
  var termBox = term.getBoundingClientRect();
  var card = document.querySelector('[data-ui="clip-card"]').getBoundingClientRect();
  var width = document.documentElement.clientWidth;
  var height = document.documentElement.clientHeight;
  return {
    terms: terms,
    tips: document.querySelectorAll('[data-ui="term-tip"]').length,
    focused: focused,
    term: tip.getAttribute('data-term-tip'),
    role: tip.getAttribute('role'),
    inBody: tip.parentElement === document.body,
    described: term.getAttribute('aria-describedby') === tip.id,
    placed: tip.getAttribute('data-placed'),
    visibility: getComputedStyle(tip).visibility,
    text: tip.textContent,
    inside: box.left >= 8 && box.top >= 0 && box.right <= width - 8 && box.bottom <= height,
    belowCard: box.bottom > card.bottom,
    above: box.bottom <= termBox.top,
    box: { left: box.left, top: box.top, right: box.right, bottom: box.bottom },
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
  await moveMouse(client, 400, 300);
  const a = await evalJson(client, SNAPSHOT);
  check("R-a seven terms and no tooltip", a.tips === 0 && JSON.stringify(a.terms) === JSON.stringify([
    "status.live", "phase.job", "phase.planning", "phase.build", "phase.test", "phase.review", "phase.finalized",
  ]), a);

  const live = await centreOf(client, "status.live");
  await moveMouse(client, live.x, live.y);
  await sleep(40);
  const early = await evalJson(client, SNAPSHOT);
  await sleep(400);
  const b = await evalJson(client, SNAPSHOT);
  check("R-b hover opens the tooltip after the delay", early.tips === 0 && b.tips === 1 && b.term === "status.live"
    && b.role === "tooltip" && b.inBody === true && b.described === true && b.placed === "true"
    && b.visibility === "visible" && b.text === `Live${LIVE_BODY}` && b.inside === true && b.belowCard === true,
    { early: early.tips, ...b });
  console.log(`screenshot bytes: ${writeScreenshot(await client.send("Page.captureScreenshot", { format: "png" }))}`);

  await moveMouse(client, 400, 300);
  await sleep(200);
  const c = await evalJson(client, SNAPSHOT);
  check("R-c leaving closes it", c.tips === 0, c);

  await moveMouse(client, live.x, live.y);
  await sleep(30);
  await moveMouse(client, 400, 300);
  await sleep(400);
  const d = await evalJson(client, SNAPSHOT);
  check("R-d passing through opens nothing", d.tips === 0, d);

  await evalJson(client, `(document.querySelector('[data-term="phase.finalized"]').focus(), true)`);
  await sleep(60);
  const e = await evalJson(client, SNAPSHOT);
  check("R-e focus opens it at once, above the term", e.tips === 1 && e.term === "phase.finalized"
    && e.focused === "phase.finalized" && e.placed === "true" && e.text === `Finalized${FINALIZED_BODY}`
    && e.above === true && e.inside === true, e);

  await client.send("Input.dispatchKeyEvent", { type: "keyDown", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
  await sleep(200);
  const f = await evalJson(client, SNAPSHOT);
  check("R-f Escape closes it and keeps the focus", f.tips === 0 && f.focused === "phase.finalized", f);

  await sleep(300);
  check("R-g no console error", problems.length === 0, problems);
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
