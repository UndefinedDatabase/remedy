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
R29 records the R28 verdict, registers R-0644 against the reviewer's own R28
block and appends the dated correction DECISION F009 D25's route inventory
needs, then runs the integration gate per docs/agents/integration_gate.md: the
full suite on this branch, the full suite at the merge base `ce49348b` in a
throwaway worktree with `apps/ui` build parity restored, and a per-id
attribution of every difference in both directions. T001, T002 and T003 are
built and verified; this is the last gate before closure.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md, in TWO rounds: the
   evidence job and a FRESH review zip first, then the authored STATUS line and
   the pull request.

## Risks
- Closure needs TWO rounds, not one: the evidence-and-zip round produces the
  values the STATUS line quotes, and a separate round commits that line. Ending
  right after a verdict strands it (DECISION F085 D9).
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- A reproducible branch-only failure coupled to feature code is a BLOCKER, and
  its fix is its own reviewer-gated round (integration_gate.md step 4).
