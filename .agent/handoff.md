# Handoff — F269 Contract & contract templates · Round 9 (R-0971 repair)

## Session

SESSION 1 of feature F269 · round 9 · rounds so far 9

Context self-assessment: the round fit in one worker context with room to spare; every gate below was run in this session at C2 `5a01e5e2`, none carried over from memory.

## Range

Review of f7775533..HEAD — branch `feature/f269-contract`.

## Summary

Round 9 lands DECISION F269 D10 and repairs R-0971:

- C1 books round 8's verdict and finding R-0971 (ledger), appends DECISION F269 D10, writes the round 9 plan, and saves the payloads (ledger, decisions, plan) and the block.
- C2, in `packages/orchestration/mission_contract.py::start_remainder_follow_up_mission`: each carried blocker is written with origin `amendment` (was: the blocker's own origin); text, blocking and the relabelled check are kept as D9 (3) orders. The follow-up's contract now holds ONE amendment entry: `id` `A001`, `text` the prefilled order, `received_at` the record's `answered_at` (the current time only when the record carries none), `applies_from` 1, `criteria` every carried id, `understood` `carries the criteria mission <id> left unmet: <old ids> as <new ids>` (ids joined by `, `), `acknowledged_in` null. `write_planner_criteria` is untouched: it keeps every non-`planner` criterion, so planning the follow-up keeps the carried ones and appends the planner's own after them.

Landed: R-0971 — a remainder follow-up's carried criteria are origin `amendment` under one entry `A001`, so `plan_mission` keeps every one of them with its id and text (C2 `5a01e5e2`).

## Commits

### 65400392 F269 R9 C1: the finding first — round 8 verdict and R-0971, DECISION F269 D10, the round 9 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f269-r9-block.md` | +69 / -0 | Byte copy of block.md |
| `.agent/authored/f269-r9-decisions.md` | +18 / -0 | Byte copy of decisions.md |
| `.agent/authored/f269-r9-ledger.md` | +4 / -0 | Byte copy of ledger.md |
| `.agent/authored/f269-r9-plan.md` | +24 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +18 / -0 | `f7775533` bytes + decisions.md (D10) |
| `.agent/live_review.md` | +4 / -0 | `f7775533` bytes + ledger.md (Gate F269 R8, R-0971) |
| `.agent/plan.md` | +7 / -9 | := plan.md |

### 5a01e5e2 F269 R9 C2: a follow-up mission carries its remainder as one amendment, so planning it keeps every carried criterion
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/mission_contract.py` | +26 / -6 | `start_remainder_follow_up_mission`: carried origin `amendment`, the one `A001` entry written with the contract; its docstring and the module docstring name D10 |
| `tests/orchestration/test_mission_contract.py` | +57 / -3 | UPDATED `test_yes_creates_the_follow_up_with_the_order_and_the_blockers`: the two carried criteria's origin is now `amendment` (was `planner`, `template`); every other pinned property (ids, text, blocking, whole-mission, `open`, no evidence, the kept and the relabelled check, template null) is kept, and `contract.amendments == ()` becomes the ids `["A001"]`. NEW `test_the_follow_up_holds_one_amendment_carrying_every_criterion`: the whole entry equals `{"id": "A001", "text": <impact>, "received_at": <answered_at>, "applies_from": 1, "criteria": ["C001","C002"], "understood": "carries the criteria mission <id> left unmet: C002, C003 as C001, C002", "acknowledged_in": None}`, and `due_contract_amendments(contract, 1)` returns it. NEW THE R-0971 TEST `test_planning_the_follow_up_keeps_a_carried_planner_criterion`: the source's C002 is asserted `planner`; after `yes`, `plan_mission(PROJECT, <follow-up>, None, root=tmp_path)` (no provider); the first two criteria are `("C001","the docs name every command","amendment")` and `("C002","tests/test_c.py passes","amendment")`, C002 unchanged by the plan; the rest are non-empty, all `planner`, numbered from `C003`; the one amendment is `A001` with criteria `["C001","C002"]` and `understood` naming `C002, C003 as C001, C002`. The module docstring names D10 |

### C3 (this commit) F269 R9 C3: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | This file |

Existing tests whose pinned behaviour D10 changes: only `TestTheRemainderAnswer::test_yes_creates_the_follow_up_with_the_order_and_the_blockers` (above). `tests/orchestration/test_mission_gate.py::TestTheRemainderAtBudgetEnd` and the cockpit door test in `tests/ui_server/test_command_channel.py` pin id, text and status only, and pass unchanged.

## External actions

- G4: `git worktree add --detach .remedy-wt/f269-r9/g4wt 5a01e5e2` (exit 0), then `git worktree remove --force` (exit 0). `git worktree list` afterwards: `/home/decodeux/Repos/remedy  5a01e5e2 [feature/f269-contract]`.
- `git push` runs after this commit. Its outcome and G5 are in the worker's final report.
- No PR was created, edited or merged.

## Verification

All gates ran at C2 `5a01e5e2` with a clean tree. The scripts are `.remedy-wt/f269-r9/gates.py` and `.remedy-wt/f269-r9/g4.py`; each exit code is a subprocess return code.

G1 transport + state, `python3 .remedy-wt/f269-r9/gates.py g1`:
```
ledger.md digest matched: True authored copy equal: True
decisions.md digest matched: True authored copy equal: True
plan.md digest matched: True authored copy equal: True
block.md digest matched: True authored copy equal: True
True
```
(the last line: `.agent/plan.md` == plan.md, and `.agent/live_review.md` and `.agent/decisions.md` == their `f7775533` bytes + their slice; the script's own exit was 0.)

G2, `python3 .remedy-wt/f269-r9/gates.py g2`, runs `python3 -m pytest -q -p no:cacheprovider` over the block's list verbatim. The one test file this round edited, `tests/orchestration/test_mission_contract.py`, is in it:
```
886 passed in 104.65s (0:01:44)
exit 0
```

G3, `python3 .remedy-wt/f269-r9/gates.py g3` = `python3 -m ruff check packages/orchestration/mission_contract.py tests/orchestration/test_mission_contract.py`:
```
All checks passed!
exit 0
```

G4 mutation red-proof, `python3 .remedy-wt/f269-r9/g4.py`: one worktree at C2, `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_mission_contract.py` from the worktree root, `__pycache__` purged before each run. Mutation: in `start_remainder_follow_up_mission`, `id=ident, text=criterion.text, origin="amendment",` becomes `id=ident, text=criterion.text, origin=criterion.origin,`.
```
worktree HEAD: 5a01e5e2
module: /home/decodeux/Repos/remedy/.remedy-wt/f269-r9/g4wt/packages/orchestration/mission_contract.py
CONTROL summary: 121 passed in 0.85s
CONTROL exit 0
MUTANT summary: 3 failed, 118 passed in 0.94s
MUTANT FAILED tests/orchestration/test_mission_contract.py::TestTheRemainderAnswer::test_yes_creates_the_follow_up_with_the_order_and_the_blockers
MUTANT FAILED tests/orchestration/test_mission_contract.py::TestTheRemainderAnswer::test_the_follow_up_holds_one_amendment_carrying_every_criterion
MUTANT FAILED tests/orchestration/test_mission_contract.py::TestTheRemainderAnswer::test_planning_the_follow_up_keeps_a_carried_planner_criterion
MUTANT exit 1
R-0971 test red: True
remove: 0
/home/decodeux/Repos/remedy  5a01e5e2 [feature/f269-contract]
```

Full suite: not run (amend0917-throughput).

## Authored-text proofs

In G1 above, each of the four payloads matches its block digest and is byte-equal to its `.agent/authored/f269-r9-*` copy. `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md` equal their ordered construction.

## Deviations & assumptions

1. No departure from the ordered commit sequence (C1, C2, C3).
2. Assumption: D10's `understood` template leaves the list separator open; the ids are joined by `, ` — the separator the contract renderer already uses for an amendment's criteria.
3. Assumption: `received_at` is the answer record's `answered_at` (which `answer_task_decision` always writes); only a record without one falls back to `now` or the current time, so a hand-built record still yields a valid entry.
4. Reading of G4's red, from the code: with the mutation, the carried criteria keep `planner` and `template`, and the `A001` entry then breaks D8 (1)'s rule "amendment criteria are amendment criteria of the contract", so `write_mission_contract` raises `ContractError` inside `start_remainder_follow_up_mission`; the three tests fail there rather than at the planning step. No second mutation was run.
5. The authored copies include `f269-r9-block.md`, as the block's PAYLOADS list names block.md and round 8's C1 did the same.

| Item | Status | Reason |
|------|--------|--------|
| C1 the finding first | done | |
| C2 the D10 repair + R-0971 test | done | assumptions 2, 3 |
| G1 to G4 at C2 | done | |
| C3 handoff + push | done | |

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Then the review of round 9 (DECISION F269 D10: the follow-up carries its remainder as one amendment; R-0971's repair), with its verdict and R-0971's resolution booked in the next round's first commit.
3. Then the closure sequence: the Built State of `docs/roadmap/features/T2_F269.md` and any docs page the shipped commands need, the integration-gate suite once, evidence, package, STATUS.

Operator questions open: 5
