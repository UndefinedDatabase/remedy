// F044 R6's render harness (evidence, not product): mounts the REAL `RemedyShell` from
// `apps/ui/src` inside the REAL `ProjectProvider`, with the app's own token and global sheets,
// over a fixed running job with three tasks, so the live graph draws three task nodes. Every node
// the shell is asked to select is pushed onto `window.__picked`. The first-run tour is recorded as
// seen and the palette's recent rows are cleared before the mount. A `window.fetch` stand-in
// answers every request with a 500; the page never leaves `127.0.0.1`.
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { normalizeApiFailure } from "../../apps/ui/src/api/remedyApi";
import type { RemedyDashboard, RemedyTaskItem } from "../../apps/ui/src/api/types";
import { ProjectProvider } from "../../apps/ui/src/components/shell/ProjectProvider";
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
  ],
};

createRoot(document.getElementById("root")!).render(
  <ProjectProvider token="token" jobId="job-1" project="" onSwitched={() => {}} onHome={() => {}}>
    <RemedyShell dashboard={dashboard} serverToken="token" selectedNodeId={null} onSelectNode={(id) => { picked.push(id); }} />
  </ProjectProvider>,
);
