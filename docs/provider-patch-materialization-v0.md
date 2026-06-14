# Trusted Provider Patch Materialization v0

Turns an **accepted** [ProviderTrustReport](provider-trust-gate-v0.md) candidate into
a **real, applyable** pending Repair Patch Intent — one that flows through the
existing approval-gated path — while the raw provider diff stays private.

    accepted trust report
      → private patch material (.data/workspaces/<job>/provider_patch_material/<id>/)
      → applyable pending Repair Patch Intent (safe metadata only)
      → remedy patch approve <job> <intent_id>
      → remedy do continue <job> --intent-id <intent_id>   # snapshot → apply → test → proof

`remedy provider intake-repair` materializes automatically when the patch shape is
supported. Inspect material with `remedy provider material-show <job> <material_id> --json`.

## accepted ≠ materialized ≠ applied

- **accepted** — passed the trust gate.
- **materialized** — converted into an applyable pending intent (still needs approval).
- **applied** — only after `remedy patch approve` + `remedy do continue`. No auto-apply.
- Materialization never marks anything verified.

## v0 supported shapes (conservative)

The existing apply path (`apply_patch_intent`) is **`.md`-only** (create writes a
markdown file; modify appends a section). So v0 materializes ONLY:

- a **single** target file,
- that file ends in `.md`,
- a **create** or **modify** operation,
- bounded line count,
- no delete, rename, binary, mode change, or generated/lock file.

Anything else (source files, multiple files, delete/rename/binary) →
`unsupported_patch_shape`: the candidate stays **accepted but not materialized**, and
**no intent is created**. (A future Provider-backed Repair Builder will extend the
applyable surface.)

## Privacy

- Raw patch material lives ONLY under the private material dir (`patch.diff`, 0o600;
  dir 0o700) with a `manifest.sha256` and a safe `material.json`.
- Public surfaces (CLI / material-show / trust-show / Progress / Feature / Review
  Bundle / Cockpit) carry counts, states, IDs, and safe target labels — never the
  raw diff, source, secrets, tracebacks, or absolute paths.
- The materialized artifact body uses the apply path's "Proposed Changes:" line
  format (scrubbed), not the raw unified diff.

## Verification

`remedy provider material-show` runs `verify_provider_patch_material`: manifest +
patch present, content hash matches, target paths still safe, trust report still
accepted, single candidate, not revoked.

## Idempotency

Re-intaking the same candidate (same content hash) returns the **same** material and
intent — no duplicate Fix Task / Repair Artifact / Patch Intent.

## Retention (v0)

- Quarantined raw input and patch material are kept in the private workspace
  (`provider_quarantine/`, `provider_patch_material/`) indefinitely in v0.
- There is **no automatic deletion** in v0. Cleanup is manual (remove the workspace
  subdir) until a safe retention policy is implemented.
- The review bundle never includes raw material — only safe summaries.

## See also

- [provider-trust-gate-v0.md](provider-trust-gate-v0.md) — the untrusted-intake trust gate.
- [do-continue-v1.md](do-continue-v1.md) — the approval-gated apply path materialized intents use.
- [repair-loop-v1.md](repair-loop-v1.md) — deterministic/fixture repair proposals.
