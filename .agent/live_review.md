# Live Review — Steps 4827-4831: Job Task Runner v0

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-25

## Verdict (reviewer-owned)
PENDING

## Commit reviewed
(pending commit)

## PR reviewed
No open PR. Builder on `feature/steps-3276-3355-job-fulfillment-spine-v0`.

## Builder handoff

### What changed
Implemented sequential multi-task job runner. Markdown job file → ordered tasks → per-task Builder/Reviewer/Repair loop → workspace apply → job report. Real target repo never mutated.

### Files changed
- `packages/orchestration/pingpong_job.py` (new, ~420 lines): job/task model, parser, runner, apply, report
- `apps/cli/commands/do_cmd.py` L658-753: 3 CLI handlers + COMMAND_HANDLERS entries
- `apps/cli/command_catalog.py` L2354-2410: 3 CommandEntry records
- `tests/orchestration/test_job_task_runner.py` (new, ~380 lines): 34 tests, 8 classes
- `.agent/plan.md` — updated
- `.agent/context.md` — updated

### Step-by-step results

**Step 4827 — Durable job plan and task state model**
TaskEntry + JobPlan dataclasses. Task statuses: pending/running/passed/applied_to_job_workspace/blocked/failed/skipped. Job statuses: planned/running/blocked/completed. Persistence: `<data_root>/task_jobs/<job_id>/job.json`.

**Step 4828 — Deterministic job-file parser and CLI**
`parse_job_file()` regex parser for `## Task N` headings. `_cmd_do_job_plan()` CLI. No provider call. Body bounded to 2000 chars. Blocks on no tasks found.

**Step 4829 — Sequential job runner**
`run_job()` iterates pending tasks. Per task: bounded prompt → TaskInput → `run_pingpong` with `keep_staging=True`. Failed task blocks job, remaining skipped. `--max-tasks` limits execution.

**Step 4830 — Workspace apply**
`_apply_task_to_workspace()` copies staged files into job workspace. Cleans up staging. On failure: task blocked, job stopped. Task flow: pending → running → passed → applied_to_job_workspace.

**Step 4831 — Job report and tests**
JSON + text report. 34 tests: parsing (8), no-provider (1), sequential (8), report (6), token-bounded (1), existing flows (4), persistence (2), CLI dispatch (4).

### Test results
- Job task runner: 34/34 pass
- Evidence bundle: 65/65 pass
- Repair loop: 131/131 pass
- Job fulfillment: 109/109 pass
- Fast lane: 571/571 pass
- Runtime lane: 57/57 pass (4/4 suites)
- Lint: ruff clean, mypy clean (200 source files)
- Full suite: 7776 passed, 8 skipped, 1 deselected, 0 failed (241s)

### Architecture guard
All clean: no `shell=True`, no provider calls during plan, no target repo mutation, no git ops, no `os.environ`/`getenv`, no `live_review.md` dependency, no unbounded history, no full repo in prompt, no auto-promote. Task 2 waits for task 1. Task done only after review + apply.

### What this proves
- Remedy can run ordered tasks sequentially with review/repair gates
- Real target repo not mutated
- Job workspace accumulates changes
- Context is task-bounded

### What this does not prove
- Real Claude CLI dogfood
- DAG/parallel scheduling
- Final target-repo job promotion

### Carry-forward
No open findings. All prior reviewer verdicts: PASS.

### Review quiet-window
- Final review file check: 2026-06-25 ~18:20 UTC
- live_review.md last modified: overwritten for this handoff
- No reviewer activity detected
- No findings requiring Builder action
