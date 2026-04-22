# Context

## Active Branch
`feature/step5-task-execution`

## PR
https://github.com/UndefinedDatabase/remedy/pull/6

## Scope
Step 5 + 5.5 + 5.6: First local task execution skeleton + execution hardening + CLI hotfix.
Builder role, single-task execution, failure rollback, richer context,
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
- TaskExecutionContext + BuilderOutput live in orchestration/ (same pattern as PlannerOutput)
- annotate_task_result finds artifact by task_id, not by index; raises if changed but missing
- annotate_planning_result finds artifact by name+task_id, not by index
- Step 4 (llm_planner, ollama_planner, plan-job-local) on main via merged PR #5
- Step 5.5 continues on same branch (PR #6) per Pull Request Continuity Rule

## Branch Scope Decision
Step 5 (execution) is clearly unrelated to Step 4 (planning/provider config).
New branch created from main (after PR #5 merged) per AGENTS.md.
Step 5.5 (execution hardening) is in-scope for PR #6 — same feature boundary.
