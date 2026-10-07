# Context — F295 Machine client contract v1

## Active Branch
feature/f295-machine-client-contract-v1, cut from `main` at `9a8431ea9`
(the merge commit of pull request 310, F290 Findings paydown v6).

## Scope
F295 (Tier 12, Luna gate A): the machine client contract — order files for `remedy do`, the
digest in `remedy status --json`, decisions and approvals without a terminal, and the contract
page with its gate test, as `docs/roadmap/features/T12_F295.md` lists them; DECISION F295 D1
fixes the slices and their order.

## Do not touch
The HTTP transport and the shipped UI's migration (F253); anything on Luna's side; any
time-of-day mechanic; the approval gate — a machine order ends where a human order ends.

## Active assumptions
- Every production change lands with a test that is red without it, proved by the reviewer's
  mutation.
- Every value the digest carries is read from the records; no word of it comes from a model.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
