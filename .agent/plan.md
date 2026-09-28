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

ROUND 8: book round 7, register and repair R-1092, then one chat turn,
a grounded answer or an action card, that both doors call (DECISION
F038 D9).

## Next Steps

1. Review round 8.
2. T003: the chat command runs a turn, prints the answer or the card,
   and sends a confirmed card through the running cockpit.
3. T003: the panel and the end-to-end proof; closure.

## Risks

None open.
