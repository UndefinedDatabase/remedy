# Live Review — Steps 2366-2445 Closure: remedy.toml Config Safety + Diagnostics Fixes

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict;
a builder `Done:` marker is NOT reviewer `Resolved`).
Scope (ALLOWED): R-0124 through R-0130 closure; quoted secret redaction; unknown key rejection;
config diagnostics; path redaction; CLI completeness; registry completeness; Changed Line Map.
Must NOT: provider execution; Claude/Pi/OpenCode/Ollama real integration; provider SDK;
auto-apply/approve/PR/git; shell=True; semantic memory; MemPalace; UI redesign; MCP; README rewrite;
package splits.
CLOSURE BLOCK — safety hardening of config system, not new features.
Timestamp: 2026-06-17

## Verdict (reviewer-owned)
**PASS** @ ceebe13 (2 commits, PR #82). All findings resolved.
R-0124 Resolved. R-0125 Resolved. R-0126 Resolved. R-0127 Resolved.
R-0128 Resolved. R-0129 Resolved. R-0130 Resolved.

## Prior block
Steps 2296-2365: PASS @ ef55c00. Merged to main via PR #81 -> b35a9f4.
Steps 2366-2445 initial: PASS WITH RISKS @ a0fda56 (pre-closure, R-0121/R-0122/R-0123 resolved).

## Findings — Steps 2366-2445 Closure

### R-0124 — Quoted secret redaction (Resolved)
`_SECRET_RE` pattern updated to `(?:"[^"]*"|'[^']*'|[^\s,;'"]*)`.
Verified:
- `api_key='mysecret'` → `[REDACTED]` (was leaking `'mysecret'`)
- `api_key="mysecret"` → `[REDACTED]` (was leaking `"mysecret"`)
- `password='hunter2'` → `[REDACTED]` (was leaking `'hunter2'`)
- `credential='x y z'` → `[REDACTED]` (spaced quoted value captured)
- `api_key=mysecret123` → `[REDACTED]` (unquoted still works)
- `No secrets configured` → unchanged (no overblocking)
- Comma case `api_key=secret,next` → `[REDACTED],next`: `,next` is delimiter context, not secret value.
  If value contains comma, quoting captures it: `api_key="secret,next"` → `[REDACTED]`. Acceptable.
Test: `TestRedactionClosure::test_r0124_quoted_key_value_redacted` PASS.

### R-0125 — Unknown/secret-like config keys cannot be written (Resolved)
`set_config_value` now rejects unknown keys (`spec is None → ValueError`) and secret keys.
Verified: `set_config_value(path, 'totally.unknown.key', 'value')` → `ValueError: Unknown config key`.
CLI `_cmd_config_set` wraps `set_config_value` in try/except — same rejection propagated.
Tests: `TestSetConfigValueGuards` (3 tests) + `test_config_set_rejects_unknown` CLI test. All PASS.

### R-0126 — Config diagnostics are not silent (Resolved)
1. `_load_toml` now accepts `diagnostics` list; malformed TOML appends parse error message.
   Verified: `"Malformed TOML in /tmp/...: Expected '=' after a key..."` in diagnostics.
2. `load_config` checks unknown keys in both project and user TOML against `_KEY_SPEC_MAP`.
   Verified: `"Unknown key in /tmp/...: bogus_key"` in `load_report.warnings`.
3. `validate_config` still catches type mismatches (unchanged, already worked).
4. All diagnostics surface via `ConfigLoadReport.warnings` — visible in CLI `config validate` and
   review bundle `config_summary.json`.
Tests: `TestLoadDiagnostics` (3 tests). All PASS.

### R-0127 — Public path redaction (Resolved)
`_redact_abs_path` replaces home-relative paths with `~/...`, other absolute with `<absolute-path-redacted>`.
Applied in:
- `RemedyConfig.to_summary_dict()` → `project_path` and `user_path`
- `_cmd_config_sources` → JSON and text output (4 references)
Verified: `to_summary_dict()["load_report"]["user_path"]` = `~/.config/remedy/remedy.toml` (was `/home/decodeux/...`).
Tests: `TestPathRedaction` (2 tests). All PASS.

### R-0128 — CLI completeness and cwd-isolated tests (Resolved)
1. `config show` added as alias for `config list` — catalog entry + handler mapping.
2. `config init --json` added — JSON output `{"created": "path"}` or `{"error": "msg"}`.
3. `config set --json` added — JSON output `{"key": k, "value": v, "path": p}` or `{"error": "msg"}`.
4. `config init --path` added — `ArgDef("--path", ...)` in catalog, handler uses `getattr(args, "path")`.
5. `config set --path` added — same pattern.
6. Tests now use `--path` for isolation (no cwd dependency).
Tests: `test_config_show_alias`, `test_config_init_json`, `test_config_set_json` CLI tests. All PASS.

### R-0129 — Registry completeness (Resolved)
Registry expanded from 9 → 18 keys:
- Original: data_dir + 8 ollama keys
- Added: ui.host, ui.port, tests.pytest_timeout_seconds, quality.coverage_fail_under, logging.level
- Added env_only: claude_enabled, opencode_enabled, pi_dev_enabled, external_memory_enabled
Provider flags are `env_only=True` — cannot be stored in config files (safe).
`write_toml_template` updated with all new sections.
Test: `TestConfigKeySpec::test_all_specs_populated` asserts >= 18 keys. PASS.

### R-0130 — Changed Line Map accuracy (Resolved)
`.agent/context.md` now has two tables:
1. "Modified files (closure commit)" — 6 entries including test files and all closure-changed files.
2. "Prior modified files (initial commit a0fda56)" — 8 entries for original commit files.
All 14 non-agent files accounted for across both tables.

## Test results (closure @ ceebe13)
| Suite | Result |
|-------|--------|
| compileall | CLEAN |
| ruff | CLEAN |
| tests/orchestration/test_config.py | 55 PASS |
| tests/cli/test_config_cmd.py | 14 PASS |
| tests/orchestration/test_review_bundle.py | 90 PASS |
| Full suite (-k "not test_full_chain_order") | 6677 PASS, 8 skipped, 0 fail |

## Hard blocker checks
| Check | Result |
|-------|--------|
| config CLI accepts unknown keys | FIXED — rejects with ValueError |
| malformed config silently ignored | FIXED — diagnostics in load_report.warnings |
| public surfaces leak private paths | FIXED — _redact_abs_path applied |
| env precedence broken | N/A — env > project > user > default (verified in prior review) |
| REMEDY_DATA_DIR compat breaks | N/A — env checked directly first (verified in prior review) |
| provider/network execution | CLEAN — no imports of ollama/httpx/requests in config.py |
| shell=True | CLEAN — not present |
| CLM missing/misleading | FIXED — all files listed |
| German content | CLEAN — English only |
| PASS without checking uncommitted changes | CHECKED — only .agent/live_review.md (reviewer-owned) |

## Uncommitted changes at review time
Only `.agent/live_review.md` (reviewer-owned). No builder uncommitted changes.

## Reviewer audit log
- Closure review opened for R-0124 through R-0130 against a0fda56.
- Initial evaluation: FAIL — 3 HIGH (R-0125, R-0126, R-0127) + 1 MEDIUM (R-0124).
- Builder commit ceebe13 detected: closure fixes for all findings.
- Re-evaluated all 7 findings against ceebe13:
  - R-0124: Regex now matches quoted values. Verified with 7 test cases. RESOLVED.
  - R-0125: Unknown keys rejected by set_config_value and CLI. Verified. RESOLVED.
  - R-0126: Malformed TOML produces diagnostics. Unknown keys flagged at load time. RESOLVED.
  - R-0127: Absolute paths redacted in to_summary_dict and CLI sources. Verified. RESOLVED.
  - R-0128: show alias + --json + --path added. Verified via tests. RESOLVED.
  - R-0129: 18 keys registered. Provider flags env_only. RESOLVED.
  - R-0130: CLM includes all files across both tables. RESOLVED.
- All required tests pass (6677/6677).
- Verdict: PASS @ ceebe13.
