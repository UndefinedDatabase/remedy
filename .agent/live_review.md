# Live Review — Steps 14361-14560 — F012 Single-Publication & Complete Token-Truth Closure Round 34

## Verdict (reviewer-owned)
**PENDING** — F1/F2 closed this round; every accepted Round-33 contract (direct-Python atomic
publication, fail-closed git_tracked_status, shared measurement-source enums, executable
create_manual_completion_bundle, FV reproducibility, total gate eval, root git-status snapshot, patchset
identity, full package-integration termination, manual token-truth equality) preserved. Not externally
accepted.

## Process inspection (mandated first action)
`ps -eo pid,pgid,etime,args` filtered for `pytest`, `make_review_zip.sh`, `build_review_zip.py`,
`build_review_manifest.py`, `remedy-review`, Round-33 Evidence job `b95cde870e6863ad`: **no review-owned
processes running**. Nothing obsolete to terminate; no process group killed (no broad Python/Bash/Remedy
kill performed).

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Every accepted Round-33 contract preserved.

External review of `remedy-review-20260719-230022-READY_FOR_REVIEW.zip` (SHA `d67895bb...c03cbc`,
Evidence `b95cde870e6863ad`, prior `453aab97e0fc3b01`, base `13cd5a5d`, HEAD `d822df9d`) accepted the
round-33 contracts and returned two bounded findings.

### Closed this round
- **F1 — one private-to-final publication; no public intermediate ZIP.** `build_review_zip.py` derives
  the exact status-bearing final path from a `{package_status}` template, builds a private
  `.remedy_zip_*.part`, verifies it, binds its SHA-256 and atomically links that inode DIRECTLY to the
  final path (returning `final_path` + `final_sha256`). `safe_publish.verify_source_identity` /
  `publish_atomically(expected_sha256=)` bind the source's regular-file/inode/same-fs/bytes identity.
  `make_review_zip.sh` builds no public temp ZIP, has no `rm -f "$OUT"`/`mv "$OUT"`/second publish/ZIP
  `_refuse_tracked_output`; it trusts the coordinator's verified JSON, checks the published SHA, and
  does READ-ONLY post-publication checks. Commit 05560d9.
- **F2 — complete TokenTruthV1 input + output semantics.** `token_truth.build_token_truth` strictly
  validates provider/token-accounting inputs (real nonnegative ints, finite cost, actual≤provider,
  cost≤actual, prompt+completion==total) and RAISES `TokenEvidenceError` — never clamps/coerces — so
  malformed Evidence → `token_truth_authority = PRODUCER_ERROR` → `BLOCKED_EVIDENCE`.
  `token_authority.validate_token_truth` is the closed TokenTruthV1 output schema + every state
  invariant. Commit 83db0e5.

## Verification

- New/affected suites pass: test_review_single_publication, test_review_atomic_publish,
  test_review_no_clobber_publish, test_review_package_full_integration, test_review_authoritative_e2e,
  test_token_truth, test_token_authority, test_token_producer_validator_compat,
  test_token_truth_v1_contract, test_review_token_truth_authority, test_review_manual_completion_shapes,
  and the docs pins (TestF012Round34IsPinned). The full acceptance matrix is re-run before packaging;
  counts recorded in verification_tests.json. `test_manual_completion_bundle` runs as its own matrix
  command (a pre-existing cross-test ordering interaction makes 2 of its cases order-dependent in a
  long mixed run; all 44 pass in isolation).

## Status

F012 `[~]` — not externally accepted. F017 `[ ]` not started. Branch locally committed, unpushed,
unmerged. Authority: staged Evidence bytes → real producers → regenerated final verifier + token truth
→ gates → archive plan → ONE private-to-final atomically-published ZIP; a supplied
final-verifier/token-status JSON is never authority.
