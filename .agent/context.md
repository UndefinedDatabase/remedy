# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 399-406: Project-level brain — complete.

## Completed
- ProjectBrainSummary: job counts, focus, blockers, touched files, token usage, next step
- Pattern detection: repeated stop reasons, frequently touched files, repeated parse failures
- Project model quality: confidence tiers (low/medium/high), fixture vs real distinction
- Memory suggestions: require approval, bounded to 10, derived from patterns
- CLI: project.summary command in catalog with text + JSON output
- Dashboard: project_summary field with compact safe metadata
- TypeScript: RemedyProjectSummary interface, normalization, null fallback

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
Steps 407-414 — Real Ollama Run Set And Prompt Iteration
