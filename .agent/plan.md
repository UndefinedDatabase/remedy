# Plan — Steps 865-879: Context Inspector v1

## Goal
Build `remedy context inspect <job_id> [task_id] --json` — safe preflight showing what worker will see.

## Current Step
Complete — all steps verified

## Steps
- [x] 865: Merge handoff consolidation
- [x] 866: Define context inspection model (dataclasses)
- [x] 867: Path policy rules (deny/protect/unsupported)
- [x] 868: Inclusion reason rules (manifests, targets, tests, config)
- [x] 869: Token/size estimation (bytes stat, ceil(bytes/4))
- [x] 870: Policy gates (7 enforced gates)
- [x] 871: Build inspection from job/task (inspect_context)
- [x] 872: CLI context inspect command + catalog entry
- [x] 873: Redaction tests (8 tests)
- [x] 874: Inclusion tests (13 tests)
- [x] 875: CLI tests (10 tests)
- [x] 876: Tooling awareness (5 tests)
- [x] 877: Docs (docs/context-inspector.md)
- [x] 878: Targeted tests — 70 targeted + 3011 fast lane passed
- [x] 879: Final handoff

## Risks
- Token estimation is heuristic (ceil(bytes/4)), documented as such.
- No deep file walk beyond 3 levels / 500 files.
