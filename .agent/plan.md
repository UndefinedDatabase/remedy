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
R12 closes this session and writes no production code. It registers R-0636 and
R-0637 — both defects in the reviewer's own R11 specification, found by the R11
review and confirmed by the round's own declared deviations — and records the R11
verdict. T002 is built except for publication, which D15 routes to T003.

## Next Steps
1. T003's effect table per D5 — the round that retires the 501 seam. It is also
   the round that adds the `publish_nonce_result` call site, writes D14's reserved
   `accepted` outcome, moves the replay's audit token off `not_implemented`
   (R-0636) and bounds the published record (R-0637). The plan-approval extraction
   lands as its own commit and the `command.accepted` SSE event lands with it.
2. Then the client wiring that sends both headers, the route-walking 405 test and
   the import guard, the integration gate, and closure.

## Risks
- R-0636 and R-0637 are both owed by the SAME round, T003, and both are one-line
  changes there. Neither is owed a change now, and neither may be paid down
  separately: each depends on the publish call site that round introduces.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
