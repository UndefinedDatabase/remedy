# Plan — F269 Contract & contract templates

Branch: feature/f269-contract, cut from `main` at `0955dd4c` (the merge
commit of pull request 256, F268's closure).

## Goal

A mission carries one contract — its acceptance criteria, compiled to
checks by F061's compiler — and is not done while a blocking criterion is
red; four templates ship as its floor; amendments and a remainder
proposal complete it (`docs/roadmap/features/T2_F269.md`).

## Current Step

Round 1: claim F269 and land T001 — the contract record on the mission
(`packages/orchestration/mission_contract.py`), the milestone a dispatched
job serves, the derived job slice, and `mission contract` and `job
contract`. DECISIONs F269 D2 and D3 bind it.

## Next Steps

1. Review round 1 (T001) and book its verdict in the next round's first
   commit.
2. T002: F061's compiler over the criteria, and the mission gate that
   holds a mission open on a red blocking criterion.
3. T003: the four templates under `docs/contracts/`, the planner's
   proposal, `--contract <name>` on `do`, and DECISION F269 D1.
4. The deletion of `job attach-repo` and `job permit`, once the contract
   writes a job's repository binding and grants (amend0917 D2).
5. T004: amendments; T005: the remainder proposal; then closure.
