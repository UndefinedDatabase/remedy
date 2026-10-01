// F292 R4's render driver (evidence, not product): drives headless Chrome over CDP (node's global
// WebSocket) through the real `RemedyShell` mounted by main.tsx, and proves the plan view's
// criteria editor and task moves as a person meets them (DECISION F292 D4):
//   C-a each criterion offers Change and Remove, each task Add a criterion, and T2's only
//       criterion's Remove is disabled with the reason;
//   C-b Change on T1's criterion 1 opens its form prefilled, in place of that criterion only;
//   C-c Save with new text sends ONE job.plan-edit-acceptance edit of index 1 against version 2,
//       the save is said, the form closes and the cockpit is asked to read the dashboard again;
//   C-d once version 3 arrives, Add a criterion on T4 refuses an empty criterion without sending,
//       then sends ONE add with no index; a refusal with a reason is said, nothing is reloaded and
//       the form stays open;
//   C-e Remove on T1's criterion 0 sends ONE remove of index 0 with no text against version 3;
//   C-f once version 4 arrives, T1's Move up and T3's Move up are disabled with their reasons,
//       and T4's Move up sends ONE job.plan-reorder with the whole new order against version 4;
//   C-g a criterion button is the 24px mini ghost, a criterion field has the 10px radius, and a
//       disabled Remove is at 45% opacity;
//   C-h Escape closes the view;
//   C-i no console error and no uncaught exception was logged in the whole run.
// Screenshots twice: with a criterion's form open, and after the move. Prints
// "RENDER: <n> of 9 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SHOTS = "/home/decodeux/Repos/remedy/.remedy-wt/f292-r4-render-";

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
const byLabel = (label) => `${VIEW}.querySelector('button[aria-label=${JSON.stringify(label)}]')`;
const byText = (taskId, text) => `Array.from(${VIEW}.querySelectorAll('[data-plan-task="${taskId}"] button')).find(function(b){ return b.textContent === ${JSON.stringify(text)}; })`;
const formSave = `${VIEW}.querySelector('[data-ui="plan-criterion-form"] button[type="submit"]')`;

async function setInput(client, value) {
  await evalJson(client, `(function(){
    var el = ${VIEW}.querySelector('[data-ui="plan-criterion-form"] input');
    Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(el, ${JSON.stringify(value)});
    el.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  })()`);
  await sleep(200);
}

const STATE = `(function(){
  var view = ${VIEW};
  if (!view) return { open: false };
  var form = view.querySelector('[data-ui="plan-criterion-form"]');
  return {
    open: true,
    headline: view.querySelector('[data-ui="plan-headline"]').textContent,
    message: view.querySelector('[data-ui="plan-edit-message"]').textContent,
    form: form ? { label: form.getAttribute('aria-label'), value: form.querySelector('input').value,
                   problem: (form.querySelector('[role="alert"]') || {}).textContent || null,
                   task: form.closest('[data-plan-task]').getAttribute('data-plan-task') } : null,
    t1: Array.from(view.querySelectorAll('[data-plan-task="T1"] ol li')).map(function(li){
      return li.querySelector('form') ? '[form]' : li.children[1].textContent;
    }),
    criterionButtons: Array.from(view.querySelectorAll('button[aria-label*=" criterion "]')).map(function(b){
      return [b.getAttribute('aria-label'), b.disabled, b.title];
    }),
    addButtons: Array.from(view.querySelectorAll('button')).filter(function(b){ return b.textContent === 'Add a criterion'; }).length,
    moves: Array.from(view.querySelectorAll('[data-plan-task]')).map(function(li){
      return Array.from(li.querySelectorAll(':scope > div > button')).filter(function(b){
        return b.textContent.indexOf('Move') === 0;
      }).map(function(b){ return [b.textContent, b.disabled, b.title]; });
    }),
    sent: window.__sent.slice(),
    reloads: window.__reloads,
  };
})()`;

const STYLES = `(function(){
  var view = ${VIEW};
  var mini = view.querySelector('button[aria-label="Change criterion 0 of T2"]');
  var removeOnly = view.querySelector('button[aria-label="Remove criterion 0 of T2"]');
  var input = view.querySelector('[data-ui="plan-criterion-form"] input');
  return {
    miniHeight: getComputedStyle(mini).height, miniBg: getComputedStyle(mini).backgroundColor,
    removeOpacity: getComputedStyle(removeOnly).opacity,
    inputRadius: input ? getComputedStyle(input).borderTopLeftRadius : null,
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
  const only = a.criterionButtons.find(([label]) => label === "Remove criterion 0 of T2");
  check("C-a Change and Remove per criterion, Add per task, the only criterion kept",
    a.criterionButtons.length === 12 && a.addButtons === 4 && only[1] === true && only[2] === "A task keeps at least one criterion.",
    { buttons: a.criterionButtons.length, adds: a.addButtons, only });

  await clickAt(client, byLabel("Change criterion 1 of T1"));
  const b = await state();
  check("C-b Change opens that criterion's form prefilled, in place", b.form !== null
    && b.form.label === "Change criterion 1 of T1" && b.form.value === "reports a missing file"
    && JSON.stringify(b.t1) === JSON.stringify(["reads a file", "[form]"]), { form: b.form, t1: b.t1 });
  const styles = await evalJson(client, STYLES);
  await shot("criterion-form");

  await answer(200, { command: "job.plan-edit-acceptance", outcome: "accepted", version: 3, tasks: ["T1", "T2", "T3", "T4"] });
  await setInput(client, "reports a missing file clearly");
  await clickAt(client, formSave);
  const c = await state();
  check("C-c Save sends one edit of index 1 against version 2; said, closed, reloaded", c.sent.length === 1
    && c.sent[0].command === "job.plan-edit-acceptance"
    && JSON.stringify(c.sent[0].args) === JSON.stringify({ task_id: "T1", op: "edit", index: 1, text: "reports a missing file clearly", expected_version: 2 })
    && c.message === "Saved as version 3." && c.form === null && c.reloads === 1, { sent: c.sent[0], message: c.message, reloads: c.reloads });

  await sleep(600);
  await clickAt(client, byText("T4", "Add a criterion"));
  await clickAt(client, formSave);
  const d1 = await state();
  await answer(409, { error: "the plan is not open for editing", detail: "the plan is approved; a plan is edited only while its approval is open" });
  await setInput(client, "shows the defaults");
  await clickAt(client, formSave);
  const d2 = await state();
  check("C-d Add refuses an empty criterion unsent, then sends one add with no index; a refusal is said, no reload, form kept",
    d1.headline === "Version 3 · waiting for approval" && d1.form !== null && d1.form.task === "T4" && d1.form.problem === "Write the criterion."
    && d1.sent.length === 1 && d2.sent.length === 2
    && JSON.stringify(d2.sent[1].args) === JSON.stringify({ task_id: "T4", op: "add", text: "shows the defaults", expected_version: 3 })
    && d2.message === "Not saved: the plan is approved; a plan is edited only while its approval is open."
    && d2.reloads === 1 && d2.form !== null,
    { headline: d1.headline, problem: d1.form && d1.form.problem, sent: d2.sent[1], message: d2.message, reloads: d2.reloads });

  await clickAt(client, `Array.from(${VIEW}.querySelectorAll('[data-ui="plan-criterion-form"] button')).find(function(b){ return b.textContent === 'Cancel'; })`);
  await answer(200, { command: "job.plan-edit-acceptance", outcome: "accepted", version: 4, tasks: ["T1", "T2", "T3", "T4"] });
  await clickAt(client, byLabel("Remove criterion 0 of T1"));
  const e = await state();
  check("C-e Remove sends one remove of index 0 with no text against version 3", e.sent.length === 3
    && JSON.stringify(e.sent[2].args) === JSON.stringify({ task_id: "T1", op: "remove", index: 0, expected_version: 3 })
    && e.message === "Saved as version 4." && e.reloads === 2, { sent: e.sent[2], message: e.message, reloads: e.reloads });

  await sleep(600);
  const f1 = await state();
  await answer(200, { command: "job.plan-reorder", outcome: "accepted", version: 5, tasks: ["T1", "T2", "T4", "T3"] });
  await clickAt(client, byText("T4", "Move up"));
  const f2 = await state();
  check("C-f blocked moves say why; T4's Move up sends the whole new order against version 4",
    f1.headline === "Version 4 · waiting for approval"
    && JSON.stringify(f1.moves[0][0]) === JSON.stringify(["Move up", true, "T1 is already first."])
    && JSON.stringify(f1.moves[2][0]) === JSON.stringify(["Move up", true, "T3 waits for T2, so it cannot come before it."])
    && f1.moves[3][0][1] === false && f2.sent.length === 4 && f2.sent[3].command === "job.plan-reorder"
    && JSON.stringify(f2.sent[3].args) === JSON.stringify({ order: ["T1", "T2", "T4", "T3"], expected_version: 4 }),
    { moves: f1.moves.map((m) => m[0]), sent: f2.sent[3] });
  await sleep(600);
  await shot("after-move");

  check("C-g the mini ghost, the criterion field and a disabled Remove wear their sizes", styles.miniHeight === "24px"
    && styles.miniBg === "rgba(0, 0, 0, 0)" && styles.inputRadius === "10px" && styles.removeOpacity === "0.45", styles);

  await client.send("Input.dispatchKeyEvent", { type: "keyDown", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
  await sleep(300);
  const h = await state();
  check("C-h Escape closes the view", h.open === false, { open: h.open });

  setTimeout(() => {
    results.push(problems.length === 0);
    console.log(`${problems.length === 0 ? "PASS" : "FAIL"} C-i no console error ${JSON.stringify(problems)}`);
    const passed = results.filter(Boolean).length;
    console.log(`RENDER: ${passed} of ${results.length} checks pass`);
    ws.close();
    process.exit(passed === results.length ? 0 : 1);
  }, 300);
}

main().catch((err) => { console.error(err); process.exit(1); });
