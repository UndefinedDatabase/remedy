# Handback — F055 round 4 — book round 3, repair R-1318, the consolidation pass, the self-use item, and the one full suite

## Session

SESSION 1 of feature F055 · round 4 · rounds so far 4

Context self-assessment: C1 to C6 landed clean on the first attempt, every gate came back green
on the one run that counts, and the context budget stayed comfortable throughout — no retries,
no stale reads, no amendment needed.

Fortschritt: ~85 % (T001 to T003 landed; the consolidation pass, the self-use run and the one full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `a2a0c20ad`..`f276ad48e` (then this commit).

## Commits

### `45bb3dde9` F055 R4 C1: book round 3, resolve R-1317, register R-1318, save the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-r4-selfuse.py` | +122/-0 | NEW: byte copy of `selfuse.py` |
| `.agent/authored/f055-r4.md` | +171/-0 | NEW: byte copy of `block.md` |
| `.agent/live_review.md` | +6/-0 | byte copy of `dry-live_review.md` (round 3 booked PASS, R-1317 resolved, R-1318 registered) |
| `.agent/plan.md` | +6/-5 | byte copy of `dry-plan.md` |
| `.agent/prose_slips.md` | +1/-0 | byte copy of `dry-prose_slips.md` (round 3 slip appended) |

### `9dca5e9cd` F055 R4 C2: the planning counter is shown to count (R-1318)
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_rehearsal.py` | +28/-0 | NEW test: installs `_setup_llm_mocks` before `count_planning_calls` wraps `job_plan.plan_job_llm`, so nothing re-patches the counting wrapper away, then rehearses an order on the planner's branch and asserts `counts["plan_job_llm"] > 0` |

### `b43eee568` F055 R4 C3: the checklist's consolidation pass for F055
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +15/-0 | byte copy of `dry-planner_reviewer_prompt.md`: F055's consolidation paragraph, nothing joined, no two items merged, the list stays at 34 items |

### `71305a2c7` F055 R4 C4: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `.agent/selfuse_f055/SU-064.md` | +17/-0 | NEW: the job's own markdown, copied from the job file path `run_next_self_use_item` returned |
| `.agent/selfuse_f055/changed_paths.txt` | +2/-0 | NEW: the two paths the job's task changed |
| `.agent/selfuse_f055/entry_and_job_file.txt` | +5/-0 | NEW: entry id/title/provenance/consumed_by and the job file path |
| `.agent/selfuse_f055/execution_config.txt` | +43/-0 | NEW: the plan's `execution_config`, JSON, sorted keys |
| `.agent/selfuse_f055/full_transcript.txt` | +14/-0 | NEW: job id/title/state/stop reason/stop source, execution, per-task summary |
| `.agent/selfuse_f055/job_diff.txt` | +32/-0 | NEW: `git diff HEAD...remedy/job-3d8b8562cbc64f34`, verbatim |
| `.agent/selfuse_f055/result_state.txt` | +12/-0 | NEW: job id/state/stop reason/source/error, budgets, budget actuals, workspace path, per-task state |
| `.agent/selfuse_f055/run_defects.txt` | +1/-0 | NEW: `describe_self_use_run_defects(plan)` — empty, so `NONE` |
| `.agent/selfuse_f055/staleness_after.txt` | +2/-0 | NEW: the staleness catalog read from the job branch (no workspace left to read) |
| `.agent/selfuse_f055/timing.txt` | +3/-0 | NEW: started/finished timestamps and wall seconds |
| `scripts/self_use_queue.json` | +8/-0 | `generate_and_append_if_empty()`'s one appended entry, `SU-064`, `consumed_by` empty |

### `f276ad48e` F055 R4 C5: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-closure-suite.txt` | +28/-0 | NEW: the suite transcript in the shape of `f308-closure-suite.txt` — exit 0, `23067 passed, 22 skipped`, `NONE` bad node ids, `NONE` leftover processes, the cost script's reading (9.7 percent more CPU than F308's, within the 14.1 percent limit) |

### (this commit) F055 R4 C6: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | rewritten |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` (read-only, checked
  before writing this handback): `[]` — no open pull request for this branch.
- No branch created this round: preconditions held at the start — `HEAD` and
  `origin/feature/f055-rehearsal` both `a2a0c20ad`, `git status --porcelain` empty, no
  `.agent/STOP`.
- `python3 launch.py selfuse ...` then `python3 wait.py selfuse ... 50` (C4): started the
  reviewer-prepared wrapper detached, waited for `selfuse.exit`, got `exit 0 wall 178.8`.
  Inside that run, `selfuse.py` itself added and removed one detached worktree at
  `.remedy-wt/f055-r4-jobtree` (pointed at `remedy/job-3d8b8562cbc64f34`, to read the job
  branch's staleness catalog once the runner had already removed the job's own workspace), and
  removed it again before exiting; nothing under that path remains.
- `python3 launch.py suite ...` then `python3 wait.py suite ... 50` (C5): started the suite
  wrapper detached, waited for `suite.exit`, got `exit 0 wall 374.4`.
- `python3 scripts/closure_suite_cost.py --feature F055 --record ~/.remedy-loop/test_load.jsonl`
  (C5): exit 0, reading quoted verbatim in the Closure suite section below.
- Push after C6 follows this commit: `git push origin feature/f055-rehearsal`; its outcome is
  reported in the session's final reply only — it does not exist yet when this file is written.
- No `gh pr merge`, `gh pr edit`, `gh pr create`, no STATUS edit, no ledger rotation — none
  ordered by this block. The one real provider call budget spent this round is C4's self-use
  run (`actual_call_count: 2`, `measured_cost_usd: 0.6761364`, `total_tokens: 11577`); no other
  provider call was made.

## Verification

**Digests verified before anything else**: `block.md` 171 lines /
`b886bdf1c0654eaa8bbca0b21f7f1a22aa13451fcd96099b5d9952b039670a8d` — matched. All eight prepared
files' sha256 (`dry-live_review.md`, `dry-prose_slips.md`, `dry-plan.md`,
`dry-planner_reviewer_prompt.md`, `selfuse.py`, `launch.py`, `wait.py`, `verify.py`) matched the
digests given in the prompt, checked with a Python sha256 reader before use.

**C2's one-file test run** (block's own exception — "not the round's test run"):
`python3 -m pytest tests/cli/test_rehearsal.py -q` while writing the test — `18 passed in
14.48s`, exit 0.

**Gate 1** — `git -C /home/decodeux/Repos/remedy status --porcelain` empty, then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f055-r4/prep/verify.py /home/decodeux/Repos/remedy`:
```
True 45bb3dde9 has the single parent a2a0c20ad (F055 R4 C1)
True 9dca5e9cd has the single parent 45bb3dde9 (F055 R4 C2)
True b43eee568 has the single parent 9dca5e9cd (F055 R4 C3)
True 71305a2c7 has the single parent b43eee568 (F055 R4 C4)
True f276ad48e has the single parent 71305a2c7 (F055 R4 C5)
True exactly one commit with the subject prefix F055 R4 C1
True exactly one commit with the subject prefix F055 R4 C2
True exactly one commit with the subject prefix F055 R4 C3
True exactly one commit with the subject prefix F055 R4 C4
True exactly one commit with the subject prefix F055 R4 C5
True the range holds C1 to C5 and at most C6 (5)
True C1 .agent/authored/f055-r4.md equals block.md
True C1 .agent/authored/f055-r4-selfuse.py equals selfuse.py
True C1 .agent/live_review.md equals dry-live_review.md
True C1 .agent/prose_slips.md equals dry-prose_slips.md
True C1 .agent/plan.md equals dry-plan.md
True C1 names exactly its paths []
True C3 docs/agents/planner_reviewer_prompt.md equals dry-planner_reviewer_prompt.md
True C3 names exactly its paths []
True C2 names only tests/cli/test_rehearsal.py ['tests/cli/test_rehearsal.py']
True C2's test reads plan_job_llm above zero on the counter
True C4 names the queue and the self-use folder only ['scripts/self_use_queue.json']
True C4 adds ten self-use files (10)
True C5 names only the transcript ['.agent/authored/f055-closure-suite.txt']
ALL True
```
One run, green.

**Gate 2** — the ten files under `.agent/selfuse_f055/`, each non-empty (bytes):
`SU-064.md` 1033, `changed_paths.txt` 61, `entry_and_job_file.txt` 395,
`execution_config.txt` 1367, `full_transcript.txt` 1578, `job_diff.txt` 1335,
`result_state.txt` 801, `run_defects.txt` 5, `staleness_after.txt` 59, `timing.txt` 105.

**Gate 3** — the suite of C5 itself: exit code 0, summary line
`23067 passed, 22 skipped, 1 warning in 373.62s (0:06:13)`, bad node ids `NONE`, as the
transcript records.

**Gate 4** — `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Then
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
```
['R-1246', 'R-1276', 'R-1277', 'R-1278', 'R-1279', 'R-1280', 'R-1281', 'R-1282', 'R-1283', 'R-1284', 'R-1285', 'R-1286', 'R-1287', 'R-1288', 'R-1289', 'R-1290', 'R-1291', 'R-1292', 'R-1293', 'R-1294', 'R-1295', 'R-1296', 'R-1297', 'R-1298', 'R-1299', 'R-1300', 'R-1301', 'R-1302', 'R-1303', 'R-1304', 'R-1305', 'R-1306', 'R-1307', 'R-1308', 'R-1309', 'R-1310', 'R-1311', 'R-1312', 'R-1313', 'R-1318']
```
40 ids: `R-1246`, then `R-1276` to `R-1313`, then `R-1318`, in order, as required.

**Gate 5** — after the push (reported in the reply only — see Next for the one line this file
cannot yet carry).

## Authored-text proofs

`.agent/authored/f055-r4.md` against `block.md`: byte-identical, sha256
`b886bdf1c0654eaa8bbca0b21f7f1a22aa13451fcd96099b5d9952b039670a8d`, confirmed by my own copy
script at write time and again independently by `verify.py`'s Gate 1 (`git show <C1>:<path>`
compared to the prep file's bytes — `True`). `.agent/authored/f055-r4-selfuse.py` against
`selfuse.py`: byte-identical, confirmed the same two ways. `docs/agents/planner_reviewer_prompt.md`
against `dry-planner_reviewer_prompt.md` (C3): byte-identical, confirmed the same two ways, and
`git show --numstat` on `b43eee568` read exactly `15\t0`, matching the block's own stated count.
The three remaining `dry-*.md` copies applied in C1 (`live_review.md`, `prose_slips.md`,
`plan.md`) were each confirmed byte-equal by a Python equality check at copy time (printed `True`
for all five C1 paths together) and again by Gate 1's per-path check. No other reviewer-authored
text was applied this round.

## Self-use run

Entry `SU-064`, "Narrow the excused handler at apps/cli/commands/status_cmd.py:96"
(generated — self-use-generator tier 4, excused handler). Job id `3d8b8562cbc64f34`. Builder:
`claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source `cli`); reviewer: `claude-cli`,
model `claude-sonnet-4-6`, effort `medium` (source `cli`) — from `execution_config.txt`. Job
state `completed`, stop reason empty, stop source empty — from `result_state.txt`. Task `T001`:
status `applied_to_job_workspace`, reviewer verdict `pass`, final status `staged_review_passed`,
`repair_rounds_used` 0 — from `result_state.txt`. Wall seconds `174.2` — from `timing.txt`.
Changed paths, from `changed_paths.txt`:
```
apps/cli/commands/status_cmd.py
tests/test_ble001_ratchet.py
```

Job diff (`job_diff.txt`, verbatim):
```
$ git diff HEAD...remedy/job-3d8b8562cbc64f34  (exit 0)
diff --git a/apps/cli/commands/status_cmd.py b/apps/cli/commands/status_cmd.py
index 9d824b069..823c2acab 100644
--- a/apps/cli/commands/status_cmd.py
+++ b/apps/cli/commands/status_cmd.py
@@ -89,11 +89,11 @@ def _cmd_status(
     for j in jobs:
         if job_is_terminal(j.state):
             continue
+        from packages.orchestration.safe_points import StopControlError, stop_requested
         try:
-            from packages.orchestration.safe_points import stop_requested
             if stop_requested(str(j.job_id)) is not None:
                 stops_pending += 1
-        except Exception:  # noqa: BLE001 — stop-check failure must not break the status overview
+        except (OSError, StopControlError):
             pass
 
     runtime_status = "unknown"
diff --git a/tests/test_ble001_ratchet.py b/tests/test_ble001_ratchet.py
index ff1f68ae3..cb21e641a 100644
--- a/tests/test_ble001_ratchet.py
+++ b/tests/test_ble001_ratchet.py
@@ -18,7 +18,7 @@ REASONED = re.compile(r"^ — \S")
 
 #: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
 #: commit that removes a mark lowers this number in the same commit, and it is never raised.
-MAX_EXCUSED = 285
+MAX_EXCUSED = 284
 
 
 def _marks() -> list[tuple[str, int, str]]:
```

`run_defects.txt` (verbatim):
```
NONE
```

## Closure suite

(`.agent/authored/f055-closure-suite.txt`, whole and verbatim)
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 374.4s (the launcher's reading); pytest's own reported wall time: 373.62s (0:06:13)
summary line: 23067 passed, 22 skipped, 1 warning in 373.62s (0:06:13)
bad node ids (failed + errors):
  NONE
leftover processes: NONE
tree it ran on: 71305a2c7 (F055 R4 C4: the closure's self-use item run to its approval gate, never applied)
tree note: C3 and C4 changed only .agent/ files, the checklist page and the self-use queue
reflog before: 71305a2c7 HEAD@{2026-10-14 17:21:29 +0200}: commit: F055 R4 C4: the closure's self-use item run to its approval gate, never applied
reflog after: 71305a2c7 HEAD@{2026-10-14 17:21:29 +0200}: commit: F055 R4 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F055 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1283.70 CPU seconds, 373.63 wall seconds, 23089 tests collected, exit status 0, recorded 2026-10-14T15:27:50Z
This closure's suite used 1283.70 CPU seconds, 9.7 percent more than F308's 1170.14, within the 14.1 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 14.1 percent.
The test modules whose CPU time rose most since F308's closure run:
  +9.45 s  tests/runtimes/test_supervisor_portability.py (35.60 -> 45.05)
  +7.87 s  tests/orchestration/test_review_zip_hygiene.py (31.38 -> 39.25)
  +6.95 s  tests/orchestration/test_self_use_runner.py (3.59 -> 10.54)
  +5.31 s  tests/orchestration/test_token_ledger.py (6.93 -> 12.24)
  +4.53 s  tests/cli/test_rehearsal.py (0.00 -> 4.53)
  +4.06 s  tests/orchestration/test_job_worktree_integration.py (6.64 -> 10.70)
  +3.57 s  tests/orchestration/test_stream_export_e2e.py (3.42 -> 6.99)
  +3.55 s  tests/ui_server/test_multi_project_live.py (14.81 -> 18.36)
  +3.40 s  tests/orchestration/test_public_api_gate_paths.py (13.95 -> 17.35)
  +3.01 s  tests/ui_server/test_public_api.py (8.94 -> 11.95)
```

## Deviations & assumptions

None. C1 to C5 and gates 1 to 4 all matched this block exactly on the first run; no amendment was
needed.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The reviewer reviews round 4, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. The evidence bundle and the review package (the suite came back green).
5. The closing round: the Built State, the resolutions, the rotation, the STATUS line and the
   pull request.

Operator questions open: 0.
Open findings: 40 (R-1318 owned by F055, R-1246 and R-1276 to R-1313 by F307).

## For the operator, in plain sentences

The paid run was asked to narrow one overly broad error handler down to the specific exceptions
it should catch, and it finished with a reviewer pass, staged but not applied anywhere. The
test collection ran once on the code about to ship and every test passed except the handful
already marked as skipped before this round began. The run took a little over six minutes.
The cost script said this feature's computer time came in under the ceiling it compares against,
a bit higher than the previous feature's but still well within what is allowed. Nothing new waits
for you.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | Gate 1's five C1 path-equality checks `True`; 306 insertions |
| C2 | done | the new test passes alone (18 passed) and under Gate 1's node-text check; 28 insertions |
| C3 | done | `git show --numstat` read exactly `15\t0`, matching the block |
| C4 | done | self-use run exit 0, `run_defects.txt` `NONE`, queue diff exactly one appended entry with empty `consumed_by` |
| C5 | done | suite exit 0, `23067 passed, 22 skipped`, cost script exit 0 within the 14.1 percent limit |
| C6 | done | this commit |
| Gate 1 | done | `ALL True`, one run |
| Gate 2 | done | all ten files non-empty |
| Gate 3 | done | exit 0, summary line as recorded, `NONE` bad node ids |
| Gate 4 | done | `fail_count` 0; 40 open finding ids in order |
| Gate 5 | done | reported in the reply, after the push |
| R-1318 | done | repaired in C2: `test_planning_counter_counts_a_real_planning_call` installs `_setup_llm_mocks` before `count_planning_calls` wraps `job_plan.plan_job_llm`, then proves `counts["plan_job_llm"] > 0` on a real rehearsed-plan run |
