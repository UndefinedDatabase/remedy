# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md` — as far as this feature reaches it; DECISION F261 D25
moves the rest to F280.

## Current Step

ROUND 25, the feature's soft limit. It books round 24's PASS and records DECISIONs F261 D24
and D25 with operator question Q3, then lands the `settings` alias over `config` by one table
and registers F280 by a second, and hands back the scope report D25 executes.

## Next Steps

1. The closure sequence of F261 under `docs/roadmap/STATUS_closure_protocol.md`: the
   integration gate, the ledger rotation, the one consolidation pass of the §3 checklist, the
   evidence package, the STATUS flip and the pull request.
2. F280, which Rule A5 proposes once F261 is merged.

## Risks

- 125 findings are open by distinct id; three are High, R-0803, R-0804 and R-0807. Seven that
  F261 owned move to F280 by DECISION F261 D25.
- F261 closes with the Goal & Done sentence not met, and says so in its Built State; the
  operator may reverse the split through operator question Q3.
- `propose` and `job fulfill` stay in the catalog because deleting either breaks a surviving
  command; F280 owes the rulings.
