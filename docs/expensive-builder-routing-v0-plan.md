# Expensive Builder Routing v0 — Design Plan (Step 1571)

A forward-looking design note. **Nothing here is built yet.** This records the constraints a
future "Expensive Builder Routing v0" block must satisfy, given the now-existing Trust Gate +
Verification rails.

## Principle

> The orchestrator controls. Evidence is truth. Local cheap advisor first. Expensive /
> external builders only when targeted and justified. No loops. No direct apply.

## Preconditions (hard order)

An expensive/external builder may be *routed to* only after **all** of these exist for the
targeted failure / self item:

1. A **repair request package** ([repair-request-builder-v0.md](repair-request-builder-v0.md)).
2. The orchestrator has a **deterministic, evidence-backed decision** that an external
   builder is justified (uncertainty / repeated cheap failure), not a model's opinion.
3. The **local advisor** ([local-model-advisor-v0.md](local-model-advisor-v0.md)) was tried
   first where useful (cheap before expensive).

## Output handling (hard order)

Any builder output (cheap or expensive) is UNTRUSTED and must pass, in order:

1. **Trust Gate** ([provider-trust-gate-v0.md](provider-trust-gate-v0.md)) — quarantine +
   safe-to-ingest.
2. **Verification** ([provider-trust-verification-v1.md](provider-trust-verification-v1.md))
   — plausible / relevant / bounded / worthy.
3. **Materialization** → pending intent → **human approval** → `do continue` apply.

No builder output is ever applied, approved, or trusted-as-truth directly.

## Budget / routing / anti-loop requirements

- A **separate, bounded budget** for expensive builder routing (distinct from the local
  advisor budget and the run contract loop/test budgets). Exhaustion blocks routing, never
  deterministic operation.
- **Anti-loop**: never re-route the same request/candidate after repeated trust/verification
  rejection (verification already flags `candidate_repeats_failed_attempt` / loop risk).
  Repeated failure escalates to human review, not another expensive call.
- **Routing decision is deterministic** and catalog-backed; the model never selects itself.

## Explicit non-goals (must stay out of v0)

No direct provider/cloud SDK execution inside Remedy, no automatic apply, no automatic
approval, no automatic PR/merge, no background multi-cycle orchestration, no network/browser/
subprocess for model execution. Routing produces a *plan/request*, not an execution.

## Why now

With Trust + Verification in place, external candidates can be ingested and judged safely, so
the remaining risk in expensive routing is **cost/loop control + justification**, not output
safety. That is what a future Expensive Builder Routing v0 block must own.
