# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8. F275 is registered, the integration gate
has PASSED, the self-use precondition is met, and R-0837 is fixed at BOTH sites, so the closure
package now builds.

## Current Step

CLOSURE ROUND A. It books round 21's PASS verdict, then rotates the ledger by
`scripts/rotate_live_review.py` as its own commit — the step operator amendment amend0905-throughput
places after the verdict bookings and before the STATUS flip — and then RUNS the closure evidence
job and the fresh review zip from a clean tree. The reviewer dry-ran this whole sequence at the
post-rotation head before authoring it: the producer returns `PASS_WITH_RISKS` and the package
builds `READY_FOR_REVIEW`. Nothing is committed after the zip except the handback, so the accepted
HEAD is the rotation commit.

## Next Steps

1. CLOSURE ROUND B, in two commits. FIRST the ledger: round 22's PASS verdict, and the authored
   `Done: R-0837` — its resolution condition requires a closure package that reaches
   READY_FOR_REVIEW, so it can only be written AFTER round A has built one. THEN the closure
   commit: the STATUS `[x]` line the reviewer authors from round A's measured values, the README
   capability sync and the one `consumed_by` edit setting `SU-013` to `f274`, all three in ONE
   commit per the closure protocol's Rule A4 ordering; then the pull request. The PR is NOT merged
   this session — it merges at the next feature's start through the Open PR Gate, which is the
   operator's manual-review window.
2. F275 is registered and placed directly after F274, so Rule A5 proposes it first in the next
   session, AFTER that Open PR Gate has merged this branch.

## Risks

- The package's `base_commit` is the FORK POINT `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, whose
  ancestry-path and plain `rev-list` counts the reviewer measured EQUAL. NEVER `git merge-base`,
  which names `origin/main`'s tip `d0d8b24d` here, gives unequal counts, and is the defect that
  packaged F260's round 22 as BLOCKED_EVIDENCE.
- The authority set is read from the WORKING TREE, and `pytest` has no `norecursedirs` here, so an
  untracked file or a leftover worktree changes what is packaged and what is collected. The tree is
  clean and the worktrees pruned before the evidence job.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12. The integrity gate's `high_blockers_open` check reports "no
  open blocker/high findings" and is WRONG while those four are open — that is R-0648, and
  DECISION F272 D17 requires the close to say so and to rest on the named list instead.
