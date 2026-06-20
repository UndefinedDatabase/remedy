# Simple Operator Quickstart v0

Start here. These are the main commands for working with Remedy.

## Quick start

```bash
# 1. Create and start a job
remedy do run "Fix the login bug" --repo /path/to/project

# 2. Check job state
remedy job status <job_id> --json

# 3. Read the job report
remedy job report <job_id> --json

# 4. Open the UI
remedy ui <job_id>

# 5. Review results
remedy review run <job_id> --json
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
remedy job status <job_id> --json
```

Read-only view of job state: tasks done, pending, blockers, and
the next safe action. No execution, no side effects.

### Read the job report

```bash
remedy job report <job_id> --json
```

Read-only report of job progress: task details, evidence count,
artifact count. No raw logs or output.

### Check worker readiness

```bash
remedy worker doctor claude --json
```

Read-only check: binary on PATH, adapter enabled, template enabled.
Reports blockers and next recommended command if not ready.

### Add a worker

```bash
remedy worker add claude --json
```

Enables the adapter and template metadata for Claude Code.
This does NOT execute the worker. Execution still requires
explicit approval per session.

Known workers: `claude`, `claude-code`, `fixture`, `generic`.

### Check core health

```bash
remedy doctor core --json
```

Read-only check: all core modules loadable, test lane scripts present.

### Disable a worker

```bash
remedy worker disable claude --json
```

Disables adapter + template. Does not delete evidence or history.

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
| `job status <id>`        | `job summary <id> --json`, `job show <id>`                 |
| `job report <id>`        | `mission report <run_id> --job-id <id>`                    |
| `job run-loop <id>`      | `mission run <run_id> --job-id <id>`                       |
| `worker add claude`      | `builder adapter-enable`, `execution template-enable`      |
| `worker doctor claude`   | `builder adapter-show`, `execution template-show`          |
| `worker disable claude`  | `builder adapter-enable --disabled`, `execution template-disable` |
| `doctor core`            | (no low-level equivalent — this is the check)              |

Note: `mission` commands are an advanced/internal facade for mission contract
bounded loops. For normal operation, use `job` commands.

## First fulfilled job demo

```bash
# Create a job, attach a repo, and run fixture fulfillment
remedy job create "Improve docs" --json
remedy job attach-repo <job_id> /path/to/repo
remedy job fulfill <job_id> --fixture-demo --json

# Check result
remedy job status <job_id> --json
remedy job report <job_id> --json
remedy propose list --job-id <job_id> --json
```

This demo uses fixture mode (no real provider). See `docs/first-fulfilled-job-demo-v0.md`.
