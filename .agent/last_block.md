== STEP T003-staleness / F109 — ROUND 16 ==

SESSION 4 of feature F109. Round 16. Rounds so far: 15 done, this is the 16th.
Soft limit is 25 rounds / 7 sessions (docs/agents/self_drive_protocol.md G7,
amend0827 rule 6); at 16 rounds and 4 sessions it is NOT reached, so no scope
report is due. No line of this block is a run of a repeated character, so there
is no run length to recover (§3 checklist item 37).

Scope rule, verbatim as every F109 order must carry it:
RESUMED SESSION ONLY, PROVEN SENDS ONLY.

## Goal

Clear the branch's stale prose before the integration gate, so the gate runs
over a tree whose comments are true. Repair `R-0780` — two "deliberate absence"
bullets in `session_sent_index.py` that tell a reader the ping-pong loop invokes
nothing, three wiring commits after it did — and register and repair `R-0781`,
the dedupe suite's module docstring, which omits the T003d slice its own file
carries and still calls eleven call sites "the first case". Also book round 15's
PASS.

## Bundle, in commit order

- C0a  save this block verbatim to `.agent/authored/f109-r16.md`
- C0b  mirror it to `.agent/last_block.md`
- C1   apply PLAN16 to `.agent/plan.md`            (FIRST substantive commit)
- C2   append RECORD16 to `.agent/live_review.md`  (verdict, new id)
- C3   apply PAIR A and PAIR B to `packages/orchestration/session_sent_index.py`
- C4   apply PAIR C and PAIR D to `tests/orchestration/test_semantic_dedupe.py`
- C5   rewrite `.agent/handoff.md`

## Change set — these paths and nothing else

    .agent/authored/f109-r16.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/session_sent_index.py
    tests/orchestration/test_semantic_dedupe.py
    .agent/handoff.md

## Constraints

1. EVERY slice below is applied BYTE FOR BYTE — no rewrap, no re-indent, no
   improvement. If a slice looks wrong, apply it anyway and declare it in the
   handback; that is how a reviewer mistake becomes visible rather than becoming
   a silent correction.
2. `.agent/live_review.md` ends WITHOUT a trailing newline and that convention is
   preserved: append exactly the two bytes `\n\n` then RECORD16, which itself
   ends without one. Never rewrite a landed entry.
3. C3 and C4 change COMMENTS AND DOCSTRINGS ONLY. No executable line moves, no
   case is added, renamed or deleted, no import changes. The collected test
   count of the dedupe suite must be IDENTICAL before and after C4.
4. Do NOT write a `Done:` paragraph for `R-0780` or `R-0781`, and do not write a
   `Landed:` line either. The reviewer resolves both at the next gate, from the
   disk state your commits produce; the pending resolution rides in your
   handback, which amend0827 rule 1 makes a durable carrier.
5. Nothing outside the change set is edited. If the G8 sweep finds something
   else, DECLARE it; do not repair it.
6. `python3 -m pytest` is the pytest route; bare `remedy` may be denied, and
   `python3 -m apps.cli.main <cmd>` is the substitute. Env-var assignment
   (`VAR=x cmd`, `env`, `export`) and `cp` are DENIED by the sandbox: copy with
   `python3 -c "import shutil; shutil.copyfile(a, b)"`, and capture real exit
   codes with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. A `bash -c` wrapper around
   a Python heredoc has been observed to be denied outright — put such logic in
   a scratch `.py` file under `.remedy-wt/` and run it directly, then delete that
   file by its exact path.
7. Do not quote this handback commit's own insertion count anywhere; it cannot
   exist while the text stating it is written (§3 checklist item 14).
8. Never force-push, never work on main, never create or merge a PR this round.

## SLICE PLAN16 — the whole of `.agent/plan.md`

BEGIN PLAN16
# Plan — F109 Semantic dedupe

Branch: feature/f109-semantic-dedupe, cut from `main` at
`5e18a8536afa086b591b5a2e13009d68d6227432` (pull request 231 merged).

## Goal

Within a RESUMED session only, stop resending context the model has
already provably received: segments whose hash already went to that exact
session are replaced by short reference markers. Everywhere else full
content wins, because only a resumed session guarantees the model still
holds the prior content. The scope rule of the whole feature is "resumed
session only, proven sends only".

## Current Step

Round 16, session 4. Clear the branch's stale prose before the
integration gate, so that gate runs over a tree whose comments are true.
Repair `R-0780`, the two deliberate absence bullets in
`session_sent_index.py` that still deny the loop wiring; register and
repair `R-0781`, the dedupe suite's module docstring, which omits the
T003d slice its own file carries and calls eleven call sites "the first
case". Also book round 15's PASS. Comments and docstrings only: no
executable line moves this round.

## Next Steps

- The integration gate (docs/agents/integration_gate.md).
- The closure sequence (docs/roadmap/STATUS_closure_protocol.md), which
  also runs the single consolidation pass on the checklist of
  docs/agents/planner_reviewer_prompt.md section 3.

## Risks

- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today.
  `docs/system/semantic-dedupe-v1.md` states this plainly.
- The measurement function is a library, consumed by the T003 fixture
  and by no production caller. The doc states that too.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
END PLAN16

## SLICE RECORD16 — appended to `.agent/live_review.md`, two paragraphs

BEGIN RECORD16
Gate: F109 R15 — the round 15 entry. VERDICT PASS, over the range `d52a5371..cf210f6f`. THE TRANSPORT PROOF IS A REAL ONE THIS ROUND, and that is worth recording because §3 checklist item 37 says it usually cannot be: the reviewer wrote the block to `.remedy-wt/f109-r15.md` before delegating, so `cmp` against `.agent/authored/f109-r15.md` compares the WORKER'S copy to the REVIEWER'S OWN ORIGINAL rather than comparing three artefacts the worker produced. It exited 0, and the digest `4c8c964df8a8f4b96253971edaf3e65aacdb206e938c1c734fd6f117baca8c7d` is the one the reviewer computed BEFORE emission. EVERY SLICE WAS VERIFIED BYTE-IDENTICAL TO THE AUTHORED TEXT by the reviewer independently: `docs/system/semantic-dedupe-v1.md` equals the DOC slice exactly at 122 lines with one trailing newline, `.agent/plan.md` equals PLAN16's predecessor exactly at 44 lines, RECORD15's three paragraphs are the tail of the record, and both `docs/README.md` pairs read FROM 0x and TO 1x. THE SUITES WERE RE-RUN BY THE REVIEWER, not read: 755 passed at exit 0 across `tests/docs/` and the six named suites — 295, 130, 54, 27, 34, 173 and 42 — with no count fallen. THE LEDGER, recomputed as a SET DIFFERENCE per `R-0778`: 341 registered ids all distinct, 66 `Done:` lines over 64 distinct resolved ids, open set 277. THE DOC'S MEASURED TABLE STANDS WITHOUT RE-MEASUREMENT and the reason is structural rather than trusting: it is dated to `d52a5371`, and round 15 touched no path under `packages/` or `tests/`, so no commit in the range could have moved it. It was independently produced twice before landing — once by the reviewer off the real fixture and once by the worker — at 556 characters avoided, 97 spent on markers, 459 net over 2 occurrences with nothing unmeasured. THE WORKER'S FIRST REPLICA DISAGREED at 3 segments and 1869 characters and the worker chased it down rather than reporting it, finding its own replica unfaithful: a shared repo and data dir with a longer path pushed `reviewer_scope` over the 200-character floor. That is the right instinct and the finding it produced is real — the figures are hermetic only THROUGH the fixture, and the doc's own "not a claim about production magnitude" already carries that weight. THE TREE is clean, no worktree but the primary checkout and the four pre-existing `remedy/job-*` worktrees remains, and the branch is pushed at `cf210f6f`.

- R-0781 — Low, THE DEDUPE SUITE'S MODULE DOCSTRING OMITS A SLICE ITS OWN FILE CARRIES, AND STILL CALLS ELEVEN CALL SITES "THE FIRST CASE". Raised by the WORKER of F109 R15 during that round's G8 sweep for the first half, and carried by the reviewer for the second, which the workers of R14 and R15 had each declared and correctly declined to repair. MEASURED INDEPENDENTLY by the reviewer at `cf210f6f`. FIRST, the docstring enumerates "the per-session sent-hash index (T001a), the composition hook and its markers (T002), the config kill switch (T002c) and the trace's record of what was not resent (T003c)" and stops there, while the file also carries `TestTheRunsOwnTraceMeasuresWhatItWithheld`, the T003d measurement class that `069f1c02` added — so the enumeration is short by one slice. THIS IS NOT A REOPENING OF `R-0779` AND THE DISTINCTION IS EXACT: that finding's resolution condition was "the module docstring names no single 'final class' and no slice the file does not cover", which is a one-directional claim about naming ABSENT slices, and it is still met — every slice the docstring names is present. The defect here is the CONVERSE, a slice the file covers that the docstring does not name, and it was created by `069f1c02` in the SAME ROUND whose `79edbcbf` repaired `R-0779` three commits earlier. A repair and its own falsification inside one round is why this is registered rather than folded in. SECOND, the sentence "The manifest in the first case is built through the REAL producer in ``prompt_segments``" is a POSITIONAL claim of the `R-0775` class: `_real_manifest_rows(` has ELEVEN call sites in that file, so "the first case" names neither a unique case nor the practice the sentence is describing. WHY LOW: no behaviour is wrong, no gate is blind, no test is weakened and the suite is green; the damage is confined to the paragraph a reader meets FIRST when deciding what the file is for. FIX: extend the enumeration to name T003d, and restate the manifest sentence to quantify over the cases that are about manifest shape rather than over a position. Resolved when the docstring names every F109 slice the file covers and makes no positional claim about which case uses the real producer.
END RECORD16

## PAIR A — in `packages/orchestration/session_sent_index.py`

Containment test, run mechanically before emission: TO contains FROM: false.
REWRITE, so the proof is FROM 0x and TO 1x after C3. FROM counted in the target
at `cf210f6f`: exactly 1x.

BEGIN PAIRA_FROM
  - The resume-fallback DECISION now lives here (T001b-i):
    ``invalidate_on_resume_fallback`` decides which session a fallen-back resume
    must forget. What is still absent is only the CALL SITES — nothing in
    ``pingpong_loop.py`` invokes it yet, and wiring those seams is T001b-ii.
END PAIRA_FROM

BEGIN PAIRA_TO
  - The resume-fallback DECISION lives here (T001b-i):
    ``invalidate_on_resume_fallback`` decides which session a fallen-back resume
    must forget. ITS CALL SITES NOW EXIST: ``pingpong_loop.py`` invokes it on the
    Builder path and again on the Reviewer path, passing the resumed ref the loop
    still holds, and the same commit added the ``record_finalized_call`` sites
    that populate the index (T001b-ii, landed at ``7451e9c7``).
END PAIRA_TO

## PAIR B — in `packages/orchestration/session_sent_index.py`

Containment test, run mechanically before emission: TO contains FROM: false.
REWRITE, same proof shape as PAIR A. FROM counted at `cf210f6f`: exactly 1x.

BEGIN PAIRB_FROM
  - The dedupe DECISION and the MARKER TEXT now live here (T002a):
    ``should_dedupe_segment`` decides whether a segment may be replaced, and
    ``dedupe_marker_for_segment`` says what the replacement reads. What is still
    absent is the COMPOSITION HOOK that calls them — no prompt is rewritten here,
    and nothing in ``pingpong_loop.py`` invokes either function yet — together
    with the config plumbing that supplies ``enabled``; both are F109 T002b.
END PAIRB_FROM

BEGIN PAIRB_TO
  - The dedupe DECISION and the MARKER TEXT live here (T002a):
    ``should_dedupe_segment`` decides whether a segment may be replaced, and
    ``dedupe_marker_for_segment`` says what the replacement reads. THE WHOLE
    CHAIN ABOVE THEM NOW EXISTS: ``_dedupe_resumed_segments`` in
    ``pingpong_loop.py`` calls both (F109 T002b, landed at ``24352750``), both
    ``compose_*`` functions call that hook (``60343048``), and the config
    plumbing that supplies ``enabled`` landed at ``b245e1c9``. No prompt is
    rewritten HERE, which stays true and is a statement about this module rather
    than about the feature.
END PAIRB_TO

## PAIR C — in `tests/orchestration/test_semantic_dedupe.py`

Containment test, run mechanically before emission: TO contains FROM: false.
REWRITE. FROM counted at `cf210f6f`: exactly 1x. This is the opening of the
module docstring, so the file's FIRST bytes change; the triple quote is part of
both FROM and TO and must not be duplicated.

BEGIN PAIRC_FROM
"""Tests for F109 semantic dedupe — the per-session sent-hash index
(T001a), the composition hook and its markers (T002), the config kill
switch (T002c) and the trace's record of what was not resent (T003c).
END PAIRC_FROM

BEGIN PAIRC_TO
"""Tests for F109 semantic dedupe — the per-session sent-hash index
(T001a), the composition hook and its markers (T002), the config kill
switch (T002c), the trace's record of what was not resent (T003c) and
the measurement of what a run withheld, read back from that record
(T003d).
END PAIRC_TO

## PAIR D — in `tests/orchestration/test_semantic_dedupe.py`

Containment test, run mechanically before emission: TO contains FROM: false.
REWRITE. FROM counted at `cf210f6f`: exactly 1x. Note the FROM's short second
line, which the TO does not reproduce; apply the bytes as given.

BEGIN PAIRD_FROM
manifest in the first case is built through the REAL producer in
``prompt_segments`` so
the index is pinned against the manifest shape that actually ships rather than
against a hand-made dictionary.
END PAIRD_FROM

BEGIN PAIRD_TO
manifests these cases hand to the index are built through the REAL producer in
``prompt_segments`` wherever the case is about manifest SHAPE, so the index is
pinned against the manifest that actually ships rather than against a hand-made
dictionary.
END PAIRD_TO

## Done when — the eight gates. RUN each one and record its REAL exit code.

Every gate below runs at a commit STRICTLY EARLIER than C5, the commit that
writes the handback, so the handback can honestly quote all eight.

G1 TRANSPORT, one comparison and no chain. Run
   `cmp .remedy-wt/f109-r16.md .agent/authored/f109-r16.md` and report the exit
   code. That scratch file is the REVIEWER'S OWN original, so this comparison
   proves real transport and not merely your own self-consistency. Then report
   `sha256sum .agent/authored/f109-r16.md .agent/last_block.md` — one digest
   twice.

G2 THE PLAN. Extract PLAN16 by delimiter index (the lines strictly between
   `BEGIN PLAN16` and `END PLAN16`) and `cmp` it against `.agent/plan.md` after
   C1: exit 0, no output. Report `wc -l .agent/plan.md`, which must be under 50
   (AGENTS.md), and `grep -c '^## Goal'` and `grep -c '^## Next Steps'`, each 1.

G3 THE RECORD APPEND, four readings; this is the only slice earning full byte
   forensics this round.
   (a) ARITHMETIC. Report the base size and base sha256 of `.agent/live_review.md`
       at `cf210f6f`, the length S of the appended bytes, the new size, and
       whether base + S equals the new size. Confirm the file still ends WITHOUT
       a trailing newline.
   (b) A SECOND READER THAT COUNTS NO BYTE, covering the WHOLE appended region.
       Split the entire file on blank-line boundaries into units. Let N be the
       paragraph count of RECORD16 as YOUR SCRIPT COUNTS IT from the slice — do
       not take N from this block. Assert the LAST N units equal RECORD16's N
       paragraphs IN ORDER, printing each one's opening 60 characters.
   (c) A NEGATIVE CONTROL ON THE FIRST APPENDED PARAGRAPH. Copy the file to
       `.remedy-wt/live_review_negative_control_r16.md`, flip one byte INSIDE
       the FIRST appended paragraph there, and show reader (b) REJECTS the copy
       while ACCEPTING the tracked file. Report the tracked sha256 before and
       after to show it never moved, then delete that scratch file BY ITS EXACT
       PATH and report `os.path.exists` on that exact path as False.
   (d) COUNTS, AS A SET DIFFERENCE and never a subtraction (`R-0778`). Read the
       base from `git show d52a5371:.agent/live_review.md`, never by rewinding
       the tracked file, and report five figures for base and five for the new
       state: registered ids, DISTINCT registered ids, `Done:` lines, DISTINCT
       resolved ids, and `len(set(registered) - set(resolved))`. Also report
       `grep -c '^Gate: F109 R15 — '` = 1 and `grep -c '^- R-0781 — '` = 1.

G4 THE FOUR PAIRS, every one a REWRITE by the containment test recorded beside
   it. For PAIR A and PAIR B report the count of each FROM in
   `packages/orchestration/session_sent_index.py` BEFORE C3 (each 1) and AFTER C3
   (each 0), and each TO after C3 (each 1). For PAIR C and PAIR D do the same in
   `tests/orchestration/test_semantic_dedupe.py` around C4. Also confirm the
   test file still begins with the three bytes of a triple quote and holds
   exactly one module docstring.

G5 COMMENTS ONLY — THE PROOF THAT NO CODE MOVED. Using `git show <sha>:<path>`
   blobs only, for C3 and for C4: parse the BEFORE and AFTER blob with `ast`,
   and report that the set of top-level and nested definition names is
   IDENTICAL, that every function/class body's line COUNT of executable
   statements is unchanged, and that the only differing AST constant is the
   docstring you edited. Report `difflib.SequenceMatcher(None, before, after,
   autojunk=False)` opcodes for each, and the TOTAL lines deleted.

G6 THE SUITES, run SERIALLY, one process finishing before the next starts.
   Report the collected count and REAL exit code of each:
   - `python3 -m pytest tests/orchestration/test_semantic_dedupe.py -q`
   - `python3 -m pytest tests/orchestration/test_prompt_trace.py -q`
   - `python3 -m pytest tests/orchestration/test_session_resume.py -q`
   - `python3 -m pytest tests/orchestration/test_pingpong.py -q`
   - `python3 -m pytest tests/orchestration/test_pingpong_cli.py -q`
   - `python3 -m pytest tests/docs/ -q`
   - `python3 -m pytest tests/cli/test_golden_path.py -q`
   The last is the mandatory canary. NOTHING may go red, and NO COUNT MAY MOVE
   IN EITHER DIRECTION this round — the reviewer measured these at `cf210f6f` as
   130, 54, 27, 34, 173, 295 and 42, and constraint 3 forbids adding or removing
   a case, so a count that RISES is as much a failure as one that falls.

G7 THE REPAIRED PROSE IS TRUE, re-measured by you rather than assumed. After C3
   and C4 report: (a) `grep -c 'invokes it yet'` and `grep -c 'invokes either
   function yet'` in `session_sent_index.py`, both 0; (b) the call sites the new
   text claims, counted in `packages/orchestration/pingpong_loop.py` —
   `invalidate_on_resume_fallback(` and `record_finalized_call(` at 2 each, and
   `should_dedupe_segment(` and `dedupe_marker_for_segment(` at 1 each; (c) each
   of `7451e9c7`, `24352750`, `60343048` and `b245e1c9` exists via
   `git cat-file -e`; (d) READ THE MODULE DOCSTRING ALONE, via
   `ast.get_docstring(ast.parse(source))`, and report that it contains `T003d`
   exactly 1x and the string `the first case` 0x. Scope this reading to the
   docstring and NOT to the whole file: line 558 of that file carries the
   unrelated plural "the first cases in this", which a whole-file count would
   match as a substring and which PAIR D deliberately does not touch. Also
   report that the class `TestTheRunsOwnTraceMeasuresWhatItWithheld` is present
   in the file. Any reading that
   contradicts a slice is a finding against the REVIEWER: report it, apply the
   slice unchanged, and do not silently correct it.

G8 THE TREE AND THE SWEEP. `git status --porcelain` must be EMPTY and
   `git ls-files .remedy-wt` must return nothing. Report each commit's insertion
   count from `git show --numstat` — the `+` column ONLY, per AGENTS.md DECISION
   F104 D1 — for every commit of this round EXCEPT C5, and compare those figures
   cell by cell against your own `## Commits` table, which must carry the same
   numbers (§3 checklist item 28). Then RE-READ each file this round touched, end
   to end, and report every sentence that is now stale, including any you did NOT
   repair, with the reason. Repair nothing outside the change set.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has NO
length cap. It must carry: the SESSION NUMBER (4) and round (16); the item-status
table with every one of C0a, C0b, C1, C2, C3, C4, C5 appearing exactly once with
`done`, `skipped` or `deviated` and a reason; a per-commit changed-files table
with the `+/-` column; ONE LINE PER GATE G1 through G8 with its real reading; the
open-finding count as a SET DIFFERENCE; a PENDING RESOLUTION note stating that
`R-0780` and `R-0781` are repaired but NOT resolved, because only reviewer-
authored text sets `Done:`; your deviations and assumptions; and the next
expected action, which is the integration gate. Then
`git push -u origin feature/f109-semantic-dedupe` and report the result. Create
no PR.
