── STEP R7/7 — F111 Diff-only repair — SESSION CLOSE (terminator round) ──────
Goal:        Persist the R6 gate and findings R-0305 and R-0306, bring the plan
             header to the new counts, and write the session-closing handoff.
             No code, no test, no docs this round.
Bundle:      C1 block save; C2 last_block mirror; C3 findings append;
             C4 plan header; C5 closing handoff. Commit AND push at every item.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f111-r7-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/plan.md, .agent/handoff.md.
Constraints: AGENTS.md in full. Apply the authored slice by READING ITS FILE
             (`cat`) — never retype, never reflow. Do NOT create a PR, do NOT
             merge, never touch main, never force-push. Write no `Done:` and no
             `Landed:` line: this round lands no fix. Scratch stays under
             .remedy-wt/. This is the LAST round of the session — after C5,
             stop and hand back.

AUTHORED SLICE — one stated digest, plus BLOCK pinned by the C1 cmp:
  .remedy-wt/f111r7/LRG  sha256=3e076d0297464c2462daee927aeb8734a0ddbacce61860172d1c45f80d49c182  50 lines, appended to .agent/live_review.md
  .remedy-wt/f111r7/BLOCK = this entire step block, byte for byte (cmp only)

PROCEDURE (in order; commit AND push at every numbered item):

0. Preconditions: `git status --porcelain` empty; branch is
   feature/f111-diff-only-repair; `git log -1 --format=%h` is b1e5cc7e.
   Verify the stated digest. Any mismatch => STOP and hand back.

1. C1 — `cp .remedy-wt/f111r7/BLOCK .agent/authored/f111-r7-1.md`; `cmp`
   silent. Commit: chore(f111): save the R7 step block verbatim   -> push

2. C2 — `cp .agent/authored/f111-r7-1.md .agent/last_block.md`; `cmp` silent.
   Commit: chore(f111): mirror the R7 block into last block   -> push

3. C3 — FINDINGS FIRST: `cat .remedy-wt/f111r7/LRG >> .agent/live_review.md`
   PURE APPEND: `git show --numstat <C3> -- .agent/live_review.md` must read
   `50 0`. A nonzero delete column means a rewrite: STOP and hand back.
   Commit: chore(f111): record the R6 gate and findings R-0305 R-0306 -> push

4. C4 — two single-line REWRITE pairs in `.agent/plan.md`. Each FROM occurs
   exactly 1x in the file today; change nothing else in that file.
   (i) FROM: Last reviewed SHA: d0952432 (R5 PASS). Next free finding ID: R-0305.
        TO:  Last reviewed SHA: b1e5cc7e (R6 PASS). Next free finding ID: R-0307.
   (ii) FROM: Open findings: 25, none above Medium.
         TO:  Open findings: 27, none above Medium.
   `git show --numstat <C4> -- .agent/plan.md` must read `2 2`.
   Commit: chore(f111): bring the plan header to the R6 gate   -> push

5. C5 — rewrite `.agent/handoff.md`, your own text. COUNT THE LINES BEFORE
   COMMITTING (`wc -l`): 60 or fewer, or carry a DECISION D15 "Deviations,
   declared" line naming the REAL measured count and the mandated content that
   caused it. It must contain: feature and round (F111 R7, SESSION CLOSE); the
   branch; a per-commit SHA table for C1-C5 with insertions; a changed-files
   table; the real gate results below with commands and real exit codes; open
   findings 27 with next free ID R-0307; an item-status table over C1-C5 whose
   Status cells carry the SAME status you declare in the handback — `done`,
   `skipped` with reason, or `deviated` with reason, never a bare `done` over a
   deviation you reported elsewhere (finding R-0306); this line verbatim, on
   its own line (finding R-0304):
Fortschritt: ~40 % (T001 ✅ Selektor + Range-Quelle · T002 offen · T003 offen) — Schätzung
   and a NEXT SESSION block stating, in this order:
     - the branch is UNMERGED and has NO PR by design; the next session's Open
       PR Gate does not apply because no PR exists — it resumes this branch
       directly, and Phase 0 must sweep `feature/*` branches (finding R-0290),
       because no probe command sees an unclaimed branch otherwise;
     - completed this session: the R4 gate, R5 (R-0300 closed;
       `parse_diff_line_ranges` and `changed_line_ranges_from_patch` built at
       30 tests and mutation-proved; DECISIONS F111 D2 and D3 on disk), and the
       R5 and R6 gates persisted with their resolutions;
     - next action: T002 — the versioned unified-diff response schema with a
       fence pre-check and strict all-or-nothing apply, on the `builder_bridge`
       seam — reading `structured_patch.py` and the `apply_structured_patch`
       fence path BEFORE designing it;
     - T001 has NO CALL SITE: a green suite is not a working feature, and T003
       is what wires it;
     - the reviewer-side findings this session opened against its own blocks:
       R-0301, R-0302, R-0303, R-0304, R-0305; plus R-0306 against the R6
       handoff.
   Commit: chore(f111): write the session closing handoff   -> push

Done when (record command + real exit code + counted value; never the word
"green"):
  a. the stated digest matches; `cmp` BLOCK vs .agent/authored/f111-r7-1.md
     silent; `cmp` that file vs .agent/last_block.md silent.
  b. `git show --numstat <C3> -- .agent/live_review.md` -> `50 0`
     `git show --numstat <C4> -- .agent/plan.md` -> `2 2`
  c. on the final `.agent/live_review.md`:
     `grep -c '^- R-0'` -> 31 ; `grep -c '^Done:'` -> 4
     `grep -c '^Landed:'` -> 0 (exit 1 is the pass)
     `grep -c '^### R6 — PASS'` -> 1
     python3 -c "import pathlib;print(pathlib.Path('.agent/live_review.md').read_text().count(pathlib.Path('.remedy-wt/f111r7/LRG').read_text()))"
     -> exit 0, printed count 1
  d. on `.agent/plan.md`: `grep -c 'R-0305'` -> 0 (exit 1 is the pass);
     `grep -c 'Next free finding ID: R-0307'` -> 1;
     `grep -c 'Open findings: 27'` -> 1; `wc -l` -> under 50
  e. `wc -l < .agent/handoff.md` -> the real number, 60 or fewer unless the
     D15 line declares it; `grep -c '^Fortschritt: ' .agent/handoff.md` -> 1
  f. `python3 -m pytest tests/orchestration/test_test_runner.py -q -k 'plan_md
     or context_md'` -> exit 0, 3 passed, 48 deselected. Do NOT run
     tests/ui_server/test_dashboard_contract.py (R-0221: real npm build).
  g. `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed
     (canary); `python3 -m pytest tests/orchestration/test_diff_repair.py -q`
     -> exit 0, 30 passed, unchanged: this round touches no code.
  h. `git status --porcelain` -> empty; `git worktree list` -> one entry;
     per-commit insertions each < 500;
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> `0 0` after the final push.
Handback:    completion report (per-commit table, changed-files table,
             item-status table over C1-C5 with real statuses, raw gate results)
             and `.agent/handoff.md` rewritten as C5. Do not merge, do not open
             a PR, do not touch `.agent/candidates.md` or `.agent/decisions.md`.
