# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 21 continues T003. It books round 20's PASS, registers R-0916 to R-0922 for F273 and
records DECISION F261 D20, then deletes `do continue` with its module and the repair-reconcile
block it was the only caller of, and repairs the group-only advertisements of R-0900 with a
guard that measures them.

## Next Steps

1. The `propose` and `repair` groups, as `.agent/f261_t003_inventory.md` proposes in its round I,
   each re-measured before it is authored.
2. The rest of T003 in the inventory's order, with R-0767 and R-0894.
3. `job budget <id> set` over the run-contract budget fields and the token budget profile, the
   word DECISION amend0905-vocab D4 gives those writes, with R-0906 and R-0909.
4. T004, which owes the visible group order of D4 and the README quickstart of R-0895.

## Risks

- 110 findings are open by distinct id before this round's record and 117 after it; three are
  High, R-0803, R-0804 and R-0807.
- The feature's soft limit of 25 rounds leaves four after this one, and the inventory proposes
  more than four; the session that reaches the limit owes the scope report and executes the
  split-and-close default of operator amendment amend0905-throughput, placing the follow-up
  feature directly after F261 per amend0906.
- Every deletion of a `do` word is measured against its heir on a fixture before it is authored,
  because six of this round's capabilities turned out to have no heir or a partial one.
