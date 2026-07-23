# Handoff — latest worker state (rewrite, never append)
Feature: scanner false-positive fix (R-0083 + R-0084 gap work)
Round: R-0084 DONE
Branch: feature/fix-path-scanner-false-positive
Base: 6dabdde (main after PR #140 merge)
HEAD: 5686d3b

Commits on branch:
  e3ae4de  fix(scanner): stop _contains_local_path false-positive on slash-command tokens
  d4e6764  chore: handoff rewrite for scanner fix Part 2
  40b0065  chore(review): persist R-0084
  5686d3b  fix(scanner): extend _REAL_ROOT_DIRS with macOS and Ubuntu root dirs

Changes:
  packages/orchestration/run_manifest.py — _neutralize_slash_commands() + _SLASH_CMD_RE + _REAL_ROOT_DIRS (extended: snap, applications, cores, library, private, system, users, volumes)
  tests/orchestration/test_run_manifest_ledger_identity_safety.py — TestSlashCommandFalsePositive: 3 safe + 6 unsafe parametrized cases
  .agent/live_review.md — R-0084 persisted and marked Done

Test results (raw):
  test_run_manifest_ledger_identity_safety.py — 77 passed (1.00s)
  test_review_subject_resolution.py — 27 passed (included in 77 total, separate file)
  ruff — 0 new findings (41 pre-existing UP037/I001/F401)

Open findings: 0
PR: draft, NOT merged (review-gated per operator instruction)
Next: Window 1 reviews 6dabdde..5686d3b
(Rules: rewritten at every handback; <=60 lines.)
