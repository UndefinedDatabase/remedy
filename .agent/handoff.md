# Handoff — F014 Flight Plan — Repair Round 2

Review of cb96022..42dc5f0

## State
- Branch: `feature/f014-flight-plan`
- Last commit: `42dc5f0` fix(f014): rejected plan blocks execution, audit visible, budget precedence, tag guard, postmortem (R-0130..R-0136)
- Repair commits: 2 (931ab7d..42dc5f0)

## Item-Status Table

| Item   | Status | Reason |
|--------|--------|--------|
| R-0130 | done   | `flight_plan_blocks_execution` returns "pending"\|"rejected"\|None; all 3 CLI entry points use distinct messages; `flight_plan_approval_open` is thin wrapper |
| R-0131 | done   | smoke 12r rewritten as real CLI sequence: save_job → run-next blocked → approve → status assert |
| R-0132 | done   | approved+audit → resolved info decision; pending → open blocker; both tested |
| R-0133 | done   | `resolve_job_budgets(project_root=repo)` called before `apply_plan_budgets`; config wins, plan fills gaps |
| R-0134 | done   | rejection hint changed to `f"Run: remedy do replan {job_id_str}"` |
| R-0135 | done   | `_LONG_TAG_EXEMPTIONS = {"flight_plan_v1"}` with 14-char cap; others keep 6-char guard |
| R-0136 | done   | `ev_dir.mkdir(parents=True, exist_ok=True)` before `write_postmortem`; wrapped in try/except |

## Per-Commit Changed Files

### 931ab7d chore(f014): persist R-0130..R-0136, resolve verified findings
- .agent/live_review.md
- .agent/plan.md

### 42dc5f0 fix(f014): rejected plan blocks execution, audit visible, budget precedence, tag guard, postmortem (R-0130..R-0136)
- apps/cli/commands/decision.py
- apps/cli/commands/do_cmd.py
- apps/cli/commands/job.py
- packages/orchestration/decision_queue.py
- packages/orchestration/flight_plan.py
- scripts/remedy_smoke.sh
- tests/cli/test_plan_approval.py
- tests/orchestration/schemas/test_schemas.py

## Verification — F014-scoped tests

```
$ python3 -m pytest tests/cli/test_plan_approval.py tests/cli/test_golden_path.py \
    tests/orchestration/schemas/test_schemas.py tests/orchestration/test_flight_plan.py \
    tests/schemas/test_flight_plan_schema.py -q --tb=short
221 passed in 22.87s
```

## Verification — smoke 12r probe (real CLI sequence)

```
$ bash scripts/remedy_smoke.sh 12r
--- section 12r: flight plan approval gate (real CLI) ---
[seed] created job with pending flight plan: FP_JOB_ID=<uuid>
[run-next] exit=3, stderr contains "plan awaiting approval" ✓
[approve] remedy decision resolve <id> fp:approval --reason approve → exit 0 ✓
[status] name matches, state=planned, pending_count present ✓
--- section 12r: PASS ---
```

## Verification — reject probe

```
$ python3 -c "
from packages.orchestration.flight_plan import flight_plan_blocks_execution
class J: flight_plan = {'_approval': 'rejected'}
assert flight_plan_blocks_execution(J()) == 'rejected'
print('reject probe: PASS')
"
reject probe: PASS
```

## Open Findings
0 (all R-0130..R-0136 resolved)

## Next Expected Action
Reviewer re-review of cb96022..42dc5f0
