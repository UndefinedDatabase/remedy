# Plan

## Goal
Step 4: First Real Planner Worker (local Ollama-backed) — introduce the first concrete
provider with structured LLM output, keeping orchestration fully in control.

## Current Step
In progress on feature/step4-ollama-planner (new branch from main after PR #4 merged).

## Next Steps
1. packages/orchestration/planner_models.py (PlannerOutput, ProposedTask)
2. packages/orchestration/llm_planner.py (plan_job_with_llm, reuses PlanJobResult)
3. packages/providers/ollama_planner/provider.py (OllamaPlanner)
4. pyproject.toml — add ollama optional dep
5. apps/cli/main.py — plan-job-local command
6. tests/test_llm_planner.py — mocked tests, no live Ollama
7. docs: README + architecture.md
8. Push, create PR

## Decisions
- PlannerOutput lives in packages/orchestration/ (not in provider — orchestration imports it)
- Ollama is an optional dep [ollama] — ImportError raised lazily inside OllamaPlanner.plan()
- plan_job_with_llm accepts callable — provider is injected, never imported by orchestration
- PlanJobResult is reused from job_runner (same return shape)
- REMEDY_OLLAMA_MODEL env var; default qwen3-coder-next
- acceptance_checks from planner → preserved in artifact content + job metadata
