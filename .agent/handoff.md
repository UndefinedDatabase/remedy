# Handoff — latest worker state (rewrite, never append)
Feature: F081 remedy init
Round: T001 complete, T002–T003 pending
Branch: feature/f081-remedy-init
Base: ef1e2e9 (main after PR #138 merge)
Last commits: 38be878 (bundle-0), 4aee255 (T001 impl)

Changed files (T001):
| File | Change |
|---|---|
| apps/cli/commands/init_cmd.py | NEW — handler with preflight + registry |
| apps/cli/command_catalog.py | init group + init.run entry |
| apps/cli/commands/__init__.py | init_cmd registered |
| apps/cli/grouped.py | _DEFAULT_COMMAND + _ALWAYS_INJECT for init |
| tests/cli/test_init_cmd.py | NEW — 5 tests (create, idempotent, exit 4, name flag, subdir) |
| .agent/decisions.md | _DEFAULT_COMMAND pattern decision |
| docs/roadmap/STATUS.md | F081 claimed [~] |
| .agent/live_review.md | reset for F081 |
| .agent/plan.md | F081 T001–T003 |

Verification (T001):
  pytest tests/cli/test_init_cmd.py: 5/5 passed
  ruff check: clean
  Manual: fresh git repo → [created] exit=0; second run → [exists] exit=0
  Manual: non-git dir → exit=4, exact message, dir untouched
  CLI suite (tests/cli): same failure pattern as main (pre-existing doc tests)

Design note: _ALWAYS_INJECT set enables bare `remedy init` (no positional args
required) while preserving `remedy ui` behavior (requires job_id, shows help
when bare). See .agent/decisions.md.

Open findings: 0 (no reviewer round yet)
Next: T002 (config template + runtime detection) or reviewer round
(Rules: rewritten at every handback; only the latest state lives here;
git history is the archive; ≤60 lines.)
