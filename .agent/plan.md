# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. T001, T002 and T003 are DONE, the
Built State is current, the integration gate passed and the self-use precondition is met.

## Current Step

CLOSURE ROUND A. It books round 107's verdict with the recurrences of `R-0784` and `R-0838`
that the self-use run produced, then rotates the ledger by `scripts/rotate_live_review.py` as
its own commit, and from a clean tree at that commit runs the closure evidence job and builds a
fresh review package. The reviewer dry-ran this sequence at a throwaway head before authoring
it: the producer returns `PASS_WITH_RISKS` and the package builds `READY_FOR_REVIEW`. The
rotation commit is the accepted head; after it come only the suite transcript and the handback.

## Next Steps

1. CLOSURE ROUND B: book round 108's verdict, then the closure commit — the STATUS `[x]` line
   authored from round A's measured values, the README sync and `SU-014`'s `consumed_by` set to
   `F275`, in one commit — then the pull request, which is not merged in that session.

## Risks

- The package's `base_commit` is the FORK POINT `a5bf894946ab6de053a4232109d6341a63533768`,
  whose ancestry-path and plain `rev-list` counts the reviewer measured equal; never
  `git merge-base`, which names `d0aa833b` after this branch merged `main` in.
- The authority set is read from the WORKING TREE, so an untracked file or a leftover worktree
  changes what is packaged: the tree is clean and the worktrees pruned before the evidence job.
- A DRY-RUN PACKAGE IS IN THE ARCHIVE: `remedy-review-20260914-230148-READY_FOR_REVIEW.zip`
  in `/home/decodeux/Repos/remedy-history/zips/` was built from the reviewer's throwaway head
  `847335e2` and is NOT the closure package.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's per DECISION F272
  D12; the integrity gate's `high_blockers_open` check does not see them, which is R-0648.
- The open set is 89 by distinct id, with `R-0784`, `R-0809`, `R-0838` and `R-0880` open.
