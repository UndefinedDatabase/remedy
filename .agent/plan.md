# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md` — as far as this feature reaches it; DECISION F261 D25
moves the rest to F280. Everything the closure protocol asks for is on disk: the Built State,
the integration gate, the self-use run, the rotated ledger and a READY_FOR_REVIEW package.

## Current Step

CLOSURE ROUND B, the last round of this branch. Its bookkeeping commit books round 27's verdict.
Its closure commit then applies the STATUS `[x]` line authored from round 27's measured values,
the README sync and `SU-015`'s `consumed_by` set to `F261`, with the final handoff, in ONE
commit, per the closure protocol's Rule A4 ordering; then the pull request is opened and NOT
merged.

## Next Steps

1. THE NEXT SESSION: Phase 1 rule 1 first, `.agent/STOP`; then the Open PR Gate merges this
   branch's pull request; then Rule A5 claims F280.

## Risks

- The open findings stand at 125 by distinct id. Three are High — R-0803, R-0804 and R-0807 —
  none of them F261's, and the integrity gate's `high_blockers_open` check does not see them,
  which is R-0648; so the close is PASS_WITH_RISKS.
- F261 closes with the Goal & Done sentence not met, and says so in its Built State; the
  operator may reverse the split through operator question Q3.
- The closure commit is the last commit on the branch, so the docs gate its own STATUS and
  README edits must satisfy runs after it; the reviewer ran that gate against the same edits in
  a disposable worktree before authoring.
