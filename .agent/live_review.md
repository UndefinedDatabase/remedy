# Live Review — F047 Checkpoint & resume (kill-proof)

Branch: feature/f047-checkpoint-resume
LAST_REVIEWED_SHA: 3b257f6
Finding IDs continue monotonically from R-0145.

## Steps

- Round 1 — Setup + T001 (checkpoint writer/loader) + T002 (resume CLI),
  89c4ef0..fd93b31. Reviewed in round 2; produced finding R-0146.
- Round 2 — R-0146 repair + T003 (kill -9 / resume, exactly-once),
  fd93b31..72fc653. Verdict PASS (below).
- Integration gate — full suite branch vs. base 89c4ef0, from 72fc653.
- Closure — its own reviewer-gated round; no artifacts built yet.

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
  Done: R-0146 — `_cmd_job_resume` takes `dry_run`, the dispatch passes
  it in the no-checkpoint branch, and the dry-run path reports every
  check read-only (`stop_requested`, never `consume_stop`), skips the
  executor and exits 0. Pinned by 9 tests in TestDryRunPreview plus a
  dispatch pass-through test; the stop-still-pending assertion re-reads
  the request rather than trusting the printed line.
  Resolved: verified by the reviewer in round 2 (fd93b31..72fc653).

## Verdicts

- Round 2 (R-0146 repair + T003, fd93b31..72fc653): PASS — issued by
  the reviewer after independent verification. Reviewer re-ran: kill
  test 7 passed in three consecutive runs (flake sniff), resume/
  checkpoints/executor suites 121 passed, canary 42 passed, ruff
  clean. R-0146 fix verified read-only: the preview observes
  stop_requested and never consume_stop, no executor hand-off; the
  test re-reads the pending request from disk after the preview.
  Scope addition 2fe5887 accepted as documented, not silent: T003's
  exactly-once assertion exposed a real defect — cycle numbering was
  per invocation, so a resumed run overwrote the killed run's cycle
  and checkpoint records; next_cycle_index(job_id) now continues the
  job's numbering (both evidence areas consulted), F046 single-pass
  default unmoved. CycleRecord.executed_task_ids records executions,
  not successes. Torn-checkpoint-by-explicit-write accepted: the
  atomic write makes a genuine mid-write tear non-producible on
  demand; the loader property under test is identical. Verification
  tier: round gate (scoped) + canary. LAST_REVIEWED_SHA = 72fc653.

- Integration gate (branch 72fc653..4692cca vs base 89c4ef0): PASS —
  issued by the reviewer after independent verification. Worker
  evidence: three -n auto branch runs 196/177/158 failed (known
  F135/F052 xdist churn, both directions vs base 190); 39 branch-only
  ids re-run serially -> 37 passed (flake class), 2 reproducible
  failures both asserting "Steps" in .agent/live_review.md —
  F047-attributable (a state file this feature authored; base passed
  only by prose accident), fixed in-round as a declared state-file
  deviation (real "## Steps" section, decisions.md entry, neither
  test modified). Post-fix: 6 branch-only ids, all pass serially.
  Reviewer re-ran independently: full suite -n auto -> 158 failed /
  14066 passed in 177.02s (matches within churn); the two fixed
  contract tests pass; F047's four suites 128 passed under -n auto;
  the six post-fix flake ids pass serially; canary 42 passed;
  reviewer-authored verdict and resolution text verified
  byte-identical; git worktree list clean. Zero F047-attributable
  regressions. Only this entry carries the "full suite" claim.
