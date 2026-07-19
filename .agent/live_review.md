# Live Review — Steps 12961-13160 — F012 hardening round 27 (real token shapes, complete verification typing, safe boundaries)

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (5 token/verification/acquisition/dirty/decoder findings), awaiting re-review (NOT accepted).

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Every accepted F012 behavior preserved.

External review of `remedy-review-20260718-213237-READY_FOR_REVIEW.zip` (SHA
`9bfe1e5abdedc8d004164b7101cb7c111bef967607cca858c9a8cb11384dd850`, Evidence job
`ebe675ec74f20c1a`, linked prior `a67d0c3f0513bd11`, HEAD `7fa4466`) returned FIVE findings.

- **F1** — the Round-26 schema rejected the REAL high/mixed-confidence token summary. One exact
  `_ACTUAL_TOKEN_SUMMARY` matches `final_verifier._token_measurement_summary`; reused for
  token_measurement.actual_summary and top-level token_actual_summary; null accepted where the
  producer emits it; unknown/wrong-type still blocks; top-level may not contradict the nested block.
- **F2** — `VerificationTestsV1` is fully typed to `job_evidence._run_verifications`: verification
  type/command/timestamp/run_id/stdout_summary typed, per-run nonnegative counts (a negative offset
  blocks), safe sorted unique test paths, unique run ids/commands, secret/path/control scan.
- **F3** — a per-member/aggregate acquisition overflow BLOCKS (charged from a trusted anchored size
  before reading) and can never become a silent `(None, "")`; absence/symlink/torn distinguished.
- **F4** — generated packaging outputs identified by EXACT repository-root path grammar; nested files
  and root lookalikes stay in the dirty subject.
- **F5** — job_flow.json, manual_repair_provenance.json, the packaged manifest.json and the
  NO_EVIDENCE root manifest decode through the shared strict decoder; duplicate/NaN/Infinity/bad-UTF8/
  non-object blocks, no silent fallback.

## Verification

### Authoritative (each command recorded in the packaged `verification_tests.json`)
- Round-27 affected suites (gate_typed_shapes, verification_tests_strict, acquisition_budget,
  shared_strict_decoder, packaging_dirty_disposition) — all pass.
- Complete F012/RunManifest (vr-0002), complete Review/Packaging (vr-0003, includes all round 24-27
  review suites), complete F010/F011/Evidence (vr-0004), CLI (vr-0005), Docs (vr-0006) — all pass.
- compileall exit 0; `bash -n scripts/make_review_zip.sh` clean; `git diff --check` clean; integrity
  check passed (fail_count 0).

### Diagnostic (nonauthoritative; NOT in verification_tests.json)
- `test_stream_export_e2e.py::...streams_under_evidence_current` fails on a stale fixture (omits
  `scripts/stage_review_evidence.py`); fails identically at the pre-round-24 base, unrelated.

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch locally committed,
unpushed, unmerged.
