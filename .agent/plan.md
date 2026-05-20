# Plan

## Goal
Step 33: Permission-gated Test Run v0

## Status
COMPLETE — smoke passed, committing

## Completed
- [x] permissions.py: add repo_test_run capability (active, default deny)
- [x] test_runner.py: new module with run_tests_local, TestRunRecord, ALLOWED_COMMANDS
- [x] project_brain.py: NT_TEST_RUN node, ET_HAS_TEST_RUN / ET_VERIFIED_AFTER_APPLY edges
- [x] brain_detail.py: _detail_test_run handler (7 evidence items + 2 redaction notes)
- [x] timeline.py: test_run_completed rendering (no raw output)
- [x] trust_report.py: new §8 Test runs; §8 Redaction → §9; §9 Next action → §10
- [x] cli/main.py: run-tests-local subcommand with permission gate
- [x] tests/test_test_runner.py: ~350 lines, 12 test classes
- [x] tests/test_permissions.py: updated for 5-capability set
- [x] tests/test_trust_report.py: updated section numbers
- [x] smoke: steps 6i–6l (grant permission, run tests, verify brain node, verify schema)
- [x] tests/test_remedy_smoke_script.py: 7 new smoke text assertions
- [x] docs/architecture.md: Step 33 section appended
- [x] 1941 tests passing
- [x] remedy_smoke: PASSED

## Next
Commit. Push. Open PR.
