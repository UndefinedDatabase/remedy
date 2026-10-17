# Test audit 2026-10-17 — baseline, cost, evidence ledger

Pinned at main `2039a6ae7` (PR 349 merged), worktree `.remedy-wt/test-audit`. Reference: the
OpenClaw test-audit skill (SKILL.md, CAMPAIGN.md, references/audit.md), adapted to pytest. Marks
follow CAMPAIGN.md: `R` retain, `F` retain and repair the assertion, `C` consolidate into a named
keeper, `D` delete with the remaining proof named. A smell count is a candidate list, never a
verdict: nothing below was marked from a file name or a pattern match alone.

## 1. Baseline (static, this tree)

| Measure | Value | Previous review |
|---|---|---|
| Test files (`tests/**/test_*.py`) | 775 | ~769 |
| Declared test functions | 17 765 | ~17 720 |
| Collected nodes (parametrized) | 21 539 | — |
| Test LOC / support LOC (conftest, helpers) | 291 900 / 2 392 | ~293 000 together |
| Non-Python fixture files under `tests/` | 61 | — |

By directory (files / tests / LOC): orchestration 541 / 12 109 / 198 708; top level 68 / 2 642 /
34 218; cli 116 / 1 901 / 36 989; ui_server 17 / 347 / 10 621; docs 10 / 336 / 3 420; runtimes
8 / 195 / 5 322; regression 9 / 107 / 1 967; ui_contracts 3 / 71 / 712; schemas 2 / 43 / 361;
storage 1 / 14 / 357. Largest owners by imports: `pingpong_job` 64 files / 1 529 tests,
`pingpong_loop` 17 / 945, `run_manifest` 37 / 638, `core.models` 27 / 633, `command_catalog`
16 / 479.

## 2. Cost

- Full suite, newest green record (`~/.remedy-loop/test_load.jsonl`, 2026-10-17 14:58Z, `pytest -n
  auto`, 6 workers): 21 572 tests, 332 s wall, 1 092 CPU s. Ten modules carry 26 % of the CPU,
  50 modules 57 %, 100 modules 74 %.
- Slowest modules (CPU s): runtimes/test_supervisor_portability 45.5, cli/test_mission_cmd 39.4,
  orchestration/test_review_zip_hygiene 33.4, cli/test_do_scale_matrix 30.0 (10 s per test),
  cli/test_do_sequence_cli 26.8, test_grouped_cli 23.7, cli/test_golden_path 18.6,
  cli/test_json_contract 17.7, orchestration/test_job_task_runner 16.9, test_job_apply_commit 16.1.
- Collection: 4.9 s warm (22.6 s cold: fresh `__pycache__` and assertion rewrite) for 21 539
  nodes; under `-n auto` every worker collects again, about 30 CPU s of 1 092 (3 %). Not the
  bottleneck.
- Subprocess: 286 files that spawn a process (subprocess, Popen, `sys.executable`) hold 6 872
  declared tests (39 %) and 800 of 1 030 attributed CPU s (78 %). Fixture setup is small: in
  test_job_task_runner setup is 0.7 s of 36.5 s; a fake two-task `run_job` spends its time in
  13 git subprocesses and JSON encoding (production cost, out of this audit's scope).
- Coverage: not measured on this tree (a full-suite run was not authorized this session); the
  only artefact, `.coverage_reports/coverage.json`, is from 2026-06-17 and stale. The batch below
  is proven by owner branch coverage and mutations instead.

## 3. Existing gates

- `remedy ci run` stages (`packages/orchestration/ci_stages.py`), collected here: `fast` 5 371,
  `standard` 16 076, `ui` 71, `smoke` 25, `budgets` 7 files by path, `excluded` 5 (real Ollama).
- `fast` is not fast: 189 files, 75 of which spawn processes (1 562 tests), 404 CPU s (39 % of
  the suite). Cause: the `subprocess` marker comes from a hard-coded 21-name list in
  `tests/conftest.py`, so a new subprocess file lands in `fast` by default.
- `scripts/remedy_test_fast.sh` runs three fixed files (`test_worker_facade_cmd`,
  `test_development_artifact_boundary`, `test_product_spine`). It shrank from eight as F275
  deleted the others; its header still lists the deleted lanes, and `tests/README.md` describes
  it as a marker lane ("excludes subprocess, real_ollama ..."), which it is not. Two guard files
  pin its text by source grep (`tests/test_test_categories.py`, `tests/cli/test_product_spine.py`
  TestFastLaneSelfTest): copied-inventory guards with no behavioral contract.
- `remedy_test_runtime.sh` (3 files), `remedy_test_integration.sh` (smokes + full minus
  real_ollama/slow), `remedy_test_full.sh` (full), `remedy_coverage.sh`; no change-aware lane.

## 4. Suite-wide candidate counts (unverified; for triage only)

Exact body clones (names stripped, literals kept, bodies of 4+ lines): 86 groups / 192 tests;
structural clones (literals stripped too): 495 groups / 1 358 tests, mostly table cases a
`parametrize` would fold (LOC only, no proof lost or gained). Shadowed test definitions: 1. Test
files importing a private (`_name`) production symbol: 215 (1 042 imports). Call-shape asserts
(`assert_called`, `call_args`, `call_count`): 64 files / 901. Source reads (`inspect.getsource`,
`ast.parse`, `.py` read_text): 111 files / 269. Production top-level names referenced only by
tests or scripts: 84 (heuristic; `__all__`, `getattr` and CLI-registry callers give false
positives, so none is a seam until its callers are read).

## 5. Ledger — four owners

### Lane 1: task routing and planning (54 files, 2 206 tests, 112 CPU s)
| Test | Mark | Evidence |
|---|---|---|
| test_model_routing `TestOverrideRuleNamesAreNotHardRuleNames` and `TestRoundSixCallsAreUnchanged` `::test_hard_rule_names_still_holds_exactly_the_names_round_five_shipped` | D (follow-up) | Byte-identical copies of `::test_hard_rule_names_carries_exactly_those_three_in_a_declared_order` (keeper; the order is reported to the operator). Saves ~14 LOC, no runtime. |
| test_model_routing rule-name tuple tests (hard, promotion, schema) | R | Observable ordering of reported rule names; one per tuple. |
| test_role_config `test_each_known_role_resolves` / `test_every_known_role_resolves_exactly_as_before` | D (follow-up) | Same body; read before deleting which one names the contract. |
| test_task_granularity split/merge tables, test_job_plan pairs | R | Same shape, different inputs: table cases, not duplicates. |

### Lane 2: Pi execution and execution guards (19 files, 619 tests, 26 CPU s)
Little safe reduction. The Pi files (test_pi_provider, _events, _loop_limits, _turn_counts,
_timeouts) are recent, small and boundary-shaped; the exec guard, tool sandbox and scratch-file
guard are security contracts (retention bar). `test_repair_loop` structural clones are table
cases (C via parametrize, LOC only). `test_commit_execution_gate` needs_tests/needs_repair: R
(different verdicts).

### Lane 3: verification and job lifecycle (55 files, 2 010 tests, 84 CPU s)
| Test | Mark | Evidence |
|---|---|---|
| test_job_task_runner, completion-gate and target-guard family (batch 1) | C/D | Section 6. |
| test_job_task_runner continuation-config family (TestContinuationConfig, TestMaxRounds-, TestTestCommand-, TestWriteMode-, TestConfigSourceAudit, TestCommandPathFullConfigContinuation, TestCommandPathExplicitOverrides) | C (batch 2 candidate) | ~30 tests, 2 `run_job` runs each, ~15 of the file's 36 s. Partial overlaps (e.g. `test_continuation_sources_persisted` holds every "persisted" source, per-field tests hold the values): one table per field (persisted / restored / override) would keep every value check. Needs its own ledger pass; not done here. |
| test_job_task_runner `TestApplySafetyReuse` vs `TestStrictWorkspaceApply` | F (follow-up) | Strict's traversal/.env/.git rows assert only `!= ""`; Reuse asserts the reason token. Keep the stronger form, fold one into the other. |
| test_test_execution_service `test_uses_popen_not_subprocess_run`, `test_no_subprocess_run_in_execute_path`, `test_start_new_session_used`, `test_stdin_devnull` | F (follow-up) | `inspect.getsource` greps of the private `_run_isolated_process`; the first two are identical. Replace with one behavior test (child sid differs, stdin reads EOF) before deleting the greps. |
| test_verifier, test_final_verifier table cases | R | Distinct inputs per rule. |

### Lane 4: review evidence and public API (93 files, 2 049 tests, 110 CPU s)
| Test | Mark | Evidence |
|---|---|---|
| test_review_subject_resolution `test_a_non_git_directory_with_a_declared_base_blocks` | D (follow-up) | Same proof as test_review_subject_explicit_base `test_a_declared_base_in_a_non_git_directory_blocks` (only the base literal differs); both from 2026-07-17. |
| test_public_api `test_interface_route_answers_the_command_envelope` / `test_the_same_route_over_the_supervisors_socket_answers_the_same_body` | R | Same body, different transport: an independent API contract. |
| test_public_api auth/404/409 rows, test_command_channel 403 rows | R | Authorization contracts (retention bar). |
| `review_subject` spread over 33 files | — | Fragmentation, not duplication; consolidating files buys nothing measurable. |

## 6. Batch 1 — test_job_task_runner completion gate and target guards

Owner `packages/orchestration/pingpong_job.py` (`validate_job_task_result`, `run_job`'s pre- and
post-apply target guards). This file is their only test file (grep of `validate_job_task_result`
and `target_repo_mutated` under `tests/`).

| Removed or folded | Mark | Remaining proof |
|---|---|---|
| TestMissingReviewerOutputGate `test_reviewer_pass_with_findings_still_blocks`, `test_reviewer_fail_still_blocks`, `test_target_mutated_still_blocks` | D | Identical inputs and asserts in TestCompletionGate (`_with_findings_blocks`, `_fail_blocks`, `_target_mutated_blocks`). |
| TestNoTestCommandValid `test_no_test_command_without_reviewer_blocks` | D | Identical to TestMissingReviewerOutputGate `test_missing_reviewer_with_test_none_blocks`. |
| TestCommandPathExplicitOverrides `test_provider_override_to_fake` | D | Byte-identical to TestProviderOverrideToFake `test_cli_handler_provider_override`. |
| TestCommandPathPreApplySmoke `test_handler_clean_run_unaffected` | D | Byte-identical to TestCommandPathGateSmoke `test_normal_two_task_job_completes`. |
| TestTargetMutationNegative `test_target_mutation_blocks_job` | D | Every assert is in the pre-apply keeper (task 2 never runs, so its first-call-only mutation is the keeper's scenario). The README-rewrite test stays: a tracked file modified, not added. |
| TestMissingReviewerE2E (3) + TestMissingReviewerReport (3) | C | One run, keeper `TestMissingReviewerE2E::test_missing_reviewer_blocks_the_job_unapplied_and_both_reports_say_so`, all asserts carried. |
| TestPreApplyTargetGuard (6) + TestPreApplyTargetGuardReport (4) | C | One run, keeper `TestPreApplyTargetGuard::test_mutation_before_apply_blocks_the_job_unapplied_and_both_reports_say_so`, all asserts carried (incl. "after_apply" not in the error). |
| TestTargetMutatedResultGatePreserved (4) | C | One run, keeper `::test_target_mutated_result_blocks_at_the_gate_unapplied`. |
| TestCorruptedResultJobBlock `test_blocked_result_not_applied`, `test_task2_does_not_start_after_block` | C | Folded into `::test_test_failed_but_final_pass_blocks_unapplied_before_task2` (same `test_passed=False` scenario). |

Result: 217 → 191 tests, 3 857 → 3 415 lines (+48 / -490), serial wall 36.5 s → 36.3 s (two
runs), i.e. no runtime gain worth the name: the folded runs block at task 1 and cost ~0.03 s
each, and the two deleted handler copies ~0.25 and ~0.7 s. The gain is maintenance (442 lines
and 26 tests fewer to keep in step), not time. Owner branch coverage from this file unchanged: 1 220 lines and 375 branches
executed before and after, none lost. Mutations of the owner, each restored byte for byte
(sha256 checked): pre-apply guard never fires; missing reviewer output passes the gate;
`result.target_mutated` ignored; a failed last-round test passes. Each turns its keeper red.
Finding from the first mutation: the handler-level `test_handler_mutation_blocks` stays green
without the pre-apply guard, because the post-apply guard's `target_repo_mutated_after_apply`
contains the substring it checks; only the keeper's "after_apply" assertion separates the two.
Production code removed: none (no test-only seam in this family).
The batch removes 25 `assert` statements (548 to 523), each a duplicate of one that still runs;
`tests/regression/test_f293_acceptance.py` holds an assertion floor for this file (525), so the
same commit records the 2 below it in `ALLOWED_REMOVALS`, as that guard prescribes. The guard was
found by the change-aware fast lane's first run, not by running the owner file alone.

Also: test_proposed_tasks `TestMaterialization` defined `test_materialize_non_approved_raises`
twice; Python kept only the second, so the first never ran. The dead copy is deleted (collected
count unchanged).
