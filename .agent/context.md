# Context — F199 Self-health & crash reports

## Active Branch
feature/f199-self-health, from `main` at `8ee65f61a` (the merge commit of pull request 332, F058).

## Scope
F199 (Tier 12): Remedy's own health checks and local crash reports, as
`docs/roadmap/features/T12_F199.md` and its amendment by DECISION F199 D1 state: the checks of
`packages/orchestration/self_health.py`, the command `remedy doctor health`, the crash report
under the data root, and the supervisor's health on its public API.

## Do not touch
`doctor core` and `doctor_core_report`, which the structure ledger lists. No check repairs, moves
or deletes anything; no check calls a provider. A crash report is never sent anywhere. The worker
isolation (F152), the secret corpus (F171), the schema registry (F245) and `remedy feedback`
(F220) are other features'.

## Active assumptions
- A detail never prints the home folder's path.
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
