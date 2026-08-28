STEP R5 / F037 — RENDERED DIFF VIEWER — T001 PART THREE, THE INTRALINE GUARDS
Goal:        MAKE THE INTRALINE TESTS DISCRIMINATE, AND MAKE THE SIMILARITY
             GUARD REACHABLE. R4 landed intraline spans and its own red-proof
             reported one mutation GREEN. Following that thread the reviewer
             measured two defects, both of them the reviewer's spec rather than
             R4's execution. `R-0717`: the side mapping is pinned only for
             `replace` opcodes, so dropping `delete` from the old side OR
             `insert` from the new side leaves the suite green. `R-0718`: the
             similarity guard cannot fire for any multi-word line, because
             separator tokens count toward the ratio and floor it at 0.333 for
             two words and higher above that. This round books R4, registers
             both, resolves `R-0716`, and repairs both with the discriminators
             they lack. IT IS THE LAST ROUND OF THIS SESSION.
             YOU CREATE NO PULL REQUEST THIS ROUND AND YOU MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the record — the R4 gate, the `R-0716` resolution, the
             registration of `R-0717` and `R-0718`, and the reviewer's slip ·
             C3 the `R-0717` discriminating fixtures · C4 the `R-0718` repair
             with its test · C5 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f037-r5.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`,
             `packages/orchestration/diff_parser.py`,
             `tests/orchestration/test_diff_parser.py`, `.agent/handoff.md`.
             This list bounds what you WRITE INTO THE REPOSITORY. It does NOT
             bound what you DO: G6 and G7 order a disposable worktree and G8
             orders a push. NOTHING under `apps/` or `docs/` is written.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f037-r5.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f037-r5.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own; G2 has you measure
    four points and prove them EQUAL.
 2. THE SLICES ARE APPLIED BYTE FOR BYTE; THE SPEC IS IMPLEMENTED, NOT COPIED.
    A SLICE begins at the line AFTER `<<<SLICE NAME` and ends at the line
    BEFORE `<<<END NAME`; its TEXT is its content lines joined with a newline
    plus ONE trailing newline, and that is the ONLY definition of a slice's
    bytes used anywhere in this block. The numbered SPEC items are NOT slices.
    If a slice contradicts something you measure, apply it anyway and DECLARE
    it under Deviations.
 3. C2 APPLIES A PAIR AND THEN AN APPEND, IN THAT ORDER. First replace the
    single line LANDEDFROM with the paragraph LANDEDTO — this is the ONE
    sanctioned rewrite of landed text in this workflow, because
    `docs/agents/planner_reviewer_prompt.md` §4 item 4 reserves `Done:` for
    reviewer-authored text and has the worker's `Landed:` line replaced by it
    at the next gate. Then append RECORDR5 by the EOF operation: the file's
    bytes as they stand AFTER the pair, plus exactly ONE newline, plus the
    slice's TEXT. Read the pre-commit baseline with `git show <sha>:<path>`
    where `<sha>` is THE COMMIT YOU ARE ABOUT TO BUILD ON — for C2 that is C1,
    whose SHA you know because you just made it. Never read a baseline from an
    earlier ROUND and never overwrite a tracked file to obtain one.
 4. SLIPR5 IS AN EOF APPEND TO `.agent/prose_slips.md` at C2, by the same
    operation: baseline, one newline, the slice's text.
 5. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5. The record moves
    BEFORE the code. `.agent/plan.md` is advanced at C1, the FIRST substantive
    commit, as `docs/agents/planner_reviewer_prompt.md` §3 item 23 requires of
    any round that touches the finding ledger.
 6. NOTHING ELSE IN THE RECORD IS EDITED. Apart from the single LANDEDFROM line
    that constraint 3 replaces, no finding paragraph, no `Done:` line and no
    existing `Gate:` paragraph is rewritten, deleted or renumbered. `R-0715`
    is NOT touched and stays OPEN.
 7. YOU RESOLVE NOTHING YOURSELF. You never write a `Gate:` paragraph, never
    mint a finding id, never author a `Done:` line of your own and never write
    a DECISION. When the repairs land you append, as the LAST lines of
    `.agent/live_review.md` in the commit that lands each, exactly one line of
    the form `Landed: R-XXXX — <one sentence: what changed, and the commit>` —
    one for `R-0717` at C3 and one for `R-0718` at C4 — and nothing else.
 8. THE MODULE STAYS SELF-CONTAINED, PURE AND TOTAL. Standard library only,
    never `review_scope` or `review_subject`, no file system, no subprocess, no
    network, no logging, no global mutable state, and it NEVER raises on
    malformed input.
 9. RE-READ `.agent/STOP` FROM DISK before C0a and again before C5. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
10. DESTRUCTIVE VERIFICATION IS ISOLATED. The red-proofs of G6 and G7 run ONLY
    inside a disposable `git worktree` under `.remedy-wt/`, never in the
    primary checkout, which reads `git status --porcelain` 0 lines at every
    commit. Remove the worktree and run `git worktree prune` before C5. Run no
    `npm`, `npx`, `node` or `vite`.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form
    of environment assignment. Route anything that counts, hashes, compares or
    mutates through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY. `--timeout` IS NOT AVAILABLE to pytest here. Purge
    `__pycache__` and use `python3 -B` around any mutation.
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `c6c490cb` was
    measured by the reviewer at that commit. It is a REFERENCE to report
    against, NOT a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
13. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 1
    of F037, that R5 is the round, and THAT THE SESSION ENDS HERE. Its `## Next`
    section names, as the next session's FIRST action, re-reading `.agent/STOP`
    from disk (Phase 1 rule 1 of `docs/agents/self_drive_protocol.md`) and only
    then the Open PR Gate, and states that F037's branch has NO open pull
    request, so the gate finds nothing to merge and work resumes at T001's read
    endpoint. The handback has NO LENGTH CAP.

SPEC — the `R-0717` discriminators, in `tests/orchestration/test_diff_parser.py`:
 S1. THE GAP, measured, so the fixtures are aimed at a real thing. Across every
     intraline fixture the file holds at `c6c490cb`, the paired lines that clear
     the ratio guard produce only `equal` and `replace` opcodes. The reviewer
     confirmed the consequence in a worktree at that commit: changing the OLD
     side's opcode tuple from `("replace", "delete")` to `("replace",)` leaves
     the suite at `24 passed`, exit 0, and changing the NEW side's from
     `("replace", "insert")` to `("replace",)` does the same.
 S2. A PURE-DELETION FIXTURE. One `del`/`add` pair where the new line is the old
     line with an interior run of words REMOVED and nothing else changed — the
     reviewer measured `keep the extra words here` against `keep the words here`
     as producing opcodes `equal`, `delete`, `equal` at a ratio of 0.875. Assert
     the EXACT spans on the `del` entry, assert that slicing `content` by them
     yields the removed text, and assert the `add` entry's spans are `[]`. That
     last assertion is the discriminator: it is what fails when `delete` is
     dropped from the old side.
 S3. A PURE-INSERTION FIXTURE, the mirror of S2: the new line is the old line
     with an interior run of words ADDED. Assert the exact spans on the `add`
     entry, assert the sliced text, and assert the `del` entry's spans are `[]`.
 S4. THE PROOF THAT THEY DISCRIMINATE is G6, which re-runs the two mutations of
     S1 against the C3 tree and requires BOTH to go red. A fixture that does not
     kill its mutation has not closed the gap it was written for.

SPEC — the `R-0718` repair, in `packages/orchestration/diff_parser.py`:
 S5. THE DEFECT, measured. The similarity ratio is computed over the FULL token
     stream produced by `re.findall(r"\w+|\W", s)`, which interleaves separator
     tokens. Two space-separated lines of equal word count always match on their
     separators, so the ratio has a FLOOR even when no word matches: the reviewer
     measured 0.333 at two words, 0.400 at three, 0.444 at five and 0.474 at ten,
     rising toward 0.5. With `DIFF_INTRALINE_MIN_RATIO` at 0.3 the guard
     therefore CANNOT fire for any multi-word line pair, and the only fixture in
     the file that exercises it is a single-word line, `alpha` against `zulu`,
     which is the one shape where a separator floor does not exist.
 S6. THE REPAIR. Compute the guard's ratio over the SIGNIFICANT tokens only —
     the tokens that are not pure whitespace — while the SPAN MAPPING continues
     to run over the full token stream, because offsets must stay exact. Keep
     `DIFF_INTRALINE_MIN_RATIO` at 0.3; the constant was never the defect, the
     stream it was measured over was. Where BOTH significant-token lists are
     empty — two lines made entirely of whitespace and punctuation — treat the
     pair as similar and emit spans from the full stream, because there is no
     word evidence either way and refusing to mark anything is the safer half of
     a choice this rule cannot make honestly.
 S7. THE TEST. Add a case with two multi-word lines that share no word — the
     reviewer measured `alpha beta gamma` against `zzz qqq www` as scoring 0.400
     on the full stream and therefore emitting spans over EVERY word today — and
     assert `[]` on both entries. Compute the significant-token ratio inside the
     test and assert it is below the exported constant, naming the constant
     rather than transcribing 0.3, exactly as the existing threshold test does.
     Keep that existing single-word test passing unchanged.
 S8. WHAT MUST NOT REGRESS. `the fox jumps` against `the cat jumps` still emits
     spans — its significant-token ratio is 0.667 — and every test the file
     already holds still passes. G7 measures that by node id.

Done when:
 G1. HYGIENE, THE BASE AND THE SENTINEL. Report `git rev-parse HEAD` BEFORE
     C0a, which must be `c6c490cb83fe4889e41fc0d14d54d80fb306d4f1`, and
     `git branch --show-current`, which must be
     `feature/f037-rendered-diff-viewer`. Report `git status --porcelain` as a
     LINE COUNT after each of C0a, C0b, C1, C2, C3 and C4, each 0. C5's own
     reading belongs in no file this round writes; take it and report it in
     your completion report. Report `.agent/STOP` read from disk before C0a and
     before C5, both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f037-r5.md`, as saved at C0a, as mirrored at C0b and
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
 G4. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF037R5 under the
     newline-INCLUDED convention of constraint 2. Run the negative control
     against the slice MINUS its trailing newline and report FALSE. Report
     `^## Goal$` 1, `^## Next Steps$` 1, a match for `\bF\d{3}\b`, and `wc -l`
     STRICTLY UNDER 50.
 G5. THE RECORD, AT C2. For the PAIR: report that LANDEDFROM occurs EXACTLY 1
     time in `.agent/live_review.md` before the edit and 0 times after, and that
     LANDEDTO occurs 0 times before and EXACTLY 1 time after; the reviewer
     measured `TO contains FROM: false`, so this is a REWRITE and the FROM-zero
     count is the right obligation for it. For the APPEND, prove it TWO WAYS
     against the file AS IT STANDS AFTER THE PAIR. Reader (a),
     RECONSTRUCTION: those bytes plus one newline plus RECORDR5's text is
     BYTE-EQUAL to the file at C2; report the arithmetic in bytes. Reader (b),
     STRUCTURE: split the file at C2 on blank lines, count N as the number of
     blank-line units the SLICE holds — a number YOUR script counts, never one
     this block asserts — and report that the LAST N units equal the slice's N
     units IN ORDER. NEGATIVE CONTROL: flip ONE byte at an offset you assert
     and report to lie inside the FIRST appended paragraph, and report that
     BOTH readers reject. Do the same two readers and control for SLIPR5 against
     `.agent/prose_slips.md`. Then report the line-anchored counts of
     `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`, `^Gate: R\d+ — ` and
     `^Gate: F\d+ R\d+ — ` before and after C2; the reviewer measured 277, 24,
     2, 19 and 74 at the base, and after C2 they must read 279, 25, 1, 19 and
     75. Report the finding ids ADDED as a SET, which must be exactly `R-0717`
     and `R-0718`; the finding ids REMOVED and the resolved ids REMOVED as
     SETS, both EMPTY; the resolved ids ADDED as a SET, which must be exactly
     `R-0716`; that all ids are DISTINCT; the maximum id after C2, which is
     `R-0718`; and the open set after C2, which is 254.
 G6. THE DISCRIMINATORS ARE PROVED BY THE REDS THEY NOW CAUSE, in a disposable
     worktree under `.remedy-wt/` and NEVER in the primary checkout, at the C3
     tree. FIRST report the UNMUTATED CONTROL: `python3 -B -m pytest
     tests/orchestration/test_diff_parser.py -q`, real exit code 0, with its
     summary line. THEN run each mutation SEPARATELY against
     `packages/orchestration/diff_parser.py`, restoring between them and purging
     `__pycache__` each time, and report for each the real exit code and the
     failing node ids VERBATIM:
     (a) the OLD side's opcode tuple `("replace", "delete")` narrowed to
         `("replace",)`. The S2 pure-deletion test must fail.
     (b) the NEW side's opcode tuple `("replace", "insert")` narrowed to
         `("replace",)`. The S3 pure-insertion test must fail.
     For EACH, name the exact file and report the count of the bytes you
     replaced IN THAT FILE, which must be 1 before the edit. The reviewer
     measured BOTH of these as exit 0 at `24 passed` against the ROUND BASE
     `c6c490cb`; both going red at C3 is the whole point of the commit, and a
     mutation that stays green means the fixture does not discriminate and must
     be reported plainly rather than replaced.
 G7. THE SUITE, THE LINT AND THE CANARY, at C4, in the PRIMARY checkout. Run,
     as ONE pytest process from the repository root, `python3 -m pytest
     tests/orchestration/test_diff_parser.py -q`; report the REAL exit code,
     the summary line VERBATIM and the COUNT of `^FAILED` lines, which must be
     0, PROVING YOUR EXTRACTOR IS NOT BLIND over a control string containing
     such a line. Report the test COUNT at C4 against the 24 the reviewer
     measured at `c6c490cb`, and confirm that every one of those 24 node ids is
     still present and still passing — name any that is not. Report
     specifically that the existing single-word threshold test and the
     `the fox jumps` replacement test both still pass, which is S8. Run
     `python3 -m ruff check packages/orchestration/diff_parser.py
     tests/orchestration/test_diff_parser.py` with the repository's own
     configuration, no `--isolated`, and report the real exit code and output
     VERBATIM. Run the canary `python3 -m pytest tests/cli/test_golden_path.py
     -q` and report its real exit code and summary line. Then, in a disposable
     worktree at C4, report the UNMUTATED CONTROL and then ONE further
     mutation: widen the guard so it can never fire — compare the significant
     ratio against a value no ratio can be below — and report the real exit
     code and failing node ids; the S7 test must fail. Remove the worktree and
     prune, then report `git worktree list` 1 line and `git status --porcelain`
     0 lines in the primary checkout.
 G8. STRUCTURE, ARTIFACTS, THE OPEN PR GATE AND THE PUSH. Compare the path set
     of `git diff --name-only c6c490cb..C4` BOTH WAYS against this round's
     expected set — the Change line's list MINUS `.agent/handoff.md`, which C5
     writes — and report both residues EMPTY. Report `git diff --stat
     c6c490cb..C4` restricted to `apps/`, `docs/`, `packages/` and `tests/` and
     confirm the first two EMPTY and the last two holding ONLY
     `packages/orchestration/diff_parser.py` and
     `tests/orchestration/test_diff_parser.py`. Report each commit's insertions
     from `git diff --numstat` for C0a through C4, confirm each single-parent
     and under 500. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
     `.agent/plan.md`, `.agent/live_review.md` and `.agent/prose_slips.md` at
     their commits, against a CONTROL over the C0a blob which is not 0. Report
     that `^Landed: R-` counts 2 in `.agent/live_review.md` at C4 — the two
     lines constraint 7 orders — and that `^Done: R-\d+ — ` counts 25 there.
     Report `git ls-files .remedy-wt` 0 lines and `git branch --list "tmp/*"`
     0 lines. Run `gh pr list --state open --json
     number,headRefName,baseRefName,isDraft` and report it VERBATIM; the
     reviewer read `[]` at the round base; MERGE NOTHING and CREATE NOTHING.
     After C5, run `git push origin feature/f037-rendered-diff-viewer`. ITS
     OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: C5 is authored
     before the push exists, so `.agent/handoff.md` states the push only as an
     INTENT under `## External actions`. Report the real exit code and the
     resulting remote tip in your completion report instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C5: the `## Session` section constraint 13 orders IN FULL, feature
             and round, branch, the round base SHA `c6c490cb`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item AND every SPEC item S1
             through S8, ONE LINE PER GATE for G1 through G8 with its real exit
             code, the open-findings count after this round, and the next
             expected action. C5 cannot table its own numstat — write `self` in
             that cell, as `R-0149` requires. Because this is the session's LAST
             round, the handback is the only return channel: state under
             `## Next` exactly what T001 still owes — the read endpoint — and
             that `R-0715` remains open and untouched.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW.

<<<SLICE PLANF037R5
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
R5 closes the parser's verification gaps and ends the session. It books R4,
resolves `R-0716`, and registers and repairs two defects the R4 red-proofs
exposed: `R-0717`, the intraline side mapping is pinned only for `replace`
opcodes, and `R-0718`, the similarity guard cannot fire for a multi-word line
because separator tokens floor its ratio. Both repairs are proved by the reds
their own fixtures now cause.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R4 gate, the resolution and both registrations | ordered | record first |
| C3 the `R-0717` discriminating fixtures | ordered | must kill both mutations |
| C4 the `R-0718` repair and its test | ordered | ratio over significant tokens |
| C5 the handback | ordered | last round of the session |

## Next Steps
1. The read endpoint, keyed on task run and job per DECISION F037 D2, against
   the route guards the R1 inventory measured. That is what T001 still owes.
2. T002 the rendering core, the binding CSS and the goldens.
3. T003 sidebar, virtual scrolling, lazy languages and the L3 tab.

## Risks
- `R-0715` is open and Low; it is a stale count in a test docstring and belongs
  to whoever next edits that file.
- The parser still has no consumer, so its corpus carries the whole weight.
  Every round that touches it orders mutation red-proofs for that reason, and
  R4 is the round that proved why: a red-proof reported green is how both of
  this round's findings were found.
<<<END PLANF037R5

<<<SLICE LANDEDFROM
Landed: R-0716 — `packages/orchestration/diff_parser.py` now folds a hunkless, noteless, non-binary, non-rename region into the region that FOLLOWS it whenever both carry the same `(minus_header, plus_header)` pair, so the `workspace.diff` shape's doubled header pair reads as ONE file entry instead of two, proved red first and guarded against the same-path/different-headers case, in commit C3 of F037 R4.
<<<END LANDEDFROM

<<<SLICE LANDEDTO
Done: R-0716 — RESOLVED at F037 R4, commit `b2fdbc4ea07b60894f8171a5edfeb8b46162254b`, and verified by the reviewer at `c6c490cb`. `packages/orchestration/diff_parser.py` now folds a region into the one that FOLLOWS it when the earlier region has no hunks, no note, no binary flag and no rename AND both carry the same `(minus_header, plus_header)` pair, which is the collapse-at-flush-time counter-measure the finding names rather than a lookahead in the walk. THE REPAIR WAS PROVED RED BEFORE IT WAS PROVED GREEN, which is the part worth recording: against the UNREPAIRED module the round's two new regression tests failed at exit 1 and the parser returned 2 files for the doubled-header input, matching the reviewer's own measurement of 2 at `6dfd27d9`; at the repaired tree the suite is exit 0. THE GUARD THE FINDING ASKED FOR IS PRESENT AND TESTED: a tracked region and a `--- /dev/null` untracked region for the SAME path stay TWO entries, because the fold compares the header PAIR and never the resolved path. The reviewer re-ran the repaired parser over a reconstruction of `job_evidence._build_workspace_diff`'s output and it returns ONE file entry carrying the real hunk and stats.
<<<END LANDEDTO

<<<SLICE RECORDR5
Gate: F037 R4 — the repair-and-intraline round, and the round whose own RED-PROOF REPORTING GREEN is what found the two findings registered below. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran them itself at `c6c490cb`. TRANSPORT: sha256 `8304eb095e810cedc7266eaf5bacc35d9053fecaae3b2c3a35946eee6076670f` over 28725 bytes and 339 lines, equal across the reviewer's scratch original and the two committed paths, which are ONE git blob `437db60f492af15f9f9fcb2c093c1ee799541aa1`; the chain covers the original, the saved copy and the mirror and claims nothing about any prompt's bytes. EXTRACTION: 2 slices at 42 and 3 content lines, CONTENT 45 against TOTAL 339, PROSE 294, both caps holding. THE PLAN is byte-equal with the trailing-newline control `False`, at 42 lines. THE REGISTRATION RECONSTRUCTS at `1140801 + 1 + 5958 = 1146760` with the baseline a byte PREFIX, and the record moved exactly as ordered: `^- R-\d+ — ` 276 to 277, the single id added being `R-0716`, nothing resolved, the open set 253 and every id distinct. THE REPAIR IS PROVED IN BOTH COLOURS, which is the discipline this record exists to enforce: against the UNREPAIRED module the two new regression tests failed at exit 1 and the parser returned 2 files for the doubled-header input, and at the repaired tree the suite is exit 0. `R-0716` IS RESOLVED ABOVE. THE ROUND'S SECOND MUTATION CAME BACK GREEN AND THE WORKER SAID SO INSTEAD OF REACHING FOR ANOTHER ONE. That mutation was the reviewer's and it was VACUOUS BY CONSTRUCTION: `difflib.SequenceMatcher.get_opcodes()` emits every `insert` opcode with `i1 == i2`, so mapping `insert` onto the OLD side can only ever produce a zero-length span, which the module's own normalisation drops — no corpus could have turned it red. The reviewer confirmed the identity independently at `c6c490cb`. The authoring failure is recorded in `.agent/prose_slips.md` and spends no id, because nothing landed wrong on disk. WHAT THE WORKER DID NEXT IS THE BEST WORK OF THE ROUND: rather than stopping at "the mutation was bad", it measured WHY, found that every intraline fixture in the file produces only `equal` and `replace` opcodes, and declared the residual blind spot it had no order to look for. THE REVIEWER VERIFIED THAT BLIND SPOT AND WIDENED IT: at `c6c490cb`, narrowing the OLD side's opcode tuple to `("replace",)` leaves the suite at `24 passed` exit 0, and narrowing the NEW side's does the same — so BOTH halves of the side mapping are unpinned, not one. That is `R-0717`. FOLLOWING THE SAME THREAD THE REVIEWER MEASURED A SECOND DEFECT the round had no way to see, `R-0718`: the similarity guard cannot fire for any multi-word line. THE CODE ITSELF IS CORRECT ON EVERY SHAPE THE REVIEWER PROBED, which is why both findings are coverage and reachability rather than wrong output: a pure interior deletion marks the removed words on the `del` side alone, a pure interior insertion marks them on the `add` side alone, a replacement marks both, and no emitted span lies outside its own content in any fixture. THREE FURTHER DECLARED DEVIATIONS ARE ALL SOUND: the `last_block.md` numstat reads `234/284` against a file of 339 lines because a full-file rewrite pairs unchanged lines, which is the R-0592 shape reported correctly rather than fabricated; the `Landed:` line names its round and commit role rather than a SHA that cannot exist when the text is written; and the token-identity check added ahead of the offset arithmetic is a refusal where the block's own S6 named the identity as the property the offsets rest on. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

- R-0717 — Medium, THE INTRALINE SIDE MAPPING IS PINNED ONLY FOR `replace` OPCODES, SO HALF OF IT IS A GATE THAT CANNOT FAIL. Raised by the reviewer at the F037 R4 gate; the worker found the gap while diagnosing a vacuous mutation it had been ordered to run, named it in its own Deviations and correctly minted no id. `packages/orchestration/diff_parser.py` maps `difflib` opcodes to character spans with two tuples — `("replace", "delete")` for the old side and `("replace", "insert")` for the new — and every intraline fixture the corpus holds produces only `equal` and `replace`. THE EFFECT IS MEASURED, NOT INFERRED, and the reviewer measured BOTH halves where the worker reported one: in a disposable worktree at `c6c490cb`, narrowing the OLD tuple to `("replace",)` gives exit 0 at `24 passed`, and narrowing the NEW tuple to `("replace",)` gives exit 0 at `24 passed`. Either whole clause can be deleted and the suite stays green, which is the blind-gate class operator amendment amend0827 rule 2 reserves an id for. MEDIUM AND NOT HIGH because the behaviour is CORRECT today — the reviewer exercised both unpinned shapes at `c6c490cb` and a pure interior deletion marks only the `del` side while a pure interior insertion marks only the `add` side — so nothing is wrong on disk and no green is false; what is missing is any test that would notice if it broke. NOT LOW because intraline emphasis is a named line of the feature file's Acceptance and this is the only gate over it. THIS IS NOT `R-0715`, which is a stale numeral in a docstring, and NOT `R-0718`, which is about whether the similarity guard can fire at all rather than about which side a span lands on. COUNTER-MEASURE: a fixture whose pair produces a bare `delete` opcode and one whose pair produces a bare `insert`, each asserting the spans on the marked side AND `[]` on the other — the second assertion is the discriminator, and a fixture that does not kill its mutation has not closed the gap. OPEN.

- R-0718 — Medium, THE INTRALINE SIMILARITY GUARD CANNOT FIRE FOR ANY MULTI-WORD LINE, BECAUSE SEPARATOR TOKENS PUT A FLOOR UNDER ITS RATIO. Raised by the reviewer at the F037 R4 gate, following the thread `R-0717` opened; no round was ordered to look for it. `packages/orchestration/diff_parser.py` tokenises with `re.findall(r"\w+|\W", s)`, which interleaves separators, and computes the guard's ratio over that FULL stream. Two space-separated lines with the SAME word count always match on their separators, so the ratio has a floor no content can go below. MEASURED BY THE REVIEWER at `c6c490cb`, for pairs sharing no word at all: 0.333 at two words, 0.400 at three, 0.429 at four, 0.444 at five and 0.474 at ten, rising toward 0.5. `DIFF_INTRALINE_MIN_RATIO` is 0.3, so the guard is UNREACHABLE for every one of them. The reviewer confirmed the consequence on the shipped module: `alpha beta gamma` against `zzz qqq www` emits spans over EVERY word of BOTH lines — precisely the outcome the guard's own stated purpose is to prevent, since marking every character is the same as marking none. THE ONLY FIXTURE THAT EXERCISES THE GUARD IS SINGLE-WORD, `alpha` against `zulu`, which is the one shape with no separator floor, so the existing threshold test passes while the guard it tests is inert for real lines. MEDIUM AND NOT HIGH because nothing consumes the parser yet and no suite is red. NOT LOW because the guard exists solely to keep whole-line replacements from rendering as all-marked noise, and it does not do that for any line a viewer will actually show. THE DEFECT IS THE REVIEWER'S SPEC: item S7 of the R4 block named the constant and the stream in one sentence and never checked whether the second made the first reachable, which is exactly the reachability class `docs/agents/planner_reviewer_prompt.md` §3 item 5 exists for, arriving through a threshold rather than through a branch. COUNTER-MEASURE: compute the ratio over the SIGNIFICANT tokens only, leaving the span mapping on the full stream so offsets stay exact, and keep the constant where it is — the constant was never the defect. OPEN.
<<<END RECORDR5

<<<SLICE SLIPR5
- 2026-08-28 · F037 R4 · The block's G7 ordered a mutation that was VACUOUS BY
  CONSTRUCTION: it had `insert` opcodes mark the OLD side, and
  `difflib.SequenceMatcher.get_opcodes()` emits every `insert` with `i1 == i2`,
  so the resulting span is always zero-length and the module's own
  normalisation drops it. No corpus could have turned that mutation red. The
  worker ran it, reported the green plainly, diagnosed the cause and declined
  to substitute another mutation, which is the ordered behaviour. Nothing
  landed wrong on disk. A mutation is checked against the SHAPE OF THE DATA THE
  MUTATED BRANCH RECEIVES before it is ordered, not only against the branch
  being reachable — `docs/agents/planner_reviewer_prompt.md` §3 item 5 asks for
  the probe form where that is not obvious, and this is the case it was written
  for.
<<<END SLIPR5
