# Handoff — latest worker state (rewrite, never append)
Feature: F081 remedy init
Round: T002 repair complete (R-0080 closed)
Branch: feature/f081-remedy-init
Base: ef1e2e9 (main after PR #138 merge)
Last commits: e8daf18 (T002), 1d3d081 (persist R-0080), bf04005 (fix R-0080)

Changed files (T002 + R-0080 repair):
| File | Change |
|---|---|
| apps/cli/commands/init_cmd.py | [remedy] → remedy.toml, [runtime] → .remedy/config.toml; _build_runtime_config; handler: config→runtime→registry, per-step report |
| tests/cli/test_init_cmd.py | 14 tests (5 T001 + 9 T002): runtime assertions on .remedy/config.toml, resolve_spec source="config" proof, existing-runtime-untouched |
| .agent/live_review.md | R-0080 persisted + Done |
| .agent/decisions.md | T002 template location + R-0080 split-file decision |
| .agent/plan.md | Status: T002 COMPLETE |

Verification (observed):
  pytest tests/cli/test_init_cmd.py -q: 14 passed (5 T001 + 9 T002)
  pytest tests/test_grouped_cli.py -q: 471 passed
  pytest tests/test_command_catalog.py -q: 3 failed (pre-existing), 15 passed
  ruff check: All checks passed
  Registry clean: 312 before, 312 after full test_init_cmd.py run
  Manual fixture (Vite repo):
    remedy.toml: [remedy] only, NO [runtime]
    .remedy/config.toml: [runtime] cmd/port filled
    resolve_spec: source='config', port=5173

Open findings: 0
Next: T003 (ignore-hygiene, summary block, --print-only, --json) or reviewer verdict
(Rules: rewritten at every handback; only the latest state lives here;
git history is the archive; ≤60 lines.)
