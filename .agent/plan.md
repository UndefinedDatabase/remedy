# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 19 continues T003. It books round 18's PASS and a prose slip, registers R-0911 and R-0912
for F273 and records DECISION F261 D18, then renames `do report` into the new `run` group as
`run show <id>` and `run list`, and deletes `do evidence`, one table per commit.

## Next Steps

1. `do repair-attest`, `do job-resume` and `do replan`, as `.agent/f261_t003_inventory.md`
   proposes, then the `do continue` hints with the command and `do_continue.py`, with R-0900.
2. The rest of T003 in the inventory's order, each round re-measured before it is authored,
   with R-0767 and R-0894.
3. `job budget <id> set` over the run-contract budget fields and the token budget profile, the
   word DECISION amend0905-vocab D4 gives those writes, with R-0906 and R-0909.
4. T004, which owes the visible group order of D4 and the README quickstart of R-0895.

## Risks

- 105 findings are open by distinct id before this round's record and 107 after it; three are
  High, R-0803, R-0804 and R-0807.
- The inventory proposes more rounds than F261's soft limit of 25 leaves; the session that
  reaches the limit owes the scope report and the split-and-close default.
- A rename keeps a payload only if every consumer is measured first, and a deletion's consumers
  include shell strings a guard cannot read, so every round of T003 runs the whole suite on its
  committed tree.
