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
R18 records the R17 verdict and rules DECISION F009 D19, which cuts the
`job.stop` dispatch into two rounds on a measurement of the pin migration. It
writes no production code. The `rejected_effect` token and DECISION F009 D18's
four rulings landed at R17; the door still answers 501.

## Next Steps
1. Round one of DECISION F009 D19: `packages/orchestration/ui_server.py`
   dispatches `job.stop` to `safe_points.request_stop` under D18's ruled order —
   effect, then the `accepted` audit line, then the nonce publication — pays
   R-0636, and moves every seam pin that must move for the suite to stay green.
   Three of those migrations are uniform byte-string transformations the
   reviewer counted at `6101ca20`: `[0] == 501` 9 times, all `job.stop` through
   `_post_command`; `assert status == 501` 7 times, of which the
   `decision.resolve` one keeps the seam; and `"not_implemented"` 5 times.
2. Round two of D19: the effect assertions in a NEW file — the stop request the
   dispatch published, the nonce record it wrote, and a retry audited
   `replayed`.
3. Then `decision.resolve` dispatches and the seam is gone; then the
   `command.accepted` SSE event; then the queue-only import guard, the
   per-command side-effect assertions and the route-walking 405 test; then the
   integration gate and closure.

## Risks
- Three vocabulary tokens exist with no caller. The door's own guard still
  asserts it writes no `accepted`, unedited, which keeps the gap visible.
- `test_an_audit_writer_that_raises_changes_neither_status_nor_body` submits the
  SAME default nonce in both of its loops, so once the door publishes, its second
  seam call becomes a REPLAY. D19's first round handles that site by itself.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
