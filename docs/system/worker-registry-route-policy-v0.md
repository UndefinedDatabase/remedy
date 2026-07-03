# Worker Registry + User-Selectable Route Policy v0 (Steps 1717-1756)

## Why this exists

Remedy must not become a single hardcoded coding agent. It is a modular **Mission Control** layer
for agentic software work:

- **workers execute** — Remedy does not
- **Remedy governs** — it routes, constrains, verifies, and records
- **users choose or constrain** workers and routes
- cheap work should prefer **local / Ollama-capable** routes when safe
- expensive models require **evidence-based justification**
- token reduction and context retention are **first-class product concerns**
- every worker output stays **untrusted until verified**
- **no route silently starts work**

This block adds the registry + policy layer that later enables a Model/Route Tournament, real
Ollama routing, cost-aware planning, and MemPalace-style project memory.

> This block is **metadata, policy, routing recommendations, safety checks, and safe surfacing
> only.** No provider/model/Ollama/cloud execution is added.

## Concepts

### WorkerSpec
A replaceable, provider-neutral description of a worker. Metadata only — no API keys, no secrets,
no endpoints, no raw prompts, no execution. Fields include `kind`, `cost_tier`, `risk_tier`,
`execution_mode`, `token_profile`/`context_profile` (estimated bands), `output_contract`,
`required_permissions`, capability flags, and `default_autonomy_ceiling`.

`WorkerKind`: `fixture`, `local_candidate`, `external_builder`, `ollama_candidate`,
`cloud_candidate`, `human`, `reviewer`, `unknown`.
`WorkerCostTier`: `free`, `cheap`, `standard`, `expensive`, `unknown`.
`WorkerRiskTier`: `low`, `medium`, `high`, `blocked`, `unknown`.
`WorkerExecutionMode`: `metadata_only`, `external_ingress`, `local_model`, `cloud_model`,
`human_in_loop`, `review_only`.

`unknown` is never silently treated as cheap or low — it ranks **worse than** the highest concrete
tier so it can never sneak past a cost/risk ceiling.

### Worker Registry
The set of `WorkerSpec`s. Built-ins (v0): `fixture.worker`, `local.candidate_generator`,
`external.builder_package`, `human.operator`, `reviewer.parallel`, `ollama.placeholder`,
`cloud.placeholder`. Built-ins load deterministically with no provider/network imports.

`ollama.placeholder` and `cloud.placeholder` are **metadata-only placeholders** — disabled,
non-`user_selectable`, and never executed. They exist so future routing can prefer local/Ollama
routes for cheap tasks **once execution is built**; they never claim readiness.

### Route Policy
A per-job, user-selectable constraint set: `user_selected_worker_ids`, `preferred_worker_ids`,
`blocked_worker_ids`, kind allow/block lists, `max_cost_tier`, `max_risk_tier`,
`prefer_local_for_cheap_tasks`, `prefer_ollama_for_cheap_tasks`,
`require_human_approval_for_expensive`, `require_human_approval_for_high_risk`, token/context budget
hints, and an autonomy level. A policy **never starts work** — it only constrains recommendations.

### User-selectable routing
`evaluate_worker_selection(...)` reads the registry + policy and recommends a worker, READ-ONLY.
User selection beats default preference **unless a safety rule blocks it** (disabled worker, blocked
worker/kind, cost/risk ceiling). Disabled and blocked workers are never recommended. Expensive,
high-risk, unknown-cost, or placeholder recommendations set `requires_human_approval`.

### Token / cost awareness
`estimate_token_cost_band`, `estimate_context_fit`, `classify_route_cost`, and
`token_reduction_reason` produce **estimated bands** only. There is no invented exact pricing and no
pricing call. Public surfaces say `estimated`, never `verified`. Unknown cost stays unknown.

### Builder Routing integration
`builder_routing` consults the route policy read-only: if the user blocked/disabled the worker a
route maps to (or selected a different worker), the route escalates to **human review** with a
catalog-valid `remedy route-policy show <job> --json` next action. This is a no-op under the default
policy (which blocks/selects nothing), so existing routing behaviour is unchanged.

## CLI

```
remedy worker registry-list --json
remedy worker registry-show <worker_id> --json
remedy worker registry-integrity --json
remedy route-policy show <job_id> --json
remedy route-policy set <job_id> [--select-worker ID] [--prefer-worker ID] [--block-worker ID]
                                 [--max-cost-tier TIER] [--max-risk-tier TIER]
                                 [--prefer-local-for-cheap-tasks] [--prefer-ollama-for-cheap-tasks]
                                 [--require-human-approval-for-expensive] --json
remedy route-policy evaluate <job_id> --task-type <type> --json
```

All are catalog + run_contract backed. None carry `may_execute_commands`. None execute a worker.

## Relationship to the existing `worker` group

There is a pre-existing `worker` group (`worker_adapters.py` / `worker_recommend.py` /
`worker_queue.py`) that catalogs **providers** (`ollama`, `claude_code`, …) and includes a
`worker run` execution loop. That is a **different taxonomy**. To avoid breaking it, the Worker
Registry is surfaced as `worker registry-*` plus the new `route-policy` group. The two views coexist
intentionally; a future block may unify them.

## Future integration (not built here)

- **Model/Route Tournament Harness** — compare routes by candidate-quality evidence.
- **Real Ollama adapter** — make `ollama.placeholder` executable (loopback-only, config-gated).
- **MemPalace project memory** — long-term context retention feeding route decisions.
- **Context Budget Optimizer** — turn the estimated token/context bands into active budgeting.

## Anti-goals (explicit)

- **No provider/model/Ollama/cloud execution.** No network, browser, subprocess, shell, MCP.
- **No hardcoded provider monopoly** — every worker is a replaceable spec.
- **Worker outputs remain untrusted** — selection never trusts or applies output.
- No auto-apply, auto-approve, auto-test, auto-PR, auto-generation, UI redesign, or Tournament
  Harness in this block.
- Token/cost figures are estimated bands — never presented as billed/verified truth.
