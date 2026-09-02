# Context — F108 Tiered artifact summaries

## Active Branch
feature/f108-tiered-artifact-summaries, cut from `main` at
`ec81e697bf498a6753d82d7e6a8d3c72467cd5d7`.

## Scope
F108 (Tier 3, depends on F107 — done): any oversized artifact gets a tiered
representation (L1 summary, sectioned L2 summaries, full reference path);
prompt assembly consumes L1 plus only the relevant L2 sections. Task
slicing: T001 schema + mechanical sectioners + storage/caching; T002
generation call with the summary role + fallback; T003 compiler
integration + end-to-end fixture.

## Do not touch
Routing decisions, local-model setup, dossier compression — all explicitly
out of scope per `docs/roadmap/features/T3_F108.md` Do not touch. No
provider-routing feature is modified; this feature only DECLARES the
summary role for T002.

## Assumptions
- F107 (context compiler v2) is `[x]` done and owns selection/budgets; T003
  integrates with it rather than replacing it.
- The summary role is a new provider-call role beside the existing evidence
  and actuals roles, not yet inspected this round beyond the feature file.

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

This round is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for this round lives in the `## Current Step` section
of `.agent/plan.md`. This file deliberately does not restate it.
