# Plan — operator amendment amend0929-context-hygiene

Branch: feature/amend0929-context-hygiene, cut from `main` at `4e643440`
(the merge commit of pull request 295, F041 Artifact preview).

## Goal

Cut the ledger a session reads at start to open findings and the current
feature's gates, add the red-CI rule to the Open PR Gate, reclaim stale
staging copies by construction, clean the checkout, answer Q6 and register
F291 (Self-use sources v2).

## Current Step

Part C: `remedy data reclaim --stale` with `data.staging_ttl_days`, the
doctor warning `data_reclaimable` and the closure step (Parts A and B are
committed: the ledger diet, the red-CI rule, no new finding for PR 295).

## Next Steps

1. Part D: worktrees, merged branches and root remnants.
2. Part E: DECISION amend0929 D2 for Q6. Part F: register F291.
3. Part G: gates, pull request, merge, carry `main` into the F042 branch.

## Risks

The F042 branch holds its own ledger records; the carry merge rebuilds the
ledger from `main` plus the branch's records by digest.
