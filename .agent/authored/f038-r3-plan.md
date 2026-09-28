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

ROUND 3: book round 2, then land the grounded answer's citation check,
its mechanical answer and the canary suite in both scopes (DECISION
F038 D4).

## Next Steps

1. Review round 3.
2. T001: the model-written answer — a chat routing class, a switch that
   is off by default, the same check over its reply, and the mechanical
   answer as its fallback.
3. T002: the intent parse, the action cards and their confirmation.
4. T003: the panel, the command line and the end-to-end proof; closure.

## Risks

None open.
