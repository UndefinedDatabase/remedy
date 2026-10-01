// F292 R5's render driver (evidence, not product): drives headless Chrome over CDP (node's global
// WebSocket) through the real `RemedyShell` mounted by main.tsx, and proves the plan view's merge
// and split as a person meets them (DECISION F292 D5):
//   M-a each task offers Merge and Split, and T2's Split, on its one criterion, is disabled with
//       the reason;
//   M-b Merge on T3 lists the three other tasks to choose; Merge tasks with none chosen is
//       answered in the form and sends nothing;
//   M-c choosing T4 shows what the merge will do, and Merge tasks sends ONE job.plan-merge-tasks
//       naming T3 and T4 against version 2; the save is said and the dashboard read again;
//   M-d once version 3 arrives, Split on T1 opens with criterion 1 in part 2 and says what the
//       split will do; with both criteria in part 1 the preview goes and Split task is answered
//       in the form, sending nothing;
//   M-e with criterion 1 back in part 2, Split task sends ONE job.plan-split-task with the
//       partition [[0],[1]] against version 3, and a refusal with a reason is said;
//   M-f the preview is set apart by a 2px rule in the strong line token, and a legend is 12px;
//   M-g Escape closes the view;
//   M-h no console error and no uncaught exception was logged in the whole run.
// Screenshots twice: the merge form with its preview, and the split form with its preview.
// Prints "RENDER: <n> of 8 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SHOTS = "/home/decodeux/Repos/remedy/.remedy-wt/f292-r5-render-";

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

async function clickAt(client, pick) {
  const at = await evalJson(client, `(function(){
    var el = ${pick};
    if (!el) return null;
    el.scrollIntoView({ block: "center" });
    var box = el.getBoundingClientRect();
    return { x: Math.round(box.left + box.width / 2), y: Math.round(box.top + box.height / 2) };
  })()`);
  if (at === null) return false;
  for (const type of ["mouseMoved", "mousePressed", "mouseReleased"]) {
    await client.send("Input.dispatchMouseEvent", { type, x: at.x, y: at.y, button: "left", clickCount: 1 });
  }
  await sleep(350);
  return true;
}

const VIEW = `document.querySelector('[data-ui="plan-view"]')`;
const byText = (taskId, text) => `Array.from(${VIEW}.querySelectorAll('[data-plan-task="${taskId}"] button')).find(function(b){ return b.textContent === ${JSON.stringify(text)}; })`;
const submitOf = (form) => `${VIEW}.querySelector('[data-ui="${form}"] button[type="submit"]')`;

async function choosePart(client, index, part) {
  await evalJson(client, `(function(){
    var el = ${VIEW}.querySelector('[data-ui="plan-split-form"] select[aria-label="Part of criterion ${index}"]');
    Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set.call(el, ${JSON.stringify(String(part))});
    el.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  })()`);
  await sleep(200);
}

const STATE = `(function(){
  var view = ${VIEW};
  if (!view) return { open: false };
  function form(name) {
    var f = view.querySelector('[data-ui="' + name + '"]');
    if (!f) return null;
    return {
      choices: Array.from(f.querySelectorAll('label span')).map(function(s){ return s.textContent; }),
      parts: Array.from(f.querySelectorAll('select')).map(function(s){ return s.value; }),
      preview: (f.querySelector('[data-ui$="-preview"]') || {}).textContent || null,
      problem: (f.querySelector('[role="alert"]') || {}).textContent || null,
    };
  }
  return {
    open: true,
    headline: view.querySelector('[data-ui="plan-headline"]').textContent,
    message: view.querySelector('[data-ui="plan-edit-message"]').textContent,
    regroup: Array.from(view.querySelectorAll('[data-plan-task]')).map(function(li){
      return Array.from(li.querySelectorAll(':scope > div > button')).filter(function(b){
        return b.textContent === 'Merge' || b.textContent === 'Split';
      }).map(function(b){ return [b.textContent, b.disabled, b.title]; });
    }),
    merge: form('plan-merge-form'),
    split: form('plan-split-form'),
    sent: window.__sent.slice(),
    reloads: window.__reloads,
  };
})()`;

const STYLES = `(function(){
  function probe(prop, value) {
    var el = document.createElement('div');
    el.style.setProperty(prop, value);
    document.body.appendChild(el);
    var out = getComputedStyle(el).getPropertyValue(prop);
    el.remove();
    return out;
  }
  var preview = ${VIEW}.querySelector('[data-ui="plan-merge-preview"]');
  var legend = ${VIEW}.querySelector('[data-ui="plan-merge-form"] legend');
  var s = getComputedStyle(preview);
  return { width: s.borderLeftWidth, color: s.borderLeftColor, strong: probe('color', 'var(--remedy-line-strong)'),
           legend: getComputedStyle(legend).fontSize };
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
  const state = () => evalJson(client, STATE);
  const answer = (status, body) => evalJson(client, `(window.__answers.push(${JSON.stringify({ status, body })}), true)`);
  const shot = async (name) => {
    const { data } = await client.send("Page.captureScreenshot", { format: "png" });
    writeFileSync(`${SHOTS}${name}.png`, Buffer.from(data, "base64"));
  };

  await client.send("Page.navigate", { url: PAGE });
  await sleep(2500);
  await clickAt(client, `document.querySelector('[data-ui="plan-button"]')`);
  const a = await state();
  check("M-a Merge and Split on each task, T2's Split disabled with the reason",
    a.regroup.length === 4 && a.regroup.every((row) => row.length === 2 && row[0][1] === false)
    && JSON.stringify(a.regroup[1][1]) === JSON.stringify(["Split", true, "A task with one criterion cannot be split."])
    && a.regroup[0][1][1] === false, { regroup: a.regroup });

  await clickAt(client, byText("T3", "Merge"));
  await clickAt(client, submitOf("plan-merge-form"));
  const b = await state();
  check("M-b Merge lists the other tasks; nothing chosen is answered and unsent", b.merge !== null
    && JSON.stringify(b.merge.choices) === JSON.stringify(["T1 — Read the config file", "T2 — Validate the fields", "T4 — Document the format"])
    && b.merge.problem === "Choose at least one task to merge with." && b.merge.preview === null && b.sent.length === 0,
    { merge: b.merge, sent: b.sent.length });

  await clickAt(client, `${VIEW}.querySelectorAll('[data-ui="plan-merge-form"] input[type="checkbox"]')[2]`);
  const c1 = await state();
  const styles = await evalJson(client, STYLES);
  await shot("merge-form");
  await answer(200, { command: "job.plan-merge-tasks", outcome: "accepted", version: 3, tasks: ["T1", "T2", "T3"] });
  await clickAt(client, submitOf("plan-merge-form"));
  const c2 = await state();
  check("M-c the preview says what happens; Merge tasks sends T3 and T4 against version 2",
    c1.merge.preview === "T3 and T4 become one task, T3, with all 3 of their criteria." && c1.merge.problem === null
    && c2.sent.length === 1 && c2.sent[0].command === "job.plan-merge-tasks"
    && JSON.stringify(c2.sent[0].args) === JSON.stringify({ task_ids: ["T3", "T4"], expected_version: 2 })
    && c2.message === "Saved as version 3." && c2.merge === null && c2.reloads === 1,
    { preview: c1.merge.preview, sent: c2.sent[0], message: c2.message, reloads: c2.reloads });

  await sleep(600);
  await clickAt(client, byText("T1", "Split"));
  const d1 = await state();
  await shot("split-form");
  await choosePart(client, 1, 1);
  const d2 = await state();
  await clickAt(client, submitOf("plan-split-form"));
  const d3 = await state();
  check("M-d Split opens on part 2 with its preview; one part drops the preview and is answered unsent",
    d1.headline === "Version 3 · waiting for approval" && JSON.stringify(d1.split.parts) === JSON.stringify(["1", "2"])
    && d1.split.preview === "T1 becomes 2 tasks run one after the other, each with its part of the criteria. T2 and T3 will wait for the last part."
    && d2.split.preview === null && d3.split.problem === "Put the criteria into at least two parts." && d3.sent.length === 1,
    { headline: d1.headline, parts: d1.split.parts, preview: d1.split.preview, after: d2.split.preview, problem: d3.split.problem });

  await choosePart(client, 1, 2);
  await answer(409, { error: "the plan is not valid", detail: "task 'T1b' would wait for nothing", current_version: 3 });
  await clickAt(client, submitOf("plan-split-form"));
  const e = await state();
  check("M-e Split task sends the partition [[0],[1]] against version 3; a refusal's reason is said",
    e.sent.length === 2 && e.sent[1].command === "job.plan-split-task"
    && JSON.stringify(e.sent[1].args) === JSON.stringify({ task_id: "T1", partition: [[0], [1]], expected_version: 3 })
    && e.message === "Not saved: task 'T1b' would wait for nothing." && e.reloads === 1 && e.split !== null,
    { sent: e.sent[1], message: e.message, reloads: e.reloads });

  check("M-f the preview's rule and the legend's size", styles.width === "2px" && styles.color === styles.strong
    && styles.legend === "12px", styles);

  await client.send("Input.dispatchKeyEvent", { type: "keyDown", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
  await sleep(300);
  const g = await state();
  check("M-g Escape closes the view", g.open === false, { open: g.open });

  setTimeout(() => {
    results.push(problems.length === 0);
    console.log(`${problems.length === 0 ? "PASS" : "FAIL"} M-h no console error ${JSON.stringify(problems)}`);
    const passed = results.filter(Boolean).length;
    console.log(`RENDER: ${passed} of ${results.length} checks pass`);
    ws.close();
    process.exit(passed === results.length ? 0 : 1);
  }, 300);
}

main().catch((err) => { console.error(err); process.exit(1); });
