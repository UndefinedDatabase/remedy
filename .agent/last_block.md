STEP R4 / F037 — RENDERED DIFF VIEWER — T001 PART TWO, THE REPAIR AND INTRALINE
Goal:        REPAIR THE DEFECT R3 SURFACED, THEN FINISH THE LINE SHAPE. R3's
             parser splits ONE file into TWO entries for the `workspace.diff`
             shape, because that emitter writes the `--- a/X` and `+++ b/X`
             header pair itself AND then hands the same pair to
             `difflib.unified_diff`. That is registered this round as `R-0716`
             and repaired in the commit after the registration. The round then
             adds the intraline spans the contract's line shape carries, which
             is the last piece of the parser before the read endpoint.
             The defect is the REVIEWER'S SPEC, not R3's execution: R3
             implemented S4 exactly as written and declared the disagreement,
             which is why this is a repair and not a fault.
             YOU CREATE NO PULL REQUEST THIS ROUND AND YOU MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the record — the R3 gate and the registration of
             `R-0716` · C3 the `R-0716` repair with its regression test ·
             C4 intraline spans with their tests · C5 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f037-r4.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `packages/orchestration/diff_parser.py`,
             `tests/orchestration/test_diff_parser.py`, `.agent/handoff.md`.
             This list bounds what you WRITE INTO THE REPOSITORY. It does NOT
             bound what you DO: G6 and G7 order a disposable worktree and G8
             orders a push. NOTHING under `apps/` or `docs/` is written, and
             under `packages/` and `tests/` ONLY the two files named.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f037-r4.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f037-r4.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own; G2 has you measure
    four points and prove them EQUAL, and the reviewer holds the scratch value.
 2. THE SLICES ARE APPLIED BYTE FOR BYTE; THE SPEC IS IMPLEMENTED, NOT COPIED.
    A SLICE begins at the line AFTER `<<<SLICE NAME` and ends at the line
    BEFORE `<<<END NAME`; its TEXT is its content lines joined with a newline
    plus ONE trailing newline, and that is the ONLY definition of a slice's
    bytes used anywhere in this block. The numbered SPEC items are NOT slices:
    they describe behaviour you write as real Python. If a slice contradicts
    something you measure, apply it anyway and DECLARE it under Deviations.
 3. THE ONE EOF APPEND IN THIS ROUND IS: the target file's bytes AS THEY STAND
    IN THE COMMIT IMMEDIATELY BEFORE the one applying the append, plus exactly
    ONE newline, plus the slice's TEXT as constraint 2 defines it. Read that
    baseline with `git show <sha>:<path>` where `<sha>` is THE COMMIT YOU ARE
    ABOUT TO BUILD ON — for C2 that is C1, whose SHA you know because you just
    made it. NEVER read a baseline from a commit of an earlier ROUND, and never
    overwrite a tracked file to obtain one.
 4. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5. THE FINDING IS
    REGISTERED BEFORE IT IS REPAIRED — C2 carries the registration and C3 the
    repair — because `docs/agents/planner_reviewer_prompt.md` §4 item 4 puts
    findings on disk first so nothing is lost if a session dies mid-repair.
    `.agent/plan.md` is advanced at C1, the FIRST substantive commit, as §3
    item 23 requires of any round that touches the finding ledger.
 5. NOTHING IS EDITED OUT OF THE APPEND-ONLY RECORD. `.agent/live_review.md` is
    append-only from its `## Findings` heading down. No existing finding
    paragraph, no `Done:` line and no existing `Gate:` paragraph is rewritten,
    deleted or renumbered. `R-0715` is NOT touched and stays OPEN.
 6. YOU DO NOT RESOLVE `R-0716`. Only reviewer-authored text sets a resolution.
    When the repair lands at C3, append to `.agent/live_review.md` — as the
    LAST line of that file, in that same commit — exactly one line of the form
    `Landed: R-0716 — <one sentence: what changed, and the commit>` and nothing
    else. Never write a `Done:` paragraph, never mint a finding id, never write
    a `Gate:` paragraph and never write a DECISION.
 7. THE MODULE STAYS SELF-CONTAINED, PURE AND TOTAL. It imports only the Python
    standard library — `difflib` is expected and permitted for S6 — and never
    `review_scope` or `review_subject`. No file system, no subprocess, no
    network, no logging, no global mutable state, and it NEVER raises on
    malformed input.
 8. RE-READ `.agent/STOP` FROM DISK before C0a and again before C5. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
 9. DESTRUCTIVE VERIFICATION IS ISOLATED. The red-proofs of G6 and G7 run ONLY
    inside a disposable `git worktree` under `.remedy-wt/`, never in the
    primary checkout, which reads `git status --porcelain` 0 lines at every
    commit. Remove the worktree and run `git worktree prune` before C5. Run no
    `npm`, `npx`, `node` or `vite`.
10. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form
    of environment assignment. Route anything that counts, hashes, compares or
    mutates through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY. `--timeout` IS NOT AVAILABLE to pytest here: it exits 4
    and reports no failure. Purge `__pycache__` and use `python3 -B` around any
    mutation, or a stale module reports the wrong colour.
11. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `6dfd27d9` was
    measured by the reviewer at that commit. It is a REFERENCE to report
    against, NOT a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
12. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 1
    of F037 and that R4 is the round. The handback has NO LENGTH CAP.

SPEC — the `R-0716` repair, in `packages/orchestration/diff_parser.py`:
 S1. THE SHAPE, so the repair is aimed at a measured thing. `job_evidence.py`
     appends `--- a/<rel>` and `+++ b/<rel>` itself, and then appends
     `difflib.unified_diff(..., fromfile=f"a/<rel>", tofile=f"b/<rel>")`, whose
     first two lines are that SAME pair. One file therefore carries the header
     pair twice, and the current `--- ` rule opens a second region on the
     repeat. The reviewer measured the result at `6dfd27d9`: two entries for
     one path, the first with 0 hunks and `stats` both 0 and `note` None.
 S2. THE REPAIR IS A COLLAPSE AT FLUSH TIME, NOT A LOOKAHEAD. After the walk
     and before regions become files, fold a region into the one that FOLLOWS
     it when ALL of these hold of the EARLIER region: it has no hunks, its
     `note` is None, it is not binary, it carries no rename, and its
     `(minus_header, plus_header)` pair is EQUAL to the following region's
     pair, with both of that earlier region's headers present. Fold by dropping
     the earlier region and keeping the later one. Apply it repeatedly so three
     repeats collapse as cleanly as two.
 S3. WHAT THE REPAIR MUST NOT DO, stated because it is the way this fix goes
     wrong. It must NOT merge two regions that resolve to the same PATH by
     different headers — `safe.diff` legitimately carries a tracked region for
     a path and an untracked `--- /dev/null` marker, and those are two facts.
     It must NOT drop a region carrying a `note`, which is the only explanation
     an empty region has. It must NOT reorder files. Compare the header pair,
     never the resolved path.
 S4. THE REGRESSION TEST IS WRITTEN BEFORE THE REPAIR AND PROVED RED. Add a
     test that feeds the doubled-header shape and asserts EXACTLY ONE file
     entry, with the hunk, the stats and the path the single real file has.
     G6 orders you to run it against the UNREPAIRED module first and report the
     failure. Add a second test asserting that a tracked region and a
     `--- /dev/null` untracked region for the SAME path stay TWO entries, which
     is the S3 guard.

SPEC — intraline spans, in the same module and its test:
 S5. THE LINE SHAPE GAINS ONE KEY. Every line entry carries `"intraline"`, a
     list of `[start, length]` integer pairs indexing into that entry's own
     `content`. It is `[]` on every `ctx` line and on any `add`/`del` line with
     nothing to mark, so the key is ALWAYS present and a client never has to
     test for it. `DIFF_VIEW_VERSION` stays 1: version 1 has never been served
     to anything — there is no endpoint yet — so this completes v1 rather than
     changing a shipped shape. Say exactly that in the docstring, in one
     sentence, so a later reader does not mistake it for an unversioned change.
 S6. PAIRING, then WORD DIFF. Within one hunk, find each maximal run of
     consecutive `del` entries immediately followed by a maximal run of
     consecutive `add` entries. Pair them by position — the i-th `del` with the
     i-th `add` — for i up to the shorter run's length; the surplus lines of the
     longer run get `[]`. For each pair, split both `content` strings into
     tokens with a regex that keeps the separators, so token boundaries map
     back to character offsets exactly; `re.findall(r"\w+|\W", s)` is
     sufficient and its concatenation must equal the original string, which is
     the property that makes the offsets sound. Run
     `difflib.SequenceMatcher(a=del_tokens, b=add_tokens)`. Map its opcodes to
     character spans: `replace` and `delete` mark the OLD side, `replace` and
     `insert` mark the NEW side, `equal` marks neither.
 S7. THE SIMILARITY GUARD, and the reason it exists. Compute the matcher's
     `ratio()`. When it is STRICTLY BELOW `DIFF_INTRALINE_MIN_RATIO = 0.3`, emit
     `[]` for BOTH lines of that pair: two lines with almost nothing in common
     are a whole-line replacement, and marking every character is the same as
     marking none. Export the constant so a test names it rather than
     transcribing `0.3`.
 S8. SPANS ARE NORMALISED. Merge spans that touch or overlap, drop zero-length
     spans, and return them sorted by `start`. Every emitted span must satisfy
     `0 <= start` and `start + length <= len(content)` — a span that indexes
     past its own content is the defect this normalisation exists to make
     impossible.
 S9. THE TESTS FOR INTRALINE. A word-diff fixture where one word changes in a
     line, asserting the EXACT spans on both the `del` and the `add` entry and
     asserting that slicing `content` by those spans yields the changed words —
     assert the SLICED TEXT, not only the numbers, because that is the property
     a reader can check. A pair below the ratio threshold asserting `[]` on
     both. A `ctx` line asserting `[]`. An unpaired surplus line asserting `[]`.
     A property test over every fixture already in the file: for every line of
     every parsed file, every span lies inside its own `content`.
S10. NOTHING ELSE CHANGES. No existing test is edited, weakened or deleted, no
     existing assertion is relaxed, and every test the file already holds still
     passes unchanged — G7 measures exactly that.

Done when:
 G1. HYGIENE, THE BASE AND THE SENTINEL. Report `git rev-parse HEAD` BEFORE
     C0a, which must be `6dfd27d94374cc1a8940394279a1fee9afeaf549`, and
     `git branch --show-current`, which must be
     `feature/f037-rendered-diff-viewer`. Report `git status --porcelain` as a
     LINE COUNT after each of C0a, C0b, C1, C2, C3 and C4, each 0. C5's own
     reading belongs in no file this round writes; take it and report it in
     your completion report. Report `.agent/STOP` read from disk before C0a and
     before C5, both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f037-r4.md`, as saved at C0a, as mirrored at C0b and
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
 G4. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF037R4 under the
     newline-INCLUDED convention of constraint 2. Run the negative control
     against the slice MINUS its trailing newline and report FALSE. Report
     `^## Goal$` 1, `^## Next Steps$` 1, a match for `\bF\d{3}\b`, and `wc -l`
     STRICTLY UNDER 50.
 G5. THE REGISTRATION, AT C2, by the operation constraint 3 defines with the
     baseline read from C1. Prove it TWO WAYS. Reader (a), RECONSTRUCTION:
     baseline plus one newline plus RECORDR4's text is BYTE-EQUAL to
     `.agent/live_review.md` at C2 and the baseline is a byte PREFIX of it;
     report the arithmetic in bytes. Reader (b), STRUCTURE: split the file at C2
     on blank lines, count N as the number of blank-line units the SLICE holds
     — a number YOUR script counts, never one this block asserts — and report
     that the LAST N units equal the slice's N units IN ORDER. NEGATIVE
     CONTROL: flip ONE byte at an offset you assert and report to lie inside
     the FIRST appended paragraph, and report that BOTH readers reject. Then
     report the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — ` before and after
     C2; the reviewer measured 276, 24, 1, 19 and 73 at the base, and after C2
     they must read 277, 24, 1, 19 and 74. Report the finding ids ADDED as a
     SET, which must be exactly `R-0716`; the resolved ids ADDED and REMOVED
     and the finding ids REMOVED as SETS, all three EMPTY; that all ids are
     DISTINCT; the maximum id after C2, which is `R-0716`; and the open set
     after C2, which is 253.
 G6. THE REPAIR IS PROVED BY ITS OWN RED, in a disposable worktree under
     `.remedy-wt/` and NEVER in the primary checkout. In that worktree, put the
     C3 TEST FILE in place while leaving `packages/orchestration/diff_parser.py`
     AT ITS C2 CONTENT — the unrepaired module — purge `__pycache__`, and run
     `python3 -B -m pytest tests/orchestration/test_diff_parser.py -q`. Report
     the real exit code, which must be NON-ZERO, the summary line, and the
     failing node ids VERBATIM: the doubled-header regression test of S4 must be
     among them. Report also, from that same unrepaired run, the number of
     files `parse_unified_diff_to_view` returns for the doubled-header input,
     which the reviewer measured as 2 at `6dfd27d9`. THEN, in the primary
     checkout at C3, run the same suite command and report a real exit 0 with
     its summary line. A repair whose test never went red has proved nothing.
 G7. THE SUITE, THE LINT, THE CANARY AND THE INTRALINE RED-PROOFS, at C4. In
     the PRIMARY checkout run, as ONE pytest process from the repository root,
     `python3 -m pytest tests/orchestration/test_diff_parser.py -q` and report
     the REAL exit code, the summary line VERBATIM and the COUNT of `^FAILED`
     lines, which must be 0; PROVE YOUR EXTRACTOR IS NOT BLIND over a control
     string containing such a line. Report the test COUNT at C4 against the 16
     the reviewer measured at `6dfd27d9`, and confirm that every one of those
     16 node ids is still present and still passing — name any that is not.
     Run `python3 -m ruff check packages/orchestration/diff_parser.py
     tests/orchestration/test_diff_parser.py` with the repository's own
     configuration, no `--isolated`, and report the real exit code and output
     VERBATIM. Run the canary `python3 -m pytest tests/cli/test_golden_path.py
     -q` and report its real exit code and summary line. THEN, in a disposable
     worktree, report the UNMUTATED CONTROL's exit code and summary FIRST, and
     then each of these mutations SEPARATELY, restoring between them and
     purging `__pycache__` each time, reporting for each the real exit code and
     the failing node ids VERBATIM:
     (a) make the similarity guard never fire — compare the ratio against a
         value no ratio can be below, so every pair gets spans. S9's
         below-threshold test must fail.
     (b) mark the OLD side from the NEW side's opcodes — swap so that `insert`
         marks the old side instead of `delete`. S9's exact-span test must fail.
     For EACH mutation name the exact file and report the count of the bytes
     you replaced IN THAT FILE, which must be 1 before the edit. If a mutation
     produces NO failure, report that plainly rather than reaching for another:
     a green mutation means the assertion does not read what it claims to.
     Remove the worktree and prune, then report `git worktree list` 1 line and
     `git status --porcelain` 0 lines in the primary checkout.
 G8. STRUCTURE, ARTIFACTS, THE OPEN PR GATE AND THE PUSH. Compare the path set
     of `git diff --name-only 6dfd27d9..C4` BOTH WAYS against this round's
     expected set — the Change line's list MINUS `.agent/handoff.md`, which C5
     writes — and report both residues EMPTY. Report `git diff --stat
     6dfd27d9..C4` restricted to `apps/`, `docs/`, `packages/` and `tests/` and
     confirm the first two EMPTY and the last two holding ONLY
     `packages/orchestration/diff_parser.py` and
     `tests/orchestration/test_diff_parser.py`. Report each commit's insertions
     from `git diff --numstat` for C0a through C4, confirm each single-parent
     and under 500. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
     `.agent/plan.md` and `.agent/live_review.md` at their commits, against a
     CONTROL over the C0a blob which is not 0. Report that
     `.agent/live_review.md` at C4 ends with the `Landed: R-0716` line
     constraint 6 orders and that `^Landed: R-` counts 2 there. Report `git
     ls-files .remedy-wt` 0 lines and `git branch --list "tmp/*"` 0 lines. Run
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
     and report it VERBATIM; the reviewer read `[]` at the round base; MERGE
     NOTHING and CREATE NOTHING. After C5, run `git push origin
     feature/f037-rendered-diff-viewer`. ITS OUTCOME IS NOT A VALUE OF ANY FILE
     THIS ROUND WRITES: C5 is authored before the push exists, so
     `.agent/handoff.md` states the push only as an INTENT under
     `## External actions`. Report the real exit code and the resulting remote
     tip in your completion report instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C5: the `## Session` section constraint 12 orders, feature and
             round, branch, the round base SHA `6dfd27d9`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item AND every SPEC item S1
             through S10, ONE LINE PER GATE for G1 through G8 with its real
             exit code, the open-findings count after this round, and the next
             expected action. C5 cannot table its own numstat — write `self` in
             that cell, as `R-0149` requires. STATE PLAINLY under Deviations
             any SPEC item you could not implement as written and why.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW.

<<<SLICE PLANF037R4
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
R4 closes T001's parser half. It registers `R-0716` — the parser splits one
file into two entries for the `workspace.diff` shape, whose emitter writes the
header pair itself and then hands the same pair to `difflib` — repairs it in
the commit after the registration, and adds the intraline spans the contract's
line shape carries. The repair is proved by its own red before it lands.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R3 gate and the `R-0716` registration | ordered | findings persist first |
| C3 the `R-0716` repair and its regression test | ordered | red proved before green |
| C4 intraline spans and their tests | ordered | the contract's line shape |
| C5 the handback | ordered | |

## Next Steps
1. The read endpoint, keyed on task run and job per DECISION F037 D2, against
   the route guards the R1 inventory measured.
2. T002 the rendering core, the binding CSS and the goldens.
3. T003 sidebar, virtual scrolling, lazy languages and the L3 tab.

## Risks
- `R-0715` is open and Low; it is a stale count in a test docstring and belongs
  to whoever next edits that file.
- The parser still has no consumer, so its corpus carries the whole weight.
  Every round that touches it orders mutation red-proofs for that reason.
<<<END PLANF037R4

<<<SLICE RECORDR4
Gate: F037 R3 — the parser round, T001 part one. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran them itself at `6dfd27d9`. TRANSPORT: sha256 `e5bd63a70b28652d86c6f76eaebd16fc0da95f11ddb46d9c7758d4607721f61a` over 30544 bytes and 389 lines, equal across the reviewer's scratch original, the committed `.agent/authored/f037-r3.md` blob and the committed `.agent/last_block.md` blob, the two committed paths being ONE git blob `b26bbb839cc26ef523c328f974d741e678310b7a`; the chain covers the original, the saved copy and the mirror and claims nothing about any prompt's bytes. EXTRACTION: 3 slices at 46, 1 and 12 content lines, CONTENT 59 against TOTAL 389, PROSE 330, both caps holding. THE PLAN is byte-equal to its slice with the trailing-newline control `False`, at 46 lines. THE TWO APPENDS RECONSTRUCT against baselines read from C1, each with the baseline a byte PREFIX: `1136389 + 1 + 4411 = 1140801` and `5070 + 1 + 922 = 5993`. THE RECORD MOVED AS ORDERED AND ONLY AS ORDERED: `^Gate: F\d+ R\d+ — ` 72 to 73 with every other counter unmoved, nothing registered and nothing resolved, the open set 252 at both points and `R-0715` still ending `OPEN.`. THE CODE IS REAL AND THE REVIEWER EXERCISED IT RATHER THAN READING ONLY ITS TESTS: `python3 -m pytest tests/orchestration/test_diff_parser.py -q` gives `16 passed` at a real exit 0, `python3 -m ruff check` over both new paths under the repository's own configuration gives `All checks passed!` at exit 0, and the canary gives `42 passed` at exit 0. THE RED-PROOFS ARE GENUINE, WITH THE UNMUTATED CONTROL REPORTED BESIDE THEM as finding R-0703 requires: control exit 0 at `16 passed`, then three separate mutations at exit 1 — suppressing the old-side line advance failed 5 nodes including the full-tuple line-number assertion, breaking the `[binary file]` sentinel literal failed the binary node, and forcing the deleted count to zero failed 4 nodes including the stats-property test. Each mutated string occurred exactly once in the file before its edit, and all of it ran in a disposable worktree with the primary checkout at 0 lines throughout. THE REVIEWER PROBED THE PARSER BEYOND ITS OWN CORPUS and every case came back right: the untracked `--- /dev/null` marker reads `added` and keeps its hash comment as the note, a git deletion reads `deleted` with stats `0/2`, a git rename reads `renamed` carrying `old_path`, both binary shapes read `binary`, the truncation sentinel sets the top-level flag, the unsafe-artifact sentinel keeps its note with no hunks, a non-diff returns no files, a deleted line whose own text begins with a dash is read as a deletion of `- dashed` rather than as structure, the no-newline marker produces no entry, and a `rstrip`-ed blank context line from the `workspace.diff` shape numbers correctly on both sides. ONE DEFECT IS REGISTERED BELOW AS `R-0716`, and it is the REVIEWER'S SPEC rather than this round's execution: the worker implemented S4 exactly as written, measured the disagreement against the real emitter, and declared it under Deviations instead of quietly widening the rule — which is the behaviour the single-writer split exists to produce. Four further filled-in choices were declared and are all sound: bounding the hunk body by the header's declared counts rather than by line shape, which is what makes the dashed-deletion case above come out right; leaving `[FOCUSED DIFF TRUNCATED]` unhandled because S8 named only the other sentinel; first-come `note` precedence with the two sentinel sources forcing an overwrite; and tolerating a non-string argument, which is constraint 8's totality carried one step further than S11 asked. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

- R-0716 — Medium, THE PARSER RETURNS TWO FILE ENTRIES FOR ONE FILE ON THE `workspace.diff` SHAPE, WHICH IS ONE OF THE TWO SCOPES THE READ ENDPOINT WILL SERVE. Raised by the reviewer at the F037 R3 gate; the worker found the shape, measured it against the real emitter and declared it under Deviations, correctly minting no id because its block ordered none. THE DEFECT IS THE REVIEWER'S SPEC, NOT THE ROUND'S EXECUTION: item S4 of the R3 block ruled that a `--- ` line outside a hunk body starts a new file entry, and `packages/orchestration/diff_parser.py` implements exactly that. THE EMITTER IS THE PROBLEM AND IT WAS MEASURED. `packages/orchestration/job_evidence.py::_build_workspace_diff` appends `--- a/<rel>` and `+++ b/<rel>` itself, and then appends the output of `difflib.unified_diff(..., fromfile=f"a/<rel>", tofile=f"b/<rel>")`, whose own first two lines are that same header pair — so every file in `workspace.diff` carries the pair TWICE. THE EFFECT IS MEASURED, NOT INFERRED: the reviewer ran the shipped parser at `6dfd27d9` over a reconstruction of that emitter's output and got 2 files for 1 path, the first with 0 hunks, `stats` of 0 and 0, and `note` None — a phantom entry a sidebar would render as a real changed file with nothing in it. MEDIUM AND NOT HIGH because nothing consumes the parser yet: there is no endpoint, no test asserts the current behaviour in either direction, and no suite is red, so no green is false today. NOT LOW because `workspace.diff` is the JOB-scope diff that DECISION F037 D2 makes one of exactly two things the v1 endpoint can serve, so the defect sits directly on the feature's own delivery path. THE COUNTER-MEASURE IS A COLLAPSE AT FLUSH TIME rather than a lookahead in the walk: fold a region into its successor when the earlier one has no hunks, no note, no binary flag, no rename and a header pair equal to the successor's. It must compare the HEADER PAIR and never the resolved path, because `safe.diff` legitimately carries both a tracked region and an untracked `--- /dev/null` marker for one path and those are two distinct facts. OPEN.
<<<END RECORDR4
