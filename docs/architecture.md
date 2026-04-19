# Remedy Architecture

## What Remedy Is

Remedy is a modular orchestration kernel. It coordinates tasks, manages artifacts, and enforces acceptance criteria. It does not implement intelligence itself — it delegates to providers.

Remedy is designed to be embedded as a library inside a larger system. It does not own the process, the event loop, or the configuration system. A host application wires the providers and runs Remedy as a module.

## Core Principles

### Strict Core / Provider Separation

The `packages/core` and `packages/contracts` packages have **no external dependencies**. They define models and interfaces only. All integrations (LLMs, runtimes, memory systems) live in `packages/providers/` and are wired in at the application layer.

```
core/contracts  ←  no external deps; models + interfaces only
       ↑
orchestration   ←  depends on contracts only
       ↑
memory/runtimes ←  provider-agnostic internal layers (see below)
       ↑
providers       ←  concrete adapters; implement contracts; depend on external systems
       ↑
apps            ←  wire everything together
```

### Package Roles

**`packages/memory/`** — Provider-agnostic memory management layer. Implements caching, indexing, and query logic on top of whatever `MemoryGateway` implementation is active. It does not depend on any specific storage backend. MemPalace or any other system plugs in via the gateway interface.

**`packages/runtimes/`** — Provider-agnostic runtime abstraction layer. Handles command scheduling, timeout enforcement, and output capture. The concrete execution environment (local shell, Docker, remote sandbox) is supplied by a `RuntimeProvider` adapter. This layer does not know whether it is running locally or in a container.

**`packages/providers/mempalace/`** — Concrete adapter: implements `MemoryGateway` backed by MemPalace. This is the only package that knows about MemPalace internals. Replace this adapter to swap the memory backend without touching `packages/memory/` or orchestration.

**`packages/providers/docker_runtime/`** — Concrete adapter: implements `RuntimeProvider` backed by Docker. This is the only package that knows about Docker. Replace this adapter to swap the execution environment without touching `packages/runtimes/` or orchestration.

### Artifact-Driven Workflow

Work is expressed as `Job → Task → Artifact`, not as prompt strings. Artifacts are explicit, typed outputs with provenance. Workflows are not driven by raw prompts.

**Artifact provenance (`task_id`):**
- `task_id = <UUID>` — artifact was produced by that specific Task execution.
- `task_id = None` — artifact was produced by orchestration or system logic (e.g. planning output, job metadata). It is not tied to any single Task.

This convention makes the source of every artifact unambiguous without requiring a separate artifact type hierarchy.

### Memory Gateway

All memory access goes through the `MemoryGateway` interface. No component reaches into a memory system directly. This makes the memory backend replaceable without touching orchestration logic.

### Composability

Every layer is replaceable:
- Swap the LLM provider without changing orchestration.
- Swap the runtime (local shell, Docker, remote) without changing task logic.
- Swap the memory backend without changing the core.

### No Monolith

Remedy must remain usable as a library inside a larger system. It does not own the process, the event loop, or the configuration system. It provides primitives that a host application composes.

## Provider Model

### Planner Providers

A planner provider is any callable with signature `(prompt: str) -> PlannerOutput`.
The `PlannerOutput` model lives in `packages/orchestration/planner_models.py` — not in the provider — because orchestration imports it and providers depend on it.

```
orchestration/planner_models.py  ←  defines PlannerOutput (no external deps)
          ↑
providers/ollama_planner/        ←  imports PlannerOutput; calls Ollama
providers/claude_planner/        ←  (future) imports PlannerOutput; calls Claude API
```

Orchestration (`plan_job_with_llm`) accepts any planner callable. The provider is injected at the call site (CLI, tests) — orchestration never imports provider packages directly. This makes providers fully swappable and testable via mock callables.

### Builder Providers

A builder provider is any callable with signature `(prompt: str) -> BuilderOutput`.
The `BuilderOutput` model lives in `packages/orchestration/builder_models.py` — same pattern as `PlannerOutput` — so orchestration can import it and providers depend on it.

```
orchestration/builder_models.py  ←  defines BuilderOutput (no external deps)
          ↑
providers/ollama_builder/        ←  imports BuilderOutput; calls Ollama
providers/docker_builder/        ←  (future) imports BuilderOutput; runs in Docker
```

Orchestration (`run_next_task`) accepts any builder callable. The provider is injected at the call site (CLI, tests) — orchestration never imports provider packages directly.

### Role-Specific Model Selection

Remedy uses role-specific model configuration. Each role has its own env var, allowing different models for different responsibilities within the same job.

Current roles:

```
REMEDY_OLLAMA_PLANNER_MODEL  ←  planner role (highest priority)
REMEDY_OLLAMA_BUILDER_MODEL  ←  builder role (highest priority)
REMEDY_OLLAMA_MODEL          ←  generic fallback (any role, backward compat)
built-in default             ←  qwen3-coder-next
```

Generation parameters follow the same pattern per role:
- `REMEDY_OLLAMA_PLANNER_TEMPERATURE` / `REMEDY_OLLAMA_BUILDER_TEMPERATURE`
- `REMEDY_OLLAMA_PLANNER_NUM_PREDICT` / `REMEDY_OLLAMA_BUILDER_NUM_PREDICT`

These are passed to Ollama only when set; unset means the model's defaults apply.
Env var parsing errors name the offending variable in the error message.

### Execution State Semantics

`run_next_task` drives job state as follows:

| Event | Job state | Task state |
|-------|-----------|------------|
| Pending task found, execution begins | `RUNNING` | `RUNNING` |
| Task execution succeeds | `RUNNING` (if more pending) | `COMPLETED` |
| Last task completes | `COMPLETED` | `COMPLETED` |
| No pending task found | unchanged | unchanged |

A partially-executed job (some tasks `COMPLETED`, some `PENDING`) remains `RUNNING`.
`run_next_task` advances one task per call; the CLI loop is the caller's responsibility.

### Step 5 Pre-execution Limitation

The builder callable currently returns structured output (`BuilderOutput`) describing *proposed* changes — it does not modify project files or execute commands. Actual code modification requires a runtime provider (Docker, local shell) and is deferred to a later step.

### Concrete Providers

**`packages/providers/ollama_planner/`** — Planner provider. Calls local Ollama with JSON schema enforcement. Configured via `REMEDY_OLLAMA_PLANNER_MODEL`, `REMEDY_OLLAMA_PLANNER_TEMPERATURE`, `REMEDY_OLLAMA_PLANNER_NUM_PREDICT`. The `ollama` package is an optional dependency; loaded lazily.

**`packages/providers/ollama_builder/`** — Builder provider. Same Ollama pattern for the builder role. Configured via `REMEDY_OLLAMA_BUILDER_MODEL`, `REMEDY_OLLAMA_BUILDER_TEMPERATURE`, `REMEDY_OLLAMA_BUILDER_NUM_PREDICT`. Env var parsing errors name the offending variable.
