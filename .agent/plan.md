# Plan — Steps 1537-1572: Provider Trust Verification v1

## Goal
Second-stage verification of UNTRUSTED external candidate output before/during
materialization into pending repair intents. Trust Gate = safe to ingest.
Verification = plausible, relevant, bounded, worthy of becoming a pending intent.
Approval + apply stay separate. No provider/model/patch/test/approval/PR/git execution.

## Core principle
Trust checks SAFE-to-ingest. Verification checks PLAUSIBLE/RELEVANT/BOUNDED/WORTHY.
Accepted ≠ verified ≠ approved ≠ applied. Evidence is truth. Model critique only.

## Current Step
1566-1572 — code/tests/docs complete; live review + handoff; PR HELD

## Steps
- [x] 1537: mainline reconciliation (advisor PR #63 merged; main 50ea930; scope 1537-1572)
- [x] 1538-1539: verification models + finding taxonomy (20 canonical + 6 scanner codes, 4 severities)
- [x] 1540-1546: checks — consistency / failure+self relevance / overclaim / minimality / testability / loop risk / secret-entropy
- [x] 1547: verification decision rules (passed/needs_review/rejected/incomplete)
- [x] 1548-1549: intake/materialization integration + safe report persistence (private report.json)
- [x] 1550-1553: CLI verify/verification-show + catalog + run_contract actions
- [x] 1554: orchestrator integration (recommend verify; escalate needs-review/repeat-rejection)
- [x] 1555: local-advisor critique hook — DEFERRED + documented (forward seam advisor_critique=None)
- [x] 1556-1559: progress/feature/review-bundle(24)/cockpit integrations
- [x] 1560-1565: tests (27 unit + 7 CLI + cockpit + bundle) + targeted + full pytest once (5812 passed)
- [x] 1564,1571: docs (verification-v1 + expensive-builder-routing-v0-plan + 5 updates)
- [x] 1566-1570: live review + readiness + PR discipline + final handoff
- [x] 1572: merge discipline — NO PR unless user explicitly asks

## Product readiness (Step 1567)
External candidates now pass Trust AND Verification before materialization/intent. Unsafe/
unverified accepted candidates create NO intent. Overclaim/unrelated/repeated-failed candidates
are caught. Local advisor can critique only (deferred). Expensive builder routing is now safer
to build next (output safety solved; cost/loop/justification remain). Direct provider execution
still not built. Readiness ~88% (verification rail complete; advisor critique hook + expensive
routing deferred).

## Hard rules
- Unsafe/unverified accepted candidates MUST NOT create pending intents (prefer verify-before-intent).
- No provider/model execution, cloud API, external network, browser, subprocess (except CLI runtime tests).
- No automatic apply/approval/repair-loop/PR/merge/git-commit-gate/background orchestration.
- No provider SDK imports; no shell=True; no dependency upgrades; no MCP; no UI mutation buttons.
- Verification reports = safe summaries only: NO raw provider output/diff/source/stdout/stderr/
  artifact-body/secrets/tracebacks/abs paths.
- Verification cannot approve/apply/test/create PRs.
- Local advisor (if used) = critique only; can only lower confidence / add human-review; cannot pass/reject.
- Overclaim + unrelated + repeated-failed candidates must not pass silently.
- Every next_safe_action exists in command catalog + references real entities.
- NO PR unless user explicitly asks (Step 1572).

## Next block
Expensive Builder Routing v0 OR Automated Candidate Generator Adapter v0.
