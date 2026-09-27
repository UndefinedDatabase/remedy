# Plan — F030 Steering messages

Branch: feature/f030-steering-messages, cut from `main` at `15f5d384`, the
merge commit of pull request 288 (F029 Subtree rerun).

## Goal

A note typed while a job runs reaches the task it is meant for: it lands
in that task's next round prompt as a binding operator note, the feed
shows the operator's own line with the builder's next action as the only
reply, and a note its task finished without reading is reported
(`docs/roadmap/features/T5_F030.md`, DECISION F030 D1).

## Current Step

ROUND 1: claim F030, book F029's round 11, record DECISION F030 D1, and
land T001 — the task address on a steering message, the drain at the
task's round start, the operator-note segment and the unconsumed listing.

## Next Steps

1. T002: the write door's `job.steer-task` and `remedy job steer` with the
   task state gate, the audit and the event.
2. T003: the feed shows the operator's line, the input addresses the
   focused task, and the end-to-end proof.
3. The closure sequence.

## Risks

None open. Open findings: 0.
