// F292 R7's render driver (evidence, not product): drives headless Chrome over CDP (node's global
// WebSocket) through the real `RemedyShell` mounted by main.tsx, and proves the hunk decisions as
// a person meets them, from the task's own detail popover (DECISION F292 D7):
//   H-a "Open diff" in the popover opens the diff panel with the diff view and, after it, the
//       hunk decisions, one row per hunk, starting from the record: the first hunk approved;
//   H-b with nothing changed, Record is disabled with the reason;
//   H-c Reject on the second hunk shows its reason field; Record without a reason is answered in
//       the panel and sends nothing;
//   H-d with the reason written, Record sends ONE patch.approve-hunks for T001 carrying the whole
//       decision, its counts are said, the record is read again, and Record is disabled again;
//   H-e Approve on the third hunk then Record, answered by the door's refusal, says the server
//       refused it and reads nothing again;
//   H-f the chosen pill wears the blue tint and border, the panel the 20px radius, the hunk
//       header the mono face;
//   H-g Escape closes the popover and no console error was logged in the whole run.
// Screenshots twice: the panel from the record, and the panel after the recorded decision.
// Prints "RENDER: <n> of 7 checks pass".
import { writeFileSync } from "node:fs";

const CDP = "http://127.0.0.1:9380";
const PAGE = "http://127.0.0.1:9010/index.html";
const SHOTS = "/home/decodeux/Repos/remedy/.remedy-wt/f292-r7-render-";

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
  await sleep(400);
  return true;
}

const PANEL = `document.querySelector('[data-ui="hunk-decisions"]')`;
const choice = (n, label) => `Array.from(${PANEL}.querySelectorAll('li')[${n}].querySelectorAll('button')).find(function(b){ return b.textContent === ${JSON.stringify(label)}; })`;
const RECORD = `Array.from(${PANEL}.querySelectorAll('button')).find(function(b){ return b.textContent === 'Record decisions'; })`;

const STATE = `(function(){
  var panel = ${PANEL};
  var diffPanel = document.querySelector('[data-ui="diff-panel"]');
  var view = document.querySelector('[data-ui="diff-view"]');
  if (!panel) return { panel: false, diffPanel: !!diffPanel };
  var record = ${RECORD};
  return {
    panel: true,
    order: !!(view && (view.compareDocumentPosition(panel) & Node.DOCUMENT_POSITION_FOLLOWING)) && diffPanel.contains(panel),
    tally: (panel.querySelector('[data-ui="hunk-tally"]') || {}).textContent || null,
    rows: Array.from(panel.querySelectorAll('li')).map(function(li){
      var pressed = Array.from(li.querySelectorAll('button[aria-pressed="true"]')).map(function(b){ return b.textContent; });
      return { id: li.getAttribute('data-hunk-id'), pressed: pressed[0] || null, reasonField: !!li.querySelector('input') };
    }),
    message: panel.querySelector('[data-ui="hunk-decision-message"]').textContent,
    record: record ? [record.disabled, record.title] : null,
    sent: window.__sent.slice(),
    reads: window.__decisionReads,
    ids: window.__ids,
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
  var panel = ${PANEL};
  var on = panel.querySelector('button[aria-pressed="true"]');
  return {
    onBg: getComputedStyle(on).backgroundColor, blue50: probe('background-color', 'var(--remedy-blue-50)'),
    onBorder: getComputedStyle(on).borderTopColor, blueStrong: probe('color', 'var(--remedy-blue-strong)'),
    radius: getComputedStyle(panel).borderTopLeftRadius,
    headerFont: getComputedStyle(panel.querySelector('li code')).fontFamily, mono: probe('font-family', 'var(--remedy-font-mono)'),
  };
})()`;

async function setReason(client, n, value) {
  await evalJson(client, `(function(){
    var el = ${PANEL}.querySelectorAll('li')[${n}].querySelector('input');
    Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(el, ${JSON.stringify(value)});
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
  await clickAt(client, `Array.from(document.querySelectorAll('button')).find(function(b){ return b.textContent.trim() === 'Open diff'; })`);
  await sleep(600);
  const a = await state();
  check("H-a Open diff shows the diff view and, after it, one row per hunk from the record", a.panel && a.order
    && a.rows.length === 3 && a.rows[0].pressed === "Approve" && a.rows[1].pressed === "Undecided"
    && a.rows[2].pressed === "Undecided" && a.tally === "1 approved, 0 rejected, 2 pending" && a.reads === 1
    && JSON.stringify(a.rows.map((r) => r.id)) === JSON.stringify(a.ids), { a });
  await shot("from-record");

  check("H-b with nothing changed Record is disabled with the reason",
    JSON.stringify(a.record) === JSON.stringify([true, "Nothing has changed since the last record."]), { record: a.record });

  await clickAt(client, choice(1, "Reject"));
  const c1 = await state();
  await clickAt(client, RECORD);
  const c2 = await state();
  check("H-c Reject shows the reason field; Record without a reason is answered and unsent",
    c1.rows[1].pressed === "Reject" && c1.rows[1].reasonField && c1.record[0] === false
    && c2.message === "Give each rejected hunk a reason." && c2.sent.length === 0, { row: c1.rows[1], message: c2.message });

  await setReason(client, 1, "caching hides a stale value");
  await evalJson(client, `(function(){
    window.__answers.push({ status: 200, body: { command: "patch.approve-hunks", outcome: "accepted",
      attempt_key: "T001:task_runs/T001/safe.diff", approved: 1, rejected: 1, pending: 1 } });
    window.__decisions = { attempt_key: "T001:task_runs/T001/safe.diff", decided_at: "2026-10-01T09:05:00+00:00",
      hunks: [{ id: window.__ids[0], state: "approved", reason: "" },
              { id: window.__ids[1], state: "rejected", reason: "caching hides a stale value" },
              { id: window.__ids[2], state: "pending", reason: "" }] };
    return true;
  })()`);
  await clickAt(client, RECORD);
  await sleep(500);
  const d = await state();
  const sent = d.sent[0] || {};
  check("H-d Record sends the whole decision for T001, says its counts, reads the record again",
    d.sent.length === 1 && sent.command === "patch.approve-hunks"
    && JSON.stringify(sent.args) === JSON.stringify({ approved: [d.ids[0]], rejected: [{ id: d.ids[1], reason: "caching hides a stale value" }], task_run: "T001" })
    && d.message === "Recorded: 1 approved, 1 rejected, 1 pending." && d.reads === 2
    && d.rows[1].pressed === "Reject" && d.tally === "1 approved, 1 rejected, 1 pending"
    && JSON.stringify(d.record) === JSON.stringify([true, "Nothing has changed since the last record."]),
    { sent: sent.args, message: d.message, reads: d.reads, record: d.record });
  await shot("after-record");

  await evalJson(client, `(window.__answers.push({ status: 409, body: { error: "hunk decision was refused" } }), true)`);
  await clickAt(client, choice(2, "Approve"));
  await clickAt(client, RECORD);
  const e = await state();
  check("H-e the door's refusal is said plainly and nothing is read again", e.sent.length === 2
    && e.message === "Not recorded: the server refused this decision for this change. Close the change, open it again and decide again."
    && e.reads === 2 && e.rows[2].pressed === "Approve", { message: e.message, reads: e.reads });

  const styles = await evalJson(client, STYLES);
  check("H-f the chosen pill, the panel and the hunk header wear their tokens", styles.onBg === styles.blue50
    && styles.onBorder === styles.blueStrong && styles.radius === "20px" && styles.headerFont === styles.mono, styles);

  await client.send("Input.dispatchKeyEvent", { type: "keyDown", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
  await client.send("Input.dispatchKeyEvent", { type: "keyUp", key: "Escape", code: "Escape", windowsVirtualKeyCode: 27 });
  await sleep(300);
  setTimeout(() => {
    check("H-g no console error", problems.length === 0, problems);
    const passed = results.filter(Boolean).length;
    console.log(`RENDER: ${passed} of ${results.length} checks pass`);
    ws.close();
    process.exit(passed === results.length ? 0 : 1);
  }, 300);
}

main().catch((err) => { console.error(err); process.exit(1); });
