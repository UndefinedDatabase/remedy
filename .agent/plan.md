# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 16 continues T003. It books round 15's PASS and its prose slip, registers R-0905 for
F273 and records DECISION F261 D15, then deletes the `guide` group with the group-count guard,
the `dashboard` group, and the `repo` group with its `dev status` block, one table per commit.

## Next Steps

1. The `readiness` group, the `contract` group and its hints, and the `policy` group, as
   `.agent/f261_t003_inventory.md` proposes.
2. The rest of T003 in the inventory's order, each round re-measured before it is authored,
   with R-0767, R-0894 and R-0900.
3. T004.

## Risks

- 99 findings are open by distinct id before this round's record and 100 after it; three are
  High, R-0803, R-0804 and R-0807.
- The inventory proposes more rounds than F261's soft limit of 25 leaves; the session that
  reaches the limit owes the scope report and the split-and-close default.
- A deletion's consumers include shell strings, subprocess help calls, event readers and the
  UI event catalog, so every deletion round runs the whole suite on its committed tree.
