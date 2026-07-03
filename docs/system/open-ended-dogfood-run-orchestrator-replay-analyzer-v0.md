# Open-Ended Dogfood Run Orchestrator + Replay Analyzer v0

> Steps 2146-2205. Workers execute. Remedy governs.

## Why This Is Not Fixed Run Profiles

Fixed-duration profiles (`quick-5min`, `focused-1h`, `overnight`) are wrong because:

- They force work to fill a time box, producing busywork or early idle time.
- They conflate *duration* with *scope*. A 5-minute run that finishes its task is better than a
  1-hour run that pads to fill its slot.
- They cannot handle blocked/waiting states honestly — a run stuck waiting for builder output
  should not count idle time against a "focused" budget.

**A task should finish when it is done.** An open-ended run stops when:

1. The mission is satisfied (all acceptance criteria met with evidence).
2. The run is blocked (waiting for human decision, approval, or external input).
3. Budget is exhausted (token budget, step count, or wall-clock ceiling).
4. The operator stops it (`remedy dogfood stop`).
5. An unrecoverable error occurs.

## Open-Ended Run Lifecycle

```
create  ->  step  ->  step  ->  ...  ->  terminal state
  |           |         |                    |
  v           v         v                    v
not_started  running   running/waiting   satisfied / blocked / stopped / budget_exhausted / error
```

Each `step_dogfood_run()` call performs **one safe, bounded action**:

- Evaluate the current state of the mission contract.
- Determine what lane needs attention (mission, builder, reviewer, test, repair).
- Propose one next safe action.
- Record the step in the checkpoint log.
- Return control to the caller.

The caller (CLI, UI, or future automation) decides whether to call `step` again. There is no
internal loop that steps forever. The run is inspectable at any time between steps.

## Run Policies / Guardrails

A `DogfoodRunPolicy` constrains the run:

| Policy field           | Default  | Purpose                                          |
|------------------------|----------|--------------------------------------------------|
| `max_steps`            | 100      | Hard ceiling on step count                       |
| `max_tokens_estimated` | 500_000  | Estimated token budget (from token_economy)      |
| `max_wall_minutes`     | 480      | Wall-clock ceiling (8 hours)                     |
| `require_clean_review` | True     | Run cannot satisfy without clean review           |
| `require_tests_green`  | True     | Run cannot satisfy without tests passing          |
| `require_proof_chain`  | False    | Run cannot satisfy without proof chain            |
| `allowed_lanes`        | all      | Which lanes may be active                        |
| `forbidden_actions`    | standard | Actions that are never proposed                  |
| `auto_step`            | False    | Whether automation may call step without operator |

Policy is immutable after run creation. To change policy, create a new run.

## Lanes

A lane is a category of work the run may engage in. Each step targets exactly one lane.

| Lane        | Purpose                                          | Autonomous? |
|-------------|--------------------------------------------------|-------------|
| `mission`   | Evaluate mission contract, determine satisfaction | Yes         |
| `builder`   | Coordinate builder sessions (export/import)       | No (approval-gated) |
| `reviewer`  | Check review findings, parse live review          | Yes (read-only) |
| `test`      | Run tests, check results                         | Gated       |
| `repair`    | Process repair loop items                        | No (approval-gated) |
| `brainstorm`| Metadata-only: record brainstorm ideas for later | Yes (metadata-only) |

Lane status is tracked per-step in the checkpoint. A lane can be `idle`, `active`, `waiting`,
`blocked`, or `done`.

## Checkpoint / Replay Model

Every step appends a `DogfoodRunCheckpoint` to an append-only checkpoint log:

```python
@dataclass
class DogfoodRunCheckpoint:
    checkpoint_id: str       # uuid
    run_id: str
    step_index: int
    timestamp: str           # UTC ISO
    lane: str                # which lane was targeted
    action_taken: str        # what the step did (safe summary)
    outcome: str             # result (safe summary)
    run_status: str          # status after this step
    lane_statuses: dict      # {lane: status} snapshot
    blocking_reasons: list   # current blockers
    next_suggested_action: str  # what should happen next
    token_estimate_used: int # estimated tokens consumed this step
    cumulative_tokens: int   # running total
    cumulative_steps: int    # running total
    wall_elapsed_seconds: float  # since run creation
```

Checkpoints are stored as JSONL (`checkpoints.jsonl`) under the run directory. They form the
complete replay log — the replay analyzer reads these to explain what happened.

## Replay Analyzer

`analyze_dogfood_run_replay(run_id, data_dir)` reads the checkpoint log and produces a
`DogfoodReplayAnalysis`:

- **Timeline**: ordered list of steps with lane, action, outcome.
- **Lane summaries**: per-lane statistics (steps taken, time spent, outcomes).
- **Blocking episodes**: periods where the run was waiting/blocked, with reasons.
- **Satisfaction trajectory**: how close the run got to satisfying criteria over time.
- **Token usage curve**: cumulative token consumption over steps.
- **Anomalies**: steps that took unusually long, lanes that never activated, budget warnings.

The replay analyzer works on both completed and in-progress runs. An operator can call
`remedy dogfood replay <run_id>` after 5 minutes, 1 hour, or overnight and get a coherent
explanation of what happened and what should happen next.

## How Logs Become Remedy Repair Suggestions

The replay analyzer inspects the checkpoint log for:

1. **Test failures** → links to `repair_loop_v2` items for the same job.
2. **Review findings** → links to `overnight_mission` open findings.
3. **Builder errors** → suggests creating a repair item if none exists.
4. **Repeated blockers** → suggests operator intervention.

These become `next_actions` in the replay analysis, not automatic execution. The operator
decides what to act on.

## How an Operator Can Inspect

At any point between steps:

| Command                        | What it shows                              |
|--------------------------------|--------------------------------------------|
| `remedy dogfood show <run_id>` | Current status, policy, latest checkpoint  |
| `remedy dogfood status`        | All active runs with status summary        |
| `remedy dogfood replay <run_id>` | Full replay analysis                     |
| `remedy dogfood checkpoints <run_id>` | Raw checkpoint log                  |
| `remedy dogfood next <run_id>` | What the next step would do (dry-run)      |

No step executes without the operator's knowledge. Between steps, the run state is fully
queriable, coherent, and safe.

## What Is Not Automated Yet

- **No provider/model execution**: Steps propose actions but do not call Claude/Pi/OpenCode/Ollama.
- **No auto-apply**: Even when a repair candidate is ready, apply requires approval.
- **No auto-PR**: No git/PR automation.
- **No real brainstorm agents**: Brainstorm lane records metadata only (idea, rationale, evidence
  needed) — no agent spawning.
- **No unbounded loops**: The step function returns after one action. The caller loops.
- **No MCP/MemPalace**: No internal memory, embeddings, or vector DB.

## Storage Layout

```
<data_root>/workspaces/<job_id>/dogfood_runs/
    <run_id>/
        run.json              # DogfoodRunRecord
        checkpoints.jsonl     # append-only checkpoint log
        replay.json           # cached replay analysis (regenerated on demand)
        brainstorm/           # brainstorm lane metadata
            <idea_id>.json
```

## Module Structure

- `packages/orchestration/dogfood_run.py` — models, storage, evaluator, stepper, replay analyzer
- `apps/cli/commands/dogfood.py` — CLI command handlers
- `tests/orchestration/test_dogfood_run.py` — targeted tests
