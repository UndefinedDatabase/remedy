# Context — F301 Mission upkeep: every fifth job cleans up

## Active Branch
feature/f301-mission-upkeep, from `main` at `fdbf0802e` (the merge commit of pull request 319,
F300).

## Scope
F301 (Tier 7, the process as the product): the project's upkeep ledger, the cadence of an upkeep
job after every fifth completed job of a mission, the upkeep job compiled from the ledger by fixed
rules, the replaced files a job leaves, and what `remedy mission show` and the client digest say
of it, as `docs/roadmap/features/T7_F301.md` lists them; DECISION F301 D1 fixes the design.

## Do not touch
The shape of the mission, job and task records. The approval gate. No clock: the cadence counts
jobs. The structure limits never rise to let a change through.

## Active assumptions
- An upkeep job is an ordinary follow-up job made by `continue_mission`; it is known by the key
  `mission_upkeep` in its job's metadata.
- A finding is keyed by its job, its task and its id, because no id is stable across jobs.
- Every production change lands with a test that is red without it, proved by the reviewer's
  mutation; a structural step is proved by the unchanged tests.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
