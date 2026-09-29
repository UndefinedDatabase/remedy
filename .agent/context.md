# Context — F043 Explanation layer

## Active Branch
feature/f043-explanation-layer, cut from `main` at `21bfc188`
(the merge commit of pull request 299, F291 Self-use sources v2).

## Scope
F043 (Tier 5): the explanation layer — one catalog of term explanations,
one `Term` component with a tooltip on hover and focus, a two-direction
audit over the rendered surfaces, a first-run tour, and a searchable '?'
panel, as `docs/roadmap/features/T5_F043.md` and DECISION F043 D1 specify.

## Do not touch
The wording of the definitions the catalog anchors to (quoted, not
edited); the result tour's stops; the docs site's content.

## Active assumptions
- Every catalog entry anchors to a phrase of the file that defines its
  term, and a test reads that file (DECISION F043 D1 (1)).
- A term is declared only through `Term`, so its `data-term` attribute is
  what the audit reads.
- The tour's palette stop is the '?' panel until F044 builds a palette.

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
