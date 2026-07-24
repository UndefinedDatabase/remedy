# Plan — F148 Project scoping everywhere

## Goal
Every job is attributable to exactly one project via an additive
`project_id` field. Listing commands default to current project with
`--all-projects` escape. Legacy data loads with project_id=None.

## Checklist
- [x] T001 — model field + creation-path audit + backward-compat fixture
- [ ] T002 — project_scope module + legacy rule + unit tests
- [ ] T003 — CLI integration across all listed commands + adopt + fixture
- [ ] T004 — docs + status view scoped label

## Current Step
T002 — scope module + legacy rule + unit tests.
