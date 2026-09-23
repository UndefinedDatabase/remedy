# Plan — F278 Durable writes & loud failures

Branch: feature/f278-durable-writes-loud-failures, cut from `main` at
`9817a927`, the merge commit of pull request 265 (F283's closure).

## Goal

One durable write in this repository, used everywhere, and no artifact that is
silently incomplete (`docs/roadmap/features/T2_F278.md`).

## Current Step

ROUND 11, the closure sequence's evidence half. It books round 10's PASS and
resolves R-1039, then builds the feature's evidence bundle against the fork
point and a fresh review package, recording the package's name, its SHA-256,
the directory it lives in and the accepted head it covers.

## Next Steps

1. The closing round: the ledger rotation, then the STATUS line with the
   README counters and the self-use item's `consumed_by` in one commit, and
   the pull request, which is never merged in the session that opens it.

## Risks

Twenty-six findings are open after this round's resolution and none is this
feature's own. Eleven rounds are spent of the soft limit of 25.
