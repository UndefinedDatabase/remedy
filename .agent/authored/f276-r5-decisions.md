
## DECISION F276 D6 (2026-09-20, reviewer, round 5) — a staging copy is freed where its work is CONSUMED, not where its job finishes
CONTEXT: R-1003, registered in this round's first commit, measures what F276's own round 4 broke:
the release T003 put in `pingpong_job._finalize_job_workspace` runs inside `run_job`'s `finally` as
soon as a copy-mode job completes, and `job_apply.apply_job` reads that same directory as the SOLE
apply source for such a job. At `a112e1fa` `tests/orchestration/test_job_apply.py` reads
`19 failed, 69 passed`; at `92d4c38b`, the commit before the hook, `88 passed`; neutering the four
added lines at `a112e1fa` restores `88 passed`. Hosted CI on the merge base is green on every one
of those nodes, so the regression is this branch's alone. DECISION F276 D5 reasoned about the disk
and about the inspection window a FAILED job wants, and never asked what reads the directory of a
job that SUCCEEDS.
CHOSEN: (1) The terminal hook releases nothing. `_finalize_job_workspace`'s no-handle branch
returns exactly as it did before T003, and `_release_job_workspace_copy`, whose only call site that
was, is deleted rather than left uncalled. The asymmetry that justifies this is stated where the
branch is: the worktree path may delete a completed job's worktree because
`W.remove(handle, keep_branch=True)` keeps the work on a retained BRANCH, and a copy job has no
branch, so its staging copy is the deliverable and not scratch until something has taken it. (2)
`job_apply` releases it, after an apply whose status is exactly `applied` and whose final record
`_apply_from_workspace` has already persisted — the record first, the directory second, so a
failure between them can lose the copy or the record but never both, and the survivor is the one
that says the target was written. Every other outcome keeps the copy: a dry run, a blocked apply,
an unapproved apply, an `applied_*` variant that left the operator something to do, and a job
nobody ever applies. (3) What frees an unapplied copy is `data reclaim`, which already treats a
terminal job's staging copy as a candidate and, with `--orphans`, reaches the ones whose record is
gone. The lifecycle therefore closes in one of two places, both of them operator-visible, and
neither of them inside a `finally` the operator never sees. (4) The outcome is reported where a
person reads it: `JobApplyResult.staging_release` renders `released <n> bytes`, `already gone` or
`kept (<reason>)` in the applied summary, a refusal is logged as a warning with its reason, and a
raise is logged with its traceback. It is deliberately NOT added to `export_job_apply_json` or to
the durable record, because the record is written BEFORE the release by clause (2) and the key
could only ever persist empty; the field's docstring says so, so the absence reads as a decision.
(5) T003's acceptance line is amended in the feature file by an appended paragraph, never a
rewrite: "a job finishing in `isolation_mode=copy` releases its staging workspace" becomes "a job
whose work has been APPLIED releases its staging workspace, and a COMPLETED copy job that was never
applied still has it", each half with its own red proof.
ALTERNATIVES: keeping the hook and having `job_apply` materialise an apply source from evidence the
way `_materialize_apply_source_owned` does for worktrees, rejected as a far larger change that
would rebuild from a record what the filesystem already holds; gating the hook on an existing apply
record, rejected because at the moment a job completes it has never been applied, so the release
would be dead where it stands and alive only for a job applied before it finished, which is no
ordering at all; releasing on the whole `applied_*` family, rejected because each of those statuses
means the operator still has something to do or read and `applied_record_update_failed` means the
record this release follows was never written.
REVERSE: restore `packages/orchestration/pingpong_job.py`, `packages/orchestration/job_apply.py`,
`tests/orchestration/test_staging_lifecycle.py`, `tests/orchestration/test_job_apply.py`,
`docs/system/architecture.md` and `docs/roadmap/features/T2_F276.md` from `a112e1fa`, and delete
this paragraph.
