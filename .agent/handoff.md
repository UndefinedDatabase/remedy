# Handoff — F269 Contract & contract templates · Round 5 (`do`'s gate)

## Session

SESSION 1 of feature F269 · round 5 · rounds so far 5

Context self-assessment: the round fit in one worker context with room to spare. Every gate below was run in this session at C4 `b2408828`; none was carried over from memory.

## Range

Review of 09d7641f..HEAD — branch `feature/f269-contract`.

## Summary

Round 5 lands DECISION F269 D6:

- C1 books round 4's verdict (ledger), appends DECISION F269 D6, writes the round 5 plan, and saves the payloads and the block.
- C2 (D6 (1)): `merge_contract_slice_into_dod` gives a whole-mission criterion's check `blocking` false, and a milestone-scoped criterion's check keeps the criterion's `blocking` (`c.blocking and bool(c.milestones)`).
- C3 (D6 (2)): `run_job`, when every task has passed, runs `dod_gate.run_job_gate` in `job.job_workspace_path` before the `finally` finalizes the workspace. A gate that holds sets the job `blocked` with `gate_blocker`'s `dod_blocking_red:<ids>`, so `_finalize_job_workspace` keeps the worktree. A job with no stored DoD is ungated and writes no result. For a job that `mission_for_job` finds, `record_contract_results` then reads the result onto the job's slice, with the milestone from `read_job_milestone`.
- C4 (D6 (3), (4)): `_step_shape` merges each job's slice into its DoD as it links the job (milestone None, so the slice is the whole-mission criteria). `do --json` gains `unmet_blocking_criteria` (`contract_blockers` over the walk's contract, `[]` without one). The text output prints one line after the step lines: `Contract: <met> of <all> criteria met; blocking criteria not met: C001 (unmet), ..., C008 (open)`, or `...; every blocking criterion is met`. `docs/guides/do-run-v1.md`'s `--json` key list names the field.
- C5 is this handoff.

## Commits

### b894529a F269 R5 C1: bookkeeping — round 4 verdict, DECISION F269 D6, the round 5 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f269-r5-block.md` | +96 / -0 | Byte copy of block.md |
| `.agent/authored/f269-r5-decisions.md` | +32 / -0 | Byte copy of decisions.md |
| `.agent/authored/f269-r5-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f269-r5-plan.md` | +26 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +32 / -0 | `09d7641f` bytes + decisions.md (D6) |
| `.agent/live_review.md` | +2 / -0 | `09d7641f` bytes + ledger.md (Gate F269 R4 PASS) |
| `.agent/plan.md` | +8 / -9 | := plan.md |

### e362fd9d F269 R5 C2: a whole-mission criterion's check enters a job's DoD non-blocking, a milestone-scoped one keeps its blocking
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/mission_contract.py` | +12 / -2 | The merge overrides each slice check's `blocking` with `c.blocking and bool(c.milestones)`. The docstring states D6 (1), and so does the module docstring |
| `tests/orchestration/test_mission_contract.py` | +26 / -1 | Three tests over the `sliced` fixture. The whole-mission C001, blocking with a blocking compiled check, enters as `ctr-C001` with `blocking` False. The M1-scoped blocking C002 enters as `ctr-C002` with `blocking` True. A job with no milestone gets only `[("ctr-C001", False)]` |
| `tests/orchestration/test_mission_gate.py` | +26 / -2 | UPDATED BY DESIGN: `test_the_job_gate_decides_two_met_and_one_unmet` asserted `gate=blocked`; its only red check is the whole-mission C003's, so under D6 (1) it asserts `gate=released`. Its property (two met, one unmet, every evidence_ref naming the job) is kept. NEW `test_a_red_whole_mission_check_releases_the_job_but_holds_the_mission`: the job's DoD reads `{acc-001: True, ctr-C002: False, ctr-C003: False}` (the milestone DoD's `acc-001` is C001's check, so C001's is not added twice). The gate result is released, with `blocking_red == []` and `reported_red == ["ctr-C003"]`. C003 reads `unmet`, and `evaluate_move`'s achieve refusal names C003 |

### 3483cb0a F269 R5 C3: run_job runs the job's DoD gate before its worktree goes — a holding gate blocks the job, a mission job's slice reads the result
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_job.py` | +40 / -1 | NEW `_gate_job_definition_of_done(job)` returns the blocker or `""`, and calls `record_contract_results` for a mission job. In `run_job`, `dod_blocker = ... if all_done else ""`, then `if dod_blocker: blocked + error` / `elif all_done:` (the existing completed branch, unchanged) |
| `tests/orchestration/test_pingpong_job_dod_gate.py` | +174 / -0 | NEW. Four tests use the real `parse_job_file` → `run_job` over a tmp git repository, with `builder_name`/`reviewer_name` `fake` and `custom_cmd` checks running `python3 -c`. (1) A red BLOCKING check ends the job `blocked` with the error `dod_blocking_red:chk-red`. Its `worktree_cleanup_status` is `retained`, and the worktree and its `docs/README.md` still exist. (2) A red non-blocking check lets the job complete, with the worktree `clean` and `reported_red == ["chk-reported"]`. (3) With no stored DoD the job completes `clean`, and no `dod_result.json` exists. (4) A mission contract has whole-mission C001 (passes) and C002 (fails), M1 C003 and M2 C004. The job is linked, its milestone M1 is recorded and its slice merged. The job completes, and the criteria read `met`/`unmet`/`met`/`open`, each with an evidence_ref `<job>:ctr-<id>` (C004 has none) |

### b2408828 F269 R5 C4: do merges each job's contract slice into its DoD, and its result names the blocking criteria not met
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/do_sequence.py` | +40 / -2 | `_step_shape` merges `merge_contract_slice_into_dod(<linked mission>, None, job_id)` after each link. NEW `do_unmet_blocking_criteria(contract)` and `do_contract_summary_line(contract)` |
| `apps/cli/commands/do_cmd.py` | +12 / -2 | `--json` gains `unmet_blocking_criteria`. The text output prints the `Contract:` line when the walk has a contract. The docstring is updated |
| `docs/guides/do-run-v1.md` | +7 / -2 | The `--json` key list names `unmet_blocking_criteria`, with one bullet |
| `tests/cli/test_do_sequence_cli.py` | +83 / -3 | NEW `test_contract_cli_tool_gates_the_job_on_its_whole_mission_checks_and_names_the_unmet`. The job's DoD holds exactly the whole-mission checks, all non-blocking, the gate releases and the job completes. `The test suite passes.` reads `unmet` with an evidence_ref starting `<job>:`, and the three hygiene criteria read `met`. `unmet_blocking_criteria` is the four suite-judged template criteria (`unmet`) plus the planner criteria (`open`), in contract order. The text walk's `Contract:` line equals `Contract: 3 of <n> criteria met; blocking criteria not met: <each id (status)>`. NEW `test_a_do_whose_order_proposes_no_template_names_only_criteria_not_met`: there is no template, the job stores no DoD, every criterion is a blocking planner criterion reading `open`, and `unmet_blocking_criteria` is their ids. UPDATED BY DESIGN: `_template_criteria` and `_contract_by_origin` now drop `status` and `evidence_ref` (NEW `_as_compiled`), because the gated job now writes them after the run. The three website tests keep their property: the template's criteria arrive unchanged in ids, texts, origin, scope, check and blocking, in order, and none is dropped |

### C5 (this commit) F269 R5 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | This file |

## External actions

- `git worktree add --detach .remedy-wt/f269-r5-g4 HEAD` (at `b2408828`) for G4. It was removed with `git worktree remove --force .remedy-wt/f269-r5-g4`. `git worktree list` afterwards: `/home/decodeux/Repos/remedy  b2408828 [feature/f269-contract]`.
- `git push` runs after this commit. Its outcome and G5 are in the worker's final report.
- No PR was created, edited or merged.

## Verification

All gates ran at C4 `b2408828` with a clean tree, through `.remedy-wt/f269-r5/run_gate.py`, which prints a subprocess's return code as `EXIT`.

G1 transport + state, `python3 .remedy-wt/f269-r5/g1.py`, EXIT 0:
```
ledger.md digest matched: True
decisions.md digest matched: True
plan.md digest matched: True
authored copy ledger.md True
authored copy decisions.md True
authored copy plan.md True
authored copy block.md True
True
```

G2, `python3 -m pytest -q -p no:cacheprovider` over the block's 19 paths plus `tests/orchestration/test_pingpong_job_dod_gate.py` (the round's one new test file; the three edited test files are already in the block's list), EXIT 0:
```
1195 passed in 193.14s (0:03:13)
```

G3, `python3 -m ruff check packages/orchestration/mission_contract.py packages/orchestration/pingpong_job.py packages/orchestration/do_sequence.py apps/cli/commands/do_cmd.py tests/orchestration/test_mission_contract.py tests/orchestration/test_mission_gate.py tests/orchestration/test_pingpong_job_dod_gate.py tests/cli/test_do_sequence_cli.py`, EXIT 0:
```
All checks passed!
```

G4, `python3 .remedy-wt/f269-r5/g4.py`: one worktree at `b2408828`, running `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_mission_contract.py tests/orchestration/test_mission_gate.py tests/orchestration/test_pingpong_job_dod_gate.py tests/cli/test_do_sequence_cli.py` from the worktree root. `__pycache__` was purged before each run. Each mutation was an exact one-occurrence string replacement, reverted with `git checkout -- <exact path>`, and the worktree status read clean after every revert.
```
mission_contract resolves to: /home/decodeux/Repos/remedy/.remedy-wt/f269-r5-g4/packages/orchestration/mission_contract.py
[control] exit 0   123 passed in 49.15s
[a] exit 1   9 failed, 114 passed in 46.69s
    test_mission_contract.py::TestTheJobDoDCarriesItsSlice::test_a_whole_mission_criterions_check_enters_non_blocking_though_the_criterion_blocks
    test_mission_contract.py::TestTheJobDoDCarriesItsSlice::test_a_job_with_no_milestone_gets_only_non_blocking_checks
    test_mission_gate.py::TestTheContractHoldsTheMission::test_the_job_gate_decides_two_met_and_one_unmet
    test_mission_gate.py::TestTheContractHoldsTheMission::test_a_red_whole_mission_check_releases_the_job_but_holds_the_mission
    test_pingpong_job_dod_gate.py::TestTheGateDecidesTheJobsContractSlice::test_the_slice_criteria_carry_the_gates_statuses_after_the_run
    test_do_sequence_cli.py::test_contract_website_on_a_bare_order_gives_the_website_templates_criteria
    test_do_sequence_cli.py::test_contract_website_with_an_extra_requirement_adds_planner_criteria_and_drops_none
    test_do_sequence_cli.py::test_without_contract_the_website_fixture_order_gets_the_proposed_template
    test_do_sequence_cli.py::test_contract_cli_tool_gates_the_job_on_its_whole_mission_checks_and_names_the_unmet
[b] exit 1   4 failed, 119 passed in 41.73s
    test_pingpong_job_dod_gate.py::TestTheGateRunsInsideRunJob::test_a_blocking_check_that_cannot_pass_blocks_the_job_and_keeps_its_worktree
    test_pingpong_job_dod_gate.py::TestTheGateRunsInsideRunJob::test_a_job_whose_only_red_check_is_non_blocking_completes
    test_pingpong_job_dod_gate.py::TestTheGateDecidesTheJobsContractSlice::test_the_slice_criteria_carry_the_gates_statuses_after_the_run
    test_do_sequence_cli.py::test_contract_cli_tool_gates_the_job_on_its_whole_mission_checks_and_names_the_unmet
[c] exit 1   1 failed, 122 passed in 41.26s
    test_do_sequence_cli.py::test_contract_cli_tool_gates_the_job_on_its_whole_mission_checks_and_names_the_unmet
```
(All failing ids are under `tests/orchestration/` or `tests/cli/`, as the file names show.)

The mutations:
- (a) In `merge_contract_slice_into_dod`, `{**c.check, "blocking": c.blocking and bool(c.milestones)})` became `{**c.check, "blocking": c.blocking})`. The website `do` walks then fail, because their whole-mission blocking checks hold the job.
- (b) In `run_job`, `dod_blocker = _gate_job_definition_of_done(job) if all_done else ""` became `dod_blocker = ""`.
- (c) In `_step_shape`, the line `merge_contract_slice_into_dod(mission, None, job_id)` was deleted.

The full suite was not run (amend0917-throughput).

## Authored-text proofs

- The four payloads (block, decisions, ledger, plan) are committed byte-identical as `.agent/authored/f269-r5-*` (G1 `authored copy ... True`).
- `.agent/plan.md` equals plan.md. `.agent/live_review.md` and `.agent/decisions.md` equal their `09d7641f` bytes plus the payload (G1 `True`).

## Deviations & assumptions

1. Existing tests updated by design, each with its property kept: `test_mission_gate.py::test_the_job_gate_decides_two_met_and_one_unmet` (`gate=blocked` → `gate=released`, D6 (1)); and in `test_do_sequence_cli.py`, the helpers `_template_criteria` / `_contract_by_origin` and one slice comparison, which now ignore `status` and `evidence_ref` (D6 (2), (3) make the gated `do` job write them). The three website tests using them are `test_contract_website_on_a_bare_order_gives_the_website_templates_criteria`, `test_contract_website_with_an_extra_requirement_adds_planner_criteria_and_drops_none` and `test_without_contract_the_website_fixture_order_gets_the_proposed_template`.
2. C3's tests are in a NEW file, `tests/orchestration/test_pingpong_job_dod_gate.py`, named after `pingpong_job.py` like the existing `test_pingpong_job_hunk_ledger.py`. It is in G2.
3. In `run_job`, `record_contract_results` is not wrapped: a contract body that breaks a D2 rule raises out of `run_job` rather than being skipped silently; the `finally` still runs, and because the job never reached `completed` it keeps the worktree. No test exercises this path (D2: "never repaired and never half-loaded"). The mission is found by `mission_for_job(job_id)` under the default data root, which is the root `run_job`'s job store uses.
4. `unmet_blocking_criteria` is `[]` when the walk left no contract, and the text output then prints no `Contract:` line. With a contract, the line counts `met` criteria against all of them, and names each blocking criterion not met as `<id> (<status>)`. With none left, it reads `every blocking criterion is met`.
5. A `do` walk with no template has no whole-mission criterion, so its job stores no DoD and runs exactly as before. Its planner criteria stay `open`, as D6's ALTERNATIVES paragraph records.
6. The orchestrator's `execute_move` still calls `record_contract_results` after `execute_dispatched_job`. That path runs `long_run_executor.run_cycles`, which does not call `pingpong_job.run_job` (the only callers are `do_sequence`, `do_cmd`'s `job run`, `self_use_runner` and `resume_job_plan`), so no job is gated twice. `self_use_runner` and `job run` jobs that carry a stored DoD are now gated inside `run_job` too, which is D6 (2) as written.
7. The import-reachability allowlist was not regenerated: `test_import_reachability.py` passed without it (G2).
8. C4's `docs/guides/do-run-v1.md` edit is inside the change set, because constraint 1 names the file for its `--json` field list.
9. Each commit's insertions are under 500 (largest: C3 at 214). The bundle's commit order was followed with no extra commit.

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| C2 the merge (D6 (1)) + tests | done | one round 2 test updated by design (deviation 1) |
| C3 the gate in `run_job` (D6 (2)) + tests | done | tests in a new file (deviation 2) |
| C4 `do` (D6 (3), (4)) + tests + guide | done | three website tests' helpers updated by design (deviation 1) |
| C5 handoff + push | done | push follows this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Then the review of round 5 (D6: `do`'s gate), with its verdict booked in round 6's first commit.

Operator questions open: 4
