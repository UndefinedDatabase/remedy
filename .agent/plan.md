# Plan — Steps 1797-1836: Model/Route Tournament Harness v0

## Goal
Evidence-based comparison layer for worker routes. Compare durable evidence (Candidate Quality,
Token Economy, Worker Registry, route policy, trust/verification, approval, proof/test, submission
history) to recommend the best route per task type. No execution — compares + recommends only.

## Core principle
Workers execute. Remedy governs. Tournament compares + recommends, never runs workers. No self-claim
becomes truth; unknown stays unknown; insufficient evidence → no winner; cheap never beats failed
trust/verification. User must always understand the recommendation.

## Current Step
1797 — mainline reconciliation done (PR #70 merged → main 6a81b8f; fresh branch). Building core.

## Steps
- [x] 1797: merge closure (PR #70 → main 6a81b8f; fresh branch) + carried risks + MemPalace deferred
- [ ] 1798: architecture doc (model-route-tournament-harness-v0.md)
- [ ] 1799-1804: model_route_tournament.py core (models; competitor discovery; evidence gathering;
      scoring with hard ceilings; report generation; storage; integrity)
- [ ] 1805-1807: builder_routing read-only tournament hint + CLI (report/show/list/integrity) +
      catalog + run_contract actions (report write_metadata; rest read_only; no may_execute)
- [ ] 1808-1812: progress_ledger + feature_planner + review_bundle section (31) + ui_server cockpit + integrity
- [ ] 1813: user-facing doc (model-route-tournament-user-guide-v0.md)
- [ ] 1814-1815: tests (unit/routing/CLI/bundle/cockpit/integrity) + architecture guards
- [ ] 1816-1817: targeted suites green → full suite once
- [ ] 1818: final handoff report (+ auto-merge on reviewer PASS)
- [ ] 1819-1836: reserved for reviewer findings (R-0101+)

## Hard rules
- NO provider/model/Ollama/cloud/local execution, network, browser, subprocess, shell=True.
- NO new candidate generation, external builder auto-calls, apply/approve/test/git/PR, MemPalace,
  real pricing sync, UI redesign, MCP.
- Evidence absence = insufficient_evidence (never failure); no self-claim becomes truth; unknown stays
  unknown; no fake winner; cheap never beats failed trust/verification.
- Scoring hard ceilings enforced (no proof → not excellent; rejected/unverified → blocked/weak;
  high-risk without approval → blocked; placeholder executable claim → blocked).
- No raw prompts/candidates/diffs/logs/secrets/abs paths in public surfaces. next_safe_action catalog-backed.
- Tests via scripts/remedy_pytest.sh; full once. NO PR unless asked (auto-merge on reviewer PASS).

## Next block
MemPalace Project Memory v0 (only after this block PASS).
