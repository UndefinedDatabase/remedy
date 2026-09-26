# Handback — F027 Task veto · Round 3

## Session

SESSION 1 of feature F027 · round 3 · rounds so far 3

Roughly two thirds of the session's context budget remained at the point this handback was
written. This round booked round 2's verdict, resolved R-1065 and registered/repaired R-1066,
recorded DECISION F027 D3, and completed T001: a task vetoed while its provider call runs finishes
that call and is then halted at the linear runner's next in-task safe point, folded with its
workspace restored, and the run continues to the next task; the cycle executor withholds a vetoed
task and its transitive dependents at every pick and ends `blocked` naming both sets when nothing
else is ready; and `worktrees.restore_tree` survives a directory standing where the tree holds a
file, converting every `OSError` of its own into a `WorktreeError`. New
`tests/orchestration/test_task_veto_cycles.py` and a grown `test_task_veto_runner.py`, with a
mutation tool proving all eleven mutations bite (m6 needed an added test, reported honestly below).

## Range

Review of cf6dc5462..HEAD

## Commits

### 801e7622e F027 R3 C1: copy round 3 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r3-block.md | +244/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f027-r3-plan.md | +33/-0 | copy of the plan.md payload |
| .agent/authored/f027-r3-records.diff | +70/-0 | copy of the records.diff payload |

347 insertions by `git show --numstat` — matches the block's stated expectation exactly (block
line count 244 plus 103), under the 500-line cap.

### 9779584cf F027 R3 C2: book round 2, resolve R-1065, register R-1066, record D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +48/-0 | DECISION F027 D3 appended, verbatim from records.diff |
| .agent/live_review.md | +6/-0 | round 2's Gate entry, R-1065's `Done:` paragraph and R-1066's registration appended |
| .agent/plan.md | +11/-15 | rewritten whole to the plan.md payload |

48/0 decisions.md, 6/0 live_review.md, 11/15 plan.md by `git show --numstat` — matches the block's
stated expectation exactly. `git apply --check` on records.diff → exit 0; the real `git apply` →
exit 0.

### 7d62737be F027 R3 C3: repair R-1066 in worktrees.restore_tree
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/worktrees.py | +39/-30 | S1: before writing back a file/symlink entry, a directory (or anything else) standing at that path is removed first; every `OSError` the function's own filesystem calls raise is re-raised as `WorktreeError` naming the path |
| tests/orchestration/test_worktrees.py | +33/-0 | two new tests: the file-to-directory restore, and an `OSError` converted to `WorktreeError` |

72 insertions by `git show --numstat` (39/30 + 33/0 = 72/30), under the 500-line cap.

### 79b5eea4d F027 R3 C4: veto an in-flight task and withhold vetoed tasks in the cycle executor
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +65/-1 | S2: `_VETO_REASON_PREFIX`/`_VETO_ERROR_REASON_PREFIX`/`_reason_is_veto`, and `_run_stop_check`'s in-task veto read after the stop and pause both answer None; S3: the `stopped` branch's veto-first halt, folding the veto, closing the task log `vetoed` and continuing, or blocking with `veto_fold_failed` when the control area no longer names the task |
| packages/orchestration/long_run_executor.py | +114/-4 | S4: `ready_tasks` gains `vetoed_ids` (seeded via new `_veto_seeds`, "not completed" not "pending"); `_TaskVetoErrorObserved`/`_vetoed_entries_or_raise`; `run_cycles` reads vetoed ids at the batch boundary and before every pick; the `all_remaining_work_vetoed` terminal; the `task_veto_control_error` except clause |

179 insertions by `git show --numstat`, under the 500-line cap.

### 08d58cb0b F027 R3 C5a: test the in-flight veto (part 1 of 3)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_veto_runner.py | +190/-0 | `_events` helper; `_SelfVetoingBuilder`/`TestInFlightVetoOfTheRunningTask` (copy job, diamond); `_WritesThenSelfVetoes`/`TestGitInFlightVetoRestoresTheWorkspace` (git job); `_BuildsThenCorruptsTheVetoArea`/`TestInFlightVetoControlAreaUnreadable` |

190 insertions by `git show --numstat`.

### a073b3c60 F027 R3 C5b: test the cycle executor's veto (part 2 of 3)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_veto_cycles.py | +217/-0 | NEW FILE: `ready_tasks` unit tests over the diamond (veto B withholds B and D; a veto of a completed task is inert); `run_cycles` integration tests — veto before the run (exact stop reason), a step vetoing another task mid-run, the only veto naming a completed task (green), the veto area unreadable |

217 insertions by `git show --numstat`.

### 251e2d26d F027 R3 C5c: the mutation tool for the in-flight and cycle-executor vetoes (part 3 of 3)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r3-mutations.py | +253/-0 | NEW: the G5 mutation tool, 11 mutations over `pingpong_job.py`, `long_run_executor.py` and `worktrees.py` |

253 insertions by `git show --numstat`. See Deviations: the block names C5 as one commit ("THE
TESTS AND THE MUTATION TOOL"), but the grown runner file (190) plus the new cycles file (217) plus
the mutation tool (253) sum to 660, over the 500-line cap, so it was split at file boundaries into
C5a/C5b/C5c.

### df9000235 F027 R3 C5d: catch m6 (ready_tasks withholds a vetoed seed but skips its dependents), found by the round's own red-proof sweep
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_veto_cycles.py | +26/-0 | one white-box test pinning that `ready_tasks` includes a vetoed seed in the `blocked_downstream` call, added after the FIRST run of the mutation tool measured m6 GREEN (see Deviations) |

26 insertions by `git show --numstat`.

## External actions

`git worktree add --detach .remedy-wt/f027-r3-mut 251e2d26d` — worktree created for the FIRST G5
sweep (m6 measured green, reported honestly, never papered over).
`git worktree remove --force .remedy-wt/f027-r3-mut` — removed after that sweep.
`git worktree add --detach .remedy-wt/f027-r3-mut df9000235` — recreated at the new last code
commit after C5d.
`python3 -B .agent/authored/f027-r3-mutations.py .remedy-wt/f027-r3-mut` — run twice (once per
worktree above); the second run caught all eleven mutations.
`git worktree remove --force .remedy-wt/f027-r3-mut` — removed after the second sweep completed.
`git worktree prune` — no-op both times (nothing stale).
`git push -u origin feature/f027-task-veto` — outcome reported in the final reply, since C5/C6
cannot contain it.
No PR created, no merge, no branch checkout/deletion, no force-push, no stash — none of these ran.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory` (absent, as
  required).
- `pwd` → `/home/decodeux/Repos/remedy`; `git status --porcelain` → empty; `git branch
  --show-current` → `feature/f027-task-veto`; `git log --oneline -1` → `cf6dc5462 F027 R2 C6:
  rewrite handoff for round 2`. All three matched.
- Block bytes: measured line count 244, sha256
  `5d95d7ed1c8597789a763612b671e5813a4de01355b2364cd623879a363b7e09` — both matched the delegation
  message's two readings exactly.
- `git worktree list` reported as found (the pre-round listing: the primary checkout plus the
  `f015-*`, `f020-*`, `f023-*`, `f024-*`, `f025-*`, `f027-r1-dry`, `f027-r2-dry`, `f027-r3-dry`,
  `f284-*` and `job-*` worktrees — unchanged by this round until the two G5 worktrees were added
  and removed).

PAYLOADS (measured against the block's table, both matched):
| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 33 | 1256 | c75da9842f99142ba9031bc04063f9434bbacc15938b4d7cd32cd27623a182cc |
| records.diff | 70 | 12143 | 64a471ee1cf66b8a672291ed58326d892a72f2058f5cbb806d173cf7a0a6cddd |

`git apply --check` on records.diff → `REAL_EXIT=0`. The real `git apply` → `REAL_EXIT=0`.

G1 TRANSPORT — each `.agent/authored/f027-r3-*` copy compared byte for byte against its source,
read back with `git show 801e7622e:<path>`:
- `f027-r3-block.md` == `.remedy-wt/f027-r3/block.md`: equal=True
- `f027-r3-plan.md` == payload plan.md: equal=True
- `f027-r3-records.diff` == payload records.diff: equal=True

G2 THE RECORDS — each file's sha256, read with `git show 9779584cf:<path>`, against the reviewer's
table:
| path | bytes | sha256 | match |
|---|---|---|---|
| .agent/live_review.md | 300067 | 269de06879d723de4bbe89cea4b57b4c6cbc709715bd3217f97a8fdfce5acc36 | True |
| .agent/decisions.md | 2166498 | e63c10eb87613715f57c1560a4c0d8497ec98a6464d396531601d2c3fcd9066b | True |
| .agent/plan.md | 1256 | c75da9842f99142ba9031bc04063f9434bbacc15938b4d7cd32cd27623a182cc | True |

Open finding ids via `open_finding_ids` (scripts/rotate_live_review.py) over the ledger's text at
9779584cf: `['R-1066']` — matches the reviewer's reading exactly. The ledger's last line begins
`- R-1066 — ` (confirmed verbatim, `startswith` check True).

G3 THE CODE:
```
$ python3 -m ruff check .agent/authored/f027-r3-mutations.py packages/orchestration/worktrees.py packages/orchestration/pingpong_job.py packages/orchestration/long_run_executor.py tests/orchestration/test_worktrees.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_task_veto_cycles.py
All checks passed!
REAL_EXIT=0
```
(run at the last code commit, df9000235 — re-run after C5d, unchanged from the reading at 251e2d26d)

`git diff --stat 9779584cf 7d62737be`:
```
 packages/orchestration/worktrees.py   | 69 ++++++++++++++++++++---------------
 tests/orchestration/test_worktrees.py | 33 +++++++++++++++++
 2 files changed, 72 insertions(+), 30 deletions(-)
```
Names `worktrees.py` and `test_worktrees.py` alone — confirmed.

G4 THE TESTS — serial run in the primary checkout at the last code commit (df9000235), real exit
code:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_veto_runner.py tests/orchestration/test_task_veto_cycles.py tests/orchestration/test_task_veto.py tests/orchestration/test_worktrees.py tests/orchestration/test_long_run_executor.py tests/orchestration/test_pause_resume_cycles.py tests/orchestration/test_escalation.py tests/orchestration/test_self_healing_cycles.py tests/orchestration/test_resume_kill.py tests/orchestration/test_checkpoints.py tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_mission_e2e.py tests/orchestration/test_run_report_hook.py tests/orchestration/test_pause_resume.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_job_worktree_integration.py tests/orchestration/test_run_manifest_zero_call_expectations.py tests/orchestration/test_task_expectation_status_truth.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_event_names.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/cli/test_golden_path.py
1056 passed in 131.01s (0:02:11)
REAL_EXIT=0
```
No `SKIPPED` line was printed by `-rs` anywhere in this selection — zero skips.

`--collect-only -q` on each new/grown file:
- `tests/orchestration/test_task_veto_runner.py`: 13 tests collected (3 new: `TestInFlightVetoOfTheRunningTask`, `TestGitInFlightVetoRestoresTheWorkspace`, `TestInFlightVetoControlAreaUnreadable`)
- `tests/orchestration/test_task_veto_cycles.py`: 7 tests collected (NEW file, all 7 new)
- `tests/orchestration/test_worktrees.py`: 43 tests collected (2 new)
- `tests/cli/test_golden_path.py`: 42 tests collected (outside the reviewer's selection entirely)

Accounting for the difference from the reviewer's `1002 passed`: the reviewer ran the same file
list WITHOUT `test_task_veto_cycles.py` and `tests/cli/test_golden_path.py`, inside its own
authoring tree — which does not carry my own test authorship for S1–S4 (the block only pins the
production code's shape, not the worker's test count). `1002 + 3 (new runner tests) + 2 (new
worktrees tests) + 7 (new cycles file) + 42 (golden path) = 1056` — matches the measured total
exactly.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [...six "pass" entries...], "fail_count": 0, "ok": true, "passed": true, ...}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0 (run after the tree was clean, i.e. after C5d).

G5 THE RED PROOFS — FIRST sweep, `git worktree add --detach .remedy-wt/f027-r3-mut 251e2d26d`
(exit 0), then `python3 -B .agent/authored/f027-r3-mutations.py .remedy-wt/f027-r3-mut`:
```
--- control run (unmutated, before) ---
control: exit=0
62 passed in 11.65s
m1 _run_stop_check never reads a veto: exit=1 failed=3 ... — CAUGHT
m2 the stopped branch lets a veto halt fall through to the stop path: exit=1 failed=3 ... — CAUGHT
m3 the halt sets TASK_VETOED itself instead of calling the fold, so nothing is restored: exit=1 failed=2 ... — CAUGHT
m4 the halt returns the job instead of continuing the loop: exit=1 failed=2 ... — CAUGHT
m5 ready_tasks ignores vetoed_ids: exit=1 failed=3 ... — CAUGHT
m6 ready_tasks withholds the vetoed seeds but not their dependents: exit=0 failed=0 failing_node_ids=[] — GREEN, NOT CAUGHT
m7 the cycle executor's veto terminal branch is removed: exit=1 failed=2 ... — CAUGHT
m8 the cycle executor swallows a TaskVetoError and picks on: exit=1 failed=1 ... — CAUGHT
m9 ready_tasks seeds a vetoed task that is completed: exit=1 failed=2 ... — CAUGHT
m10 restore_tree removes nothing standing where the tree holds a file: exit=1 failed=1 ... — CAUGHT
m11 restore_tree lets an OSError escape unconverted: exit=1 failed=1 ... — CAUGHT
--- control run (unmutated, after) ---
control: exit=0
62 passed in 9.53s
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: False
```
REAL_EXIT=1. m6 was GREEN — reported here honestly rather than papered over. Every mutation's
`restored byte-identical: True`. Per the block's own instruction ("you then add the test that
catches it before C6 and re-run the tool"), commit C5d added
`TestReadyTasksVetoedIds::test_a_vetoed_seed_joins_the_downstream_computation`, a white-box test
that spies on `long_run_executor.blocked_downstream` and asserts a vetoed seed is included in its
call — necessary because a vetoed task's transitive dependent is ALREADY unready by
`dag_schedule.ready_set`'s own completion requirement regardless of `blocked_downstream` (verified
directly: `ready_tasks(job, 10)` with only A completed returns `[B, C]` and never `D`, with or
without any withholding), so the black-box ready-list alone cannot distinguish "seed reached
`blocked_downstream`" from "seed did not."

`git worktree remove --force .remedy-wt/f027-r3-mut` (exit 0), `git worktree prune` (exit 0).

SECOND sweep, after C5d: `git worktree add --detach .remedy-wt/f027-r3-mut df9000235` (exit 0),
then `python3 -B .agent/authored/f027-r3-mutations.py .remedy-wt/f027-r3-mut`:
```
--- control run (unmutated, before) ---
control: exit=0
63 passed in 11.53s
m1 _run_stop_check never reads a veto: exit=1 failed=3 failing_node_ids=[...3 ids...]
restored byte-identical: True
m2 the stopped branch lets a veto halt fall through to the stop path: exit=1 failed=3 failing_node_ids=[...3 ids...]
restored byte-identical: True
m3 the halt sets TASK_VETOED itself instead of calling the fold, so nothing is restored: exit=1 failed=2 failing_node_ids=[...2 ids...]
restored byte-identical: True
m4 the halt returns the job instead of continuing the loop: exit=1 failed=2 failing_node_ids=[...2 ids...]
restored byte-identical: True
m5 ready_tasks ignores vetoed_ids: exit=1 failed=4 failing_node_ids=[...4 ids...]
restored byte-identical: True
m6 ready_tasks withholds the vetoed seeds but not their dependents: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_task_veto_cycles.py::TestReadyTasksVetoedIds::test_a_vetoed_seed_joins_the_downstream_computation']
restored byte-identical: True
m7 the cycle executor's veto terminal branch is removed: exit=1 failed=2 failing_node_ids=[...2 ids...]
restored byte-identical: True
m8 the cycle executor swallows a TaskVetoError and picks on: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_task_veto_cycles.py::TestUnreadableVetoArea::test_blocks_with_task_veto_control_error_and_zero_task_steps']
restored byte-identical: True
m9 ready_tasks seeds a vetoed task that is completed: exit=1 failed=2 failing_node_ids=[...2 ids...]
restored byte-identical: True
m10 restore_tree removes nothing standing where the tree holds a file: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_worktrees.py::TestRestoreTree::test_restore_replaces_a_directory_standing_where_the_tree_holds_a_file']
restored byte-identical: True
m11 restore_tree lets an OSError escape unconverted: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_worktrees.py::TestRestoreTree::test_restore_converts_an_oserror_to_worktree_error_naming_the_path']
restored byte-identical: True
--- control run (unmutated, after) ---
control: exit=0
63 passed in 9.35s
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
REAL_EXIT=0. Every one of the 11 mutations was red with at least one failing node; none stayed
green; every restoration was byte-identical.

`git worktree remove --force .remedy-wt/f027-r3-mut` → exit 0. `git worktree prune` → exit 0.
`git worktree list` afterward: the primary checkout plus exactly the worktrees constraint 6 named
at step 4 (`f015-*`, `f020-*`, `f023-*`, `f024-*`, `f025-*`, `f027-r1-dry`, `f027-r2-dry`,
`f027-r3-dry`, `f284-*` and the `job-*` worktrees) — nothing else.

CONSTRAINT 3 — round path set: `git diff --name-only cf6dc5462` (before C6) named exactly:
`.agent/authored/f027-r3-block.md`, `.agent/authored/f027-r3-mutations.py`,
`.agent/authored/f027-r3-plan.md`, `.agent/authored/f027-r3-records.diff`, `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/long_run_executor.py`,
`packages/orchestration/pingpong_job.py`, `packages/orchestration/worktrees.py`,
`tests/orchestration/test_task_veto_cycles.py`, `tests/orchestration/test_task_veto_runner.py`,
`tests/orchestration/test_worktrees.py` — the block's whole named set, nothing extra (this file,
`.agent/handoff.md`, is added by C6 itself). None of the forbidden paths (`task_veto.py`,
`pause_control.py`, `safe_points.py`, `dag_schedule.py`, `pingpong_loop.py`, `run_manifest.py`,
`ui_server.py`, `apps/`, `docs/`, `.agent/context.md`, `.agent/prose_slips.md`,
`.agent/candidates.md`, `.agent/operator_questions.md`) were touched.

G6 TREE AND PUSH — real readings reported in the final reply (this file cannot contain them, since
they are measured AFTER this commit).

## Authored-text proofs

Every `.agent/authored/f027-r3-*` copy was compared disk-to-disk against its committed source and
matched byte for byte (see G1 above): the block copy, the plan payload copy and the records.diff
payload copy. `f027-r3-mutations.py` is the worker's own tool, not a reviewer-authored payload — no
fidelity proof applies to it.

## Deviations & assumptions

1. C5 was split into C5a, C5b, C5c and C5d. The block names C5 as one commit ("THE TESTS AND THE
   MUTATION TOOL"), but the grown runner file (190 insertions), the new cycles file (217) and the
   mutation tool (253) together reach 660 — well over the 500-line cap — so the split ran at file
   boundaries: C5a (the grown `test_task_veto_runner.py`), C5b (the new
   `test_task_veto_cycles.py`), C5c (the mutation tool). C5d is an ADDITIONAL commit beyond the
   block's named set (see item 2).
2. G5's FIRST sweep (at 251e2d26d) measured mutation m6 GREEN — `ready_tasks` ignoring
   `vetoed_ids` when computing `blocked_downstream`'s seed set produced no observable difference in
   the diamond, because a vetoed task's transitive dependent is ALREADY excluded from
   `dag_schedule.ready_set`'s own output by its ordinary "every dependency must be COMPLETED" rule,
   independent of `blocked_downstream` — verified directly with a probe script (reported in G5
   above). Per the block's own instruction ("a green one is reported as green, never papered over,
   and you then add the test that catches it before C6 and re-run the tool"), C5d added a
   white-box test spying on `long_run_executor.blocked_downstream` to pin that a vetoed seed
   reaches it, mirroring exactly how the paused/blocked seeds are already proven to join it. The
   second sweep, run after C5d, caught all eleven mutations.
3. `_VETO_REASON_PREFIX` (`"task_veto: "`) and `_VETO_ERROR_REASON_PREFIX`
   (`"task_veto_control_error: "`) are choices the block leaves open (it names only their role, not
   their literal text); the error prefix's text matches the string `_fold_task_vetoes` already
   writes to `job.error` on the same control-read failure, so the two routes read consistently.
4. S3's "block the job" branch (the control area no longer names the task after the fold) sets
   `task.status = TASK_BLOCKED` and `task.error`/`job.error` to the exact ordered string
   `veto_fold_failed: task <task id> halted for a veto the control area no longer holds` — the
   block specifies the message text but not whether the task's own status field changes;
   `TASK_BLOCKED` was chosen for consistency with every other block path in `run_job` (each sets
   `task.status = TASK_BLOCKED` alongside `job.state = JOB_BLOCKED`), leaving no task stuck at
   `running` in a blocked job. This branch is unreached by any of this round's tests (it requires
   the veto entry to vanish from the control area between the in-task read and the fold, a race the
   block does not ask a test to construct) and is reported here as an intentional, untested gap
   consistent with the block's own test list.
5. No other deviation from the block's ordered commit sequence, specification or constraints.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5a | deviated | C5 split into C5a/C5b/C5c/C5d — see Deviations 1 |
| C5b | deviated | see C5a |
| C5c | deviated | see C5a |
| C5d | deviated | additional commit catching m6, found by this round's own G5 sweep — see Deviations 2 |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOFS | done | m6 measured green on the first sweep, repaired, second sweep all-caught — see Deviations 2 |
| G6 TREE AND PUSH | done | reported in the final reply, not this file, per the block |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 3, then T002: the replan
proposal in the decision inbox with its two-option menu and both options' documented effects. Open
findings: 1 (R-1066, landed this round and awaiting the reviewer's resolution). Operator questions:
5.
