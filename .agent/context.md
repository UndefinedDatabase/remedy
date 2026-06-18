# Context

## Active Branch
feature/steps-2876-2915-package-truth-runtime-closure-v0.2
(forked from main at 0bc5a4f after PR #92 merged).

## Scope
Steps 2876-2915: Package path truth fix + runtime lane closure.
Fix _load_package() to use main_builder_adapter/packages.
Add unmocked integration tests. Propagate specific denial codes.
Guard .agent/live_review.md artifact boundary.

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
