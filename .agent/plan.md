# Plan

## Goal
Step 5: First Local Task Execution Skeleton.

## Current Step
Commit 1/7 — builder_models.py

## Commits Planned
1. [ ] packages/orchestration/builder_models.py
2. [ ] packages/providers/ollama_builder/ (OllamaBuilder provider)
3. [ ] packages/orchestration/task_runner.py (run_next_task)
4. [ ] Hardening: planner env var validation + annotate_planning_result fix
5. [ ] CLI: run-next-task-local command
6. [ ] Tests: test_task_runner.py + test_ollama_builder.py + hardening tests
7. [ ] Docs + .agent state

## State Semantics (documented)
- PLANNED -> RUNNING: when first pending task starts executing
- RUNNING -> COMPLETED: when all tasks are COMPLETED
- Partially-executed job (some COMPLETED, some PENDING): stays RUNNING

## Constraints
- No Docker, no filesystem editing, no command execution
- No retries, no Claude, no MemPalace
- Provider must not mutate Job directly
- Builder role separate from planner role
