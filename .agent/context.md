# Context — F287 Provider session continuity across relaunch

## Active Branch
feature/f287-provider-session-continuity, cut from `main` at `7c91c3b69`
(the merge commit of pull request 311, F295 Machine client contract v1).

## Scope
F287 (Tier 3, Luna gate B): a relaunch of an interrupted task resumes the provider sessions it
last used on `claude-cli`, and every other production provider says in the run's evidence that it
did not, as `docs/roadmap/features/T3_F287.md` lists them; DECISION F287 D1 fixes the slices and
their order.

## Do not touch
The persisted session fields and the relaunch hand-over F285 built (DECISION F285 D2); the
fallback-once rule; the prompt, which stays at full context on a resumed call.

## Active assumptions
- Every production change lands with a test that is red without it, proved by the reviewer's
  mutation.
- No test starts a real `claude` process; the CLI is replaced by a recorded stand-in.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
