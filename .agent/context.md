# Context — F055 Rehearsal (dry check)

## Active Branch
feature/f055-rehearsal, from `main` at `eea4f5cfe` (the merge commit of pull request 337).

## Scope
F055 (Tier 3), as `docs/roadmap/features/T3_F055.md` and DECISION F055 D1 state: the
`--rehearse` mode of `remedy do`, its record and summary, and the reuse of a rehearsed plan.

## Do not touch
Approval semantics, the estimator's internals, and what the planner plans. A structural step
changes no behaviour.

## Active assumptions
- A rehearsal is a walk with `--plan-only`; the rehearsed job is an ordinary planned job.
- Every behaviour lands with a test that is red without it, proved by the reviewer's mutation; a
  structural step is proved by the unchanged tests.

## Constraints
- Every pytest run in a round is targeted; the closure runs the one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.
- The functions and files on `docs/system/structure-ledger-v1.md` may not grow.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
