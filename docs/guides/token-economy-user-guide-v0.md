# Token budgets and context packs — user guide (v0)

This guide explains, in plain language, how Remedy estimates token usage and recommends context
packs. None of this runs a model or spends real money — it helps you see costs **before** they
happen and keep work cheap and focused.

## Why Remedy estimates token usage

Every task uses some context (the files and summaries a worker sees) and produces some output. Both
cost tokens. Remedy gives you an **estimate** up front so you can decide whether a task is cheap
enough to run locally, or expensive enough that you want to look first. Estimates are approximations
(roughly four characters per token) — they are clearly labeled `estimated`, never `verified`.

```
remedy token estimate <job_id> --json
remedy token economy-report <job_id> --json
```

## Setting a budget

A token budget profile sets soft caps for a job: how much context, how much generation, and the
total you're comfortable with — plus the point where Remedy should prefer a local route, and the
point where it should ask you before anything expensive.

```
remedy token budget-show <job_id> --json
remedy token budget-set <job_id> --max-total-estimated-tokens 40000 \
                                 --prefer-local-under-tokens 8000 \
                                 --require-human-approval-over-tokens 120000 --json
```

Budgets always stay positive — a zero or negative value is rejected.

## Why cheap tasks should use local / Ollama routes later

Small, routine tasks don't need an expensive model. Remedy prefers a **local** route for cheap tasks
to cut token spend and keep work on your machine. Once a real Ollama adapter exists, the same
preference can route cheap tasks to Ollama. Today the Ollama worker is a **placeholder** — Remedy
will recommend *configuring* it, and will never pretend it can run yet.

## Why expensive models need justification

Expensive, unknown-cost, or high-risk routes are powerful but costly and riskier. Remedy **always**
asks for your approval before recommending them — and this safety floor cannot be turned off by a
budget setting. If your estimated tokens go over budget or over your approval threshold, Remedy asks
first.

## What context packs are

A context pack is the bundle of context a worker would see. Remedy recommends a **pack kind**:

- **minimal** — tiny context, cheapest
- **focused** — just the task-relevant context
- **balanced** — fits the budget comfortably
- **full** — everything (may exceed budget)
- **defer for human** — Remedy can't safely decide; you choose

```
remedy context-pack recommend <job_id> --json
```

Protected files (secrets, `.env`, `.git`, …) are **always excluded** from a pack, and Remedy never
dumps raw file contents into a recommendation.

## What compression means

When the estimated context is larger than your budget, Remedy recommends **compressing** to a
smaller pack — trimming to the budget or choosing a focused pack. It shows an **estimated** token
savings band (low/medium/high). It never claims the savings are verified.

## How this prepares long-term project memory

Some context (project manifests, READMEs) is durable knowledge worth keeping across runs. Remedy
lists these as **memory candidates** — *suggestions only*. Nothing is stored as long-term memory in
this version; a future MemPalace layer will handle that.

## What is *not* built yet

- Remedy does **not** run Ollama, cloud, or any model in this version.
- Token and cost numbers are **estimates** (bands), not billed measurements.
- No durable project memory is stored yet — memory candidates are suggestions.
- There is no automatic apply, approve, test, or PR here — you stay in the loop.
