# Context — F299 Acceptance checks on a repository that is not Remedy's own

## Active Branch
feature/f299-acceptance-checks-other-repos, from `main` at `1acd5ac39` (the merge commit of pull
request 317, F253).

## Scope
F299 (Tier 7, Luna gate A, part two): a mission's acceptance checks on a repository that is not
Remedy's own, as `docs/roadmap/features/T7_F299.md` lists them; DECISION F299 D1 fixes the order
and the shape. T001 measures, T002 runs the project's own test command in the project's own
environment, T003 says "no check ran" instead of judging red, T004 is the page and the proof.

## Do not touch
The closed list of executables, which grows only by its own review; the approval gate; the push
rule of F270 for a criterion that really is unmet; the compiler's fallback for a job's own
definition of done; anything in the universe workspace.

## Active assumptions
- Remedy's checks on Remedy's own repository stay unchanged, and a test pins it.
- Every production change lands with a test that is red without it, proved by the reviewer's
  mutation.
- Every probe runs with the fake providers on scratch repositories and a scratch data root; a
  folder that must not be a repository gets `GIT_CEILING_DIRECTORIES`, because `.remedy-wt/` sits
  inside the primary checkout.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
