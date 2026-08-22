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
R16 closes this session and writes no production code. It records the R15
verdict, resolves R-0637 with the reviewer's own verification, and adds the
three R15 recurrences to the open findings that already describe them — no new
id is minted. The nonce store's publication bound and the `accepted` and
`replayed` audit tokens landed at R15.

## Next Steps
1. Round 2 of DECISION F009 D17: `packages/orchestration/ui_server.py`
   dispatches `job.stop` to `safe_points.request_stop`, writes the `accepted`
   outcome, publishes the nonce record, and moves the replay audit token to
   `replayed`, which pays R-0636. The seam pins in
   `tests/ui_server/test_command_channel.py` migrate in that same round —
   roughly seventeen sites, which is why D17 gave that round its own budget.
   `decision.resolve` keeps answering 501.
2. Then `decision.resolve` dispatches and the seam is gone; then the
   `command.accepted` SSE event; then the queue-only import guard, the
   per-command side-effect assertions and the route-walking 405 test; then the
   integration gate and closure.

## Risks
- The door will briefly dispatch one exposed id and refuse the other with 501.
  That is honest, but the tests must assert it deliberately rather than inherit
  it, and `test_every_exposed_command_reaches_the_seam` loops over both ids and
  must be split when that round lands.
- `accepted` and `replayed` are in the vocabulary with no caller. The door's own
  guard still asserts it writes no `accepted`, which keeps the gap visible.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
