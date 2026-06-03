# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 415-424: Mission Control design fit — complete.

## Completed
- docs/ui-target.md: written target, proportions, QA checklist
- Right panel: flexbox compact stack, lighter card styles
- ProjectSummaryCard v2: chip layout, accessible button, mini card aesthetic
- UI drift tests: 13 tests preventing design regression
- Responsive test updated for flexbox panel layout

## Resource-Safety Rules (permanent)
- Never run pytest in background
- Always use scripts/remedy_pytest.sh for pytest execution
- Full pytest tests/ at most once per worker block

## Constraints
- UI remains read-only
- No fake data in UI
- No major redesign — refinement only

## Note on live_review.md
R-18001: detailed review history (Steps 321-414) was truncated from working file across sessions. Detailed history preserved in git (67cc20f and earlier commits). This is expected for .data/ (gitignored) files that get recreated each session.

## Recommended Next Block
Steps 425-432 — Real Ollama Run Set And Prompt Improvement
