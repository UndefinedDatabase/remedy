# Context — S1+S2 self-drive skill, R3 (final round); R2 accepted at 151733e1

## Active Branch
feature/selfdrive-skill, cut from main at df39c3fa after the Open PR
Gate merged PR #184. The PR for this branch is created in THIS round and
is not merged here. F080 (roadmap mirror) is accepted and on main; F103
remains the next roadmap feature and is NOT claimed here.

## Scope
R3 touches exactly: .agent/live_review.md, .agent/plan.md,
.agent/context.md, .agent/authored/selfdrive-r3-*.md, .agent/handoff.md,
AGENTS.md (one number), docs/README.md (one number) and
tests/docs/test_docs_consistency.py (one added pin). The R1 and R2
deliverables are accepted and are not reopened. Nothing under packages/,
apps/ or scripts/.

## Constraints
- No STATUS.md edit, no evidence job, no review zip: not a roadmap
  feature (D7). The PR is the end of the build.
- The main session writes nothing in the work tree; a delegated worker
  subagent makes every commit (D6).
- Merges only at the Open PR Gate; never force-push; never touch main.
  The PR created this round is NOT merged this round.
- Findings persist before they are fixed: R-0208 and R-0209 land in
  their own commit ahead of any correction, and a Done line is never
  applied before its fix is on disk.
- The ledger-count change and its test pin land in the SAME commit
  (R-0151).
- Verification is pytest, per file: tests/docs/ (AGENTS.md and
  docs/README.md are PRIMARY_DOCS there),
  tests/ui_server/test_dashboard_contract.py,
  tests/orchestration/test_test_runner.py and
  tests/regression/test_resource_safety.py for the .agent contract
  readers, tests/test_agent_tooling.py for the R1 pins, and the canary
  tests/cli/test_golden_path.py. No background pytest; resource safety
  unchanged.

## Steps
Commit 1 state + findings R-0208/R-0209 → commit 2 the two count fixes,
the new pin and the three live-review pairs → push → PR created, not
merged → handoff rewrite. S4 rehearsal follows in a fresh session.
