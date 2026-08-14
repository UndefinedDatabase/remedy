── SESSION CLOSE 3 — F077 Autonomy watchdog · after R15 ──────────

Goal:        Bring the open-finding COUNT mirrors back into agreement with
             `.agent/live_review.md` after R-0394 was registered. This is the
             residue the previous worker reported, and it is the same class
             R-0394 itself names — so this block greps the claim across every
             state file FIRST and names all three that carry it.

The claim was located mechanically, not from memory:
`grep -n 'TWENTY-FOUR\|Next free\|Open findings' .agent/plan.md
.agent/handoff.md .agent/context.md` → the four regions this block rewrites,
and nothing else. `.agent/handoff.md` lines 45-46 and 65 also name 24 and
R-0393, and they are NOT touched: they are R15's own gate-4 MEASUREMENT, true
of that round when it ran, and rewriting a past measurement to match a later
state would be falsifying the record rather than mirroring it.

Bundle:
  C0   save this block verbatim to `.agent/authored/f077-r15-close3.md`, then
       `cp` it to `.agent/last_block.md`
  C1   apply all four authored pairs — PLANHEAD and PLANRISK to
       `.agent/plan.md`, CONTEXT to `.agent/context.md`, HANDOFF5 to
       `.agent/handoff.md` — in ONE commit, because they are one claim

Change:      EXACTLY these files: `.agent/authored/f077-r15-close3.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/context.md`,
             `.agent/handoff.md`. Five files. NO product file, and
             `.agent/live_review.md` is NOT touched — it is the source of
             truth these three mirror, and it is already correct.

Constraints:
  - AGENTS.md Commit Gate before every commit.
  - You never author a `Gate:`, a `Done:`, a `- R-NNNN` or a `Landed:` line.
    All four pairs are reviewer text, extracted from the COMMITTED
    `.agent/authored/f077-r15-close3.md` and applied byte for byte.
  - This round registers and resolves NOTHING. Registering a finding here
    would invalidate the very counts it is fixing; the open set stays 25 and
    the next free id stays R-0395.
  - Every pair is a REWRITE whose FROM and TO have the SAME number of physical
    lines — 6, 1, 2 and 4 — so `.agent/plan.md` stays 45 lines,
    `.agent/context.md` stays 88 and `.agent/handoff.md` stays 133. A file
    that changes length means a mis-application: stop and report.

Done when: every gate below has been RUN by you and its REAL value recorded.
The base commit is `2d35b701`.

  1.  `git status --porcelain` → EMPTY. `git worktree list` → exactly 1 line.
  2.  `cmp .agent/authored/f077-r15-close3.md .agent/last_block.md` → exit 0.
      Report the shared sha256 and the line count.
  3.  Recompute the open set from `.agent/live_review.md` mechanically — every
      `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line. Expected 25
      open, next free R-0395, UNCHANGED by this round. Report what you measure.
  4.  `grep -c 'TWENTY-FOUR' .agent/plan.md .agent/context.md` → 0 and 0.
      `grep -c 'Next free id: \*\*R-0394\*\*' .agent/handoff.md` → 0.
      NOTE why these three files and not `.agent/*.md`: this block's own FROM
      slices quote the retired strings, and the block is copied to
      `.agent/last_block.md` and `.agent/authored/`, so a whole-directory zero
      count is unsatisfiable by construction. The gate is scoped to the files
      the claim actually had to leave.
  5.  `grep -c 'TWENTY-FIVE' .agent/plan.md .agent/context.md` → 1 and 1.
      `grep -c 'R-0395' .agent/plan.md .agent/context.md .agent/handoff.md`
      → report all three; each must be at least 1.
  6.  `grep -c 'R-0394' .agent/plan.md .agent/handoff.md` → report both; each
      must be at least 1, because R-0394 is now an OPEN finding and belongs in
      both name lists.
  7.  `wc -l .agent/plan.md .agent/context.md .agent/handoff.md`
      → 45, 88, 133.
  8.  `git diff --name-only 2d35b701..HEAD` → exactly the five files.
  9.  `python3 -m pytest tests/ -q -k "dashboard_contract or resource_safety or test_runner"`
      → both numbers. The reviewer measured `216 passed, 16671 deselected` at
      `2d35b701`. These suites read these exact state files, so this is the
      gate that matters this round.
  10. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → number.
      The reviewer measured `42 passed` at `2d35b701`.
  11. `test -e .agent/STOP` → ABSENT or PRESENT.
  12. `git diff --check 2d35b701..HEAD` → no output.
  13. Insertions per commit — none over 500.
  14. `git push -u origin feature/f077-autonomy-watchdog`. No `gh`, no PR.

Handback:    reply with the commit SHAs and the fourteen gate values, nothing
             else. Do not rewrite `.agent/handoff.md` beyond the HANDOFF5 pair.

── AUTHORED PAIRS — apply byte for byte ──────────────────────────

Four REWRITE pairs. In each, FROM and TO are disjoint and have the same
physical line count, so the proof per pair is FROM 0x and TO 1x in its target
file after the edit.

<<<BEGIN PLANHEAD-FROM>>>
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0394.
Open findings: TWENTY-FOUR — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393 — recomputed
mechanically at R15 from `.agent/live_review.md`: 28 registered, 4 resolved
(R-0383, R-0384, R-0388, R-0390), no duplicate id. That file is the source of
<<<END PLANHEAD-FROM>>>

<<<BEGIN PLANHEAD-TO>>>
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0395.
Open findings: TWENTY-FIVE — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393, R-0394 —
recomputed at the session close from `.agent/live_review.md`: 29 registered,
4 resolved (R-0383, R-0384, R-0388, R-0390), no duplicate id. It is the source of
<<<END PLANHEAD-TO>>>

<<<BEGIN PLANRISK-FROM>>>
- Twenty-four open findings is the largest carry any feature has held.
<<<END PLANRISK-FROM>>>

<<<BEGIN PLANRISK-TO>>>
- Twenty-five open findings is the largest carry any feature has held.
<<<END PLANRISK-TO>>>

<<<BEGIN CONTEXT-FROM>>>
import cycle `watchdog` keeps its imports inside function bodies to avoid. Open
findings after R15: TWENTY-FOUR, next free id R-0394.
<<<END CONTEXT-FROM>>>

<<<BEGIN CONTEXT-TO>>>
import cycle `watchdog` keeps its imports inside function bodies to avoid. Open
findings after the session close: TWENTY-FIVE, next free id R-0395.
<<<END CONTEXT-TO>>>

<<<BEGIN HANDOFF5-FROM>>>
5. Open findings: **24** — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
   R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378,
   R-0379, R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393.
   Next free id: **R-0394**.
<<<END HANDOFF5-FROM>>>

<<<BEGIN HANDOFF5-TO>>>
5. Open findings after the session close: **25** — R-0380, R-0381, R-0361,
   R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375,
   R-0376, R-0377, R-0378, R-0379, R-0382, R-0385, R-0386, R-0387, R-0389,
   R-0391, R-0392, R-0393, R-0394. Next free id: **R-0395**.
<<<END HANDOFF5-TO>>>
──────────────────────────────────────────────────────────────────
