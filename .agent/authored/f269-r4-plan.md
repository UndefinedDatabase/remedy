# Plan — F269 Contract & contract templates

Branch: feature/f269-contract, cut from `main` at `0955dd4c` (the merge
commit of pull request 256, F268's closure).

## Goal

A mission carries one contract — its acceptance criteria, compiled to
checks by F061's compiler — and is not done while a blocking criterion is
red; four templates ship as its floor; amendments and a remainder
proposal complete it (`docs/roadmap/features/T2_F269.md`).

## Current Step

Round 4: T003's hygiene half — `packages/orchestration/contract_hygiene.py`
measuring the three hygiene criteria, the criteria in every template, and
the reviewer's rule enforced in the ping-pong round and proved with the
fake provider. DECISION F269 D5 binds it. Rounds 1 to 3 passed.

## Next Steps

1. Review round 4 and book its verdict in the next round's first commit.
2. The gate on `do`'s own job: its contract slice in its DoD, the gate run
   before its worktree is removed, and the results read back.
3. The deletion of `job attach-repo` and `job permit`, once the contract
   writes a job's repository binding and grants (amend0917 D2).
4. T004: amendments; T005: the remainder proposal; then closure.
