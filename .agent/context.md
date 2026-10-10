# Context — F205 Multi-repo missions

## Active Branch
feature/f205-multi-repo-missions, from `main` at `c72d2a7ec` (the merge commit of pull request
321, F302).

## Scope
F205 (Tier 13, Luna gate A part three): one order naming several registered projects, one job per
repository, each job applied, committed and pushed in its own repository, the loop switching
project per job, the digest and the public API naming each job's repository, the upkeep across
repositories, and the fixture mission over two repositories, as
`docs/roadmap/features/T13_F205.md` lists them; DECISION F205 D1 fixes the order.

## Do not touch
No global evidence store and no second mission store: evidence, cards and ledgers stay in their
own project. The approval gate. A merge stays the operator's. A cost in US dollars is never shown
to the operator (DECISION amend1007b D7).

## Active assumptions
- A mission over several repositories lives under the project its order names first.
- Until F206's catalog exists, the jobs follow the order the order names its projects.
- Every production change lands with a test that is red without it, proved by the reviewer's
  mutation; a structural step is proved by the unchanged tests.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.
- `do_sequence.py`, `apps/cli/commands/do_cmd.py`, `orchestrator_loop.py`, `job_apply.py`,
  `pingpong_job.py` and `public_api.py` are on the structure page and may not grow.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
