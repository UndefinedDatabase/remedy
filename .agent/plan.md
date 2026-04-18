# Plan

## Goal
Step 4: First Real Planner Worker (local Ollama-backed).

## Current Step
Step 4 — COMPLETE. Pushing and creating PR.

## Completed
- [x] packages/orchestration/planner_models.py (PlannerOutput, ProposedTask)
- [x] packages/orchestration/llm_planner.py (plan_job_with_llm)
- [x] packages/providers/ollama_planner/provider.py (OllamaPlanner)
- [x] pyproject.toml: ollama optional dep
- [x] CLI: plan-job-local command
- [x] tests/test_llm_planner.py (22 tests, no live Ollama)
- [x] README + architecture.md

## Next Steps
Step 5: TBD (task execution, second provider, or worker routing)
