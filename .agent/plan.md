# Plan — Steps 5571-5620: Verification Gates + Token Truth v1

## Goal
Integrate and harden four verification gate modules (final_verifier,
missing_tests_gate, scratch_file_guard, token_truth) into the evidence
pipeline. Final verifier verdict must drive final audit status and
promote_ready.

## Current Step
Step 5620: Final compile/test/smoke validation, review zip, handoff

## Completed Steps
- Step 5571: Integrate final verifier into _build_final_audit()
- Step 5572: Fix evidence completeness self-reference (final verifier)
- Step 5573: Extend missing tests gate for TS/JS source files
- Step 5574: Fix sandbox-blocked false positive in _tests_executed()
- Step 5575: Write focused tests for all gates
- Step 5576: Update live_review.md and plan.md for current run

## Constraints
No auto-approval, no target mutation, no self-merge,
no fabricated evidence, no blocking make_review_zip.sh.
