# Handback — F027 Task veto · Round 2

## Session

SESSION 1 of feature F027 · round 2 · rounds so far 2

The large majority of the session's context budget remained at the point this handback was
written. This round booked round 1's verdict, registered and repaired R-1065, recorded DECISION
F027 D2, and landed the rest of T001 on the linear runner: `run_job` now folds a veto before its
task loop and at every pre-task safe point, returns a vetoed attempt's job workspace to its start
tree via a new `worktrees.restore_tree`, never dispatches the unreachable set, sends a block's
skipped tasks back to pending unless they are unreachable, ends a run whose remaining work is all
vetoed or unreachable `blocked` naming both sets, and the run manifest accepts `vetoed` — with a
new `tests/orchestration/test_task_veto_runner.py` and a mutation tool proving all fourteen
mutations bite.

## Range

Review of 25ab44dec..HEAD

## Commits

### 4b2856072 F027 R2 C1: copy round 2 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r2-block.md | +277/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f027-r2-plan.md | +37/-0 | copy of the plan.md payload |
| .agent/authored/f027-r2-records.diff | +89/-0 | copy of the records.diff payload |

403 insertions by `git show --numstat` — matches the block's stated expectation exactly (block
line count 277 plus 126), under the 500-line cap.

### 843249805 F027 R2 C2: book round 1, register R-1065, record D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +69/-0 | DECISION F027 D2 appended, verbatim from records.diff |
| .agent/live_review.md | +4/-0 | round 1's Gate entry and R-1065's registration appended |
| .agent/plan.md | +11/-11 | rewritten whole to the plan.md payload |

69/0 decisions.md, 4/0 live_review.md, 11/11 plan.md by `git show --numstat` — matches the block's
stated expectation exactly. `git apply --check` on records.diff → exit 0; the real `git apply` →
exit 0.

### 61250e1e7 F027 R2 C3: repair R-1065 and add worktrees.restore_tree
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/task_veto.py | +47/-15 | S1: both `task_already_vetoed` routes now share one refused shape via new `_already_vetoed_refusal`, which repairs the entry's missing event first; `veto_refusal`'s detail now says "the task is already vetoed" rather than naming the status |
| packages/orchestration/worktrees.py | +69/-0 | S2: NEW `restore_tree(handle, tree) -> list[str]` |
| tests/orchestration/test_task_veto.py | +41/-1 | new tests: the gate route's own repair, a vetoed-status-with-no-entry edge, the retry test's shape updated to the new refused/request_id contract |
| tests/orchestration/test_worktrees.py | +132/-0 | NEW `TestRestoreTree`: modified/added/deleted/executable/symlink paths, a nested directory left empty, the submodule refusal and the equality check |

289 insertions by `git show --numstat` (no expectation was stated for C3; reported as measured),
under the 500-line cap.

### 636e9c69e F027 R2 C4: fold a veto in the linear runner
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +146/-0 | S3 `_fold_task_vetoes` (module-level helper), its two call sites (before the loop, and at the pre-task safe point after the stop/pause check), S4's `TASK_VETOED` pass-over and unreachable-skip, S5's terminal before the `all_done` reading |
| packages/orchestration/run_manifest.py | +12/-6 | S6: `"vetoed"` joins `VALID_TASK_STATUSES` and the four `_TASK_EXPECTATION_ALLOWED_STATUSES` sets; a vetoed task with no run is `EXPECT_SKIPPED` |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | S7: `packages.orchestration.task_veto` added in sorted place |
| tests/orchestration/test_task_expectation_status_truth.py | +5/-5 | S6: `_ALLOWED` gains the same four entries; the vocabulary test gains `PJ.TASK_VETOED` |
| tests/test_no_orphan_modules.py | +0/-3 | S7: the `ALLOWED_UNWIRED` entry for `task_veto.py` removed — it now has a production importer |

164 insertions by `git show --numstat`, under the 500-line cap. `git diff -U0 61250e1e7 636e9c69e --
tests/orchestration/test_task_expectation_status_truth.py tests/test_no_orphan_modules.py
tests/orchestration/import_reachability_allowlist.txt` holds exactly S6's and S7's lines (see G3
below for the whole diff).

### 1ff1f5c30 F027 R2 C5a: test the runner's fold of a veto (part 1 of 3)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_veto_runner.py | +279/-0 | NEW (part 1 of 3): fixtures, fakes, the diamond-veto-before-the-run test, every-task-vetoed, the legacy job-file test, the during-the-run veto test |

279 insertions by `git show --numstat`.

### f49f1b792 F027 R2 C5b: test the runner's fold of a veto (part 2 of 3)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_veto_runner.py | +272/-0 | REST (part 2 of 3): the block-then-veto-then-relaunch test, a direct unit test of the fold's skip-reset rule, the task-cap/paused-manifest test, the inert-veto test, the corrupt-veto-file test, the git-worktree restore test |

272 insertions by `git show --numstat`.

### 0739f3162 F027 R2 C5c: test the runner's fold of a veto (part 3 of 3)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f027-r2-mutations.py | +280/-0 | NEW: the G5 mutation tool, 14 mutations over `pingpong_job.py`, `worktrees.py`, `run_manifest.py` and `task_veto.py` |

280 insertions by `git show --numstat`. See Deviations: the block names C5 as one commit
("THE RUNNER TESTS AND THE MUTATION TOOL"), but the test file alone (551 insertions) already
exceeds the 500-line cap, so it was split at class boundaries into C5a/C5b/C5c.

## External actions

`git worktree add --detach .remedy-wt/f027-r2-mut 0739f3162` — worktree created for the G5 mutation
sweep.
`git worktree remove --force .remedy-wt/f027-r2-mut` — removed after the sweep completed.
`git worktree prune` — no-op (nothing stale).
`git push -u origin feature/f027-task-veto` — outcome reported in the final reply, since C5/C6
cannot contain it.
No PR created, no merge, no branch checkout/deletion, no force-push, no stash — none of these ran.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, `REAL_EXIT=2`
  (absent, as required).
- `pwd` → `/home/decodeux/Repos/remedy`; `git status --porcelain` → empty; `git branch
  --show-current` → `feature/f027-task-veto`; `git log --oneline -1` → `25ab44dec F027 R1 C5:
  rewrite handoff for round 1`. All three matched.
- Block bytes: measured line count 277, sha256
  `5caf7382b6953bdd3f2c5b316e9d86952400bd0eb45a3e341e1fc4e39b04884d` — both matched the delegation
  message's two readings exactly.
- `git worktree list` reported as found (the pre-round listing: the primary checkout plus the
  `f015-*`, `f020-*`, `f023-*`, `f024-*`, `f025-*`, `f027-r1-dry`, `f027-r2-dry`, `f284-*` and
  `job-*` worktrees — unchanged by this round until the G5 worktree was added and removed).

PAYLOADS (measured against the block's table, both matched):
| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 37 | 1567 | 0cb52ffa8ec84b08caeb9ec2dba6921aeba0e163c5c53bfb6f8084d2c234cb0d |
| records.diff | 89 | 15591 | f9e82396ddfe8ced08b85553cb6e5e5c834f5a8097e305565061684c3ccb0fbb |

`git apply --check` on records.diff → `REAL_EXIT=0`. The real `git apply` → `REAL_EXIT=0`.

G1 TRANSPORT — each `.agent/authored/f027-r2-*` copy compared byte for byte against its source,
read back with `git show 4b2856072:<path>`:
- `f027-r2-block.md` == `.remedy-wt/f027-r2/block.md`: equal=True
- `f027-r2-plan.md` == payload plan.md: equal=True
- `f027-r2-records.diff` == payload records.diff: equal=True

G2 THE RECORDS — each file's sha256, read with `git show 843249805:<path>`, against the reviewer's
table:
| path | bytes | sha256 | match |
|---|---|---|---|
| .agent/live_review.md | 295025 | b866146d3419b4856d42e18e56359086df9a469389b13efed6b1a01cd62b3a68 | True |
| .agent/decisions.md | 2162102 | e9152eb667c14f8ce4828ffbf12bac2359af2fc4434242dcfb381d8bf0f0e1ab | True |
| .agent/plan.md | 1567 | 0cb52ffa8ec84b08caeb9ec2dba6921aeba0e163c5c53bfb6f8084d2c234cb0d | True |

Open finding ids via `open_finding_ids` (scripts/rotate_live_review.py) over the ledger's text at
843249805: `['R-1065']` — matches the reviewer's reading exactly. The ledger's last line begins
`- R-1065 — ` (confirmed verbatim, `startswith` check True).

G3 THE CODE:
```
$ python3 -m ruff check packages/orchestration/task_veto.py packages/orchestration/worktrees.py packages/orchestration/pingpong_job.py packages/orchestration/run_manifest.py tests/orchestration/test_task_veto.py tests/orchestration/test_worktrees.py tests/orchestration/test_task_expectation_status_truth.py tests/test_no_orphan_modules.py tests/orchestration/test_task_veto_runner.py .agent/authored/f027-r2-mutations.py
All checks passed!
REAL_EXIT=0
```
(run at the last code commit, 0739f3162)

`git diff -U0 61250e1e7 636e9c69e -- tests/orchestration/test_task_expectation_status_truth.py tests/test_no_orphan_modules.py tests/orchestration/import_reachability_allowlist.txt`
— whole diff:
```
diff --git a/tests/orchestration/import_reachability_allowlist.txt b/tests/orchestration/import_reachability_allowlist.txt
@@ -246,0 +247 @@ packages.orchestration.task_runner
+packages.orchestration.task_veto
diff --git a/tests/orchestration/test_task_expectation_status_truth.py b/tests/orchestration/test_task_expectation_status_truth.py
@@ -49 +49 @@ _ALLOWED = {
-    EXPECT_SKIPPED: {"skipped"},
+    EXPECT_SKIPPED: {"skipped", "vetoed"},
@@ -53 +53 @@ _ALLOWED = {
-                      "failed", "blocked"},
+                      "failed", "blocked", "vetoed"},
@@ -55,2 +55,2 @@ _ALLOWED = {
-                           "failed", "blocked"},
-    EXPECT_DISPATCHED_NO_CALLS: {"failed", "blocked", "pending", "running"},
+                           "failed", "blocked", "vetoed"},
+    EXPECT_DISPATCHED_NO_CALLS: {"failed", "blocked", "pending", "running", "vetoed"},
@@ -234 +234 @@ class TestTheInputsThemselvesAreClosed:
-                                       PJ.TASK_SKIPPED}
+                                       PJ.TASK_SKIPPED, PJ.TASK_VETOED}
diff --git a/tests/test_no_orphan_modules.py b/tests/test_no_orphan_modules.py
@@ -95,3 +94,0 @@ ALLOWED_UNWIRED: tuple[tuple[str, str], ...] = (
-    ("packages/orchestration/task_veto.py",
-     "F027 T001: the veto control protocol; the runners' fold and the write door wire it in "
-     "later rounds"),
```
Holds exactly S6's and S7's lines — confirmed.

G4 THE TESTS — serial run in the primary checkout at the last code commit (0739f3162), real exit
code:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_veto_runner.py tests/orchestration/test_task_veto.py tests/orchestration/test_worktrees.py tests/orchestration/test_task_expectation_status_truth.py tests/orchestration/test_run_manifest.py tests/orchestration/test_run_manifest_zero_call_expectations.py tests/orchestration/test_run_manifest_task_history_chain.py tests/orchestration/test_pause_manifest.py tests/orchestration/test_pause_resume.py tests/orchestration/test_pause_resume_cycles.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_job_worktree_integration.py tests/orchestration/test_job_worktree_handoff.py tests/orchestration/test_job_worktree_integrity.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_pingpong_job_dod_gate.py tests/cli/test_job_pause.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_event_names.py tests/orchestration/test_dag_schedule.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/cli/test_golden_path.py
757 passed in 203.72s (0:03:23)
REAL_EXIT=0
```
No `SKIPPED` line was printed by `-rs` anywhere in this selection — zero skips.

`--collect-only -q` on the new file alone: `10 tests collected`.

Accounting for the difference from the reviewer's `688 passed`: the reviewer's selection omitted
the new test file and the golden path, and ran over R1's code (before this round's growth of
`test_task_veto.py` and `test_worktrees.py`, and before `"vetoed"` widened
`test_task_expectation_status_truth.py`'s parametrized matrix). Measured directly: `test_task_veto.py`
grew 127→129 (+2), `test_worktrees.py` grew 32→41 (+9, confirmed by collecting R1's own copy of the
file via `git show 25ab44dec:tests/orchestration/test_worktrees.py`), and
`test_task_expectation_status_truth.py` grew 75→81 (+6 — one new status × six expectations in the
exhaustive matrix). `test_task_veto_runner.py` is new (+10) and `tests/cli/test_golden_path.py`
(+42) was outside the reviewer's selection entirely. `688 + 2 + 9 + 6 + 10 + 42 = 757` — matches the
measured total exactly.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [...six "pass" entries...], "fail_count": 0, "ok": true, "passed": true, ...}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0 (run after the tree was clean, i.e. after C5c).

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f027-r2-mut 0739f3162` (exit 0), then
`python3 -B .agent/authored/f027-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f027-r2-mut`:
```
--- control run (unmutated, before) ---
control: exit=0
180 passed in 10.24s
m1 the pre-task fold is removed, so only the fold before the loop runs: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestVetoDuringTheRun::test_a_veto_recorded_while_the_prior_task_runs_stops_the_next_one']
restored byte-identical: True
m2 the fold never calls restore_tree: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestGitWorktreeVetoRestoresTheWorkspace::test_a_veto_and_relaunch_removes_the_blocked_attempts_file']
restored byte-identical: True
m3 the loop dispatches an unreachable task: exit=1 failed=2 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestDiamondVetoBeforeTheRun::test_b_vetoed_before_the_run', 'tests/orchestration/test_task_veto_runner.py::TestLegacyJobFileVeto::test_the_second_of_three_vetoed']
restored byte-identical: True
m4 the fold never sends a skipped task back to pending: exit=1 failed=2 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestBlockThenVetoThenRelaunch::test_the_independent_task_returns_to_pending_and_runs', 'tests/orchestration/test_task_veto_runner.py::TestFoldSkipResetIsExact::test_only_the_reachable_skipped_task_returns_to_pending']
restored byte-identical: True
m5 the fold sends every skipped task after the vetoed one back to pending, unreachable ones too: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestFoldSkipResetIsExact::test_only_the_reachable_skipped_task_returns_to_pending']
restored byte-identical: True
m6 the terminal branch is removed: exit=1 failed=6 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestBlockThenVetoThenRelaunch::test_the_independent_task_returns_to_pending_and_runs', 'tests/orchestration/test_task_veto_runner.py::TestDiamondVetoBeforeTheRun::test_b_vetoed_before_the_run', 'tests/orchestration/test_task_veto_runner.py::TestEveryTaskVetoed::test_nothing_is_dispatched_and_the_error_names_them_all', 'tests/orchestration/test_task_veto_runner.py::TestGitWorktreeVetoRestoresTheWorkspace::test_a_veto_and_relaunch_removes_the_blocked_attempts_file', 'tests/orchestration/test_task_veto_runner.py::TestLegacyJobFileVeto::test_the_second_of_three_vetoed', 'tests/orchestration/test_task_veto_runner.py::TestVetoDuringTheRun::test_a_veto_recorded_while_the_prior_task_runs_stops_the_next_one']
restored byte-identical: True
m7 the terminal's error leaves out the unreachable set: exit=1 failed=2 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestDiamondVetoBeforeTheRun::test_b_vetoed_before_the_run', 'tests/orchestration/test_task_veto_runner.py::TestEveryTaskVetoed::test_nothing_is_dispatched_and_the_error_names_them_all']
restored byte-identical: True
m8 the fold vetoes a task whose status is outside VETOABLE_TASK_STATUSES: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestInertVeto::test_a_veto_of_an_already_applied_task_changes_nothing']
restored byte-identical: True
m9 the fold swallows a TaskVetoError and dispatches on: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestCorruptVetoFile::test_blocks_with_task_veto_control_error_and_dispatches_nothing']
restored byte-identical: True
m10 restore_tree never deletes a path the tree lacks: exit=1 failed=3 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestGitWorktreeVetoRestoresTheWorkspace::test_a_veto_and_relaunch_removes_the_blocked_attempts_file', 'tests/orchestration/test_worktrees.py::TestRestoreTree::test_restore_removes_a_nested_directory_left_empty', 'tests/orchestration/test_worktrees.py::TestRestoreTree::test_restore_removes_an_added_file']
restored byte-identical: True
m11 restore_tree drops the executable bit: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_worktrees.py::TestRestoreTree::test_restore_recreates_an_executable_path']
restored byte-identical: True
m12 "vetoed" is left out of VALID_TASK_STATUSES: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_task_veto_runner.py::TestTaskCapAfterAVeto::test_the_paused_manifest_reads_the_vetoed_task_as_skipped']
restored byte-identical: True
m13 the gate's task_already_vetoed route repairs no event (R-1065 as it stood): exit=1 failed=3 failing_node_ids=['tests/orchestration/test_task_veto.py::TestTaskVetoedEvent::test_the_gate_route_repairs_a_missing_event_too', 'tests/orchestration/test_task_veto.py::TestVetoTaskCommand::test_a_vetoed_status_with_no_entry_answers_empty_request_id_and_repairs_nothing', 'tests/orchestration/test_task_veto.py::TestVetoTaskCommand::test_task_already_vetoed_refusal_when_an_entry_already_exists']
restored byte-identical: True
m14 the lost race answers {"outcome": "task_already_vetoed"} as before: exit=1 failed=1 failing_node_ids=['tests/orchestration/test_task_veto.py::TestTaskVetoedEvent::test_a_retry_repairs_a_missing_event_after_a_failed_write']
restored byte-identical: True
--- control run (unmutated, after) ---
control: exit=0
180 passed in 8.73s
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
REAL_EXIT=0. Every one of the 14 mutations was red with at least one failing node; none stayed
green; every restoration was byte-identical.

`git worktree remove --force .remedy-wt/f027-r2-mut` → exit 0. `git worktree prune` → exit 0.
`git worktree list` afterward: the primary checkout plus exactly the worktrees constraint 6 named
at step 4 (`f015-*`, `f020-*`, `f023-*`, `f024-*`, `f025-*`, `f027-r1-dry`, `f027-r2-dry`, `f284-*`
and the `job-*` worktrees) — nothing else.

CONSTRAINT 3 — round path set: `git diff --name-only 25ab44dec` (before C6) named exactly:
`.agent/authored/f027-r2-block.md`, `.agent/authored/f027-r2-mutations.py`,
`.agent/authored/f027-r2-plan.md`, `.agent/authored/f027-r2-records.diff`, `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/pingpong_job.py`,
`packages/orchestration/run_manifest.py`, `packages/orchestration/task_veto.py`,
`packages/orchestration/worktrees.py`, `tests/orchestration/import_reachability_allowlist.txt`,
`tests/orchestration/test_task_expectation_status_truth.py`, `tests/orchestration/test_task_veto.py`,
`tests/orchestration/test_task_veto_runner.py`, `tests/orchestration/test_worktrees.py`,
`tests/test_no_orphan_modules.py` — the block's whole named set, nothing extra (this file,
`.agent/handoff.md`, is added by C6 itself). None of the forbidden paths
(`long_run_executor.py`, `pause_control.py`, `safe_points.py`, `dag_schedule.py`,
`pingpong_loop.py`, `ui_server.py`, `apps/`, `docs/`, `.agent/context.md`, `.agent/prose_slips.md`,
`.agent/candidates.md`, `.agent/operator_questions.md`) were touched.

G6 TREE AND PUSH — real readings reported in the final reply (this file cannot contain them, since
they are measured AFTER this commit).

## Authored-text proofs

Every `.agent/authored/f027-r2-*` copy was compared disk-to-disk against its committed source and
matched byte for byte (see G1 above): the block copy, the plan payload copy and the records.diff
payload copy. `f027-r2-mutations.py` is the worker's own tool, not a reviewer-authored payload — no
fidelity proof applies to it.

## Deviations & assumptions

1. C5 was split into C5a, C5b and C5c. The block names C5 as one commit ("THE RUNNER TESTS AND THE
   MUTATION TOOL"), but the new test file alone is 551 insertions — already over the 500-line cap
   before the mutation tool's 280 are added. Per AGENTS.md's commit-size rule and this block's
   constraint 2, the test file was split at a class boundary (right before
   `TestBlockThenVetoThenRelaunch`) into C5a (279 insertions: fixtures, fakes, the diamond, every-
   task-vetoed, the legacy job-file test, the during-the-run veto test) and C5b (272 insertions: the
   remaining classes), with the mutation tool as its own C5c (280 insertions). All three stay under
   the 500-line cap. This is the only oversize-avoidance split in this round.
2. `_fold_task_vetoes` is a MODULE-LEVEL function in `pingpong_job.py`, not a closure nested inside
   `run_job` (unlike `_stop_check`/`_absorb_here`, which are nested). The block says only "one
   helper that `run_job` calls," leaving the shape open; a module-level function let a test
   (`TestFoldSkipResetIsExact`) call it directly to pin the skip-reset rule's exact boundary — a
   scenario driven end-to-end through `run_job`'s own loop cannot distinguish "reset nothing" from
   "reset every skipped task, unreachable ones too" (mutations m4 and m5), because the loop's own
   per-task unreachable filter (S4) independently withholds an incorrectly-reset task from dispatch
   and the terminal (S5) converts it back to `skipped` regardless — both defences mask the fold's own
   bug at the level of `run_job`'s final output. The direct unit test was added specifically to make
   m5 red; without it, m5 was measured GREEN in an early dry run of the mutation tool (reported
   honestly here rather than silently strengthened away).
3. S3 says a vetoed entry's `unreachable_task_ids` is "that task's `veto_unreachable` over the
   tasks" — read literally as `veto_unreachable(job.tasks, [entry.task_id])`, this task's OWN
   downstream alone, computed at the moment it is folded, rather than the cumulative union of every
   veto folded so far in the same pass. This matches `veto_task_command`'s own S7 per-entry
   `unreachable` field (which the block's R1 text established the same way), and is exercised by the
   diamond test (`veto["unreachable"] == [d_id]` at the command, `entry["unreachable_task_ids"] ==
   [d_id]` at the fold).
4. One runner test (`TestTaskCapAfterAVeto`) uses a markdown job (`parse_job_file`) rather than the
   general `_save_job` (Task-Plan) pattern the rest of the file follows. A Task-Plan job never
   carries a `job_file_sha256` (it has no underlying job file), which fails the run manifest's own
   schema validation for a reason wholly unrelated to the veto feature; the markdown form was needed
   specifically because this test reads a real, validated `paused` manifest. The chain's tail task is
   vetoed (nothing depends on it) so the middle task stays reachable and pending when the cap parks
   the run — the intended shape ("the vetoed task as `skipped`" in a valid manifest) is unchanged.
5. No other deviation from the block's ordered commit sequence, specification or constraints.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5a | deviated | C5 split into C5a/C5b/C5c — the test file alone exceeds the 500-line cap |
| C5b | deviated | see C5a |
| C5c | deviated | see C5a |
| G1 TRANSPORT | done | |
| G2 THE RECORDS | done | |
| G3 THE CODE | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOFS | done | |
| G6 TREE AND PUSH | done | reported in the final reply, not this file, per the block |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 2, then the rest of T001: a
task vetoed while its provider call runs, and the cycle executor's reading of a veto. Open findings:
1 (R-1065, landed this round and awaiting the reviewer's resolution). Operator questions: 5.
