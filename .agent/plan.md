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

ROUND 1: claim F038, move F286 behind it (DECISION F038 D2), book F036's
round 9, register and repair R-1091, and land the node scope of T001 in
`packages/orchestration/chat_evidence.py`.

## Next Steps

1. Review round 1.
2. T001: the project scope over the spec's evidence set, with the spec's
   set-list update.
3. T001: the grounded answer, its citation check, the unsupported marker
   and the canary suite.
4. T002: the intent parse, the action cards and their confirmation.
5. T003: the panel, the command line and the end-to-end proof; closure.

## Risks

- R-1091 is open and High until its repair is reviewed, so the integrity
  check reads its open-High check as failed until then.
