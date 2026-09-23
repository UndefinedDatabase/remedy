
DECISION F263 D5 (2026-09-23, round 5) — A GIT JOB ABSORBS A HUMAN CHANGE AT EVERY SAFE POINT
AND NO LONGER BLOCKS ON IT; ONLY A NON-GIT COPY JOB KEEPS THE FILE-WALK GUARD.

CONTEXT. T003 of T2_F263.md: the run detects a human change at a safe point, absorbs it through
T001 and T002's shared path, and continues, and the drift error for this case is DELETED rather
than kept as a fallback. Measured by the reviewer at `a2361d9a`: `run_job` in
`packages/orchestration/pingpong_job.py` hashes every target file into memory once per episode
and, for a git job and a copy job alike, blocks the job with `target_repo_mutated_during_job`
before a task's apply and with `target_repo_mutated_after_apply` after it. Its job-level safe
points are the one before any work, the one before each task and the one after each applied
task, and it hands `_stop_check` to `run_pingpong`, which calls it at the run's own safe points.
Every test that pins the drift error runs a job over a directory that is not a git repository.

CHOSEN. (1) For a job with a worktree — every git job — the two drift blocks are gone. The run
calls `human_change.absorb_job` at the episode start, before each task, at every safe point of
the task's own run, where the pre-apply guard stood, and after each applied task, so a hand edit
is certified and the job's last known state moves onto it while the job keeps running. (2) A
failure to absorb is never silent: the first one sticks, and the next job-level point blocks the
job with `human_change_absorb_failed at <point>: <reason>`; nothing in the repository is written
either way. (3) Every check is counted and timed into `job.metadata["human_change_checks"]` —
count, total seconds, slowest — which is where the Acceptance list's cost is measured. (4) A git
job made before F263 has no last known state; a run that resumes it records one first. (5) The
job's `target_guard` keeps its flags false for a git job: they now mean a change the run could
not take in, and such a change blocks the job instead. (6) A copy job over a non-git directory
keeps the file-walk guard and its drift block unchanged: without a tree it has no diff to
certify, and blocking is the "stop and say why" D-E allows. (7) `job apply` and `do run --apply`
are the next round's half of T003.

ALTERNATIVES. Absorb only at the job-level points — rejected: the Acceptance list asks for every
safe point of a run. Keep the drift block as a fallback when absorption fails — rejected: T003
deletes it, and a failed absorption already blocks with its own reason. Stop a job whose
absorption failed through the kill switch's stop request — rejected: that path records an
operator or budget stop, and this is neither.

REVERSE by deleting this paragraph and `tests/orchestration/test_human_change_in_run.py`, and
restoring `packages/orchestration/pingpong_job.py` from git history at `a2361d9a`.
