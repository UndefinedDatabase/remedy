# Context — F038 Grounded chat & intent dispatch

## Active Branch
feature/f038-grounded-chat, cut from `main` at `fec08a5b`
(the merge commit of pull request 291, F036 Guided result tour).

## Scope
F038 (Tier 5): grounded chat — answers in a node scope and a project scope
from numbered evidence items, cited or saying "not in evidence", and intent
dispatch to the exposed command verbs through confirmable action cards,
command line first and then the panel, as `docs/roadmap/features/T5_F038.md`,
`docs/roadmap/design/grounded-chat-spec.md` and DECISION F038 D1 specify.

## Do not touch
The exposed-verb list (it grows per feature, never for the chat), evidence
formats, and the spec outside its reviewed set-list update.

## Active assumptions
- A chat answer says only what a numbered evidence item says; a source
  with nothing recorded is an item saying so (DECISION F038 D1).
- `remedy chat` keeps `send` as its default subcommand (F264).
- The findings paydown F286 waits behind F038 while no finding is open
  (DECISION F038 D2).

## Constraints
- Every pytest run in a round is targeted and serial; the resource and
  pytest budgets of `tests/regression/test_resource_safety.py` apply.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
