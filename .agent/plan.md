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
R32 clears the block condition this session inherited. It records the R31
verdict, registers as R-0646 and R-0647 the two reviewer-block defects the
closure-candidate carrier held, and empties that carrier in the same round. The
build and its integration gate are done; what remains is closure.

## Next Steps
1. Closure round one: the evidence job and a FRESH review zip, whose values the
   STATUS line quotes.
2. Closure round two: the authored STATUS line, the README capability sync in
   the SAME commit, and the pull request.

## Risks
- Closure needs TWO rounds, not one: ending right after a verdict strands it
  (DECISION F085 D9).
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- The closure zip's known blockers are on disk, not in memory: sorted
  `verification_runs[].test_files`, an `output_hash` that is sha256 of
  `stdout_summary` exactly, node ids from `--collect-only`, and no full-suite
  node-id list (STATUS_closure_protocol.md, algorithm step 1).
