# Context — F116 Cost anomaly alarm

## Active Branch
feature/f116-cost-anomaly-alarm, cut from `main` at `e80b95467`
(the merge commit of pull request 312, F287 Provider session continuity across relaunch).

## Scope
F116 (Tier 3, Luna gate B): one burn detector that compares a run's spend rate with what is
expected, trip actions for jobs, and the watchdog's burn tripwire as a caller of the same
detector, as `docs/roadmap/features/T3_F116.md` lists them; DECISION F116 D1 fixes the slices and
their order.

## Do not touch
Notification channels, budget limits (a separate mechanism), calibration (F074's), as the feature
file says.

## Active assumptions
- Every production change lands with a test that is red without it, proved by the reviewer's
  mutation.
- The detector runs at the existing safe points; no test starts a real provider process.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
