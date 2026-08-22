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
R23 dispatches `decision.resolve` and retires the 501 placeholder. Both exposed
ids now reach a real effect: the answer is written and PERSISTED per DECISION
F009 D21, a declined answer is 409 and `rejected_state`, and DECISION F009 D22
rules the `answer_source` trap and turns the 501 into a guard.

## Next Steps
1. R24 adds the tests DECISION F009 D22's fifth clause defers, purely
   additively: the 200 acceptance path, the 501 guard, and the disk-level
   `decision.resolve` effect assertions in `test_command_dispatch.py` — the
   reads that file already does for `job.stop`. Until it lands, `save_job`
   running and the accepted body's `decision_id` are asserted by nothing.
2. Then the `command.accepted` SSE event on the F008 stream.
3. Then the queue-only import guard, whose allowed set includes `save_job`
   because DECISION F009 D5's own effect mapping names it; then the
   route-walking 405 test; then the integration gate and closure.

## Risks
- `answer_source` is a two-valued field the escalation assumption log COUNTS.
  D22 rules that this door must NOT pass its own source into it, which is the
  opposite of D20's rule for `request_stop`; a later round that generalises one
  to the other silently drops answers from both tallies.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
