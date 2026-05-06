# Plan

## Goal
Step 21.1: Project Constitution trust/timeline polish.

## Prior step
Step 21 delivered Project Constitution v1 (extraction, CLI, cockpit integration).

## Status
COMPLETE — 982 tests pass.

## Steps
1. [x] trust_report.py: add constitution parameter with 5 rendering cases
2. [x] timeline.py: first-class project_constitution_loaded event rendering
3. [x] main.py: _cmd_trust_report loads constitution at render time; passes None when no repo
4. [x] tests/test_project_constitution.py: 13 new tests (trust-report CLI + timeline event)
5. [x] Fix: pass constitution=None (not load(None)) when target_repo absent
6. [x] Run full suite (982 pass)
7. [x] Update docs/architecture.md
8. [x] Update .agent files
9. [ ] Commit Step 21.1 changes
10. [ ] Push to feature/step21-project-constitution-v1

## Branch
feature/step21-project-constitution-v1
