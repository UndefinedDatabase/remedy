// THE ATTEMPT VIEW (DECISION F029 D5): pure functions of a task item that
// decide what the graph's chip and the popover's Attempts list show. Nothing
// here reaches a fetch, a clock or a DOM — every answer is a function of the
// item alone, exactly as `taskSpecView.ts` reads a task's spec and version
// chain and for the same reason: the shipped vitest config collects
// `src/**/*.test.ts` only and no DOM harness exists, so a rule written
// inside a component or the graph builder would ship untested.
import type { RemedyState, RemedyTaskAttempt, RemedyTaskItem } from "./types";

/** DECISION F029 D5 (1) — the CANVAS chip's own fragment for a task on its
 *  second or later attempt: short, because the chip itself is small
 *  (graph_spec §4's synapse-scale text), exactly the size
 *  `ORIGIN_CANVAS_CHIP_TEXT` in `injectView.ts` is built for. `taskChipOf` in
 *  `buildForceBrainModel.ts` is the one caller, joining this after `v<n>`
 *  and "added" when they apply. */
export function attemptChipText(n: number): string {
  return `attempt ${n}`;
}

/** DECISION F029 D5 (2) — one changed fact between two attempt readings: its
 *  label and the value shown before and after. Mirrors
 *  `TaskSpecVersionChange` in `taskSpecView.ts` exactly. */
export interface TaskAttemptChange {
  label: string;
  before: string;
  after: string;
}

/** One row of the popover's Attempts list: the attempt it names, its own
 *  label, its facts in words, the facts that changed from the row before it
 *  (empty for the first row and for the current row), and whether it is the
 *  current, still-running attempt. */
export interface TaskAttemptRow {
  attempt: number;
  label: string;
  facts: string[];
  changes: TaskAttemptChange[];
  current: boolean;
}

const ENDED_WORDS: Readonly<Record<string, string>> = {
  applied_to_job_workspace: "It was applied",
  passed: "It was applied",
  blocked: "It was blocked",
  failed: "It failed",
  skipped: "It was skipped",
  vetoed: "It was vetoed",
  pending: "It had not run",
};

/** How an earlier attempt ended, in words — the closed set of task status
 *  words this browser already names (`pingpong_job.py`'s `TASK_*`
 *  constants), or `` `It ended as ${status}` `` for any other value. */
function endedFact(status: string): string {
  return ENDED_WORDS[status] ?? `It ended as ${status}`;
}

/** The reviewer's verdict, in words — `""` reads as no verdict was ever
 *  recorded, never a fabricated one. */
function verdictFact(verdict: string): string {
  return verdict === "" ? "no review verdict" : `the reviewer said ${verdict}`;
}

/** Whether the attempt's tests passed, in words — `null` (never run, or not
 *  recorded) reads as "no test result", distinct from a recorded failure. */
function testsFact(testPassed: boolean | null): string {
  if (testPassed === true) return "its tests passed";
  if (testPassed === false) return "its tests failed";
  return "no test result";
}

/** The model the attempt ran with, in words — an empty override reads as
 *  the job's own model, never `` `it ran on ` `` with nothing after it. */
function modelFact(modelOverride: string): string {
  return modelOverride === "" ? "it ran on the job's own model" : `it ran on ${modelOverride}`;
}

/** The attempt's worktree commit, in words — its first twelve characters
 *  (the same width `git`'s own short hash and this codebase's other commit
 *  mentions use), or "no commit" when none was ever recorded. */
function commitFact(worktreeCommit: string): string {
  return worktreeCommit === "" ? "no commit" : `commit ${worktreeCommit.slice(0, 12)}`;
}

/** THE FIVE FACTS, IN ORDER: how the attempt ended, the reviewer's verdict,
 *  its tests, its model, and its commit — the fixed order `taskAttemptRows`
 *  below both reads them in and diffs them in. */
function attemptFacts(entry: RemedyTaskAttempt): string[] {
  return [
    endedFact(entry.status),
    verdictFact(entry.reviewerVerdict),
    testsFact(entry.testPassed),
    modelFact(entry.modelOverride),
    commitFact(entry.worktreeCommit),
  ];
}

// The five facts' own labels, in the same fixed order `attemptFacts` answers
// them — the order DECISION F029 D5 names for a row's `changes`.
const FACT_LABELS: readonly string[] = ["Outcome", "Reviewer", "Tests", "Model", "Commit"];

/** The facts that changed between one earlier row's own five facts and the
 *  row before it: `[]` for the first earlier row, which has nothing before
 *  it to differ from — mirrors `taskSpecView.ts`'s `changesFrom` exactly. */
function changesFromFacts(previous: string[] | null, next: string[]): TaskAttemptChange[] {
  if (!previous) return [];
  const changes: TaskAttemptChange[] = [];
  for (let i = 0; i < FACT_LABELS.length; i++) {
    if (previous[i] !== next[i]) {
      changes.push({ label: FACT_LABELS[i], before: previous[i], after: next[i] });
    }
  }
  return changes;
}

const CURRENT_STATE_WORDS: Readonly<Partial<Record<RemedyState, string>>> = {
  pending: "waiting to run",
  current: "running",
  done: "finished",
  blocked: "blocked",
};

/** The current row's own present-tense word — the four DECISION F029 D5
 *  names, or the state itself for any other (`suggested` has no attempt
 *  fan to begin with, but this stays total rather than assuming so). */
function currentStateWord(state: RemedyState): string {
  return CURRENT_STATE_WORDS[state] ?? state;
}

/** DECISION F029 D5 (2), (3) — the popover's Attempts list: `[]` unless the
 *  item carries at least one earlier attempt, else one row per entry
 *  (oldest first, exactly the order the server archives them in), each
 *  row's `changes` against the row before it, and last the current row —
 *  the task's present status, in words, with no `changes` of its own. */
export function taskAttemptRows(item: RemedyTaskItem | undefined): TaskAttemptRow[] {
  if (!item || !item.attempts || item.attempts.length === 0) return [];

  const rows: TaskAttemptRow[] = [];
  let previousFacts: string[] | null = null;
  for (const entry of item.attempts) {
    const facts = attemptFacts(entry);
    rows.push({
      attempt: entry.attempt,
      label: `Attempt ${entry.attempt}`,
      facts,
      changes: changesFromFacts(previousFacts, facts),
      current: false,
    });
    previousFacts = facts;
  }
  rows.push({
    attempt: item.attempt as number,
    label: `Attempt ${item.attempt} · current`,
    facts: [`Now ${currentStateWord(item.state)}`],
    changes: [],
    current: true,
  });
  return rows;
}

/** One row's facts as the one sentence the list draws beneath its button —
 *  joined by "; ", ended by a full stop, its first letter upper-cased.
 *  Mirrors `taskSpecView.ts`'s own small text-assembly helpers. */
export function attemptFactsSentence(facts: readonly string[]): string {
  const sentence = `${facts.join("; ")}.`;
  return sentence.charAt(0).toUpperCase() + sentence.slice(1);
}
