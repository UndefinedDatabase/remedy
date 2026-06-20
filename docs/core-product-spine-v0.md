# Core Product Spine v0

## What Remedy is today

Remedy is a structured repair and improvement system for software projects.
It helps operators track what needs fixing, plan repairs, manage builder
workers, and verify that repairs are safe and correct.

Remedy does NOT automatically execute repairs, approve changes, create PRs,
or deploy code. Every action that changes the project requires explicit
operator approval.

## Product terminology

| Term | Meaning |
|------|---------|
| **Job** | The thing the user wants done — primary work item. |
| **Run** | One attempt to work on a job. |
| **Worker** | An external tool (like Claude Code) that does the work. |
| **Approval** | Human or policy permission to proceed with an action. |
| **Policy** | Rules governing what can be approved automatically. |
| **Evidence** | Structured proof of what happened during a run. |
| **Review** | Checking the result of a run. |
| **Report** | Summary of job state and next safe action. |
| **Mission Contract** | Internal/advanced completion criteria for a job. |

## The main operator flow

```
1. Create a job       →  remedy do run "<goal>" --repo <path>
2. Check job state    →  remedy job status <job_id> --json
3. Read the report    →  remedy job report <job_id> --json
4. Open the UI        →  remedy ui <job_id>
5. Review results     →  remedy review run <job_id> --json
6. Check worker       →  remedy worker doctor <name> --json
7. Approve if needed  →  remedy approval summary --json
```

Each step is explicit. No step runs automatically from the previous one.

## What a job is

A job is the primary user-facing work item. It holds the user’s goal,
planned tasks, evidence, and completion state. All Remedy product flows
start with a job.

## What a worker is

A worker is an external tool (like Claude Code) that Remedy can delegate
tasks to. Workers are not embedded in Remedy — they run as separate
processes through bounded command templates.

Adding a worker (`remedy worker add claude`) enables the adapter and template
metadata. It does NOT execute the worker or create any sessions.

## What a report is

A job report (`remedy job report`) is a read-only summary of the current
job state. It shows tasks, progress, evidence, and what to do next.
It does not execute anything.

## What a mission contract is

A mission contract is an internal/advanced "definition of done" for a job.
It defines completion criteria that the bounded run loop evaluates.
Normal users interact with jobs — mission contracts are an advanced concept
used by the autonomy loop internally.

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

### Primary operator path

| Command | What it does | Mutates? | Executes? |
|---------|-------------|----------|-----------|
| `do "<goal>" --repo <path>` | Create and start a job | Yes | No* |
| `job status <id> --json` | Show job state | No | No |
| `job report <id> --json` | Read job progress report | No | No |
| `job run-loop <id> --json` | Contract-gated autonomy loop | Metadata | No* |
| `ui <id>` | Open interactive UI | No | No |
| `review run <id> --json` | Reviewer recommendations | No | No |
| `worker doctor <name>` | Check worker readiness | No | No |
| `worker add <name>` | Enable adapter + template | Metadata | No |
| `config list/show/get` | View config | No | No |
| `review bundle <id>` | Review evidence bundle | No | No |
| `job fulfill <id> --fixture-demo` | Run fixture fulfillment demo | Metadata+repo | No* |

*These commands orchestrate steps but do not execute external processes
without prior explicit approval.

### Advanced operator path

| Command | What it does | When to use |
|---------|-------------|-------------|
| `approval summary/show/enable` | Execution approval policy | Advanced autonomy setting |
| `mission run/report` | Mission contract facade | Internal bounded loops |
| `execution approve/run/show` | Direct execution control | Debugging execution state |
| `builder adapter-show/enable/list` | Direct adapter management | Debugging adapter state |
| `overnight *` | Bounded overnight preparation | Pre-run planning |

### Developer / internal path

| Command | What it does | When to use |
|---------|-------------|-------------|
| `dogfood create/step/show/stop/replay` | Mission internals | Debugging mission state |
| `self inspect/plan/propose/reconcile` | Self-dogfood internals | Development |
| `self-repair *` | Self-repair proposals | Development-time |
| `local-advisor *` | Ollama advisory | Disabled by default |
| `local-candidate *` | Local model candidate gen | Disabled by default |
| `tournament *` | Model comparison harness | Evaluation only |
| `external-builder *` | External builder ingress | Quarantine only |

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
