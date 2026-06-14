# Plan — Steps 1399-1428: Self-Dogfood Readiness + Self-Improvement Planner v0

## Goal
Let Remedy inspect its OWN evidence (reports, findings, risks, failed tests, stale
handoff, missing evidence) and produce structured SelfImprovementItems + a Plan +
ProposedTasks that flow through the EXISTING approval workflow. NOT autonomous self-
modification: no self-apply, no self-merge, no auto-PR, no auto-approval, no main
mutation, no scheduled/background self-run. Planning rail only.

## Flow
project evidence → SelfDogfoodInspection → SelfImprovementItems → SelfImprovementPlan
→ ProposedTasks → human evaluate/approve/materialize (existing flow).

## Current Step
1425 — full pytest once (post targeted green)

## Steps
- [x] 1399: Mainline reconciliation + clean branch (PR #59 merged; scope→1399-1428)
- [x] 1400: Self-dogfood models (Inspection/Item/Plan/Evidence/Source/Risk/Action/Result)
- [x] 1401: Evidence source registry (available|missing|malformed|stale; safe summaries)
- [x] 1402: Live review parser reuse (verdict + open counts; PENDING/FAIL/blocker→blocker)
- [x] 1403: Stale handoff detector (plan/context/verdict/changed-files/test-count/drift)
- [x] 1404: Evidence gap detector (claimed-PASS/full-pytest/readiness/proof/repair chain gaps)
- [x] 1405: Quality debt detector (missing tests/docs/catalog/bundle/cockpit; from registries)
- [x] 1406: Product roadmap item detector (deterministic rules; cite evidence)
- [x] 1407: Item classification (type/priority/confidence)
- [x] 1408: Plan builder (group/dedupe by fingerprint; top 3; bounded; no raw)
- [x] 1409: CLI self inspect (read-only)
- [x] 1410: CLI self plan (read-only)
- [x] 1411: CLI self propose (metadata-only; ProposedTask; item-id/--top N; idempotent)
- [x] 1412: Command catalog (inspect/plan read_only; propose write_metadata)
- [x] 1413: RunContract (self_inspect/self_plan/self_propose_task)
- [x] 1414: ProposedTask integration (origin self_dogfood; existing evaluate/approve/materialize)
- [x] 1415: Progress Ledger integration
- [x] 1416: Feature Planner integration (consume items; no auto exec)
- [x] 1417: Review Bundle self_dogfood_summary.json
- [x] 1418: Cockpit read-only self improvement counts
- [x] 1419: CLI self report (read-only markdown/json)
- [x] 1420: Idempotency tests
- [x] 1421: Redaction tests
- [x] 1422: Architecture guards
- [x] 1423: CLI runtime tests
- [x] 1424: Documentation (self-dogfood-v0)
- [ ] 1425: Targeted tests + full pytest once
- [ ] 1426: Live review
- [ ] 1427: Final handoff
- [ ] 1428: Hard completion criteria

## Hard rules
- READ-ONLY or metadata-only. NO code edits, NO apply, NO approval, NO PR, NO git ops,
  NO direct Job.tasks insertion, NO main mutation, NO scheduled/background self-run.
- Self-generated tasks enter the EXISTING ProposedTask flow (evaluate/approve/materialize).
- NO provider SDK/network/subprocess (except existing CLI runtime tests), NO browser.
- NO raw source/diff/stdout/stderr/secrets/tracebacks/absolute private paths in any surface.
- No arbitrary code scanning — use known summaries/registries only.
- PENDING/FAIL/open blocker/high review status → self-improvement BLOCKER.
- Idempotent: dedupe items + ProposedTasks by stable fingerprint.
- Every next safe action catalog-backed + references real entities.

## Next block
Self-Dogfood Execution v0 OR Provider Trust Verification v1.
