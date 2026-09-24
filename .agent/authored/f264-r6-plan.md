# Plan — F264 Steering channel (remedy chat)

Branch: feature/f264-steering-channel, cut from `main` at `ef4cb503`,
the merge commit of pull request 270 (F282 Findings paydown v2).

## Goal

A free-form steering message to a running job, accepted over the CLI and
the cockpit, read at the run's next safe point, and acknowledged with what
was understood and from which round it applies
(`docs/roadmap/features/T5_F264.md`). Open findings: 3, all owned by F284.

## Current Step

ROUND 6: book round 5's PASS, record DECISION F264 D6, and land T003's
first half — the consumption event restates the message with its round,
the stream carries that acknowledgement, and `remedy chat show` lists each
message as acknowledged, waiting or not taken in.

## Next Steps

1. T003's second half: the cockpit renders the acknowledgement from the
   stream, under the steering input.
2. The closure sequence.

## Risks

None open inside this feature; its closure runs the one full suite.
