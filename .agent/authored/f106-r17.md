── STEP REPAIR-R0760/1 — F106 ─────────────────────────────────────────────
Goal: Repair R-0760 (Medium, OPEN, registered round 16's integration gate):
add the additive `resume: str | None = None` no-op parameter to all seven
signatures across three test-double files, the same fix shape that already
closed R-0758 and R-0759 twice before. Test-only, zero production code
change.

Bundle:
  C0a — save this step block verbatim to .agent/authored/f106-r17.md
  C0b — mirror it into .agent/last_block.md
  C1  — rewrite .agent/plan.md for round 17 (PLAN17 below)
  C2  — apply the seven REWRITE pairs below to
        tests/orchestration/test_structured_outputs.py,
        tests/orchestration/test_worktree_isolation.py and
        tests/orchestration/test_worktree_persistence.py
  C3  — append the LANDED marker below (with <PIN> replaced by C2's real
        commit SHA) to .agent/live_review.md, ONE paragraph; run the full
        suite to confirm the gate is clean
  C4  — rewrite .agent/handoff.md for round 17 handback

Change: exactly the three test files named above, plus the four .agent/**
paths named in C0a/C0b/C1/C3/C4. No path under packages/, apps/, docs/.

Constraints:
1. C0a/C0b verbatim single-.agent-state-file saves (shutil.copyfile, never
   cp, never retyped), exempt from the 500-line cap.
2. C1 — PLAN17 is a REWRITE of .agent/plan.md, applied via shutil.copyfile
   from .remedy-wt/f106-r17-plan.md (33 lines, < 50, holds `## Goal`/
   `## Next Steps`, sha256
   9f8a09758dd897b7aad967beb83b29b5452aaee3305192b08e7e7f9df330cc5c, 1524
   bytes).
3. C2 — SEVEN REWRITE pairs, each independently verified by the reviewer
   before this block was authored (FROM occurs exactly 1x, anchored at a
   real line start, in its named file; `TO contains FROM: false` for
   every one — the closing `):` in FROM never survives into TO unbroken).
   Apply all seven; each file's expected post-commit state is given so you
   can confirm without guessing:

     tests/orchestration/test_structured_outputs.py (FROM baseline 26832
     bytes, sha256 0c321dc59b78a3db24b16cbae2ec569093378266b4ade0bde24f714a37bfb926):
       PAIR1 (line 342, `_FlakyReviewer.review`):
         FROM: "            def review(self, prompt, *, timeout_sec=120, max_output_chars=50000):"
         TO:   "            def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):"
       PAIR2 (line 389, `_RecordingReviewer.review`):
         FROM: "    def review(self, prompt, *, timeout_sec=120, max_output_chars=50000):"
         TO:   "    def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):"
       Expected post-commit: 26886 bytes, sha256
       656c5916ea35d58bcd6e1ca4ccce587a7769c77b663f7b9ed6597490b2570211.

     tests/orchestration/test_worktree_isolation.py (FROM baseline 10102
     bytes, sha256 d2479dbee3ddd8b103568ee9d154391c40358a6f3cb4aa37ae40ca399b827aca):
       PAIR3 (line 53, `_WritingBuilder.build`):
         FROM: "    def build(self, prompt, *, timeout_sec=120, max_output_chars=50000):"
         TO:   "    def build(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):"
       PAIR4 (line 62, `_WritingBuilder.review`):
         FROM: "    def review(self, prompt, *, timeout_sec=120, max_output_chars=50000):"
         TO:   "    def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):"
       PAIR5 (line 166, `_FailingBuilder.build`):
         FROM: "            def build(self, prompt, *, timeout_sec=120, max_output_chars=50000):"
         TO:   "            def build(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):"
       Expected post-commit: 10183 bytes, sha256
       98fa48566736aa0611e65ab033d8e95c113f51f2aa96e9a60c5804a25cd93040.

     tests/orchestration/test_worktree_persistence.py (FROM baseline 15871
     bytes, sha256 c13813acf376244a6ab0934c6a890ff0c72a8eddc658fde64519164f7cfbf0c6):
       PAIR6 (line 61, `_WritingProvider.build`):
         FROM: "    def build(self, prompt, *, timeout_sec=120, max_output_chars=50000):"
         TO:   "    def build(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):"
       PAIR7 (line 68, `_WritingProvider.review`):
         FROM: "    def review(self, prompt, *, timeout_sec=120, max_output_chars=50000):"
         TO:   "    def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):"
       Expected post-commit: 15925 bytes, sha256
       e0d61bc926300155c10392fee74d0230d3521d206c3fedd85e0df84bc9cc6680.

   This was dry-run verified by the reviewer before this block was
   authored, in a disposable worktree, never the tracked files: `ast.parse`
   clean on all three post-edit files, `ruff check` clean (repo's own
   pyproject config, not --isolated), and `python3 -m pytest
   tests/orchestration/test_structured_outputs.py
   tests/orchestration/test_worktree_isolation.py
   tests/orchestration/test_worktree_persistence.py -q` 76 passed (0
   failed) — you are REPRODUCING this against the real tracked files, not
   discovering it fresh.
4. C3 — ONE paragraph appended to .agent/live_review.md, never retyped:
   LANDED (.remedy-wt/f106-r17-landed.txt, 656 bytes, sha256
   a746b25baafd3a2afcba724edabc37ed1dede02e45f32437e7c2b2962720346b) with
   its single `<PIN>` token (5 bytes) replaced by C2's real 40-hex-char
   commit SHA — the ONLY edit permitted to the copied text, applied AFTER
   the copy, never retyped otherwise. Re-measure the file's own base
   length and trailing-newline state before appending: at this round's
   base the file is 1886178 bytes and does NOT end in a trailing newline,
   so the separator is "\n\n". No total byte count is given here — it
   depends on the real SHA the substitution inserts, which does not exist
   until C2 lands, so YOU compute and report the real post-commit
   bytes/sha256 yourself (G4 checks that computation, not a number stated
   in advance). This paragraph does NOT set the finding Resolved — only
   reviewer-authored `Done:` text does that (§4 item 4); this is why the
   text says `NOT RESOLVED` in its own closing sentence, and you must not
   alter that sentence.
5. C3's suite run: `python3 -m pytest -n auto -q` — record the REAL exit
   code, FAILED count (expect 0, confirming R-0760's own 25 ids are gone),
   passed/skipped counts and wall time. This is NOT a second dedicated
   integration-gate round (no base-worktree comparison this round — a
   test-only fix cannot introduce a base-only failure, and re-running the
   base side would spend a round's worth of wall clock proving a null
   result) — it is this round's own scoped verification, at the tier-1
   round-gate level, run at full-suite breadth because that is what proves
   R-0760's fix. The reviewer will authorize the CLOSURE-GRADE integration
   gate re-run (both sides) as part of confirming precondition 2, separate
   from this round.
6. C4 — .agent/handoff.md rewrite per AGENTS.md's handoff contract: state,
   SESSION 5, branch, commit SHAs, a changed-files table, this round's
   real G1-G8 results (numbers, never "green"), open-findings count (321
   registered, R-0760 now LANDED but not yet Resolved — that distinction
   named explicitly), and next expected action: the reviewer re-runs the
   full suite independently to confirm R-0760's fix, then authors the
   `Done: R-0760` resolution and a closure-grade integration-gate
   confirmation as the next round's own work.

Done when (run every command yourself; record REAL exit codes, never the
word "green"):
G1 TRANSPORT — .agent/authored/f106-r17.md and .agent/last_block.md both
   sha256-equal to this block as saved (single digest comparison).
G2 THE PLAN — .agent/plan.md sha256
   9f8a09758dd897b7aad967beb83b29b5452aaee3305192b08e7e7f9df330cc5c, 33
   lines (`wc -l`), holds `## Goal` and `## Next Steps`.
G3 THE SEVEN PAIRS — each of the three files' post-commit bytes/sha256
   match constraint 3's stated expectations exactly; `git diff --stat` for
   the whole round shows exactly these three files under `tests/` and
   nothing under `packages/`, `apps/`, `docs/`.
G4 LIVE_REVIEW APPEND — .agent/live_review.md's real post-commit bytes and
   sha256, as you computed and reported them under constraint 4; its last
   `\n\n`-delimited unit is byte-equal to the LANDED text WITH the
   substitution applied, and that unit contains zero occurrences of the
   literal string `<PIN>`; that unit ends in the exact sentence "NOT
   RESOLVED: only reviewer-authored `Done:` text closes it.", unaltered.
G5 THE LEDGER — `grep -cE '^- R-[0-9]{4} — '`,
   `grep -cE '^Done: R-[0-9]{4} — '`, `grep -cE '^DECISION F[0-9]+ D[0-9]+ — '`
   over .agent/live_review.md read 321, 59, 20 — IDENTICAL before (base)
   and after (HEAD) this round: a `Landed:` line is not a `Done:` line and
   spends no ledger movement.
G6 THE TESTS — `python3 -m pytest -n auto -q` REAL exit 0 (expect 0
   failed, ~18736 passed including the previously-failing 25, 20 skipped —
   report the REAL numbers, these are the reviewer's own pre-emission
   prediction, not an assertion to force); `ast.parse`/`ruff check` on all
   three edited files: exit 0 each.
G7 ZERO PRODUCTION CHANGE — `git diff --stat` for every path under
   `packages/` over the whole round is EMPTY.
G8 THE TREE — `git status --porcelain` empty; every commit's insertions
   under 500 (C0a/C0b exempt as verbatim `.agent/**` state-file saves);
   canary (`pytest tests/cli/test_golden_path.py -q`) REAL exit 0; HEAD
   pushed and equal to `origin/feature/f106-session-resume`.

Handback: completion report + rewrite .agent/handoff.md (C4 above). State
the real numbers for every gate above, not the word "green". Name every
deviation, however small.
─────────────────────────────────────────────────────────────────────────
