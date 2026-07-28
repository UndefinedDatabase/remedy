# Plan — F251 Full-suite stabilization (R4, Ruling A)

> Progress marks added after the authored f251-r4-2 was applied verbatim
> (c1b3341, cmp 0); AGENTS.md requires plan.md to be current per commit.

## Goal
Persist Ruling A (2026-07-28) into the docs, then close F251: scope =
flake stabilization, DONE = the achieved state (three identical
full-suite runs, 0 churning, 0 quarantined); the 154 standing-red ids
and the 2 stopped F-A ids move to registered item F252.

## Checklist
- [x] T1_F251.md: scope-ruling section applied (f251-r4-3) — 8a7c8e7
- [x] ATOMIC ledger commit: T1_F252.md (f251-r4-4) + STATUS F252 line
      before F050 (f251-r4-5) + ROADMAP tier-1 entry (f251-r4-6) +
      TOTAL_FEATURES 251->252 — one commit, never split (R-0151
      lesson, extended to the feature-file count) — 7d4b586
- [x] Verify: FeatureLedger 4 passed; canary 42 passed; one full-suite
      run = 152, a strict SUBSET of the catalogued 154 — the delta is
      exactly the two documented D4 live_review ids, now green
- [ ] Handback; closure runs as its OWN round after the verdict

## Current Step
Handback. No closure work this round.

## Risks
- Ledger (files + STATUS) and pin move atomically, always.
- No D-class edits; F252 is registration only this round.
- plan.md stays current per commit (R-0153).
- D4 coupling is a substring check: the R4 verdict text contains the
  word "Steps" while stating live_review has no Steps section, which
  is what flipped the two ids. Documented, not touched — F252 item 7.
