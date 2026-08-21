# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling.

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
R6 builds T001's door: the POST route dispatching `/api/jobs/<job_id>/commands`,
the bearer plus X-Remedy-CSRF pair D2 and D11 rule, request-shape validation
returning typed errors that name the offending field, and BOTH halves of D3's
constant-time comparison — compared as BYTES, because `secrets.compare_digest`
raises TypeError on a non-ASCII str and the query token is attacker-controlled.
A well-formed authenticated command reaches a 501 seam, which is the honest
answer while D4's exposed subset is unbuilt. Contract tests go in
`tests/ui_server/test_command_channel.py` per D1.

## Next Steps
1. R7 replaces the 501 seam with the catalog subset D4 rules, and adds the rate
   limit D9 rules as a typed `ConfigKeySpec`.
2. R8 the nonce store and the audit record per D6, D7 and D8, so that a replay
   returns the ORIGINAL body and a rejection is audited.
3. T003's effect table per D5, the plan-approval extraction landing as its own
   commit; then the client wiring that sends both headers, the integration gate,
   then closure.

## Risks
- R6 changes a live authentication line on the GET door. It is a SPLIT round and
  `tests/ui_server/test_live_state.py` already asserts the `invalid token`
  response the change must preserve.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
