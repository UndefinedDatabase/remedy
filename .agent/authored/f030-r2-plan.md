# Plan — F030 Steering messages

Branch: feature/f030-steering-messages, cut from `main` at `15f5d384`, the
merge commit of pull request 288 (F029 Subtree rerun).

## Goal

A note typed while a job runs reaches the task it is meant for: it lands
in that task's next round prompt as a binding operator note, the feed
shows the operator's own line with the builder's next action as the only
reply, and a note its task finished without reading is reported
(`docs/roadmap/features/T5_F030.md`, DECISIONS F030 D1 and D2).

## Current Step

ROUND 2: book round 1's PASS, record DECISION F030 D2, and land T002 —
`job.steer` on the write door and as `remedy job steer`, one shared
command with the task state gate, and `remedy chat show` naming a note's
task.

## Next Steps

1. T003: the feed shows the operator's line, the input addresses the
   focused task, and the end-to-end proof.
2. The closure sequence.

## Risks

None open. Open findings: 0.
