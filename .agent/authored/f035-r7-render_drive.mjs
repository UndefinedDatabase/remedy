// Drives headless Chrome over CDP (node's global WebSocket) to load the
// render harness page built under dist/, then proves the task detail's
// "Who did what" section and the evidence panel's ownership tab as a person
// sees them (DECISION F035 D6), and R-1083's repair to both lists' type
// scale:
//   C-a (i) holds data-ui="ownership-section" after data-ui="unreachable-section"
//       when both exist, and its chips read, in order, Veto then Note;
//   C-b (i)'s sentences equal the fixed view's two sentences for task A
//       character for character, the two-line reason included, and the
//       second line is rendered below the first;
//   C-c every chip of (i) is a pill: computed border-radius at least half its
//       height, and its height at most 24 pixels;
//   C-d (ii) holds no data-ui="ownership-section";
//   C-e (iii)'s section reads exactly the unreadable line and the page's
//       text nowhere holds the server's own error text;
//   C-f (iv)'s tab row reads Diff, Prompt trace, Chat, Ownership, and its
//       list holds the four sentences of the view in order;
//   C-g (R-1083) (i)'s and (iv)'s lists both compute `list-style-type: none`,
//       and every row of both computes `font-size: 13px`.
// R-1083's repair to the harness itself: render-detail.png is captured
// BEFORE the evidence panel mounts, so it shows the task detail with entries
// alone; window.__openPanel() then mounts (iv) for the checks that read it
// and for render-tab.png.
// Saves Page.captureScreenshot PNGs as render-detail.png (before the panel
// mounts) and render-tab.png (after C-f and C-g run), and prints their byte
// counts. Prints one line per check and exits 0 only when every one passed
// and no page exception was thrown. f035-r7-render_measure.py, the caller,
// stops Chrome and the server by pid.
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9364";
const PAGE = "http://127.0.0.1:8994/index.html";
const DETAIL_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f035-r7-worker/render-detail.png";
const TAB_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f035-r7-worker/render-tab.png";
const RAW_ERROR_TEXT = "boom: secret";
const UNREADABLE_LINE = "Who did what could not be read for this job.";

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
  const evaluated = await client.send("Runtime.evaluate", { expression, returnByValue: true });
  if (evaluated.exceptionDetails) {
    throw new Error(`evaluate failed: ${JSON.stringify(evaluated.exceptionDetails).slice(0, 300)}`);
  }
  return evaluated.result.value;
}

async function screenshot(client, path) {
  const { data } = await client.send("Page.captureScreenshot", { format: "png" });
  const bytes = Buffer.from(data, "base64");
  writeFileSync(path, bytes);
  return bytes.length;
}

async function main() {
  const list = await (await fetch(`${CDP}/json/list`)).json();
  const page = list.find((t) => t.type === "page");
  if (!page) throw new Error("no page target");
  const exceptions = [];
  const client = makeClient(await connect(page.webSocketDebuggerUrl), (m) => {
    if (m.method === "Runtime.exceptionThrown") exceptions.push(JSON.stringify(m.params.exceptionDetails).slice(0, 300));
  });
  await client.send("Page.enable");
  await client.send("Runtime.enable");
  await client.send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
  await client.send("Page.navigate", { url: PAGE });
  await sleep(3000);

  const checks = [];
  const fail = (label, why) => checks.push({ label, ok: false, why });
  const pass = (label) => checks.push({ label, ok: true });

  // R-1083's repair — the evidence panel is not mounted yet: this screenshot
  // shows the task detail (i) alone, with its ownership entries.
  const detailBytes = await screenshot(client, DETAIL_PNG);

  // C-a — (i) holds data-ui="ownership-section" after data-ui="unreachable-section"
  // when both exist, and its chips read, in order, Veto then Note.
  const cA = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var html = document.querySelector('#popover-a').innerHTML;
      var posUnreachable = html.indexOf('data-ui="unreachable-section"');
      var posOwnership = html.indexOf('data-ui="ownership-section"');
      var lis = Array.from(document.querySelectorAll('#popover-a section[data-ui="ownership-section"] li'));
      var chips = lis.map(function(li){ return li.querySelectorAll('span')[0].textContent; });
      return { posUnreachable: posUnreachable, posOwnership: posOwnership, chips: chips };
    })())`,
  ));
  if (cA.posUnreachable >= 0 && cA.posOwnership >= 0 && cA.posOwnership > cA.posUnreachable
      && JSON.stringify(cA.chips) === JSON.stringify(["Veto", "Note"])) {
    pass("C-a ownership-section after unreachable-section, chips Veto then Note");
  } else {
    fail("C-a ownership-section after unreachable-section, chips Veto then Note", JSON.stringify(cA));
  }

  // C-b — (i)'s sentences equal the fixed view's two sentences for task A
  // character for character, the two-line reason included, and the second
  // line is rendered below the first: a Range split at the sentence's own
  // "\n" puts the text before it and the text after it at different
  // vertical positions, which only a forced line break (not mere wrapping)
  // guarantees regardless of the popover's width.
  const cB = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var view = window.__ownershipView;
      var taskA = window.__taskA;
      var expected = view.entries.filter(function(e){
        return e.taskId === taskA || e.consequence.taskIds.indexOf(taskA) !== -1;
      }).map(function(e){ return e.sentence; });
      var lis = Array.from(document.querySelectorAll('#popover-a section[data-ui="ownership-section"] li'));
      var actual = lis.map(function(li){ return li.querySelectorAll('span')[1].textContent; });
      var vetoTextNode = lis[0].querySelectorAll('span')[1].firstChild;
      var fullText = vetoTextNode.textContent;
      var nlIndex = fullText.indexOf('\\n');
      var r1 = document.createRange(); r1.setStart(vetoTextNode, 0); r1.setEnd(vetoTextNode, nlIndex);
      var r2 = document.createRange(); r2.setStart(vetoTextNode, nlIndex + 1); r2.setEnd(vetoTextNode, fullText.length);
      var rect1 = r1.getBoundingClientRect();
      var rect2 = r2.getBoundingClientRect();
      return { expected: expected, actual: actual, nlIndex: nlIndex, rect1Top: rect1.top, rect1Bottom: rect1.bottom, rect2Top: rect2.top };
    })())`,
  ));
  const sentencesMatch = JSON.stringify(cB.expected) === JSON.stringify(cB.actual) && cB.expected.length === 2;
  const secondLineBelowFirst = cB.nlIndex > 0 && cB.rect2Top >= cB.rect1Bottom - 1;
  if (sentencesMatch && secondLineBelowFirst) {
    pass("C-b sentences match character for character, the reason's second line renders below the first");
  } else {
    fail("C-b sentences match character for character, the reason's second line renders below the first", JSON.stringify(cB));
  }

  // C-c — every chip of (i) is a pill: border-radius at least half its
  // height, height at most 24 pixels.
  const cC = JSON.parse(await evalJson(
    client,
    `JSON.stringify(Array.from(document.querySelectorAll('#popover-a section[data-ui="ownership-section"] li')).map(function(li){
      var chip = li.querySelectorAll('span')[0];
      var rect = chip.getBoundingClientRect();
      var radius = parseFloat(getComputedStyle(chip).borderRadius);
      return { height: rect.height, radius: radius };
    }))`,
  ));
  const allPills = cC.length > 0 && cC.every((c) => c.height <= 24 && c.radius >= c.height / 2);
  if (allPills) pass("C-c every chip is a pill: radius at least half height, height at most 24px");
  else fail("C-c every chip is a pill: radius at least half height, height at most 24px", JSON.stringify(cC));

  // C-d — (ii) holds no data-ui="ownership-section".
  const cD = await evalJson(client, `document.querySelector('#popover-c [data-ui="ownership-section"]') === null`);
  if (cD === true) pass("C-d task C's popover holds no ownership-section");
  else fail("C-d task C's popover holds no ownership-section", String(cD));

  // C-e — (iii)'s section reads exactly the unreadable line, and the page's
  // text nowhere holds the server's own error text.
  const cE = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var p = document.querySelector('#popover-a-error section[data-ui="ownership-section"] p');
      return { line: p ? p.textContent : null, bodyHoldsRaw: document.body.textContent.indexOf(${JSON.stringify(RAW_ERROR_TEXT)}) !== -1 };
    })())`,
  ));
  if (cE.line === UNREADABLE_LINE && cE.bodyHoldsRaw === false) {
    pass("C-e unreadable section reads exactly the fixed line, raw error text nowhere on the page");
  } else {
    fail("C-e unreadable section reads exactly the fixed line, raw error text nowhere on the page", JSON.stringify(cE));
  }

  // C-g's popover half is checkable now — the ownership list at (i) never
  // moves when the panel mounts — but it is read together with (iv) below so
  // one line reports both halves of R-1083's repair together.
  const cGPopoverBefore = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var list = document.querySelector('#popover-a section[data-ui="ownership-section"] ul');
      var lis = list ? Array.from(list.querySelectorAll('li')) : [];
      return {
        listStyle: list ? getComputedStyle(list).listStyleType : null,
        fontSizes: lis.map(function(li){ return getComputedStyle(li).fontSize; }),
      };
    })())`,
  ));

  // R-1083's repair — mount the evidence panel (iv) now, for C-f, C-g and
  // render-tab.png.
  await evalJson(client, `window.__openPanel()`);
  await sleep(1000);

  // C-f — (iv)'s tab row reads Diff, Prompt trace, Chat, Ownership, and its
  // list holds the four sentences of the view in order.
  const cF = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var tabs = Array.from(document.querySelectorAll('[data-ui="evidence-panel"] [role="tablist"] button')).map(function(b){ return b.textContent; });
      var lis = Array.from(document.querySelectorAll('[data-ui="evidence-panel"] [role="tabpanel"] li'));
      var sentences = lis.map(function(li){ return li.querySelectorAll('span')[1].textContent; });
      var expected = window.__ownershipView.entries.map(function(e){ return e.sentence; });
      return { tabs: tabs, sentences: sentences, expected: expected };
    })())`,
  ));
  const tabsMatch = JSON.stringify(cF.tabs) === JSON.stringify(["Diff", "Prompt trace", "Chat", "Ownership"]);
  const listMatches = JSON.stringify(cF.sentences) === JSON.stringify(cF.expected) && cF.expected.length === 4;
  if (tabsMatch && listMatches) {
    pass("C-f evidence panel's tab row and ownership list read as the fixed view orders them");
  } else {
    fail("C-f evidence panel's tab row and ownership list read as the fixed view orders them", JSON.stringify(cF));
  }

  // C-g (R-1083) — (i)'s and (iv)'s lists both compute list-style-type: none,
  // and every row of both computes font-size: 13px.
  const cGPanel = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var list = document.querySelector('[data-ui="evidence-panel"] [role="tabpanel"] ul');
      var lis = list ? Array.from(list.querySelectorAll('li')) : [];
      return {
        listStyle: list ? getComputedStyle(list).listStyleType : null,
        fontSizes: lis.map(function(li){ return getComputedStyle(li).fontSize; }),
      };
    })())`,
  ));
  const cG = { popover: cGPopoverBefore, panel: cGPanel };
  const bothNoBullet = cG.popover.listStyle === "none" && cG.panel.listStyle === "none";
  const allFontSizes = [...cG.popover.fontSizes, ...cG.panel.fontSizes];
  const bothThirteen = allFontSizes.length > 0 && allFontSizes.every((f) => f === "13px")
    && cG.popover.fontSizes.length > 0 && cG.panel.fontSizes.length > 0;
  if (bothNoBullet && bothThirteen) {
    pass("C-g (i) and (iv)'s ownership lists compute list-style-type none and every row 13px");
  } else {
    fail("C-g (i) and (iv)'s ownership lists compute list-style-type none and every row 13px", JSON.stringify(cG));
  }

  // R-1083's repair — the evidence panel is now mounted: this screenshot
  // shows the tab (iv).
  const tabBytes = await screenshot(client, TAB_PNG);

  for (const e of exceptions) console.log(`EXCEPTION ${e}`);
  for (const c of checks) console.log(c.ok ? `PASS ${c.label}` : `FAILED ${c.label}: ${c.why}`);
  console.log(`SCREENSHOT detail ${DETAIL_PNG} ${detailBytes} bytes`);
  console.log(`SCREENSHOT tab ${TAB_PNG} ${tabBytes} bytes`);
  const allPassed = checks.every((c) => c.ok);
  console.log(`RENDER: ${checks.filter((c) => c.ok).length} of ${checks.length} checks pass`);
  const ok = exceptions.length === 0 && allPassed;
  process.exit(ok ? 0 : 1);
}

main().catch((e) => {
  console.error("FATAL:", e);
  process.exit(1);
});
