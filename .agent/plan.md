# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 18 continues T003. It books round 17's PASS and a prose slip, registers R-0908 and R-0910
for F273 and R-0909 for this feature and records DECISION F261 D17, then deletes the `context`
group, the `token` group with `context-pack`, and the `review` group, one table per commit, and
takes the groups rounds 16 and 17 deleted out of the smoke script's group-help loop.

## Next Steps

1. `do report` becomes `run show` and `run list`, and `do evidence` goes, as
   `.agent/f261_t003_inventory.md` proposes.
2. The rest of T003 in the inventory's order, each round re-measured before it is authored,
   with R-0767, R-0894 and R-0900.
3. `job budget <id> set` over the run-contract budget fields and the token budget profile, the
   word DECISION amend0905-vocab D4 gives those writes, with R-0906 and R-0909.
4. T004.

## Risks

- 102 findings are open by distinct id before this round's record and 105 after it; three are
  High, R-0803, R-0804 and R-0807.
- The inventory proposes more rounds than F261's soft limit of 25 leaves; the session that
  reaches the limit owes the scope report and the split-and-close default.
- A deletion's consumers include shell strings a guard cannot read, subprocess help calls,
  event readers and the UI event catalog, so every deletion round runs the whole suite on its
  committed tree and re-reads the smoke script.
