# Live Review — Steps 5901-5960 — F004 — Raw stream evidence

Reviewer: external final reviewer (independent; owns verdict).

## Verdict

**`PASS_WITH_RISKS — ACCEPTED`.** F004 is externally accepted. F001/F002/F003
are accepted and merged (PR #123, merge commit `663aeb0`). F004 is ready for
commit, push, PR and merge.

## Branch / Base

- Branch: `feature/f004-raw-stream-evidence`
- Base/HEAD before commit: `663aeb0a140d475bde805daddc5778474408dd3e`

## Scope

F004 — Raw stream evidence. Opt-in `--stream-evidence` uses Claude CLI
`stream-json`, redacts before any raw byte is persisted, writes bounded raw
JSONL plus normalized run events, and lets every normalized event be traced back
to its raw line/byte offset. The default provider path remains the accepted F003
JSON mode.

Supporting evidence-infrastructure hygiene (not a new feature or gate): job
evidence defaults to the hidden `.data/evidence_exports/<JOB_ID>` location, the
existing job evidence index records repository/branch/commit/alignment, review-zip
selection is index-driven (`--job-id`, `--include-recent`), the artifact contract
recomputes stream-artifact hashes and sizes, and the shareable review manifest
carries no machine-specific absolute paths.

## Task scopes (manual completion, non-overlapping, 28 content-proof files)

- T001 stream wrapper, redaction and parser (6) — `stream_evidence.py`,
  `test_stream_evidence.py`, four recorded stream fixtures.
- T002 provider, CLI and trace integration (8) — `pingpong_provider.py`,
  `pingpong_loop.py`, `pingpong_job.py`, `agent_run_trace.py`, three CLI files,
  `test_stream_evidence_integration.py`.
- T003 evidence storage, index, artifact contract and selection (10) —
  `data_paths.py`, `evidence_index.py`, `job_evidence.py`,
  `artifact_contract_gate.py`, `select_review_evidence.py`,
  `make_review_zip.sh`, `build_review_manifest.py`, `test_evidence_index.py`,
  `test_artifact_contract_gate.py`, `test_stream_export_e2e.py`.
- T004 shareable manifest privacy and packaging test contract (3) —
  `test_review_zip_hygiene.py`, `test_review_manifest_privacy.py`,
  `test_do_job_flow.py`.
- T005 roadmap status note (1) — `docs/roadmap/STATUS.md`.

## Verification (accepted)

- Accepted battery — 362 passed: `test_stream_evidence.py`,
  `test_stream_evidence_integration.py`, `test_evidence_index.py`,
  `test_artifact_contract_gate.py`, `test_stream_export_e2e.py`,
  `test_review_zip_hygiene.py`, `test_review_manifest_privacy.py`,
  `test_do_job_flow.py`.
- Accepted regression battery — 600 passed: `test_token_truth.py`,
  `test_token_actuals.py`, `test_final_verifier.py`, `test_job_evidence.py`,
  `test_repair_attest.py`, `test_change_provenance_gate.py`,
  `test_pingpong_cli.py`, `test_manual_completion_bundle.py`,
  `test_provider_timeouts.py`, `test_provider_evidence_integration.py`.
- Nine verification runs in the manual completion job: 962 passed, 0 failed.
- compileall, `bash -n scripts/make_review_zip.sh`, `git diff --check` clean.

## Accepted package

- Job `621369b56e834cd4`; hidden evidence `.data/evidence_exports/621369b56e834cd4`.
- ZIP `remedy-review-20260709-225052-READY_FOR_REVIEW.zip`
  sha256 `9660884805a76558ac793fb08645766183b51ec97a1e169a87c11b236de77130`.
- history: `c6d7ca0e716d4d3d`, `d082c9177359488f`.
- All gates as recorded in `.agent/plan.md`; commit_execution_gate =
  NEEDS_HUMAN_APPROVAL; human final reviewer required.

## Supplemental runtime evidence (separate; not the review subject)

Authoritative live Sonnet smoke in a temporary repository outside this checkout:
job `f22d69ed4c1f491b`, run `54d4adc45d964812`, exactly 2 provider calls (1
Builder + 1 Reviewer, `max_rounds=1`, `repair_rounds=0`, no retries or parse
retries). Distinct per-attempt directories (`streams/<role>/round-01/attempt-01`);
2/2/2 provider/actual/cost calls; USD 0.206335; all 10 raw byte offsets resolve;
6 production trace events with `trace_source=normalized_raw_stream` and no
reconstructed duplicates; artifact contract recomputed all 4 hashes/sizes (PASS);
0 cap events, 0 timeouts; the canonical checkout was not mutated. Archive outside
this repository: `remedy-f004-final-smoke-20260709-203130.tar.gz`
sha256 `b884c62c0bec858f9995e80eff633f4b37fefbe974cf32d6b12ba4f931f11bf4`.

## Status

F004 accepted and ready for commit/push/PR/merge. F005 begins only after the
F004 merge. F006 untouched.
