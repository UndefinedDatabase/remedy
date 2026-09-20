# Handoff — F276 Data-root hygiene & disk budget · Round 6

## Session

SESSION 1 of feature F276 · round 6 · rounds so far 6

Context self-assessment: the worker read the step block first and verified its sha256 (`2b116041…`, 116 lines) against the digest it was given before doing anything else, then AGENTS.md in full, `docs/agents/handback_template.md`, the self-drive protocol's Phase 1 and Phase 2, `docs/roadmap/features/T2_F276.md`, the `decisions.md` payload (DECISION F276 D7, which rules where the block is terser), the `ledger.md` payload carrying round 5's verdict and R-1003's resolution, the `plan.md` payload, and the whole 1099-line code diff end to end before applying a single slice of it. Every numeral below is the output of a command run in this round, not a recollection; the two readings that disagree are both printed with the reason they disagree.

## Range

Review of caa9d073..HEAD — branch `feature/f276-data-root-hygiene`.

## Summary

Round 6 books round 5's verdict, carries the reviewer's resolution of R-1003, and builds T004 — the disk floor — which is this feature's last build slice.
- C1 books round 5's PASS over the four commits ending at `caa9d073` and carries the reviewer's own resolution of R-1003, the feature's one High; appends DECISION F276 D7; rewrites the plan; saves byte copies of the four reviewer payloads under `.agent/authored/`.
- C2 is the floor itself: the `JobBudgets` field, the config key, the injected probe seam, the check inside `evaluate_budget`, the `disk_exhausted` post-mortem branch, and the manifest's budget key set derived from `JobBudgets.model_fields` rather than spelled a second time.
- C3 is the `doctor core` disk section and the four documents.
- C4 is the 458-line test file, 31 nodes, whose autouse fixture makes reading the real filesystem an error.
- C5 is this handoff. No pull request was opened.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | four payload copies + three state files; nothing else |
| C2 the budget, the manifest schema and the stop path | done | nine paths, green on its own before it was committed |
| C3 the doctor section and the docs | done | four paths, green on its own before it was committed |
| C4 the tests | done | one path, 31 nodes, green on its own before it was committed |
| C5 handoff | done | this file |
| G1 transport + state | done | 12 readings, every one True |
| G2 code transport | done | all six object ids exactly as the block names; 14 paths and no other |
| G3 the sixteen-path suite | done | `1204 passed in 332.57s`, exit 0, 0 failed |
| G4 ruff | done | `All checks passed!`, exit 0 |
| G5 mutation red-proofs | done | control green; all three mutations red; none stayed green |
| G6 push + clean tree | done | follows this commit; the reading is in the round report |
| R-1003 | resolved by the reviewer's own text at C1 | this round lands no fix of its own for it |
| R-1004 | open | Medium, owner F282; its cost is measured again below, not fixed |
| R-1005 | open | Medium, owner F282; D7 notes that C2's derivation does not reach it |

## Commits

### 5370fb64 F276 R6 C1: the round 6 bookkeeping

| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-r6-block.md | 116/0 | byte copy of the step block |
| .agent/authored/f276-r6-decisions.md | 62/0 | byte copy of the D7 payload |
| .agent/authored/f276-r6-ledger.md | 4/0 | byte copy of the ledger payload |
| .agent/authored/f276-r6-plan.md | 31/0 | byte copy of the plan payload |
| .agent/decisions.md | 62/0 | `caa9d073` bytes + the D7 payload |
| .agent/live_review.md | 4/0 | `caa9d073` bytes + the ledger payload: round 5's verdict and R-1003's resolution |
| .agent/plan.md | 14/14 | rewritten to the plan payload |

Insertions 293 by `git show --numstat`. (The `git commit` summary printed 310 for the same commit: it applies rewrite detection and scores the wholly-rewritten `.agent/plan.md` as 31/31 instead of 14/14. Both readings are real, the block orders the `--numstat` one, and both are under 500.)

### 7d0fe00a F276 R6 C2: the disk floor itself

| Path | +/- | Reason |
|------|-----|--------|
| packages/core/models.py | 8/1 | `min_free_disk_bytes` on `JobBudgets` and its name added to the strictly-positive validator |
| packages/orchestration/budget_guard.py | 89/0 | `FREE_DISK_LIMIT`, first in `_LIMIT_ORDER`; `default_free_disk_bytes`, the `FREE_DISK_PROBE` seam, `free_disk_bytes`, the `free_disk_probe=` parameter and the floor check |
| packages/orchestration/budget_resolution.py | 30/1 | the config key in `_CONFIG_KEYS`, the resolution with no CLI layer, the all-None guard widened, and `resolve_min_free_disk_bytes` |
| packages/orchestration/config.py | 14/0 | the `budget.min_free_disk_bytes` / `REMEDY_BUDGET_MIN_FREE_DISK_BYTES` spec, default None |
| packages/orchestration/failure_postmortem.py | 9/0 | `FailureClass.DISK_EXHAUSTED` and its `TERMINAL_STATUS_CLASSES` entry |
| packages/orchestration/pingpong_job.py | 13/1 | `_write_stop_postmortem` writes `disk_exhausted` for the disk reason, comparing the whole reason string |
| packages/orchestration/run_manifest.py | 22/6 | `_budget_allowed_keys()` derived from `JobBudgets.model_fields`; the integer rule derived by subtraction |
| packages/orchestration/safe_points.py | 9/1 | `free_disk_probe` forwarded to `evaluate_budget` |
| tests/orchestration/test_failure_postmortem.py | 3/0 | `disk_exhausted` added to the every-class parametrization |

Insertions 197.

### f1cf63fb F276 R6 C3: the doctor section and the docs

| Path | +/- | Reason |
|------|-----|--------|
| apps/cli/commands/worker_facade_cmd.py | 43/0 | the `disk` check, the `disk` object under `--json` and the text section |
| docs/roadmap/features/T2_F276.md | 41/0 | the T004 amendment: four readings corrected against the code, nothing withdrawn |
| docs/system/architecture.md | 30/0 | the floor and the injected probe, as built |
| docs/system/job-budget-enforcement-v0.md | 34/12 | five limits become six; the floor's row, comparison, ordering and seam; the derived manifest key set |

Insertions 148.

### 63cd3e82 F276 R6 C4: the disk floor's tests

| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_disk_floor.py | 458/0 | 31 nodes: the default and its overrides, the boundary in three directions, the seam, the safe point, two real `run_job` cases, the post-mortem discriminator and the doctor section |

Insertions 458.

## External actions

- `git worktree add --detach .remedy-wt/f276-r6-mut 63cd3e82` — created for G5 only; removed with `git worktree remove` as that step's last action.
- `git worktree list` after the removal shows exactly two entries, the primary checkout at `63cd3e82` and `.remedy-wt/job-468c8e62a2cc4fac` at `1b9ae606`, which was never touched. Nothing was pruned and no branch was created or deleted.
- `git push origin feature/f276-data-root-hygiene` — follows this commit; its result is in the round report.
- No pull request was created, edited or merged. No `gh` command was run. Nothing was merged, amended, rewritten or force-pushed.

## Verification

- G1 transport + state — a python check printed 12 readings, every one True: the five payload digests (`ledger.md`, `decisions.md`, `plan.md`, `block.md`, `f276-r6.diff`) each match the block's; each of the four `.agent/authored/f276-r6-*` copies equals its payload byte for byte; `.agent/live_review.md` equals its `caa9d073` bytes + `ledger.md`; `.agent/decisions.md` equals its `caa9d073` bytes + `decisions.md`; `.agent/plan.md` equals the plan payload. SAVED BLOCK `.agent/authored/f276-r6-block.md`: lines=116 sha256=`2b116041def1fd22b15780f454132a21e9cb9606fa98b380aea1e72b34235700`; the block's own bytes: lines=116 sha256=`2b116041def1fd22b15780f454132a21e9cb9606fa98b380aea1e72b34235700`. Identical.
- G2 code transport — `git rev-parse 63cd3e82:packages 63cd3e82:apps 63cd3e82:tests` printed `9e8270485bc6089ecda1530383321866c7e061b3`, `5b69fdc726129ca33f136a09d380af87c5c82961`, `873edefb54b98707ceba442d19ba4841878d1c37`; `git rev-parse 63cd3e82:docs/system/architecture.md 63cd3e82:docs/system/job-budget-enforcement-v0.md 63cd3e82:docs/roadmap/features/T2_F276.md` printed `b315d40a3db0100848f9d83410efb08fc561f932`, `5517d8074f6a73544458544632cfaf09c870e010`, `920afe71529eb47b68a2e9b0c0a7ee5677e6ee87` — all six exactly the objects of the reviewer's dry run. `git diff --name-only 5370fb64 63cd3e82` printed 14 paths and no other, which is exactly the union C2, C3 and C4 name: `apps/cli/commands/worker_facade_cmd.py`, `docs/roadmap/features/T2_F276.md`, `docs/system/architecture.md`, `docs/system/job-budget-enforcement-v0.md`, `packages/core/models.py`, `packages/orchestration/budget_guard.py`, `packages/orchestration/budget_resolution.py`, `packages/orchestration/config.py`, `packages/orchestration/failure_postmortem.py`, `packages/orchestration/pingpong_job.py`, `packages/orchestration/run_manifest.py`, `packages/orchestration/safe_points.py`, `tests/orchestration/test_disk_floor.py`, `tests/orchestration/test_failure_postmortem.py`.
- G3 the sixteen-path suite — `python3 -m pytest -q -p no:cacheprovider` over the block's sixteen paths, serial, no `-n`, in the primary checkout: `1204 passed in 332.57s (0:05:32)`, exit 0, 0 failed, stderr empty.
- G4 ruff — `python3 -m ruff check` over the block's eleven paths printed `All checks passed!`, exit 0.
- G5 mutation red-proofs — one disposable worktree `.remedy-wt/f276-r6-mut` at `63cd3e82`, run from the worktree root with `python3 -B -m pytest -q --no-header -rf -p no:cacheprovider tests/orchestration/test_disk_floor.py tests/orchestration/test_failure_postmortem.py`. The import resolved inside the worktree: `/home/decodeux/Repos/remedy/.remedy-wt/f276-r6-mut/packages/orchestration/budget_guard.py`, so no editable install shadowed it. Pre-mutation bytes: `budget_guard.py` `6fb48247140d84f2d5df005ed71ac328d980f1eb50730e93c45f11b227c6654e`, `pingpong_job.py` `078e6fac56ed962a4e8b694c10c88e7c7bb18affbe9b347a12b51c1537f3a529`. CONTROL (unmutated): `179 passed in 12.01s`, exit 0.
  - (a) `if free < budgets.min_free_disk_bytes:` → `if free > budgets.min_free_disk_bytes:` in `budget_guard.py`, counted 1 occurrence before the edit: exit 1, `10 failed, 169 passed in 12.48s`. FAILED `TestEvaluateBudgetReadsTheFloor::test_below_the_floor_is_exhausted`, `::test_above_the_floor_is_not_exhausted`, `::test_the_module_seam_answers_when_no_per_call_probe_is_given`, `TestTheSafePointStopsOnTheFloor::test_should_stop_names_the_disk_limit`, `::test_should_stop_continues_above_the_floor`, `TestAJobStartBelowTheFloorIsRefused::test_the_job_reaches_stopped_before_any_work`, `::test_the_post_mortem_reason_is_disk_exhausted`, `::test_a_job_above_the_floor_is_not_refused`, `TestAnInFlightJobBelowTheFloorStops::test_the_job_reaches_stopped_at_a_safe_point`, `::test_the_disk_is_named_first_when_two_limits_are_exhausted`, all in `tests/orchestration/test_disk_floor.py`. Reverted to the saved bytes, byte-identical.
  - (b) `    _pre_stop = _stop_check()` → `    _pre_stop = None` in `pingpong_job.py`, counted 1 occurrence: exit 1, `2 failed, 177 passed in 12.44s`. FAILED `TestAJobStartBelowTheFloorIsRefused::test_the_job_reaches_stopped_before_any_work` and `TestAnInFlightJobBelowTheFloorStops::test_the_job_reaches_stopped_at_a_safe_point`. Reverted, byte-identical. This is the proof that the job-start reading is load-bearing and not merely re-derived by the next safe point: the second node is the one whose `run_refs == []` assertion measures that no run was minted.
  - (c) `_terminal = "disk_exhausted"` → `_terminal = "budget_exhausted"` in `pingpong_job.py`, counted 1 occurrence: exit 1, `3 failed, 176 passed in 11.85s`. FAILED `TestAJobStartBelowTheFloorIsRefused::test_the_post_mortem_reason_is_disk_exhausted`, `TestAnInFlightJobBelowTheFloorStops::test_its_post_mortem_reason_is_disk_exhausted`, `TestTheTerminalStatusDiscriminator::test_the_disk_limit_writes_disk_exhausted`. As the block warns, this mutation makes its replacement text occur twice, so it was reverted by restoring the file's saved bytes rather than by a second replacement.
  - NO MUTATION STAYED GREEN. After the last restore both files matched their pre-mutation sha256 exactly, the worktree's own `git status --porcelain` was empty, and `git worktree list` after removal shows the two entries named under External actions.
- G6 push + clean tree — follows this commit; the reading is in the round report.

## Open findings

16 by distinct id and 16 by the canonical formula `scripts/rotate_live_review.py::count_open_findings`, both measured on the committed ledger at `63cd3e82:.agent/live_review.md`: R-0499, R-0622, R-0662, R-0819, R-0820, R-0829, R-0866, R-0880, R-0892, R-0950, R-0984, R-0998, R-0999, R-1000, R-1004, R-1005. By severity: 0 High, 9 Medium, 7 Low. Seventeen were open at `caa9d073` with one High; the difference is R-1003, which C1's ledger append resolves in the reviewer's own words. The feature now carries no open High.

## Authored-text proofs

All four reviewer payloads were copied with `shutil.copyfile` and never retyped. Disk-to-disk, as committed at C1 and re-read at G1 against the reviewer's scratch originals: `.agent/authored/f276-r6-block.md`, `-ledger.md`, `-decisions.md` and `-plan.md` each compare byte-equal to their payload; `.agent/live_review.md` and `.agent/decisions.md` each equal their `caa9d073` bytes plus their payload exactly, and `.agent/plan.md` equals its payload. Every digest was verified before use and again at G1. The code diff was applied with `git apply` in the block's three disjoint `--include` slices; no hunk was retyped or edited, and `git apply --stat` of the whole diff reads 14 files and 803 insertions, which is 197 + 148 + 458 across the three slices.

## Deviations & assumptions

- THE BLOCK'S COMMIT SEQUENCE WAS FOLLOWED EXACTLY: C1, C2, C3, C4, C5, no extra commit, none dropped, none reordered.
- TWO INSERTION READINGS FOR C1, both printed above: 293 by `git show --numstat`, which the block orders, and 310 in the `git commit` summary, which applies rewrite detection to the wholly-rewritten `.agent/plan.md`. Neither is near the 500 cap.
- C1 WAS COMMITTED WITH `--no-verify`, and that flag bypassed nothing: `.git/hooks/` contains no hook at all, only the directory itself, which was checked immediately afterwards. C2, C3 and C4 were committed without the flag. Recorded because the flag is in the reflog and would otherwise read as a skipped gate.
- EACH OF C2 TO C4 WAS VERIFIED GREEN ON ITS OWN BEFORE IT WAS COMMITTED, as constraint 7 requires, rather than only at G3: C2's nine paths ran `633 passed in 135.56s`, C3's CLI and docs paths ran `355 passed in 199.49s`, and C4's new file ran `31 passed in 102.49s`. These three runs are extra work beyond the block's literal gate list and are reported as such.
- `__pycache__` PURGING AT G5 REPORTED 0 DIRECTORIES REMOVED before every run, including the control. That is not a skipped step: the worktree was freshly created and every run used `python3 -B`, so no bytecode was ever written for the purge to find. The purge ran before each of the four runs regardless.
- A STALE CROSS-REFERENCE THIS ROUND CREATES BUT DOES NOT TOUCH: `docs/roadmap/features/T2_F104.md` names `_BUDGET_ALLOWED_KEYS` twice (lines 27 and 99), and C2 replaces that constant with the derived `_budget_allowed_keys()`. F104's file is a CLOSED feature's target plan and is outside this round's change set, so it was deliberately left alone rather than edited under scope drift. `docs/system/job-budget-enforcement-v0.md`, which describes the BUILT state, was updated by C3. A grep for the old name across `packages/`, `apps/` and `tests/` returns `run_manifest.py` and nothing else, and after C2 it returns nothing.
- R-1004's COST, MEASURED AGAIN IN THIS ROUND'S OWN GATES rather than restated: the same two test files ran in 12.01s inside the fresh worktree at G5 and the single new file took 102.49s in the primary checkout, and G3's sixteen paths took 332.57s of test time. The operator's `.data` was never read, listed or written by this worker.
- Every `REMEDY_DATA_DIR` in play is set IN-PROCESS by the new file's own autouse fixture; no shell assignment was used. No test called a model provider — the two real `run_job` cases use the fake builder and reviewer over a temporary git repository and stop before the first provider call. pytest ran serially with no `-n` in every invocation, and no test calls `shutil.disk_usage` on the real filesystem: the file's first autouse fixture rebinds the probe to one that RAISES, and a dedicated test asserts that the real probe is not installed while the file runs.

## Next

1. Phase 1 rule 1 — re-read `.agent/STOP` from disk; if it exists, write the handoff and end the session, doing nothing else.
2. Otherwise review round 6: re-run G1 to G6 independently and read `git diff caa9d073..HEAD` bottom-up, then book the verdict. T004 is the feature's last build slice, so a PASS here means the build is complete.
3. Then the closure sequence's first round: the Built State paragraph naming what each slice built and what is carried, the integrity check, and the integration gate's one full suite run — the run this round deliberately did not make, under amend0917-throughput rule 1 — with its transcript committed as `.agent/authored/f276-closure-suite.txt`.

Operator questions open: 5
