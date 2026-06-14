# Live Review — Steps 1335-1364: Trusted Provider Patch Materialization v0

Reviewer: parallel reviewer
Scope: Materialize ACCEPTED provider candidates into REAL applyable Repair Patch
Intents (approval → do continue → snapshot → apply → test → proof), raw diff/output
PRIVATE only. Must NOT: invoke provider/Ollama/Claude API, network, subprocess,
auto-apply, auto-approve; expose raw diff/source/secrets/tracebacks/abs paths; let a
materialized intent bypass approval or apply automatically. Patch material private
workspace only; intent exposes safe metadata; apply via existing do continue.
Timestamp: 2026-06-14

## Verdict
PENDING — block in progress. Builder constructing provider_patch_material.py +
intake materialization on top of main b38cf94 (PR #57 merged). Hard completion
criteria (Step 1364) gate the verdict.

## Check Matrix (1-15) — to fill
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation | PENDING | branch off clean main b38cf94; PR #57 recorded |
| 2. Material models (no raw fields) | PENDING | |
| 3. Private material storage (0o700/0o600, hashed) | PENDING | |
| 4. Material verification | PENDING | |
| 5. Unified diff → structured patch | PENDING | |
| 6. JSON structured_operations materialization | PENDING | |
| 7. Applyable provider repair intent (real/resolvable/pending) | PENDING | |
| 8. Approve + do_continue compatibility | PENDING | |
| 9. Trust report state updates | PENDING | |
| 10. CLI (material-show / materialize) + catalog + RunContract | PENDING | |
| 11. RepairAttempt linkage + idempotency | PENDING | |
| 12. Integrations (Progress/Feature/Review/Cockpit) | PENDING | |
| 13. Retention docs | PENDING | |
| 14. Redaction | PENDING | |
| 15. Architecture guards | PENDING | |

## Findings — Steps 1335-1364
(none yet)
