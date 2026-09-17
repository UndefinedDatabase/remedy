# Simple Operator Quickstart v0

Start here. These are the main commands for working with Remedy.

## Quick start

```bash
# 1. Create and start a job
remedy do run "Fix the login bug" --repo /path/to/project

# 2. Check job state and read the job report
remedy job show <job_id> --full --json

# 3. Open the UI
remedy ui <job_id>

# 4. Review proposed follow-ups
remedy decision list <job_id> --json
```

## What these commands do

### Create a job

```bash
remedy do run "<goal>" --repo <path>
```

Creates a new job from your goal and starts the first safe actions.
This is the normal entry point for Remedy.

### Check job status

```bash
remedy job show <job_id> --full --json
```

Read-only view of job state: tasks done, pending, blockers, and
the next safe action. Its `report` section is the job's progress
report: task details, evidence count, artifact count, and the run
report. No raw logs, no execution, no side effects.

### Check core health

```bash
remedy doctor core --json
```

Read-only check: all core modules loadable, test lane scripts present.

## What Remedy does NOT do automatically

- Apply code changes
- Create PRs or commits
- Execute providers (Claude, GPT, Ollama)
- Approve sessions
- Run tests without approval
- Deploy anything

## Advanced commands

Low-level and internal commands are available for debugging and advanced use.
See `docs/core-product-spine-v0.md` for the full command taxonomy.

| Normal command           | Advanced equivalent(s)                                     |
|--------------------------|------------------------------------------------------------|
| `job show <id> --full`   | `job show <id>`, `mission report <run_id> --job-id <id>`   |
| `job run-loop <id>`      | `mission run <run_id> --job-id <id>`                       |
| `doctor core`            | (no low-level equivalent — this is the check)              |

Note: `mission` commands are an advanced/internal facade for mission contract
bounded loops. For normal operation, use `job` commands.

## First fulfilled job demo (commands deleted 2026-09-16)

```bash
# The `create` word under `job` built the job here, until F280 round 6 deleted it; the fixture
# fulfillment step that followed was deleted by round 3. `do run "<goal>"` is the CLI's own
# job-creation path today.
remedy job attach-repo "$JOB_ID" /path/to/repo

# Check result
remedy job show "$JOB_ID" --full --json
remedy decision list "$JOB_ID" --json
```

F280 round 3 deleted the `fulfill` word of the `job` group, which ran this demo in fixture mode
(no real provider), and round 6 deleted the `create` word, so the demo no longer runs. See
`docs/first-fulfilled-job-demo-v0.md` for what it did.
