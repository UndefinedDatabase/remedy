# Live Review — F012 Byte-and-Inode-Bound Publication & Typed Token-Input Closure Round 36

## Verdict (reviewer-owned)
**PENDING** — F1/F2/F3/F4/F5 closed this round; every accepted Round-35 contract preserved. Not
externally accepted.

## Process inspection (mandated first action)
`ps -eo pid,pgid,etime,args` filtered for `pytest`, `make_review_zip.sh`, `build_review_zip.py`,
`build_review_manifest.py`, `remedy-review`: **no review-owned processes running**. Nothing obsolete to
terminate; no process group killed.

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Every accepted Round-35 contract preserved.

### Closed this round
- **F1 — byte-and-inode-bound publication with post-publication re-hash.** `verify_published_inode`
  replaced with `verify_published_identity`: inode check AND re-hash through retained FD.
  `expected_sha256` now mandatory. Commit f31f9ee.
- **F2 — pathname replacement cleanup.** `_cleanup_published_link` removes final path only after
  proving it is this invocation's inode. Evil final ZIPs cleaned up. Commit f31f9ee.
- **F3 — typed object roots.** `_read_json` enforces dict root; non-dict raises
  `TokenEvidenceError`. Commit f5763bb.
- **F4 — strict scalar field validation.** `str()` coercions replaced with `_strict_string`,
  `_strict_nullable_string`, `_strict_string_list`. Non-string trust-bearing fields raise
  `TokenEvidenceError`. Commit f5763bb.
- **F5 — red-test repair.** Authority test assertions accept either "not the aggregate" or
  "invalid". Commit 81518c7.

## Verification

- New/affected suites pass: test_review_atomic_publish (26), test_token_truth_v1_contract (85),
  test_token_truth (29), test_token_authority (18), test_review_token_truth_authority (15).
  Full acceptance matrix re-run before packaging.

## Status

F012 `[~]` — not externally accepted. F017 `[ ]` not started. Branch locally committed, unpushed,
unmerged.
