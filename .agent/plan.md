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
R14 closes this session and writes no production code. It records the R13 verdict
and rules DECISION F009 D16, which cuts the rest of T003 into four rounds and
retires the 501 seam one COMMAND at a time rather than all at once. The plan
approval became the package function `resolve_flight_plan_approval` at R13.

## Next Steps
1. `job.stop` dispatches to `safe_points.request_stop`. That path writes
   DECISION F009 D14's reserved `accepted` outcome, publishes the nonce record
   through `publish_nonce_result` with R-0637's bound applied AT PUBLICATION, and
   moves R-0636's replay token off `not_implemented`. `decision.resolve` keeps
   answering 501 until the round after.
2. Then `decision.resolve` dispatches and the seam is gone; then the
   `command.accepted` SSE event; then the queue-only import guard, the
   per-command side-effect assertions and the route-walking 405 test; then the
   integration gate and closure. DECISION F009 D16 carries the ordering and why.

## Risks
- R-0636 and R-0637 are owed by the round that adds the publish call site, which
  is the FIRST of the four rounds D16 rules and not this one.
- Splitting by command means the door is briefly dispatching one exposed id and
  refusing the other with 501. That is honest — `not_implemented` is exactly what
  the audit records for a command this door has not yet dispatched — but it is a
  state the tests must assert deliberately rather than inherit.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
