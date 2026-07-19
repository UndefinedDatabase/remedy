# Live Review — Steps 13561-13760 — F012 Evidence Authority Round 30 (PARTIAL: primary blocker closed)

## Verdict (reviewer-owned)
**PENDING** — the primary Round-29 blocker (Finding 1) is fixed; Findings 2–7 remain OPEN and are
named follow-ups below. Not externally accepted.

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Every accepted Round-29 improvement preserved.

External review of `remedy-review-20260719-170939-READY_FOR_REVIEW.zip` (SHA `b29826a4...f3e21e`,
Evidence `ee7cc57fcbe5acdd`, prior `be06ea70dd607523`, HEAD `37053ee`) returned SEVEN findings.

### Closed this round
- **F1 (primary blocker) — final verifier report not reproducible.** The coordinator now REGENERATES
  the final_verifier_report from the immutable staged Evidence snapshot with the real
  `build_final_verifier_report` and REQUIRES the packaged report to be semantically equal, else
  BLOCKED_EVIDENCE (`build_review_zip` passes `verify_final_verifier=True`;
  `regenerate_final_verifier` materializes the snapshot to a private temp dir and runs the pure
  producer; the manifest records `final_verifier_reproducible`). A hand-written verdict / manual flag /
  attested-task list / completeness map / commit-execution status / recommended action can no longer
  pass. A new product module `packages/orchestration/manual_attestation.py` is the single producer of
  a legitimate zero-provider manual completion, emitting every field the current verifier requires
  (complete token_accounting kind/reason, manual_repair_provenance timestamp/workspace_scope/
  task_scope_known, the completeness artifacts, valid nonempty token_truth). The authoritative e2e
  fixture is migrated to a producer-generated report; a reproducibility suite proves a fresh rebuild
  equals the packaged report and that editing any authoritative field blocks.

### OPEN — named follow-ups (NOT addressed this round; must be closed before F012 acceptance)
- **F2 — token_truth/token_status authority.** token_truth validity-when-present and full
  token_status regeneration/coherence not yet enforced as a standalone pipeline.
- **F3 — complete manual-completion typed scalar semantics.** The Round-29 container validation is not
  yet extended to full scalar typing (no-bool-for-int, enums, ranges, cross-artifact equality).
- **F4 — core no-clobber collision safety.** Collision safety still lives partly in the shell; the
  direct Python `--out` overwrite and the final status-bearing `mv` path are not yet closed in a
  shared Python coordinator.
- **F5 — fail-closed Git-status snapshots.** `_git_status_records()` still returns `[]` on failure
  (fail-open); a typed OK/FAILED/… result that blocks READY is not yet implemented.
- **F6 — total gate evaluation.** `evaluate_ready_gate_matrix` is not yet proven total against a
  recursive malformed-value mutation matrix.
- **F7 — full-integration file single-invocation termination.** Not yet investigated/pinned.

## Verification (this round)

- New/affected suites pass: test_review_authoritative_e2e (producer-migrated),
  test_review_final_verifier_reproducible (new), test_review_manual_completion_shapes,
  test_final_verifier, test_final_audit_evidence, do_job_flow packaging status suites — green.
- The full acceptance matrix is re-run before packaging; counts recorded in verification_tests.json.

## Status

F012 `[~]` — **not externally accepted**; the primary blocker is closed but Findings 2–7 remain open.
F017 `[ ]` not started. Branch locally committed, unpushed, unmerged. Authority model:
staged Evidence bytes → real producers → regenerated final verifier → gates → archive plan →
immutable ZIP; a supplied final-verifier JSON is never authority.
