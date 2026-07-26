# Handoff — F047 Checkpoint & resume, Round 1 (Setup + T001 + T002)

Branch: feature/f047-checkpoint-resume · PR #153 (draft)
Base: main @ 89c4ef0e723f89c58956de3964d1653461d273b9 (MAIN_HEAD)
Review range: 89c4ef0..fd93b31 · Open findings: 0 · Next: T003 kill test

## Item status

| Item | Status | Reason |
|------|--------|--------|
| [0] Open PR Gate + setup | done | |
| [0]g inspection notes | done | all four parts exist; decisions.md |
| [1] T001 checkpoints.py | done | |
| [2] T002 resume CLI | deviated | name collision, see below |
| T003 | not in scope | separate round per the order |

**Deviation (T002):** `remedy job resume` ALREADY EXISTED — an event-replay
resume with a required `--checkpoint <id>`. A second catalog entry with the
same `command_id` produced a silent duplicate (get_command returned the new
entry, the dispatch dict kept the old handler). Resolved by extending the
existing command instead of shadowing it: `--checkpoint` is now optional,
given → old path unchanged, absent → F047 path. Omitting it used to be an
argparse error, so no existing invocation changes behavior. Recorded in
decisions.md; both branches are pinned by tests.

## External actions taken

| Action | Detail |
|--------|--------|
| Merged PR #152 | `gh pr merge 152 --merge --delete-branch` (F046 closure) |
| Pushed branch | `git push -u origin feature/f047-checkpoint-resume`, then `git push` |
| Created PR #153 | draft, base main — https://github.com/UndefinedDatabase/remedy/pull/153 |

## Commits this round

**0987211** chore(f047): claim F047 — branch, STATUS, state files, inspection notes

| File | +/- |
|------|-----|
| .agent/decisions.md | +38 / −0 |
| .agent/live_review.md | +6 / −49 |
| .agent/plan.md | +19 / −17 |
| docs/roadmap/STATUS.md | +1 / −1 |

**c708ef0** feat(f047): checkpoint record — writer, loader, hashing, retention (T001)

| File | +/- |
|------|-----|
| packages/orchestration/checkpoints.py | +454 / −0 (new) |
| packages/orchestration/config.py | +12 / −0 |
| .agent/decisions.md | +21 / −0 |

**bfbb503** feat(f047): write a checkpoint at the cycle boundary (T001)

| File | +/- |
|------|-----|
| packages/orchestration/long_run_executor.py | +47 / −1 |

**f9dc6cd** test(f047): checkpoint chain, corruption matrix, retention, wiring (T001)

| File | +/- |
|------|-----|
| tests/orchestration/test_checkpoints.py | +390 / −0 (new) |
| .agent/plan.md | +5 / −3 |

**98f71f8** feat(f047): resume a job from its newest valid cycle checkpoint (T002)

| File | +/- |
|------|-----|
| apps/cli/commands/job.py | +154 / −5 |
| packages/orchestration/checkpoints.py | +23 / −0 |
| packages/orchestration/worktrees.py | +17 / −0 |
| apps/cli/command_catalog.py | +11 / −3 |
| .agent/decisions.md | +20 / −0 |

**fd93b31** test(f047): resume decisions before the hand-off (T002)

| File | +/- |
|------|-----|
| tests/orchestration/test_resume_cli.py | +392 / −0 (new) |
| .agent/plan.md | +9 / −5 |

## Inspection notes ([0]g) — decisions.md "F047 inspection notes"

1. Atomic write reused: `storage._atomic_write_job` (temp + fsync + os.replace).
   No new atomic writer. F046's `write_cycle_record` uses plain `write_text`;
   checkpoints deliberately do not copy that.
2. Cycle-boundary hook: `long_run_executor.run_cycles` step 5, after
   `save_fn(job)` and `write_cycle_record` — a checkpoint references the
   persisted snapshot, so the snapshot must already be on disk.
3. Evidence area: `pingpong_job.job_evidence_dir(id)/checkpoints/`, sibling
   of F046's `cycles/`.
4. Consumed on resume: `safe_points.stop_requested` / `consume_stop`, and
   `flight_plan.flight_plan_blocks_execution` (same check `job run` makes).
   Live head via new read-only `worktrees.head_at`; recorded head from the
   F006 job plan (`packages.core.models.Job` has no worktree field).

## Verification (raw)

    $ python3 -m pytest tests/orchestration/test_checkpoints.py -q
    35 passed in 0.21s                                        exit 0

    $ python3 -m pytest tests/orchestration/test_resume_cli.py -q
    25 passed in 0.20s                                        exit 0

    $ python3 -m pytest tests/cli/test_golden_path.py -q      # canary
    42 passed in 18.75s                                       exit 0

    $ python3 -m pytest tests/orchestration/test_long_run_executor.py -q
    49 passed in 0.26s                                        exit 0   # F046 regression

    $ ruff check packages/orchestration/{checkpoints,long_run_executor,config,worktrees}.py \
        apps/cli/commands/job.py apps/cli/command_catalog.py \
        tests/orchestration/test_{checkpoints,resume_cli}.py
    All checks passed!                                        exit 0

Pre-existing red, NOT F047-attributable — proven by stashing the branch and
re-running on the clean base: `-k "command_catalog or catalog or
command_discovery"` gives the IDENTICAL 14 failures with and without this
branch (job.budget's `read_metadata` action_class, `--task-scoped` help text
tripping the `sk-` scanner, missing `docs/resume.md`).

## Notes for the reviewer

- DEFAULT behavior unchanged: `CYCLE_SAFETY_CAP` stays 1; the checkpoint
  write is the only new work at a cycle boundary and it cannot raise.
- No evidence bundle / review zip was built this round (closure artifact).
- Docs deferred to closure: `remedy job resume` gained a second mode;
  `docs/resume.md` does not exist and its two tests are red on main.
