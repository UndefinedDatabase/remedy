# Context — F058 Model failover chain

## Active Branch
feature/f058-model-failover-chain, from `main` at `4f294374a` (the merge commit of pull request
330, F206).

## Scope
F058 (Tier 3): per-role model failover chains, as `docs/roadmap/features/T3_F058.md` and its
amendment by DECISION F058 D1 state: the chains' key and their hard-rule validation, the failover
walk with its disclosure, the trigger discipline, the sticky cooldown and the session guard.

## Do not touch
The transport retry policy (`packages/orchestration/provider_timeouts.py`), the rate governor's
pacing and routing's class table. Escalation on classified failures is F296's, never this
feature's. A cost in US dollars is never shown to the operator (DECISION amend1007b D7).

## Active assumptions
- Failover is opt-in: a role without a chain behaves exactly as today.
- A link declares its tier; Remedy maps no model name to a tier.
- Every production change lands with a test that is red without it, proved by the reviewer's
  mutation; a structural step is proved by the unchanged tests.

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.
- The functions and files on `docs/system/structure-ledger-v1.md` may not grow.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
