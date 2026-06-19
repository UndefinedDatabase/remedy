# Context

## Active Branch
feature/steps-3046-3095-runtime-isolation-no-agent-proof-v0.2
(forked from main at ea93771 after PR #95 merged).

## Scope
Steps 3046-3095: Runtime Lane Per-Test Isolation + Real No-Agent Proof v0.2.
Per-node isolation for subprocess-heavy runtime suites. Strengthen no-.agent
functional proofs with real product function calls.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- No new feature layer, no provider execution
- No auto-apply/PR/merge, no shell=True, no provider SDK
- Legacy development reads are classified and whitelisted
- New product paths must not introduce live_review.md dependency

## Resource safety
- All pytest tests must run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path
- Use scripts/remedy_pytest.sh wrapper for bounded execution
