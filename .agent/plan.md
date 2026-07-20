# Plan — F012 Verified-Inode Publication & Strict Token Producer Closure Round 35

Round-34 contracts FROZEN. External review returned four bounded findings. Round 35 closes exactly
these four and broadens no further.

## Scope 1 — FD-retained, inode-bound, OverlayFS-safe publication

`verify_source_identity` hashes by pathname then links — a TOCTOU gap allows a post-hash swap. The
`st_dev` precheck falsely blocks on OverlayFS (file and parent report different st_dev).

- `safe_publish.py`: rewrite `verify_source_identity` to use FD-retained protocol: open source
  O_RDONLY|O_NOFOLLOW, fstat to verify regular, hash through FD, retain FD. Remove st_dev precheck.
  After os.link, stat the final path and compare (st_dev, st_ino) to the retained FD's fstat — the
  published inode is the verified inode. Handle EXDEV from os.link for true cross-filesystem rejection.
- Tests: post-hash swap blocked (pathname replaced between hash and link), in-place mutation blocked
  (bytes written through a second FD after hash), symlink replacement blocked, FD/inode equality
  verified after publication, OverlayFS-like different st_dev doesn't falsely block, true cross-fs
  blocks (via EXDEV), concurrent publication exactly one wins.

## Scope 2 — strict raw token/provider Evidence decoding + producer self-validation + authority validity

### 2a — strict raw decoding
`_read_json()` uses tolerant `json.loads`. `_as_int()` coerces floats.

- `token_truth.py`: replace `_read_json` with `strict_loads` from `packages/common/strict_json.py`
  for token_accounting.json, provider_evidence.json, prompt_trace_summary.json. Replace `_as_int()`
  for prompt_trace_count with `_strict_count`. Distinguish absent vs present-invalid.
- Tests: duplicate keys, NaN, Infinity, wrong root type, malformed JSON, bool/float/string trace
  count, genuinely absent optional still degrades.

### 2b — successful producer always valid + authority validity
`build_token_truth()` can emit invalid TokenTruthV1: prompt+completion present but total null;
cache-only triggers high confidence; non-string model identity accepted. `_token_truth_authority()`
declares VERIFIED_EQUAL without validating either canonical or supplied.

- `token_truth.py`: derive actual_total from prompt+completion when absent. Cache-only (no
  prompt/completion/total) → not high confidence. Strictly type model identities (must be str or
  absent). Call `validate_token_truth(report)` before returning; raise TokenEvidenceError if invalid.
- `build_review_manifest.py`: `_token_truth_authority()` validates canonical output, validates
  supplied output, only then compares. PRODUCER_ERROR for raised or invalid canonical. MISMATCH for
  unequal valid outputs, or valid canonical + invalid supplied.
- Tests: meta-regression, canonical-invalid authority blocking, prompt+completion-without-total
  derives correctly, cache-only is not high.

## Scope 3 — truthful Round-35 docs + operator state

Update T0_F012.md with "Hardening round 35" section. Update test_docs_consistency.py with
TestF012Round35IsPinned. Update plan.md and live_review.md.

## Constraints (unchanged)

Zero provider calls; manual only; no job-flow/job-run/db/network/docker/new deps. Small local commits,
never amend/squash. No push/PR/merge/main. Do not start F017. Fresh Evidence linked to prior
`d167552dc8e31fd0` through the real operator entry, VERIFIED_EQUAL, git OK; one READY ZIP; then stop.
