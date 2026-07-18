# Live Review — Steps 11761-11960 — F012 hardening round 21 (final root-identity closure)

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (10 final root-identity findings), awaiting re-review (NOT accepted).

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Raw-stream format unchanged; F001 timeout/retry unchanged; F010/F011 not
weakened. Only the additive `package_hash_chain` (round 20) and the `review_archive.expectation`
rename (round 21) touch the manifest schema.

External review of `remedy-review-20260718-010345-READY_FOR_REVIEW.zip` (SHA
`2b51417f…c010c8`, Evidence job `0ffc34687764446b`) returned TEN final root-identity findings.
Fixed as one small closure block: every packaged identity is now an exact raw-byte identity over one
immutable staged byte map.

- **F1** — the manifest names only members that exist; `review_archive.expectation` points at the
  real `review_zip_expectation.json` (the stale `review_zip_verification.json` reference is retired).
- **F2/F4** — every root `*_sha256` (Subject/Proof/Commit-Chain) is `SHA256(exact packaged bytes)`,
  equal across plan/expectation/manifest and the packaged member — never a reserialized projection.
- **F3** — a DECLARED subject (`subject.declared`) always requires a strict Proof; a declared
  zero-file/net-zero/revert subject requires a valid empty Proof.
- **F5** — `_StagedArtifacts` reads each root artifact once; decode-bytes and package-bytes are
  provably identical, and a staged file changed between the two reads blocks.
- **F6** — one ArchivePlan disposition per path: unchanged sensitive context is EXCLUDE_SAFE_CONTEXT,
  a FIFO/special file is BLOCK_UNSUPPORTED; nothing silently disappears (the Shell `find` enumerates
  special files as defense-in-depth).
- **F7** — the final status/filename come from the verified build model on build_review_zip's
  stdout, never a post-build reread of the mutable disk manifest.
- **F8** — ContentProof accepts only the exact version set `{"1.1.0"}`.
- **F9** — the complete authoritative regression is recorded in `verification_tests.json`.
- **F10** — the snapshot inventory covers exactly the source Evidence members at the snapshot
  boundary (generated members outside it), with a validator matching every entry to its Plan member.

## Verification

### Authoritative (each command recorded in the packaged `verification_tests.json`)
- Round-21 closure suites (root_artifact_references, raw_byte_hash_identity, declared_empty_subject,
  staged_decode_snapshot_race, single_bundle_disposition, final_status_source, schema_versions,
  authoritative_e2e, snapshot_inventory_consistency) → **33 passed**.
- Full F012/review batch (run_manifest, job_input_definition, persisted schemas, review_*, round13,
  job_rerun_manifest, do_job_flow_review_base) → **1646 passed**.
- F010/F011/Evidence (failure_postmortem, job_stop, stop_reasons, job_evidence, evidence_bundle/
  index/mode, final_verifier, final_audit_evidence, fresh_evidence_gate) → **502 passed**.
- Authoritative CLI (`tests/test_do_job_flow.py` + `tests/cli`, excluding the two PRE-EXISTING
  doc-path suites) → **1030 passed**.
- Docs consistency (incl. `TestF012Round21IsPinned`) → **187 passed**.
- Full-package integration (`test_review_package_full_integration.py`, 6 REAL cases, no skips) →
  **6 passed**.
- compileall (`packages apps scripts tests`) exit 0; `bash -n scripts/make_review_zip.sh` clean;
  `git diff --check` clean; `remedy integrity check` passed (fail_count 0).

### Diagnostic (nonauthoritative; NOT in verification_tests.json)
- A broad `tests/orchestration` sweep still carries the pre-existing baseline failures (stale
  fixtures / doc-path debt unrelated to this block). Reported for context only, never as a proof.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch locally committed,
unpushed, unmerged.
