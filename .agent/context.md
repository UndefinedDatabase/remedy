# Context — F255 Teacher role

## Active Branch
feature/f255-teacher-role, cut from `main` at the merge commit of pull request
#207, which this round merged at the Open PR Gate. Self-drive session per
docs/agents/self_drive_protocol.md: the main session plans and reviews and
writes nothing in the work tree, one delegated worker per round makes every
commit.

## Scope
In: a fourth configured role `teacher`, resolved through the same `role_config`
mechanism as orchestrator, worker and reviewer; passive narration keyed to
ledger events (Stage 1: deterministic templates, zero tokens, offline);
on-demand Q&A (Stage 2) through the teacher role's own model over a small
context; three grounding sources kept separate and labelled; a teacher budget
pool reported apart from mission spend in the F103 ledger; a level dial; and the
CLI surfaces `remedy do watch --learn` and `remedy teach ask`.

Out, per the feature file's Non-goals: any write access to the run, mission
steering, and any influence on orchestrator, worker or reviewer decisions. The
cockpit panel ships with Tier 5 and not before.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/ and tests/orchestration/test_roadmap_index.py, and a round
  rewriting `.agent/` state also gates the four files that read that state
  live: tests/orchestration/test_test_runner.py,
  tests/ui_server/test_dashboard_contract.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource
  safety stays intact. Two pytest processes never run at once.
- THE FEATURE FILE IS A REGISTRATION STUB: Goal & Done, Scope and Non-goals and
  nothing else. R2 inventories the ground and R3 rules the shape and amends the
  file; no build round starts before that amendment lands.
- Repository-wide `ruff check` is RED at the claim and is NOT a gate (R-0364):
  the reviewer measured 26 errors at 538323e0 — 20 I001, 4 F401, 1 UP035 and
  1 F821. Ruff is gated scoped to the files a round touches, measured against
  the SAME files at the claim so a pre-existing error is not read as a new one.
- 176 findings are open once this round registers R-0600, all carried forward
  into the reset record per DECISION F057 D1. R-0403, R-0448, R-0482, R-0487,
  R-0490, R-0567, R-0568, R-0569, R-0570 and R-0571 stay routed to a paydown
  branch and are deliberately not fixed here.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
