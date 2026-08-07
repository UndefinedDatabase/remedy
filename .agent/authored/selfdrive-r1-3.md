# Context — S1+S2 self-drive skill; F080 closed, PR #184 merged

## Active Branch
feature/selfdrive-skill, cut from main after the Open PR Gate merged
PR #184 (the ADR-0001 cycle-cap micro-round). F080 (roadmap mirror) is
accepted and on main; F103 remains the next roadmap feature and is NOT
claimed by this branch.

## Scope
Only the self-drive build discipline: docs/agents/self_drive_protocol.md,
.claude/skills/remedy-self-drive/SKILL.md,
.claude/commands/build-remedy-self.md, the docs/README.md index rows,
the .claude/README.md contents line, the pins appended to
tests/test_agent_tooling.py, plus the F080 closure-candidate sweep in
docs/roadmap/STATUS_closure_protocol.md and .agent/candidates.md.
Nothing under packages/ or apps/ is touched.

## Constraints
- No STATUS.md edit: this is not a roadmap feature (DECISION D7), and
  the 250-item ledger pins in tests/docs/ would reject an invented line.
- The main session writes nothing in the work tree; a delegated worker
  subagent makes every commit (DECISION D6).
- Merges only at the Open PR Gate; never force-push; never touch main.
- Verification is pytest, per file: tests/docs/ (docs/roadmap changed),
  tests/test_agent_tooling.py (the new pins), and the canary
  tests/cli/test_golden_path.py every round. Resource safety unchanged —
  no background pytest, no direct writes outside the branch.

## Steps
Gate #184 and branch → commit 1 state + candidate sweep + closure
protocol → commit 2 protocol doc + docs index → commit 3 skill +
command + .claude/README → commit 4 test pins → push → handoff.
