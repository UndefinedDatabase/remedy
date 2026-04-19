# Context

## Active Branch
`feature/step4-ollama-planner`

## PR
https://github.com/UndefinedDatabase/remedy/pull/5

## Scope
Step 4 + 4.6: First concrete provider — Ollama-backed local planner with role-specific configuration.

## Constraints
- No Claude integration yet
- No Docker, no MemPalace
- No async orchestration frameworks
- No retries
- No broad multi-provider routing
- Ollama is optional dep — not required for core to work
- plan_job_with_llm must not import provider code directly

## Assumptions
- OllamaPlanner.plan() lazily imports ollama; ImportError surfaced at call time
- Planner models (PlannerOutput) live in orchestration/, not in the provider
- CLI plan-job-local catches ImportError and Ollama errors gracefully
- REMEDY_OLLAMA_PLANNER_MODEL takes priority; falls back to REMEDY_OLLAMA_MODEL, then default
- Deterministic plan-job path unchanged and coexists with the new LLM path
- annotate_planning_result() called in CLI after plan_job_with_llm; timing measured at CLI layer

## Branch Scope Decision
Step 4 (real provider integration) is clearly unrelated to Step 3/3.5
(orchestration skeleton + semantics). New branch correct per AGENTS.md.
PR #4 was merged before creating this branch.
Step 4.6 continues on same branch (feature/step4-ollama-planner) per Pull Request Continuity Rule.
