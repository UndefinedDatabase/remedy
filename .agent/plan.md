# Plan

## Goal
Step 2: Packaging + First Runnable System Layer — make Remedy properly packaged, import-safe, runnable via CLI, able to create and persist a Job locally.

## Current Step
In progress: implementing packaging and CLI.

## Next Steps
1. apps/cli/main.py (create-job command)
2. tests: remove sys.path hack, add storage smoke test
3. README.md: add install/run instructions
4. Push, create PR

## Risks
- storage path is CWD-relative; documented assumption
- user_prompt on Job is a minimal model change, not orchestration logic
