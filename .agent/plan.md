# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md` — as far as this feature reaches it; DECISION F261 D25
moves the rest to F280. The Built State is current, the integration gate passed and the
self-use precondition is met.

## Current Step

CLOSURE ROUND A. It books round 26's verdict with the recurrences of R-0645, R-0784 and R-0838
that round measured, then rotates the ledger by `scripts/rotate_live_review.py` as its own
commit, and from a clean tree at that commit runs the closure evidence job, the integrity check
and a fresh review package. The rotation commit is the accepted head; only the handback follows
it in this round.

## Next Steps

1. CLOSURE ROUND B: book round A's verdict, then the closure commit — the STATUS `[x]` line
   authored from round A's measured values, the README sync and `SU-015`'s `consumed_by` set to
   `F261`, in one commit — then the pull request, which is not merged in that session.
2. F280, which Rule A5 proposes once F261 is merged.

## Risks

- The package's `base_commit` is the FORK POINT `7cdde89b`, which is also the merge base
  because this branch has merged nothing in.
- The authority set is read from the WORKING TREE, so an untracked file or a leftover worktree
  changes what is packaged: the tree is clean and the worktrees pruned before the evidence job.
- The open High findings are R-0803, R-0804 and R-0807, none of them F261's; the integrity
  gate's `high_blockers_open` check does not see them, which is R-0648.
- The open set is 125 by distinct id; seven that F261 owned belong to F280 by DECISION F261 D25.
