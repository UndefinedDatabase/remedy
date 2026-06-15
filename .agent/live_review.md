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
PASS — re-reviewed @ fix commit `32e480f`; all three directed findings RESOLVED + reviewer-verified;
ZERO open Blocker/High/Medium/Low. R-0095 status table:
| ID | Sev | Status | Note |
|---|---|---|---|
| R-0095 | high | RESOLVED @32e480f | `hard_safety_requires_approval(spec)` is an unconditional FLOOR called first in `_requires_approval` (+ candidate.requires_human_justification + integrity): expensive/unknown cost, HIGH/BLOCKED/UNKNOWN risk, EXTERNAL_BUILDER/CLOUD kinds, CLOUD_MODEL, any placeholder ALWAYS require approval regardless of policy flags; flags only add. Tests: test_external_always_requires_approval, test_high_risk_route_cannot_become_no_approval, test_unknown_cost_route_requires_approval |
| R-0096 | medium | RESOLVED @32e480f | integrity flags `high_risk_route_approval_disabled` (hard-safety route + flag disabled) + real `unknown_cost_treated_cheap` (estimate_token_cost_band=="low") replacing the dead check + placeholder_claims_ready retained. Tests: test_high_risk_route_approval_disabled_flagged, test_unknown_cost_selected_treated_cheap_flagged, test_placeholder_claiming_executable_readiness_flagged |
| R-0097 | low | RESOLVED @32e480f | plan.md steps 1717-1739 marked [x], Current Step → review closure; consistent with context.md |

REVIEWER-INDEPENDENT re-verification: inspected fix diff `73d89b0..32e480f` line-level
(hard_safety_requires_approval covers all hard classes; `_requires_approval` calls it first as a floor
so a HIGH-risk external route with both approval flags false still returns True; integrity new safe
codes present); re-ran targeted `scripts/remedy_pytest.sh` (test_worker_registry +
test_worker_route_integration + test_route_policy_cli + test_builder_routing) = **81 passed** incl. all
6 new regression tests. Builder full suite 6033 passed/8 skipped/1 deselected now ACCEPTED (targeted
green, zero open Blocker/High/Medium). No forbidden execution path (metadata+policy only). No German
project-facing content. Commit reviewed: `32e480f`. MERGE-READY. NO PR unless user asks.
(superseded) FAIL @ 73d89b0 — R-0095/R-0096/R-0097 opened; now all resolved.

## Check Matrix (1-10)
| Check | Status | Note |
|---|---|---|
| 1. Mainline closure (Ext Builder Sandbox reviewer PASS; fresh branch after merge; no pre-closure work) | PASS | branch off a290238 (PR #68 merged); 0 drift commits |
| 2. WorkerSpec safety (bounded fields; no secrets/keys/raw prompts/abs paths; disabled unselectable; unknown≠truth) | PASS | bounded safe fields; integrity flags raw/abs-path/disabled-but-selectable; no secrets/raw prompts |
| 3. Built-in registry (deterministic; Ollama placeholder/metadata-only; external→package-create; no provider/network import) | PASS | deterministic built-ins; ollama.placeholder enabled=False metadata-only; external.builder_package → package-create; stdlib only |
| 4. RoutePolicy (select/prefer/block; local/Ollama pref; max cost/risk; blocked beats preference; expensive needs justification; never starts work) | PASS | R-0095 RESOLVED @32e480f — hard_safety approval floor; flags only stricter; blocked-beats-preference; never starts work |
| 5. Builder routing integration (respects policy; next_safe_action catalog-valid; external→package-create; no exec; no provider/model/local call; unknown cost stays unknown) | PASS | routing respects policy; emits strings only; no exec/provider call |
| 6. Token economy (estimated bands; no invented pricing; cheap/local metadata-only; high risk not overridden by cheap cost) | PASS | estimated bands; cost rejection by ceiling not selection; risk ceiling independent of cost |
| 7. CLI/catalog/run_contract (worker list/show + route-policy; safe JSON; safe invalid-id errors; catalog entries; read_only/write_metadata only; no may_execute_commands) | PASS | route-policy + registry commands; read_only/write_metadata; no may_execute (verify in detail) |
| 8. Progress/Feature/Review/Cockpit (safe summaries; no fake worker-running/Ollama-ready/provider-avail; no mutation buttons; understandable next action) | PASS | safe counts/status; no fake readiness; no buttons |
| 9. Integrity (detects missing/disabled/blocked selected worker; expensive-w/o-justification; Ollama placeholder claiming exec readiness; unknown-cost-as-cheap; public leak) | PASS | R-0096 RESOLVED @32e480f — flags high_risk_route_approval_disabled + real unknown_cost_treated_cheap + placeholder_claims_ready + leaks |
| 10. Architecture guards (no provider SDK/network/subprocess/shell/apply/approve/test/git/PR/Ollama/cloud exec) | PASS | stdlib + scrub helpers only; danger scan clean |
| (tests) Targeted + full suite reported | PASS | reviewer targeted post-fix = 81 passed (incl. 6 new regression tests covering approval floor + integrity); builder full 6033 passed/8 skipped/1 deselected ACCEPTED |
| (handoff) Changed-files table present | PASS | plan.md reconciled @32e480f (R-0097); verify changed-files table in final handoff before merge |

## Findings — Steps 1717-1756

### R-0095: High-risk/external route can bypass human approval via user policy flags
- **Status**: Resolved (reviewer-verified @32e480f)
- **Severity**: High
- **Area**: packages/orchestration/worker_registry.py (`_requires_approval`)
- **Details**: `_requires_approval(spec, pol)` gates the approval requirement behind two
  user-settable policy flags. For an enabled, user-selectable, HIGH-risk, non-placeholder route
  (the default built-in `external.builder_package`: enabled=True, user_selectable=True,
  risk_tier=HIGH, kind=EXTERNAL_BUILDER), setting `require_human_approval_for_high_risk=false`
  makes `_requires_approval` skip the high-risk branch, skip the expensive branch (STANDARD cost not
  expensive), skip the placeholder branch, and `return False`. Result:
  `requires_human_approval = false` for a high-risk external route. The flags weaken approval instead
  of acting as a one-way floor. Violates the block invariants "high-risk/external/unknown/placeholder
  routes always require human approval", "policy flags can only make approval stricter, never weaker",
  and "user selection cannot override hard safety". Not an auto-execution path (recommendation is
  metadata-only), so not a Blocker — but a downstream consumer reading `requires_human_approval=false`
  on an external/high-risk route is a real safety-surface defect → High.
- **Evidence**: worker_registry.py `_requires_approval` (returns False when both flags off / single
  flag off for STANDARD-cost HIGH-risk); built-in `external.builder_package` enabled+user_selectable+
  risk_tier=HIGH (worker_registry.py ~L265-275); RoutePolicy fields
  `require_human_approval_for_high_risk`/`_for_expensive` loaded from policy JSON via `bool(d.get(...))`.
- **Expected fix**: Make a mandatory approval FLOOR independent of policy flags: any route that is
  external-builder / high-risk / unknown-cost / unknown-risk / placeholder ALWAYS sets
  `requires_human_approval=True` (and `requires_human_justification=True`); the policy flags may only
  ADD approval for additional tiers (e.g. medium), never remove the floor. Add a regression test:
  high-risk external route with both approval flags false → still `requires_human_approval=True`.
  Then write `Done: R-0095`.

### R-0096: Integrity does not catch unsafe approval policy / expensive-without-approval
- **Status**: Resolved (reviewer-verified @32e480f)
- **Severity**: Medium
- **Area**: packages/orchestration/worker_registry.py (`worker_registry_integrity`)
- **Details**: `worker_registry_integrity()` flags placeholder_claims_ready, unknown_cost_treated_cheap,
  raw_or_secret_in_public, absolute_path_in_public, disabled_but_user_selectable, selected_worker_missing,
  selected_worker_disabled, worker_selected_and_blocked. It does NOT detect: (a) a persisted policy that
  disables approval for a high-risk/external selected route (`require_human_approval_for_high_risk=false`
  while a HIGH-risk worker is selected) — the R-0095 state; (b) an expensive selected route without
  approval requirement (`require_human_approval_for_expensive=false`) — the code comment claims this is
  "flagged" but no such check exists; (c) the `unknown_cost_treated_cheap` per-spec check
  (`cost_tier==UNKNOWN and cost_tier in _CHEAP_TIERS`) is logically dead (a tier cannot be both), so it
  never fires; (d) `placeholder_claims_ready` EXEMPTS kind OLLAMA_CANDIDATE/CLOUD_CANDIDATE, so an Ollama
  placeholder marked enabled+ready-mode would not be caught.
- **Evidence**: worker_registry.py `worker_registry_integrity` (L922+) — no approval-flag inspection in
  the per-policy loop; comment "expensive selection without approval requirement is flagged" with no
  matching code; dead `unknown_cost_treated_cheap` condition; placeholder check `kind not in
  (OLLAMA_CANDIDATE, CLOUD_CANDIDATE)` exemption.
- **Expected fix**: Add integrity checks that fail with safe codes when a persisted policy selects a
  high-risk/external/unknown route with approval disabled, or selects an expensive route without
  approval/justification, or treats an unknown-cost route as cheap; remove the OLLAMA/CLOUD exemption
  from `placeholder_claims_ready` (or justify it). Keep positive integrity passing for safe defaults.
  Add tests for each new failure code + a passing safe-default case. Then write `Done: R-0096`.

### R-0097: `.agent/plan.md` is stale (says still building; steps unchecked)
- **Status**: Resolved (reviewer-verified @32e480f)
- **Severity**: Low
- **Area**: .agent/plan.md
- **Details**: The implementation is committed and complete @ 73d89b0, but `.agent/plan.md` still
  marks steps 1718-1740 as `- [ ]` (unchecked) and only 1717 as `[x]`, contradicting `.agent/context.md`
  ("implementation complete") and the committed code/tests. Handoff inconsistency.
- **Evidence**: `git show 73d89b0:.agent/plan.md` — lines 19-30 all `- [ ]` (architecture doc, core,
  routing, CLI, integrations, doc, tests, full-suite, handoff) despite those files existing in the commit.
- **Expected fix**: Update plan.md to check off the completed steps and set Current Step to
  review-closure / awaiting reviewer PASS, consistent with context.md + final report + this ledger.
  Then write `Done: R-0097`.

Next id: R-0098.

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

## Builder remediation — audit findings R-0095..R-0097 (awaiting reviewer re-check @ new HEAD)
Done: R-0095 - hard-safety approval floor added (hard_safety_requires_approval): expensive/unknown cost, high/blocked/unknown risk, external-builder + cloud kinds, cloud execution mode, and any placeholder ALWAYS require human approval regardless of RoutePolicy flags; policy flags can only add stricter approval, never weaken it. _requires_approval + candidate.requires_human_justification both route through it. Tests: test_external_always_requires_approval, test_high_risk_route_cannot_become_no_approval, test_unknown_cost_route_requires_approval.
Done: R-0096 - worker_registry_integrity now flags unsafe policies: a hard-safety selected route with the matching approval flag disabled (high_risk_route_approval_disabled), an unknown-cost selected worker treated as cheap/local-safe (unknown_cost_treated_cheap), and replaced the no-op UNKNOWN-in-CHEAP_TIERS per-spec check with a real estimate_token_cost_band=="low" check; placeholder_claims_ready retained. Tests: test_high_risk_route_approval_disabled_flagged, test_unknown_cost_selected_treated_cheap_flagged, test_placeholder_claiming_executable_readiness_flagged.
Done: R-0097 - .agent/plan.md reconciled: steps 1717-1740 marked [x], 1741-1756 marked review-closure in progress, Current Step set to review closure / awaiting reviewer PASS; carried risks preserved; reviewer verdict NOT set by builder.

Builder verification: targeted worker_registry/route-integration/CLI/builder_routing/catalog/run_contract/review_bundle/cockpit = 284 passed; worker registry-integrity passed=True/violations=0. Full pytest = 6039 passed, 8 skipped, 1 deselected (exit 0). NOT claiming merge-ready — reviewer owns verdict at new HEAD.
