# Handoff — latest worker state (rewrite, never append)
Feature: F081 remedy init
Round: T002 complete (config template + runtime detection)
Branch: feature/f081-remedy-init
Base: ef1e2e9 (main after PR #138 merge)
Last commit: e8daf18 (T002 implementation)

Changed files (T002):
| File | Change |
|---|---|
| apps/cli/commands/init_cmd.py | _CORE_TEMPLATE + _RUNTIME_ACTIVE + _RUNTIME_SKIP constants, _build_config(), handler restructured (config before registry, no early return) |
| tests/cli/test_init_cmd.py | TestInitConfig class: 7 new tests (no-marker, vite, uvicorn, existing-untouched, loader round-trip, output ordering) + _sha256 helper |
| .agent/decisions.md | T002 template-location + reorder decision recorded |
| .agent/plan.md | Status updated to T002 COMPLETE |

Verification (observed):
  pytest tests/cli/test_init_cmd.py -q: 11 passed (5 T001 + 6 T002)
  pytest tests/test_grouped_cli.py -q: 471 passed
  pytest tests/test_command_catalog.py -q: 3 failed (pre-existing), 15 passed
  ruff check: All checks passed
  Registry clean: 312 projects before, 312 after full test_init_cmd.py run
  Manual fixtures: Vite repo → [runtime] filled port 5173; bare repo → # [runtime] + [skipped]

Open findings: 0
Next: T003 (ignore-hygiene, summary block, --print-only, --json) or reviewer verdict
(Rules: rewritten at every handback; only the latest state lives here;
git history is the archive; ≤60 lines.)
