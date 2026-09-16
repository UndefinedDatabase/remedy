# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 24 continues T003. It books round 23's PASS, registers R-0931 for F273 and records
DECISION F261 D23, then deletes `job rerun` by one table and renames the group `teach` to
`teacher` by a second. `job fulfill` is deferred by D23, as `propose` is by D22.

## Next Steps

1. The `settings` alias surface over `config`, DECISION D-D of the feature file.
2. `job budget <id> set` over the run-contract budget fields and the token budget profile, with
   R-0906 and R-0909, and then `job fulfill`, which D23 defers until that write exists.
3. The `propose` group, with the DECISION its deletion needs about the two surviving gates D22
   names, and the F011 `--status` discriminator `tests/cli/test_job_stop.py` loses with it.
4. The rest of T003 in the inventory's order, with R-0767 and R-0894.
5. T004, which owes the visible group order of D4 and the README quickstart of R-0895.

## Risks

- 124 findings are open by distinct id before this round's record and 125 after it; three are
  High, R-0803, R-0804 and R-0807.
- The feature's soft limit of 25 rounds leaves one after this one, and the steps above are more
  than one round; the session that reaches the limit owes the scope report and executes the
  split-and-close default of operator amendment amend0905-throughput, placing the follow-up
  feature directly after F261 per amend0906.
- A deletion that would break a SURVIVING command is deferred to a round that can rule on it,
  never shipped with a finding: that is why `propose` and `job fulfill` are not in this round.
