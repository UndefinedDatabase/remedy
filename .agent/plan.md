# Plan — Steps 4266-4315: Reviewer JSON Reliability + Real Dogfood Pass Closure v3

## Goal
Fix reviewer parse failures preventing real dogfood success. Reviewer must receive
actual safe diff. Add JSON-only hardening to reviewer prompt. Add one bounded parse
retry. Handle Claude CLI JSON envelope formats. Repair prompt must include findings
+ safe diff. Report must expose parse retry metadata.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- _REVIEWER_JSON_SCHEMA: strict JSON-only contract in reviewer prompt
- _REVIEWER_RETRY_PROMPT: compact correction prompt for parse retry
- _unwrap_envelope(): handle result/content/message/text envelope wrappers
- _parse_reviewer_json: strip markdown code fences, envelope unwrap, raw_text cap 500
- _REVIEWER_SYSTEM: JSON-only instructions
- _build_reviewer_prompt: accepts safe_diff with 30K cap (_REVIEWER_DIFF_CAP)
- Reviewer call site computes safe diff before reviewer runs
- Bounded parse retry: one retry on malformed_output:, no fake pass
- ReviewerOutput: parse_retried, parse_retry_recovered fields
- PingPongResult: reviewer_parse_retry_count, reviewer_parse_error,
  reviewer_malformed_excerpt, reviewer_json_recovered
- FakeProvider: malformed_review_recoverable option for testing
- _build_builder_prompt: safe_diff param with 20K cap for repair rounds
- Repair diff computed before builder call in round > 1
- export_pingpong_json: parse metadata + per-round parse_retried/recovered
- summarize_pingpong: shows retry count and recovered status
- _cmd_do_report: shows parse retry info
- 32 new tests (73-104), total 124 in test_pingpong_cli.py
- Ruff lint: clean
- Full suite: 7254 passed, 0 failed (pre-existing test_project_brain unrelated)
- Architecture guard: CLEAN
- Dogfood smoke: 3/3 scenarios pass

## Dogfood command
```
remedy do run "Add docs note about ping-pong reports" \
  --repo . --builder claude-cli --reviewer claude-cli \
  --claude-cli-write-mode allowed-tools \
  --max-rounds 2 --mode staged \
  --test-command "python3 -m pytest tests/orchestration/test_pingpong.py -q" \
  --keep-staging --json
```
