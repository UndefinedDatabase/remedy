// Drives headless Chrome over CDP (node's global WebSocket) to load the render harness page
// built under dist/, then proves the in-app story panel as a person sees it (DECISION F039
// D6):
//   C-a the panel is a child of document.body, its computed z-index is 80, and its box lies
//       inside the 1280x800 viewport;
//   C-b the chapter buttons read "The build", "The review" and "The finish" in order, and the
//       position label reads "Chapter 3 of 3: The finish" (the ledger is fully loaded and LIVE
//       sits at its own head, the last chapter);
//   C-c after clicking "The review", the label reads "Chapter 2 of 3: The review", the card
//       holds exactly one beat whose text holds "Verdict: needs repair", and the timeline's own
//       readout begins "Event 1 of 9";
//   C-d Play walks the positions 2 to 9 in order (recorded on window by an effect on the
//       scrub's own position, never re-read from the DOM) and stops with the button reading
//       "Play";
//   C-e Play again restarts at -1, and Space pressed 400 ms later stops the positions growing;
//   C-f Escape removes the panel from the DOM and records the close on window;
//   C-g after a reload with `prefers-reduced-motion: reduce` emulated, Play walks exactly the
//       positions -1, 0, 1 and 9;
//   C-h a reload with `?running=1` shows the running line.
// Screenshots once, right after C-c. Prints "RENDER: <n> of 8 checks pass". Arrow and Escape
// and Space are dispatched as real `keydown` events on `window`, exactly as a person's key
// presses would arrive at the panel's own listener; button presses call `.click()` directly.
// f039-r5-render_measure.py, the caller, stops Chrome and the server by pid.
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9366";
const PAGE = "http://127.0.0.1:8996/index.html";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f039-r5-worker/render-story.png";

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

async function screenshot(client, path) {
  const { data } = await client.send("Page.captureScreenshot", { format: "png" });
  const bytes = Buffer.from(data, "base64");
  writeFileSync(path, bytes);
  return bytes.length;
}

async function pressKey(client, key, code) {
  const codeArg = code ?? key;
  await evalJson(
    client,
    `window.dispatchEvent(new KeyboardEvent("keydown", { key: ${JSON.stringify(key)}, code: ${JSON.stringify(codeArg)}, bubbles: true }))`,
  );
  await sleep(80);
}

async function clickButtonByText(client, scopeSelector, text) {
  await evalJson(
    client,
    `(function(){
      var scope = document.querySelector(${JSON.stringify(scopeSelector)});
      var btn = Array.from(scope.querySelectorAll('button')).find(function(b){ return b.textContent === ${JSON.stringify(text)}; });
      if (!btn) throw new Error('button not found: ${text}');
      btn.click();
      return true;
    })()`,
  );
}

async function positionsLength(client) {
  return evalJson(client, "window.__storyPositions.length");
}

async function positionsSince(client, from) {
  return JSON.parse(await evalJson(client, `JSON.stringify(window.__storyPositions.slice(${from}))`));
}

async function playPauseLabel(client) {
  return evalJson(
    client,
    `(function(){
      var panel = document.querySelector('[data-ui="story-panel"]');
      var btn = Array.from(panel.querySelectorAll('button')).find(function(b){ return b.textContent === "Play" || b.textContent === "Pause"; });
      return btn ? btn.textContent : null;
    })()`,
  );
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
  await sleep(2000);

  const checks = [];
  const fail = (label, why) => checks.push({ label, ok: false, why });
  const pass = (label) => checks.push({ label, ok: true });

  // C-a — the panel is a child of document.body, z-index 80, box inside the viewport.
  const cA = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var isChild = Array.from(document.body.children).some(function(c){
        return c.getAttribute && c.getAttribute('data-ui') === 'story-panel';
      });
      var panel = document.querySelector('[data-ui="story-panel"]');
      var rect = panel.getBoundingClientRect();
      var z = parseInt(getComputedStyle(panel).zIndex, 10);
      return {
        isChild: isChild,
        z: z,
        rect: { left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom },
        viewport: { width: window.innerWidth, height: window.innerHeight },
      };
    })())`,
  ));
  const withinViewport = cA.rect.left >= 0 && cA.rect.top >= 0
    && cA.rect.right <= cA.viewport.width && cA.rect.bottom <= cA.viewport.height;
  if (cA.isChild && cA.z === 80 && withinViewport) {
    pass("C-a the panel is a child of document.body, z-index 80, its box inside the viewport");
  } else {
    fail("C-a the panel is a child of document.body, z-index 80, its box inside the viewport", JSON.stringify(cA));
  }

  // C-b — the chapter buttons read "The build", "The review" and "The finish", and the initial
  // label (LIVE sits at the ledger's own head, the last chapter) reads "Chapter 3 of 3: The finish".
  const cB = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var panel = document.querySelector('[data-ui="story-panel"]');
      var titles = Array.from(panel.querySelectorAll('[data-ui="story-chapters"] button')).map(function(b){ return b.textContent; });
      var label = panel.querySelector('[data-ui="story-position"]').textContent;
      return { titles: titles, label: label };
    })())`,
  ));
  if (JSON.stringify(cB.titles) === JSON.stringify(["The build", "The review", "The finish"])
      && cB.label === "Chapter 3 of 3: The finish") {
    pass('C-b chapter buttons read "The build", "The review", "The finish"; label reads "Chapter 3 of 3: The finish"');
  } else {
    fail('C-b chapter buttons read "The build", "The review", "The finish"; label reads "Chapter 3 of 3: The finish"',
      JSON.stringify(cB));
  }

  // C-c — click "The review": label updates, the card holds one beat with "Verdict: needs
  // repair", and the timeline's own readout begins "Event 1 of 9".
  await clickButtonByText(client, '[data-ui="story-chapters"]', "The review");
  await sleep(150);
  const cC = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var panel = document.querySelector('[data-ui="story-panel"]');
      var label = panel.querySelector('[data-ui="story-position"]').textContent;
      var card = panel.querySelector('[data-ui="story-card"]');
      var beats = card ? Array.from(card.querySelectorAll('p:not([data-ui])')) : [];
      var beatTexts = beats.map(function(b){ return b.textContent; });
      var timelineReadout = document.querySelector('[data-ui="phase-timeline"] .readout, [data-ui="phase-timeline"] [aria-live="polite"]');
      return { label: label, beatCount: beats.length, beatTexts: beatTexts, readout: timelineReadout ? timelineReadout.textContent : null };
    })())`,
  ));
  const shotBytes = await screenshot(client, SCREENSHOT_PNG);
  const oneBeatNeedsRepair = cC.beatCount === 1 && cC.beatTexts[0].indexOf("Verdict: needs repair") !== -1;
  const readoutBegins = typeof cC.readout === "string" && cC.readout.indexOf("Event 1 of 9") === 0;
  if (cC.label === "Chapter 2 of 3: The review" && oneBeatNeedsRepair && readoutBegins) {
    pass('C-c clicking "The review" updates the label, shows one "Verdict: needs repair" beat, timeline readout begins "Event 1 of 9"');
  } else {
    fail('C-c clicking "The review" updates the label, shows one "Verdict: needs repair" beat, timeline readout begins "Event 1 of 9"',
      JSON.stringify(cC));
  }

  // C-d — Play walks the positions 2 to 9 in order and stops, the button reading "Play".
  const beforeD = await positionsLength(client);
  await clickButtonByText(client, '[data-ui="story-panel"]', "Play");
  await sleep(1800);
  const afterD = await positionsSince(client, beforeD);
  const labelD = await playPauseLabel(client);
  const walkedDInOrder = JSON.stringify(afterD) === JSON.stringify([2, 3, 4, 5, 6, 7, 8, 9]);
  if (walkedDInOrder && labelD === "Play") {
    pass('C-d Play walks the positions 2 to 9 in order and stops with the button reading "Play"');
  } else {
    fail('C-d Play walks the positions 2 to 9 in order and stops with the button reading "Play"',
      JSON.stringify({ afterD, labelD }));
  }

  // C-e — Play again restarts at -1 (position 9 has reached the last seq, so storyPlayStart
  // returns -1); Space pressed 400 ms later stops the positions from growing further.
  const beforeE = await positionsLength(client);
  await clickButtonByText(client, '[data-ui="story-panel"]', "Play");
  await sleep(400);
  const afterEFirst = await positionsSince(client, beforeE);
  await pressKey(client, " ", "Space");
  await sleep(500);
  const afterESecond = await positionsSince(client, beforeE);
  const labelE = await playPauseLabel(client);
  const restartedAtMinusOne = afterEFirst.length > 0 && afterEFirst[0] === -1;
  const stoppedGrowing = JSON.stringify(afterESecond) === JSON.stringify(afterEFirst);
  if (restartedAtMinusOne && stoppedGrowing && labelE === "Play") {
    pass('C-e Play again restarts at -1, Space 400 ms later stops the positions growing, button reads "Play"');
  } else {
    fail('C-e Play again restarts at -1, Space 400 ms later stops the positions growing, button reads "Play"',
      JSON.stringify({ afterEFirst, afterESecond, labelE }));
  }
  // C-f — Escape removes the panel and records the close.
  await pressKey(client, "Escape");
  const cF = JSON.parse(await evalJson(
    client,
    `JSON.stringify({
      panelGone: document.querySelector('[data-ui="story-panel"]') === null,
      closed: window.__storyClosed,
    })`,
  ));
  if (cF.panelGone && cF.closed === true) {
    pass("C-f Escape removes the panel from the DOM and records the close");
  } else {
    fail("C-f Escape removes the panel from the DOM and records the close", JSON.stringify(cF));
  }

  // C-g — reload with `prefers-reduced-motion: reduce` emulated; Play walks exactly -1, 0, 1, 9.
  await client.send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
  await client.send("Page.navigate", { url: PAGE });
  await sleep(2000);
  const beforeG = await positionsLength(client);
  await clickButtonByText(client, '[data-ui="story-panel"]', "Play");
  await sleep(1500);
  const afterG = await positionsSince(client, beforeG);
  if (JSON.stringify(afterG) === JSON.stringify([-1, 0, 1, 9])) {
    pass("C-g reduced motion: Play walks exactly the positions -1, 0, 1 and 9");
  } else {
    fail("C-g reduced motion: Play walks exactly the positions -1, 0, 1 and 9", JSON.stringify(afterG));
  }

  // C-h — a reload with `?running=1` shows the running line.
  await client.send("Emulation.setEmulatedMedia", { features: [] });
  await client.send("Page.navigate", { url: `${PAGE}?running=1` });
  await sleep(2000);
  const cH = await evalJson(
    client,
    `(function(){
      var p = document.querySelector('[data-ui="story-running"]');
      return p ? p.textContent : null;
    })()`,
  );
  if (cH === "This job is still running, so its story ends where the record ends now.") {
    pass('C-h the page with ?running=1 shows the running line');
  } else {
    fail('C-h the page with ?running=1 shows the running line', JSON.stringify(cH));
  }

  for (const e of exceptions) console.log(`EXCEPTION ${e}`);
  for (const c of checks) console.log(c.ok ? `PASS ${c.label}` : `FAILED ${c.label}: ${c.why}`);
  console.log(`SCREENSHOT story ${SCREENSHOT_PNG} ${shotBytes} bytes`);
  const allPassed = checks.every((c) => c.ok);
  console.log(`RENDER: ${checks.filter((c) => c.ok).length} of ${checks.length} checks pass`);
  const ok = exceptions.length === 0 && allPassed;
  process.exit(ok ? 0 : 1);
}

main().catch((e) => {
  console.error("FATAL:", e);
  process.exit(1);
});
