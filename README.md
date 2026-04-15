# Remedy

Remedy is a modular orchestration kernel for artifact-driven workflows.

## What It Is

Remedy coordinates tasks, tracks artifacts, and enforces acceptance criteria. External systems (LLMs, runtimes, memory backends) plug in as providers via well-defined interfaces. The core has no external dependencies.

## Step 1 + 1.5: Foundation

Step 1 established the project structure and core contracts. Step 1.5 hardened them. Together they include:

- **`packages/core/models.py`** — Pydantic domain models: `Budget`, `AcceptanceCheck`, `RunState`, `Artifact` (with task provenance), `Task` (with lifecycle state and output artifact linkage), `Job`
- **`packages/contracts/interfaces.py`** — Protocol interfaces: `LLMWorker` (task-oriented, not prompt-centric), `MemoryGateway`, `RuntimeProvider`, `Verifier` (typed with `AcceptanceCheck`)
- **`tests/test_imports.py`** — Smoke tests verifying clean imports, model defaults, and provenance fields
- **`docs/architecture.md`** — Architecture definition, package role boundaries, and module-usability guarantee
- Full directory skeleton for all planned modules and apps

## Step 2: Packaging + CLI

Step 2 makes Remedy a real installable Python project:

- **`pyproject.toml`** — hatchling build, `pydantic` dependency, `remedy` console script, pytest configured with `pythonpath = ["."]`
- **`packages/orchestration/storage.py`** — `save_job` / `load_job` backed by JSON files under `.data/jobs/`
- **`apps/cli/main.py`** — `remedy create-job "<prompt>"` command

### Install

```bash
pip install -e ".[dev]"
```

### Run CLI

```bash
remedy create-job "summarise the repo"
# prints the new job UUID, e.g.:
# 3f2a1b4c-...
```

### Run Tests

```bash
pytest
```

## What Is NOT Implemented Yet

- Orchestration logic
- Agent loops
- Provider implementations (Claude, Docker, MemPalace)
- Configuration system
- API and worker apps

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
