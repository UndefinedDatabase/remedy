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
R20 is round two of DECISION F009 D19 and is purely additive: a new
`tests/ui_server/test_command_dispatch.py` asserts DECISION F009 D18's three
writes from the outside — the published stop request, the nonce record, a retry
audited `replayed` — and the `rejected_effect` path that R19 shipped with no
test reaching it. It also records the R19 verdict and registers R-0639.

## Next Steps
1. `decision.resolve` dispatches to `answer_task_decision` followed by
   `save_job` per DECISION F009 D5, and the 501 seam is gone entirely. That
   round re-examines D18's clause three against a non-idempotent effect, as D18
   requires of it, and migrates the two pins that still expect 501.
2. Then the `command.accepted` SSE event on the F008 stream.
3. Then the queue-only import guard, the per-command side-effect assertions and
   the route-walking 405 test; then the integration gate and closure.

## Risks
- DECISION F009 D18's clause three ruled soft failure for BOTH later writes on
  the strength of `request_stop` being idempotent. `answer_task_decision`
  followed by `save_job` is not obviously so, and D18 already names that as the
  next round's obligation rather than an inheritance.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
