// The explanation catalog (T5_F043 T001, DECISION F043 D1): the one source every surface's
// `Term` draws from. Each entry names the file that DEFINES its term (`source`) and a phrase
// that file states (`anchor`); `terminology.test.ts` reads every source back and requires the
// anchor still there, so a definition that is reworded or moved turns the catalog red instead
// of leaving a stale explanation behind it. Deliberate absence: Remedy deliberately does not
// explain a term whose defining feature has not shipped.

/** One entry: a plain-language explanation, quoted from — not copying — its source. */
export interface TermEntry {
  readonly title: string;
  readonly body: string;
  readonly source: string;
  readonly anchor: string;
}

/** The longest a body may run, so a tooltip stays a tooltip. */
export const TERM_BODY_MAX_CHARS = 240;

/** A term key: dotted lowercase words, one dot at least. A word whose meaning depends on its
 *  context (a status, a phase) takes one key per context rather than one shared key. */
export const TERM_KEY_PATTERN = /^[a-z][a-z0-9_]*(\.[a-z0-9_]+)+$/;

export const TERM_CATALOG: Readonly<Record<string, TermEntry>> = {
  "status.live": {
    title: "Live",
    body: "This job is running, and the cockpit receives its events the moment they happen.",
    source: "docs/roadmap/features/T5_F008.md",
    anchor: "(live | reconnecting | delayed)",
  },
  "status.idle": {
    title: "Idle",
    body: "No part of this job is running right now. The cockpit shows the job as it last stood.",
    source: "apps/ui/src/cockpitLogic.ts",
    anchor: "return dashboard.live.running === true;",
  },
  "status.reconnecting": {
    title: "Reconnecting",
    body: "The live connection dropped and the cockpit is opening it again. Events that arrive meanwhile are not lost: they are replayed once it is back.",
    source: "docs/roadmap/features/T5_F008.md",
    anchor: "resume replays exactly the missed span",
  },
  "status.delayed": {
    title: "Delayed",
    body: "The live connection is not available, so the cockpit asks for new events at intervals instead. What you see can lag behind the job.",
    source: "docs/roadmap/features/T5_F008.md",
    anchor: 'labels itself visibly ("delayed") instead of pretending to be live',
  },
  "status.replay": {
    title: "Replay",
    body: "You are looking at an earlier moment of this job, chosen on the timeline. Press LIVE on the timeline to return to the present.",
    source: "docs/roadmap/features/T5_F024.md",
    anchor: "the pill says REPLAY",
  },
  "phase.job": {
    title: "Job",
    body: "The job phase begins with the job's first event.",
    source: "docs/roadmap/features/T5_F024.md",
    anchor: "Job begins at the ledger's first row",
  },
  "phase.planning": {
    title: "Planning",
    body: "The planning phase begins when planning starts.",
    source: "docs/roadmap/features/T5_F024.md",
    anchor: "sends the three `planning_*` kinds to Planning",
  },
  "phase.build": {
    title: "Build",
    body: "The build phase begins when the first task run starts.",
    source: "docs/roadmap/features/T5_F024.md",
    anchor: "`task_run_started` and the two `builder_*` kinds to Build",
  },
  "phase.test": {
    title: "Test",
    body: "The test phase begins when the first test or verification runs.",
    source: "docs/roadmap/features/T5_F024.md",
    anchor: "the `test_run_*` and `verification_*` kinds to Test",
  },
  "phase.review": {
    title: "Review",
    body: "The review phase begins when the first review verdict arrives.",
    source: "docs/roadmap/features/T5_F024.md",
    anchor: "a `task_round_completed` carrying a reviewer's verdict to Review",
  },
  "phase.finalized": {
    title: "Finalized",
    body: "Reached when every task has passed, and held only while that stays true.",
    source: "docs/roadmap/features/T5_F024.md",
    anchor: "holds only while every task has passed",
  },
  "metric.open": {
    title: "Open",
    body: "Questions this job is waiting for you to answer. You find them in the decision inbox.",
    source: "packages/orchestration/ui_server.py",
    anchor: "Number of still-open human decisions for a job",
  },
  "metric.planned": {
    title: "Planned",
    body: "Tasks of this job that have not started yet.",
    source: "packages/orchestration/ui_server.py",
    anchor: "\"planned\": sum(1 for t in job.tasks if",
  },
  "metric.done": {
    title: "Done",
    body: "Tasks of this job that have finished.",
    source: "packages/orchestration/ui_server.py",
    anchor: "\"done\": sum(1 for t in job.tasks if",
  },
  "metric.progress": {
    title: "Progress",
    body: "The share of this job's tasks that have finished. A job without tasks shows 0%.",
    source: "packages/orchestration/ui_server.py",
    anchor: "\"progress_percent\": round((sum(1 for t in job.tasks",
  },
  "metric.tests": {
    title: "Tests",
    body: "How many of this job's recorded test runs passed. The dot shows whether the latest run passed or failed.",
    source: "packages/orchestration/ui_server.py",
    anchor: "Safe test counters from the event ledger. Counts only, no output.",
  },
  "metric.proof": {
    title: "Proof",
    body: "How many of this job's changes carry a verified proof, out of all its changes. A dash means the proof could not be read.",
    source: "packages/orchestration/ui_server.py",
    anchor: "Counts only (total changes vs verified).",
  },
  "task.done": {
    title: "Done",
    body: "This task has finished.",
    source: "apps/ui/src/api/remedyApi.ts",
    anchor: "if (text.includes(\"done\") || text.includes(\"pass\") || text.includes(\"complete\") || text.includes(\"applied\")) return \"done\";",
  },
  "task.in_progress": {
    title: "In progress",
    body: "This task is running now.",
    source: "apps/ui/src/api/remedyApi.ts",
    anchor: "text.includes(\"running\") || text.includes(\"progress\")) return \"current\";",
  },
  "blocked.task": {
    title: "Blocked",
    body: "This task stopped: it failed, or something blocked it.",
    source: "apps/ui/src/api/remedyApi.ts",
    anchor: "if (text.includes(\"block\") || text.includes(\"fail\")) return \"blocked\";",
  },
  "task.planned": {
    title: "Planned",
    body: "This task is not running: it has not started yet, or it was paused or cancelled.",
    source: "apps/ui/src/api/remedyApi.ts",
    anchor: "if (text.includes(\"suggest\")) return \"suggested\"; return \"pending\";",
  },
  "task.partially_applied": {
    title: "Partially applied",
    body: "Only some of this task's changes landed in the project; the rest did not apply.",
    source: "packages/orchestration/proof_chain.py",
    anchor: "The apply fold agrees or it says \"partial\"",
  },
  "panel.tasks": {
    title: "Tasks",
    body: "The steps of this job's plan. The planner decides how many there are, up to a configured limit.",
    source: "docs/system/vocabulary.md",
    anchor: "One step in a job plan; the planner chooses how many",
  },
  "panel.decisions": {
    title: "Decision inbox",
    body: "Questions Remedy cannot answer for itself, waiting for you. Open ones come first, the most urgent at the top: a question grows more urgent the longer it waits and the more tasks it holds up.",
    source: "apps/ui/src/api/decisionOrder.ts",
    anchor: "`(blockedCount + 1) * ageSeconds`, and the inbox reads open cards first",
  },
  "panel.activity": {
    title: "Activity",
    body: "What this job has been doing, in plain words. Choose a row to find its task in the graph.",
    source: "docs/roadmap/features/T5_F021.md",
    anchor: "feed rows carry their seq and click-jump to their node in the graph",
  },
  "panel.agent_now": {
    title: "Agent is doing now",
    body: "The newest real action of this job's agents. Reading files and other bookkeeping are left out.",
    source: "apps/ui/src/components/panels/AgentNowCard.tsx",
    anchor: "Bookkeeping is excluded on purpose",
  },
  "agent.live": {
    title: "Live",
    body: "Shown while the job is running and its agents did something in the last half minute.",
    source: "apps/ui/src/components/panels/AgentNowCard.tsx",
    anchor: "RUNNING AND RECENT, never either alone.",
  },
  "graph.scrubbed": {
    title: "Scrubbed",
    body: "The graph shows this job as it stood at the moment chosen on the timeline. New events keep arriving and wait until you return to LIVE.",
    source: "docs/roadmap/features/T5_F024.md",
    anchor: "scrubbed mode is unmistakably labeled with live updates queuing behind the toggle",
  },
};

/** The entry for an OWN key of the catalog, or null — never a prototype member
 *  (`toString`, `constructor`), which `hasOwnProperty` keeps out. */
export function termEntry(key: string): TermEntry | null {
  return Object.prototype.hasOwnProperty.call(TERM_CATALOG, key) ? TERM_CATALOG[key] : null;
}
