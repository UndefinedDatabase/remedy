# Live Review — Steps 13161-13360 — F012 hardening round 28 (coherence + invocation-binding closure)

## Verdict (reviewer-owned)
**PENDING** — F012 hardened (4 coherence/invocation/crash findings + 1 fixture maintenance), awaiting
re-review (NOT accepted).

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Every accepted F012 behavior preserved.

External review of `remedy-review-20260719-124709-READY_FOR_REVIEW.zip` (SHA
`7a452c42...d898d1`, Evidence job `a3d937ec1835eb93`, linked prior `ebe675ec74f20c1a`, HEAD
`8c32724`) returned FOUR findings plus one isolated fixture failure.

- **F1** — a token producer projection could contradict `token_status`. One shared projection mapping
  requires token_measurement, its actual_summary and top-level token_actual_summary to EQUAL the
  authoritative token_status for every overlapping field; a disagreement blocks; the low/null summary
  carries no projection.
- **F2** — `VerificationTestsV1` diverged from the `_run_verifications` producer. A repeated command
  is now legitimate (unique run ids stay mandatory), the top-level command must equal
  `" && ".join(run commands)` and exit_code must be 0 iff every run exited 0, and the timestamp must
  be a real timezone-aware ISO-8601 datetime (date-only / naive blocks).
- **F3** — the packaging-output classifier matched an invocation-INDEPENDENT filename grammar, hiding
  a stale/forged root ZIP. It is now bound to the EXACT set of outputs the current invocation
  generates, passed from make_review_zip.sh through both builders; only exact membership classifies.
- **F4** — a valid-JSON job_flow with a malformed nested shape (final_audit a list, target_guard a
  list) crashed the manifest builder with AttributeError. The minimal closed shape is validated before
  any nested read; a wrong inner type appends a validation error and never raises.
- **Fixture (maintenance, separate commit)** — the stream-export review-ZIP fixture is repaired for
  the current pipeline: it copies every helper make_review_zip.sh invokes and models an internally
  consistent git-backed job (authority set {docs/README.md} agreed across subject, content proof,
  final verifier and change-provenance gate). No assertion weakened.

## Verification

### Authoritative (each command recorded in the packaged `verification_tests.json`)
- Round-28 affected suites — gate_typed_shapes, verification_tests_strict, packaging_dirty_disposition,
  malformed_nested_evidence, stream_export_e2e (vr-0001) — all pass.
- Complete F012/RunManifest (vr-0002), complete Review/Packaging (vr-0003, includes all round 24-28
  review suites), complete F010/F011/Evidence (vr-0004), CLI (vr-0005), Docs (vr-0006) — all pass.
- compileall exit 0; `bash -n scripts/make_review_zip.sh` clean; `git diff --check` clean; integrity
  check passed (fail_count 0).

## Status

F012 `[~]` — **not externally accepted**. F017 and later not started. Branch locally committed,
unpushed, unmerged. Per the F012 closure section of `docs/roadmap/features/T0_F012.md`, further
generic hardening is follow-up maintenance and does not reopen F012.
