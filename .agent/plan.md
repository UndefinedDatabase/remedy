# Plan

## Goal
Step 13.2: Final Registry Hygiene

## Status
COMPLETE — committed, pushed

## Steps
1. [x] docs/architecture.md: fix wrapped import → single inline code span
2. [x] test_cli_main.py: split test_all_stored_risk_values_are_in_risk_levels into
       test_stored_risk_count_matches_intent_count (len == 1) +
       test_all_stored_risk_values_are_in_risk_levels (RISK_LEVELS membership)
3. [x] patch_intent.py: update _ARTIFACT_SECTION_HEADERS comment (no task_runner ref)
4. [x] plan.md: Step-14 invariant note
5. [x] 456 tests pass; committed; pushed

## Branch
feature/step13-task-registry

## PR
#13 (open)

## Step-14 invariant note
In v1, is_known_task_type(task_type) is equivalent to
get_task_type_spec(task_type).repo_route is not None.
If Step 14 introduces known non-repo task types (e.g., code-generation with a
verifier profile but no repo_route), this invariant breaks. At that point:
  - is_known_task_type must use a stronger marker (e.g., explicit registry flag)
  - test_is_known_matches_get_spec_has_repo_route must be audited and updated
  - task_registry.py docstring for is_known_task_type already carries this warning
