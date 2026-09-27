# Plan — F030 Steering messages

Branch: feature/f030-steering-messages, cut from `main` at `15f5d384`, the
merge commit of pull request 288 (F029 Subtree rerun).

## Goal

A note typed while a job runs reaches the task it is meant for: it lands
in that task's next round prompt as a binding operator note, the feed
shows the operator's own line with the builder's next action as the only
reply, and a note its task finished without reading is reported
(`docs/roadmap/features/T5_F030.md`, DECISIONS F030 D1 to D3).

## Current Step

ROUND 3: book round 2's PASS, record DECISION F030 D3, and land T003's
browser half — the stream carries a note's text, the feed shows it as
the operator's own line, the input addresses the selected task, and the
copy promises no conversation.

## Next Steps

1. T003's end-to-end proof: a note sent through the door while a task
   builds reaches its next round's trace, and the stream shows the note
   before the task's next action.
2. The closure sequence.

## Risks

None open. Open findings: 0.
