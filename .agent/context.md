# Context

## Active Branch
`feature/step5-task-execution`

## PR
https://github.com/UndefinedDatabase/remedy/pull/6

## Scope
Step 5: First local task execution skeleton — builder role, single-task execution,
artifact provenance, job state advancement.

## Constraints
- No Docker, no filesystem editing, no command execution, no retries
- No Claude, no MemPalace, no broad multi-provider routing
- Provider must not mutate Job directly
- Builder role distinct from planner role
- ollama is optional dep — not required for core to work
- run_next_task must not import provider code directly

## Assumptions
- OllamaBuilder.build() lazily imports ollama; ImportError surfaced at call time
- BuilderOutput lives in orchestration/ (same pattern as PlannerOutput)
- annotate_task_result finds artifact by task_id, not by index
- Step 4 (llm_planner, ollama_planner, plan-job-local) now on main via merged PR #5

## Branch Scope Decision
Step 5 (execution) is clearly unrelated to Step 4 (planning/provider config).
New branch created from main (after PR #5 merged) per AGENTS.md.
