// F292 R3's render driver (evidence, not product): drives headless Chrome over CDP (node's global
// WebSocket) through the real `RemedyShell` mounted by main.tsx, and proves the plan view's edit
// and delete as a person meets them (DECISION F292 D3):
//   E-a the open plan offers Edit and Delete on each of its three tasks;
//   E-b Edit on T2 opens its form prefilled, with the title, the goal and the size M;
//   E-c Save with the title changed sends ONE job.plan-edit-task to the commands door carrying
//       only the title and the version shown, 2;
//   E-d the accepted answer is said as "Saved as version 3.", the form closes, the cockpit is asked
//       to read the dashboard again once, and the controls wait, disabled with the reason, until
//       version 3 arrives;
//   E-e version 3 arrives with the new title and the controls are usable again;
//   E-f Delete on T1 asks first, naming the tasks that wait for it; Keep it sends nothing;
//   E-g Delete on T2 confirmed sends ONE job.plan-delete-task against version 3, and a stale answer
//       is said in plain words with the controls left usable and no reload asked for;
//   E-h the save pill is filled blue, the delete button is outlined in the red token, a disabled
//       control is at 45% opacity, and a field has the 10px radius and the line border;
//   E-i Escape closes the view;
//   E-j no console error and no uncaught exception was logged in the whole run.
// Every expected colour is read from a probe styled with the same token. Screenshots twice:
// with the edit form open, and with the delete question shown. Prints "RENDER: <n> of 10 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SHOTS = "/home/decodeux/Repos/remedy/.remedy-wt/f292-r3-render-";

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

/** Clicks the element `pick` (a JS expression answering one element) finds, by a real mouse event. */
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

const tile = (id) => `document.querySelector('[data-ui="plan-view"] [data-plan-task="${id}"]')`;
const button = (id, label) => `Array.from(${tile(id)}.querySelectorAll('button')).find(function(b){ return b.textContent === ${JSON.stringify(label)}; })`;

const STATE = `(function(){
  var view = document.querySelector('[data-ui="plan-view"]');
  if (!view) return { open: false };
  var form = view.querySelector('[data-ui="plan-task-form"]');
  var confirm = view.querySelector('[data-ui="plan-delete-confirm"]');
  return {
    open: true,
    headline: view.querySelector('[data-ui="plan-headline"]').textContent,
    message: view.querySelector('[data-ui="plan-edit-message"]').textContent,
    controls: Array.from(view.querySelectorAll('[data-plan-task]')).map(function(li){
      return Array.from(li.querySelectorAll(':scope > div > button')).map(function(b){
        return [b.textContent, b.disabled, b.title];
      });
    }),
    titles: Array.from(view.querySelectorAll('[data-plan-task]')).map(function(li){
      return li.querySelector(':scope > div > span:nth-child(2)').textContent;
    }),
    form: form ? {
      label: form.getAttribute('aria-label'),
      title: form.querySelector('input').value,
      goal: form.querySelector('textarea').value,
      size: form.querySelector('select').value,
    } : null,
    confirm: confirm ? confirm.querySelector('p').textContent : null,
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
  var view = document.querySelector('[data-ui="plan-view"]');
  var save = view.querySelector('[data-ui="plan-task-form"] button[type="submit"]');
  var input = view.querySelector('[data-ui="plan-task-form"] input');
  return {
    saveBg: getComputedStyle(save).backgroundColor, blue: probe('background-color', 'var(--remedy-blue)'),
    inputRadius: getComputedStyle(input).borderTopLeftRadius,
    inputBorder: getComputedStyle(input).borderTopColor, line: probe('color', 'var(--remedy-line)'),
  };
})()`;

const DANGER = `(function(){
  function probe(prop, value) {
    var el = document.createElement('div');
    el.style.setProperty(prop, value);
    document.body.appendChild(el);
    var out = getComputedStyle(el).getPropertyValue(prop);
    el.remove();
    return out;
  }
  var danger = Array.from(document.querySelectorAll('[data-ui="plan-delete-confirm"] button'))
    .find(function(b){ return b.textContent === 'Delete task'; });
  var s = getComputedStyle(danger);
  return { border: s.borderTopColor, color: s.color, red: probe('color', 'var(--remedy-red-500)') };
})()`;

async function setValue(client, selector, value) {
  await evalJson(client, `(function(){
    var el = document.querySelector(${JSON.stringify(selector)});
    var proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, ${JSON.stringify(value)});
    el.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  })()`);
  await sleep(200);
}

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
  const shot = async (name) => {
    const { data } = await client.send("Page.captureScreenshot", { format: "png" });
    writeFileSync(`${SHOTS}${name}.png`, Buffer.from(data, "base64"));
  };

  await client.send("Page.navigate", { url: PAGE });
  await sleep(2500);
  await clickAt(client, `document.querySelector('[data-ui="plan-button"]')`);
  const a = await state();
  const usable = [["Edit", false, ""], ["Delete", false, ""]];
  check("E-a Edit and Delete on each task", a.open && JSON.stringify(a.controls) === JSON.stringify([usable, usable, usable]),
    { controls: a.controls });

  await clickAt(client, button("T2", "Edit"));
  const b = await state();
  check("E-b the form opens prefilled", b.form !== null && b.form.label === "Edit T2" && b.form.title === "Validate the fields"
    && b.form.goal === "Make validate the fields work end to end" && b.form.size === "M", { form: b.form });
  const styles = await evalJson(client, STYLES);
  await shot("edit-form");

  await evalJson(client, `(window.__answers.push({ status: 200, body: { command: "job.plan-edit-task", outcome: "accepted", version: 3, tasks: ["T1","T2","T3"] } }), true)`);
  await setValue(client, '[data-ui="plan-task-form"] input', "Check every field");
  await clickAt(client, `document.querySelector('[data-ui="plan-task-form"] button[type="submit"]')`);
  const c = await state();
  const sentEdit = c.sent[0] || {};
  check("E-c Save sends one edit with only the title and the version shown", c.sent.length === 1
    && sentEdit.command === "job.plan-edit-task"
    && JSON.stringify(sentEdit.args) === JSON.stringify({ task_id: "T2", fields: { title: "Check every field" }, expected_version: 2 }),
    { sent: c.sent });

  const waiting = ["Waiting for version 3 of the plan to arrive."];
  check("E-d the save is said, the form closes, one reload, the controls wait with the reason", c.message === "Saved as version 3."
    && c.form === null && c.reloads === 1
    && c.controls.every((row) => row.every(([, disabled, title]) => disabled === true && title === waiting[0])),
    { message: c.message, form: c.form, reloads: c.reloads, controls: c.controls[0] });
  const disabledOpacity = await evalJson(client, `getComputedStyle(${button("T1", "Edit")}).opacity`);

  await sleep(700);
  const e = await state();
  check("E-e version 3 arrives and the controls are usable again", e.headline === "Version 3 · waiting for approval"
    && e.titles[1] === "Check every field" && JSON.stringify(e.controls) === JSON.stringify([usable, usable, usable]),
    { headline: e.headline, titles: e.titles, controls: e.controls[0] });

  await clickAt(client, button("T1", "Delete"));
  const f1 = await state();
  const danger = await evalJson(client, DANGER);
  await shot("delete-question");
  await clickAt(client, `Array.from(document.querySelectorAll('[data-ui="plan-delete-confirm"] button')).find(function(b){ return b.textContent === 'Keep it'; })`);
  const f2 = await state();
  check("E-f Delete asks first, naming who waits; Keep it sends nothing",
    f1.confirm === "Delete T1? T2 and T3 wait for it; that wait will be dropped." && f2.confirm === null && f2.sent.length === 1,
    { question: f1.confirm, after: f2.confirm, sent: f2.sent.length });

  await evalJson(client, `(window.__answers.push({ status: 409, body: { error: "the plan changed since this edit was made", current_version: 4 } }), true)`);
  await clickAt(client, button("T2", "Delete"));
  await clickAt(client, `Array.from(document.querySelectorAll('[data-ui="plan-delete-confirm"] button')).find(function(b){ return b.textContent === 'Delete task'; })`);
  const g = await state();
  const del = g.sent[1] || {};
  check("E-g a confirmed delete sends one edit against version 3; a stale answer is said and nothing waits",
    g.sent.length === 2 && del.command === "job.plan-delete-task"
    && JSON.stringify(del.args) === JSON.stringify({ task_id: "T2", expected_version: 3 })
    && g.message === "Not saved: the plan changed since you opened it. Look at it again and redo the edit."
    && g.reloads === 1 && g.confirm !== null && g.controls[0].every(([, disabled]) => disabled === false),
    { sent: g.sent.length, args: del.args, message: g.message, reloads: g.reloads, confirm: g.confirm });

  check("E-h the save pill, the delete button, a disabled control and a field wear their tokens",
    styles.saveBg === styles.blue && danger.border === danger.red && danger.color === danger.red
    && disabledOpacity === "0.45" && styles.inputRadius === "10px" && styles.inputBorder === styles.line,
    { styles, danger, disabledOpacity });

  await clickAt(client, `document.body`);
  await client.send("Input.dispatchKeyEvent", { type: "keyDown", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
  await sleep(300);
  const i = await state();
  check("E-i Escape closes the view", i.open === false, { open: i.open });

  setTimeout(() => {
    results.push(problems.length === 0);
    console.log(`${problems.length === 0 ? "PASS" : "FAIL"} E-j no console error ${JSON.stringify(problems)}`);
    const passed = results.filter(Boolean).length;
    console.log(`RENDER: ${passed} of ${results.length} checks pass`);
    ws.close();
    process.exit(passed === results.length ? 0 : 1);
  }, 300);
}

main().catch((err) => { console.error(err); process.exit(1); });
