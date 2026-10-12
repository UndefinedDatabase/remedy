# Context — F305 Multi-repo missions: the cockpit's chain band

## Active Branch
feature/f305-multi-repo-chain-band, from `main` at `f6004fdf1` (the merge commit of pull request
328, F297).

## Scope
F305 (Tier 13), split off F205: the cockpit's mission card and its chain band of repository chips,
as `docs/roadmap/features/T13_F305.md` and its amendment by DECISION F305 D1 state, and R-1248,
the card one per repository's mission with its orders loaded on demand and a per-order roll-up.

## Do not touch
The mission record's shape and its writers; the client digest and the public API. A cost in US
dollars is never shown to the operator (DECISION amend1007b D7). No global evidence store: a chip
names another project's job by references and titles only, and its click opens that project's own
cockpit.

## Active assumptions
- An order over several repositories is one batch in each repository's mission, the batches
  sharing a correlation id (DECISION amend1011b D4); its chain is read across those batches.
- Every production change lands with a test that is red without it, proved by the reviewer's
  mutation; a structural step is proved by the unchanged tests.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.
- The functions and files on `docs/system/structure-ledger-v1.md` may not grow.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
