# Plan

## Goal
Step 15: Verifier Profiles v1

## Status
COMPLETE — 568 tests pass

## Steps
Pre-flight:
1. [x] Rename _pa → pa in task_runner._build_execution_context
2. [x] Update docstring for test_context_no_planning_summary_when_absent

Implementation:
3. [x] Create packages/orchestration/verifier_profiles.py (4 profiles, get/iter API)
4. [x] Update task_registry.py: _ROUTE_RULES 4-tuple with verifier_profile per route
5. [x] Update verifier.py: profile-driven checks (sections, min_changes, forbidden_phrases)

Tests:
6. [x] Create tests/test_verifier_profiles.py (unit tests for all profiles)
7. [x] Update test_task_registry.py (rename/update verifier_profile test, add 4 new)
8. [x] Update test_verifier.py (profile-specific integration tests: repo_doc, analysis_doc, implementation_plan)
9. [x] Fix _ROUTE_RULES unpack in test_patch_intent.py and test_task_registry.py (3→4 tuple)

Docs + agents:
10. [x] Update docs/architecture.md (Verifier Profiles v1 section)
11. [x] Update .agent files and commit

## Branch
feature/step14-artifact-kinds
