# Live Review — Steps 1757-1796: Token Economy + Context Budget Optimizer v0

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict).
Scope: token budget profiles + context budget estimates + context pack recommendations + token-economy
decisions + estimate helpers + worker-registry/route-policy + builder-routing read-only integration +
CLI visibility + catalog/run-contract entries + progress/feature/review/cockpit safe surfacing +
integrity + placeholder-readiness hardening + docs/tests. ESTIMATES + METADATA + POLICY ONLY — no
execution. Must NOT: call provider/Ollama/cloud/local model/network/browser/subprocess/shell, execute
workers, sync/claim real provider pricing, run a Model/Route Tournament, implement MemPalace/memory,
auto-apply/approve/test/repair, automate git/PR, redesign UI, or activate MCP. All costs/tokens are
ESTIMATED bands unless configured evidence exists; unknown stays unknown (never cheap). Expensive/
unknown/high-risk/placeholder routes always require human approval. NO PR unless user asks.
Timestamp: 2026-06-15

## Verdict (reviewer-owned)
FAIL — reviewed @ commit `729d44c` (branch off merged main `c8f4fa5`, Check 1 met). Three directed
findings all confirmed OPEN: R-0098 (HIGH, unknown context/budget can bypass human approval and be
presented as a cheap/local-ready route — safety-invariant defect), R-0099 (MEDIUM, token economy
integrity does not catch the unknown-budget-no-approval state; its docstring overclaims a sample-
decision check that does not exist), R-0100 (LOW, plan.md stale). One open HIGH + one open MEDIUM →
FAIL; merge-readiness HELD until R-0098/R-0099 fixed (R-0100 for an honest handoff). No FORBIDDEN
execution path found: no provider/Ollama/cloud/network/browser/subprocess/git/tokenizer calls, no
invented exact pricing, workers not executed, route policy does not start work — metadata+policy only.
R-0098–R-0100 status table:
| ID | Sev | Status | Note |
|---|---|---|---|
| R-0098 | high | OPEN | `compute_token_economy_decision` approval set has no term for no_context_inspection / UNKNOWN band / UNKNOWN budget; no-inspection sets est_total=0 → budget UNDER → cheap local worker gets requires_human_approval=False + local_first_recommended=True; reason "Cheap/local route fits the estimated budget" misrepresents unknown context as a budget-fit. Needs: unknown context/band/budget ALWAYS requires_human_approval=True + local_first_recommended=False + reason states unknown + next_action → context inspection. |
| R-0099 | medium | OPEN | `token_economy_integrity` only checks profiles (non-positive budget / exact pricing / abs path / raw). The docstring claims it flags "expensive route without approval, placeholder marked executable, unknown band marked cheap (when a sample is built)" but NO such sample-decision check exists. Misses unknown-band-no-approval, unknown-budget-no-approval, no-inspection+local-first, unknown-as-budget-fit. |
| R-0100 | low | OPEN | plan.md steps 1758-1781 unchecked, only 1757 `[x]`; contradicts context.md "implementation complete". |

REVIEWER-INDEPENDENT verification: targeted `scripts/remedy_pytest.sh` (test_token_economy +
test_token_economy_integration + test_token_cli + test_worker_registry + test_builder_routing +
test_review_bundle) = **166 passed** — but the suite does NOT assert the unknown-context approval floor,
so R-0098 passes (unsafe behavior is "working as coded"; untested). Builder full suite NOT accepted as
merge-evidence while R-0098/R-0099 open. Integrity: `token_economy_integrity` runs (profiles) but has
the R-0099 gaps. Commit reviewed: `729d44c`. MERGE-READINESS: HELD (FAIL). No German project-facing
content observed. NO PR unless user asks.

## Findings — Steps 1757-1796

### R-0098: Unknown context/budget can bypass human approval (presented as cheap/local-ready)
- **Status**: Open
- **Severity**: High
- **Area**: packages/orchestration/token_economy.py (`compute_token_economy_decision`, `routing_token_hint`)
- **Details**: When there is no context inspection (`est.warnings` contains
  `no_context_inspection_available`), the code correctly sets `estimated_token_band = UNKNOWN`, but
  `estimate_context_budget` sets `estimated_total_tokens = 0` (token_economy.py L367-369), so
  `_budget_status(0, profile)` returns UNDER (not OVER), and `over_threshold` is False (requires
  `est_total > 0`). The approval expression
  `requires_human_approval = selection.requires_human_approval or hard or over_threshold or
  budget_status==OVER or not spec` has NO term for the unknown/no-inspection state. So if the route
  policy selects a cheap, low-risk, non-placeholder LOCAL worker, `requires_human_approval=False`, the
  decision falls into the `else` branch with reason "Cheap/local route fits the estimated budget", and
  `routing_token_hint` sets `local_first_recommended = (cost_band in (free,cheap) and not
  requires_human_approval) = True`. Result: unknown context is presented as a cheap/local-ready route
  with no approval — violating "unknown never cheap/safe", "unknown budget can avoid approval", and the
  R-0098 expectation. Metadata-only recommendation (not auto-exec) → High, not Blocker.
- **Evidence**: token_economy.py `compute_token_economy_decision` L582-660 (no unknown-context approval
  term); L367-369 (no-inspection → est_total=0); `routing_token_hint` L678-679
  (`local_first_recommended = cost_band in (free,cheap) and not requires_human_approval`).
- **Expected fix**: Add an unknown floor: if `no_context_inspection_available` in warnings, or
  `estimated_token_band==UNKNOWN`, or `budget_status==UNKNOWN`, then force
  `requires_human_approval=True`, `local_first_recommended=False`, set a reason that states context/
  budget is unknown, and point `next_safe_action` at context inspection / safe estimation (not a
  cheap-ready route). Add regression tests (no-inspection job → approval required, not local-first).
  Then write `Done: R-0098`.

### R-0099: Integrity misses the unknown-budget / no-approval state (docstring overclaims)
- **Status**: Open
- **Severity**: Medium
- **Area**: packages/orchestration/token_economy.py (`token_economy_integrity`)
- **Details**: `token_economy_integrity` only iterates persisted budget profiles and flags
  non_positive_budget, exact_pricing_claimed, absolute_path_in_public, raw_or_secret_in_public. Its
  own docstring claims it flags "expensive route without approval, placeholder marked executable,
  unknown band marked cheap (when a sample is built)" — but there is NO sample-decision check in the
  body. So integrity does not catch: unknown token band + no approval, unknown budget + no approval,
  no context inspection + local-first recommendation, unknown context presented as a budget-fit
  (the R-0098 states).
- **Evidence**: token_economy.py `token_economy_integrity` L712-735 — profile loop only; docstring vs
  code mismatch.
- **Expected fix**: Add an invariant check (in integrity or a tested helper) that fails with safe
  codes when a sample/persisted decision shows unknown band/budget/no-inspection with
  `requires_human_approval=False` or `local_first_recommended=True`, or unknown presented as
  budget-fit; keep positive integrity passing for safe defaults; either implement the docstring's
  promised checks or correct the docstring. Add tests per failure code. Then write `Done: R-0099`.

### R-0100: `.agent/plan.md` is stale (says still building; steps unchecked)
- **Status**: Open
- **Severity**: Low
- **Area**: .agent/plan.md
- **Details**: The implementation is committed and complete @ 729d44c, but plan.md marks steps
  1758-1781 as `- [ ]` (unchecked) and only 1757 as `[x]`, contradicting context.md ("implementation
  complete") and the committed code/tests.
- **Evidence**: `git show 729d44c:.agent/plan.md` lines 18-29 all `- [ ]` despite those files existing.
- **Expected fix**: Update plan.md to check off completed steps and set Current Step to review-closure
  / awaiting reviewer PASS, consistent with context.md + final report + this ledger. Then write
  `Done: R-0100`.

Next id: R-0101.

## Reviewer audit log
- PR #69 merged Worker Registry + Route Policy v0 (1717-1756) to main → `c8f4fa5`; reviewer verdict
  PASS @ `32e480f`. New branch `feature/steps-1757-1796-token-economy-context-budget-optimizer-v0`
  off `c8f4fa5` (clean merged main).
- WATCH: ESTIMATES/METADATA/POLICY ONLY. No provider/Ollama/cloud/local-model/network/subprocess
  execution. No invented exact pricing — all costs/tokens ESTIMATED bands; unknown never cheap.
  Context pack recommendations must exclude protected paths + never dump raw content; missing context
  → warning not fake zero. memory_candidates are SUGGESTIONS only (not persisted memory). Expensive/
  unknown/high-risk/placeholder routes always require human approval (reuse worker_registry
  hard_safety floor). Ollama/cloud placeholders must not appear executable/ready. CLI read_only/
  write_metadata only (no may_execute_commands). next_safe_action catalog-valid. All project-facing
  text English.

## Builder remediation — audit findings R-0098..R-0100 (awaiting reviewer re-check @ new HEAD)
Done: R-0098 - compute_token_economy_decision now has an unknown-context floor: if no_context_inspection_available in warnings OR estimated_token_band==UNKNOWN OR budget_status==UNKNOWN, then requires_human_approval is forced True, the reason states context/budget is unknown (no "fits the estimated budget" claim) and next_safe_action points to `remedy context inspect`; routing_token_hint local_first_recommended is False when approval required. Tests: test_unknown_context_requires_approval, test_unknown_context_hint_not_local_first, test_real_unknown_decision_is_safe_under_audit.
Done: R-0099 - added audit_decision_safety(decision) invariant helper (codes: unknown_token_band_without_approval, unknown_budget_without_approval, no_inspection_without_approval, unknown_context_presented_as_fit) and wired token_economy_integrity(decisions=[...]) to scan decision samples; corrected the docstring to match the actual checks. Tests: test_audit_flags_* (4), test_audit_safe_decision_clean, test_integrity_scans_decisions.
Done: R-0100 - .agent/plan.md reconciled: steps 1757-1781 marked [x], 1782-1796 review-closure in progress, Current Step set to review closure / awaiting reviewer PASS; carried risks preserved; reviewer verdict NOT set by builder.

Builder verification: targeted token/worker/routing/catalog/run_contract/bundle/ledger/planner/cockpit = 381 passed; token + worker registry integrity passed=True. Full pytest = 6111 passed, 8 skipped, 1 deselected (exit 0). NOT claiming merge-ready — reviewer owns verdict at new HEAD.
