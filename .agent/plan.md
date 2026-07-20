# Plan — F012 Anonymous-Inode Publication, Semantic Provider Evidence, Complete Verification Round 37

Round-36 contracts FROZEN. External review returned four bounded findings. Round 37 closes
exactly these and broadens no further.

## Scope 1 — anonymous immutable publication inode

Round 36's publication still links a named source path (`os.link(source_path, final)`). A writable
FD on that named inode can mutate it after the final hash read. Cleanup ownership is inferred
after the race (lstat of the just-linked final path), so a foreign replacement can be removed.

- `safe_publish.py`: replace named-source publication with anonymous-FD protocol:
  1. `O_TMPFILE` creates an anonymous inode in the final parent directory.
  2. Copy verified source bytes into the anonymous FD.
  3. `fsync` + set mode.
  4. Hash the anonymous FD; require `expected_sha256`.
  5. `linkat(fd, "", AT_FDCWD, final, AT_EMPTY_PATH)` for no-replace publication.
  6. Known inode = `fstat(anonymous_fd)` BEFORE publication (not from post-link lstat).
  7. Post-publication: open final with `O_NOFOLLOW`, compare inode, re-hash both FDs.
  8. Cleanup uses pre-publication anonymous inode, never post-race observation.
  9. `O_TMPFILE`/`linkat` unavailable → fail closed with `PublishSourceError`.
- Tests: named `.part` mutation after anonymous copy cannot alter publication; no pathname
  swap affects anonymous inode; no external writable FD on anonymous inode; final bytes ==
  expected_sha256; exactly one concurrent publisher wins; pre-existing destination preserved;
  no `os.link(source_path, final)` fallback; foreign replacement between publication and
  postverification remains byte-identical.

## Scope 2 — semantic Provider-Evidence validation

Round 36 validated field types but not semantic relationships. Contradictory provider evidence
(verified model without identity, cost without cost-covered call, etc.) is silently normalized.

- `token_truth.py`: add `validate_provider_evidence(pe, ctx)` before aggregation:
  - `actual_model_verified=true` → at least one nonempty actual model identity required
  - actual model identity present → `actual_model_verified` must be true
  - `total_cost_usd` present → `cost_call_count > 0`
  - `cost_call_count == 0` → `total_cost_usd` must be absent or null
  - `actual_call_count == 0` → ordinary actual token counters must be absent
  - actual token counters present → `actual_call_count > 0`
  All raise `TokenEvidenceError`.
- Tests: each exact contradiction → `TokenEvidenceError` → authority = PRODUCER_ERROR
  → package_status = BLOCKED_EVIDENCE.

## Scope 3 — complete authoritative and diagnostic verification

Round 36 packaged only 12 test files (496 passed, 0 failed). The quoted 7432/56 broad run was
not packaged. The verification contract requires every authoritative command separately plus
any quoted diagnostic run with a grounded baseline comparison.

- Package every required authoritative command as its own typed run in `verification_tests.json`.
- Run the broad orchestration suite; capture failing node IDs.
- Run the same command against a grounded baseline commit; capture baseline failures.
- Prove the failure sets are identical (pre-existing, unchanged).
- Package the diagnostic run as a typed artifact (not authoritative green proof).
- Update T0_F012.md, test_docs_consistency.py, plan.md, live_review.md.

## Constraints (unchanged)

Zero provider calls; manual only; no job-flow/job-run/db/network/docker/new deps. Small local
commits, never amend/squash. No push/PR/merge/main. Do not start F017. Fresh Evidence linked to
prior `r36_byte_inode_typed_token` through the real operator entry, VERIFIED_EQUAL, git OK; one
READY ZIP; then stop.
