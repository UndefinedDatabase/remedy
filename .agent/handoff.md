# Handoff — latest worker state (rewrite, never append)
Feature: F147 Golden-path CLI — IMPLEMENTATION COMPLETE (pending review)
Branch: feature/f147-golden-path-cli (4 commits, not yet pushed)

## Commits
  746455c chore(f147): claim feature, reset ledgers
  2e4a8c3 feat(f147): T001 remedy do mission — golden-path job creation
  48899b9 feat(f147): T002 remedy status — project status overview
  a99e220 feat(f147): T003 help pinning + golden-path smoke test

## Changed files
  | File | Change |
  |------|--------|
  | packages/core/models.py | +mission field on Job (additive, Optional) |
  | apps/cli/commands/do_cmd.py | bare-mission detection → _cmd_do_mission() |
  | apps/cli/commands/status_cmd.py | NEW — status handler with 4 sections |
  | apps/cli/command_catalog.py | +status group, +status.run entry, help reorder |
  | apps/cli/grouped.py | +status in _DEFAULT_COMMAND/_ALWAYS_INJECT |
  | apps/cli/commands/__init__.py | +status_cmd import/registration |
  | tests/cli/test_golden_path.py | 18 tests (8 T001 + 8 T002 + 2 T003) |
  | docs/roadmap/STATUS.md | F147 [~] in progress |
  | .agent/plan.md | T001-T003 all checked |

## Test baseline
  Pre-existing: 21 failed (all docs/missing-file; unrelated)
  New tests: 18/18 passed
  Regression: 0 new failures

## Open findings: 0
## Next: push branch, open PR, request review
(Rules: rewritten at every handback; <=60 lines.)
