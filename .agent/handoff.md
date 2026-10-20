# Handoff — F310 round 5 (the integration-gate round: Built State, consolidation, self-use run, one full suite)

## Session

SESSION 1 of feature F310 · round 5 · rounds so far 5

Context self-assessment: the session stayed small; every prepared file was digest-checked with a Python reader before use, copies were made by script, and the two long commands ran once each.

State block:
Feature F310 (claimed `[~]`), branch `feature/f310-provider-budgets`, base `b8b4a9546`.
Fortschritt: ~90 % (T001 to T004 landed; the consolidation pass, the self-use run and the one full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `b8b4a9546`..HEAD (the five commits below, then this handback's own commit).

## Commits

### 1cc06950f F310 R5 C1: book round 4, resolve R-1370 R-1371 R-1373 R-1374, register R-1375, DECISION F310 D7
327 insertions, 9 deletions.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f310-r5.md` | +166 | byte copy of the block |
| `.agent/authored/f310-r5-selfuse.py` | +127 | byte copy of the self-use script |
| `.agent/plan.md` | +10/-9 | byte copy of the prepared plan |
| `.agent/live_review.md` | +12 | appended ledger text |
| `.agent/prose_slips.md` | +2 | appended slips |
| `.agent/decisions.md` | +10 | appended DECISION F310 D7 |

### 370251a81 F310 R5 C2: F310's Built State
37 insertions.
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T12_F310.md` | +37 | the Built State appended |

### 273ed22c6 F310 R5 C3: the checklist's consolidation pass for F310
13 insertions.
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +13 | the consolidation paragraph before the next-consolidation line |

### 9c072b916 F310 R5 C4: the closure's self-use item run to its approval gate, never applied
115 insertions.
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8 | the one generated entry SU-065, `consumed_by` empty |
| `.agent/selfuse_f310/` | +107 | 10 files under this directory |

### 56187b7b0 F310 R5 C5: the closure's one full suite and its CPU cost
28 insertions.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f310-closure-suite.txt` | +28 | the transcript, written as read (suite RED) |

### this handback's commit (C6)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file |
| `.agent/operator_questions.md` | +17 | one empty line and Q20 appended |

## External actions

- `git push origin feature/f310-provider-budgets` after C6; the result is in the worker's report.
- The self-use run made two real provider calls through the claude-cli provider (budgeted).
- No pull request opened; no other gh command.

## Verification

1. Gate 1: `git status --porcelain` printed nothing. `python3 .remedy-wt/f310-r5/prep/verify.py .` (at `56187b7b0`): every line `True`, `absent` for C6, last line `ALL True`.
2. Gate 2: the ten files under `.agent/selfuse_f310/`, all non-empty, bytes: `SU-065.md` 658, `entry_and_job_file.txt` 366, `execution_config.txt` 1367, `result_state.txt` 866, `timing.txt` 104, `changed_paths.txt` 15, `full_transcript.txt` 1586, `staleness_after.txt` 59, `job_diff.txt` 1219, `run_defects.txt` 5.
3. Gate 3: the suite of C5: exit code 1; summary line `1 failed, 21988 passed, 11 skipped, 1 warning in 305.15s (0:05:05)`; bad node id `tests/orchestration/test_public_api_gate_paths.py::test_f295s_gate_path_runs_from_the_order_to_the_proof_over_http_alone`. The failure: `assert len(remainder) == 1` at `tests/orchestration/test_public_api_gate_paths.py:286` got 0 (`remainder` is the digest's `task_decision` entries for the stopped job).
4. Gate 4: `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing check `high_blockers_open`: `13 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362, R-1369` (the same thirteen as at the base). `open_finding_ids` over the ledger: `86`.

## Authored-text proofs

Byte copies and appends made by script from the digest-checked prepared files (all twelve digests matched before use); `verify.py` after C5 confirms C1 (block, self-use script, plan, the three appends), C2 and C3 equal their sources. C6's `operator_questions.md` append is one empty line plus the bytes of `src-question.md`.

## Self-use run

- Entry id: `SU-065`; title: `Fix stale documentation: docs_index_guide_registration in docs/README.md`; job id: `ad990252606040b2`.
- Builder: `claude-cli`, model `claude-sonnet-4-6`; reviewer: `claude-cli`, model `claude-sonnet-4-6`.
- Job state `completed`; stop reason empty.
- Task T001: `applied_to_job_workspace`, reviewer verdict `pass`, final status `staged_review_passed`, repair rounds used 0.
- Wall seconds (`timing.txt`): 37.7.
- Changed paths: `docs/README.md`.

`job_diff.txt` verbatim:

```
$ git diff HEAD...remedy/job-ad990252606040b2  (exit 0)
diff --git a/docs/README.md b/docs/README.md
index b11482934..4cf43d72f 100644
--- a/docs/README.md
+++ b/docs/README.md
@@ -167,6 +167,7 @@ User-facing guides, quickstarts, and usage documentation.
 | [environment.md](guides/environment.md) | Every environment variable Remedy reads, generated from the key registry |
 | [exit-codes.md](guides/exit-codes.md) | Every CLI exit code's meaning, asserted from the command catalog |
 | [hunk-approval-user-guide-v1.md](guides/hunk-approval-user-guide-v1.md) | Recording a hunk-level approve and reject decision over a job's diff |
+| [http-clients.md](guides/http-clients.md) | Walking a program through the public HTTP API with `curl`: token, start an order, poll, read the story, apply or decline |
 | [job-context-view-user-guide-v0.md](guides/job-context-view-user-guide-v0.md) | What one task's compiled context carries and what was omitted |
 | [real-test-execution-snapshot-rollback-user-guide-v1.md](guides/real-test-execution-snapshot-rollback-user-guide-v1.md) | Test execution + snapshot/rollback usage |
 | [remedy-toml-user-guide.md](guides/remedy-toml-user-guide.md) | remedy.toml configuration guide |
```

`run_defects.txt` verbatim:

```
NONE
```

## Closure suite

Quoting `.agent/authored/f310-closure-suite.txt` whole:

```
command: python3 -m pytest -n auto -q
real exit code: 1
wall time: 305.8s (the launcher's reading); pytest's own reported wall time: 305.15s (0:05:05)
summary line: 1 failed, 21988 passed, 11 skipped, 1 warning in 305.15s (0:05:05)
bad node ids (failed + errors):
  - tests/orchestration/test_public_api_gate_paths.py::test_f295s_gate_path_runs_from_the_order_to_the_proof_over_http_alone
leftover processes: NONE
tree it ran on: 9c072b916 (F310 R5 C4: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C4 changed only .agent/ files, the feature file, the checklist page and the self-use queue
reflog before: 9c072b916 HEAD@{2026-10-20 21:20:18 +0200}: commit: F310 R5 C4: the closure's self-use item run to its approval gate, never applied
reflog after: 9c072b916 HEAD@{2026-10-20 21:20:18 +0200}: commit: F310 R5 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F310 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1201.66 CPU seconds, 305.16 wall seconds, 22000 tests collected, exit status 1, recorded 2026-10-20T19:25:26Z
This closure's suite used 1201.66 CPU seconds, 6.1 percent less than F055's 1279.63, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F055's closure run:
  +38.09 s  tests/cli/test_do_scale_matrix.py (0.00 -> 38.09)
  +10.56 s  tests/cli/test_do_adversarial_orders.py (0.00 -> 10.56)
  +7.75 s  tests/ui_server/test_public_api_lifecycle.py (0.00 -> 7.75)
  +7.72 s  tests/orchestration/test_client_story.py (0.00 -> 7.72)
  +7.29 s  tests/orchestration/test_event_name_coupling.py (13.13 -> 20.42)
  +5.37 s  tests/cli/test_do_order_budget.py (0.00 -> 5.37)
  +5.24 s  tests/cli/test_do_bounded_lane.py (0.00 -> 5.24)
  +4.82 s  tests/orchestration/test_order_cancel.py (0.00 -> 4.82)
  +4.43 s  tests/cli/test_do_pi_default.py (0.00 -> 4.43)
  +4.09 s  tests/cli/test_do_verified_repair.py (0.00 -> 4.09)
```

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | self-use run exit 0, SU-065 ran to its approval gate, never applied |
| C5 | done | suite RED (one failed node), transcript committed as read |
| C6 | done | this commit |
| Gate 1 | done | ALL True |
| Gate 2 | done | ten files non-empty |
| Gate 3 | done | exit 1, one bad node id |
| Gate 4 | done | fail_count 1, the standing thirteen; open findings 86 |

## Deviations & assumptions

None. The suite was red; per the block it was committed as read and nothing was investigated or re-run. I did not read the diff of the byte-copy commits line by line, only their `--stat`, since `verify.py` proves them equal to their sources.

## For the operator, in plain sentences

Before a feature closes, Remedy runs one real piece of work on itself with a paid model, and then runs its whole test collection once on the code that will ship. The paid run was asked to add a missing link to a guide in the documentation index, and it finished that in under a minute with its reviewer passing the change, which was left unapplied for approval. The test run passed 21,988 tests, skipped 11 and failed 1, so the code that will ship is not yet green. The run took about five minutes, and the cost reading said the computer time was about 6 percent lower than for the previous feature, within the allowed limit.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`); rule 2 (Open PR Gate; no pull request is open for this branch yet); the reviewer reviews round 5, books its verdict and registers every self-use run defect in the next round's first commit; a repair round naming every bad node id (`tests/orchestration/test_public_api_gate_paths.py::test_f295s_gate_path_runs_from_the_order_to_the_proof_over_http_alone`); the closing round: the rotation, the STATUS line, the README and the pull request.
Operator questions open: 2. Open findings: 86 (gate 4, `open_finding_ids`, rule: the base's 89, less R-1370, R-1371, R-1373 and R-1374 resolved, plus R-1375; read at `56187b7b0`).
