# Plan — F012 Byte-and-Inode-Bound Publication & Typed Token-Input Closure Round 36

Round-35 contracts FROZEN. External review returned five bounded findings. Round 36 closes
exactly these and broadens no further.

## Scope 1 — exact verified-source publication (byte + inode binding)

Round 35's FD-retained inode check is necessary but insufficient: a same-inode in-place mutation
through a second writable FD passes the inode check. A detected pathname swap leaves an evil
final ZIP on disk.

- `safe_publish.py`: replace `verify_published_inode` with `verify_published_identity` — after
  `os.link`, compare inode AND re-hash through the retained FD. Post-publication hash mismatch
  raises `PublishSourceError`. Make `expected_sha256` mandatory (missing → `PublishSourceError`).
  On any post-publication failure, `_cleanup_published_link` unlinks the final path only after
  proving it is the inode this invocation created. No foreign pre-existing destination removed.
- Tests: same-inode in-place mutation blocks + no final remains, pathname replacement blocks +
  no final remains, symlink replacement blocks, omitted hash blocks, OverlayFS still succeeds,
  cross-fs blocks, concurrent exactly one wins (all with expected_sha256), foreign pre-existing
  preserved, successful bytes hash exactly.

## Scope 2 — typed raw token Evidence (object roots + scalar fields)

Round 35's strict JSON syntax (duplicate keys, NaN, etc.) did not validate the decoded root
type or trust-bearing scalar fields.

### 2a — typed object roots
`_read_json` currently returns non-dict types (null, list) as valid decoded data which callers
treat as absent. Fix: `FileNotFoundError` = absent; any other OSError = present-invalid; decoded
non-dict root = present-invalid (raises `TokenEvidenceError`).

### 2b — scalar field validation
`str()` coerces non-string provider/model/role/configured_model into "valid" strings. Fix: add
`_strict_string`, `_strict_nullable_string`, `_strict_string_list` helpers. Validate every
trust-bearing identity field and `usage` when present.

- Tests: list/null/string/number/bool roots for each Evidence file raise; non-string provider,
  model, role, configured_model, cli_version raise; non-list actual_missing_reasons raises;
  non-dict usage raises; table-driven mutation suite.

## Scope 3 — red-test repair + complete verification + truthful documentation

### 3a — red-test repair
`test_review_token_truth_authority.py::test_forged_root_field_blocks` asserts "not the aggregate"
in reason, but round-35 validation now catches invalid supplied truth as "invalid" before the
comparison. Update assertions to accept either "not the aggregate" OR "invalid" without removing
the reason check.

### 3b — complete verification
Run every named test file separately. Record every command in `verification_tests.json`.

### 3c — truthful documentation
Update T0_F012.md, test_docs_consistency.py, plan.md, live_review.md. Correct round-35
overclaims.

## Execution

All five findings closed:
- Scope 1: f31f9ee (byte-and-inode-bound publication + cleanup)
- Scope 2: f5763bb (typed roots + strict scalars)
- Scope 3a: 81518c7 (red-test repair)
- Scope 3c: docs commit (pending)

## Constraints (unchanged)

Zero provider calls; manual only; no job-flow/job-run/db/network/docker/new deps. Small local
commits, never amend/squash. No push/PR/merge/main. Do not start F017. Fresh Evidence linked to
prior `c323341f2542e9d4` through the real operator entry, VERIFIED_EQUAL, git OK; one READY ZIP;
then stop.
