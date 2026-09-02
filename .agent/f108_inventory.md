# F108 Source Inventory — Tiered artifact summaries

Read `docs/roadmap/features/T3_F108.md` in full before this file (Goal &
Done, Design, Task slicing, Acceptance, Orchestrator brief, Do not touch).
This is round-1 research only: nothing here is production code, and none
of it was written or modified this round.

## 1. `packages/orchestration/context_compiler.py` — selection & budget

The compiler is the SELECTOR T003 hooks into. Structure (all in this one
file, 1133 lines):

- `compile_task_context()` (context_compiler.py:740) is the entry point.
  It buckets every candidate path into four tiers — `TIER_FENCED` (1),
  `TIER_NEIGHBOR` (2), `TIER_DISTANT` (3), `TIER_OMITTED` (4) — declared at
  context_compiler.py:609-612. Tier 1 (the task's declared write scope) is
  always carried in FULL and never demoted. Tier 2 (direct import
  neighbors) is full when `fits_inline_size_cap()` (context_compiler.py:427)
  allows, else demoted to signatures. Tier 3 is signatures always. Tier 4
  is omitted for distance.
- The budget mechanism is three ordered demotion phases, each a `while`
  loop re-checking the running total against `token_budget`
  (context_compiler.py:868-916): Phase A demotes the largest full tier-2
  file to signatures; Phase B omits the largest tier-3 file; Phase C omits
  the largest tier-2 file entirely. Victim selection is centralized in
  `_largest_tokens_first()` (context_compiler.py:723), which always picks
  the largest `estimated_tokens` within a tier (ties broken by
  `rel_path` ascending) — this is the exact mechanism T003 would extend
  with a new demotion phase/threshold check for oversized artifacts.
- `SelectedFile` (context_compiler.py:632) carries `rel_path`, `tier`,
  `rendering` (`"full"` or `"signatures"`), `estimated_tokens`. A tiered
  artifact summary (L1/L2/full_ref) would most naturally become a THIRD
  `rendering` value alongside `"full"` and `"signatures"` — the module's
  own docstring (context_compiler.py:14-16) explicitly anticipates this:
  "tiered summaries are a NEW REPRESENTATION it can select instead of full
  content when an artifact exceeds a size threshold."
- `OmissionRecord` (context_compiler.py:650) and the `OMISSION_REASON_*`
  constants (context_compiler.py:615-620) are the existing "why wasn't X
  included / why was X reduced" audit trail; a new `OMISSION_REASON_SIZE`-
  adjacent reason (e.g. `"summarized"`) would follow the same pattern.
- Token estimation throughout is `estimate_text_tokens()`, imported from
  `packages/orchestration/token_economy.py` (context_compiler.py:114) —
  the same estimator T003's size-comparison work should reuse rather than
  inventing a second one.
- `DEFAULT_CONTEXT_TOKEN_BUDGET = 24000` (context_compiler.py:603) and
  `DEFAULT_INLINE_SIZE_CAP_BYTES = 16384` (context_compiler.py:143) are the
  two existing size/budget constants in this module; F108's own oversized-
  artifact threshold (Design section, "Threshold (config, e.g.
  lines/tokens)") is a new constant of the same kind, not yet declared
  anywhere.
- Note: `compile_task_context()` selects and renders repository SOURCE
  FILES (task write-scope + import graph), not job ARTIFACTS (diffs,
  logs, reports). F108's "oversized artifact" scope (evidence-directory
  files like `workspace.diff`, per-task JSON, `safe.diff`) is a
  DIFFERENT candidate set than what this module currently walks — T003
  will need to decide whether artifacts enter through this same selector
  or a sibling path that shares its tier/budget/rendering vocabulary. This
  is exactly the "inspect current shape before building" question the
  feature file's "How it fits" section poses; it is not yet answered by
  anything on disk.

## 2. `packages/orchestration/role_config.py` — declaring a provider-call role

The full pattern an existing role uses (154 lines total, read whole):

- `KNOWN_ROLES: tuple[str, ...]` (role_config.py:60-69) is the single
  registry of recognised role names — currently `builder`, `reviewer`,
  `repair`, `design_worker`, `test_worker`, `final_verifier`,
  `orchestrator`, `teacher`. Declaring T002's `summary` role means adding
  one string to this tuple, with a one-line WHY comment above the tuple
  (following the `orchestrator`/`teacher` precedent at role_config.py:50-59)
  explaining why `summary` needs no CLI override flags / budget limit, or
  why it does.
- `resolve_role_config(role, cli_args=None, config_file=None) -> RoleConfig`
  (role_config.py:107) resolves precedence CLI args > config file >
  provider-aware built-in defaults for `provider`/`model`/`effort`. An
  unknown role only WARNS (role_config.py:130-135), it does not raise —
  so declaring `summary` in `KNOWN_ROLES` is additive and silences that
  warning rather than being required for the role to function at all.
- `RoleConfig` (role_config.py:80-87) is a frozen dataclass:
  `role, provider=DEFAULT_PROVIDER, model=DEFAULT_MODEL,
  effort=DEFAULT_EFFORT`.
- `default_model_for_provider()` (role_config.py:75) and
  `_PROVIDER_DEFAULT_MODELS` (role_config.py:38-44) are where a role's
  provider-specific default MODEL is chosen, sourced from
  `packages/orchestration/model_aliases.py` — routing `summary` to a
  cheap/local model (F110/F113, both explicitly out of scope for F108
  per "Do not touch") would eventually touch this table or the config
  file layer, never this feature.

## 3. Existing schema-validated JSON artifact pattern

Two reusable patterns exist; either could back `artifact.summary.json`:

- **Pydantic-model validation (F005)** —
  `packages/orchestration/schemas/validation.py`, in particular
  `validate_response(model_cls: type[BaseModel], raw: Any) -> ValidationResult`
  (validation.py:90) and `to_json_schema(model_cls) -> dict`
  (validation.py:41, via `model_cls.model_json_schema()`). This is THE
  existing "turn a raw provider response into a validated model or a
  classified parse failure" primitive — directly reusable for T002's
  "generation call with the summary role + validation + fallback": define
  an `ArtifactSummary` (or `artifact.summary.json`) pydantic model, get its
  JSON Schema for free via `model_json_schema()`, and validate the
  provider's response through this same entry point, inheriting its parse-
  failure classification (`PARSE_ERROR_CLASS = "parse"`) and hint-building
  (`_hint_from_errors`, validation.py:77).
- **Strict external-schema hand-validation (F012)** —
  `packages/orchestration/manifest_schema.py` (160 lines): a
  dependency-light layer of `req_map`/`req_key`/similar primitives
  (manifest_schema.py:61-70) raising `SchemaError(ValueError)`
  (manifest_schema.py:54) for untrusted JSON read back off disk, with a
  single shared numeric LIMITS table (manifest_schema.py:32-51) so a
  writer can never create a record the reader would later refuse for size
  alone. `packages/orchestration/dod_schema.py` (406 lines,
  `DoDSpecError` at dod_schema.py:105,
  `validate_check_spec(kind, spec)` at dod_schema.py:158) follows the same
  shape for a different artifact family. This is the heavier-weight
  pattern used where the reader must be defensive against a TAMPERED file
  (bools/ints not silently coerced, required fields have no default) — the
  Design section's "hash-invalidated... cached" language for
  `artifact.summary.json` suggests this level of defensiveness may not be
  needed (it is Remedy's own generated cache, not untrusted external
  input), making the lighter pydantic route (F005's) the better fit,
  but both exist on disk as precedent.

## 4. Existing diff reader / log-parsing code

- **Unified-diff reader: YES, two complementary modules.**
  `packages/orchestration/diff_parser.py` (735 lines) is PURE (no
  filesystem access) and turns diff TEXT into a contract-versioned view:
  entry point `parse_unified_diff_to_view(diff_text: str) -> dict`
  (diff_parser.py:461), returning
  `{"version": DIFF_VIEW_VERSION, "truncated": bool, "files": [...]}`
  with per-file, per-line structure (`_FileRegion` at diff_parser.py:175)
  and two built-in ceilings, `DIFF_VIEW_MAX_BODY_LINES = 20_000`
  (diff_parser.py:131) and `DIFF_VIEW_MAX_FILES = 2_000`
  (diff_parser.py:147) — i.e. it already sections a diff PER FILE, which
  is exactly the "sectioning is mechanical first (diff per file...)"
  Design requirement.
  `packages/orchestration/diff_view_source.py` (196 lines) is the
  filesystem half: `build_diff_view(evidence_dir, task_id=None) -> dict`
  (diff_view_source.py:90) resolves WHICH artifact to read
  (`workspace.diff` at the job root or `task_runs/<id>/safe.diff`, named
  once at diff_view_source.py:35-36), reads it under a byte ceiling
  `DIFF_VIEW_MAX_ARTIFACT_BYTES = 8_000_000` (diff_view_source.py:59,
  cutting back to the last newline so a mid-line/mid-character cut never
  happens, diff_view_source.py:170-179), then hands the text to
  `parse_unified_diff_to_view`. T001's mechanical diff sectioner should
  reuse `parse_unified_diff_to_view`'s per-file regions directly rather
  than re-parsing unified-diff syntax from scratch.
- **Log parser by time/marker blocks: NONE FOUND.** Searched
  `packages/orchestration/run_log.py` (append-only JSONL event trail,
  one JSON object per line — already structured, not free text needing
  sectioning) and grepped broadly across `packages/orchestration/*.py`
  for section/split/log-parsing helpers; nothing implements "logs per
  time/marker blocks" as the Design section describes. T001's log
  sectioner is new code with no existing implementation to reuse, though
  it can borrow the ceiling/truncation-sentinel DISCIPLINE (not the code)
  from `diff_view_source.py`'s byte-ceiling handling above.

## 5. Evidence storage layout — where tiers would live "next to the artifact"

- Evidence root resolution: `packages/orchestration/data_paths.py`,
  `resolve_data_root()` (data_paths.py:37) resolves `REMEDY_DATA_DIR` (env
  var, then `remedy.toml`, then `<repo_root>/.data`);
  `evidence_exports_dir(root=None)` (data_paths.py:103) returns
  `<data_root>/evidence_exports`; `job_evidence_export_dir(job_id, root=None)`
  (data_paths.py:112) returns `<evidence_exports>/<job_id>` — one directory
  per job.
- Inside one job's evidence directory (written by
  `export_job_evidence()`, `packages/orchestration/job_evidence.py:169`):
  the job-level diff lands at the root as `workspace.diff`
  (job_evidence.py:247/249, via the local `_write()` closure at
  job_evidence.py:198); per-task artifacts land under
  `task_runs/<task_id>/` — e.g. `stream_artifacts.json`
  (job_evidence.py:293), `task_execution_evidence.json`
  (job_evidence.py:386), `task_actor_binding.json` (job_evidence.py:428),
  each with a `.error.txt` sibling on write failure
  (job_evidence.py:305/314/331/344/392/434) rather than a silent drop —
  the pattern F108's own "missing/failed summary NEVER blocks the run"
  fallback rule should match.
  `_task_evidence_dir(out_base, task_id)` (job_evidence.py:46) is the one
  function that resolves a task's evidence subdirectory, contained
  against path traversal via `_validate_output_path`
  (job_evidence.py:61).
- Given this, "tiers live next to the artifact in evidence" (Design
  section) most naturally means: a `workspace.diff.summary.json` (or
  `<artifact-name>.summary.json`) sibling file written into the SAME
  directory `export_job_evidence()` already writes the artifact into —
  root-level next to `workspace.diff`, or inside
  `task_runs/<task_id>/` next to `safe.diff` — rather than a new evidence
  subtree. No existing writer produces a summary sibling today; this is
  new ground T001's storage/caching work covers.

## 6. Suggested test path

Confirmed: `tests/orchestration/test_artifact_summaries.py` does not exist
in this repository as of this round (`ec81e697` base, and unchanged on
this branch — this round wrote no test file).
