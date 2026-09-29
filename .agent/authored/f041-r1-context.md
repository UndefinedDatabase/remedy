# Context — F041 Artifact preview

## Active Branch
feature/f041-artifact-preview, cut from `main` at `45c584e6`
(the merge commit of pull request 294, F286 Findings paydown v5).

## Scope
F041 (Tier 5): the artifact preview — a README rendered and sanitized on
the server, screenshots in a lightbox, and preview commands whose app card
links only after a probe passes, as `docs/roadmap/features/T5_F041.md` and
DECISION F041 D1 specify.

## Do not touch
Supervisor process semantics, harness probe logic, evidence layout.

## Active assumptions
- The attack corpus in `tests/orchestration/test_artifact_markdown.py` only
  grows; a vector is never removed (DECISION F041 D1).
- The artifact roots are derived, never read from a job record.

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
