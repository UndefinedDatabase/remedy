# Context — F085 Sandbox hardening (stage 1)

## Active Branch
feature/f085-sandbox-hardening, cut from origin/main at a5a70621 after the F083
closure PR #202 and the operator amendment PR #203 were both merged. Self-drive
session per docs/agents/self_drive_protocol.md: the main session plans and
reviews and writes nothing in the work tree, one delegated worker per round
makes every commit.

## Scope
In: stage-1 containment for builder-, test- and DoD-spawned subprocesses — a
common `exec_guard` seam carrying POSIX resource limits, a wall timeout distinct
from the provider timeouts, output-size caps, a cwd pinned inside the worktree,
an environment allowlist, and a default-deny network posture for build and test
commands, plus the honest limitations document and its README link. The tripped
limit becomes an additive `resource_limit` postmortem class.

Out, per the feature file's Do-not-touch: container isolation, provider
transport timeouts, and fence semantics. Windows is explicitly out of scope for
stage 1 and is documented as such. No wording anywhere — code comments included
— may claim more containment than is enforced.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/, and a round rewriting `.agent/` state also gates the four files
  that read that state live: tests/orchestration/test_test_runner.py,
  tests/ui_server/test_dashboard_contract.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource
  safety stays intact.
- Repository-wide `ruff check` is RED on main with pre-existing errors and is
  NOT a gate (R-0364); ruff is gated scoped to the files a round touches,
  measured against the SAME files at origin/main so a pre-existing error is not
  read as a new one.
- Two AST guards already constrain this feature's target files and bind every
  seam order: `test_no_subprocess_in_discovery_module` forbids `subprocess.run`
  in packages/orchestration/command_discovery.py, and
  `test_no_shell_true_in_orchestration` forbids `shell=True` anywhere in
  packages/orchestration/*.py.
- 104 findings are open at the claim, carried forward into the reset record per
  DECISION F057 D1. R-0403, R-0448, R-0482, R-0487 and R-0490 are routed to a
  paydown branch and are deliberately not fixed here.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
