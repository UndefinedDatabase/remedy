# Plan

## Goal
Step 33.1: Test Run Smoke Precision + Runner Polish

## Status
COMPLETE — committing

## Completed
- [x] test_runner.py: __test__ = False on TestRunRecord (suppress PytestCollectionWarning)
- [x] test_runner.py: assert command in ALLOWED_COMMANDS before subprocess.run
- [x] test_runner.py: FileNotFoundError → _blocked("command_not_found"), output_path == ""
- [x] smoke step 6m: Trust/Timeline structural check, no bare-stdout false-positive
- [x] tests: test_command_not_found_output_path_is_empty
- [x] tests: test_allowed_command_invariant_fires_for_unknown_command
- [x] tests: test_test_run_record_not_collected_by_pytest
- [x] tests: 5 new smoke text assertions for step 6m
- [x] docs/architecture.md: Step 33.1 clarification section
- [x] 1949 tests passing
- [x] remedy_smoke: PASSED (step 6m OK)

## Next
Commit. Push. PR #29 already open — update it.
