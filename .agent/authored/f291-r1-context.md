# Context — F291 Self-use sources v2

## Active Branch
feature/f291-self-use-sources-v2, cut from `main` at `aa5defde`
(the merge commit of pull request 298, F042 Multi-project cockpit).

## Scope
F291 (Tier 5): two more sources for the self-use generator — Tier 4, the
excused blind handlers the BLE001 ratchet counts, and Tier 5, the production
modules no test file imports — as `docs/roadmap/features/T5_F291.md` and
DECISION F291 D1 specify.

## Do not touch
Tiers 0 to 3 and their order; the fence over `.agent/` that a self-use run
carries (DECISION amend0926-decisions-selfuse D4); the ratchet's rule that
the count may only go down.

## Active assumptions
- Tier 4 reads exactly what `tests/test_ble001_ratchet.py` counts, and the
  generator's own source spells no mark (DECISION F291 D1).
- Tier 5 reads `import` statements under `tests/`, never history or strings.

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
