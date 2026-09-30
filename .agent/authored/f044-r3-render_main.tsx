// F044 R3's render harness (evidence, not product): mounts the REAL `RemedyShell` from
// `apps/ui/src` with the app's own token and global sheets, over a fixed running job with five
// tasks of distinct labels and one open decision, and a write token. The first-run tour is
// recorded as seen and the palette's recent rows are cleared before the mount. A `window.fetch`
// stand-in records the body of every POST to the job's commands door on `window.__posts` and
// answers it 200, except a `job.preview-start`, which it refuses with a 409; every other request
// answers 500, so every door the shell reads reports itself unavailable. The page never leaves
// `127.0.0.1`.
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { buildDecisionCardModel } from "../../apps/ui/src/api/decisionCard";
import { normalizeApiFailure } from "../../apps/ui/src/api/remedyApi";
import type { RemedyDashboard, RemedyTaskItem } from "../../apps/ui/src/api/types";
import { RemedyShell } from "../../apps/ui/src/components/shell/RemedyShell";

const posts: unknown[] = [];
(window as unknown as { __posts: unknown[] }).__posts = posts;
window.fetch = async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
  const url = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
  if (init?.method === "POST" && url.endsWith("/api/jobs/job-1/commands")) {
    const body = JSON.parse(String(init.body)) as { command: string };
    posts.push(body);
    if (body.command === "job.preview-start") {
      return new Response(JSON.stringify({ error: "preview is not available" }), { status: 409 });
    }
    return new Response(JSON.stringify({ command: body.command, outcome: "accepted" }), { status: 200 });
  }
  return new Response("{}", { status: 500 });
};
window.localStorage.setItem("remedy:first-run-tour", "seen");
window.localStorage.removeItem("remedy:palette-recent");

function task(id: string, label: string, kind: RemedyTaskItem["kind"]): RemedyTaskItem {
  return { id, label, state: "pending", kind, checked: false, muted: false, nodeId: `node-${id}` };
}

const base = normalizeApiFailure("job-1", []);
const dashboard: RemedyDashboard = {
  ...base,
  live: { ...base.live, running: true },
  tasks: [
    task("t1", "Fix error handling", "task"),
    task("t2", "Write tests", "test"),
    task("t3", "Check the diff", "review"),
    task("t4", "Errata", "task"),
    task("t5", "Review output", "review"),
  ],
  decisionInbox: [buildDecisionCardModel({ id: "d-1", status: "open", type: "clarification", age_seconds: 60, blocked_count: 1 })],
};

createRoot(document.getElementById("root")!).render(
  <RemedyShell dashboard={dashboard} serverToken="token" selectedNodeId={null} onSelectNode={() => {}} />,
);
