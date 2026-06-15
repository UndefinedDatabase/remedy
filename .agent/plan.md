# Plan — Steps 1717-1756: Worker Registry + User-Selectable Route Policy v0

## Goal
Make Remedy a modular Baukasten Mission Control layer: workers are REPLACEABLE specs; the user can
select/constrain routes (workers, cost tier, risk tier, local/Ollama-first preference). This block
is the registry + policy + routing-recommendation + safety + visibility layer that later enables
Model/Route Tournament, real Ollama routing, cost-aware planning, and MemPalace project memory.

## Core principle
Workers execute. Remedy governs. Users choose. Cheap → local/Ollama-first when safe; expensive →
evidence-based justification. Worker output untrusted until verified. No route silently starts work.

## Current Step
1717 — mainline reconciliation done (PR #68 merged → main a290238; fresh branch). Building core.

## Steps
- [x] 1717: merge closure (PR #68 PASS → main a290238; fresh branch) + reconcile existing `worker`
      group collision (registry surfaced as `worker registry-*` + `route-policy`); Tournament deferred
- [ ] 1718: architecture doc (worker-registry-route-policy-v0.md) — anti-goals explicit
- [ ] 1719-1722,1724: worker_registry.py core (WorkerSpec/RoutePolicy + enums + built-ins + storage +
      evaluate_worker_selection + token/cost band scoring)
- [ ] 1723: builder_routing integration (user selection/blocked/disabled/cost/risk/local-Ollama pref;
      recommendation only; catalog-valid next actions)
- [ ] 1725-1726: CLI (worker registry-list/registry-show + route-policy show/set/evaluate) + catalog +
      run_contract actions (read_only/write_metadata; no may_execute)
- [ ] 1727-1731: progress_ledger + feature_planner + review_bundle section + ui_server cockpit + integrity
- [ ] 1732: user-facing route policy doc (worker-route-policy-user-guide-v0.md)
- [ ] 1733-1737: tests (unit/routing/CLI/bundle/cockpit/integrity) + architecture import guards
- [ ] 1738-1739: targeted suites green → full suite once
- [ ] 1740: final handoff report
- [ ] 1741-1756: reserved for reviewer findings (R-0095+)

## Hard rules
- NO provider/model/Ollama/cloud calls, network, browser, subprocess, shell=True.
- NO apply/approve/reject/test-run/git/PR/merge; NO automatic generation/repair; NO worker execution.
- Disabled/blocked workers never recommended/selected. Unknown cost never "cheap".
- Expensive/cloud/unknown route requires human-facing justification.
- local/Ollama preference cannot override safety/missing capability. Ollama/cloud = placeholders.
- No raw prompts/secrets/abs paths/raw model output in any public surface.
- Every next_safe_action catalog-backed + entity-backed. Tests via scripts/remedy_pytest.sh; full once.
- NO PR unless the user explicitly asks.

## Next block
Token Economy + Context Budget Optimizer v0 (or Model/Route Tournament Harness v0 if route evidence
is sufficient) — only after this block PASS.
