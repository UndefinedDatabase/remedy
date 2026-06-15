# Provider Trust Gate + External Repair Intake v0

External model/agent output (Claude / Fable / Sonnet / Opus / Pi / Ollama) is
produced **outside Remedy** and is treated as **untrusted**. This gate takes a
candidate repair from a local file or stdin, quarantines the raw bytes privately,
validates it, emits a safe `ProviderTrustReport`, and — only when accepted —
creates a Repair Artifact + a **pending** Repair Patch Intent.

    remedy provider intake-repair <job_id> --input <path> --failure-artifact-id <id> \
        --provider <name> [--model <name>] [--json]
    remedy provider intake-repair <job_id> --stdin --failure-artifact-id <id> --provider <name>
    remedy provider trust-show <job_id> <trust_report_id> --json

## No provider execution in v0

This block does **not** invoke any provider. No API calls, no Ollama calls, no
model invocation, no network, no subprocess. The only input is text you already
obtained from a model and saved to a file (or piped on stdin).

## Flow

    external model output (file/stdin)
      → private quarantine record (0o700 dir / 0o600 file, hashed, never public)
      → parse/normalize (JSON OR exactly one fenced unified diff)
      → trust validation (secret scan, path safety, patch shape, failure link)
      → safe ProviderTrustReport (findings/counts/IDs only)
      → if accepted: Repair Artifact + ONE pending Repair Patch Intent
      → approval_required → stop

## Accepted ≠ applied

`accepted` means the candidate passed the trust gate and a **pending** intent was
created. It does **not** mean the patch was applied, approved, or verified. Apply
still happens only through the existing approval-gated path:

    remedy patch approve <job_id> <intent_id> --json
    remedy do continue <job_id> --intent-id <intent_id> --json

## Trust decision

| Finding severity present | Trust status |
|---|---|
| blocker or high | `rejected` (no intent) |
| medium (or no parseable patch) | `needs_human_review` (no intent) |
| low only | `accepted` (pending intent created) |

Rejected/needs-review candidates create **no** intent. Unparseable output never
creates an intent.

## What is quarantined vs. exposed

- **Quarantined privately** (never exported): the raw provider output and the raw
  diff/source — under `.data/workspaces/<job>/provider_quarantine/<id>/raw_input.txt`.
- **Exposed publicly** (CLI/trust-show/Progress/Feature/Review Bundle/Cockpit):
  trust status, finding codes/severities, candidate metadata (kind, format, file
  count, hunk/line counts), confidence, safe IDs, the next safe action. No raw
  output, diffs, source, secrets, tracebacks, or absolute paths.

## Findings (taxonomy)

`provider_output_unparseable`, `multiple_patch_candidates`, `raw_secret_detected`,
`protected_path_targeted`, `path_traversal`, `absolute_path`, `unknown_file_target`,
`generated_file_too_large`, `patch_too_large`, `unsupported_patch_operation`,
`deletes_file`, `binary_file_change`, `test_file_only_change`, `docs_only_change`,
`no_failure_link`, `no_repair_attempt_link`, `low_confidence`, `requires_human_review`
(+ input findings: `input_not_found/too_large/binary/nul_byte/empty`).

## Using Claude / Fable / Pi output manually

1. Ask the model for a repair as a single unified diff (or the structured JSON
   form: `summary`, `target_files`, `patch_format`, `unified_diff`, `rationale`,
   `risk_notes`).
2. Save it to a file.
3. `remedy provider intake-repair <job> --input <file> --failure-artifact-id <fa> --provider claude`.
4. If accepted, review with `remedy provider trust-show`, then approve + `do continue`.

## Materialization

An accepted candidate is now **materialized** into a real applyable pending Repair
Patch Intent (v0: single `.md` create/modify) — see
[provider-patch-materialization-v0.md](provider-patch-materialization-v0.md). Accepted
≠ materialized ≠ applied; apply still requires approval + `do continue`.

## Next block

**Provider-backed Repair Builder v0** will wire a real (local-first, gated) provider
builder *behind* this trust gate — the gate stays the boundary, the builder just
produces the candidate instead of a human pasting it.

## See also

- [provider-patch-materialization-v0.md](provider-patch-materialization-v0.md) — accepted candidate → applyable pending intent.
- [repair-loop-v1.md](repair-loop-v1.md) — deterministic/fixture repair proposals.
- [bounded-overnight-executor-v0.md](bounded-overnight-executor-v0.md) — foreground one-step executor.
- [do-continue-v1.md](do-continue-v1.md) — the approval-gated apply path.
- [repair-request-builder-v0.md](repair-request-builder-v0.md) — provider-agnostic repair request package for any external actor (output re-enters via provider intake).
- [self-dogfood-execution-v0.md](self-dogfood-execution-v0.md) — self-improvement attempts reuse this candidate-intake → trust → materialize path.
- [provider-trust-verification-v1.md](provider-trust-verification-v1.md) — **second-stage** check that now runs between trust-accept and materialization; an accepted candidate must also pass verification before any pending intent is created.
