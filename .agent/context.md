# Context — F203 Structured logging & correlation

## Active Branch
feature/f203-structured-logging, from `main` at `e37f15be4` (the merge commit of pull request 333,
F199).

## Scope
F203 (Tier 12): one structured operations log with job, task and run correlation, as
`docs/roadmap/features/T12_F203.md` and its amendment by DECISION F203 D1 state: the setup in
`packages/orchestration/structured_log.py`, the file under `<data root>/logs/`, the wiring and the
id bindings, the `print` lint over `packages/`, and the read by job or run id.

## Do not touch
The job's timeline under `<data root>/job_logs/` and every evidence file: logs are operations
data, never evidence. The error stream keeps showing warnings exactly as it does today. OpenTelemetry
export (F197) and metrics (F198) are other features'.

## Active assumptions
- Every log line passes through the evidence redaction before it is written.
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
