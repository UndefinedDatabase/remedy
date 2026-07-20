# Context — F017 Scope Fences

## Branch
`feature/f017-scope-fences` (from main after F012 merge)

## Scope
T001 only: FenceSpec + load precedence + pure path checker + exhaustive tests.
T002 (applicator enforcement) and T003 (job field + config keys + CLI) are future.

## Key decisions
- Module placed at `packages/orchestration/scope_fences.py` (not `fences.py`)
- Builtin deny uses root-level paths only (`.git/` not `*/.git/`)
- `..` is structurally denied (never resolved, even if non-escaping)
- Symlink resolution uses `Path.resolve()` (read-only filesystem access)
- Case sensitivity: no folding, documented as filesystem-dependent
- Empty allow list = allow-all with logged warning (not a brick)
- Config scope table read from `[remedy.scope]` in remedy.toml

## Applicator choke point (T002 reference)
- Primary: `patch_apply.apply_patch_intent` (all repo writes per job_fulfillment.py)
- Structured: `source_apply.apply_structured_patch` (has rollback)
- Task output: `repo_applicator.apply_task_output_to_repo` (markdown-only)
