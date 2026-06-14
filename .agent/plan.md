# Plan — Steps 1465-1498: Main Orchestrator Brain v0

## Goal
First "main orchestrator brain": read current project/job/system state from SAFE
summaries, build a Situation, generate deterministic Options, score them, guard
against repeated failed loops, define a model routing PLAN (no model calls), and
select ONE structured next-step Decision with rationale. Planning/decision ONLY —
no execution, no LLM/provider/Ollama, no apply/approve/PR/code mutation.

## Core principle
LLMs are advisors/builders. The orchestrator is the controller. Evidence is truth.

## Current Step
DONE — R-0086 resolved; verdict PASS WITH RISKS; merge-ready; PR HELD (Step 1495/1498)

## Steps
- [x] 1465: Mainline reconciliation + clean branch (PR #61 merged; scope→1465-1498)
- [x] 1466: Orchestrator models (Situation/Decision/Option/EvidenceRef/Risk/Trace/LoopGuard/RoutingPlan/Recommendation/StopReason)
- [x] 1467: build_orchestrator_situation (safe summaries only; unknown stays unknown)
- [x] 1468: Option generator (deterministic; real entities/commands only)
- [x] 1469: Decision scorer (deterministic factors → score/reason codes/confidence)
- [x] 1470: Anti-loop guard (durable summaries; allow/warn/block/require_human_review)
- [x] 1471: Model routing plan v0 (deterministic_only/local_advisor/external_builder/human; no calls)
- [x] 1472: Decision selector (exactly one: option | human_review | no_safe_action | evidence_incomplete)
- [x] 1473: Decision trace persistence (safe, atomic, hashed, no raw)
- [x] 1474: CLI orchestrator inspect (read-only)
- [x] 1475: CLI orchestrator decide (read/metadata-only)
- [x] 1476: CLI orchestrator report (read-only markdown/json)
- [x] 1477: Command catalog (inspect/report read_only; decide read_only/write_metadata)
- [x] 1478: RunContract (orchestrator_inspect/decide/report)
- [x] 1479: User idea intake (orchestrator idea; scrub; classify; metadata-only)
- [x] 1480: Idea-to-option integration (ideas are hints, not truth; dedupe; risky→human review)
- [x] 1481: Progress Ledger integration
- [x] 1482: Feature Planner integration
- [x] 1483: Review Bundle orchestrator_decision_summary.json
- [x] 1484: Cockpit read-only decision summary
- [x] 1485: Orchestrator quality tests
- [x] 1486: Anti-loop tests
- [x] 1487: Model routing tests
- [x] 1488: CLI runtime tests
- [x] 1489: Redaction tests
- [x] 1490: Architecture guards
- [x] 1491: Documentation (orchestrator-brain-v0)
- [x] 1492: Targeted tests + full pytest once
- [x] 1493: Live review
- [x] 1494: Product readiness update
- [x] 1495: PR discipline (clean branch; NO PR unless user asks)
- [x] 1496: Final handoff
- [x] 1497: Hard completion criteria
- [x] 1498: Merge discipline — DO NOT create PR unless user explicitly asks

## Hard rules
- READ-ONLY or metadata-only. NO action execution from the brain.
- NO Ollama/provider/API/network/subprocess/browser; model routing is a PLAN, never a call.
- NO apply/test, NO source_apply/patch_apply, NO approval, NO PR/git/main mutation, NO Job.tasks insertion.
- Model output never truth; never bypass approval; never retry a model indefinitely.
- Anti-loop: no infinite "try again"; repeated failed action → warn/block/human_review.
- Open blocker/high review → human_review_required. Budget exhaustion blocks execution-like options.
- Every next_safe_action catalog-backed + references real entities; no fake commands/missing entities.
- No raw source/diff/stdout/stderr/artifact-body/secrets/tracebacks/absolute private paths.
- NO PR unless the user explicitly asks (Step 1495/1498).

## Next block
Local Model Advisor Adapter v0 OR Provider Trust Verification v1.
