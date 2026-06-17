# Core Product Spine v0

## What Remedy is today

Remedy is a structured repair and improvement system for software projects.
It helps operators track what needs fixing, plan repairs, manage builder
workers, and verify that repairs are safe and correct.

Remedy does NOT automatically execute repairs, approve changes, create PRs,
or deploy code. Every action that changes the project requires explicit
operator approval.

## The main operator flow

```
1. Add a worker       →  remedy worker add claude --json
2. Check readiness    →  remedy worker doctor claude --json
3. Run a mission      →  remedy mission run <run_id> --job-id <job_id> --json
4. Read the report    →  remedy mission report <run_id> --job-id <job_id> --json
5. Approve if safe    →  remedy execution approve <session_id> --template <id> --json
6. Review proposals   →  remedy self-repair proposal-list --json
7. Use as prompt      →  remedy self-repair worker-prompt <proposal_id> --json
```

Each step is explicit. No step runs automatically from the previous one.

## What a worker is

A worker is an external tool (like Claude Code) that Remedy can delegate
repair tasks to. Workers are not embedded in Remedy — they run as separate
processes through bounded command templates.

Adding a worker (`remedy worker add claude`) enables the adapter and template
metadata. It does NOT execute the worker or create any sessions.

## What a mission is

A mission (internally called a "dogfood run") is a bounded repair loop.
Each step evaluates the current state, decides the next safe action, and
records evidence. The loop stops when the mission is satisfied, blocked,
waiting for approval, budget-limited, or out of safe next actions.

Running a mission (`remedy mission run`) calls the bounded loop with
configurable max-steps and max-seconds limits.

## What a report is

A morning report (`remedy mission report`) is a read-only summary of the
current mission state. It shows what happened, whether the mission is done,
what is blocked, and what to do next. It does not execute anything.

## What approval means

Before any worker can execute a command, an operator must explicitly approve
the execution session. Approval is per-session, not blanket. The approval
references a specific command template that constrains what the worker can do.

## What self-repair proposals are

Self-repair proposals are structured suggestions for improvements that
Remedy generates based on its own evidence. They are metadata records, not
executed actions.

An operator can:
- List proposals: `remedy self-repair proposal-list --json`
- Approve a proposal: `remedy self-repair proposal-approve <id> --json`
- Deny a proposal: `remedy self-repair proposal-deny <id> --json`
- Edit a proposal: `remedy self-repair proposal-edit <id> --json`
- Convert to worker prompt: `remedy self-repair worker-prompt <id> --json`

Converting to a worker prompt creates a safe, bounded prompt for the operator
to give to a worker. The proposal itself never executes anything.

## Command taxonomy

### Operator-facing (normal use)

| Command | What it does | Mutates? | Executes? | Approval? |
|---------|-------------|----------|-----------|-----------|
| `worker doctor <name>` | Check readiness | No | No | No |
| `worker add <name>` | Enable adapter + template | Metadata | No | No |
| `worker disable <name>` | Disable adapter + template | Metadata | No | No |
| `mission run <id>` | Bounded repair loop | Metadata | No* | No |
| `mission report <id>` | Morning report | No | No | No |
| `execution approve <id>` | Approve a session | Metadata | No | Yes (this IS approval) |
| `self-repair proposal-list` | List proposals | No | No | No |
| `self-repair proposal-approve <id>` | Approve proposal | Metadata | No | No |
| `self-repair proposal-deny <id>` | Deny proposal | Metadata | No | No |
| `self-repair worker-prompt <id>` | Get worker prompt | No | No | No |
| `config list/show/get` | View config | No | No | No |
| `review bundle` | Review evidence | No | No | No |
| `progress checklist` | See progress | No | No | No |

*`mission run` orchestrates steps but does not execute external processes
without prior explicit approval.

### Advanced / internal rails

| Command | What it does | When to use |
|---------|-------------|-------------|
| `builder adapter-show/enable/list` | Direct adapter management | Debugging adapter state |
| `execution template-show/enable/disable/update` | Direct template management | Debugging templates |
| `execution run/show/list` | Direct execution control | Debugging execution |
| `execution debug-bundle` | Execution debug info | Investigating failures |
| `execution operator-runbook` | Runbook for approvals | Learning the approval flow |
| `execution claude-doctor` | Claude-specific diagnostics | Claude Code troubleshooting |
| `dogfood create/show/step/stop/replay` | Direct mission internals | Debugging mission state |
| `dogfood run-loop/morning-report` | Low-level loop/report | Same as mission run/report |
| `builder session-create/show/intake` | Direct session management | Debugging sessions |
| `self inspect/plan/propose/reconcile` | Self-dogfood internals | Development |
| `config set/init/validate` | Config mutations | Initial setup |

### Future / experimental

| Command | Status |
|---------|--------|
| `overnight *` | Overnight planning framework — not operator-ready |
| `local-advisor *` | Optional Ollama advisory — disabled by default |
| `local-candidate *` | Local model candidate gen — disabled by default |
| `tournament *` | Model comparison harness — evaluation only |
| `external-builder *` | External builder ingress — quarantine only |

## What Remedy still does not automate

1. **Code application** — patches are never applied without operator approval
2. **PR/git operations** — no automatic commits, branches, or PRs
3. **Provider execution** — no automatic calls to Claude, GPT, or any model
4. **Test execution** — tests run only through the safe runner with approval
5. **Deployment** — no deployment capability
6. **Secret management** — no API keys stored in config
7. **Network calls** — no outbound network requests from core
8. **Full overnight autonomy** — the loop is bounded and stops for approval

## Blockers for full overnight autonomy

1. Execution approval is per-session manual (no safe auto-approve policy yet)
2. No automatic test verification after repair
3. No automatic rollback on failure
4. No budget-aware auto-stop with operator notification
5. No safe PR creation from verified repairs
