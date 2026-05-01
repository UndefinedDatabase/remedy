# Context

## Active Branch
`feature/step12-risk-classification`

## PR
#12 (open — Steps 12–12.6 are in-scope hardening continuations)

## Scope
Step 12.6: dry-run boundary + risk coverage hardening. No behaviour changes beyond:
- generate_dry_run_preview rejects paths outside repo_root (RuntimeError)
- truncate_preview() helper in patch_intent.py; CLI uses it instead of inline [:2000]
- CLI risk test tightened: assert exact RISK_UNKNOWN value in stdout
- diff_preview CLI omission documented
Non-blocking; no execution gates, no prompts, no overwrite logic.

## Key files changed
- packages/orchestration/patch_intent.py: boundary check in generate_dry_run_preview, truncate_preview helper, module docstring
- apps/cli/main.py: import + use truncate_preview; comment on diff_preview omission
- tests/test_patch_intent.py: TestGenerateDryRunPreviewBoundary (4 tests), TestTruncatePreview (5 tests), updated imports
- tests/test_cli_main.py: exact RISK_UNKNOWN assertion in TestPatchIntentRisksCLI
- docs/architecture.md: diff_preview omission note, boundary check constraint, truncate_preview note
