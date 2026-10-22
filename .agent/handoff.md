# Handback — F113 round 4: book round 3, T003c on real runs, the consolidation pass, the self-use item, and the one full suite

## Session

SESSION 1 of feature F113 · round 4 · rounds so far 4

Context self-assessment: this worker verified the block and every prepared digest before any write, copied each prepared file by a script with a byte-for-byte proof, ran the self-use job and the suite once each through the launcher, and context stayed ample throughout.

Fortschritt: ~80 % (T001 to T003c landed; the consolidation pass, the self-use run and the one full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `531e22e00`..`HEAD` on `feature/f113-local-side-roles`.

## Commits

### 57e45e11f F113 R4 C1: book round 3, the plan, the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f113-r4.md` | +162/-0 | NEW FILE, this round's block, byte copy equal to `block.md` (162 lines, sha256 `91387a08...5544bb8`, equal to the prompt's) |
| `.agent/authored/f113-r4-selfuse.py` | +127/-0 | NEW FILE, the self-use script |
| `.agent/live_review.md` | +2/-0 | round 3's verdict booked |
| `.agent/plan.md` | +5/-5 | rewritten for round 4 |

Total 296 insertions, 5 deletions, under 500.

### c0a020b61 F113 R4 C2: the Acceptance held on real runs of the build-and-review loop
| Path | +/- | Reason |
|---|---|---|
| `tests/regression/test_f113_acceptance.py` | +183/-0 | NEW FILE |
| `docs/system/local-side-roles-v1.md` | +3/-2 | the status banner names the acceptance test |

Total 186 insertions, 2 deletions, under 500.

### eed7db5be F113 R4 C3: the checklist's consolidation pass for F113
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +4/-0 | the consolidation paragraph (numstat `4	0`) |

### 908d30689 F113 R4 C4: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | the one appended entry SU-075, empty `consumed_by` |
| `.agent/selfuse_f113/` | +126/-0 | 10 NEW FILES, the run's record |

Total 134 insertions, under 500.

### 74dd07fe2 F113 R4 C5: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f113-closure-suite.txt` | +26/-0 | NEW FILE, the transcript |

### (this commit) F113 R4 C6: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback (a handoff cannot table the commit that writes it) |

## Item status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD `531e22e00` equal to origin, status empty, no `.agent/STOP`, open PR list `[]`, branch as ordered |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this commit |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | |

## External actions

- `python3 .remedy-wt/f113-r4/prep/launch.py selfuse` and `wait.py`: one real self-use run through the `self_use` role's provider, exit 0, wall 65.4 s.
- `python3 .remedy-wt/f113-r4/prep/launch.py suite` and `wait.py`: the one full suite, exit 0, wall 362.6 s.
- `python3 scripts/closure_suite_cost.py --feature F113 --record ~/.remedy-loop/test_load.jsonl`: exit 0.
- `git push origin feature/f113-local-side-roles`: after this commit (outcome in the worker's reply).
- No pull request created, no `gh` write.

## Verification

Gate 1: `git status --porcelain` printed nothing; `python3 .remedy-wt/f113-r4/prep/verify.py .` exit 0, every line `True` (C6 `absent` at that moment), last line `ALL True`.

Gate 2: the ten files under `.agent/selfuse_f113/`, all non-empty, bytes: `SU-075.md` 1079, `entry_and_job_file.txt` 405, `execution_config.txt` 1367, `result_state.txt` 866, `timing.txt` 104, `changed_paths.txt` 68, `full_transcript.txt` 1586, `staleness_after.txt` 200, `job_diff.txt` 1267, `run_defects.txt` 5.

Gate 3: the suite of C5: exit code 0, `23353 passed, 11 skipped, 1 warning in 361.64s (0:06:01)`, bad node ids NONE.

Gate 4: `python3 -m apps.cli.main integrity check --json` exit 0, `"fail_count": 0`; checks: handler_import pass, live_review_verdict pass, plan_consistency pass, relevant_untracked pass, repo_root_hygiene pass, high_blockers_open pass. `open_finding_ids` printed `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421']` (7 open findings).

## Self-use run

- Entry id: SU-075; title: "Narrow the excused handler at apps/cli/commands/worker_facade_cmd.py:352".
- Job id: 15154c7ee5cd42f7.
- Builder: claude-cli, model claude-sonnet-4-6. Reviewer: claude-cli, model claude-sonnet-4-6.
- Job state: completed; stop reason: (empty).
- Task statuses: T001: applied_to_job_workspace, reviewer verdict pass (final_status staged_review_passed, repair_rounds_used 0).
- Wall seconds: 61.0.
- Changed paths: `apps/cli/commands/worker_facade_cmd.py`, `tests/test_ble001_ratchet.py`.

Job diff (`job_diff.txt`, verbatim):

```
$ git diff HEAD...remedy/job-15154c7ee5cd42f7  (exit 0)
diff --git a/apps/cli/commands/worker_facade_cmd.py b/apps/cli/commands/worker_facade_cmd.py
index c22649d44..0e2fcdc91 100644
--- a/apps/cli/commands/worker_facade_cmd.py
+++ b/apps/cli/commands/worker_facade_cmd.py
@@ -349,7 +349,7 @@ def doctor_core_report() -> DoctorCoreReport:
                f"{len(shipped_entries)} shipped + "
                f"{len(dead_ids) - len(shipped_entries)} config-only dead ids "
                f"({len(dead_ids)} total)")
-    except Exception as exc:  # noqa: BLE001 — a dead-model-list read failure is its own check result
+    except (ImportError, RuntimeError) as exc:
         _check("dead_model_list", False, report_safe_text(exc, limit=120))
 
     if dead_ids:
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

`run_defects.txt` (verbatim):

```
NONE
```

No finding registered by the worker.

## Closure suite

Quoting `.agent/authored/f113-closure-suite.txt`, whole:

```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 362.6s (the launcher's reading); pytest's own reported wall time: 361.64s (0:06:01)
summary line: 23353 passed, 11 skipped, 1 warning in 361.64s (0:06:01)
bad node ids (failed + errors):
  - NONE
leftover processes: NONE
tree it ran on: 908d30689 (F113 R4 C4: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C4 changed only .agent/ files, the acceptance test, the local side roles page, the checklist page and the self-use queue
reflog before: 908d30689 HEAD@{2026-10-22 10:08:32 +0200}: commit: F113 R4 C4: the closure's self-use item run to its approval gate, never applied
reflog after: 908d30689 HEAD@{2026-10-22 10:08:32 +0200}: commit: F113 R4 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F113 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1347.63 CPU seconds, 361.65 wall seconds, 23364 tests collected, exit status 0, recorded 2026-10-22T08:14:42Z
This closure's suite used 1347.63 CPU seconds, 1.6 percent less than F296's 1369.23, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F296's closure run:
  +6.83 s  tests/cli/test_do_sequence_cli.py (31.51 -> 38.34)
  +4.56 s  tests/test_grouped_cli.py (24.51 -> 29.07)
  +2.79 s  tests/orchestration/test_token_ledger.py (7.66 -> 10.45)
  +2.59 s  tests/orchestration/test_self_use_generator.py (4.59 -> 7.18)
  +2.49 s  tests/orchestration/test_stream_export_e2e.py (3.19 -> 5.68)
  +1.87 s  tests/test_command_discovery.py (6.53 -> 8.40)
  +1.85 s  tests/cli/test_test_run_runtime.py (8.33 -> 10.18)
  +1.64 s  tests/cli/test_mission_cmd.py (46.42 -> 48.06)
  +1.49 s  tests/serve_http_handler/test_subtree_rerun_e2e_live.py (5.12 -> 6.61)
  +1.30 s  tests/orchestration/test_event_name_coupling.py (16.11 -> 17.41)
```

## Authored-text proofs

The prepared files of C1, C2 and C3 were copied by a Python byte copy and proven equal over bytes at copy time; `verify.py` re-proved each against the commit (gate 1, all `True`). `block.md` equals the saved `.agent/authored/f113-r4.md`.

## Deviations & assumptions

None. (One shell call of mine that began with a directory change was refused by the sandbox before it ran anything; the same steps were then run without it. The suite run printed a notice that two entries of the configured data root changed in supervisor-written folders and were not counted; the suite still exited 0 with no leftover-process line.)

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2 (Open PR Gate); no pull request is open for this branch yet.
3. The reviewer reviews round 4, books its verdict and registers every self-use run defect in the next round's first commit.
4. The evidence bundle and the review package (the suite is green).
5. The closing round: the Built State, the rotation, the STATUS line, the README and the pull request.

Operator questions open: 0. Open findings (gate 4): 7.

## For the operator, in plain sentences

Before a feature closes, Remedy runs one real piece of work on itself with a paid model, and then runs its whole test collection once on the code that will ship. The paid run was asked to narrow one overly broad error handler in a diagnostic check and lower the matching counter, and it finished with the reviewing model passing the change and nothing applied. The whole collection ran 23353 tests that passed, none failed, 11 were skipped, and it took about six minutes. The cost reading said the computer time was about 1.6 percent lower than for the previous feature, well within the allowed margin. Remedy can now send its summaries to a model server on the operator's own machine, it refuses to send the building, reviewing or planning work there, and a fixed test switches a poor server off.
