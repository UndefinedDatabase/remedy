# Plan — Amendment round amend0805-v3

Branch: feature/amend0805-v3 (F075 PR #179 merged at Open PR Gate)

## Goal
Apply operator-relayed amendment round amend0805-v3 (docs/planning only;
replaces amend0804 v1/v2, neither ran). Items B1–B5 (roadmap), C1
(reviewer conventions), D1–D2 (doc drift), E1–E2 (workflow docs +
candidates note). Single-session permitted per §3 Named Round Types.
Not a feature claim; candidates block condition does not fire.

## Current Step
Presence checks done — all 10 items absent, all live. Applying in
order B → C → D → E; commit per part, push, PR, handback with
item-status table.

## Next Steps
- Part B: STATUS.md (F254 line + Milestone R1), new T2_F254.md,
  appends to T12_F253.md / T17_F243.md / T2_F103.md
- Part C: reviewer_conventions.md specified-route-exercised rule
- Part D: self_run_gauntlet.py docstring, claude_agent/__init__.py
- Part E: planner_reviewer_prompt.md Laufzeit row + definition;
  candidates.md R-0199 operator-priority note
- Rewrite handoff.md at handback

## Risks
- No product code or order/template edits allowed in this round.
- After this round: F079 per Rule A5; candidates.md still non-empty
  (block condition at F079 claim). ADR-0001 still awaits a human.
