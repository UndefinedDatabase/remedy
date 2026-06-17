# Live Review — Steps 2366-2445: remedy.toml Configuration System v0 + Redaction Closure

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict;
a builder `Done:` marker is NOT reviewer `Resolved`).
Scope (ALLOWED): R-0121/R-0122/R-0123 closure; centralized remedy.toml config system;
ConfigSource/ConfigValue/ConfigKeySpec/RemedyConfig models; TOML loading with precedence;
config key registry; resolver migration (data_paths, ollama providers); config CLI commands
(list/get/sources/init/set/validate); command catalog registration; review bundle
config_summary.json section; docs; tests; `.agent/context.md` / `.agent/plan.md` backlog update.
Must NOT: provider execution; Claude/Pi/OpenCode/Ollama real integration; provider SDK;
auto-apply; auto-approval; auto-PR/git; direct repo mutation beyond config file writes;
shell=True; arbitrary shell; semantic memory; MemPalace; UI redesign; MCP; README rewrite;
ui_server split; orchestration subpackage split; review_bundle package split;
API key storage in config v0.
CONFIGURATION SYSTEM BLOCK — infrastructure, not features.
Timestamp: 2026-06-17

## Verdict (reviewer-owned)
Pending review.

## Prior block
Steps 2296-2365: PASS @ ef55c00 (R-0121/R-0122/R-0123 Low).
Merged to main via PR #81 -> b35a9f4.

## Changed files (Steps 2366-2445 @ a0fda56)
| File | What changed |
|------|-------------|
| packages/orchestration/config.py | NEW +313L: ConfigSource enum, ConfigValue/ConfigKeySpec/RemedyConfig dataclasses, TOML loading, key registry (9 keys), resolver, CLI API |
| packages/orchestration/redaction_patterns.py | +1/-1: R-0121 _SECRET_RE key=value captures value |
| packages/orchestration/review_bundle.py | +33/-6: R-0122/R-0123 wire ReviewBundleSectionError; config_summary.json section; REQUIRED_SECTIONS 40 |
| packages/orchestration/data_paths.py | +11/-4: migrate to config with direct env var first |
| packages/providers/ollama_builder/provider.py | +35/-43: migrate to config with direct env var checks |
| packages/providers/ollama_planner/provider.py | +38/-43: migrate to config with direct env var checks |
| apps/cli/commands/config_cmd.py | NEW +140L: CLI handlers for config group |
| apps/cli/commands/__init__.py | +2/-1: register config_cmd |
| apps/cli/command_catalog.py | +60: config group + 6 entries |
| docs/remedy-toml-configuration-system-v0.md | NEW +124L: architecture doc |
| docs/remedy-toml-user-guide.md | NEW +114L: user guide |
| tests/orchestration/test_config.py | NEW +282L: 46 unit tests |
| tests/cli/test_config_cmd.py | NEW +63L: 10 CLI subprocess tests |
| tests/orchestration/test_review_bundle.py | +3/-1: REQUIRED_SECTIONS 39->40 |
| .agent/context.md | Updated scope, backlog 5/30 |
| .agent/plan.md | Updated for 2366-2445 |

## Builder self-report
- R-0121 closed: `_SECRET_RE` key=value regex extended with `\s*=[^\s,;'"]*` to capture value
- R-0122 closed: `is_optional`/`is_bug` used in `ReviewBundleSectionError` construction
- R-0123 closed: `ReviewBundleSectionError` instantiated in `_build_section_safe`, stored on `ReviewBundleSection.structured_error`, used via `to_dict()` in `section_error_summary`
- Config system: 9 keys, 4 sources, TOML loading, precedence, fallback keys, validation
- Resolver migration: backward-compatible (env vars checked directly, config for TOML only)
- CLI: 6 commands with --json, catalog registered
- Review bundle: config_summary.json section added
- Tests: 56 new (46 config + 10 CLI), all passing
- Lint: Ruff + Mypy clean (188 files)
- Full suite: 6664 passed, 8 skipped, 1 pre-existing failure (test_project_brain unrelated)
- Backlog: 4/30 → 5/30

Next id: R-0124.
