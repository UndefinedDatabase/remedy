// The client half of the per-round facts route (DECISION F023 D3): the path it
// is served at, and the decoder that turns whatever arrived into the one total
// shape the L2 run detail renders. The server half is
// packages/orchestration/run_rounds_view.py; the door that fetches is
// `loadTaskRunRounds` in ./remedyApi, beside the diff and digest doors.

/** The envelope version this client reads; any other decodes as unavailable. */
export const TASK_RUN_ROUNDS_VERSION = 1;

/** One round of a task's latest run, as the server keeps it: numbers, short
 *  vocabulary words and timestamps only. Every field may be null when the run
 *  report did not record it. */
export interface TaskRunRound {
  round: number | null;
  kind: string | null;
  startedAt: string | null;
  finishedAt: string | null;
  durationMs: number | null;
  testPassed: boolean | null;
  builder: { durationMs: number | null; tokensUsed: number | null } | null;
  reviewer: { verdict: string | null; durationMs: number | null; parseRetried: boolean } | null;
}

/** The whole answer. `available` false carries the server's reason, or
 *  `unreadable` when nothing usable arrived at all. */
export interface TaskRunRounds {
  available: boolean;
  reason: string | null;
  taskId: string;
  runId: string | null;
  retriesUsed: number | null;
  rounds: TaskRunRound[];
}

/** The route, with every interpolated value percent-encoded for the reason
 *  `diffEnvelopePath` gives: the task id is a path SEGMENT. */
export function taskRunRoundsPath(request: { jobId: string; taskId: string; token: string; baseUrl?: string }): string {
  const base = request.baseUrl || "";
  const job = encodeURIComponent(request.jobId);
  const task = encodeURIComponent(request.taskId);
  return `${base}/api/jobs/${job}/task-runs/${task}/rounds?token=${encodeURIComponent(request.token)}`;
}

function record(value: unknown): Record<string, unknown> | null {
  return value !== null && typeof value === "object" && !Array.isArray(value) ? (value as Record<string, unknown>) : null;
}

function count(value: unknown): number | null {
  return typeof value === "number" && Number.isInteger(value) && value >= 0 ? value : null;
}

function text(value: unknown): string | null {
  return typeof value === "string" && value !== "" ? value : null;
}

function decodeRound(value: unknown): TaskRunRound | null {
  const r = record(value);
  if (!r) return null;
  const builder = record(r.builder);
  const reviewer = record(r.reviewer);
  return {
    round: count(r.round),
    kind: text(r.kind),
    startedAt: text(r.started_at),
    finishedAt: text(r.finished_at),
    durationMs: count(r.duration_ms),
    testPassed: typeof r.test_passed === "boolean" ? r.test_passed : null,
    builder: builder ? { durationMs: count(builder.duration_ms), tokensUsed: count(builder.tokens_used) } : null,
    reviewer: reviewer
      ? { verdict: text(reviewer.verdict), durationMs: count(reviewer.duration_ms), parseRetried: reviewer.parse_retried === true }
      : null,
  };
}

/** Decode one payload for `taskId`. NEVER THROWS: a payload that is not an
 *  envelope of this version, or names another task, is unavailable. */
export function decodeTaskRunRounds(payload: unknown, taskId: string): TaskRunRounds {
  const unreadable: TaskRunRounds = {
    available: false, reason: "unreadable", taskId, runId: null, retriesUsed: null, rounds: [],
  };
  const env = record(payload);
  if (!env || env.version !== TASK_RUN_ROUNDS_VERSION || env.task_id !== taskId) return unreadable;
  const rounds = Array.isArray(env.rounds)
    ? env.rounds.map(decodeRound).filter((r): r is TaskRunRound => r !== null)
    : [];
  return {
    available: env.available === true,
    reason: env.available === true ? null : text(env.reason) ?? "unreadable",
    taskId,
    runId: text(env.run_id),
    retriesUsed: count(env.retries_used),
    rounds: env.available === true ? rounds : [],
  };
}
