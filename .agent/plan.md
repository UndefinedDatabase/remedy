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
R28 closes T003 and records the R27 verdict. Every route `do_GET` dispatches is
walked with POST, PUT and DELETE and answers 405; the job endpoints come out of
`do_GET`'s own dict literal by AST so a new one joins the walk automatically, and
a drift test fails the moment a literal route appears the walk does not know.
With T001, T002 and T003 built, what remains is verification rather than
construction.

## Next Steps
1. The integration gate per docs/agents/integration_gate.md — the full suite,
   once, before closure.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a
   FRESH review zip, the authored STATUS line, and the pull request.

## Risks
- Closure needs TWO rounds, not one: the evidence-and-zip round produces the
  values the STATUS line quotes, and a separate round commits that line. Ending
  right after a verdict strands it (DECISION F085 D9).
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
