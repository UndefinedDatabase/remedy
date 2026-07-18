# Live Review — Steps 12161-12360 — F012 hardening round 23 (semantic-gate + complete-snapshot closure)

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (5 semantic-gate/snapshot findings), awaiting re-review (NOT accepted).

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Raw-stream format unchanged; F001 timeout/retry unchanged; F010/F011 not
weakened. Manifest gains additive `snapshot_inventory_status`; the commit gate is recorded in
`ready_gate_matrix.gate_verdicts`.

External review of `remedy-review-20260718-133146-READY_FOR_REVIEW.zip` (SHA
`6256a748…384b89`, Evidence job `ff07e91816a146e1`) returned FIVE findings. Fixed as one bounded
closure block.

- **F1** — one semantic validator per READY gate checks the gate's INTERNAL truth (schema closed to
  {"1.0.0"}); a document that claims PASS while its body records an unresolved blocker, a failed
  test, a stale/non-authoritative state, a missing artifact, an uncovered file or an integrity
  failure now BLOCKS.
- **F2** — the commit_execution gate is CHECKED (exists, strict JSON, version, verdict
  NEEDS_HUMAN_APPROVAL, promote_ready=false, blocked_gates=[], embedded gate_checks == packaged
  verdicts) yet nonblocking; a missing/invalid/contradictory commit gate blocks Evidence integrity.
- **F3** — build_review_zip.py rebuilds the Root Manifest from the SAME staged evidence tree it
  packages, so no evidence artifact is interpreted from one read and packaged from another; the
  manifest's evidence facts equal the packaged bytes.
- **F4** — the inventory member size is bound EXACTLY: inventory.size == snapshot bytes ==
  plan expected_size == packaged ZIP uncompressed size, verified from the ZIP.
- **F5** — a prior `remedy-review-*` package (or its `.sha256` sidecar) reaches the ArchivePlan and
  gets an explicit EXCLUDE_SAFE_CONTEXT record; the shell keeps only structural pruning.

## Verification

### Authoritative (each command recorded in the packaged `verification_tests.json`)
- Round-23 closure suites (gate_semantic_consistency, commit_gate_consistency,
  complete_staged_byte_map, snapshot_inventory_size_binding, old_package_disposition) →
  **36 passed**.
- Full F012/review batch incl. all 46 `test_run_manifest*.py`, review_*, round13, persisted schemas →
  **1611 passed**.
- Complete F010/F011/Evidence block (11 files) → **525 passed**.
- Authoritative CLI (`tests/test_do_job_flow.py` + `tests/cli`, excluding the two PRE-EXISTING
  doc-path suites) → **1030 passed**.
- Docs consistency (incl. `TestF012Round23IsPinned`) → **195 passed**.
- Full-package integration (6 REAL cases, no skips) → **6 passed** (inside the review batch).
- compileall exit 0; `bash -n scripts/make_review_zip.sh` clean; `git diff --check` clean;
  `remedy integrity check` passed (fail_count 0).

### Diagnostic (nonauthoritative; NOT in verification_tests.json)
- A broad `tests/orchestration` sweep still carries the pre-existing baseline failures (stale
  fixtures / doc-path debt unrelated to this block). Reported for context only, never as a proof.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch locally committed,
unpushed, unmerged.
