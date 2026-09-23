
DECISION F263 D4 (2026-09-23, round 4) — `remedy absorb` ABSORBS INTO EVERY UNFINISHED JOB OF
THE REPOSITORY IT RUNS IN, LEAVES A RUNNING JOB TO ITS OWN RUNNER, AND RE-BASES BY MOVING THE
JOB'S LAST KNOWN STATE, THROUGH THE ONE PATH THE RUN WILL USE.

CONTEXT. T002 of T2_F263.md orders the explicit command over T001's machinery, with its catalog
entry and help text; DECISION F259 D1 names it `absorb`, and DECISION amend0911-feedback D1
reserves its help slot after `runtime`. Measured by the reviewer at `d5fe145f`: jobs are scoped
elsewhere by project id, never by repository path, and a job's worktree lock is the only sign
that a runner holds it, with no helper that asks whether it is held. `job apply` leaves an
applied job `completed`, so no state tells an applied job from one that still waits.

CHOSEN. (1) `human_change.absorb_job` is the one implementation: it measures the job's last
known state, certifies the change through `absorb`, and re-bases by moving the job's
`target-last-known` checkpoint ref and its `target_last_known` to the tree the human left, then
persisting the job. No file in the repository is written. A job with no last known state is
skipped, not failed. T003 calls the same function from the run's safe points. (2) The command
selects every persisted job whose `repo_path` resolves to the repository it runs in, whose state
is neither `failed` nor `cancelled`, and — with `--job` — whose id is the one named; `completed`
jobs stay in, because a hand edit before `job apply` is exactly the second demo case. (3) A job
whose worktree lock a live process holds is reported `skipped_running` and not touched: a
second writer of its record would lose the runner's next save; `worktrees.lock_is_held` asks the
lock without keeping it. (4) The group `absorb` is visible, in the help slot after `runtime`,
and a bare `remedy absorb` runs `absorb run`, like `init` and `status`. The command answers
`--json` with one row per job, its status, its record name and its files; it exits 0 when it
ran, 1 outside a git repository, for an unknown `--job` or when a job cannot be absorbed, and 2
on usage — the floor, so no exit-code table row is owed.

ALTERNATIVES. Scope by project, as `job list` does — rejected: a hand edit happens in one
repository, and a project may hold several. Absorb into a running job too — rejected: the
runner rewrites the whole record at its next save and would drop the re-base; T003's safe
points are where a running job absorbs. Skip `completed` jobs — rejected: that is the job a
hand edit before `job apply` must reach.

REVERSE by deleting this paragraph, `apps/cli/commands/absorb_cmd.py`,
`tests/cli/test_absorb_cmd.py` and the module's allowlist line, removing `absorb_job` and
`JobAbsorbOutcome` from `packages/orchestration/human_change.py`, `lock_is_held` from
`packages/orchestration/worktrees.py`, the `absorb` group, entry and help slot from
`apps/cli/command_catalog.py`, its two entries in `apps/cli/grouped.py`, its import in
`apps/cli/commands/__init__.py`, and restoring the three pinned tests from git history at
`d5fe145f`.
