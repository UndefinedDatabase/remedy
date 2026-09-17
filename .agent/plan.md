# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4 apart from the words
D4 gives F268, F269 and F273, and T001's remaining Acceptance lines hold, per
`docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by DECISION amend0917-throughput D4).
The Built State is current, the closure suite ran once with its repair confirmed, and the
self-use precondition is met.

## Current Step

CLOSURE ROUND A. Books round 23's verdict, rotates the ledger by `scripts/rotate_live_review.py`
as its own commit, and from a clean tree at that commit runs the closure evidence job, the
integrity check and a fresh review package. The rotation commit is the accepted head; only the
handback follows it in this round.

## Next Steps

1. CLOSURE ROUND B: book round A's verdict, then the closure commit — the STATUS `[x]` line
   authored from round A's measured values, the README sync and `SU-016`'s `consumed_by` set to
   `F280`, in one commit — then the pull request, which is not merged in that session.
2. The next feature Rule A5 proposes once F280 is merged.

## Risks

- The package's `base_commit` is the FORK POINT `9f1b6d25`, which is also the merge base because
  this branch has merged nothing in.
- The authority set is read from the WORKING TREE, so an untracked file or a leftover worktree
  changes what is packaged: the tree is clean and the worktrees pruned before the evidence job.
- The open High findings are R-0803, R-0804 and R-0807, none of them F280's; the integrity gate's
  `high_blockers_open` check does not see them, which is the already-open R-0648 gap.
- The open set is 132 by distinct id before this round's booking; R-0899, R-0937, R-0938, R-0941
  and R-0950 are re-assigned to F273 in the closure commit per amend0911-feedback rule A.
- `git branch --list 'remedy/job-*'` reads 19 lines at this round's base; no runner is called this
  round, so it must still read 19 at the round's own head.
