# Context

## Active Branch
`feature/step2-packaging-cli`

## PR
None yet — will be created after commits are pushed.

## Scope
Step 2: Make Remedy a real installable Python project with a working CLI.

## Constraints
- No orchestration logic
- No provider implementations
- No agent loops
- No database; JSON files only for storage
- No external deps beyond pydantic (already required)
- Storage path is CWD-relative (.data/jobs/)

## Assumptions
- CLI runs from the project root; .data/ is created relative to CWD
- user_prompt on Job is a pure data field, not orchestration
- hatchling used as build backend (minimal, no extra config)
- pytest pythonpath = ["."] replaces all sys.path hacks in tests

## Branch Scope Decision
Step 2 is a new branch because purpose, merge intent, and feature boundary
are all distinct from Step 1.5 (contracts hardening). Recorded per AGENTS.md.
