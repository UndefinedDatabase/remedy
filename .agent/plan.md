# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 20 continues T003. It books round 19's PASS, registers R-0913, R-0914 and R-0915 for F273
and records DECISION F261 D19, then deletes `do repair-attest`, `do job-resume` and `do replan`,
one table per commit.

## Next Steps

1. The `do continue` hints, then the command and `do_continue.py`, with R-0900, as
   `.agent/f261_t003_inventory.md` proposes.
2. The rest of T003 in the inventory's order, each round re-measured before it is authored,
   with R-0767 and R-0894.
3. `job budget <id> set` over the run-contract budget fields and the token budget profile, the
   word DECISION amend0905-vocab D4 gives those writes, with R-0906 and R-0909.
4. T004, which owes the visible group order of D4 and the README quickstart of R-0895.

## Risks

- 107 findings are open by distinct id before this round's record and 110 after it; three are
  High, R-0803, R-0804 and R-0807.
- The feature's soft limit of 25 rounds leaves five after this one, and the inventory proposes
  more than five; the session that reaches the limit owes the scope report and executes the
  split-and-close default of operator amendment amend0905-throughput.
- Every deletion of a `do` word is measured against its heir on a fixture before it is authored,
  because three of this round's capabilities turned out to have no heir at all.
