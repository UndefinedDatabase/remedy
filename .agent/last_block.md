── STEP CLOSURE-BUILTSTATE/1 — F106 ──────────────────────────────────────
Goal: Satisfy closure precondition 4 (feature file's Built State section is
current) by appending a Built State section to
docs/roadmap/features/T3_F106.md describing what T001-T003 actually built,
with real file/function citations and the T003 measured byte-reduction
numbers. Register DECISION F106 D2, resolving the feature file's own Scope
note (job/mission resume-from-persisted-state, F075 candidate routing
R-0201) against Task slicing: close F106 on T001-T003 alone, carrying the
job/mission-resume half forward as a closure-commit candidate rather than
building it now or dropping it silently.

Bundle:
  C0a — save this step block verbatim to .agent/authored/f106-r19.md
  C0b — mirror it into .agent/last_block.md
  C1  — rewrite .agent/plan.md for round 19 (PLAN19 below)
  C2  — append the Built State section to
        docs/roadmap/features/T3_F106.md (APPEND pair, below)
  C3  — append DECISION F106 D2 (one paragraph) to .agent/live_review.md
  C4  — rewrite .agent/handoff.md for round 19 handback

Change: exactly the .agent/** paths of C0a/C0b, .agent/plan.md,
docs/roadmap/features/T3_F106.md, .agent/live_review.md and
.agent/handoff.md. No path under packages/, apps/, tests/.

Constraints:
1. C0a/C0b verbatim single-.agent-state-file saves (shutil.copyfile, never
   cp, never retyped), exempt from the 500-line cap.
2. C1 — PLAN19 is a REWRITE of .agent/plan.md, applied via shutil.copyfile
   from .remedy-wt/f106-r19-plan.md (33 lines, < 50, holds `## Goal`/
   `## Next Steps`, sha256
   084510784d8b9df15dd31223d7ea44df4736c813cfab87a63f62ac24b4b22609, 1536
   bytes).
3. C2 — an APPEND pair on docs/roadmap/features/T3_F106.md. TO contains
   FROM verbatim as a prefix (containment test run at emission: true).
   FROM is the file's own trailing paragraph starting `## Scope note
   (F075 candidate routing, 2026-08-06)` through end of file — 501 bytes,
   sha256 07532a048612db00c45b405e7b9f3b593a6b66a16f724306e45ca31e551dbc5f,
   occurring exactly 1x in the base file. TO is FROM + one `\n` + the
   verbatim contents of .remedy-wt/f106-r19-builtstate.txt (1950 bytes,
   sha256 0fb23b0b804c00ca359d93071f5ba68ec43cb48fa0f9770f8ff27f438942719a,
   itself never retyped, applied via shutil.copyfile) — TO totals 2452
   bytes, sha256
   e88c497fd5739a4841180a4daa6f0a7a155b613b50bc5a7c642404347652e842. The
   base file is 4025 bytes before this commit; the post-commit file is
   base + 1 + 1950 = 5976 bytes, sha256
   1c4abe34db9508e1113b31ce90bb498fd89b419ad6d64cac779b9f849a5df5c7, 113
   lines (`wc -l`).
4. C3 — a ONE-PARAGRAPH append to .agent/live_review.md, never retyped,
   applied via shutil.copyfile from .remedy-wt/f106-r19-decision2.txt
   (4485 bytes, sha256
   779fdc9148fc654a1e28ec7e087b162af2f95a59ad2cfa72450154ef89ae050d, zero
   internal newlines, no trailing newline). Re-measure the file's own base
   length before appending: at this round's base the file is 1895281 bytes
   and does NOT end in a trailing newline, so the separator is "\n\n" (this
   file's own convention). Expected total: base + 2 + 4485 = 1899768
   bytes, sha256
   03f4719e80889a685c22fc0c6eb41f69155ba1a9cd5329478f7c746a5c499757. (If
   your own measured total differs from this arithmetic, recompute the sum
   yourself rather than trusting either number blindly, and state which
   number you land on and why.)
5. C4 — .agent/handoff.md rewrite per AGENTS.md's handoff contract: state,
   SESSION 6, branch, commit SHAs, a changed-files table, this round's
   real gates (below), open-findings count (321 registered, 60 resolved,
   21 decisions — up from 20), and next expected action: closure
   precondition 4 is MET and DECISION F106 D2 is registered; the next
   round addresses closure precondition 3
   (`remedy integrity check --json` / no relevant untracked files) and
   precondition 6 (self-use track consumption), naming that DECISION F106
   D2 obliges the eventual closure commit to add ONE entry to
   .agent/candidates.md (the exact text is in DECISION F106 D2 itself).

Done when (run every command yourself; record REAL exit codes, never the
word "green"):
G1 TRANSPORT — .agent/authored/f106-r19.md and .agent/last_block.md both
   sha256-equal to this block as saved (single digest comparison).
G2 THE PLAN — .agent/plan.md sha256
   084510784d8b9df15dd31223d7ea44df4736c813cfab87a63f62ac24b4b22609, 33
   lines (`wc -l`), holds `## Goal` and `## Next Steps`.
G3 THE FEATURE FILE APPEND — docs/roadmap/features/T3_F106.md's real
   post-commit bytes and sha256 (compute and report; constraint 3 gives
   the expected arithmetic but you verify it, not assume it); the file's
   tail is byte-equal to the TO text of constraint 3; `grep -c '^## Built
   State' docs/roadmap/features/T3_F106.md` reads exactly 1, and
   `grep -n '^## '` shows it is the LAST such heading in the file.
G4 THE LEDGER APPEND — .agent/live_review.md's real post-commit bytes and
   sha256 (compute and report; constraint 4 gives the expected arithmetic
   but you verify it, not assume it); the file's last `\n\n`-delimited
   unit is byte-equal to the DECISION F106 D2 text; negative control —
   flip one byte inside a SCRATCH copy of that text and confirm the
   flipped copy no longer byte-equals the file's own last unit (never
   mutate the tracked file itself).
G5 THE LEDGER COUNTS — over .agent/live_review.md at HEAD:
   `grep -cE '^- R-[0-9]{4} — '` reads 321 (unmoved — no new finding id
   this round); `grep -cE '^Done: R-[0-9]{4} — '` reads 60 (unmoved);
   `grep -cE '^DECISION F[0-9]+ D[0-9]+ — '` reads 21 (up from 20 —
   exactly `DECISION F106 D2` added, confirmed by
   `grep -c '^DECISION F106 D2 — '` reading exactly 1).
G6 THE DOCS GATE — `python3 -m pytest tests/orchestration/test_roadmap_index.py
   tests/docs/ -q`: REAL exit 0; report the passed count (325 at this
   round's base — confirm it is unchanged or explain any difference).
G7 THE TREE — `git status --porcelain` empty; every commit THROUGH C3's
   insertions under 500 (C0a/C0b exempt as verbatim `.agent/**`
   state-file saves; C4's own insertions are reported in the handback,
   not gated here, since C4 is the handback commit itself); canary
   (`pytest tests/cli/test_golden_path.py -q`) REAL exit 0; HEAD pushed
   and equal to `origin/feature/f106-session-resume`.

Handback: completion report + rewrite .agent/handoff.md (C4 above). State
the real numbers for every gate above, not the word "green". Name every
deviation, however small.
─────────────────────────────────────────────────────────────────────────
