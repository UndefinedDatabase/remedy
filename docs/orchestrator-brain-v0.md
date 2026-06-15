# Main Orchestrator Brain v0

The orchestrator reads the current project/job/system state from **safe summaries**,
builds a Situation, generates deterministic Options, scores them, guards against
repeated failed loops, defines a **model routing plan** (never a model call), and
selects exactly **one** structured next-step Decision with rationale.

    remedy orchestrator inspect [--job-id <id>]   # read-only situation
    remedy orchestrator decide  [--job-id <id>]   # one decision (metadata-only trace)
    remedy orchestrator report  [--job-id <id>] [--markdown]
    remedy orchestrator idea "<text>"             # capture a roadmap hint

## Core principle

**LLMs are advisors/builders. The orchestrator is the controller. Evidence is truth.**
v0 is planning/decision only — it executes nothing, calls no model/provider/network,
applies/approves nothing, creates no PR, mutates no code, inserts no `Job.tasks`.

## How it decides

1. **Situation** — gather safe summaries (live review verdict, failures, repair
   attempts, patch intents, provider trust/material, self attempts, budget, ideas).
   Unknown stays unknown; missing/malformed sources become risks.
2. **Options** — deterministic candidate actions, each with a real entity and a
   **catalog-backed** command (fake commands / missing-entity commands are dropped).
3. **Score** — base priority adjusted by review status, budget, risk, and loop guard.
4. **Loop guard** — durable repeated-failure signals (repair failures, trust
   rejections) plus decision-history repetition (same decision + same evidence
   fingerprint) → `allow / warn / block / require_human_review`. No infinite "try again".
5. **Routing plan** — `deterministic_only` (a clear winner), `local_advisor_preferred`
   (close options; a cheap local advisor could critique — future), `external_builder_
   needed` (candidate generation is the bottleneck, evidence complete, budget allows —
   output still only via the Trust Gate), or `human_review_required`.
6. **Decision** — exactly one of: a selected option, `human_review_required`,
   `no_safe_action`, or `evidence_incomplete`, with rationale + rejected alternatives.

## Deterministic first; models later

Deterministic decisioning is preferred whenever evidence is sufficient. The optional
**[Local Model Advisor Adapter v0](local-model-advisor-v0.md)** now provides cheap advisory
critique behind the routing plan (`remedy orchestrator decide --use-local-advisor`) — it can
only lower confidence, add missing-evidence hints, or escalate weak evidence to human review,
never change the deterministic action. Expensive/external builders remain reserved for
justified, targeted candidate generation (see
[expensive-builder-routing-future.md](expensive-builder-routing-future.md)). Model output is
**never truth** and never bypasses approval. The base orchestrator still calls no model.

## Anti-loop

Open blocker/high review forces `human_review_required`. Repeated repair failures or
provider trust rejections block the retry loop. The same decision with no new evidence
escalates warn → block. New evidence resets the guard.

## Future

- [Local Model Advisor Adapter v0](local-model-advisor-v0.md) — **built**: optional cheap
  advisory critique behind the routing plan (loopback-only, advisory-only).
- Provider Trust Verification v1 — stronger verification for untrusted output.
- [Expensive Builder Routing (future)](expensive-builder-routing-future.md).

## See also

- [self-dogfood-v0.md](self-dogfood-v0.md), [self-dogfood-execution-v0.md](self-dogfood-execution-v0.md)
- [provider-trust-gate-v0.md](provider-trust-gate-v0.md), [do-continue-v1.md](do-continue-v1.md)
- [provider-trust-verification-v1.md](provider-trust-verification-v1.md) — the brain now recommends `provider verify` for trust-accepted-but-unverified candidates and escalates needs-review/repeated-rejection to human review (deterministic, catalog-backed).
- [expensive-builder-routing-v0.md](expensive-builder-routing-v0.md) — a local-first routing/policy layer that consumes the brain's signals to decide deterministic vs local-advisor vs local/external candidate generation (planning only; never executes).
