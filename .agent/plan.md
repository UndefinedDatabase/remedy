# Plan

## Goal
Step 15.1: Verifier Profile Contract Cleanup

## Status
COMPLETE — 571 tests pass

## Steps
1. [x] Remove dead workspace fields from VerifierProfile (require_workspace_file, require_nonempty_workspace_file)
2. [x] Move profile checks before require_workspace_file guard in verifier.py
3. [x] Add comment to implementation_plan profile: TODO intentionally not forbidden
4. [x] Update test_verifier_profiles.py: remove dead-field tests, add workspace-field tests, add TODO test
5. [x] Add test_profile_checks_run_without_workspace_file to test_verifier.py
6. [x] Add test_implementation_plan_does_not_forbid_TODO to test_verifier.py
7. [x] Update docs/architecture.md and .agent files, commit + push + PR

## Branch
feature/step14-artifact-kinds
