# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 23 continues T003. It books round 22's PASS, registers R-0927 to R-0930 for F273 and
records DECISION F261 D22, then deletes the queue words of `job`, `worker run` and
`mission ledger` by one table. The `propose` group stays deferred, for the reasons D22 measures.

## Next Steps

1. `job rerun` and `job fulfill`, the inventory's round L.
2. The `propose` group, with the DECISION its deletion needs about the two surviving gates D22
   names, and the F011 `--status` discriminator `tests/cli/test_job_stop.py` loses with it.
3. The rest of T003 in the inventory's order, with R-0767 and R-0894.
4. `job budget <id> set` over the run-contract budget fields and the token budget profile, the
   word DECISION amend0905-vocab D4 gives those writes, with R-0906 and R-0909.
5. T004, which owes the visible group order of D4 and the README quickstart of R-0895.

## Risks

- 120 findings are open by distinct id before this round's record and 124 after it; three are
  High, R-0803, R-0804 and R-0807.
- The feature's soft limit of 25 rounds leaves two after this one, and the inventory proposes
  more than two; the session that reaches the limit owes the scope report and executes the
  split-and-close default of operator amendment amend0905-throughput, placing the follow-up
  feature directly after F261 per amend0906.
- A deletion that would break a SURVIVING command is deferred to a round that can rule on it,
  never shipped with a finding: that is why `propose` is still not in this round.
