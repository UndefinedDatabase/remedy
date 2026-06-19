# Context

## Active Branch
feature/steps-2916-2995-dev-artifact-boundary-v0
(forked from main at f0b6cea after PR #93 merged).

## Scope
Steps 2916-2995: Development Artifact Boundary + Product Truth Sources.
Audit, classify, and guard .agent/live_review.md boundary.
Document product truth sources. Add whitelist-based guard tests.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- No new feature layer, no provider execution
- No auto-apply/PR/merge, no shell=True, no provider SDK
- Legacy development reads are classified and whitelisted
- New product paths must not introduce live_review.md dependency
