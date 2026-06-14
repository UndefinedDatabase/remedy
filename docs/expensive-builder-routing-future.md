# Expensive Builder Routing (future)

> Design note. **Not built.** Records the intended ordering and the hard guardrails for any
> future expensive/external builder routing, so it is never bolted on unsafely.

## Ordering

1. **Deterministic first.** If the evidence yields a clear next action, no model is used.
2. **Local cheap advisor next.** When options are close or evidence is weak, the optional
   [local model advisor](local-model-advisor-v0.md) may *critique* the deterministic plan
   (loopback-only, advisory-only).
3. **Expensive/external builder last,** and only when candidate generation is the
   bottleneck, the request is **targeted and justified**, and budget allows.

## Hard guardrails for any expensive builder

- **Output is untrusted.** It must enter through the existing **Provider Trust Gate** —
  quarantined privately, parsed, validated, scrubbed — before anything else.
- **No direct apply.** No `source_apply`/`patch_apply`; apply stays behind `do continue`
  with an approved patch intent.
- **No automatic approval, PR, or job creation.** Human approval gates remain.
- **No retry loops.** Bounded attempts; repeated failure → human review, never a storm.
- **Budget/usage policy required**, tracked separately from the local-advisor budget.
- **Output verification required** — never treat builder output as truth, never let it
  become the `next_safe_action` directly.
- **No model output overrides** a contract/budget/review blocker or marks evidence
  complete/success/failure.

## Why this order

Cheap, local, deterministic checks resolve most decisions. The local advisor adds a low-cost
sanity critique. An expensive external builder is the only step that may produce *new*
candidate work — so it is the most tightly gated and the last resort.

## See also

- [local-model-advisor-v0.md](local-model-advisor-v0.md)
- [orchestrator-brain-v0.md](orchestrator-brain-v0.md)
- [provider-trust-gate-v0.md](provider-trust-gate-v0.md)
