# Plan — F264 Steering channel (remedy chat)

Branch: feature/f264-steering-channel, cut from `main` at `ef4cb503`,
the merge commit of pull request 270 (F282 Findings paydown v2).

## Goal

A free-form steering message to a running job, accepted over the CLI and
the cockpit, read at the run's next safe point, and acknowledged with what
was understood and from which round it applies
(`docs/roadmap/features/T5_F264.md`). Open findings at the claim: 3, all
owned by F284.

## Current Step

ROUND 1: claim F264, re-head the live review record, record DECISION F264
D1, and land T001's first half — `packages/orchestration/steering.py`, the
sealed record certified into the run log, and `remedy chat`, its first
caller, with their tests and red proofs.

## Next Steps

1. T001's second half: the cockpit's route, `chat.send` exposed on F009's
   write channel.
2. T002: consumption at the run's next safe point, with a red proof that a
   mid-call message waits.
3. T003: the acknowledgement event, in the cockpit and in `remedy chat`.
4. The closure sequence.

## Risks

T002's safe-point boundary is the property most likely to be quietly
violated; its red proof is not optional.
