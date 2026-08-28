STEP R3 / F037 — RENDERED DIFF VIEWER — T001 PART ONE, THE PARSER
Goal:        BUILD THE UNIFIED-DIFF PARSER AND ITS CORPUS. A new module turns a
             unified diff into the versioned view JSON the feature file's
             contract specifies, and a corpus test pins one shape per row of
             the feature file's own list. This is PRODUCTION CODE: the module
             and its tests are DESCRIBED by the numbered SPEC below and written
             by you, not pasted from a slice. The round also books the R2
             verdict and the reviewer's authoring slip, which is the first
             commit of a round that is happening anyway rather than a round of
             its own.
             YOU CREATE NO PULL REQUEST THIS ROUND AND YOU MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the record — the R2 gate and the reviewer's slip ·
             C3 the parser module · C4 the corpus tests · C5 the handback ·
             then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f037-r3.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`, `packages/orchestration/diff_parser.py`,
             `tests/orchestration/test_diff_parser.py`, `.agent/handoff.md`.
             This list bounds what you WRITE INTO THE REPOSITORY. It does NOT
             bound what you DO: G7 orders a disposable worktree and G8 orders a
             push. NOTHING under `apps/` or `docs/` is written, and under
             `packages/` and `tests/` ONLY the two files named.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f037-r3.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f037-r3.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own; G2 has you measure
    four points and prove them EQUAL, and the reviewer holds the scratch value.
 2. THE SLICES ARE APPLIED BYTE FOR BYTE; THE SPEC IS IMPLEMENTED, NOT COPIED.
    A SLICE begins at the line AFTER `<<<SLICE NAME` and ends at the line
    BEFORE `<<<END NAME`; its TEXT is its content lines joined with a newline
    plus ONE trailing newline, and that is the ONLY definition of a slice's
    bytes used anywhere in this block. The numbered SPEC items S1 onward are
    NOT slices: they describe behaviour you write in your own words as real
    Python. If a slice contradicts something you measure, apply it anyway and
    DECLARE the contradiction under Deviations.
 3. EVERY EOF APPEND IN THIS ROUND IS THE SAME OPERATION: the target file's
    bytes AS THEY STAND IN THE COMMIT IMMEDIATELY BEFORE the one applying the
    append, plus exactly ONE newline, plus the slice's TEXT as constraint 2
    defines it. Read that baseline with `git show <sha>:<path>` where `<sha>`
    is the commit you are about to build on — for C2 that is C1, whose SHA you
    know because you just made it. NEVER read a baseline from a commit of an
    earlier ROUND, and never overwrite a tracked file to obtain one.
 4. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5. The record moves
    BEFORE the code. `.agent/plan.md` is advanced at C1, the FIRST substantive
    commit, as `docs/agents/planner_reviewer_prompt.md` §3 item 23 requires of
    any round that touches the finding ledger.
 5. NOTHING IS EDITED OUT OF ANY APPEND-ONLY RECORD. `.agent/live_review.md` is
    append-only from its `## Findings` heading down and `.agent/prose_slips.md`
    is append-only entire. No existing finding paragraph, no `Done:` line and
    no existing `Gate:` paragraph is rewritten, deleted or renumbered. This
    round REGISTERS nothing and RESOLVES nothing: `R-0715` stays OPEN and
    untouched.
 6. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Gate:` paragraph of
    your own, never mint a finding id, never author a `Done:` line and never
    write a DECISION. If you find a defect, report it under Deviations.
 7. THE MODULE IS SELF-CONTAINED AND IMPORTS NOTHING FROM THIS REPOSITORY.
    `packages/orchestration/diff_parser.py` uses only the Python standard
    library. It does NOT import, extend, wrap or modify
    `packages/orchestration/review_scope.py` or
    `packages/orchestration/review_subject.py`, and it changes no existing
    file. Amendment A3 of `docs/roadmap/features/T5_F037.md` rules why, and the
    equality guards the R1 inventory measured over those two modules are the
    reason a widening would be wrong rather than merely unnecessary.
 8. THE PARSER IS PURE AND TOTAL. It takes text and returns data: no file
    system, no subprocess, no network, no logging, no global state. It NEVER
    raises on malformed input — an unparseable region is reported in the data
    it returns, because this parser feeds a VIEWER and a viewer that crashes on
    a strange diff is worse than one that says "I could not read this".
 9. RE-READ `.agent/STOP` FROM DISK before C0a and again before C5. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
10. DESTRUCTIVE VERIFICATION IS ISOLATED. G7's mutations run ONLY inside a
    disposable `git worktree` under `.remedy-wt/`, never in the primary
    checkout, which reads `git status --porcelain` 0 lines at every commit.
    Remove the worktree and run `git worktree prune` before C5. Run no `npm`,
    `npx`, `node` or `vite`, and build nothing.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form
    of environment assignment. Route anything that counts, hashes, compares or
    mutates through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY. `--timeout` IS NOT AVAILABLE to pytest here: passing it
    exits 4 and reports no failure. Purge `__pycache__` and use `python3 -B`
    around any mutation, or a stale module will report the wrong colour.
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `09cbe24c` was
    measured by the reviewer at that commit. It is a REFERENCE to report
    against, NOT a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
13. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 1
    of F037 and that R3 is the round. The handback has NO LENGTH CAP.

SPEC — `packages/orchestration/diff_parser.py`, written by you:
 S1. MODULE HEADER. A docstring saying, in your own words, what the module is
     for and the one-line WHY: this repository's diffs arrive in THREE real
     shapes and a viewer must read all three. Name them, because the next
     reader will search for exactly this: (a) `difflib.unified_diff` output
     with `--- a/<path>` and `+++ b/<path>` headers, which is what
     `pingpong_loop.py` writes into `safe.diff` and what `job_evidence.py`
     writes into `workspace.diff`; (b) real `git diff` hunks, which
     `repair_attest.build_safe_diff_text` concatenates; (c) that same
     function's untracked-file markers, `--- /dev/null` then `+++ b/<path>`.
     State that `review_subject.py`'s status vocabulary is deliberately NOT
     reused and point at amendment A1 of
     `docs/roadmap/features/T5_F037.md` — a deliberate absence documented
     where a reader would search for it, per `AGENTS.md`.
 S2. PUBLIC NAMES. `DIFF_VIEW_VERSION = 1`; the five status constants
     `DIFF_STATUS_ADDED`, `DIFF_STATUS_MODIFIED`, `DIFF_STATUS_DELETED`,
     `DIFF_STATUS_RENAMED`, `DIFF_STATUS_BINARY` with the string values
     `added`, `modified`, `deleted`, `renamed`, `binary`; a frozenset
     `DIFF_VIEW_STATUSES` holding exactly those five values; and the entry
     point `parse_unified_diff_to_view(diff_text: str) -> dict`.
 S3. THE RETURN SHAPE. `{"version": DIFF_VIEW_VERSION, "truncated": bool,
     "files": [file, ...]}`. A file is `{"path": str, "old_path": str | None,
     "status": str, "stats": {"added": int, "deleted": int}, "note": str |
     None, "hunks": [hunk, ...]}`. A hunk is `{"id": str, "header": str,
     "old_start": int, "new_start": int, "lines": [line, ...]}`. A line is
     `{"kind": str, "old_ln": int | None, "new_ln": int | None, "content":
     str}` where `kind` is one of `ctx`, `add`, `del`. `old_path` is None
     unless the status is `renamed`. The feature file's contract writes the
     stats as `stats {+,-}`; this SPEC reads that shorthand as the two named
     integer keys above, and `truncated` and `note` are additions the contract's
     own version field exists to carry — say so in the docstring rather than
     leaving a reader to wonder which is authoritative.
 S4. FILE SPLITTING. Start a new file entry at a `diff --git ` line, or at a
     `--- ` line that is not part of the hunk body currently being read. Take
     the path from the `+++ ` header, stripping one leading `a/` or `b/`, and
     where that header is `/dev/null` take it from the `--- ` header instead.
     `parse_safe_diff_paths` in `packages/orchestration/repair_attest.py`
     already reads `+++ b/<path>` headers and skips `/dev/null`; follow that
     same convention so this repository keeps ONE spelling for the concept.
 S5. STATUS DERIVATION, in this order, first match wins. `renamed` when a
     git-style `rename from ` / `rename to ` pair is present. `binary` when the
     literal line `[binary file]` appears in the file's region, or a git-style
     `Binary files ` line does. `added` when the `--- ` header is `/dev/null`,
     or when every hunk of the file has an old-side count of 0. `deleted` when
     the `+++ ` header is `/dev/null`, or when every hunk has a new-side count
     of 0. Otherwise `modified`. A file with no hunks at all and no other
     signal is `modified` with an empty hunk list, never an error.
 S6. HUNK HEADERS. Parse `@@ -<old_start>[,<old_count>] +<new_start>[,<new_count>] @@[ <section>]`,
     capturing BOTH sides — the old start and count as well as the new. The
     absent count means 1. Keep the header line VERBATIM as `header`, section
     heading included, because the viewer renders it. A `@@` line that does not
     match is not a hunk: leave it, and let S8 record it.
 S7. LINE NUMBERING. Walk each hunk body maintaining two counters seeded from
     the header's two starts. A ` ` line is `ctx` and carries both numbers and
     advances both. A `+` line is `add`, carries `new_ln` only with `old_ln`
     None, and advances the new counter. A `-` line is `del`, carries `old_ln`
     only with `new_ln` None, and advances the old counter. `content` is the
     line WITHOUT its leading marker character and WITHOUT a trailing newline.
     A `\ No newline at end of file` line is metadata: it belongs to no line
     entry, advances no counter, and is dropped.
 S8. THE SENTINELS THIS REPOSITORY REALLY EMITS, each recorded rather than
     guessed at. `[binary file]` sets the status per S5 and sets `note` to that
     literal text. A line beginning `[unsafe staged artifact skipped:` sets
     `note` to the whole line and leaves the file with no hunks. A line whose
     stripped form is `[DIFF TRUNCATED]` sets the view's top-level `truncated`
     to True and ends parsing of the current file cleanly. A `#` comment line
     outside any hunk — `job_evidence.py`'s workspace preamble and
     `repair_attest`'s untracked-file marker both emit these — is skipped when
     no file is open, and sets `note` when one is.
 S9. HUNK IDS ARE PROVISIONAL AND SAY SO. `id` is the string
     `f"{file_index}:{hunk_index}"`, both zero-based, stable only within one
     parse of one diff. The docstring states in one sentence that F033 replaces
     these with content-hash ids and that `DIFF_VIEW_VERSION` is the seam
     through which it does — the feature file's "How it fits" section requires
     that note and this is where a reader looks for it.
S10. STATS. `stats["added"]` and `stats["deleted"]` count the `add` and `del`
     LINE ENTRIES of that file across all its hunks. They are counted from the
     parsed entries, never from a second walk of the text, so they cannot
     disagree with the lines the viewer renders.
S11. EMPTY AND MALFORMED INPUT. `parse_unified_diff_to_view("")` returns
     `{"version": 1, "truncated": False, "files": []}`. Input that is not a
     diff at all returns the same empty-files shape. Nothing raises.

SPEC — `tests/orchestration/test_diff_parser.py`, written by you:
S12. ONE TEST PER SHAPE THE FEATURE FILE LISTS, each with its diff text inline
     as a fixture so a reader sees the input beside the expectation: a plain
     modification; a file ADDED via `--- /dev/null`; a file ADDED via difflib
     with an all-zero old side; a file DELETED; a git-style RENAME; a BINARY
     file via the `[binary file]` sentinel; an empty-string input; a
     multi-file diff proving the files come back in input order with distinct
     hunk ids; a multi-hunk file proving the second hunk's line numbers are
     seeded from its OWN header and not continued from the first.
S13. THE LINE-NUMBER TEST IS THE ONE THAT MATTERS AND IT ASSERTS BOTH SIDES.
     For a hunk with context, additions and deletions, assert the FULL list of
     `(kind, old_ln, new_ln, content)` tuples for every line of that hunk, in
     order. This is the assertion that fails if the old-side capture is
     dropped, which is the exact defect the R1 inventory measured in the
     existing reader, so it is written to catch that defect and not merely to
     cover the function.
S14. FURTHER PINS. `DIFF_VIEW_STATUSES` equals the five expected strings.
     `parse_unified_diff_to_view` on a truncated diff sets `truncated` True.
     `\ No newline at end of file` produces no line entry. Every returned
     file's `stats` equals a recount of its own parsed line kinds — assert the
     PROPERTY, not a transcribed number.
S15. NOTHING ELSE IS TOUCHED. No existing test is edited, no assertion
     weakened, no fixture moved.

Done when:
 G1. HYGIENE, THE BASE AND THE SENTINEL. Report `git rev-parse HEAD` BEFORE
     C0a, which must be `09cbe24c2723b2aacb62e355fe5e03f9c8e46fe7`, and
     `git branch --show-current`, which must be
     `feature/f037-rendered-diff-viewer`. Report `git status --porcelain` as a
     LINE COUNT after each of C0a, C0b, C1, C2, C3 and C4, each 0. C5's own
     reading belongs in no file this round writes; take it and report it in
     your completion report. Report `.agent/STOP` read from disk before C0a and
     before C5, both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f037-r3.md`, as saved at C0a, as mirrored at C0b and
     as read off disk at C4 — all four must be EQUAL — and say whether C0a and
     C0b are the same git blob. Report whether any line of the block as saved
     is a run of a single repeated character at length 4 or more, which must
     come back as none. THEN STATE IN ONE SENTENCE WHAT THIS PROOF COVERS: the
     scratch file, the saved copy, its mirror and the working copy, and NOT the
     bytes of any prompt.
 G3. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES. Report how many slices your extractor printed, each
     slice's own line count, the CONTENT total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE at most 400, TOTAL at
     most 490.
 G4. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF037R3 under the
     newline-INCLUDED convention of constraint 2. Run the negative control
     against the slice MINUS its trailing newline and report FALSE. Report
     `^## Goal$` 1, `^## Next Steps$` 1, a match for `\bF\d{3}\b`, and `wc -l`
     STRICTLY UNDER 50.
 G5. THE TWO RECORD APPENDS, AT C2, each by the operation constraint 3 defines
     and each baseline read from C1. Prove each TWO WAYS. Reader (a),
     RECONSTRUCTION: baseline plus one newline plus the slice text is
     BYTE-EQUAL to the file at C2 and the baseline is a byte PREFIX of it;
     report the arithmetic in bytes. Reader (b), STRUCTURE: split the file at
     C2 on blank lines, count N as the number of blank-line units the SLICE
     holds — a number YOUR script counts, never one this block asserts — and
     report that the LAST N units equal the slice's N units IN ORDER. NEGATIVE
     CONTROL for each: flip ONE byte at an offset you assert and report to lie
     inside the FIRST appended paragraph, and report that BOTH readers reject.
     Then report, for `.agent/live_review.md` before and after C2, the
     line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`,
     `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `; the reviewer measured 276, 24,
     1, 19 and 72 at the base, and after C2 they must read 276, 24, 1, 19 and
     73. Report the finding ids and resolved ids ADDED and REMOVED as SETS, all
     four EMPTY, the maximum id `R-0715` at both points, the open set 252 at
     both points, and that `R-0715` still ends with the word `OPEN.`
 G6. THE PARSER RUNS AND IS CLEAN, at C4. Run, as ONE pytest process from the
     repository root, `python3 -m pytest tests/orchestration/test_diff_parser.py
     -q` and report the REAL exit code, the summary line VERBATIM and the COUNT
     of lines matching `^FAILED`, which must be 0. PROVE YOUR `^FAILED`
     EXTRACTOR IS NOT BLIND over a control string that contains such a line.
     Then run `python3 -m ruff check packages/orchestration/diff_parser.py
     tests/orchestration/test_diff_parser.py` from the repository root — the
     repository's own configuration, no `--isolated` and no `--line-length` —
     and report the REAL exit code and the output VERBATIM. Both paths are
     added by this branch, so NO baseline reading at an earlier commit is
     ordered or possible. Finally report `python3 -m pytest
     tests/cli/test_golden_path.py -q`, the canary, with its real exit code and
     summary line.
 G7. THE RED-PROOFS, in a disposable worktree under `.remedy-wt/` and NEVER in
     the primary checkout. Add the worktree at C4. FIRST report the UNMUTATED
     CONTROL there: `python3 -B -m pytest tests/orchestration/test_diff_parser.py
     -q` with its real exit code, which must be 0, and its summary line — a
     colour with no baseline is not evidence. Then perform each mutation below
     SEPARATELY, restoring the file between them, purging `__pycache__` each
     time, and report for EACH the real exit code, the count of `^FAILED`
     lines and the failing node ids VERBATIM.
     (a) In `packages/orchestration/diff_parser.py`, make the old-side line
         counter never advance — the single statement that increments the OLD
         line number for a `ctx` or `del` line. Report which nodes fail. S13's
         full-tuple assertion is the node that must, and if NOTHING fails,
         report that plainly: it means the assertion never reads `old_ln` and
         the test is the defect, not the mutation.
     (b) In the same file, make the `[binary file]` sentinel not set the binary
         status — change the literal it compares against to a string that
         cannot occur, `[binary file NEVER]`. Report which nodes fail; the S12
         binary test must.
     (c) In the same file, make `stats["deleted"]` always 0. Report which nodes
         fail; S14's stats-property test must.
     NAME, for each mutation, the exact file it was applied in and report the
     count of the bytes you replaced IN THAT FILE, which must be 1 before the
     edit. Remove the worktree and run `git worktree prune`, then report `git
     worktree list` as 1 line and `git status --porcelain` as 0 lines in the
     primary checkout.
 G8. STRUCTURE, ARTIFACTS, THE OPEN PR GATE AND THE PUSH. Compare the path set
     of `git diff --name-only 09cbe24c..C4` BOTH WAYS against this round's
     expected set — the Change line's list MINUS `.agent/handoff.md`, which C5
     writes — and report both residues EMPTY. Report `git diff --stat
     09cbe24c..C4` restricted to `apps/`, `docs/`, `packages/` and `tests/` and
     confirm the first two EMPTY and the last two holding ONLY
     `packages/orchestration/diff_parser.py` and
     `tests/orchestration/test_diff_parser.py`. Report each commit's insertions
     from `git diff --numstat` for C0a through C4, confirm each single-parent
     and under 500. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
     `.agent/plan.md`, `.agent/live_review.md` and `.agent/prose_slips.md` at
     their commits, against a CONTROL over the C0a blob which is not 0. Report
     `git ls-files .remedy-wt` 0 lines and `git branch --list "tmp/*"` 0 lines.
     Run `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
     and report it VERBATIM; the reviewer read `[]` at the round base; MERGE
     NOTHING and CREATE NOTHING. After C5, run `git push origin
     feature/f037-rendered-diff-viewer`. ITS OUTCOME IS NOT A VALUE OF ANY FILE
     THIS ROUND WRITES: C5 is authored before the push exists, so
     `.agent/handoff.md` states the push only as an INTENT under
     `## External actions`. Report the real exit code and the resulting remote
     tip in your completion report instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C5: the `## Session` section constraint 13 orders, feature and
             round, branch, the round base SHA `09cbe24c`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item AND every SPEC item S1
             through S15, ONE LINE PER GATE for G1 through G8 with its real
             exit code, the open-findings count after this round, and the next
             expected action. C5 cannot table its own numstat — write `self` in
             that cell, as `R-0149` requires. STATE PLAINLY under Deviations
             any SPEC item you could not implement as written and why, and any
             place the three real diff shapes disagreed with S4 through S8 —
             that answer is what the reviewer rules on next round.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW.

<<<SLICE PLANF037R3
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F037 D1 and D2.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments that reconcile it with the source.

## Current Step
R3 opens T001 with the parser itself: a new self-contained module that turns a
unified diff into the versioned view JSON, plus the corpus that pins one shape
per row of the feature file's list. It reads the THREE diff shapes this
repository really produces — difflib output, git hunks, and untracked-file
markers — rather than the single git-style shape the contract assumed. The
round also books the R2 verdict and the reviewer's authoring slip.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R2 gate and the reviewer's slip | ordered | the record moves first |
| C3 the parser module | ordered | production code, spec-driven |
| C4 the corpus tests | ordered | one shape per row, plus red-proofs |
| C5 the handback | ordered | |

## Next Steps
1. Intraline spans over the parsed lines, with the word-diff fixture the
   feature file's Acceptance names.
2. The read endpoint, keyed on task run and job per DECISION F037 D2, with the
   route guards the R1 inventory measured.
3. T002 the rendering core, the binding CSS and the goldens; then T003 sidebar,
   virtual scrolling, lazy languages and the L3 tab.

## Risks
- `R-0715` is open and Low. It is a stale count in a test docstring, turns
  nothing red, and belongs to whoever next edits that file.
- The parser is new surface with no consumer yet. Until the endpoint lands it
  is proved only by its own corpus, so the corpus carries the whole weight and
  the round orders mutation red-proofs against it.
<<<END PLANF037R3

<<<SLICE RECORDR3
Gate: F037 R2 — the booking-and-amendment round, and the round in which the WORKER CAUGHT A DEFECT IN THE REVIEWER'S OWN BLOCK THAT WOULD HAVE CORRUPTED THIS RECORD. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all eight itself at `09cbe24c`. THE DEFECT FIRST, because it is the most useful thing this round produced: G5 ordered every append baseline read with `git show 89b96df7:<path>`, and `89b96df7` is R1's C1, not the round base. Measured by the reviewer, `.agent/live_review.md` at `89b96df7` is 1126556 bytes carrying 70 gate keys and NO `Gate: F032 R19 — ` entry, while at the round base `69f6478c` it is 1130704 bytes carrying 71 and that entry — because R1's own C3 reset the header and appended the F032 R19 gate AFTER `89b96df7`. Appending onto the named baseline would have DELETED R1's header reset and the F032 R19 gate paragraph from an append-only record, which constraint 5 of that same block forbids outright. The worker measured all three baselines against the base before using any of them, found the one that differed, read it instead from the pre-C2 tip, applied the append onto the correct bytes and DECLARED the whole thing rather than silently correcting or silently obeying. That is the single-writer discipline doing exactly what it exists for, and the reviewer confirms the landed record is intact: `Gate: F032 R19 — ` occurs exactly once at `09cbe24c` and the pre-C2 blob is a byte PREFIX of the result. The reviewer's authoring failure is recorded in `.agent/prose_slips.md`; no id is spent, because nothing landed wrong on disk and operator amendment amend0827 rule 2 reserves an id for defects with product effect. THE REST OF THE ROUND REPRODUCES EXACTLY. TRANSPORT: sha256 `e6ef75ba2400c2bc4c3ab30256e85f0a1bf7fb42e9a1ae4f9760763d485fc332` over 31950 bytes and 416 lines, equal across the reviewer's scratch original, the committed `.agent/authored/f037-r2.md` blob and the committed `.agent/last_block.md` blob, the two committed paths being ONE git blob `c0812abbe876801a5ac5c737918400f46ced453b`; the chain covers the original, the saved copy and the mirror and claims nothing about any prompt's bytes. EXTRACTION: 7 slices at 44, 3, 10, 83, 1, 3 and 45 content lines, CONTENT 189 against TOTAL 416, PROSE 227, both caps holding. THE PLAN is byte-equal to its slice with the trailing-newline control `False`, at 44 lines. THE THREE APPENDS RECONSTRUCT EXACTLY against the correct baselines, each with the baseline a byte PREFIX: `1130704 + 1 + 5684 = 1136389`, `4319 + 1 + 750 = 5070` and `649977 + 1 + 5442 = 655420`. THE RECORD MOVED AS ORDERED: `^- R-\d+ — ` 275 to 276, `^Done: R-\d+ — ` unmoved at 24, `^Gate: F\d+ R\d+ — ` 71 to 72, the single id added being `R-0715`, nothing resolved, all 276 ids distinct, the open set 252 and the maximum `R-0715`. THE DECISION SERIES GREW BY THE TWO ORDERED ENTRIES, `^## DECISION ` 166 to 168, with `F037 D1` and `F037 D2` each occurring exactly once. THE FEATURE FILE MOVED IN THE SHAPE THE BLOCK ASSIGNED IT: the DFROM/DTO pair was declared APPEND-shaped on a containment test reading `true`, and after C3 the FROM still occurs 1x and the TO 1x with each TO-ONLY line occurring exactly 1x among that commit's added lines — no FROM-zero count was ordered, being unattainable by construction — and the reconstruction reads `5110 + 1 + 2870 = 7981` with `^## Design amendments$` 0 to 1 and `^## Do not touch$` unmoved at 1. THE DOCS GATE AND THE CANARY were re-run by the reviewer as ONE process at a real exit 0: `367 passed`, zero `^FAILED` lines. THE TWO DECISIONS ARE CORRECT ON THE EVIDENCE, and the reviewer re-derived the load-bearing half of each rather than accepting the inventory's word: `binary` is absent from `review_subject.py`'s seven statuses, and the R1 inventory's own Q8 lists the `validate_review_file_schema(...) == []` and `validate_review_subject_schema(...) == []` guards that reading `_VALID_STATUSES` would turn red, so D1's refusal to widen that vocabulary is measured rather than asserted; and the three modules the attempt-parameter finding rests on — `repair_loop_v2.py`, `pingpong_evidence.py` and `job_evidence.py` — were re-read at the citations given and all three resolve. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END RECORDR3

<<<SLICE SLIPR3
- 2026-08-28 · F037 R2 · The block's G5 ordered every append baseline read with
  `git show 89b96df7:<path>`, naming R1's C1 instead of the round base — a
  commit at which `.agent/live_review.md` predates R1's own header reset and
  F032 R19 gate append by 4148 bytes and one gate key. Obeying it literally
  would have deleted landed text from an append-only record, which the same
  block's constraint 5 forbids, so the block contradicted itself and the worker
  had to resolve it. Nothing landed wrong: the worker measured all three
  baselines against the base first, used the correct pre-commit tip and
  declared the deviation. A baseline SHA is COPIED FROM THE COMMIT THE APPEND
  BUILDS ON, never carried over from the previous round's block, and where the
  worker makes that commit itself the gate names it by ROLE — "the commit you
  are about to build on" — rather than by a SHA the reviewer guessed.
<<<END SLIPR3
