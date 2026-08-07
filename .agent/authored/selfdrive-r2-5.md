# Context — S1+S2 self-drive skill, R2; R1 accepted at 54a99c8e

## Active Branch
feature/selfdrive-skill, cut from main at df39c3fa after the Open PR
Gate merged PR #184. No PR exists for this branch yet — it is created in
R3. F080 (roadmap mirror) is accepted and on main; F103 remains the next
roadmap feature and is NOT claimed here.

## Scope
R2 touches exactly: .agent/live_review.md, .agent/plan.md,
.agent/context.md, .agent/authored/selfdrive-r2-*.md,
.agent/handoff.md, and docs/agents/planner_reviewer_prompt.md (the
R-0207 fix). Nothing else — the R1 deliverables are accepted and are not
reopened. Nothing under packages/, apps/ or scripts/.

## Constraints
- No STATUS.md edit and no review zip: not a roadmap feature (D7).
- The main session writes nothing in the work tree; a delegated worker
  subagent makes every commit (D6).
- Merges only at the Open PR Gate; never force-push; never touch main.
- Findings persist before they are fixed: the R-0207 entry lands in its
  own commit ahead of the fix.
- Verification is pytest, per file: tests/docs/ (docs/ changed),
  tests/ui_server/test_dashboard_contract.py,
  tests/orchestration/test_test_runner.py and
  tests/regression/test_resource_safety.py for the .agent contract
  readers, tests/test_agent_tooling.py for the R1 pins, and the canary
  tests/cli/test_golden_path.py. No background pytest; resource safety
  unchanged.

## Steps
Commit 1 state + finding R-0207 → commit 2 the planner-prompt fix and
the Done flip → read-only Phase 0 dry run, raw transcript into the
handoff → push → handback. The PR is R3, not this round.
