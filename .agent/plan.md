# Plan

## Goal
Step 12.5: Risk Contract Hardening

## Status
IN PROGRESS

## Steps
1. [x] Confirm branch: feature/step12-risk-classification (same branch, Step 12.5 is in-scope hardening)
2. [ ] patch_intent.py: add RISK_* constants + RISK_LEVELS frozenset; __post_init__ validation on PatchDryRunResult; blank line between multi-result blocks; document unknown conservatism
3. [ ] tests/test_patch_intent.py: use constants in TestClassifyRisk; cover __post_init__ invalid risk; update multi-result format test; add unknown docstring/comment coverage
4. [ ] tests/test_cli_main.py: add CLI test proving patch_intent_risks stored + all values in RISK_LEVELS + risk line in output
5. [ ] docs/architecture.md: update risk section — explicit constants, unknown is conservative
6. [ ] .agent/decisions.md: record key decisions
7. [ ] Self-review, run tests (target 385+), commit, push

## Branch
feature/step12-risk-classification

## PR
#12 (open, same branch — Step 12.5 is a hardening continuation)
