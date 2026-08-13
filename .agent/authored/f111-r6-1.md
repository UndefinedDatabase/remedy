── STEP R6/6 — F111 Diff-only repair — SESSION CLOSE ─────────────────────────
Goal:        Persist the R5 gate, resolve R-0300/R-0301/R-0302 with the
             reviewer's authored `Done:` text, register R-0303 and R-0304, and
             end the session cleanly at its context limit. No code this round.
Bundle:      C1 block save; C2 last_block mirror; C3 findings append;
             C4 the three resolutions; C5 plan rewrite; C6 closing handoff.
             Commit AND push at every item.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f111-r6-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/plan.md, .agent/handoff.md.
             No production file, no test file, no docs change this round.
Constraints: AGENTS.md in full. Apply authored slices by READING THEIR FILES
             (`cp`/`cat`) — never retype, never reflow. Do NOT create a PR, do
             NOT merge, never touch main, never force-push. Write no `Done:`
             and no `Landed:` line of your own: this round lands no fix, and
             the only `Done:` text is the authored DONE3 slice. Scratch stays
             under .remedy-wt/.

AUTHORED SLICES — two stated digests, plus BLOCK pinned by the C1 cmp:
  .remedy-wt/f111r6/LRG    sha256=e6cd8de11cec7993c2331a5a472915234cc08787301c86008d18d869e9c69a37  63 lines, appended to .agent/live_review.md
  .remedy-wt/f111r6/DONE3  sha256=ef77c26fb83d99dd1f3263d89bbe77d5fb1a8f5ce8464d6897f9838ecb0c3d43  4 lines, replaces the three `Landed:` lines
  .remedy-wt/f111r6/BLOCK = this entire step block, byte for byte (cmp only)

PROCEDURE (in order; commit AND push at every numbered item):

0. Preconditions: `git status --porcelain` empty; branch is
   feature/f111-diff-only-repair; `git log -1 --format=%h` is d0952432.
   Verify the two stated digests. Any mismatch => STOP and hand back.

1. C1 — `cp .remedy-wt/f111r6/BLOCK .agent/authored/f111-r6-1.md`; `cmp`
   silent. Commit: chore(f111): save the R6 step block verbatim   -> push

2. C2 — `cp .agent/authored/f111-r6-1.md .agent/last_block.md`; `cmp` silent.
   Commit: chore(f111): mirror the R6 block into last block   -> push

3. C3 — FINDINGS FIRST: `cat .remedy-wt/f111r6/LRG >> .agent/live_review.md`
   PURE APPEND: `git show --numstat <C3> -- .agent/live_review.md` must read
   `63 0`. A nonzero delete column means a rewrite: STOP and hand back.
   Commit: chore(f111): record the R5 gate and findings R-0303 R-0304 -> push

4. C4 — resolve the three fixes the R5 gate reviewed. In
   `.agent/live_review.md`, delete the three consecutive lines that begin
   `Landed: R-0300`, `Landed: R-0301` and `Landed: R-0302`, and put the
   CONTENTS OF `.remedy-wt/f111r6/DONE3` in their place (read the file; do not
   retype it). The slice carries the blank separator line the three landed
   lines were missing — that is the R-0303 fix, so keep it.
   `git show --numstat <C4> -- .agent/live_review.md` must read `4 3`.
   Commit: chore(f111): resolve R-0300 R-0301 R-0302 at the R5 gate  -> push

5. C5 — rewrite `.agent/plan.md`, your own text, UNDER 50 lines, keeping the
   headings `## Goal` and `## Next Steps` (contract tests assert them). It
   must state: branch and merge base (main 4e0b762e); last reviewed SHA
   d0952432 (R5 PASS); next free finding ID R-0305; open findings 25; that
   T001 is complete (selector + range source, 30 tests) and STILL HAS NO CALL
   SITE; and Next Steps 1 = T002 on the `builder_bridge` seam
   (`run_builder_bridge_loop`), 2 = T003 wiring plus mode and token evidence,
   3 = integration gate, then closure. Keep the two existing Risks entries.
   Commit: chore(f111): rewrite the plan for the session close   -> push

6. C6 — rewrite `.agent/handoff.md`, your own text. COUNT THE LINES BEFORE
   COMMITTING (`wc -l`): 60 or fewer, or carry a DECISION D15 "Deviations,
   declared" line naming the REAL measured count and the mandated content that
   caused it. It must contain: feature and round (F111 R6, SESSION CLOSE); the
   branch; a per-commit SHA table for C1-C6 with insertions; a changed-files
   table; the real gate results below with commands and real exit codes; open
   findings 25 with next free ID R-0305; an item-status table over C1-C6, each
   item exactly once; this line verbatim, on its own line, as
   docs/agents/planner_reviewer_prompt.md section 3 requires and finding
   R-0304 records (copy it exactly):
Fortschritt: ~40 % (T001 ✅ Selektor + Range-Quelle · T002 offen · T003 offen) — Schätzung
   and a NEXT SESSION block stating, in this order:
     - the branch is UNMERGED and has NO PR by design; the next session's Open
       PR Gate does not apply because no PR exists — it resumes this branch
       directly, and Phase 0 must sweep `feature/*` branches (finding R-0290)
       because no probe command sees an unclaimed branch otherwise;
     - work completed this session: the R4 gate, then R5 — R-0300 closed,
       `parse_diff_line_ranges` and `changed_line_ranges_from_patch` built at
       30 tests and mutation-proved, DECISION F111 D2 and D3 on disk;
     - next action: T002, the versioned unified-diff response schema with a
       fence pre-check and strict all-or-nothing apply, on the
       `builder_bridge` seam — read `structured_patch.py` and the
       `apply_structured_patch` fence path BEFORE designing it;
     - the reviewer-side findings this session opened against its own blocks:
       R-0301, R-0302, R-0303, R-0304.
   Commit: chore(f111): write the session closing handoff   -> push

Done when (record command + real exit code + counted value; never the word
"green"):
  a. the two stated digests match; `cmp` BLOCK vs .agent/authored/f111-r6-1.md
     silent; `cmp` that file vs .agent/last_block.md silent.
  b. `git show --numstat <C3> -- .agent/live_review.md` -> `63 0`
     `git show --numstat <C4> -- .agent/live_review.md` -> `4 3`
  c. on the final `.agent/live_review.md`:
     `grep -c '^- R-0'` -> 29 ; `grep -c '^Done:'` -> 4
     `grep -c '^Landed:'` -> 0 (exit 1 is the pass)
     `grep -c '^### R5 — PASS'` -> 1
     python3 -c "import pathlib;print(pathlib.Path('.agent/live_review.md').read_text().count(pathlib.Path('.remedy-wt/f111r6/DONE3').read_text()))"
     -> exit 0, printed count 1
  d. `wc -l < .agent/plan.md` -> under 50; `wc -l < .agent/handoff.md` -> the
     real number, and 60 or fewer unless the D15 line declares it.
  e. `python3 -m pytest tests/orchestration/test_test_runner.py -q -k 'plan_md
     or context_md'` -> exit 0, 3 passed, 48 deselected. Do NOT run
     tests/ui_server/test_dashboard_contract.py (R-0221: it runs a real npm
     build mid-suite).
  f. `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed
     (canary).
  g. `python3 -m pytest tests/orchestration/test_diff_repair.py -q` -> exit 0,
     30 passed, unchanged: this round touches no code.
  h. `git status --porcelain` -> empty; `git worktree list` -> one entry;
     per-commit insertions each < 500;
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> `0 0` after the final push.
Handback:    completion report (per-commit table, changed-files table,
             item-status table over C1-C6, raw gate results) and
             `.agent/handoff.md` rewritten as C6. Do not merge, do not open a
             PR, do not touch `.agent/candidates.md` or `.agent/decisions.md`.
