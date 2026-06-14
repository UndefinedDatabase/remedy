# Live Review — Steps 1365-1398: Provider-Agnostic Repair Request Builder v0

Reviewer: parallel reviewer
Scope: From a FailureArtifact build a SAFE provider-AGNOSTIC RepairRequestPackage for
ANY external worker/model/human; external output re-enters ONLY via existing
`provider intake-repair` → Trust Gate → materialization → approval → do continue.
Interface-only candidate generator adapter (no execution). Must NOT: call any
provider/SDK/network/subprocess/browser/IDE; apply; create Patch Intent from request;
leak raw output/source/diff/secrets/tracebacks/abs paths; assume any single provider/
subscription/account/IDE. NO PR unless user explicitly asks (Step 1398).
Timestamp: 2026-06-14

## Verdict
PENDING — block in progress. Builder constructing repair_request_builder.py + CLI on
top of main 871fb8d (PR #58 merged). Hard completion criteria (Step 1395) gate verdict.

## Check Matrix (1-15) — to fill
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation | PENDING | branch off clean main 871fb8d; PR #58 recorded |
| 2. Repair request models (no raw fields) | PENDING | |
| 3. Safe request builder (from RepairContextSummary) | PENDING | |
| 4. Candidate output schema (one candidate; JSON or fenced diff) | PENDING | |
| 5. Request package private storage (atomic, hashed, no abs paths) | PENDING | |
| 6. CLI (request / request-show) + catalog + RunContract | PENDING | |
| 7. Candidate generator adapter boundary (no execution) | PENDING | |
| 8. External generator record + RepairAttempt linkage + idempotency | PENDING | |
| 9. Import guidance (exact human steps; no fake automation) | PENDING | |
| 10. Integrations (Progress/Feature/Review/Cockpit) | PENDING | |
| 11. Request quality | PENDING | |
| 12. Redaction | PENDING | |
| 13. Architecture guards (no provider/network/subprocess/apply/intent) | PENDING | |
| 14. Request→intake E2E (simulated; no real provider) | PENDING | |
| 15. Provider-agnostic language audit | PENDING | |

## Findings — Steps 1365-1398
(none yet)
