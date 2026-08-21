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
R13 opens T003 with the half DECISION F009 D5 orders to land first and alone: the
plan approval becomes the package function `resolve_flight_plan_approval` and
`apps/cli/commands/decision.py` becomes its first caller. It is a refactor, so it
carries no endpoint change and no new behaviour. The round also records the R12
verdict.

## Next Steps
1. The effect table itself: the three exposed commands dispatch, the 501 seam is
   retired, DECISION F009 D14's reserved `accepted` outcome is written,
   `publish_nonce_result` gains its door call site with R-0637's bound applied at
   publication, R-0636's replay token moves off `not_implemented`, and the
   `command.accepted` SSE event lands with it.
2. Then the queue-only import guard and the per-command side-effect assertions,
   the route-walking 405 test, the client wiring that sends both headers, the
   integration gate, and closure.

## Risks
- R-0636 and R-0637 are owed by the round that retires the 501 seam, which is the
  NEXT round and not this one: both depend on the publish call site it adds.
- A green approval suite proves nothing on its own if it never reaches the new
  function, so the extraction is gated by a probe as well as by a colour.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
