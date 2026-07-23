# Plan — F081 remedy init

## Goal
`remedy init` — non-interactive, idempotent command that registers a git
repo as a Remedy project. Three task slices (T001–T003).

## Status: T001 COMPLETE (repair round done), T002–T003 pending

## T001 (current): command skeleton + preflight + registry + idempotency
- init_cmd.py: `remedy init [--project-name NAME]`
- Preflight: non-git → exit 4, exact error message
- Registry: resolve_project / register_project_repo from F146
- Idempotency: second run → all `[exists]`, exit 0
- Tests: tests/cli/test_init_cmd.py

## T002 (next): config template + runtime detection
- One module constant for config template
- Runtime detection wiring (confident → fill table, else skip)
- Honest-skip path for no-marker repos

## T003 (later): hygiene + summary + print-only/json
- Ignore-file entries for data dir
- Summary block with slug, uuid, config path, next command
- --print-only, --json flags
