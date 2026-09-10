# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE.

## Current Step

ROUND 33 continues T003. It registers and repairs R-0874, the two sentences in
`docs/system/architecture.md` that still describe the execution loop round 32 deleted. It
then retires the `job.run-next` command surface: the catalog entry, the dispatch line, the
two `related=` tuples that would otherwise dangle, and all 29 advertisements of it across
eight orchestration modules, the smoke script and seven test files, which move to
`job resume` under DECISION F275 D18. The handler `_cmd_run_next_task_local` SURVIVES as an
internal function; only its command door closes.

## Next Steps

1. Retire the `job.run` command surface and absorb both handlers under the `job.resume`
   door, one owner and no copy, registering the `--unattended` and `--yes` surfaces
   DECISION F275 D18 names as genuinely lost.
2. The flip DECISION F275 D17 sized, as the one declared-oversize commit AGENTS.md permits
   per feature, re-deriving the site set at its own base.
3. The resolver collapse DECISION F260 D5 places in T003, and the classic store.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- A command deletion is invisible to a text sweep wherever the CLI is invoked as an argv
  LIST, because the group and the subcommand are separate elements. Round 33 found two such
  sites this way and no other instrument would have. Step 1 above re-runs that sweep.
- The open set is 87 by distinct id at this round's base `7d14e89f`. This round registers
  R-0874 and resolves it in the same round, so it returns to 87. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
