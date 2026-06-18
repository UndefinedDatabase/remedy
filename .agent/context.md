# Context

## Active Branch
feature/steps-2836-2875-approval-policy-closure-v0.1
(forked from main at e083bed after PR #91 merged).

## Scope
Steps 2836-2875: Execution Approval Policy closure + hardening.
No new feature layer. Fix truthfulness, redaction, package loading, token awareness,
denial codes, real-provider confirmation, uses decrement ordering, report visibility.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- Policy grant creates approval metadata only — never executes anything
- No auto-apply/PR/merge, no shell=True, no provider SDK
- Unknown token estimates require manual approval in v0
- Denial codes must be specific, not collapsed
- Public export must redact secrets and private paths

## Resource safety
- All pytest tests must run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path
