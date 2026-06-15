# Plan — Steps 1757-1796: Token Economy + Context Budget Optimizer v0

## Goal
First structured layer to ESTIMATE token cost + context budget, recommend context packs, surface
budget warnings, and integrate with the Worker Registry route policy. Prepares cost-aware planning,
future Ollama routing, and durable project memory. Estimates + metadata + policy only — no execution.

## Core principle
Workers execute. Remedy governs. Token reduction + context retention are core pillars. All costs are
ESTIMATED bands; unknown never cheap; expensive/unknown/high-risk/placeholder routes need human
approval. User never feels lost — every warning understandable + actionable.

## Current Step
1757 — mainline reconciliation done (PR #69 merged → main c8f4fa5; fresh branch). Building core.

## Steps
- [x] 1757: merge closure (PR #69 PASS → main c8f4fa5; fresh branch) + carried risks + Tournament deferred
- [ ] 1758: architecture doc (token-economy-context-budget-optimizer-v0.md)
- [ ] 1759-1762: token_economy.py core (TokenBudgetProfile/ContextBudgetEstimate/ContextPackRecommendation/
      TokenEconomyDecision; estimate helpers; profile storage; context pack recommender)
- [ ] 1763-1764: worker_registry + builder_routing read-only integration (token band/warning/pack rec)
- [ ] 1765-1766: CLI (token budget-show/set/estimate, context-pack recommend, token economy-report) +
      catalog + run_contract actions (read_only/write_metadata; no may_execute)
- [ ] 1767-1772: progress_ledger + feature_planner + review_bundle section + ui_server cockpit +
      integrity + placeholder-readiness hardening
- [ ] 1773: user-facing doc (token-economy-user-guide-v0.md)
- [ ] 1774-1778: tests (unit/routing/CLI/bundle/cockpit/integrity) + architecture guards
- [ ] 1779-1780: targeted suites green → full suite once
- [ ] 1781: final handoff report (+ auto-merge on reviewer PASS)
- [ ] 1782-1796: reserved for reviewer findings (R-0098+)

## Hard rules
- NO provider/model/Ollama/cloud/local-model calls, network, browser, subprocess, shell=True.
- NO apply/approve/reject/test-run/git/PR/merge; NO automatic generation/repair; NO worker execution.
- NO invented exact pricing / pricing sync — estimates labeled `estimated`; unknown never cheap.
- Context pack excludes protected paths + raw content; missing context → warning. memory_candidates
  = suggestions only. Expensive/unknown/high-risk/placeholder routes always require human approval.
- No raw prompts/context/secrets/abs paths in public surfaces. next_safe_action catalog-backed.
- Tests via scripts/remedy_pytest.sh; full once. NO PR unless asked (auto-merge on reviewer PASS).

## Next block
Model/Route Tournament Harness v0 (only after this block PASS).
