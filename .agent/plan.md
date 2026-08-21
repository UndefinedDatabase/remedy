# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling, which is derived with
`max` over its line-anchored entries.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI-exposed catalog subset, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through their
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R3 records the R2 verdict and rules the channel's shape as DECISIONS F009 D1
through D9, each grounded in a citation R2 measured rather than in the feature
file's wording: the test home, the auth pair, the token comparison, the exposed
subset, the effect table, the audit record, the fingerprint, the nonce store and
the rate limit. It also amends the one feature-file line naming a directory this
repository does not have.

## Next Steps
1. R4 builds T001's first half against D2, D3 and D4: the POST route, the bearer
   and CSRF checks, the constant-time comparison for both doors, and the typed
   validation errors, with contract tests in `tests/ui_server/`.
2. R5 completes T001 with the rate limit as the typed config key D9 rules, then
   T002's nonce store and audit record per D6, D7 and D8.
3. T003's effect table and queue-only guards per D5, including the plan-approval
   extraction, which lands as its own commit before the endpoint uses it.
4. The integration gate before closure, then the closure round.

## Risks
- D3 touches the EXISTING GET token check, the only line this feature changes
  outside its own new surface. It is declared, it is two lines, and the
  `tests/ui_server/` suite gates it.
- D5's plan-approval extraction is a refactor of `apps/cli/commands/decision.py`;
  AGENTS.md forbids mixing it with feature code, so it is its own commit.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
