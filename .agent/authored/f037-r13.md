STEP T001 — F037 Rendered diff viewer — ROUND 13

Goal: DECISION F037 D5's ceiling bounds body LINES only. A file that carries no
body line — a mode change, a binary marker, a pure rename — appends nothing to
that counter, so a diff made of such files is bounded by nothing; and every
assertion the R12 suite added is expressed in terms of the constant itself, so
raising the constant tenfold leaves the suite green. This round registers that
as `R-0722`, adds a second ceiling on FILE ENTRIES, re-bases the two R12 tests
whose fixture crosses both ceilings, and pins the serialized worst-case payload
against a recorded budget so either ceiling being widened turns the suite red.

Base: the round starts from `327c1333` on branch
`feature/f037-rendered-diff-viewer`. Nothing else is in flight.

Bundle, one commit each, in this order:
- C0a save this block verbatim to `.agent/authored/f037-r13.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 apply PLANF037R13 to `.agent/plan.md`
- C2 append GATER12 and FIND0722 to `.agent/live_review.md`, and SLIPR13 to
  `.agent/prose_slips.md`
- C3 append DECISION6 to `.agent/decisions.md` and write SPEC S1 through S3 into
  `packages/orchestration/diff_parser.py`
- C4 write SPEC S4 through S11 into `tests/orchestration/test_diff_parser.py`
- C5 append DONE0722 to `.agent/live_review.md`
- C6 rewrite `.agent/handoff.md` as the handback

Change set, and nothing outside it: `.agent/authored/f037-r13.md`,
`.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
`.agent/prose_slips.md`, `.agent/decisions.md`, `.agent/handoff.md`,
`packages/orchestration/diff_parser.py`,
`tests/orchestration/test_diff_parser.py`. Push the branch after C6. Create no
PR, merge nothing.

Constraints:
1. A slice between the markers is applied BYTE FOR BYTE. Never edit a slice,
   never reflow it, never fix a typo in it. If a slice looks wrong, apply it and
   say so in the handback's Deviations.
2. Production code and test code are DESCRIBED by the SPEC below, not sliced.
   Write them yourself, in this repository's idiom, and report every place your
   reading of the SPEC differed from what you wrote.
3. `packages/orchestration/diff_view_source.py` and
   `packages/orchestration/ui_server.py` are NOT touched this round. The other
   half of `R-0721` — the artifact is read whole before the parser sees it — is
   the next round's, and keeping it out is what lets this round's red-proofs say
   which half they proved.
4. Nothing under `apps/` or `docs/` is touched.
5. Exactly the two existing tests SPEC S5 names change, and in them only the
   fixture they parse and their docstrings; their assertions about the body
   ceiling stay. Every other test in
   `tests/orchestration/test_diff_parser.py` as it stands at `327c1333` is left
   byte-identical.
6. Ruff runs under this repository's own configuration — line length 120, rules
   `E`, `F`, `W`, `I`, `UP`. Never `--isolated`.
7. Every destructive check runs inside a disposable `git worktree` under
   `.remedy-wt/`, never in the primary checkout, which reads
   `git status --porcelain` empty after every commit.
8. C5 runs after C3 and C4. DONE0722 states what this round landed, so the
   commit order is what makes it true.
9. The value in SPEC S1 and the budget in SPEC S11 are the reviewer's measured
   figures, recorded in DECISION6. Do not re-derive them; if a measurement of
   yours disagrees, report the disagreement and apply the SPEC.

SPEC — `packages/orchestration/diff_parser.py`

S1. A module-level constant `DIFF_VIEW_MAX_FILES = 2_000`, placed directly below
    `DIFF_VIEW_MAX_BODY_LINES` and its comment block. Its own comment block
    states: it is the ceiling on FILE ENTRIES the view carries; DECISION F037 D6
    fixes the value at five times the 400-file corpus shape
    `MANY_FILE_DIFF_FILE_COUNT` names; and the DELIBERATE ABSENCE that the two
    ceilings bound the OUTPUT — the input is still read whole by
    `packages/orchestration/diff_view_source.py`, which is where that bound
    belongs.

S2. In `parse_unified_diff_to_view`, immediately AFTER the existing
    `regions = _collapse_doubled_header_regions(regions)` line and before the
    `for file_index, region in enumerate(regions):` loop:

        if len(regions) > DIFF_VIEW_MAX_FILES:
            truncated = True
            regions = regions[:DIFF_VIEW_MAX_FILES]

    with a WHY comment directly above it carrying two facts. FIRST, why the cut
    sits AFTER the collapse: `workspace.diff` carries every header pair twice
    (finding `R-0716`), so a count taken during the walk would bound that shape
    at half the files a reader sees; the collapsed list is the list that becomes
    `files`, so it is the list the ceiling belongs to. SECOND, why the
    comparison is `>` and not `>=`: exactly the ceiling parses in full and is
    not marked truncated, which is the same inclusive boundary
    `DIFF_VIEW_MAX_BODY_LINES` already has.

S3. The `Returns` paragraph of `parse_unified_diff_to_view`'s docstring gains
    one sentence naming BOTH ceilings and saying that `truncated` is True when
    either bites. Nothing else in that docstring changes.

SPEC — `tests/orchestration/test_diff_parser.py`

S4. `_generated_many_file_diff` gains a second parameter
    `pairs_per_file: int = 1`, and writes that many deletion/addition pairs into
    each file's single hunk, with the hunk header's counts following it. Every
    existing call passes one argument and keeps its current behaviour.

S5. `TRUNCATING_MANY_FILE_COUNT` is REPLACED by a constant whose file count is
    strictly below `DIFF_VIEW_MAX_FILES` while its TOTAL body lines are strictly
    above `DIFF_VIEW_MAX_BODY_LINES` — `DIFF_VIEW_MAX_FILES // 2` files at 20
    pairs each is the shape, expressed in the two module constants and not as a
    literal. Both tests that used the old constant,
    `test_many_small_files_are_bounded_by_the_same_total_counter` and
    `test_every_file_stats_still_recount_its_own_lines_under_truncation`, move
    onto it. WHY they must move, and this goes in the first test's docstring:
    the old fixture was 10,400 files, which crosses the FILE ceiling this round
    adds, so the file cut would bite first and the test would stop measuring the
    body counter it exists to measure. The first test additionally asserts that
    the surviving file count is STRICTLY BELOW `DIFF_VIEW_MAX_FILES`, which is
    the discriminator that keeps it about the body ceiling alone. Its assertions
    on `truncated` and on the parsed body-line total are unchanged.

S6. `test_a_diff_of_files_with_no_body_lines_is_cut_to_the_file_ceiling`. A
    generated diff of `DIFF_VIEW_MAX_FILES + 10` files, each a `diff --git`
    header followed by `old mode 100644` and `new mode 100755` and no hunk at
    all. Asserts `truncated` is True, the file entries number exactly
    `DIFF_VIEW_MAX_FILES`, and the parsed body-line total is 0. The third
    assertion is the discriminator: it is the shape the body ceiling cannot see,
    because nothing is ever appended to its counter, and it is the whole of the
    finding.

S7. `test_the_file_ceiling_boundary_holds_on_both_of_its_sides`. Exactly
    `DIFF_VIEW_MAX_FILES` of the same header-only files parse in full with
    `truncated` False; exactly one more is cut to `DIFF_VIEW_MAX_FILES` with
    `truncated` True. Both halves in one test, for the reason the body ceiling's
    boundary test already states: each half alone is satisfiable by a bound one
    off in either direction.

S8. `test_binary_marker_files_are_bounded_by_the_file_ceiling_too`. A generated
    diff of `DIFF_VIEW_MAX_FILES + 10` files, each a `diff --git` header
    followed by a `Binary files a/<path> and b/<path> differ` line. Asserts
    `truncated` True and exactly `DIFF_VIEW_MAX_FILES` entries. Its docstring
    records the measured reason it is a separate shape from S6: at
    `327c1333` the reviewer measured 100,000 such files at 20.3 MB of
    serialized JSON, the largest payload any input shape produced, because the
    binary note is carried per file.

S9. `test_the_file_ceiling_counts_files_after_the_doubled_header_collapse`. A
    generated diff of `DIFF_VIEW_MAX_FILES + 1` files in the `workspace.diff`
    shape — each file's `--- ` and `+++ ` header pair written TWICE, once by the
    wrapper and once by the inner unified diff, exactly as
    `job_evidence._build_workspace_diff` emits it and as this module's own
    `WORKSPACE_DOUBLED_HEADER_DIFF` fixture shows. Asserts `truncated` True and
    exactly `DIFF_VIEW_MAX_FILES` entries. The discriminator, and the docstring
    says so: a cut applied BEFORE the collapse would leave half that many.

S10. `test_the_acceptance_many_file_fixture_stays_below_the_file_ceiling`.
    Asserts `MANY_FILE_DIFF_FILE_COUNT < DIFF_VIEW_MAX_FILES` directly, then
    parses the 400-file corpus fixture and asserts `truncated` False and 400
    entries. A file ceiling at or below the corpus shape would truncate the
    fixture the R11 corpus round added while satisfying every other assertion
    here.

S11. `test_the_worst_case_payload_stays_inside_the_recorded_budget`, and a
    module constant `DIFF_VIEW_MAX_PAYLOAD_BYTES = 4_000_000` above it. The test
    serializes with `json.dumps(view).encode()` and asserts the byte length is
    at most that constant, for BOTH dimensions in one test: the file-dimension
    fixture of `DIFF_VIEW_MAX_FILES + 100` files at one pair each with long
    paths, and the body-dimension fixture
    `_generated_huge_single_file_diff(DIFF_VIEW_MAX_BODY_LINES * 2)`. The
    constant's comment records the two figures the reviewer measured at
    `327c1333`: 1.269 MB for the file dimension and 2.096 MB for the body
    dimension, so the budget is roughly twice the larger of them. WHY the
    budget exists at all, in the test's docstring: both ceilings are expressed
    in constants and every other assertion in this file follows those constants
    wherever they go, so this is the only assertion that fails when a ceiling is
    re-decided upward — the reviewer raised `DIFF_VIEW_MAX_BODY_LINES` tenfold
    at `327c1333` and the whole file stayed green at 37 passed.
    A long path here means one of at least sixty characters; the measured
    figure above was taken on paths of that shape, and a short-path fixture
    measures roughly two thirds of it.

Slice convention: each authored text sits between a line beginning `<<<SLICE `
and a line beginning `<<<END `, both carrying the slice's name. The marker lines
are NEVER written into any target file. The slices are PLANF037R13, GATER12,
FIND0722, SLIPR13, DECISION6 and DONE0722.

<<<SLICE PLANF037R13
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D6.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A4.

## Current Step
R13 repairs `R-0722`. DECISION F037 D5's ceiling bounds body LINES only, so a
diff whose files carry no body lines is bounded by nothing, and every assertion
the R12 suite added follows the constant wherever it goes. The parser gains a
second ceiling on FILE ENTRIES where the collapsed region list becomes `files`;
the two R12 tests whose fixture crosses both ceilings are re-based onto a shape
crossing only the body one; and a recorded payload budget pins what the two
ceilings are for. DECISION F037 D6 records all of it.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R12 verdict, `R-0722`, the slip | ordered | record first |
| C3 DECISION F037 D6 and the file ceiling | ordered | the choice beside what it governs |
| C4 the file-ceiling tests and the budget | ordered | both ceilings, both sides |
| C5 the resolution | ordered | written after the repair is proved |
| C6 the handback | ordered | |

## Next Steps
1. The round after this one carries the other half of `R-0721`:
   `diff_view_source.py` still reads the artifact whole with `read_text` before
   the parser sees it, so the INPUT stays unbounded while the OUTPUT is bounded
   in both dimensions.
2. T002 and T003 are NOT blocked by the refused runner, and the round after that
   states why: `apps/ui/vitest.config.ts` collects `src/**/*.test.ts` in a node
   environment, `tests/orchestration/test_test_runner.py` runs `npx vitest run`
   from pytest and is exit 0 here at `327c1333`, and `tests/ui_contracts/` pins
   the markup vitest never renders.

## Risks
- A ceiling is a behaviour change on a shipped read path. The tests R11 and R12
  added are the regression guard; if one moves that this round did not order
  moved, a ceiling was chosen wrong rather than the test being stale.
- The binding CSS defines no intraline treatment while Acceptance requires it,
  so that stays a question for the round that renders spans.
<<<END PLANF037R13

<<<SLICE GATER12
Gate: F037 R12 — the repair round that bounded the parser's own output. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran the load-bearing ones itself at `327c1333`. TRANSPORT IS PROVED AS FAR AS THIS WORKFLOW CAN PROVE IT, AND NO FURTHER: `.agent/authored/f037-r12.md` and `.agent/last_block.md` are ONE git blob `dab1d123bf1dace73fa89323a671c1cdafa69528`, and that saved copy is 439 lines and 32012 bytes at sha256 `29c103ae837cbf96b80f39377f514531ddcc89956d1fc19486a6dfe127e38bb3`, equal to the sha256 the worker measured on the reviewer's scratch original before C0a. The chain covers the scratch original, the saved copy and its mirror; it says nothing about the bytes the reviewer emitted, which is unmeasurable here. THE PLAN IS BYTE-EQUAL to PLANF037R12 with the trailing-newline negative control False, at 47 lines with one `## Goal` and one `## Next Steps`, re-measured by the reviewer from the committed C0a blob rather than from the worker's report. THE RECORD MOVED AS ORDERED AND ONLY AS ORDERED, recomputed mechanically at `327c1333`: `^- R-\d+ — ` 282 registrations all distinct, `^Done: R-\d+ — ` 30, `^Landed: R-` 1, `^Gate: F\d+ R\d+ — ` 82, open set 252 — down one from 253, the single move being `R-0721`. THE CODE IS RIGHT AND THE REVIEWER READ IT RATHER THAN THE SUMMARY: the guard sits inside `if kind is not None:` so only body lines are counted, it stands BEFORE the append and before either line counter advances so the ceiling is what is appended rather than what is examined, the `break` leaves the flush loop untouched, and `stats` are recounted from the parsed entries at flush so a truncated file can never describe lines the payload does not carry. THE SUITES ARE GREEN AT REAL EXIT CODES RE-RUN BY THE REVIEWER: `python3 -m pytest tests/orchestration/test_diff_parser.py -q` exit 0 at `37 passed in 2.14s`, `python3 -m pytest tests/ui_server/test_diff_endpoint.py tests/orchestration/test_diff_view_source.py -q` exit 0 at `15 passed`, `python3 -m ruff check packages/orchestration/diff_parser.py tests/orchestration/test_diff_parser.py` exit 0 at `All checks passed!`, and the canary `python3 -m pytest tests/cli/test_golden_path.py -q` exit 0 at `42 passed`, matching the base figure. THE REVIEWER RAN ITS OWN RED-PROOFS RATHER THAN REPRODUCING THE ORDERED ONES, in a disposable worktree at `327c1333` with `python3 -B` and the parser restored and re-hashed after every mutation to sha256 `a5b40fe9243f63f9ad8a3aa139ac19d8c7aa14aefcd1f764f42989dd9c49b7f0`: the unmutated control is exit 0 at `37 passed`; the off-by-one `>=` to `>` is exit 1 at `3 failed, 34 passed`, which is the boundary test earning its place; and `body_lines_appended += 1` weakened to `+= 0` is exit 1 at `4 failed, 33 passed`. THE THIRD READING IS THE ONE THAT MATTERS AND IT CAME BACK GREEN: raising `DIFF_VIEW_MAX_BODY_LINES` from 20_000 to 200_000 is exit 0 at `37 passed`, because every assertion in that file is expressed in terms of the constant and the only pin outside it is a lower bound. That is registered as `R-0722` by the round reading this entry, and it is a gap in the ROUND'S GATES rather than in its execution: the block ordered a ceiling and got one, correctly, in both colours. THE DECLARED DEVIATIONS ARE ALL HONEST: the six-line WHY comment, the whole-directory gate run twice because the first run's output was piped through `tail` and could not carry the completeness sweep, one unordered base worktree for a timing figure that cannot be taken in the primary checkout, and two mutations firing on fewer tests than a reader would predict — each reported with its reason and its measurement, and the last two are the block's own instruction that the ordered property is the COLOUR obeyed correctly. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER12

<<<SLICE FIND0722
- R-0722 — Medium, DECISION F037 D5's CEILING BOUNDS ONE OF THE PAYLOAD'S TWO DIMENSIONS, AND NO TEST IN THE SUITE CAN SEE EITHER THAT GAP OR THE CEILING BEING RAISED. Raised by the reviewer at the F037 R12 gate while running red-proofs of its own choosing; no round was ordered to look for it. THE GAP IS THE FILE DIMENSION. `parse_unified_diff_to_view` counts BODY LINES against `DIFF_VIEW_MAX_BODY_LINES`, and a file that carries no body line appends nothing to that counter — a mode change, a binary marker, a pure rename — so a diff made of such files is bounded by nothing at all and `truncated` stays False however large it is. MEASURED BY THE REVIEWER at `327c1333` on this host: 100,000 mode-change files parse to 100,000 file entries at `truncated` False and 13.8 MB of serialized JSON in 1.49 s, and 100,000 binary-marker files parse to 100,000 entries at `truncated` False and 20.3 MB, against the 2.096 MB the single-file worst case AT the body ceiling produces. The bounded dimension's worst case is a tenth of the unbounded one's, which is the whole shape of the defect. THE GUARD IS BLIND IN THE OTHER DIRECTION TOO, AND THAT IS THE HALF THAT MAKES THIS AN ID RATHER THAN A SLIP: every ceiling assertion F037 R12 added is expressed in terms of `DIFF_VIEW_MAX_BODY_LINES` itself, so the suite follows the constant wherever it goes. In a disposable worktree at `327c1333`, with `python3 -B` and the module restored and re-hashed afterwards, raising that constant tenfold to 200_000 leaves `python3 -B -m pytest tests/orchestration/test_diff_parser.py -q` at REAL EXIT CODE 0 and `37 passed`; the only pin outside the constant is `HUGE_DIFF_BODY_LINE_COUNT < DIFF_VIEW_MAX_BODY_LINES`, a LOWER bound that cannot fail when a ceiling rises. DECISION F037 D5 states that the worst-case payload is bounded at roughly 2.6 MB of JSON and nothing on disk measures that consequence. MEDIUM AND NOT HIGH because the two constants on disk are correct today, no suite is red, nothing renders wrong, and the failure mode is degradation rather than incorrectness. NOT LOW because `workspace.diff` at job scope is exactly where a formatter run, a vendored dependency or a lockfile rewrite produces tens of thousands of file entries carrying no body lines, because a bound that cannot notice being widened is the blind-gate class operator amendment amend0827 rule 2 reserves an id for, and because this is the bound `R-0721`'s repair exists to be. THIS IS NOT `R-0721`, which is the ABSENCE of any bound in F037 and is resolved in part: this is the bound that exists being one-dimensional and unpinned. COUNTER-MEASURE: a second ceiling on FILE ENTRIES, applied where the collapsed region list becomes `files` so `workspace.diff`'s doubled headers are counted once; the two R12 tests whose fixture crosses both ceilings re-based onto a shape that crosses only the body one, so each ceiling keeps a test that measures it alone; and a test pinning the SERIALIZED worst-case payload of both dimensions against a recorded byte budget, which is the assertion that fires when either ceiling is re-decided upward. OPEN.
<<<END FIND0722

<<<SLICE SLIPR13
- 2026-08-28 · F037 R12 · The resolution `Done: R-0721 — RESOLVED IN PART`
  removes that id from the open set the pre-emission checklist derives
  mechanically — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — while half of the finding, the unbounded artifact read in
  `diff_view_source.py`, is still open on disk. The remaining half survives in
  prose only, in the handback and in the plan's Next Steps. A partial
  resolution is invisible to the one arithmetic the checklist runs, so a round
  that resolves half of a finding says so in the resolution AND leaves the
  remainder somewhere the count can see it.
<<<END SLIPR13

<<<SLICE DECISION6
## DECISION F037 D6 — the parsed diff is bounded in BOTH dimensions, and a recorded payload budget is what notices a ceiling being widened

**Date:** 2026-08-28 · **Round:** F037 R13 · **Finding:** `R-0722`

**The choice.** `packages/orchestration/diff_parser.py` gains a second module
constant `DIFF_VIEW_MAX_FILES = 2_000`. Where the collapsed region list becomes
the view's `files`, a list longer than that ceiling is cut to it and the
contract's `truncated` flag is set. A diff of exactly the ceiling parses in full
and is not marked truncated, which is the same inclusive boundary
`DIFF_VIEW_MAX_BODY_LINES` already has. `tests/orchestration/test_diff_parser.py`
gains a recorded payload budget, `DIFF_VIEW_MAX_PAYLOAD_BYTES = 4_000_000`,
asserted over the serialized worst case of both dimensions.

**Why a second ceiling exists at all.** D5's ceiling counts BODY LINES, and a
file can carry none: a mode change, a binary marker and a pure rename each add a
file entry and append nothing to that counter. Measured at `327c1333`, 100,000
mode-change files parse to 100,000 entries and 13.8 MB of JSON with `truncated`
False, and 100,000 binary-marker files to 20.3 MB, against 2.096 MB for the
single-file worst case at the body ceiling. D5 bounded the dimension that was
easy to see and left the other one open.

**Why 2,000 files.** The corpus's many-files shape is 400
(`MANY_FILE_DIFF_FILE_COUNT`), so five times it leaves the fixture the R11 round
added rendering in full with room to spare, and the file dimension's worst case
then measures 1.269 MB of JSON at long paths. A sidebar listing more than two
thousand files is not a reading surface in any case; beyond it the honest answer
is the one the contract already has, which is to say in the data that the list
is a prefix.

**Why the cut is applied AFTER the doubled-header collapse.** `workspace.diff`
emits every file's header pair twice — that is finding `R-0716`, and
`_collapse_doubled_header_regions` exists to fold it away. A count taken during
the walk would therefore bound the job-scope shape at half the files a reader
sees, which is a bound that depends on which producer wrote the artifact. The
collapsed list is the list that becomes `files`, so it is the list the ceiling
belongs to.

**Why a recorded payload budget rather than more assertions about the
constants.** Every ceiling assertion in the suite is expressed in terms of the
constant it tests, so the suite follows a constant wherever it is moved: raising
`DIFF_VIEW_MAX_BODY_LINES` tenfold at `327c1333` left the file green at 37
passed. A budget over the SERIALIZED bytes is the only assertion in this file
that is stated in a unit neither ceiling controls, so it is the only one that
fails when a ceiling is widened. The value is roughly twice the larger of the
two measured worst cases, which leaves room for path lengths the fixtures do not
model while still failing an order-of-magnitude change.

**What a truncated view looks like, unchanged from D5.** The last file present
may carry a partial hunk or none, files after it do not appear, each file's
`stats` still equal a recount of that file's own parsed lines, and `truncated`
True is the client's signal that the list is a prefix. A file-dimension
truncation drops whole file entries from the tail and changes nothing about the
entries that remain.

**What is still NOT bounded, stated plainly.** The INPUT.
`packages/orchestration/diff_view_source.py` reads the artifact with
`read_text`, whole, before the parser is called, so both ceilings bound what is
BUILT and SERVED and neither bounds what is READ. That is the remaining half of
`R-0721` and it is the next round's; a diff of one enormous minified line is the
shape that reaches neither ceiling and still costs the read.

**Alternatives rejected.** (1) Stop the walk when the region count crosses the
ceiling — rejected because the count during the walk is the UNCOLLAPSED one, so
the effective limit would differ between the two artifacts F037 serves. (2)
Fold the file ceiling into the body counter by charging each file header a
notional number of lines — rejected as a bound nobody can read off the contract.
(3) Bound the serialized bytes directly in the parser — rejected because the
parser builds a structure and does not serialize it; the byte figure belongs to
the layer that does, and as a TEST budget it pins the consequence without
putting a serialization step in a pure function. (4) Leave the file dimension
unbounded and rely on the read bound coming next — rejected because the input
bound cannot express a file count and 8 MB of headers is still 100,000 entries.

**How to reverse.** Delete `DIFF_VIEW_MAX_FILES` and the three-line cut that
reads it in `parse_unified_diff_to_view`, delete
`DIFF_VIEW_MAX_PAYLOAD_BYTES` and the tests F037 R13 added, and restore the
fixture of the two tests S5 re-based to the 10,400-file shape they carried at
`327c1333`. DECISION F037 D5 and its ceiling are untouched by this decision and
survive its reversal.
<<<END DECISION6

<<<SLICE DONE0722
Done: R-0722 — RESOLVED at F037 R13 by the round's C3 and C4, in the commit order constraint 8 of the R13 block fixes. `packages/orchestration/diff_parser.py` now carries `DIFF_VIEW_MAX_FILES` beside `DIFF_VIEW_MAX_BODY_LINES` and cuts the region list to it where that list becomes the view's `files`, setting the contract's `truncated` flag — so the dimension a file with no body lines lives in is bounded, which is the gap the finding measured at 13.8 MB and 20.3 MB of JSON for a hundred thousand mode-change and binary-marker files. THE CUT IS PLACED WHERE THE FINDING ASKED, after `_collapse_doubled_header_regions`, so `workspace.diff`'s doubled header pairs are counted once and the bound does not depend on which producer wrote the artifact; a test whose fixture doubles every header pair is the discriminator for that placement rather than a comment claiming it. THE SECOND HALF OF THE FINDING IS THE ONE THAT REQUIRED A NEW KIND OF ASSERTION AND IT IS PRESENT: `DIFF_VIEW_MAX_PAYLOAD_BYTES` pins the SERIALIZED worst case of both dimensions, in a unit neither ceiling controls, which is why it is the assertion that fires when a ceiling is re-decided upward — the exact blindness the finding demonstrated by raising `DIFF_VIEW_MAX_BODY_LINES` tenfold and watching 37 tests stay green. EACH CEILING KEEPS A TEST THAT MEASURES IT ALONE: the two R12 tests whose 10,400-file fixture crosses both are re-based onto a shape below the file ceiling, and the first of them now asserts that the surviving file count is strictly below `DIFF_VIEW_MAX_FILES`, so a file cut can never be mistaken for the body cut it exists to measure. WHAT THIS RESOLUTION DOES NOT CLAIM: the INPUT is still read whole by `packages/orchestration/diff_view_source.py`, which is the remaining half of `R-0721` and not of this finding, and no assertion here bounds a diff of one enormous line, which reaches neither ceiling.
<<<END DONE0722

Done when — the gates below, every one executed with its REAL exit code recorded,
one line per gate in the handback. G1 through G8 run at the commits named; none
of them runs after C6, so the handback can quote every one of them.

G1 HYGIENE. Read `.agent/STOP` from disk before C0a and again before C6 and
report both readings. Report `git rev-parse HEAD` before C0a and state whether
it equals `327c1333`, `git branch --show-current`, and the `git status
--porcelain` line count after each of C0a through C5.

G2 TRANSPORT, ONE DIGEST COMPARISON. Report sha256, byte count and line count of
the committed `.agent/authored/f037-r13.md` blob, and state whether they equal
the reviewer's scratch original at `.remedy-wt/f037-r13-block.md` — compare the
two files directly, disk to disk. Report `git rev-parse <C0b>:.agent/authored/f037-r13.md`
and `git rev-parse <C0b>:.agent/last_block.md` and whether they are the same
blob. State what the chain covers and what it does not.

G3 EXTRACTION AND CAPS, measured on the COMMITTED C0a blob and never on the
prose. For each slice report its content line count; report TOTAL lines of the
blob, CONTENT as their sum, PROSE as TOTAL minus CONTENT, and whether TOTAL is
at most 490 and PROSE at most 400.

G4 THE PLAN AT C1. Report whether `.agent/plan.md` is byte-equal to the
PLANF037R13 slice extracted from the committed C0a blob, including the trailing
newline, plus the negative control against that slice minus its trailing
newline. Report the count of lines exactly `## Goal` and exactly `## Next
Steps`, and `wc -l` with whether it is strictly under 50.

G5 THE RECORD AT C2 AND C5. For each of the four appends — GATER12 and FIND0722
into `.agent/live_review.md`, SLIPR13 into `.agent/prose_slips.md`, DONE0722
into `.agent/live_review.md` — report reader (a), `result == before + b"\n" +
slice` re-read from disk; reader (b), which COUNTS the blank-line-separated
units of the slice and compares the LAST that many units of the file against
them IN ORDER, reporting the count it measured; and a negative control for both
readers that flips one byte inside the FIRST appended paragraph. Report whether
each file's pre-round blob is a byte PREFIX of the result, reading that blob
with `git show 327c1333:<path>` into memory and never over the tracked file.
Then
report, line-anchored over `.agent/live_review.md` after C5 with the base figure
beside each: `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`, `^Gate: F\d+ R\d+
— `, the open-set size, whether every registered id is distinct, and the number
of times `R-0722` occurs as a registration and as a resolution. Over
`.agent/decisions.md`, report `^## DECISION ` and the count of `F037 D6`.

G6 THE RED-PROOFS OF THE FILE CEILING. All runs inside a disposable worktree at
the C4 tree, never in the primary checkout, with `__pycache__` purged and
`python3 -B` for every run, the module restored between runs and each restore
verified byte-identical by sha256 against the unmutated C4 blob. Report the
UNMUTATED CONTROL's exit code and summary line first. Then, for each mutation
below, report the occurrences of the replaced string BEFORE the edit — which
must be 1 — the REAL exit code, the summary line, and the node ids that fail.
The ordered property is the COLOUR: report the names and counts you measure
rather than any this block predicts.
(a) Delete the three lines SPEC S2 adds. Expect RED.
(b) Change S2's `>` to `>=`. Expect RED.
(c) Move S2's three lines to directly ABOVE the
`regions = _collapse_doubled_header_regions(regions)` line instead of below it.
Expect RED.
(d) Raise `DIFF_VIEW_MAX_FILES` tenfold to `20_000`. Expect RED.
(e) Raise `DIFF_VIEW_MAX_BODY_LINES` tenfold to `200_000`. Expect RED — this
mutation is exit 0 at `327c1333` and is the whole of `R-0722`'s second half.
Runs (d) and (e) are SLOW and are not hung: every fixture in the file is
expressed in the two constants, so raising one multiplies the generated input by
the same factor. Give each of them several minutes before concluding anything.

G7 SUITE, LINT AND CANARY AT C4. One pytest process at a time; never two at
once. Report the REAL exit code and the full summary line of each:
`python3 -m pytest tests/orchestration/test_diff_parser.py -q`;
`python3 -m pytest tests/orchestration/test_diff_view_source.py
tests/ui_server/test_diff_endpoint.py -q`, whose base figure at `327c1333` is
`15 passed`; `python3 -m ruff check packages/orchestration/diff_parser.py
tests/orchestration/test_diff_parser.py` under this repository's own
configuration; and the canary `python3 -m pytest tests/cli/test_golden_path.py
-q`, whose base figure is `42 passed`. Report the parser suite's `in <n>s`
figure at C4 beside the base figure `37 passed in 2.14s`, and if the difference
is more than two seconds name which fixtures account for it.

G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C5. Report `git diff
--name-only 327c1333..<C5>` and both residues against the change set above —
actual minus expected and expected minus actual. Report `git diff --stat`
restricted to `docs/`, to `apps/`, and to `packages/`; the third must hold
`packages/orchestration/diff_parser.py` and nothing else, which is what proves
constraint 3. Report each commit's insertion count from `git show --numstat`
for C0a through C5 and whether each is under 500, and check those figures cell
by cell against the `+/-` column of the handback's own `## Commits` table.
Report the count of lines matching `^<<<SLICE ` and `^<<<END ` in
`.agent/plan.md`, `.agent/live_review.md`,
`packages/orchestration/diff_parser.py` and
`tests/orchestration/test_diff_parser.py`, and the same counts over the C0a blob
as the control that the counter is not blind. Report `git ls-files .remedy-wt`
line count. Run `gh pr list --state open --json
number,headRefName,baseRefName,isDraft` verbatim and report its exit code and
stdout.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It
carries the SESSION NUMBER of this feature — session 4 — the round, the range
`327c1333..<C6>`, a per-commit changed-files table with the `+/-` column, one
line per gate G1 through G8 with its real result, the authored-text proofs, the
deviations, the item-status table covering C0a through C6 and G1 through G8 and
`R-0722`, and the next expected action. Derive any cap it must respect from
AGENTS.md yourself; this block states none. Then push the branch.
