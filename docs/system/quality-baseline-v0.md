# Quality Baseline v0

Established in Steps 2226-2295. This is a pragmatic starting point, not strict mode.

## Tools

| Tool | Version | Purpose |
|------|---------|---------|
| Ruff | >=0.15 | Linting + import sorting |
| Mypy | >=2.1 | Type checking (permissive baseline) |
| pytest-cov | >=7.1 | Coverage measurement |
| coverage | >=7.0 | Coverage reporting + JSON artifacts |

All tools listed in `pyproject.toml` under `[project.optional-dependencies].dev`.

## Commands

```bash
# Lint (Ruff + Mypy)
scripts/remedy_lint.sh          # both
scripts/remedy_lint.sh ruff     # ruff only
scripts/remedy_lint.sh mypy     # mypy only

# Coverage (separate from normal test runs)
scripts/remedy_coverage.sh                      # full
scripts/remedy_coverage.sh tests/orchestration  # scoped

# Normal tests (no coverage overhead)
scripts/remedy_pytest.sh tests/ -q
```

## Ruff

Rules enabled: `E`, `F`, `W`, `I`, `UP` (errors, pyflakes, warnings, isort, pyupgrade).

Rules deferred with documented reasons:
- `E501` (line-too-long) — 330 hits, mostly in catalog descriptions and compact data; needs line wrapping pass
- `E702` (multiple-statements-on-semicolon) — 136 hits in compact test/data patterns; style choice
- `E741` (ambiguous-variable-name) — 30 hits (`l`, `I` as loop vars); existing patterns
- `F841` (unused-variable) — 47 hits; many are intentional (capturing return values for assertions)
- `B`, `C90`, `PL`, `ANN` — not enabled yet; each would require dedicated tightening pass

Per-file ignores for intentional patterns documented in `pyproject.toml`.

Auto-fixed on first run: 1669 issues (import ordering, unused imports, deprecated typing, pyupgrade).

Manual fixes: unused `_safe_path_label` import, unused `resolve_data_root` import, unused `export_project_summary_json` import, missing `Path` import in proof_chain.py, missing `EventPersistenceResult` TYPE_CHECKING import in repository_snapshot.py.

## Mypy

Strictness: permissive baseline.
- `ignore_missing_imports = true`
- `check_untyped_defs = false`
- `disallow_untyped_defs = false`
- `explicit_package_bases = true` (needed for namespace packages)

42 modules excluded with `ignore_errors = true` (144 errors total). Top offenders:
- `ui_view_model` (24 errors) — complex dict/union typing
- `agent_loop` (12 errors) — dynamic dispatch
- `worker_queue` (11 errors) — generic container typing

These require architectural typing work beyond this baseline. Listed in `pyproject.toml` `[[tool.mypy.overrides]]`.

## Coverage

Baseline: **76.3%** (branch coverage enabled).

`fail_under = 75.0` (rounded down from 76.3% for safety margin).

### Top 10 coverage gaps

| Coverage | Missing lines | File |
|----------|--------------|------|
| 5.2% | 107 | apps/cli/commands/contract_cmd.py |
| 5.9% | 127 | apps/cli/commands/test_cmds.py |
| 6.7% | 147 | apps/cli/commands/dogfood_cmd.py |
| 6.8% | 80 | apps/cli/commands/snapshot_cmds.py |
| 6.9% | 113 | apps/cli/commands/route_policy_cmd.py |
| 7.6% | 99 | apps/cli/commands/provider_cmd.py |
| 9.5% | 93 | apps/cli/commands/self_cmd.py |
| 10.9% | 70 | apps/cli/commands/event.py |
| 11.1% | 48 | apps/cli/commands/overnight_cmd.py |
| 11.2% | 83 | apps/cli/commands/external_builder_cmd.py |

All gaps are in CLI command handlers. Core orchestration modules range 72-98%.

### Known exclusions

- `apps/ui/*` — frontend TypeScript, not Python
- `tests/*` — test code itself
- `__pycache__/*`

### Coverage artifacts

JSON report: `.coverage_reports/coverage.json` (gitignored).

## Future tightening

1. Enable `E501` with line wrapping for catalog descriptions
2. Enable `B` (bugbear) rules
3. Type-annotate top 10 mypy-excluded modules
4. Add CLI handler tests to close the coverage gap
5. Consider `C90` (mccabe complexity) for new code
6. Enable `check_untyped_defs` in mypy after type annotation pass

## How future agents should use the scripts

1. Before every commit: `scripts/remedy_lint.sh` must pass
2. Before every PR: `scripts/remedy_pytest.sh` must pass
3. Periodically: `scripts/remedy_coverage.sh` to check coverage trends
4. Coverage JSON can be diffed between branches to detect regressions
