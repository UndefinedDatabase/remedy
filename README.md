# Remedy

Remedy is a modular orchestration kernel for artifact-driven workflows.

## What It Is

Remedy coordinates tasks, tracks artifacts, and enforces acceptance criteria. External systems (LLMs, runtimes, memory backends) plug in as providers via well-defined interfaces. The core has no external dependencies.

## Step 1: Foundation Skeleton

This step establishes the project structure and core contracts. It includes:

- **`packages/core/models.py`** — Pydantic domain models: `Budget`, `AcceptanceCheck`, `Artifact`, `Task`, `RunState`, `Job`
- **`packages/contracts/interfaces.py`** — Protocol interfaces: `LLMWorker`, `MemoryGateway`, `RuntimeProvider`, `Verifier`
- **`tests/test_imports.py`** — Smoke tests verifying clean imports and basic instantiation
- **`docs/architecture.md`** — Architecture definition and principles
- Full directory skeleton for all planned modules and apps

## What Is NOT Implemented Yet

- Orchestration logic
- Agent loops
- Provider implementations (Claude, Docker, MemPalace)
- Build tooling, packaging, or dependency management
- Configuration system
- API, worker, or CLI apps

## Structure

```
apps/           # Runnable applications (api, worker, cli)
packages/
  core/         # Domain models
  contracts/    # Protocol interfaces
  orchestration/# (future) orchestration kernel
  memory/       # (future) memory management
  runtimes/     # (future) runtime abstractions
  verification/ # (future) artifact verification
  artifacts/    # (future) artifact management
  providers/    # External system adapters (claude_agent, docker_runtime, mempalace)
prompts/        # Prompt templates
tests/          # Test suite
docs/           # Architecture and long-term documentation
.agent/         # Agent working state (plan, context, decisions)
```
