// F044 R4's render harness (evidence, not product): mounts the REAL `RemedyShell` from
// `apps/ui/src` with the app's own token and global sheets, over a fixed running job with five
// tasks of distinct labels, and a write token. The first-run tour is recorded as seen and the
// palette's recent rows are cleared before the mount. A `window.fetch` stand-in records the URL of
// every read of the job's chat route on `window.__chats` and answers it that the chat is not
// available, with a reason; every other request answers 500, so every other door the shell reads
// reports itself unavailable. The page never leaves `127.0.0.1`.
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { normalizeApiFailure } from "../../apps/ui/src/api/remedyApi";
import type { RemedyDashboard, RemedyTaskItem } from "../../apps/ui/src/api/types";
import { RemedyShell } from "../../apps/ui/src/components/shell/RemedyShell";

const chats: string[] = [];
(window as unknown as { __chats: string[] }).__chats = chats;
window.fetch = async (input: RequestInfo | URL): Promise<Response> => {
  const url = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
  if (url.includes("/api/jobs/job-1/chat?")) {
    chats.push(url);
    return new Response(JSON.stringify({ available: false, reason: "no model is configured for the chat" }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
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
};

createRoot(document.getElementById("root")!).render(
  <RemedyShell dashboard={dashboard} serverToken="token" selectedNodeId={null} onSelectNode={() => {}} />,
);
