# Handoff — F269 Contract & contract templates · Round 7 (T004 amendments)

## Session

SESSION 1 of feature F269 · round 7 · rounds so far 7

Context self-assessment: the round fit in one worker context with room to spare; every gate below was run in this session at C3 `e383c7fb`, none carried over from memory.

## Range

Review of c4bd55c1..HEAD — branch `feature/f269-contract`.

## Summary

Round 7 lands DECISION F269 D8 (T004):

- C1 books round 6's verdict (ledger), appends DECISION F269 D8, writes the round 7 plan, and saves the payloads (ledger, decisions, plan) and the block.
- C2, D8 (1), (2) and (5). `MissionContract.__post_init__` now checks every amendment entry through NEW `_check_amendment`, so a read and a write refuse the same entry. The rules are: exactly the seven fields, all required; `id` is `A` plus three digits and unique; `text` is non-empty; `received_at` parses with `datetime.fromisoformat`; `applies_from` is an int of at least 1, never a bool; `criteria` is a list of distinct ids, each a criterion of the contract whose origin is `amendment`; `understood` is non-empty; `acknowledged_in` is null, or a round not before `applies_from`. NEW `amend_mission_contract(project_id, mission_id, text, *, milestones=(), blocking=True, root=None, now=None)`: it creates the contract when there is none and adds one `amendment` criterion, compiled by `compile_contract_criteria` with the next free `C` id. It appends the entry with the next free `A` id, `applies_from = orchestrator_loop.next_iteration_index(...)`, `understood = "adds <blocking|advisory> criterion <id>: <text>"` and `acknowledged_in = null`. It edits no existing criterion or entry. No command calls it. `render_contract_lines` takes an optional `amendments` argument and lists them after the criteria, as `Amendments: <n>` and then, for each, `<id>  applies from round <n>  <acknowledged in round <m> | not yet acknowledged>  adds <ids>` with its text beneath. A contract with no amendments prints no section, so the existing renders are unchanged. `mission contract` passes `contract.amendments`.
- C3, D8 (3) and (4). NEW `mission_contract.due_contract_amendments(contract, round)` and `record_amendments_acknowledged(project_id, mission_id, ids, round, root)`, plus NEW `orchestrator_loop.acknowledge_due_amendments`, `MOVE_ACKNOWLEDGE_AMENDMENT = "acknowledge_amendment"` and `OUTCOME_ACKNOWLEDGED = "acknowledged"`. In `run_mission`, at the top of each iteration's boundary `try`, after the safe point and the active check and before the dossier refresh, context and move, each due amendment gets one ledger entry. That entry has the same iteration number, an empty context digest, move `{"kind": "acknowledge_amendment", "payload": {"amendment_id": <id>}}`, outcome `acknowledged` with detail `<understood>; applies from round <n>`, and cost `{"calls": 0, "usage": null, "usage_source": "unmeasured"}`. Then `acknowledged_in` is set to that round and the mission is reloaded. D8 (3) needed no code: a job's DoD already takes its slice at dispatch (`merge_contract_slice_into_dod`), so the acceptance test proves it. For the ledger readers, `mission_dossier.mission_iteration_facts` gives an acknowledgement the DECISIONS id `I<round>-<amendment id>`. Without that id it would share `I<round>` with the move written after it, and `_merge_by_id` would replace it.

## Commits

### 4a667fa4 F269 R7 C1: bookkeeping — round 6 verdict, DECISION F269 D8, the round 7 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f269-r7-block.md` | +89 / -0 | Byte copy of block.md |
| `.agent/authored/f269-r7-decisions.md` | +39 / -0 | Byte copy of decisions.md |
| `.agent/authored/f269-r7-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f269-r7-plan.md` | +24 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +39 / -0 | `c4bd55c1` bytes + decisions.md (D8) |
| `.agent/live_review.md` | +2 / -0 | `c4bd55c1` bytes + ledger.md (Gate F269 R6 PASS) |
| `.agent/plan.md` | +7 / -8 | := plan.md |

### b48a1623 F269 R7 C2: an amendment's shape is checked on read and write, amend_mission_contract adds its compiled criterion applying from the next round, and mission contract lists amendments
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/mission_contract.py` | +131 / -5 | NEW `_AMENDMENT_ID_RE`, `_AMENDMENT_FIELDS`, `_is_round` and `_check_amendment`, called from `MissionContract.__post_init__` along with the unique-id rule. NEW `amend_mission_contract`. `render_contract_lines` gains `amendments`. The module and class docstrings name D8 |
| `apps/cli/commands/contract_cmd.py` | +2 / -1 | `mission contract` passes `contract.amendments` to the renderer (deviation 1) |
| `tests/orchestration/test_mission_contract.py` | +221 / -0 | NEW `BROKEN_AMENDMENTS` (14 rows over 10 distinct rule names), each refused on write and on a raw read (parametrized), plus a valid round trip. NEW `TestAmendingAContract`: (1) a mission with no contract gets one; (2) the criterion is `amendment`, compiled (`ctr-C004`, selector `tests/test_login.py`), with the next free id, and `understood` reads right; (3) an advisory milestone amendment says `advisory`; (4) `applies_from == 3` over a ledger holding rounds 1 and 2; (5) a second amendment gets `A002` and `C005`, and the first criterion and entry are byte-identical in the stored record; (6) a re-plan (`plan_mission`, so `write_planner_criteria`) keeps the amendment criterion and entry. NEW `TestTheRendererListsAmendments` has two tests. The docstring names D8 |
| `tests/cli/test_contract_cmd.py` | +42 / -0 | NEW `TestTheMissionViewListsAmendments`: `mission contract` text lists `A001  applies from round 2  acknowledged in round 2  adds C004` after the criteria, and `--json` carries the stored body with the amendment |

### e383c7fb F269 R7 C3: each loop round acknowledges the amendments due in it before its move, and the dossier keeps an acknowledgement beside its round's move
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/mission_contract.py` | +37 / -1 | NEW `due_contract_amendments` and `record_amendments_acknowledged`. The docstring names them |
| `packages/orchestration/orchestrator_loop.py` | +57 / -1 | NEW `MOVE_ACKNOWLEDGE_AMENDMENT`, `OUTCOME_ACKNOWLEDGED` and `acknowledge_due_amendments`, which writes the ledger entry through `record` and then marks the contract. It is called at the start of each iteration in `run_mission`. The docstring is updated |
| `packages/orchestration/mission_dossier.py` | +19 / -2 | NEW `_ledger_decision_id`: an acknowledgement's DECISIONS id is `I<round>-<amendment id>` |
| `tests/orchestration/test_orchestrator_loop.py` | +136 / -0 | NEW `TestAnAmendmentTakesEffectInTheNextRound`, the acceptance test. The mission has an M001 and M002 plan and a compiled `tests/test_app.py` contract. It uses fake dispatch, execute and evidence seams and a scripted provider. Run 1 is round 1, which dispatches M001. Then `amend_mission_contract(... "tests/test_login.py passes")` runs. Run 2 is round 2, which dispatches M002, and round 3, which waits. The tests: `applies_from == 2`; the ledger reads `(1 dispatch_job) (2 acknowledge_amendment) (2 dispatch_job) (3 wait_on_decisions)`, with the ack payload `A001`, status `acknowledged`, detail `adds blocking criterion C002: tests/test_login.py passes; applies from round 2`, and `acknowledged_in == 2`; round 1's job DoD selectors are `[tests/test_app.py]` and round 2's are `[tests/test_app.py, tests/test_login.py]`; round 3 writes no second ack. Reader tests: the ack costs no call, and `prompt_trace.jsonl` holds 3 rows for the 3 provider calls; the watchdog treats it as no dispatch, no measured tokens and no trip, and an ack between dispatches does not reset no-progress; `render_ledger` shows the ack and what was understood; `next_iteration_index == 4` |
| `tests/orchestration/test_mission_dossier.py` | +18 / -0 | An ack and its round's move keep two DECISIONS lines, `I002-A001` and `I002`, through `append_facts` |

### C4 (this commit) F269 R7 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | This file |

## Ledger readers (C3's reading, reader by reader)

- `apps/cli/commands/mission_cmd.py`: it renders `result.entries` through `render_ledger`, which prints the ack as `[2] acknowledge_amendment -> acknowledged` with `amendment_id` and the detail (tested). `ledger_entries` is a plain count. `latest_trips_from_ledger` reads only `watchdog_tripped` entries (tested: `[]`). No change was needed.
- `packages/orchestration/mission_dossier.py`: it was broken by the shared iteration id, and is changed and tested as above.
- `packages/orchestration/watchdog.py`: the ack is no dispatch, so it is no progress and no goal drift. Its `usage` is null, so it is no burn. It is not a trip. No change was needed (tested).
- `packages/orchestration/token_ledger.py`: it does not read `ledger.jsonl`; it mirrors provider calls into SQLite. The ack makes no call and writes no prompt-trace row (tested through the trace row count). No change was needed.
- `packages/orchestration/self_use_generator.py`: it reads the finding ledger (`.agent/live_review.md`), not a mission's `ledger.jsonl`. No change was needed and nothing is testable for it.
- Also read: `orchestrator_loop.dispatched_job_for` reads only `dispatch_job` entries, and `next_iteration_index` takes the highest number, so an ack beside its round's move does not advance the round (tested: 4 after rounds 1 to 3).

## External actions

- For G4: `git worktree add --detach .remedy-wt/f269-r7-g4 e383c7fb`, then `git worktree remove .remedy-wt/f269-r7-g4`. `git worktree list` afterwards: `/home/decodeux/Repos/remedy  e383c7fb [feature/f269-contract]`.
- `git push` runs after this commit. Its outcome and G5 are in the worker's final report.
- No PR was created, edited or merged.

## Verification

All gates ran at C3 `e383c7fb` with a clean tree. The scripts are under `.remedy-wt/f269-r7/`, and each exit code is a subprocess return code.

G1 transport + state, `python3 .remedy-wt/f269-r7/gates.py G1`, exit code 0:
```
ledger.md digest matches and authored copy equal: True
decisions.md digest matches and authored copy equal: True
plan.md digest matches and authored copy equal: True
block.md digest matches and authored copy equal: True
.agent/plan.md == plan.md: True
.agent/live_review.md == c4bd55c1 bytes + ledger.md: True
.agent/decisions.md == c4bd55c1 bytes + decisions.md: True
True
```

G2, `python3 .remedy-wt/f269-r7/gates.py G2`, runs `python3 -m pytest -q -p no:cacheprovider` over the block's list verbatim. The four test files this round edited are all in it (`test_mission_contract.py`, `test_contract_cmd.py`, `test_orchestrator_loop.py`, `test_mission_dossier.py`), and it creates no new test file. Exit code 0:
```
1302 passed in 107.59s (0:01:47)
```

G3, `python3 -m ruff check` over the 8 `.py` files C2 and C3 touched (`packages/orchestration/{mission_contract,orchestrator_loop,mission_dossier}.py apps/cli/commands/contract_cmd.py tests/cli/test_contract_cmd.py tests/orchestration/{test_mission_contract,test_orchestrator_loop,test_mission_dossier}.py`). Exit code 0:
```
All checks passed!
```

G4 mutation red-proofs, `python3 .remedy-wt/f269-r7/g4.py e383c7fb`. It runs in one worktree at C3 and uses `python3 -B -m pytest -q -p no:cacheprovider` from the worktree root, over `tests/orchestration/test_mission_contract.py tests/cli/test_contract_cmd.py tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_mission_dossier.py`. `__pycache__` is purged before each run. Each mutation is reverted by writing back the original bytes, and `git status --porcelain` reads `''` after each revert.
```
/home/decodeux/Repos/remedy/.remedy-wt/f269-r7-g4/packages/orchestration/mission_contract.py
/home/decodeux/Repos/remedy/.remedy-wt/f269-r7-g4/packages/orchestration/orchestrator_loop.py
== control (unmutated)
436 passed in 8.12s
exit 0
== a: applies_from = the current round, not the next
FAILED tests/orchestration/test_mission_contract.py::TestAmendingAContract::test_it_applies_from_the_missions_next_round
FAILED tests/orchestration/test_orchestrator_loop.py::TestAnAmendmentTakesEffectInTheNextRound::test_the_amendment_applies_from_round_two
FAILED tests/orchestration/test_orchestrator_loop.py::TestAnAmendmentTakesEffectInTheNextRound::test_round_two_acknowledges_it_before_its_move
FAILED tests/orchestration/test_orchestrator_loop.py::TestAnAmendmentTakesEffectInTheNextRound::test_the_rendered_ledger_shows_what_was_understood
4 failed, 432 passed in 8.19s
exit 1
== b: the loop's acknowledgement is not written
FAILED tests/orchestration/test_orchestrator_loop.py::TestAnAmendmentTakesEffectInTheNextRound::test_round_two_acknowledges_it_before_its_move
FAILED tests/orchestration/test_orchestrator_loop.py::TestAnAmendmentTakesEffectInTheNextRound::test_a_third_round_writes_no_second_acknowledgement
FAILED tests/orchestration/test_orchestrator_loop.py::TestAnAmendmentTakesEffectInTheNextRound::test_the_acknowledgement_costs_no_call
FAILED tests/orchestration/test_orchestrator_loop.py::TestAnAmendmentTakesEffectInTheNextRound::test_the_watchdog_reads_it_as_no_progress_and_no_burn
FAILED tests/orchestration/test_orchestrator_loop.py::TestAnAmendmentTakesEffectInTheNextRound::test_the_rendered_ledger_shows_what_was_understood
5 failed, 431 passed in 8.17s
exit 1
== c: an acknowledged amendment is acknowledged again
FAILED tests/orchestration/test_orchestrator_loop.py::TestAnAmendmentTakesEffectInTheNextRound::test_round_two_acknowledges_it_before_its_move
FAILED tests/orchestration/test_orchestrator_loop.py::TestAnAmendmentTakesEffectInTheNextRound::test_a_third_round_writes_no_second_acknowledgement
FAILED tests/orchestration/test_orchestrator_loop.py::TestAnAmendmentTakesEffectInTheNextRound::test_the_acknowledgement_costs_no_call
FAILED tests/orchestration/test_orchestrator_loop.py::TestAnAmendmentTakesEffectInTheNextRound::test_the_watchdog_reads_it_as_no_progress_and_no_burn
4 failed, 432 passed in 8.18s
exit 1
```
The mutation texts were:
- (a): `"applies_from": max(next_iteration_index(project_id, mission_id, root) - 1, 1)`. The `max(..., 1)` keeps an empty ledger's entry valid, so the mutation reaches the round assertion rather than a shape refusal.
- (b): the record loop iterates over `()`, so no entry is written, while `acknowledged_in` is still set.
- (c): `due_contract_amendments` drops `and a["acknowledged_in"] is None`.

Full suite: not run (amend0917-throughput).

## Authored-text proofs

In G1 above, each of the four payloads matches its block digest and is byte-equal to its `.agent/authored/f269-r7-*` copy. `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md` equal their ordered construction.

## Deviations & assumptions

1. `apps/cli/commands/contract_cmd.py` is outside the Bundle's named paths. C2 adds one argument there (`contract.amendments`) to the `mission contract` renderer call. Without it, `mission contract` text cannot show the amendment, which C2's ordered test and D8 (5) require. `job contract` is unchanged. D8 does not say which amendments a job's slice view lists, so it lists none, and its `--json` shape is unchanged.
2. The acknowledgement is written inside the iteration's boundary `try`, at its top. A contract body that breaks a rule is therefore classified as that iteration's failure rather than escaping the loop. Before this round the same body already raised at dispatch (`merge_contract_slice_into_dod`).
3. The ledger entry is written before `acknowledged_in` is set. If the process dies between the two, the next round writes a second acknowledgement rather than losing the only one. This is the order D8 (4) lists them in.
4. No docs page describes a contract amendment or the loop's ledger kinds. `docs/system/autonomy-watchdog-v1.md` names only `watchdog_tripped`. The change set excludes `docs/`, so none was edited.

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| C2 shape + amend + renderer | done | deviation 1 |
| C3 the loop + readers | done | |
| C4 handoff + push | done | |

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Then the review of round 7 (D8: the amendment's shape, `amend_mission_contract`, the loop's acknowledgement and the renderers), with its verdict booked in round 8's first commit.

Operator questions open: 5
