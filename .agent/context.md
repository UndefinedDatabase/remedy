# Context — F290 Findings paydown v6

## Active Branch
feature/f290-findings-paydown-v6, cut from `main` at `31542dbfd`
(the merge commit of pull request 308, F200 Daemon mode).

## Scope
F290 (Tier 2): the rolling findings paydown. It takes the seven findings open at its claim, one
slice per finding, as `docs/roadmap/features/T2_F290.md` lists them; DECISION F290 D1 fixes the
slices and their order.

## Do not touch
The resolutions earlier paydowns landed; the record is append-only. A repair changes only what its
finding's own text names.

## Active assumptions
- Every repair lands with a test that is red without it, proved by the reviewer's mutation.
- A finding that cannot be repaired in one round keeps its owner line and is carried by name.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
