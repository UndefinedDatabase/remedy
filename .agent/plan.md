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
R33 is closure round one. It records the R32 verdict, then builds the two
artefacts the STATUS line quotes: the closure evidence bundle for job
`f009-closure` and a FRESH review zip, both covering the accepted HEAD this
round creates. No STATUS line, no README edit and no pull request happen here.

## Next Steps
1. Closure round two: the authored STATUS `[x]` line and the README capability
   sync in the SAME commit (R-0154), then the pull request.
2. The PR is NOT merged in this session; it merges at the next feature's start
   via the Open PR Gate, which is the operator's manual-review window.

## Risks
- The zip is a closure BLOCKER, not a formality: a PACKAGE_STATUS other than
  READY_FOR_REVIEW stops closure rather than being worked around.
- Two open High findings, R-0495 from F085 and R-0574 from F086, are inherited
  from closed features and are documented risks, not F009 defects. F008 closed
  the same way one feature ago, so the F009 verdict is PASS_WITH_RISKS.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
