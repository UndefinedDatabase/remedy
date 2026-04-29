# Context

## Active Branch
`feature/step11-patch-dry-run`

## PR
None yet.

## Scope
Step 11: Dry-run preview + human-readable explanation layer.
Read-only interaction with target repo. No file writes.

## Constraints
- NO patch application, NO repo writes of any kind
- repo_overwrite stays reserved
- Only read existing target files (read_text, no write)
- Dry-run results stored in artifact metadata only (not persisted as separate files)
- Explanations derived from task_type and artifact.content; raw LLM strings are
  not used as-is — summaries are extracted and truncated
- target_path is already verified safe by verify_patch_intent_set before this runs

## Key Design Decisions
- PatchDryRunResult is a dataclass (transient, not persisted via Pydantic)
- generate_dry_run_preview is a pure read-only function
- format_dry_run_explanations produces the CLI text block
- dry_run_block is a string computed inside the if vr.passed: block,
  printed after save_job to keep the output ordering clean
