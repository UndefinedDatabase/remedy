── SESSION CLOSE 2 — F077 Autonomy watchdog · after R15 ──────────

Goal:        Retire the SECOND copy of the "R16 owes the R15 gate" claim, which
             the previous close block retargeted in `.agent/handoff.md` and
             missed in `.agent/plan.md`, and register that miss as a finding
             against the reviewer who wrote it.

Bundle:
  C0   save this block verbatim to `.agent/authored/f077-r15-close2.md`, then
       `cp` it to `.agent/last_block.md`
  C1   append the authored FINDING-R394 slice to the END of
       `.agent/live_review.md`
  C2   apply the authored PLAN1 pair to `.agent/plan.md`

Change:      EXACTLY these files: `.agent/authored/f077-r15-close2.md`,
             `.agent/last_block.md`, `.agent/live_review.md`,
             `.agent/plan.md`. Four files. NO product file, and NOT
             `.agent/handoff.md` — it is already correct and must not be
             touched.

Constraints:
  - AGENTS.md Commit Gate before every commit. C1 and C2 may share one commit.
  - You never author a `Gate:`, a `Done:`, a `- R-NNNN` or a `Landed:` line.
    Both slices are reviewer text, extracted from the COMMITTED
    `.agent/authored/f077-r15-close2.md` and applied byte for byte.
  - The residual `Landed: R-0384` stays — open finding R-0380's evidence.
  - PLAN1 is a REWRITE and both sides are exactly 3 physical lines, so
    `.agent/plan.md` must still be 45 lines afterwards. If it is not 45, you
    have mis-applied it — stop and report rather than trimming.

Done when: every gate below has been RUN by you and its REAL value recorded.
The base commit is `d3d5dbd2`.

  1.  `git status --porcelain` → EMPTY. `git worktree list` → exactly 1 line.
  2.  `cmp .agent/authored/f077-r15-close2.md .agent/last_block.md` → exit 0.
      Report the shared sha256 and the line count.
  3.  `grep -c '^- R-0394 — ' .agent/live_review.md` → 1.
      `grep -c '^Gate: R15 — ' .agent/live_review.md` → 1, still.
      `grep -c '^Landed: ' .agent/live_review.md` → 1, NOT 0.
  4.  Recompute the open set mechanically — every `^- R-\d+ — ` paragraph minus
      every `^Done: R-\d+ — ` line. C1 registers R-0394, so 25 open and next
      free R-0395 is the expected reading. Report what you measure.
  5.  `grep -c 'Gate: R15' .agent/plan.md` → 0. The claim is gone from that
      file entirely.
  6.  `wc -l .agent/plan.md` → 45.
  7.  `git diff --name-only d3d5dbd2..HEAD` → exactly the four files.
  8.  `python3 -m pytest tests/ -q -k "dashboard_contract or resource_safety or test_runner"`
      → both numbers. The reviewer measured `216 passed, 16671 deselected` at
      `d3d5dbd2`; this round adds no test, so both are expected to hold.
  9.  Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → number.
      The reviewer measured `42 passed` at `d3d5dbd2`.
  10. `test -e .agent/STOP` → ABSENT or PRESENT.
  11. `git diff --check d3d5dbd2..HEAD` → no output.
  12. Insertions per commit — none over 500.
  13. `git push -u origin feature/f077-autonomy-watchdog`. No `gh`, no PR.

Handback:    do NOT rewrite `.agent/handoff.md`. Reply with the commit SHAs and
             the thirteen gate values, and nothing else.

── AUTHORED SLICES — apply byte for byte ─────────────────────────

FINDING-R394 is ONE physical line, appended to the END of
`.agent/live_review.md`, separated from the text above by one blank line.

<<<BEGIN FINDING-R394>>>
- R-0394 — Low — the session-close block that recorded `Gate: R15 — PASS` retargeted the "R16 owes R15's gate paragraph" claim in `.agent/handoff.md` and left the SAME claim standing in `.agent/plan.md`, whose Next Steps item 1 still read "Its FIRST commit owes R15's own `Gate: R15 — ` paragraph, which cannot exist before this round is reviewed" after that paragraph demonstrably existed. This is a reviewer defect, not a worker one: the block named `.agent/handoff.md` as its only amendment target and its own change set forbade touching `plan.md`, so the worker was right to apply it as written and to report the residue instead of silently widening scope — which is exactly what it did. The cost was bounded only by that report. `docs/agents/planner_reviewer_prompt.md` §1 has the next session read `.agent/plan.md` at bootstrap, so a reader arriving on this branch would have been told by the plan to write a gate paragraph the record already carries, and the likely outcome is a duplicate `Gate: R15` line or a round spent discovering it is not needed. The root cause is the one finding R-0331's class keeps naming: a claim that lives in more than one state file is retired in all of them or in none, and the reviewer checked its own edit against the file it was editing rather than grepping the claim across `.agent/`. From here, a block that retires a claim from a state file greps that claim's distinguishing text across `.agent/*.md` FIRST and names every file that carries it in the change set — the grep is one command and it is the whole fix.
<<<END FINDING-R394>>>

PLAN1 is a REWRITE pair over `.agent/plan.md` — FROM and TO are disjoint, so the
proof is FROM 0x and TO 1x after the edit. Both are exactly 3 physical lines,
which is why the file stays 45 lines.

<<<BEGIN PLAN1-FROM>>>
1. R16 — the integration gate per docs/agents/integration_gate.md. Its FIRST
   commit owes R15's own `Gate: R15 — ` paragraph, which cannot exist before
   this round is reviewed.
<<<END PLAN1-FROM>>>

<<<BEGIN PLAN1-TO>>>
1. R16 — the integration gate per docs/agents/integration_gate.md. It owes no
   gate paragraph: R15 was reviewed and its verdict is on the record, so R16's
   first commit is the integration gate's own work.
<<<END PLAN1-TO>>>
──────────────────────────────────────────────────────────────────
