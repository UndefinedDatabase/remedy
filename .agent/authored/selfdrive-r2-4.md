# Plan — S1+S2 self-drive skill (R2); R1 accepted

Branch: feature/selfdrive-skill, cut at df39c3fa after the Open PR Gate
merged PR #184. R1 PASSed at 54a99c8e: the protocol doc, the skill, the
`/build-remedy-self` command, the docs-index rows and the three test
pins are on the branch, and the F080 closure candidate is swept.
Rule A5 still names F103 (Token ledger, SQLite) as the next ROADMAP
feature; this track claims no STATUS line (D7).

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
R2 — two commits plus a read-only dry run:
(1) persist the R1 PASS verdict and finding R-0207 (own commit, first);
(2) fix R-0207 in docs/agents/planner_reviewer_prompt.md §4 item 9 and
    mark it Done in the live review;
(3) dry-run the protocol's own Phase 0 state probe end to end and record
    the RAW transcript in the handoff — the S1 acceptance item that R1
    did not cover.
Stop at the first red verification (AGENTS.md If Blocked).

## Next Steps
- R3: the PR round — push, `gh pr create`, no merge. No STATUS line, no
  evidence job, no review zip: this is not a roadmap feature (D7). The
  PR merges at the next work item's Open PR Gate.
- S4: rehearsal — F254 built end to end through the skill with the
  operator present; success = accepted with zero operator edits beyond
  starting it.
- Then normal feature flow through the skill, starting at F103.

## Risks
- Hard date 2026-08-12; today is 2026-08-07. R2+R3 are short rounds, so
  the rehearsal keeps roughly a three-day buffer.
- The reviewer's independence is weaker in one session than across two
  windows. Mitigated by D6 (delegated worker subagent, one per round) —
  not eliminated. The review zip stays the operator's out-of-band
  window.
- The dry run exercises Phase 0 only. Phases 1 and 2 are first exercised
  for real in the S4 rehearsal, with the operator watching.
