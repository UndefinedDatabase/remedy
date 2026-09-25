# Handback — F025 Pause/resume (global & per node) · Round 3

## Session

SESSION 1 of feature F025 · round 3 · rounds so far 3

Roughly a third of the context budget remained at the point this handback was written; the round
repaired two findings (R-1049, R-1050), then designed and built the pause for the cycle executor
from scratch (E1–E7) with a ten-row test file and an 11-mutation red-proof tool. Two dead ends:
G5's first mutation run left m3 green (fixed in C6b, re-run clean), and a real product gap surfaced
while writing c5 (a stop must supersede a pending pause in the cycle executor too, fixed in C4b).

## Range

Review of 312b9512f..HEAD

## Commits

### 33472dadd F025 R3 C1: book round 2's FAIL, register R-1049 and R-1050, copy round 3 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r3-block.md | +212/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f025-r3-ledger.md | +6/-0 | copy of the ledger.md payload |
| .agent/authored/f025-r3-plan.md | +35/-0 | copy of the plan.md payload |
| .agent/authored/f025-r3-slip.txt | +1/-0 | copy of the slip.txt payload |
| .agent/live_review.md | +6/-0 | ledger.md appended (bytes to bytes) |
| .agent/plan.md | +11/-12 | rewritten whole to the plan.md payload |
| .agent/prose_slips.md | +1/-0 | slip.txt appended (bytes to bytes) |

272 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 212, plus 60) — matches exactly.

### 034c78d3d F025 R3 C2: catch only the pause errors a stop's settle raises (R-1049)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +15/-6 | `_stop_job`'s pause-settle-on-stop catch narrowed from blind `except Exception: # noqa: BLE001` to `except (_pc.PauseControlError, StopControlError) as exc:`, logging a warning naming the job and the error instead of passing; `StopControlError` added to the existing local `safe_points` import |

15 insertions, well under the 500-line cap. `python3 -m pytest tests/test_ble001_ratchet.py` now
reads 3 passed (was 1 failed at `312b9512`).

### de4013790 F025 R3 C3: record a pause event that fails and keep its request pending (R-1050)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +96/-46 | `_append_job_paused_event`/`_append_job_resumed_event` now return whether the write landed and record the failure (`job.pause["event_error"]`, `job.metadata["pause_event_error"]`) instead of swallowing it; the S3 park (steps 2–5) and S5 lift are factored out of `_park_job`/`_lift_job_pause` into shared, importable `park_job_pause`/`lift_job_pause` (E1) that take the persist step as an argument; `_park_job` becomes a thin wrapper (in-flight task rollback, then `park_job_pause(..., persist=_persist_job, ...)`, `_persist_job` referenced by name so a monkeypatch of it is still honored) |
| tests/orchestration/test_pause_resume.py | +103/-0 | three new test classes: R-1049's settle-inside-a-served-stop test, and R-1050's two event-failure tests (`job_paused` re-parks/re-settles/clears `event_error`; `job_resumed` records `pause_event_error` and the run still completes) |

199 insertions, under the 500-line cap.

### a6ded43f7 F025 R3 C4: pause the cycle executor at its safe points and in its ready set
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/long_run_executor.py | +373/-160 | E2: `TERMINAL_PAUSED_BY_OPERATOR` mapped to `JOB_PAUSED`/`RunState.PAUSED`, absent from `REPORTED_TERMINALS`; a job pause read after `_should_stop` at the loop's own safe point and before every task pick inside a cycle, parked through E1's shared `park_job_pause`; E3: `ready_tasks` gains `paused_ids` (PENDING-filtered before it becomes a withholding seed — D1 clause 4's inert rule), `paused_task_ids_for`/`paused_downstream_tasks` helpers, `CycleRecord` gains `paused_task_ids`/`paused_downstream_task_ids`; E4: the relaunch (job.state PAUSED, non-empty pause) stays parked when a job pause is pending or the mask withholds every otherwise-ready task, else lifts through E1 and continues; E5: `_PauseControlErrorObserved` unwinds a `PauseControlError` at any pause read straight to `blocked`, no further task step |
| packages/orchestration/run_report.py | +4/-1 | E6: `recommended_next_action` treats `paused_by_operator` exactly like `stopped_by_operator` (same next-action text) |

373 insertions in the executor file alone; both files together 377, under the 500-line cap.

### 3f2d00efd F025 R3 C4b: supersede a pending job pause when a stop wins in the cycle executor
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/long_run_executor.py | +27/-0 | `_supersede_pending_job_pause_on_stop`, called at both places the loop ends on a stop (the main safe point and the between-repair-rounds stop) — mirrors `pingpong_job._stop_job`'s own "a stop always wins" handling, written with R-1049's narrow catch from the start rather than a blind one |

27 insertions. See Deviations #1 for why this was split from C4.

### 3f5fc7f6e F025 R3 C5: test the pause on the cycle executor
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_pause_resume_cycles.py | +387/-0 | NEW FILE — one test class per row c1–c10 of the block's semantics table, reusing `test_long_run_executor.py`'s fixtures and fakes (`FakeClock`, `FakeProvider`, `SteeredStep`, `make_diamond_job`, `make_job`, `control_root`, `isolate_data_root`, …) exactly as `test_pause_resume.py` reuses `test_job_stop_integration.py`'s |

387 insertions, under the 500-line cap.

### d4d277c4e F025 R3 C6: add the mutation tool for round 3
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r3-mutations.py | +261/-0 | the G5 tool: m1–m8 edit `packages/orchestration/long_run_executor.py`, m9–m11 edit `packages/orchestration/pingpong_job.py`, inside one worktree, against both new/updated test files |

261 insertions, under the 500-line cap.

### e101b931b F025 R3 C6b: retarget m3 to the observable withholding it proves
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r3-mutations.py | +16/-10 | m3 retargeted from `ready_tasks`'s internal downstream computation (dispatch-unobservable — see Deviations #2) to `paused_downstream_tasks`, the function the CycleRecord and the E1 park's `withheld_task_ids` both actually read |

16 insertions. See Deviations #2.

### (this commit) F025 R3 C7: rewrite handoff for round 3
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f025-r3-mut d4d277c4e` (C6's HEAD) — succeeded, for G5's
  first run.
- `git worktree remove --force .remedy-wt/f025-r3-mut` — succeeded, after the first G5 run found
  m3 green.
- `git worktree add --detach .remedy-wt/f025-r3-mut e101b931b` (C6b's HEAD) — succeeded, for G5's
  second, clean run.
- `git worktree remove --force .remedy-wt/f025-r3-mut` — succeeded; `git worktree prune` —
  succeeded (no-op); `git worktree list` afterward shows only the primary checkout and the
  pre-existing worktrees named in constraint 5 — nothing new left behind.
- `git push origin feature/f025-pause-resume` — runs immediately after this commit (C7); its real
  outcome is reported in the final reply, since the handoff commit precedes the push.

No `gh pr create`, no `gh pr merge`, no other `gh` command this round (constraint 4: nothing is
merged). No `git stash`, no force-push, no checkout of another branch.

## Verification

```
$ ls .agent/STOP; echo "REAL_EXIT=$?"
ls: cannot access '.agent/STOP': No such file or directory
REAL_EXIT=2
(absent, as required — checked before step one)
```

```
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f025-pause-resume
$ git log --oneline -1
312b9512f F025 R2 C6: rewrite handoff for round 2
```

```
$ (line count and sha256 of .remedy-wt/f025-r3/block.md, measured)
line_count: 212
sha256: dbd10b49da8a9321fd56048afd72205d7a4fc66cc3b5df8d428b6f49b0d52e03
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list   (as found, before this round touched anything)
```
Listed the primary checkout at `feature/f025-pause-resume`/`312b9512f`, every `f015-*`/`f020-*`/
`f023-*`/`f024-*`/`f025-*`/`f284-*` round worktree already on disk (including `f025-r1-dry`,
`f025-r2-sim`, `f025-r3-sim`), and four `job-*` worktrees — all left untouched all round.

### PAYLOADS table
```
$ (python: newline count, byte count, sha256 of each payload)
ledger.md  lines=6  bytes=5390 sha256=05c8f31ef429dee4c5d6d9ad0ff83ea22c1e797eadad9c6c003d6d2256e8303b
plan.md    lines=35 bytes=1415 sha256=6c812aff48496b1a336e75d730db1ecd057b979ba34d4e05b936df90e39360af
slip.txt   lines=1  bytes=329  sha256=2cf3c7e78b4d4213a359200b63e5833f530cf192d6854c71eebbe69846018f29
```
All 3 match the PAYLOADS table exactly (G1).

### G1 — transport
```
$ (python: each committed .agent/authored/f025-r3-* copy, read via `git show <C1>:<path>`,
   compared byte for byte against its source)
.agent/authored/f025-r3-block.md  == .remedy-wt/f025-r3/block.md  : True
.agent/authored/f025-r3-ledger.md == .remedy-wt/f025-r3/ledger.md : True
.agent/authored/f025-r3-plan.md   == .remedy-wt/f025-r3/plan.md   : True
.agent/authored/f025-r3-slip.txt  == .remedy-wt/f025-r3/slip.txt  : True
```
```
$ (bytes comparison: C1's .agent/live_review.md vs 312b9512's bytes + ledger.md)
live_review match:  True
$ (bytes comparison: C1's .agent/prose_slips.md vs 312b9512's bytes + slip.txt)
prose_slips match:  True
$ (bytes comparison: C1's .agent/plan.md vs plan.md payload)
plan match:  True
```
```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over C1's .agent/live_review.md
['R-1008', 'R-1049', 'R-1050']
```
Matches the block's stated reading exactly.

### G2 — the code
```
$ python3 -m ruff check packages/orchestration/long_run_executor.py \
  packages/orchestration/pingpong_job.py packages/orchestration/run_report.py \
  tests/orchestration/test_pause_resume.py tests/orchestration/test_pause_resume_cycles.py \
  .agent/authored/f025-r3-mutations.py
All checks passed!
```
```
$ git diff --stat 312b9512 HEAD -- packages/orchestration/safe_points.py \
  packages/orchestration/pingpong_loop.py packages/orchestration/checkpoints.py \
  packages/orchestration/escalation.py packages/orchestration/dag_schedule.py \
  packages/common/secure_fs.py
(empty)
```
Confirmed empty — none of the six forbidden files touched.
```
$ git diff 312b9512 HEAD -- packages apps scripts | grep -c "^+.*noqa: BLE001"
0
```
```
$ git diff --name-only C1 HEAD
.agent/authored/f025-r3-mutations.py
packages/orchestration/long_run_executor.py
packages/orchestration/pingpong_job.py
packages/orchestration/run_report.py
tests/orchestration/test_pause_resume.py
tests/orchestration/test_pause_resume_cycles.py
```
Every path is inside constraint 3's set. `packages/orchestration/pause_control.py` was NOT
touched this round — every S2–S5/E1–E5 read of it already existed with the exact signature the
executor needed.

### G3 — the new tests, serially
```
$ python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_pause_resume_cycles.py \
  tests/orchestration/test_pause_resume.py tests/orchestration/test_pause_control.py \
  tests/test_ble001_ratchet.py
.............................................................            [100%]
61 passed in 4.25s
REAL_EXIT=0
```
```
$ python3 -m pytest --collect-only -q tests/orchestration/test_pause_resume_cycles.py
10 tests collected
$ python3 -m pytest --collect-only -q tests/orchestration/test_pause_resume.py
18 tests collected
$ python3 -m pytest --collect-only -q tests/orchestration/test_pause_control.py
30 tests collected
$ python3 -m pytest --collect-only -q tests/test_ble001_ratchet.py
3 tests collected
```
10 + 18 + 30 + 3 = 61, matching the summary line exactly.

### G4 — the neighbours
```
$ python3 .remedy-wt/f025-r3/run_sel.py /home/decodeux/Repos/remedy 8
files 154 exit 0 wall 89 s
6109 passed, 9 skipped in 89.02s (0:01:29)
```
0 failed at C6b (the block's own gate requirement); the 9 skips are the pre-existing D3/D12/opt-in
quarantines, unrelated to this round. (6105 passed at `312b9512` + the 1 previously-red
`test_ble001_ratchet` node R-1049 fixed + the 3 new R-1049/R-1050 tests in
`test_pause_resume.py`, which is IN this selection = 6109 — arithmetic checks.) No node failed, so
no serial re-run was needed.
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=157"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict FAIL"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0. (`live_review_verdict` correctly reads the round 2 FAIL
this round's own C1 just booked — that verdict does not flip until the reviewer writes round 3's.)

### G5 — the red proofs
First run, worktree at C6's HEAD `d4d277c4e`:
```
$ git worktree add --detach .remedy-wt/f025-r3-mut d4d277c4e
$ python3 -B .agent/authored/f025-r3-mutations.py .../f025-r3-mut
control (before): exit=0 failed=0
m1, m2, m4..m11: each exit=1, failed>=1, with failing node ids (caught)
m3: ready_tasks withholds the paused seeds but not their dependents -- exit=0 failed=0
  failing_node_ids=[(none)]           <-- GREEN, reported as green, not papered over
m3: restored byte-identical: True
control (after): exit=0 failed=0
packages/orchestration/long_run_executor.py: restored byte-identical: True
packages/orchestration/pingpong_job.py: restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: False
$ git worktree remove --force .remedy-wt/f025-r3-mut
```
WHY m3 stayed green: mutating `ready_tasks`'s OWN downstream-propagation seeds has no
dispatch-observable effect — a genuine DAG dependent of a still-pending (never-completed) paused
seed is ALREADY excluded from `dag_ready_set` by the plain dependency-completion check alone,
mask or no mask (the same redundancy the pre-existing `blocked_ids`/`awaiting_ids` downstream
propagation already has). C6b retargets the mutation at `paused_downstream_tasks`, the function
the CycleRecord and the E1 park's `withheld_task_ids` both actually read — which IS what c3
observes — and the tool was re-run from a fresh worktree at the new HEAD:
```
$ git worktree add --detach .remedy-wt/f025-r3-mut e101b931b
$ python3 -B .agent/authored/f025-r3-mutations.py .../f025-r3-mut
control (before): unmutated control run -- exit=0 failed=0 failing_node_ids=[(none)]
m1: the executor reads (and acts on) the job pause before _should_stop -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume_cycles.py::TestC5AStopAndAJobPauseBothPending::test_the_stop_wins_and_the_pause_is_superseded]
m1: restored byte-identical: True (packages/orchestration/long_run_executor.py)
m2: ready_tasks ignores paused_ids -- exit=1 failed=4 failing_node_ids=[tests/orchestration/test_pause_resume_cycles.py::TestC3TheDiamondWithBPaused::test_a_and_c_run_d_is_withheld_and_the_park_names_b, tests/orchestration/test_pause_resume_cycles.py::TestC4AfterReleaseTheRelaunchResumes::test_writes_one_job_resumed_runs_b_then_d_and_ends_all_green, tests/orchestration/test_pause_resume_cycles.py::TestC6AnAwaitingBranchBesideAPausedBranch::test_ends_with_the_awaiting_terminal_and_names_both, tests/orchestration/test_pause_resume_cycles.py::TestC9ARelaunchWhileStillPaused::test_stays_parked_with_zero_steps_and_no_new_event]
m2: restored byte-identical: True (packages/orchestration/long_run_executor.py)
m3: ready_tasks withholds the paused seeds but not their dependents -- exit=1 failed=2 failing_node_ids=[tests/orchestration/test_pause_resume_cycles.py::TestC3TheDiamondWithBPaused::test_a_and_c_run_d_is_withheld_and_the_park_names_b, tests/orchestration/test_pause_resume_cycles.py::TestC6AnAwaitingBranchBesideAPausedBranch::test_ends_with_the_awaiting_terminal_and_names_both]
m3: restored byte-identical: True (packages/orchestration/long_run_executor.py)
m4: paused_by_operator is added to REPORTED_TERMINALS -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume_cycles.py::TestC10PausedByOperatorWritesNoFinalReport::test_write_final_report_is_never_called]
m4: restored byte-identical: True (packages/orchestration/long_run_executor.py)
m5: the relaunch runs while the mask still withholds every pending task -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume_cycles.py::TestC9ARelaunchWhileStillPaused::test_stays_parked_with_zero_steps_and_no_new_event]
m5: restored byte-identical: True (packages/orchestration/long_run_executor.py)
m6: the relaunch never lifts the pause -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume_cycles.py::TestC4AfterReleaseTheRelaunchResumes::test_writes_one_job_resumed_runs_b_then_d_and_ends_all_green]
m6: restored byte-identical: True (packages/orchestration/long_run_executor.py)
m7: the job pause is not read before a task pick inside a cycle -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume_cycles.py::TestC2AJobPauseDuringTheFirstTaskStep::test_the_running_step_finishes_and_task_two_is_never_picked]
m7: restored byte-identical: True (packages/orchestration/long_run_executor.py)
m8: a PauseControlError in the executor is swallowed and the task step runs -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume_cycles.py::TestC7ACorruptPausedTasksEntry::test_blocks_with_pause_control_error_and_zero_task_steps]
m8: restored byte-identical: True (packages/orchestration/long_run_executor.py)
m9: the park settles a job-scope request although the job_paused write failed -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestR1050AFailedPausedEventReparksAndClearsTheError::test_the_next_run_writes_one_job_paused_and_clears_event_error]
m9: restored byte-identical: True (packages/orchestration/pingpong_job.py)
m10: the park drops event_error instead of recording it -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestR1050AFailedPausedEventReparksAndClearsTheError::test_the_next_run_writes_one_job_paused_and_clears_event_error]
m10: restored byte-identical: True (packages/orchestration/pingpong_job.py)
m11: a settle raising PauseControlError inside a served stop propagates out of the stop -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestR1049APauseSettleFailureInsideAServedStopStillStops::test_a_pause_control_error_from_the_settle_does_not_block_the_stop]
m11: restored byte-identical: True (packages/orchestration/pingpong_job.py)
control (after): unmutated control run -- exit=0 failed=0 failing_node_ids=[(none)]
packages/orchestration/long_run_executor.py: restored byte-identical: True
packages/orchestration/pingpong_job.py: restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
$ git worktree remove --force .remedy-wt/f025-r3-mut
$ git worktree prune
$ git worktree list
(primary + the pre-existing set only; f025-r3-mut gone)
```
Every one of the 11 mutations is now red with at least one failing node id; every restore is
byte-identical for both target files; the tool's own final line reads `True`.

### G6 — tree and push (readings go in the final reply, after C7)

## Authored-text proofs

`.agent/authored/f025-r3-block.md`, `f025-r3-ledger.md`, `f025-r3-plan.md` and `f025-r3-slip.txt`
were built with `shutil.copyfile` from the reviewer's payload files — never retyped, never edited
— and G1 compared every one byte for byte, read back with `git show <C1>:<path>`, against its
source: all four BYTE-IDENTICAL. `.agent/live_review.md` and `.agent/prose_slips.md` were appended
with raw bytes read from `ledger.md`/`slip.txt` (`open(..., "ab").write(...)`), never retyped;
`.agent/plan.md` was rewritten whole from `plan.md`'s bytes (`shutil.copyfile`). G1's
byte-comparisons confirm all three match the payloads exactly. `packages/orchestration/pingpong_job.py`,
`packages/orchestration/long_run_executor.py`, `packages/orchestration/run_report.py`,
`tests/orchestration/test_pause_resume.py`, `tests/orchestration/test_pause_resume_cycles.py` and
`.agent/authored/f025-r3-mutations.py` are WORKER-authored production code, tests and the G5 tool
per the block's E1–E7 specification and the two findings' FIX clauses — not reviewer payloads —
so no authored-text proof applies to them.

## Deviations & assumptions

1. **Extra commit C4b.** Writing c5's test (a stop and a job pause both pending) surfaced a real
   product gap: nothing in the cycle executor's stop path settled a pending job-scope pause as
   `superseded_by_stop` the way `pingpong_job._stop_job` already does for the linear runner —
   `_should_stop` firing simply left the pause file sitting there. C4b adds
   `_supersede_pending_job_pause_on_stop`, called at both places the loop ends on a stop, written
   with R-1049's narrow catch (`PauseControlError`/`StopControlError`, logged not swallowed) from
   the start rather than inventing a matching blind-except defect. Not named in the block's
   C1–C6 sequence; recorded here per the "extra commit is a deviation even when correct" rule.
2. **Extra commit C6b.** G5's first run (worktree at C6's HEAD) found mutation m3 green — mutating
   `ready_tasks`'s own downstream-seed computation has no dispatch-observable effect, because a
   true DAG dependent of a still-pending paused seed is already excluded from `dag_ready_set` by
   the plain dependency-completion check alone (the same redundancy the pre-existing
   `blocked_ids`/`awaiting_ids` downstream propagation already carries — this is not a defect in
   E3, just an unobservable mutation target). Per the block's own G5 clause ("a mutation that
   stays green... the catching test is added in a further commit before C7, and the tool
   re-run"), C6b retargets m3 at `paused_downstream_tasks` — the function the CycleRecord and the
   E1 park's `withheld_task_ids` both actually read, which c3 DOES observe. No test was missing;
   the mutation itself was aimed at a redundant computation. G5's second run, from a fresh
   worktree at C6b's HEAD, caught all 11 mutations and reported `True`.
3. **E6 consumers checked, most needed no change.** `TERMINAL_JOB_STATUS`/`REPORTED_TERMINALS` are
   the defining site (C4). `render_cycle_summary_line` renders a single `CycleRecord`, never
   branches on a terminal-status string, and needed no change. `apps/cli/commands/job.py`'s
   `remedy job resume` output (`_cmd_job_run_cycles`'s print line and its
   `if result.terminal_status not in ("all_green", "max_cycles_reached"): sys.exit(1)`) and its
   `_report_section`'s `mode = MODE_FINAL if terminal in REPORTED_TERMINALS else MODE_INTERIM`
   already treat any terminal outside that allow-list/set generically — `paused_by_operator`
   already exits 1 and already renders interim, with zero code change, purely because it is
   absent from `REPORTED_TERMINALS`. `packages/orchestration/run_report.py`'s
   `recommended_next_action` DID need a change (C4): its `terminal == "stopped_by_operator"` check
   widened to `terminal in {"stopped_by_operator", "paused_by_operator"}`. The mission loop
   (`packages/orchestration/orchestrator_loop.py`)'s `_resumable()` checks `evidence.job_state ==
   "paused"` — since `TERMINAL_RUN_STATE[TERMINAL_PAUSED_BY_OPERATOR] = RunState.PAUSED`, exactly
   the same core state every other resumable terminal (`stopped_by_operator`, `budget_exhausted`,
   `deadline_reached`, `blocked`) already writes, a `paused_by_operator` job is already resumable
   with zero code change there too. Grepped the repository for every other literal
   `"stopped_by_operator"`/`"budget_exhausted"`/`"deadline_reached"` occurrence outside
   `long_run_executor.py`/`run_report.py`; none branches on the executor's own terminal vocabulary
   (the `budget_exhausted:*` matches elsewhere are `safe_points.should_stop`'s own, unrelated,
   reason-string vocabulary, and several of those files are in constraint 3's forbidden set
   regardless).
4. **No full-suite run.** Per constraint 6 (amend0917-throughput), only G4's targeted selection
   ran; the one full-suite run per feature belongs to F025's closure, not this round.
5. **No existing test file widened.** Constraint 3 names this as a possible category; none was
   needed this round beyond the two new test files and the already-listed production/test paths.
6. **`packages/orchestration/pause_control.py` untouched.** The block allowed "small helpers
   only, named in the handback" there; none were needed — every read the executor makes
   (`pause_requested`, `paused_tasks`) already existed from round 1 with the exact signature
   needed, wrapped by this round's own `_job_pause_or_raise`/`_paused_entries_or_raise` in
   `long_run_executor.py`.

No payload was edited or retyped. No production file outside
`packages/orchestration/pingpong_job.py`, `packages/orchestration/long_run_executor.py` and
`packages/orchestration/run_report.py` was touched; `safe_points.py`, `pingpong_loop.py`,
`checkpoints.py`, `escalation.py`, `dag_schedule.py` and `secure_fs.py` are confirmed untouched by
G2's `git diff --stat`. The worktree `.remedy-wt/f025-r3-mut` this round created (twice, for G5's
two runs) was removed both times, per constraint 5; every pre-existing worktree and stash was left
alone.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 272 insertions, matches the block's expectation (212+60) exactly |
| C2 | done | 15 insertions; R-1049's FIX landed; the BLE001 ratchet is green again |
| C3 | done | 199 insertions; R-1050's FIX and E1's shared park/lift functions landed with their tests |
| C4 | done | 377 insertions across the executor and run_report.py; E1–E6 landed |
| C4b | deviated | extra commit for a real product gap c5's own test surfaced; see Deviations #1 |
| C5 | done | 387 insertions; one test class per row c1–c10 |
| C6 | done | 261 insertions; the mutation tool, m1–m11 |
| C6b | deviated | extra commit fixing a mutation G5 found green; see Deviations #2 |
| C7 | done | this handback |
| G1 | done | all payload and copy identity checks byte-identical; open-finding set matched |
| G2 | done | ruff clean over every changed .py file; forbidden files untouched; noqa:BLE001 added = 0; name-only diff exactly inside constraint 3 |
| G3 | done | 61 passed (10+18+30+3), exit 0 |
| G4 | done | 6109 passed, 9 skipped, exit 0, 0 failed; integrity check 6/6 pass |
| G5 | deviated | first run found m3 green (reported as green, not papered over); fixed in C6b; second run caught all 11, `True` |
| G6 | done | reported in the final reply, after C7 and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 3. Then T002: the channel
commands with their audit, the CLI verbs and live fake-job tests of both scopes. Open findings: 3,
the C1 reading (`R-1008`, owned by F285; `R-1049` and `R-1050`, repaired this round and awaiting
the reviewer's close). Operator questions open: 3.
