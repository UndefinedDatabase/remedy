# Live Review — Steps 12761-12960 — F012 hardening round 26 (fully typed shapes + fail-closed total + bounded acquisition)

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (6 typed-shape/verification/acquisition findings), awaiting re-review (NOT accepted).

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. The gate schema, verification decoder and staged acquisition are
additive-hardened; no manifest field was removed.

External review of `remedy-review-20260718-201125-READY_FOR_REVIEW.zip` (SHA
`2250e8cb8d82cecc3b37721ab81a6a5d61816cba7d55634e0d7f80d778374674`, Evidence job
`a67d0c3f0513bd11`, linked prior `041261b92c134f5b`, HEAD `78cbb9b`) returned SIX findings. Fixed as
one bounded closure block.

- **F1** — the schema engine has NO accept-anything node; every scalar/list element/nested value is
  typed, with `_Nullable` unions, `_OneOf`, exact finding/mismatch records, and two distinct
  token_status/token_measurement shapes.
- **F2** — `_Obj` requires its full producer shape; a missing required nested field (token block,
  stream/worktree section, test_status, evidence_freshness, integrity notes) blocks.
- **F3** — a strict `VerificationTestsV1` (exact version/fields, real-int counts, no int() coercion,
  exit==0/failed==0/passed>=1, totals==sum of runs, test_files==union) is enforced fail-closed by
  the gate matrix AND the manual-completion validator; a missing/invalid record blocks and the FV
  total must equal it.
- **F4** — one shared `AcquisitionBudget` (per-member/aggregate/count/duplicate) bounds both
  `_view_from_dir` and `_StagedArtifacts`; exceeding any limit BLOCKS, never a silent absence.
- **F5** — the dependency-free duplicate-key decoder lives only in `packages/common/strict_json.py`;
  both packaging scripts import it and keep no private copy.
- **F6** — the exact generated packaging outputs get a `packaging_generated_outputs` disposition in
  the review-state; a clean branch stays clean during packaging while a real dirty file stays dirty.

## Verification

### Authoritative (each command recorded in the packaged `verification_tests.json`)
- Round-26 closure suites (gate_typed_shapes, verification_tests_strict, acquisition_budget,
  shared_strict_decoder, packaging_dirty_disposition) → **52 passed**.
- Complete F012/review block (46 test_run_manifest*.py + persisted schemas + round13 + the full
  review/archive/snapshot/gate batch incl. all round 24-26 suites) → all pass.
- Complete F010/F011/Evidence block (11 files) → all pass.
- Authoritative CLI (`tests/test_do_job_flow.py` + `tests/cli`, excluding the two PRE-EXISTING
  doc-path suites) → all pass.
- Docs consistency (incl. `TestF012Round26IsPinned`) → all pass.
- compileall exit 0; `bash -n scripts/make_review_zip.sh` clean; `git diff --check` clean;
  integrity check passed (fail_count 0).

### Diagnostic (nonauthoritative; NOT in verification_tests.json)
- `test_stream_export_e2e.py::...streams_under_evidence_current` fails on a stale fixture (omits
  `scripts/stage_review_evidence.py`); it fails identically at the pre-round-24 base and is unrelated.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch locally committed,
unpushed, unmerged.
