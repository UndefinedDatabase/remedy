# Handback — F305 round 3: book round 2, T003, the consolidation pass, the self-use run, the one full suite

## Session

SESSION 1 of feature F305 · round 3 · rounds so far 3

Context self-assessment: the session verified the block's own line count and sha256 and all six
gate-script/append-file digests before any write, diffed every prepared `dry-*` file against its
current target to confirm each numstat by hand before staging, ran the self-use script and the
full suite each exactly once through the reviewer's own `launch.py`/`wait.py` pair with no edit to
either, and closed all four gates green on the first pass; context remains comfortable at
handback.

Fortschritt: ~85 % (T001 to T003 landed; the consolidation pass, the self-use run and the one full
suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `13407b81e`..HEAD.

## Commits

### 4f771f99f F305 R3 C1: book round 2, the plan, save the block and the self-use script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f305-r3-selfuse.py` | +122/-0 | NEW FILE, byte copy of `prep/selfuse.py` (reviewer-authored, adapted from `.agent/authored/f297-r12-selfuse.py` with only its paths and header changed) |
| `.agent/authored/f305-r3.md` | +185/-0 | NEW FILE, byte copy of `block.md` (185 lines, sha256 `c1079d3c2b60eef8704a5fda7e438af165366a2d73c626060da3bd9cce3b6d90`, matching both values the session was given) |
| `.agent/live_review.md` | +2/-0 | byte copy of base `13407b81e` plus `prep/append-live_review.txt`: the `Gate: F305 R2` entry appended, VERDICT PASS |
| `.agent/plan.md` | +12/-15 | rewritten in full for F305 round 3, byte copy of `prep/dry-plan.md` |

### 4c6c488cc F305 R3 C2: the browser proof of the missions panel and its chain band, and the user guide (T003)

| Path | +/- | Reason |
|---|---|---|
| `docs/README.md` | +2/-0 | byte copy of `prep/dry-README.md`: the quick-find and docs-index rows for the new user guide |
| `docs/guides/missions-panel-user-guide-v1.md` | +46/-0 | NEW FILE, byte copy of `prep/dry-missions-panel-user-guide-v1.md`: the short operator-facing guide to the missions panel |
| `tests/ui_server/test_mission_chain_live.py` | +228/-0 | NEW FILE, byte copy of `prep/dry-test_mission_chain_live.py`: the headless-browser proof over a fixture order of three jobs in two repositories (DECISIONS F305 D1 to D3; resolves R-1248) |

### 625fd5818 F305 R3 C3: the checklist's consolidation pass for F305

| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +9/-0 | byte copy of `prep/dry-planner_reviewer_prompt.md`: F305's consolidation paragraph — nothing joined, no two items merged, the list stays at 34 items |

### 2506d3f3a F305 R3 C4: the closure's self-use item run to its approval gate, never applied

| Path | +/- | Reason |
|---|---|---|
| `.agent/selfuse_f305/SU-057.md` | +17/-0 | NEW FILE, the generated item's own job markdown |
| `.agent/selfuse_f305/changed_paths.txt` | +2/-0 | NEW FILE, the two files the job's own branch touched |
| `.agent/selfuse_f305/entry_and_job_file.txt` | +5/-0 | NEW FILE, the queue entry and job-file identity |
| `.agent/selfuse_f305/execution_config.txt` | +39/-0 | NEW FILE, the `self_use` role's resolved execution config |
| `.agent/selfuse_f305/full_transcript.txt` | +26/-0 | NEW FILE, the job/task summary |
| `.agent/selfuse_f305/job_diff.txt` | +27/-0 | NEW FILE, `git diff HEAD...remedy/job-49cf7ccc9be64f1d` verbatim |
| `.agent/selfuse_f305/result_state.txt` | +14/-0 | NEW FILE, job and task state/verdict |
| `.agent/selfuse_f305/run_defects.txt` | +3/-0 | NEW FILE, `describe_self_use_run_defects()` output |
| `.agent/selfuse_f305/staleness_after.txt` | +2/-0 | NEW FILE, the staleness catalog read from the job workspace |
| `.agent/selfuse_f305/timing.txt` | +3/-0 | NEW FILE, start/finish/wall seconds |
| `scripts/self_use_queue.json` | +8/-0 | the generator's one appended entry, `SU-057`, `consumed_by` empty |

### a09a65206 F305 R3 C5: the closure's one full suite and its CPU cost

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f305-closure-suite.txt` | +26/-0 | NEW FILE, the closure's one full-suite transcript and `closure_suite_cost.py` reading, in `f297-closure-suite.txt`'s shape |

### this commit F305 R3 C6: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file (self-reference rule, `docs/agents/handback_template.md`) |

## External actions

None yet in this commit. `git -C /home/decodeux/Repos/remedy push origin
feature/f305-multi-repo-chain-band` follows this commit, per the block's push-after-C6 instruction.
Its outcome is reported in the final reply, not in this file. No pull request is opened, edited or
merged this round (none is open for this branch; the block forbids opening one). No other `gh`
command run. No worktree added or removed by the worker beyond the pre-existing, gitignored
`.remedy-wt/f305-r3-worker/` scratch directory this session created for its own copy/hash scripts,
and the self-use script's own transient `git worktree add`/`remove` of
`.remedy-wt/f305-r3-jobtree` was not needed this run (the job workspace directory still existed).

## Verification

**Preconditions (before C1):** `git rev-parse HEAD` read `13407b81e877c41ae452effe3f2faa216c474a0a`,
equal to `origin/feature/f305-multi-repo-chain-band`; `git status --porcelain` empty;
`.agent/STOP` absent; `git branch --show-current` read `feature/f305-multi-repo-chain-band`.

**Block and Bundle digests (before any write):** `wc -l block.md` read `185`, its sha256 read
`c1079d3c2b60eef8704a5fda7e438af165366a2d73c626060da3bd9cce3b6d90` — both equal to the values the
prompt delivered. All six helper-file digests (`verify.py`, `build_ui.py`, `launch.py`, `wait.py`,
`append-live_review.txt`, `c3-tree.txt`) matched the prompt's stated values. All seven
digest-bearing Bundle-listed prepared files (`selfuse.py`, `dry-live_review.md`, `dry-plan.md`,
`dry-test_mission_chain_live.py`, `dry-missions-panel-user-guide-v1.md`, `dry-README.md`,
`dry-planner_reviewer_prompt.md`) were hashed and matched the block's stated digests exactly before
use.

**C1:** `c1_copy.py` byte-copied `selfuse.py`, `dry-live_review.md` and `dry-plan.md` to their
destinations, and byte-copied `block.md` to `.agent/authored/f305-r3.md`. `c1_check.py` printed
`True` for all four pairs, the authored copy's line count (`185`) and sha256 matching the block
exactly. `git diff --cached --numstat` after `git add` read exactly `122 0`, `185 0`, `2 0`,
`12 15` for the four Bundle paths, no other path. `git branch --show-current` read
`feature/f305-multi-repo-chain-band` immediately before the commit.

**C2:** `c2_copy.py` byte-copied the three files (two NEW FILEs, one rewrite) and `c2_check.py`
re-hashed all three pairs: `True` for each. `git diff --cached --numstat` read exactly `2 0`,
`46 0`, `228 0` for the three Bundle paths, no other path. `git branch --show-current` re-read
correctly before the commit.

**C3:** `c3_copy.py` byte-copied the one file and `c3_check.py` re-hashed it: `True`. `git diff
--cached --numstat` read exactly `9 0` for `docs/agents/planner_reviewer_prompt.md` alone. `git
branch --show-current` re-read correctly before the commit. `git rev-parse HEAD^{tree}` at this
point read `864c6bffe4d8aa5798a454a046bb926dbdc882a8`, equal to `prep/c3-tree.txt`'s stated value,
confirmed before C4 began.

**C4:** `python3 .../launch.py selfuse ...` started the self-use script detached; `python3
.../wait.py selfuse ... 58` returned `exit 0 wall 108.8` on its first call (no `still running`
retry needed) and printed the ten output files' contents, reproduced below under "Self-use run".
Exit was 0, so the block's non-zero abort clause did not apply. `git status --porcelain` then
showed exactly `M scripts/self_use_queue.json` and `?? .agent/selfuse_f305/`; `git diff
scripts/self_use_queue.json` showed exactly one appended entry, id `SU-057`, `"consumed_by": ""`.
`git diff --cached --numstat` after `git add` read exactly the eleven Bundle paths (ten new files
under `.agent/selfuse_f305/` plus `scripts/self_use_queue.json`), no other path. `git
branch --show-current` re-read correctly before the commit.

**C5:**
1. `python3 .../build_ui.py /home/decodeux/Repos/remedy` →
   ```
   vite build exit 0 :: - Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
   porcelain empty True
   ```
2. `git reflog -n 1 --date=iso` before the suite read:
   `2506d3f3a HEAD@{2026-10-12 02:58:15 +0200}: commit: F305 R3 C4: the closure's self-use item run to its approval gate, never applied`
3. `python3 .../launch.py suite ...` started `python3 -m pytest -n auto -q` detached; `python3
   .../wait.py suite ... 58` returned on its first call:
   ```
   22641 passed, 22 skipped, 1 warning in 436.71s (0:07:16)
   exit 0 wall 437.5
   ```
   No FAILED or ERROR line and no line containing `process(es) behind` anywhere in the captured
   log (checked by grep over the full log, not only the tail).
4. `git reflog -n 1 --date=iso` after the suite read the identical line as step 2 — the branch did
   not move during the run.
5. `python3 scripts/closure_suite_cost.py --feature F305 --record
   /home/decodeux/.remedy-loop/test_load.jsonl` → exit 0; full output quoted below under "Closure
   suite". Within the 14.1 percent limit (9.8 percent more CPU seconds than F297's run).
6. `.agent/authored/f305-closure-suite.txt` written in `f297-closure-suite.txt`'s shape and
   committed alone; `git diff --cached --numstat` read exactly `26 0` for that one path.

**Gate 1:** `git -C /home/decodeux/Repos/remedy status --porcelain` → empty. Then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f305-r3/prep/verify.py /home/decodeux/Repos/remedy`
→
```
equal True .agent/authored/f305-r3.md
equal True .agent/authored/f305-r3-selfuse.py
equal True .agent/live_review.md
equal True .agent/plan.md
equal True tests/ui_server/test_mission_chain_live.py
equal True docs/guides/missions-panel-user-guide-v1.md
equal True docs/README.md
equal True docs/agents/planner_reviewer_prompt.md
base plus slice True .agent/live_review.md
C3 tree equals the replay True 864c6bffe4d8aa5798a454a046bb926dbdc882a8
ALL True
```
Exit 0, every line `True`, last line `ALL True`. Then
`python3 -m ruff check tests/ui_server/test_mission_chain_live.py
.agent/authored/f305-r3-selfuse.py` → `All checks passed!`, exit 0.

**Gate 2:** The ten files under `.agent/selfuse_f305/`, each confirmed non-empty, byte sizes:
`SU-057.md` 1020, `entry_and_job_file.txt` 399, `execution_config.txt` 1203, `result_state.txt`
1245, `timing.txt` 105, `changed_paths.txt` 54, `full_transcript.txt` 1570,
`staleness_after.txt` 94, `job_diff.txt` 1231, `run_defects.txt` 387.

**Gate 3:** The suite of C5 itself: exit code `0`; summary line `22641 passed, 22 skipped, 1
warning in 436.71s (0:07:16)`; bad node ids (failed + errors) `NONE`, as the transcript records.

**Gate 4:** `python3 -m apps.cli.main integrity check --json` →
```json
{"check_count": 6, "checks": [{"message": "handlers=184", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Exit 0, all six checks `pass`, `fail_count` 0. Then
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1235', 'R-1246', 'R-1248', 'R-1251', 'R-1252']`, matching exactly.

**Gate 5 (after the push):** reported in the final reply, not here (block instruction).

No mutation run (the block forbids it this round). No test run beyond C5's one full suite;
`REMEDY_TEST_MAX_WORKERS` was never set, no extra `-n` was passed, no two test commands ran at
once. No `npm` or `npx` run; the one UI tool run was C5 step 1's `vite build`, through
`build_ui.py`. No worktree of the worker's own beyond the gitignored scratch directory named
above. The only provider calls this round were the self-use run's own (2 calls, `pingpong_live`
source, `$0.3840876` measured cost, 6284 total tokens, within the role's `max_cost_usd: 6.0` /
`max_provider_calls: 8` budget).

## Self-use run

- Entry id: `SU-057`
- Title: Narrow the excused handler at apps/cli/commands/job.py:2074
- Job id: `49cf7ccc9be64f1d`
- Builder: `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source: `cli`)
- Reviewer: `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source: `cli`)
- Job state: `paused`. Stop reason: (empty). Stop source: (empty).
- Task states (from `result_state.txt`):
  - `T001`: status `split`, reviewer verdict (empty)
  - `T001a`: status `applied_to_job_workspace`, reviewer verdict `pass` (final status
    `staged_review_passed`)
  - `T001b`: status `pending`, reviewer verdict (empty)
- Wall seconds (from `timing.txt`): `105.6`
- Changed paths (from `changed_paths.txt`):
  ```
  apps/cli/commands/job.py
  tests/test_ble001_ratchet.py
  ```
- Job diff (from `job_diff.txt`, VERBATIM):
  ```
  $ git diff HEAD...remedy/job-49cf7ccc9be64f1d  (exit 0)
  diff --git a/apps/cli/commands/job.py b/apps/cli/commands/job.py
  index 583968cb9..152942647 100644
  --- a/apps/cli/commands/job.py
  +++ b/apps/cli/commands/job.py
  @@ -2071,7 +2071,7 @@ def _cmd_job_budget(
                   if _budgets is not None:
                       evaluation = evaluate_budget(_budgets, counters)
                   _counter_status = "evaluated"
  -            except (BudgetCounterError, Exception) as _budget_exc:  # noqa: BLE001 — corrupted budgets must not crash
  +            except BudgetCounterError as _budget_exc:
                   _counter_status = "corrupt"
                   _counter_diagnostic = str(_budget_exc)
                   counters = None
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
- `run_defects.txt`, VERBATIM:
  ```
  From describe_self_use_run_defects():

  1. job 49cf7ccc9be64f1d (paused): run_manifest_error=run_manifest_write_failed: ManifestError: the job's task list ['T001', 'T001a', 'T001b'] no longer matches the episode-start snapshot's job-input definition ['T001'] (F7: tasks were added, removed or reordered after capture; this episode cannot be finalized against a definition it did not run)
  ```

No finding is registered by this worker for the above; the reviewer mints an id from this verbatim
quote in round 4's first commit, per the block's instruction.

## Closure suite

Quoting `.agent/authored/f305-closure-suite.txt` whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 437.5s (the launcher's reading); pytest's own reported wall time: 436.71s (0:07:16)
summary line: 22641 passed, 22 skipped, 1 warning in 436.71s (0:07:16)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: 2506d3f3a (F305 R3 C4: the closure's self-use item run to its approval gate, never applied)
reflog before: 2506d3f3a HEAD@{2026-10-12 02:58:15 +0200}: commit: F305 R3 C4: the closure's self-use item run to its approval gate, never applied
reflog after: 2506d3f3a HEAD@{2026-10-12 02:58:15 +0200}: commit: F305 R3 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F305 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1205.80 CPU seconds, 436.73 wall seconds, 22663 tests collected, exit status 0, recorded 2026-10-12T01:05:44Z
This closure's suite used 1205.80 CPU seconds, 9.8 percent more than F297's 1097.85, within the 14.1 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 14.1 percent.
The test modules whose CPU time rose most since F297's closure run:
  +20.14 s  tests/runtimes/test_supervisor_portability.py (32.27 -> 52.41)
  +7.56 s  tests/ui_server/test_mission_chain_live.py (0.00 -> 7.56)
  +4.61 s  tests/cli/test_do_sequence_cli.py (23.78 -> 28.39)
  +4.42 s  tests/ui_server/test_multi_project_live.py (14.84 -> 19.26)
  +3.14 s  tests/ui_server/test_public_api.py (8.66 -> 11.80)
  +3.01 s  tests/orchestration/test_self_use_runner.py (4.62 -> 7.63)
  +2.81 s  tests/runtimes/test_runtime_lifecycle_safety.py (1.87 -> 4.68)
  +2.71 s  tests/runtimes/test_runtime_cli_process_boundary.py (7.77 -> 10.48)
  +2.59 s  tests/runtimes/test_runtime_state_machine.py (3.13 -> 5.72)
  +2.48 s  tests/orchestration/test_job_task_runner.py (13.27 -> 15.75)
```

## Authored-text proofs

1. `block.md` → `.agent/authored/f305-r3.md` (C1): byte-equal, confirmed by `c1_check.py` and
   again by gate 1's `verify.py`.
2. `prep/selfuse.py` → `.agent/authored/f305-r3-selfuse.py` (C1): byte-equal, confirmed the same
   way; never edited.
3. The base `13407b81e:.agent/live_review.md` + `prep/append-live_review.txt` →
   `.agent/live_review.md` (C1): built by the formula gate 1's `verify.py` checks
   ("base plus slice True"), byte-equal to `prep/dry-live_review.md`.
4. `prep/dry-plan.md` → `.agent/plan.md` (C1): byte-equal, confirmed by `c1_check.py` and gate 1.
5. `prep/dry-test_mission_chain_live.py` → `tests/ui_server/test_mission_chain_live.py` (C2),
   `prep/dry-missions-panel-user-guide-v1.md` →
   `docs/guides/missions-panel-user-guide-v1.md` (C2), `prep/dry-README.md` → `docs/README.md`
   (C2): each byte-equal, confirmed by `c2_check.py` and gate 1.
6. `prep/dry-planner_reviewer_prompt.md` → `docs/agents/planner_reviewer_prompt.md` (C3):
   byte-equal, confirmed by `c3_check.py` and gate 1; and `git rev-parse HEAD^{tree}` at that
   commit matched `prep/c3-tree.txt`'s stated value, proving the full replayed commit sequence
   C1 to C3, not only the individual files, matches the reviewer's own dry tree.

## Deviations & assumptions

None. Every commit matched the block's ordered commit sequence (C1 to C5, then C6) with no extra
commit, no dropped commit and no reordering. No file was written outside each commit's named path
set; no mutation was run (none was ordered); exactly one test command ran this round (C5's full
suite); `REMEDY_TEST_MAX_WORKERS` was never set and no extra `-n` was passed; `npm`/`npx` were
never run; `.agent/STOP` did not appear during the round; no merge, branch create/switch beyond the
one feature branch, or force-push was performed; no pull request was opened or merged. All six
helper-file digests and all seven Bundle-digest prepared files matched the prompt's and the
block's stated values on the first check, so no stop-and-report was triggered. The self-use run
exited 0 (not the non-zero case the block's abort clause covers), so C4 proceeded to commit; its
one run_manifest_error defect is recorded verbatim above for the reviewer to mint a finding from,
not registered by this worker. `launch.py`'s selfuse and suite steps each returned on `wait.py`'s
first call (no `still running` retry was needed for either).

## Next

1. Phase 1 rule 1 (`.agent/STOP`): absent throughout this round; the next session checks it first.
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The reviewer reviews round 3, books its verdict, the resolution of R-1248 and every self-use
   run defect in the next round's first commit.
4. The evidence bundle and the review package (the suite is green).
5. The closing round: the Built State, the rotation, the STATUS line and the pull request.

Operator questions open: 1.
Open findings: 5 — R-1248, owned by F305, and R-1235, R-1246, R-1251 and R-1252, owned by F306.

## For the operator, in plain sentences

A test now opens the cockpit in a real browser and proves that the missions panel shows an order's
three jobs across two repositories, and that a click opens the other repository's job. A short
guide explains the panel. Before a feature closes, Remedy runs one real piece of work on itself
with a paid model and then its whole test collection once. The paid run was asked to tighten one
overly broad error handler in the job command and lower the matching safety count by one; it
reached its review stage with the change accepted there, then stopped on its own bookkeeping
before it could finish, so nothing from it was applied anywhere. All of the tests but twenty-two
skipped ones passed, and the whole run took a little over seven minutes. The cost script said this
feature's test run used a bit more computer time than the previous feature's did, well inside the
allowed range. Nothing new waits for the operator.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | round 2 booked (VERDICT PASS), the block and the self-use script saved, `.agent/plan.md` rewritten for round 3; all byte proofs `True` |
| C2 | done | T003's browser proof `test_mission_chain_live.py` and the user guide, with its two `docs/README.md` rows |
| C3 | done | the checklist's consolidation paragraph for F305; list stays at 34 items |
| C4 | done | the closure's self-use item `SU-057` generated and run to its approval gate, never applied; queue entry appended, ten evidence files written |
| C5 | done | `apps/ui` built, the closure's one full suite run (`22641 passed, 22 skipped`, exit 0), the cost script run (exit 0, within limit), transcript committed |
| C6 | done | this handback |
| T003 | done | the headless-browser proof and the user guide; resolves R-1248 |
| Gate 1 | passed | every line `True`, `ALL True`; ruff `All checks passed!` |
| Gate 2 | passed | all ten self-use evidence files non-empty |
| Gate 3 | passed | exit 0, summary line as recorded, bad node ids `NONE` |
| Gate 4 | passed | integrity `fail_count` 0, all six checks `pass`; open findings list matched exactly |
| Gate 5 | pending | runs after the push; reported in the final reply |
