# Plan — operator amendment amend0929-context-hygiene

Branch: feature/amend0929-context-hygiene, cut from `main` at `4e643440`
(the merge commit of pull request 295, F041 Artifact preview).

## Goal

Cut the ledger a session reads at start to open findings and the current
feature's gates, add the red-CI rule to the Open PR Gate, reclaim stale
staging copies by construction, clean the checkout, answer Q6 and register
F291 (Self-use sources v2).

## Current Step

Part A: the rotation moves resolved finding text (tests first, then the
rule, then one real rotation and the two docs sentences).

## Next Steps

1. Part B: the red-CI rule and the retro-check of pull request 295.
2. Part C: `data reclaim --stale`, the doctor warning, the closure step.
3. Part D: worktrees, merged branches and root remnants.
4. Part E: DECISION amend0929 D2 for Q6. Part F: register F291.
5. Part G: gates, pull request, merge, carry `main` into the F042 branch.

## Risks

The F042 branch holds its own ledger records; the carry merge rebuilds the
ledger from `main` plus the branch's records by digest.
