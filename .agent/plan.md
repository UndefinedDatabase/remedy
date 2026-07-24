# Plan — F148 Project scoping everywhere

## Goal
Every job is attributable to exactly one project via an additive
`project_id` field. Listing commands default to current project with
`--all-projects` escape. Legacy data loads with project_id=None.

## Checklist
- [ ] T001 — model field + creation-path audit + backward-compat fixture
- [ ] T002 — project_scope module + legacy rule + unit tests
- [ ] T003 — CLI integration across all listed commands + adopt + fixture
- [ ] T004 — docs + status view scoped label

## Current Step
T001 — add project_id to Job model, audit and wire all creation paths,
backward-compat fixture for old JSON without the field.
