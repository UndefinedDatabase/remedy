BEGIN BLOCK f045-r11
── STEP T003f/6 — F045 Loop definitions · ROUND 11 (session close) ───────

Goal:        Put the two outstanding reviewer counter-measures ON DISK, where
             R-0347 proved they have to live, and write the session-closing
             handoff. No code changes.
Bundle:      ITEM 1 C0a+C0b save block · ITEM 2 C1 the pre-emission checklist ·
             ITEM 3 C2 plan + closing handoff · ITEM 4 gates.
Change:      .agent/authored/f045-r11.md · .agent/last_block.md ·
             docs/agents/planner_reviewer_prompt.md · .agent/plan.md ·
             .agent/handoff.md. Five files, nothing else. Do NOT touch
             `.agent/live_review.md` this round — see the note in ITEM 2 about
             why R-0353 and R-0356 stay OPEN.
Constraints: Never work on main; never force-push; merge nothing. Do NOT open
             a PR: this feature's branch has deliberately carried no PR across
             several sessions and the closing handoff raises that as the
             operator's call, not the session's.
Insertion budget, per commit: C0a and C0b ≈ block size (single `.agent/**`
             state-file rewrites, cap-exempt by DECISION F104 D1) · C1 ≤ 30 ·
             C2 ≤ 130.
Done when:   every gate in ITEM 4 has been RUN and its real output recorded.
Handback:    completion report + rewrite .agent/handoff.md

═══ ITEM 1 · C0a and C0b — save this block verbatim ═══
C0a: write the block bytes (BEGIN..END markers included) to
`.agent/authored/f045-r11.md`. No trailing whitespace on any line.
Commit subject: `chore(f045): save the R11 block verbatim`
C0b: copy that file over `.agent/last_block.md`, replacing the R10 block.
Commit subject: `chore(f045): point last_block at the R11 block`
Prove it: cmp .agent/authored/f045-r11.md .agent/last_block.md → exit 0

═══ ITEM 2 · C1 — docs/agents/planner_reviewer_prompt.md, §3 ═══
The "Pre-emission block checklist" bullet begins at line 173 and its numbered
items run 1 to 8. Its own intro sentence says "Run all six checks" while EIGHT
items already exist — the count went stale when items 7 and 8 were added, which
is the same carried-forward-count failure R-0356 names, sitting in the very
file that is supposed to prevent it. Verify both facts before editing: count
the numbered items yourself and read the intro line.

Two edits, one commit.

(1) Correct the intro count to match the item count AFTER your additions below.
    Change only the number word; leave the rest of that sentence alone.

(2) Append items 9 and 10 after item 8, in the same style as the eight above —
    bold lead-in, the finding id that produced it, and the reason it is its own
    check rather than a sub-point of an existing one:

    Item 9 — citations re-measured against this branch's own edits (finding
    R-0353). Every `file:line` a block cites for a file the CURRENT feature
    branch has modified is re-grepped at emission. Prefer citing the SYMBOL
    plus its distinguishing text over a bare number: a symbol survives an edit
    above it, a line number does not. Say why it is separate from item 8: item
    8 checks a gate's expected VALUE against the code, this one checks that the
    block's POINTERS resolve at all — a different failure, and one that halted
    two rounds of this feature before it was written down.

    Item 10 — the open-finding set is recomputed, never carried forward
    (findings R-0354 and R-0356). Derive it mechanically from
    `.agent/live_review.md` at emission — every `^- R-\d+ — ` paragraph minus
    every `^Done: R-\d+ — ` line — and name each finding explicitly, never by
    position. Record that naming them explicitly is NOT sufficient on its own:
    two consecutive blocks did exactly that and were both still wrong, because
    each took its set from the previous block instead of from the record, and a
    finding that drops out of the count stays dropped.

Write the prose yourself; the substance above is what must be preserved.

Why `.agent/live_review.md` is NOT in this change set: R-0353 and R-0356 stay
OPEN. This commit is their FIX, and the reviewer has not yet verified it — a
`Done:` line written in the same round as the repair, by the worker who applied
it, is a finding self-certified by its own author. The next session's reviewer
verifies this edit and writes both `Done:` lines. Recording that in the handoff
is what carries the obligation forward.

Commit subject: `docs(agents): add the citation and open-set checks to the block checklist`

═══ ITEM 3 · C2 — .agent/plan.md and the session-closing handoff ═══
Rewrite `.agent/plan.md` (under 50 lines, keeping `## Goal`, `## Current Step`,
`## Next Steps`, `## Risks`). RECOMPUTE the open-finding set from
`.agent/live_review.md` with the command in gate (c) and write what you
measure, naming each finding. This block gives you no count on purpose. Current
Step becomes R11 — the T003 CLI is complete (`list`, `validate`, `run`), the
two reviewer counter-measures are on disk, and the session is closing at its
declared round cap. Next Steps: the end-to-end fixture loop through the
fake-provider pipeline, the integration gate, then closure per
docs/roadmap/STATUS_closure_protocol.md. State plainly that F045 is NOT closed
and that the next session's first bookkeeping act is to verify this round's
checklist edit and write the `Done:` lines for R-0353 and R-0356. Keep the
Fortschritt line
`Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung` verbatim.

Then rewrite `.agent/handoff.md` as a SESSION-CLOSING handoff, per the
AGENTS.md contract (≤60 lines, or a "Deviations, declared" line naming the real
count and the mandated content that caused it; sections are NEVER dropped). It
carries:
- feature, round, branch, and the fact that this was a one-session self-drive
  run (docs/agents/self_drive_protocol.md) that ended at its DECLARED round cap
  with all work committed and pushed — a success under G7, not a failure
- a per-round table for this session: R6 reviewed PASS, R7 PASS, R8 FAIL (the
  listing printed the run notice), R9 the repair PASS, R10 PASS, R11 this round
- every commit SHA of THIS round with its changed files
- this round's gate results from ITEM 4
- the recomputed open-finding count with every finding named, and the explicit
  statement that R-0353 and R-0356 are FIXED ON DISK but still OPEN pending the
  next reviewer's verification
- an item-status table with one row per ITEM 1-4
- what F045 still needs: the end-to-end fixture loop, the integration gate,
  closure. Say plainly that the feature is NOT done
- the state of the branch: no PR is open, nothing was merged, main was never
  touched, no force-push occurred, no worktree was left behind. Add one line
  flagging FOR THE OPERATOR that this branch has carried no PR across several
  sessions and that whether to open one is their call — the session did not
  make it either way
- the next expected action, naming Phase 1 rule 1 (read `.agent/STOP` from
  disk) BEFORE rule 2 (the Open PR Gate)
- the Fortschritt line verbatim
Commit subject: `docs(f045): close the session with the R11 handoff`

═══ ITEM 4 · gates ═══
Run every command. Record REAL exit codes and REAL output. Report counts as
OBSERVED.

(a) cmp .agent/authored/f045-r11.md .agent/last_block.md
(b) the checklist item count, measured not asserted:
    python3 -c "
    import re, pathlib
    t = pathlib.Path('docs/agents/planner_reviewer_prompt.md').read_text()
    print('ITEMS', re.findall(r'^  (\d+)\. \*\*', t, re.M)[:14])"
    → the run must end at 10, and the intro sentence's number word must agree.
      Quote the intro line in your report.
(c) the recomputed open set:
    python3 -c "
    import re, pathlib
    t = pathlib.Path('.agent/live_review.md').read_text()
    o = re.findall(r'^- (R-\d+) — ', t, re.M); d = re.findall(r'^Done: (R-\d+) — ', t, re.M)
    print('OPEN', [x for x in o if x not in d])"
(d) git diff --name-only 6e6e3479..HEAD  → exactly the five Change files;
    `.agent/live_review.md` must NOT appear.
(e) python3 -m pytest tests/docs -q
    → this round edits a docs file that the docs tests may assert over. If
      tests/docs does not exist or collects nothing, say so; that is an
      observation, not a failure.
(f) python3 -m pytest tests/cli/test_golden_path.py -q            (canary)
(g) git status --porcelain               → EMPTY
(h) git worktree list                    → ONE line
(i) confirm no PR was created: gh pr list --state open --json number,headRefName
    → report its raw output.

Push after EVERY commit: `git push origin feature/f045-loop-definitions`.
Do NOT open a PR and do NOT merge anything.

If any gate is RED, or anything here contradicts AGENTS.md or the disk: STOP,
commit nothing further, and report the exact blocker with its raw output.
END BLOCK f045-r11
