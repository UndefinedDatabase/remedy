# Context

## Active Branch
`feature/step9-permission-model`

## PR
#9 — open, updating in place (PR Continuity Rule).

## Scope
Step 9.6: Permission Enforcement Ordering Hotfix.
In-scope correctness fix for Step 9's permission model (same branch, same PR).

## Constraints
- No Docker, no shell, no Git, no patch application
- No interactive permission prompts
- workspace_write check moved to before builder call — eliminates wasted LLM calls
- Late materialization gate removed (check already passed by this point)
- show-permissions labels ALL capabilities ([active] or [reserved])
- No changes to reserved capabilities (repo_overwrite, shell_exec still reserved)

## Assumptions
- workspace_write check lives in the CLI, not in task_runner.py or run_next_task
- The early check calls sys.exit(1) — no task state mutation, no builder call
- materialize_task_output remains unconditional after the early check passes
