# Context

## Active Branch
feature/steps-2716-2835-execution-approval-policy-v0
(forked from main at f7cbc04 after PR #90 merged).

## Scope
Steps 2716-2835: Execution approval policy + policy-gated mission continuation.
Add bounded policy layer for managed execution approval. No auto-apply, no auto-PR, no auto-merge.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
It is NOT part of Remedy's product runtime.
Product code must NOT depend on `.agent/live_review.md`.
For product/runtime truth, use structured Remedy state: run records, ledgers,
review bundles, policy records, execution records, mission records.

## Constraints
- Manual approval remains default
- Policy approval is advanced, disabled by default
- Real provider policy requires explicit operator enablement + confirmation
- Policy grant creates approval metadata only — never executes anything
- No auto-apply, no auto-PR, no auto-merge
- No shell=True, no raw leaks, no secret storage
- Fixture policy for deterministic tests only

## Resource safety
All pytest runs use scripts/remedy_pytest.sh (flock-serialized, timeout-bounded).
No shell=True. No background pytest.
