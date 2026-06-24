# Live Review — Steps 4266-4315: Reviewer JSON Reliability + Real Dogfood Pass Closure v3

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-24

## Verdict (reviewer-owned)
**PASS WITH RISKS** @ working tree (parent b1d10f4, no commit yet)

Zero open Blocker/High. One open Medium (lint). All functional requirements met.
Real Claude CLI dogfood achieved first `staged_review_passed`: builder edited staging,
test ran in staging, reviewer parsed JSON first attempt, target unchanged, safe diff preserved.
Reviewer sees actual unified diff. Bounded retry works. Parse metadata in reports.
124 CLI tests. 7337 full suite pass. **Builder must commit after fixing lint import sort.**

## Commit reviewed
Working tree changes on parent b1d10f4. Builder has not committed yet.

## PR reviewed
No open PR. Builder on `feature/steps-3276-3355-job-fulfillment-spine-v0`.

## Protocol compliance
- Builder did NOT write reviewer verdict: PASS
- Builder did NOT self-merge: PASS
- Builder did NOT mark findings as resolved: PASS
- No German in project-facing content: PASS

## Worker 5-minute quiet-window assessment
Builder code stable since ~14:17 UTC (45+ min). No new changes. Builder stalled — did not commit.
Code is feature-complete with all tests passing. PASS (builder idle).

## Reviewer 10-minute quiet-window assessment
- Quiet window started: 15:00:15 UTC
- Quiet window ended: 15:08:31 UTC (5 checks, ~10 min)
- Activity during window: none (same 5 files, same stats)
- Re-verified findings: R-0901 through R-0907 all confirmed
- Findings remaining open: R-0907a (lint, Medium)

## Finding status

### R-0901 Blocker — Real Reviewer still fails due malformed JSON → **Resolved (working tree)**
Three-layer fix:
1. **Reviewer prompt rewritten** (`pingpong_provider.py`): "Return ONLY valid JSON. No markdown.
   No code fence." Clear, explicit instruction.
2. **Code fence stripping** in `_parse_reviewer_json()`: strips ```json...``` wrappers before parsing.
3. **`_unwrap_envelope()`**: handles Claude CLI envelopes (`{"result":...}`, `{"content":...}`,
   `{"message":...}`, `{"text":"json_string"}`).
4. **Bounded retry**: one retry on malformed output with `_REVIEWER_RETRY_PROMPT`.
**Real smoke**: reviewer JSON parsed first attempt, `verdict=pass`, `parse_retry=0`.
Status: `staged_review_passed` — first real end-to-end dogfood pass.
Tests: `TestParseReviewerJsonCodeFence`, `TestParseReviewerJsonBare`, `TestParseReviewerJsonNoJson`,
`TestParseReviewerJsonSurroundingProse`, `TestParseReviewerJsonRawTextCap`.

### R-0902 High — Reviewer does not see actual safe diff → **Resolved (working tree)**
`_build_reviewer_prompt()` now takes `safe_diff` parameter. `_REVIEWER_DIFF_CAP = 30000`.
Safe diff computed BEFORE reviewer call at `pingpong_loop.py` lines 673-677:
`_compute_safe_diff(staging, original, result.staged_files)` → passed as `safe_diff`.
Prompt section: `## Staged Unified Diff` with ```diff...``` block.
Fallback: if no safe_diff, uses `diff_summary` (file names only).
No absolute staging paths in diff (relative `a/`/`b/` paths from `_compute_safe_diff`).
Tests: `TestReviewerPromptSafeDiff`, `TestReviewerPromptDiffCap`, `TestReviewerPromptFallbackDiffSummary`,
`TestReviewerReceivesSafeDiff`.

### R-0903 High — Malformed Reviewer output can pass → **Resolved (working tree)**
`_parse_reviewer_json()`: malformed output → `verdict="blocked"`, `error="malformed_output:..."`.
Invalid verdict → `verdict="blocked"`. No JSON → `verdict="blocked"`.
`FakeProvider(malformed_review=True)`: both calls malformed → `review_failed`, not pass.
`TestRetryCannotFakePass`: asserts `final_status != "staged_review_passed"`.
`TestMalformedReviewRetryPersistent`: `review_failed`, `reviewer_json_recovered=False`.

### R-0904 High — Reviewer retry is unbounded or unsafe → **Resolved (working tree)**
Retry at `pingpong_loop.py` lines 699-720:
- **Bounded**: exactly one retry (`if reviewer_out.error.startswith("malformed_output:")`).
  No loop, no recursion. Counter incremented once.
- **Read-only**: `reviewer_provider.review()` — reviewer has `write_mode="none"` (double safety from v1).
- **Timeout-limited**: same `timeout_sec` as original call.
- **Output-capped**: same `max_output_chars`.
- **Documented**: `parse_retried`, `parse_retry_recovered` on ReviewerOutput.
  `reviewer_parse_retry_count`, `reviewer_parse_error`, `reviewer_malformed_excerpt` on result.
Tests: `TestMalformedReviewRetryPersistent`, `TestMalformedReviewRecoverable`, `TestParseRetriedFlag`.

### R-0905 Medium — Repair prompt lacks enough context → **Resolved (working tree)**
`_build_builder_prompt()` takes `safe_diff` parameter. `_REPAIR_DIFF_CAP = 20000`.
Repair rounds (round_num > 1): safe diff computed before builder call (lines ~651-656).
Builder gets: goal, context, `## Current Staged State`, `## Current Staged Diff`, `## Reviewer Findings to Fix`.
Diff only shown when findings present (repair rounds only, not round 1).
Tests: `TestBuilderRepairPromptDiff`, `TestBuilderRepairPromptDiffCap`, `TestBuilderPromptRound1NoDiff`,
`TestRepairRoundGetsDiff`.

### R-0906 Medium — Report lacks parse metadata → **Resolved (working tree)**
`PingPongResult` fields: `reviewer_parse_retry_count`, `reviewer_parse_error`,
`reviewer_malformed_excerpt`, `reviewer_json_recovered`.
`ReviewerOutput` fields: `parse_retried`, `parse_retry_recovered`.
`export_pingpong_json()`: all fields exported including per-round `parse_retried`/`parse_retry_recovered`.
`summarize_pingpong()`: "Reviewer parse: retried Nx, recovered/NOT recovered".
`_cmd_do_report()`: shows retry status and parse error.
Tests: `TestParseMetadataInExport`, `TestParseMetadataInSummary`, `TestRecoveredParseInSummary`,
`TestParseRetriedInRoundExport`.

### R-0907 Medium — Existing dogfood safety regresses → **Resolved (working tree)**
- Cache noise: all 29 noise tests pass
- Target mutation: blocking tests pass
- Staged evidence: preserved even on block
- Keep-staging: boolean flag works
- JSON/report: all fields present
- Fulfillment: 109 x 2 pass
- Pingpong E2E: 33 pass
- Full suite: 7337 passed, 0 failed

### R-0907a Medium — Lint import sort failure → **OPEN**
`ruff check` reports I001 (import block unsorted) in two files:
- `packages/orchestration/pingpong_loop.py`: `_REVIEWER_RETRY_PROMPT` private import
- `tests/orchestration/test_pingpong_cli.py`: private imports (`_REVIEWER_RETRY_PROMPT`, etc.)
Fix: `ruff --fix` or manually sort. Mypy passes. All tests pass.
**Builder must fix before commit.**

## Real dogfood smoke result — PASS
- Claude CLI at `/home/decodeux/.local/bin/claude`
- Temp repo with `main.py` + 3 cache dirs
- `claude_cli_write_mode="allowed-tools"`, `test_command="python3 -c 'import main'"`
- **Result: `staged_review_passed`** — first real end-to-end dogfood pass!
  - Builder added docstring to `greet()` in staging
  - Test passed in staging (exit=0)
  - Reviewer parsed JSON first attempt (`parse_retry=0`)
  - Reviewer verdict: `pass`
  - Target unchanged: `"def greet(): pass\n"`
  - Cache noise classified: all 3 dirs
  - Safe diff: unified diff shows docstring addition
  - Status: `staged_review_passed`

## Reviewer JSON parse assessment — PASS
- Prompt rewritten: explicit "Return ONLY valid JSON" instruction
- Code fence stripping before parse
- Envelope unwrapping for Claude CLI output formats
- Invalid verdict → blocked
- No JSON → blocked
- Real smoke: parsed first attempt

## Reviewer retry assessment — PASS
- Bounded: exactly one retry on `malformed_output:` error
- Read-only: reviewer has no write permissions
- Same timeout/output cap
- Parse metadata tracked on result and per-round
- Fake tests: persistent malformed → `review_failed`; recoverable → `staged_review_passed`

## Safe diff in Reviewer prompt assessment — PASS
- `_build_reviewer_prompt()` includes `## Staged Unified Diff` with bounded content
- Capped at 30K (`_REVIEWER_DIFF_CAP`)
- Relative paths, no secrets
- Computed BEFORE reviewer call

## Repair prompt context assessment — PASS
- Builder repair round gets: findings + safe diff + staged state
- Diff capped at 20K (`_REPAIR_DIFF_CAP`)
- Only shown when findings present (round 2+)
- Two-round repair tested: `TestRepairRoundGetsDiff`

## Cache-noise regression assessment — PASS
All 29 cache-noise tests pass. Noise dirs don't block.

## Meaningful target mutation assessment — PASS
Real mutations still block. `TestRealTargetMutationStillBlocks`, `TestExistingSnapshotGuard` pass.

## Staged evidence assessment — PASS
Staged files + safe diff preserved in finally block, even on block.

## Explicit test-command assessment — PASS
Test ran in staging cwd. Real smoke: `python3 -c "import main"` exit=0.

## JSON/report assessment — PASS
All metadata fields exported. Parse retry info in report.

## Target mutation assessment — PASS
Target unchanged in both smoke runs. Cache noise classified, not blocking.

## Test evidence (reviewer-run, working tree on b1d10f4)

### Targeted tests
- Pingpong CLI: **124 passed, 0.57s** (92 existing + 32 new)
- Pingpong E2E: **33 passed, 0.13s**
- Fulfillment: **109 passed x 2** (8.63s, 9.01s)
- Compile: clean

### Lanes
- Runtime lane: NOT re-run (no runtime changes this block)
- Lint: **ruff I001 failure** (import sort in 2 files), **mypy clean**

### Full suite
- **7337 passed, 0 failed, 8 skipped** (230.56s)

### Post-test process/lock check
- Lock: free
- No stale processes

## Architecture guard scan
- `shell=True`: none
- Provider timeout/output cap: enforced on retry too
- API key logging: none
- `.env` leakage: excluded
- Unbounded retries: exactly one retry, no loop
- Reviewer write permissions: never (unchanged)
- Target test execution: in staging cwd
- Malformed accepted as pass: no (blocked)
- Meaningful mutations as noise: no
- JSON pollution: clean

## Edited-file line-range map (reviewer-constructed, v2→v3 working tree)

| File | Lines | What changed | Tests |
|------|-------|-------------|-------|
| `packages/orchestration/pingpong_provider.py` | 211-240, 349-400, 412-455 | Reviewer prompt rewrite, `_REVIEWER_RETRY_PROMPT`, `_unwrap_envelope()`, code fence strip, envelope unwrap, `parse_retried`/`parse_retry_recovered` fields | 10 parse/envelope tests |
| `packages/orchestration/pingpong_loop.py` | 33-38, 80-87, 199-204, 215-218, 231-270, 651-677, 699-720, 960-975, 1021-1024, 1058-1065 | Parse metadata fields, reviewer prompt diff, repair diff, bounded retry, export, summary | 22 tests |
| `apps/cli/commands/do_cmd.py` | 269-273 | Report shows parse retry metadata | TestParseMetadataInSummary |
| `tests/orchestration/test_pingpong_cli.py` | 1472-1949 | 32 new tests for parse, retry, diff, repair | Self-covering |

## Top risks
- **Medium (OPEN)**: R-0907a — ruff I001 import sort in 2 files. Builder must fix before commit.
- Low — `BUILDER_WAS_HERE.txt` + `docs/report-guide.md` stale test artifacts
- Low — `_TARGET_NOISE_DIRS` hardcoded
- Low — Claude CLI output parsing heuristic

## Final recommendation
**READY TO DOGFOOD.** First real `staged_review_passed` achieved with Claude CLI builder + reviewer.
Builder must fix lint (import sort) and commit. Once committed and lint clean, merge-ready.

Exact dogfood command:
```bash
REMEDY_DATA_DIR=/tmp/remedy-data remedy do run "Add docstring to main.py:greet" \
  --builder claude-cli --reviewer claude-cli \
  --claude-cli-write-mode allowed-tools \
  --max-rounds 2 --mode staged \
  --test-command "python3 -c 'import main'" --json
```

## Merge readiness
**CONDITIONAL READY.** Builder must:
1. Fix ruff I001 import sort (2 files)
2. Commit
Then merge-autonomy applies.

NO PR unless user asks.
