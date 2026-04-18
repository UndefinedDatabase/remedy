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

## Step 2 + 2.5: Packaging + CLI + Storage Hardening

Step 2 makes Remedy a real installable Python project. Step 2.5 hardens the local persistence layer and expands the CLI.

- **`pyproject.toml`** — hatchling build, `pydantic` dependency, `remedy` console script, pytest configured with `pythonpath = ["."]`
- **`packages/orchestration/storage.py`** — `save_job` / `load_job` / `list_jobs`; `JobNotFoundError`; storage directory resolved via `REMEDY_DATA_DIR` env var or `<repo_root>/.data/jobs`
- **`apps/cli/main.py`** — `create-job`, `list-jobs`, `show-job`, `plan-job` commands

## Step 3: First Orchestration Skeleton

Step 3 introduces the first local, deterministic job-processing step.
"Planning" here means shaping the job into structured work — no LLM is involved.

- **`packages/orchestration/job_runner.py`** — `plan_job(job)`: adds 3 standard planning Tasks and 1 `planning_output` Artifact; idempotent

### What "planning" means at this stage

When you run `remedy plan-job <id>`, Remedy:
1. Loads the job from disk
2. Adds 3 fixed Tasks: `analyze_requirements`, `define_acceptance_checks`, `prepare_implementation_plan`
3. Attaches a `planning_output` Artifact describing the generated plan
4. Persists the updated job

This is deterministic scaffolding — the same 3 tasks are added for every job.
LLM-driven planning is deferred to a later step.

After planning, the job state changes from `pending` → `planned`.
A job in the `planned` state has tasks ready but execution has not started.
The `planning_output` artifact has `task_id = null` because it is produced
by orchestration logic, not by a specific Task.

## Step 4: First Real Planner Worker (Ollama-backed)

Step 4 introduces the first concrete provider: an Ollama-backed local planner.
Orchestration still owns the workflow — the provider only produces structured data.

- **`packages/orchestration/planner_models.py`** — `PlannerOutput`, `ProposedTask`: structured planner output model (lives in orchestration, not in the provider)
- **`packages/orchestration/llm_planner.py`** — `plan_job_with_llm(job, call_planner)`: orchestration function that accepts any planner callable and drives the PENDING → PLANNED transition
- **`packages/providers/ollama_planner/provider.py`** — `OllamaPlanner`: calls local Ollama with JSON schema enforcement; lazy-imports the `ollama` package
- **`apps/cli/main.py`** — `remedy plan-job-local <job_id>` command

### Install with Ollama support

```bash
pip install -e ".[dev,ollama]"
```

### Run local LLM planning

Make sure Ollama is running locally with your chosen model, then:

```bash
# Create a job
remedy create-job "build a CLI tool that summarises files in a directory"

# Plan it using the local model
REMEDY_OLLAMA_MODEL=qwen2.5:7b remedy plan-job-local <job_id>
# → Job <id> planned via Ollama: 4 task(s), 1 artifact(s)

# Inspect the LLM-generated plan
remedy show-job <job_id>
```

Configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `REMEDY_OLLAMA_MODEL` | `qwen3-coder-next` | Ollama model to use |
| `REMEDY_OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |

### Adding a second planner (e.g. Claude)

To add Claude as a planner provider:
1. Create `packages/providers/claude_planner/provider.py` with a `ClaudePlanner` class
2. Implement `ClaudePlanner.plan(prompt: str) -> PlannerOutput`
3. Wire it in the CLI as `plan-job-claude`

The orchestration logic (`plan_job_with_llm`) is provider-agnostic — it accepts any callable returning `PlannerOutput`.

### Install

```bash
pip install -e ".[dev]"
```

### CLI Usage

```bash
# Create a job (prints UUID)
remedy create-job "summarise the repo"
# → 3f2a1b4c-8d6e-4f9a-b1c2-...

# List all jobs (newest first)
remedy list-jobs
# → 3f2a1b4c-...  pending       2026-04-15T19:37:36+00:00  summarise the repo

# Inspect a job as JSON
remedy show-job 3f2a1b4c-8d6e-4f9a-b1c2-...

# Plan a job (adds tasks and artifact)
remedy plan-job 3f2a1b4c-8d6e-4f9a-b1c2-...
# → Job 3f2a1b4c-... planned: 3 task(s), 1 artifact(s)

# Running plan-job again is safe (idempotent)
remedy plan-job 3f2a1b4c-8d6e-4f9a-b1c2-...
# → Job 3f2a1b4c-... already planned — no changes made.
```

### Storage Location

By default, jobs are stored at `<repo_root>/.data/jobs/`.
Override with the `REMEDY_DATA_DIR` environment variable:

```bash
REMEDY_DATA_DIR=/tmp/my-jobs remedy create-job "test"
```

### Run Tests

```bash
pytest
```

## What Is NOT Implemented Yet

- Task execution
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
  orchestration/# job_runner (plan_job), storage
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
