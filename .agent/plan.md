# Plan — F012 Versioned PE Schema, Authoritative Evidence, Publication Capability Round 38

Round-37 contracts FROZEN. External review returned six bounded findings. Round 38 closes
exactly these and broadens no further.

## Scope 1 — complete versioned ProviderTokenEvidence

Round 37 validated semantic relationships but left three gaps:

- F1: `total_cost_usd` present without `cost_call_count` → silently accepted (pass branch).
  Fix: raise `TokenEvidenceError` — cost must carry its call-count provenance.
- F2: generic `actual_model` accepted by validation, used as per-task fallback, but discarded
  at aggregate level. Fix: reject `actual_model` as ambiguous — require `builder_actual_model`
  or `reviewer_actual_model` explicitly.
- F3: `actual_model_verified=true` with `provider_call_count=0` accepted. Fix: require
  `provider_call_count > 0` when `actual_model_verified=true`.

Tests: each exact reproduction → `TokenEvidenceError` → PRODUCER_ERROR → BLOCKED_EVIDENCE.

## Scope 2 — machine-verifiable authoritative and diagnostic test Evidence

- F4: diagnostic broad-run baseline comparison is self-asserted (`baseline_match: true`).
  Fix: produce machine-validated comparison — sorted failure node IDs, SHA-256 of failure
  sets, derived `failure_sets_equal`. Use `git archive` for baseline extraction.
- F5: authoritative test matrix incomplete. Fix: package every named file and group as
  typed verification runs with exact command, timestamps, durations, counts.

## Scope 3 — explicit anonymous-publication capability contract

- F6: O_TMPFILE availability is implicit. Fix: typed capability probe returning
  SUPPORTED / UNSUPPORTED_OS / UNSUPPORTED_FILESYSTEM / LINKAT_UNAVAILABLE / PERMISSION_DENIED.
  Capability-aware tests. Source `.part` cleanup ownership binding: record (st_dev, st_ino)
  before copy, unlink only if same inode.

## Commits (5, in order)

1. `fix(evidence): complete versioned PE schema and semantic matrix`
2. `fix(evidence): validated diagnostic current-vs-baseline comparison`
3. `fix(evidence): complete authoritative verification matrix`
4. `fix(evidence): publication capability probe and source-cleanup ownership`
5. `docs(f012): truthful Round-38 documentation and operator state`

## Constraints (unchanged)

Zero provider calls; manual only; no job-flow/job-run/db/network/docker/new deps. Small local
commits, never amend/squash. No push/PR/merge/main. Do not start F017. Fresh Evidence linked to
prior `r37_anonymous_inode_semantic_provider`, VERIFIED_EQUAL, git OK; one READY ZIP; then stop.
