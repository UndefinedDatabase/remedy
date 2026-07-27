# Plan — Process-Hardening v1 (chore round, no feature)

## Goal
Move accepted process lessons (F016..F047) from session memory into the
workflow docs. Docs + index only. No production code, no tests, no
STATUS.md feature lines.

## Checklist
- [x] Round 1: 10 authored texts persisted; C1 C2 C3 C4 C5 C6 IDX applied;
      proofs PASS; PR #154 created. Verdict: FAIL (R-0148).
- [x] Round 2 (PH-2): R-0148 fixed in b586e5c, ROW OK, canary 42 passed.
      Verdict: PASS at 11a417f.
- [x] PH-3 Part 1: phv1-r3-1 persisted; live_review.md replaced (IDENTICAL)
- [x] PH-3 Part 2: final handoff, push (+ one trim commit to hold the cap)
- [ ] PH-3 Part 3: merge PR #154, checkout main, pull --ff-only

## Current Step
PH-3 merge round. Verdict persisted, handoff final. Next and last action:
merge PR #154, then main. Nothing is committed after the merge.

## Next Steps
None on this branch. After the merge the branch is deleted and the session
ends; R-0149 rides onto main for a later operator ruling.

## Risks
- D1: PR #153 (F047 closure) stays open and untouched; it merges at the
  next feature's start (operator process-hardening directive 2026-07-27).
- D2: branch is chore/* not feature/* (same directive).
- D3 superseded: PR #154 merges this session under the operator-approved
  exception to the split_workflow.md merge policy — not a precedent.
- R-0149 (handback template vs. AGENTS.md 60-line cap, plus the handoff
  self-reference case) stays OPEN, routed to planning.
