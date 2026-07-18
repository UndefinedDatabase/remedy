# Live Review — Steps 11961-12160 — F012 hardening round 22 (final gate-and-snapshot closure)

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (5 gate-and-snapshot findings), awaiting re-review (NOT accepted).

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Raw-stream format unchanged; F001 timeout/retry unchanged; F010/F011 not
weakened. Manifest gains additive `ready_gate_matrix` and `snapshot_inventory_status` fields.

External review of `remedy-review-20260718-103941-READY_FOR_REVIEW.zip` (SHA
`b3fee1cd…f28336`, Evidence job `5bd1eb8fa7ed4601`) returned FIVE gate-and-snapshot findings. Fixed
as one bounded closure block.

- **F1** — READY_FOR_REVIEW is bound to the complete packaged gate verdict matrix
  (`evaluate_ready_gate_matrix`); a BLOCKED/missing/invalid/unknown/contradictory gate →
  BLOCKED_EVIDENCE. A BLOCKED final_verifier can no longer ride inside a READY package.
- **F2** — the manifest and the archive consume ONE immutable staged byte map; the seven gate files
  and the inventory are bound into the plan's evidence-member hashes (a post-manifest mutation
  blocks), the status is derived from that map, and the package contains exactly the gate bytes used
  to decide it.
- **F3** — strict `EvidenceSnapshotInventoryV1` with an exact Plan bijection, CALLED in the
  production build before READY is possible; a forged inventory member SHA blocks.
- **F4** — the ArchivePlan is the sole bundle-policy owner: the Shell `find` drops its sensitive
  name/suffix exclusions, so an unchanged `.env`/log/archive/key gets an explicit
  EXCLUDE_SAFE_CONTEXT record and a FIFO a BLOCK_UNSUPPORTED record — nothing silently disappears.
- **F5** — the complete F012/F010/F011 acceptance regression is recorded in the fresh Evidence.

## Verification

### Authoritative (each command recorded in the packaged `verification_tests.json`)
- Round-22 closure suites (ready_gate_matrix, manifest_archive_same_snapshot,
  snapshot_inventory_strict, real_single_bundle_policy, complete_acceptance_commands) → **34 passed**.
- Every F012/review suite incl. all 46 `test_run_manifest*.py`, review_*, round13, job_evidence and
  the gates → **1771 passed** in the combined batch.
- Complete F010/F011/Evidence block (failure_postmortem, job_stop_integration, stop_reasons,
  job_evidence, evidence_bundle/index/mode, final_verifier, final_audit_evidence, fresh_evidence_gate,
  change_provenance_gate) → **525 passed**.
- Authoritative CLI (`tests/test_do_job_flow.py` + `tests/cli`, excluding the two PRE-EXISTING
  doc-path suites) → **1030 passed**.
- Docs consistency (incl. `TestF012Round22IsPinned`) → **195 passed**.
- Full-package integration (6 REAL cases, no skips) → **6 passed**.
- compileall exit 0; `bash -n scripts/make_review_zip.sh` clean; `git diff --check` clean;
  `remedy integrity check` passed (fail_count 0).

### Diagnostic (nonauthoritative; NOT in verification_tests.json)
- A broad `tests/orchestration` sweep still carries the pre-existing baseline failures (stale
  fixtures / doc-path debt unrelated to this block). Reported for context only, never as a proof.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch locally committed,
unpushed, unmerged.
