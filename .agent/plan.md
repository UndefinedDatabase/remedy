# Plan — Steps 13761-13960 — F012 Evidence Semantics Authority Round 31

## Round 31 binding decision

Reviewed `remedy-review-20260719-193515-READY_FOR_REVIEW.zip` (SHA `f6ad4f23...882865`, Evidence
`3316418eb96477f9`, prior `ee7cc57fcbe5acdd`, base `37053ee`, HEAD `095506b`). Round 30 closed the
main FV-reproducibility path but left two fail-open holes; F2/F3/F6 remain on the same
Evidence-semantics boundary. Close this coherent block. F4/F5/F7 stay explicitly OPEN, untouched.

Non-overlapping Round-31 scopes, one commit each:

1. **Fail-closed tri-state final-verifier reproducibility (F1A/F1B).** Reproducibility is a tri-state
   record `{checked, reproducible, status in VERIFIED_EQUAL|VERIFIED_MISMATCH|NOT_CHECKED|
   PRODUCER_ERROR, problems}`. `build_manifest` ALWAYS verifies when Evidence is present (no unchecked
   `true`), so the standalone manifest can never claim reproducibility it did not perform. Producer
   unavailable / import-fail / raise / materialization-fail / None / non-object → PRODUCER_ERROR,
   reproducible False, BLOCKED_EVIDENCE, bounded reason — never translated to success. READY requires
   VERIFIED_EQUAL. do_job_flow's hand-FV fixtures migrated to producer-generated reports.
2. **Token-truth / token-status authority (F2).** One pure producer validates token_truth (nonempty,
   strict, typed object, schema version, enum confidence/source, int-not-bool nonneg counts, finite
   nonneg cost, totals coherence, call/coverage/availability coherence, model identity from Evidence)
   and regenerates token_status; a supplied/embedded token_status must equal regeneration or block.
   Consumed by the verifier + gate validator. Mutation suite covers every rejection.
3. **Complete manual-completion typed semantics + production integration (F3).** One normalized typed
   contract (exact scalar type, no-bool-for-int, enums, nonempty, ranges, cross-field/cross-artifact
   equality) for every consumed manual-completion artifact; the canonical `manual_attestation`
   producer is the documented supported creation boundary (operator CLI entry), not test-only. Full
   scalar mutation matrix.
4. **Total gate evaluation (F6).** `evaluate_ready_gate_matrix` finishes closed-schema validation
   before any semantic op; no set/list/sorted/membership/arith/.get on unvalidated values; one
   malformed gate never hides others; never raises. Recursive mutation matrix.
5. **Truthful Round-31 docs + operator state.** Authority: a report is authoritative only when the
   producer ran successfully and exact equality was verified; unchecked/failed regeneration is never
   reproducible. F4/F5/F7 kept explicitly open.

## Constraints (unchanged)

Zero provider calls; manual only; no job-flow/job-run/db/network/docker/new deps. Small local commits,
never amend/squash. No push/PR/merge/main. Do not start F017. Fresh Evidence linked
`3316418eb96477f9` satisfying the real verifier with VERIFIED_EQUAL; one READY ZIP; then stop. F012
`[~]`, F017 `[ ]`. F4 (no-clobber publication), F5 (fail-closed git status), F7 (integration-file
termination) remain OPEN and are not touched this round.
