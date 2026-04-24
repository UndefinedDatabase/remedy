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

A builder provider is any callable with signature `(context: TaskExecutionContext) -> BuilderOutput`.
Both `TaskExecutionContext` and `BuilderOutput` live in `packages/orchestration/builder_models.py`
so providers depend on orchestration, not the reverse.

```
orchestration/builder_models.py  ←  defines TaskExecutionContext + BuilderOutput (no external deps)
          ↑
providers/ollama_builder/        ←  imports both; calls Ollama
providers/docker_builder/        ←  (future) imports both; runs in Docker
```

Orchestration (`run_next_task`) builds a `TaskExecutionContext` from the current job and
task state, then passes it to the injected callable. The provider receives all context it
needs and must not mutate the Job.

### Task Execution Context

`TaskExecutionContext` is the structured input every builder provider receives:

| Field | Description |
|-------|-------------|
| `job_id` | UUID of the job |
| `job_prompt` | User prompt from the job (may be None) |
| `task_id` | UUID of the task to execute |
| `task_type` | snake_case type identifier |
| `task_description` | Human-readable task description |
| `planning_summary` | Summary from the `planning_output` artifact, if present |
| `prior_task_summaries` | Summaries from already-completed task artifacts, in order |

This gives the provider the full execution context without exposing the mutable `Job` object.

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

### Execution State Semantics (Step 7 — verifier gate)

`run_next_task` sets the task to `RUNNING` and produces an artifact, but does **not**
mark the task `COMPLETED`. Task completion requires the full verification sequence:

| Event | Job state | Task state |
|-------|-----------|------------|
| Pending task found, execution begins | `RUNNING` | `RUNNING` |
| Builder succeeds (artifact created) | `RUNNING` | `RUNNING` (stays) |
| `verify_task_output` passes, `finalize_task` called | `RUNNING` (if pending remain) | `COMPLETED` |
| `finalize_task` on last task | `COMPLETED` | `COMPLETED` |
| No pending task found | unchanged | unchanged |
| Builder fails | restored to pre-call value | `PENDING` (rolled back) |
| Verification fails, `finalize_task` called | `RUNNING` | `PENDING` (rolled back) |

A partially-executed job (some tasks `COMPLETED`, some `PENDING`) remains `RUNNING`.
Verification failure records diagnostic metadata in the artifact and rolls the task
back to `PENDING` — retryable by re-running the command.

**Failure rollback**: builder exceptions roll back task to `PENDING` and restore `job.state`.
Verification failures do the same via `finalize_task` — no exception raised, no stranded state.

### Artifact Metadata Conventions

Task execution artifacts carry consistent metadata keys:

| Key | Added by |
|-----|----------|
| `task_type` | `run_next_task` |
| `summary` | `run_next_task` (from `BuilderOutput.summary`) |
| `provider` | `annotate_task_result` |
| `role` | `annotate_task_result` |
| `model` | `annotate_task_result` |
| `elapsed_ms` | `annotate_task_result` |
| `workspace_file` | `materialize_task_output` (absolute path of the materialized file; deterministic, collision-safe name) |
| `verification_passed` | `finalize_task` — present only on verification failure; value `False` |
| `verification_failures` | `finalize_task` — list of `"check: message"` strings on failure |

Planning artifacts carry: `summary`, `provider`, `role`, `model`, `task_count`, `elapsed_ms`.
Legacy ambiguous keys (`"builder": "llm"`, `"planner": "llm"`) are not used.

### Task Type Normalization

If a planner returns duplicate `task_type` values (e.g. two tasks both typed
`"write_tests"`), `plan_job_with_llm` deduplicates them by appending `_2`, `_3`, etc.
to subsequent occurrences. This prevents downstream execution from confusing two
semantically different tasks with the same identifier.

### Workspace Runtime

`packages/orchestration/workspace.py` provides the `LocalWorkspaceRuntime`, which is the first concrete runtime implementation.

Each job gets a dedicated directory: `<workspace_root>/<job_id>/`. The workspace root defaults to `<repo_root>/.data/workspaces/` and follows the same `REMEDY_DATA_DIR` resolution logic as `storage.py`.

The runtime is **injected** into orchestration functions — it is never imported directly by providers. This allows future runtime implementations (Docker sandbox, remote) to be swapped in without changing orchestration logic.

```
orchestration/workspace.py  ←  Workspace, MaterializedFile, LocalWorkspaceRuntime
         ↑
orchestration/task_runner.py  ←  materialize_task_output(result, runtime)
         ↑
apps/cli/main.py  ←  creates runtime, calls materialize_task_output
```

`materialize_task_output(result, runtime)` writes the builder's proposed changes to a task-specific file inside the workspace and records the absolute path in the artifact's `workspace_file` metadata key. It is a no-op when `result.changed` is False.

### Workspace File Naming (Step 6.5)

Materialized files are placed at `task_output/<index>_<safe_type>_<short_id>.txt` inside the job's workspace directory:

- `<index>` — 0-based position of the task in `job.tasks`, zero-padded to 3 digits. Makes filenames ordered and collision-safe across tasks.
- `<safe_type>` — `task_type` sanitized via `_sanitize_path_component`: non-`[a-zA-Z0-9_-]` characters replaced with `_`, truncated to 48 characters, leading/trailing underscores stripped. Falls back to `"unknown"` if empty after sanitization.
- `<short_id>` — first 8 hex characters of the task UUID. Guarantees uniqueness even if two tasks share the same type and index (e.g. after a refactor).

Properties:
- **Collision-safe**: index + UUID fragment make every file unique even with duplicate `task_type` values.
- **Deterministic**: same task always produces the same filename.
- **Path-safe**: sanitization prevents traversal sequences, spaces, and other unsafe characters from flowing into file paths.

### Materialization Content (Step 6.5)

Only the **Proposed Changes** section of the builder artifact content is written to the workspace file. Notes and Risks sections are excluded. `_extract_proposed_changes` uses a simple section-aware state machine keyed on the known section headers (`"Proposed Changes:"`, `"Notes:"`, `"Risks:"`).

### Materialization and Verification Ordering (Step 7)

The conservative ordering used by the CLI:

1. `annotate_task_result` — enriches artifact metadata in memory only
2. `materialize_task_output` — writes workspace file; adds `workspace_file` path to artifact metadata in memory
3. `verify_task_output` — pure check; reads artifact and workspace file; returns `VerificationResult` without mutating state
4. `finalize_task` — applies the result: `COMPLETED` on pass, `PENDING` + metadata on failure
5. `save_job` — persists the authoritative post-verification job state

`verify_task_output` is pure — it does not mutate the job. `finalize_task` is the only
function that transitions a task from `RUNNING` to `COMPLETED` or `PENDING`. Saving
after finalization ensures the persisted state is always authoritative.

### Task Contract v1 and Verifier Gate

`packages/orchestration/verifier.py` defines the first explicit task contract.

**`TaskContract`** — a minimal Pydantic model capturing which checks are required:
- `require_artifact`: task must produce an artifact with a matching task_id
- `require_workspace_file`: artifact must record a valid, non-empty workspace file
- `require_proposed_changes`: workspace file must contain at least one `  - ` line

All fields default to `True`. Step 7 always runs all checks. The model reserves space
for per-task contract customization in a future step.

**`verify_task_output(job, task_id)`** — 7 deterministic checks, all local-only:

| Check | What it verifies |
|-------|-----------------|
| `has_output_artifact` | `task.output_artifact_ids` is non-empty |
| `artifact_exists` | the first artifact ID resolves in `job.artifacts` |
| `artifact_task_id_matches` | `artifact.task_id == task.id` |
| `workspace_file_in_metadata` | `"workspace_file"` key present in artifact metadata |
| `workspace_file_exists` | the recorded path exists on disk |
| `workspace_file_not_empty` | file size > 0 bytes |
| `has_proposed_change` | at least one line starting with `"  - "` in the file |

Early return: if a check fails in a way that makes the next check meaningless (e.g.
artifact is None), the function returns immediately with the accumulated failures rather
than raising. All checks that ran are always included in the `VerificationResult.checks`
list.

### Planner Output Validation

`PlannerOutput.proposed_tasks` requires at least one entry (`Field(min_length=1)`). A plan with zero tasks is invalid and rejected at the model boundary before reaching orchestration.

### Concrete Providers

**`packages/providers/ollama_planner/`** — Planner provider. Calls local Ollama with JSON schema enforcement. Configured via `REMEDY_OLLAMA_PLANNER_MODEL`, `REMEDY_OLLAMA_PLANNER_TEMPERATURE`, `REMEDY_OLLAMA_PLANNER_NUM_PREDICT`. The `ollama` package is an optional dependency; loaded lazily.

**`packages/providers/ollama_builder/`** — Builder provider. Same Ollama pattern for the builder role. Configured via `REMEDY_OLLAMA_BUILDER_MODEL`, `REMEDY_OLLAMA_BUILDER_TEMPERATURE`, `REMEDY_OLLAMA_BUILDER_NUM_PREDICT`. Env var parsing errors name the offending variable.
