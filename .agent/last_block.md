── STEP R5/5 — F111 Diff-only repair — the range source, proved by reading code ──
Goal:        Close R-0300 with the missing test, give T001 its real range
             source (`parse_diff_line_ranges` + `changed_line_ranges_from_patch`),
             and correct the two planning defects R-0301 and R-0302 in the
             feature file. Findings persist BEFORE any fix.
Bundle:      C1 block save; C2 last_block mirror; C3 findings append;
             C4 resolve R-0299; C5 code + tests; C6 docs; C7 Landed lines;
             C8 plan rewrite; C9 handoff. Commit AND push at every item.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f111-r5-1.md (new), .agent/last_block.md,
             .agent/live_review.md, packages/orchestration/review_scope.py,
             packages/orchestration/diff_repair.py,
             tests/orchestration/test_diff_repair.py,
             docs/roadmap/features/T2_F111.md, .agent/plan.md, .agent/handoff.md.
             Do NOT touch builder_bridge.py, repair_context.py, source_apply.py
             or pingpong_loop.py: this round builds the seam, T003 wires it.
Constraints: AGENTS.md in full. Apply every authored slice by READING ITS FILE
             (`cat`/`cp`) — never retype, never reflow, never reindent. Do NOT
             create a PR, do NOT merge, never touch main, never force-push.
             Write no `Done:` line of your own: the only `Done:` text in this
             round is the C4 text authored below. Scratch stays under
             .remedy-wt/. Feature file Do-not-touch: repair round counts and
             policy, applicator semantics, session resume.

AUTHORED SLICES — five files, each pinned by a stated sha256:
  .remedy-wt/f111r5/LRG     sha256=691a4cee1821a5dc56f33df6df78f257e7b3e27b2f9783801b77a0ad3fc3232b  59 lines, appended to .agent/live_review.md
  .remedy-wt/f111r5/RS      sha256=8e4f18cde48803b0767d5fb7e215c7538d8f96166485b4e7bcef5fa5c882c919  9 lines, inserted into review_scope.py
  .remedy-wt/f111r5/DR      sha256=f31bede5bb1694c83c383a5a43ce718c36ee5d6abe17242414cb14244d7b2bdc  25 lines, appended to diff_repair.py
  .remedy-wt/f111r5/TESTS   sha256=070f7003ca96eec3ce2339c2da9438c5d2e833f63a6dc3ec8cee86725320d6c3  120 lines, appended to test_diff_repair.py
  .remedy-wt/f111r5/FEATD3  sha256=0dc92ba0972fc99c2aac1f313a015621dbcea2215bf796fae842214e1fecff6f  19 lines, appended to T2_F111.md
  .remedy-wt/f111r5/BLOCK = this entire step block, byte for byte (cmp only)

PROCEDURE (in order; commit AND push at every numbered item):

0. Preconditions: `git status --porcelain` empty; branch is
   feature/f111-diff-only-repair; `git log -1 --format=%h` is c9064b17.
   Verify the five stated digests with `sha256sum`. Any mismatch => STOP and
   hand back without committing.

1. C1 — `cp .remedy-wt/f111r5/BLOCK .agent/authored/f111-r5-1.md`; `cmp` the
   two, silent. Commit: chore(f111): save the R5 step block verbatim   -> push

2. C2 — `cp .agent/authored/f111-r5-1.md .agent/last_block.md`; `cmp` silent.
   Commit: chore(f111): mirror the R5 block into last block   -> push

3. C3 — FINDINGS FIRST, before any fix:
   `cat .remedy-wt/f111r5/LRG >> .agent/live_review.md`
   PURE APPEND: `git show --numstat <C3> -- .agent/live_review.md` must read
   `59 0`. A nonzero delete column means a rewrite: STOP and hand back.
   Commit: chore(f111): record the R4 gate and findings R-0301 R-0302  -> push

4. C4 — resolve R-0299, whose fix the R4 gate above reviewed. Replace the
   single line in `.agent/live_review.md` that begins `Landed: R-0299` with
   the single line between the markers below (one line, no wrapping):
   <<<C4 REPLACEMENT LINE — REWRITE pair, FROM 0x / TO 1x after the edit>>>
Done: R-0299 — the `out_of_bounds` reason ships and is pinned. Verified at the R3 gate above: `_expand_and_merge_ranges` is unchanged, the discrimination happens at the call site, and the reviewer's own mutation red-proof in a disposable worktree turned exactly the two `TestOutOfBounds` tests red when the reason was reverted to a bare `no_ranges`. RESOLVED.
   <<<END C4 REPLACEMENT LINE>>>
   `git show --numstat <C4> -- .agent/live_review.md` must read `1 1`.
   Commit: chore(f111): resolve R-0299 at the R3 gate   -> push

5. C5 — code and its tests, ONE commit, three files:

   5a. `packages/orchestration/review_scope.py`. The file contains
       `    return files` followed by exactly two blank lines and then
       `def _detect_symbols(added_lines: list[str]) -> list[str]:`. Insert the
       CONTENTS OF `.remedy-wt/f111r5/RS` (read the file; do not retype it)
       after those two blank lines, then two more blank lines, so
       `_detect_symbols` keeps its two-blank-line separation.

   5b. `packages/orchestration/diff_repair.py`, three edits:
       (i) imports — APPEND-shaped pair, FROM occurs exactly 1x:
           FROM: from pathlib import Path
           TO (four lines, the blank line included):
from pathlib import Path

from packages.orchestration.review_scope import parse_diff_line_ranges
from packages.orchestration.structured_patch import StructuredPatch
       (ii) the module docstring's Public API list — APPEND-shaped pair,
            FROM occurs exactly 1x (8 leading spaces on the FROM line):
           FROM:         -> RepairHunkSelection
           TO (two lines):
        -> RepairHunkSelection
    changed_line_ranges_from_patch(patch) -> {path: [[start, end], ...]}
       (iii) append the new function: `printf '\n\n' >> the file`, then
             `cat .remedy-wt/f111r5/DR >> the file`. Two blank lines separate
             it from `select_repair_hunks`; the file ends `    return ranges`.

   5c. `tests/orchestration/test_diff_repair.py`, two edits:
       (i) the import block — REWRITE pair. Replace these five lines
from packages.orchestration.diff_repair import (
    RepairHunk,
    RepairHunkSelection,
    select_repair_hunks,
)
           with these seven (import order is ruff-isort's: classes, then
           functions, then the second module):
from packages.orchestration.diff_repair import (
    RepairHunk,
    RepairHunkSelection,
    changed_line_ranges_from_patch,
    select_repair_hunks,
)
from packages.orchestration.structured_patch import FileOp, StructuredPatch, UnifiedDiff
       (ii) `cat .remedy-wt/f111r5/TESTS >> the file`. The slice carries its
            own two leading blank lines; add none.

   Commit: feat(f111): derive repair line ranges from the applied patch  -> push

6. C6 — `docs/roadmap/features/T2_F111.md`, two edits:
   (i) DECISION F111 D2, the R-0301 fix — REWRITE pair, one line, FROM 1x:
       FROM: `packages/orchestration/builder_bridge.py` (`run_bounded_repair_loop`), whose
       TO:   `packages/orchestration/builder_bridge.py` (`run_builder_bridge_loop`), whose
   (ii) DECISION F111 D3, the R-0302 fix:
       `cat .remedy-wt/f111r5/FEATD3 >> the file`. The slice carries its own
       leading blank line; the file ends with the D3 paragraph.
   Commit: docs(f111): correct the loop name and record the range source -> push

7. C7 — three `Landed:` lines appended to `.agent/live_review.md`, YOUR OWN
   words, one line each, in this order: R-0300, R-0301, R-0302. Each names
   what changed and its commit BY SUBJECT, never by a SHA it cannot contain.
   Write no `Done:` line and no paragraph — one `Landed:` line per finding.
   `git show --numstat <C7> -- .agent/live_review.md` must read `3 0`.
   Commit: chore(f111): mark the R5 fixes as landed   -> push

8. C8 — rewrite `.agent/plan.md`, your own text, UNDER 50 lines, keeping the
   headings `## Goal` and `## Next Steps` (contract tests assert them). It
   must state: branch and merge base (main 4e0b762e); last reviewed SHA
   c9064b17 (R4 PASS); next free finding ID R-0303; open findings 26; that
   T001 now has both its selector and its range source, with NO call site yet;
   and Next Steps 1 = T002 (versioned unified-diff response schema, fence
   pre-check, strict apply with all-or-nothing fallback) on the
   `builder_bridge` seam, 2 = T003 wiring `changed_line_ranges_from_patch`
   into `run_builder_bridge_loop` plus mode/token evidence, 3 = integration
   gate, then closure. Delete the falsified `source_patch_applied` hypothesis;
   it is now recorded as R-0302 and DECISION F111 D3.
   Commit: chore(f111): rewrite the plan after the range source lands  -> push

9. C9 — rewrite `.agent/handoff.md`, your own text. COUNT THE LINES BEFORE
   COMMITTING (`wc -l`): 60 or fewer, or carry a DECISION D15 "Deviations,
   declared" line naming the real count and the mandated content that caused
   it. It must contain: feature and round (F111 R5); the branch; a per-commit
   SHA table for C1-C9 with insertions; a changed-files table; the real gate
   results from "Done when" below, each with its command and REAL exit code
   and counted value; open findings 26 with next free ID R-0303; an
   item-status table over C1-C9, each item exactly once; and the next
   expected action (T002).
   Commit: chore(f111): write the R5 handoff   -> push

Done when (record command + real exit code + counted value; never the word
"green"):
  a. the five stated digests match; `cmp` BLOCK vs .agent/authored/f111-r5-1.md
     silent; `cmp` that file vs .agent/last_block.md silent.
  b. `git show --numstat <C3> -- .agent/live_review.md` -> `59 0`
     `git show --numstat <C4> -- .agent/live_review.md` -> `1 1`
     `git show --numstat <C7> -- .agent/live_review.md` -> `3 0`
  c. on the final `.agent/live_review.md`:
     `grep -c '^- R-0'` -> 27 ; `grep -c '^Landed:'` -> 3
     `grep -c '^Landed: R-0299'` -> 0 (exit 1 is the pass)
     `grep -c '^Done:'` -> 1 ; `grep -c '^### R4 — PASS'` -> 1
  d. verbatim application of the four content slices, exactly once each:
     python3 -c "import pathlib;[print(t,pathlib.Path(t).read_text().count(pathlib.Path(s).read_text())) for s,t in [('.remedy-wt/f111r5/RS','packages/orchestration/review_scope.py'),('.remedy-wt/f111r5/DR','packages/orchestration/diff_repair.py'),('.remedy-wt/f111r5/TESTS','tests/orchestration/test_diff_repair.py'),('.remedy-wt/f111r5/FEATD3','docs/roadmap/features/T2_F111.md')]]"
     -> exit 0 and every printed count is 1.
     `grep -c '^def parse_diff_line_ranges' packages/orchestration/review_scope.py` -> 1
     `grep -c '^def changed_line_ranges_from_patch' packages/orchestration/diff_repair.py` -> 1
     `grep -c '^from packages.orchestration.review_scope import' packages/orchestration/diff_repair.py` -> 1
     `grep -c '^    changed_line_ranges_from_patch,' tests/orchestration/test_diff_repair.py` -> 1
  e. on `docs/roadmap/features/T2_F111.md`:
     `grep -c 'run_bounded_repair_loop'` -> 0 (exit 1 is the pass)
     `grep -c 'run_builder_bridge_loop'` -> 2
  f. `python3 -m pytest tests/orchestration/test_diff_repair.py -q` -> exit 0,
     30 passed (21 before this round)
     `python3 -m pytest tests/orchestration/test_review_scope.py -q` -> exit 0,
     32 passed (unchanged)
     `python3 -m pytest tests/docs/ -q` -> exit 0, 294 passed (docs-round gate,
     planner_reviewer_prompt.md section 3, this round touches docs/roadmap/**)
     `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed
     (canary)
     `python3 -m ruff check packages/orchestration/diff_repair.py
      packages/orchestration/review_scope.py
      tests/orchestration/test_diff_repair.py` -> exit 0
  g. MUTATION RED-PROOF, inside a DISPOSABLE worktree only, never in the
     primary checkout: `git worktree add .remedy-wt/f111r5wt HEAD`; in THAT
     copy delete the two lines
         for file_op in patch.file_ops:
             ranges.setdefault(file_op.path, [])
     from `packages/orchestration/diff_repair.py`, run
     `python3 -m pytest tests/orchestration/test_diff_repair.py -q` there, and
     record the real counts. EXPECTED: 2 failed, 28 passed —
     `test_file_ops_paths_carry_no_lines` and
     `test_a_file_ops_path_is_reported_as_no_ranges_by_selection`. Report what
     actually happened, including a different number. Then
     `git worktree remove --force .remedy-wt/f111r5wt` and
     `git worktree prune`; `git worktree list` must show one entry.
  h. `git status --porcelain` -> empty; per-commit insertions each < 500;
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> `0 0` after the final push.
Handback:    completion report (per-commit table, changed-files table,
             item-status table over C1-C9, raw gate results) and
             `.agent/handoff.md` rewritten as C9. Do not merge, do not open a
             PR, do not touch `.agent/candidates.md` or `.agent/decisions.md`.
