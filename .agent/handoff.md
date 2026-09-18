# Handoff — F269 Contract & contract templates · Round 2 (T002)

## Session

SESSION 1 of feature F269 · round 2 · rounds so far 2

Context self-assessment: the round fit in one worker context with room to spare; every gate below was run in this session at C4 `6304f875`, none carried over from memory.

## Range

Review of 17edb194..HEAD — branch `feature/f269-contract`.

## Summary

Round 2 lands T002 under DECISION F269 D4:

- C1 books round 1's verdict (ledger), appends DECISION F269 D4, writes the round 2 plan, saves the payloads and the block, and rewords the stale docstring in `tests/orchestration/test_mission_state.py`.
- C2 compiles criteria through `dod_compiler.compile_dod` and writes one planner criterion per milestone from `plan_mission` (D4 (1), (2)).
- C3 merges a job's slice checks into its stored DoD at dispatch and reads the job's gate result back onto the slice criteria after it ran (D4 (3), (4)).
- C4 adds the blockers function, `evaluate_move`'s refusal, `mission achieve`'s notice line and `unmet_blocking_criteria`, `do --json`'s `contract`, and the acceptance test (D4 (5), (6)).
- C5 is this handoff and the operator question Q4.

## Commits

### 6b5069fb F269 R2 C1: bookkeeping — round 1 verdict, DECISION F269 D4, the round 2 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f269-r2-block.md` | +108 / -0 | Byte copy of block.md |
| `.agent/authored/f269-r2-decisions.md` | +44 / -0 | Byte copy of decisions.md |
| `.agent/authored/f269-r2-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f269-r2-opq.md` | +10 / -0 | Byte copy of opq.md |
| `.agent/authored/f269-r2-plan.md` | +29 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +44 / -0 | `17edb194` bytes + decisions.md (D4) |
| `.agent/live_review.md` | +2 / -0 | `17edb194` bytes + ledger.md (Gate F269 R1 PASS) |
| `.agent/plan.md` | +9 / -10 | := plan.md |
| `tests/orchestration/test_mission_state.py` | +6 / -1 | Docstring of `test_the_contract_round_trips_through_disk` only: no longer "reserved"/"empty", names `packages/orchestration/mission_contract.py` as the shape's owner |

### 50884744 F269 R2 C2: the contract compiled by F061's compiler, and planner criteria written when a mission is planned
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/mission_compiler.py` | +6 / -0 | `plan_mission` calls `write_planner_criteria` after `attach_milestone_dods`, before `set_mission_plan` |
| `packages/orchestration/mission_contract.py` | +86 / -7 | `CONTRACT_CHECK_ID_PREFIX`, `compile_contract_criteria` (one task per criterion, first check whose refs hold `<id>:0`, relabelled `ctr-<id>`, refs [`<id>:0`], the criterion's `blocking`), `write_planner_criteria`; module docstring |
| `tests/orchestration/test_mission_contract.py` | +118 / -1 | `TestTheCompiledContract` (5 tests: ids/refs/blocking, non-blocking stays non-blocking, test path → selector, check validates as `DoDCheck`, empty) and `TestThePlannerCriteria` (3 tests: one planner criterion per milestone of the replayed 4-milestone fixture, no-provider plan → C001/M001, re-plan keeps C004 template criterion and replaces the planner one with C005) |

### 7d550edb F269 R2 C3: each dispatched job's DoD carries its contract slice, and its gate result decides the slice criteria
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/mission_contract.py` | +101 / -1 | `merge_contract_slice_into_dod` (through `dod_gate.load_dod`/`store_dod`) and `record_contract_results` (through `load_dod`/`load_gate_result`) |
| `packages/orchestration/orchestrator_loop.py` | +17 / -9 | `execute_move`'s dispatch branch: the mission is loaded once; merge after `attach_milestone_dod`; results after the job executed; imports moved up |
| `tests/orchestration/test_mission_contract.py` | +113 / -3 | `TestTheJobDoDCarriesItsSlice` (5 tests: no DoD → slice DoD, M1 job gets no M2 check, equal kind+spec not added twice, a second merge adds nothing, no contract stores nothing) and `TestTheJobGateDecidesItsCriteria` (stored gate result → met/unmet/open with `evidence_ref`; no gate result changes nothing) |

### 6304f875 F269 R2 C4: the mission gate — blocking criteria hold the achieve move, mission achieve names them, do --json reports the contract
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/do_cmd.py` | +5 / -3 | `contract` = `do_mission_contract(ctx)`; docstring |
| `apps/cli/commands/mission_cmd.py` | +26 / -2 | `achieve` computes the blockers, prints `  Unmet blocking criteria: …` before `  Status:` when any, and carries `unmet_blocking_criteria` under `--json`; never refused |
| `docs/guides/do-run-v1.md` | +2 / -1 | The `contract` key line no longer says null until F269 (deviation 1) |
| `packages/orchestration/do_sequence.py` | +15 / -0 | `do_mission_contract(ctx)`: the walk's mission contract body from its record, or None |
| `packages/orchestration/mission_contract.py` | +17 / -0 | `contract_blockers` |
| `packages/orchestration/orchestrator_loop.py` | +19 / -1 | `evaluate_move` refuses `declare_mission_achieved` after the plan and milestone refusals: an unreadable body with its rule, else the unmet blocking ids |
| `tests/cli/test_do_sequence_cli.py` | +15 / -2 | Pinned behaviour D4 changes by design: `test_run_to_stop_leaves_the_target_untouched_and_stops_before_apply` and `test_plan_only_writes_the_mission_plan_plans_the_jobs_and_runs_none` asserted `data["contract"] is None`; they now assert it equals the mission record's contract (planner criteria, `contract_v1`) — the property kept is "the JSON reports the mission's contract" |
| `tests/cli/test_golden_path.py` | +6 / -1 | Pinned behaviour D4 changes by design: `TestDoMission::test_do_mission_json` asserted `data["contract"] is None`; it now asserts the one planner criterion C001 for M001 of the deterministic plan |
| `tests/orchestration/test_mission_gate.py` | +208 / -0 | NEW. THE ACCEPTANCE TEST: planned mission, three-criterion contract (C001 planner → `tests/test_a.py`, C002/C003 template → `test_b.py`/`test_c.py`) in a tmp work dir where `test_c.py` passes only once `ready.txt` exists; dispatched through `execute_move` with an `execute` seam running the real `dod_gate.run_job_gate`; two met + one unmet; `evaluate_move` refuses naming C003; `ready.txt` + re-run → refusal gone. Plus `mission achieve` text/JSON (exit 0, unmet ids, status achieved) and the met case |
| `tests/orchestration/test_orchestrator_loop.py` | +47 / -0 | `TestTheContractHoldsTheAchievedClaim`: unmet and open blocking refuse by id, non-blocking unmet does not hold, a broken body refuses with the rule |

### C5 (this commit) F269 R2 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/operator_questions.md` | +10 / -0 | `17edb194` bytes + opq.md (Q4) |
| `.agent/handoff.md` | rewrite | This file |

## External actions

- `git worktree add --detach .remedy-wt/f269-r2-g4 HEAD` (HEAD = `6304f875`) for G4; removed with `git worktree remove --force` (exit 0); `git worktree list` afterwards showed only the primary checkout.
- `git push` runs after this commit; its outcome and G5 are in the worker's final report.
- No PR created, edited or merged.

## Verification

All gates ran at C4 `6304f875`, before this commit, through `python3 .remedy-wt/f269-r2/gates.py` and `.remedy-wt/f269-r2/g4.py` (exit codes are the subprocess return codes).

G1 transport + state, `python3 .remedy-wt/f269-r2/g1.py`, exit 0:
```
ledger.md digest True authored copy True
decisions.md digest True authored copy True
plan.md digest True authored copy True
opq.md digest True authored copy True
block.md digest True authored copy True
plan.md True
live_review.md True
decisions.md True
```

G2, the block's 20 paths plus `tests/orchestration/test_mission_gate.py` (the one test file this round created; every other file it edited is already in the list), `python3 -m pytest -q -p no:cacheprovider …`: `1336 passed in 127.09s (0:02:07)`, exit 0. Base reading of the block's 20 paths at `17edb194` in this session: `1311 passed in 121.97s`.

G3, `python3 -m ruff check` over the 12 .py files C1 to C4 touched (`apps/cli/commands/do_cmd.py`, `apps/cli/commands/mission_cmd.py`, `packages/orchestration/do_sequence.py`, `packages/orchestration/mission_compiler.py`, `packages/orchestration/mission_contract.py`, `packages/orchestration/orchestrator_loop.py`, `tests/cli/test_do_sequence_cli.py`, `tests/cli/test_golden_path.py`, `tests/orchestration/test_mission_contract.py`, `tests/orchestration/test_mission_gate.py`, `tests/orchestration/test_mission_state.py`, `tests/orchestration/test_orchestrator_loop.py`): `All checks passed!`, exit 0.

G4, one worktree at `6304f875`, `python3 -B -m pytest -q -p no:cacheprovider -rf` from the worktree root over `tests/orchestration/test_mission_contract.py`, `tests/orchestration/test_mission_gate.py`, `tests/orchestration/test_orchestrator_loop.py`; `__pycache__` purged before each run; each mutation reverted by writing the original bytes back to the exact path, worktree status empty after every revert:
```
[control] mission_contract resolves to: /home/decodeux/Repos/remedy/.remedy-wt/f269-r2-g4/packages/orchestration/mission_contract.py
[control] 274 passed — exit 0
[a: the compiler sets every check blocking] 2 failed, 272 passed — exit 1
  test_mission_contract.py::TestTheCompiledContract::test_every_criterion_gets_its_own_check_with_its_own_blocking
  test_mission_contract.py::TestTheCompiledContract::test_a_non_blocking_criterion_stays_non_blocking
[b: the merge adds a check even when an equal kind and spec is present] 2 failed, 272 passed — exit 1
  test_mission_contract.py::TestTheJobDoDCarriesItsSlice::test_a_check_equal_in_kind_and_spec_is_not_added_a_second_time
  test_mission_contract.py::TestTheJobDoDCarriesItsSlice::test_merging_twice_adds_nothing_the_second_time
[c: the results function sets met whatever the evidence says] 6 failed, 268 passed — exit 1
  test_mission_contract.py::TestTheJobGateDecidesItsCriteria::test_statuses_and_evidence_follow_the_stored_gate_result
  test_mission_gate.py::TestTheContractHoldsTheMission::test_the_job_gate_decides_two_met_and_one_unmet
  test_mission_gate.py::TestTheContractHoldsTheMission::test_the_achieve_move_is_refused_naming_the_unmet_criterion
  test_mission_gate.py::TestTheContractHoldsTheMission::test_once_the_check_can_pass_a_re_run_lifts_the_refusal
  test_mission_gate.py::TestTheOperatorsAchieveIsNotHeld::test_text_names_the_unmet_criteria_before_the_status_line
  test_mission_gate.py::TestTheOperatorsAchieveIsNotHeld::test_json_carries_the_unmet_criteria
[d: evaluate_move's contract refusal removed] 3 failed, 271 passed — exit 1
  test_mission_gate.py::TestTheContractHoldsTheMission::test_the_achieve_move_is_refused_naming_the_unmet_criterion
  test_mission_gate.py::TestTheContractHoldsTheMission::test_once_the_check_can_pass_a_re_run_lifts_the_refusal
  test_orchestrator_loop.py::TestTheContractHoldsTheAchievedClaim::test_unmet_and_open_blocking_criteria_refuse_by_id
```
(The ids are under `tests/orchestration/`; the mission_contract path printed identically before every run.) Mutations: (a) `blocking=criterion.blocking` → `blocking=True` in `compile_contract_criteria`; (b) the dedupe `continue` → `pass` in `merge_contract_slice_into_dod`; (c) `status="met" if match.id in passed else "unmet"` → `status="met"` in `record_contract_results`; (d) the four-line `if blockers: return …` deleted from `evaluate_move`.

The import-reachability test passed without a regeneration, so the allowlist is untouched. The full suite was not run (amend0917-throughput).

## Authored-text proofs

- All five payloads (block, decisions, ledger, opq, plan) are committed byte-identical as `.agent/authored/f269-r2-*`; G1 printed `authored copy True` for each.
- `.agent/plan.md` equals plan.md; `.agent/live_review.md` and `.agent/decisions.md` equal their `17edb194` bytes + the payload (G1 True).
- `.agent/operator_questions.md` equals its `17edb194` bytes + opq.md (`.remedy-wt/f269-r2/c5.py` printed `equal True`).

## Deviations & assumptions

1. `docs/guides/do-run-v1.md` is outside the block's change set. Its line "`contract` is `null` until F269 lands" became false with D4 (6), and AGENTS.md (Documentation Updates, which wins over other files) requires the doc to follow a changed behaviour, so C4 rewrites that one line.
2. D4 (2) "all compiled by (1)": the new planner criteria, and any KEPT criterion whose `check` is still null, are compiled with no provider; a kept criterion that already has a check keeps it (a recompile could replace a provider-compiled check with a deterministic one). Kept criteria stay in their order, the new planner criteria follow.
3. D4 (3) details the block leaves open: a job whose `dod.json` exists but will not parse is left alone (the gate already holds it; overwriting would hide that); a DoD created from slice checks alone is labelled `compiled=False`, `origin="deterministic"`; two slice criteria with the same kind and spec share one DoD check; a slice check whose id is already taken by a different check gets a `-2` suffix (the results function matches by kind and spec, never by id).
4. D4 (4): a criterion whose DoD check has no evidence entry in the gate result reads `unmet`; a gate result with no readable DoD changes nothing.
5. D4 (5) for `mission achieve`: the notice line is printed only when unmet blocking criteria exist; `unmet_blocking_criteria` is present only for `achieve` (`[]` when none); a contract body that breaks a D2 rule prints `Warning: the mission's contract is unreadable: …` on stderr, the status is still set, and the JSON key is `null`.
6. `plan_mission` writes the contract before `set_mission_plan`, so the record it returns carries both. A mission whose stored contract breaks a D2 rule now makes `plan_mission` raise `ContractError` (a `ValueError`); `do` always plans a fresh mission, so its walk never meets one.
7. `do --json`'s `contract` is read from the mission record when the walk ends (`do_mission_contract`), not cached from the plan step.
8. C2, C3 and C4 are single commits (210, 231 and 360 insertions), each under 500, so no code/test split was needed.

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| C2 compile + planner criteria | done | kept null checks compiled too (deviation 2) |
| C3 job DoD + results | done | |
| C4 gate + surfaces + acceptance test | deviated | one doc line outside the change set (deviation 1) |
| C5 handoff + push | done | push follows this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Then the review of round 2 (T002), with its verdict booked in round 3's first commit.

Operator questions open: 4
