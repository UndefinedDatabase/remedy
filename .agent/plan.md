# Plan — Steps 1645-1680: Local Candidate Quality Evaluation v1

## Goal
Evidence-based quality evaluation of candidate-generation OUTCOMES. After a candidate is generated
and run through trust/verification/materialization/approval/apply/test/proof, score whether it was
actually USEFUL (not just safe). Produce model/route scorecards that feed future routing.
Evaluation / reporting / routing-feedback ONLY — no generation, no model calls, no approval/apply/
test/PR/git/mutation.

## Core principle
Evidence, not model confidence, determines quality. No score claims success without linked
proof/test evidence. Candidate quality feeds future routing decisions. No automatic execution.

## Current Step
1672-1680 — code/tests/docs complete; live review + handoff; PR HELD

## Steps
- [x] 1645: mainline reconciliation (generator PR #66 merged; main 3641618; scope 1645-1680)
- [x] 1646-1647: quality models + taxonomy (21 finding codes, 5 severities)
- [x] 1648-1650: evidence inputs (safe summaries) + scoring dimensions + outcome classification
- [x] 1651-1652: idempotent evaluate (fingerprint) + model/route scorecards
- [x] 1653-1654: routing feedback (builder_routing hook) + orchestrator surfacing (progress/feature)
- [x] 1655-1660: CLI evaluate/show/scorecard/report/integrity + catalog + run_contract
- [x] 1661-1664,1678: progress/feature/review-bundle(27)/cockpit
- [x] 1665-1671,1679: tests (24 unit + 7 CLI) + targeted + full pytest once (5927 passed)
- [x] 1670,1677: docs (candidate-quality-evaluation-v1 + model-route-tournament-future + 4 updates)
- [x] 1672-1675: live review + readiness + PR discipline + handoff
- [x] 1680: merge discipline — NO PR unless user explicitly asks

## Product readiness (Step 1673)
Remedy now evaluates generated candidates AFTER THE FACT from durable evidence (trust/verification/
approval/apply/proof) — no score claims success without proof; pending≠completed; rejected→low.
Model/route scorecards feed Builder Routing (repeated poor quality → human review; proof-verified →
raise confidence; unknown never promotes expensive). Still no automatic PR/apply/approval.
Readiness ~85% (evaluation rail complete; tournament harness + external builder sandbox deferred).
Next: External Builder Sandbox v0 OR Model/Route Tournament Harness v0.

## Hard rules
- Evaluation/reporting/routing-feedback ONLY. No generation, no model/provider calls, no approval/apply/test/PR/git/mutation.
- No score claims success without linked proof/test evidence. Score ≤ medium if verification missing;
  not high if human decision unknown; not excellent without proof_verified. Rejected/trust-failed → low.
- Pending approval is NOT completed. Model confidence is NOT truth.
- Routing feedback must NEVER trigger automatic generation.
- Reports = safe IDs / hashes / counts / statuses / evidence refs only. No raw prompt/output/
  candidate/diff/source/stdout/stderr/secrets/tracebacks/abs paths.
- No token/cost invention (unknown stays unknown).
- Every next_safe_action catalog-backed + entity-backed.
- NO PR unless the user explicitly asks (Step 1680).

## Next block
External Builder Sandbox v0 OR Model/Route Tournament Harness v0.
