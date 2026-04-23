# Decisions

## 2026-04-23: Step 6.5 continues on feature/step6-workspace-runtime (PR #7)
Workspace materialization hardening is in-scope for PR #7 — same feature boundary
(workspace runtime, file materialization). Per Pull Request Continuity Rule, no new branch.

## 2026-04-23: _extract_proposed_changes uses section-header state machine, not prefix-only
Original approach grabbed all "  - " lines from artifact.content, mixing Notes and Risks
into the Proposed Changes output. A simple state machine keyed on known section headers
("Proposed Changes:", "Notes:", "Risks:") is correct and adds zero dependencies.

## 2026-04-23: Filename = index + safe_type + short_id (not task_type alone)
task_type alone is not collision-safe (two tasks can share a type) and is not path-safe
(user-supplied, arbitrary string). Index ensures ordering; short_id (task UUID[:8]) ensures
uniqueness. Format: {index:03d}_{safe_type}_{short_id}.txt. Readable and deterministic.

## 2026-04-23: _sanitize_path_component is local to task_runner.py
Only used by materialize_task_output. Keeping it local avoids premature abstraction.
If workspace.py ever needs its own path policy, it can define one separately.

## 2026-04-23: Materialization ordering documented, not enforced by transactions
materialize → save_job is the conservative ordering. Documenting it in the docstring
and architecture.md makes the contract explicit for future callers. No transaction
mechanism is added — overkill for a local dev tool at this stage.

## 2026-04-23: Step 6 on new branch (feature/step6-workspace-runtime)
Workspace runtime and file materialization have a different purpose (filesystem output)
and review scope from Step 5/5.5 (execution hardening, context, metadata). New branch
created from main after PR #6 merged.

## 2026-04-23: materialize_task_output re-derives proposed_changes from artifact content
The builder's proposed_changes are already serialized into artifact.content (lines starting
with "  - "). Re-parsing artifact.content avoids storing proposed_changes redundantly in
metadata or changing RunTaskResult/BuilderOutput signatures. Simple and zero-schema-change.

## 2026-04-23: workspace_file metadata key records absolute path
Stored as str (not Path) since Pydantic artifact metadata is dict[str, Any] and str
is unambiguous across platforms. Callers can convert to Path as needed.

## 2026-04-23: LocalWorkspaceRuntime is injected, not instantiated in orchestration
runtime.write() is the only filesystem operation in task_runner.py. Injecting the runtime
keeps orchestration testable and swappable — a future Docker or sandboxed runtime can
drop in with no orchestration changes.

## 2026-04-23: PlannerOutput.proposed_tasks min_length=1
An empty proposed_tasks list produces an unrunnable job with zero tasks. Rejected at the
model boundary before reaching orchestration. Symmetric with BuilderOutput.proposed_changes
min_length=1 (added in Step 5.7).

## 2026-04-22: Step 5.5 continues on feature/step5-task-execution (PR #6)
Execution hardening (failure rollback, richer context, metadata cleanup) is in-scope
for the same feature boundary as Step 5 (task execution). Per Pull Request
Continuity Rule, no new branch was created.

## 2026-04-22: Builder failure rolls task back to PENDING, not FAILED
FAILED state exists in RunState but using it requires deciding how to surface and
re-run failed tasks — deferred to a later step. Rolling back to PENDING is the
conservative safe choice: the job can be re-attempted cleanly without state repair.
original_job_state is captured before mutation so both task and job are fully restored.

## 2026-04-22: annotate_task_result raises RuntimeError on changed-without-artifact
Previously silently returned. A changed=True result with no matching artifact means
run_next_task has a bug. Silent no-op would hide it; raising makes the bug visible
immediately. The condition cannot occur in normal operation.

## 2026-04-22: annotate_planning_result finds artifact by name+task_id, not index 0
Index 0 was fragile — artifacts can accumulate from multiple calls or be reordered.
Finding by name="planning_output" and task_id=None is unambiguous. Kept as no-op if
not found (valid: job might have no planning artifact when annotation is called on a
partially-migrated job).

## 2026-04-22: TaskExecutionContext passed to builder (not a raw string)
Provides job context, planning summary, and prior task summaries to the builder.
Separating input context from Job prevents provider from mutating state. Small and
serializable (Pydantic model). Lives in orchestration/ so providers depend on it.

## 2026-04-22: task_type deduplication via _2/_3 suffix
Duplicate task_type values from LLM planners confuse downstream task selection.
Simple suffix append is localized to plan_job_with_llm, requires no schema change,
and is deterministic. Does not redesign the planner schema.

## 2026-04-19: Step 5 on new branch (feature/step5-task-execution)
Task execution has different purpose, review scope, and feature boundary from
Step 4 (planning/provider config). New branch created from main per AGENTS.md.
PR #5 merged before rebasing this branch.

## 2026-04-19: annotate_task_result finds artifact by task_id, not by index
Blindly using job.artifacts[-1] or job.artifacts[0] would break if a planning
artifact precedes the task artifact or artifacts accumulate across calls.
Finding by task_id == result.task_id is unambiguous and safe regardless of order.

## 2026-04-19: RunTaskResult.task_id is UUID | None (not opaque object)
Typed as UUID | None in the dataclass. task_id=None signals no-op (no task ran).
Caller can always check result.changed first before using task_id.

## 2026-04-18: Role-specific env vars with backward-compat fallback (Step 4.6)
REMEDY_OLLAMA_PLANNER_MODEL takes priority over REMEDY_OLLAMA_MODEL. The generic var is kept as a fallback so existing setups are not broken. Precedence: constructor arg > REMEDY_OLLAMA_PLANNER_MODEL > REMEDY_OLLAMA_MODEL > default. Same pattern will apply to future roles (executor, verifier).

## 2026-04-18: annotate_planning_result called in CLI, not inside plan_job_with_llm
Elapsed time must be measured around the call_planner invocation, which happens inside plan_job_with_llm. Passing elapsed_ms into plan_job_with_llm would mix orchestration and timing concerns. Measuring in the CLI and annotating after the call keeps the functions focused and keeps annotate_planning_result independently testable.

## 2026-04-18: temperature/num_predict passed as Ollama options only when set
Sending these only when the user has configured them preserves Ollama model defaults otherwise. An empty options dict would be harmless but is avoided for clarity.

## 2026-04-18: PlannerOutput lives in orchestration/, not in the provider
Orchestration imports PlannerOutput to perform the transformation. If PlannerOutput lived in the provider, orchestration would depend on the provider — inverting the correct dependency direction. All providers depend on orchestration/planner_models.py.

## 2026-04-18: plan_job_with_llm accepts a callable, not a provider object
Provider is injected as `call_planner: Callable[[str], PlannerOutput]`. No provider protocol or ABC needed yet. This keeps orchestration completely decoupled and makes testing trivial (pass a lambda). Can be formalised into a protocol if multiple providers need a shared interface in a later step.

## 2026-04-18: ollama is an optional dep, imported lazily inside OllamaPlanner.plan()
Core remedy must remain usable without Ollama installed. The lazy import with clear ImportError message makes the missing-dep case user-friendly. Importing the provider module itself is safe; only calling .plan() requires ollama.

## 2026-04-18: CLI imports plan_job_with_llm and OllamaPlanner inside the function
Deferred imports in _cmd_plan_job_local prevent ollama-related import errors when the CLI module is loaded. Follows the same pattern as the lazy provider import.

## 2026-04-18: acceptance_checks not mapped to Task.acceptance_checks yet
PlannerOutput.acceptance_checks is job-level, not task-level. Mapping them to individual Tasks would require a decision about which task owns which check — deferred to a later step. Currently preserved in artifact content and metadata.

## 2026-04-18: Step 4 on new branch (feature/step4-ollama-planner)
Real provider integration has a different purpose, review scope, and feature boundary from Step 3/3.5 (orchestration skeleton + semantics). New branch correct per AGENTS.md.

## 2026-04-18: PlanJobResult is a dataclass, not a Pydantic model
It is a return type, not a domain model — no serialization or validation needed. A dataclass is the minimal correct choice. If this type ever needs to be persisted or serialized, it should be promoted to a Pydantic model at that point.

## 2026-04-18: PLANNED state added to RunState
Distinct from PENDING: PENDING = no planning yet; PLANNED = tasks generated, awaiting execution. Step 3 previously reused PENDING after planning, which was semantically ambiguous. The new state makes the lifecycle unambiguous without adding new orchestration logic.

## 2026-04-18: Step 3.5 continues on feature/step3-orchestration-skeleton (PR #4)
Step 3.5 (planning semantics hardening) is in-scope for PR #4: same feature boundary (orchestration skeleton), same review scope, same merge intent. Per Pull Request Continuity Rule, no new branch was created.

## 2026-04-15: Use `typing.Protocol` for interfaces
Protocol-based interfaces (structural subtyping) require no inheritance, keeping core completely decoupled from providers. Any class matching the signature satisfies the contract.

## 2026-04-15: Provider directories are empty stubs
`packages/providers/claude_agent/`, `docker_runtime/`, `mempalace/` exist as empty packages with `__init__.py` only. No implementation until later steps to avoid scope drift.

## 2026-04-15: contracts/ imports from core/ models
Verifier and LLMWorker interfaces need AcceptanceCheck and Task/Artifact types. The contracts package is allowed to depend on core models — both are internal, zero external deps. The dependency flows one way: contracts → core.

## 2026-04-15: LLMWorker.execute takes Task, returns Artifact
Replacing prompt-centric generate(prompt: str) with execute(task: Task) -> Artifact enforces the artifact-driven architecture at the contract level. Raw strings are a provider concern, not an interface concern.

## 2026-04-15: LLMWorker.stream returns AsyncIterator[str]
Streaming full Artifact objects is a more complex problem deferred to a later step. str tokens are kept for now as a pragmatic compromise; this is documented.

## 2026-04-15: Artifact.content kept as str
Binary artifact support (str | bytes) is a non-trivial serialization question. Deferred to Step 2 or later. Documented as a known limitation.

## 2026-04-15: Task.output_artifact_ids is list[UUID]
Task references artifact IDs, not embedded Artifact objects, to avoid circular model issues and keep the models flat.

## 2026-04-15: Step 3 on new branch (feature/step3-orchestration-skeleton)
Step 3 (orchestration logic) is clearly unrelated to Step 2/2.5 (packaging + CLI). PR #3 was merged before creating the new branch, per AGENTS.md starting-a-new-feature workflow.

## 2026-04-15: plan_job mutates Job in place
Pydantic v2 models are mutable by default. Mutation + return avoids deep-copy complexity and is consistent with how the CLI uses the result (save_job after plan_job). The function signature returns Job to make the behavior explicit.

## 2026-04-15: Idempotency guard checks tasks OR artifacts
If either is non-empty, planning is skipped entirely. This is strict but safe — prevents partial re-planning. A partially-planned job (tasks but no artifact) would be unusual and is better fixed manually.

## 2026-04-15: Job state is PENDING after planning (not a new state)
After plan_job, the job returns to PENDING. This represents "has tasks, awaiting execution". RunState values are not extended in Step 3 — the available states are sufficient for now. A PLANNED state could be added in a later step if needed.

## 2026-04-15: Step 2.5 continues on feature/step2-packaging-cli (PR #3)
Step 2.5 (storage + CLI hardening) is an in-scope extension of Step 2 (same feature boundary). Per the Pull Request Continuity Rule, continued on the existing branch and PR rather than creating a new one.

## 2026-04-15: Step 2 on new branch (feature/step2-packaging-cli)
Step 2 (packaging + CLI) has a distinct purpose, merge scope, and feature boundary from Step 1.5 (contracts hardening). New branch is correct per AGENTS.md "clearly unrelated" criteria.

## 2026-04-15: hatchling as build backend
Minimal, modern, zero-config for simple package layouts. `packages = ["packages", "apps"]` exposes both top-level dirs as importable packages.

## 2026-04-15: Storage is repo-root-relative (not CWD-relative)
_resolve_data_dir() uses Path(__file__).resolve() to find the repo root, avoiding CWD fragility. REMEDY_DATA_DIR env var overrides for non-standard setups.

## 2026-04-15: list_jobs silently skips corrupted files
Corrupted JSON files are skipped without raising. Acceptable for local dev tool; can be hardened to warn/error in a later step.

## 2026-04-15: Storage was CWD-relative (superseded)
.data/jobs/ is relative to the working directory where the CLI is invoked. Simple and deterministic for single-user local use. No config system yet.

## 2026-04-15: Job.user_prompt field added
CLI requires a prompt field on Job to persist the user's input. Added as str | None = None — pure data, no orchestration logic.
