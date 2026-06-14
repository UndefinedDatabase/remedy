# Provider-Agnostic Repair Request Builder v0

Given a TestFailureArtifact, Remedy produces a **safe, structured request package**
that can be handed to **any** external worker / model / human. Remedy stays
provider-, worker-, model-, subscription-, IDE-, and account-**agnostic**: external
systems are only example **untrusted candidate generators**, never required
infrastructure.

    remedy repair request <job_id> --failure-artifact-id <id> [--target <label>] [--model <hint>] [--new] [--json]
    remedy repair request-show <job_id> <request_package_id> --json

## Workflow (provider-agnostic)

    FailureArtifact
      → RepairContext (safe)
      → RepairRequestPackage (safe to share)
      → hand to ANY external actor (model / worker / human)
      → external actor returns a candidate OUTSIDE Remedy
      → remedy provider intake-repair … (Trust Gate → Materialization)
      → remedy patch approve …
      → remedy do continue …

This block never calls a provider, model, network, subprocess, browser, or IDE. It
only prepares the request and records an offline candidate-generator record.

## The request package

A package contains safe sections only: problem summary, test-failure summary, linked
entity IDs, relevant file **names** (sensitive names filtered), proof/snapshot status,
constraints, the required response format, forbidden content, and how Remedy will
handle the output. It excludes raw stdout/stderr, source, diffs, artifact bodies,
secrets, tracebacks, and absolute/private paths (all free text is scrubbed).

## Required candidate output contract

The external actor must return EITHER a single JSON object:

```json
{
  "summary": "<one-line safe summary>",
  "target_files": ["relative/path.md"],
  "patch_format": "unified_diff",
  "unified_diff": "<a single unified diff>",
  "rationale": "<why this fixes the failure>",
  "risk_notes": "<risks/uncertainty>"
}
```

OR a single fenced unified diff. Exactly one candidate, relative paths only, no
secrets, no protected files, no claims of having applied or tested.

## Target templates

`--target external` (default), `docs_only`, `test_failure`, `markdown_only`. These add
constraint wording to the request; they are templates, not execution.

## Re-entry is mandatory

External output re-enters ONLY through `remedy provider intake-repair`, where it is
quarantined, trust-validated, and (if accepted + a supported single `.md` shape)
materialized into a pending patch intent. accepted ≠ approved ≠ applied.

## Candidate generator adapter boundary (interface only)

`CandidateGeneratorAdapter` defines `describe()/build_request()/supports_execution()/
execute()`. v0 ships ONLY `ManualCandidateGeneratorAdapter` (offline): it builds a
request package and its `execute()` raises `CandidateGeneratorExecutionUnavailable`.
No network/SDK/subprocess/browser. See
[candidate-generator-adapter-future.md](candidate-generator-adapter-future.md).

## Idempotency

A repeated request for the same (failure, target, model_hint) returns the same
package; pass `--new` to force a fresh one.

## See also

- [provider-trust-gate-v0.md](provider-trust-gate-v0.md) — untrusted intake + trust gate.
- [provider-patch-materialization-v0.md](provider-patch-materialization-v0.md) — accepted candidate → applyable intent.
- [do-continue-v1.md](do-continue-v1.md) — the approval-gated apply path.
- [repair-loop-v1.md](repair-loop-v1.md) — deterministic/fixture repair proposals.
- [self-dogfood-execution-v0.md](self-dogfood-execution-v0.md) — self-improvement attempts route candidate output through the same request/intake flow.
