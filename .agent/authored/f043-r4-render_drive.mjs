// F043 R4's render driver (evidence, not product): drives headless Chrome over CDP (node's
// global WebSocket) through the real `RemedyShell` mounted by main.tsx, in a browser profile that
// has never seen the cockpit, and proves the first-run tour and the shared overlay engine as a
// person meets them (DECISION F043 D4), and the tooltip detail's separator (R-1115):
//   R-a the Welcome tour opens by itself at "Step 1 of 6", titled "The graph", its spotlight on
//       the graph stage's box, and its card off the centre of that box;
//   R-b Next walks the other five steps, each spotlight on its own region's box and each card
//       off that box's centre;
//   R-c Finish closes the tour and records "seen" under the tour's storage key;
//   R-d a reload opens no tour;
//   R-e the Terms panel's "Take the tour" starts it again at step 1, and "Skip tour" closes it;
//   R-f Escape closes a tour started again the same way;
//   R-g the right panel's Tour button opens the result tour through the same frame: the dialog
//       "Guided tour" over its whole-page backdrop, no spotlight, and Escape closes it;
//   R-h the Tokens tooltip's breakdown is a block under a 1px rule, apart from the explanation;
//   R-i no console error and no uncaught exception was logged in the whole run.
// Screenshots once, at R-a. Prints "RENDER: <n> of 9 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f043-r4-render-tour.png";
const STEPS = [
  ["The graph", "brain-graph-stage"],
  ["The timeline", "phase-timeline"],
  ["What is happening now", "right-live-panel"],
  ["Decisions", "decision-inbox-card"],
  ["A note for the job", "chat-input-row"],
  ["Every word explained", "terms-button"],
];
const PAD = 6;

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

async function key(client, name, code, vk, text, modifiers) {
  const common = { key: name, code, windowsVirtualKeyCode: vk, modifiers };
  await client.send("Input.dispatchKeyEvent", { type: "keyDown", ...common, ...(text ? { text } : {}) });
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", ...common });
}

const TOUR = `(function(){
  var card = document.querySelector('[data-ui="first-run-tour"]');
  if (!card) return { open: false, seen: window.localStorage.getItem("remedy:first-run-tour") };
  var spot = document.querySelector('[data-ui="first-run-backdrop"]');
  var title = card.querySelector('h3');
  var label = card.querySelector('p');
  var box = function(el){ var b = el.getBoundingClientRect(); return { left: b.left, top: b.top, right: b.right, bottom: b.bottom }; };
  return {
    open: true,
    name: card.getAttribute('aria-label'),
    role: card.getAttribute('role'),
    label: label ? label.textContent : null,
    title: title ? title.textContent : null,
    spotted: card.getAttribute('data-spot'),
    spot: spot ? box(spot) : null,
    card: box(card),
    seen: window.localStorage.getItem("remedy:first-run-tour"),
  };
})()`;

function targetBox(client, target) {
  return evalJson(client, `(function(){ var b = document.querySelector('[data-ui="${target}"]').getBoundingClientRect();
    return { left: b.left, top: b.top, right: b.right, bottom: b.bottom }; })()`);
}

function spotFits(spot, box) {
  return spot !== null && Math.abs(spot.left - (box.left - PAD)) < 1.5 && Math.abs(spot.top - (box.top - PAD)) < 1.5
    && Math.abs(spot.right - (box.right + PAD)) < 1.5 && Math.abs(spot.bottom - (box.bottom + PAD)) < 1.5;
}

/** True when the card leaves the centre of the spotted box uncovered: a region as wide as the
 *  graph cannot always be clear of a docked card, but the thing a step points at must be seen. */
function clearOfCentre(card, spot) {
  const x = (spot.left + spot.right) / 2;
  const y = (spot.top + spot.bottom) / 2;
  return x < card.left || x > card.right || y < card.top || y > card.bottom;
}

async function clickButton(client, scope, text) {
  return evalJson(client, `(function(){
    var button = Array.from(document.querySelectorAll('${scope} button')).find(function(el){ return el.textContent === ${JSON.stringify(text)}; });
    if (!button) return false;
    button.click();
    return true;
  })()`);
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
  const a = await evalJson(client, TOUR);
  const graph = await targetBox(client, "brain-graph-stage");
  check("R-a the Welcome tour opens by itself on the graph", a.open === true && a.role === "dialog"
    && a.name === "Welcome tour" && a.label === "Step 1 of 6" && a.title === "The graph" && a.spotted === "true"
    && spotFits(a.spot, graph) && clearOfCentre(a.card, a.spot) && a.seen === null, { ...a, graph });
  console.log(`screenshot bytes: ${writeScreenshot(await client.send("Page.captureScreenshot", { format: "png" }))}`);

  const walked = [];
  for (let index = 1; index < STEPS.length; index += 1) {
    await clickButton(client, '[data-ui="first-run-tour"]', "Next");
    await sleep(300);
    const at = await evalJson(client, TOUR);
    const target = await targetBox(client, STEPS[index][1]);
    walked.push({ step: index + 1, ok: at.label === `Step ${index + 1} of 6` && at.title === STEPS[index][0]
      && spotFits(at.spot, target) && clearOfCentre(at.card, at.spot), title: at.title, spot: at.spot, target, card: at.card });
  }
  check("R-b every step spots its own region", walked.every((w) => w.ok), walked.filter((w) => !w.ok));

  await clickButton(client, '[data-ui="first-run-tour"]', "Finish");
  await sleep(300);
  const c = await evalJson(client, TOUR);
  check("R-c Finish closes it and records seen", c.open === false && c.seen === "seen", c);

  await client.send("Page.reload");
  await sleep(2000);
  const d = await evalJson(client, TOUR);
  check("R-d a reload opens no tour", d.open === false && d.seen === "seen", d);

  await clickButton(client, '[data-ui="right-live-panel"]', "Terms");
  await sleep(300);
  await clickButton(client, '[data-ui="term-panel"]', "Take the tour");
  await sleep(400);
  const e1 = await evalJson(client, TOUR);
  const panelGone = await evalJson(client, `document.querySelector('[data-ui="term-panel"]') === null`);
  await clickButton(client, '[data-ui="first-run-tour"]', "Skip tour");
  await sleep(300);
  const e2 = await evalJson(client, TOUR);
  check("R-e Take the tour starts it again and Skip closes it", e1.open === true && e1.label === "Step 1 of 6"
    && panelGone === true && e2.open === false && e2.seen === "seen", { e1: e1.label, panelGone, e2 });

  await clickButton(client, '[data-ui="right-live-panel"]', "Terms");
  await sleep(300);
  await clickButton(client, '[data-ui="term-panel"]', "Take the tour");
  await sleep(400);
  const f1 = await evalJson(client, TOUR);
  await key(client, "Escape", "Escape", 27, null, 0);
  await sleep(300);
  const f2 = await evalJson(client, TOUR);
  check("R-f Escape closes it", f1.open === true && f2.open === false, { f1: f1.open, f2: f2.open });

  await clickButton(client, '[data-ui="right-live-panel"]', "Tour");
  await sleep(600);
  const g1 = await evalJson(client, `(function(){
    var card = document.querySelector('[data-ui="tour-overlay"]');
    return card ? { name: card.getAttribute('aria-label'), role: card.getAttribute('role'), spot: card.getAttribute('data-spot'),
      backdrop: document.querySelector('[data-ui="tour-backdrop"]') !== null, inBody: card.parentElement === document.body } : null;
  })()`);
  await key(client, "Escape", "Escape", 27, null, 0);
  await sleep(300);
  const g2 = await evalJson(client, `document.querySelector('[data-ui="tour-overlay"]') === null`);
  check("R-g the result tour renders through the same frame", g1 !== null && g1.name === "Guided tour"
    && g1.role === "dialog" && g1.spot === "false" && g1.backdrop === true && g1.inBody === true && g2 === true, { g1, g2 });

  const at = await evalJson(client, `(function(){
    var el = document.querySelector('[data-term="metric.tokens"]');
    el.scrollIntoView({ block: "center" });
    var b = el.getBoundingClientRect();
    return { x: Math.round(b.left + b.width / 2), y: Math.round(b.top + b.height / 2) };
  })()`);
  await client.send("Input.dispatchMouseEvent", { type: "mouseMoved", x: at.x, y: at.y });
  await sleep(400);
  const h = await evalJson(client, `(function(){
    var rows = document.querySelector('[data-ui="term-tip"] [data-testid="token-tooltip"]');
    if (!rows) return null;
    var detail = rows.parentElement;
    var style = getComputedStyle(detail);
    var body = detail.previousElementSibling.getBoundingClientRect();
    return { display: style.display, border: style.borderTopWidth, gap: detail.getBoundingClientRect().top - body.bottom };
  })()`);
  check("R-h the breakdown sits apart under a rule", h !== null && h.display === "block" && h.border === "1px"
    && h.gap >= 6, h);

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
