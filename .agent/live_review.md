# Live Review — Steps 4266-4315: Reviewer JSON Reliability + Real Dogfood Pass Closure v3

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-24

## Verdict (reviewer-owned)
**PASS** @ 79d27c3

Zero open Blocker/High/Medium findings. First real `staged_review_passed` with Claude CLI.
Builder edits staging with allowed-tools. Test runs in staging. Reviewer parses JSON first
attempt. Safe diff in reviewer prompt. Bounded retry (1 attempt, read-only). Parse metadata
in reports. Repair prompt includes findings + safe diff. Lint clean. 124 CLI tests.
7337 full suite pass. Merge-ready.

Follow-up commit 602fd66 (settings-only, no production changes) also clean.

## Commit reviewed
79d27c3 Steps 4266-4315: Reviewer JSON Reliability + Real Dogfood Pass Closure v3
602fd66 Remove pytest deny rules from project settings (settings-only follow-up)

## PR reviewed
No open PR. Builder on `feature/steps-3276-3355-job-fulfillment-spine-v0`.

## Protocol compliance
- Builder did NOT write reviewer verdict: PASS
- Builder did NOT self-merge: PASS
- Builder did NOT mark findings as resolved: PASS
- No German in project-facing content: PASS

## Worker 5-minute quiet-window assessment
Builder commit 79d27c3 at ~15:54 UTC. Follow-up 602fd66 at ~15:59 UTC (settings only).
No production changes after 79d27c3. PASS.

## Reviewer 10-minute quiet-window assessment
- Quiet window started: 15:59:42 UTC (after 602fd66)
- Quiet window ended: 16:08:05 UTC (5 checks, ~10 min)
- Activity during window: none
- Re-verified findings: R-0901 through R-0907 all confirmed resolved
- Findings remaining open: none

## Finding status

### R-0901 Blocker — Real Reviewer still fails due malformed JSON → **Resolved @ 79d27c3**
Three-layer fix:
1. Reviewer prompt rewritten: "Return ONLY valid JSON. No markdown. No code fence."
2. Code fence stripping in `_parse_reviewer_json()`.
3. `_unwrap_envelope()`: handles Claude CLI envelopes (result/content/message/text wrappers).
4. Bounded retry: one retry on malformed output.
**Real smoke**: `staged_review_passed`. Reviewer JSON parsed first attempt, verdict=pass.
Tests: `TestParseReviewerJsonCodeFence`, `TestParseReviewerJsonBare`, `TestParseReviewerJsonNoJson`,
`TestParseReviewerJsonInvalidVerdict`, `TestParseReviewerJsonSurroundingProse`, `TestParseReviewerJsonRawTextCap`.

### R-0902 High — Reviewer does not see actual safe diff → **Resolved @ 79d27c3**
`_build_reviewer_prompt()` takes `safe_diff` parameter. `_REVIEWER_DIFF_CAP = 30000`.
Safe diff computed BEFORE reviewer call. Prompt section: `## Staged Unified Diff`.
Relative paths only. Fallback to file names if no safe_diff.
Tests: `TestReviewerPromptSafeDiff`, `TestReviewerPromptDiffCap`, `TestReviewerPromptFallbackDiffSummary`.

### R-0903 High — Malformed Reviewer output can pass → **Resolved @ 79d27c3**
Malformed → `verdict="blocked"`. Invalid verdict → `verdict="blocked"`.
`FakeProvider(malformed_review=True)`: persistent malformed → `review_failed`, never pass.
Tests: `TestRetryCannotFakePass`, `TestMalformedReviewRetryPersistent`.

### R-0904 High — Reviewer retry is unbounded or unsafe → **Resolved @ 79d27c3**
Exactly one retry on `malformed_output:` error. No loop. Read-only (reviewer has write_mode="none").
Same timeout/output cap. Parse metadata tracked.
Tests: `TestMalformedReviewRecoverable`, `TestParseRetriedFlag`, `TestParseRetriedFlagNotSet`.

### R-0905 Medium — Repair prompt lacks enough context → **Resolved @ 79d27c3**
`_build_builder_prompt()` takes `safe_diff`. `_REPAIR_DIFF_CAP = 20000`.
Repair rounds get: findings + safe diff + staged state. Only shown with findings (round 2+).
Tests: `TestBuilderRepairPromptDiff`, `TestBuilderRepairPromptDiffCap`, `TestBuilderPromptRound1NoDiff`,
`TestRepairRoundGetsDiff`.

### R-0906 Medium — Report lacks parse metadata → **Resolved @ 79d27c3**
`PingPongResult`: `reviewer_parse_retry_count`, `reviewer_parse_error`, `reviewer_malformed_excerpt`,
`reviewer_json_recovered`. `ReviewerOutput`: `parse_retried`, `parse_retry_recovered`.
All exported in JSON (top-level and per-round). Summary shows retry status. Report shows parse info.
Tests: `TestParseMetadataInExport`, `TestParseMetadataInSummary`, `TestRecoveredParseInSummary`,
`TestParseRetriedInRoundExport`.

### R-0907 Medium — Existing dogfood safety regresses → **Resolved @ 79d27c3**
- Cache noise: all tests pass, noise doesn't block
- Target mutation: real mutations still block
- Staged evidence: preserved even on block
- Keep-staging: boolean flag works
- Fulfillment: 109 x 2 pass
- Full suite: 7337 passed, 0 failed

## Real dogfood smoke result — PASS
- Claude CLI at `/home/decodeux/.local/bin/claude`
- Temp repo with `main.py` + 3 cache dirs
- `claude_cli_write_mode="allowed-tools"`, `test_command="python3 -c 'import main'"`
- **Result: `staged_review_passed`** — first real end-to-end dogfood pass!
  - Builder added docstring to `greet()` in staging
  - Test passed in staging (exit=0)
  - Reviewer parsed JSON first attempt (parse_retry=0)
  - Reviewer verdict: pass
  - Target unchanged: `"def greet(): pass\n"`
  - Cache noise classified (3 dirs)
  - Safe diff: unified diff shows docstring addition

## Reviewer JSON parse assessment — PASS
- Prompt rewritten with explicit JSON-only instruction
- Code fence stripping, envelope unwrapping
- Invalid verdict → blocked
- Real smoke: parsed first attempt

## Reviewer retry assessment — PASS
- Bounded: exactly one retry
- Read-only: no write permissions
- Same timeout/output cap
- Metadata tracked in result and per-round

## Safe diff in Reviewer prompt assessment — PASS
- Reviewer gets `## Staged Unified Diff` with bounded content (30K cap)
- Relative paths, no secrets, no absolute staging paths
- Computed before reviewer call

## Repair prompt context assessment — PASS
- Builder repair round gets findings + safe diff (20K cap)
- Only shown with findings (round 2+)

## Cache-noise regression assessment — PASS
All noise tests pass. Noise doesn't block.

## Meaningful target mutation assessment — PASS
Real mutations still block. Guard tests pass.

## Staged evidence assessment — PASS
Preserved in finally block, even on blocker.

## Explicit test-command assessment — PASS
Test ran in staging cwd. Real smoke: exit=0.

## JSON/report assessment — PASS
All metadata fields exported. Parse retry info in report. Lint clean.

## Target mutation assessment — PASS
Target unchanged in real smoke. No meaningful mutations.

## Test evidence (reviewer-run, commit 79d27c3)

### Targeted tests
- Pingpong CLI: **124 passed, 0.56s** (92 existing + 32 new)
- Pingpong E2E: **33 passed**
- Fulfillment: **109 passed x 2** (8.80s, 9.03s)
- Compile: clean

### Lanes
- Runtime lane: **4/4 suites passed**
- Lint: **ruff clean, mypy clean (196 files)**

### Full suite
- **7337 passed, 0 failed, 8 skipped** (233.04s)

### Post-test process/lock check
- Lock: free
- No stale processes

## Architecture guard scan
- `shell=True`: none
- Provider timeout/output cap: enforced on retry too
- Unbounded retries: exactly one, no loop
- Reviewer write permissions: never
- Malformed accepted as pass: no (blocked)
- Meaningful mutations as noise: no
- JSON pollution: clean
- Secrets: excluded

## Edited-file line-range map (reviewer-constructed, v2→v3)

| File | Lines | What changed | Tests |
|------|-------|-------------|-------|
| `pingpong_provider.py` | 113-120, 169-178, 211-240, 349-400, 412-455 | FakeProvider recoverable mode, reviewer prompt rewrite, retry prompt, envelope unwrap, code fence strip, parse_retried fields | 15 tests |
| `pingpong_loop.py` | 33-38, 80-87, 204, 215-270, 651-677, 699-720, 960-975, 1021-1024, 1058-1065 | Parse metadata fields, reviewer/repair diff, bounded retry, export, summary | 17 tests |
| `do_cmd.py` | 269-273 | Report shows parse retry metadata | 1 test |
| `test_pingpong_cli.py` | 1472-1949 | 32 new tests | Self-covering |

## Final recommendation
**READY TO DOGFOOD.** First real `staged_review_passed` achieved. All safety intact.

Exact dogfood command:
```bash
REMEDY_DATA_DIR=/tmp/remedy-data remedy do run "Add docstring to main.py:greet" \
  --builder claude-cli --reviewer claude-cli \
  --claude-cli-write-mode allowed-tools \
  --max-rounds 2 --mode staged \
  --test-command "python3 -c 'import main'" --json
```

## Merge readiness
**READY.** Zero Blocker/High/Medium open. Lint clean. All tests pass.
Once PR is created, merge-autonomy applies per memory/merge-autonomy.md.

NO PR unless user asks.
