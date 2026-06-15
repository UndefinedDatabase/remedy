# Choosing workers and routes — user guide (v0)

This guide explains, in plain language, how you tell Remedy **which workers** it may use and **how**
it should pick between them. None of this makes Remedy run a worker — it only shapes what Remedy
*recommends* and what it asks you to approve.

## The idea in one line

> Workers do the building. Remedy governs. You choose or limit which workers and routes are allowed.

## What is a "worker"?

A worker is anything that could do a piece of work: a local model, an external builder you hand a
task to, a future Ollama model, a future cloud model, the reviewer, or **you** (the human operator).
Each worker is described by a small, swappable spec — its kind, its rough cost, its risk, and what
it is allowed to do. You can list them:

```
remedy worker registry-list --json
remedy worker registry-show local.candidate_generator --json
```

Some workers are **placeholders** (`ollama.placeholder`, `cloud.placeholder`). They are listed so
the system is ready for them, but they are **not runnable yet** — Remedy will never pretend they
are, and will never call Ollama or a cloud provider in this version.

## Why cheap tasks prefer local / Ollama

Small, routine fixes don't need an expensive model. By default Remedy prefers a **local** route for
cheap tasks, because local routes reduce token spend and keep your work on your machine. Once a real
Ollama adapter exists, the same preference can route cheap tasks to Ollama. Today this is a
preference *setting* — it changes recommendations, not execution.

```
remedy route-policy set <job_id> --prefer-local-for-cheap-tasks --json
remedy route-policy set <job_id> --prefer-ollama-for-cheap-tasks --json
```

## Why expensive models need justification

Expensive or high-risk routes (e.g. a future cloud model) are powerful but costly and riskier. By
default Remedy **requires human approval** before recommending them, and an unknown-cost route is
treated as *not cheap* — it never slips through a cost ceiling. You can tighten this further:

```
remedy route-policy set <job_id> --max-cost-tier cheap --json
remedy route-policy set <job_id> --max-risk-tier medium --json
remedy route-policy set <job_id> --require-human-approval-for-expensive --json
```

## Choosing or blocking specific workers

```
remedy route-policy set <job_id> --select-worker external.builder_package --json   # you pick this one
remedy route-policy set <job_id> --prefer-worker local.candidate_generator --json  # nudge toward it
remedy route-policy set <job_id> --block-worker cloud.placeholder --json           # never use it
```

Your selection wins **among eligible workers**. If you select a worker that is disabled or blocked,
Remedy refuses safely rather than silently doing something else.

## See what the policy would recommend

```
remedy route-policy show <job_id> --json
remedy route-policy evaluate <job_id> --task-type repair --json
```

`evaluate` tells you the recommended worker, whether it needs your approval, and the safe next
command. It does **not** start any work.

## Why Remedy never trusts a worker blindly

Whatever a worker produces — local, external, or future cloud — is **untrusted input**. It goes
through the same quarantine → Trust Gate → Verification → human approval path before anything is
applied. The route policy decides *who is allowed to try*; it never decides *what is true*.

## How this connects to what's coming

- A **Model/Route Tournament** can later compare routes using real quality evidence.
- **MemPalace project memory** can later feed long-term context into route choices.
- A **Context Budget Optimizer** can turn today's estimated token/context bands into active budgets.

## What is *not* built yet (be clear with yourself)

- Remedy does **not** run Ollama, cloud, or external models in this version.
- Token and cost numbers are **estimates** (bands), not billed measurements.
- There is no automatic apply, approve, test, or PR here — you stay in the loop.
