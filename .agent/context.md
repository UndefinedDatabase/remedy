# Context

## Active Branch
`feature/step6-workspace-runtime`

## PR
PR #7 — open at https://github.com/UndefinedDatabase/remedy/pull/7

## Scope
Step 6 + 6.5 + 6.7 + Step 7: workspace runtime, materialization hardening, runtime boundary
enforcement, and Task Contract v1 verifier gate.

## Constraints
- No Docker, no command execution, no patch parsing
- Runtime injected into orchestration; never imported by providers
- Workspace dir: .data/workspaces/<job_id>/task_output/<index>_<safe_type>_<short_id>.txt
- materialize_task_output and finalize_task raise RuntimeError on impossible states
- Task stays RUNNING after run_next_task; COMPLETED only after verify_task_output passes
- verify_task_output is pure (no mutation); finalize_task applies the result
- No FAILED state: verification failure rolls task to PENDING (retryable)

## Assumptions
- LocalWorkspaceRuntime is the only runtime; Docker runtime is future
- Workspace root follows same REMEDY_DATA_DIR resolution as storage.py
- workspace_file metadata key records the absolute path of the materialized file
- verification_failures metadata key is set by finalize_task on failure only
