// F044 R4's render driver (evidence, not product): drives headless Chrome over CDP (node's global
// WebSocket) through the real `RemedyShell` mounted by main.tsx, and proves the route of a question
// from the bar to the chat as a person meets it (DECISION F044 D4):
//   R-a the bar's placeholder is the reference's own words;
//   R-b a question lists the Ask row first, holding the line and the hint "Ask the chat";
//   R-c Enter opens the chat sheet, which asks the question at once, about the whole project (no
//       task in the read, no scope choice offered), and shows the chat's own unavailable line;
//   R-d the sheet is a fixed dialog on the overlay layer, 24px in from the top and the right;
//   R-e Escape closes the sheet;
//   R-f a line nothing else matches lists only the Ask row, and Enter asks it in a fresh sheet,
//       which its Close button closes;
//   R-g a command's verb lists no Ask row;
//   R-h no asked line is remembered as a recent row;
//   R-i no console error and no uncaught exception was logged in the whole run.
// Screenshots once, while R-c's sheet is open. Prints "RENDER: <n> of 9 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f044-r4-render-chat.png";

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

async function click(client, selector) {
  const at = await evalJson(client, `(function(){
    var el = document.querySelector(${JSON.stringify(selector)});
    if (!el) return null;
    var box = el.getBoundingClientRect();
    return { x: Math.round(box.left + box.width / 2), y: Math.round(box.top + box.height / 2) };
  })()`);
  if (at === null) return false;
  for (const type of ["mouseMoved", "mousePressed", "mouseReleased"]) {
    await client.send("Input.dispatchMouseEvent", { type, x: at.x, y: at.y, button: "left", clickCount: 1 });
  }
  await sleep(250);
  return true;
}

async function key(client, name, code, vk, text) {
  const common = { key: name, code, windowsVirtualKeyCode: vk };
  await client.send("Input.dispatchKeyEvent", { type: "keyDown", ...common, ...(text ? { text } : {}) });
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", ...common });
  await sleep(200);
}

async function type(client, text) {
  await client.send("Input.insertText", { text });
  await sleep(250);
}

const BAR_INPUT = '[data-ui="command-bar"] input';
const REFERENCE_PLACEHOLDER = 'Ask your agent or jump to anything (e.g., "improve error handling")';

const SNAPSHOT = `(function(){
  var input = document.querySelector('${BAR_INPUT}');
  var sheet = document.querySelector('[data-ui="palette-sheet"]');
  var options = sheet ? Array.from(sheet.querySelectorAll('[role="option"]')) : [];
  var first = options[0] || null;
  var chat = document.querySelector('[data-ui="chat-sheet"]');
  var chatStyle = chat ? getComputedStyle(chat) : null;
  var chatBox = chat ? chat.getBoundingClientRect() : null;
  var questions = chat ? Array.from(chat.querySelectorAll('[data-ui="chat-question"]')).map(function(el){ return el.textContent; }) : [];
  return {
    placeholder: input.placeholder,
    focused: document.activeElement === input,
    rows: options.map(function(el){ return el.getAttribute('data-palette-row'); }),
    groups: sheet ? Array.from(sheet.querySelectorAll('[role="group"]')).map(function(el){ return el.getAttribute('aria-label'); }) : [],
    firstLabel: first ? first.firstElementChild.textContent : null,
    firstHint: first ? first.lastElementChild.textContent : null,
    chat: chat !== null,
    chatRole: chat ? chat.getAttribute('role') : null,
    questions: questions,
    unavailable: chat ? chat.querySelectorAll('[data-ui="chat-unavailable"]').length : 0,
    scopeChoice: chat ? chat.querySelectorAll('input[type="checkbox"]').length : 0,
    position: chatStyle ? chatStyle.position : null,
    zIndex: chatStyle ? chatStyle.zIndex : null,
    top: chatBox ? Math.round(chatBox.top) : null,
    rightGap: chatBox ? Math.round(document.documentElement.clientWidth - chatBox.right) : null,
    chats: window.__chats.slice(),
    stored: window.localStorage.getItem('remedy:palette-recent'),
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
  const snap = () => evalJson(client, SNAPSHOT);
  const enter = () => key(client, "Enter", "Enter", 13, "\r");
  const clear = () => evalJson(client, `(function(){
    var input = document.querySelector('${BAR_INPUT}');
    var setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
    setter.call(input, '');
    input.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  })()`);
  const readUrl = (raw) => {
    const url = new URL(raw, "http://127.0.0.1:9010");
    return { path: url.pathname, text: url.searchParams.get("text"), task: url.searchParams.get("task") };
  };

  await client.send("Page.navigate", { url: PAGE });
  await sleep(2000);
  const a = await snap();
  check("R-a the bar's placeholder is the reference's", a.placeholder === REFERENCE_PLACEHOLDER, { placeholder: a.placeholder });

  await click(client, BAR_INPUT);
  await type(client, "why did the build fail?");
  const b = await snap();
  check("R-b a question lists the Ask row first", b.rows[0] === "ask" && b.groups[0] === "Ask"
    && b.firstLabel === "why did the build fail?" && b.firstHint === "Ask the chat",
  { first: b.rows[0], groups: b.groups, label: b.firstLabel, hint: b.firstHint });

  await enter();
  await sleep(600);
  const c = await snap();
  const read = c.chats.length === 1 ? readUrl(c.chats[0]) : null;
  check("R-c Enter asks it at once in the chat sheet, about the whole project", c.chat === true && c.chatRole === "dialog"
    && JSON.stringify(c.questions) === JSON.stringify(["why did the build fail?"]) && read !== null
    && read.path === "/api/jobs/job-1/chat" && read.text === "why did the build fail?" && read.task === null
    && c.unavailable === 1 && c.scopeChoice === 0, { chat: c.chat, role: c.chatRole, questions: c.questions, read,
    unavailable: c.unavailable, scopeChoice: c.scopeChoice });
  console.log(`screenshot bytes: ${writeScreenshot(await client.send("Page.captureScreenshot", { format: "png" }))}`);

  const d = c;
  check("R-d the sheet is fixed on the overlay layer", d.position === "fixed" && d.zIndex === "80" && d.top === 24
    && d.rightGap === 24, { position: d.position, zIndex: d.zIndex, top: d.top, rightGap: d.rightGap });

  await key(client, "Escape", "Escape", 27);
  const e = await snap();
  check("R-e Escape closes the sheet", e.chat === false, { chat: e.chat });

  await click(client, BAR_INPUT);
  await type(client, "zzqx");
  const f1 = await snap();
  await enter();
  await sleep(600);
  const f2 = await snap();
  const closed = await click(client, '[data-ui="chat-sheet"] button');
  const f3 = await snap();
  check("R-f a line nothing matches is asked in a fresh sheet, and Close closes it", JSON.stringify(f1.rows) === '["ask"]'
    && JSON.stringify(f2.questions) === '["zzqx"]' && f2.chats.length === 2 && readUrl(f2.chats[1]).text === "zzqx"
    && closed === true && f3.chat === false, { rows: f1.rows, questions: f2.questions, reads: f2.chats.length, closed, after: f3.chat });

  await click(client, BAR_INPUT);
  await type(client, "pause");
  const g = await snap();
  check("R-g a command's verb lists no Ask row", g.rows[0] === "command:job.pause" && !g.rows.includes("ask"),
    { rows: g.rows });
  await key(client, "Escape", "Escape", 27);
  await clear();

  await key(client, "ArrowDown", "ArrowDown", 40);
  const h = await snap();
  check("R-h no asked line is remembered", !h.rows.some((row) => row.startsWith("recent:"))
    && (h.stored === null || !JSON.parse(h.stored).includes("ask")), { rows: h.rows.slice(0, 3), stored: h.stored });

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
