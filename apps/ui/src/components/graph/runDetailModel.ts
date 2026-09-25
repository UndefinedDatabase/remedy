// Owns what the L2 run detail SAYS about one run node: its verdict, the round
// it belongs to, and its tokens, duration and retries, each either a real value
// or a plain sentence saying why it is not shown. PURE: it reads the run node,
// the ledger rows the graph folded, the per-round facts of the task's latest
// run (api/taskRunRounds.ts) and the dashboard's prompt trace, and returns
// text, so every answer is goldened headless (graph_spec.md §10, DECISION F023
// D4). Nothing here guesses a number the evidence does not hold.
import type { TaskRunRound, TaskRunRounds } from "../../api/taskRunRounds";
import type { RemedyPromptTraceItem } from "../../api/types";
import type { BrainEventRow, BrainNode } from "./brainOntology";
import { GLYPHS } from "./renderers/glyphPaths";

/** One fact of the detail: a value to show, or the reason there is none. */
export type RunFact = { value: string } | { missing: string };

export interface RunDetail {
  /** The run's kind as the legend names it, e.g. "Review run". */
  title: string;
  /** The verdict in words, e.g. "Needs repair". */
  verdict: string;
  /** The task the run belongs to, by its bare id. */
  taskId: string;
  /** The round of the task's run this node stands for, when it can be told. */
  round: number | null;
  tokens: RunFact;
  duration: RunFact;
  retries: RunFact;
  /** The prompt the "Why" button opens, or null when none was recorded. */
  promptItemId: string | null;
}

export const RUN_FACT_LOADING = "Loading the run report.";
export const RUN_FACT_RUNNING = "The run is still going.";
export const RUN_FACT_EARLIER = "Only the task's latest run keeps its report.";
export const RUN_FACT_NO_RUN = "This task has not finished a run yet.";
export const RUN_FACT_UNREADABLE = "The run report could not be read.";
export const RUN_FACT_NO_ROUND = "The run report has no entry for this round.";
export const RUN_FACT_REVIEWER_TOKENS = "The run report does not record the reviewer's tokens.";
export const RUN_FACT_TEST_TOKENS = "A test run makes no model call.";
export const RUN_FACT_TEST_TIMING = "Test runs are not timed on their own.";

const VERDICT_WORDS: Readonly<Record<string, string>> = {
  pass: "Passed",
  fail: "Failed",
  needs_repair: "Needs repair",
  blocked: "Blocked",
};

const STATE_WORDS: Readonly<Record<BrainNode["state"], string>> = {
  open: "Open",
  planned: "Waiting",
  in_progress: "Running",
  pass: "Passed",
  fail: "Failed",
  blocked: "Stopped before it finished",
  vetoed: "Vetoed",
  paused: "Paused",
};

/** A duration in words: "850 ms", "4.2 s", "38 s", "2 min 5 s". */
export function formatDurationMs(ms: number): string {
  if (ms < 1000) return `${ms} ms`;
  if (ms < 9950) return `${(ms / 1000).toFixed(1)} s`;
  const whole = Math.round(ms / 1000);
  if (whole < 60) return `${whole} s`;
  return `${Math.floor(whole / 60)} min ${whole % 60} s`;
}

/** A token count with thousands separators: "1,834". */
export function formatTokens(count: number): string {
  return count.toLocaleString("en-US");
}

/** Where a run node sits in its task's ledger: the seq of the builder run it
 *  belongs to, the round within that run (review runs only), and whether that
 *  builder run is the task's latest, the only one whose report the task keeps. */
export function runPlaceOf(node: Pick<BrainNode, "kind" | "seq">, taskId: string, rows: readonly BrainEventRow[]):
  { startSeq: number | null; round: number | null; latest: boolean } {
  const own = rows.filter((r) => r.taskId === taskId).sort((a, b) => a.seq - b.seq);
  const starts = own.filter((r) => r.kind === "task_run_started").map((r) => r.seq);
  const startSeq = starts.filter((s) => s <= node.seq).pop() ?? null;
  const latest = startSeq !== null && startSeq === starts[starts.length - 1];
  if (node.kind !== "review_run" || startSeq === null) return { startSeq, round: null, latest };
  const round = own.filter((r) => r.kind === "task_round_completed" && r.seq > startSeq && r.seq <= node.seq).length;
  return { startSeq, round, latest };
}

function missingFor(rounds: TaskRunRounds | null): string {
  if (rounds === null) return RUN_FACT_LOADING;
  if (rounds.reason === "no_run_recorded") return RUN_FACT_NO_RUN;
  return RUN_FACT_UNREADABLE;
}

function sum(values: readonly (number | null)[]): number | null {
  const known = values.filter((v): v is number => v !== null);
  return known.length === 0 ? null : known.reduce((a, b) => a + b, 0);
}

function reviewFacts(round: TaskRunRound | undefined): Pick<RunDetail, "tokens" | "duration" | "retries"> {
  if (!round || !round.reviewer) {
    return { tokens: { missing: RUN_FACT_NO_ROUND }, duration: { missing: RUN_FACT_NO_ROUND }, retries: { missing: RUN_FACT_NO_ROUND } };
  }
  const ms = round.reviewer.durationMs;
  return {
    tokens: { missing: RUN_FACT_REVIEWER_TOKENS },
    duration: ms === null ? { missing: RUN_FACT_NO_ROUND } : { value: formatDurationMs(ms) },
    retries: { value: round.reviewer.parseRetried ? "Asked again once: the first reply could not be read" : "None" },
  };
}

function builderFacts(rounds: TaskRunRounds): Pick<RunDetail, "tokens" | "duration" | "retries"> {
  const tokens = sum(rounds.rounds.map((r) => r.builder?.tokensUsed ?? null));
  const ms = sum(rounds.rounds.map((r) => r.durationMs));
  const repairs = rounds.rounds.filter((r) => r.kind === "repair").length;
  const provider = rounds.retriesUsed;
  const parts = [`${repairs} repair round${repairs === 1 ? "" : "s"}`];
  if (provider !== null) parts.push(`${provider} provider retr${provider === 1 ? "y" : "ies"}`);
  return {
    tokens: tokens === null ? { missing: RUN_FACT_NO_ROUND } : { value: `${formatTokens(tokens)} (the builder, as the provider reported)` },
    duration: ms === null ? { missing: RUN_FACT_NO_ROUND } : { value: formatDurationMs(ms) },
    retries: { value: parts.join(", ") },
  };
}

/** The prompt "Why" opens: the reviewer's prompt of a review run's round, or
 *  the builder's first prompt of a builder run's task. */
function promptFor(node: Pick<BrainNode, "kind">, taskId: string, round: number | null,
  items: readonly RemedyPromptTraceItem[]): string | null {
  const own = items.filter((p) => p.taskId === taskId);
  if (node.kind === "review_run" && round !== null) {
    return own.find((p) => p.role === "reviewer" && p.round === round)?.id ?? null;
  }
  if (node.kind === "builder_run") {
    return [...own].filter((p) => p.role === "builder").sort((a, b) => a.round - b.round)[0]?.id ?? null;
  }
  return null;
}

/** The whole detail of one run node. `rounds` is null while the report loads. */
export function runDetailOf(input: {
  node: Pick<BrainNode, "id" | "kind" | "state" | "parentId" | "seq" | "meta">;
  rows: readonly BrainEventRow[];
  rounds: TaskRunRounds | null;
  promptItems: readonly RemedyPromptTraceItem[];
}): RunDetail {
  const { node, rows, rounds, promptItems } = input;
  const taskId = (node.parentId ?? "").replace(/^task:/, "");
  const place = runPlaceOf(node, taskId, rows);
  const outcome = typeof node.meta.outcome === "string" ? node.meta.outcome : "";
  const base = {
    title: GLYPHS[node.kind].name,
    verdict: VERDICT_WORDS[outcome] ?? STATE_WORDS[node.state],
    taskId,
    round: place.round,
    promptItemId: promptFor(node, taskId, place.round, promptItems),
  };
  if (node.kind === "test_run") {
    return { ...base, tokens: { value: RUN_FACT_TEST_TOKENS }, duration: { missing: RUN_FACT_TEST_TIMING }, retries: { value: "None" } };
  }
  const why = node.state === "in_progress" ? RUN_FACT_RUNNING
    : !place.latest ? RUN_FACT_EARLIER
      : rounds === null || !rounds.available ? missingFor(rounds) : null;
  if (why !== null || rounds === null) {
    const missing = why ?? RUN_FACT_LOADING;
    return { ...base, tokens: { missing }, duration: { missing }, retries: { missing } };
  }
  if (node.kind === "review_run") {
    return { ...base, ...reviewFacts(rounds.rounds.find((r) => r.round === place.round)) };
  }
  return { ...base, ...builderFacts(rounds) };
}
