# Context — F111 Diff-only repair

## Active Branch
feature/f111-diff-only-repair, cut from main at 4e0b762e after PR #193 was
merged at the Open PR Gate. F111 is claimed `[~]` under Rule A5 as the first
`[ ]` line of docs/roadmap/STATUS.md (Package 1 Self-Use, Tier 2).

## Scope
In: what a repair round SENDS and ACCEPTS — a hunk selection helper
(line-range slicing with a configurable context margin), a versioned
unified-diff response schema, a fence pre-check before any apply, strict
apply with an all-or-nothing conflict fallback to the full-file round, and
per-round mode and token evidence. Tests under
tests/orchestration/test_diff_repair.py.

Out, per the feature file's Do-not-touch: repair round counts and policy,
applicator semantics, and session resume. No fuzzy diff application — v1
requires exact context matches, and no implementation may shell out to
`patch` or `git apply` with fuzz enabled. Deletions stay on the full-file
path in v1; new-file creation inside a diff is allowed if the path passes
fences.

## Constraints
- SPLIT rounds are mandatory: this feature touches packages/, and production
  code never merges self-certified
  (docs/agents/planner_reviewer_prompt.md §3).
- The main session writes nothing in the work tree; a delegated worker
  subagent makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never touch main.
- A round pushes after EVERY commit, not once at its last step (R-0289).
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/ also runs
  tests/docs/. The full suite runs only at the integration gate, with
  `-n auto`. Destructive and mutation checks run only inside a disposable
  git worktree, so resource safety stays intact and no background pytest
  process is ever left running.
- Build on what exists, do not duplicate it: `review_scope._parse_diff`
  already parses a unified diff into per-file new-file line ranges, and
  `source_apply._apply_hunks` is already a strict, non-fuzzy hunk applier
  that returns None on any context mismatch.

## Steps
R1 claim and state reset → R2 repair-path DECISION plus T001 hunk selection →
T002 response schema, fence pre-check and apply fallback → T003 wiring, mode
and token evidence → integration gate → closure.
