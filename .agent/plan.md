# Plan — Process-Hardening v1 (chore round, no feature)

## Goal
Move accepted process lessons (F016..F047) from session memory into the
workflow docs. Docs + index only. No production code, no tests, no
STATUS.md feature lines.

## Checklist
- [x] Round 1: 10 authored texts persisted; C1 C2 C3 C4 C5 C6 IDX applied;
      proofs PASS; PR #154 created (NOT merged). Verdict: FAIL (R-0148).
- [x] PH-2 Part 1: persist phv1-r2-1/phv1-r2-2; reset .agent/live_review.md
- [x] PH-2 Part 2: R-0148 — one-line integration_gate row in docs/README.md
- [x] PH-2 done-when: ROW OK, canary 42 passed, clean tree, pushed

## Current Step
PH-2 complete. R-0148 fixed in b586e5c and marked Done; handoff rewritten
per the template at 60 lines. Handed back for review of 89c4ef0..HEAD.

## Next Steps
Window 1 reviews 89c4ef0..HEAD and rules on R-0149. PR #154 stays open
and unmerged until instructed.

## Risks
- D1: PR #153 (F047 closure) stays open and untouched; it merges at the
  next feature's start (operator process-hardening directive 2026-07-27).
- D2: branch is chore/* not feature/* (same directive).
- D3: PR #154 stays unmerged in this block.
- R-0149 (handback template vs. AGENTS.md 60-line cap) is routed to
  planning; no in-round fix, not a merge blocker.
