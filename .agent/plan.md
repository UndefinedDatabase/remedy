# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 6, round 22.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step
All six closure preconditions are MET (round 21). This round executes
STATUS_closure_protocol.md Algorithm steps 1 (evidence job) and 2 (review
zip) only — it does NOT close the feature: no STATUS `[x]` edit, no README
sync, no `consumed_by` edit, no PR. The evidence bundle is built via
`packages.orchestration.job_evidence.create_manual_completion_bundle`
(`job_id=f106-closure`) over 8 scoped verification suites (244 tests, all
passing), then the review zip via `scripts/make_review_zip.sh`. Neither
the evidence dir nor the zip is committed (STATUS_closure_protocol.md
convention) — only this round's `.agent/` bookkeeping is.

## Next Steps
1. Round 23: reviewer authors the STATUS line from this round's real
   package filename/SHA-256/path, and the closure commit (STATUS.md,
   README.md, `scripts/self_use_queue.json` SU-003 `consumed_by=F106`,
   final `.agent/` state) plus the DECISION F106 D2 candidates.md-only
   follow-up commit.
2. Then: the AGENTS.md PR workflow.
3. Merge is deferred to the next feature's Open PR Gate, per the closure
   algorithm's own rule.

## Risks
- R-0761 (Medium, OPEN) carries into the closure verdict as PASS WITH
  RISKS, documented, not a blocker.
