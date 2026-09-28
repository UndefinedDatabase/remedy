// Drives headless Chrome over CDP (node's global WebSocket) to load the render harness page
// built under dist/, then proves the guided tour overlay as a person sees it (DECISION F036
// D6):
//   C-a the backdrop covers the viewport with a non-transparent computed background and the
//       card's z-index is above it;
//   C-b the step label reads "Stop 1 of 6" and the progress list holds six items, the first
//       "current";
//   C-c Previous is disabled at the first stop and, after five ArrowRight presses, Next is
//       disabled and the label reads "Stop 6 of 6";
//   C-d on the first diff stop "Show me" records that anchor and removes the backdrop, and
//       ArrowRight brings it back;
//   C-e the command stop shows its command inside <code>, and an evidence stop shows no
//       "Show me";
//   C-f the overlay's root and backdrop are children of document.body;
//   C-g Escape closes and is recorded;
//   C-h the unreadable remount shows exactly "This job's tour could not be read." and no text
//       of the payload.
// Takes render-tour.png at the first stop (before any stepping) and render-tour-shown.png
// right after "Show me" lifts the backdrop (C-d), and prints "RENDER: <n> of 8 checks pass".
// Arrow-key and Escape steps are dispatched as real `keydown` events on `window`, exactly as a
// person's key presses would arrive at the overlay's own listener; button presses call
// `.click()` directly. f036-r5-render_measure.py, the caller, stops Chrome and the server by
// pid.
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9365";
const PAGE = "http://127.0.0.1:8995/index.html";
const TOUR_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f036-r5-worker/render-tour.png";
const SHOWN_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f036-r5-worker/render-tour-shown.png";
const UNREADABLE_MARKER = "SECRET_MARKER_TEXT_NOT_SHOWN";
const UNREADABLE_LINE = "This job's tour could not be read.";

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

async function pressKey(client, key) {
  await evalJson(client, `window.dispatchEvent(new KeyboardEvent("keydown", { key: ${JSON.stringify(key)}, bubbles: true }))`);
  await sleep(80);
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

  // Screenshot at the first stop, before any interaction.
  const tourBytes = await screenshot(client, TOUR_PNG);

  // C-a — the backdrop covers the viewport with a non-transparent computed background, and the
  // card's z-index is above it.
  const cA = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var backdrop = document.querySelector('[data-ui="tour-backdrop"]');
      var card = document.querySelector('[data-ui="tour-overlay"]');
      var bRect = backdrop.getBoundingClientRect();
      var bStyle = getComputedStyle(backdrop);
      var cStyle = getComputedStyle(card);
      return {
        rect: { top: bRect.top, left: bRect.left, width: bRect.width, height: bRect.height },
        viewport: { width: window.innerWidth, height: window.innerHeight },
        backdropBg: bStyle.backgroundColor,
        backdropZ: parseInt(bStyle.zIndex, 10),
        cardZ: parseInt(cStyle.zIndex, 10),
      };
    })())`,
  ));
  const coversViewport = cA.rect.top === 0 && cA.rect.left === 0
    && cA.rect.width === cA.viewport.width && cA.rect.height === cA.viewport.height;
  // Chrome resolves `color-mix(in srgb, ...)` to a `color(srgb r g b / a)` string rather than
  // `rgba(...)`, so this checks the computed value is neither of the two ways a fully
  // transparent background renders, rather than parsing a specific colour function's syntax.
  const notTransparent = cA.backdropBg.length > 0
    && cA.backdropBg !== "transparent" && cA.backdropBg !== "rgba(0, 0, 0, 0)";
  const cardAbove = cA.cardZ > cA.backdropZ;
  if (coversViewport && notTransparent && cardAbove) {
    pass("C-a backdrop covers the viewport with a non-transparent background, card above it");
  } else {
    fail("C-a backdrop covers the viewport with a non-transparent background, card above it", JSON.stringify(cA));
  }

  // C-b — the step label reads "Stop 1 of 6" and the progress list holds six items, the first
  // "current".
  const cB = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var card = document.querySelector('[data-ui="tour-overlay"]');
      var label = Array.from(card.querySelectorAll('p')).map(function(p){ return p.textContent; })
        .find(function(t){ return /^Stop \\d+ of \\d+$/.test(t); });
      var items = Array.from(document.querySelectorAll('[data-ui="tour-progress"] li'));
      return { label: label, count: items.length, first: items[0] ? items[0].getAttribute('data-state') : null };
    })())`,
  ));
  if (cB.label === "Stop 1 of 6" && cB.count === 6 && cB.first === "current") {
    pass('C-b step label reads "Stop 1 of 6", six progress items, the first "current"');
  } else {
    fail('C-b step label reads "Stop 1 of 6", six progress items, the first "current"', JSON.stringify(cB));
  }

  // C-c — Previous is disabled at the first stop and, after five ArrowRight presses, Next is
  // disabled and the label reads "Stop 6 of 6".
  const previousDisabledAtFirst = await evalJson(
    client,
    `Array.from(document.querySelectorAll('[data-ui="tour-overlay"] button'))
      .find(function(b){ return b.textContent === "Previous"; }).disabled`,
  );
  for (let i = 0; i < 5; i += 1) await pressKey(client, "ArrowRight");
  const cC = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var card = document.querySelector('[data-ui="tour-overlay"]');
      var label = Array.from(card.querySelectorAll('p')).map(function(p){ return p.textContent; })
        .find(function(t){ return /^Stop \\d+ of \\d+$/.test(t); });
      var next = Array.from(card.querySelectorAll('button')).find(function(b){ return b.textContent === "Next"; });
      return { label: label, nextDisabled: next.disabled };
    })())`,
  ));
  if (previousDisabledAtFirst === true && cC.nextDisabled === true && cC.label === "Stop 6 of 6") {
    pass('C-c Previous disabled at the first stop, Next disabled and "Stop 6 of 6" after five ArrowRight presses');
  } else {
    fail('C-c Previous disabled at the first stop, Next disabled and "Stop 6 of 6" after five ArrowRight presses',
      JSON.stringify({ previousDisabledAtFirst, ...cC }));
  }

  // Step back to the first diff stop (index 1): four ArrowLeft presses from index 5.
  for (let i = 0; i < 4; i += 1) await pressKey(client, "ArrowLeft");

  // C-d — on the first diff stop, "Show me" records that anchor and removes the backdrop, and
  // ArrowRight brings it back.
  await evalJson(
    client,
    `Array.from(document.querySelectorAll('[data-ui="tour-overlay"] button'))
      .find(function(b){ return b.textContent === "Show me"; }).click()`,
  );
  await sleep(100);
  const shownBytes = await screenshot(client, SHOWN_PNG);
  const cDAfterShow = JSON.parse(await evalJson(
    client,
    `JSON.stringify({
      backdrop: document.querySelector('[data-ui="tour-backdrop"]') !== null,
      calls: window.__onShowAnchorCalls,
    })`,
  ));
  await pressKey(client, "ArrowRight");
  const backdropAfterStep = await evalJson(client, `document.querySelector('[data-ui="tour-backdrop"]') !== null`);
  const anchorRecorded = cDAfterShow.calls.length === 1
    && cDAfterShow.calls[0].kind === "diff"
    && cDAfterShow.calls[0].ref === "packages/orchestration/result_tour.py";
  if (anchorRecorded && cDAfterShow.backdrop === false && backdropAfterStep === true) {
    pass('C-d "Show me" records the diff anchor and removes the backdrop, ArrowRight brings it back');
  } else {
    fail('C-d "Show me" records the diff anchor and removes the backdrop, ArrowRight brings it back',
      JSON.stringify({ cDAfterShow, backdropAfterStep }));
  }

  // Now at index 2 (the second diff stop). Step to the command stop (index 4).
  await pressKey(client, "ArrowRight");
  await pressKey(client, "ArrowRight");

  // C-e (i) — the command stop shows its command inside <code>, and offers no "Show me".
  const cECommand = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var card = document.querySelector('[data-ui="tour-overlay"]');
      var code = card.querySelector('code');
      var showMe = Array.from(card.querySelectorAll('button')).find(function(b){ return b.textContent === "Show me"; });
      return { code: code ? code.textContent : null, hasShowMe: !!showMe };
    })())`,
  ));
  // Step to the second evidence stop (index 5).
  await pressKey(client, "ArrowRight");
  const cEEvidence = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var card = document.querySelector('[data-ui="tour-overlay"]');
      var showMe = Array.from(card.querySelectorAll('button')).find(function(b){ return b.textContent === "Show me"; });
      return { hasShowMe: !!showMe };
    })())`,
  ));
  if (cECommand.code === "pytest tests/orchestration/test_result_tour.py" && cECommand.hasShowMe === false
      && cEEvidence.hasShowMe === false) {
    pass('C-e command stop shows its command inside <code>, evidence stop shows no "Show me"');
  } else {
    fail('C-e command stop shows its command inside <code>, evidence stop shows no "Show me"',
      JSON.stringify({ cECommand, cEEvidence }));
  }

  // C-f — the overlay's root and backdrop are children of document.body.
  const cF = await evalJson(
    client,
    `Array.from(document.body.children).some(function(c){ return c.getAttribute && c.getAttribute('data-ui') === 'tour-overlay'; })
      && Array.from(document.body.children).some(function(c){ return c.getAttribute && c.getAttribute('data-ui') === 'tour-backdrop'; })`,
  );
  if (cF === true) pass("C-f the overlay's root and backdrop are children of document.body");
  else fail("C-f the overlay's root and backdrop are children of document.body", String(cF));

  // C-g — Escape closes and is recorded.
  await pressKey(client, "Escape");
  const cG = await evalJson(client, `window.__onCloseCalled`);
  if (cG === true) pass("C-g Escape closes and is recorded");
  else fail("C-g Escape closes and is recorded", String(cG));

  // C-h — the unreadable remount shows exactly the fixed unreadable line and no text of the
  // payload.
  await evalJson(client, `window.__remountUnreadable()`);
  await sleep(1500);
  const cH = JSON.parse(await evalJson(
    client,
    `JSON.stringify({
      message: (function(){ var p = document.querySelector('[data-ui="tour-message"]'); return p ? p.textContent : null; })(),
      bodyHoldsMarker: document.body.textContent.indexOf(${JSON.stringify(UNREADABLE_MARKER)}) !== -1,
    })`,
  ));
  if (cH.message === UNREADABLE_LINE && cH.bodyHoldsMarker === false) {
    pass("C-h unreadable remount shows exactly the fixed line, no text of the payload");
  } else {
    fail("C-h unreadable remount shows exactly the fixed line, no text of the payload", JSON.stringify(cH));
  }

  for (const e of exceptions) console.log(`EXCEPTION ${e}`);
  for (const c of checks) console.log(c.ok ? `PASS ${c.label}` : `FAILED ${c.label}: ${c.why}`);
  console.log(`SCREENSHOT tour ${TOUR_PNG} ${tourBytes} bytes`);
  console.log(`SCREENSHOT shown ${SHOWN_PNG} ${shownBytes} bytes`);
  const allPassed = checks.every((c) => c.ok);
  console.log(`RENDER: ${checks.filter((c) => c.ok).length} of ${checks.length} checks pass`);
  const ok = exceptions.length === 0 && allPassed;
  process.exit(ok ? 0 : 1);
}

main().catch((e) => {
  console.error("FATAL:", e);
  process.exit(1);
});
