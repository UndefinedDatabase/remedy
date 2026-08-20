# Context — F086 Release capability

## Active Branch
feature/f086-release-capability, cut from `main` at 76661dc1, the merge commit
of PR #206, which the operator merged manually at the Open PR Gate. Self-drive
session per docs/agents/self_drive_protocol.md: the main session plans and
reviews and writes nothing in the work tree, one delegated worker per round
makes every commit.

## Scope
In: shipping Remedy as a normal installable tool — a single wheel with the
console entrypoint `remedy`, the built UI carried as package data, asset
resolution that works from an installed wheel as well as from a checkout, a
single-sourced version with build info behind `remedy --version`, a release CI
stage gated on tag/version agreement and on a changelog section, a wheel-size
budget, and a fresh-virtualenv install smoke.

Out, per the feature file's Do-not-touch: auto-publishing, installers beyond
pip, update mechanisms and the license choice. Publishing to an index stays a
HUMAN command in v1; automating the final upload is explicitly rejected for this
feature. No wording anywhere may claim the wheel ships assets it does not.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/ and tests/orchestration/test_roadmap_index.py, and a round
  rewriting `.agent/` state also gates the four files that read that state live:
  tests/orchestration/test_test_runner.py,
  tests/ui_server/test_dashboard_contract.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource
  safety stays intact. Two pytest processes never run at once.
- Repository-wide `ruff check` is RED at the claim and is NOT a gate (R-0364):
  the reviewer measured 26 errors at 76661dc1 — 20 I001, 4 F401, 1 F821 and 1
  UP035. Ruff is gated scoped to the files a round touches, measured against the
  SAME files at 76661dc1 so a pre-existing error is not read as a new one.
- A wheel build runs npm. Every such spawn goes through the F085 `exec_guard`
  seam rather than a bare subprocess, and a round that adds one says so.
- 152 findings are open at the claim, carried forward into the reset record per
  DECISION F057 D1. R-0403, R-0448, R-0482, R-0487, R-0490, R-0567, R-0568,
  R-0569, R-0570 and R-0571 are routed to a paydown branch and are deliberately
  not fixed here.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
