# Context

## Active Branch
`feature/step9-permission-model`

## PR
None yet — will create after Step 9 is complete.

## Scope
Step 9: Permission Model v1 for Controlled Execution.
New branch from main (all prior steps merged). Clearly distinct purpose from Step 8.

## Constraints
- No Docker, no shell, no Git, no patch application
- No interactive permission prompts
- No arbitrary LLM paths into repo writes — static keyword mapping only
- No overwriting existing repo files (repo_overwrite reserved but unused)
- shell_exec reserved but unused
- Permissions stored in job.metadata["permissions"] as {"cap": "allow"|"deny"}
- workspace_write allowed by default; all others denied by default
- repo_generated_write must be explicitly allowed for repo application to proceed
- check_and_apply_to_repo annotates artifact with repo_application_skipped_reason on denial
- Task completion is always determined by the verifier, never by repo application

## Assumptions
- LocalWorkspaceRuntime is the only runtime; Docker runtime is future
- Workspace root follows same REMEDY_DATA_DIR resolution as storage.py
- target_repo is stored as str (absolute path) in job.metadata["target_repo"]
- Repo markdown content is derived from artifact metadata + content (not workspace file)
