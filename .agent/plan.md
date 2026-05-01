# Plan

## Goal
Step 13.3: Final Pre-Step-14 Hygiene

## Status
COMPLETE — committed, pushed

## Steps
1. [x] test_cli_main.py: add isinstance(stored_risks, list) to
       test_all_stored_risk_values_are_in_risk_levels
2. [x] .agent/context.md: copy Step-14 invariant note
3. [x] 456 tests pass; committed; pushed

## Branch
feature/step13-task-registry

## PR
#13 (open)

## Step-14 invariant note
In v1, is_known_task_type(task_type) == (get_task_type_spec(task_type).repo_route is not None).
If Step 14 introduces known non-repo task types, this invariant and
test_is_known_matches_get_spec_has_repo_route must be revisited.
