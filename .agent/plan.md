# Plan — Steps 4146-4215: Claude CLI Write-Enabled Staged Self-Run v1

## Goal
Make real local Claude CLI Builder edits work safely in staging via
`--claude-cli-write-mode none|allowed-tools|dangerous-skip`. Add safe diff
report artifact. Add `builder_no_changes` status.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- `--claude-cli-write-mode` wired through CLI (command_catalog, do_cmd, run_pingpong)
- `build_claude_cli_args()` produces correct argv for all 3 write modes
- Builder gets write_mode from CLI; Reviewer ALWAYS gets write_mode="none"
- `_compute_safe_diff()`: unified diff, excludes secrets/binaries, capped at 50K chars
- Safe diff fields in PingPongResult, export JSON, summary text, and report output
- `builder_no_changes` status when Claude CLI builder produces no file changes
- 25 new E2E tests (total 63 in test_pingpong_cli.py)
- Real Claude CLI smoke: builder edited main.py in staging, target untouched
  - staged_files=["main.py"], safe_diff shows actual code change
  - target_mutated=false confirmed
- Full suite: 7276 passed, 0 failed, 8 skipped
- Fast lane: 571 passed
- Runtime lane: 4/4 suites
- Lint: ruff clean, mypy clean (196 files)

## Dogfood command
```
remedy do run "Add docstring to greet() in main.py" \
  --builder claude-cli --reviewer claude-cli \
  --claude-cli-write-mode allowed-tools \
  --max-rounds 3 --keep-staging --json
```

## Risks
- Reviewer runs without staging cwd (prompt-only), may not see builder edits
- `dangerous-skip` requires explicit user opt-in (intentional friction)
