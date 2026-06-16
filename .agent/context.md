# Context

## Active Branch
feature/steps-2226-2295-ruff-mypy-coverage-baseline-v0
(forked from clean main at 6b3d8fc after PR #79 merged Dogfood Run Closure v0.1).

## Scope
Steps 2226-2295: Ruff / Mypy / Coverage Baseline v0.

## Modified files
| File | Change |
|------|--------|
| pyproject.toml | Dev deps (ruff, mypy, pytest-cov, coverage); Ruff/Mypy/Coverage configs |
| scripts/remedy_lint.sh | New — runs Ruff + Mypy |
| scripts/remedy_coverage.sh | New — runs pytest with coverage |
| docs/quality-baseline-v0.md | New — baseline documentation |
| tests/orchestration/test_dogfood_run.py | +4 tests closing R-0119/R-0120 |
| .gitignore | +.coverage_reports/ |
| ~200 files | Ruff auto-fix: import ordering, unused imports, pyupgrade |
| packages/orchestration/proof_chain.py | Added missing Path import |
| packages/orchestration/repository_snapshot.py | Added TYPE_CHECKING EventPersistenceResult import |

## 30-task backlog
- Strict completed: 3/30 (Ruff baseline, Mypy baseline, Coverage baseline)
- Partially prepared: ~6/30
- Next: Review Bundle Structured Error Reporting v1

## Carried observations
- R-0119: Resolved (positive-path tests added)
- R-0120: Resolved (token guardrail test added)

## Status
Code + tests complete. Lint/Mypy green. Coverage 76.3%. Awaiting commit + PR + reviewer verdict.
