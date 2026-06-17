# Simple Operator Quickstart v0

Start here. These are the main commands for working with Remedy.

## Quick start

```bash
# 1. Check if your worker is ready
remedy worker doctor claude --json

# 2. Set up the worker (enables adapter + template)
remedy worker add claude --json

# 3. Run a bounded mission loop
remedy mission run <run_id> --job-id <job_id> --json

# 4. Read the morning report
remedy mission report <run_id> --job-id <job_id> --json
```

## What these commands do

### Check readiness

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

### Run a bounded mission loop

```bash
remedy mission run <run_id> --job-id <job_id> --json
```

Options:
- `--max-steps` (default 10)
- `--max-seconds` (default 300)

The loop stops when the mission is satisfied, blocked, waiting for
approval, budget exhausted, operator stopped, max steps reached,
max seconds elapsed, no safe next action, or on error.

### Approve execution when prompted

```bash
remedy execution approve <session_id> --template claude-code-repair-v0 --json
```

Execution requires explicit operator approval per session. No blanket
approval exists. Each session references a specific command template.

### Read the morning report

```bash
remedy mission report <run_id> --job-id <job_id> --json
```

Read-only summary: what happened, whether the mission is done, what
is blocked, and what to do next. No raw logs or output.

### Review self-repair proposals

```bash
remedy self-repair proposal-list --json
remedy self-repair proposal-approve <id> --json
remedy self-repair worker-prompt <id> --json
```

Proposals are structured suggestions. They never execute anything.
Converting to a worker prompt creates a safe, bounded prompt for
an operator to give to a worker manually.

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

Low-level commands are available for debugging and advanced use.
See `docs/core-product-spine-v0.md` for the full command taxonomy.

| Facade command         | Low-level equivalent(s)                                    |
|------------------------|------------------------------------------------------------|
| `worker add claude`    | `builder adapter-enable`, `execution template-enable`      |
| `worker doctor claude` | `builder adapter-show`, `execution template-show`          |
| `worker disable claude`| `builder adapter-enable --disabled`, `execution template-disable` |
| `mission run`          | `dogfood run-loop`                                         |
| `mission report`       | `dogfood morning-report`                                   |
| `doctor core`          | (no low-level equivalent — this is the check)              |
