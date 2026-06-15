# Model / Route Tournament Harness — Future Design Note (Step 1677)

A forward-looking note. **Nothing here is built.** It records what a future controlled comparison
between candidate generators (local vs local, or local vs external) must satisfy, given the now-
existing [Candidate Quality Evaluation v1](candidate-quality-evaluation-v1.md).

## Idea

Compare two or more generators / models / routes head-to-head on the **same** repair/self request
package, then judge them with the **same** evidence-based machinery — to learn which route/model is
actually best for a given failure or self-improvement type.

## Required invariants

- **Same request package** for every contender (the existing
  [Repair Request Builder](repair-request-builder-v0.md) package — no per-model special-casing).
- **Same Trust Gate + Verification** for every output ([provider-trust-gate-v0](provider-trust-gate-v0.md),
  [provider-trust-verification-v1](provider-trust-verification-v1.md)). No contender skips a gate.
- **Same quality scoring** ([candidate-quality-evaluation-v1](candidate-quality-evaluation-v1.md)) —
  ranking uses evidence (proof-verified > applied > approved > verified > rejected), never model
  confidence.
- **No automatic apply / approval.** A tournament produces a ranked, human-reviewable scorecard;
  humans still approve and `do_continue` still applies.
- **Budget + loop limits required.** Bounded total generations, per-contender caps, and the
  existing anti-loop rules (no repeat on the same evidence fingerprint). Unknown cost blocks
  expensive contenders by default (mirrors Builder Routing).

## Explicit non-goals (any v0)

No direct provider/cloud execution without a sandbox boundary, no background multi-cycle
orchestration, no automatic PR/merge, no browser, no MCP. The harness orchestrates *evaluation*,
not new apply powers.
