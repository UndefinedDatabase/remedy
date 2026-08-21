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
R11 lands the NONCE half of T002 and closes R10's record. DECISION F009 D15 rules
where the replay lookup sits in the door's order and what may publish a record: a
new `packages/orchestration/command_nonce.py` owns the create-only per-nonce
store, the door validates the nonce as a path component and answers a replay from
the store, and PUBLICATION waits for the round that retires the 501 seam, because
a 501 is not a result worth freezing. The round also registers R-0635 against the
reviewer's own R10 spec and resolves R-0634.

## Next Steps
1. T003's effect table per D5 — the round that finally retires the 501 seam —
   which is also the round that publishes a nonce record and writes the `accepted`
   audit outcome D14 reserved. The `command.accepted` SSE event lands with it.
2. Then the client wiring that sends both headers, the route-walking 405 test and
   the import guard, the integration gate, and closure.

## Risks
- Publication and lookup land in different rounds by D15, so until T003 the
  lookup can only ever miss at the door; its tests seed the store through the
  module's own publish function rather than through a test-only path.
- A nonce becomes a FILENAME, so its character class is the guard: it reuses the
  same `_ID_RE` that already guards the job segment of that directory.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
