# Context — test audit and suite optimization (operator order 2026-10-17)

## Active Branch
feature/test-audit, cut from main `2039a6ae7` (PR 349 merged), checked out in the worktree
`.remedy-wt/test-audit`. Another session runs in parallel; the main checkout and the running
`remedy serve start` are not touched.

## Reference
OpenClaw test-audit skill (SKILL.md, CAMPAIGN.md, references/audit.md), adapted to pytest:
judge a test by its assertions, one owner per contract, keep independent security/API/
persistence/packaging contracts, a mutation shows a keeper goes red.

## Scope
Phase 1 audit + Phase 2 ledger over four owners (routing/planning, Pi execution and guards,
verification and job lifecycle, review evidence and public API); one test-only batch; the fast
lane script and its guards.

## Do not touch
Production behavior, the roadmap queue (F078 stays next), `.agent/STOP`, the supervisor, runtime data, CI stage
budgets.

## Constraints
- Operator, this session: collection only, no suite runs; single owner files may run to prove a
  batch (fake providers only, never concurrent with a real Ollama acceptance run).
- Test load records go to the session scratchpad (`REMEDY_TEST_LOAD_LOG`), not the shared record.
- Commits at most 500 insertions.
