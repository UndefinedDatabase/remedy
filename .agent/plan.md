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

ROUND 7: book round 6, then the model-written intent parse behind
`chat.model_written`, with answering a decision and adding a task as
two new chat verbs (DECISION F038 D8).

## Next Steps

1. Review round 7.
2. T003: the chat command finds the running cockpit, answers a
   question, and confirms a card on a y/N line.
3. T003: the panel and the end-to-end proof; closure.

## Risks

None open.
