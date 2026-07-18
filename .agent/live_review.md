# Live Review — Steps 12361-12560 — F012 hardening round 24 (closed gate schemas + snapshot-only manifest)

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (6 closed-schema/snapshot findings), awaiting re-review (NOT accepted).

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Raw-stream format unchanged; F001 timeout/retry unchanged; F010/F011 not
weakened. The gate matrix and manifest construction are additive-hardened; no manifest field was
removed.

External review of `remedy-review-20260718-155415-READY_FOR_REVIEW.zip` (SHA
`40f1fd24679288515a5229c3f950a5fe7d5a81750530e0d1dc3ca53ca5093e16`, Evidence job
`14f211210d044bfb`, linked prior `ff07e91816a146e1`, HEAD `2f19a66`) returned SIX findings. Fixed as
one bounded closure block.

- **F1** — each READY gate is validated by an EXACT recursive schema: a CLOSED allowed-field set
  (unknown field BLOCKS), version closed to {"1.0.0"}, and the complete internal truth of the
  fresh/artifact/change/runtime gates (per-field + per-check).
- **F2** — the final_verifier's embedded gate verdicts must EQUAL the packaged gate verdicts; all its
  blocking fields must be clear; its own commit-readiness view (a distinct field from the packaged
  commit gate's verdict) must be a not-ready, non-auto-promotable state.
- **F3** — complete fresh/artifact/change/runtime semantics (nested freshness+validity, every
  required_artifact true, stale_apply_proofs=[], each runtime check found/not-missing/known
  type/unique path-safe id + count coherence).
- **F4** — the commit_execution gate is an EXACT derived document: gate_checks are exactly the five
  packaged verdicts, non_pass_gates is the derived set, blocked_gates=[], promote_ready=false,
  verdict NEEDS_HUMAN_APPROVAL.
- **F5** — every textual gate field is scanned recursively for secrets, local absolute paths and
  control characters; a canary blocks before the ZIP is built.
- **F6** — the Root Manifest is built from the IMMUTABLE Source snapshot bytes via
  `build_manifest_from_snapshot`; no Evidence helper opens/stats/lists the staging filesystem after
  the snapshot, so no artifact is interpreted from one read and packaged from another.

## Verification

### Authoritative (each command recorded in the packaged `verification_tests.json`)
- Round-24 closure suites (gate_exact_schemas, gate_embedded_verdicts, gate_sensitive_metadata,
  commit_gate_exact_derivation, manifest_from_source_snapshot, manifest_snapshot_races) → **64
  passed**.
- The round-23 gate/commit/e2e suites (semantic_consistency, commit_gate_consistency,
  ready_gate_matrix, authoritative_e2e) → all pass under the round-24 complete fixtures.
- Broad review/manifest orchestration batch (`-k review or manifest or snapshot or evidence or gate
  or bundle or archive or commit or stream`) → **2888 passed, 1 pre-existing baseline failure**.
- Docs consistency (incl. `TestF012Round24IsPinned`) → **209 passed**.
- compileall exit 0.

### Diagnostic (nonauthoritative; NOT in verification_tests.json)
- `test_stream_export_e2e.py::...test_final_zip_contains_streams_under_evidence_current` fails
  because the test's helper-copy list omits `scripts/stage_review_evidence.py` (a stale fixture). It
  fails IDENTICALLY at the pre-round-24 base `5691c51`, so it is a pre-existing baseline failure,
  unrelated to this block. Reported for context only, never as a proof.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch locally committed,
unpushed, unmerged.
