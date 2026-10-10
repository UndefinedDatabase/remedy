# Context — F302 The claude-cli worker's tokens per call: measure, attribute, cut

## Active Branch
feature/f302-claude-cli-tokens, from `main` at `6689c581e` (the merge commit of pull request 320,
F301).

## Scope
F302 (Tier 3, token economy): what one `claude-cli` call spends before it does any work, measured
from the records, attributed to the sources the worker loads, cut by the configuration Remedy
starts it with, and shown by `remedy stats`, as `docs/roadmap/features/T3_F302.md` lists them;
DECISION F302 D1 fixes the order.

## Do not touch
Which model a task class is routed to (F110, F296). The reviewer's independence from the builder.
The approval gate. A cost in US dollars is never shown to the operator (DECISION amend1007b D7).

## Active assumptions
- The data root is read only through Remedy's own commands; `.claude/settings.json` closes it to
  every agent of the loop.
- A cut that makes a builder worse is no cut; each source switched off keeps a key that turns it
  back on.
- Every production change lands with a test that is red without it, proved by the reviewer's
  mutation; a structural step is proved by the unchanged tests.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.
- `packages/orchestration/pingpong_provider.py`, `pingpong_loop.py`, `config.py`,
  `token_ledger.py` and `apps/cli/command_catalog.py` are on the structure page and may not grow.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
