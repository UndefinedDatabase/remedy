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
};

/** The entry for an OWN key of the catalog, or null — never a prototype member
 *  (`toString`, `constructor`), which `hasOwnProperty` keeps out. */
export function termEntry(key: string): TermEntry | null {
  return Object.prototype.hasOwnProperty.call(TERM_CATALOG, key) ? TERM_CATALOG[key] : null;
}
