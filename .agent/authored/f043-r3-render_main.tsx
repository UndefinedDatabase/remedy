// F043 R3's render harness (evidence, not product): mounts the REAL `RemedyShell` from
// `apps/ui/src` with the app's own token and global sheets, over a fixed running job whose
// metrics carry a token breakdown and an estimated cost, a task in each state the task list
// words differently, and one open decision. A `window.fetch` stand-in answers every request
// with a 500, so every door the shell reads reports itself unavailable and nothing waits on a
// server; the page never leaves `127.0.0.1`.
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { costMetricOf } from "../../apps/ui/src/api/costMetric";
import { buildDecisionCardModel } from "../../apps/ui/src/api/decisionCard";
import { normalizeApiFailure } from "../../apps/ui/src/api/remedyApi";
import type { RemedyDashboard, RemedyMetric, RemedyState, RemedyTaskItem } from "../../apps/ui/src/api/types";
import { RemedyShell } from "../../apps/ui/src/components/shell/RemedyShell";

window.fetch = async (): Promise<Response> => new Response("{}", { status: 500 });

function task(id: string, state: RemedyState, applyStatus?: string): RemedyTaskItem {
  return {
    id, label: `Task ${id}`, state, kind: "task", checked: state === "done", muted: false, nodeId: `node-${id}`,
    ...(applyStatus === undefined ? {} : { applyStatus }),
  };
}

const METRICS: RemedyMetric[] = [
  { key: "open", label: "Open", value: 1 },
  { key: "planned", label: "Planned", value: 1 },
  { key: "done", label: "Done", value: 2 },
  { key: "progress", label: "Progress", value: 40, suffix: "%" },
  { key: "tests", label: "Tests", value: 3, state: "pass" },
  { key: "proof", label: "Proof", value: 1, suffix: "/2" },
  { key: "tokens", label: "Tokens", value: 1200, tooltip: { builder: 1200 } },
  { key: "cost", label: "Cost", value: "—", cost: costMetricOf({ spent_usd: 0.42, limit_usd: 2, basis: { cost: "estimated" } }) },
];

const base = normalizeApiFailure("job-1", []);
const dashboard: RemedyDashboard = {
  ...base,
  metrics: METRICS,
  live: { ...base.live, running: true },
  tasks: [task("a", "done"), task("b", "current"), task("c", "blocked"), task("d", "pending"), task("e", "done", "partial")],
  decisionInbox: [buildDecisionCardModel({ id: "d-1", status: "open", type: "clarification", age_seconds: 60, blocked_count: 1 })],
};

createRoot(document.getElementById("root")!).render(
  <RemedyShell dashboard={dashboard} serverToken="token" selectedNodeId={null} onSelectNode={() => {}} />,
);
