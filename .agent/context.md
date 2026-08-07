# Context — S1+S2 self-drive skill, build complete; PR #185 awaits the gate

## Active Branch
feature/selfdrive-skill, cut from main at df39c3fa. PR #185 is open and
NOT merged: it merges at the next work item's Open PR Gate, the
operator's manual-review window. F080 (roadmap mirror) is accepted and
on main; F103 remains the next roadmap feature and was never claimed by
this branch (D7). F254 is the designated rehearsal feature.

## Scope
This branch delivered only the self-drive build discipline:
docs/agents/self_drive_protocol.md, the remedy-self-drive skill, the
build-remedy-self command, the docs/README.md and .claude/README.md
registrations, three pins in tests/test_agent_tooling.py, the F080
closure-candidate sweep in docs/roadmap/STATUS_closure_protocol.md, the
proof-shape rule in docs/agents/planner_reviewer_prompt.md, and the
255-count repair in AGENTS.md + docs/README.md with its pin. Nothing
under packages/, apps/ or scripts/ was touched, and no STATUS.md line
was claimed.

## Constraints
- The next session must run its Open PR Gate FIRST: PR #185 is the one
  open, non-draft feature branch into main.
- Merges only at that gate; never force-push; never touch main.
- The main session writes nothing in the work tree; a delegated worker
  subagent makes every commit (D6).
- Verification on this branch was pytest, per file: tests/docs/,
  tests/test_agent_tooling.py, tests/ui_server/test_dashboard_contract.py,
  tests/orchestration/test_test_runner.py,
  tests/regression/test_resource_safety.py and the canary
  tests/cli/test_golden_path.py — all green at every round, re-run
  independently by the reviewer. No full-suite claim was made; resource
  safety unchanged, no background pytest.

## Steps
R1 build → R2 rule repair + Phase 0 dry run → R3 count repair + PR #185
→ R4 verdict persisted, build closed. Next: the S4 rehearsal on F254 in
a fresh session, which merges PR #185 at its Open PR Gate.
