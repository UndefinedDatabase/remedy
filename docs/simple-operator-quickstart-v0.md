# Simple Operator Quickstart v0

Operator-friendly commands for setting up a worker and running missions.
These facades call existing safe low-level rails. No auto-approval.
No auto-apply. No provider SDK integration.

## 1. Add a worker

```bash
remedy worker add claude --json
```

Enables the adapter + template for Claude Code.
Execution still requires explicit approval per session.

Known workers: `claude`, `claude-code`, `fixture`, `generic`.

## 2. Check readiness

```bash
remedy worker doctor claude --json
```

Read-only check: binary on PATH, adapter enabled, template enabled.
Reports blockers and next recommended command.

## 3. Run a bounded mission loop

```bash
remedy mission run <run_id> --job-id <job_id> --json
```

Options:
- `--max-steps` (default 10)
- `--max-seconds` (default 300)

Stops on: mission satisfied, blocked, waiting for approval,
budget exhausted, operator stop, max steps, max seconds,
no safe next action, error, or not found.

## 4. Approve execution when prompted

```bash
remedy execution approve <session_id> --template claude-code-repair-v0 --json
```

Execution requires explicit operator approval per session.

## 5. Read the morning report

```bash
remedy mission report <run_id> --job-id <job_id> --json
```

Read-only summary: what happened, is it done, what to do next.
No raw logs. No raw output.

## 6. Disable a worker

```bash
remedy worker disable claude --json
```

Disables adapter + template. Does not delete evidence or history.

## Low-level equivalents

| Facade command         | Low-level equivalent(s)                                    |
|------------------------|------------------------------------------------------------|
| `worker add claude`    | `builder adapter-enable`, `execution template-enable`      |
| `worker doctor claude` | `builder adapter-show`, `execution template-show`          |
| `worker disable claude`| `builder adapter-enable --disabled`, `execution template-disable` |
| `mission run`          | `dogfood run-loop`                                         |
| `mission report`       | `dogfood morning-report`                                   |
