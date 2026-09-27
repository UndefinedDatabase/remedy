# Context — F030 Steering messages

## Active Branch
feature/f030-steering-messages, cut from `main` at `15f5d384`
(the merge commit of pull request 288, F029 Subtree rerun).

## Scope
F030 (Tier 5): a steering note addressed to one task of a running job —
taken in at that task's next round start as a binding operator note at
the steering rank, shown in the feed as the operator's own line, and
listed when its task finished without reading it — built on F264's
steering channel, as `docs/roadmap/features/T5_F030.md` and DECISION
F030 D1 specify.

## Do not touch
Chat and question answering, segment ranks, and round mechanics.

## Active assumptions
- A note is a steering message with a task address; F264's record,
  seal, event and consumption marker are reused (DECISION F030 D1).
- A note is carried by every later round of its task, as F264 carries a
  job-wide message.

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
