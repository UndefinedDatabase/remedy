# Handback — F313 round 4

## Session

SESSION 1 of feature F313 · round 4 · rounds so far 4

Context self-assessment: this session verified every prepared file's digest before use, applied the
three prepared files as proved byte copies, and ran both long steps once through the launch and wait
helpers; no stop condition was met.

Fortschritt: ~85 % (T001 to T003 landed; the consolidation pass, the self-use run and the one full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `3a35ea1c5`..HEAD (C1 to C5, then this commit C6, which carries this handback).

## Commits

### 87d084fc5 F313 R4 C1: book round 3, the plan, the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f313-r4.md` | +154 (new) | byte copy of `block.md` (154 lines, sha256 0efd5d4ede73866428041f05feaee50d0b880f7a2dfef08de0489e39cf9866e4, equal to the prompt's) |
| `.agent/authored/f313-r4-selfuse.py` | +127 (new) | byte copy of the self-use script |
| `.agent/live_review.md` | +2 | byte copy, round 3's verdict |
| `.agent/plan.md` | +5/-6 | byte copy, the plan advanced |

### ec27dfd08 F313 R4 C2: F313's Built State
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T12_F313.md` | +35 | byte copy, the Built State |

### cdcbffe8f F313 R4 C3: the checklist's consolidation pass for F313
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +8/-0 | byte copy, the consolidation paragraph (numstat `8 0`) |

### 64249f32b F313 R4 C4: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8 | the generator's one appended entry SU-068, consumed_by empty |
| `.agent/selfuse_f313/` | +133 (10 new files) | the run's record |

### 3f7d7a36c F313 R4 C5: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f313-closure-suite.txt` | +28 (new) | the suite transcript |

### C6 (this commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## External actions

- `python3 .remedy-wt/f313-r4/prep/launch.py selfuse ...` then `wait.py selfuse ... 50`: ended `exit 0 wall 53.8`; real provider calls of the self-use run only (2 calls).
- `python3 .remedy-wt/f313-r4/prep/launch.py suite ...` then `wait.py suite ... 50`: ended `exit 0 wall 374.2`.
- `python3 scripts/closure_suite_cost.py --feature F313 --record ~/.remedy-loop/test_load.jsonl`: exit 0.
- `git push origin feature/f313-contract-1-22`: see the reply of this session (the push follows this commit). No pull request created or merged.

## Verification

1. Gate 1: `git status --porcelain` empty; `python3 .remedy-wt/f313-r4/prep/verify.py .` exit 0, every line `True`, `absent` for C6, last line `ALL True`.
2. Gate 2, the ten files under `.agent/selfuse_f313/`, bytes: `SU-068.md` 1048, `entry_and_job_file.txt` 398, `execution_config.txt` 1367, `result_state.txt` 856, `timing.txt` 104, `changed_paths.txt` 60, `full_transcript.txt` 1578, `staleness_after.txt` 200, `job_diff.txt` 1540, `run_defects.txt` 5; all non-empty.
3. Gate 3, the suite: exit 0; `22100 passed, 11 skipped, 1 warning in 373.36s (0:06:13)`; bad node ids NONE.
4. Gate 4: `python3 -m apps.cli.main integrity check --json` exit 1, `fail_count` 1, the one failing check `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`; `open_finding_ids` count printed `87`.

## Authored-text proofs

Python byte equality against the prepared file, all `True`: `.agent/authored/f313-r4.md`, `.agent/authored/f313-r4-selfuse.py`, `.agent/live_review.md`, `.agent/plan.md` (C1); `docs/roadmap/features/T12_F313.md` (C2); `docs/agents/planner_reviewer_prompt.md` (C3). The digests of `block.md`, `verify.py` and `digests.txt` and of every listed prepared file matched before use.

## Self-use run

- Entry id: SU-068
- Title: Narrow the excused handler at apps/cli/commands/test_cmds.py:108
- Job id: 365cba7fcaa04392
- Builder: claude-cli, model claude-sonnet-4-6; reviewer: claude-cli, model claude-sonnet-4-6 (from `execution_config.txt`).
- Job state: completed; stop reason: empty.
- Task T001: applied_to_job_workspace, reviewer verdict pass (final_status staged_review_passed, repair rounds used 0).
- Wall seconds (`timing.txt`): 49.5
- Changed paths: `apps/cli/commands/test_cmds.py`, `tests/test_ble001_ratchet.py`

Job diff verbatim (`job_diff.txt`):

```
$ git diff HEAD...remedy/job-365cba7fcaa04392  (exit 0)
diff --git a/apps/cli/commands/test_cmds.py b/apps/cli/commands/test_cmds.py
index 3ff8393e5..98ff8cec4 100644
--- a/apps/cli/commands/test_cmds.py
+++ b/apps/cli/commands/test_cmds.py
@@ -103,9 +103,13 @@ def _print_result_text(result: object, *, out=None) -> None:
 def _cmd_discover_commands(job_id_str: str, *, as_json: bool) -> None:
     job_id = resolve_job_id_or_fail(job_id_str, json_output=as_json)
     try:
-        from packages.orchestration.pingpong_job import require_job_plan
+        from packages.orchestration.pingpong_job import (
+            JobNotFoundError,
+            JobStoreError,
+            require_job_plan,
+        )
         job = require_job_plan(job_id)
-    except Exception as exc:  # noqa: BLE001 — job lookup failure is reported, not raised, from a read command
+    except (JobNotFoundError, JobStoreError) as exc:
         fail("job_store_error", str(exc), json_output=as_json)
 
     target_repo_str = job.metadata.get("target_repo")
diff --git a/tests/test_ble001_ratchet.py b/tests/test_ble001_ratchet.py
index 1fa195707..e1cce97e9 100644
--- a/tests/test_ble001_ratchet.py
+++ b/tests/test_ble001_ratchet.py
@@ -18,7 +18,7 @@ REASONED = re.compile(r"^ — \S")
 
 #: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
 #: commit that removes a mark lowers this number in the same commit, and it is never raised.
-MAX_EXCUSED = 282
+MAX_EXCUSED = 281
 
 
 def _marks() -> list[tuple[str, int, str]]:
```

`run_defects.txt` verbatim:

```
NONE
```

## Closure suite

```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 374.2s (the launcher's reading); pytest's own reported wall time: 373.36s (0:06:13)
summary line: 22100 passed, 11 skipped, 1 warning in 373.36s (0:06:13)
bad node ids (failed + errors):
  - NONE
leftover processes: NONE
tree it ran on: 64249f32b (F313 R4 C4: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C4 changed only .agent/ files, the feature file, the checklist page and the self-use queue
reflog before: 64249f32b HEAD@{2026-10-21 05:03:38 +0200}: commit: F313 R4 C4: the closure's self-use item run to its approval gate, never applied
reflog after: 64249f32b HEAD@{2026-10-21 05:03:38 +0200}: commit: F313 R4 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F313 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1304.91 CPU seconds, 373.37 wall seconds, 22111 tests collected, exit status 0, recorded 2026-10-21T03:09:54Z
This closure's suite used 1304.91 CPU seconds, 0.4 percent less than F311's 1310.31, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F311's closure run:
  +8.08 s  tests/runtimes/test_supervisor_portability.py (49.59 -> 57.67)
  +3.96 s  tests/test_grouped_cli.py (24.04 -> 28.00)
  +3.45 s  tests/orchestration/test_subtree_rerun_prepare.py (10.79 -> 14.24)
  +2.76 s  tests/orchestration/test_record_client_answers.py (0.00 -> 2.76)
  +2.07 s  tests/orchestration/test_serve_daemon.py (19.92 -> 21.99)
  +1.74 s  tests/orchestration/test_stream_export_e2e.py (3.57 -> 5.31)
  +1.73 s  tests/runtimes/test_runtime_cli_process_boundary.py (9.93 -> 11.66)
  +1.48 s  tests/orchestration/test_public_api_gate_paths.py (19.07 -> 20.55)
  +1.47 s  tests/orchestration/test_job_worktree_integration.py (6.22 -> 7.69)
  +1.47 s  tests/orchestration/test_token_ledger.py (8.81 -> 10.28)
```

## Deviations & assumptions

None. (The block's compound shell shapes were refused by the sandbox in a few calls; the commands were re-run as separate calls or as small scripts under `.remedy-wt/f313-r4-worker/`, with the same commands and results. The reflog line was read twice around the suite and the cost script ran once with output captured by a script.)

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. The reviewer reviews round 4, books its verdict and registers every self-use run defect in the next round's first commit.
4. The evidence bundle and the review package (the suite is green).
5. The closing round: the STATUS line, the README and the pull request.

Operator questions open: 1. Open findings count gate 4 printed: 87 (rule: `open_finding_ids` over `.agent/live_review.md`; commit `3f7d7a36c`).

## For the operator, in plain sentences

Before a feature closes, Remedy runs one real piece of work on itself with a paid model, and then runs its whole test collection once on the code that will ship. The paid run was asked to replace one overly broad error catch in a command with the specific errors it can really hit, and it finished cleanly with the reviewer passing it and no defects, held at the approval gate and not applied. The whole test collection ran 22100 tests that passed and none that failed, with 11 skipped. The run took about six and a quarter minutes. The computer-time reading was a little under half a percent lower than the previous feature's, well inside the allowed rise.
