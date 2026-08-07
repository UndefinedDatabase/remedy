# Plan — S1+S2 self-drive skill (R3, final round); R1+R2 accepted

Branch: feature/selfdrive-skill, cut at df39c3fa after the Open PR Gate
merged PR #184. R1 PASSed at 54a99c8e (protocol doc, skill,
build-remedy-self command, docs-index rows, three test pins, F080
candidate swept). R2 PASSed at 151733e1 (R-0207 fixed in
planner_reviewer_prompt.md §4 item 9; Phase 0 of the shipped protocol
dry-run green end to end). Rule A5 still names F103 (Token ledger,
SQLite) as the next ROADMAP feature; this track claims no STATUS line
(D7).

## Goal
Build the one-session build discipline so the operator can start Claude
Code, invoke ONE skill, and have a feature built end to end with the
review discipline intact — deliverables per .agent/selfdrive_package.md
S1 (the skill) and S2 (the guardrails).

## Operator constraint (verbatim)
From 2026-08-13 the operator reaches this machine ONLY via SSH from a
phone. Starting Claude Code and invoking ONE skill must be the only
required touchpoint. Target: operational and rehearsed by 2026-08-12.

## Current Step
R3 — the final round of the build:
(1) persist the R2 PASS verdict and findings R-0208 + R-0209 (own
    commit, before any fix);
(2) fix both: the ledger count in AGENTS.md and docs/README.md, the
    matching pin in tests/docs/test_docs_consistency.py, and the D7
    wording — count change and pin in the SAME commit (R-0151);
(3) push and create the PR. The PR is NOT merged: it merges at the next
    work item's Open PR Gate, which is the operator's review window.
Stop at the first red verification (AGENTS.md If Blocked).

## Next Steps
- S4 rehearsal: F254 built end to end through the skill with the
  operator present. Success = accepted with zero operator edits beyond
  starting it. This is the acceptance test of S1+S2, and it needs a
  fresh session.
- Then normal feature flow through the skill, starting at F103.

## Risks
- Hard date 2026-08-12; today is 2026-08-07. With R3 closing the build,
  the rehearsal keeps a buffer of roughly four days including one
  repair round.
- Phases 1 and 2 of the protocol have not run for real yet — only
  Phase 0 is proven. The rehearsal is where they are first exercised,
  deliberately with the operator watching.
- The reviewer's independence is weaker in one session than across two
  windows. Mitigated by D6 (delegated worker subagent, one per round) —
  not eliminated. The review zip stays the operator's out-of-band
  window.
