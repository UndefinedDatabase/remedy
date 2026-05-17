# Plan

## Goal
Step 30.10: Smoke Determinism + Markdown Safety Type Tightening

## Status
COMPLETE — committing

## Completed
- [x] markdown_output_safety.py: tighten signature to str, remove object coercion
- [x] repo_applicator.py: str() normalisation at metadata boundary
- [x] patch_apply.py: add belt-and-suspenders comment on stem neutralization
- [x] scripts/remedy_smoke.sh: seed README.md; deterministic write_readme prompt
- [x] tests/test_markdown_output_safety.py: remove coercion tests, fix str-only assertion
- [x] tests/test_patch_apply.py: rename misleading stem tests to state actual invariant
- [x] tests/test_remedy_smoke_script.py: add README seed + prompt assertions
- [x] docs/architecture.md: str signature, caller normalisation, smoke seeding note
- [x] Suite: 1720 passed (same count — removals balanced additions)

## Next
Push. PR #26 already open.
