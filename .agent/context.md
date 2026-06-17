# Context

## Active Branch
feature/steps-2366-2445-remedy-toml-configuration-system-v0-redaction-closure
(forked from clean main at a9e6244 after PR #81 merged).

## Scope
Steps 2366-2445: remedy.toml Configuration System v0 + Redaction Closure.

## Modified files
| File | Change |
|------|--------|
| packages/orchestration/redaction_patterns.py | R-0121: _SECRET_RE key=value now captures value |
| packages/orchestration/review_bundle.py | R-0122/R-0123: ReviewBundleSectionError wired into production; config_summary.json section added; REQUIRED_SECTIONS 39->40 |
| packages/orchestration/config.py | NEW — ConfigSource, ConfigValue, ConfigKeySpec, RemedyConfig, load/resolve/get API |
| packages/orchestration/data_paths.py | Migrated resolve_data_root() to config system |
| packages/providers/ollama_builder/provider.py | Migrated _resolve_model + constructor to config system |
| packages/providers/ollama_planner/provider.py | Migrated _resolve_model + constructor to config system |
| apps/cli/commands/config_cmd.py | NEW — CLI handlers for config list/get/sources/init/set/validate |
| apps/cli/commands/__init__.py | Added config_cmd to handler registry |
| apps/cli/command_catalog.py | Added config group + 6 command entries |
| docs/remedy-toml-configuration-system-v0.md | NEW — architecture doc |
| docs/remedy-toml-user-guide.md | NEW — user guide |

## 30-task backlog
- Strict completed: 5/30 (Ruff, Mypy, Coverage baselines + Review Bundle Structured Error Reporting v1 + remedy.toml Config System v0)
- Partially prepared: ~7/30
- Next: README Current-State Refresh v1 OR Structured Logging v0

## Resource safety
All pytest runs use scripts/remedy_pytest.sh (flock-serialized, timeout-bounded).
No shell=True. No background pytest.

## Carried observations
- R-0121/R-0122/R-0123 resolved in this block

## Status
Implementation complete. Awaiting tests + lint + full suite + commit.
