# Plan — F012 Round 39 — COMPLETE

Round-38 contracts FROZEN. External review returned four bounded findings. Round 39 closed
exactly these four. All scopes complete, all tests green, Evidence generated.

## Scope 1 — closed versioned ProviderTokenEvidenceV1

Round 38 added semantic cross-field validation but left the input schema open:

- No schema_version required (missing version passes).
- Wrong schema_version passes (e.g. "999.0").
- Unknown trust-bearing fields accepted (e.g. "claimed_actual_cost_usd").
- Unknown execution_mode accepted (e.g. "banana").
- Missing `provider_call_count` on non-manual PE causes inference (`+= 1`).

Fix: Create `packages/orchestration/provider_token_evidence.py` with:
- `PROVIDER_TOKEN_EVIDENCE_SCHEMA_VERSION = "1.0.0"`
- Closed allowed field set
- Required fields by execution mode
- Supported execution modes enum
- `validate_provider_token_evidence(pe, ctx)` — the single entry point

In `token_truth.py`:
- Call new validator at the start of PE processing (before `validate_provider_evidence`)
- Remove `agg_provider_call_count += 1` fallback when `provider_call_count` absent
- Require `provider_call_count` in all non-manual PE

Tests: complete omission/mutation matrix + all 5 external reproductions.

## Scope 2 — diagnostic producer and validator

Round 38's `diagnostic_broad_run.json` was captured at afe8394, not final HEAD f3ed24f,
and has no production consumer.

Fix: Create `packages/orchestration/diagnostic_comparison.py` with:
- `produce_diagnostic_comparison(repo_root, base_commit, current_commit, command, ...)` —
  extracts both commits via `git archive`, runs the exact same command in both,
  produces sorted failure IDs, SHA-256 hashes, derived comparison.
- `validate_diagnostic_comparison(comparison, expected_head)` — recomputes counts,
  sortedness, set differences, hashes, `failure_sets_equal`, commit == expected_head.

The Evidence bundle calls the producer; the final verifier calls the validator.

## Scope 3 — complete authoritative verification matrix

Round 38's verification_tests.json recorded 17 runs / 583 passed but handoff said 578.
Missing: reviewer-confirmed suites, full F012/RunManifest group, Review/Packaging group,
F010/F011/Evidence group, CLI group, Docs group. No real timestamps.

Fix: Extend the verification_runs to cover all listed suites. Each run records
real start/end timestamps (ISO-8601), duration, exact command, environment qualifiers,
exit code, passed/failed/skipped, and failing node IDs when applicable. Top-level
totals are the exact sum of individual runs.

## Scope 4 — capability-integrated publication

`probe_anonymous_publication_capability()` has no production callers.

Fix:
- In `build_review_zip.py`: probe the final parent directory before publication;
  record result in coordinator JSON output; SUPPORTED required for publication;
  unsupported → typed error, zero public outputs.
- In `make_review_zip.sh` output parsing: record capability in `.review_zip_manifest.json`.
- Capability-aware tests: on supported → real publication + concurrency + shell E2E;
  on unsupported → typed status, nonzero result, zero public/part files.
  Tests green in both environments (no skips).

## Commits (in order)

1. `fix(evidence): closed versioned ProviderTokenEvidenceV1 with complete mutation matrix`
2. `fix(evidence): diagnostic producer/validator with comparable archive execution`
3. `fix(evidence): complete authoritative verification schema and matrix`
4. `fix(evidence): capability-integrated coordinator and capability-aware tests`
5. `docs(f012): truthful Round-39 documentation and operator state`

## Constraints (unchanged)

Zero provider calls; manual only; no job-flow/job-run/db/network/docker/new deps. Small local
commits, never amend/squash. No push/PR/merge/main. Do not start F017. Fresh Evidence linked to
prior `r38_versioned_pe_publication_capability`, VERIFIED_EQUAL, git OK; one READY ZIP; then stop.
