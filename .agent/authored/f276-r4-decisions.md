
## DECISION F276 D5 (2026-09-20, reviewer, round 4) — the copy's release is two layers, the ignore pass is guarded by the target's own `.git`, and the size ceiling is a backstop measured at 16 MiB
CONTEXT: T003 of `docs/roadmap/features/T2_F276.md` orders `release_staging_workspace(job_id)`
"called from the same terminal-state hook the worktree cleanup already uses", a `.gitignore`-aware
copy filter and a per-file size ceiling. A research helper prototyped it at `543863a0`; the
reviewer re-applied it, re-ran the gates and re-proved three of its mutations. Measuring first
showed the feature file's sentence describes a hook that has no terminal-state predicate:
`pingpong_job._finalize_job_workspace`, the "ONE cleanup path for a job-owned worktree", keys on
`job.state == JOB_COMPLETED and not job.result_diff_error` and deliberately RETAINS a failed,
cancelled, blocked, paused or stopped worktree, while T002's `job_is_terminal` reads
`COMPLETED|FAILED|CANCELLED`. It also showed that `discard_staging`, which the feature file's
Why-this-exists says the copy path never calls, does not exist at all at `543863a0` — F273's
R-0936 paydown deleted it — so this slice supplies a cleanup that was never built rather than
repairing one that broke.
CHOSEN: (1) TWO LAYERS, so the two vocabularies do not have to be reconciled. The public
`release_staging_workspace` refuses on its own authority through `job_state_refusal`, the same
predicate `data reclaim` uses, because a function that deletes must never free what reclaim would
refuse. The HOOK is stricter: it calls the release only under the literal condition
`_finalize_job_workspace` already applies to a worktree, so a copy job that did not complete keeps
its staging copy exactly as such a worktree job keeps its worktree, and `data reclaim` offers it to
the operator later. That makes the feature file's sentence true of both the hook and its predicate.
(2) The structural rules are REUSED, not re-spelled: `data_reclaim._deletion_refusal` and
`_job_state` become public as `child_deletion_refusal` and `job_state_refusal`, and
`_JOB_KEYED_PREFIXES` imports `staging_workspace.STAGING_DIR_PREFIX`, so the module that mints the
directory name and the command that reads it cannot drift. (3) The ignore pass runs only when the
TARGET holds its own `.git`, which is load-bearing rather than a convenience: a target nested
inside another repository answers `git check-ignore` successfully with the OUTER repository's
rules, and the helper's hand run demonstrated that an unguarded pass drops a file the outer
`.gitignore` happens to name. One subprocess for the whole candidate list, pinned by a test that
counts the calls; a `.git` FILE, as a git worktree checkout carries, counts deliberately. (4) The
ceiling is `MAX_COPY_FILE_BYTES = 16 * 1024 * 1024`, a BACKSTOP behind the ignore pass rather than
the main filter, measured on this repository at `543863a0`: two files at or above 5 MiB hold 86.4
per cent of the untracked-and-tracked tree and both are gitignored artifacts, no tracked file of
5358 reaches 5 MiB, and the largest tracked file is `.agent/live_review_archive.md` at 4284047
bytes and append-only — so a 5 MiB ceiling would sit at 82 per cent of a file this workflow grows
every round, while 16 MiB is 3.9 times it and still 4 to 26 times under the artifacts the backstop
exists for. (5) `StagingWorkspace` records `excluded_ignored`, `excluded_oversize` and
`excluded_bytes`, the last being the bytes of exactly those two lists and of no other, because a
skipped directory is never walked and a total over all five exclusion lists would be a number no
caller could interpret; `gitignore_filter` carries one of three matched tokens so a copy that ran
unfiltered says so instead of looking like a copy with nothing to ignore. (6) Both new silences
speak through the module logger `pingpong_job` already uses — what a copy excluded, and a release
that failed inside `run_job`'s `finally` — and NOT through the run-log event stream, because an
event name there is a product-vocabulary decision with a `humanizeCatalog.ts` entry behind it.
(7) The cleanup condition is now spelled twice inside `_finalize_job_workspace`. Extracting a
shared predicate would edit the worktree path the feature file's Do-not-touch protects, so the
duplication is deliberate and the drift is covered behaviourally instead: a parametrised test keeps
every non-completing state, and a mutation widening the hook to `job_is_terminal` reddens exactly
the two states where the vocabularies differ.
ALTERNATIVES: one predicate for hook and function, rejected under (1) because it would either
strand failed copies against reclaim's reading or delete what the worktree path retains; deciding
"is this a git repository" by running `check-ignore` and reading its exit code, rejected under (3)
with a demonstration; a 5 MiB ceiling as the feature file's sample suggests, rejected under (4);
a `JobPlan` field or a new run-log event for the two silences, rejected under (6) as a slice of its
own that changes a persisted shape or a published vocabulary.
REVERSE: restore `packages/orchestration/staging_workspace.py`,
`packages/orchestration/data_reclaim.py`, `packages/orchestration/pingpong_job.py` and
`docs/system/architecture.md` from `543863a0`, delete
`tests/orchestration/test_staging_lifecycle.py` and the T003 amendment paragraph this decision
appended to `docs/roadmap/features/T2_F276.md`, and delete this paragraph.
