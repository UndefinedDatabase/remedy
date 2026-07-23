# Handoff — latest worker state (rewrite, never append)
Feature: F081 remedy init
Round: T001 repair complete (R-0077, R-0078, R-0079 closed)
Branch: feature/f081-remedy-init
Base: ef1e2e9 (main after PR #138 merge)
Last commits: 0be3b05 (persist findings), 996e1b5 (R-0077), 08ed03a (R-0078), this commit (R-0079)

Changed files (repair round):
| File | Change |
|---|---|
| apps/cli/grouped.py | _DEFAULT_COMMAND + _ALWAYS_INJECT hoisted to module level |
| tests/test_grouped_cli.py | group-help parametrizations exempt _ALWAYS_INJECT |
| tests/cli/test_init_cmd.py | REMEDY_DATA_DIR isolation + mtime before/after proof |
| .agent/live_review.md | R-0077..R-0079 persisted, all Done |
| .agent/plan.md | T001 status updated |
| .agent/handoff.md | rewritten |

Verification (re-verified):
  pytest tests/test_grouped_cli.py -q: 471 passed, 0 failures
  pytest tests/cli/test_init_cmd.py -q: 5 passed
  pytest tests/test_command_catalog.py -q: 3 failed, 15 passed
    Pre-existing only: job.budget (read_metadata not in valid set),
    do.job-evidence (mutates but classified read_only),
    do.repair-attest (arg help substring match on "sk-"). NOT from F081.
  ruff check: All checks passed
  Registry clean: 312 projects before, 312 after full test_init_cmd.py run

Open findings: 0
Next: T002 (config template + runtime detection) or reviewer verdict
(Rules: rewritten at every handback; only the latest state lives here;
git history is the archive; ≤60 lines.)
