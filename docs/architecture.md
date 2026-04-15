# Remedy Architecture

## What Remedy Is

Remedy is a modular orchestration kernel. It coordinates tasks, manages artifacts, and enforces acceptance criteria. It does not implement intelligence itself — it delegates to providers.

## Core Principles

### Strict Core / Provider Separation

The `packages/core` and `packages/contracts` packages have **no external dependencies**. They define models and interfaces only. All integrations (LLMs, runtimes, memory systems) live in `packages/providers/` and are wired in at the application layer.

```
core/contracts  ←  no deps, no providers
       ↑
orchestration   ←  depends on contracts only
       ↑
providers       ←  implement contracts, depend on external systems
       ↑
apps            ←  wire everything together
```

### Artifact-Driven Workflow

Work is expressed as `Job → Task → Artifact`, not as prompt strings. Artifacts are explicit, versioned, typed outputs. Workflows are not driven by raw prompts.

### Memory Gateway

All memory access goes through the `MemoryGateway` interface. No component reaches into a memory system directly. This makes the memory backend replaceable without touching orchestration logic.

### Composability

Every layer is replaceable:
- Swap the LLM provider without changing orchestration.
- Swap the runtime (local shell, Docker, remote) without changing task logic.
- Swap the memory backend without changing the core.

### No Monolith

Remedy must remain usable as a library inside a larger system. It does not own the process, the event loop, or the configuration system. It provides primitives that a host application composes.
