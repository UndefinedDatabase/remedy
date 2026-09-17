── STEP T001/F280 — round 20 ────────────────────────────────────────
Goal: Book round 19's independently-reviewed PASS, resolve R-0945
through R-0949, and write T2_F280.md's Built State section — closure
precondition 4 (STATUS_closure_protocol.md).

Bundle:
1. Book Gate: F280 R19 (PASS, no new finding); resolve R-0945, R-0946,
   R-0947, R-0948 and R-0949 (all repaired and independently confirmed
   by round 19's review).
2. Replace `.agent/plan.md` with the round-20 plan.
3. Append the reviewer's authored Built State section to
   `docs/roadmap/features/T2_F280.md`, verbatim, at the end of the file.
4. Write the handback and rewrite `.agent/handoff.md`.

Change: `docs/roadmap/features/T2_F280.md`, plus `.agent/live_review.md`
and `.agent/plan.md`. Nothing else — no code change this round.

Constraints:
- The Built State text is authored, verbatim; apply it byte-for-byte,
  do not paraphrase or summarize it further.
- Commit sequence: C1 (append Gate:F280 R19 + five Done: entries +
  replace plan.md, ONE commit) → C2 (append the Built State section,
  ONE commit) → C3 (handback commit). No commit lands after C3.

Done when (exact verification commands; run each, record real exit codes
and trimmed output):

G1 THE RECORD — after C1: `grep -cE '^Gate: F\d+ R\d+ — ' .agent/live_review.md`
reads 46; `grep -oE '^- (R-[0-9]{4}) — ' .agent/live_review.md | grep -oE 'R-[0-9]{4}' | sort -u | wc -l`
reads 146 (unchanged); `grep -oE '^Done: (R-[0-9]{4}) — ' .agent/live_review.md | grep -oE 'R-[0-9]{4}' | sort -u | wc -l`
reads 14; `wc -l < .agent/plan.md` reads 39 with exactly one each of
`## Goal`, `## Current Step`, `## Next Steps`, `## Risks`.

G2 THE BUILT STATE LANDS VERBATIM — after C2: `docs/roadmap/features/T2_F280.md`
ends with the authored section's exact bytes (`tail -c <n>` of the file
equals the authored source, `cmp` clean); `python3 -m pytest tests/docs/ -q`
reads all passed.

Handback: completion report + rewrite .agent/handoff.md.
──────────────────────────────────────────────────────────────────────
