// F292 R2's render harness (evidence, not product): mounts the REAL `RemedyShell` from
// `apps/ui/src` inside the REAL `ProjectProvider`, with the app's own token and global sheets,
// over a job whose dashboard carries a stored plan of three tasks waiting for approval. The
// first-run tour is recorded as seen before the mount. A `window.fetch` stand-in answers every
// request with a 500; the page never leaves `127.0.0.1`.
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { normalizeApiFailure } from "../../apps/ui/src/api/remedyApi";
import type { RemedyDashboard, RemedyPlanTask } from "../../apps/ui/src/api/types";
import { ProjectProvider } from "../../apps/ui/src/components/shell/ProjectProvider";
import { RemedyShell } from "../../apps/ui/src/components/shell/RemedyShell";

window.fetch = async (): Promise<Response> => new Response("{}", { status: 500 });
window.localStorage.setItem("remedy:first-run-tour", "seen");

function planned(id: string, title: string, dependsOn: string[], acceptance: string[]): RemedyPlanTask {
  return {
    id, title, goal: `Make ${title.toLowerCase()} work end to end`, dependsOn, estTokensBand: "M",
    filesHint: [], acceptance, jobTaskId: `entry-${id}`, status: "pending", specVersion: 1,
  };
}

const base = normalizeApiFailure("job-1", []);
const dashboard: RemedyDashboard = {
  ...base,
  apiHealth: { degraded: false, failedEndpoints: [] },
  plan: {
    available: true, version: 2, approval: "pending", editable: true, notEditableBecause: "",
    error: "",
    tasks: [
      planned("T1", "Read the config file", [], ["reads a file", "reports a missing file"]),
      planned("T2", "Validate the fields", ["T1"], ["rejects an unknown key"]),
      planned("T3", "Write the tests", ["T2", "T1"], ["covers both paths", "runs in under a second", "names each case"]),
    ],
  },
};

createRoot(document.getElementById("root")!).render(
  <ProjectProvider token="token" jobId="job-1" project="" onSwitched={() => {}} onHome={() => {}}>
    <RemedyShell dashboard={dashboard} serverToken="token" selectedNodeId={null} onSelectNode={() => {}} />
  </ProjectProvider>,
);
