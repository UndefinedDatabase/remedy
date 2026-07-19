# Live Review — Steps 13761-13960 — F012 Evidence Semantics Authority Round 31

## Verdict (reviewer-owned)
**PENDING** — F1A/F1B/F2/F3/F6 closed; F4/F5/F7 remain OPEN (deferred to the Packaging/System-State
round). Not externally accepted.

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Every accepted Round-30 improvement preserved.

External review of `remedy-review-20260719-193515-READY_FOR_REVIEW.zip` (SHA `f6ad4f23...882865`,
Evidence `3316418eb96477f9`, prior `ee7cc57fcbe5acdd`, base `37053ee`, HEAD `095506b`) confirmed the
delivered ZIP is reproducible, but left two fail-open holes in F1 plus F2/F3/F6 open.

### Closed this round
- **F1A/F1B** — reproducibility is a fail-closed tri-state `{checked, reproducible, status, problems}`
  (VERIFIED_EQUAL / VERIFIED_MISMATCH / NOT_CHECKED / PRODUCER_ERROR). build_manifest ALWAYS verifies
  when Evidence is present; a producer that is unavailable/imports-fail/raises/returns None/returns a
  non-object, or a materialization failure, is PRODUCER_ERROR — never translated to success. READY
  requires VERIFIED_EQUAL. do_job_flow fixtures migrated to producer-generated reports.
- **F2** — `token_authority.validate_token_truth` rejects empty/whitespace/malformed/wrong-root/
  enum-violating/incoherent token truth; wired into the manual-completion validator. token_status
  equality is transitively enforced (embedded in the VERIFIED_EQUAL report).
- **F3** — typed scalar + cross-artifact binding (task_count == len(task_ids); provider/completion
  call counts integer 0; availability/trace flags exactly False; token_accounting kind/reason manual;
  booleans rejected for integers). manual_attestation.py is the single supported creation producer.
- **F6** — evaluate_ready_gate_matrix is total: closed-schema before semantics, type-checked verdict
  membership, wrapped semantics/commit-gate/VT validation, missing-commit-gate blocks, build_manifest
  coerces malformed gate lists; recursive mutation matrix proves it never throws.

### OPEN — deferred to the Packaging/System-State round (untouched)
- **F4** — core no-clobber publication (direct --out + final status-bearing path).
- **F5** — fail-closed Git-status snapshot (_git_status_records still returns [] on failure).
- **F7** — whole-file integration termination.

## Verification

- New/affected suites pass: test_review_final_verifier_reproducible (tri-state + producer-failure),
  test_review_gate_totality, test_token_authority, test_review_manual_completion_shapes (+scalars),
  test_review_authoritative_e2e, test_do_job_flow (producer-migrated). The full acceptance matrix is
  re-run before packaging; counts recorded in verification_tests.json.
- The stream E2E also passes with the parent PYTHONPATH unset.

## Status

F012 `[~]` — not externally accepted; F1A/F1B/F2/F3/F6 closed, F4/F5/F7 open. F017 `[ ]` not started.
Branch locally committed, unpushed, unmerged. Authority: a report is authoritative only when the
producer ran successfully and exact equality was verified; an unchecked or failed regeneration is
never reproducible.
