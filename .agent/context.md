# Context — F297 Findings paydown v7

## Active Branch
feature/f297-findings-paydown-v7, from `main` at `9dab4d7f0` (the merge commit of pull request
325, amend1011b-one-repo-mission).

## Scope
F297 (Tier 2), the seventh rolling findings paydown: the open findings it owns, one slice per
module, each finding's text its spec, as `docs/roadmap/features/T2_F297.md` lists them; DECISION
F297 D1 fixes the order, the two findings carried and the structural step that closes it.

## Do not touch
The resolutions earlier paydowns landed; the record is append-only. The approval gate. A cost in
US dollars is never shown to the operator (DECISION amend1007b D7).

## Active assumptions
- A repair changes what its finding names and nothing beside it.
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
