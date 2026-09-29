# Context — F042 Multi-project cockpit

## Active Branch
feature/f042-multi-project-cockpit, cut from `main` at `4e643440`
(the merge commit of pull request 295, F041 Artifact preview).

## Scope
F042 (Tier 5): the multi-project cockpit — a project list and per-project
summary on the server, a client project context with a header switcher, and
a home grid of project cards with deep links carrying `?project=`, as
`docs/roadmap/features/T5_F042.md` and DECISION F042 D1 specify.

## Do not touch
Scoping rules and semantics, registry mechanics, per-job SSE contracts.

## Active assumptions
- A card's numbers come from readers that already exist: `scoped_jobs`,
  each job's decision inbox, the newest job's digest and the ledger's cost
  query (DECISION F042 D1).
- Cost today is the UTC calendar day, and its basis uses the digest's words.

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
