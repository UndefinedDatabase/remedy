# Plan — F269 Contract & contract templates

Branch: feature/f269-contract, cut from `main` at `0955dd4c` (the merge
commit of pull request 256, F268's closure).

## Goal

A mission carries one contract — its acceptance criteria, compiled to
checks by F061's compiler — and is not done while a blocking criterion is
red; four templates ship as its floor; amendments and a remainder
proposal complete it (`docs/roadmap/features/T2_F269.md`).

## Current Step

Round 5: whole-mission checks enter a job's DoD as reported checks, the
job gate runs inside `run_job` before the worktree goes, `do`'s jobs carry
their contract slice, and `do`'s result names the unmet blocking
criteria. DECISION F269 D6 binds it. Rounds 1 to 4 passed.

## Next Steps

1. Review round 5 and book its verdict in the next round's first commit.
2. The deletion of `job attach-repo` and `job permit`, once the contract
   writes a job's repository binding and grants (amend0917 D2).
3. T004: amendments, their round of effect, recompile and acknowledgement.
4. T005: the remainder proposal at budget end; then closure.
