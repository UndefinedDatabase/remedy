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
R22 rules DECISION F009 D21 — what `decision.resolve`'s effect is and where it
becomes durable, the re-examination of D18's clause three that D18 names as this
round's obligation, and the refusal that did not raise — and lands the audit
token `rejected_state` one round ahead of its writer. It touches NO door.

## Next Steps
1. R23 edits `packages/orchestration/ui_server.py` alone: `decision.resolve`
   dispatches to `answer_task_decision` followed by `save_job` under D21, the
   501 seam and its `not_implemented` writer go, and the two pins that still
   expect 501 migrate — the absent-args test and the exposed-subset loop's
   `else` branch.
2. Then the `command.accepted` SSE event on the F008 stream.
3. Then the queue-only import guard, the per-command side-effect assertions and
   the route-walking 405 test; then the integration gate and closure.

## Risks
- D21 rules `save_job` to be PART of the effect rather than a post-effect write,
  which is the substantive difference from `job.stop`: the answer is durable
  only after it returns. A round that treated it as D18's third write would
  answer 200 for an answer no later reader can find.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
