# Context — F036 Guided result tour

## Active Branch
feature/f036-guided-result-tour, cut from `main` at `9dc2f2a7`
(the merge commit of pull request 290, F035 Ownership ledger).

## Scope
F036 (Tier 5): a guided tour of a finished job — at most eight stops built
from the report, the diff, the evidence files and the Definition of Done,
each anchored to a place that exists, written by a side-role model call
with a mechanical fallback, shown as a browser overlay and printed by the
command line, as `docs/roadmap/features/T5_F036.md` and DECISION F036 D1
specify.

## Do not touch
Report content, deep-link formats (consumed, not changed), and preview
mechanics, which F041 adds to tour stops later.

## Active assumptions
- A tour restates what the job's own records say and adds no claim; a stop
  without a resolving anchor is dropped, never shipped (DECISION F036 D1).
- The findings paydown F286 waits behind F036 while no finding is open
  (DECISION F036 D2).

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
