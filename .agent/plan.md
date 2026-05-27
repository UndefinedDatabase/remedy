# Plan

## Goal
Step 34.1: Dynamic Command Discovery Hardening + Provider-neutral Execution Foundation

## Status
COMPLETE — 2049 tests passing, smoke passed

## Completed

### Step 34 (v0 — PR #30)
- [x] command_discovery.py: CommandCandidate, discover_commands, select_best_test_candidate
- [x] Detectors: constitution, pyproject, package_json, makefile, justfile, taskfile, cargo, go
- [x] Risky token detection → high-risk candidates not auto-runnable
- [x] test_runner.py: uses discover_commands; _EXECUTION_SAFE_EXECUTABLES guard
- [x] TestRunRecord: 4 new provenance fields (command_source_type/path/purpose/confidence)
- [x] CLI: discover-commands subcommand (text + --json)
- [x] 1998 tests passing; smoke PASSED

### Step 34.1 (hardening)
- [x] command_discovery.py full rewrite with 13 detectors (added gradle, maven, dotnet, ruby, composer)
- [x] JS lockfile-based package manager selection (pnpm/yarn/bun/npm)
- [x] _SCAN_IGNORE_DIRS: centralized ignore list; _SCAN_MAX_DEPTH=2 bounded scan
- [x] _SOURCE_PRIORITY: deterministic priority (constitution=0 > makefile/justfile/taskfile=1 > manifests=2 > uncommon=3 > heuristic=9)
- [x] Dedup key: (purpose, argv, source_type) — same argv from different sources both kept
- [x] All source_path values repo-relative; constitution uses "(project-constitution)"
- [x] Makefile/Justfile recipe body inspection for risk
- [x] _EXECUTION_SAFE_EXECUTABLES expanded (pnpm, yarn, gradle, gradlew, mvn, mvnw, dotnet, rake, composer, poetry, uv, hatch)
- [x] permissions.py: removed "pytest only" wording
- [x] CLI discover-commands --json: schema v1 (version, selected_test_candidate, counts)
- [x] remedy_smoke.sh: multi-ecosystem target repo (Makefile, pnpm-lock.yaml, rust-lib/Cargo.toml, go-service/go.mod, jvm-app/build.gradle)
- [x] smoke step 6n: verifies version=1, multi-ecosystem sources, selected=constitution:make test, pnpm, relative paths
- [x] tests/test_command_discovery.py: 20 test classes (N–V added: JS lockfiles, Gradle, Maven, .NET/Ruby/Composer, source_path relative, ignore dirs, dedup, CLI schema v1, no provider coupling)
- [x] tests/test_remedy_smoke_script.py: 14 new Step 34.1 assertions
- [x] docs/architecture.md: updated detector table + schema docs
- [x] 2049 tests passing; smoke PASSED

## Next
Commit. Push. Open PR.
