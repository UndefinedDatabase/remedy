# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4 apart from the words
D4 gives F268, F269 and F273, and T001's remaining Acceptance lines hold, per
`docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by DECISION amend0917-throughput D4).
Everything the closure protocol asks for is on disk: the Built State, the closure suite and its
repair, the self-use run and a READY_FOR_REVIEW package (accepted HEAD `102950eb`, DECISION F280
D11).

## Current Step

CLOSURE ROUND B, the last round of this branch. Its bookkeeping commit books round 24's verdict
(PASS, one finding R-0952 resolved by DECISION F280 D11 in the same commit). Its closure commit
then applies the STATUS `[x]` line authored from round 24's measured values, the README sync and
`SU-016`'s `consumed_by` set to `F280`, with the final handoff, in ONE commit, per the closure
protocol's Rule A4 ordering; then the pull request is opened and NOT merged.

## Next Steps

1. THE NEXT SESSION: Phase 1 rule 1 first, `.agent/STOP`; then the Open PR Gate merges this
   branch's pull request; then Rule A5 claims the next feature.

## Risks

- The open findings stand at 132 before this round's C1, 131 after (R-0952 registered and
  resolved, R-0944 marked Done, net one fewer open). Three are High — R-0803, R-0804 and R-0807 —
  none of them F280's, and the integrity gate's `high_blockers_open` check does not see them,
  which is R-0648; so the close is PASS_WITH_RISKS.
- F280 owned four findings by its own `Owner:` tag: R-0944 resolved this round (fixed at round 17,
  never marked); R-0934, R-0938 and R-0940 re-assigned to F273 in C1 per amend0911-feedback rule A,
  each gaining one Acceptance line in `docs/roadmap/features/T2_F273.md`. R-0899, R-0937 and R-0941
  and R-0950 were already `Owner: F273` from earlier rounds and are untouched.
- The accepted HEAD is `102950eb`, not the rotation commit `98a5c352` the round-24 block named,
  per DECISION F280 D11 — the closure commit's STATUS line uses `102950eb`.
- The closure commit is the last commit on the branch, so the docs gate over its own STATUS and
  README edits must satisfy runs after it; the reviewer ran that gate against the same edits in
  a disposable worktree before authoring, and it read 310 passed. That same dry run found the
  README's per-tier Done/Total table needs its Tier 2 row bumped 21 to 22 alongside the two edits
  already planned — a fourth table row, not a third file.
