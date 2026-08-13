── STEP R3/n — F115 Prompt breakdown & cost report · Round 3 ─────────
Goal:        Close the two open loops the R2 gate left and persist the reviewer
             error that caused R2's declared deviation: fix the R-0321
             miscount, register R-0322 for the pre-existing suite red, and add
             an eighth item to the pre-emission block checklist so the next
             reviewer does not repeat the unmeetable-arithmetic gate.
Bundle:      C1a save this block · C1b mirror it · C2 register R-0322 ·
             C3 fix R-0321 and mark it Landed · C4 checklist item 8 ·
             C5 plan + handback
Change:      EXACTLY these paths:
               .agent/authored/f115-r3-1.md          (new, C1a)
               .agent/last_block.md                  (rewrite, C1b)
               .agent/live_review.md                 (C2 append, C3 append)
               .agent/f115_inventory.md              (C3: one pair)
               docs/agents/planner_reviewer_prompt.md (C4: one pair)
               .agent/plan.md                        (C5: full replace)
               .agent/handoff.md                     (C5: rewrite)
             NO source file and NO test file this round.
Constraints:
  - TEXT-A … TEXT-D are AUTHORED text. Apply them byte for byte. Do not reword,
    rewrap or re-punctuate. No placeholder slots: substitute nothing.
  - Do NOT write a `Done:` paragraph. R-0321's fix lands here, so you mark it
    `Landed:` per TEXT-C and nothing else; only reviewer-authored text sets
    Resolved (docs/agents/planner_reviewer_prompt.md §4.4). The next session's
    reviewer authors the `Done:` line at its first gate. A surviving `Landed:`
    line is an unreviewed fix and is exactly what the disk should show.
  - Do NOT fix the R-0322 red. It is inherited from main, it is not an F115
    defect, and AGENTS.md bars mixing an unrelated fix into a feature branch.
    Registering it is the whole action.
  - Never force-push. Never commit on main. Push after EVERY commit (R-0289).
  - Do NOT create a pull request this round.
Done when: every command has been RUN for real and its TRUE output recorded. A
           guessed, expected or remembered value is a finding.
  a. `cmp .agent/authored/f115-r3-1.md .agent/last_block.md` exits 0; record
     `sha256sum` of both and `wc -lc` of the authored file.
  b. After C2: `grep -c '^- R-0322' .agent/live_review.md` prints 1 and
     `grep -c '^- R-0' .agent/live_review.md` prints 3.
  c. After C3, the R-0321 pair is a REWRITE, so prove it in both directions:
     in `.agent/f115_inventory.md`, `grep -c 'four of the eight'` prints 0 and
     `grep -c 'four of the seven'` prints 1. Also `grep -c '^Landed: R-0321'`
     in `.agent/live_review.md` prints 1, and `grep -c '^Done:'` prints 0.
  d. After C4, the checklist pair is APPEND-shaped — its TO contains its FROM
     verbatim — so do NOT attempt a "FROM 0x" count. Prove instead:
     `grep -c 'Why this is on disk and not a habit' docs/agents/planner_reviewer_prompt.md`
     prints 1 (unchanged), `grep -c '  8. \*\*Gates whose expected VALUE'`
     prints 1, and the item-8 text appears exactly ONCE among the lines this
     commit ADDS — measure with
     `git show --numstat <sha> -- docs/agents/planner_reviewer_prompt.md` for
     the total plus a count over that diff's added lines. Record both numbers.
  e. `python3 -m pytest tests/docs/ -q` and
     `python3 -m pytest tests/cli/test_golden_path.py -q`. Record tail and exit
     code for each. Neither should change, and if either does, STOP and hand
     back rather than adjusting an authored text to suit a test.
  f. `wc -l .agent/plan.md` prints a number BELOW 50 — record the real number.
  g. `git status --porcelain` empty; `git diff --name-only 0d6c97aa..HEAD`
     lists ONLY the thirteen paths from R1+R2 plus this round's two new ones
     (`.agent/authored/f115-r3-1.md`, `docs/agents/planner_reviewer_prompt.md`)
     — fifteen in total, nothing else;
     `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
     prints 0 and 0 after the final push.
Handback:  completion report + rewrite `.agent/handoff.md`. Item-status table
           (C1a, C1b, C2, C3, C4, C5 — each exactly once), commit table with
           real SHAs and insertions, changed-files table, every result a-g as a
           REAL value. Repeat the Fortschritt line verbatim. Over 60 lines ⇒
           carry a "Deviations, declared" line naming the count and the
           mandated content that caused it (AGENTS.md DECISION D15).

           THIS IS THE LAST ROUND OF THE SESSION. The handoff is the only
           return channel, so make it the one a cold reader can resume from:
           name the branch, the head SHA, the last reviewed SHA, the open
           findings and their state, and that T001 proper (persist the manifest
           alongside the ledger row) is the next work with the reviewer and
           planner call sites still unwired. Do NOT create a PR.
──────────────────────────────────────────────────────────────────────

PROCEDURE

C1a `chore(f115): save the R3 step block verbatim` — copy the reviewer's
    scratchpad original `.remedy-wt/f115-r3-1.md` to
    `.agent/authored/f115-r3-1.md`. Copy the FILE; do not retype it.
C1b `chore(f115): mirror the R3 block into last_block` — copy that same file to
    `.agent/last_block.md`. Run gate (a).

C2 `chore(f115): register R-0322 for the inherited suite red`
    Append TEXT-A to the END of `.agent/live_review.md`. Run gate (b).

C3 `docs(f115): correct the call-site count in the inventory`
    Apply the TEXT-B pair to `.agent/f115_inventory.md` (REWRITE, one line),
    then append TEXT-C to the END of `.agent/live_review.md`. Run gate (c).

C4 `docs(agents): add checklist item 8 on unmeetable gate arithmetic`
    Apply the TEXT-D pair to `docs/agents/planner_reviewer_prompt.md`. The
    FROM is the single line that opens the checklist's closing paragraph; the
    TO is item 8 followed by that same line verbatim, so item 8 lands as the
    last numbered item and the closing paragraph keeps its place. Run gate (d).

C5 `chore(f115): refresh the plan and write the R3 handoff`
    `.agent/plan.md` ← TEXT-E in full, then rewrite `.agent/handoff.md`.
    Run gates (e), (f), (g).

TEXT-A — append to the END of .agent/live_review.md

- R-0322 — Medium — the suite is RED at this branch's merge base. Five ids in
  `tests/orchestration/test_role_conventions.py` fail, every one a
  `[reviewer]` parametrization, each raising `PromptSegmentError: prompt
  segment 'reviewer_conventions' is over its token cap: 954 tokens estimated,
  cap 800` before any assertion in the test runs. Measured by the reviewer at
  the R2 gate: `5 failed, 21 passed in 0.14s`. It is NOT an F115 defect —
  `docs/agents/reviewer_conventions.md` was last touched at a85e82f5 on
  2026-08-12, before this branch existed, and
  `git diff --name-only 0d6c97aa..HEAD` over that path and over
  `prompt_facts.py` is empty. It is the same class F111 recorded as R-0286 and
  attributed at its integration gate in both trees. It is registered here
  rather than inherited silently because F115's own integration gate will meet
  it, and a gate that has to rediscover a known red spends a round proving
  something already known. It is deliberately NOT fixed on this branch:
  AGENTS.md bars mixing an unrelated fix into a feature branch. The fix
  belongs to a round that legitimately opens the conventions document or the
  cap. OPEN.

TEXT-B — one REWRITE pair for .agent/f115_inventory.md
  FROM (1 line, occurs exactly once):
LOAD-BEARING GAP: only four of the eight `build_trace_entry` call sites pass
  TO (1 line):
LOAD-BEARING GAP: only four of the seven `build_trace_entry` call sites pass

TEXT-C — append to the END of .agent/live_review.md

Landed: R-0321 — the inventory's "eight" is now "seven" in the LOAD-BEARING GAP sentence of `.agent/f115_inventory.md`; the enumeration below it was already correct at four wired plus three unwired. Fixed in the C3 commit of R3.

TEXT-D — one APPEND-shaped pair for docs/agents/planner_reviewer_prompt.md
  FROM (1 line, occurs exactly once):
  Why this is on disk and not a habit: item 2 has recurred six times across
  TO (begins with item 8 and ENDS with that same FROM line verbatim):
  8. **Gates whose expected VALUE the code contradicts.** A done-when may not
     assert a number, an equality or an identity that the source makes
     impossible. Before ordering one, read the code that PRODUCES the value and
     compute the expected result from it — do not derive it from what the field
     is named or from what it obviously ought to be. The F115 R2 instance: a
     gate demanded `segment_manifest_chars == sum(row["chars"])`, but
     `build_trace_entry` sets that field to `len(composed_prompt.text)`
     (`prompt_trace.py:157-158`) and `compose_prompt_segments` joins segments
     with a two-character delimiter, so the composed text is exactly
     `2*(N-1)` characters longer than the row sum and the equality is
     unreachable for every multi-segment prompt. Items 1-4 read the block,
     item 5 the code the block points at, item 6 the file the block writes
     into, item 7 the tests that already guard that file — and this one the
     code that computes the number the gate asserts. A worker who meets such a
     gate has either fabricated the number or changed the code to suit it;
     both are worse outcomes than the declared deviation an honest worker is
     forced into, and the round pays for the reviewer's arithmetic either way.
  Why this is on disk and not a habit: item 2 has recurred six times across

TEXT-E — the complete new .agent/plan.md

# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged at the Open PR Gate. Last reviewed SHA: cc635159 (R2 PASS).
Next free finding ID: R-0323. Open findings: 3 — R-0320 (Low, carried
from F111), R-0321 (Low, fixed in R3, awaiting the reviewer's Done),
R-0322 (Medium, inherited suite red, not an F115 defect).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R3 done — housekeeping only. T001a wired the BUILDER call site through
`compose_builder_prompt` (DECISION F115 D1), proved the sent bytes
unchanged, and pinned it with a behaviour test plus an
`inspect.getsource` wiring guard whose red-proof really goes red.

## Next Steps
1. The reviewer call site. Decide first: its traced text is
   `_reviewer_effective_prompt(...)`, which appends the native-schema
   tail unconditionally in structured mode, so the manifest covers the
   composed BASE and `segment_manifest_chars < prompt_chars` records the
   gap — the F105 D3 precedent already covers this shape. Then the
   planner site at `apps/cli/commands/job.py:236`.
2. T001 proper — persist the manifest, or a reference to it, alongside
   the ledger row, additively, with backfill tolerance: old rows render
   as "unattributed", never guessed.
3. T002 — aggregation queries plus the pure renderer, with goldens;
   follow `gauntlet_matrix.py` and `tests/cli/test_stats_cost.py:49-128`.
4. T003 — CLI, prior-period comparison, json schema; then the
   integration gate and closure.

## Risks
- The per-role breakdown has one bucket until `role` stops being
  hardcoded, and per-task-class has no source at all. Both are recorded
  in the feature file; F115 must report "no data", never a fake bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.

Fortschritt: 20 % (R1 ✅ · T001a ✅ · Reviewer-Site · T001 · T002 · T003 offen) — Schätzung
