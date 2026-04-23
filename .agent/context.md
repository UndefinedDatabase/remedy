# Context

## Active Branch
`feature/step6-workspace-runtime`

## PR
(none yet — to be created after commit)

## Scope
Step 6: First Runtime-Backed Workspace Execution.
Local workspace runtime, file materialization, planner min_length=1.

## Constraints
- No Docker, no command execution, no patch parsing
- Runtime injected into orchestration; never imported by providers
- Workspace dir structure: .data/workspaces/<job_id>/task_output/<task_type>.txt
- materialize_task_output raises RuntimeError on impossible state (bug indicator)
- annotate RuntimeError propagates — not caught in CLI

## Assumptions
- LocalWorkspaceRuntime is the only runtime for Step 6; Docker runtime is future
- Workspace root follows same REMEDY_DATA_DIR resolution as storage.py
- Proposed_changes re-derived from artifact content (lines starting with "  - ")
- workspace_file metadata key records the absolute path of the materialized file
