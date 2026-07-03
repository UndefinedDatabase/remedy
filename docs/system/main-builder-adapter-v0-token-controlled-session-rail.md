# Main Builder Adapter v0 — Token-Controlled External Session Rail

## Why Remedy needs a main builder adapter

Remedy's overnight mission spine is:

    Mission Contract → Test Failure / Review Finding → Token-Aware Repair Loop →
    **Main Builder Worker** → Candidate Intake → Review → Apply Proof → Re-Test →
    Mission Contract Satisfaction.

The Repair Loop (v1/v2) identifies what needs fixing and tracks whether it is fixed. But
it does not generate fix candidates — that is the builder's job. Remedy needs a controlled
rail for external builder sessions so that:

- The operator can choose which builder to use (Claude Code, Pi.dev, OpenCode, or a generic CLI).
- Remedy can produce a token-aware request package for the chosen builder.
- Builder output is quarantined and untrusted until sandbox intake, trust/quality checks,
  review, apply proof, and re-test gates pass.
- No single provider is hardcoded. All adapter types are replaceable and user-selectable.

## Controlled external session model

A builder adapter session follows this lifecycle:

    1. Adapter selected (from registry; disabled by default; requires operator approval)
    2. Token-aware request package created (minimal context; bounded)
    3. Session record created (metadata only; status: not_started → package_ready)
    4. Operator launches the external builder with the request package
    5. Session status: waiting_for_operator → running (operator marks)
    6. Builder produces output (transcript_ref + candidate_artifact_ref)
    7. Session status: candidate_received
    8. Candidate routed to External Builder Sandbox (quarantine → Trust Gate → Candidate Quality)
    9. Session status: needs_review → completed_intake_only
    10. Repair Loop evaluates: candidate_received ≠ repaired (review/apply/retest gates remain)

Remedy never launches the external builder process itself in v0. The operator does.

## Adapter types

| Kind | Description | Default state |
|---|---|---|
| `claude_code` | Claude Code CLI session | disabled, package_only, requires approval |
| `pi_dev` | Pi.dev web/CLI session | disabled, package_only, requires approval |
| `opencode` | OpenCode CLI session | disabled, package_only, requires approval |
| `generic_external_cli_builder` | Any external CLI builder | disabled, requires approval |
| `fixture_builder` | Deterministic test fixture | enabled only in test/fixture mode |

No adapter is enabled by default. No provider SDK is imported. No secrets or env tokens are stored.

## Token-aware builder request packages

A request package contains:

- Goal summary (safe, redacted)
- Acceptance criteria references (IDs only)
- Context pack reference (from Repair Loop token-aware context pack)
- Safe context summary (no raw logs/diffs/candidates)
- Forbidden actions list
- Token budget summary (from Token Economy)
- Expected output contract (proposed patch only; no apply; no completion claim)
- Route reason (why this adapter was selected)

If the token estimate is unknown, the package requires human decision. If oversized, it requires
compression or human decision. If the adapter is expensive/high-risk/unknown, it requires human
approval.

## External Builder Sandbox intake

Builder output is ALWAYS untrusted. The candidate artifact goes through:

1. External Builder Sandbox quarantine
2. Provider Trust Gate
3. Candidate Quality evaluation
4. Human review
5. Apply proof (existing approval + intent gates)
6. Re-test (bounded safe test runner)

No candidate is applied directly. No candidate is accepted from self-claim.

## No direct mutation

In v0, no adapter is allowed to:
- Write directly to the repository
- Apply patches without approval gates
- Execute commands on the host
- Store secrets or env tokens
- Bypass the External Builder Sandbox intake

`allows_direct_repo_write` is always `false` in v0.
`requires_external_sandbox_intake` is always `true` for non-fixture real adapters.

## No auto-apply

Session completion does not mean the repair is done. The candidate must still pass:
- Candidate Quality evaluation
- Review gate (open findings block)
- Apply proof (human approval required)
- Re-test gate (bounded, failing blocks)

## No provider monopoly

Remedy is a modular Baukasten. This adapter layer does not hardcode any single provider:
- Claude Code is one option among many.
- Pi.dev is one option among many.
- OpenCode is one option among many.
- Generic CLI builders can be added.
- Ollama/local models may handle cheap tasks later (separate adapter, not this block).

All adapters share the same lifecycle, the same intake path, the same trust/quality/review gates.

## User approval / policy gates

- All real adapters require operator approval before first use.
- Expensive/unknown token use requires human decision.
- Adapter selection respects Worker Registry, Route Policy, Token Economy, and Tournament evidence.
- Disabled/blocked adapters cannot be selected or recommended.

## Future: Ollama/local worker relationship

Ollama and local models are separate from main builder adapters. They handle cheap, repetitive,
low-risk tasks when safe and available. Main builder adapters handle hard, high-value work that
justifies the token cost. The Token Economy and Tournament evidence guide this split.

## Future: external memory adapter relationship

MemPalace and external memory remain future external adapters — not Remedy core. This block does
not implement any internal long-term memory, embeddings, or vector DB.

## Anti-goals

This block intentionally does NOT build:
- Real provider/model execution (Claude, Pi, OpenCode, Ollama, cloud)
- Automatic candidate generation by any model
- Auto-apply, auto-approval, or autonomous mutation
- Provider SDK imports or network calls
- Secret/env token storage
- Direct repository writes
- Git automation (PR, push, merge)
- Real rollback restore
- Internal MemPalace/embeddings/vector DB
- UI redesign or MCP activation
- Shell=True or arbitrary command execution
