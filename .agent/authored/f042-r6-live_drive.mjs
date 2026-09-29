// F042 R6's live render driver (evidence, not product): drives headless Chrome over CDP (node's
// global WebSocket) through the REAL cockpit served by the REAL UI server over REAL jobs, which
// measure.py registered and planned: alpha holds two jobs, the first run to its end, and beta
// one (DECISION F042 D6). The facts arrive in the JSON file named by the first argument.
//   L-a `?token=<t>` shows the home grid with the cards alpha and beta, each reading "1 active";
//   L-b choosing alpha's card sets the address to `?token=<t>&project=alpha&job=<alpha's newest>`,
//       the cockpit loads that job, the brand rail's switcher reads "alpha" and the right panel's
//       project line, under its "System details" toggle, reads "Project: 2 jobs";
//   L-c with alpha's Story panel open, choosing beta in the rail's switcher sets the address to
//       beta's job, the switcher reads "beta" and the project line "Project: 1 jobs";
//   L-g the switch leaves nothing of alpha behind: the Story panel opened on alpha is gone, and
//       in the 3 seconds after beta is shown no request the page sends names alpha's job, so
//       alpha's event stream and its polls stopped with the switch;
//   L-d Back returns the address to alpha's job, the switcher to "alpha" and the line to 2 jobs;
//   L-e the dock's Overview opens `?token=<t>` and the grid again;
//   L-f no uncaught exception was thrown in the whole run.
// Screenshots twice: the grid after L-a and alpha's cockpit after L-b. Prints
// "LIVE: <n> of 7 checks pass".
import { readFileSync, writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9372";
const FACTS = JSON.parse(readFileSync(process.argv[2], "utf-8"));
const HOME_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f042-r6-live-home.png";
const COCKPIT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f042-r6-live-cockpit.png";

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

const SNAPSHOT = `(function(){
  var rail = document.querySelector('[data-ui="left-brand-rail"] [data-ui="project-switcher"] select');
  var panel = document.querySelector('[data-ui="right-live-panel"]');
  var label = panel ? Array.from(panel.querySelectorAll('strong')).find(function(el){ return el.textContent === 'Project:'; }) : null;
  var line = label && label.parentElement ? label.parentElement.textContent : null;
  return {
    search: window.location.search,
    cards: Array.from(document.querySelectorAll('[data-ui="project-card"]')).map(function(c){
      var a = c.querySelector('[data-ui="card-active"]');
      return { slug: c.getAttribute('data-slug'), active: a ? a.textContent : null };
    }),
    rail: rail ? rail.value : null,
    line: line || null,
  };
})()`;

// The project line sits under the right panel's "System details" toggle, which a remounted
// shell starts closed; each poll opens it the way a person would, with one click.
const OPEN_DETAILS = `(function(){
  var b = Array.from(document.querySelectorAll('[data-ui="right-live-panel"] button[aria-expanded]'))
    .find(function(el){ return el.textContent === 'System details'; });
  if (b && b.getAttribute('aria-expanded') === 'false') b.click();
  return true;
})()`;

async function until(client, predicate, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  await evalJson(client, OPEN_DETAILS);
  let snap = await evalJson(client, SNAPSHOT);
  while (!predicate(snap) && Date.now() < deadline) {
    await sleep(250);
    await evalJson(client, OPEN_DETAILS);
    snap = await evalJson(client, SNAPSHOT);
  }
  return snap;
}

async function shot(client, path) {
  const { data } = await client.send("Page.captureScreenshot", { format: "png" });
  writeFileSync(path, Buffer.from(data, "base64"));
}

async function main() {
  const targets = await (await fetch(`${CDP}/json/list`)).json();
  const page = targets.find((t) => t.type === "page");
  const ws = await connect(page.webSocketDebuggerUrl);
  const problems = [];
  const requests = [];
  const client = makeClient(ws, (msg) => {
    if (msg.method === "Runtime.exceptionThrown") problems.push(`exception: ${JSON.stringify(msg.params).slice(0, 300)}`);
    if (msg.method === "Network.requestWillBeSent") requests.push({ at: Date.now(), url: msg.params.request.url });
  });
  await client.send("Page.enable");
  await client.send("Runtime.enable");
  await client.send("Network.enable");
  const results = [];
  const check = (label, ok, detail) => { results.push(ok); console.log(`${ok ? "PASS" : "FAIL"} ${label} ${JSON.stringify(detail)}`); };
  const t = FACTS.token;
  const alphaNewest = FACTS.jobs.alpha[FACTS.jobs.alpha.length - 1];
  const beta = FACTS.jobs.beta[0];
  const alphaSearch = `?token=${t}&project=alpha&job=${alphaNewest}`;
  const betaSearch = `?token=${t}&project=beta&job=${beta}`;

  await client.send("Page.navigate", { url: `${FACTS.base}?token=${t}` });
  const a = await until(client, (s) => s.cards.length === 2 && s.cards.every((c) => c.active !== null), 20000);
  check("L-a the grid shows both projects", JSON.stringify(a.cards) === JSON.stringify([
    { slug: "alpha", active: "1 active" }, { slug: "beta", active: "1 active" }]), a.cards);
  await shot(client, HOME_PNG);

  await evalJson(client, `(document.querySelector('[data-ui="project-card"][data-slug="alpha"]').click(), true)`);
  const b = await until(client, (s) => s.search === alphaSearch && s.rail === "alpha" && s.line !== null, 30000);
  check("L-b a card opens its project's newest job", b.search === alphaSearch && b.rail === "alpha"
    && (b.line ?? "").startsWith("Project: 2 jobs"), b);
  await shot(client, COCKPIT_PNG);

  await evalJson(client, `(Array.from(document.querySelectorAll('[data-ui="right-live-panel"] button'))
    .find(function(b){ return b.textContent === 'Story'; }).click(), true)`);
  await sleep(500);
  const storyOpen = await evalJson(client, `document.querySelector('[data-ui="story-panel"]') !== null`);
  await evalJson(client, `(function(){
    var select = document.querySelector('[data-ui="left-brand-rail"] [data-ui="project-switcher"] select');
    var setter = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set;
    setter.call(select, 'beta');
    select.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  })()`);
  const c = await until(client, (s) => s.search === betaSearch && s.rail === "beta" && (s.line ?? "").startsWith("Project: 1 jobs"), 30000);
  check("L-c the rail's switcher opens beta", c.search === betaSearch && c.rail === "beta"
    && (c.line ?? "").startsWith("Project: 1 jobs"), c);
  const shownAt = Date.now();
  await sleep(3000);
  const storyAfter = await evalJson(client, `document.querySelector('[data-ui="story-panel"]') !== null`);
  const late = requests.filter((r) => r.at >= shownAt && r.url.includes(alphaNewest)).map((r) => r.url);
  check("L-g nothing of alpha survives the switch", storyOpen === true && storyAfter === false && late.length === 0,
    { storyOpen, storyAfter, late: late.slice(0, 5), betaRequests: requests.filter((r) => r.at >= shownAt && r.url.includes(beta)).length });

  await evalJson(client, `(window.history.back(), true)`);
  const d = await until(client, (s) => s.search === alphaSearch && s.rail === "alpha" && (s.line ?? "").startsWith("Project: 2 jobs"), 30000);
  check("L-d Back returns to alpha", d.search === alphaSearch && d.rail === "alpha"
    && (d.line ?? "").startsWith("Project: 2 jobs"), d);

  await evalJson(client, `(document.querySelector('[data-ui="left-brand-rail"] nav button[aria-label="Overview"]').click(), true)`);
  const e = await until(client, (s) => s.search === `?token=${t}` && s.cards.length === 2, 20000);
  check("L-e the dock returns to the grid", e.search === `?token=${t}` && e.cards.length === 2, { search: e.search });

  check("L-f no uncaught exception", problems.length === 0, problems);
  const passed = results.filter(Boolean).length;
  console.log(`LIVE: ${passed} of ${results.length} checks pass`);
  ws.close();
  process.exit(passed === results.length ? 0 : 1);
}

main().catch((err) => { console.error(err); process.exit(1); });
