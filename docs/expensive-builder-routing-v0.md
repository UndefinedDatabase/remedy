# Expensive Builder Routing v0 (Steps 1573–1608)

A **local-first, budgeted, anti-loop ROUTING / POLICY** layer that decides *when* Remedy should
use deterministic logic, local advisory, local candidate generation, or expensive external
candidate generation. This block is **routing / policy / planning only** — it never executes a
builder/model/provider, never generates candidates, never calls the network, and never creates
Patch Intents or ProposedTasks.

## Core principle

> LLMs advise or build candidates. The orchestrator controls. Evidence is truth. Local first
> when useful. Expensive builders only when targeted, budgeted, and bounded. No loops.

## Routing tiers

| Tier | Meaning |
|---|---|
| `deterministic_only` | A safe deterministic next action exists (approve / continue / verify / propose). No model needed. |
| `local_advisor` | Ambiguity exists and the loopback local advisor has not been consulted for this evidence. |
| `local_candidate_generator` | Local generation is justified + allowed + budgeted (recommended only; not built/executed in v0). |
| `external_candidate_generator` | External generation is justified + explicitly allowed + bounded (recommended only; not executed in v0). |
| `human_review_required` | High risk / unknown evidence / loop guard / blocked generation. |
| `no_safe_route` | No candidate-generation need, or a missing precondition (e.g. no request package). |

## Local-first order (deterministic → local → external)

1. **Deterministic first.** If a concrete deterministic command exists (pending intent → approve,
   approved intent → continue, trust-accepted-unverified → `provider verify`, verification
   needs-review → `verification-show`, unresolved failure with no attempt → `repair propose`),
   that route wins. A **pending approval/intent always beats a new builder route.**
2. **Local advisor before any generation.** If there is ambiguity (or a generation need) and the
   local advisor has not run for this evidence, route to `local_advisor`. The advisor is **never
   looped** — once it has run for the current evidence, routing does not repeat it.
3. **Local candidate generator** — only if policy enables it, a request package exists, no pending
   candidate/intent, budget allows, loop risk is low, and Trust Gate + Verification are available.
4. **External candidate generator** — only if policy explicitly enables it AND all hard
   preconditions hold (below). Unknown cost blocks external by default.
5. **Human review** for high risk / unknown evidence / loop block / generation needed but disabled.

## Expensive builder justification

Deterministic justification codes are attached to the decision: `no_deterministic_fix_available`,
`local_advisor_insufficient`, `repeated_local_failure`, `high_value_failure`,
`request_package_ready`, `trust_and_verification_available`, `budget_available`,
`user_explicitly_requested`, `loop_risk_low`, `human_approval_required_after_generation`.

**An external builder route is NEVER recommended without ALL of:** request package ready,
Trust Gate available, Verification available, budget allowed, loop risk not high, and no pending
approval/intent. `--user-requested` can *justify* an external route but can **never bypass**
trust/verification/budget/loop preconditions.

## Budget model

`compute_budget` reports: local advisor runs remaining (config max − usage), local/external
candidate runs remaining (policy caps − durable attempts), daily external attempts, per-failure
and per-self-item attempts, and `estimated_external_cost`. **Cost is never invented** — it stays
`"unknown"`, and unknown cost BLOCKS external by default unless the policy sets a known
`max_estimated_cost`. *Local unavailable does not imply external allowed.* Note: the
orchestrator's `budget_exhausted` (loop/test-run budget; test runs are 0 by default) is **not**
the builder budget and does not suppress generation need — the dedicated builder budget gates the
local/external routes.

## Loop governor

Uses durable summaries (repair failures, trust/verification rejections, prior routing traces).
Status ∈ `allow | warn | block | human_review_required`. Repeated failure (≥2 rejections / repair
failures, or verification loop risk) → human review. An external route already taken for the
**same evidence fingerprint** → `block` (no repeated expensive route without NEW evidence).

## Persistence

Safe trace at `.data/workspaces/orchestrator/builder_routing/<routing_id>/routing.json` (atomic
0o600, dir 0o700), with a content hash. **Idempotent by evidence fingerprint** unless `--new`.
No raw prompt/response/provider output/source/diff/log/secrets/absolute paths — counts, codes,
tiers, and safe IDs only.

## CLI

- `remedy builder-routing decide [--job-id …] [--failure-artifact-id …] [--self-attempt-id …]
  [--request-package-id …] [--orchestrator-decision-id …] [--user-requested] [--new] [--json]`
  — selects ONE tier and persists a safe trace (metadata-only; never executes/generates).
- `remedy builder-routing report [--job-id …] [--markdown] [--json]` — read-only.

Both `may_mutate_repo=false`, `may_execute_commands=false`. Contract actions
`builder_routing_decide` (metadata) / `builder_routing_report` (read-only), allowed by default,
distinct from any provider/cloud execution.

## Integrations

- **Orchestrator**: routing consumes the orchestrator's durable signals; deterministic routes
  emit the orchestrator's own catalog commands.
- **Local advisor**: recommends the advisor only when untried for the current evidence; never loops.
- **Provider Verification**: trust-accepted-unverified → `provider verify` first; verification
  rejected → revise (not immediate external retry); repeated rejection → human review;
  verification passed + intent pending → approve/reject (not build again).
- **Self-dogfood**: self attempt awaiting candidate → generation route (if allowed); pending
  intent → approve/reject; repeated failure → human review.
- **Progress Ledger / Feature Planner / Review Bundle (`builder_routing_summary.json`, 24→25
  sections) / Cockpit** — safe counts/tiers/status only; no buttons, no raw content.

## What this block does NOT do

No external provider/cloud execution, no automated candidate generation, no network, no browser,
no subprocess (except CLI runtime tests), no provider SDK. No automatic apply/approval/repair-
loop/PR/merge/git-commit-gate/background orchestration/UI mutation/MCP/dep upgrades. No routing
result executes anything or creates a Patch Intent / ProposedTask. Every next action is
catalog-backed and entity-backed.

## Next

- **Automated Local Candidate Generator Adapter v0** — a loopback/local generator whose output
  re-enters via Trust Gate + Verification (still approval-gated).
- **External Builder Adapter v0 / Provider Execution Sandbox v0** — bounded external generation,
  gated behind request package + trust + verification + budget + anti-loop.

See also: [local-candidate-generator-v0.md](local-candidate-generator-v0.md) — when this router
selects the `local_candidate_generator` tier, it emits `remedy local-candidate generate …` as the
next action; that adapter runs only if explicitly enabled + routed and routes output through Trust
Gate + Verification. Routing also consumes
[candidate-quality-evaluation-v1.md](candidate-quality-evaluation-v1.md) feedback: repeated poor
quality for the local-candidate route escalates to human review instead of recommending more
generation (read-only; never triggers generation).
