# Plan

## Goal
Step 2: Packaging + First Runnable System Layer — make Remedy properly packaged, import-safe, runnable via CLI, able to create and persist a Job locally.

## Current Step
In progress: implementing packaging and CLI.

## Next Steps
1. Job model: add user_prompt field
4. packages/orchestration/storage.py (JSON file storage)
5. apps/cli/main.py (create-job command)
6. tests: remove sys.path hack, add storage smoke test
7. README.md: add install/run instructions
8. Commit each logical unit, push, create PR

## Risks
- storage path is CWD-relative; documented assumption
- user_prompt on Job is a minimal model change, not orchestration logic
