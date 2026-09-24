# Plan — F264 Steering channel (remedy chat)

Branch: feature/f264-steering-channel, cut from `main` at `ef4cb503`,
the merge commit of pull request 270 (F282 Findings paydown v2).

## Goal

A free-form steering message to a running job, accepted over the CLI and
the cockpit, read at the run's next safe point, and acknowledged with what
was understood and from which round it applies
(`docs/roadmap/features/T5_F264.md`). Open findings: 3, all owned by F284.

## Current Step

ROUND 7: book round 6's PASS, record DECISION F264 D7, and land T003's
second half — the cockpit's activity feed shows each acknowledgement as
the round and the restatement, read from the stream by one checked reader.
With it T001 to T003 are built.

## Next Steps

1. The closure sequence's first half: the user-facing docs for `remedy
   chat`, the feature file's Built State, the checklist consolidation, the
   self-use track, and the feature's one full suite.
2. The evidence bundle and the review package.
3. The closing round: STATUS flip with its README pins, and the pull
   request.

## Risks

None open inside this feature.
