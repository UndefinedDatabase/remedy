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
R9 closes this session. It registers R-0634 and records the R8 verdict, and it
writes no production code. IT IS DECLARED AS A FIFTH ROUND AGAINST A STATED
FOUR-ROUND CAP: the reviewer's own red-proof of R8 removed the lock that
`test_concurrent_callers_never_oversubscribe_one_budget` names and measured the
test green ten times out of ten, so the suite carries a thread-safety claim
nothing verifies. That finding existed only in the reviewer's session, and a
finding that is not on disk when a session ends is lost.

## Next Steps
1. R10 the nonce store and the audit record per D6, D7 and D8 — a replay returns
   the ORIGINAL body, and every refusal this door already makes, the 429
   included, becomes an audited rejection. R-0634's repair is small and belongs
   to whichever round next touches `tests/ui_server/test_command_channel.py`.
2. T003's effect table per D5 — the round that finally retires the 501 seam —
   with the plan-approval extraction landing as its own commit.
3. Then the client wiring that sends both headers, the integration gate, and
   closure.

## Risks
- The rate limiter's lock is CORRECT and is not the defect; R-0634 is about the
  test's claim, so no production change is owed and none may be made in its name.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
