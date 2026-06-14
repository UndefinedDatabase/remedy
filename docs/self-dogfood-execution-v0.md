# Self-Dogfood Execution v0

After a human **approves** a self-dogfood ProposedTask (from
[Self-Dogfood Planner v0](self-dogfood-v0.md)), Remedy creates and tracks a bounded
**SelfImprovementAttempt** that routes the work through the **existing** safe systems.
It is an orchestrator/tracking rail — it bypasses no gate, edits no code, applies
nothing, approves nothing.

    remedy self execute <proposed_task_id> [--job-id <job>]   # metadata-only
    remedy self status [--attempt-id <id>]                    # read-only
    remedy self reconcile <attempt_id>                        # metadata-only
    remedy self integrity                                     # read-only

## Planner vs execution

- **Planner** (`self inspect/plan/propose`) finds improvement items and creates
  ProposedTasks.
- **Execution** (`self execute/status/reconcile`) acts on an **approved** ProposedTask
  by preparing a request and tracking the candidate through the existing gates.

## Flow

    approved ProposedTask (origin self_dogfood, status approved_for_build)
      → SelfImprovementAttempt + safe request package
      → state: awaiting_external_candidate
      → [human relays request to any external actor; saves the response]
      → remedy provider intake-repair <job> --input <file> --provider self_dogfood
          → Provider Trust Gate → materialized PENDING intent
      → remedy self reconcile <attempt_id>   (links the intent; state intent_pending_approval)
      → remedy patch approve <job> <intent_id>
      → remedy do continue <job> --intent-id <intent_id>   (snapshot → apply → test → proof)
      → remedy self reconcile <attempt_id>   (state completed when proof verified)

## Hard boundaries

- **Approved self tasks only** — unapproved/non-self-dogfood tasks are refused.
- **No auto apply** — apply happens only through the existing `do continue`.
- **No self PR/merge, no main mutation** — mutation-capable execution is refused on
  `main`/`master`/unknown branch (branch read from `.git/HEAD`, no subprocess).
- **No approval** — the intent stays pending until a human approves it.
- **No provider/network/subprocess/browser.** Candidate output re-enters only through
  the existing Provider Trust Gate.
- pending intent ≠ completed; no test/proof overclaim; idempotent (one attempt per
  item fingerprint; one intent per candidate hash).

## States

`proposed → approved → request_prepared → awaiting_external_candidate →
candidate_imported → (trust_rejected | trust_needs_review | intent_pending_approval)
→ intent_approved → apply_started → applied → tested_passed/tested_failed →
proof_verified → completed`; plus `blocked` / `evidence_incomplete`.

`reconcile` advances state from durable truth only (ProposedTask, provider trust
report, materialization, patch-intent approval, proof chain) — never applies, never
approves, never runs tests, never calls a provider.

## Future

A future [Self-Dogfood Overnight](self-dogfood-overnight-future.md) could run bounded
self-improvement cycles unattended — only on a non-main branch, no auto-merge, all
outputs through the same trust/apply/test/proof gates.

## See also

- [self-dogfood-v0.md](self-dogfood-v0.md) — the planner.
- [provider-trust-gate-v0.md](provider-trust-gate-v0.md), [repair-request-builder-v0.md](repair-request-builder-v0.md)
- [do-continue-v1.md](do-continue-v1.md) — the approval-gated apply path.
- [local-model-advisor-v0.md](local-model-advisor-v0.md) — optional advisory critique of orchestrator decisions (advisory-only; never changes the gated apply path).
