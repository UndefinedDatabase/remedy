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

## Step 4 + 4.6: First Real Planner Worker (Ollama-backed) + Role-Specific Configuration

Step 4 introduces the first concrete provider: an Ollama-backed local planner.
Step 4.6 adds role-specific model selection, generation parameters, and richer planning metadata.
Orchestration still owns the workflow — the provider only produces structured data.

- **`packages/orchestration/planner_models.py`** — `PlannerOutput`, `ProposedTask`: structured planner output model (lives in orchestration, not in the provider)
- **`packages/orchestration/llm_planner.py`** — `plan_job_with_llm(job, call_planner)`: orchestration function that accepts any planner callable and drives the PENDING → PLANNED transition; `annotate_planning_result()` enriches the planning artifact with provider/model/timing metadata
- **`packages/providers/ollama_planner/provider.py`** — `OllamaPlanner`: calls local Ollama with JSON schema enforcement; lazy-imports the `ollama` package; supports role-specific model and generation parameter configuration
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
REMEDY_OLLAMA_PLANNER_MODEL=qwen2.5:7b remedy plan-job-local <job_id>
# → Job <id> | role=planner model=qwen2.5:7b tasks=4 elapsed=3201ms

# Inspect the LLM-generated plan
remedy show-job <job_id>
```

### Planner configuration

Remedy uses role-specific environment variables. The current implementation covers the **planner** role only; additional roles (executor, verifier) will have their own variables in future steps.

| Variable | Default | Description |
|----------|---------|-------------|
| `REMEDY_OLLAMA_PLANNER_MODEL` | — | Model for the planner role (takes priority) |
| `REMEDY_OLLAMA_MODEL` | `qwen3-coder-next` | Fallback model (any role) |
| `REMEDY_OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `REMEDY_OLLAMA_PLANNER_TEMPERATURE` | — | Sampling temperature for the planner (e.g. `0.2`) |
| `REMEDY_OLLAMA_PLANNER_NUM_PREDICT` | — | Max tokens to generate for the planner |

Model selection precedence (highest to lowest):
1. `OllamaPlanner(model=...)` constructor argument
2. `REMEDY_OLLAMA_PLANNER_MODEL`
3. `REMEDY_OLLAMA_MODEL`
4. Built-in default (`qwen3-coder-next`)

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

## Step 5 + 5.5: First Local Task Execution Skeleton + Execution Hardening

Step 5 introduces single-task execution via a local Ollama-backed builder worker.
Step 5.5 hardens execution semantics: safer failure handling, richer task context,
cleaner metadata, and planner task_type normalization.

- **`packages/orchestration/builder_models.py`** — `TaskExecutionContext` (richer input context for builders) and `BuilderOutput` (structured result)
- **`packages/orchestration/task_runner.py`** — `run_next_task(job, call_builder)`: builds context, executes, creates a task-owned Artifact, advances state; rolls back on failure; `annotate_task_result()` enriches artifact metadata
- **`packages/providers/ollama_builder/provider.py`** — `OllamaBuilder`: receives `TaskExecutionContext`, builds a rich Ollama prompt; role-specific env vars
- **`apps/cli/main.py`** — `remedy run-next-task-local <job_id>` command

### Run local task execution

```bash
# Create a job and plan it first
remedy create-job "build a CLI tool that summarises files in a directory"
remedy plan-job <job_id>

# Execute the next pending task
remedy run-next-task-local <job_id>
# → Job <id> | task=<task-id> type=analyze_requirements role=builder model=qwen3-coder-next elapsed=1820ms remaining=2

# Call again to advance through remaining tasks
remedy run-next-task-local <job_id>
remedy run-next-task-local <job_id>

# When all tasks are done:
# → Job <id> — no pending tasks.
```

### Builder configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `REMEDY_OLLAMA_BUILDER_MODEL` | — | Model for the builder role (takes priority) |
| `REMEDY_OLLAMA_MODEL` | `qwen3-coder-next` | Fallback model (any role) |
| `REMEDY_OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `REMEDY_OLLAMA_BUILDER_TEMPERATURE` | — | Sampling temperature for the builder |
| `REMEDY_OLLAMA_BUILDER_NUM_PREDICT` | — | Max tokens to generate for the builder |

Numeric env vars (`TEMPERATURE`, `NUM_PREDICT`) emit a clear error message naming
the offending variable if the value is not parseable (e.g. `REMEDY_OLLAMA_BUILDER_TEMPERATURE=foo`).

### Execution state semantics

| Transition | When |
|------------|------|
| `planned` → `running` | First pending task starts executing |
| `running` → `completed` | All tasks have been executed |
| Stays `running` | Some tasks completed, others still pending |
| Unchanged | Builder failure: task rolls back to `pending`, job state restored |

**Important**: `run-next-task-local` advances one task per call. Run it repeatedly to
fully execute a planned job.

**Failure behavior**: if the builder fails (network error, validation error, etc.), the
task is rolled back to `pending` and the job state is restored to its value before the
call. The job can be re-attempted cleanly. Errors are reported in the CLI with a concise
message distinguishing missing-dependency, configuration, invalid-output, and general
execution failures.

### What the builder receives (TaskExecutionContext)

The builder provider receives a structured `TaskExecutionContext` containing:
- The job ID and user prompt
- The task ID, type, and description
- The planning summary (from the `planning_output` artifact, if present)
- Summaries from previously completed tasks (in order)

This gives the builder full context without exposing the mutable `Job` object.

### Artifact metadata conventions (Step 5.5)

After annotation, every task execution artifact contains:

| Key | Source |
|-----|--------|
| `task_type` | Set by `run_next_task` |
| `summary` | Set by `run_next_task` (from BuilderOutput) |
| `provider` | Added by `annotate_task_result` |
| `role` | Added by `annotate_task_result` |
| `model` | Added by `annotate_task_result` |
| `elapsed_ms` | Added by `annotate_task_result` |

The legacy `"builder": "llm"` and `"planner": "llm"` keys have been removed.

### Limitations in Step 5 (pre-Docker)

This step does **not** modify project files, run commands, or apply patches. The builder returns structured output (`BuilderOutput`) describing *proposed* changes. Actual code modification is deferred to a later step involving Docker or a local runtime provider.

## Step 6: First Runtime-Backed Workspace Execution

Step 6 introduces a local workspace runtime that materializes builder output as real files on disk. Each job now gets its own workspace directory under `.data/workspaces/<job_id>/`.

- **`packages/orchestration/workspace.py`** — `Workspace`, `MaterializedFile`, `LocalWorkspaceRuntime`: local filesystem-backed runtime; `write(relative_path, content)` creates dirs and writes UTF-8 files; storage location follows the same `REMEDY_DATA_DIR` resolution as `storage.py`
- **`packages/orchestration/task_runner.py`** — `materialize_task_output(result, runtime)`: writes the builder's proposed changes to `task_output/<task_type>.txt` inside the workspace and records the file path in the artifact metadata
- **`packages/orchestration/planner_models.py`** — `PlannerOutput.proposed_tasks` now requires at least 1 task (`min_length=1`); empty task lists are rejected at validation time
- **`apps/cli/main.py`** — `run-next-task-local` now creates a workspace, materializes the task output, and prints the file path

### What materialization means

After each task executes, the builder's `proposed_changes` and `summary` are written to a text file in the workspace. This is the first time builder output becomes a physical file on disk — not just a JSON artifact in the job file.

The workspace file path is also recorded in the artifact's metadata (`workspace_file` key) so it can be found without re-deriving the path.

```bash
# Execute a task and materialize its output
remedy run-next-task-local <job_id>
# → Job <id> | task=<task-id> type=write_code role=builder model=... elapsed=1820ms remaining=2 file=/path/to/.data/workspaces/<job_id>/task_output/write_code.txt
```

### Workspace storage

By default, workspaces are stored at `<repo_root>/.data/workspaces/<job_id>/`.
The same `REMEDY_DATA_DIR` env var controls the base location:

```bash
REMEDY_DATA_DIR=/tmp/remedy remedy run-next-task-local <job_id>
# → workspace at /tmp/remedy/workspaces/<job_id>/
```

## What Is NOT Implemented Yet

- Code/file modification via patches or diffs (builder output is structured prose, not patches)
- Agent loops (auto-advance through all tasks)
- Provider implementations (Claude, MemPalace)
- Docker or sandboxed runtime execution
- Configuration system
- API and worker apps

## Structure

```
apps/           # Runnable applications (api, worker, cli)
packages/
  core/         # Domain models
  contracts/    # Protocol interfaces
  orchestration/# job_runner, task_runner, storage, builder_models, planner_models, workspace
  memory/       # (future) memory management
  runtimes/     # (future) runtime abstractions
  verification/ # (future) artifact verification
  artifacts/    # (future) artifact management
  providers/    # External system adapters; ollama_builder, ollama_planner (in PR)
prompts/        # Prompt templates
tests/          # Test suite
docs/           # Architecture and long-term documentation
.agent/         # Agent working state (plan, context, decisions)
```
