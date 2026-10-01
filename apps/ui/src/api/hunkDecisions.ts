// T5_F292 T003, DECISION F292 D6: the hunk decision recorded for the attempt a diff shows, as
// `/api/jobs/<id>/hunk-decisions` and `/api/jobs/<id>/task-runs/<tid>/hunk-decisions` serve it
// (`_hunk_decisions_for_view` in `packages/orchestration/ui_server.py`). A decision REPLACES the
// whole record for its attempt, so the hunk controls start from this. Pure: the path and the
// decoder reach no fetch, clock, storage or DOM; the loader lives in `remedyApi.ts`.

/** The states a recorded hunk carries (`HUNK_STATE_*` in `hunk_ledger.py`). */
export const HUNK_STATES = ["approved", "rejected", "pending"] as const;
export type HunkState = (typeof HUNK_STATES)[number];

/** One recorded hunk: its id, its state, and the reason it was rejected (`""` otherwise). */
export interface RecordedHunk {
  id: string;
  state: HunkState;
  reason: string;
}

/** The record of one attempt: its key, when it was decided (`""` when nothing is recorded), and
 *  every hunk it names, in the diff's order. */
export interface HunkDecisions {
  attemptKey: string;
  decidedAt: string;
  hunks: RecordedHunk[];
}

/** The answer for an attempt nothing is recorded for, and for any answer that cannot be read. */
export const NO_HUNK_DECISIONS: HunkDecisions = { attemptKey: "", decidedAt: "", hunks: [] };

/** The route for one diff's recorded decision: the job's own diff when `taskId` is blank, else
 *  the task run's, mirroring `diffEnvelopePath`. */
export function hunkDecisionsPath(jobId: string, token: string, taskId: string): string {
  const job = encodeURIComponent(jobId);
  const query = `?token=${encodeURIComponent(token)}`;
  return taskId.trim() === ""
    ? `/api/jobs/${job}/hunk-decisions${query}`
    : `/api/jobs/${job}/task-runs/${encodeURIComponent(taskId)}/hunk-decisions${query}`;
}

/** The decoder: total. A payload that is not an object reads as `NO_HUNK_DECISIONS`; a row that
 *  is not an object with a text `id` and one of the three states is dropped, never guessed at. */
export function readHunkDecisions(raw: unknown): HunkDecisions {
  if (raw === null || typeof raw !== "object" || Array.isArray(raw)) return { ...NO_HUNK_DECISIONS, hunks: [] };
  const payload = raw as Record<string, unknown>;
  const rows = Array.isArray(payload["hunks"]) ? payload["hunks"] : [];
  const hunks: RecordedHunk[] = [];
  for (const row of rows) {
    if (row === null || typeof row !== "object") continue;
    const entry = row as Record<string, unknown>;
    const state = entry["state"];
    if (typeof entry["id"] !== "string" || !(HUNK_STATES as readonly unknown[]).includes(state)) continue;
    hunks.push({ id: entry["id"], state: state as HunkState,
      reason: typeof entry["reason"] === "string" ? entry["reason"] : "" });
  }
  return {
    attemptKey: typeof payload["attempt_key"] === "string" ? payload["attempt_key"] : "",
    decidedAt: typeof payload["decided_at"] === "string" ? payload["decided_at"] : "",
    hunks,
  };
}
