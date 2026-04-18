# Context

## Active Branch
`feature/step4-ollama-planner`

## PR
None yet — will be created after commits are pushed.

## Scope
Step 4: First concrete provider — Ollama-backed local planner.

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
- REMEDY_OLLAMA_MODEL env var controls the model; default: qwen3-coder-next
- Deterministic plan-job path unchanged and coexists with the new LLM path

## Branch Scope Decision
Step 4 (real provider integration) is clearly unrelated to Step 3/3.5
(orchestration skeleton + semantics). New branch correct per AGENTS.md.
PR #4 was merged before creating this branch.
