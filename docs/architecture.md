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
| 1 | `task_run_failed` with `outcome=permission_denied` | `blocked` | `blocked` |
| 2 | Pending medium/high/unknown-risk patch intent | `needs_approval` | `review` |
| 3 | All tasks done + all non-low intents approved | `complete` | `completed` |
| 4 | Pending tasks | `continue` | `build` |
| 5 | No tasks | `continue` | `planned` |

Low-risk pending intents do not trigger `needs_approval` in v1.  Unknown risk is
treated conservatively (same as high risk — requires approval).

**CLI command:** `remedy agent-loop <job_id>` — loads job and run events, derives state,
prints `summarize_agent_loop_state` output, writes `agent_loop_inspected` run log event
with structured fields: `stage`, `decision`, `cycle`, `max_cycles`, `pending_finding_count`.
No raw artifact content, prompts, approval reasons, diff previews, or exception messages
in the run log.

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
