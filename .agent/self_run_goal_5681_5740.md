# Steps 5681-5740: Model / Role Runtime Configuration v1 + Execution Config Evidence + Evidence Hygiene

## Product goal

Add configurable model/provider settings per role (builder, reviewer, repair),
structured execution config evidence, prompt trace and token truth role metadata,
final verifier model mismatch detection, evidence hygiene fixes, and large-task
orchestration plan artifact.

## Hard constraints

- Do NOT fake provider token usage.
- Do NOT fake provider/model data.
- Do NOT invent prompt/provider evidence for manual repair tasks.
- Do NOT reuse old evidence as proof.
- Do NOT auto-push or auto-merge.
- Do NOT use variable names or strings containing `secret`, `password`, `token`, `key`, `credential`, `api_key`, `SECRET`, `SYSTEM PROMPT`, `API_KEY` in test fixtures.
- Do NOT label estimated tokens as exact/actual.
- Do NOT copy estimated values into `actual_*` fields.
- Do NOT copy configured values into actual values unless they are truly the same source.

---

## Task 1: Role-based runtime configuration

### Files allowed

- `packages/orchestration/role_config.py` (new)
- `tests/orchestration/test_role_config.py` (new)

### Summary

Create a role configuration module that resolves model/provider/effort settings
per role (builder, reviewer, repair, design_worker, test_worker, final_verifier).
Configuration comes from CLI args, config file, or defaults.

### Acceptance

- `RoleConfig` dataclass with provider, model, effort fields
- `resolve_role_config(role, cli_args, config_file)` returns RoleConfig
- CLI args override config file, config file overrides defaults
- Defaults preserve current behavior (no breaking change)
- Unknown roles produce warning, not crash
- At least 8 tests covering: defaults, CLI override, config file, precedence, unknown role, all 6 roles

---

## Task 2: CLI/config model override flags

### Files allowed

- `apps/cli/commands/do_cmd.py` (modify)
- `tests/test_do_job_flow.py` (modify)

### Summary

Add CLI flags for per-role provider/model/effort configuration:
--builder-provider, --builder-model, --builder-effort,
--reviewer-provider, --reviewer-model, --reviewer-effort,
--repair-provider, --repair-model, --repair-effort.
Wire them through to job-flow and job-run.

### Acceptance

- CLI flags parsed and validated
- Flags passed through to role config resolution
- Invalid provider/model/effort rejected at CLI layer
- Existing --builder/--reviewer still work (backward compatible)
- At least 5 tests: flag parsing, validation, passthrough, backward compat, invalid rejection

---

## Task 3: Execution config evidence artifact

### Files allowed

- `packages/orchestration/execution_config_evidence.py` (new)
- `tests/orchestration/test_execution_config_evidence.py` (new)

### Summary

Create structured `execution_config.json` evidence artifact with schema_version,
source_root, job_id, step_range, resolved_at, per-role config, fallback models,
invocation args, warnings, mismatch findings, and evidence status.

### Acceptance

- `build_execution_config_evidence(job_id, step_range, role_configs, cli_args)` returns dict
- Schema version 1
- Per-role fields: configured provider/model/effort, actual provider/model if known
- actual_config_available = false when actual provider/model unavailable
- Unavailable fields recorded as null, not invented
- At least 8 tests: schema fields, per-role recording, unavailable actual, warnings, mismatch detection

---

## Task 4: Prompt trace role/model metadata

### Files allowed

- `packages/orchestration/job_evidence.py` (modify)
- `tests/orchestration/test_job_evidence.py` (modify)

### Summary

Update prompt trace and provider evidence so each provider-backed call records:
role, configured provider, configured model, actual provider/model if known,
source of model resolution, whether actual model is verified or assumed.

### Acceptance

- Prompt trace entries include role field
- Prompt trace entries include configured_provider, configured_model
- Prompt trace entries include actual_provider, actual_model (null if unknown)
- Prompt trace entries include model_resolution_source
- Prompt trace summary includes per-role model information
- At least 6 tests: role recording, configured fields, actual null when unknown, summary per-role

---

## Task 5: Token truth role/model integration

### Files allowed

- `packages/orchestration/token_truth.py` (modify)
- `tests/orchestration/test_token_truth.py` (modify)

### Summary

Update token truth so token records include role, provider, configured model,
actual model if available, actual token usage if provider exposes it,
estimated token usage if not, actual_available boolean, estimation_method.

### Acceptance

- Per-task token records include role field
- Per-task records include configured_model, actual_model
- actual_available = false when provider doesn't expose usage
- estimated values never in actual_* fields
- estimation_method recorded when estimated
- At least 6 tests: role field, model fields, actual_available false, no fake actuals, estimation method

---

## Task 6: Final verifier model mismatch policy

### Files allowed

- `packages/orchestration/final_verifier.py` (modify)
- `tests/orchestration/test_final_verifier.py` (modify)

### Summary

Final verifier inspects execution config and provider/prompt evidence for
model configuration consistency. Detect configured-vs-actual mismatches,
missing model evidence, fake/contradictory model data.

### Acceptance

- Matching configured/actual model → PASS
- Unavailable actual model with configured → PASS_WITH_RISKS + warning
- Configured says model-A but evidence shows model-B → BLOCKED or PASS_WITH_RISKS
- Missing builder/reviewer model config → warning (not silent PASS)
- Fake/contradictory model evidence → BLOCKED
- At least 8 tests: match pass, unavailable warn, mismatch block, missing warn, fake block, role severity

---

## Task 7: Evidence hygiene fixes

### Files allowed

- `packages/orchestration/job_evidence.py` (modify)
- `scripts/build_review_manifest.py` (modify)
- `tests/orchestration/test_job_evidence.py` (modify)
- `tests/test_do_job_flow.py` (modify)

### Summary

Fix evidence hygiene: verification_tests.json must be terminal/current,
manual repair provenance hashes validated against content proof,
review bundle integrity remains packaging-layer check.

### Acceptance

- verification_tests.json refreshed after new tests added
- Manual repair provenance hash fields validated against current content proof
- Stale manual repair provenance recorded but not blocking if content proof current
- Review bundle integrity stays packaging-layer (not runtime gate)
- At least 5 tests: stale verification detection, manual hash validation, supersession recording

---

## Task 8: Large-task orchestration plan artifact

### Files allowed

- `packages/orchestration/task_plan_evidence.py` (new)
- `tests/orchestration/test_task_plan_evidence.py` (new)

### Summary

Create package-level task plan artifact (large_task_plan.json) with schema_version,
package_goal, step_range, tasks, dependencies, expected changed areas, tests per task,
risk tags, review strategy, completion criteria.

### Acceptance

- `build_task_plan_evidence(goal, step_range, tasks, risks)` returns dict
- Schema version 1
- Tasks list with id, summary, dependencies, expected files, expected tests
- Risk tags per task
- Completion criteria present
- At least 6 tests: schema fields, task list, dependencies, risks, completion criteria
