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
      → state: awaiting_external_candidate    ← THE RAIL ENDS HERE
      → [human relays request to any external actor; saves the response]
      → (nothing: Remedy has no command that imports the answer)

**Remedy deliberately has no import step here.** F275 T001 deleted the Provider Trust
Gate and its `provider intake-repair` command, which was the one command that read an
external candidate back in, and DECISION F260 D3 maps the external builder to "none,
deliberately". Finding **R-0866** records the loss. A reader looking for the import
step will look exactly here, which is why the absence is written down rather than left
as a gap.

The states after `awaiting_external_candidate` are KEPT and still run for an attempt
whose `patch_intent_id` is already on disk:

    (existing patch intent) → remedy self reconcile <attempt_id>
      → remedy patch approve <job> <intent_id>
      → remedy do continue <job> --intent-id <intent_id>   (snapshot → apply → test → proof)
      → remedy self reconcile <attempt_id>   (state completed when proof verified)

No NEW attempt can acquire such an intent, so this is degraded reachability rather than
dead code.

## Hard boundaries

- **Approved self tasks only** — unapproved/non-self-dogfood tasks are refused.
- **No auto apply** — apply happens only through the existing `do continue`.
- **No self PR/merge, no main mutation** — mutation-capable execution is refused on
  `main`/`master`/unknown branch (branch read from `.git/HEAD`, no subprocess).
- **No approval** — the intent stays pending until a human approves it.
- **No provider/network/subprocess/browser.** Candidate output does not re-enter at
  all: there is no intake command left (R-0866).
- pending intent ≠ completed; no test/proof overclaim; idempotent (one attempt per
  item fingerprint; one intent per candidate hash).

## States

`proposed → approved → request_prepared → awaiting_external_candidate →
candidate_imported → (trust_rejected | trust_needs_review | intent_pending_approval)
→ intent_approved → apply_started → applied → tested_passed/tested_failed →
proof_verified → completed`; plus `blocked` / `evidence_incomplete`.

An attempt that reaches `awaiting_external_candidate` STAYS there: the members after it
are reachable only for an attempt whose patch intent already exists. They are kept
rather than retired because retiring a surviving module's vocabulary is a product
change; R-0866's fix clause routes that question to the DECISION F260 D3 round.

`reconcile` advances state from durable truth only (ProposedTask, patch-intent
approval, proof chain) — never applies, never approves, never runs tests, never calls a
provider. It no longer links a candidate to an attempt, because there is none to link.

## Future

A future [Self-Dogfood Overnight](../archive/self-dogfood-overnight-future.md) could run bounded
self-improvement cycles unattended — only on a non-main branch, no auto-merge, all
outputs through the same apply/test/proof gates.

## See also

- [self-dogfood-v0.md](self-dogfood-v0.md) — the planner.
- [repair-request-builder-v0.md](repair-request-builder-v0.md)
- [do-continue-v1.md](../guides/do-continue-v1.md) — the approval-gated apply path.
