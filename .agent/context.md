# Context

## Active Branch
`feature/step12-risk-classification`

## PR
#12 (open — Step 12.5 is in-scope hardening continuation of Step 12)

## Scope
Step 12.5: Risk contract hardening.  No behaviour changes beyond:
- RISK_* constants (single source of truth for valid levels)
- PatchDryRunResult.__post_init__ fails fast on invalid risk_level
- format_dry_run_explanations blank line between multiple blocks
- CLI test proving patch_intent_risks stored + all values valid
Non-blocking; no execution gates, no prompts, no overwrite logic.

## Key files changed
- packages/orchestration/patch_intent.py: RISK_* constants, RISK_LEVELS, __post_init__, format blank-line
- tests/test_patch_intent.py: constants in TestClassifyRisk, TestPatchDryRunResultValidation (3 tests), multi-result blank-line assertion
- tests/test_cli_main.py: TestPatchIntentRisksCLI (1 test)
- docs/architecture.md: updated risk section with constants, RISK_UNKNOWN note, metadata table
