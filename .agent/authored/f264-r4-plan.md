# Plan — F264 Steering channel (remedy chat)

Branch: feature/f264-steering-channel, cut from `main` at `ef4cb503`,
the merge commit of pull request 270 (F282 Findings paydown v2).

## Goal

A free-form steering message to a running job, accepted over the CLI and
the cockpit, read at the run's next safe point, and acknowledged with what
was understood and from which round it applies
(`docs/roadmap/features/T5_F264.md`). Open findings: 3, all owned by F284.

## Current Step

ROUND 4: book round 3's PASS, record DECISION F264 D4, and land T002 — the
ping-pong loop consumes pending messages at the top of each round, exactly
once, records the consumption round, and carries every consumed message in
the builder prompt, with the with-and-without fixture and red proofs.

## Next Steps

1. T002's mission half: a message consumed for a job that belongs to a
   mission also amends the mission's contract.
2. T003: the acknowledgement event, in the cockpit and in `remedy chat`.
3. The closure sequence.

## Risks

A message that arrives during a task's last round waits for the next
task's first round; one that arrives during the job's last round is never
consumed, and T003's acknowledgement must say so rather than stay silent.
