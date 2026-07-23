# Handoff — latest worker state (rewrite, never append)
Feature: F081 remedy init
Round: CLOSURE-PREP complete
Branch: feature/f081-remedy-init
Base: ef1e2e9 (main after PR #138 merge)
Last commit: c4cd7ab (resolve R-0077..R-0080)

Changed files (closure-prep, uncommitted):
| File | Change |
|---|---|
| tests/cli/test_init_cmd.py | +1 test: test_in_repo_data_dir_ignored (23 total) |
| .agent/decisions.md | duplication tradeoff note for _ensure_ignore_entry |
| docs/roadmap/features/T0_F081.md | Added ## Built State section (T001–T003) |
| .agent/handoff.md | This rewrite (closure-ready) |

Verification (observed, this round):
  pytest tests/cli/test_init_cmd.py -q: 23 passed
  pytest tests/test_grouped_cli.py -q: 471 passed
  pytest tests/test_command_catalog.py -q: 3 failed (pre-existing: job.budget,
    do.job-evidence, do.repair-attest), 15 passed
  ruff check: All checks passed
  Registry clean: 312 before, 312 after
  Evidence job: not applicable (F081 is CLI feature, no job-scoped evidence;
    no feature-level evidence export machinery exists)

Cumulative F081 deliverables:
  apps/cli/commands/init_cmd.py — full handler (T001–T003)
  apps/cli/command_catalog.py — init.run entry with --print-only, --json
  apps/cli/grouped.py — _ALWAYS_INJECT, _DEFAULT_COMMAND (T001-REPAIR)
  tests/cli/test_init_cmd.py — 23 tests
  tests/test_grouped_cli.py — _HELP_CONTRACT_GROUPS exemption (T001-REPAIR)
  packages/runtimes/runtime_config.py — unchanged (used, not modified)
  .agent/live_review.md — R-0077..R-0080 all Resolved
  .agent/plan.md — T001–T003 COMPLETE
  .agent/decisions.md — 4 decisions
  docs/roadmap/features/T0_F081.md — Built State added

Open findings: 0
Reviewer resolutions: R-0077..R-0080 all applied and confirmed
Next: commit closure-prep changes, push, build review ZIP
(Rules: rewritten at every handback; only the latest state lives here;
git history is the archive; ≤60 lines.)
