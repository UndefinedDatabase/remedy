# Plan — Steps 3996-4075: Claude CLI Staged Self-Run v0

## Goal
Make Remedy usable for real local Claude-powered staged self-runs.
Add claude-cli provider, real staged test execution, durable run storage,
and `remedy do report`.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- ClaudeCliProvider: subprocess `claude -p` with shutil.which detection, timeout, output cap
- Test command support: `--test-command` with shlex.split (no shell=True), timeout, output cap
- Durable run storage: `.data/pingpong_runs/<run_id>/result.json`
- `remedy do report <run_id>` and `remedy do report list`
- Fixed JSON mode: no human headers before JSON in --json
- Fixed `summarize_pingpong`: references `remedy do report` not `remedy job report`
- Keep staging: `--keep-staging` preserves staging workspace
- CLI catalog: 4 new args (--test-command, --provider-timeout-sec, --max-output-chars, --keep-staging)
- 23 E2E tests (test_pingpong_cli.py) covering all provider/storage/test-command paths
- Fast lane: 7056 passed, 0 failed, 8 skipped
- Regression: 97 passed
- Lint: ruff clean, mypy clean
- Pre-existing: test_project_brain.py::TestFileProvenanceChain::test_full_chain_order (not our change)

## Risks
- Real claude-cli smoke not run (claude CLI not in this env's PATH)
