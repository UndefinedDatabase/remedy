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
R8 rate-limits the door per DECISION F009 D9: a typed `ConfigKeySpec` bounds the
commands one token fingerprint may have accepted for one job per minute, and the
excess is refused with 429 rather than made to wait, because an inbound request
is holding a connection. D7's fingerprint — a truncated digest that never carries
the raw token — is introduced here, where it is first used. DECISION F009 D13
rules that the limit is consulted only for a request that would otherwise be
accepted, so a malformed or unexposed command cannot spend a client's budget.
The 429 is NOT yet audited; the audit record is D6 and lands with the nonce store.

## Next Steps
1. R9 the nonce store and the audit record per D6, D7 and D8 — a replay returns
   the ORIGINAL body, and every refusal this door already makes, the 429
   included, becomes an audited rejection.
2. T003's effect table per D5 — the round that finally retires the 501 seam —
   with the plan-approval extraction landing as its own commit.
3. Then the client wiring that sends both headers, the integration gate, and
   closure.

## Risks
- The limiter is in-process state on a threaded server, so it is read and written
  under one lock, and its bucket map must not grow without bound.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
