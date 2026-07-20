# Live Review — F012 Versioned PE Schema, Publication Capability Round 38

## Verdict (reviewer-owned)
**PENDING** — F1/F2/F3/F4/F5/F6 closed this round; every accepted Round-37 contract preserved. Not
externally accepted.

## Process inspection (mandated first action)
`ps -eo pid,pgid,etime,args` filtered for `pytest`, `make_review_zip.sh`, `build_review_zip.py`,
`build_review_manifest.py`, `remedy-review`: **no review-owned processes running**. Nothing obsolete to
terminate; no process group killed.

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Every accepted Round-37 contract preserved.

### Closed this round
- **F1 — cost without call-count provenance.** `total_cost_usd` without `cost_call_count` now
  raises `TokenEvidenceError`. The empty `pass` branch replaced with `raise`. Commit 61b0a6f.
- **F2 — ambiguous generic actual_model.** Generic `actual_model` field rejected as ambiguous.
  Callers must use `builder_actual_model` or `reviewer_actual_model`. Per-task fallback removed.
  Commit 61b0a6f.
- **F3 — verified model with zero provider calls.** `actual_model_verified=true` with
  `provider_call_count=0` now raises `TokenEvidenceError`. Commit 61b0a6f.
- **F4 — machine-validated diagnostic comparison.** Self-asserted `baseline_match` replaced with
  machine-validated comparison: sorted failure node IDs, SHA-256 of failure sets, derived
  `failure_sets_equal`. Baseline via `git archive` extraction. Schema 2.0.0.
- **F5 — complete authoritative test matrix.** 17 suites (578 passed, 0 failed). Every named
  file and group packaged as typed verification runs.
- **F6 — explicit publication capability probe.** `probe_anonymous_publication_capability()`
  returns typed result. Source `.part` cleanup ownership-bound: record (st_dev, st_ino) before
  copy, only unlink if same inode. Commit 86e1070.

## Verification

- Authoritative suites: test_review_atomic_publish (32), test_token_truth_v1_contract (96),
  test_token_truth (37), test_token_authority (13), test_review_token_truth_authority (15),
  test_review_manual_completion_shapes (18), test_review_single_publication (7),
  test_review_package_full_integration (8), test_review_authoritative_e2e (1),
  test_token_producer_validator_compat (8), test_docs_consistency (275),
  test_review_archive_plan (10), test_provider_evidence_integration (56),
  test_stream_export_e2e (7), compileall (clean), bash -n (clean), git diff --check (clean).
- Diagnostic: tests/orchestration/ broad (7446/56/7) — 56 failures all pre-existing, zero new
  from R38. Machine-validated with sorted node IDs + SHA-256 comparison.

## Status

F012 `[~]` — not externally accepted. F017 `[ ]` not started. Branch locally committed, unpushed,
unmerged.
