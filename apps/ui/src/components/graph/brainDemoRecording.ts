// The demo recording DECISION F019 D1 (10) calls for: a fixture stream
// captured from a real job, committed beside the reducer's own fixtures
// (brainReducer.fixtures.ts), so the brain graph can render with no live
// server. Captured on 2026-09-27 from a real job run on the fake builder and
// reviewer providers — no network, no model — for the order "fix
// src/main.py and update README.md". The task list below is the dashboard's
// `tasks` as `normalizeDashboardPayload` (apps/ui/src/api/remedyApi.ts) maps
// them, read after `python3 -m apps.cli.main do "<order>" --no-llm
// --plan-only --json` planned the job and before `python3 -m apps.cli.main
// job run <job id> --builder-provider fake --reviewer-provider fake --json`
// ran it. The frames are every event the `events-since` cursor endpoint
// served after the run, paged from cursor 0, byte-for-byte in their field
// values. The product's demo mode stays F084's; T003's end-to-end test
// compares a live fake job's model against this recording's.
import type { RemedyTaskItem } from "../../api/types";
import type { BrainStreamFrame } from "../../api/brainStream";
import { feedRowOf } from "../../api/feedRow";
import type { BrainEventRow } from "./brainOntology";

export const BRAIN_DEMO_JOB_ID = "1fe464f842e74f55";

/** The captured before-run task list, normalized. `kind` is not among the
 *  fields the capture holds with a non-null value: `normalizeDashboardPayload`
 *  falls back to `"task"` when the raw dashboard task carries none, which is
 *  what both of these captured tasks did. */
export const BRAIN_DEMO_TASKS: readonly RemedyTaskItem[] = [
  {
    id: "fe1b5b487fda490f",
    label: "Deliver src/main.py",
    state: "pending",
    kind: "task",
    checked: false,
    muted: true,
    nodeId: "fe1b5b487fda490f",
    testStatus: "none",
    proofStatus: "none",
    applyStatus: "not_applied",
  },
  {
    id: "4b3ddac9dba846af",
    label: "Deliver README.md",
    state: "pending",
    kind: "task",
    checked: false,
    muted: true,
    nodeId: "4b3ddac9dba846af",
    testStatus: "none",
    proofStatus: "none",
    applyStatus: "not_applied",
  },
];

/** Every frame the `events-since` cursor endpoint served after the run, in
 *  seq order, wrapped the way `GOLDEN_A_FRAMES` (brainReducer.fixtures.ts)
 *  wraps them: `{ seq, event: {...} }`. */
export const BRAIN_DEMO_FRAMES: readonly BrainStreamFrame[] = [
  { seq: 0, event: { seq: 0, event: "task_run_started", timestamp: "2026-09-27T00:54:45.510057+00:00", outcome: "", task_id: "fe1b5b487fda490f", attempt_id: "b1603f4616344102" } },
  { seq: 1, event: { seq: 1, event: "task_round_completed", timestamp: "2026-09-27T00:54:46.009027+00:00", outcome: "needs_repair", task_id: "fe1b5b487fda490f", attempt_id: "b1603f4616344102" } },
  { seq: 2, event: { seq: 2, event: "task_round_repaired", timestamp: "2026-09-27T00:54:46.009224+00:00", outcome: "changed", task_id: "fe1b5b487fda490f", attempt_id: "b1603f4616344102" } },
  { seq: 3, event: { seq: 3, event: "task_round_completed", timestamp: "2026-09-27T00:54:46.009370+00:00", outcome: "pass", task_id: "fe1b5b487fda490f", attempt_id: "b1603f4616344102" } },
  { seq: 4, event: { seq: 4, event: "task_run_completed", timestamp: "2026-09-27T00:54:46.082451+00:00", outcome: "pass", task_id: "fe1b5b487fda490f", attempt_id: "b1603f4616344102" } },
  { seq: 5, event: { seq: 5, event: "task_run_started", timestamp: "2026-09-27T00:54:46.155145+00:00", outcome: "", task_id: "4b3ddac9dba846af", attempt_id: "935e9371d7ce4fe5" } },
  { seq: 6, event: { seq: 6, event: "task_round_completed", timestamp: "2026-09-27T00:54:46.679271+00:00", outcome: "needs_repair", task_id: "4b3ddac9dba846af", attempt_id: "935e9371d7ce4fe5" } },
  { seq: 7, event: { seq: 7, event: "task_round_repaired", timestamp: "2026-09-27T00:54:46.679481+00:00", outcome: "changed", task_id: "4b3ddac9dba846af", attempt_id: "935e9371d7ce4fe5" } },
  { seq: 8, event: { seq: 8, event: "task_round_completed", timestamp: "2026-09-27T00:54:46.679637+00:00", outcome: "pass", task_id: "4b3ddac9dba846af", attempt_id: "935e9371d7ce4fe5" } },
  { seq: 9, event: { seq: 9, event: "task_run_completed", timestamp: "2026-09-27T00:54:46.734042+00:00", outcome: "pass", task_id: "4b3ddac9dba846af", attempt_id: "935e9371d7ce4fe5" } },
];

/** `BRAIN_DEMO_FRAMES` through the one frame parser, `feedRowOf`
 *  (DECISION F019 D1 (2)) — `FeedRow` is structurally a `BrainEventRow`, so
 *  no adapter sits between this and `reduceBrainEvent`/`rebuildBrainModel`. */
export function brainDemoRows(): BrainEventRow[] {
  return BRAIN_DEMO_FRAMES.map((frame) => feedRowOf(frame, 0));
}
