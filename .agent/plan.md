# Plan — F264 Steering channel (remedy chat)

Branch: feature/f264-steering-channel, cut from `main` at `ef4cb503`,
the merge commit of pull request 270 (F282 Findings paydown v2).

## Goal

A free-form steering message to a running job, accepted over the CLI and
the cockpit, read at the run's next safe point, and acknowledged with what
was understood and from which round it applies
(`docs/roadmap/features/T5_F264.md`). Open findings: 3, all owned by F284.

## Current Step

ROUND 5: book round 4's PASS, record DECISION F264 D5, and land T002's
mission half — a consumed message of a job that belongs to a mission
amends the mission's contract once, before its consumption marker is
published, and the marker and the event name the amendment.

## Next Steps

1. T003: the acknowledgement event — what was understood and from which
   round — in the cockpit and in `remedy chat`.
2. The closure sequence.

## Risks

A message that arrives during a task's last round waits for the next
task's first round; one that arrives during the job's last round is never
consumed, and T003's acknowledgement must say so rather than stay silent.
