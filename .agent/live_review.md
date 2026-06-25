# Live Review — Steps 4906-4916: Job Evidence Bundle v0

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-26

## Verdict (reviewer-owned)
**PENDING** — Awaiting builder implementation.

## Commit reviewed
(none yet — builder planning)

## Findings

### R-3401 Blocker — Job evidence export mutates state
**OPEN.** Awaiting implementation.

### R-3402 Blocker — Job evidence export calls providers or tests
**OPEN.** Awaiting implementation.

### R-3403 Blocker — Evidence bundle leaks secrets/raw prompts
**OPEN.** Awaiting implementation.

### R-3404 High — Task evidence missing or invented
**OPEN.** Awaiting implementation.

### R-3405 High — Timeline does not prove sequencing
**OPEN.** Awaiting implementation.

### R-3406 High — Workspace diff is unsafe or misleading
**OPEN.** Awaiting implementation.

### R-3407 Medium — Summary is not human-useful
**OPEN.** Awaiting implementation.

### R-3408 Medium — Existing safety regresses
**OPEN.** Awaiting implementation.

## Step assessments
(pending — no code to review yet)

## Notes
Builder updated .agent/context.md and .agent/plan.md. No production or test code changes observed. Reviewer waiting for builder to commit or signal handoff.

---

## Builder Handoff — Steps 4906-4916

**Builder**: Claude (agent)
**Handoff timestamp**: 2026-06-26
**Branch**: feature/steps-3276-3355-job-fulfillment-spine-v0

### What changed

**New file** (1):
- `packages/orchestration/job_evidence.py` — Job evidence bundle export module. Read-only, provider-free, redacted. Reuses `pingpong_evidence` redaction helpers. Exports: manifest.json, summary.md, job_report.json, job_timeline.json, tasks.json, execution_config.json, context_strategy.json, target_guard.json, workspace_apply.json, workspace.diff, task_runs/T00N/\*.

**New test file** (1):
- `tests/orchestration/test_job_evidence.py` — 32 tests covering: completed/blocked/paused export, missing task evidence, missing job, read-only, no state mutation, path traversal blocked, timeline proof, workspace diff, redaction scanner (7 secret shapes), CLI JSON redaction, machine-verifiable JSON, command catalog, handler existence, dogfood command shape.

**Modified files** (4):
- `apps/cli/command_catalog.py` — Added `do.job-evidence` entry (read_only, may_mutate_repo=False, may_execute_commands=False)
- `apps/cli/commands/do_cmd.py` — Added `_cmd_do_job_evidence()` handler + COMMAND_HANDLERS mapping
- `.agent/plan.md` — Updated for Steps 4906-4916
- `.agent/context.md` — Updated for Steps 4906-4916

### Command implemented

```bash
remedy do job-evidence <job_id> --out <dir> --json
```

### Output file layout

```
manifest.json
summary.md
job_report.json
job_timeline.json
tasks.json
execution_config.json
context_strategy.json
target_guard.json
workspace_apply.json
workspace.diff
task_runs/T001/manifest.json
task_runs/T001/summary.md
task_runs/T001/safe.diff
task_runs/T001/tests.txt
task_runs/T001/review.json
task_runs/T001/repair_loop.json
task_runs/T001/token_accounting.json
task_runs/T001/provider_evidence.json
task_runs/T002/...
```

### Step results

| Step | Description | Result |
|------|-------------|--------|
| 4906 | Job evidence bundle model | Done. `export_job_evidence()` in job_evidence.py |
| 4907 | CLI command | Done. `do.job-evidence` in catalog + handler |
| 4908 | Bundle file layout | Done. 10 top-level files + per-task nested evidence |
| 4909 | Reuse single-run evidence | Done. Uses `build_evidence_bundle()` + `write_evidence_bundle()` from pingpong_evidence |
| 4910 | Job timeline proof | Done. `job_timeline.json` with sequencing_proof events |
| 4911 | Workspace diff | Done. `workspace.diff` with unified diff, unavailable note when applicable |
| 4912 | Redaction scanner tests | Done. 7 secret shapes tested across JSON/text/CLI output |
| 4913 | Behavior tests | Done. 32 tests covering all required scenarios |
| 4914 | Dogfood command shape | Done. Catalog/handler/documented shape tests |
| 4915 | Preserve existing safety | Done. 7955 pass in full suite |
| 4916 | Architecture guard and handoff | Done |

### Test results

| Suite | Result |
|-------|--------|
| Compile | Clean |
| Job evidence | 32 passed (all new) |
| Job task runner | 181 passed |
| Job fulfillment | 109 passed (2x) |
| Evidence bundle | 65 passed |
| Fast lane | 571 passed |
| Runtime lane | 4/4 suites |
| Lint (ruff + mypy) | Clean |
| Full suite | 7955 passed, 0 failed, 8 skipped |

### What this proves

- Job-level evidence bundle exports as a single command
- Export is read-only (no providers, no mutations, no test execution)
- All output files are redacted (7 secret shapes verified)
- Raw task body bounded to 500 chars in report
- Absolute home paths sanitized to ~
- Timeline proves task sequencing
- Workspace diff shows changes without git mutation
- Completed, blocked, and paused jobs all export honestly
- Missing task evidence writes explicit unavailable note
- Per-task evidence reuses existing single-run redaction
- Path traversal blocked
- CLI JSON output is redacted
- Machine-verifiable JSON with required fields

### What this does not prove

- Real Claude CLI dogfood evidence export (need dogfood run with REMEDY_DATA_DIR)
- Large job (>10 tasks) performance
- Evidence bundle zip packaging
- Cross-machine portability of evidence paths

### 5-minute quiet-window check

**Check timestamp**: 2026-06-26
**Activity seen**: No new reviewer findings during implementation. All findings marked "awaiting implementation".
**Findings addressed**: Implementation addresses all 8 finding areas (R-3401 through R-3408).
**Findings still open**: All findings awaiting reviewer verdict on committed code.
