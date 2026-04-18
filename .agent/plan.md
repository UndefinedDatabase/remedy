# Plan

## Goal
Step 4 + 4.6: First Real Planner Worker + Role-Specific Configuration.

## Current Step
Step 4.6 in progress on feature/step4-ollama-planner (PR #5 open — in scope).

## Next Steps
1. provider.py: role-specific env vars (REMEDY_OLLAMA_PLANNER_MODEL, temperature, num_predict)
2. llm_planner.py: add annotate_planning_result() utility
3. CLI: timing, metadata enrichment, richer output
4. tests: env var precedence, metadata annotation
5. docs: README + architecture.md
6. Push

## Decisions
- REMEDY_OLLAMA_PLANNER_MODEL takes priority; falls back to REMEDY_OLLAMA_MODEL, then default
- annotate_planning_result in llm_planner.py — testable, provider-agnostic utility
- Timing measured in CLI (total planning time), passed to annotate_planning_result
- temperature/num_predict: read from env, passed as Ollama options only if set
