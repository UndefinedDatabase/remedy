// F044 R2's render harness (evidence, not product): mounts the REAL `RemedyShell` from
// `apps/ui/src` with the app's own token and global sheets, over a fixed running job with five
// tasks of distinct labels. The first-run tour is recorded as seen and the palette's recent rows
// are cleared before the mount, so the bar is the first thing a key reaches. A `window.fetch`
// stand-in answers every request with a 500, so every door the shell reads reports itself
// unavailable and nothing waits on a server; the page never leaves `127.0.0.1`. Every node the
// shell is asked to select is pushed onto `window.__picked`.
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { normalizeApiFailure } from "../../apps/ui/src/api/remedyApi";
import type { RemedyDashboard, RemedyTaskItem } from "../../apps/ui/src/api/types";
import { RemedyShell } from "../../apps/ui/src/components/shell/RemedyShell";

window.fetch = async (): Promise<Response> => new Response("{}", { status: 500 });
window.localStorage.setItem("remedy:first-run-tour", "seen");
window.localStorage.removeItem("remedy:palette-recent");
const picked: (string | null)[] = [];
(window as unknown as { __picked: (string | null)[] }).__picked = picked;

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
  <RemedyShell dashboard={dashboard} serverToken="token" selectedNodeId={null} onSelectNode={(id) => { picked.push(id); }} />,
);
