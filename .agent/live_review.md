# Live Review — F012 Verified-Inode Publication & Strict Token Producer Closure Round 35

## Verdict (reviewer-owned)
**PENDING** — F1/F2/F3/F4 closed this round; every accepted Round-34 contract preserved. Not
externally accepted.

## Process inspection (mandated first action)
`ps -eo pid,pgid,etime,args` filtered for `pytest`, `make_review_zip.sh`, `build_review_zip.py`,
`build_review_manifest.py`, `remedy-review`: **no review-owned processes running**. Nothing obsolete to
terminate; no process group killed.

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Every accepted Round-34 contract preserved.

### Closed this round
- **F1 — FD-retained, inode-bound, OverlayFS-safe publication.** `verify_source_identity` opens
  O_RDONLY|O_NOFOLLOW, fstat, hashes through FD, returns retained FD. `verify_published_inode`
  checks (st_dev, st_ino) match. st_dev precheck removed; EXDEV catches true cross-device. Commit
  a583fcd.
- **F2 — strict raw token/provider Evidence JSON decoding.** `_read_json` uses `strict_loads` —
  rejects duplicate keys, NaN, Infinity, invalid UTF-8. `_as_int` replaced with `_strict_count` for
  prompt_trace_count. Commit bb3842d.
- **F3 — successful producer always emits valid TokenTruthV1.** Derives actual_total from
  prompt+completion. Cache-only is not actual usage. Model identity strictly typed. Producer
  self-validates via `validate_token_truth(report)`. Commit b3b35fd.
- **F4 — authority validates both canonical and supplied before VERIFIED_EQUAL.** Invalid canonical →
  PRODUCER_ERROR; invalid supplied → MISMATCH. Commit b3b35fd.

## Verification

- New/affected suites pass: test_review_atomic_publish (20), test_token_truth_v1_contract (56),
  test_token_truth (29), test_token_authority (12), test_token_producer_validator_compat (7),
  test_review_single_publication (7), test_review_package_full_integration, test_review_authoritative_e2e,
  TestF012Round35IsPinned (5). Full acceptance matrix re-run before packaging.

## Status

F012 `[~]` — not externally accepted. F017 `[ ]` not started. Branch locally committed, unpushed,
unmerged.
