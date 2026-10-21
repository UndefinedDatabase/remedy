# Handback — F303 round 6: book round 5, R-1410, the self-use item, the Built State, the consolidation pass, and the one full suite

## Session

SESSION 2 of feature F303 · round 6 · rounds so far 6

Context self-assessment: this worker verified every prepared digest, byte-copied the prepared files, ran the self-use script and the suite once each through the launch and wait helpers, and wrote the transcript and this handback from what it read; context is ample and nothing was lost.

Fortschritt: ~85 % (T001 to T003 and the MCP facet landed; the self-use run, the consolidation pass and the one full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `0ff034c22`..`HEAD` on `feature/f303-face-public-api`.

## Commits

### 3a99cca4a F303 R6 C1: book round 5, register R-1410, the plan, the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f303-r6.md` | 172/0 | this round's block, byte copy (172 lines, sha256 `2a85797685807c0b13a79d18c6c3d15631a3a3b1d004bda9d9fdd4c04c7570c5`, equal to `block.md`) |
| `.agent/authored/f303-r6-selfuse.py` | 127/0 | prepared file, byte copy: the self-use script |
| `.agent/live_review.md` | 4/0 | prepared file, byte copy |
| `.agent/prose_slips.md` | 3/0 | prepared file, byte copy |
| `.agent/plan.md` | 6/7 | prepared file, byte copy |

### 2c32846e9 F303 R6 C2: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | 8/0 | the generator's one appended entry SU-072, `consumed_by` empty |
| `.agent/selfuse_f303/` | 10 files | NEW FILES: the run's record (sizes under Gate 2) |

### 39e60cfc4 F303 R6 C3: R-1410, a last line without ok is no envelope
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_mcp_tools.py` | 13/0 | one test added with a monkeypatched `subprocess.run`, plus the line `import subprocess` it needs (a new line, no existing line changed) |

### 36931cb3d F303 R6 C4: F303's Built State
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T12_F303.md` | 45/0 | prepared file, byte copy |

### 9595d5607 F303 R6 C5: the checklist's consolidation pass for F303
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | 13/0 | prepared file, byte copy (`git show --numstat` read `13	0`) |

### c07eb552c F303 R6 C6: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f303-closure-suite.txt` | 26/0 | NEW FILE: the suite transcript and the cost reading |

### (this commit) F303 R6 C7: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## External actions

- `git push origin feature/f303-face-public-api` follows this commit; its outcome is in the session reply.
- Provider calls: the self-use run of C2 only (four calls, see below). No pull request, no merge, no worktree of my own (the script added and removed its own temporary one), no `gh` command.

## Verification

Preconditions: the five prepared digests and the c1/c4/c5 digests matched; the saved block and `block.md` both read 172 lines and the sha256 above. Before the first write `HEAD` was `0ff034c22`, equal to `origin/feature/f303-face-public-api`, the tree was clean and `.agent/STOP` was absent.

1. Gate 1: `git status --porcelain` empty. `python3 .remedy-wt/f303-r6/prep/verify.py .` — every line `True`, `absent` for C7, last line `ALL True`.
2. Gate 2: the ten files under `.agent/selfuse_f303/`, bytes: `SU-072.md` 2025, `entry_and_job_file.txt` 224, `execution_config.txt` 1367, `result_state.txt` 857, `timing.txt` 105, `changed_paths.txt` 35, `full_transcript.txt` 1543, `staleness_after.txt` 200, `job_diff.txt` 860, `run_defects.txt` 5. All non-empty.
3. Gate 3: the suite of C6: exit code 0; summary line `23044 passed, 11 skipped, 1 warning in 349.69s (0:05:49)`; bad node ids NONE; data root guard NONE (no `R-0803:` line); leftover processes NONE.
4. Gate 4: `python3 -m apps.cli.main integrity check --json` exit 1 — `fail_count` 1, the one failing check `high_blockers_open`: "12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362", the other five checks pass. `open_finding_ids` over `.agent/live_review.md` prints `92`.

C3's own run: `python3 -m pytest -q tests/orchestration/test_mcp_tools.py` — `24 passed in 1.26s`.

## Authored-text proofs

C1's five files and C4's and C5's files are byte copies of the prepared files; each was proved equal by a Python equality over bytes right after the copy, and `verify.py` re-proved them (`True`). `.agent/authored/f303-r6.md` equals `block.md` (172 lines, sha256 `2a85797685807c0b13a79d18c6c3d15631a3a3b1d004bda9d9fdd4c04c7570c5`).

## Self-use run

- Entry id: `SU-072`. Title: `Address ledger finding R-1407`. Job id: `fa8071ff5aa24f46`.
- Builder: `claude-cli`, model `claude-sonnet-4-6`, effort medium. Reviewer: `claude-cli`, model `claude-sonnet-4-6`, effort medium (`execution_config.txt`).
- Job state `completed`; stop reason empty. Task `T001`: status `applied_to_job_workspace`, reviewer verdict `pass`, final status `staged_review_passed`, repair rounds used 1.
- Wall seconds (`timing.txt`): 669.6. Provider calls 4, measured cost within the job's declared budget (max 8 calls).
- Changed paths (`changed_paths.txt`): `tests/cli/test_client_interface.py`.
- `staleness_after.txt` (read from the job branch): `docs_index_guide_registration | docs/README.md | the Guides section has no link to `guides/http-clients.md` | `docs/guides/http-clients.md` ships`.

`job_diff.txt` verbatim:

```
$ git diff HEAD...remedy/job-fa8071ff5aa24f46  (exit 0)
diff --git a/tests/cli/test_client_interface.py b/tests/cli/test_client_interface.py
index 2d4fe0599..fb43446a1 100644
--- a/tests/cli/test_client_interface.py
+++ b/tests/cli/test_client_interface.py
@@ -768,6 +768,8 @@ def test_the_hand_verified_answer_key_sets_still_equal_what_their_code_names():
         | _stored_keys("apps/cli/commands/job.py", "_cmd_resume", "_payload"))
     assert sites["apps.cli.commands.job:_cmd_resume:**export_dry_run_json(dr)"] == (
         _returned_dict_keys("packages/orchestration/event_replay.py", "export_dry_run_json"))
+    assert sites["apps.cli.commands.job_steer_cmd:_cmd_job_steer:**result"] == (
+        _returned_dict_keys("packages/orchestration/steering.py", "steer_task_command"))
 
 
 # The keys under the answers' top-level keys (DECISION F298 D8).
```

`run_defects.txt` verbatim:

```
NONE
```

No finding is registered by this worker.

## Closure suite

Verbatim `.agent/authored/f303-closure-suite.txt`:

```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 350.6s (the launcher's reading); pytest's own reported wall time: 349.69s (0:05:49)
summary line: 23044 passed, 11 skipped, 1 warning in 349.69s (0:05:49)
bad node ids (failed + errors): NONE
leftover processes: NONE
data root guard: NONE
tree it ran on: 9595d5607 (F303 R6 C5: the checklist's consolidation pass for F303)
tree note: C1, C2, C4 and C5 changed only .agent/ files, the self-use queue, the feature file and the checklist page; C3 added one test
reflog before: 9595d5607 HEAD@{2026-10-21 17:59:55 +0200}: commit: F303 R6 C5: the checklist's consolidation pass for F303
reflog after: 9595d5607 HEAD@{2026-10-21 17:59:55 +0200}: commit: F303 R6 C5: the checklist's consolidation pass for F303
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F303 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1319.51 CPU seconds, 349.70 wall seconds, 23055 tests collected, exit status 0, recorded 2026-10-21T16:05:47Z
This closure's suite used 1319.51 CPU seconds, 0.6 percent more than F060's 1311.49, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F060's closure run:
  +2.86 s  tests/ui_server/test_public_api.py (13.97 -> 16.83)
  +2.28 s  tests/cli/test_client_mcp_cmd.py (0.00 -> 2.28)
  +2.23 s  tests/runtimes/test_supervisor_portability.py (46.97 -> 49.20)
  +2.19 s  tests/orchestration/test_serve_daemon.py (21.35 -> 23.54)
  +2.06 s  tests/cli/test_do_several_projects.py (8.72 -> 10.78)
  +1.76 s  tests/orchestration/test_run_manifest_integrity.py (4.49 -> 6.25)
  +1.74 s  tests/cli/test_do_scale_matrix.py (37.43 -> 39.17)
  +1.70 s  tests/orchestration/test_review_zip_hygiene.py (36.72 -> 38.42)
  +1.29 s  tests/orchestration/test_review_single_publication.py (3.82 -> 5.11)
  +1.22 s  tests/cli/test_do_evidence_package.py (4.59 -> 5.81)
```

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | script exit 0, queue diff one appended entry SU-072 with empty `consumed_by` |
| C3 | done | one test and the `import subprocess` line it needs |
| C4 | done | |
| C5 | done | numstat `13 0` |
| C6 | done | suite green, cost exit 0 |
| C7 | done | this handback |
| Gate 1 | done | ALL True |
| Gate 2 | done | ten non-empty files |
| Gate 3 | done | green, no bad node |
| Gate 4 | done | fail_count 1 (twelve high blockers), 92 open |

## Deviations & assumptions

- C3 also adds the line `import subprocess` at the top of the test file (the block says one test is added and no existing line changed; the import is a new line and no existing line changed, but it is not inside the test). The test passed on first run: production code already refused a last line without `ok`.
- The cost script's exit code was read as 0 from the shell reporting no error; no separate `echo $?` was run.
- Otherwise none.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Rule 2: Open PR Gate; no pull request is open for this branch yet.
3. The reviewer reviews round 6, books its verdict, resolves R-1329 and R-1407 to R-1410 and registers every self-use run defect in the next round's first commit.
4. The evidence bundle and the review package (the suite is green).
5. The closing round: the STATUS line, the README and the pull request.

Operator questions open: 0
Open findings: 92 (gate 4: `open_finding_ids` over `.agent/live_review.md`, at commit c07eb552c)

## For the operator, in plain sentences

Before a feature closes, Remedy runs one real piece of work on itself with a paid model, and then runs its whole test collection once on the code that will ship. The paid run was asked to repair a small recorded flaw: a test did not hold one command's published answer to what its code returns; it added the missing check, passed its reviewer after one repair round, and was stopped at the approval step, never applied. The whole collection ran 23044 tests with none failing and 11 skipped. The run took about six minutes. The cost reading said the computer time was 0.6 percent above the previous feature's, well inside the allowed 10 percent.
