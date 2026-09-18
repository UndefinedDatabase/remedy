# Plan — F269 Contract & contract templates

Branch: feature/f269-contract, cut from `main` at `0955dd4c` (the merge
commit of pull request 256, F268's closure).

## Goal

A mission carries one contract — its acceptance criteria, compiled to
checks by F061's compiler — and is not done while a blocking criterion is
red; four templates ship as its floor; amendments and a remainder
proposal complete it (`docs/roadmap/features/T2_F269.md`).

## Current Step

Round 3: T003's templates — the four pages under `docs/contracts/`, their
loader and compiler, the deterministic proposal from the order, and
`remedy do --contract <name>`. DECISION F269 D1 binds it. Rounds 1 and 2
(T001, T002) passed.

## Next Steps

1. Review round 3 and book its verdict in the next round's first commit.
2. T003's hygiene half: a check that measures the three hygiene criteria,
   the criteria in every template, the reviewer's matching rule proved
   with the fake provider, and the gate on `do`'s own job.
3. The deletion of `job attach-repo` and `job permit`, once the contract
   writes a job's repository binding and grants (amend0917 D2).
4. T004: amendments; T005: the remainder proposal; then closure.
