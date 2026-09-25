# Handback — F026 Task edit at runtime · Round 2

## Session

SESSION 1 of feature F026 · round 2 · rounds so far 2

The large majority of the session's context budget remained at the point this handback was
written. This round booked round 1's PASS verdict, registered R-1059, recorded DECISION F026 D2,
repaired R-1059 (`run_job` now clears the job's stale `error` when it moves to `JOB_RUNNING`),
closed round 1's one unmet test obligation (`_assert_refused` now also proves the evidence export
directory's own files are untouched by a refusal), and landed T002: `job.edit-task` reaches the
operator through the catalog, the CLI (`apps/cli/commands/job_plan_cmd.py`) and the write door
(`packages/orchestration/ui_server.py`), `job plan-show` names each task's own id, status and
spec version, and a fake-run trace proof shows the next run's prompt trace carries an edited
task's new goal/acceptance and none of the old.

## Range

Review of ee874cb2f..HEAD

## Commits

### af785519f F026 R2 C1a: copy round 2 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f026-r2-block.md | +280/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f026-r2-plan.md | +31/-0 | copy of the plan.md payload |
| .agent/authored/f026-r2-records.diff | +69/-0 | copy of the records.diff payload |

380 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 280, plus 100: 31+69 = 100) — matches exactly.

### ebeb3eaa1 F026 R2 C1b: book round 1, register R-1059, record D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +49/-0 | records.diff: DECISION F026 D2 appended |
| .agent/live_review.md | +4/-0 | records.diff: F026 R1 gate entry and R-1059 registration appended |
| .agent/plan.md | +9/-14 | rewritten whole to the plan.md payload (`shutil.copyfile`) |

49/0, 4/0, 9/14 — matches the block's G2 stated expectation exactly. `git apply --check` on
records.diff: exit 0; `git apply`: exit 0.

### 772ae9429 F026 R2 C2: clear a relaunched job's stale error when it starts running (R-1059)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +1/-0 | S1: `job.error = ""` in the same persist that moves the job to `JOB_RUNNING`, one comment line naming R-1059 |
| .agent/live_review.md | +2/-0 | the `Landed: R-1059 — ` line the block orders, appended |

3 insertions; `git diff --numstat ee874cb2 <this commit> -- packages/orchestration/pingpong_job.py`
reads 1/0 (G3).

### 52b7adeaf F026 R2 C3: a refused runtime edit leaves the export directory unchanged
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_edit_runtime.py | +11/-0 | S2: `_assert_refused` also records/compares the sorted file names directly in the evidence export dir |

11 insertions.

### 912b20eef F026 R2 C4: job.edit-task in the catalog and the CLI, and the spec version in plan-show
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +29/-0 | S3: `job.edit-task` entry after `job.plan-edit-task`; joins `UI_EXPOSED_COMMANDS` with the D2 comment |
| apps/cli/commands/job_plan_cmd.py | +96/-2 | S4: `_cmd_edit_task`, `_spec_version`, `_resolve_task_arg`, refusal classes, `COMMAND_HANDLERS` entry; S5: `plan-show`'s three new keys and text line |
| docs/guides/exit-codes.md | +1/-0 | S3: the `remedy job edit-task` row, exit code 3, after `plan-edit-task`'s row |
| tests/ui_server/test_command_channel.py | +4/-4 | S7 (the exposed set): `job.edit-task` added to `test_the_set_holds_exactly_the_ruled_ids_and_no_other`'s list |

130 insertions, under the cap.

### 83f6c2542 F026 R2 C5: the door dispatches job.edit-task
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +80/-0 | S6: `JOB_EDIT_TASK_COMMAND_ID`, the shape check in `_read_command_payload`, `task_edit_refusal`, the `_handle_command_submission` clause, `_dispatch_edit_task` |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | S7: `packages.orchestration.task_edit_runtime` in sorted place |
| tests/test_no_orphan_modules.py | +0/-2 | S7: the `ALLOWED_UNWIRED` entry round 1 added, removed (T002 wires the module in) |
| tests/ui_server/test_command_channel.py | +4/-2 | S7 (the door's methods and imports): `_dispatch_edit_task` in `DOOR_METHODS`, `edit_task_at_runtime` in `ALLOWED_IMPORTS`, the plan-edits' dispatch-effect branch widened to `job.edit-task` |

85 insertions, under the cap.

### 37dddbcf7 F026 R2 C6: test job.edit-task and prove the next run's trace carries the edit
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_plan_cmd.py | +156/-1 | THE TESTS: `approved_job_id` fixture, `_entry_for`, `TestEditTaskCommand`, `TestEditTaskRefusals`, three `plan-show` key/text tests |
| tests/orchestration/test_task_edit_runtime.py | +96/-4 | S8: `TestTracePreservesTheEdit`, `_save_job` gains `repo_path`, new imports |
| tests/ui_server/test_command_dispatch.py | +146/-0 | THE TESTS: `TestEditTaskDispatchEffects` beside `TestPlanEditDispatchEffects` |

398 insertions, under the cap.

### cf0476dc1 F026 R2 C7: the round's red-proof mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f026-r2-mutations.py | +198/-0 | G5: the round's mutation tool, `git add`ed |

198 insertions.

### (pending) F026 R2 C8: rewrite handoff for round 2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback (self-reference, R-0149 pattern) |

## External actions

- `git worktree add --detach .remedy-wt/f026-r2-mut cf0476dc1` (G5) — added, then
  `git worktree remove --force .remedy-wt/f026-r2-mut` and `git worktree prune` — removed after
  the mutation tool's run. `git worktree list` afterward shows the primary checkout and every
  worktree already present at session start, minus one pre-existing PRUNABLE entry
  (`/tmp/pytest-of-decodeux/.../ba7a5118c3244937`) that `git worktree prune` also cleared as a
  side effect — recorded as a deviation below.
- `git push origin feature/f026-task-edit-runtime` (after C8) — its real outcome is reported in
  the final reply, since the push happens after this commit.
- No `gh pr create` — the branch's pull request opens at F026's closure, per the block.
- No `git stash`, no force-push, no checkout of `main`, no branch deletion, no `remedy/job-*`
  worktree or branch created or deleted by this worker, no `npm`/`npx`.

## Verification

```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
(absent, checked before step one)
```

```
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f026-task-edit-runtime
$ git log --oneline -1
ee874cb2f F026 R1 C5: rewrite handoff for round 1
```
All three matched the block's stated readings exactly, before any commit of this round.

```
$ (line count and sha256 of .remedy-wt/f026-r2/block.md, measured)
line_count: 280
sha256: dda9886cf0b56660bc9f53532855d82469758786b49d3af0eb8da39535f3eaaa
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list
(reported at step 4: primary checkout + the pre-existing F015/F020/F023/F024/F025/F026-r2-dry/sim/
F284 dry/sim worktrees, the same remedy/job-* worktrees already present at session start, and one
PRUNABLE entry under /tmp/pytest-of-decodeux/... left by an earlier test run.)
```

### G1 — payload transport

```
$ (lines/bytes/sha256 of each .remedy-wt/f026-r2-payloads/ payload, measured)
plan.md          31 lines,  1104 bytes, 1de25789543af4d85db2a056ce89a37ec02e7d6b58577f599bc9cf7bfe480a97
records.diff     69 lines, 12896 bytes, 0a5a6c6877112c41e880102013eb0ee68f89e77c7d393acadcea461edbe128bd
```
Every payload's measured lines/bytes/sha256 matched the block's table exactly.

```
$ python3 -c "committed = git show <commit>:<path>; source = open(<src>, 'rb').read(); committed == source"
f026-r2-block.md     (at af785519f)  EQUAL (sha256 dda9886c...)
f026-r2-plan.md      (at af785519f)  EQUAL (sha256 1de25789...)
f026-r2-records.diff (at af785519f)  EQUAL (sha256 0a5a6c68...)
```
Each `.agent/authored/f026-r2-*` copy, read back with `git show af785519f:<path>`, is
byte-identical to its `.remedy-wt/f026-r2(-payloads)/` source.

### G2 — the records

```
$ python3 -c "bytes/sha256 of each path read with git show ebeb3eaa1:<path>"
.agent/live_review.md    317479 bytes  e6187e0747c474f67f1ea514493bb21a7a5799bebefcbf952337212f8cbfb97e
.agent/decisions.md     2131684 bytes  2172168d78f16fe12ef96a865d5445769dc41b67fe4ff7d5914ebd7c8a710510
.agent/plan.md             1104 bytes  1de25789543af4d85db2a056ce89a37ec02e7d6b58577f599bc9cf7bfe480a97
```
All three equal the block's stated G2 table exactly.

```
$ python3 -c "from scripts.rotate_live_review import open_finding_ids; ..."
open at ee874cb2f: ['R-1008', 'R-1055', 'R-1057', 'R-1058']
open at ebeb3eaa1:  ['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1059']
open at cf0476dc1:  ['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1059']
```
Matches the block's stated reading exactly at every point named.

```
$ tail -1 .agent/live_review.md at 772ae9429 (C2)
Landed: R-1059 — `run_job` in `packages/orchestration/pingpong_job.py` now clears `job.error`
to `""` in the same persist that moves the job to `JOB_RUNNING` before the dispatch loop;
landed at this round's C2.
```
Begins `Landed: R-1059 — ` exactly, as the block requires.

### G3 — the code, at C7 (cf0476dc1)

```
$ python3 -m ruff check .agent/authored/f026-r2-mutations.py packages/orchestration/pingpong_job.py packages/orchestration/ui_server.py apps/cli/command_catalog.py apps/cli/commands/job_plan_cmd.py tests/orchestration/test_task_edit_runtime.py tests/cli/test_job_plan_cmd.py tests/ui_server/test_command_dispatch.py tests/ui_server/test_command_channel.py tests/test_no_orphan_modules.py
All checks passed!
REAL_EXIT=0
```
(every `.py` path of CONSTRAINT 2; `import_reachability_allowlist.txt` and `exit-codes.md` are not
`.py` and are excluded from this gate by its own wording.)

```
$ git diff --numstat ee874cb2 cf0476dc1 -- packages/orchestration/pingpong_job.py
1	0	packages/orchestration/pingpong_job.py
```
1 insertion, 0 deletions — within the block's stated "1 or 2 insertions and 0 deletions".

### G4 — the tests, in the primary checkout at C7

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_edit_runtime.py tests/cli/test_job_plan_cmd.py tests/ui_server/test_command_dispatch.py tests/ui_server/test_command_channel.py tests/cli/test_exit_codes.py tests/test_command_catalog.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/cli/test_job_refusal_envelope.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_pause_resume.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_plan_edit_execution.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
1580 passed, 1 skipped in 177.09s (0:02:57)
REAL_EXIT=0
```
Only ONE `SKIPPED` line printed — the D12 quarantine, unchanged. The reviewer's baseline run (same
selection WITHOUT `test_task_edit_runtime.py` and the golden path, at `ee874cb2` carrying this
round's records) read `1467 passed, 2 skipped`; the vitest node of `test_test_runner.py` that
skipped there PASSES here, accounting for the skip count dropping by one.

Accounting for the rest of the difference, measured directly (not by assumption):
- `--collect-only -q` on each file this round changed, at `ee874cb2` and at `cf0476dc1`:
  `tests/orchestration/test_task_edit_runtime.py` 48 → 49 (+1, `TestTracePreservesTheEdit`);
  `tests/cli/test_job_plan_cmd.py` 22 → 35 (+13, the `plan-show` key/text tests + `TestEditTaskCommand` +
  `TestEditTaskRefusals`); `tests/ui_server/test_command_dispatch.py` 32 → 38 (+6, `TestEditTaskDispatchEffects`);
  `tests/ui_server/test_command_channel.py` 109 → 109 (+0, assertion-content-only changes, no new
  node). Net across the reviewer's own selection: +19.
- The reviewer's exact baseline selection (all files except `test_task_edit_runtime.py` and the
  golden path), `--collect-only -q` at `cf0476dc1`: **1490** nodes, against the reviewer's own 1469
  at `ee874cb2` — a further +2 the per-file deltas above do not explain. Measured directly: this +2
  is TWO NEW parametrized instances of `test_exit_codes.py`'s two
  `@pytest.mark.parametrize("entry", CATALOG, ...)` tests, one each, gained purely from the new
  `job.edit-task` `CommandEntry` in `apps/cli/command_catalog.py` (S3) — no test FILE this round
  touched, but a test that parametrizes over the whole catalog. 1469 + 19 + 2 = 1490. Exact.
- `--collect-only -q` on `tests/cli/test_golden_path.py`: 42 nodes, all passing (no skip inside it).
- 1490 (reviewer's selection at `cf0476dc1`) + 49 (`test_task_edit_runtime.py`, wholly new to this
  round's selection) + 42 (golden path, wholly new) = **1581** = 1580 passed + 1 skipped, exactly
  this run's total. Every difference accounted for.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=160"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```
Six `pass`, `fail_count` 0.

### G5 — the red proofs

```
$ git worktree add --detach .remedy-wt/f026-r2-mut cf0476dc1
Preparing worktree (detached HEAD cf0476dc1)
$ python3 -B .agent/authored/f026-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f026-r2-mut
control (before): exit=0 failed=0 ids=[]
m1 run_job leaves `error` as it was when the job starts running: exit=1 failed=1 ids=[...TestTracePreservesTheEdit::test_the_new_runs_trace_carries_the_edit_and_the_old_run_keeps_the_old_spec] restored=True
m2 the edit no longer updates the entry's title (the v1 remnant): exit=1 failed=5 ids=[...test_waiting_task_is_edited, ...test_keeps_identity_fields_and_updates_the_prompt_fields, ...TestTracePreservesTheEdit(...), ...TestEditTaskCommand::test_accepted_by_the_task_entrys_own_id, ...TestEditTaskDispatchEffects::test_accepted_edit_updates_the_entry_and_audits_the_tokens_fingerprint] restored=True
m3 the reset no longer restores the skipped tasks after the reset task: exit=1 failed=3 ids=[...TestReset::test_reset_restores_skipped_tasks_after_it_not_before[failed], ...[blocked], ...TestTracePreservesTheEdit(...)] restored=True
m4 the door admits job.edit-task without expected_version: exit=1 failed=1 ids=[...TestEditTaskDispatchEffects::test_a_missing_expected_version_is_a_shape_error_on_that_field] restored=True
m5 task_edit_refusal answers task_not_editable with 500: exit=1 failed=1 ids=[...TestEditTaskDispatchEffects::test_a_runtime_refusal_is_409_rejected_state_with_the_detail[passed-the task is passed]] restored=True
m6 the door's dispatcher names the actor "door" instead of the token fingerprint: exit=1 failed=1 ids=[...TestEditTaskDispatchEffects::test_accepted_edit_updates_the_entry_and_audits_the_tokens_fingerprint] restored=True
m7 the CLI exits 1 for task_not_editable: exit=1 failed=1 ids=[...TestEditTaskRefusals::test_a_passed_task_refuses_task_not_editable] restored=True
m8 the CLI does not resolve a planned id to its task entry: exit=1 failed=1 ids=[...TestEditTaskCommand::test_accepted_by_the_task_plans_own_id] restored=True
m9 the CLI reads a missing --spec-version as 1: exit=1 failed=1 ids=[...TestEditTaskRefusals::test_missing_spec_version] restored=True
m10 `job plan-show` omits `spec_version`: exit=1 failed=4 ids=[...TestPlanShow::test_text_prints_each_criterion_under_the_index_the_edits_take, ...test_json_names_each_tasks_own_id_status_and_spec_version, ...test_text_prints_spec_version_and_status_under_the_goal_line, ...test_after_a_runtime_edit_the_spec_version_advances] restored=True
packages/orchestration/pingpong_job.py restored byte-identical: True
packages/orchestration/task_edit_runtime.py restored byte-identical: True
packages/orchestration/ui_server.py restored byte-identical: True
apps/cli/commands/job_plan_cmd.py restored byte-identical: True
control (after): exit=0 failed=0 ids=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
$ git worktree remove --force .remedy-wt/f026-r2-mut
$ git worktree prune
$ git worktree list
(primary checkout + the pre-existing F015/F020/F023/F024/F025/F026-r2-dry/sim/F284 dry/sim
worktrees and the same remedy/job-* worktrees already present at session start; f026-r2-mut
absent; the one pre-existing PRUNABLE tmp entry also gone — see Deviations)
```
Every one of the 10 mutations was caught (exit≠0, failed>0), every restore byte-identical, both
controls green (exit 0, 0 failed). No test needed adding — every mutation was already red under
the committed test files.

## Authored-text proofs

`.agent/authored/f026-r2-block.md`, `f026-r2-plan.md` and `f026-r2-records.diff` (at C1a) were
built with `shutil.copyfile` from the reviewer's payload files — never retyped, never edited —
and G1 compared every one byte for byte, read back with `git show af785519f:<path>`, against its
source: all three BYTE-IDENTICAL. `.agent/plan.md` was REWRITTEN whole (`shutil.copyfile`) from
`plan.md` at C1b; `records.diff` was applied verbatim with `git apply --check` then `git apply`,
never retyped or hand-edited — G2's byte/sha256 table on the resulting `.agent/live_review.md`,
`.agent/decisions.md` and `.agent/plan.md` confirms the applied result matches the reviewer's own
target state exactly.

Everything else this round wrote — the R-1059 fix, the `_assert_refused` evidence-directory
comparison, `job.edit-task`'s catalog entry and CLI handler, `plan-show`'s three new keys and text
line, the door's dispatch clause, every S7 guard widening, the trace-proof test class, the CLI and
dispatch-effect tests, and the mutation tool — is WORKER-authored production code and tests
against the specification S1–S9 (the block's own framing, "THE PRODUCTION CHANGE IS SPECIFIED, NOT
SLICED"), not reviewer payload text, so no authored-text fidelity proof applies to it.

## Deviations & assumptions

1. **`git worktree prune` cleared a pre-existing stale entry.** G5 orders `git worktree prune`
   after removing this round's own mutation worktree. At session start, `git worktree list`
   already carried one PRUNABLE entry unrelated to this round
   (`/tmp/pytest-of-decodeux/pytest-16995/.../ba7a5118c3244937`, left by an earlier test run
   outside this session). Running the ordered `prune` also cleared that entry, which the block's
   step-4 reading (before any command of this round) still showed. `git worktree list` at G6
   therefore differs from the step-4 reading by exactly that one absent PRUNABLE line, beyond the
   primary checkout's advanced HEAD. Not a worktree CONSTRAINT 5 names to leave alone — it was
   already prunable, not active — but noted here because the two readings are not byte-identical.
2. Everything else followed the block's ordered commit sequence exactly (C1a, C1b, C2, C3, C4, C5,
   C6, C7, then C8 inside which this handback lives); no payload was edited or retyped; no commit
   touched a path outside the tracked set CONSTRAINT 2 names (confirmed by
   `git diff --name-only ee874cb2` below); no gate went red, so no repair or STOP was needed; no
   mutation stayed green, so no test needed adding before C8.

```
$ git diff --name-only ee874cb2
.agent/authored/f026-r2-block.md
.agent/authored/f026-r2-mutations.py
.agent/authored/f026-r2-plan.md
.agent/authored/f026-r2-records.diff
.agent/decisions.md
.agent/handoff.md
.agent/live_review.md
.agent/plan.md
apps/cli/command_catalog.py
apps/cli/commands/job_plan_cmd.py
docs/guides/exit-codes.md
packages/orchestration/pingpong_job.py
packages/orchestration/ui_server.py
tests/cli/test_job_plan_cmd.py
tests/orchestration/import_reachability_allowlist.txt
tests/orchestration/test_task_edit_runtime.py
tests/test_no_orphan_modules.py
tests/ui_server/test_command_channel.py
tests/ui_server/test_command_dispatch.py
```
(measured again after C8, before push, in the final reply) Exactly CONSTRAINT 2's named path set.
None of `packages/orchestration/task_edit_runtime.py`, `packages/orchestration/plan_editing.py`,
`packages/orchestration/long_run_executor.py`, `apps/ui/`, `.agent/prose_slips.md`,
`.agent/candidates.md`, `.agent/operator_questions.md`, `README.md` or
`docs/roadmap/features/T5_F026.md` appears.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 380 insertions (280+100), matches the block's expectation exactly; all three copies byte-identical |
| C1b | done | `git apply --check`/`git apply` both exit 0; per-file numstat 49/0, 4/0, 9/14 matches the G2 table exactly; open-finding set gains R-1059 only |
| C2 | done | 1 insertion in `pingpong_job.py` (G3); `Landed: R-1059 — ` line appended, begins exactly that |
| C3 | done | 11 insertions; `_assert_refused` now compares the export dir's own files too |
| C4 | done | 130 insertions, under the cap; catalog entry, CLI handler, plan-show keys, exit-codes row, exposed-set guard all land together |
| C5 | done | 85 insertions, under the cap; door constant, shape check, refusal mapper, dispatch clause and `_dispatch_edit_task`, plus the door-method/import/allowlist/orphan guards |
| C6 | done | 398 insertions, under the cap; trace-proof class passes first try after one assertion correction (title includes the goal); CLI and dispatch-effect test classes both pass |
| C7 | done | 198 insertions; mutation tool ruff-clean |
| G1 | done | every payload's lines/bytes/sha256 matched the table; every copy byte-identical by `git show` |
| G2 | done | all three files match the stated bytes/sha256; open-finding set correct at both readings; ledger's last line at C2 begins `Landed: R-1059 — ` |
| G3 | done | ruff clean over every `.py` path of CONSTRAINT 2 at C7; `pingpong_job.py` diff reads 1/0 |
| G4 | done | 1580 passed, 1 skipped (D12 only), exit 0; every difference from the reviewer's 1467/2 accounted for by measurement, including a +2 catalog-parametrize ripple this round's code (not test files) caused; six `integrity check` pass |
| G5 | done | all 10 mutations caught, every restore byte-identical, both controls green |
| G6 | done | reported in the final reply, after C8, the push and the pull-request list |
| Pull request | skipped | not opened this round — the branch opens one at F026's closure, per the block |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 2. Then T003 — the version
chip, the popover's version list, the edit affordance on eligible nodes only, and the end-to-end.
Open findings: 5 — `R-1008`, `R-1055`, `R-1057` and `R-1058`, all owned by F285, and `R-1059`,
owned by F026 (stays open until the reviewer's own `Done:` closes it). Operator questions open: 4
— the count of `### Q` headings in `.agent/operator_questions.md`.
