# Live Review — F012 Anonymous-Inode Publication & Semantic Provider Evidence Round 37

## Verdict (reviewer-owned)
**PENDING** — F1/F2/F3/F4 closed this round; every accepted Round-36 contract preserved. Not
externally accepted.

## Process inspection (mandated first action)
`ps -eo pid,pgid,etime,args` filtered for `pytest`, `make_review_zip.sh`, `build_review_zip.py`,
`build_review_manifest.py`, `remedy-review`: **no review-owned processes running**. Nothing obsolete to
terminate; no process group killed.

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Every accepted Round-36 contract preserved.

### Closed this round
- **F1 — anonymous-FD no-replace publication.** Named-source `os.link(source_path, final)` replaced
  with anonymous-inode protocol: `O_TMPFILE` + `linkat(fd, "", AT_FDCWD, final, AT_EMPTY_PATH)`.
  No named source path participates in the security decision. Commit a159b47.
- **F2 — pre-publication cleanup ownership.** `owned_inode` from `fstat(anonymous_fd)` BEFORE
  publication. `_cleanup_published_link` uses pre-publication anonymous inode identity, never
  post-race observation. Commit a159b47.
- **F3 — semantic ProviderTokenEvidence validation.** `validate_provider_evidence(pe, ctx)` added
  before aggregation. Rejects: verified-without-model, model-without-verified, cost-without-cost-calls,
  counters-without-actual-calls. Each raises `TokenEvidenceError`. Commit ddbf911.
- **F4 — complete authoritative and diagnostic verification.** 15 authoritative runs (503 passed,
  0 failed). Diagnostic broad run: 7440 passed, 56 failed — all pre-existing (identical on parent
  commit b2c9840). Commit 99df826.

## Verification

- Authoritative suites: test_review_atomic_publish (26), test_token_truth_v1_contract (90),
  test_token_truth (37), test_token_authority (13), test_review_token_truth_authority (15),
  test_review_manual_completion_shapes (18), test_review_single_publication (7),
  test_review_package_full_integration (8), test_review_authoritative_e2e (1),
  test_token_producer_validator_compat (8), test_docs_consistency (270),
  test_review_archive_plan (10), compileall (clean), bash -n (clean), git diff --check (clean).
- Diagnostic: tests/orchestration/ broad (7440/56/7) — 56 failures all pre-existing on b2c9840.

## Status

F012 `[~]` — not externally accepted. F017 `[ ]` not started. Branch locally committed, unpushed,
unmerged.
