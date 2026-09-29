// Drives headless Chrome over CDP (node's global WebSocket) to load the render harness page
// built under dist/, then proves the results panel as a person sees it (DECISION F041 D5):
//   C-a the panel is a child of document.body, its computed z-index is 80, and its box lies
//       inside the 1280x800 viewport;
//   C-b the README shows "Fixture app", holds exactly one image whose address holds
//       "path=captures%2Fone.png" and "token=render-token" and whose naturalWidth is above 0,
//       shows "elsewhere shot" as text, no resource entry names "elsewhere.png", and the full
//       README link holds "path=README.md";
//   C-c the grid holds three buttons captioned "one", "two" and "three", the second opens the
//       dialog reading "2 of 3 · two" with focus on Close, ArrowRight reads "3 of 3 · three"
//       twice over, ArrowLeft "2 of 3 · two", and Escape removes the dialog while the panel
//       stays;
//   C-d the card reads "The app is not running." with "Start app" and no link, a click posts
//       job.preview-start with args {} and the CSRF header, and the card reaches "Live on port
//       5173." within 15 seconds with the link to "http://127.0.0.1:5173/", while a sample every
//       50 ms finds no link before the card's data-state reads "live";
//   C-e "Stop app" posts job.preview-stop and the card returns to "The app is not running." with
//       no link;
//   C-f a reload with ?preview=failed shows the reason and "Try again";
//   C-g a reload with ?preview=na shows "This project has no app to run." and no button in the
//       card;
//   C-h Escape removes the panel and records the close, the count of preview reads then stays
//       unchanged over a 3-second idle wait, and no console error was logged in the whole run.
// Screenshots once, right after C-b. Prints "RENDER: <n> of 8 checks pass". Arrow, Escape and
// button presses are dispatched as real events (keydown on window, .click() on the element), the
// way a person's key presses and clicks would arrive. f041-r5-render_measure.py, the caller,
// stops Chrome and the server by pid.
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9368";
const PAGE = "http://127.0.0.1:8998/index.html";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f041-r5-worker/render-results.png";

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
    `window.dispatchEvent(new KeyboardEvent("keydown", { key: ${JSON.stringify(key)}, code: ${JSON.stringify(codeArg)}, bubbles: true, cancelable: true }))`,
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

async function waitForImagesLoaded(client, selector, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const ready = await evalJson(
      client,
      `(function(){
        var imgs = Array.from(document.querySelectorAll(${JSON.stringify(selector)}));
        return imgs.length > 0 && imgs.every(function(img){ return img.complete; });
      })()`,
    );
    if (ready) return true;
    await sleep(100);
  }
  return false;
}

async function main() {
  const list = await (await fetch(`${CDP}/json/list`)).json();
  const page = list.find((t) => t.type === "page");
  if (!page) throw new Error("no page target");
  const exceptions = [];
  const consoleErrors = [];
  const client = makeClient(await connect(page.webSocketDebuggerUrl), (m) => {
    if (m.method === "Runtime.exceptionThrown") {
      exceptions.push(JSON.stringify(m.params.exceptionDetails).slice(0, 300));
    } else if (m.method === "Runtime.consoleAPICalled" && m.params.type === "error") {
      consoleErrors.push(JSON.stringify(m.params.args).slice(0, 300));
    }
  });
  await client.send("Page.enable");
  await client.send("Runtime.enable");
  await client.send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
  await client.send("Page.navigate", { url: PAGE });
  await sleep(2000);

  const results = {};
  const record = (label, ok, why) => { results[label] = { ok, why }; };

  // C-a — the panel is a child of document.body, z-index 80, box inside the viewport.
  const cA = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var isChild = Array.from(document.body.children).some(function(c){
        return c.getAttribute && c.getAttribute('data-ui') === 'artifacts-panel';
      });
      var panel = document.querySelector('[data-ui="artifacts-panel"]');
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
  record("C-a the panel is a child of document.body, z-index 80, its box inside the viewport",
    cA.isChild && cA.z === 80 && withinViewport, JSON.stringify(cA));

  // C-b — the README fragment: heading, the one recognised image addressed and loaded, the
  // dropped image's alt text, no request for the dropped image, and the full-README link.
  await waitForImagesLoaded(client, '[data-ui="artifacts-readme"] img', 5000);
  const cB = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var article = document.querySelector('[data-ui="artifacts-readme"]');
      var h1 = article.querySelector('h1');
      var imgs = Array.from(article.querySelectorAll('img'));
      var resources = performance.getEntriesByType('resource').map(function(r){ return r.name; });
      var fullLink = document.querySelector('[data-ui="artifacts-readme-full"]');
      return {
        h1Text: h1 ? h1.textContent : null,
        imgCount: imgs.length,
        imgSrc: imgs.length ? imgs[0].src : null,
        imgNaturalWidth: imgs.length ? imgs[0].naturalWidth : 0,
        articleText: article.textContent,
        resourceNamesElsewhere: resources.some(function(u){ return u.indexOf('elsewhere.png') !== -1; }),
        fullLinkHref: fullLink ? fullLink.getAttribute('href') : null,
      };
    })())`,
  ));
  const cBOk = cB.h1Text === "Fixture app"
    && cB.imgCount === 1
    && typeof cB.imgSrc === "string" && cB.imgSrc.indexOf("path=captures%2Fone.png") !== -1
    && cB.imgSrc.indexOf("token=render-token") !== -1
    && cB.imgNaturalWidth > 0
    && cB.articleText.indexOf("elsewhere shot") !== -1
    && !cB.resourceNamesElsewhere
    && typeof cB.fullLinkHref === "string" && cB.fullLinkHref.indexOf("path=README.md") !== -1;
  record('C-b the README shows "Fixture app", the one recognised image loaded and addressed, '
    + '"elsewhere shot" as text, no request for it, and the full README link', cBOk, JSON.stringify(cB));

  const shotBytes = await screenshot(client, SCREENSHOT_PNG);

  // C-c — the screenshot grid and the lightbox it opens.
  const captions = JSON.parse(await evalJson(
    client,
    `JSON.stringify(Array.from(document.querySelectorAll('[data-ui="artifacts-captures"] button')).map(function(b){ return b.getAttribute('aria-label'); }))`,
  ));
  await evalJson(
    client,
    `(function(){
      var buttons = document.querySelectorAll('[data-ui="artifacts-captures"] button');
      buttons[1].click();
      return true;
    })()`,
  );
  await sleep(150);
  const openedCaption = await evalJson(client, `document.querySelector('[data-ui="artifact-lightbox-caption"]').textContent`);
  const focusedIsClose = await evalJson(
    client,
    `(function(){
      var dialog = document.querySelector('[data-ui="artifact-lightbox"]');
      var closeBtn = Array.from(dialog.querySelectorAll('button')).find(function(b){ return b.textContent === 'Close'; });
      return document.activeElement === closeBtn;
    })()`,
  );
  await pressKey(client, "ArrowRight");
  const afterRight1 = await evalJson(client, `document.querySelector('[data-ui="artifact-lightbox-caption"]').textContent`);
  await pressKey(client, "ArrowRight");
  const afterRight2 = await evalJson(client, `document.querySelector('[data-ui="artifact-lightbox-caption"]').textContent`);
  await pressKey(client, "ArrowLeft");
  const afterLeft = await evalJson(client, `document.querySelector('[data-ui="artifact-lightbox-caption"]').textContent`);
  await pressKey(client, "Escape");
  const afterEscapeC = JSON.parse(await evalJson(
    client,
    `JSON.stringify({
      dialogGone: document.querySelector('[data-ui="artifact-lightbox"]') === null,
      panelStill: document.querySelector('[data-ui="artifacts-panel"]') !== null,
    })`,
  ));
  const cCOk = JSON.stringify(captions) === JSON.stringify(["Open screenshot one", "Open screenshot two", "Open screenshot three"])
    && openedCaption === "2 of 3 · two"
    && focusedIsClose === true
    && afterRight1 === "3 of 3 · three"
    && afterRight2 === "3 of 3 · three"
    && afterLeft === "2 of 3 · two"
    && afterEscapeC.dialogGone === true
    && afterEscapeC.panelStill === true;
  record('C-c three buttons captioned one/two/three; the second opens the dialog at "2 of 3 '
    + '· two" focused on Close, ArrowRight caps at "3 of 3 · three", ArrowLeft reads '
    + '"2 of 3 · two", Escape removes the dialog and keeps the panel', cCOk, JSON.stringify({
    captions, openedCaption, focusedIsClose, afterRight1, afterRight2, afterLeft, afterEscapeC,
  }));

  // C-d — the stopped card, a start, and the walk to live within 15 seconds with no premature
  // link (sampled every 50 ms).
  const initialCardD = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var card = document.querySelector('[data-ui="app-preview-card"]');
      var link = card.querySelector('[data-ui="app-preview-link"]');
      var startBtn = Array.from(card.querySelectorAll('button')).find(function(b){ return b.textContent === 'Start app'; });
      return { text: card.textContent, hasLink: !!link, hasStartBtn: !!startBtn };
    })())`,
  ));
  await clickButtonByText(client, '[data-ui="app-preview-card"]', "Start app");
  let liveReached = false;
  let prematureLink = false;
  const deadlineD = Date.now() + 15000;
  while (Date.now() < deadlineD) {
    const sample = JSON.parse(await evalJson(
      client,
      `JSON.stringify({
        state: document.querySelector('[data-ui="app-preview-card"]').getAttribute('data-state'),
        hasLink: !!document.querySelector('[data-ui="app-preview-link"]'),
      })`,
    ));
    if (sample.hasLink && sample.state !== "live") prematureLink = true;
    if (sample.state === "live") { liveReached = true; break; }
    await sleep(50);
  }
  const finalCardD = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var card = document.querySelector('[data-ui="app-preview-card"]');
      var link = card.querySelector('[data-ui="app-preview-link"]');
      return { text: card.textContent, href: link ? link.getAttribute('href') : null };
    })())`,
  ));
  const callsAfterStart = JSON.parse(await evalJson(client, "JSON.stringify(window.__previewCalls)"));
  const startCall = callsAfterStart.find((c) => c.path.includes("/commands") && c.body
    && JSON.parse(c.body).command === "job.preview-start");
  const startCallOk = !!startCall
    && JSON.stringify(JSON.parse(startCall.body).args) === "{}"
    && Object.keys(startCall.headers).some((h) => h.toLowerCase() === "x-remedy-csrf");
  const cDOk = initialCardD.text.indexOf("The app is not running.") !== -1
    && initialCardD.hasStartBtn && !initialCardD.hasLink
    && liveReached && !prematureLink
    && finalCardD.text.indexOf("Live on port 5173.") !== -1
    && finalCardD.href === "http://127.0.0.1:5173/"
    && startCallOk;
  record('C-d the stopped card with Start app and no link; a click posts job.preview-start with '
    + "args {} and the CSRF header; the card reaches live within 15 seconds with no premature link",
    cDOk, JSON.stringify({ initialCardD, liveReached, prematureLink, finalCardD, startCallOk }));

  // C-e — Stop app posts job.preview-stop and returns to stopped with no link.
  await clickButtonByText(client, '[data-ui="app-preview-card"]', "Stop app");
  await sleep(300);
  const afterStopE = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var card = document.querySelector('[data-ui="app-preview-card"]');
      var link = card.querySelector('[data-ui="app-preview-link"]');
      return { text: card.textContent, hasLink: !!link };
    })())`,
  ));
  const callsAfterStop = JSON.parse(await evalJson(client, "JSON.stringify(window.__previewCalls)"));
  const stopCall = callsAfterStop.find((c) => c.path.includes("/commands") && c.body
    && JSON.parse(c.body).command === "job.preview-stop");
  const cEOk = afterStopE.text.indexOf("The app is not running.") !== -1 && !afterStopE.hasLink && !!stopCall;
  record('C-e Stop app posts job.preview-stop and the card returns to "The app is not '
    + 'running." with no link', cEOk, JSON.stringify({ afterStopE, stopCall }));

  // C-h — Escape closes the panel and records it; the read count then stays put over a 3-second
  // idle wait; no console error, checked over the whole run once C-f and C-g have also run.
  const readCountBeforeH = await evalJson(client, "window.__previewReadCount");
  await pressKey(client, "Escape");
  await sleep(200);
  const afterEscapeH = JSON.parse(await evalJson(
    client,
    `JSON.stringify({
      panelGone: document.querySelector('[data-ui="artifacts-panel"]') === null,
      closed: window.__artifactsClosed,
    })`,
  ));
  await sleep(3000);
  const readCountAfterH = await evalJson(client, "window.__previewReadCount");
  const idleDrained = readCountAfterH === readCountBeforeH;

  // C-f — a reload with ?preview=failed shows the reason and "Try again".
  await client.send("Page.navigate", { url: `${PAGE}?preview=failed` });
  await sleep(2000);
  const cF = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var card = document.querySelector('[data-ui="app-preview-card"]');
      var tryAgain = Array.from(card.querySelectorAll('button')).find(function(b){ return b.textContent === 'Try again'; });
      return { text: card.textContent, hasTryAgain: !!tryAgain };
    })())`,
  ));
  const cFOk = cF.text.indexOf("The app could not be shown.") !== -1
    && cF.text.indexOf("started but health check failed: connection refused") !== -1
    && cF.hasTryAgain;
  record('C-f a reload with ?preview=failed shows the reason and "Try again"', cFOk, JSON.stringify(cF));

  // C-g — a reload with ?preview=na shows the not-applicable line and no button in the card.
  await client.send("Page.navigate", { url: `${PAGE}?preview=na` });
  await sleep(2000);
  const cG = JSON.parse(await evalJson(
    client,
    `JSON.stringify((function(){
      var card = document.querySelector('[data-ui="app-preview-card"]');
      return { text: card.textContent, buttonCount: card.querySelectorAll('button').length };
    })())`,
  ));
  const cGOk = cG.text.indexOf("This project has no app to run.") !== -1 && cG.buttonCount === 0;
  record('C-g a reload with ?preview=na shows "This project has no app to run." and no button '
    + "in the card", cGOk, JSON.stringify(cG));

  const cHOk = afterEscapeH.panelGone === true && afterEscapeH.closed === true
    && idleDrained && consoleErrors.length === 0;
  record("C-h Escape removes the panel and records the close, the read count stays put over a "
    + "3-second idle wait, and no console error was logged in the whole run",
    cHOk, JSON.stringify({ afterEscapeH, readCountBeforeH, readCountAfterH, consoleErrors }));

  const order = Object.keys(results);
  for (const e of exceptions) console.log(`EXCEPTION ${e}`);
  for (const label of order) {
    const r = results[label];
    console.log(r.ok ? `PASS ${label}` : `FAILED ${label}: ${r.why}`);
  }
  console.log(`SCREENSHOT results ${SCREENSHOT_PNG} ${shotBytes} bytes`);
  const passCount = order.filter((label) => results[label].ok).length;
  console.log(`RENDER: ${passCount} of ${order.length} checks pass`);
  const ok = exceptions.length === 0 && passCount === order.length;
  process.exit(ok ? 0 : 1);
}

main().catch((e) => {
  console.error("FATAL:", e);
  process.exit(1);
});
