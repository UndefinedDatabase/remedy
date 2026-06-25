# Live Review — Steps 4869-4878: Job Runner Continuation Config Truth Closure v4

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-25

## Verdict (reviewer-owned)
(pending)

## Commit reviewed
(pending — awaiting push)

## PR reviewed
(pending)

## Protocol compliance
(pending)

## Worker 5-minute quiet-window assessment
(pending)

## Reviewer 10-minute quiet-window assessment
(pending)

## Findings

### R-3001 Blocker — Paused continuation loses max_rounds
(pending — awaiting reviewer)

### R-3002 Blocker — Explicit provider override to fake is ignored
(pending — awaiting reviewer)

### R-3003 High — Omitted vs explicit options still indistinguishable
(pending — awaiting reviewer)

### R-3004 High — Test command silently drops or cannot be audited
(pending — awaiting reviewer)

### R-3005 Medium — Write mode silently changes
(pending — awaiting reviewer)

### R-3006 Medium — Execution config audit missing
(pending — awaiting reviewer)

### R-3007 Medium — Completion gate or safety regresses
(pending — awaiting reviewer)

## Step assessments
(pending — awaiting reviewer)

## Architecture guard
(pending)

## Full suite result
(pending)

## Final recommendation
(pending)

---

## Builder Handoff — Steps 4869-4878

**Builder**: Claude (agent)
**Handoff timestamp**: 2026-06-25
**Branch**: feature/steps-3276-3355-job-fulfillment-spine-v0

### What changed

**Root cause**: CLI handler collapsed omitted options to default values (`or "fake"`, `or 3`), making "omitted" indistinguishable from "explicitly set to default". This caused:
1. `max_rounds` always reset to 3 on continuation (persisted 7 lost)
2. Explicit `--builder fake` ignored after persisted `claude-cli` (both were "fake")

**Fix**: Three-layer resolution — `None` = omitted, concrete value = explicit.

#### Production code

**`apps/cli/command_catalog.py`** (L2381-2386):
- Changed `default="fake"/"3"/"2"/""/"none"` to `default=None` for all continuation-critical do.job-run args
- Help text updated: "(default: fake, persisted on continuation)"

**`apps/cli/commands/do_cmd.py`** (L697-760, L846-857):
- `_cmd_do_job_run()`: Changed param types to `str | None` / `int | None`
- Added validation for non-None provider/write-mode values
- `resolve_repair_rounds` only called when `repair_rounds is not None`
- Handler lambda: removed all `or "fake"` / `or 3` coercions, passes raw `None`

**`packages/orchestration/pingpong_job.py`** (L122-138, L253-292, L728-733, L742-824, L1168-1186):
- `ExecutionConfig`: Added `*_source` fields (builder_source, reviewer_source, max_rounds_source, test_command_source, claude_cli_write_mode_source)
- `_export_execution_config()`: Exports all source fields + `test_command_present: bool`
- `_import_execution_config()`: Imports source fields with backward-compatible defaults
- `_resolve_cfg()`: Generic resolver — explicit CLI > persisted > product default
- `run_job()`: Changed all continuation-critical params to `None`-able. Resolution block uses `_resolve_cfg()` for each field with source tracking.
- `format_job_report_text()`: Shows source info: `Builder: fake (source: cli)`

#### Test code

**`tests/orchestration/test_job_task_runner.py`** (+26 new tests, 604 lines added):

| Class | Tests | What it proves |
|-------|-------|----------------|
| `TestMaxRoundsContinuation` | 4 | max_rounds persisted on pause, restored on continuation, explicit override works, CLI handler path works |
| `TestProviderOverrideToFake` | 4 | provider persisted on pause, restored on continuation, explicit --builder fake overrides persisted claude-cli, CLI handler path works |
| `TestTestCommandContinuation` | 3 | test_command persisted, restored, override works |
| `TestWriteModeContinuation` | 3 | write_mode persisted, restored, override works |
| `TestConfigSourceAudit` | 5 | first run cli sources, first run default sources, continuation persisted sources, source in JSON report, source in text report |
| `TestCommandPathFullConfigContinuation` | 2 | all config fields survive pause/continue through handler, no config drift in report |
| `TestCommandPathExplicitOverrides` | 5 | provider override to fake, max_rounds override, repair_rounds override to 0, test_command override, report shows override |

**`_make_args()`**: Updated defaults from `"fake"/"3"/""/"none"` to `None` to match new catalog.

### Test results

| Lane | Result |
|------|--------|
| Compile check | Clean |
| Job task runner | 147 passed |
| Job fulfillment | 109 passed (2x deterministic) |
| Fast lane | 571 passed |
| Lint (ruff + mypy) | Clean |
| Full suite | 7889 passed, 8 skipped, 1 deselected, 0 failed |

### Architecture guard

All checks clean:
- No `or "fake"` / `or 3` coercion in job-run handler: CLEAN
- No git/subprocess in product code: CLEAN
- No auto-promotion: CLEAN
- No .agent refs in product code: CLEAN
- No shell=True: CLEAN
- No env/API key leakage: CLEAN
- Catalog defaults all None for continuation-critical args: CLEAN
- Completion gate uses validate_job_task_result (7 conditions): CLEAN
- Test command bounded by tc[:80] truncation: CLEAN

### Safety invariants preserved

- Staged safety: unchanged
- Promotion safety: unchanged
- Target mutation guards: unchanged
- Reviewer JSON retry: unchanged
- Artifact-set validation: unchanged
- Token accounting honesty: unchanged
- Task-file safety: unchanged
- Scope safety: unchanged
- Repair-loop bounds: unchanged
- Test-evidence dominance: unchanged
- Evidence-bundle redaction: unchanged
- Job workspace apply safety: unchanged
- Token-bounded job context: unchanged
- Completion gate: unchanged (validate_job_task_result, 7 conditions)
- Explicit promotion approval: unchanged

### Not built (per spec)

No UI, DAG scheduling, parallel execution, final target-repo job promotion, long-term memory, local LLM routing, model tournament, git commit/push/rollback/automatic promotion in product code.

### What this proves

- Paused continuation preserves ALL config fields (max_rounds, builder, reviewer, repair_rounds, test_command, write_mode)
- Copy-pasted `remedy do job-run <job_id>` does not silently change execution config
- Explicit `--builder fake` overrides persisted `claude-cli`
- Explicit `--max-rounds 3` overrides persisted `7`
- Source/audit trail shows where each config value came from (cli/persisted/default)
- Both primary bugs (R-3001, R-3002) are fixed and tested through the full CLI handler path

### What this does NOT prove

- Real Claude provider integration (tests use FakeProvider)
- Real `claude-cli` subprocess behavior
- Network/API failures during continuation
- Concurrent job runs
- Job promotion to real target repo
