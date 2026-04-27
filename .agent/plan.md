# Plan

## Goal
Step 9.5: Permission Model Honesty and CLI UX Hotfix.

## Status
READY TO COMMIT

## Steps
1. [x] Update .agent/plan.md and context.md
2. [x] permissions.py: add _RESERVED, is_reserved(), effective_permissions()
3. [x] CLI: reserved notice in set-permission; workspace_write gate; show-permissions command
4. [x] Tests: TestIsReserved + TestEffectivePermissions; new tests/test_cli_main.py (301 tests pass)
5. [x] Update README.md and docs/architecture.md
6. [x] Update .agent/decisions.md
7. [ ] Self-review, commit, push, update PR

## Branch
feature/step9-permission-model

## PR
#9 (existing — update, do not create new)
