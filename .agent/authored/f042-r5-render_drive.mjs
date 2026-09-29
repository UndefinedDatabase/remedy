// F042 R5's render driver (evidence, not product), grown from R4's: drives headless Chrome over
// CDP (node's global WebSocket) through the real `RemedyApp` mounted by main.tsx, and proves the
// project switcher, the address and the home grid as a person meets them (DECISIONS F042 D3, D4):
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
//   R-g a reload with `fixture=single` and a project shows no switcher and the kicker "alpha";
//   R-i (R-1108) on alpha's empty project the sentence starts at most 48 px below the switcher's
//       group, the lower of its box and its "All projects" button, one group rather than two
//       halves of the page, and the button starts within 4 px of the select's left edge;
//   R-j (R-1109) a switch to beta, then a switch to gamma whose answer is held for 800 ms and a
//       Back step at once, leaves the address at the first one after 1500 ms: the answer for a
//       page the reader left is dropped;
//   H-a `?token=t` shows the home grid's cards in the list's order, alpha, beta, gamma, delta:
//       delta's reads "The run is running." in the current tone with "1 active" and "2 open
//       decisions" marked urgent, alpha's "No jobs yet." with "Cost today: $0.25", and beta's
//       carries its fix-it;
//   H-b choosing delta's card sets the address to "?token=t&project=delta&job=d1" with one
//       history entry added;
//   H-c Back returns to "?token=t" and the grid;
//   H-d "All projects" beside the switcher on alpha's empty project opens "?token=t" and the grid;
//   H-e `?token=t&fixture=single` becomes "?token=t&project=alpha" in place, adding no history
//       entry beyond the load itself;
//   H-f `?token=t&fixture=none` invites "No projects yet. Run remedy init in a project's folder
//       to add it.";
//   H-g `?token=t&fixture=many` shows twelve cards from p01 and "Page 1 of 3", and Next shows
//       twelve from p13 and "Page 2 of 3";
//   H-h (R-1110) on the grid, alpha's result line, which has no state, keeps a transparent left
//       border, and delta's, which is running, takes `--remedy-state-current`, rgb(76, 131, 255);
//   H-i at 1100 by 800, where the rail hides its copy block and so the switcher, the dock's
//       Overview button on delta's cockpit is visible and opens "?token=t" and the grid;
//   R-h no console error and no uncaught exception was logged in the whole run.
// Screenshots twice: the empty project after R-a and the grid after H-a. Prints
// "RENDER: <n> of 19 checks pass". A choice is made the way a person's is: the select's value is
// set through the element's own setter and a bubbling `change` event is dispatched, which is
// what React listens for; a card and a button are clicked with `.click()`.
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9370";
const BASE = "http://127.0.0.1:9000/index.html";
const START = "?token=t&project=alpha&focus=n1&level=2";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f042-r5-render-switcher.png";
const HOME_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f042-r5-render-home.png";

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
    homeAligned: (function(){ var h = document.querySelector('[data-ui="project-home"]');
      return h && select ? Math.abs(h.getBoundingClientRect().left - select.getBoundingClientRect().left) <= 4 : null; })(),
    gap: box && empty ? empty.getBoundingClientRect().top - Math.max(box.bottom,
      (document.querySelector('[data-ui="project-home"]') || select).getBoundingClientRect().bottom) : null,
    cards: Array.from(document.querySelectorAll('[data-ui="project-card"]')).map(function(c){
      function text(sel){ var el = c.querySelector(sel); return el ? el.textContent : null; }
      var result = c.querySelector('[data-ui="card-result"]');
      var decisions = c.querySelector('[data-ui="card-decisions"]');
      return { slug: c.getAttribute('data-slug'), result: text('[data-ui="card-result"]'),
        tone: result ? result.getAttribute('data-tone') : null, active: text('[data-ui="card-active"]'),
        decisions: text('[data-ui="card-decisions"]'), urgent: decisions ? decisions.getAttribute('data-urgent') : null,
        cost: text('[data-ui="card-cost"]'), fixIt: text('[data-ui="card-fix-it"]') };
    }),
    pageLine: (function(){ var el = document.querySelector('[data-ui="home-page"]'); return el ? el.textContent : null; })(),
    homeEmpty: (function(){ var el = document.querySelector('[data-ui="home-empty"]'); return el ? el.textContent : null; })(),
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


  await navigate(client, START);
  const i = await evalJson(client, SNAPSHOT);
  check("R-i the empty project is one group", i.gap !== null && i.gap >= 0 && i.gap <= 48 && i.homeAligned === true,
    { gap: i.gap, homeAligned: i.homeAligned });

  await choose(client, "beta");
  await sleep(1000);
  await evalJson(client, `(window.__summaryDelays = { gamma: 800 }, true)`);
  await choose(client, "gamma");
  await evalJson(client, `(window.history.back(), true)`);
  await sleep(1500);
  const j = await evalJson(client, SNAPSHOT);
  check("R-j a switch in flight is dropped by Back", j.search === START && j.select?.value === "alpha", { search: j.search });

  await navigate(client, "?token=t");
  await sleep(600);
  const ha = await evalJson(client, SNAPSHOT);
  const bySlug = Object.fromEntries(ha.cards.map((c) => [c.slug, c]));
  check("H-a the grid draws every card", JSON.stringify(ha.cards.map((c) => c.slug)) === JSON.stringify(["alpha", "beta", "gamma", "delta"])
    && bySlug.delta?.result === "The run is running." && bySlug.delta?.tone === "current" && bySlug.delta?.active === "1 active"
    && bySlug.delta?.decisions === "2 open decisions" && bySlug.delta?.urgent === "true"
    && bySlug.alpha?.result === "No jobs yet." && bySlug.alpha?.cost === "Cost today: $0.25"
    && bySlug.beta?.fixIt === "The folder /work/beta is not there any more.", ha.cards);
  const { data: homeShot } = await client.send("Page.captureScreenshot", { format: "png" });
  writeFileSync(HOME_PNG, Buffer.from(homeShot, "base64"));

  await evalJson(client, `(document.querySelector('[data-ui="project-card"][data-slug="delta"]').click(), true)`);
  await sleep(1200);
  const hb = await evalJson(client, SNAPSHOT);
  check("H-b a card opens its project", hb.search === "?token=t&project=delta&job=d1" && hb.history === ha.history + 1, { search: hb.search });

  await evalJson(client, `(window.history.back(), true)`);
  await sleep(800);
  const hc = await evalJson(client, SNAPSHOT);
  check("H-c Back returns to the grid", hc.search === "?token=t" && hc.cards.length === 4, { search: hc.search });

  await navigate(client, START);
  await evalJson(client, `(document.querySelector('[data-ui="project-home"]').click(), true)`);
  await sleep(800);
  const hd = await evalJson(client, SNAPSHOT);
  check("H-d All projects opens the grid", hd.search === "?token=t" && hd.cards.length === 4, { search: hd.search });

  const before = await evalJson(client, "window.history.length");
  await navigate(client, "?token=t&fixture=single");
  await sleep(600);
  const he = await evalJson(client, SNAPSHOT);
  check("H-e one project skips the grid in place", he.search === "?token=t&fixture=single&project=alpha"
    && he.history === before + 1 && he.cards.length === 0, { search: he.search, history: he.history, before });

  await navigate(client, "?token=t&fixture=none");
  const hf = await evalJson(client, SNAPSHOT);
  check("H-f no project invites remedy init", hf.homeEmpty === "No projects yet. Run remedy init in a project's folder to add it.", { homeEmpty: hf.homeEmpty });

  await navigate(client, "?token=t&fixture=many");
  await sleep(600);
  const hg1 = await evalJson(client, SNAPSHOT);
  await evalJson(client, `(Array.from(document.querySelectorAll('[data-ui="home-pager"] button')).find(function(b){ return b.textContent === 'Next'; }).click(), true)`);
  await sleep(600);
  const hg2 = await evalJson(client, SNAPSHOT);
  check("H-g the grid pages in twelves", hg1.cards.length === 12 && hg1.cards[0].slug === "p01" && hg1.pageLine === "Page 1 of 3"
    && hg2.cards.length === 12 && hg2.cards[0].slug === "p13" && hg2.pageLine === "Page 2 of 3",
    { first: [hg1.cards.length, hg1.cards[0]?.slug, hg1.pageLine], second: [hg2.cards.length, hg2.cards[0]?.slug, hg2.pageLine] });

  await navigate(client, "?token=t");
  await sleep(600);
  const borders = await evalJson(client, `(function(){
    function border(slug){ var el = document.querySelector('[data-ui="project-card"][data-slug="' + slug + '"] [data-ui="card-result"]');
      return el ? getComputedStyle(el).borderLeftColor : null; }
    return { alpha: border("alpha"), delta: border("delta") };
  })()`);
  check("H-h a result with no state has no state colour", borders.alpha === "rgba(0, 0, 0, 0)" && borders.delta === "rgb(76, 131, 255)", borders);

  await client.send("Emulation.setDeviceMetricsOverride", { width: 1100, height: 800, deviceScaleFactor: 1, mobile: false });
  await navigate(client, "?token=t&project=delta&job=d1");
  await sleep(600);
  const dock = await evalJson(client, `(function(){
    var b = document.querySelector('[data-ui="left-brand-rail"] nav button[aria-label="Overview"]');
    var r = b ? b.getBoundingClientRect() : null;
    var copy = document.querySelector('[data-ui="left-brand-rail"] [data-ui="project-switcher"]');
    var shown = r !== null && r.width > 0 && r.height > 0 && r.right <= window.innerWidth;
    var copyShown = copy !== null && copy.getBoundingClientRect().width > 0;
    if (shown) b.click();
    return { shown: shown, copyShown: copyShown, title: b ? b.getAttribute("title") : null };
  })()`);
  await sleep(800);
  const hi = await evalJson(client, SNAPSHOT);
  await client.send("Emulation.clearDeviceMetricsOverride");
  check("H-i the dock opens the grid where the switcher hides", dock.shown === true && dock.copyShown === false
    && dock.title === "All projects" && hi.search === "?token=t" && hi.cards.length === 4, { dock, search: hi.search });

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
