# Plan

## Goal
Step 5.5: Execution Hardening and Richer Task Context.

## Current Step
Commit 1/7 — TaskExecutionContext model

## Commits Planned
1. [ ] builder_models.py: add TaskExecutionContext
2. [ ] task_runner.py: failure rollback, context building, metadata cleanup, annotate safety
3. [ ] llm_planner.py: metadata cleanup, annotate fix (by name), task_type deduplication
4. [ ] OllamaPlanner: env var validation hardening; OllamaBuilder: context interface
5. [ ] CLI: differentiated error handling for ImportError/ValidationError/generic
6. [ ] Tests: update existing (new stub signature) + new (failure rollback, context, metadata)
7. [ ] Docs + .agent state

## Decisions Pending
- Failure rollback: task -> PENDING, job -> original_state (captured before mutation)
- annotate_task_result: raise RuntimeError if changed=True but no artifact found
- Metadata: remove "builder":"llm" and "planner":"llm" legacy keys
- Context: built inside run_next_task from job+task; includes planning_summary + prior_task_summaries
- task_type dedup: append _2, _3 on collision (simple, localized, no new schema)
- annotate_planning_result: find by name=="planning_output" + task_id is None instead of index 0

## Branch
feature/step5-task-execution (PR #6) — in-scope extension per PR Continuity Rule
