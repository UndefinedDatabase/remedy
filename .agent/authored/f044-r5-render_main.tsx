// F044 R5's render harness (evidence, not product): mounts the REAL `RemedyShell` from
// `apps/ui/src` inside the REAL `ProjectProvider`, with the app's own token and global sheets, over
// a fixed running job with five tasks, and a write token. The provider's `onHome` counts on
// `window.__home` how often the cockpit asked to go to the projects' home. The first-run tour is
// recorded as seen and the palette's recent rows are cleared before the mount. A `window.fetch`
// stand-in answers every request with a 500, so every door reports itself unavailable and nothing
// waits on a server; the page never leaves `127.0.0.1`.
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
const counter = window as unknown as { __home: number };
counter.__home = 0;

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
  <ProjectProvider token="token" jobId="job-1" project="" onSwitched={() => {}} onHome={() => { counter.__home += 1; }}>
    <RemedyShell dashboard={dashboard} serverToken="token" selectedNodeId={null} onSelectNode={() => {}} />
  </ProjectProvider>,
);
