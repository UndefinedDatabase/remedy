# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 407-414: Project Brain productization — complete.

## Completed
- ProjectSummaryCard: visible in right panel, shows job counts, blockers, patterns, model confidence
- CLI project summary: 9 contract tests (catalog, JSON shape, safety, patterns, suggestions)
- Model quality linkage: confidence derived from real builder events, not hardcoded
- Stronger patterns: test failure, permission block, provider unavailable, repair exhaustion
- Memory suggestions: titles shown in CLI, require approval, bounded
- docs/project-brain.md: plain language, commands, patterns, confidence levels

## Resource-Safety Rules (permanent)
- Never run pytest in background
- Never run multiple pytest commands in parallel
- Always use scripts/remedy_pytest.sh for pytest execution
- Full pytest tests/ at most once per worker block

## Constraints
- UI remains read-only
- No auto-write to project memory without approval
- source_apply requires permission + approved intent

## Recommended Next Block
Steps 415-422 — Real Ollama Run Set And Prompt Iteration
