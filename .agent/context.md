# Context

## Active Branch
`feature/step12-risk-classification`

## PR
None yet.

## Scope
Step 12: non-blocking risk classification.  Only classifies and surfaces risk.
No execution changes, no prompts, no overwrite logic.

## Key files changed
- packages/orchestration/patch_intent.py: classify_risk(), risk_level field
- apps/cli/main.py: patch_intent_risks metadata key, risk in explanations
- tests/test_patch_intent.py: TestClassifyRisk (8 tests), risk assertions
- .agent/decisions.md: 3 new decisions
