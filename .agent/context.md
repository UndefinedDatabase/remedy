# Context — F300 Structure ledger and size ratchet

## Active Branch
feature/f300-structure-ledger-size-ratchet, from `main` at `b25d87a24` (the merge commit of pull
request 318, F299).

## Scope
F300 (Tier 2, the process as the product): a measure of a repository's structure as a product
command, Remedy's ledger of its large functions and files, a ratchet test that lets each recorded
size fall and never rise, the paydown rule, and the first structural step, as
`docs/roadmap/features/T2_F300.md` lists them; DECISION F300 D1 fixes the measure.

## Do not touch
Behaviour, except R-1160's repair, which lands alone with its red-proof. Any public import path.
The limits never rise to let a change through.

## Active assumptions
- The measure reads only and assumes nothing about Remedy's own layout, because F301 uses it on
  every project Remedy builds.
- Every production change lands with a test that is red without it, proved by the reviewer's
  mutation.
- A test that needs a repository builds one under `tmp_path`; a folder that must not be a
  repository gets `GIT_CEILING_DIRECTORIES`, because `.remedy-wt/` sits inside the checkout.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
