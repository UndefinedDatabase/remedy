# Plan — amend0905-testlog (operator planning follow-up)

Branch: feature/amend0905-testlog, cut from `main` at b3224322 (PR #238
amend0905-vocab-rebuild merged); STATUS.md had 0 `[~]` lines and
`remedy plan next` proposed F259 at the cut.

## Goal

Turn the operator's hands-on tests.md run (Levels 0–7 against b2ee0a84 on
2026-09-05, ~/remedy-tests.log) into acceptance criteria: register the ten
measured findings A–J as R-0803..R-0812 in `.agent/live_review.md`, add
each acceptance sentence to its feature file (F260, F261, F268) under
`## Acceptance`, add the tests.md Level 4.1 line to F260, clarify D4 for
the catalog group `repo` and resolve R-0800 with that reference, and write
the data-root hygiene note for the operator into the handoff. PLANNING
ONLY: no product code, no tests, every edit presence-checked.

## Current Step

Commit sequence of the single round: (1) this plan · (2) findings
R-0803..R-0812 + R-0800 resolved + D4 clarification · (3) acceptance
lines in T2_F260 / T2_F261 / T2_F268 · (4) handoff rewrite. Then push,
PR, hosted run GREEN, checks read, merge (two separate commands), verify
on main.

## Next Steps

- Operator starts remedy-loop-feature; Rule A5 proposes F259.
- F259 → F260 → F261 → F266 → F268 → … in the D12 order; F260 now owes
  the data-root isolation, cockpit walk, ledger-row, fake-builder and
  narration acceptance; F261 the ui-session prune, blocked-findings
  display and one id-error shape; F268 the cost line, granularity
  ceiling and repo auto-attach.

## Risks

- Finding A's acceptance line arrives cut mid-sentence in the order
  (after `ls <data_root>/runs`); completed as an equal-count check and
  declared in R-0803 and the handoff.
- `grep -c 'R-08' .agent/live_review.md` must rise by exactly 10: every
  finding is one line and R-0800 is resolved IN its own line, not by a
  new `Done:` line.
