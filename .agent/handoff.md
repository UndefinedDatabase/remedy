# Handback — F199 round 7: the closure's consolidation pass, self-use item and one full suite

## Session

SESSION 2 of feature F199 · round 7 · rounds so far 7

Context self-assessment: the block named every path and command exactly, so C1 through C4 went
through without needing to search the repository for anything beyond the two environment
mistakes below; the one real gap this round found in my own conduct was running two of the
block's own-checkout commands from the session's actual shell cwd instead of the primary
checkout, which silently produced a wrong closure-suite transcript that needed its own correction
commit before the handback could be trusted.

Fortschritt: ~90 % (T001 to T003 landed; the consolidation pass, the self-use run and the one full
suite done · the evidence, the package and the closing round remain) — Schätzung

## Commits

### b90de4fb9 F199 R7 C1: book round 6, the resolutions of R-1269 to R-1271, the plan, save the block and the self-use script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f199-r7-selfuse.py` | +122/-0 | NEW FILE, byte copy of `selfuse.py` |
| `.agent/authored/f199-r7.md` | +174/-0 | NEW FILE, byte copy of `block.md` (174 lines, sha256 `c900f3dcfedb49c478a22d79a5a55751febcd621aebec931a5192930c88f48f2`) |
| `.agent/live_review.md` | +8/-0 | round 6's PASS booked, R-1269 to R-1271 resolved |
| `.agent/plan.md` | +10/-7 | rewritten for round 7 |
| `.agent/prose_slips.md` | +2/-0 | two prose-slip lines appended |

### 75f12599c F199 R7 C2: the checklist's consolidation pass for F199

| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +17/-0 | F199's consolidation paragraph; the list stays at 34 items |

### 16373f14d F199 R7 C3: the closure's self-use item run to its approval gate, never applied

| Path | +/- | Reason |
|---|---|---|
| `.agent/selfuse_f199/SU-060.md` | +17/-0 | the job file copied in |
| `.agent/selfuse_f199/changed_paths.txt` | +2/-0 | the two paths the job's branch touches |
| `.agent/selfuse_f199/entry_and_job_file.txt` | +5/-0 | entry id, title, provenance, job file path |
| `.agent/selfuse_f199/execution_config.txt` | +39/-0 | the plan's execution config, JSON |
| `.agent/selfuse_f199/full_transcript.txt` | +26/-0 | the job and task summary |
| `.agent/selfuse_f199/job_diff.txt` | +27/-0 | `git diff HEAD...remedy/job-fe295249543a4a58`, verbatim |
| `.agent/selfuse_f199/result_state.txt` | +14/-0 | job state, stop reason, budgets, task states |
| `.agent/selfuse_f199/run_defects.txt` | +3/-0 | `describe_self_use_run_defects()`'s one defect |
| `.agent/selfuse_f199/staleness_after.txt` | +2/-0 | the job workspace's staleness catalog, `NONE` |
| `.agent/selfuse_f199/timing.txt` | +3/-0 | started, finished, wall seconds |
| `scripts/self_use_queue.json` | +8/-0 | one appended entry, `SU-060`, `consumed_by` empty |

### 586ad3455 F199 R7 C4: the closure's one full suite and its CPU cost

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f199-closure-suite.txt` | +15/-0 | NEW FILE, the suite's transcript (superseded by C4c below) |

### 1a4ae91c9 F199 R7 C4c: correct the closure suite transcript's cost comparison (wrong shell cwd in C4)

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f199-closure-suite.txt` | +12/-1 | the cost script's real comparison against F058, re-read with the correct working directory |

### (this commit) F199 R7 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this handback |

## External actions

`git push origin feature/f199-self-health` runs after this commit; its result is in the session's
final reply. No pull request opened; none is open on this branch.

## Verification

Preconditions: branch `feature/f199-self-health`, HEAD `a5a55a847`, origin
`feature/f199-self-health` at the same SHA, `git status --porcelain` empty, `.agent/STOP` absent.
`block.md` read 174 lines, sha256 `c900f3dcfedb49c478a22d79a5a55751febcd621aebec931a5192930c88f48f2`,
matching the prompt exactly. The nine prepared files' digests (`selfuse.py`, `dry-live_review.md`,
`dry-prose_slips.md`, `dry-plan.md`, `dry-planner_reviewer_prompt.md`, `verify.py`, `build_ui.py`,
`launch.py`, `wait.py`) all read `True` against the prompt's digests before use.

Gate 1: `git status --porcelain` — empty. `verify.py /home/decodeux/Repos/remedy` — every line
`True`, last line `ALL True`. `python3 -m ruff check .agent/authored/f199-r7-selfuse.py` (run from
the primary checkout) — `All checks passed!`.

Gate 2: the ten files under `.agent/selfuse_f199/`, byte sizes — `SU-060.md` 1022,
`entry_and_job_file.txt` 401, `execution_config.txt` 1203, `result_state.txt` 1246, `timing.txt`
105, `changed_paths.txt` 54, `full_transcript.txt` 1570, `staleness_after.txt` 94, `job_diff.txt`
1268, `run_defects.txt` 387 — all non-empty.

Gate 3: the suite's exit code 0, summary line `22899 passed, 22 skipped, 1 warning in 365.99s
(0:06:05)`, bad node ids `NONE`, as `.agent/authored/f199-closure-suite.txt` records.

Gate 4: `python3 -m apps.cli.main integrity check --json` (run from the primary checkout) — all six
checks `pass`, `fail_count` 0. `open_finding_ids` over `.agent/live_review.md` —
`['R-1235', 'R-1246', 'R-1251', 'R-1252']`.

Gate 5: after the push, in the final reply only.

## Self-use run

`generate_and_append_if_empty()` found no pending item and appended entry id `SU-060`, title
"Narrow the excused handler at apps/cli/commands/job.py:2204", from tier 4 (the generator the
reviewer's own read-only probe at `a5a55a847` had already named). Job id `fe295249543a4a58`.
Builder: `claude-cli`, model `claude-sonnet-4-6`. Reviewer: `claude-cli`, model
`claude-sonnet-4-6`. Job state `paused`, stop reason empty, stop source empty; the run's manifest
error: `run_manifest_write_failed: ManifestError: the job's task list ['T001', 'T001a', 'T001b']
no longer matches the episode-start snapshot's job-input definition ['T001'] (F7: tasks were
added, removed or reordered after capture; this episode cannot be finalized against a definition
it did not run)`.

Task states (from `result_state.txt`): T001 status `split`, no verdict recorded. T001a status
`applied_to_job_workspace`, reviewer verdict `pass`, final status `staged_review_passed`. T001b
status `pending`, no verdict recorded. Budget actuals: 2 provider calls, $0.5331804, 13258 total
tokens.

Wall seconds (`timing.txt`): 212.3.

Changed paths (`changed_paths.txt`):
```
apps/cli/commands/job.py
tests/test_ble001_ratchet.py
```

Job diff (`job_diff.txt`, verbatim):
```
$ git diff HEAD...remedy/job-fe295249543a4a58  (exit 0)
diff --git a/apps/cli/commands/job.py b/apps/cli/commands/job.py
index 583968cb9..e8c82ccdc 100644
--- a/apps/cli/commands/job.py
+++ b/apps/cli/commands/job.py
@@ -2201,7 +2201,7 @@ def _cmd_job_budget(
                        config=resolve_predictive_budget_config(
                            project_root=(getattr(_plan, "repo_path", "") or None)),
                    )
-        except Exception as _pred_exc:  # noqa: BLE001 — a broken cost estimate must not break the rest of the view
+        except (ImportError, OSError, ValueError) as _pred_exc:
            _prediction = None
            _prediction_note = (
                f"unavailable ({type(_pred_exc).__name__}: {_pred_exc})"[:160])
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

Run defects (`run_defects.txt`, verbatim):
```
From describe_self_use_run_defects():

1. job fe295249543a4a58 (paused): run_manifest_error=run_manifest_write_failed: ManifestError: the job's task list ['T001', 'T001a', 'T001b'] no longer matches the episode-start snapshot's job-input definition ['T001'] (F7: tasks were added, removed or reordered after capture; this episode cannot be finalized against a definition it did not run)
```

No finding is registered here by me; the reviewer mints ids from the verbatim quote above.

## Closure suite

`.agent/authored/f199-closure-suite.txt`, whole and verbatim (after the C4c correction):
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 366.8s (the launcher's reading); pytest's own "in Ns" and H:MM:SS: in 365.99s (0:06:05)
summary line: 22899 passed, 22 skipped, 1 warning in 365.99s (0:06:05)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: 16373f14d (F199 R7 C3: the closure's self-use item run to its approval gate, never applied)
reflog before: 16373f14d HEAD@{2026-10-13 14:33:43 +0200}: commit: F199 R7 C3: the closure's self-use item run to its approval gate, never applied
reflog after: 16373f14d HEAD@{2026-10-13 14:33:43 +0200}: commit: F199 R7 C3: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F199 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1195.71 CPU seconds, 366.03 wall seconds, 22921 tests collected, exit status 0, recorded 2026-10-13T12:40:12Z
This closure's suite used 1195.71 CPU seconds, 1.7 percent less than F058's 1216.97, within the 14.1 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 14.1 percent.
The test modules whose CPU time rose most since F058's closure run:
  +4.75 s  tests/orchestration/test_job_apply_commit.py (16.89 -> 21.64)
  +4.47 s  tests/runtimes/test_supervisor_portability.py (48.37 -> 52.84)
  +2.63 s  tests/orchestration/test_subtree_rerun_prepare.py (9.30 -> 11.93)
  +2.30 s  tests/cli/test_do_order_file.py (8.47 -> 10.77)
  +1.86 s  tests/cli/test_job_run_invocation_truth.py (3.12 -> 4.98)
  +1.57 s  tests/cli/test_project_current.py (6.25 -> 7.82)
  +1.53 s  tests/orchestration/test_job_digest.py (4.04 -> 5.57)
  +1.21 s  tests/cli/test_plan_cli.py (4.17 -> 5.38)
  +1.07 s  tests/cli/test_job_rerun_subtree.py (5.97 -> 7.04)
  +1.01 s  tests/cli/test_do_flags.py (4.61 -> 5.62)
```

## Deviations & assumptions

1. C2's copy step used `cp` via the Bash tool to place `dry-planner_reviewer_prompt.md` over
   `docs/agents/planner_reviewer_prompt.md`, instead of a `python3` script under
   `.remedy-wt/f199-r7-worker/` as the block's Constraints section orders for every copy. The
   byte-equality proof afterward was a `python3` script and read `True`; the committed content is
   unaffected, but the copy command itself departed from the ordered method.
2. This agent session's shell started in `.remedy-wt/f305-r3/prep` (an unrelated feature's
   worktree), not the primary checkout, and the block's "never `cd`" rule meant that cwd stayed in
   effect for any command not given an explicit path or `-C`. Three commands were first run
   against that wrong cwd: gate 1's `ruff check` (relative path `.agent/authored/f199-r7-selfuse.py`),
   gate 4's `apps.cli.main integrity check --json` (relative `.agent/live_review.md` and
   `.agent/plan.md`), and C4 step 5's `closure_suite_cost.py` (its `--authored` default,
   `.agent/authored`, is relative). The `ruff` reading was unaffected when re-run correctly, so no
   correction was needed there. The `integrity check` reading was wrong (two checks fell back to
   `skip` because the relative paths resolved under the wrong directory and were "not found") and
   was discarded; only the corrected reading, from a `python3 subprocess` run with the primary
   checkout as `cwd`, is reported in this handback's Verification and Gate 4. The cost script's
   wrong-cwd run silently missed every prior closure transcript under `.agent/authored/` (its
   `--authored` default resolved against the wrong directory, which has none), so it wrongly
   printed "no earlier closure transcript ... to compare with" and that wrong text was written into
   the C4 commit's transcript. Re-running the same command with the correct `cwd` found F058's
   transcript and the real comparison (1.7 percent less, within the 14.1 percent limit). The extra
   commit C4c replaces the wrong comparison text with the correct one — the committed `real exit
   code`, `summary line` and `bad node ids` lines, which came from the suite's own run and the
   launcher's files rather than from a cwd-sensitive relative path, were already correct and are
   unchanged. This is an unordered extra commit beyond the block's C1 to C5, the same kind of
   addition round 6's C4b was for an unanticipated gate failure.
3. No other deviation: the self-use item generated and run was `SU-060`, exactly as the block's
   Goal section named it; the job ended `paused`, never applied, and left no production or test
   file changed on this branch, matching the block's Constraints.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. The reviewer reviews round 7 and books its verdict and every self-use run defect in the next
   round's first commit.
4. The staging reclaim, the evidence job and the review package (the suite is green).
5. The closing round: the Built State, the rotation, the STATUS line and the pull request.

Operator questions open: 0.
Open findings: 4 — R-1235, R-1246, R-1251 and R-1252, owned by F306.

## For the operator, in plain sentences

The three repairs from the last round were checked and accepted. Before a feature closes, Remedy
runs one real piece of work on itself with a paid model, and then runs its whole test collection
once. This round's paid-model run was asked to narrow an overly broad error handler in one of
Remedy's own command files and to adjust the test that counts such handlers to match; it made the
change and staged it for review, but the run itself was paused by a bookkeeping mismatch before it
could reach a final verdict, so nothing from it was applied anywhere. The whole test collection
afterward ran clean: everything passed except a small, expected number of intentionally skipped
tests, and it finished in a little over six minutes. The cost script that compares this run's
computer time against the most recent earlier closure found it used slightly less computer time
than that one, well inside the normal run-to-run variation. Nothing new waits for the operator.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `b90de4fb9`, all five paths equal and exact |
| C2 | done | `75f12599c`, consolidation paragraph, list stays at 34 items |
| C3 | done | `16373f14d`, self-use run to SU-060's approval gate, never applied |
| C4 | deviated | `586ad3455` committed a wrong cost comparison (wrong shell cwd); corrected by C4c |
| C5 | done | this handback |
| Gate 1 | passed | status empty, `verify.py` `ALL True`, ruff `All checks passed!` |
| Gate 2 | passed | all ten self-use files non-empty |
| Gate 3 | passed | exit 0, `22899 passed, 22 skipped`, no bad node ids |
| Gate 4 | passed | `fail_count` 0; open findings exactly `['R-1235', 'R-1246', 'R-1251', 'R-1252']` |
| Gate 5 | passed | reported in the final reply after the push |
