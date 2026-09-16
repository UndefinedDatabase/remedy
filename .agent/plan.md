# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 17 continues T003. It books round 16's PASS, registers R-0906 for this feature and R-0907
for F273 and records DECISION F261 D16, then deletes the `readiness` group, the `contract` group
with its hints, and the `policy` group, one table per commit.

## Next Steps

1. The `context` group, the `token` group with `context-pack`, and the `review` group, as
   `.agent/f261_t003_inventory.md` proposes.
2. The rest of T003 in the inventory's order, each round re-measured before it is authored,
   with R-0767, R-0894 and R-0900.
3. `job budget <id> set` over the run-contract budget fields, the word DECISION amend0905-vocab
   D4 gives the write that `contract set` performed, with R-0906.
4. T004.

## Risks

- 100 findings are open by distinct id before this round's record and 102 after it; three are
  High, R-0803, R-0804 and R-0807.
- The inventory proposes more rounds than F261's soft limit of 25 leaves; the session that
  reaches the limit owes the scope report and the split-and-close default.
- A deletion's consumers include shell strings, subprocess help calls, event readers, the UI
  event catalog and the readiness signals, so every deletion round runs the whole suite on its
  committed tree.
