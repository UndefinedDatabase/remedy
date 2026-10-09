# Context — F253 Headless API contract: the public HTTP API

## Active Branch
feature/f253-public-http-api-v2, the copy of `feature/f253-public-http-api` with five commit
subjects reworded (DECISIONs F253 D32 and D33); both start from `main` at `1474a65ea` (the merge
commit of pull request 316, F304), and the old branch stays at `83d266f5c` as the record.

## Scope
F253 (Tier 12, Luna gate A, part two): the public HTTP API a machine client uses, as
`docs/roadmap/features/T12_F253.md` and its amendment of DECISION amend1007b D3 list the
operations; DECISION F253 D1 fixes the shape and the order of the slices. The shipped cockpit's
migration onto the API, and the MCP facet, belong to F303.

## Do not touch
The cockpit's existing routes and their token in the query (F303's), the approval gate (nothing
applied without approval, nothing committed or pushed without its flag), the exclusion list
except to grow it, anything bound beyond localhost, TLS or any remote story (F201), and anything in
the universe workspace.

## Active assumptions
- Every route calls the function its command-line twin calls, and a test compares the route's
  answer with the command's `--json` envelope.
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
