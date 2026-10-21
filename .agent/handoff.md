# Handback — F078 round 7: the closure's integration-gate round (consolidation pass, self-use run, the one full suite)

## Session

SESSION 2 of feature F078 · round 7 · rounds so far 7

Context self-assessment: this worker copied prepared files, ran the two long commands through the helpers and wrote text, and the context was far from exhausted.

Fortschritt: ~92 % (T001 to T003 landed, contract 1.23; the consolidation pass, the self-use run and the one full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `295ad358c`..`HEAD` on `feature/f078-autonomy-levels-2` (base: round 6's handback commit `295ad358c`).

## Commits

### 1e0440d35 F078 R7 C1: book round 6, the plan, the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f078-r7.md` | +154/-0 | new: the block of this round |
| `.agent/authored/f078-r7-selfuse.py` | +127/-0 | new: the self-use script |
| `.agent/live_review.md` | +2/-0 | round 6 booked |
| `.agent/plan.md` | +5/-6 | rewritten |

### cd41569b3 F078 R7 C2: F078's Built State
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T3_F078.md` | +53/-0 | the Built State |

### 867dc1d27 F078 R7 C3: the checklist's consolidation pass for F078
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +12/-0 | F078's consolidation paragraph |

### 239bfc93b F078 R7 C4: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | the generator's one appended entry, SU-069, `consumed_by` empty |
| `.agent/selfuse_f078/` | 10 new files | the run's record (SU-069.md 17, changed_paths.txt 2, entry_and_job_file.txt 5, execution_config.txt 43, full_transcript.txt 14, job_diff.txt 27, result_state.txt 12, run_defects.txt 1, staleness_after.txt 2, timing.txt 3 lines) |

### 1287824bc F078 R7 C5: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f078-closure-suite.txt` | new | the suite transcript |

### (this commit) F078 R7 C6: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | full rewrite | this handback |

## External actions

- Real provider calls: the self-use run of C4 (budgeted, expected), 2 calls through the claude-cli provider.
- The self-use job created the branch `remedy/job-4ef9b1c80c774ba2` locally; it was never applied or pushed.
- No pull request is open and none was created. `git push origin feature/f078-autonomy-levels-2` after this commit: result in the worker's final reply.

## Verification

1. Preconditions: `git rev-parse --short=9 HEAD` `295ad358c`, equal to the remote branch tip; `git status --porcelain` empty; `.agent/STOP` absent. All prepared digests matched (block.md 154 lines, sha256 `da43ef867b683513ed19e44522c4cadcb825a76b2b3ae8bec5348522e69dd7f3`).
2. Self-use run: `launch.py selfuse` then `wait.py selfuse 50`: `exit 0 wall 103.6`. After it `git status --porcelain` showed only `scripts/self_use_queue.json` modified and `.agent/selfuse_f078/` new; the diff of the queue is one appended entry SU-069 with an empty `consumed_by`.
3. Suite (C5): `python3 -m pytest -n auto -q`, exit 1, `3 failed, 22185 passed, 11 skipped, 1 warning in 360.08s (0:06:00)`. Reflog unchanged during the run. Cost script exit 0 (see below).
4. Gate 1: `git status --porcelain` empty; `verify.py .`: every line `True`, C6 `absent`, last line `ALL True`.
5. Gate 2: ten files under `.agent/selfuse_f078/`, all non-empty: SU-069.md 1075, changed_paths.txt 68, entry_and_job_file.txt 401, execution_config.txt 1367, full_transcript.txt 1586, job_diff.txt 1272, result_state.txt 866, run_defects.txt 5, staleness_after.txt 200, timing.txt 104 bytes.
6. Gate 3: suite exit 1, summary `3 failed, 22185 passed, 11 skipped, 1 warning in 360.08s (0:06:00)`; bad node ids: the three listed in the transcript below.
7. Gate 4: `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing check `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`. `open_finding_ids` count: `87`.

## Self-use run

- Entry id: SU-069
- Title: Narrow the excused handler at apps/cli/commands/worker_facade_cmd.py:257
- Job id: 4ef9b1c80c774ba2
- Builder: claude-cli, model claude-sonnet-4-6 (effort medium). Reviewer: claude-cli, model claude-sonnet-4-6 (effort medium).
- Job state: completed. Stop reason: empty.
- Tasks: T001: applied_to_job_workspace, reviewer verdict pass (final_status staged_review_passed, repair_rounds_used 0).
- Wall seconds (timing.txt): 99.2
- Paths in `changed_paths.txt`: `apps/cli/commands/worker_facade_cmd.py`, `tests/test_ble001_ratchet.py`
- `job_diff.txt` verbatim:

```
$ git diff HEAD...remedy/job-4ef9b1c80c774ba2  (exit 0)
diff --git a/apps/cli/commands/worker_facade_cmd.py b/apps/cli/commands/worker_facade_cmd.py
index c5d1220ab..9f33b92bd 100644
--- a/apps/cli/commands/worker_facade_cmd.py
+++ b/apps/cli/commands/worker_facade_cmd.py
@@ -254,7 +254,7 @@ def doctor_core_report() -> DoctorCoreReport:
                 _check(name, False, f"{attr} not found in {module}")
             else:
                 _check(name, True, f"{attr} available")
-        except Exception as exc:  # noqa: BLE001 — an import probe failure is that check's own result
+        except ImportError as exc:
             _check(name, False, _safe_err(exc))
 
     _try_import("worker_facade", "apps.cli.commands.worker_facade_cmd", "COMMAND_HANDLERS")
diff --git a/tests/test_ble001_ratchet.py b/tests/test_ble001_ratchet.py
index 1fa195707..e1cce97e9 100644
--- a/tests/test_ble001_ratchet.py
+++ b/tests/test_ble001_ratchet.py
@@ -18,7 +18,7 @@ REASONED = re.compile(r"^ — \S")
 
 #: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
 #: commit that removes a mark lowers this number in the same commit, and it is never raised.
-MAX_EXCUSED = 282
+MAX_EXCUSED = 281
 
```

- `run_defects.txt` verbatim:

```
NONE
```

## Closure suite

Quoting `.agent/authored/f078-closure-suite.txt` whole:

```
command: python3 -m pytest -n auto -q
real exit code: 1
wall time: 360.7s (the launcher's reading); pytest's own reported wall time: 360.08s (0:06:00)
summary line: 3 failed, 22185 passed, 11 skipped, 1 warning in 360.08s (0:06:00)
bad node ids (failed + errors):
  - tests/orchestration/test_agent_state_and_readiness.py::TestLiveReviewAndAgentStateRefs::test_context_md_no_stale_steps
  - tests/orchestration/test_event_names.py::TestTheEventVocabularyIsDeclared::test_every_written_event_name_is_declared
  - tests/orchestration/test_event_names.py::TestTheEventVocabularyIsDeclared::test_every_read_event_name_is_declared
leftover processes: NONE
tree it ran on: 239bfc93b (F078 R7 C4: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C4 changed only .agent/ files, the feature file, the checklist page and the self-use queue
reflog before: 239bfc93b HEAD@{2026-10-21 06:37:37 +0200}: commit: F078 R7 C4: the closure's self-use item run to its approval gate, never applied
reflog after: 239bfc93b HEAD@{2026-10-21 06:37:37 +0200}: commit: F078 R7 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F078 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1319.47 CPU seconds, 360.09 wall seconds, 22199 tests collected, exit status 1, recorded 2026-10-21T04:43:40Z
This closure's suite used 1319.47 CPU seconds, 1.1 percent more than F313's 1304.91, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F313's closure run:
  +5.57 s  tests/cli/test_do_scale_matrix.py (37.13 -> 42.70)
  +5.10 s  tests/cli/test_scoped_listings.py (10.09 -> 15.19)
  +3.33 s  tests/orchestration/test_self_use_generator.py (3.60 -> 6.93)
  +2.91 s  tests/orchestration/test_review_subject_artifact_integrity.py (1.96 -> 4.87)
  +2.71 s  tests/orchestration/test_run_manifest_call_task_binding.py (4.71 -> 7.42)
  +2.26 s  tests/orchestration/test_review_commit_chain.py (1.36 -> 3.62)
  +2.13 s  tests/orchestration/test_product_smoke.py (2.96 -> 5.09)
  +1.84 s  tests/orchestration/test_autonomy_seams.py (0.00 -> 1.84)
  +1.81 s  tests/orchestration/test_review_reports.py (2.14 -> 3.95)
  +1.77 s  tests/cli/test_do_several_projects.py (7.82 -> 9.59)
```

## Authored-text proofs

C1, C2, C3: each prepared file is a byte copy, proven by a Python equality over bytes at copy time (all True) and again by `verify.py` (all `True`). All prepared digests were checked before use and every one matched.

## Deviations & assumptions

- None in the commit sequence. The helpers `launch.py` and `wait.py` were run through a small wrapper script that sets the repository root as the working directory. The suite is RED (3 failed); per the block it was committed as read and nothing was investigated or re-run. Gate 4 exits 1 by design.

## For the operator, in plain sentences

Before a feature closes, Remedy runs one real piece of work on itself with a paid model, and then runs its whole test collection once on the code that will ship. The paid run was asked to narrow one overly broad error handler in a diagnostics command and lower the matching counter in a test, and it finished cleanly with the reviewer passing its single task, stopped at the approval gate and never applied. The whole test run passed 22185 tests and failed 3, and it took about six minutes. The cost reading said the computer time was about one percent above the previous feature, well inside the allowed margin.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. The reviewer reviews round 7, books its verdict and registers every self-use run defect in the next round's first commit.
4. A repair round naming every bad node id (the suite was red: the three nodes listed above).
5. The closing round: the STATUS line, the README and the pull request.

Operator questions open: 2.
Open findings: 87 (rule: `scripts.rotate_live_review.open_finding_ids` over `.agent/live_review.md`, gate 4 at commit `1287824bc`).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `1e0440d35` |
| C2 | done | `cd41569b3` |
| C3 | done | `867dc1d27` |
| C4 | done | `239bfc93b` |
| C5 | done | `1287824bc`, suite red as read |
| C6 | done | this commit |
| Gate 1 | done | ALL True |
| Gate 2 | done | ten files non-empty |
| Gate 3 | done | exit 1, 3 failed, 22185 passed |
| Gate 4 | done | fail_count 1, the twelve findings; 87 open |
