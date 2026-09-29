# Plan — operator amendment amend0929-context-hygiene

Branch: feature/amend0929-context-hygiene, cut from `main` at `4e643440`
(the merge commit of pull request 295, F041 Artifact preview).

## Goal

Cut the ledger a session reads at start to open findings and the current
feature's gates, add the red-CI rule to the Open PR Gate, reclaim stale
staging copies by construction, clean the checkout, answer Q6 and register
F291 (Self-use sources v2).

## Current Step

Part G: gates, the pull request and its merge, then carry `main` into
`feature/f042-multi-project-cockpit`. Parts A to F are committed: the
ledger diet, the red-CI rule, `data reclaim --stale` with the doctor
warning and the closure step, the checkout hygiene, Q6 (D2) and F291.

## Next Steps

1. The next loop session resumes F042 at round 7 on its own branch.

## Risks

The F042 branch holds its own ledger records; the carry merge rebuilds the
ledger from `main` plus the branch's records by digest.
