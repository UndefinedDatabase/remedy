# Live Review — Process-Hardening v1 (chore round)

Branch: chore/process-hardening-v1 (PR #154)
LAST_REVIEWED_SHA: 11a417f
Finding IDs continue monotonically from R-0147. The F046 ledger is
archived in git history; this file is per-round working state.

## Findings

- R-0148 · Medium · round 1 — RESOLVED (round 2, commit b586e5c)
  docs/README.md integration_gate.md index row was transport-wrapped
  across two physical lines, breaking the markdown table. Fixed by
  applying the authored single row (.agent/authored/phv1-r2-2.md).
  Reviewer verified independently: row count 1, wrapped form absent,
  cumulative diff clean. Resolved by this reviewer-authored entry.

- R-0149 · Medium · round 1 — OPEN, routed to planning (spec conflict)
  (1) The mandatory per-commit tables of
  docs/agents/handback_template.md collide with the AGENTS.md ≤60-line
  handoff cap on rounds with more than ~5 commits (round 1 handoff:
  106 lines, documented deviation). (2) Discovered in round 2: the
  template's "every commit" rule cannot cover the final handoff commit
  itself (self-reference); trailing bookkeeping commits were grouped
  into one per-commit-attributed table — accepted deviation. Operator
  ruling (options a/b/c in the PH round-1 brief) pending; the accepted
  resolution will be authored as a template/AGENTS.md amendment in a
  later round. Not a merge blocker; this file carries the finding onto
  main when PR #154 merges.

## Verdicts

- Round 1 (89c4ef0..ac97215): FAIL — R-0148 (broken index table row).
  Full entry in git history (commit d3f929c); superseded by round 2.
- Round 2 (ac97215..11a417f): PASS — issued by the reviewer after
  independent verification: repair row applied from the committed
  authored file (ROW OK re-run, exit 0); live_review.md byte-matched
  the authored text plus exactly the ordered Done line (diff -u
  re-run, zero removals); canary re-run 42 passed; tree clean; PR #154
  untouched. Grouped bookkeeping table accepted as a documented
  deviation, folded into R-0149(2). Verification tier: round gate
  (scoped) + canary. LAST_REVIEWED_SHA = 11a417f. Merge of PR #154
  instructed (operator-approved exception, directive 2026-07-27).
