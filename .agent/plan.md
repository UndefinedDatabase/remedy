# Plan — Steps 13561-13760 — F012 Evidence Authority Round 30 (PRODUCER-DERIVED, STAGED-BYTE-BOUND AUTHORITY)

## Round 30 binding decision

Reviewed `remedy-review-20260719-170939-READY_FOR_REVIEW.zip`
(SHA `b29826a4...f3e21e`, Evidence `ee7cc57fcbe5acdd`, prior `be06ea70dd607523`, HEAD `37053ee`).
Verdict FINDINGS. Primary blocker: the packaged `final_verifier_report.json` cannot be reproduced by
the current `build_final_verifier_report` from the packaged Evidence — the report was hand-templated,
and the real producer rejects the attestation (token_accounting.kind/reason missing;
manual_repair_provenance.timestamp/workspace_scope/task_scope_known missing) and denies completeness
for artifacts that do not exist. Replace the remaining trust model with producer-derived,
staged-byte-bound authority.

Non-overlapping Round-30 scopes, one commit each:

1. **Staged-byte final-verifier regeneration** — the coordinator materializes the immutable Evidence
   snapshot, runs the real `build_final_verifier_report` over those bytes, and REQUIRES the supplied
   `final_verifier_report.json` to be semantically equal or BLOCKS. The report is generated ONCE and
   reused for gate evaluation, planning, hashing and ZIP emission. Same path for direct Python and
   shell. Evidence producers corrected so a legitimate manual completion satisfies the real verifier.
   Scope: `_regenerate_final_verifier` in build_review_zip + the equality gate + the evidence builder.
2. **Token-truth / token-status authority** — `token_truth.json` must be valid nonempty typed JSON
   when claimed present; empty/whitespace/malformed/wrong-root does not count as complete. token_status
   fields validated (enum confidence, real nonneg int counts, finite nonneg cost, totals coherence).
   Scope: token_truth validity in the FV completeness + a shared token-status validator.
3. **Complete manual-completion typed semantics** — extend `_MC_SHAPES`/`_read_mc` from container to
   full scalar typing: exact scalar type, no-bool-for-int, enums, ranges, cross-field/cross-artifact
   equality (task_count == len(task_ids) == dirs == review ids; provider-call counts agree;
   no_provider_calls/actual_provider_available/prompt_trace_available consistency). Same normalized
   structures feed the verifier. Scope: `_MC_SCALARS` + `_read_mc` + validate_manual_completion crosschecks.
4. **Core no-clobber collision safety** — a shared Python coordinator resolves the exact final path,
   refuses every tracked/symlink/unsafe/foreign collision, creates exclusively, and publishes
   atomically; the shell cannot bypass via a later `mv`. Scope: a `safe_publish` primitive used by
   build_review_zip + make_review_zip.sh reserving all final status paths up front.
5. **Fail-closed Git-status snapshots** — `_git_status_records` returns a typed
   {status, records, diagnostic}; only OK may mean clean; every other state blocks READY and is
   recorded; one command per snapshot; malformed NUL blocks. Scope: `_git_status_snapshot` +
   classifier + manifest.
6. **Total gate evaluation** — `evaluate_ready_gate_matrix` finishes closed-schema validation before
   any semantic op; semantic validators consume normalized typed structures only; never throws; one
   malformed gate does not hide others. Scope: the semantic layer guards + a recursive mutation matrix.
7. **Whole-file integration termination** — diagnose and fix the stall in
   `test_review_package_full_integration.py`; add an order/repetition regression; leave no subprocess.
8. **Truthful Round-30 documentation + operator state** — the new authority model; correct the
   Round-29 "classes already closed" over-claim; T0_F012 section + pinned test; plan/live-review.

## Constraints (unchanged)

No provider calls; no Evidence job-flow/job-run; no database; no LLM rerun; no network; no Fable; no
subagents; no Docker; no new dependency. Manual operator work only. Small local commits, never amend/
squash prior rounds. Do not push, PR, merge, or begin F017. Fresh Evidence linked `ee7cc57fcbe5acdd`
that satisfies the REAL final verifier without hand-editing; one READY_FOR_REVIEW ZIP; then stop.
Preserve every accepted Round-29 improvement. F012 stays `[~]`, F017 stays `[ ]`, pending external
acceptance. Authority = staged Evidence bytes → real producers → regenerated final verifier →
regenerated gates → archive plan → immutable ZIP; a supplied FV/token-status JSON is never authority.
