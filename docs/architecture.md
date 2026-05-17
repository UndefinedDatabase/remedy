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
| `repo_applied_files` | CLI — list of absolute path strings; present only when ≥1 file was written to the attached repo |

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

**`verify_task_output(job, task_id)`** — deterministic checks, all local-only:

Artifact structural checks (when `require_artifact=True`):

| Check | What it verifies |
|-------|-----------------|
| `has_output_artifact` | `task.output_artifact_ids` is non-empty |
| `artifact_exists` | the first artifact ID resolves in `job.artifacts` |
| `artifact_task_id_matches` | `artifact.task_id == task.id` |

Profile checks (run after artifact confirmed valid; see Verifier Profiles section):

| Check | What it verifies |
|-------|-----------------|
| `required_section:<section>` | section header present in `artifact.content` |
| `min_proposed_changes` | proposed-change line count meets profile threshold |
| `forbidden_phrase:<phrase>` | phrase absent from `artifact.content` (case-insensitive) |

Workspace-file structural checks (when `require_workspace_file=True`):

| Check | What it verifies |
|-------|-----------------|
| `workspace_file_in_metadata` | `"workspace_file"` key present in artifact metadata |
| `workspace_file_exists` | the recorded path exists on disk |
| `workspace_file_not_empty` | file size > 0 bytes |
| `has_proposed_change` | at least one line starting with `"  - "` in the file |

Early return: if a check fails in a way that makes the next check meaningless (e.g.
artifact is None), the function returns immediately with the accumulated failures rather
than raising. All checks that ran are always included in the `VerificationResult.checks`
list.

### Target Repository Attachment (Step 8)

Remedy separates its **workspace** (Remedy-owned execution boundary) from the **target
repository** (user-owned project tree):

```
workspace  →  .data/workspaces/<job_id>/   (Remedy writes; always)
target repo →  user-supplied directory       (Remedy writes selectively; only when attached)
```

**Attaching a repo** stores the resolved absolute path in `job.metadata["target_repo"]`:

```bash
remedy attach-repo <job_id> /path/to/my-repo
```

No files are written during attachment — only the path is recorded. The path is validated
at attach time (must exist and be a directory) and resolved to an absolute path.

**Safe repo application** (`packages/orchestration/repo_applicator.py`) bridges the
workspace and the target repo for eligible task output. Rules:

1. **Registry routing only** — `task_type` is matched via `task_registry.get_task_type_spec()`
   (no LLM paths accepted). Ineligible task types produce no repo write.
2. **No overwriting** — if the target file already exists, the write is skipped silently.
3. **No source code** — only markdown files under `docs/` or `README.md` are ever written.
4. **No Git, no shell, no patch application** — writes use `Path.write_text()` only.
5. **Boundary-safe** — `_write_to_repo` resolves the target path and verifies it remains
   inside `repo_root` before writing. Boundary violations raise `RuntimeError`.

Current mapping:

| task_type keyword | repo-relative path |
|-------------------|--------------------|
| `readme` | `README.md` |
| `changelog`, `architecture`, `design`, `guide`, `documentation`, `doc` | `docs/<safe_type>.md` |
| `plan`, `spec`, `requirement`, `acceptance`, `analysis` | `docs/remedy/<safe_type>.md` |

Rules are ordered: `docs/remedy/` keywords appear before `doc`/`documentation` so that
compound task types like `spec_document` or `planning_document` match the specific
`docs/remedy/` rule rather than the broader `doc` catch-all.

`<safe_type>` is the task_type sanitized via the same `_sanitize_path_component` logic as
the workspace (non-`[a-zA-Z0-9_-]` replaced with `_`, truncated to 48 chars).

Repo application runs only when:
- `vr.passed` (verification passed) — no repo writes on failed verification
- `job.metadata["target_repo"]` is set — no repo writes without attachment
- `repo_generated_write` permission is granted (see Step 9 below)
- The task type matches a keyword — no repo writes for ineligible types
- The target file does not already exist — no overwriting

If no repo is attached or the task type is ineligible, the flow continues workspace-only
without any error or warning.

**Artifact metadata keys added by Step 8:**

| Key | Added by |
|-----|----------|
| `repo_applied_files` | CLI (`run-next-task-local`), only when at least one repo file was written; list of absolute path strings |
| `repo_application_skipped_reason` | `check_and_apply_to_repo` — present only when repo write was skipped due to `"permission_denied"` |

**Failed-artifact retention**: on verification failure, `finalize_task` clears
`task.output_artifact_ids` (so the next retry uses a fresh artifact) but retains the
failed artifact in `job.artifacts` for diagnostics. The artifact is detached from the
task but preserved in the job — accessible by iterating `job.artifacts`.

### Permission Model v1 (Steps 9 and 9.5)

`packages/orchestration/permissions.py` defines the first explicit permission boundary.

**`Capability`** — a `str` enum listing all execution capabilities that Remedy may exercise:

| Capability | Default | Status | Meaning |
|-----------|---------|--------|---------|
| `workspace_write` | allow | **active** | Write files into the Remedy-owned workspace |
| `repo_generated_write` | deny | **active** | Write generated markdown into the user's target repo |
| `repo_overwrite` | deny | reserved | Overwrite existing files in the target repo |
| `shell_exec` | deny | reserved | Execute shell commands |

**Active** capabilities are enforced at runtime. **Reserved** capabilities are configurable
and persisted, but no code path consults them during execution. Setting a reserved capability
has no operational effect in this version; the CLI prints a notice when this happens.

**`is_allowed(job, capability)`** — pure check; reads from `job.metadata["permissions"]`
falling back to conservative defaults. Only the string `"allow"` grants permission.

**`is_reserved(capability)`** — returns `True` for capabilities that are defined but not yet
enforced at runtime (`repo_overwrite`, `shell_exec`).

**`effective_permissions(job)`** — returns a list of `{capability, effective, status}` dicts
for all capabilities; used by `show-permissions`.

**`set_permission(job, capability, *, allow)`** — mutates `job.metadata["permissions"]`.
Callers must persist the job afterwards.

**`check_and_apply_to_repo(job, artifact, repo_root)`** in `repo_applicator.py` — the
permission-gated entry point for repo application:
1. Checks `repo_generated_write` via `is_allowed`.
2. If denied: records `repo_application_skipped_reason="permission_denied"` on artifact; returns `[]`.
3. If allowed: delegates to `apply_task_output_to_repo` (all existing rules apply).

**`workspace_write` enforcement (Step 9.6):** `run-next-task-local` checks
`workspace_write` **before** instantiating the builder or calling `run_next_task`. If
denied, the CLI prints a clear error to stderr and exits non-zero immediately — no LLM
call is made, no task state is mutated, no artifacts are created. Materialization is
unconditional after the guard passes (the check cannot be reached again).

Permissions are stored in `job.metadata["permissions"]` as `{"capability": "allow"|"deny"}`.
Missing keys fall back to `_DEFAULTS`. Explicit `"deny"` overrides a default allow.

**`show-permissions` CLI command (Steps 9.5/9.6):** `remedy show-permissions <job_id>`
displays all capabilities, their effective allow/deny state, and a status label. Every
capability is labeled `[active]` (enforced at runtime) or `[reserved]` (configurable but
not yet enforced). The symmetric labeling makes capability status unambiguous at a glance.

**Design principles:**
- Default safe: no capability is allowed unless explicitly granted (except `workspace_write`).
- No interactive prompts: permissions are set once via CLI and persisted.
- Honest: reserved capabilities are labeled as such in the CLI and source code; no silent
  no-ops without user-visible notice.
- Task completion is always determined by the verifier — never by repo application.

### Run Logs v1 (Step 16)

`packages/orchestration/run_log.py` introduces an append-only JSONL event trail
for every meaningful Remedy operation.

**File location:**

```
<REMEDY_DATA_DIR>/runs/<job_id>/<run_id>.jsonl
```

One file per CLI invocation (`run_id` is a UUID4 hex string generated at startup).
The directory follows the same `REMEDY_DATA_DIR` resolution order as `storage.py`
and `workspace.py`: env var first, then `<repo_root>/.data/runs/`.

**Format:** one compact JSON object per line (no trailing comma, no wrapping array).
Files are append-only — no event is ever modified or deleted.

**Event model (`RunEvent`):**

| Field | Type | Description |
|-------|------|-------------|
| `event` | str | Event name (e.g. `"builder_started"`) |
| `job_id` | str | UUID of the job |
| `run_id` | str | UUID4 hex shared by all events in one CLI invocation |
| `timestamp` | str | UTC ISO 8601 timestamp |
| `task_id` | str \| None | UUID of the task, if applicable |
| `artifact_id` | str \| None | UUID of the relevant artifact, if applicable |
| `provider` | str \| None | e.g. `"ollama"` |
| `role` | str \| None | e.g. `"planner"`, `"builder"` |
| `model` | str \| None | model identifier |
| `outcome` | str \| None | e.g. `"pass"`, `"fail"`, `"noop"`, `"changed"` |
| `message` | str \| None | short human-readable context, if useful |
| `metadata` | dict | extra structured data (task_type, counts, risk levels, etc.) |

None-valued top-level fields are omitted from the serialized line. `metadata` is always included (may be `{}`).

**Events logged per CLI command:**

`plan-job-local`:
- `planning_started` — before the LLM call; includes provider/role/model
- `planning_completed` — after success; outcome = `"changed"` or `"noop"`; metadata includes task_count, artifact_id, elapsed_ms
- `planning_failed` — on exception; outcome = `"error"`; `message` = `"planning failed"` (fixed,
  redaction-safe); `metadata.error_category` = exception type name; raw exception strings are
  never logged

`run-next-task-local`:
- `task_run_noop` — before any builder call, when no pending tasks exist;
  outcome = `"no_pending_tasks"` *(pre-execution noop; no `task_run_started` is emitted)*
- `task_run_started` — logged before builder call; metadata includes task_type
- `builder_started` — after builder instantiation, before LLM call; includes provider/role/model
- `builder_completed` — after builder returns; includes artifact_id, elapsed_ms
- `workspace_materialized` — after workspace file written; metadata includes workspace_file path
- `verification_passed` — after verifier passes; metadata includes verifier_profile
- `verification_failed` — after verifier fails; metadata includes failure_count, failed_checks list
- `repo_application_completed` — when repo write succeeds; metadata includes file_count, files
- `repo_application_skipped` — when repo write skipped (e.g. permission denied); metadata includes reason
- `patch_intent_created` — after patch intents materialized; metadata includes intent_count, risk_levels
- `patch_intent_skipped` — when no intents derived for this task type
- `patch_intent_failed` — when patch intent verification errors occur; metadata includes error_count
- `task_run_completed` — terminal event on success; outcome = `"pass"`
- `task_run_failed` — terminal event on failure; outcome values:
  - `"fail"` — verification failure
  - `"permission_denied"` — workspace_write not granted; metadata includes `capability`
  - `"missing_dependency"` / `"invalid_builder_output"` / `"configuration_error"` / `"builder_error"` — builder exceptions
  - metadata includes `error_category` (exception type name); raw exception strings are never logged
- `task_run_noop` — terminal event when builder returns no change; outcome = `"no_change"`;
  metadata includes `reason = "builder_returned_no_change"`

**Terminal-event invariant (v1):**

Every `task_run_started` must be followed by exactly one terminal task event in the same log:

- `task_run_completed` — successful path
- `task_run_failed` — any failure or permission denial
- `task_run_noop` (outcome=`"no_change"`) — builder returned no change

A cockpit reading run logs MUST treat a log file that contains `task_run_started` but no terminal
event as an interrupted or crashed run (e.g. power loss, SIGKILL). The pre-execution noop
(`task_run_noop/no_pending_tasks`) is emitted *before* `task_run_started` and is not a terminal
event; it stands alone.

`create-job`:
- `job_created` — after job is saved; outcome = `"created"`

**Redaction policy (v1):**

Logged: IDs, event names, provider/model/role, task_type, artifact kind, file paths
already visible in CLI output, counts, booleans, outcomes, elapsed_ms, risk levels,
verifier profile name, verification failure check names and messages.

**Not logged:** full artifact content, full prompts, full workspace file contents,
full diff previews, raw exception messages or tracebacks. These are stored in job
artifacts and workspace files; the run log contains only the structural and
observability-relevant fields. Failure events record `error_category` (exception
type name) — never `str(exc)`. The Timeline renderer follows the same rule.

**Public API:**

```python
RunLogWriter(job_id, run_id=None, *, runs_root=None)
  .path    → Path   # absolute JSONL path
  .run_id  → str
  .log(event, *, task_id=None, ..., **metadata)   # convenience method
  .append(RunEvent)                               # lower-level

read_run_events(path)  → list[dict]  # for tests and diagnostics
new_run_id()           → str
```

**CLI output:** `log=<path>` is appended to the output line of `plan-job-local` and
`run-next-task-local` (all outcomes including noop) so the operator can always locate
the log for a specific invocation.

**Design principles:**
- Append-only: events are never mutated; each invocation adds a new file under the
  same `<job_id>/` directory, preserving full history across retries.
- Local-only: no external telemetry, no network calls, no database.
- Non-blocking: log writes use standard `open("a")` and are not transactional.
  In v1, if a log write raises unexpectedly the exception surfaces normally.
- Foundation for future features: cockpit/timeline UX, session resume after
  terminal loss, autonomy/approval modes, MemPalace memory integration.

### Timeline v1 (Step 17)

`packages/orchestration/timeline.py` provides the first user-facing cockpit layer
over run-log events: `remedy timeline <job_id>`.

**Public API:**

```python
load_run_events(data_dir: Path, job_id: UUID | str) -> list[dict]
    # Reads all *.jsonl under <data_dir>/runs/<job_id>/; sorted by timestamp.
    # Returns [] if directory is missing. Ignores empty/malformed lines.

summarize_timeline(job: Job, events: list[dict]) -> str
    # Returns a human-readable multiline terminal string.
```

**Output sections:** header (job id, state, task counts) → Events → Current status →
Next suggested action.

**planning_failed rendering rule:** `summarize_timeline` uses `metadata.error_category` as the
diagnostic detail. If `error_category` is absent (e.g. events from older log files), it renders
`"unknown error"`. It never renders `event.message` — that field may contain raw exception strings
from older log formats and must be treated as opaque.

**task_run_noop outcomes:**
- `no_pending_tasks` — emitted *before* `task_run_started`; builder was not called
- `no_change` with `reason="builder_returned_no_change"` — emitted *after* `task_run_started`;
  builder ran and returned changed=False. Timeline renders these two outcomes with distinct text
  so a cockpit can distinguish "nothing queued" from "ran but produced nothing".

**Event rendering:** each event type is rendered with a symbol prefix (`✓` success,
`✕` failure, `!` warning, `○` noop/info). Task events are grouped into compact
blocks (task_run_started → terminal) showing type, outcome, verification, workspace
path, repo path, patch intent count and risk levels. Unknown events render as
`○ <event-name>` rather than crashing.

`project_constitution_loaded` is a first-class event: rendered as
`✓ Project Constitution loaded  sources=N  tests=yes/no  warnings=N` (the
`warnings=N` field is omitted when `warning_count` is zero).

**Next suggested action (deterministic, no LLM):**
1. Last terminal is `task_run_failed/permission_denied` → suggest `set-permission`.
2. `patch_intent_created` with medium/high/unknown risk → suggest review.
3. Pending tasks remain → suggest `run-next-task-local`.
4. No pending tasks → suggest inspect or `create-job`.

**Design principles:**
- Read-only: never mutates job state or run logs.
- No external dependencies: plain text, no rich/textual/click.
- Degrades gracefully: missing logs, unknown events, and interrupted task blocks
  all render without raising exceptions.
- Foundation for a future TUI/web cockpit — the same run-log contract is consumed
  by any future UI layer.

### Cockpit v1 (Step 18)

`packages/orchestration/cockpit.py` provides a decision-oriented overview of a job:
`remedy cockpit <job_id>`.

**Timeline vs Cockpit:**
- Timeline answers: *"what happened?"* — chronological audit trail of events.
- Cockpit answers: *"where are we, what matters, what needs the user, what can continue
  automatically, and what should I do next?"* — decision surface, not event history.

**Public API:**

```python
summarize_cockpit(job: Job, events: list[dict], *, data_dir: Path | None = None) -> str
    # Returns a decision-oriented cockpit string.
    # data_dir is REMEDY_DATA_DIR; when provided, the run-log dir path appears
    # in the Important artifacts section.
```

**Output sections:**
1. **Header** — job id (8 chars), name, state, task progress.
2. **Situation** — last run outcome, patch intent risk, permission status
   (workspace_write and repo_generated_write), pending task count.
3. **Needs your attention** — actionable items requiring human review:
   interrupted runs, workspace_write denied with pending tasks, patch risk
   (medium/high/unknown), verification failures, repo_generated_write *explicitly*
   denied when patch/repo output exists.
4. **Can continue automatically** — yes/no with a one-line reason.
5. **Important artifacts** — workspace file path, repo file path, patch intent
   count + risk, run log directory (when data_dir provided).
6. **Next best action** — single deterministic suggested CLI command.

**Permission attention rule:** The repo_generated_write attention item only fires when
the permission has been *explicitly* denied (`set_permission(job, ..., allow=False)`).
It does not fire when the permission is at its default (False/opt-in), since the
absence of an explicit grant is the expected initial state.

**Interrupted run auto-continue safety:** When an interrupted run is detected (a
`task_run_started` with no terminal event), `Can continue automatically` returns **no**,
even when pending tasks exist. This is intentionally conservative: a future autonomy
controller must not treat interrupted=True as auto-continue=True. The `Next best action`
section still guides the human operator to inspect the timeline and then resume manually.

**Next best action priority (deterministic, no LLM):**
1. Workspace_write denied + pending tasks → `set-permission … allow workspace_write`.
2. Interrupted run + pending tasks → `timeline <job_id>` then `run-next-task-local`.
3. Patch risk (medium/high/unknown) + pending tasks → review, then `run-next-task-local`.
4. Pending tasks, no blockers → `run-next-task-local`.
5. No pending tasks → inspect files or `create-job`.

**Design principles:**
- Read-only: never mutates job state or run logs.
- No external dependencies: plain text only.
- Shares `load_run_events` from `timeline.py` — one reader, two views.

### Approval Queue v1 (Step 19)

`packages/orchestration/approval_queue.py` provides metadata-only approval decisions for
patch intents.  Four new CLI commands: `list-patch-intents`, `show-patch-intent`,
`approve-patch-intent`, `reject-patch-intent`.

**Scope:** Approval is a recorded decision only.  It does not apply patches, modify
repository files, or trigger any automated action.  The apply step is not implemented
in this version.  A future Visual Patch Lab / apply step will consume approvals.

**Approval states:**
- `pending` — no decision recorded (implicit default for every new intent)
- `approved` — user reviewed and approved
- `rejected` — user reviewed and rejected

**Latest decision wins:** calling `approve-patch-intent` after `reject-patch-intent`
(or vice versa) overwrites the stored state.  No intent is irrecoverably decided while
no apply step exists.

**Intent IDs (v1):**
Format `"<artifact_short_id>-<idx>"` — the first 8 hex characters of the owning
artifact's UUID followed by the 0-based index into its `patch_intent_explanations` list.
Example: `a1b2c3d4-0`.  IDs are deterministic and stable across sessions.

**Intent ID ordering invariant (v1):** IDs are index-based, so the ordering of
`patch_intent_explanations` in artifact metadata must not change after approval decisions
are recorded.  Reordering the list would misalign existing approvals with the wrong intents.
Builders and future code must treat `patch_intent_explanations` as append-only once written.
Future versions with multi-intent or regenerated-intent workflows should replace this with
content-hash-based stable IDs (e.g. SHA256 of `target_path + action + intent`) to survive
reordering and regeneration.

**Storage:** Approval data is stored durably in `artifact.metadata["patch_intent_approvals"]`
as a dict mapping `intent_id → approval dict`.  The approval dict contains:
`intent_id`, `target_path`, `action`, `risk`, `state`, `decided_at`, `decided_by`,
`reason` (optional free-text from the user, stored in metadata only — not in run logs).

**Run log events:** `patch_intent_approved` / `patch_intent_rejected`
Metadata: `intent_id`, `target_path`, `risk`, `reason_present` (bool).  The raw reason
string is **never** written to run logs (redaction policy).

**Invalid stored risk values:** Any `risk` value not in `RISK_LEVELS` is coerced to
`RISK_UNKNOWN` by `list_patch_intents` and `set_approval_state`.  Unknown values must not
be treated as equivalent to `RISK_LOW` (see patch_intent.py module docstring).

**Cockpit integration (Step 19):**
- Pending approval + medium/high/unknown risk → `Needs your attention` item with pending
  count and `remedy list-patch-intents` command.
- Rejected intents → separate attention item with count.
- Pending approvals + risk → `Next best action` directs to `list-patch-intents`, then
  `approve-patch-intent`, then `run-next-task-local`.
- All intents approved + no pending tasks → next action notes approval is complete and
  states that the apply step is not implemented in v1 (does not imply files changed).

**Public API::

```python
list_patch_intents(job: Job) -> list[dict]
    # All intents across all artifacts, with current approval state.
    # Invalid stored risk coerced to RISK_UNKNOWN.

get_patch_intent(job: Job, intent_id: str) -> dict | None
    # Single intent by intent_id; None if not found.

set_approval_state(job, intent_id, state, *, reason=None, decided_by="user") -> dict
    # Record an approval decision.  Caller must save_job() afterwards.
    # Raises ValueError for invalid state or unknown intent_id.

make_intent_id(artifact_id: UUID, idx: int) -> str
    # Build the stable "<short_id>-<idx>" intent ID.
```

### Trust Report v1 (Step 20)

`packages/orchestration/trust_report.py` provides a read-only, auditable, plain-text
summary of a Remedy job.

**Relationship to Timeline and Cockpit:**

| View         | Question answered                                             |
|--------------|---------------------------------------------------------------|
| Timeline     | What happened, in chronological order?                        |
| Cockpit      | Where are we right now, what matters, what should I do next? |
| Trust Report | What was requested, planned, run, created, verified, decided, and explicitly NOT done? |

The Trust Report is the audit-ready view.  It assembles evidence across all layers of the
system — Job model, Artifact metadata, run-log JSONL, Permissions, and Approval Queue —
into a single, deterministic, human-readable document.

**Scope:** Read-only.  No `save_job`, no artifact mutation, no filesystem writes, no repo
writes, no shell execution, no LLM calls.  No new dependencies.  One public function:

```python
summarize_trust_report(
    job: Job,
    events: list[dict],
    *,
    data_dir: Path | None = None,
    constitution: ProjectConstitution | None = None,
) -> str
```

**Report sections (numbered, deterministic order):**

1. **User request** — `job.user_prompt` (truncated at 400 chars) or fallback to job name.
2. **Plan** — task count by status, task types and descriptions.
3. **Execution summary** — run invocations, completed, failed/blocked, no-op, interrupted.
   `planning_failed` events are shown as `✕ Planning failed: <error_category>` (or
   `unknown error` when no `error_category` is set).  Raw `message` from `planning_failed`
   events is never rendered — same redaction rule as Timeline v1.
4. **Artifacts** — one line per artifact (name + short ID + kind); raw content never shown.
5. **Verification** — per-task pass/fail from `verification_passed`/`verification_failed`
   events; failed check names shown; raw exception text never shown.
6. **Permissions and safety** — all four capabilities with effective state and reserved note;
   blocked run events (permission-denied `task_run_failed`) shown as a list.
7. **Patch intents and decisions** — all intents with state, risk, action, target path;
   approval counts; explicit note: approval is metadata-only, apply not implemented in v1.
   Free-text approval `reason` supplied by the user is stored in artifact metadata only and
   is never rendered in the Trust Report.
8. **Redaction / trust boundary** — explicit statement that raw prompts, artifact content,
   and diff text are not included; run logs contain structured labels/counts/outcomes only.
9. **Next safe action** — priority order: plan job (if no tasks) → grant permission →
   inspect timeline → review intents → run task → create job.
   When `job.tasks` is empty, the action is always `plan-job-local` — never "Inspect
   generated files", which would be misleading before any planning has occurred.

**Approval/rejection CLI output redaction:** `approve-patch-intent` and
`reject-patch-intent` do not echo the free-text `--reason` argument in their output.
Instead they print `reason: recorded` (when a reason was supplied) or `reason: none`.
The raw reason is stored in `artifact.metadata["patch_intent_approvals"]` for the caller's
reference, but is never surfaced in CLI summaries, run logs (`reason_present` bool only),
or the Trust Report.

**Redaction policy:** The Trust Report inherits the run-log redaction contract — no raw
exception text, no raw artifact content, no full diff previews, no free-text approval
reasons.  The report renders only IDs, counts, labels, risk levels, approval states, and
target paths already stored in structured metadata.

**CLI command:** `remedy trust-report <job_id>` — loads job, loads run events via
`timeline.load_run_events`, prints the report to stdout, exits 0.  If no run logs exist,
the report still renders (execution section says "No run logs available") and exits 0.

### Project Constitution v1 (Step 21)

`packages/orchestration/project_constitution.py` provides a read-only, deterministic
extraction of project policy signals from known files in an attached target repository.

**Purpose:** Give Remedy a structured, machine-readable description of a project's expected
commands, risky paths, coding conventions, and approval hints.  This is the foundation for
future Context Inspector, Verifier Marketplace, MCP Quarantine, Autonomy Modes, and
Memory/MemPalace integration.  It is **not an enforcement layer** in v1 — nothing in the
task execution pipeline consults the constitution today.

**Model:** `ProjectConstitution` (Pydantic BaseModel) with fields:
`source_files`, `test_commands`, `build_commands`, `lint_commands`,
`forbidden_commands`, `risky_paths`, `protected_paths`, `doc_paths`,
`repo_conventions`, `approval_rules`, `definition_of_done`, `warnings`.

**Public API:**
```python
load_project_constitution(repo_root: Path | None) -> ProjectConstitution
render_constitution(constitution, repo_root) -> str
```

**Extraction sources (fixed set — no recursive scan):**
`AGENTS.md`, `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`,
`pyproject.toml`, `package.json`, `Makefile`, `justfile`, `tox.ini`, `pytest.ini`,
`.github/workflows/*.yml` (up to 10 files).

**Extraction is purely lexical:** string/regex matching only.  No `eval`, no `import`,
no subprocess.  Uncertain findings are phrased as "detected" / "possible" / "suggested".
`tox.ini` and `pytest.ini` currently produce the advisory command `"pytest"`; future
autonomy modes must treat Constitution commands as hints, not guaranteed exact project
invocations.

**Safety constraints:**
- Read-only.  No subprocess, no shell, no writes.
- Path boundary enforced: `Path.resolve().relative_to(repo_root.resolve())` — symlink-safe.
- Secret files never read: files whose name starts with `.env`, `secret`, `credential`,
  `token`, `.netrc`, or ends with `.key`, `.pem`, `.p12`, `.pfx`, `.crt`.
- Max 200 lines read per file; max 10 workflow files scanned.

**CLI command:** `remedy constitution <job_id>` — loads job, reads `target_repo`,
calls `load_project_constitution`, prints `render_constitution` output, emits
`project_constitution_loaded` run log event with `source_count`, `warning_count`,
`has_test_commands` (structured counts only — no raw file content).
Exits 0 even when no repo is attached (prints warning).

**Cockpit integration:** `summarize_cockpit` accepts an optional `constitution` parameter.
When provided, a concise `constitution: N source file(s)` line appears in the
Important artifacts section.  No line appears when `constitution=None`.

**Trust Report integration:** `_cmd_trust_report` loads the constitution at render time
(same pattern as cockpit) and passes it to `summarize_trust_report`.  Section 6
(Permissions and safety) renders a one-line Project Constitution status:

| Condition | Displayed text |
|-----------|---------------|
| `constitution` provided, sources found | `Project Constitution: available from N source file(s)` |
| `constitution` provided, no sources, no warnings | `Project Constitution: no sources found` |
| `constitution` provided, warnings, no sources | `Project Constitution: unavailable (attached repo missing or not a directory)` |
| `constitution=None`, `target_repo` set in metadata | `Project Constitution: not loaded (run: remedy constitution <job_id>)` |
| `constitution=None`, no `target_repo` | `Project Constitution: no attached repo` |

The constitution is never persisted to job metadata — it is loaded fresh and read-only each time.

### Agent Loop Contract v1 (Step 22)

`packages/orchestration/agent_loop.py` defines the orchestration contract and data models
for coordinating external agent workflows.

**Purpose:** This is a contract and inspection layer — not execution.  External tools
(Claude Code, Copilot CLI, local models) are **not called** in v1.  The module provides
immutable models, deterministic state derivation, and a CLI inspection command with an
audit trail.

**Models (all immutable):**

| Model | Type | Key fields |
|-------|------|-----------|
| `AgentRole` | `str, Enum` | planner, builder, reviewer, fixer, verifier, reporter |
| `AgentLoopStage` | `str, Enum` | planned, build, review, fix, verify, completed, blocked, failed |
| `AgentLoopDecision` | `str, Enum` | continue, needs\_review, needs\_fix, needs\_approval, blocked, complete |
| `AgentAdapterSpec` | `frozen dataclass` | name, role, provider, command\_hint, capabilities (frozenset), dry\_run\_only=True, notes (tuple) |
| `AgentLoopState` | `frozen dataclass` | job\_id, current\_stage, cycle, max\_cycles, decision, builder, reviewer, pending\_findings, completed\_cycles, blocked\_reason |

All `AgentAdapterSpec` instances default to `dry_run_only=True` — no execution in v1.

**Public API:**
```python
default_agent_loop_state(job, *, max_cycles=3) -> AgentLoopState
summarize_agent_loop_state(job, state) -> str
derive_agent_loop_state(job, events, *, max_cycles=3) -> AgentLoopState
```

**State derivation (deterministic, priority order):**

| Priority | Condition | Decision | Stage |
|----------|-----------|----------|-------|
| 1 | Current blocker (see below) | `blocked` | `blocked` |
| 2 | Pending medium/high/unknown-risk patch intent | `needs_approval` | `review` |
| 3 | All tasks done + all non-low intents approved | `complete` | `completed` |
| 4 | Pending tasks | `continue` | `build` |
| 5 | No tasks | `continue` | `planned` |

Low-risk pending intents do not trigger `needs_approval` in v1.  Unknown risk is
treated conservatively (same as high risk — requires approval).

**Blocking logic (Step 22.1 — stale-event fix):**

Agent Loop derives the *current* orchestration state, not the worst historical event.
A blocker is active when EITHER:

1. A non-reserved capability is **explicitly** set to `"deny"` in `job.metadata["permissions"]`
   AND pending tasks exist.  Default-deny states (e.g. `repo_generated_write` before it
   has been granted) do not constitute a current block.
2. A `task_run_failed outcome=permission_denied` event exists for a task that is still
   `PENDING` in `job.tasks` AND no later `task_run_completed` event exists for the same
   `task_id`.  Events without a `task_id` are treated conservatively (cannot be proven stale).

Historical `permission_denied` events are **ignored** (treated as stale) when:
- There are no pending tasks (all work is done or no work has started yet).
- The same `task_id` has a later `task_run_completed` event.
- The corresponding task is no longer `PENDING` in `job.tasks`.

**`blocked_reason` format:**

```
"permission_denied:<capability>"   — e.g. "permission_denied:workspace_write"
"permission_denied"                — capability unknown (legacy event without metadata)
```

Summary output renders `"permission_denied:workspace_write"` as
`blockers: permission_denied (workspace_write)`.  The next-action hint renders the
concrete `remedy set-permission <job_id> allow workspace_write` command.

**`agent_loop_inspected` run-log schema (intentionally minimal and fixed):**

```json
{
  "event": "agent_loop_inspected",
  "outcome": "inspected",
  "metadata": {
    "stage":                "<AgentLoopStage value>",
    "decision":             "<AgentLoopDecision value>",
    "cycle":                0,
    "max_cycles":           3,
    "pending_finding_count": 0
  }
}
```

No raw artifact content, prompts, approval reasons, diff previews, command output,
or exception messages appear in the run log.

**CLI command:** `remedy agent-loop <job_id>` — loads job and run events, derives state,
prints `summarize_agent_loop_state` output, writes `agent_loop_inspected` run log event.

**Run-log event names:**

| Event | Status | Description |
|-------|--------|-------------|
| `agent_loop_inspected` | active — emitted by `remedy agent-loop` | Loop state snapshot |
| `external_agent_proposed` | reserved | External agent submitted a proposal |
| `external_review_recorded` | reserved | Reviewer agent returned findings |
| `fix_cycle_requested` | reserved | Fixer agent was requested |
| `agent_loop_completed` | reserved | Loop reached a terminal state |

**Future adapter examples:** `claude_code_builder`, `copilot_cli_reviewer`,
`local_model_reviewer`.  All adapters must be `dry_run_only=True` in v1.

**Authority:** Remedy remains the sole authority — permissions, verifier profiles,
project constitution, run logs, cockpit, and trust report govern all decisions.
Agent loop decisions are recommendations only; human approval gates are enforced by
the existing approval queue.  Agent loop must integrate with the future autonomy ladder
and respect MCP quarantine boundaries when adopted.

### Verifier Profiles v1 (Step 15)

`packages/orchestration/verifier_profiles.py` introduces profile-based semantic verification. Profiles are deterministic and local-only — no shell execution, no LLM calls.

**Routing chain:**
```
task.inputs["task_type"]
  → get_task_type_spec(task_type)  [task_registry.py]
  → TaskTypeSpec.verifier_profile  (e.g. "repo_doc")
  → get_verifier_profile(name)     [verifier_profiles.py]
  → VerifierProfile                (checks applied to artifact.content)
```

**v1 profiles:**

| Profile | min_changes | forbidden_phrases | required_sections |
|---------|-------------|-------------------|-------------------|
| `generic` | 1 | _(none)_ | Summary:, Proposed Changes: |
| `repo_doc` | 1 | TODO, TBD | Summary:, Proposed Changes: |
| `analysis_doc` | 2 | maybe, probably, some files, TODO | Summary:, Proposed Changes: |
| `implementation_plan` | 2 | some files, maybe, probably | Summary:, Proposed Changes:, Risks: |

**Task type → profile mapping (Step 15):**
- `readme` → `repo_doc`
- `plan` → `implementation_plan`
- `spec`, `requirement`, `acceptance`, `analysis` → `analysis_doc`
- `changelog`, `architecture`, `design`, `guide`, `documentation`, `doc` → `repo_doc`
- Unknown task types → `generic` (conservative fallback)

**Responsibility split:**
- `TaskContract` controls structural/materialization requirements:
  - artifact present (`has_output_artifact`, `artifact_exists`, `artifact_task_id_matches`)
  - workspace file present, exists, and non-empty (`workspace_file_in_metadata`, `workspace_file_exists`, `workspace_file_not_empty`, `has_proposed_change`)
- `VerifierProfile` controls artifact-content profile checks:
  - `required_section:<section>` — section header must appear in `artifact.content`
  - `min_proposed_changes` — count of `  - ` lines in Proposed Changes section must meet threshold
  - `forbidden_phrase:<phrase>` — phrase must be absent from `artifact.content` (case-insensitive)

**Profile-driven checks** run after the task artifact is confirmed valid. They are independent of workspace-file requirements; workspace-file checks are controlled by `TaskContract`. Profile checks are skipped only when `TaskContract(require_artifact=False)` is used, because they operate on `artifact.content`.

These checks are the **first real Task Contract layer**: they enforce output quality at the content level, not just at the file-existence level. This is the foundation for better autonomy modes, run-log quality gates, and future per-task SLAs.

### Artifact Kinds v1 (Step 14)

`packages/core/models.py` exposes `ArtifactKind`, a `str` enum that annotates
the semantic role of each `Artifact`.

**Values:**

| Value | Meaning |
|-------|---------|
| `unknown` | Default / not yet classified (backward-compat default for old JSON) |
| `planning` | Produced by a planning step (deterministic or LLM planner; `task_id=None`) |
| `builder_proposal` | Produced by a builder/task execution step (`task_id` set) |
| `workspace_materialization` | Represents a file written to the local workspace |
| `verification` | Produced by a verification step |
| `patch_intent` | Produced by patch-intent derivation (`patch_intent.py`) |
| `repo_application` | Produced by repo application (`repo_applicator.py`) |

**`Artifact.kind` field:**
- Default: `ArtifactKind.UNKNOWN` — backward-compatible; old JSON without `kind` deserializes to `UNKNOWN`.
- Set explicitly at all creation sites in `job_runner.py`, `llm_planner.py`, and `task_runner.py`.
- **v1 active:** `PLANNING` and `BUILDER_PROPOSAL` are the only kinds currently emitted; `WORKSPACE_MATERIALIZATION`, `VERIFICATION`, `PATCH_INTENT`, and `REPO_APPLICATION` are reserved for future steps.

**Artifact index helpers** (`packages/orchestration/artifact_index.py`):

```python
artifacts_by_kind(artifacts, kind)              # → list[Artifact]
first_artifact_by_kind(artifacts, kind)         # → Artifact | None
task_artifacts_by_kind(artifacts, task_id, kind) # → list[Artifact]
planning_artifact(artifacts)                    # → Artifact | None
```

`planning_artifact` prefers explicit `kind=PLANNING` but falls back to the legacy
convention (`name="planning_output"` and `task_id=None`) for pre-Step-14 artifacts.

### Task Type Registry v1 (Step 13)

`packages/orchestration/task_registry.py` is the central, extensible semantic catalogue
of known task types.

**Design:**
- `task_type` is **not** a closed enum — LLM-generated task types remain valid.
- Known task types get structured `TaskTypeSpec` metadata (routing, verifier profile,
  agent role hint, capabilities).
- Unknown task types fall back to a **conservative** spec: `repo_route=None`,
  `verifier_profile="generic"`, `capabilities=frozenset({"unknown_task_type"})`.
  Future autonomy modes MUST NOT treat an unknown type as low-risk.

**`TaskTypeSpec` fields:**

| Field | Description |
|-------|-------------|
| `name` | The queried `task_type` string |
| `description` | Human-readable purpose summary |
| `allowed_outputs` | Artifact kinds the task may produce |
| `repo_route` | Fully-resolved repo-relative path, or `None`; no `{safe_type}` in the returned value |
| `verifier_profile` | Verifier profile name (`"generic"` in v1) |
| `suggested_agent_role` | Builder role hint (`"generic_builder"` in v1) |
| `capabilities` | Frozenset of tokens; `{"unknown_task_type"}` signals unknown |

**Public API:**

```python
get_task_type_spec(task_type)  # → TaskTypeSpec — single source of routing truth
is_known_task_type(task_type)  # → bool
iter_task_type_specs()         # → tuple[TaskTypeSpec, ...]
```

**Single source of truth:** both `repo_applicator._resolve_repo_path` and
`patch_intent._derive_target_path` now delegate to `get_task_type_spec()`.
The formerly duplicated `_REPO_PATH_RULES` / `_INTENT_RULES` tables are removed.
Routing parity is guaranteed by construction and enforced by `TestKeywordSync`.

**Keyword ordering (v1):** first keyword that is a case-insensitive substring wins.
`"plan"` precedes `"doc"`; `"documentation"` precedes `"doc"` (substring ordering).
Source code task types (`write_code`, `write_tests`, etc.) return `repo_route=None`.

**Prepared for future steps:**
- Step 14+: verifier profiles → route-specific verification rules
- Step 14+: suggested_agent_role → role-specific builder prompts
- Step 15+: autonomy-mode gating — unknown type → conservative/deny path
- Future: context selection, MemPalace integration, subagent roles

### Patch Intent v1 (Step 10)

`packages/orchestration/patch_intent.py` introduces the first structured concept for
changes to existing files — as proposals only.  No repo files are read or modified.

**`PatchIntent`** — a Pydantic model representing one proposed change:
- `target_path`: repo-relative path of the file that would be changed (relative, `.md` only in v1)
- `intent`: human-readable description of the proposed change
- `rationale`, `expected_effect`: optional context fields
- `safety_notes`: list of notes about what was checked and deferred

**`PatchIntentSet`** — container for all intents from one task artifact:
- `task_id`, `artifact_id`: provenance fields (UUID)
- `intents`: list of `PatchIntent` (may be empty — always valid)

**`derive_patch_intents(artifact, task_type)`** — conservative derivation via
`task_registry.get_task_type_spec()`. Only task types that map to a documentation path
(`repo_route != None`) produce an intent; all others produce an empty set. Raw LLM
strings are never used to construct `target_path`.

**`verify_patch_intent_set(pis)`** — pure structural verifier; returns `list[str]` of errors:
- `target_path` is non-empty and relative (no leading `/`)
- `target_path` contains no null bytes
- `target_path` has no `..` traversal components
- `target_path` ends in `.md` (documentation-like paths only in v1)
- `intent` is non-empty
An empty `intents` list is always valid.

**`materialize_patch_intents(pis, runtime, task_index, task_type)`** — writes the
`PatchIntentSet` as a JSON file into the Remedy-owned workspace at:
`patch_intents/{index:03d}_{safe_type}_{short_id}.json`
Returns `None` when `intents` is empty (no file written).

**Artifact metadata keys (Step 10 / 10.5):**

| Key | Set when | Added by |
|-----|----------|----------|
| `patch_intent_file` | verification passed, intents materialized | CLI |
| `patch_intent_count` | verification passed, intents materialized | CLI |
| `patch_intent_errors` | verification failed (non-fatal) | CLI |

Patch intent verification errors are **not fatal** in v1.  When `verify_patch_intent_set`
returns errors, the CLI prints a warning to stderr and records the errors in
`artifact.metadata["patch_intent_errors"]`.  No intent file is written.  Task completion
is still governed by the existing task verifier — patch intent errors do not roll back the
task.

**`derive_patch_intents` invariant guards:**
- `artifact.task_id is None` → `RuntimeError` (planning artifacts must not be used)
- `artifact.id is None` → `RuntimeError` (artifact must have a valid id)

### Dry-Run Preview, Explanation, and Risk Layer (Steps 11–12.5)

`generate_dry_run_preview(pis, artifact_content, task_type, repo_root=None)` adds the
first read-only interaction with the target repository.  **No files are written.**

For each intent in the `PatchIntentSet`:
- If `repo_root` is provided and the target file **exists**: `action = "modify"`, first
  few lines of the existing file are shown as context.
- If `repo_root` is provided and the target file **does not exist**: `action = "create"`.
- If `repo_root` is `None`: `action = "preview-only"` (no filesystem access at all).

Proposed-change lines are extracted from the builder artifact's `Proposed Changes:`
section and shown in the preview block.  Raw LLM strings are never used directly —
they are extracted, section-bounded, and shown as labeled additions, not as patches.

`format_dry_run_explanations(results)` renders results as a human-readable CLI block.
Multiple intents are separated by a blank line:

```
Planned change:
  file   : README.md
  action : modify
  risk   : medium
  reason : task type 'write_readme'
  summary: adds installation and usage sections
```

**Risk classification** (`classify_risk(action) -> str`, Step 12):

| Action | Risk level | Meaning |
|--------|------------|---------|
| `create` | `low` | New file — no existing content at risk |
| `modify` | `medium` | Existing file would change |
| `overwrite` | `high` | Reserved — unconditional replacement (future) |
| `preview-only` / unrecognised | `unknown` | Cannot determine without repo context |

Risk levels are defined as explicit constants in `patch_intent.py`:
`RISK_LOW`, `RISK_MEDIUM`, `RISK_HIGH`, `RISK_UNKNOWN`, and `RISK_LEVELS` (frozenset).
`PatchDryRunResult.risk_level` is validated against `RISK_LEVELS` in `__post_init__` —
construction raises `ValueError` immediately for any invalid value.

**`RISK_UNKNOWN` is conservative:** future approval/autonomy modes must not treat it
as equivalent to `RISK_LOW`.  Attaching a repository and re-running will replace it
with a concrete level.

**Artifact metadata keys added in Steps 11–12:**

| Key | Set when | Added by |
|-----|----------|----------|
| `patch_intent_explanations` | intents present, no errors | CLI |
| `patch_intent_diff_preview` | intents present, no errors | CLI |
| `patch_intent_risks` | intents present, no errors | CLI |

`patch_intent_diff_preview` is capped at `_MAX_PREVIEW_CHARS` (2 000) characters before
storage via `truncate_preview(text)` in `patch_intent.py`.  Callers use the helper
rather than an inline slice so the constant stays in one place.
`patch_intent_risks` is a flat `list[str]` — one risk level per intent — for fast
scanning without parsing the full `patch_intent_explanations` dict list.

**Consumer contract:** any future code that reads `patch_intent_risks` from
`artifact.metadata` to make approval or autonomy decisions **must** validate every
value against `RISK_LEVELS` before acting (`from packages.orchestration.patch_intent import RISK_LEVELS`).  Stored strings are already validated at
write time by `PatchDryRunResult.__post_init__`, but defensive re-validation at the
consumption site guards against metadata written by older code, hand-edited records,
or future refactors that add new risk levels before consumers are updated.  Treat any
value outside `RISK_LEVELS` as `RISK_UNKNOWN` (conservative fallback).

**`diff_preview` CLI omission (intentional):** `format_dry_run_explanations` prints the
concise explanation block only (file / action / risk / reason / summary).  The full
`diff_preview` is stored in `patch_intent_diff_preview` metadata but not printed to the
terminal.  Reason: avoid noisy multi-line output for each intent; a future guarded mode
can surface it intentionally when prompting for approval.

**Design constraints (Steps 11–12.6, all still in effect):**
- Patch intents are created only when `vr.passed` (confirmed builder output only).
- `generate_dry_run_preview` resolves `repo_root` and each `target_file`; raises
  `RuntimeError` if the target is outside `repo_root` (defence in depth beyond
  `verify_patch_intent_set`'s static path checks).
- `generate_dry_run_preview` uses `read_text` (read-only); no open-for-write calls.
- `repo_overwrite` remains reserved; dry-run does not activate it.
- Intents are written to the Remedy workspace, not to the target repo.
- Risk classification is non-blocking — it does not gate or delay execution.
- The full patch-apply lifecycle (apply diff, verify result) is deferred to a
  future permission-gated step.

**Prior Step 10 design constraints (still in effect):**
- No repo files are modified by any function in `patch_intent.py`.
- target_path is always relative, traversal-free, and ends in `.md` (v1).

### Planner Output Validation

`PlannerOutput.proposed_tasks` requires at least one entry (`Field(min_length=1)`). A plan with zero tasks is invalid and rejected at the model boundary before reaching orchestration.

### Concrete Providers

**`packages/providers/ollama_planner/`** — Planner provider. Calls local Ollama with JSON schema enforcement. Configured via `REMEDY_OLLAMA_PLANNER_MODEL`, `REMEDY_OLLAMA_PLANNER_TEMPERATURE`, `REMEDY_OLLAMA_PLANNER_NUM_PREDICT`. The `ollama` package is an optional dependency; loaded lazily.

**`packages/providers/ollama_builder/`** — Builder provider. Same Ollama pattern for the builder role. Configured via `REMEDY_OLLAMA_BUILDER_MODEL`, `REMEDY_OLLAMA_BUILDER_TEMPERATURE`, `REMEDY_OLLAMA_BUILDER_NUM_PREDICT`. Env var parsing errors name the offending variable.

---

## Project Brain Graph v1 (Steps 23 / 23.1)

`packages/orchestration/project_brain.py` — read-only graph representation of a Remedy job.  It is a pure data contract layer and the foundation for a future visual cockpit.

**Scope constraints (enforced):**  No frontend, no rendering, no external processes, no repo mutation, no job/artifact writes, no patch apply, no memory writes, no shell/Git/Docker/network calls.  This module is observation-only.

### Purpose

The Project Brain Graph provides a single, normalised view of every meaningful entity in a job — tasks, artifacts, patch intents, approval decisions, verification events, permission blockers, agent-loop snapshots, and the Project Constitution — as a labelled directed graph.  This graph is the data contract that Step 24+ will map to React Flow / Three.js / AG-UI / A2UI / MemPalace / MCP Quarantine visual components.

### Relationship to other views

| View | Purpose |
|------|---------|
| Timeline | Chronological run-log event list |
| Cockpit | Decision-oriented status overview |
| Trust Report | Audit / provenance report |
| Agent Loop | Orchestration state machine snapshot |
| **Project Brain** | Graph-structured full-picture of all entities |

### Public API

```python
build_project_brain(job, events, *, constitution=None) -> ProjectBrainGraph
summarize_project_brain(graph) -> str
export_project_brain_json(graph) -> dict  # {"version": 1, "job_id", "nodes", "edges"}
```

All three functions are read-only, deterministic, and emit no side effects.

### Data models

`BrainNode(frozen=True)` — fields: `id`, `type`, `label`, `status`, `risk`, `ref_id`, `metadata: dict[str, str|int|bool]`

`BrainEdge(frozen=True)` — fields: `source`, `target`, `type`, `metadata: dict[str, str|int|bool]`

`ProjectBrainGraph(frozen=True)` — fields: `job_id: UUID`, `nodes: tuple[BrainNode, ...]`, `edges: tuple[BrainEdge, ...]`

### Node types

| Type | Source | Description |
|------|--------|-------------|
| `job` | `job` model | Top-level job |
| `task` | `job.tasks` | Individual task |
| `artifact` | `job.artifacts` | Output artifact |
| `patch_intent` | `list_patch_intents` | Proposed file patch |
| `approval_decision` | decided intents | Recorded approval or rejection |
| `verification` | `task_run_completed` events | Task verification passed |
| `permission_blocker` | `task_run_failed outcome=permission_denied` | Permission failure event |
| `run_event` | key lifecycle events | Notable run-log milestone |
| `agent_loop` | `agent_loop_inspected` events | Agent loop snapshot |
| `constitution` | constitution object or `project_constitution_loaded` event | Attached Project Constitution |
| `memory_placeholder` | always | Reserved for Step 24+ MemPalace |
| `mcp_placeholder` | always | Reserved for Step 24+ MCP Quarantine |

### Edge types

| Type | Direction | Description |
|------|-----------|-------------|
| `has_task` | job → task | Task membership |
| `created_artifact` | task (or job) → artifact | Artifact ownership |
| `emitted_event` | job → run_event | Event emission |
| `produced_patch_intent` | artifact → patch_intent | Patch derivation |
| `decided_by` | patch_intent → approval_decision | Decision linkage |
| `verified_by` | task → verification | Verification linkage |
| `blocked_by` | task → permission_blocker | Blocker linkage |
| `inspected_by` | agent_loop → job | Agent loop inspection |
| `governed_by` | job → constitution | Constitution governance |
| `future_memory_layer` | job → memory_placeholder | Future MemPalace |
| `future_mcp_layer` | job → mcp_placeholder | Future MCP Quarantine |

### Constitution node deduplication (Step 23.1)

`project_constitution_loaded` is represented **only** as a `constitution` node — it is **not** also promoted to a `run_event` node.  This prevents duplication: the dedicated constitution node (built from the event metadata or the live object) is the canonical representation.  `project_constitution_loaded` is therefore excluded from `_KEY_EVENTS`.

### Visual status legend (Step 24+ mapping)

The text summary includes a stable legend section for future visual mapping:

```
pending nodes: grey
running nodes: pulsing
completed nodes: white
blocked nodes: red
needs approval: amber
memory layer: violet
mcp quarantine: orange
```

No frontend or rendering exists in Steps 23/23.1.  This legend is a data contract for Step 24+.

### Sorting

Nodes are sorted by `(_NODE_TYPE_ORDER, id)` — type-priority order (job, task, artifact, …, memory_placeholder, mcp_placeholder) then lexicographic node ID.  Edges are sorted by `(source, target, type)`.  Both sorts are deterministic.

### Redaction policy

Read-only, no side effects, no repo/job/artifact writes, no memory writes, no patch apply.  No artifact content, no diff previews, no approval reasons, no event messages, and no raw command output appear in any node label, metadata value, summary string, or JSON export.  Only counts, IDs, risk labels, and status values are surfaced.  This policy applies to both text output and `--json` output.

### CLI

```
remedy brain <job_id>           # text summary (default)
remedy brain <job_id> --json    # JSON export (future frontend data source)
```

Loads the job, run events, and Project Constitution (from `target_repo` if attached; silently `None` if absent), builds the graph, and emits a `project_brain_inspected` run-log event.  With `--json`, prints `export_project_brain_json` serialised with `sort_keys=True`; text output and run-log event are otherwise identical.

`project_brain_inspected` metadata schema (exact keyset):
```json
{ "node_count": N, "edge_count": N, "task_count": N, "patch_intent_count": N }
```

The `--json` output is the intended data source for a future frontend (React Flow / Three.js / AG-UI); no frontend integration exists in Steps 23/23.1.

### Future steps (Step 24+)

Step 24+ will add:
- React Flow visual mapping (node type → component, edge type → connector style)
- Three.js 3-D cockpit rendering using the visual status legend above
- AG-UI / A2UI streaming integration
- MemPalace semantic memory nodes (replacing `memory_placeholder`)
- MCP Quarantine tool-layer nodes (replacing `mcp_placeholder`)

No frontend, AG-UI, Three.js, or MCP integration is present in Steps 23/23.1.

---

## Brain Node Detail v1 (Step 24)

`packages/orchestration/brain_detail.py` — read-only explanation and detail layer for individual Project Brain nodes.  This is the CLI foundation for the future "click a brain sphere and inspect it" UX in a visual cockpit.

**Scope constraints (enforced):**  Read-only only.  No repo mutation, no `save_job`, no patch apply, no permission mutation, no shell/subprocess/Git/Docker/network/MCP/Claude execution, no memory writes, no frontend implementation, no raw artifact content rendering.

### View relationships

| View | Purpose |
|------|---------|
| Project Brain (`remedy brain`) | Full graph map — all nodes and edges for a job |
| **Brain Node Detail (`remedy brain-node`)** | **Drill into one node — explanation, connections, evidence, actions** |
| Cockpit | Current decision/status overview |
| Timeline | Chronological run-log history |
| Trust Report | Full audit/provenance report |

Brain Node Detail is the future detail panel contract for React Flow / Three.js / AG-UI / A2UI: selecting a visual node will call this layer for its detail content.

### Public API

```python
build_brain_node_detail(job, graph, node_id, events) -> BrainNodeDetail
summarize_brain_node_detail(detail) -> str
export_brain_node_detail_json(detail) -> dict
```

Raises `ValueError` (safe message) if `node_id` is not found in the graph.  All three functions are read-only, deterministic, and emit no side effects.

### Data model

`BrainNodeDetail(frozen=True)` — fields:

| Field | Type | Description |
|-------|------|-------------|
| `job_id` | `str` | Parent job UUID |
| `node_id` | `str` | Graph node ID |
| `node_type` | `str` | Node type string |
| `title` | `str` | Human-readable title |
| `status` | `str` | Node status |
| `risk` | `str \| None` | Risk level (patch intents only) |
| `explanation` | `str` | Plain-text explanation of what this node is |
| `why_it_exists` | `tuple[str, ...]` | Reasons this node type appears in the graph |
| `connected_to` | `tuple[dict[str, str], ...]` | Incoming + outgoing edges with neighbour info |
| `evidence` | `tuple[str, ...]` | Short factual strings from safe metadata |
| `affected_files` | `tuple[str, ...]` | File paths (target_path or repo_applied_files only) |
| `next_actions` | `tuple[str, ...]` | Suggested CLI commands |
| `redaction_notes` | `tuple[str, ...]` | What is NOT rendered and why |

Each `connected_to` entry: `{"direction": "incoming"|"outgoing", "edge_type", "node_id", "node_type", "node_label"}`.

### Node-type behaviour

| Node type | Key detail surfaced |
|-----------|-------------------|
| `job` | State, task/artifact counts, prompt (truncated to 120 chars) |
| `task` | Task type, status, linked repo_applied_files |
| `artifact` | Kind, owner (task or job), repo_applied_files — no content |
| `patch_intent` | Target path, action, risk, state — no diff preview |
| `approval_decision` | State, decided_at, decided_by — no approval_reason |
| `verification` | Pass/fail status and task ref |
| `permission_blocker` | Blocked capability + `set-permission` hint |
| `run_event` | Event type and outcome — no message or command output |
| `agent_loop` | Stage, decision, cycle |
| `constitution` | Source count, has_test_commands |
| `memory_placeholder` | Informational — Step 24+ only |
| `mcp_placeholder` | Informational — Step 24+ only |

### Redaction policy

The following are **never** surfaced in any field, summary string, JSON export, or run-log event:
- `artifact.content`
- Diff preview (`patch_intent_diff_preview`)
- Approval reason text (`approval_reason`)
- Event message (`event.message`)
- Raw command output (`metadata.command_output`, `metadata.output`)
- Raw LLM prompts (user prompt is truncated to 120 chars for the job node)

### CLI

```
remedy brain-node <job_id> <node_id>           # text detail (default)
remedy brain-node <job_id> <node_id> --json    # JSON export
```

Loads the job, run events, and Project Constitution; builds the graph; calls `build_brain_node_detail`; prints text or `--json`; emits a `brain_node_inspected` run-log event.

`brain_node_inspected` metadata schema (exact keyset):
```json
{ "node_id": "...", "node_type": "...", "connected_count": N, "evidence_count": N }
```

The `--json` output is the intended data contract for a future frontend detail panel.  No frontend integration exists in Step 24.

---

## Brain CLI JSON Contract v1 (Step 24.1)

Step 24.1 hardens the machine-readable contract for the two brain CLI commands and establishes the canonical path for the future visual frontend.

### Canonical machine contracts

| Command | `--json` contract | Future consumer |
|---|---|---|
| `remedy brain <job_id> --json` | `export_project_brain_json` schema (version, job_id, nodes, edges) | 2D / 3D graph visualisation |
| `remedy brain-node <job_id> <node_id> --json` | `export_brain_node_detail_json` schema (13 keys) | Click-detail panel for a selected node |

**Invariants enforced and smoke-tested:**

- `--json` stdout is **pure JSON** — no human-readable header, no legend text, no trailing summary.
- `stderr` is empty on success for both commands.
- No `Traceback` appears in stdout on success.
- All 5 redaction sentinels are absent from `--json` stdout and from the corresponding run-log events (`project_brain_inspected`, `brain_node_inspected`).

### Run-log event schemas (exact key sets)

`project_brain_inspected` metadata (set by `remedy brain`):
```json
{ "node_count": N, "edge_count": N, "task_count": N, "patch_intent_count": N }
```

`brain_node_inspected` metadata (set by `remedy brain-node`):
```json
{ "node_id": "...", "node_type": "...", "connected_count": N, "evidence_count": N }
```

Both schemas hold regardless of whether `--json` is used.

### Future frontend priority (Step 24+)

1. **2D graph** via `remedy brain --json` + `remedy brain-node --json` — these JSON contracts are the integration surface for a React Flow / AG-UI / A2UI canvas.
2. **3D / Animus** — Three.js / WebGL rendering of the same graph JSON contract.
3. **MemPalace** — `memory_placeholder` nodes become live semantic memory nodes when the MemPalace layer is implemented (Step 24+).
4. **MCP Quarantine** — `mcp_placeholder` nodes become live MCP tool nodes when the MCP integration layer is implemented (Step 24+).

No frontend rendering exists in Steps 23–24.1.  The `--json` contracts are the stable integration surface that must not change without a version bump.

**Step 24.2** locks the smoke-level JSON contract before any frontend work begins.  After Step 24.2, future frontend code must treat `--json` stdout as the only machine-readable input and must never parse the human-readable text output (the non-`--json` mode).  Any regression in JSON stdout purity, stderr cleanliness, or run-log schema is a contract break.

**Step 24.3** is the final pre-frontend smoke hardening pass (redaction target alignment, raw-stdout sentinel checks, docstring polish).  After Step 24.3 the JSON contract is fully locked.

**Step 25** starts the read-only local Brain Viewer v0.  The viewer must consume only `remedy brain --json` (graph data) and `remedy brain-node --json` (node detail data).  It must not call any other CLI output mode, shell command, or internal Python API directly.

## Brain Viewer v0 (Steps 25 / 25.1)

`packages/orchestration/brain_viewer.py` generates a self-contained, read-only HTML viewer for a job's Project Brain Graph.  It is strictly read-only: it performs no repo mutation, no patch apply, no permission mutation, no shell/subprocess/Git/Docker/network/MCP/Claude execution, no memory writes, and has no external dependencies (Python stdlib only).

**Current scope:** Brain Viewer v0 is job-scoped.  It visualises a single job's graph.  It is not a Project Brain, a Repo Brain, or a Global Brain.  See *Future Brain Hierarchy* below.

### CLI

```
remedy brain-view <job_id>
```

Writes files under `REMEDY_DATA_DIR/viewers/<job_id>/`:
- `index.html` — self-contained dark-themed viewer with embedded JSON data
- `viewer_data.json` — machine-readable copy of the embedded data

Prints `Brain Viewer v0: <path>` to stdout on success.

**Smoke test helper.**  `scripts/remedy_smoke.sh` is an end-to-end smoke function that creates a project, a job (with `--task-type write_readme` — no planner call), runs the task, and asserts the brain viewer files are produced correctly.  It does not start any server.

```bash
# Source and call:
source scripts/remedy_smoke.sh
remedy_smoke

# Or run directly:
./scripts/remedy_smoke.sh
```

The smoke function runs its body in a subshell so sourcing it does not change the caller's shell options (`nounset`, `pipefail`).

On success the summary prints `VIEW_PATH` — the path to the generated `index.html` — which can be opened directly in a local browser:

```
open "file://<VIEW_PATH>"
```

No http.server, no LAN URLs, no PID files.

The frontend must consume only `viewer_data.json` and the embedded JSON already in `index.html`.  No other data sources are accepted.

**Constitution loading is advisory.**  If the attached repo path is absent, stale, or inaccessible, the viewer continues with `constitution=None` and prints a safe warning to stderr:

```
Warning: project constitution unavailable for viewer.
```

No raw exception messages are included.  The viewer is always generated.

### Run-log event

`brain_viewer_prepared` — emitted once per invocation with metadata:

```json
{
  "node_count": <int>,
  "edge_count": <int>,
  "detail_count": <int>,
  "detail_fallback_count": <int>,
  "mode": "static"
}
```

`detail_fallback_count` is an observable health signal: it counts the number of nodes for which full detail generation failed and a safe fallback was used instead.  It is 0 on a clean job.  Callers may use it to detect unexpected edge cases without ever logging raw exception messages.

### Architecture

`BrainViewerData` (frozen dataclass) — `{job_id, generated_at, graph, node_details, positions, detail_fallback_count}` — bundles all render data.  Built by `build_brain_viewer_data(job, graph, events)`, which calls `export_project_brain_json` for the graph and `build_brain_node_detail` / `export_brain_node_detail_json` per node.  Any per-node detail failure increments `detail_fallback_count` and uses a safe minimal fallback; it never propagates exceptions or exposes raw error text.

**Redaction:** same policy as `brain_detail.py` — no artifact content, diff previews, approval reasons, event messages, or raw command output in any generated file, including content injected via run-log events.

**Layout:** layered radial — job at centre (layer 0, r=0), constitution/tasks at layer 1 (r=150), artifacts/run_event/agent_loop at layer 2 (r=290), patch_intent/approval/verification/permission_blocker at layer 3 (r=420), memory_placeholder/mcp_placeholder at layer 4 (r=530).  Positions are pre-computed in Python and embedded in the HTML; JavaScript scales to the viewport.

**Rendering:** vanilla JS SVG with `esc()` for attribute safety, `data-nid` attribute for node click, `window.pick(nodeId)` for detail panel.  No external frameworks, no external network requests.

**Node colours:** `memory_placeholder`=#7c4fb0 (violet), `mcp_placeholder`=#e06c1a (orange), blocked=#cf4444, running=#4488ff (pulsing), completed/passed/loaded=#d0d7de, patch_intent pending=#d9a520, approved=#3fb950, default=#6e7681.

### Loading diagnostics and failure handling (Step 26.5)

**The Brain Viewer must never show an infinite spinner.**  The page body carries a `data-render-status` attribute that transitions through the following states:

| Status | Condition |
|---|---|
| `static-fallback` | Initial state; server-rendered fallback is visible; JS not yet run |
| `ready` | JS parsed graph; at least one node rendered; fallback hidden |
| `empty` | JS parsed graph; zero nodes; fallback hidden |
| `error` | JS initialisation or render threw an exception; fallback stays visible |

All JavaScript initialisation runs inside a `try/catch`.  A global `_vErr(category, msg)` function and a `window.onerror` handler both catch failures outside the IIFE.  On error, `_vErr` shows `#err-panel` (an overlaid warning box) and sets `data-render-status="error"`.  Only the JS error message is displayed, capped to 120 characters — no raw stack trace, no node content, no embedded JSON values.

A `#diag` bar below the legend shows live diagnostics populated by JavaScript after render:

- **nodes** — `G.nodes.length`
- **edges** — `G.edges.length`
- **details** — `Object.keys(DET).length`
- **fallbacks** — `VD.detail_fallback_count`
- **selected** — current selected node id (`none` until a node is clicked)
- **status** — current `data-render-status` value

These fields let a developer confirm graph data loaded correctly without opening browser dev-tools.  They are read-only and contain no raw content.

### Data island and static fallback (Step 27)

**Problem with Step 26.5:** embedding viewer data as `var VD=<json>;` in the execution script means a JS parse error in the data would prevent `_vErr` itself from being defined, leaving the spinner frozen.

**Fix:** use a non-executable JSON data island.

```html
<script id="viewer-data" type="application/json">{ ... }</script>
```

`type="application/json"` prevents browser execution.  The execution script reads it at runtime:

```javascript
var _src = document.getElementById('viewer-data');
if (!_src) throw new Error('viewer-data island missing');
var VD = JSON.parse(_src.textContent);
```

Any parse failure is caught by the surrounding `try/catch`, which calls `_vErr` — guaranteed because `_vErr` is defined outside the IIFE before the data is read.

**Server-rendered static fallback:** Python generates a `<div id="static-fallback">` containing a node/edge/detail/fallback count summary and a table of up to 50 nodes (type, label, status, risk).  This is visible immediately without JavaScript.  `setRenderStatus('ready')` and `setRenderStatus('empty')` hide it with `style.display='none'`.  On error, it stays visible alongside `#err-panel`, so the page always shows something useful.  The body starts at `data-render-status="static-fallback"` (not `"loading"`).

### v0 scope constraints

v0 is the read-only foundation.  Future steps will add:
1. **React Flow** — interactive 2D graph replacing the SVG layer.
2. **Three.js / Animus** — 3D visualisation.
3. **MemPalace** — live semantic memory nodes replacing `memory_placeholder`.
4. **MCP Quarantine** — live MCP tool nodes replacing `mcp_placeholder`.
5. **AG-UI / A2UI** — real-time streaming updates.

---

## Future Brain Hierarchy

*This section documents the intended architecture.  None of these layers are implemented yet.*

### Layer 1 — Job Brain

A single concrete job/prompt/run.  Current Brain Viewer v0 is job-scoped.  Every node in the current viewer belongs to a single job.

### Layer 2 — Repo Brain

A single attached repository: backend, frontend, pipeline, infra, docs, etc.  A Repo Brain aggregates:
- Multiple jobs targeting the same repo.
- Repo constitution (CLAUDE.md, test commands, lint rules, structure).
- Repo-level task/artifact/patch/verification history.
- Repo-scoped policy decisions.

### Layer 3 — Project Brain

A product or project spanning multiple repos and many jobs.  A Project Brain aggregates:
- Multiple repos (each with its own Repo Brain).
- Multiple jobs across repos.
- All repo constitutions.
- All task, artifact, patch intent, verification, and approval nodes.
- Project-level memory.
- Context coverage signals.
- Enabled skills and capabilities.
- Project-scoped policy decisions.

Future `remedy brain --json` may accept a `--scope project` flag that produces a multi-repo aggregate graph.  Current Brain Viewer v0 must not pretend to be a Project Brain.

### Layer 4 — Remedy Global Brain

Global reusable knowledge and capabilities.  Includes:
- **Quarantined MCPs** — MCPs under evaluation, not yet approved.
- **Approved MCP Skill Cards** — MCPs that passed quarantine and are globally registered as reusable skills.
- **Provider / model scorecards** — observed performance, latency, and cost data per provider/model combination.
- **Global capability policies** — default permission posture across all projects.
- **Verifier / provider / router knowledge** — reusable acceptance-criteria profiles and routing hints.

**MCP Skill Card lifecycle:**  MCPs that pass quarantine become globally registered Skill Cards.  However, a globally approved Skill Card does not automatically grant permission to any project or repo.  Projects must opt in via an explicit policy grant scoped to the project, repo, or capability.  A Skill Card is an offer; a policy grant is acceptance.

### Future Context Collector

The Context Collector should report *Context Coverage*, not an absolute "knowledge percentage".  Coverage is calculated from observable signals, not estimated from unknowns.  Signals include:

| Signal | Description |
|---|---|
| Repo constitution availability | Is a CLAUDE.md / constitution present and parseable? |
| Repo index coverage | What fraction of repo files have been indexed? |
| Relevant file coverage | Are the files relevant to the current task indexed? |
| Prior job/artifact availability | Are prior runs for this repo/task type accessible? |
| Project memory availability | Is project-level memory online? |
| Enabled MCP/tool context | Which MCP Skill Cards are active in this project? |
| Verifier/criteria availability | Are acceptance criteria defined for this task type? |
| Unresolved unknowns | Are there open blockers or ambiguities in the current job? |

Context Coverage is a health signal, not a score.  Low coverage means the agent lacks context — not that it is unintelligent.

### Future "Continue from Node"

Future node detail JSON may expose `continuable: bool` and `allowed_actions: list[str]` fields, enabling a "continue from node" workflow that creates a new job linked by:

```json
{
  "project_id": "<uuid>",
  "repo_id": "<uuid>",
  "parent_job_id": "<uuid>",
  "origin_node_id": "<node_id>",
  "origin_node_type": "<type>"
}
```

Not every node will be continuable.  These fields are **not implemented** in v0 and must not be added to current node detail JSON yet.


---

## Context Coverage v0 (Step 26)

`packages/orchestration/context_coverage.py` provides a deterministic, redaction-safe context-health indicator for a job.

**This is not a model confidence score and not a truth score.**  It is a context-health signal based on available, observable structured signals — job model fields, run-log events, and project constitution presence.

### CLI

```
remedy context <job_id> [--json]
```

Text output shows a coverage bar, present signals, missing signals, a meaning section, and next-action hints.  JSON output is pure parseable JSON.

### Run-log event

`context_coverage_inspected` — emitted once per invocation with metadata:

```json
{
  "score": <int>,
  "present_signal_count": <int>,
  "missing_signal_count": <int>,
  "scope": "job"
}
```

No labels, no prompt text, no paths, no raw details.

### Signals and weights (total = 100)

| Signal | Weight | v0 behaviour |
|---|---|---|
| `attached_repo` | 15 | present if `job.metadata["target_repo"]` is set |
| `project_constitution` | 15 | present if constitution is loaded with non-empty source files |
| `planned_tasks` | 10 | present if `job.tasks` is non-empty |
| `builder_artifacts` | 10 | present if any `BUILDER_PROPOSAL` artifact exists |
| `patch_intents` | 10 | present if patch_intent metadata or `patch_intent_created` event |
| `verification_results` | 10 | present if `verification_passed` or `verification_failed` event |
| `run_logs` | 10 | present if events list is non-empty |
| `approval_decisions` | 5 | present if `patch_intent_approved` or `patch_intent_rejected` event |
| `project_memory` | 10 | **always absent in v0** — MemPalace not connected |
| `mcp_tool_context` | 5 | **always absent in v0** — MCP Quarantine not connected |

`score = round(present_weight / 100 * 100)`, clamped 0..100.

### JSON export schema

```json
{
  "version": 1,
  "job_id": "<uuid>",
  "scope": "job",
  "score": <int>,
  "present_weight": <int>,
  "total_weight": 100,
  "signals": [{"key", "label", "present", "weight", "detail"}, ...],
  "missing_keys": ["<key>", ...]
}
```

### Brain integration

A `context_coverage` node (13th node type) is added to the Project Brain Graph on every `build_project_brain` call.  It is always present.

- `id`: `"context_coverage"` (fixed)
- `label`: `"Context Coverage (<score>%)"`
- `status`: `"low"` (score < 50), `"partial"` (50–79), `"strong"` (≥ 80)
- `metadata`: `{score, present_signal_count, missing_signal_count, scope}`
- Edge: `job --has_context_snapshot--> context_coverage`

The `brain-node context_coverage --json` detail explains what context coverage means, what is present/missing, and that it is not model confidence.

### Brain Viewer integration

- The context_coverage node appears in the graph in layer 1 (same as constitution/task).
- A `ctx-badge` in the viewer header shows `Context: <score>%`, populated by JavaScript from the embedded graph data.
- No external data is fetched.

### Redaction

No artifact content, diff previews, approval reasons, event messages, or raw command output appear in any signal detail, summary, or JSON export.  Signal details describe only structural facts (e.g. "3 artifact(s)"), never raw content.

### Scope in v0

Context Coverage v0 is job-scoped.  Future steps will add:
- **Repo Context Coverage** — aggregates multiple jobs targeting the same repo, adds repo index coverage and constitution richness.
- **Project Context Coverage** — aggregates across repos, adds project memory, cross-repo task history, and enabled skill coverage.
- **Global Context Coverage** — adds Global Brain signals: MCP Skill Card availability, provider scorecards, global policy coverage.

## Context Coverage v0 robustness and UX polish (Step 26.1)

Incremental hardening of Context Coverage v0.

### Safe integer parsing (`_safe_int`)

`context_coverage.py` now uses a `_safe_int(value, default=0)` helper for all artifact-metadata integer fields (starting with `patch_intent_count`).  Any value that cannot be parsed by `int()` — strings like `"not-an-int"`, empty lists, `None` — returns `default` instead of raising `ValueError` or `TypeError`.

### v0 maximum score = 85

Because `project_memory` (weight 10) and `mcp_tool_context` (weight 5) are always absent in v0, the maximum achievable score is **85**.  This is "complete for v0" — the score is never normalized to 100.  The summary Meaning section now explicitly states: *"In v0, the maximum score is 85% — Project Memory (+10) and MCP/tool context (+5) are not yet implemented."*

### Stale repo warning in `remedy context`

`_cmd_context` now mirrors `_cmd_brain_view`: if `target_repo` is set but the path does not exist or is not a directory, it prints a fixed safe warning to stderr and continues without a constitution.  Any unexpected exception from `load_project_constitution` is caught and the same warning is emitted.  The raw exception text is never surfaced.

## Project Registry v0 (Step 28)

`packages/orchestration/project_registry.py` — minimal project metadata store.

### Purpose

Projects are named scopes that group one or more repos and jobs.  They are the foundation for the future brain hierarchy:

```
Global Brain → Project Brain → Repo Brain → Job Brain
```

The registry stores and retrieves `RemyProject` records from disk.  No repo scanning, no artifact content, no approval reasons, no diff previews, no event messages.

### Data model

`RemyProject(BaseModel)` — Pydantic model with fields:

| Field | Type | Default |
|---|---|---|
| `id` | `UUID` | `uuid4()` |
| `name` | `str` | required |
| `description` | `str \| None` | `None` |
| `created_at` | `datetime` | UTC now |
| `repo_paths` | `list[str]` | `[]` |
| `job_ids` | `list[str]` | `[]` |
| `metadata` | `dict[str, Any]` | `{}` |

### Storage

Files are written to `<REMEDY_DATA_DIR>/projects/<project_id>.json` (env var) or `<repo_root>/.data/projects/<project_id>.json` (fallback).

### Public API

```python
save_project(project) -> None
load_project(project_id: UUID) -> RemyProject      # raises ProjectNotFoundError
list_projects() -> list[RemyProject]               # sorted newest-first; corrupt files skipped
attach_repo(project, repo_path) -> bool            # True if added (idempotent)
attach_job(project, job_id_str) -> bool            # True if added (idempotent)
summarize_project(project, jobs) -> str
export_project_json(project, jobs) -> dict
```

### CLI commands

```
remedy create-project <name> [--description <desc>]   — create and print project ID
remedy list-projects                                  — list all projects (newest first)
remedy attach-project-repo <project_id> <repo_path>  — attach a repo to a project
remedy attach-project-job <project_id> <job_id>      — link a job to a project
remedy project <project_id> [--json]                 — show project summary (user-facing alias)
remedy show-project <project_id> [--json]            — show project summary (backward-compat)
remedy create-job "<prompt>" [--project <project_id>]
    [--task-type <type>] [--task-description "<desc>"]
                                                       — create job and optionally link;
                                                         --task-type creates one Task immediately
                                                         and sets state=PLANNED (bypasses plan-job)
```

`remedy project` is the primary user-facing alias.  `remedy show-project` remains for backward compatibility; both call the same implementation.

When `--project` is passed to `create-job`:
- The project is **validated and loaded first**.
- If the project is valid: `metadata["project_id"]` is set, the job is created, and both are persisted.
- If the project UUID is invalid or not found: the job is still created **without** `metadata["project_id"]`, and a warning is printed to stderr: `Warning: project unavailable; job created without project link.`
- Raw exception text is never surfaced.

### Brain connection marker (`project_placeholder` node)

When a job has `metadata["project_id"]` set to a **valid UUID string**, `build_project_brain` adds:

- **Node**: `id="project:<project_id>"`, `type="project_placeholder"`, `status="linked"`, `label="Project <short_id>"`
- **Edge**: `job --belongs_to_project--> project:<project_id>`

This node is absent when:
- The job has no `project_id` in metadata.
- The `project_id` value is present but not a valid UUID string (malformed values are silently ignored).

It is a lightweight marker only — no project aggregation occurs in v0.

### Brain Viewer layer

`project_placeholder` nodes appear in layer 1 (same as `constitution`, `task`, `context_coverage`).

### JSON export schema

```json
{
  "version": 1,
  "project": {"id", "name", "description", "created_at"},
  "repo_paths": ["<resolved_path>", ...],
  "jobs": [{"id", "state", "task_count", "artifact_count"}, ...],
  "counts": {"repo_count", "job_count", "task_count", "artifact_count"},
  "future_layers": {
    "repo_brain": "not_implemented",
    "project_brain": "not_implemented",
    "global_brain": "not_implemented",
    "mempalace": "not_implemented",
    "mcp_skill_registry": "not_implemented"
  }
}
```

### Future layers (not implemented in v0)

| Layer | Description |
|---|---|
| Repo Brain | Aggregated brain across all jobs targeting the same repo |
| Project Brain | Aggregated brain across all repos in a project |
| Global Brain | Cross-project, cross-provider aggregate with skill registry |
| MemPalace | Semantic memory layer for jobs and projects |
| MCP Skill Registry | Registry of verified MCP skills available to agents |

### Redaction

No artifact content, approval reasons, diff previews, event messages, or command output appear in any project summary or JSON export.  Only counts, IDs, names, and status values are surfaced.

## Project Context Coverage v0 (Step 29)

`packages/orchestration/project_context_coverage.py` — project-scoped, deterministic context-health indicator.

### Purpose

Project Context Coverage is the first user-visible signal that Remedy is building project-level understanding across multiple repos and jobs.  A project may span a frontend repo, backend repo, pipeline repo, docs repo, and infrastructure repo — each with its own jobs.  Project Context Coverage aggregates structured context signals across all of them.

This is **not** model confidence, **not** a truth score, and **not** a Project Brain UI.  It is a deterministic read-only indicator of how much structured context is available at the project level.

### Scope

Project-scoped in v0.  Aggregates linked jobs and repo paths only.  No repo scanning, no event log reading, no artifact content.

### Signals (weights sum to 100)

| Signal | Weight | v0 behaviour |
|---|---|---|
| `project_metadata` | 10 | present when project object exists with a name |
| `linked_repos` | 15 | present if `project.repo_paths` is non-empty |
| `linked_jobs` | 15 | present if any linked Job objects are loaded |
| `planned_tasks` | 10 | present if any linked job has tasks |
| `builder_artifacts` | 10 | present if any linked job has a `BUILDER_PROPOSAL` artifact |
| `patch_intents` | 10 | present if any linked job has derived patch intents |
| `verification_results` | 10 | present if any `VERIFICATION` artifact or completed task across linked jobs |
| `approval_decisions` | 5 | present if any linked job has approved or rejected patch intents |
| `project_memory` | 10 | **always absent in v0** — MemPalace not connected |
| `mcp_tool_context` | 5 | **always absent in v0** — MCP Skill Registry not connected |

`score = round(present_weight / 100 * 100)`, clamped 0..100.  **v0 maximum = 85.**

### Public API

```python
derive_project_context_coverage(project, jobs) -> ProjectContextCoverageSnapshot
summarize_project_context_coverage(snapshot) -> str
export_project_context_coverage_json(snapshot) -> dict[str, Any]
```

`ProjectContextCoverageSnapshot(frozen=True)` — fields: `project_id`, `project_name`, `scope`, `score`, `present_signal_count`, `missing_signal_count`, `repo_count`, `job_count`, `signals: tuple[ProjectContextSignal, ...]`, `missing_keys: tuple[str, ...]`

`ProjectContextSignal(frozen=True)` — fields: `key`, `label`, `present`, `weight`, `detail`

### CLI

```
remedy project-context <project_id>
remedy project-context <project_id> --json
```

Loads the project and all linked jobs, derives the snapshot, and prints the summary or JSON.  Emits a `project_context_coverage_inspected` run-log event to the first linked job's run log (skipped if no jobs are linked).

### Run-log event

`project_context_coverage_inspected` — emitted once per invocation with metadata:

```json
{
  "score": int,
  "present_signal_count": int,
  "missing_signal_count": int,
  "scope": "project",
  "repo_count": int,
  "job_count": int
}
```

No raw prompts, artifact content, approval reasons, event messages, diff previews, or exception text.

### JSON export schema

```json
{
  "version": 1,
  "project_id": "<uuid>",
  "project_name": "<name>",
  "scope": "project",
  "score": 0..85,
  "present_signal_count": int,
  "missing_signal_count": int,
  "repo_count": int,
  "job_count": int,
  "v0_max_score": 85,
  "signals": [{"key", "label", "weight", "present", "detail"}, ...],
  "missing_keys": ["<key>", ...]
}
```

### Project JSON integration

`export_project_json(project, jobs)` (via `remedy project --json`) includes a compact context summary:

```json
"context_coverage": {
  "score": int,
  "scope": "project",
  "present_signal_count": int,
  "missing_signal_count": int,
  "v0_max_score": 85
}
```

Full signal details are available only via `remedy project-context <project_id> --json`.

### Not implemented in v0

| Layer | Status |
|---|---|
| Project Brain graph viewer | not implemented |
| Repo Brain | not implemented |
| Global Brain | not implemented |
| MemPalace (`project_memory` signal) | not implemented |
| MCP Skill Registry (`mcp_tool_context` signal) | not implemented |

### Redaction

No artifact content, approval reasons, diff previews, event messages, or raw exception text appear in any signal detail, summary, or JSON export.  Details describe only structural facts (e.g. `"3 repo(s)"`), never raw content.

## Patch Apply v0 (Step 30)

### Purpose

Patch Apply v0 is the first real execution slice after approval.  An approved PatchIntent can be applied to the attached repo under strict v0 constraints.  This is the first step that makes Remedy **execution-first**: the Brain/Viewer/Trust surfaces now show real work happening.

### Proof-chain model (Step 30.1)

Remedy's core differentiator is not autonomy alone — it is **auditability**.  Every real action must become a proof object traceable through the full intent chain:

```
Patch Intent → Approval Decision → Patch Apply → affected file
```

This is surfaced in run logs, Trust Report, Timeline, Brain, and Viewer with **structural evidence only** — never raw patch content or diff text.

Enforcement:
- No shell execution
- No Git operations
- No arbitrary diff application
- No `repo_overwrite`
- Markdown-only (`.md`)
- `modify` is append-only (markers, never replace/remove)
- Run-log schema is exact: `{intent_id, target_path, action, outcome, bytes_written, line_count}` — no extra keys

```
Prompt → Task → Artifact → Patch Intent → Approval → Apply → Verification
```

### Markerless Apply v0 (Step 30.4, hardened Step 30.8)

Remedy must never write internal control metadata into user repository files.
This is a hard invariant — there is no backward-compatibility migration for
historical marker blocks because Remedy is still in active development.

**Invariants:**
- No raw `<!--` HTML comment starts appear in any Remedy-written file
- No intent IDs appear in any written file
- No "Generated by Remedy" provenance strings appear in any written file
- `modify` appends a plain `## Proposed Update` Markdown section only
- `create` writes a plain `# <title>` / `## Proposed Update` structure only
- **Markdown write-boundary neutralization** (`neutralize_markdown_html_comment_start(text: str) -> str`
  in `packages/orchestration/markdown_output_safety.py`):
  every Remedy-generated text field passed to a repo file write replaces `<!--`
  with `&lt;!--` (HTML entity encoding). `&lt;!--` is renderer-portable and
  unambiguously not an active HTML comment. This applies to titles, summaries,
  and proposed lines from both `patch_apply.py` and `repo_applicator.py`.
  The helper accepts `str` only; callers must normalise optional metadata fields
  (e.g. `str(value or "")`) at the data boundary before calling it.
  The helper is defined once in `markdown_output_safety.py` and imported by
  both modules — it is not duplicated. Existing user file content is never rewritten.
- **Newline contract**: `_build_modify_section` and `_build_create_content` each
  return a string ending with exactly one newline. Callers compose around this
  contract rather than adding extra newlines.
- **Idempotency is metadata-only** via `patch_intent_apply_records[intent_id].state`
  — the target file is never read for idempotency detection.
  v0 has no recovery if both metadata and run-log proof are lost; file-content
  scanning is not supported and historical marker migration is not implemented.
- Provenance is preserved externally in apply records, run logs, Brain nodes,
  Timeline events, and Trust Report — not inside the repo files themselves

### End-to-end apply proof smoke (Step 30.3)

Step 30.3 locks the full apply proof lifecycle in the smoke script:

```
apply before approval  →  blocked (non-zero exit)
approve intent
apply approved intent  →  applied (file written)
repeat apply           →  noop (exit 0)
brain assertion        →  patch_apply node present
run-log schema check   →  exact keys {intent_id, target_path, action, outcome, bytes_written, line_count}
                          outcomes include: blocked, applied, noop
```

Additional proof hardening:
- Markdown write-boundary neutralization covers titles, summaries, and proposed
  lines in both `patch_apply.py` and `repo_applicator.py` via the shared
  `neutralize_markdown_html_comment_start` helper in `markdown_output_safety.py`.
  `&lt;!--` is chosen over `\<!--` for broader renderer portability.
- `RUNS_ROOT` uses the public filesystem convention only (`$REMEDY_DATA_DIR/runs` or
  `<repo_root>/.data/runs`); the smoke must not import private run-log helpers.

### Smoke markerless scan invariants (Step 30.7/30.8)

The smoke checks both the applied file and the whole TARGET_REPO for forbidden strings:

- Scans for raw `<!--` (any active HTML comment start — forbidden).
- Scans for `Generated by Remedy` (internal provenance string — forbidden).
- Scans for the concrete patch intent id when non-empty.
- Does **not** scan for `&lt;!--` or bare `remedy:patch-intent`, because the
  safely neutralized form `&lt;!-- …` is intentionally user-visible text.
- Applied file must also end with exactly one newline.
- Binary/unreadable files are skipped via `UnicodeDecodeError`/`OSError` catch.
- Smoke seeds `README.md` in TARGET_REPO before running so that `modify`-action
  apply always finds the target file (v0 modify requires the target to exist).
- Smoke creates the job with `--task-type write_readme` (Step 30.12), which sets
  `job.state = PLANNED` and creates exactly one `Task` with `inputs={"task_type":
  "write_readme"}` without calling `plan-job`. The smoke immediately asserts this
  before attaching the repo or running any task. The assertion reads job JSON via
  a Bash temp file (`mktemp`) rather than a nested `subprocess.run(['remedy', ...])`.
- Viewer sanity (step 12) is fully self-diagnosing: every check prints an
  actionable `ERROR: viewer sanity failed: <reason>` message; no bare `assert`.
  Checks: `version`, `graph`, `node_details`, `positions`, `detail_fallback_count`,
  `graph.nodes` non-empty, `node_details` count == `nodes` count, all HTML
  placeholder strings (`__VIEWER_DATA_JSON__` etc.) resolved in `index.html`.
- **Viewer redaction sentinel scan** (Step 30.13): After placeholder checks, step 12
  scans both `viewer_data.json` and `index.html` for precise dangerous tokens:
  `approval_reason`, `diff_preview`, `command_output`, `raw_command_output`,
  `DIFF_PREVIEW`, `RAW_COMMAND_OUTPUT`, `APPROVAL_REASON`, `MUST_NOT_RENDER`,
  `Traceback`, `Exception:`. Plain phrases like `artifact content` are **not** in
  the forbidden list — safe explanatory viewer copy such as "Does not include raw
  prompt, file content, artifact content, event messages." is intentional UI text,
  not a leak. The whole-repo markerless scan (step 6g) remains stricter because it
  checks generated target-repo files, not viewer explanatory text.
- This is a developer smoke invariant, not runtime Remedy behavior.

### v0 Constraints

| Constraint | Status |
|---|---|
| Markdown-only (`.md`) target paths | enforced |
| `create` action (new file) | supported |
| `modify` action (append-only) | supported |
| `high` / `unknown` risk | blocked |
| `pending` / `rejected` state | blocked |
| `repo_generated_write` permission required | enforced |
| `repo_overwrite` | **not used** — reserved for a future step |
| `shell_exec` | **not used** |
| Git operations | not implemented |
| Arbitrary unified-diff application | not implemented |
| Code-file patching | not implemented |
| Multi-loop autonomy | not implemented |

### Apply behavior

**`create`**
Writes a new markdown file.  Blocked if the target already exists.
Content (no Remedy provenance metadata — only user-facing Markdown):
```
# <title from target_path stem>

## Proposed Update

- bullet 1
- bullet 2
```

**`modify`**
Appends a plain Markdown section to an existing file.  Blocked if the target is missing.  Never replaces or removes existing content.
Appended section (no HTML control markers):
```
## Proposed Update

- bullet 1
- bullet 2
```

**Idempotency**
A second apply on the same intent is a no-op (`already_applied`).  Idempotency is **metadata-only** — the target file is never read to detect prior application.  The authoritative check is `patch_intent_apply_records[intent_id].state == "applied"` in the artifact metadata.

### Apply record

Stored under `artifact.metadata["patch_intent_apply_records"][intent_id]`:

```json
{
  "state":         "applied" | "noop" | "blocked",
  "applied_at":    "ISO timestamp",
  "target_path":   "README.md",
  "action":        "create" | "modify",
  "bytes_written": 42,
  "line_count":    5,
  "reason":        "applied"
}
```

No raw artifact content, approval reasons, or diff text is stored.

### CLI command

```
remedy apply-patch-intent <job_id> <intent_id>
remedy apply-patch-intent <job_id> <intent_id> --json
```

Exit codes: `0` on applied or noop; `1` on blocked (error message to stderr, no traceback).

### Run-log event

Event name: `patch_intent_applied`

```json
{
  "event":   "patch_intent_applied",
  "outcome": "applied" | "noop" | "blocked",
  "metadata": {
    "intent_id":     "a1b2c3d4-0",
    "target_path":   "README.md",
    "action":        "modify",
    "outcome":       "applied",
    "bytes_written": 42,
    "line_count":    5
  }
}
```

Emitted for all outcomes (applied, noop, blocked).  No raw content, approval reasons, or diff text.

### Brain integration

New node type: `patch_apply`

| Field | Value |
|---|---|
| node id | `apply:<intent_id>` |
| type | `patch_apply` |
| status | `applied` \| `noop` \| `blocked` |
| label | `applied <intent_id>` |
| metadata | `target_path`, `action`, `bytes_written`, `line_count` |

New edge type: `applied_by`  
Direction: `pi:<intent_id>` → `apply:<intent_id>`

The node is built from `artifact.metadata["patch_intent_apply_records"]`, not from run-log events.  No patch content or diff text appears in node metadata, detail view, or viewer data.

### Trust Report integration

Section 7 (Patch intents and decisions) now shows a structural apply line per applied intent:

```
  applied: yes  outcome=applied  target=README.md
```

No content, diff text, or approval reason is rendered.

### Timeline integration

`patch_intent_applied` events appear as:

```
  ✓ patch intent applied  a1b2c3d4-0  README.md  outcome=applied
```

### Redaction

The following are never surfaced in any apply record, run-log event, Brain node, Trust Report section, or Timeline entry:
- Raw artifact content
- Diff preview text
- Approval reason text
- Exception messages
- Command output

## Apply Snapshot + Diff Proof v0 (Step 31)

### Purpose

When `apply_patch_intent` successfully applies a patch intent, it records a **structural proof snapshot**: SHA-256 hashes of the file before and after the write, plus byte and line deltas. This proof is stored in job/artifact metadata and emitted as a new run-log event.

Rollback is not implemented in v0. The proof snapshot is evidence-only.

### Proof schema (stored under `apply_record["proof"]`)

```python
{
    "before_sha256":     str,   # "" for create (file did not exist)
    "after_sha256":      str,   # 64-char lowercase hex SHA-256
    "before_bytes":      int,   # 0 for create
    "after_bytes":       int,
    "bytes_delta":       int,   # after_bytes - before_bytes
    "before_line_count": int,   # 0 for create
    "after_line_count":  int,
    "line_delta":        int,   # after_line_count - before_line_count
}
```

The proof is a nested dict inside the existing apply record. It does **not** replace any existing apply record field.

### `patch_apply_proof_recorded` run-log event

A new separate event is emitted after every successful apply (not on noop, not on blocked). The `patch_intent_applied` event schema is **unchanged**.

Metadata exact keys (13):

```python
{
    "intent_id":          str,
    "target_path":        str,
    "action":             str,   # "create" | "modify"
    "outcome":            str,   # "applied"
    "before_sha256":      str,
    "after_sha256":       str,
    "before_bytes":       int,
    "after_bytes":        int,
    "bytes_delta":        int,
    "before_line_count":  int,
    "after_line_count":   int,
    "line_delta":         int,
    "applied_at":         str,   # ISO timestamp
}
```

### Surfaces

- **Brain node**: `patch_apply` node metadata extended with `before_sha256`, `after_sha256`, `bytes_delta`, `line_delta`. Brain Node Detail evidence shows truncated hashes (first 16 chars) and signed deltas.
- **Trust Report**: Section 7 shows a `proof:` line for each applied intent with truncated hashes and `Δbytes`/`Δlines`.
- **Timeline**: `patch_apply_proof_recorded` event rendered as `✓ patch apply proof  <intent_id>  after_sha=<first16>…  Δbytes=+N  Δlines=+N`.

### Redaction policy

The proof snapshot contains only structural hashes and counts. The following are **never** stored in the proof or emitted in the proof event:
- Raw file content (before or after)
- Full diff text
- Approval reason text
- Exception messages
- Command output
