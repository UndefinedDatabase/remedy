# Plan

## Goal
Step 34: Project Command Discovery v0

## Status
COMPLETE — smoke passed, committing

## Completed
- [x] command_discovery.py: CommandCandidate, discover_commands, select_best_test_candidate
- [x] Detectors: constitution, pyproject, package_json, makefile, justfile, taskfile, cargo, go
- [x] Risky token detection → high-risk candidates not auto-runnable
- [x] test_runner.py: uses discover_commands; _EXECUTION_SAFE_EXECUTABLES guard; ALLOWED_COMMANDS removed
- [x] TestRunRecord: 4 new provenance fields (command_source_type/path/purpose/confidence)
- [x] CLI: discover-commands subcommand (text + --json); run-tests-local logs 11 keys
- [x] project_brain.py: test_run node stores 4 new provenance fields
- [x] brain_detail.py: 11 evidence items (was 7)
- [x] trust_report.py: shows source_type + confidence in test run section
- [x] tests/test_command_discovery.py: 13 test classes, ~270 lines
- [x] tests/test_test_runner.py: updated for 11-key schema, new evidence count, new invariant test
- [x] tests/test_remedy_smoke_script.py: 3 new Step 34 smoke text assertions
- [x] smoke step 6l: 11-key schema; step 6n: discover-commands check
- [x] 1998 tests passing
- [x] remedy_smoke: PASSED (step 6n: candidates=1, best_source=pyproject)

## Next
Commit. Push. Open PR.
