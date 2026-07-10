# Plan — Steps 5901-5960 — F004 — Raw stream evidence

## Goal
Opt-in `--stream-evidence` uses Claude CLI `stream-json`, redacts before any raw
byte is persisted, writes bounded raw JSONL plus normalized run events, and lets
every normalized event be traced back to its raw line/byte offset. Default
behavior stays the F003 JSON mode.

## Current Step
**F004 ACCEPTED — `PASS_WITH_RISKS`. Ready for commit / push / PR / merge.**
T001, T002, T003 done; evidence-storage and selection hygiene done; live smoke
done; five-scope manual completion packaged and externally accepted.

## Delivered
- `stream_evidence.py` — bounded, redacted stream capture; inline normalization;
  raw line/byte offset backreferences; honest 50 MB cap (terminates a live
  provider instead of draining it); real wall-clock timeout with process-group
  TERM/KILL; bounded concurrent stderr drain.
- Provider/CLI: opt-in `--stream-evidence` (stream-json + `--verbose`); default
  stays `--output-format json` (accepted F003 behaviour). Threaded through
  `run_pingpong` → `run_job` → `do run` / `do job-run`. Per-attempt stream
  directories (`streams/<role>/round-NN/attempt-NN`); a failed attempt still
  references the artifacts it produced; the version probe is pinned to staging.
- Trace: `agent_run_trace` consumes normalized `run_events.jsonl` when present
  (`normalized_raw_stream`), else the existing reconstruction
  (`reconstructed_legacy_evidence`); API retries stay visible; no reconstructed
  duplicates of stream-owned kinds.
- Evidence hygiene: hidden `.data/evidence_exports/<JOB_ID>` default; the
  existing job evidence index extended (repo/branch/commit/status/changed files);
  `make_review_zip.sh --job-id / --include-recent`; index-driven selection that
  never picks by mtime and never substitutes another job; honest NO_EVIDENCE;
  deprecated root-directory fallback warns.
- Stream-artifact integrity: `artifact_contract_gate` recomputes SHA-256 and
  byte size for every referenced stream artifact against the exported listing.
- Shareable manifest: no machine-specific absolute paths; correct manual-
  completion Job ID and final audit status.

## Evidence (accepted)
- External verdict: **`PASS_WITH_RISKS — ACCEPTED`**.
- Manual completion job `621369b56e834cd4` (5 non-overlapping scopes, 28 content-
  proof files, zero provider calls). Hidden evidence:
  `.data/evidence_exports/621369b56e834cd4`.
- ZIP: `remedy-review-20260709-225052-READY_FOR_REVIEW.zip`
  (`evidence/current` = the F004 job; two earlier same-repo F004 exports under
  `evidence/history/`: `c6d7ca0e716d4d3d`, `d082c9177359488f`).
- Gates: package_status READY_FOR_REVIEW · evidence_authoritative true ·
  review_bundle_integrity PASS · alignment PASS · final_verifier PASS_WITH_RISKS ·
  artifact_contract_gate PASS · change_provenance_gate PASS · fresh_evidence_gate
  PASS · runtime_integration_gate PASS · commit_execution_gate
  NEEDS_HUMAN_APPROVAL · content proofs 28 · hash mismatches [] · missing proofs
  [] · uncovered files [] · completion provider calls 0.
- Supplemental live smoke (AUTHORITATIVE): job `f22d69ed4c1f491b`,
  run `54d4adc45d964812`, exactly 2 provider calls (1 Builder + 1 Reviewer,
  `max_rounds=1`, `repair_rounds=0`, 0 retries, 0 cap events, 0 timeouts),
  USD 0.206335, 10/10 offsets resolved, 6 production normalized trace events,
  0 reconstructed duplicates, target not mutated. Evidence:
  `.data/evidence_exports/f22d69ed4c1f491b` (evidence export only, no provider
  call). Archive outside this repository:
  `remedy-f004-final-smoke-20260709-203130.tar.gz`
  sha256 `b884c62c0bec858f9995e80eff633f4b37fefbe974cf32d6b12ba4f931f11bf4`.

## Tests
Accepted battery (362 passed): `test_stream_evidence.py`,
`test_stream_evidence_integration.py`, `test_evidence_index.py`,
`test_artifact_contract_gate.py`, `test_stream_export_e2e.py`,
`test_review_zip_hygiene.py`, `test_review_manifest_privacy.py`,
`test_do_job_flow.py`. Accepted regression battery (600 passed):
`test_token_truth.py`, `test_token_actuals.py`, `test_final_verifier.py`,
`test_job_evidence.py`, `test_repair_attest.py`, `test_change_provenance_gate.py`,
`test_pingpong_cli.py`, `test_manual_completion_bundle.py`,
`test_provider_timeouts.py`, `test_provider_evidence_integration.py`.
Nine verification runs in the manual completion: 962 passed, 0 failed.
compileall / `bash -n` / `git diff --check` clean.

## Next
Commit, push, open the F004 PR, apply the Open PR Gate, merge. After merge start
**F005 — Enforced structured outputs** on `feature/f005-structured-outputs`.

## Hard Rules
No Fable; no nested Builders/Reviewers/subagents; no `job-flow`/`job-run` for
implementation. Do not touch F006. F003 accepted/merged (PR #123, merge commit
`663aeb0`). Deferred hardening notes are in `.agent/decisions.md`.
