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
R15 lands the two package-level prerequisites of the dispatch and changes the
door not at all. The nonce store refuses an oversize record AT PUBLICATION,
which pays R-0637, and `command_audit.OUTCOMES` gains the `accepted` and
`replayed` tokens the door will write next round. The 501 seam still stands.

## Next Steps
1. `job.stop` dispatches to `safe_points.request_stop`, writing `accepted` and
   publishing the nonce record; the replay audit moves to `replayed`, which
   pays R-0636. `tests/ui_server/test_command_channel.py` migrates its seam
   pins in that same round. `decision.resolve` keeps answering 501.
2. Then `decision.resolve` dispatches and the seam is gone; then the
   `command.accepted` SSE event; then the queue-only import guard, the
   per-command side-effect assertions and the route-walking 405 test; then the
   integration gate and closure. DECISION F009 D17 carries the ordering.

## Risks
- Splitting by command means the door briefly dispatches one exposed id and
  refuses the other with 501. That is honest — `not_implemented` is what the
  audit records for a command this door has not yet dispatched — but the tests
  must assert it deliberately rather than inherit it.
- `accepted` and `replayed` enter the vocabulary a round before any caller
  writes them. `tests/ui_server/test_command_channel.py` still asserts the door
  writes no `accepted`, which stays true and is what keeps the gap honest.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
