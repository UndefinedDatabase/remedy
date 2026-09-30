// F044 R3's render driver (evidence, not product): drives headless Chrome over CDP (node's global
// WebSocket) through the real `RemedyShell` mounted by main.tsx, and proves the palette's commands
// as a person meets them (DECISION F044 D3):
//   R-a "pause" lists the pause command first in the Commands section, enabled;
//   R-b Enter sends it, with no argument, and the status line under the bar says it was sent, in
//       the ok tone, fixed 6px under the bar;
//   R-c "resume" lists the resume command disabled, at 45% opacity, its reason as its hint, and
//       Enter sends nothing;
//   R-d "veto" asks for a task under a chip naming the command, listing only the Jump rows; "err"
//       and Enter answer Errata; the reason is asked next with no sheet; "wrong" and Enter send the
//       veto with both arguments;
//   R-e "stop" asks for its optional reason, and Enter on a blank line sends the stop with none;
//   R-f Escape part-way through a note cancels it: no chip, the bar's own placeholder, nothing sent;
//   R-g a refused send says so in the error tone;
//   R-h "add a task" and Enter open the add-task sheet;
//   R-i "reorder" lists the plan edit disabled with the form reason;
//   R-j "answer" and Enter move the focus into the decision inbox;
//   R-k the posts the door received are exactly the four sends above, in order;
//   R-l no console error and no uncaught exception was logged in the whole run.
// Screenshots once, during R-d's task question. Prints "RENDER: <n> of 12 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SCREENSHOT_PNG = "/home/decodeux/Repos/remedy/.remedy-wt/f044-r3-render-commands.png";

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

const SNAPSHOT = `(function(){
  var input = document.querySelector('${BAR_INPUT}');
  var bar = document.querySelector('[data-ui="command-bar"]');
  var sheet = document.querySelector('[data-ui="palette-sheet"]');
  var status = document.querySelector('[data-ui="palette-outcome"]');
  var chip = document.querySelector('[data-ui="palette-chip"]');
  var options = sheet ? Array.from(sheet.querySelectorAll('[role="option"]')) : [];
  var first = options[0] || null;
  var barBox = bar.getBoundingClientRect();
  var statusBox = status ? status.getBoundingClientRect() : null;
  var inbox = document.querySelector('[data-ui="decision-inbox-card"]');
  return {
    placeholder: input.placeholder,
    value: input.value,
    chip: chip ? chip.textContent : null,
    sheet: sheet !== null,
    groups: sheet ? Array.from(sheet.querySelectorAll('[role="group"]')).map(function(el){ return el.getAttribute('aria-label'); }) : [],
    rows: options.map(function(el){ return el.getAttribute('data-palette-row'); }),
    firstDisabled: first ? first.getAttribute('aria-disabled') : null,
    firstHint: first ? first.lastElementChild.textContent : null,
    firstOpacity: first ? getComputedStyle(first).opacity : null,
    status: status ? status.textContent : null,
    tone: status ? status.getAttribute('data-tone') : null,
    statusColor: status ? getComputedStyle(status).color : null,
    statusPosition: status ? getComputedStyle(status).position : null,
    statusGap: statusBox ? Math.round((statusBox.top - barBox.bottom) * 10) / 10 : null,
    posts: window.__posts.map(function(p){ return JSON.stringify({ command: p.command, args: p.args }); }),
    addTask: document.querySelector('[data-ui="add-task-sheet"]') !== null,
    inInbox: inbox !== null && inbox.contains(document.activeElement),
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
  // Escape closes the sheet and keeps what was typed, so a check that escapes with text in the bar
  // empties it the way a person would, through the input's own change event.
  const clear = () => evalJson(client, `(function(){
    var input = document.querySelector('${BAR_INPUT}');
    var setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
    setter.call(input, '');
    input.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  })()`);

  await client.send("Page.navigate", { url: PAGE });
  await sleep(2000);
  await click(client, BAR_INPUT);

  await type(client, "pause");
  const a = await snap();
  check("R-a pause lists its command first, enabled", a.groups[0] === "Commands" && a.rows[0] === "command:job.pause"
    && a.firstDisabled === null, { groups: a.groups, first: a.rows[0], disabled: a.firstDisabled });

  await enter();
  await sleep(300);
  const b = await snap();
  check("R-b Enter sends it and says so under the bar", b.posts.length === 1
    && b.posts[0] === JSON.stringify({ command: "job.pause", args: {} }) && b.status === "Sent: job.pause."
    && b.tone === "ok" && b.statusColor === "rgb(52, 194, 126)" && b.statusPosition === "fixed" && b.statusGap === 6
    && b.sheet === false, { posts: b.posts, status: b.status, tone: b.tone, color: b.statusColor, position: b.statusPosition, gap: b.statusGap });

  await type(client, "resume");
  const c1 = await snap();
  await enter();
  const c2 = await snap();
  check("R-c resume is disabled with its reason and sends nothing", c1.rows[0] === "command:job.unpause"
    && c1.firstDisabled === "true" && c1.firstHint === "The job is not paused." && c1.firstOpacity === "0.45"
    && c2.posts.length === 1 && c2.chip === null, { first: c1.rows[0], disabled: c1.firstDisabled, hint: c1.firstHint,
    opacity: c1.firstOpacity, posts: c2.posts.length, chip: c2.chip });
  await key(client, "Escape", "Escape", 27);
  await clear();

  await type(client, "veto");
  await enter();
  const d1 = await snap();
  await type(client, "err");
  const d2 = await snap();
  console.log(`screenshot bytes: ${writeScreenshot(await client.send("Page.captureScreenshot", { format: "png" }))}`);
  await enter();
  const d3 = await snap();
  await type(client, "wrong");
  await enter();
  await sleep(300);
  const d4 = await snap();
  check("R-d the veto asks a task, then a reason, then sends both", d1.chip === "Veto the task"
    && d1.placeholder === "Which task?" && JSON.stringify(d1.groups) === JSON.stringify(["Jump"])
    && d2.rows[0] === "jump:t4" && d3.placeholder === "Why veto it?" && d3.sheet === false && d3.chip === "Veto the task"
    && d4.posts[1] === JSON.stringify({ command: "job.veto-task", args: { task_id: "t4", reason: "wrong" } })
    && d4.chip === null && d4.status === "Sent: job.veto-task.", { d1: [d1.chip, d1.placeholder, d1.groups],
    d2: d2.rows[0], d3: [d3.placeholder, d3.sheet], d4: [d4.posts[1], d4.chip, d4.status] });

  await type(client, "stop");
  await enter();
  const e1 = await snap();
  await enter();
  await sleep(300);
  const e2 = await snap();
  check("R-e the stop's reason is optional", e1.placeholder === "Why stop? (optional)"
    && e2.posts[2] === JSON.stringify({ command: "job.stop", args: {} }), { placeholder: e1.placeholder, post: e2.posts[2] });

  await type(client, "note");
  await enter();
  const f1 = await snap();
  await key(client, "Escape", "Escape", 27);
  const f2 = await snap();
  check("R-f Escape cancels a flow part-way", f1.chip === "Send a message to the job"
    && f1.placeholder === "Your message to the job" && f2.chip === null && f2.placeholder.startsWith("Jump to anything")
    && f2.posts.length === 3, { f1: [f1.chip, f1.placeholder], f2: [f2.chip, f2.placeholder, f2.posts.length] });

  await type(client, "start the app");
  await enter();
  await sleep(300);
  const g = await snap();
  check("R-g a refused send says so in the error tone", g.posts[3] === JSON.stringify({ command: "job.preview-start", args: {} })
    && g.status === "The job refused it in its current state, so nothing was done." && g.tone === "error"
    && g.statusColor === "rgb(239, 99, 99)", { post: g.posts[3], status: g.status, tone: g.tone, color: g.statusColor });

  await type(client, "add a task");
  await enter();
  const h = await snap();
  check("R-h add a task opens the add-task sheet", h.addTask === true, { addTask: h.addTask });
  await key(client, "Escape", "Escape", 27);

  await click(client, BAR_INPUT);
  await type(client, "reorder");
  const i = await snap();
  check("R-i a plan edit is disabled with the form reason", i.rows[0] === "command:job.plan-reorder"
    && i.firstDisabled === "true" && i.firstHint === "The palette cannot ask for this command's arguments yet.",
  { first: i.rows[0], disabled: i.firstDisabled, hint: i.firstHint });
  await key(client, "Escape", "Escape", 27);
  await clear();

  await type(client, "answer");
  await enter();
  const j = await snap();
  check("R-j answer moves the focus into the decision inbox", j.inInbox === true, { inInbox: j.inInbox });

  const k = await snap();
  check("R-k the door received exactly the four sends", k.posts.length === 4, k.posts);

  await sleep(300);
  check("R-l no console error", problems.length === 0, problems);
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
