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
R30 is closure preparation. It records the R29 verdict and the integration-gate
verdict, registers R-0645, repairs docs/agents/integration_gate.md so the base
run's neutralisation check measures the EVENT rather than the outcome — R-0444
recurred at R29 under its own standing rule — and adds the `## Built State`
section that closure precondition 4 requires of the feature file. The build
itself is done: the integration gate found an EMPTY branch-only set.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md, in TWO rounds: the
   evidence job and a FRESH review zip first, then the authored STATUS line,
   the README capability sync and the pull request.

## Risks
- Closure needs TWO rounds, not one: the evidence-and-zip round produces the
  values the STATUS line quotes, and a separate round commits that line. Ending
  right after a verdict strands it (DECISION F085 D9).
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- The closure zip's known blockers are on disk, not in memory: sorted
  `verification_runs[].test_files`, an `output_hash` that is sha256 of
  `stdout_summary` exactly, node ids from `--collect-only`, and no full-suite
  node-id list (STATUS_closure_protocol.md, algorithm step 1).
