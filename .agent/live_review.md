# Live Review — Steps 13361-13560 — F012 hardening round 29 (systemic class closure)

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (5 complete-class findings), awaiting external re-review (NOT accepted).

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Every accepted F012 behavior preserved, including Round 28's externally-
verified VerificationTests corrections.

External review of `remedy-review-20260719-134026-READY_FOR_REVIEW.zip` (SHA
`6d1a28a7...e9712`, Evidence job `be06ea70dd607523`, linked prior `a3d937ec1835eb93`, HEAD
`925c6fa`) returned FIVE findings — each a class Round 28 fixed only by example.

- **F1** — the packaged token block was not reproducible from the current producer, and impossible
  confidence/summary/note combinations passed. One shared module
  (`token_measurement.token_measurement_summary`) is imported by both `final_verifier` and the gate;
  the gate requires the block to equal a fresh producer rebuild plus its top-level projections. No
  duplicated field list remains to drift.
- **F2** — manual-only Evidence still threw raw `TypeError`/`AttributeError` on nested fields Round 28
  did not name. One shape contract (`_MC_SHAPES` + `_read_mc`) validates every consumed collection/
  record before iteration; a table-driven mutation matrix proves none throws and each invalidates.
- **F3** — the generated-output authority was caller-supplied, so a declared source path hid a dirty
  file. Eligibility is now a repository-ROOT packaging-output shape, `build_review_zip.py` derives the
  set from its own `--out`/`--manifest-rel`, and `make_review_zip.sh` refuses (exit 3) a tracked
  manifest/ZIP collision byte-identically.
- **F4** — `git status` porcelain paths were corrupted (`_dirty_files` stripped the leading status
  column). Parsing now uses `--porcelain=v1 -z` and preserves both status columns and the exact path.
- **F5** — the stream-export E2E depended on inherited `PYTHONPATH`. The child now gets an intentional
  `PYTHONPATH=<repo root>` from a cleared environment and passes under `env -u PYTHONPATH`.

## Verification

### Authoritative (each command recorded in the packaged `verification_tests.json`)
- Round-29 affected suites (gate_typed_shapes, verification_tests_strict, packaging_dirty_disposition,
  packaging_collision_safety, malformed_nested_evidence, manual_completion_shapes, git_porcelain_paths,
  stream_export_e2e) — all pass.
- Complete F012/RunManifest, complete Review/Packaging (incl. round 24-29 review suites), complete
  F010/F011/Evidence, CLI, Docs — all pass.
- The stream E2E also passes with the parent `PYTHONPATH` unset (`env -u PYTHONPATH`).
- compileall exit 0; `bash -n scripts/make_review_zip.sh` clean; `git diff --check` clean; integrity
  check passed (fail_count 0).

## Status

F012 `[~]` — **not externally accepted**. F017 `[ ]` and later not started. Branch locally committed,
unpushed, unmerged. Per the F012 acceptance-criteria section of `docs/roadmap/features/T0_F012.md`,
acceptance is a reviewer decision pending external confirmation; further generic hardening is
follow-up maintenance.
