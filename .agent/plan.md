# Plan — Steps 2226-2295: Ruff / Mypy / Coverage Baseline v0

## Goal
Add pragmatic static-analysis and coverage baseline. Close R-0119/R-0120.

## Core principle
Workers execute. Remedy governs. Automated quality visibility, not perfection.

## Steps
- [x] Phase 0: Close R-0119 (positive-path tests for checks 10/11) + R-0120 (token guardrail path)
- [x] Phase 1-4: Dev deps + Ruff/Mypy/Coverage configs in pyproject.toml
- [x] Phase 5: Scripts (remedy_lint.sh, remedy_coverage.sh)
- [x] Phase 6: Fix safe lint/type issues (1669 auto-fixed, F821/F401 manual, per-file ignores)
- [x] Phase 7: Coverage baseline 76.3%, gap document, fail_under=75.0
- [x] Phase 8: Backlog update (3/30 strict completed)
- [ ] Phase 9-12: Catalog verify, targeted tests, full suite, commit + PR + reviewer

## 30-task backlog
- Strict completed: 3/30
- Next: Review Bundle Structured Error Reporting v1

## Hard rules
No shell=True; no provider SDK; no auto-apply/approve/PR/git; no MemPalace/embeddings.
