# Plan — F264 Steering channel (remedy chat)

Branch: feature/f264-steering-channel, cut from `main` at `ef4cb503`,
the merge commit of pull request 270 (F282 Findings paydown v2).

## Goal

A free-form steering message to a running job, accepted over the CLI and
the cockpit, read at the run's next safe point, and acknowledged with what
was understood and from which round it applies
(`docs/roadmap/features/T5_F264.md`). Open findings: 3, all owned by F284.

## Current Step

ROUND 10, the closing round: book round 9's PASS, rotate the ledger, flip
F264's STATUS line to accepted with its README pins in the same commit,
and open the pull request. T001 to T003 are built and the package is
READY_FOR_REVIEW.

## Next Steps

1. The next session merges this feature's pull request at the Open PR
   Gate, then claims the next feature under Rule A5.

## Risks

None open inside this feature.
