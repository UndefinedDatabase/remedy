# Context — F304 Machine client contract v1.1, part two: what a client can rely on

## Active Branch
feature/f304-machine-client-contract-v1-1-part-two, cut from `main` at `4eda924c5`
(the merge commit of pull request 315, F298).

## Scope
F304 (Tier 12, Luna gate A, part two): T002 to T007 carried word for word from F298 — the
semantics a machine client relies on, repaired on the command line that F253's HTTP API will call,
each added to the interface F298's T001 generates from the code, as
`docs/roadmap/features/T12_F304.md` lists them; DECISION F304 D1 fixes the order.

## Do not touch
The approval gate (nothing applied without `--approve`, nothing committed or pushed without its
flag), the transport (F253's), anything in the universe workspace, any time-of-day mechanic.

## Active assumptions
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
