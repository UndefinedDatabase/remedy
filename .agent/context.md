# Context — F294 Test load diet, part two

## Active Branch
feature/f294-test-load-diet-two, cut from `main` at `020bc9a16`
(the merge commit of pull request 305, F293 Test load diet).

## Scope
F294 (Tier 2, split off F293 by DECISION F293 D15): the rest of F293's T002. Cut the full suite's
CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001 baseline of 1,246.09, without
losing an assertion, per `docs/roadmap/features/T2_F294.md`. It starts from F293's closure reading,
940.64 CPU seconds. The first cuts make a job run start fewer git processes (DECISION F293 D10):
product work in the job runner that must keep every job's behaviour exactly as it is.

## Do not touch
No assertion is weakened or deleted to gain time (feature file, "Do not touch"). The rule of one
full suite per feature (amend0917-throughput). The worker cap and its record
(`tests/load_governor.py`, `tests/conftest.py`). The F7 rule that reading a repository never runs
its configured helpers (`packages/orchestration/run_manifest.py`).

## Active assumptions
- A cut is measured before and after in one tree, by the reviewer's dry run: the git processes one
  in-process one-task `remedy do` starts, and the CPU seconds of the test files it touches.
- The "after" reading of the 40 percent target is the closure's one full-suite run.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
