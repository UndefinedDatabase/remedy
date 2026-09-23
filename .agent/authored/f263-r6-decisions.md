
DECISION F263 D6 (2026-09-23, round 6) — EVERY APPLY ABSORBS FIRST, THE APPLY'S DRIFT BLOCK IS
DELETED, AND A HAND EDIT THE JOB ALSO CHANGED STOPS THE APPLY WITH ITS NAME.

CONTEXT. The Acceptance list of T2_F263.md: `job apply` and `do run --apply`, and every commit
flag, always run the detection first and absorb before apply, and a hand edit made between the
run's end and the apply is absorbed and neither overwritten nor discarded (DECISION
amend0921-operator-feedback D4). Measured by the reviewer at `5fd8b648`: `apply_job` in
`packages/orchestration/job_apply.py` refuses with `target_mutated_during_job` whenever the job's
guard flag is set, then compares every file the job changed with the baseline its task recorded
and refuses a changed one as `baseline_check_failed` — and `do run --apply` and every commit
flag reach the apply through `apply_job`. After round 5 a git job's guard flag is never set.

CHOSEN. (1) `apply_job` calls `human_change.absorb_job` right after the readiness gates, before
any source is materialized or any file copied, for every job holding a last known state, a
dry run included: the record is evidence, and the repository is not written. A failure to
absorb refuses the apply with `human_change_absorb_failed: <reason>`. (2) The drift block on
the guard flag is deleted. (3) `human_change.recorded_human_changes` names every path of the
job's intact records, from any safe point or from this apply, and when the baseline check
refuses a path among them its reason keeps every existing baseline reason and adds
`human_change_conflict: <paths>` with the sentence that the apply stops rather than overwrite
either side. Nothing is merged, copied or reverted on that path; the human's file keeps its
bytes. (4) The test that pinned the deleted block now pins that the flag alone refuses nothing.

ALTERNATIVES. Absorb only on an approved apply — rejected: the Acceptance list says always, and
a dry run is where an operator first learns that a human change meets the job. Name only the
paths the apply itself detects — rejected: an edit absorbed at a run's safe point is just as
much the human's when the apply meets it. Resolve the conflict by preferring either side —
rejected: DECISION D-E forbids discarding the human's side, and the job's side is reviewed work.

REVERSE by deleting this paragraph and `tests/orchestration/test_human_change_at_apply.py`,
removing `recorded_human_changes` from `packages/orchestration/human_change.py`, and restoring
`packages/orchestration/job_apply.py` and `tests/orchestration/test_job_apply.py` from git history
at `5fd8b648`.
