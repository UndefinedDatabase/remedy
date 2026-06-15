# Plan — Steps 1573-1608: Expensive Builder Routing v0

## Goal
Local-first, budgeted, anti-loop ROUTING/POLICY for *when* Remedy should use deterministic
logic, local advisory, local candidate generation, or expensive external builder generation.
Routing/policy/planning ONLY — no execution, no provider/cloud calls, no candidate generation,
no intent/ProposedTask creation. May define future adapter contracts, budgets, decision records.

## Core principle
LLMs advise or build candidates. The orchestrator controls. Evidence is truth. Local first when
useful. Expensive builders only when targeted, budgeted, and bounded. No loops.

## Current Step
1603-1608 — code/tests/docs complete; live review + handoff; PR HELD

## Steps
- [x] 1573: mainline reconciliation (verification PR #64 merged; main d22e1dd; scope 1573-1608)
- [x] 1574-1575: routing models + policy (tiers, budget, risk, evidence, stop reasons)
- [x] 1576-1577: routing inputs (safe summaries) + candidate-generation need detector
- [x] 1578-1579: local-first decision rules + expensive builder justification codes
- [x] 1580-1581: budget model + loop governor integration
- [x] 1582-1583: routing decision selector + safe trace persistence (idempotent)
- [x] 1584-1587: CLI decide/report + catalog + run_contract actions
- [x] 1588-1591: orchestrator / local-advisor / verification / self-dogfood integration (consumed by selector)
- [x] 1592-1595: progress / feature / review-bundle(25) / cockpit integrations
- [x] 1596-1602: tests (18 unit + 7 CLI + bundle/cockpit) + targeted + full pytest once (5846 passed)
- [x] 1601: docs (expensive-builder-routing-v0 + 4 updates)
- [x] 1603-1606: live review + readiness + PR discipline + handoff
- [x] 1608: merge discipline — NO PR unless user explicitly asks

## Product readiness (Step 1604)
Remedy can now DECIDE when builder help is justified: deterministic-first, local-advisor before
expensive, local/external candidate generation only when targeted + budgeted + bounded + trust/
verification available + low loop risk. Local-first + anti-loop routing exists. Expensive builders
are STILL NOT executed (routing produces a plan/trace, never a call). Readiness ~85% (routing rail
complete; actual local/external candidate generators deferred). Next: Automated Local Candidate
Generator Adapter v0 OR External Builder Adapter / Provider Execution Sandbox v0.

## Hard rules
- Routing/policy/planning ONLY. No routing result executes anything; none creates Patch Intents/ProposedTasks.
- No external provider/cloud execution, no automated candidate generation, no network, no browser, no subprocess (except CLI runtime tests), no provider SDK.
- No auto apply/approval/repair-loop/PR/merge/git-commit-gate/background orchestration/UI mutation/MCP/dep upgrades.
- External builder NEVER recommended without: request package ready + Trust Gate available + Verification available + budget allowed + loop risk not high + no pending approval/intent.
- Local first; deterministic first; local advisor before external builder; no repeated expensive route without new evidence.
- Unknown cost stays unknown and BLOCKS external by default. Local unavailable does NOT imply external allowed.
- No raw prompt/response/source/diff/stdout/stderr/artifact-body/secrets/tracebacks/abs paths in any surface.
- Every next_safe_action catalog-backed + entity-backed.
- NO PR unless the user explicitly asks (Step 1608).

## Next block
Automated Local Candidate Generator Adapter v0 OR Provider Execution Sandbox v0.
