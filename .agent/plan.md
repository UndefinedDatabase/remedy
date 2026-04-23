# Plan

## Goal
Step 6: First Runtime-Backed Workspace Execution.

## Status
COMPLETE. All changes on feature/step6-workspace-runtime (PR to be created).

## What Was Done
1. workspace.py: Workspace, MaterializedFile, LocalWorkspaceRuntime (REMEDY_DATA_DIR resolution)
2. task_runner.py: materialize_task_output(); workspace_file metadata key; RuntimeError guard
3. planner_models.py: proposed_tasks min_length=1
4. CLI: integrate runtime + materialize_task_output after run_next_task; show file path
5. Tests: 20 new tests in test_workspace.py; 2 updated + 1 new in test_llm_planner.py
6. Docs: README + architecture.md updated

## Key Decisions
- Workspace stored at <repo_root>/.data/workspaces/<job_id>/
- LocalWorkspaceRuntime.write() creates dirs, writes files, returns MaterializedFile
- materialize_task_output re-derives proposed_changes from artifact.content (no schema change)
- workspace_file metadata key: absolute str path
- CLI annotate RuntimeError propagates — bug indicator, not user error

## Branch
feature/step6-workspace-runtime (PR to be created)
