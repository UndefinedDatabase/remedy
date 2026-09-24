# Plan — F264 Steering channel (remedy chat)

Branch: feature/f264-steering-channel, cut from `main` at `ef4cb503`,
the merge commit of pull request 270 (F282 Findings paydown v2).

## Goal

A free-form steering message to a running job, accepted over the CLI and
the cockpit, read at the run's next safe point, and acknowledged with what
was understood and from which round it applies
(`docs/roadmap/features/T5_F264.md`). Open findings: 3, all owned by F284.

## Current Step

ROUND 2: book round 1's PASS, record DECISION F264 D2, and land T001's
second half — `chat.send` exposed on F009's write door, recorded through
`steering.record_steering_message` with channel `cockpit`, with its
effect tests and red proofs.

## Next Steps

1. The cockpit's input field: the request builder, the send flow and the
   component, under `docs/ui/design_reference`.
2. T002: consumption at the run's next safe point, with a red proof that a
   mid-call message waits.
3. T003: the acknowledgement event, in the cockpit and in `remedy chat`.
4. The closure sequence.

## Risks

T002's safe-point boundary is the property most likely to be quietly
violated; its red proof is not optional.
