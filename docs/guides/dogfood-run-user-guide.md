# Dogfood Run User Guide

## Quick Start

```bash
# Create a dogfood run for a job
remedy dogfood create <job_id>

# Step through the run (one safe step at a time)
remedy dogfood step <run_id> <job_id>

# Check what the next step would do (dry-run)
remedy dogfood next <run_id> <job_id>

# See current run status
remedy dogfood show <run_id> <job_id>

# Stop the run
remedy dogfood stop <run_id> <job_id> --reason "done for now"

# Replay analysis (works during or after the run)
remedy dogfood replay <run_id> <job_id>
```

## How It Works

A dogfood run is an **open-ended, step-at-a-time** orchestration loop. Each call to
`remedy dogfood step` performs exactly one safe action:

1. Evaluates the mission contract for the job.
2. Determines which lane (mission, builder, reviewer, test, repair) needs attention.
3. Proposes one next action.
4. Records a checkpoint.

The run stops when:
- Mission is satisfied (all criteria met with evidence)
- Run is blocked (waiting for human/external input)
- Budget is exhausted (steps, tokens, or wall-clock)
- Operator stops it

There are **no fixed time profiles**. A run finishes when the work is done.

## Commands

| Command | Purpose |
|---------|---------|
| `dogfood create` | Create a new run with configurable policy |
| `dogfood show` | Show run details |
| `dogfood status` | List all runs |
| `dogfood step` | Execute one step |
| `dogfood stop` | Stop a run |
| `dogfood next` | Dry-run: what would the next step do? |
| `dogfood evaluate` | Evaluate state without stepping |
| `dogfood replay` | Full replay analysis |
| `dogfood checkpoints` | Raw checkpoint log |
| `dogfood brainstorm` | List brainstorm ideas |

## Policy Configuration

When creating a run, you can set budget limits:

```bash
remedy dogfood create <job_id> \
  --max-steps 50 \
  --max-tokens 200000 \
  --max-wall-minutes 60
```

Defaults: 100 steps, 500K tokens, 480 minutes (8 hours).

## Inspecting Runs

At any point between steps, the run is fully queryable:

```bash
# JSON output for programmatic use
remedy dogfood show <run_id> <job_id> --json
remedy dogfood replay <run_id> <job_id> --json
```

The replay analyzer explains:
- Timeline of steps with lane/action/outcome
- Per-lane statistics
- Blocking episodes
- Token usage curve
- Anomalies and next suggested actions

## Limitations

- **No provider execution**: Steps propose actions but never call Claude/Pi/OpenCode/Ollama.
- **No auto-apply**: Patches require approval.
- **No auto-PR**: No git/PR automation.
- **No brainstorm agents**: Brainstorm lane records ideas as metadata only.
