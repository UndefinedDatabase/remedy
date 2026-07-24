# Plan — F148 Project scoping everywhere

## Goal
Every job is attributable to exactly one project via an additive
`project_id` field. Listing commands default to current project with
`--all-projects` escape. Legacy data loads with project_id=None.

## Checklist
- [x] T001 — model field + creation-path audit + backward-compat fixture
- [x] T002 — project_scope module + legacy rule + unit tests
- [x] R-0098..R-0101 — reviewer repairs (ruff fix, creation guard, attach_job, precomputed legacy)
- [x] T003 — CLI integration across all listed commands + adopt + fixture
- [x] T004 — docs + status view scoped label

- [x] R-0102..R-0107 — reviewer repairs round 2
- [x] R-0108..R-0109 — reviewer repairs round 3
- [x] Closure — verdict PASS, evidence job, STATUS [x], PR

## Current Step
Closure complete.
