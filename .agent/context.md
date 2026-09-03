# Context — F110 Model routing by task class

## Active Branch
feature/f110-model-routing-by-task-class, cut from `main` at the merge
commit of pull request 232.

## Scope
F110 (Tier 3, depends on F103 — done): each provider call declares a task
class; a router maps classes to model tiers; every routed call records the
routed model with its reason; the hard rules of
`docs/agents/model_routing_policy.md` are enforced in code; and a class
moves to a cheaper tier only against documented benchmark evidence. Task
slicing: T001 the call-site and role inventory, the single resolver seam
and the class declarations; T002 the resolver, the config schema and the
hard-rule checks with a refused fixture per rule; T003 the
promotion-evidence discipline, the evidence fields and the goldens.

## Do not touch
Failover chains, local-endpoint setup and learned routing — all explicitly
out of scope per `docs/roadmap/features/T3_F110.md` Do not touch. Model
UNAVAILABILITY belongs to the failover feature; F110 only picks the
intended model. `packages/orchestration/builder_routing.py` is a DIFFERENT
routing layer — it decides WHEN an expensive builder is worth spending, not
WHICH model a task class gets — and F110 neither edits nor absorbs it.

## Assumptions
- `docs/agents/model_routing_policy.md` is the human-readable policy and
  stays so; F110 seeds the class table FROM it and enforces it in code,
  and the acceptance line is a sync test that diffs the two.
- `packages/orchestration/role_config.py` resolves provider, model and
  effort per ROLE today. Whether it is already the single selection seam
  or only one of several is what T001a MEASURES rather than assumes.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree,
  never in the primary checkout, which satisfies `git status --porcelain`
  empty at every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- This session's reviewer CAN execute `ruff`, measured at the F110 claim as
  version 0.15.17 with `ruff check packages/orchestration/role_config.py`
  answering "All checks passed!" under the repository's own configuration.
  F109's opposite constraint was measured for F109 and does NOT carry
  forward: a round of F110 that ships a `.py` file may gate on ruff.

This round is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`, which AGENTS.md's "Completion Report — Item-Status
Table" section requires of every completion report. This file deliberately
does not restate it.
