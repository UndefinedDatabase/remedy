── STEP T003/1 — F106 ──────────────────────────────────────────────────
Goal: Close T003, the last open item on F106: a fixture repair chain that
shows a MEASURED prompt-byte reduction when a repair round resumes versus
when it resends full context (the feature's own Goal & Done acceptance
criterion, docs/roadmap/features/T3_F106.md), plus a built-state doc
recording the measured numbers. Zero production code changes — T001 and
T002 (both sides, closed rounds 2-14) already wired the mechanism this
round measures and documents. Also books round 14's already-produced
verdict (RECORD14) and its two prose-only notes into the permanent record,
per amend0827-process-diet rule 1 (a pushed handoff is a durable carrier;
its verdict is booked in the first round that is happening anyway, not a
round of its own).

Bundle:
  C0a — save this step block verbatim to .agent/authored/f106-r15.md
  C0b — mirror it into .agent/last_block.md
  C1  — rewrite .agent/plan.md for round 15 (PLAN15 below)
  C2  — append RECORD14 (booking round 14's PASS) to .agent/live_review.md,
        ONE paragraph
  C3  — append two dated lines (PROSESLIPR14A, PROSESLIPR14B) to
        .agent/prose_slips.md, in that order
  C4  — append the new test class below to
        tests/orchestration/test_session_resume.py
  C5  — add docs/system/session-resume-v1.md (SESSIONRESUMEDOC below,
        with <PIN> replaced by C4's real commit SHA before writing),
        register it in docs/README.md (two rows: PAIR-QUICKFIND,
        PAIR-SYSTABLE below), and append PAIR-BACKLINK below to
        docs/system/diff-only-repair-v1.md's "## Related" section
  C6  — rewrite .agent/handoff.md for round 15 handback

Change: exactly tests/orchestration/test_session_resume.py,
docs/system/session-resume-v1.md (new file), docs/README.md,
docs/system/diff-only-repair-v1.md, plus the six .agent/** paths named in
C0a/C0b/C1/C2/C3/C6. No path under packages/ — this round is tests + docs
only, zero production code.

Constraints:
1. C0a/C0b verbatim single-.agent-state-file saves (shutil.copyfile, never
   cp, never retyped), exempt from the 500-line cap.
2. C1 — PLAN15 is a REWRITE of .agent/plan.md, applied via
   shutil.copyfile from .remedy-wt/f106-r15-plan.md (30 lines, < 50, holds
   `## Goal`/`## Next Steps`, sha256
   838177464fd521896c771661e074221aa1dcfb96a3277ea3a5fbf5838564a97f, 1235
   bytes).
3. C2 — ONE paragraph appended to .agent/live_review.md, never retyped:
   RECORD14 (.remedy-wt/f106-r15-record14.txt, 4350 bytes, sha256
   d8f6d0bc7c3b3133024f52d07d6a8c4588ad8bdd550458263511e03dedf9e5b7).
   Re-measure the file's own base length and trailing-newline state before
   appending. At this round's base the file is 1874218 bytes and does NOT
   end in a trailing newline, so the separator is "\n\n". Expected total:
   base + 2 + 4350 = base + 4352 = 1878570 bytes, sha256
   cf49bcaf444168e6f0890a09aa6ef746ecf9f27e06e5b05c05f8d0ab849ab2b1.
4. C3 — TWO paragraphs appended to .agent/prose_slips.md, never retyped,
   IN ORDER: PROSESLIPR14A (.remedy-wt/f106-r15-prose1.txt, 398 bytes,
   sha256 3858b346007ba262edac9a1da178dd0d74f860996c739b9545c7deb1161b18a4)
   then PROSESLIPR14B (.remedy-wt/f106-r15-prose2.txt, 370 bytes, sha256
   5dd71bfb281070c1bf024363a2351ef39130f83f50ed8c1a1f52ef12c1a20bfd). THIS
   FILE'S OWN CONVENTION: every entry, including these two, already carries
   its own trailing newline (re-verify: the file's current last byte is
   `\n`), so the append is base + "\n" + PROSESLIPR14A + "\n" +
   PROSESLIPR14B — single-newline separators, not "\n\n" (this file's
   convention differs from live_review.md's; do not copy constraint 3's
   arithmetic here). Expected total at this round's base (38444 bytes):
   38444 + 1 + 398 + 1 + 370 = 39214 bytes, sha256
   aa2627345eb174400e9e32e15446121c79270aee22378cb916666f7e47ffff22.
5. C4 — APPEND-shaped pair against tests/orchestration/test_session_resume.py:
   FROM is the file's real current EOF (the file has no lines after
   `assert all(rd.reviewer_output.resume_fallback is False for rd in
   result.rounds)\n` — 15293 bytes, sha256
   c90746200c1613821bb5f1de789028057a3f62fb52647e90ef129f7e5e7e5681); TO is
   FROM plus the exact text of .remedy-wt/f106-r15-test-append.txt (3645
   bytes, sha256 1ed3d46b20abfa6c93c34ba60601f4a12a74d1630c626cb9198ed841da33b402)
   appended verbatim, never retyped (shutil.copyfile the base, then a
   single open(...,'ab').write() of the scratch bytes, or equivalent).
   Expected post-commit file: 18938 bytes, sha256
   b0eb31478b0ed1c2fd6f96ae2537ed391b8f7ebecac49c215fa938009c83d008. This
   was dry-run verified by the reviewer before this block was authored, in
   a disposable scratch copy, never the tracked file: `ast.parse` clean,
   `ruff check` clean (repo's own pyproject config, not --isolated), and
   `pytest <scratch copy> -q` 27 passed (26 pre-existing + 1 new) — you are
   REPRODUCING this against the real tracked file, not discovering it
   fresh. Do not alter the test's logic, fixtures, or assertions; the two
   `print(...)` lines inside the new test are DELIBERATE evidence output
   (docs/system/session-resume-v1.md's measured table cites them), not
   debug leftovers — keep them.
6. C5a — docs/system/session-resume-v1.md is a NEW file: copy
   .remedy-wt/f106-r15-doc.md (5699 bytes, sha256
   c27ea0a2600cefd419a5b59baab13ea3dba697cc1c83bb7f341e286484c5e30d)
   verbatim via shutil.copyfile, THEN replace the single literal token
   `<PIN>` (appears exactly once, in the "Measured at commit" sentence)
   with C4's real commit SHA (a plain string replace on the one token —
   this is the ONLY edit permitted to the copied text; every other byte
   stays exactly as scratch). The measured-numbers table (Builder
   1331/1384, Reviewer 2208/2270) is not a projection — it is the real
   output of running the C4 test (`pytest
   tests/orchestration/test_session_resume.py -k T003MeasuredTokenReduction
   -s`, printed lines) after C4 lands; re-run it and confirm the four
   numbers match before C5, and if they do not, STOP and report rather
   than editing the doc's numbers to match a different reading — a
   mismatch means either the dry-run above was not reproduced faithfully
   or something in this environment differs, and either way is a finding,
   not a rounding error to paper over.
7. C5b — PAIR-QUICKFIND, a REWRITE against docs/README.md's Quick-Find
   Table (mechanically verified by the reviewer: FROM occurs exactly 1x
   pre-commit, TO 0x pre-commit, `TO contains FROM: false`):
     FROM (2 lines, exact, currently lines 63-64):
       "| self-dogfood | [self-dogfood-execution-v0.md](system/self-dogfood-execution-v0.md) | system |\n| snapshot | [snapshot-rollback-v1.md](system/snapshot-rollback-v1.md) | system |\n"
     TO:
       "| self-dogfood | [self-dogfood-execution-v0.md](system/self-dogfood-execution-v0.md) | system |\n| session resume | [session-resume-v1.md](system/session-resume-v1.md) | system |\n| snapshot | [snapshot-rollback-v1.md](system/snapshot-rollback-v1.md) | system |\n"
   Re-grep both anchor lines' exact current byte content before applying —
   this branch has not touched docs/README.md before, so they should be
   unmoved from what is quoted here, but verify rather than assume.
8. C5c — PAIR-SYSTABLE, a REWRITE against docs/README.md's System
   Documentation table (mechanically verified, same shape as C5b),
   currently lines 137-138:
     FROM (2 lines, exact):
       "| [self-use-track-v1.md](system/self-use-track-v1.md) | Self-use track: the curated queue, the job-file format, one item consumed per feature close |\n| [snapshot-rollback-v1.md](system/snapshot-rollback-v1.md) | Snapshot/rollback proof system |\n"
     TO:
       "| [self-use-track-v1.md](system/self-use-track-v1.md) | Self-use track: the curated queue, the job-file format, one item consumed per feature close |\n| [session-resume-v1.md](system/session-resume-v1.md) | Provider session resume + delta-prompt shrink: capability surface, resume threading, fallback-once, and the measured reduction |\n| [snapshot-rollback-v1.md](system/snapshot-rollback-v1.md) | Snapshot/rollback proof system |\n"
9. C5d — PAIR-BACKLINK, an APPEND-shaped pair against
   docs/system/diff-only-repair-v1.md (mechanically verified: TO contains
   FROM):
     FROM = the file's real current WHOLE-FILE bytes, 5246 bytes, sha256
     6bcb06cb68ea081a54f85ce9b53db20844e7d3a2b9995b169003c968ee5b4a08
     (ends "...never applies code and never calls a provider.\n-
     `docs/roadmap/features/T2_F111.md` — the target spec and its
     decisions.\n" — re-read the WHOLE file yourself before applying; the
     pair is the full-file byte-exact prefix, not the tail excerpt shown
     here for anchoring).
     TO = FROM plus, appended at EOF:
       "- [session-resume-v1.md](session-resume-v1.md) — reuses `select_repair_hunks`/`render_repair_hunks` for a different purpose: shrinking a REPAIR PROMPT under an active resumed session, never applying a patch; DECISION F111 D1 (no diff-apply seam in `pingpong_loop.py`) is unchanged.\n"
     Expected post-commit file: 5530 bytes, sha256
     243f7d692c331a7e71e3742b3aa86e62f8ca6fd10573ea85da218edc702634ee.
10. C5 touches no path outside docs/system/session-resume-v1.md,
    docs/README.md, docs/system/diff-only-repair-v1.md. No packages/ path,
    no test path, in C5.
11. C6 — .agent/handoff.md rewrite: state and F106's SESSION NUMBER (still
    5, this is the session's only round), branch, commit SHAs, a
    changed-files table, this round's real verification results (all 8
    gates below with real numbers, not "green"), open-findings count
    (unchanged at this round — no new R-id), and next expected action:
    F106 moves to CLOSURE next round, per
    docs/roadmap/STATUS_closure_protocol.md (evidence job + fresh review
    zip, the authored STATUS line, PR creation) — T001, T002 (both sides)
    and T003 are now ALL closed.

Done when (run every command yourself; record REAL exit codes, never the
word "green"):
G1 TRANSPORT — .agent/authored/f106-r15.md and .agent/last_block.md both
   sha256-equal to this block as saved (single digest comparison).
G2 THE PLAN — .agent/plan.md sha256 838177464fd521896c771661e074221aa1dcfb96a3277ea3a5fbf5838564a97f,
   30 lines (`wc -l`), holds `## Goal` and `## Next Steps`.
G3 LIVE_REVIEW APPEND — .agent/live_review.md is 1878570 bytes, sha256
   cf49bcaf444168e6f0890a09aa6ef746ecf9f27e06e5b05c05f8d0ab849ab2b1; its
   last `\n\n`-delimited unit is byte-equal to RECORD14
   (.remedy-wt/f106-r15-record14.txt); negative control — flip one byte
   inside that last unit in a SCRATCH copy and confirm the flipped copy no
   longer byte-equals RECORD14 (never mutate the tracked file itself).
G4 PROSE_SLIPS APPEND — .agent/prose_slips.md is 39214 bytes, sha256
   aa2627345eb174400e9e32e15446121c79270aee22378cb916666f7e47ffff22.
G5 THE LEDGER — `grep -cE '^- R-[0-9]{4} — '`,
   `grep -cE '^Done: R-[0-9]{4} — '` and
   `grep -cE '^DECISION F[0-9]+ D[0-9]+ — '` over .agent/live_review.md
   read 320, 59 and 20 respectively, IDENTICAL before (base) and after
   (HEAD) this round's C2 — this round adds no new finding.
G6 THE CODE — zero production change: `git diff --stat` for every path
   under `packages/` over the whole round is EMPTY.
G7 TESTS AND DOCS — `python3 -m pytest tests/orchestration/test_session_resume.py -q`
   REAL exit 0, 27 passed (26 pre-existing + 1 new); the new test's two
   `print(...)` lines, re-run with `-s -k T003MeasuredTokenReduction`,
   read `resumed=1331 full=1384` (builder) and `resumed=2208 full=2270`
   (reviewer) and both inequalities hold; `ast.parse`/`ruff check` on
   tests/orchestration/test_session_resume.py exit 0; `python3 -m pytest
   tests/docs/ -q` REAL exit 0, 295 passed (this round's own base reading,
   re-confirmed by the reviewer before this block was authored; docs/README.md
   is in `PRIMARY_DOCS` and its markdown links are swept by
   `TestPrimaryDocLinksResolve`, so this gate is meaningful for C5, not
   vacuous); docs/README.md contains exactly one
   occurrence each of `session-resume-v1.md` in the Quick-Find Table and
   in the System Documentation table (2 total, `grep -c` over the whole
   file); docs/system/session-resume-v1.md exists and contains the
   substrings `supports_resume`, `resume_hunks_text`, `T002b-ii`, and the
   four measured numbers `1331`, `1384`, `2208`, `2270`.
G8 THE TREE — `git status --porcelain` empty; every commit's insertions
   via `git diff --numstat <sha>^..<sha>` under 500 (C0a/C0b exempt as
   verbatim `.agent/**` state-file saves); the canary
   (`pytest tests/cli/test_golden_path.py -q`) REAL exit 0; HEAD pushed
   and equal to `origin/feature/f106-session-resume`.

Handback: completion report + rewrite .agent/handoff.md (C6 above). State
the real numbers for every gate above, not the word "green". Name every
deviation, however small.
──────────────────────────────────────────────────────────────────────────
