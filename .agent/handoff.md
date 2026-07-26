# Handoff — F047 Checkpoint & resume, Round 2 (R-0146 repair + T003)

Branch: feature/f047-checkpoint-resume · PR #153 (draft, description updated)
Base: main @ 89c4ef0e723f89c58956de3964d1653461d273b9
Review range this round: `fd93b31..7539442` · Feature range: `89c4ef0..7539442`
Open findings: 0 (R-0146 fixed) · Next expected action: reviewer verdict, then
the integration gate.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| [A] persist R-0146 | done | own commit 269195f, first action |
| [B] fix R-0146 | done | b3cea6e; `Done: R-0146` in the same commit |
| [C] T003 kill test | done | 7539442, plus a forced production fix in 2fe5887 |

**In-scope addition (not asked for, but T003 could not pass without it):**
the kill test's exactly-once assertion came out short (3 of 5 tasks) and the
cause was a production defect, not a test artifact — see commit 2fe5887 below.
Both parts recorded in decisions.md.

## External actions taken

| Action | Detail |
|--------|--------|
| Pushed branch | `git push` → `864f945..7539442` |
| Updated PR #153 | `gh pr edit 153 --title --body` (scope now T001–T003 + R-0146) |

## Commits this round

**269195f** chore(f047): persist finding R-0146

| File | +/- |
|------|-----|
| .agent/live_review.md | +13 / −1 |

**b3cea6e** fix(f047): --dry-run is a read-only resume preview (R-0146)

| File | +/- |
|------|-----|
| apps/cli/commands/job.py | +121 / −1 |
| tests/orchestration/test_resume_cli.py | +142 / −1 |
| .agent/live_review.md | +6 / −0 |

`_cmd_job_resume` takes `dry_run`; the dispatch passes it in the
no-checkpoint branch too. The preview observes the stop request via
`stop_requested` and NEVER `consume_stop`, reports the head comparison
(naming both heads on drift, without the exit-3 refusal), the gate state and
the checkpoint / no-checkpoint / all-green state, then exits 0 without
touching the executor. JSON mirrors it under `action=preview`.

**2fe5887** fix(f047): cycle numbering is per job, and evidence names the tasks it ran

| File | +/- |
|------|-----|
| packages/orchestration/long_run_executor.py | +45 / −1 |
| tests/orchestration/test_checkpoints.py | +30 / −0 |
| .agent/decisions.md | +33 / −0 |
| .agent/plan.md | +10 / −9 |

1. `run_cycles` numbered cycles `len(cycles) + 1` **within one invocation**,
   so the resumed run started at 1 again and wrote `cycle_0001.json` /
   `checkpoint_0001.json` over the killed run's records — the pre-kill
   history was silently destroyed. `next_cycle_index(job_id)` now reads the
   highest index already persisted in BOTH evidence areas and the loop starts
   one past it; `first_cycle_index` is a test seam. `max_cycles` still bounds
   one invocation, and a fresh job still starts at 1 (F046 default unmoved).
2. `CycleRecord.executed_task_ids` — nothing on disk previously named WHICH
   tasks a cycle ran. Records executions, not successes.

**7539442** test(f047): kill -9 mid-cycle, resume, exactly-once (T003)

| File | +/- |
|------|-----|
| tests/orchestration/test_resume_kill.py | +358 / −0 (new) |

## Verification (raw)

    $ python3 -m pytest tests/orchestration/test_resume_cli.py -q     # gate for [B]
    35 passed in 0.23s                                                exit 0

    $ ruff check apps/cli/commands/job.py tests/orchestration/test_resume_cli.py
    All checks passed!                                                exit 0

    $ python3 -m pytest tests/orchestration/test_resume_kill.py -q
    7 passed in 1.32s                                                 exit 0

    $ python3 -m pytest tests/orchestration/test_resume_cli.py \
          tests/orchestration/test_checkpoints.py -q
    72 passed in 0.35s                                                exit 0

    $ python3 -m pytest tests/orchestration/test_long_run_executor.py -q   # F046
    49 passed in 0.27s                                                exit 0

    $ ruff check tests/orchestration/test_resume_kill.py \
          tests/orchestration/test_checkpoints.py \
          tests/orchestration/test_resume_cli.py \
          packages/orchestration/long_run_executor.py apps/cli/commands/job.py
    All checks passed!                                                exit 0

    $ python3 -m pytest tests/cli/test_golden_path.py -q              # canary
    42 passed in 18.79s                                               exit 0

Kill test, named:

    tests/orchestration/test_resume_kill.py::TestKillAndResume::
      test_the_kill_leaves_checkpoints_for_the_committed_cycles      PASSED
      test_the_in_flight_task_was_never_recorded_as_executed         PASSED
      test_resume_completes_the_job_with_each_task_executed_exactly_once PASSED
      test_the_f047_resume_path_accepts_the_killed_job               PASSED
      test_the_dry_run_preview_of_a_killed_job_runs_nothing          PASSED
    tests/orchestration/test_resume_kill.py::TestTornCheckpoint::
      test_resume_falls_back_to_the_previous_valid_checkpoint        PASSED
      test_a_torn_newest_still_completes_the_job_exactly_once        PASSED
    7 passed in 1.32s

## Exactly-once evidence (same scenario run standalone, raw)

    child returncode         : -9 (-9 == SIGKILL)
    in-flight task at kill   : {'cycle': 3, 'task_id': '747b3c3d-f7b8-473e-9145-80554a7de243'}
    executed ids BEFORE kill : ['ddcef197-9292-45dd-a530-4ea04a46197a',
                                'ba72e311-eb1f-433f-a588-7f80dd9e63d5']
    resume exit              : 0 {"terminal_status": "all_green", "cycles_run": 3,
                                  "job_id": "7bdd37de-da14-439f-9bdb-66f52d2af4df"}
    executed ids AFTER resume:
       1. ddcef197-9292-45dd-a530-4ea04a46197a
       2. ba72e311-eb1f-433f-a588-7f80dd9e63d5
       3. 747b3c3d-f7b8-473e-9145-80554a7de243   <- the in-flight task, run ONCE
       4. dea5b71d-deef-4011-9aa1-d19fe7c647a7
       5. 11f43465-3829-46d2-bf61-7716cfc81001
    duplicates               : NONE
    total executions         : 5 for 5 tasks
    pre-kill work redone     : NO
    cycle record files       : cycle_0001..cycle_0005.json
    checkpoint files         : checkpoint_0001..checkpoint_0005.json

Read from `evidence/cycles/*.json` (`executed_task_ids`) — durable state
written by BOTH processes, not a counter in the test process.

## Notes for the reviewer

- The kill is a real `SIGKILL` to a real child; the parent asserts
  `returncode == -signal.SIGKILL`, so a child that merely exited would fail.
- Synchronisation is a marker file polled by the parent; no `sleep` is used
  as a synchronisation device.
- The torn checkpoint is written explicitly rather than raced for: the atomic
  write makes a half-written file impossible to produce on demand, so racing
  the rename would only generate flakes. The property under test — the loader
  falls back to the previous valid checkpoint — is identical either way.
  Reasoning recorded in decisions.md and in the test class docstring.
- In `test_the_f047_resume_path_accepts_the_killed_job` only the executor
  hand-off is stubbed; every F047 check (checkpoint load, stop request, head,
  gate) runs for real. The production executor binds a live provider.
- Runtime 1.32s for the whole file — no slow/integration marker needed.
- Pre-existing red, unchanged from round 1 and NOT F047-attributable (proven
  by stashing the branch): the 14 `command_catalog`/`command_discovery`
  failures (`job.budget` action_class, `--task-scoped` tripping the `sk-`
  scanner, missing `docs/resume.md`).
- No evidence bundle / review zip built (closure artifact). Docs deferred to
  closure: `remedy job resume` gained two behaviors this feature.
