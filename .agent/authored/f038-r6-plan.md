# Plan — F038 Grounded chat & intent dispatch

Branch: feature/f038-grounded-chat, cut from `main` at `fec08a5b`, the
merge commit of pull request 291 (F036 Guided result tour).

## Goal

The chat becomes the cockpit's grounded control stand: answers in a node
scope and a project scope cite numbered evidence items or say "not in
evidence", and typed intent becomes a confirmable card for an exposed
command (`docs/roadmap/features/T5_F038.md`, the spec
`docs/roadmap/design/grounded-chat-spec.md`, DECISION F038 D1).

## Current Step

ROUND 6: book round 5, then send a confirmed card through the cockpit's
write door, audited exactly as a browser command is (DECISION F038 D7).

## Next Steps

1. Review round 6.
2. T002: a model-written parse for the exposed commands a sentence
   cannot fill, behind `chat.model_written`, off by default.
3. T003: the chat command finds the running cockpit, then the panel
   and the end-to-end proof; closure.

## Risks

None open.
