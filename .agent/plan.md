# Plan — Steps 2366-2445: remedy.toml Configuration System v0 + Redaction Closure

## Goal
Add centralized remedy.toml config with safe source precedence, CLI visibility,
backward-compatible env var overrides. Close carried Low findings R-0121/R-0122/R-0123.

## Steps
- [x] Phase 0: Close R-0121 (key=value redaction gap), R-0122 (dead variables), R-0123 (unused dataclass)
- [x] Phase 1: Architecture doc (docs/remedy-toml-configuration-system-v0.md)
- [x] Phase 2: Core config module (packages/orchestration/config.py)
- [x] Phase 3: TOML loading with tomllib/tomli + precedence
- [x] Phase 4: ConfigKeySpec registry (9 keys)
- [x] Phase 5: Migrate resolvers (data_paths, ollama_builder, ollama_planner)
- [x] Phase 6: CLI commands (config list/get/sources/init/set/validate)
- [x] Phase 7: Command Catalog + handler registration (6 entries)
- [x] Phase 8: Review Bundle config_summary.json section
- [x] Phase 9: User guide doc
- [x] Phase 10: Backlog update (5/30 strict)
- [ ] Phase 11-13: Tests + coverage + lint + full suite + commit + PR

## Hard rules
No provider execution; no shell=True; no auto-apply/approve/PR/git; no secret storage in config.
