// F042 R3's render driver (evidence, not product): drives headless Chrome over CDP (node's
// global WebSocket) through the real `RemedyApp` mounted by main.tsx, and proves the project
// switcher and the address as a person meets them (DECISION F042 D3):
//   R-a at `?token=t&project=alpha&focus=n1&level=2` the page shows "This project has no jobs
//       yet." and a switcher whose select is named "Project", holds the options "alpha",
//       "beta (folder missing)", "gamma" and "delta", reads "alpha", and whose box lies inside
//       the 1280x800 viewport;
//   R-b the select takes the keyboard's focus;
//   R-c a switch to gamma whose answer is held for 800 ms, overtaken at once by a switch to
//       beta, leaves the address at exactly "?token=t&project=beta" and the select at "beta"
//       after 1500 ms, with ONE history entry added, and the dropped zoom parameters gone;
//   R-d Back returns the address to the first one and the select to "alpha";
//   R-e a switch to delta, whose newest job is d1, sets the address to
//       "?token=t&project=delta&job=d1", the page asks for d1's dashboard, and the shell's own
//       brand rail carries the switcher reading "delta";
//   R-f Back from there returns to alpha's empty project with its switcher;
//   R-g a reload with `fixture=single` shows no switcher and the kicker "alpha";
//   R-h no console error and no uncaught exception was logged in the whole run.
// Screenshots once, after R-a. Prints "RENDER: <n> of 8 checks pass". A choice is made the way
// a person's is: the select's value is set through the element's own setter and a bubbling
// `change` event is dispatched, which is what React listens for.
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9370";
const BASE = "http://127.0.0.1:9000/index.html";
const START = "?token=t&project=alpha&focus=n1&level=2";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f042-r3-render-switcher.png";

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

async function navigate(client, search) {
  await client.send("Page.navigate", { url: `${BASE}${search}` });
  await sleep(1200);
}

async function choose(client, slug) {
  await evalJson(client, `(function(){
    var select = document.querySelector('[data-ui="project-switcher"] select');
    if (!select) throw new Error('no switcher');
    var setter = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set;
    setter.call(select, ${JSON.stringify(slug)});
    select.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  })()`);
}

const SNAPSHOT = `(function(){
  var select = document.querySelector('[data-ui="project-switcher"] select');
  var kicker = document.querySelector('[data-ui="project-kicker"]');
  var empty = document.querySelector('[data-ui="empty-project"]');
  var app = document.querySelector('[data-ui="remedy-app"]');
  var box = select ? select.closest('[data-ui="project-switcher"]').getBoundingClientRect() : null;
  var railSelect = document.querySelector('[data-ui="left-brand-rail"] [data-ui="project-switcher"] select');
  return {
    search: window.location.search,
    history: window.history.length,
    select: select ? { name: select.getAttribute('aria-label'), value: select.value,
      options: Array.from(select.options).map(function(o){ return o.textContent; }) } : null,
    kicker: kicker ? kicker.textContent : null,
    empty: empty ? empty.textContent : null,
    app: app ? app.textContent : null,
    inside: box ? box.top >= 0 && box.left >= 0 && box.bottom <= window.innerHeight && box.right <= window.innerWidth : null,
    rail: railSelect ? railSelect.value : null,
    calls: window.__calls.slice(),
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

  await navigate(client, START);
  const a = await evalJson(client, SNAPSHOT);
  check("R-a empty project and switcher", a.empty === "This project has no jobs yet." && a.select !== null
    && a.select.name === "Project" && a.select.value === "alpha" && a.inside === true
    && JSON.stringify(a.select.options) === JSON.stringify(["alpha", "beta (folder missing)", "gamma", "delta"]), a);
  console.log(`screenshot bytes: ${writeScreenshot(await client.send("Page.captureScreenshot", { format: "png" }))}`);

  const focused = await evalJson(client, `(function(){ var s = document.querySelector('[data-ui="project-switcher"] select'); s.focus(); return document.activeElement === s; })()`);
  check("R-b the select takes focus", focused === true, { focused });

  await evalJson(client, `(window.__summaryDelays = { gamma: 800 }, true)`);
  await choose(client, "gamma");
  await sleep(50);
  await choose(client, "beta");
  await sleep(1500);
  const c = await evalJson(client, SNAPSHOT);
  check("R-c the later switch wins", c.search === "?token=t&project=beta" && c.select?.value === "beta"
    && c.history === a.history + 1, c);

  await evalJson(client, `(window.history.back(), true)`);
  await sleep(800);
  const d = await evalJson(client, SNAPSHOT);
  check("R-d Back returns to alpha", d.search === START && d.select?.value === "alpha", d);

  await choose(client, "delta");
  await sleep(1200);
  const e = await evalJson(client, SNAPSHOT);
  check("R-e a switch opens the newest job", e.search === "?token=t&project=delta&job=d1"
    && e.calls.some((p) => p.startsWith("/api/jobs/d1/dashboard")) && e.rail === "delta",
    { search: e.search, app: e.app, rail: e.rail });

  await evalJson(client, `(window.history.back(), true)`);
  await sleep(800);
  const f = await evalJson(client, SNAPSHOT);
  check("R-f Back returns to the empty project", f.search === START && f.empty !== null && f.select?.value === "alpha", f);

  await navigate(client, "?token=t&project=alpha&fixture=single");
  const g = await evalJson(client, SNAPSHOT);
  check("R-g one project shows no switcher", g.select === null && g.kicker === "alpha", g);

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
