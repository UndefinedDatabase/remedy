# Context — F206 Repo dependency catalog

## Active Branch
feature/f206-repo-dependency-catalog, from `main` at `74100f3cc` (the merge commit of pull request
329, F305).

## Scope
F206 (Tier 13): the repository dependency catalog, as `docs/roadmap/features/T13_F206.md` and its
amendment by DECISION F206 D1 state: the file, its validation, the order it gives an order over
several projects with the edge cited, the lockfile plausibility check, and the two commands.

## Do not touch
The job record's and the mission record's shapes, the client digest and the public API. The
catalog is maintained by hand: no crawler derives it, and the plausibility check only warns. A
cost in US dollars is never shown to the operator (DECISION amend1007b D7).

## Active assumptions
- A catalog `pid` names a registered project by its slug or its id, as an order file's `project`
  line does.
- Without a catalog an order's jobs keep the order its `project` lines give (DECISION F205 D1).
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
