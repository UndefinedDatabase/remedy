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

ROUND 4: book round 3, then land the model-written answer behind a
switch that is off by default, the claim check that binds every answer,
and the fallback to the mechanical answer (DECISION F038 D5).

## Next Steps

1. Review round 4.
2. T002: the intent parse, the action cards and their confirmation.
3. T003: the panel, the command line and the end-to-end proof; closure.

## Risks

None open.
