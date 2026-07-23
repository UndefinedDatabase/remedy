# Decisions

/review-remedy command added — reviewer bootstraps review rounds from disk, operator no longer relays completion reports

## 2026-07-23: Config template lives in init_cmd.py, written before registry (F081 T002)
`_CORE_TEMPLATE`, `_RUNTIME_ACTIVE`, `_RUNTIME_SKIP` are module-level string constants
in `apps/cli/commands/init_cmd.py`. Config file is written BEFORE project registry so
that a registry failure still leaves a valid `remedy.toml`. Handler reports each step
as `[created|exists|skipped]` with no early return. Runtime detection calls
`detect_runtimes(root)` from `packages/runtimes/runtime_config.py` — exactly 1 result
fills `[runtime]`, 0 or >1 produces commented-out section + `[skipped]` message.

## 2026-07-23: Runtime table written to .remedy/config.toml, not remedy.toml (R-0080)
Two config systems exist: `config.py` reads `remedy.toml` `[remedy]` table only;
`runtime_config.py` reads `.remedy/config.toml` `[runtime]` section. init now writes
each table to the file its loader reads: `[remedy]` → `remedy.toml`, `[runtime]` →
`.remedy/config.toml`. On no-marker repos, `.remedy/config.toml` gets the commented
`[runtime]` example (not omitted) so users have a template to fill in. `.remedy/` is
the project config directory, NOT the data root (which is do-not-touch).

## 2026-07-23: `remedy init` uses the _DEFAULT_COMMAND pattern (F081)
No top-level command pattern exists in the CLI. `remedy init` is implemented
as group "init" with subcommand "run", and `_DEFAULT_COMMAND["init"] = "run"`
in grouped.py so `remedy init --project-name foo` auto-maps to
`remedy init run --project-name foo`. Matches the existing `do`/`ui` pattern.

## 2026-07-23: /build-remedy is a command, not a skill
A command fires only on explicit `/build-remedy` invocation. A skill description
could auto-trigger from the agent's skill-matching heuristic — deliberately
avoided. The command bootstraps Window 1 (planner/reviewer) from
docs/agents/planner_reviewer_prompt.md.

## 2026-07-23: Legacy remedy-reviewer.md subagent deleted
Superseded by split_workflow.md Window 1. The subagent from the retired
parallel-review system risked a conflicting reviewer path. Git history
preserves it.

## 2026-07-23: Legacy parallel-reviewer artifacts deleted; reviewer is fully read-only
self_run_goal_*.md, job_workflow_readiness.md, post_apply_smoke_5361.md deleted.
These were superseded by docs/agents/split_workflow.md which codifies the
two-window lifecycle. The reviewer (Window 1) is now fully read-only by
design; all writes are authored by the reviewer and applied verbatim by the
worker (Window 2). Git history preserves the legacy files.

## 2026-07-23: R4 test count discrepancy — documentation error, not test deletion (Phase 1)
Handoff docs (.agent/context.md, .agent/live_review.md) claimed 499 tests green
(95 in test_project_resolution.py, 13 in test_f146_package_pipeline_e2e.py).
Evidence run produced 495 (93 resolution, 11 f146_e2e). Investigation confirmed
the committed test files always had 93 and 11 test methods — git log and method
counts prove no tests were ever deleted. The 95/13 numbers were never real;
they were documentation errors in .agent/ state files. Corrected to verified
actuals: 93 + 11 = 104 (was claimed 95 + 13 = 108), total 495 (was 499).
Evidence ZIP (remedy-review-20260723-141827-READY_FOR_REVIEW.zip) generated with
correct 495 count. Commits: all R4 production code unchanged.

## 2026-06-13: UI `npm run lint` is pre-existing broken; rely on typecheck/vitest/build (Block 1180-1192)
`apps/ui/eslint.config.js` (unchanged since the Steps 172-201 UI rebuild) registers no
TypeScript parser, so eslint parses every `.ts/.tsx` with espree and fails with parse errors
on ALL files — including untouched legacy ones. `@typescript-eslint` is not installed.
This block forbids new dependencies, so the proper fix (add the TS parser/plugin) is out of
scope. Quality gates used instead: `npm run typecheck` (tsc), `npm run test:unit` (vitest),
`npm run build` (vite). Lint remains a pre-existing repo blocker, documented for a future
dedicated branch.

## 2026-05-05: Project Constitution v1 is read-only extraction, not enforcement (Step 21)
Constitution extracts policy signals from known project files using purely lexical matching.
No subprocess, no eval, no recursive scan, no secrets. It is not consulted by task execution
in v1 — it is a structured metadata layer for future Context Inspector, Verifier Marketplace,
MCP Quarantine, Autonomy Modes, and Memory/MemPalace. The optional constitution parameter
was added to summarize_cockpit and summarize_trust_report rather than loading inside those
functions, to keep them pure and testable without a live repo.

## 2026-05-05: Trust Report v1 is read-only and text-first (Step 20)
Trust Report assembles evidence across Job JSON, Artifact metadata, JSONL run logs,
Permissions, and Approval Queue into one auditable plain-text document. It is intentionally
read-only with no apply/autonomy behavior. The design prepares for future Replay, Live
Cockpit, MemPalace, and MCP Quarantine reports by establishing a clean summary contract
(what was requested / planned / run / created / verified / decided / NOT done) without
coupling to any execution-side behavior. Redaction policy is inherited from run-log
contract: no raw exception text, no raw artifact content, no full diff text.

## 2026-05-05: v1 intent IDs are index-based; patch_intent_explanations must be stable (Step 19.1)
Intent IDs encode the 0-based index into artifact.metadata["patch_intent_explanations"].
This is simple and stable for v1 (intents are generated once per task run, never reordered).
Builders must treat patch_intent_explanations as append-only after creation — reordering
would misalign existing approval decisions with the wrong intents. This is documented as
an explicit invariant in architecture.md. Future multi-intent or regenerated-intent workflows
must move to content-hash-based stable IDs (e.g. SHA256 of target_path + action + intent).

## 2026-05-05: Approval states: latest decision wins (Step 19)
Approving a rejected intent (or vice versa) overwrites the stored state. No "un-decide"
operation exists. This is safe for v1 because no apply step exists — no state is
irrecoverable. The policy is documented in the CLI help text and module docstring.

## 2026-05-05: Approval raw reason text NOT logged to run log (Step 19)
The user-supplied --reason text is stored in artifact.metadata["patch_intent_approvals"]
but never written to run log events. Run logs record reason_present=True|False only.
This matches the general redaction policy: user-supplied strings may contain sensitive text.

## 2026-05-05: Intent ID format "<artifact_short_id>-<idx>" (Step 19)
Intent IDs use the first 8 hex chars of the artifact UUID + 0-based index into the
patch_intent_explanations list. rfind("-") is used to parse — robust against the 8-char
hex portion potentially containing no dashes (since it's hex, it won't, but defensive code).
Index-based v1 chosen over hash-based: simpler, stable, human-readable in the CLI.

## 2026-05-04: interrupted run → can_auto_continue=False (Step 18.1)
An interrupted run (task_run_started with no terminal event) causes _can_auto_continue to
return (False, "interrupted run detected — inspect timeline before continuing"). Previously
it returned True. The boolean must be conservative: a future autonomy controller must never
treat interrupted=True as a green light to continue. The Next best action section still guides
the human to inspect the timeline and then resume manually — human guidance is preserved,
machine-readable signal is conservative.

## 2026-05-04: repo_generated_write attention item fires only on explicit denial (Step 18)
repo_generated_write defaults to False (opt-in). The cockpit attention item
("Repo writes are denied — allow with: remedy set-permission …") should NOT fire
just because the permission hasn't been granted — that is the expected initial state for
most jobs. It fires only when the user has explicitly called set_permission(..., allow=False).
Detection: check job.metadata.get("permissions", {}).get("repo_generated_write") == "deny".

## 2026-05-04: Cockpit reuses load_run_events from timeline.py (Step 18)
Both views read the same JSONL files. Sharing load_run_events avoids duplicating the
file-reading logic. The CLI calls load_run_events once and passes events to
summarize_cockpit. This is the same "load once, render separately" pattern as timeline.

## 2026-05-04: Cockpit signal extraction: one pass for interrupts, second pass for last events (Step 18)
_extract_signals does two forward passes over the event list. The first detects interrupted
runs (task_run_started without a terminal event). The second collects the last occurrence
of each relevant event type. Two passes are clearer than interleaving the two accumulation
patterns. Events are short — no performance concern.

## 2026-05-03: ValidationError must be caught before ValueError in exception handlers (Step 17.1)
In Pydantic v2, `pydantic.ValidationError` inherits from `ValueError`. If `except ValueError`
appears first, it silently swallows `ValidationError` and the `except ValidationError` block is
dead code. Fix: reorder so `except ValidationError` precedes `except ValueError`, with inline
comment. This was the original Step 16.1 fix — re-applied after merge loss.

## 2026-05-03: planning_failed uses fixed message + error_category, never str(exc) (Step 17.1)
Raw exception messages may contain server URLs, tokens, connection strings, or other sensitive
text. Logging `message=str(exc)` violates the run-log redaction policy. Fix: always log
`message="planning failed"` (stable, safe) and `metadata.error_category=type(exc).__name__`.
The Timeline renderer reads only `error_category`; never renders `message` as diagnostic text.

## 2026-05-03: _fail() closure in _cmd_run_next_task_local (Step 17.1)
A local `_fail(outcome, **meta)` helper closes over `log`, `pending_task`, and `pending_task_type`
to emit `task_run_failed` from any of the 5 early-exit paths without repeating the full log.log()
call. Preserves the terminal-event invariant without code duplication.

## 2026-05-03: Timeline uses sequential event processing with task-block accumulation (Step 17)
Events are processed in timestamp order. When task_run_started is seen, a "task block"
is opened and subsequent events are accumulated until a terminal event (task_run_completed,
task_run_failed, task_run_noop). The block is then rendered as a compact multi-line summary.
Events outside a task block are rendered individually. This matches the natural event structure
without requiring a pre-grouping pass and handles multiple retries of the same task_id naturally.

## 2026-05-03: load_run_events takes data_dir (parent of runs/) not runs_root (Step 17)
`data_dir` maps to REMEDY_DATA_DIR — the same value used by storage.py and workspace.py.
`load_run_events` appends `runs/<job_id>/` internally. The CLI resolves data_dir from the
REMEDY_DATA_DIR env var or the repo-local default, matching run_log.py's resolution order.

## 2026-05-03: summarize_timeline is pure — events pre-loaded by caller (Step 17)
Separating load from render makes summarize_timeline trivially testable (pass crafted dicts).
The CLI loads events and passes them in. This also allows future callers (web server, TUI) to
load events differently without changing the renderer.

## 2026-05-03: Unknown events render as "○ <name>" rather than being silenced or crashing (Step 17)
Silencing unknown events would hide bugs and make logs harder to diagnose. Crashing would
break the timeline on log format evolution. Rendering with the INFO symbol is honest: the
event is present and acknowledged; its semantics are just not yet implemented in the renderer.

## 2026-05-03: Run Logs v1 — one JSONL file per CLI invocation (Step 16)
Each CLI invocation creates a RunLogWriter with a fresh run_id (UUID4 hex). All events
from that invocation share the same run_id, forming a chronological session trail.
Multiple invocations for the same job produce separate files under <job_id>/: history
accumulates across retries without overwriting earlier sessions. Enables resume,
diagnostics, and future cockpit/timeline UX without a database.

## 2026-05-03: Redaction policy: no full content or prompts in run logs (Step 16)
Run logs store only IDs, counts, outcomes, metadata labels (task_type, model, risk levels,
verifier profile, check names). Full artifact content, prompts, workspace file contents,
and diff previews are excluded. The authoritative full content lives in job artifacts and
workspace files; the run log is the lightweight observability layer only.

## 2026-05-03: log= appended to CLI output for plan-job-local and run-next-task-local (Step 16)
The log path is appended to the existing summary output line (two spaces before "log=")
for both commands, including the noop case. create-job does not print log= because its
stdout is machine-parsed (bare job UUID); adding log= would break scripts that capture it.

## 2026-05-03: RunLogWriter creates the job directory eagerly, file is created on first write (Step 16)
mkdir in __init__; file created on first append(). If a command exits before writing any
events (e.g. workspace_write denial happens before any log.log() calls), no JSONL file is
produced but the directory exists. This is intentional — the directory is cheap and the
denial case is covered by the permission error output, not the run log.

## 2026-05-02: Verifier Profiles v1 checks run inside workspace block, after check 6 (Step 15)
Profile-driven checks (required_sections, min_proposed_changes, forbidden_phrases) are
placed inside the `if contract.require_workspace_file:` block in verify_task_output,
after workspace file is confirmed present and non-empty (but not gated on require_proposed_changes).
This means they are skipped if workspace file is missing or empty — both of which are
hard infrastructure failures where semantic content checks are irrelevant. Profile checks
read artifact.content, not the workspace file. All four check types run unconditionally
once the workspace gate passes; no early returns within profile checks.

## 2026-05-02: Profile verifier_profile field added to _ROUTE_RULES 4-tuple (Step 15)
_ROUTE_RULES changed from list[tuple[str, str, str | None]] to list[tuple[str, str, str | None, str]].
The fourth element is the verifier_profile name. get_task_type_spec and iter_task_type_specs
now read it from the rule. is_known_task_type uses `kw, _, _, _` unpacking.
All three callers (task_registry, test_task_registry, test_patch_intent) updated.
Single source of truth: routing and profile are co-located in the same rule entry.

## 2026-05-02: generic profile fallback is permissive by design (Step 15)
Unknown task types (and None profile names) fall back to the generic profile, which has
no forbidden_phrases and min_proposed_changes=1. This ensures no new verification failures
are introduced for task types that were passing before Step 15. The profile escalation is
intentional and conservative: unknown → generic, not unknown → strictest.

## 2026-04-28: Step 11 uses a structured preview block, not unified_diff
A real unified_diff was considered but rejected: artifact proposed changes are
bullet-point descriptions of changes, not actual file content. Diffing them against
the current file would produce a misleading all-removal + all-addition diff.
The structured block (header + existing context + labeled additions) is honest
about what it is — a proposal preview, not a diff from current to new state.

## 2026-04-28: PatchDryRunResult is a dataclass, not a Pydantic model
It is a transient, in-memory object used only for CLI output and compact metadata
storage. Pydantic overhead and serialization coupling are not needed. The CLI
converts it to a plain dict before storing in artifact.metadata.

## 2026-04-28: dry_run_block computed inside if vr.passed block, printed after save_job
Storing the formatted string (not a function reference) avoids a second late import
after save_job. The explanation is printed immediately after the main summary line
so the user sees it in context with the job/task summary.

## 2026-04-28: artifact_content extraction mirrors task_runner logic but stays local
_extract_proposed_lines in patch_intent.py duplicates the section-boundary logic
from task_runner._extract_proposed_changes. This is intentional — importing private
helpers across modules creates invisible coupling. Both copies are small and the
comment in patch_intent.py documents the parallel.

## 2026-04-28: Step 10.9 continues on feature/step10-patch-intent (PR #10)
Minor hygiene pass before Step 11 (patch apply). Same branch and PR. No new tests,
no behavior changes — comments and one additional assertion only.

## 2026-04-28: KEEP IN SYNC comments include the exact test file path
"enforced by TestKeywordSync in tests/test_patch_intent.py" removes all ambiguity
for a developer editing either rule table without first checking the test suite.

## 2026-04-28: private-import comment added to all three TestKeywordSync test methods
Each test method imports _INTENT_RULES and _REPO_PATH_RULES directly. The comment
explains that this is intentional (testing the contract) rather than accidental.

## 2026-04-28: Step 10.8 continues on feature/step10-patch-intent (PR #10)
Post-failure state accuracy and sync hardening are final refinements of the
Patch Intent v1 reliability work. Same branch and PR.

## 2026-04-28: verifier-failure test uses real finalize_task
The prior version mocked finalize_task as a no-op, leaving the task lifecycle
untested. Using the real finalize_task confirms both behaviors together: patch
intent is skipped (vr.passed=False) AND the task correctly rolls back to PENDING.
All finalize_task invariants are satisfied by the test setup (task.output_artifact_ids
is populated, artifact is in job.artifacts, task.status is RUNNING).

## 2026-04-28: KEEP IN SYNC comments are placed at the definition site
Both rule tables now carry a KEEP IN SYNC comment pointing to the other table.
This makes the contract visible to anyone editing either file, regardless of
whether they remember to check the test suite first.

## 2026-04-28: Step 10.7 continues on feature/step10-patch-intent (PR #10)
Template mapping sync and verifier-failure skip coverage are final reliability
checks for Patch Intent v1. Same branch and PR as Steps 10–10.6.

## 2026-04-28: keyword→template mapping must be identical between both tables
Two tables can have identical keyword sets and identical ordering but still route
a given task type to different paths if a template string differs. The mapping
test (test_intent_rules_and_repo_rules_full_mapping_matches) catches this by
comparing {keyword: template} dicts directly.

## 2026-04-28: verifier-failure skip is tested via assert_not_called
The `if vr.passed:` guard prevents any patch intent code from running on verifier
failure. The test patches derive_patch_intents and verify_patch_intent_set as
named mocks and calls assert_not_called() on both after the CLI function returns.
This is an explicit behavioral contract, not just an absence of metadata keys.

## 2026-04-28: Step 10.6 continues on feature/step10-patch-intent (PR #10)
Rule ordering and CLI coverage hotfix is an in-scope refinement of Step 10.5.
Same purpose (patch intent reliability), same PR. No new branch.

## 2026-04-28: Keyword ordering is part of the rule-table contract
Both _INTENT_RULES and _REPO_PATH_RULES are first-match-wins. A keyword promoted
or demoted in one table but not the other silently changes routing semantics.
The ordering test (test_intent_rules_and_repo_rules_keyword_order_matches) uses a
direct list comparison — simple, deterministic, failure message is clear.

## 2026-04-28: CLI-level patch intent test uses module-attribute patching
_cmd_run_next_task_local uses late `from X import Y` imports for all heavy
dependencies. Patching the module attributes (e.g. packages.orchestration.
patch_intent.verify_patch_intent_set) intercepts the lookup at import time inside
the function — no need to patch at the apps.cli.main namespace. Only
verify_patch_intent_set is mocked to inject errors; derive_patch_intents runs
normally so the full patch-intent derivation path is exercised.

## 2026-04-28: Step 10.5 continues on feature/step10-patch-intent (PR #10)
Reliability hotfix is an in-scope refinement of Patch Intent v1 (Step 10). Same
purpose (patch intent observability and guard hardening), same PR. No new branch.

## 2026-04-28: derive_patch_intents raises RuntimeError (not ValueError) for invariant violations
task_id=None and artifact.id=None are programming errors (invariant violations), not
user-input errors. RuntimeError is the correct signal for internal invariant failures.
ValueError is reserved for user-facing or schema-level validation. Both guards added.

## 2026-04-28: Patch intent verification errors are non-fatal (warn + record)
Turning verify_patch_intent_set failures into hard task failures would require a new
exit code or a new failure mode in the existing task contract system. Since patch
intents are proposals only (never applied), a non-fatal warning + metadata record is
the correct conservative position. This preserves the existing task completion model.

## 2026-04-28: patch_intent_errors recorded in artifact.metadata (not logged only)
Recording errors in metadata makes them auditable in job JSON (show-job), consistent
with how verification_failures is recorded on task artifacts. CLI stderr warning is an
operator signal; metadata is the durable record.

## 2026-04-28: Keyword sync enforced by test, not by shared module
The keyword sets in _INTENT_RULES and _REPO_PATH_RULES are identical today. A shared
module is not needed yet — the two tables serve different purposes (workspace patch
proposals vs. repo file writes) and may diverge intentionally in a future step.
A focused sync test (TestKeywordSync) is the smallest reliable change and will catch
any accidental divergence at test time.

## 2026-04-28: Null-byte check uses `continue` after recording error
After detecting a null byte, further checks on the same path (absolute check, traversal
check, .md check) are unreliable because the path itself is malformed. Short-circuiting
with `continue` is consistent with the empty-path guard above it.

## 2026-04-27: Step 10 on new branch feature/step10-patch-intent
Patch Intent v1 has a clearly different purpose (structured change proposals), review scope,
and feature boundary from the permission model (Steps 9–9.6). New branch from main is correct.

## 2026-04-27: Patch intent derivation uses task_type keyword match only (not free-form LLM text)
Raw LLM strings can contain arbitrary path references. Keying derivation on task_type —
using the same conservative keyword table as repo_applicator — ensures the target_path is
always predictable and never injected from model output. This is intentionally limiting;
future steps can expand derivation safely with more explicit input handling.

## 2026-04-27: PatchIntentSet can be empty; no file written when intents is empty
Most task types do not match documentation keywords (e.g. "write_tests", "implement_feature").
An empty PatchIntentSet is valid and expected. No workspace file is written in that case.
patch_intent_count and patch_intent_file are not set in artifact metadata if no intents.

## 2026-04-27: verify_patch_intent_set is a pure function returning list[str] (not VerificationResult)
Keeping it separate from the existing VerificationResult/TaskContract hierarchy avoids
coupling patch intent verification to the Task Contract v1 system. A simple list of error
strings is sufficient and testable in isolation. Integration into VerificationResult is
deferred to a later step if needed.

## 2026-04-27: Patch intents derived only when vr.passed
Deriving intents from a failed task execution risks capturing incomplete/wrong output.
Tying derivation to verification-passed ensures intents represent only confirmed builder output.

## 2026-04-27: no-pending-tasks early check added before workspace_write guard
workspace_write denial should only block actual work. If there are no pending tasks, the
job is complete (or was never planned) and should exit(0) cleanly regardless of permissions.
Fix: check any(t.status==PENDING) before the workspace_write guard.

## 2026-04-27: mf dead branch removed (file_info always set after Step 9.6)
After Step 9.6, mf is always a MaterializedFile when we reach the output line:
- result.changed=True (returned early if False)
- workspace_write confirmed (exited early if denied)
- materialize_task_output returns None only when result.changed=False
The `if mf is not None else ""` guard is genuinely dead code; simplifying it.

## 2026-04-27: Step 9.6 continues on feature/step9-permission-model (PR Continuity Rule)
Enforcement ordering fix is a correctness fix for the workspace_write gate introduced
in Step 9.5. Same purpose (permission model), same PR (#9). No new branch.

## 2026-04-27: workspace_write check moved before builder instantiation (not after)
Step 9.5 placed the check after run_next_task returned, wasting an LLM call when denied.
The fix: check immediately before `start = time.monotonic()` (after imports, before
OllamaBuilder() is instantiated). Denial exits non-zero with no state mutation.
The late materialization conditional is removed — check has already passed by that point.

## 2026-04-27: show-permissions labels ALL capabilities ([active] and [reserved])
Asymmetric labeling (reserved gets a label, active gets nothing) was confusing — users
couldn't easily distinguish active from unlabeled. Adding [active] to all rows makes
the status column consistent and self-explanatory.

## 2026-04-27: Step 9.5 continues on feature/step9-permission-model (PR Continuity Rule)
Permission model honesty / CLI UX hotfix is a direct in-scope refinement of Step 9.
Same purpose (permission model), same review scope, same PR (#9). No new branch.

## 2026-04-27: workspace_write is enforced in the CLI, not in task_runner.py
The gate is a single conditional in _cmd_run_next_task_local before materialize_task_output.
Enforcing inside task_runner.py would require adding a Job parameter to materialize_task_output
(signature change, more invasive). CLI-level gate is sufficient: if denied, mf=None,
verifier fails on workspace_file_in_metadata, task rolls back to PENDING. This is honest.

## 2026-04-27: Reserved capabilities print a CLI notice; they are not blocked from being set
Preventing set-permission for reserved capabilities would require extra validation that serves
no safety purpose (setting them is harmless since no code path checks them). Persisting the
setting with a notice is user-friendly and preserves future compatibility when the capability
becomes active — the user's grant will take effect automatically.

## 2026-04-27: show-permissions is a dedicated CLI command (not buried in show-job JSON)
show-job dumps raw job JSON — useful for debugging but verbose and requires jq/parsing to
extract permissions. A dedicated show-permissions command is one line per capability and
labeled clearly. Minimal code, maximum clarity.

## 2026-04-27: effective_permissions() is a pure helper in permissions.py
No storage access, no CLI dependency. Takes job (already loaded by caller), returns list of
dicts. Testable in isolation. The CLI formats and prints; permissions.py owns the logic.

## 2026-04-25: Step 9 on new branch feature/step9-permission-model
Permission model is clearly unrelated to repo attachment/applicator (different purpose,
review scope, merge intent). All Step 8.x work is merged to main. New branch correct.

## 2026-04-25: Capability as str, Enum — Capability("foo") raises ValueError
Using str, Enum makes capability values self-documenting strings and makes invalid
values fail at construction time. The CLI catches the ValueError and prints a clear
error with the valid capability list.

## 2026-04-25: workspace_write is allowed by default
workspace_write is always needed for local task execution; requiring explicit opt-in
would break the existing flow and add friction with no security benefit in the current
local-only model. All other capabilities default to deny.

## 2026-04-25: check_and_apply_to_repo lives in repo_applicator.py, not permissions.py
It combines permission checking with repo application logic and must import from both
modules. Placing it in repo_applicator (which already imports Artifact and Path) is
cleaner than importing repo_applicator logic into permissions.py or creating a third
module for a single function. No circular import: permissions.py imports Job via
TYPE_CHECKING only; repo_applicator.py imports permissions at function call time.

## 2026-04-25: check_and_apply_to_repo mutates artifact.metadata on denial
Recording repo_application_skipped_reason directly on the artifact is consistent with
how verification_failures and verification_passed are recorded (finalize_task). The
artifact is the authoritative record of what happened during task execution. The caller
(CLI) persists the job after this call, which saves the annotation.

## 2026-04-25: repo_overwrite and shell_exec are defined but unused in Step 9
They exist to make the capability namespace stable and to allow CLI experimentation.
Granting them has no effect because no code path checks them yet. This is intentional
and documented. Preventing them from being set would require extra validation that
serves no safety purpose in the current implementation.

## 2026-04-25: Step 8.6 continues on feature/step8-repo-attachment (PR Continuity Rule)
Routing and boundary hotfix is an in-scope correctness fix for the repo applicator
introduced in Step 8. Same branch, same PR.

## 2026-04-25: _REPO_PATH_RULES: docs/remedy/ keywords moved before plain docs/ keywords
Substring match on "doc" would match compound types like "spec_document" before "spec"
got a chance to match. Fix: evaluate all docs/remedy/ entries first. readme stays first
as a special case. Within each group, "documentation" appears before "doc" since "doc"
is a substring of "documentation". Order is now explicit and documented with comments.

## 2026-04-25: _write_to_repo resolves repo_root internally before boundary comparison
target = (repo_root / path).resolve() produces a real absolute path. Comparing it to
an unresolved repo_root (e.g. a symlink) with is_relative_to() would always return False
even for legitimately in-bounds paths. Resolving repo_root inside _write_to_repo makes
the boundary check self-contained — callers no longer need to pre-resolve.

## 2026-04-25: Stale-path guard added to apply_task_output_to_repo (return [])
Moved from CLI-only to the function itself. Benefit: the guard is now testable directly
without invoking the full CLI+Ollama stack. The CLI's explicit re-validation + warning
is retained as defense in depth (user-visible stderr signal); the function-level guard
prevents silent filesystem writes if the CLI guard is somehow bypassed.

## 2026-04-25: Step 8.5 continues on feature/step8-repo-attachment (PR Continuity Rule)
Rule hardening is an in-scope refinement of the repo applicator introduced in Step 8.
Same branch, same PR. No new branch created.

## 2026-04-25: Removed 5 broad keywords from _REPO_PATH_RULES
Removed: implementation, prepare, define, summarize, summary.
These all match task types that produce code or non-doc output (e.g. write_implementation,
define_api_endpoint, prepare_data_migration). The false-positive risk outweighs any benefit.
Added changelog and guide as clearly documentation-oriented replacements.

## 2026-04-25: Stale repo path check lives in the CLI, not in repo_applicator.py
The re-validation (exists + is_dir) before calling apply_task_output_to_repo is in the CLI.
Reason: repo_applicator.py has no concept of "attached repo" — it just writes to a path.
The CLI is the caller responsible for policy decisions (warn vs fail vs skip). Putting it
there keeps apply_task_output_to_repo a pure boundary-safe writer with no policy.

## 2026-04-25: Stale repo path → warn + skip, never fail task completion
Task completion is defined by workspace verification, not repo application (established
in Step 8). A stale repo path is a user-environment issue, not a task failure. The CLI
prints a warning to stderr and skips the repo write; the task is still marked COMPLETED.

## 2026-04-24: Step 8 branches from feature/step6-workspace-runtime (not main)
Step 8 depends on workspace runtime, verifier gate, and diagnostic semantics introduced
in Steps 6–7.6 which are not yet merged to main (PR #7 open). Branching from main would
miss those changes entirely. Branched from feature/step6-workspace-runtime to form a PR
chain. This is documented as a necessary exception to the "branch from main" default.

## 2026-04-24: repo_applicator uses keyword matching on task_type (not exact match)
task_type values come from LLM output and are not guaranteed to match exact strings. A
keyword substring match (case-insensitive) against a static table is inspectable, fast,
and does not require config. Each entry maps a keyword to a path template. First match
wins; order is from most-specific to least-specific keyword.

## 2026-04-24: No overwriting existing repo files in Step 8
The conservative rule: if the target path exists, skip silently and return []. This
prevents Remedy from accidentally clobbering user-edited docs on retry. A future
permission-gated step can relax this for explicitly approved paths.

## 2026-04-24: Repo application is workspace-only fallback (not a failure condition)
If no repo is attached, or the task type is ineligible, or the target file already
exists, run-next-task-local continues without error. Repo application is opportunistic —
task completion is defined by workspace verification only, not by repo writes.

## 2026-04-24: _sanitize_path_component duplicated in repo_applicator.py
The same sanitization regex appears in both task_runner.py and repo_applicator.py. The
function is tiny (3 lines) and importing a private helper across modules is worse style
than a local copy. If this pattern grows, extract it to a shared utility in a later step.

## 2026-04-24: repo_applicator content is section-aware (excludes Notes and Risks)
Uses the same section-header state machine as _extract_proposed_changes in task_runner.py.
Notes and Risks appear in artifact.content with the same "  - " prefix as proposed
changes; section-aware extraction is the only correct approach.

## 2026-04-24: finalize_task carry-in: raise RuntimeError on invariant violations
Two invariant violations in the failure branch that were previously silent are now
explicit RuntimeErrors: (1) empty output_artifact_ids before clear, (2) artifact ID
captured but not found in job.artifacts. Both represent bugs in run_next_task. Silent
skip would hide the bug; raising makes it visible immediately. The conditions cannot
occur in normal operation.

## 2026-04-24: finalize_task captures artifact ID before clearing output_artifact_ids
The failure branch in finalize_task previously scanned job.artifacts by task_id after
clearing output_artifact_ids. Because multiple failed artifacts can accumulate in
job.artifacts with the same task_id, the scan would find the first (stale) artifact
instead of the current attempt's artifact. Fix: capture output_artifact_ids[0] before
clear(), then look up by artifact ID (not task_id). This ensures failure metadata
(verification_passed, verification_failures) is always annotated on the current attempt's
artifact, not a stale earlier one.

## 2026-04-24: Step 7.6 continues on feature/step6-workspace-runtime (PR #7)
Diagnostic artifact fix is a correctness fix for the verifier gate introduced in Step 7.
Per Pull Request Continuity Rule, no new branch.

## 2026-04-24: Step 7.5 continues on feature/step6-workspace-runtime (PR #7)
Retry semantics hotfix is clearly in-scope for the same PR — it is a correctness fix
for the verifier gate introduced in Step 7. Per Pull Request Continuity Rule, no new branch.

## 2026-04-24: materialize_task_output uses task.output_artifact_ids[0] not task_id scan
The previous implementation found the artifact by scanning job.artifacts for the first
entry with matching task_id. After a failed verification + retry, the stale failed
artifact sits earlier in job.artifacts and would be found first, causing materialization
to write to the wrong artifact object. The fix: locate artifact via
task.output_artifact_ids[0] (always the current attempt's artifact after finalize_task
has cleared the list on failure). This also removes the separate task_index lookup —
both task_obj and task_index come from one pass over job.tasks.

## 2026-04-24: finalize_task clears task.output_artifact_ids on verification failure
Failed artifact IDs must not persist in task.output_artifact_ids after rollback. If they
did, the next run_next_task would append the new artifact ID but the verifier would still
check index [0] (the stale one). Clearing on failure means [0] always refers to the
most recent attempt. The failed artifact stays in job.artifacts for diagnostics; it is
simply no longer reachable from the task.

## 2026-04-24: CLI exits with code 1 on verification failure
Matches the existing CLI discipline: non-zero exit for any failure that should stop
automation pipelines. save_job is called before sys.exit(1) so the rolled-back state
is persisted (task=PENDING, failure metadata in artifact) before the process terminates.

## 2026-04-24: Step 7 continues on feature/step6-workspace-runtime (PR #7)
Step 7 (verifier gate) is in-scope for the same PR. The workspace runtime branch
encompasses: workspace creation, materialization hardening, runtime boundary safety, and
now the verifier gate. All are part of the same "safe task execution" feature progression.
Per Pull Request Continuity Rule, no new branch.

## 2026-04-24: verify_task_output is pure; finalize_task handles mutation
Separating the pure check from the state mutation makes verify_task_output testable
in isolation and composable — callers can inspect the VerificationResult before deciding
whether to finalize. This mirrors the annotate_* pattern established in Step 5.5.

## 2026-04-24: No FAILED task state in Step 7
Verification failure rolls the task back to PENDING rather than introducing a FAILED state.
Reasons: keeps the state machine simple; PENDING tasks are retryable without extra tooling;
FAILED would require additional handling in the CLI and sequencing logic. FAILED can be
introduced in a later step if retry exhaustion or terminal failure semantics are needed.

## 2026-04-24: TaskContract Pydantic model — all flags True by default
Step 7 always runs all checks. The model exists to name the concept and reserve space for
per-task contract customization (e.g. skip workspace checks for tasks that don't materialize).
Using a Pydantic model rather than a bool parameter keeps the interface stable as new checks
are added.

## 2026-04-24: test_context_includes_prior_task_summaries rewritten to set state directly
With the verifier gate, tasks stay RUNNING after run_next_task — they no longer appear as
"prior completed tasks". The test was rewritten to manually set tasks 0 and 1 to COMPLETED
with artifacts, isolating _build_execution_context from the full execution+verification flow.
This is cleaner and more focused on what the test actually verifies.

## 2026-04-23: Step 6.7 continues on feature/step6-workspace-runtime (PR #7)
Runtime boundary hardening and final schema fixes are in-scope for PR #7 — same feature
boundary (workspace runtime, materialization). Per Pull Request Continuity Rule, no new branch.

## 2026-04-23: Workspace boundary check lives in runtime.write(), not only in callers
_sanitize_path_component in task_runner.py removes traversal before forming relative_path,
but callers could bypass it or a future caller could skip it entirely. Enforcing the check
inside write() makes the runtime a safe boundary regardless of call site. Uses resolve() +
is_relative_to() — two standard library calls, no sandbox framework.

## 2026-04-23: Root stored as resolved Path in LocalWorkspaceRuntime.__init__
Calling resolve() on the root at construction time ensures the is_relative_to() comparison
is always against a canonical absolute path. Consistent regardless of env var or symlinks.

## 2026-04-23: Missing task_id in materialize raises RuntimeError (not silent 0)
The old fallback of next(..., 0) would silently mislabel an orphan task as index 0,
producing a wrong filename. Like annotate_task_result, this is an invariant violation
that must not be silently swallowed — raise RuntimeError with a diagnostic message.

## 2026-04-23: BuilderOutput.proposed_changes min_length=1
Symmetric with PlannerOutput.proposed_tasks (min_length=1). An empty proposed_changes
produces an artifact with no content — useless and likely a provider bug. Rejected at
the model boundary before reaching orchestration.

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

## 2026-04-29: classify_risk is non-blocking and has no side effects
Risk classification is a one-shot mapping (action → risk level string). It is
intentionally non-blocking: a future step can use risk_level to prompt for
user confirmation, but Step 12 only stores and surfaces it. The "overwrite"
case is reserved and not yet produced by any code path — it is classified now
so the function is complete and future code paths don't need to change classify_risk.

## 2026-04-29: risk_level stored in both patch_intent_explanations and patch_intent_risks
patch_intent_explanations is a per-intent dict (file, action, risk, reason, summary);
patch_intent_risks is a flat list of risk strings, one per intent.
The flat list makes it easy for operators to scan risk levels without parsing dicts
(e.g. "are there any high-risk changes?"). Both keys are in artifact.metadata.

## 2026-04-29: "preview-only" and unknown actions map to "unknown" risk
When no repository is attached, the file may or may not exist — risk cannot be
determined. Mapping to "unknown" rather than inventing a level (e.g. "low") is
honest: the caller must attach a repo and re-run to get a meaningful risk signal.

## 2026-04-30: RISK_* constants defined in patch_intent.py (single source of truth)
Freeform strings scattered across classify_risk, tests, and CLI are error-prone.
Named constants (RISK_LOW/MEDIUM/HIGH/UNKNOWN) and a frozenset (RISK_LEVELS) give
one canonical definition. PatchDryRunResult.__post_init__ validates against RISK_LEVELS,
making invalid risk levels a loud construction-time failure rather than a silent
propagation. Tests import the constants so they stay in sync automatically.

## 2026-04-30: PatchDryRunResult.__post_init__ raises ValueError (not a Literal type)
Literal[...] would require changing the field annotation and adding a Pydantic validator
or a TypeVar constraint — heavier than needed for a dataclass. __post_init__ raises
ValueError with a clear message. Callers producing PatchDryRunResult (only
generate_dry_run_preview) already pass a value from classify_risk, which always returns
a member of RISK_LEVELS. The guard catches bugs in future callers, not the current path.

## 2026-04-30: format_dry_run_explanations uses "\n\n".join(blocks) for multi-result spacing
Original "\n".join(parts) across all results produced one dense block with no visual
separation between intents. Building a list of per-result blocks and joining with "\n\n"
is the minimal correct change: one blank line between blocks, no trailing newline, no
leading newline. Tested by assert "\n\n" in text in test_multiple_results_all_appear.

## 2026-04-30: RISK_UNKNOWN is conservative by design — documented in code and docs
Both the module docstring and the classify_risk docstring now explicitly state that
RISK_UNKNOWN must NOT be equated with RISK_LOW by future approval/autonomy modes.
This pre-empts a common mistake: treating an absence of evidence (no repo attached)
as evidence of absence (no risk). The architecture.md section echoes the same note.

## 2026-04-30: generate_dry_run_preview owns its own boundary check (Step 12.6)
verify_patch_intent_set already rejects ".." components in target_path. The boundary
check in generate_dry_run_preview (resolve both sides + is_relative_to) is defence in
depth: it catches symlink escapes and any edge-case path that static split-based checks
miss. The rule is "check at the use site" — the function that reads from the filesystem
is responsible for confirming it stays inside its root, regardless of upstream validation.

## 2026-04-30: truncate_preview extracted to patch_intent.py (Step 12.6)
The inline combined_preview[:2000] in the CLI required the caller to know the internal
constant _MAX_PREVIEW_CHARS. truncate_preview(text) moves the cap to the module that
owns the constant. CLI callers import the function, not the constant — implementation
detail stays local to patch_intent.py. No behaviour change; same 2 000-character cap.

## 2026-04-30: diff_preview omitted from CLI terminal output (documented Step 12.6)
format_dry_run_explanations renders the concise block (file/action/risk/reason/summary)
only. The full diff_preview per intent can be several lines; printing it for every intent
in a multi-intent job would produce cluttered terminal output with low signal-to-noise.
The full preview is stored in patch_intent_diff_preview metadata for tooling/guarded mode
to surface intentionally. This is not a bug — it is a deliberate noise-control decision.

## 2026-04-30: patch_intent_risks consumers must validate against RISK_LEVELS (Step 12.8)
Documented in architecture.md. Rationale: PatchDryRunResult.__post_init__ validates at
write time, but Step 13+ will read the stored list and act on it. Defensive re-validation
at the consumption site protects against: (a) metadata written by older code before the
RISK_LEVELS constant existed, (b) hand-edited or test-fabricated records, (c) new risk
levels added in future patches before all consumers are updated. Unknown values must fall
back to RISK_UNKNOWN (conservative), never to RISK_LOW.

## 2026-04-30: Skipped optional triple-run elimination in TestPatchIntentRisksCLI (Step 12.8)
The three focused tests each call _run_risk_scenario, running the full CLI mock 3×. Making
them share a single run would require a class-scoped pytest fixture, but class-scoped
fixtures cannot depend on function-scoped fixtures (tmp_path, monkeypatch, capsys). Adding
a conftest.py or session fixture would sacrifice clarity. Three fast runs (<0.4s total) are
preferable. Documented here so the duplication is intentional, not an oversight.

## 2026-05-01: Task Type Registry v1 — keyword-backed internal, registry-first public API (Step 13)
The registry uses an ordered keyword list internally (v1) — identical semantics to
the former _INTENT_RULES / _REPO_PATH_RULES tables. This preserves routing correctness
while eliminating the duplication. The public API (get_task_type_spec) returns a fully
resolved TaskTypeSpec with repo_route substituted; callers never see {safe_type}.

## 2026-05-01: task_type remains open — unknown fallback is conservative (Step 13)
task_type is not an enum. LLM-generated task types that don't match any keyword return
a fallback spec with repo_route=None and capabilities={"unknown_task_type"}. This is
the safe default: no repo writes, no elevated autonomy. Future step must not promote
unknown_task_type to a permissive path without explicit registry entry.

## 2026-05-01: _INTENT_RULES and _REPO_PATH_RULES removed — single source (Step 13)
Both duplicated keyword tables are gone. TestKeywordSync now tests routing parity at
the function level: both _derive_target_path and _resolve_repo_path call
get_task_type_spec and must return the same result. This is a structural guarantee,
not a copy-sync check. The KEEP IN SYNC comments are no longer needed.

## 2026-05-01: repo_applicator._sanitize_path_component removed (Step 13)
_resolve_repo_path now returns a fully-resolved path from get_task_type_spec; no local
sanitization needed in repo_applicator. patch_intent keeps its own local copy for
materialize_patch_intents workspace filenames (different use site, not routing).

## 2026-05-01: ArtifactKind defaults to UNKNOWN — explicit at creation sites (Step 14)
The default kind=UNKNOWN is a backward-compatibility affordance, not the preferred state.
Every creation site (job_runner, llm_planner, task_runner) sets kind explicitly. Unknown
stays as the default only so old persisted JSON without 'kind' deserializes safely.

## 2026-05-01: planning_artifact prefers explicit kind over legacy name convention (Step 14)
The helper checks kind=PLANNING first (explicit path, Step 14+), then falls back to
name="planning_output" and task_id=None (legacy convention, pre-Step-14). The explicit
path is preferred because: (a) it is the intended stable signal, (b) it does not depend
on a name string that could change. The fallback is deliberate and documented.

## 2026-05-01: artifact_index helpers accept Sequence[Artifact], not Job (Step 14)
Accepting a sequence rather than a Job makes the helpers composable: callers can pass
job.artifacts, a filtered slice, or any other artifact list. No coupling to Job required.

## 2026-06-08: Sole-change generic tests require timestamp ordering (Steps 840-849)
Intent/task-linked tests remain valid without timestamps because their linkage is explicit.
Generic tests can verify a sole applied change only when both apply and test timestamps parse
and the parsed test time is at or after parsed apply time. Missing/invalid ordering is incomplete,
not verified. Parsed datetime comparison is required so timezone offsets cannot create false order.

## 2026-06-08: Steps 810-839 cherry-picked as Proof Chain dependency (Steps 840-849)
After merging the open PR, main lacked the Proof Chain v1/truth-closure files referenced by this task.
The branch cherry-picked Steps 810-824 and 825-839 before applying the ordering closure so the current
block is reviewable against the expected Proof Chain baseline.

## 2026-06-08: Reviewer findings beat worker self-report (Steps 850-864)
GPT5.5 Medium handled narrow Proof Chain ordering logic well, but overclaimed final PASS while
`.agent/live_review.md` still contained a blocking file-provenance finding. Future agents must
read `.agent/live_review.md` before final handoff and treat reviewer findings as authoritative
until resolved in code and tests.

## 2026-06-08: MCP remains inactive by default (Steps 850-864)
Claude Code and VS Code MCP config files were added with empty server maps only. No MCP server is
installed or active. Pi MCP is documented as extension/package-driven; `pi-mcp-adapter` and
`mcporter` were audited by package metadata but not installed.

## 2026-07-09: Two deferred evidence-metadata hardening notes (F003 accepted, not reopened)
F003 was externally accepted (PASS_WITH_RISKS). Two runtime-evidence metadata gaps were observed
and are deliberately NOT fixed under F003, because they do not affect the accepted token/cost
totals (provider_evidence and token_truth carry valid actuals; totals reconcile exactly):

1. Runtime `task_runs/<task>/task_execution_evidence.json` reports
   `actual_provider_available=false` and `actual_token_usage_available=false` even though
   `provider_evidence.json` and `token_truth.json` contain valid provider actuals.
2. Runtime `prompt_trace_summary.json` reports some role/model metadata as unknown although the
   raw `prompt_trace.jsonl` contains it.

Both are evidence-surface metadata defects, not measurement defects. Deferred as hardening
candidates for the later evidence/replay work — preferably F140 or F163. Do not reopen F003.

## 2026-07-09: F004 stream redaction composes, not replaces, the prompt corpus
While building `stream_evidence.py` the existing `prompt_trace.redact_prompt_text`
was found to MISS several real secret shapes, because its patterns disallow the
hyphens/underscores that appear inside modern provider keys:

- `sk-ant-api03-…` (real Anthropic key format) — unredacted
- `AWS_SECRET_ACCESS_KEY=…` (the `SECRET` token is not immediately followed by `=`)
- `-----BEGIN … PRIVATE KEY-----` blocks, JWTs, `xox*-` Slack tokens

F004's binding rule is "no secrets in raw streams, ever", so `redact_stream_line`
COMPOSES the existing helper with a stream-specific corpus (sensitive JSON keys,
provider key shapes, env assignments, private-key headers) rather than trusting
it alone. Redaction stays textual so a stream line remains valid JSON.

The prompt path is deliberately NOT changed here: that is F003-accepted behaviour
and altering it is out of F004 scope. Hardening `redact_prompt_text` with the same
corpus is a follow-up candidate and should be raised as its own item — the gap is
security-relevant and affects prompt traces today.

## 2026-07-10: F004 accepted (PASS_WITH_RISKS) — three deferred hardening notes
F004 (raw stream evidence) received external acceptance `PASS_WITH_RISKS`. Manual
completion job `621369b56e834cd4`; accepted ZIP
`remedy-review-20260709-225052-READY_FOR_REVIEW.zip`. The following non-blocking
notes are recorded as later hardening items and MUST NOT reopen F004:

1. `missing_tests_gate` treats `.jsonl` fixtures as test files requiring direct
   coverage. A fixture is data, not an executable test; the gate should not demand
   a verification run keyed on it.
2. A changed task with no task-local test files may receive `NEEDS_TESTS` even
   when verification is genuinely supplied through another explicit scope. The
   gate's `covered = bool(related_tests) and not uncovered_tests` is vacuously
   false for a code-only task and should recognize cross-scope verification.
3. `job_evidence.py` reads each exported stream artifact fully into memory while
   copying/hashing it. Bounded at 50 MB/task, so acceptable for F004; stream the
   copy+hash later for very large artifacts.

Preferred home for (1) and (2): the evidence/replay hardening work (F140/F163).
(3) is a local streaming optimization in `job_evidence.py`.

## 2026-07-10: F005 reuses the existing PlannerOutput shape, adds schema_v (Steps 5961-6020)
`planner_models.PlannerOutput` is already a Pydantic model consumed by
`llm_planner.plan_job_with_llm`. F005 adds a `schema_v`-bearing schema model in the
new `schemas/` package rather than inventing a second planner taxonomy; the schema
model round-trips to/from the existing `PlannerOutput` so the planner path keeps its
current downstream contract. Same principle for the reviewer verdict: the schema
model mirrors the accepted verdict/findings/confidence/summary shape already parsed
by `_parse_reviewer_json`, not a new one (anti-goal A6: no new taxonomies).

## 2026-07-10: F005 FINDINGS correction — mandatory schema_v, hard retry cap, native schemas (Steps 5961-6020)
External review returned FINDINGS on the first F005 package. Six corrections, no
new taxonomy or gate:
1. `schema_v` is a REQUIRED response field (bare `Literal`, no default); the
   model's version is a `SCHEMA_V` ClassVar so the field never needs a default.
   Missing schema_v is now a `parse` failure (was silently defaulted).
2. The single-retry maximum is a hard safety rule: `run_structured_call` takes a
   boolean `allow_parse_retry` (no integer knob); three+ calls are impossible.
3. Provider-native schema enforcement: Claude CLI `--json-schema` (via
   `build_claude_cli_args(json_schema=)`) and Ollama `format=` (via
   `OllamaPlanner.plan_raw`). The reviewer sends a SHORT instruction, not a
   duplicated schema, and fails clearly if the CLI lacks the option — no
   prompt-only pretense. The capability probe (`claude --help`) is cwd-pinned
   like every other CLI call.
4. `plan-job-local` uses the structured planner by default; legacy `planner.plan`
   only under `REMEDY_PLANNER_FREETEXT=1`; missing structured capability fails
   (error_category=config), never a silent legacy fallback.
5. Prompt trace records one entry per actual provider call (reviewer initial +
   parse-retry; planner initial + retry), each carrying `schema_v`.
6. Parse exhaustion is classified `parse` in run-log/result evidence
   (`error_category=parse`, `ReviewerOutput.error_class`), not the exception
   class name. `parse` already exists in F005 / is required by F010.

Pre-F005 CLI-reviewer unit tests (fake bins without --json-schema / schema_v)
were pinned to the legacy free-text reviewer via `REMEDY_REVIEWER_FREETEXT=1`;
they validate transport/usage/safety, not F005 schema enforcement, which has its
own dedicated fake-provider tests.

## 2026-07-10: F005 runtime FINDINGS correction — native structured_output envelope (Steps 5961-6020)
External review returned FINDINGS on ZIP remedy-review-20260710-231042 (reviewed
job 2f1ca41f52564511). Seven runtime corrections, no new taxonomy or gate:
- Claude Code's structured result carries the object in `structured_output`, not a
  string `result`. `token_actuals.parse_cli_envelope` parses the envelope ONCE
  (value, usage, subtype). The CLI reviewer prefers `structured_output` in
  structured mode; a success envelope without it, or a malformed one, is `parse`.
- The F004 stream path (`final_result_text`) compact-serializes `structured_output`
  so streamed and non-stream yield the same validated value; normalized events
  still never copy the model response.
- `subtype=error_max_structured_output_retries` is a structured parse/validation
  failure → error_class `parse` (JSON + stream), not `provider_error`; it triggers
  Remedy's one parse retry and its Usage/cost are retained so the failed attempt
  counts toward 2/2/2 totals.
- Finding 5: the reviewer effective `-p` prompt is built once in the loop
  (`_reviewer_effective_prompt`) and recorded; provider sends it verbatim, so
  `prompt_sha256 == sha256(sent)` for initial and retry. Schema is out-of-band via
  `--json-schema`, never duplicated into the prompt.
- Finding 6: removed the `claude --help` preflight (help omits flags; absence is
  not proof). `--json-schema` support is proven by the real invocation; an
  unknown-option stderr → `config`; ordinary provider errors stay provider errors.
All proven with recorded envelopes / mocked subprocess; zero provider calls.

## 2026-07-11: F005 runtime FINDINGS #2 — stream classification + per-call traces (Steps 5961-6020)
External review returned FINDINGS on ZIP remedy-review-20260710-235823 (reviewed
job 997bcc036c12415e). Two corrections, no new taxonomy or gate:
1. The stream path previously reduced the final result to text + usage, losing
   is_error/subtype/errors, so an ordinary streamed provider error (e.g.
   subtype=error_during_execution) was misclassified as `parse` merely because the
   extracted text was empty. `stream_evidence.final_result_envelope()` now returns
   the COMPLETE final-result record (structured_output, legacy text, is_error,
   subtype, errors, usage/cost, raw line/byte refs) read back from the persisted
   redacted raw line, and the streamed structured Reviewer classifies exactly like
   the JSON path. Class is never inferred from an empty result string. Normalized
   events still copy no model response text.
2. `_call_with_retry()` may invoke the provider more than once (F001 transport
   retry), but only one reviewer trace was recorded up front. It now takes a narrow
   `on_call(transport_attempt, is_transport_retry)` callback fired immediately
   before every real call, and the single logical parse retry runs through the same
   helper with `is_parse_retry=True`. Result: one trace per ACTUAL provider call,
   reviewer traces == reviewer ProviderAttempts, transport retries of the parse
   retry stay ONE logical parse retry, and every trace prompt hash equals the sent
   string. This reuses the existing retry mechanism — no second retry system.
All proven with recorded stream envelopes, fake CLI executables and fake providers;
zero provider calls.

## 2026-07-11: F005 FINDINGS #3 — envelope-before-exit-code, planner pre-call traces (Steps 5961-6020)
External review returned FINDINGS on ZIP remedy-review-20260711-115512 (reviewed
job c4def4a3074d4a7c). Two corrections, no new taxonomy or gate:
1. The streamed CLI can emit a valid final result envelope (e.g. a native
   structured-output failure carrying Usage/cost) and THEN exit nonzero. Reading
   the return code first threw that envelope away, so exhaustion+exit1 became a
   provider_error with null usage. `_call_streamed()` now parses events, Usage and
   the FinalStreamResult BEFORE interpreting the exit code, and raises a typed
   `_StreamNonZeroExit` carrying the envelope/usage/returncode/stderr. The
   structured Reviewer classifies from the envelope: exhaustion -> parse (+usage)
   on exit 0 or 1; any other is_error -> provider_error; a "successful" structured
   result contradicted by a nonzero exit is rejected as provider_error (we do not
   trust an inconsistent process). The raw stream is parsed in exactly one place.
2. Planner traces were written by `call_recorder` AFTER `plan_raw()` returned, so a
   provider/network exception produced a real call with NO trace — violating "every
   call logs its schema_v". The split on_call/call_recorder API is replaced by ONE
   pre-call callback `on_call(attempt, schema_v, is_parse_retry, effective_prompt)`
   fired immediately before every real call. Traces now persist for success,
   invalid JSON and raised exceptions alike; no provider call still means no trace.
Both proven with fake executables and fake planners; zero provider calls.

## 2026-07-11: F006 — worktree isolation replaces copy staging (Steps 6021-6080)
- The run workspace IS a git worktree for a git target; nothing is copied. The
  filtered-copy staging path survives ONLY as the non-git fallback, so the
  historic "self-run dirties the main checkout" risk is structurally impossible.
- `.remedy-wt/` is excluded via `.git/info/exclude`, not `.gitignore`: the rule
  that protects the checkout must not itself dirty that checkout. (The repo's own
  `.gitignore` also lists it, for humans.)
- In a worktree `.git` is a FILE, not a directory, so the staged-change scanner
  needed an explicit file-level skip — otherwise the gitdir pointer would have
  been reported as a run change.
- Locks live under `<data>/projects/<sha256(repo path)[:16]>/locks/`. A short
  digest of the resolved repository path is a sufficient stable project id; F146
  is deliberately not implemented here.
- `remove()` keeps the result branch by default and there is no merge path at
  all: the branch plus `result.diff` is the entire hand-off, and merging stays a
  deliberate human action.

## F007 — Runtime harness

- Runtime state identity is PID **plus** process creation time **plus** a command
  fingerprint. A PID alone is not identity: the OS recycles PIDs, and `runtime stop`
  must never kill an innocent process that inherited one. A mismatch clears the
  stale state and reports it, killing nothing.
- A busy port is never fought over. The harness picks a free port and reports the
  EFFECTIVE port; killing whatever owns the requested port would be a footgun.
- Detection reads checked-in files only (package.json, pyproject.toml, requirements)
  and never imports project code. Two candidate runtimes is ambiguity, and ambiguity
  blocks with "configuration required" rather than guessing.
- `.remedy/config.toml [runtime]` is the canonical binding for F007. The general
  `remedy.toml` config system is deliberately NOT migrated or replaced.
- The project digest is F006's resolved-path digest. F146 (the project registry) is
  not implemented here.
- F008 (SSE stream, hook, polling fallback) is Tier 5 and depends on F146: no
  endpoint, EventSource, hook or UI work belongs on this branch.
