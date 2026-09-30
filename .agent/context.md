# Context — F293 Test load diet

## Active Branch
feature/f293-test-load-diet, cut from `main` at `8a067a3b9`
(the merge commit of pull request 304, amend0930b-slow-cap).

## Scope
F293 (Tier 2, registered thin by operator amendment amend0930-test-load): cut the CPU cost of the
full suite and round test selections by at least 40%, per `docs/roadmap/features/T2_F293.md` and
DECISION amend0930 D5. No behavioural feature surface; every assertion the suite makes today still
holds after this feature.

## Do not touch
No assertion is weakened or deleted to gain time (feature file, "Do not touch"). The rule of one
full suite per feature (amend0917-throughput). The worker cap and its record
(`tests/load_governor.py`, `tests/conftest.py`).

## Active assumptions
- The full suite's CPU seconds baseline is 1,288 CPU seconds / 448.7s wall, measured under the
  6-worker cap on 2026-09-30 (feature file, "Baseline"); T002's 40% target is computed against
  that figure unless this round's own T001 run reads a materially different number, in which case
  the round states which baseline it used and why.
- R-1118 (a leaked test process, owned by this feature) is read against T001's own "processes alive
  after the run" reading before it is marked resolved or carried.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to anything other than this round's own explicitly-authorized full-suite measurement.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
