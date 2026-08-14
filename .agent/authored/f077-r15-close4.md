── SESSION CLOSE 4 — F077 Autonomy watchdog · after R15 ──────────

Goal:        Register the reviewer's stale-gate-value defect as R-0395 AND
             move the three count mirrors to 26 in the SAME commit, so this
             block leaves nothing stale behind it. That coupling is the whole
             point: close 2 registered a finding and staled the counts, close 3
             fixed the counts and could not register anything without staling
             them again, and doing both at once is what breaks the loop.

The claim was located mechanically: `grep -n 'TWENTY-FIVE\|Next free\|Open
findings' .agent/plan.md .agent/context.md .agent/handoff.md` → the four
regions below and nothing else. `.agent/handoff.md` line 46 also names R-0394
and is NOT touched — it is R15's own gate-4 MEASUREMENT, true of that round
when it ran.

Bundle:
  C0   save this block verbatim to `.agent/authored/f077-r15-close4.md`, then
       `cp` it to `.agent/last_block.md`
  C1   ONE commit: append the authored FINDING-R395 slice to the END of
       `.agent/live_review.md`, and apply all four count pairs — PLANHEAD and
       PLANRISK to `.agent/plan.md`, CONTEXT to `.agent/context.md`, HANDOFF5
       to `.agent/handoff.md`. The finding and the counts it changes land
       together or not at all.

Change:      EXACTLY these files: `.agent/authored/f077-r15-close4.md`,
             `.agent/last_block.md`, `.agent/live_review.md`,
             `.agent/plan.md`, `.agent/context.md`, `.agent/handoff.md`.
             Six files. NO product file.

Constraints:
  - AGENTS.md Commit Gate before every commit.
  - You never author a `Gate:`, a `Done:`, a `- R-NNNN` or a `Landed:` line.
    All five slices are reviewer text, extracted from the COMMITTED
    `.agent/authored/f077-r15-close4.md` and applied byte for byte.
  - The residual `Landed: R-0384` stays — open finding R-0380's evidence.
  - Every pair is a REWRITE whose FROM and TO have the SAME physical line
    count — 6, 1, 2 and 4 — so `.agent/plan.md` stays 45, `.agent/context.md`
    stays 100 and `.agent/handoff.md` stays 133. A file whose length changed
    means a mis-application: stop and report rather than trimming.

Done when: every gate below has been RUN by you and its REAL value recorded.
The base commit is `9a272020`.

  1.  `git status --porcelain` → EMPTY. `git worktree list` → exactly 1 line.
  2.  `cmp .agent/authored/f077-r15-close4.md .agent/last_block.md` → exit 0.
      Report the shared sha256 and the line count.
  3.  `grep -c '^- R-0395 — ' .agent/live_review.md` → 1.
      `grep -c '^Gate: R15 — ' .agent/live_review.md` → 1, still.
      `grep -c '^Landed: ' .agent/live_review.md` → 1, NOT 0.
  4.  Recompute the open set from `.agent/live_review.md` mechanically — every
      `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line. C1 registers
      R-0395, so 26 open and next free R-0396 is the expected reading. Report
      what you measure and name the set.
  5.  `grep -c 'TWENTY-FIVE' .agent/plan.md .agent/context.md` → 0 and 0.
      Scoped to these two files, not `.agent/*.md`: this block's own FROM
      slices quote the retired string and the block is copied into
      `.agent/last_block.md`, so a whole-directory zero is unsatisfiable by
      construction.
  6.  `grep -c 'TWENTY-SIX' .agent/plan.md .agent/context.md` → 1 and 1.
      `grep -c 'R-0396' .agent/plan.md .agent/context.md .agent/handoff.md`
      → each at least 1. Report all three.
  7.  `wc -l .agent/plan.md .agent/context.md .agent/handoff.md`
      → 45, 100, 133. These three numbers were re-measured at `9a272020` by
      the reviewer immediately before this block was written, after the last
      one ordered a stale 88 for `.agent/context.md` — which is the defect
      R-0395 registers.
  8.  `git diff --name-only 9a272020..HEAD` → exactly the six files.
  9.  `python3 -m pytest tests/ -q -k "dashboard_contract or resource_safety or test_runner"`
      → both numbers. The reviewer measured `216 passed, 16671 deselected` at
      `9a272020`. These suites read these exact state files.
  10. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → number.
      The reviewer measured `42 passed` at `9a272020`.
  11. `test -e .agent/STOP` → ABSENT or PRESENT.
  12. `git diff --check 9a272020..HEAD` → no output.
  13. Insertions per commit — none over 500.
  14. `git push -u origin feature/f077-autonomy-watchdog`. No `gh`, no PR.

Handback:    reply with the commit SHAs and the fourteen gate values, nothing
             else. Do not rewrite `.agent/handoff.md` beyond the HANDOFF5 pair.

── AUTHORED SLICES — apply byte for byte ─────────────────────────

FINDING-R395 is ONE physical line, appended to the END of
`.agent/live_review.md`, separated from the text above by one blank line.

<<<BEGIN FINDING-R395>>>
- R-0395 — Low — the third session-close block ordered `wc -l .agent/context.md` → 88 as a gate, and the file was 100 at that block's own base commit `2d35b701` and had been since `7c5749a7`. The reviewer measured 88 after R14 and reused the number after R15 without re-measuring, though R15's own handback table records `.agent/context.md` moving +17/-5 in that very round — 88 + 12 = 100, arithmetic the block had in front of it. This is the finding R-0364's class names, "run every gate at base", recurring in the one place it is easiest to skip: a state file the reviewer is not editing and therefore does not re-read. Nothing was harmed, which is why it is Low: the worker reported the contradiction instead of routing around it, and the invariant the block actually depends on — that a rewrite pair of equal line counts leaves its file's length unchanged — held at 100 → 100, with `.agent/plan.md` 45 → 45 and `.agent/handoff.md` 133 → 133 matching their ordered values exactly. The residual risk was a worker trimming a correct file to satisfy an incorrect gate, which the block's own "stop and report rather than trimming" clause is what prevented. From here, EVERY length gate over a state file is measured at the round's base commit in the same command that produces the block's other base values, never carried forward from an earlier round — a length is a measurement, and a measurement more than one round old is a memory. This finding and the count mirrors it invalidates are applied in ONE commit, because the two previous close rounds demonstrated that registering a finding and updating the counts that quote it are a single indivisible edit.
<<<END FINDING-R395>>>

Four REWRITE pairs. In each, FROM and TO are disjoint and have the same
physical line count, so the proof per pair is FROM 0x and TO 1x in its target
file after the edit.

<<<BEGIN PLANHEAD-FROM>>>
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0395.
Open findings: TWENTY-FIVE — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393, R-0394 —
recomputed at the session close from `.agent/live_review.md`: 29 registered,
4 resolved (R-0383, R-0384, R-0388, R-0390), no duplicate id. It is the source of
<<<END PLANHEAD-FROM>>>

<<<BEGIN PLANHEAD-TO>>>
F077 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding id: R-0396.
Open findings: TWENTY-SIX — R-0380, R-0381, R-0361, R-0362, R-0363, R-0364,
R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379,
R-0382, R-0385, R-0386, R-0387, R-0389, R-0391, R-0392, R-0393, R-0394, R-0395 —
recomputed at the session close from `.agent/live_review.md`: 30 registered,
4 resolved (R-0383, R-0384, R-0388, R-0390), no duplicate id. It is the source of
<<<END PLANHEAD-TO>>>

<<<BEGIN PLANRISK-FROM>>>
- Twenty-five open findings is the largest carry any feature has held.
<<<END PLANRISK-FROM>>>

<<<BEGIN PLANRISK-TO>>>
- Twenty-six open findings is the largest carry any feature has held.
<<<END PLANRISK-TO>>>

<<<BEGIN CONTEXT-FROM>>>
import cycle `watchdog` keeps its imports inside function bodies to avoid. Open
findings after the session close: TWENTY-FIVE, next free id R-0395.
<<<END CONTEXT-FROM>>>

<<<BEGIN CONTEXT-TO>>>
import cycle `watchdog` keeps its imports inside function bodies to avoid. Open
findings after the session close: TWENTY-SIX, next free id R-0396.
<<<END CONTEXT-TO>>>

<<<BEGIN HANDOFF5-FROM>>>
5. Open findings after the session close: **25** — R-0380, R-0381, R-0361,
   R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375,
   R-0376, R-0377, R-0378, R-0379, R-0382, R-0385, R-0386, R-0387, R-0389,
   R-0391, R-0392, R-0393, R-0394. Next free id: **R-0395**.
<<<END HANDOFF5-FROM>>>

<<<BEGIN HANDOFF5-TO>>>
5. Open findings after the session close: **26** — R-0380, R-0381, R-0361,
   R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375,
   R-0376, R-0377, R-0378, R-0379, R-0382, R-0385, R-0386, R-0387, R-0389,
   R-0391, R-0392, R-0393, R-0394, R-0395. Next free id: **R-0396**.
<<<END HANDOFF5-TO>>>
──────────────────────────────────────────────────────────────────
