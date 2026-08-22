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
R17 records the R16 verdict, rules DECISION F009 D18 — which splits D17's round
two and fixes the accepted response, the two write-failure rules and the
dispatch-failure token — and lands `rejected_effect` in the audit vocabulary
with its pin. The door is not touched and keeps answering 501.

## Next Steps
1. Round two of DECISION F009 D18: `packages/orchestration/ui_server.py`
   dispatches `job.stop` to `safe_points.request_stop` under D18's ruled order —
   effect, then the `accepted` audit line, then the nonce publication — and pays
   R-0636 by moving the replay token to `replayed`. The seam pins in
   `tests/ui_server/test_command_channel.py` migrate in that same round, and
   `test_every_exposed_command_reaches_the_seam` splits because after it one
   exposed id dispatches and the other still answers 501.
2. Then `decision.resolve` dispatches and the seam is gone; then the
   `command.accepted` SSE event; then the queue-only import guard, the
   per-command side-effect assertions and the route-walking 405 test; then the
   integration gate and closure.

## Risks
- Three vocabulary tokens now exist with no caller. The door's own guard still
  asserts it writes no `accepted`, which keeps the gap visible rather than
  papered over, and it is unedited by this round.
- The seam-pin migration is the largest single piece left: 21 lines of
  `tests/ui_server/test_command_channel.py` mention the literal 501, measured at
  `e7c621fc`, and most reach the door through a helper defaulting to `job.stop`.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
