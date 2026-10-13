# Context — F306 Findings paydown v8

## Active Branch
feature/f306-findings-paydown-v8, from `main` at `f51232ee2` (the merge commit of pull request 334,
F203).

## Scope
F306 (Tier 2): the rolling findings paydown, as `docs/roadmap/features/T2_F306.md` and DECISION
F306 D1 state: the structural steps for `packages/runtimes/dev_server.py` and
`packages/orchestration/run_manifest.py`, the repairs of R-1251 and R-1252, R-1235's three steps,
and R-1246 carried to the next paydown.

## Do not touch
The resolutions F297 landed; the record is append-only. A structural step changes no behaviour.

## Active assumptions
- Every repair lands with a test that is red without it, proved by the reviewer's mutation; a
  structural step is proved by the unchanged tests.
- This session's permission settings refuse every read under `.data/`, so R-1246 cannot be repaired.

## Constraints
- Every pytest run in a round is targeted; the closure runs the one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.
- The functions and files on `docs/system/structure-ledger-v1.md` may not grow.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
