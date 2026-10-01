// F292 R3's render harness (evidence, not product): mounts the REAL `RemedyShell` from
// `apps/ui/src` inside the REAL `ProjectProvider`, with the app's own token and global sheets,
// over a job whose dashboard carries a plan of three tasks waiting for approval, at version 2.
// A `window.fetch` stand-in records every POST to the job's commands door in `window.__sent` and
// answers it with the next entry of `window.__answers`; every other request is answered 500, so
// the page never leaves `127.0.0.1`. The shell's `onReload` counts in `window.__reloads` and
// serves the plan at the version and with the title the last accepted answer implies, exactly
// as a dashboard read after an accepted edit would.
import { useState } from "react";
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { normalizeApiFailure } from "../../apps/ui/src/api/remedyApi";
import type { RemedyDashboard, RemedyPlanTask } from "../../apps/ui/src/api/types";
import { ProjectProvider } from "../../apps/ui/src/components/shell/ProjectProvider";
import { RemedyShell } from "../../apps/ui/src/components/shell/RemedyShell";

type Answer = { status: number; body: unknown };
const harness = window as unknown as { __sent: unknown[]; __answers: Answer[]; __reloads: number };
harness.__sent = [];
harness.__answers = [];
harness.__reloads = 0;

window.fetch = async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
  const url = String(input);
  if (init?.method === "POST" && url.endsWith("/commands")) {
    harness.__sent.push(JSON.parse(String(init.body)));
    const answer = harness.__answers.shift() ?? { status: 500, body: {} };
    return new Response(JSON.stringify(answer.body), { status: answer.status });
  }
  return new Response("{}", { status: 500 });
};
window.localStorage.setItem("remedy:first-run-tour", "seen");

function planned(id: string, title: string, dependsOn: string[], acceptance: string[]): RemedyPlanTask {
  return {
    id, title, goal: `Make ${title.toLowerCase()} work end to end`, dependsOn, estTokensBand: "M",
    filesHint: [], acceptance, jobTaskId: `entry-${id}`, status: "pending", specVersion: 1,
  };
}

const base = normalizeApiFailure("0123456789abcdef", []);
const TASKS = [
  planned("T1", "Read the config file", [], ["reads a file", "reports a missing file"]),
  planned("T2", "Validate the fields", ["T1"], ["rejects an unknown key"]),
  planned("T3", "Write the tests", ["T2", "T1"], ["covers both paths"]),
];

function dashboardAt(version: number, t2Title: string): RemedyDashboard {
  return {
    ...base,
    apiHealth: { degraded: false, failedEndpoints: [] },
    plan: {
      available: true, version, approval: "pending", editable: true, notEditableBecause: "", error: "",
      tasks: TASKS.map((task) => (task.id === "T2" ? { ...task, title: t2Title } : task)),
    },
  };
}

function App() {
  const [dashboard, setDashboard] = useState(() => dashboardAt(2, "Validate the fields"));
  function reload() {
    harness.__reloads += 1;
    // The dashboard read after an accepted edit: one version later, with the edited title.
    setTimeout(() => setDashboard(dashboardAt(3, "Check every field")), 400);
  }
  return (
    <ProjectProvider token="token" jobId="0123456789abcdef" project="" onSwitched={() => {}} onHome={() => {}}>
      <RemedyShell dashboard={dashboard} serverToken="token" selectedNodeId={null} onSelectNode={() => {}} onReload={reload} />
    </ProjectProvider>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
