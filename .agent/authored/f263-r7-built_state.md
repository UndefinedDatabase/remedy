
## Built State

A git job records the target checkout's last known state when its workspace is created: the
tree object `worktrees.write_tree_at` takes through a private index, untracked files included,
with the commit `HEAD` names and the time, kept alive by a checkpoint ref named
`target-last-known` that the end of a job does not drop (DECISION F263 D1). A human change is
the difference between that tree and the current one, classified by the run guard's own rules,
so tool noise and Remedy's own artifacts never count as the human's. It is certified as a
sealed record, `jobs/<id>/evidence/human_changes/hcr-<before>-<after>.json` beside its `.diff`,
the diff written first and both checked by `verify_human_change_record`; `absorb` writes the
record and only then calls the re-base, so a re-base that fails leaves the record and the hand
edit in place. All of it lives in `packages/orchestration/human_change.py` and is tested in
`tests/orchestration/test_human_change.py`, whose
`test_a_failed_rebase_leaves_the_record_and_the_hand_edit` is the fixture the Acceptance list
names.

The record is evidence like any other (DECISION F263 D2): the job's evidence export copies every
record and its diff into the bundle, verifies the copies, and writes
`human_change_integrity.json`; the final verifier reports `human_change_integrity_blocked`, a
record that does not verify makes the package BLOCKED, and the review manifest requires the file
for READY. Tested in `tests/orchestration/test_human_change_evidence.py`. `.agent/authored/` left
the lint's reach, because its files are transport records that are never edited after they land
(DECISION F263 D3).

`remedy absorb` (DECISION F263 D4) absorbs the repository's current state into every job of
that repository that has not failed or been cancelled, leaves a job whose worktree lock a live
process holds untouched, and re-bases by moving the job's last known state to the tree the human
left; it writes no file in the repository. It lives in `apps/cli/commands/absorb_cmd.py`, sits
in the help after `runtime`, and is tested in `tests/cli/test_absorb_cmd.py`.

A git job absorbs at every safe point of its run (DECISION F263 D5): at the episode start,
before each task, at each safe point of the task's own run, before and after each applied task.
The two drift errors are deleted for git jobs; a failed absorption blocks the job and names the
point and the reason. A copy job over a directory that is not a git repository has no tree to
certify and keeps the file-walk guard, which stops and says why. Every check is counted and
timed into the job record's `human_change_checks` — count, total seconds and slowest — and the
closure's self-use job, the first real job run with absorption, carries the reading this
feature's evidence reports. The demo case is
`test_a_hand_edit_during_a_job_is_absorbed_and_the_job_completes` in
`tests/orchestration/test_human_change_in_run.py`.

Every apply absorbs first (DECISION F263 D6): `job apply`, `do run --apply` and every commit
flag reach `apply_job`, which absorbs before a single file is copied, refuses if the absorption
fails, and no longer refuses on the old drift flag. A hand edit to a file the job changed too is
never overwritten and never discarded: the apply stops and names it as
`human_change_conflict`. The second demo case, a hand edit between the run's end and the apply,
is `test_a_hand_edit_after_the_run_is_absorbed_and_kept_by_the_apply` in
`tests/orchestration/test_human_change_at_apply.py`, beside the refusals for a conflicting edit.

The explicit command, the run's safe points and the apply are one implementation:
`tests/orchestration/test_human_change_one_path.py` reads every tracked module under `packages/`
and `apps/` and holds that `absorb` is called from `absorb_job` alone and that `absorb_job` is
called from exactly those three places.

This feature added two modules, `packages/orchestration/human_change.py` and
`apps/cli/commands/absorb_cmd.py`, and one line for each to
`tests/orchestration/import_reachability_allowlist.txt`, because each is reachable from the
command catalog (closure precondition 7). It added nothing to `ALLOWED_UNWIRED`. Its test
files are `tests/orchestration/test_human_change.py`,
`tests/orchestration/test_human_change_evidence.py`, `tests/cli/test_absorb_cmd.py`,
`tests/orchestration/test_human_change_in_run.py`,
`tests/orchestration/test_human_change_at_apply.py` and the guard above.

The reviewer checklist was left unedited at this feature's closure: F263 wrote no line into
`.agent/prose_slips.md`, so its one consolidation pass had no lesson to fold and the list keeps
its length.
