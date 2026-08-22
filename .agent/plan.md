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
R19 is round one of DECISION F009 D19: the door dispatches `job.stop` to
`safe_points.request_stop`, answers 200 with the body DECISION F009 D18 rules,
audits a raised effect as `rejected_effect`, pays R-0636 by moving the replay
token to `replayed`, and migrates the seam pins. `decision.resolve` keeps the
501 seam. DECISION F009 D20 rules the two arguments the client does not supply
and records the migration's MEASURED shape, correcting D19 per finding R-0638.

## Next Steps
1. Round two of D19: the effect assertions in a NEW file,
   `tests/ui_server/test_command_dispatch.py` — that the stop request the
   dispatch published exists and carries the door's source, that the nonce
   record holds the body the client received, and that a retry of the same
   nonce is audited `replayed`. Purely additive; it edits no existing test.
2. Then `decision.resolve` dispatches and the seam is gone; then the
   `command.accepted` SSE event; then the queue-only import guard, the
   per-command side-effect assertions and the route-walking 405 test; then the
   integration gate and closure.

## Risks
- `rejected_effect` is written from R19 but no shipped test reaches it; the
  reviewer's own worktree probe did, and round two owes it a permanent test.
- `test_an_audit_writer_that_raises_changes_neither_status_nor_body` submits the
  SAME default nonce in both of its loops, so its second seam call is now a
  REPLAY. R19 moves that site to `replayed` by its own FROM/TO pair.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
