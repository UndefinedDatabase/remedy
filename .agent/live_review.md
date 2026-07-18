# Live Review — Steps 12561-12760 — F012 hardening round 25 (recursive gate schema + safe snapshot acquisition)

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (6 recursive-schema/acquisition findings), awaiting re-review (NOT accepted).

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. The gate matrix and staged-byte acquisition are additive-hardened; no
manifest field was removed.

External review of `remedy-review-20260718-190112-READY_FOR_REVIEW.zip` (SHA
`d40e2454dbfe0e576412bdc257ad7da4aede484256f694d1437f33b44afa0cb9`, Evidence job
`041261b92c134f5b`, linked prior `14f211210d044bfb`, HEAD `3d11fc9`) returned SIX findings. Fixed as
one bounded closure block.

- **F1** — every gate is validated by an EXACT typed RECURSIVE schema; an unknown NESTED field, a
  wrong element type, or a dynamic-map key violating its grammar all block.
- **F2** — complete READY semantics per gate: FV evidence-completeness/spec/scratch/alignment/change
  PASS + token-critical clear + test_status.passed == recorded total; fresh id/range direct
  equality; artifact exact required key set + stream/worktree PASS-or-NOT_APPLICABLE; change
  covered == source-excluded == evidence_covered == ContentProof authority, and current_hashes ==
  evidence_hashes == ContentProof file hashes (one authority model).
- **F3** — the metadata scanner walks dictionary KEYS as well as values; secret/local-path/control/
  over-length/credential-name keys block, and dynamic keys satisfy their typed grammar.
- **F4** — the commit gate's blocked_gates, non_pass_gates AND issues are all exactly derived from
  gate_checks by the writer's deterministic rule; an empty/unrelated issues list blocks.
- **F5** — every trusted gate/subject/proof/chain decode rejects DUPLICATE JSON keys at any depth
  (a dependency-free object_pairs_hook), so a duplicated verdict no longer resolves to last-wins.
- **F6** — staged bytes are acquired only through anchored, O_NOFOLLOW secure_fs reads
  (`_StagedArtifacts.load` and `_view_from_dir`); a symlink/FIFO/socket/device is never followed or
  read, size limits are enforced during acquisition, and the preliminary manifest pass uses the same
  secure reader.

## Verification

### Authoritative (each command recorded in the packaged `verification_tests.json`)
- Round-25 closure suites (recursive_schemas, complete_semantics, key_safety,
  commit_gate_issue_derivation, duplicate_keys, staged_artifact_no_follow) → **51 passed**.
- Complete F012/review block (46 test_run_manifest*.py + persisted schemas + round13 + the full
  review/archive/snapshot/gate batch incl. all round-24 and round-25 suites) → all pass.
- Complete F010/F011/Evidence block (11 files) → all pass.
- Authoritative CLI (`tests/test_do_job_flow.py` + `tests/cli`, excluding the two PRE-EXISTING
  doc-path suites) → all pass.
- Docs consistency (incl. `TestF012Round25IsPinned`) → all pass.
- compileall exit 0; `bash -n scripts/make_review_zip.sh` clean; `git diff --check` clean;
  integrity check passed (fail_count 0).

### Diagnostic (nonauthoritative; NOT in verification_tests.json)
- `test_stream_export_e2e.py::...streams_under_evidence_current` fails on a stale fixture (omits
  `scripts/stage_review_evidence.py`); it fails identically at the pre-round-24 base and is unrelated.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch locally committed,
unpushed, unmerged.
