# Plan — F269 Contract & contract templates

Branch: feature/f269-contract, cut from `main` at `0955dd4c` (the merge
commit of pull request 256, F268's closure).

## Goal

A mission carries one contract — its acceptance criteria, compiled to
checks by F061's compiler — and is not done while a blocking criterion is
red; four templates ship as its floor; amendments and a remainder
proposal complete it (`docs/roadmap/features/T2_F269.md`).

## Current Step

Round 2: T002 — the contract compiled by F061's compiler, planner
criteria written at mission planning, each dispatched job's DoD carrying
its slice, criterion statuses read from the job gate, and the loop's
achieve move held while a blocking criterion is not met. DECISION F269 D4
binds it. Round 1 (T001) passed.

## Next Steps

1. Review round 2 (T002) and book its verdict in the next round's first
   commit.
2. T003: the four templates under `docs/contracts/`, the planner's
   proposal, `--contract <name>` on `do`, and DECISION F269 D1.
3. The deletion of `job attach-repo` and `job permit`, once the contract
   writes a job's repository binding and grants (amend0917 D2).
4. T004: amendments; T005: the remainder proposal; then closure.
