# Plan

## Goal
Step 12.5: Risk Contract Hardening

## Status
COMPLETE — committed, pushed, PR #12 updated

## Steps
1. [x] Confirm branch: feature/step12-risk-classification (same branch, Step 12.5 is in-scope hardening)
2. [x] patch_intent.py: RISK_* constants + RISK_LEVELS; __post_init__ validation; blank-line format; RISK_UNKNOWN conservatism doc
3. [x] tests/test_patch_intent.py: constants in TestClassifyRisk; TestPatchDryRunResultValidation (3 tests); multi-result blank-line assertion
4. [x] tests/test_cli_main.py: TestPatchIntentRisksCLI — risks stored, all in RISK_LEVELS, risk line in output
5. [x] docs/architecture.md: updated risk section with constants, RISK_UNKNOWN note, metadata table
6. [x] .agent/decisions.md: 4 new decisions added
7. [x] 384 tests pass; committed dd23a79; pushed; PR #12 updated

## Branch
feature/step12-risk-classification

## PR
#12 (open)
