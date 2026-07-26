# Live Review — F047 Checkpoint & resume (kill-proof)

Branch: feature/f047-checkpoint-resume
LAST_REVIEWED_SHA: 89c4ef0e723f89c58956de3964d1653461d273b9
Finding IDs continue monotonically from R-0145.

## Findings

- R-0146 · Medium · round 1 (89c4ef0..fd93b31)
  `remedy job resume <id> --dry-run` without `--checkpoint` silently
  drops --dry-run and executes for real: the catalog advertises
  "Preview resume without executing" on job.resume, but the dispatch
  passes dry_run only to the event-replay branch; _cmd_job_resume
  neither accepts nor receives it and hands off to the multi-cycle
  executor (apply_write, may_mutate_repo). A preview request must
  never silently execute. Fix: F047 mode honors --dry-run as a
  read-only preview — reports the checkpoint (or the no-checkpoint
  fallback) and what the checks would decide, consumes NOTHING (a
  pending stop request must remain pending), no executor hand-off,
  exit 0. Tests pin: no hand-off, stop not consumed, preview named in
  output. Resolved when tests are green and the reviewer verifies.

## Verdicts

(none yet)
