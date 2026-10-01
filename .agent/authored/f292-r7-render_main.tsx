// F292 R7's render harness (evidence, not product): mounts the REAL `RemedyShell` from
// `apps/ui/src` inside the REAL `ProjectProvider`, with the app's own token and global sheets,
// over a job with one task, T001, selected, so its detail popover offers "Open diff". A
// `window.fetch` stand-in answers the task run's diff route with ENVELOPE, an envelope the
// server's own `build_diff_view` built from a three-hunk diff, and its hunk-decisions route
// with `window.__decisions`, counting each read in `window.__decisionReads`; it records every
// POST to the commands door in `window.__sent` and answers it with the next entry of
// `window.__answers`. Every other request is answered 500, so the page never leaves 127.0.0.1.
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { normalizeApiFailure } from "../../apps/ui/src/api/remedyApi";
import type { RemedyDashboard } from "../../apps/ui/src/api/types";
import { ProjectProvider } from "../../apps/ui/src/components/shell/ProjectProvider";
import { RemedyShell } from "../../apps/ui/src/components/shell/RemedyShell";

const ENVELOPE = {"version": 2, "scope": "task_run", "task_id": "T001", "source": "task_runs/T001/safe.diff", "available": true, "reason": null, "truncated": false, "files": [{"path": "src/config.py", "old_path": null, "status": "modified", "stats": {"added": 3, "deleted": 3}, "note": null, "hunks": [{"id": "40a22d59e1f29d0f", "header": "@@ -1,6 +1,6 @@", "old_start": 1, "new_start": 1, "lines": [{"kind": "ctx", "old_ln": 1, "new_ln": 1, "content": "value_1 = load(1)", "intraline": []}, {"kind": "ctx", "old_ln": 2, "new_ln": 2, "content": "value_2 = load(2)", "intraline": []}, {"kind": "del", "old_ln": 3, "new_ln": null, "content": "value_3 = load(3)", "intraline": []}, {"kind": "add", "old_ln": null, "new_ln": 3, "content": "value_3 = load(3, strict=True)", "intraline": [[16, 13]]}, {"kind": "ctx", "old_ln": 4, "new_ln": 4, "content": "value_4 = load(4)", "intraline": []}, {"kind": "ctx", "old_ln": 5, "new_ln": 5, "content": "value_5 = load(5)", "intraline": []}, {"kind": "ctx", "old_ln": 6, "new_ln": 6, "content": "value_6 = load(6)", "intraline": []}]}, {"id": "cb77f83a553455ba", "header": "@@ -17,7 +17,7 @@", "old_start": 17, "new_start": 17, "lines": [{"kind": "ctx", "old_ln": 17, "new_ln": 17, "content": "value_17 = load(17)", "intraline": []}, {"kind": "ctx", "old_ln": 18, "new_ln": 18, "content": "value_18 = load(18)", "intraline": []}, {"kind": "ctx", "old_ln": 19, "new_ln": 19, "content": "value_19 = load(19)", "intraline": []}, {"kind": "del", "old_ln": 20, "new_ln": null, "content": "value_20 = load(20)", "intraline": [[11, 4]]}, {"kind": "add", "old_ln": null, "new_ln": 20, "content": "value_20 = load_cached(20)", "intraline": [[11, 11]]}, {"kind": "ctx", "old_ln": 21, "new_ln": 21, "content": "value_21 = load(21)", "intraline": []}, {"kind": "ctx", "old_ln": 22, "new_ln": 22, "content": "value_22 = load(22)", "intraline": []}, {"kind": "ctx", "old_ln": 23, "new_ln": 23, "content": "value_23 = load(23)", "intraline": []}]}, {"id": "0675030a2d04d7d6", "header": "@@ -34,7 +34,7 @@", "old_start": 34, "new_start": 34, "lines": [{"kind": "ctx", "old_ln": 34, "new_ln": 34, "content": "value_34 = load(34)", "intraline": []}, {"kind": "ctx", "old_ln": 35, "new_ln": 35, "content": "value_35 = load(35)", "intraline": []}, {"kind": "ctx", "old_ln": 36, "new_ln": 36, "content": "value_36 = load(36)", "intraline": []}, {"kind": "del", "old_ln": 37, "new_ln": null, "content": "value_37 = load(37)", "intraline": [[11, 8]]}, {"kind": "add", "old_ln": null, "new_ln": 37, "content": "value_37 = None", "intraline": [[11, 4]]}, {"kind": "ctx", "old_ln": 38, "new_ln": 38, "content": "value_38 = load(38)", "intraline": []}, {"kind": "ctx", "old_ln": 39, "new_ln": 39, "content": "value_39 = load(39)", "intraline": []}, {"kind": "ctx", "old_ln": 40, "new_ln": 40, "content": "value_40 = load(40)", "intraline": []}]}]}], "task_run_ids": ["T001"]};
const IDS: string[] = ENVELOPE.files.flatMap((file: { hunks: { id: string }[] }) => file.hunks.map((hunk) => hunk.id));

type Answer = { status: number; body: unknown };
const harness = window as unknown as {
  __sent: unknown[]; __answers: Answer[]; __decisions: unknown; __decisionReads: number; __ids: string[];
};
harness.__sent = [];
harness.__answers = [];
harness.__decisionReads = 0;
harness.__ids = IDS;
harness.__decisions = {
  attempt_key: "T001:task_runs/T001/safe.diff", decided_at: "2026-10-01T09:00:00+00:00",
  hunks: [{ id: IDS[0], state: "approved", reason: "" }, { id: IDS[1], state: "pending", reason: "" },
    { id: IDS[2], state: "pending", reason: "" }],
};

window.fetch = async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
  const url = String(input);
  if (init?.method === "POST" && url.endsWith("/commands")) {
    harness.__sent.push(JSON.parse(String(init.body)));
    const answer = harness.__answers.shift() ?? { status: 500, body: {} };
    return new Response(JSON.stringify(answer.body), { status: answer.status });
  }
  if (url.includes("/task-runs/T001/hunk-decisions")) {
    harness.__decisionReads += 1;
    return new Response(JSON.stringify(harness.__decisions), { status: 200 });
  }
  if (url.includes("/task-runs/T001/diff")) return new Response(JSON.stringify(ENVELOPE), { status: 200 });
  return new Response("{}", { status: 500 });
};
window.localStorage.setItem("remedy:first-run-tour", "seen");

const base = normalizeApiFailure("0123456789abcdef", []);
const dashboard: RemedyDashboard = {
  ...base,
  apiHealth: { degraded: false, failedEndpoints: [] },
  tasks: [{ id: "T001", label: "Harden the config loader", state: "done", kind: "task", checked: true, muted: false, nodeId: "node-T001" }],
  graph: { nodes: [{ id: "node-T001", label: "Harden the config loader", kind: "task", state: "done", nodeId: "node-T001",
    visibleFromZoom: 0, showLabelFromZoom: 0 }], edges: [] },
};

createRoot(document.getElementById("root")!).render(
  <ProjectProvider token="token" jobId="0123456789abcdef" project="" onSwitched={() => {}} onHome={() => {}}>
    <RemedyShell dashboard={dashboard} serverToken="token" selectedNodeId="node-T001" onSelectNode={() => {}} />
  </ProjectProvider>,
);
