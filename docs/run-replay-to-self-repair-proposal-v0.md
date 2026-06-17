# Run Replay to Self-Repair Proposal v0

## Problem

Remedy runs produce durable evidence: replay analysis, review bundles, integrity
checks, config diagnostics, managed execution results. When something goes wrong
inside Remedy itself (a degraded review bundle section, a failed integrity check,
a blocking config diagnostic), the operator must manually read the evidence, form
a diagnosis, write a worker prompt, and apply it.

This is slow and error-prone. Remedy already has the evidence — it should be able
to draft a repair proposal for the operator to review.

## Solution

A **self-repair proposal** is a safe, bounded draft that answers:

- What seems broken?
- What evidence proves it?
- Which files might be involved?
- What should the Worker fix?
- What must the Worker not do?
- Which tests must run?
- What counts as done?
- What risks remain?

### Why proposals are not execution

A proposal is a document. It does not:

- Execute code
- Apply patches
- Run tests
- Call providers or models
- Create PRs or commits
- Approve itself
- Modify the repository

The proposal exists only to help a human operator make a faster, better-informed
decision about whether and how to repair Remedy.

### Approval / denial / edit flow

```
  Replay Analysis
        │
        ▼
  ┌─────────────┐
  │    Draft     │  ← Remedy creates this
  └──────┬──────┘
         │
         ▼
  ┌──────────────────┐
  │ Awaiting Operator │  ← Operator sees the proposal
  └──────┬───────────┘
         │
    ┌────┼────┐
    ▼    ▼    ▼
 Approve Deny  Edit
    │    │      │
    │    │      └──→ back to Awaiting Operator
    │    │
    │    └──→ Denied (terminal)
    │
    ▼
 Approved
    │
    ▼
 Convert to Worker Prompt (text only — no execution)
```

Only an approved proposal can be converted to a Worker prompt. Denied proposals
are terminal. Edited proposals return to awaiting-operator status and require
explicit approval.

### How evidence references are used

Proposals contain evidence references, not raw data:

- `replay:<run_id>` — links to a dogfood run replay analysis
- `integrity:<check_code>` — links to a specific integrity check result
- `review_bundle:<section_name>` — links to a degraded bundle section
- `config:<warning_text>` — links to a config diagnostic warning
- `managed_execution:<execution_id>` — links to a failed execution result

The operator can follow these references to inspect the underlying evidence.
Raw logs, prompts, transcripts, candidate bodies, and secrets are never included
in the proposal itself.

### Why raw logs are not exposed

Raw logs may contain:

- API keys or tokens
- Absolute private paths
- User-specific data
- Full tracebacks with implementation details
- Provider prompt/response pairs

Exposing these in a proposal would violate the redaction contract that the rest
of the system enforces. Evidence references provide the same diagnostic value
without the safety risk.

### What is intentionally not automated yet

- **Automatic repair execution**: proposals are text, not actions
- **Automatic approval**: proposals always require operator decision
- **Automatic PR/commit creation**: conversion produces prompt text only
- **Provider/model-assisted diagnosis**: proposals use rule-based analysis only
- **Cross-run correlation**: each proposal is scoped to a single run
- **Priority scoring with ML**: priority is rule-based (error > warning > info)
- **Proposal templates from history**: no learning from past proposals yet
