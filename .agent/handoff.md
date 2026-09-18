# Handoff — F268 remedy do: the one-command start · Round 10 (deletion round: the do v1 flow and dry_run_autorun)

## Session

SESSION 2 of feature F268 · round 10 · rounds so far 10

## Range

Review of 4362894d..HEAD — branch `feature/f268-remedy-do`.

## Summary

Round 10 is a deletion round (amend0906-triage-throughput (1)). It booked round 9's PASS and R-0933's `Done:` line (C1). It deleted the phased `remedy do` v1 flow that round 9 left with no caller from `packages/orchestration/do_run.py`, and `dry_run_autorun` / `_autonomy_label` from `packages/orchestration/autorun.py` (C2). It deleted their tests (C3) and rewrote the do guide to describe the sequence (C4). G2 reads `1023 passed, 6 skipped`, exit 0. G3 reads 117 hits at `4362894d` and 0 at `34e51da9`. G4 reads `All checks passed!`.

- **C2 (a):** `do_run.py` keeps `DoRunNextAction`, `_REMEDY_CMD_RE` and `validate_next_safe_action_command`, with a new module docstring and only the `re` and `dataclass` imports. Before deleting, a grep of every other symbol (`DO_PHASES`, `DoRunPhase`, `DoRunStopReason`, `DoRunResult`, `_DO_V1_MAX_AUTONOMY`, `DoRunContract`, `_check_contract`, `run_do`, the four `_run_*_phase` helpers, `export_do_run_json`, `summarize_do_run`, `_do_emit`) over `apps/`, `packages/`, `scripts/`, `tests/`, `docs/` (minus `docs/roadmap/`) and `README.md` found callers only in `do_run.py` itself and in the tests C3 deletes. `repair_loop.py` imports only `DoRunNextAction`.
- **C2 (b):** `dry_run_autorun` and `_autonomy_label` had callers only in `tests/cli/test_job_commands.py`, the two tests C3 deletes. The module docstring no longer names them and no longer calls the module `remedy do`'s loop. Autonomy level 0's line now reads "create the job only", which is what `run_autorun` does at level 0; the old line described the dry run. `run_autorun` is untouched.
- **C2 (c):** `do.run`'s description now reads `Plan and run what you ask: study the repo, plan a mission of jobs and their tasks, run the first job, and stop before apply unless --apply.` `tests/docs/test_vocabulary.py` reads 8 passed: Plan and Run carry `task`, and Mission carries `job`. `do_cmd.py`'s module docstring now describes the sequence and names the other handlers the module holds.
- **C4:** `docs/guides/do-run-v1.md` is rewritten in full. It covers the seven `DO_SEQUENCE` steps in order, one line each, the stop before apply, `--plan-only`, `--step-by-step`, the twelve `--json` keys `_cmd_do_order` prints, the flag list from the `do.run` entry and `validate_next_safe_action_command`. The title changed from "remedy do v1 — Cohesive Flow", which is no longer true, to "remedy do — the one-command start". `docs/system/run-contract-v1.md` lines 5, 55 and 68 no longer name `do_run`. `docs/guides/autocoder-usage.md` lines 152 and 160 no longer name `--max-cycles`, and `repair_budget_exhausted` is kept. Smoke line 1987's comment and line 2072's message no longer say a repair loop ran.

### Tests deleted BY DESIGN (C3), each checked against its body first

`tests/orchestration/test_do_run.py`: 69 → 17 tests, so 52 were deleted. Every deleted test calls `run_do` (through `_run_with_tmp` or directly), `export_do_run_json`, `summarize_do_run` or `_run_build_phase`, or constructs `DoRunPhase` / `DoRunStopReason` or reads `DO_PHASES`. All of these symbols were deleted in C2.

| Test(s) | Reason |
|------|--------|
| `TestPhaseModel::test_phases_defined`, `::test_phase_dataclass`, `::test_stop_reason` | Read `DO_PHASES`, `DoRunPhase`, `DoRunStopReason` |
| `TestDoRunFlow` (11 tests) | Every one runs `run_do` through `_run_with_tmp` |
| `TestDoRunExport` (7) | `run_do` + `export_do_run_json` |
| `TestDoRunSafety` (6) | `run_do` + `export_do_run_json` / `summarize_do_run` |
| `TestApprovalGate` (6 of 7: `test_stop_before_apply_default`, `test_no_source_apply_without_approval`, `test_no_apply_phase_before_approval`, `test_patch_intent_not_approved`, `test_proof_not_verified_before_apply`, `test_next_action_is_approval`) | `run_do`; `test_no_apply_import_in_do_run` is kept |
| `TestContextProofAlignment` (2) | `run_do` |
| `TestDoRunSummary` (3) | `run_do` + `summarize_do_run` |
| `TestNextSafeActionValidation::test_all_emitted_actions_valid`, `::test_low_autonomy_action_valid` | Validate a `run_do` result's next action; the other 8 are kept |
| `TestContextFailureStops` (3) | Patch `do_run._run_context_phase`, run `run_do` |
| `TestContractConsolidation::test_contract_in_result` | Reads `run_do`'s `_contract`; the other 3 are kept |
| `TestMaxLoopsEnforcement` (4) | `run_do` |
| `TestAutonomyTruth` (3) | `run_do` |
| `TestSystemArtifactKeepsTaskIdAbsent::test_the_build_phase_on_a_task_less_job_leaves_task_id_absent` | Imports `_run_build_phase` |

Its dead helpers `_make_repo` and `_run_with_tmp`, the imports `json`, `os`, `Path`, `patch` and `normalize_job_id`, and the deleted symbols' import names all went. The module docstring was rewritten to cover what remains.

Kept (17): `TestPhaseModel::test_next_action`, `::test_contract_defaults`; `TestApprovalGate::test_no_apply_import_in_do_run`; 8 × `TestNextSafeActionValidation`; 3 × `TestCatalogMetadataTruth`; `TestContractConsolidation::test_contract_has_source`, `::test_contract_has_allowed_actions`, `::test_contract_has_denied_actions`. All are byte-identical to `4362894d`.

| Other test | Reason |
|------|--------|
| `tests/orchestration/test_run_contract.py::TestApprovalGateRegression::test_no_fake_apply_phase` | Imports and runs `run_do` |
| `tests/orchestration/test_test_failure_repair.py::TestDoRunIntegration` (3 tests) + its docstring line "Step 949: Integration — failure_summary field in DoRunResult" | Construct `DoRunResult`, call `export_do_run_json` |
| `tests/cli/test_job_commands.py::TestRemedyDo::test_dry_run_no_side_effects`, `::test_dry_run_phases_by_autonomy` | Call `dry_run_autorun` |
| `tests/orchestration/test_test_runner.py::TestPatchApplyTestLoop::test_autorun_has_test_phase` | Scans `autorun.py` for `run_tests`, a string only `dry_run_autorun` held |

No other test went red (G2).

## Commits

### 170d4753 F268 R10 C1: bookkeeping — book round 9's verdict, R-0933 resolved, round 10 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r10-block.md` | +107 / -0 | Byte copy of the block |
| `.agent/authored/f268-r10-ledger.md` | +4 / -0 | Byte copy of ledger.md |
| `.agent/authored/f268-r10-plan.md` | +23 / -0 | Byte copy of plan.md |
| `.agent/live_review.md` | +4 / -0 | `4362894d` bytes + ledger.md (Gate F268 R9 PASS, `Done: R-0933`) |
| `.agent/plan.md` | +6 / -9 | := plan.md |

### 41d1e2ff F268 R10 C2: deletion — the do v1 flow leaves do_run.py, dry_run_autorun leaves autorun.py, the do.run description and do_cmd docstring describe the sequence
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/do_run.py` | +9 / -613 | (a) keeps the three survivors |
| `packages/orchestration/autorun.py` | +7 / -86 | (b) `dry_run_autorun`, `_autonomy_label`, docstring |
| `apps/cli/command_catalog.py` | +1 / -1 | (c) `do.run` description |
| `apps/cli/commands/do_cmd.py` | +8 / -1 | (c) module docstring |

### c59b2498 F268 R10 C3: test deletion — the tests of the deleted do v1 flow and dry_run_autorun leave, by design
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_do_run.py` | +8 / -550 | 52 tests, helpers, imports; docstring rewritten |
| `tests/orchestration/test_run_contract.py` | +0 / -11 | `test_no_fake_apply_phase` |
| `tests/orchestration/test_test_failure_repair.py` | +0 / -34 | `TestDoRunIntegration` + docstring line |
| `tests/cli/test_job_commands.py` | +0 / -14 | Two `dry_run_autorun` tests |
| `tests/orchestration/test_test_runner.py` | +0 / -5 | `test_autorun_has_test_phase` |

### 34e51da9 F268 R10 C4: docs — the do guide describes the sequence, the run contract page, autocoder guide and smoke text stop naming the deleted flow
| Path | +/- | Reason |
|------|-----|--------|
| `docs/guides/do-run-v1.md` | +73 / -106 | Rewritten in full |
| `docs/system/run-contract-v1.md` | +3 / -5 | Lines 5, 55, 68: no `do_run` caller |
| `docs/guides/autocoder-usage.md` | +2 / -2 | Lines 152, 160: no `--max-cycles` |
| `scripts/remedy_smoke.sh` | +2 / -2 | Lines 1987, 2072 |

### C5 (this commit) F268 R10 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines; the largest is C1 with 144.

## External actions

- `git push origin feature/f268-remedy-do` after C4: pushed `4362894d..34e51da9`.
- `git push origin feature/f268-remedy-do` after C5 (this commit).
- No PR, worktree or gh action.

## Verification

All gates ran after C4 at `34e51da9` and before C5.

- **G1** (python byte check): `ledger.md True`, `plan.md True`, `block.md True` (sha256 against the block's digests); `append True` (`.agent/live_review.md` == `git show 4362894d:.agent/live_review.md` + ledger.md); `plan True` (`.agent/plan.md` == plan.md).
- **G2** — the block's exact command, output in `.remedy-wt/f268-r10/g2.txt`: `1023 passed, 6 skipped in 81.17s (0:01:21)`, then `pytest exit 0` (the chain was `… && print('pytest exit 0') || print('pytest exit NONZERO')`). The 6 skips are all `tests/regression/test_named_bugs.py` "D3 quarantine (F252)" (lines 295, 312, 321, 387, 396, 403), read with `-rs` on the same list.
- **G3** — `.remedy-wt/f268-r10/g3.py <rev>` reads `git ls-tree`/`git show` at the revision over apps/, packages/, scripts/, tests/, docs/ (minus docs/roadmap/) and README.md:
  - `4362894d: files scanned 1300, hits 117`: 56 in `do_run.py`, 4 in `autorun.py`, 5 in `test_job_commands.py`, 40 in `test_do_run.py`, 2 in `test_run_contract.py`, 10 in `test_test_failure_repair.py`.
  - `HEAD: files scanned 1300, hits 0`, with HEAD at `34e51da9` (`--print` printed no hit lines).
- **G4** — `python3 -m ruff check` over the nine touched .py files (`do_run.py`, `autorun.py`, `command_catalog.py`, `do_cmd.py`, `test_do_run.py`, `test_run_contract.py`, `test_test_failure_repair.py`, `test_job_commands.py`, `test_test_runner.py`): `All checks passed!`
- **G5** at `34e51da9`, after the first push: `git status --porcelain` printed nothing. `git rev-parse HEAD origin/feature/f268-remedy-do` printed `34e51da9e75a61bc7b25c8fa3463fca8558618dd` twice. `git worktree list` showed one row (`/home/decodeux/Repos/remedy 34e51da9 [feature/f268-remedy-do]`), and the `remedy/job-*` branch count was `31`. The same checks run again after the C5 push, and the round report carries that run.

## Authored-text proofs

- The digests of `ledger.md` (`67ce92ee…48c6`) and `plan.md` (`34982dfe…2ec2`), and the block's own (`a995d010…cdc`), matched before use.
- Byte copies are at `.agent/authored/f268-r10-{block,ledger,plan}.md`.
- `.agent/authored/f268-r10-block.md` sha256: `a995d010b4fc114b2e1e533c360da4ae265876a527b504e59d4e6a5fa8383cdc`.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `170d4753` |
| C2 production deletion (a)(b)(c) | done | `41d1e2ff` |
| C3 test deletion | done | `c59b2498` |
| C4 docs | done | `34e51da9` |
| C5 handoff | done | This commit |
| R-0933 | done | Booked `Done:` in C1 |

## Open findings

125 open by distinct id, from `.remedy-wt/f268-r4/count.py`: HEAD has 140 registrations and 15 `Done:` ids. That is round 9's 126 minus R-0933, booked in C1. This round opens no finding.

## Deviations & assumptions

- **Commit sequence:** as ordered (C1, C2, C3, C4, C5). Between C2 and C3 the tree is red by design: the tests C3 deletes import symbols C2 deleted.
- **Pushed before the handoff.** C1 to C4 were pushed before C5 so that G5 could be read with real output. C5 is pushed after.
- **Outside the change set, left untouched:**
  - `docs/README.md:125` still describes the guide as "`remedy do` cohesive flow".
  - `packages/orchestration/ui_server.py:3192`'s docstring still names `do_run` as a lazy importer of the catalog. That remains true: `validate_next_safe_action_command` imports it inside the function.
- **Pre-existing red outside G2:** `tests/cli/test_product_spine.py` reads 3 failed: `TestJobFirstHappyPath::test_happy_path_starts_with_do`, `::test_happy_path_has_job_show` and `TestDoRunHelpAlignment::test_happy_path_uses_do_run`. They assert that the quick start's first line is `remedy do` and that it names `job show`. All three read `_QUICK_START` from `apps/cli/grouped.py`. That file is unchanged since `4362894d` (`git diff 4362894d --stat -- apps` names only `command_catalog.py` and `do_cmd.py`), so the three failures were already there before this round. With C4's docs changes stashed, the tree read the same 3 failed. The file is not on G2's list, and the round does not repair it.
- **The guide's validator section.** `validate_next_safe_action_command` is described as what it is: a catalog check that `repair_loop`'s callers and the tests use. `do`'s own `Next:` lines are not passed through it, and the guide does not claim they are.
- **The shell guard refuses `$?` and `${PIPESTATUS}`,** so G2's exit status comes from an `&& … ||` chain.

## Next

Reviewer: review round 10 and book its verdict in the next round's first commit. Then the closure sequence (docs/roadmap/STATUS_closure_protocol.md). Operator questions open: 3.
