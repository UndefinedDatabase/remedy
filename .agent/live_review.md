# Live Review — Steps 1717-1756: Worker Registry + User-Selectable Route Policy v0

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict, protocol §5)
Scope: Worker Registry + WorkerSpec metadata model + built-in worker specs + User-Selectable Route
Policy + token/cost/risk metadata scoring + routing recommendation integration + CLI visibility +
command catalog/run-contract entries + progress/feature/review/cockpit safe surfacing + integrity +
docs/tests. METADATA + POLICY ONLY — no execution. Must NOT: call Ollama/cloud/provider/network/
browser, execute workers, run a model/route tournament, implement MemPalace/memory, auto-apply/
approve/test/repair, automate git/PR, redesign UI, or activate MCP. Remedy stays a modular Baukasten:
workers/models replaceable, routes user-selectable, local/Ollama preferred for cheap-safe tasks,
expensive routes need justification, token reduction first-class, no provider monopoly, no worker
output trusted without verification. NO PR unless user asks.
Timestamp: 2026-06-15

## Verdict (reviewer-owned)
PENDING — block just started. New branch `feature/steps-1717-1756-worker-registry-route-policy-v0`
off clean merged main `a290238` (PR #68 merged External Builder Sandbox v0; reviewer closure PASS
@ e243eb2). Zero block commits (`git log main..HEAD` empty). No code to verdict yet. Merge-ready
CANNOT be claimed while this verdict is PENDING.

## Check Matrix (1-10)
| Check | Status | Note |
|---|---|---|
| 1. Mainline closure (Ext Builder Sandbox reviewer PASS; fresh branch after merge; no pre-closure work) | PASS | branch off a290238 (PR #68 merged); 0 drift commits |
| 2. WorkerSpec safety (bounded fields; no secrets/keys/raw prompts/abs paths; disabled unselectable; unknown≠truth) | PENDING | |
| 3. Built-in registry (deterministic; Ollama placeholder/metadata-only; external→package-create; no provider/network import) | PENDING | |
| 4. RoutePolicy (select/prefer/block; local/Ollama pref; max cost/risk; blocked beats preference; expensive needs justification; never starts work) | PENDING | |
| 5. Builder routing integration (respects policy; next_safe_action catalog-valid; external→package-create; no exec; no provider/model/local call; unknown cost stays unknown) | PENDING | |
| 6. Token economy (estimated bands; no invented pricing; cheap/local metadata-only; high risk not overridden by cheap cost) | PENDING | |
| 7. CLI/catalog/run_contract (worker list/show + route-policy; safe JSON; safe invalid-id errors; catalog entries; read_only/write_metadata only; no may_execute_commands) | PENDING | |
| 8. Progress/Feature/Review/Cockpit (safe summaries; no fake worker-running/Ollama-ready/provider-avail; no mutation buttons; understandable next action) | PENDING | |
| 9. Integrity (detects missing/disabled/blocked selected worker; expensive-w/o-justification; Ollama placeholder claiming exec readiness; unknown-cost-as-cheap; public leak) | PENDING | |
| 10. Architecture guards (no provider SDK/network/subprocess/shell/apply/approve/test/git/PR/Ollama/cloud exec) | PENDING | |
| (tests) Targeted + full suite reported | PENDING | |
| (handoff) Changed-files table present | PENDING | |

## Findings — Steps 1717-1756
(none yet)

Next id: R-0095.

## Reviewer audit log
- PR #68 merged External Builder Sandbox v0 (1681-1716) to main → `a290238`; reviewer closure PASS
  committed @ `e243eb2` (R-0091/R-0092/R-0094 resolved, R-0093 refuted). New branch
  `feature/steps-1717-1756-worker-registry-route-policy-v0` off `a290238` (clean merged main).
  `git log main..HEAD` empty → no drift, no block code yet. Check 1 PASS. Awaiting builder commits.
- WATCH: METADATA/POLICY ONLY. WorkerSpec public = bounded safe fields (no secrets/keys/raw prompts/
  abs paths); disabled workers unselectable; Ollama built-in is placeholder/metadata-only (must NOT
  claim executable readiness); external-builder worker maps to `external-builder package-create` rail;
  RoutePolicy blocked-beats-preference + never starts work + user selection cannot override hard safety
  block; token/cost = estimated bands, unknown stays unknown (never "cheap"), high risk not overridden
  by cheap cost; CLI read_only/write_metadata only (no may_execute_commands); no provider/network/
  subprocess/Ollama/cloud exec; routing next_safe_action catalog-valid. All project-facing notes English.
