# Token Economy + Context Budget Optimizer v0 (Steps 1757-1796)

## Why this exists

Remedy is the Mission Control layer for agentic software work. Two product pillars: **token
reduction** and **context retention**. This block adds the first structured layer that helps Remedy
answer, safely and honestly:

- How expensive is this task likely to be?
- How much context does it need?
- Can a cheaper/local/Ollama-capable route handle it later?
- What context can be compressed?
- What context should become durable project memory?
- When should the user be asked before an expensive route?
- How does Remedy explain token/cost/context decisions?

> This block is **estimates, policy, metadata, summaries, budget recommendations, safe surfacing,
> CLI visibility, docs, and tests.** It adds **no** provider/model/Ollama/cloud/local execution and
> **no** real pricing.

## Estimated vs verified

Everything here is an **estimate**. Token counts use a deterministic `chars / 4` approximation (the
same convention as the context inspector); cost is expressed as **bands** (`low`/`medium`/`high`/
`unknown`), never as a currency amount. Public exports carry `"estimated": true` and `"verified":
false`. **Unknown stays unknown — it is never downgraded to "cheap".**

## Token economy model

- `TokenBudgetProfile` (per job): `max_context_tokens`, `max_generation_tokens`,
  `max_total_estimated_tokens`, `prefer_local_under_tokens`, `require_human_approval_over_tokens`.
  Safety floor: every budget is `>= 1`; a `<= 0` value is rejected.
- `ContextBudgetEstimate`: estimated input/output/total tokens + confidence (`estimated_low/medium`)
  + basis + warnings. Built from the existing safe context inspection (relative paths + estimated
  tokens). Missing inspection → a **warning + unknown**, never a fabricated zero presented as truth.
- `TokenEconomyDecision`: recommended worker + budget status + estimated cost/token bands +
  `requires_human_approval` + reason + catalog-valid next action.

## Context budget model

`ContextPackRecommendation` recommends a pack kind — `minimal` / `focused` / `balanced` / `full` /
`defer_for_human` — from the estimated context size vs the budget profile. It carries safe relative
included/excluded refs, a compression recommendation, durable-memory **candidates** (suggestions
only), an **estimated** token-savings band, risk notes, and a catalog-valid next action. Protected /
symlink / unsupported paths are **always excluded** and never appear in the included refs; raw file
content is never dumped.

## Local / Ollama-first relationship

Cheap, small tasks (estimated tokens under `prefer_local_under_tokens`) should prefer a local /
Ollama-capable route **when safe**. This is metadata only: the Ollama worker is a non-executable
placeholder (from Worker Registry v0), so the recommendation points to **configuration / planning**,
never execution.

## Expensive route justification

Expensive, unknown-cost, high-risk, external, cloud, and placeholder routes **always** require
human-facing approval — this reuses the Worker Registry hard-safety floor
(`hard_safety_requires_approval`) and cannot be weakened by any budget setting. A decision also
requires approval when the estimated total exceeds the budget or the approval-token threshold.

## User-facing budget explanations

Every warning is plain and actionable: "estimated context exceeds the budget — recommend compressing
to the budget cap or selecting a focused pack (estimate, not verified)". The user is never told a
number is verified when it is an estimate.

## Future relationships

- **MemPalace**: the `memory_candidates` here are suggestions only. A future MemPalace block can
  retain durable knowledge across runs; nothing is persisted as memory in this block.
- **Model/Route Tournament**: the estimated bands + budget signals created here are the inputs a
  future Tournament Harness can compare routes with.
- **Context Budget Optimizer enforcement**: a future block can turn these recommendations into an
  enforcing (still human-gated) optimizer.

## CLI

```
remedy token budget-show <job_id> --json
remedy token budget-set <job_id> [--max-context-tokens N] [--max-generation-tokens N]
                                 [--max-total-estimated-tokens N] [--prefer-local-under-tokens N]
                                 [--require-human-approval-over-tokens N] --json
remedy token estimate <job_id> [--task-id ID] [--route-id ID] --json
remedy token economy-report <job_id> [--task-id ID] [--route-id ID] --json
remedy context-pack recommend <job_id> [--task-id ID] [--route-id ID] --json
```

All catalog + run_contract backed. `budget-set` is `write_metadata`; the rest are `read_only`. None
carry `may_execute_commands`. None execute a worker.

## Anti-goals (explicit)

- **No provider/model/Ollama/cloud/local execution.** No network, browser, subprocess, shell, MCP.
- **No real provider pricing** and no pricing sync / web calls — all costs are estimated bands.
- **No durable memory** persisted — memory candidates are suggestions only.
- **No** Model/Route Tournament, MemPalace implementation, auto-apply/approve/test/repair, auto-PR/
  git, or UI redesign in this block.
- Estimates are never presented as verified truth; unknown is never treated as cheap.
