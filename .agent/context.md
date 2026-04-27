# Context

## Active Branch
`feature/step9-permission-model`

## PR
#9 — open, updating in place (PR Continuity Rule).

## Scope
Step 9.5: Permission Model Honesty and CLI UX Hotfix.
In-scope extension of Step 9 (same branch, same PR).

## Constraints
- No Docker, no shell, no Git, no patch application
- No interactive permission prompts
- No arbitrary LLM paths into repo writes — static keyword mapping only
- No overwriting existing repo files (repo_overwrite reserved but unused)
- shell_exec reserved but unused
- workspace_write: now enforced in CLI before materialize_task_output
- repo_overwrite and shell_exec: configurable but reserved — print notice on set-permission
- Task completion still determined by verifier; denying workspace_write causes verifier failure

## Assumptions
- LocalWorkspaceRuntime is the only runtime; Docker runtime is future
- workspace_write gate lives in the CLI (_cmd_run_next_task_local), not in task_runner.py
- effective_permissions() is a pure helper in permissions.py (no storage access)
