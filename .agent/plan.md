# Plan — Steps 1429-1464: Self-Dogfood Execution v0

## Goal
After a human approves a self-dogfood ProposedTask, create + track a bounded
SelfImprovementAttempt that routes work through EXISTING safe systems:
item → ProposedTask → approval → attempt → request package → external candidate →
Provider Trust Gate → materialized pending intent → approval → do continue →
snapshot → apply → test → proof → result. Orchestrator/tracking rail; bypasses NO gate.

## Current Step
1454 — full pytest once (post targeted green)

## Steps
- [x] 1429: Mainline reconciliation + clean branch (PR #60 merged; scope→1429-1464)
- [ ] 1430: Self-execution models (Attempt/Result/State/Phase/Checkpoint/StopReason/Linkage)
- [ ] 1431: Attempt storage (atomic, safe-transition, hashed fingerprint, no raw)
- [ ] 1432: evaluate_self_execution_eligibility (approved self ProposedTask; no dup; review ok)
- [ ] 1433: Branch/main safety gate (refuse mutation-capable on main/master; no git ops)
- [ ] 1434: Attempt state machine (legal transitions; pending≠completed; idempotent)
- [ ] 1435: Build self request package (no FailureArtifact required; safe)
- [ ] 1436: CLI self execute (create/resume attempt → awaiting_external_candidate; real intake cmd)
- [ ] 1437: Generic candidate intake compat (existing intake-repair w/o failure-artifact-id)
- [ ] 1438: Link materialized intent → attempt (intent_pending_approval; idempotent)
- [ ] 1439: Approved self intent → do continue compat (snapshot/test/proof; no overclaim)
- [ ] 1440: CLI self status (read-only)
- [ ] 1441: CLI self reconcile (metadata-only refresh from durable truth; no apply/provider)
- [ ] 1442: Progress Ledger integration
- [ ] 1443: Feature Planner integration (no auto exec)
- [ ] 1444: Review Bundle self_execution_summary.json
- [ ] 1445: Cockpit read-only attempt counts
- [ ] 1446: self report includes execution attempts
- [ ] 1447: RunContract (self_execute_prepare/self_reconcile/self_execution_status)
- [x] 1448: Idempotency tests
- [x] 1449: Redaction tests
- [x] 1450: Architecture guards
- [x] 1451: CLI runtime tests
- [x] 1452: E2E simulated self-improvement test (no real provider/git/main)
- [x] 1453: Documentation (self-dogfood-execution-v0 + cross-links)
- [x] 1454: Targeted tests + full pytest once
- [ ] 1455: Live review
- [ ] 1456: Product readiness update
- [ ] 1457: PR discipline (clean branch; NO PR unless user asks)
- [ ] 1458: Final handoff
- [ ] 1459: Hard completion criteria
- [ ] 1460: Merge recommendation (separate PR; no provider-trust stacking)
- [x] 1461: Future design note (self-dogfood-overnight-future.md)
- [ ] 1462: Optional self integrity gate (read-only)
- [x] 1463: Review Bundle section count update
- [ ] 1464: Final verification (targeted + full suite; record counts; NO PR unless asked)

## Hard rules
- Orchestrator/tracking rail. Bypasses NO existing gate.
- NO code edits, NO direct source_apply/patch_apply, NO apply outside `do continue`.
- NO approval, NO PR/merge, NO main/master mutation, NO git ops, NO direct Job.tasks insertion.
- NO provider/model/network/subprocess/browser. Candidate output goes through existing
  Provider Trust Gate + Materialization (existing intake-repair, no failure-artifact-id needed).
- Mutation-capable phase refused on main/master or unknown branch.
- pending intent ≠ completed; approved ProposedTask ≠ execution success; no overclaim.
- Idempotent by item fingerprint + candidate hash; no duplicate attempts/intents.
- No raw source/diff/stdout/stderr/secrets/tracebacks/absolute private paths.
- Every next_safe_action catalog-backed + references real entities.
- NO PR unless the user explicitly asks (Step 1457/1464).

## Next block
Provider Trust Verification v1 OR Self-Dogfood Overnight v0.
