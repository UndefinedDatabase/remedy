# F037 R11 — the huge-diff corpus shape and the recorded budget

## Goal

Book the R10 verdict, close the one shape T001's own task slicing names and the
corpus never grew, and record the number Acceptance asks for.

`docs/roadmap/features/T5_F037.md` slices T001 as "the parser (unified → JSON) +
corpus tests (rename, binary, mode change, empty file, huge file chunking)". Every
shape in that list has a test except the last. Acceptance asks for a "10k-line
fixture within the perf budget (recorded)" and no fixture in the repository is
larger than a few dozen lines. This round closes the corpus gap and records the
measurement; it changes no parser behaviour.

It also registers, without repairing, what the reviewer measured while sizing the
round: nothing in F037 bounds the work a single diff can cost. That is `R-0721`,
and R12 carries the repair, because a ceiling is a behaviour change and belongs in
a round whose red-proofs are about it rather than beside a corpus addition.

## Base

Base commit `dc938d0e2faa11c84fc1da459e967cc0bc655c82`, branch
`feature/f037-rendered-diff-viewer`. This is the SHA of the R10 handback this round
starts from; every range reading below is against it.

## Bundle — five commits

| Commit | Subject | Paths |
|--------|---------|-------|
| C0a | docs(agent): save the F037 R11 step block | `.agent/authored/f037-r11.md` |
| C0b | docs(agent): mirror the F037 R11 block into last_block | `.agent/last_block.md` |
| C1 | docs(agent): point the plan at the F037 R11 corpus round | `.agent/plan.md` |
| C2 | docs(agent): book the R10 gate verdict and register R-0721 | `.agent/live_review.md` |
| C3 | test(orchestration): add the huge-diff corpus shape and record its budget | `tests/orchestration/test_diff_parser.py` |
| C4 | docs(agent): hand back F037 R11 | `.agent/handoff.md` |

## Exact change set

Nothing outside these six paths is written, created or deleted:

    .agent/authored/f037-r11.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    tests/orchestration/test_diff_parser.py
    .agent/handoff.md

Plus the push of `feature/f037-rendered-diff-viewer` after C4, which is ordered
explicitly here and sits outside every gate below.

## Constraints

1. A slice between its marker lines is applied BYTE FOR BYTE and is never edited,
   retyped, reflowed or trimmed — not to make a numeral in this block come true,
   and not to satisfy a cap. A slice's text already carries exactly one trailing
   newline. If a slice and a gate disagree, apply the slice, report the
   measurement, and declare the contradiction under Deviations.
2. Production code is DESCRIBED by the SPEC below, never sliced. The worker writes
   that code itself, in the idiom of the file it is editing, and reads the whole
   file before touching it.
3. `packages/` IS NOT TOUCHED THIS ROUND. `packages/orchestration/diff_parser.py`
   is READ and exercised; not one byte of it changes. This round pins the parser's
   CURRENT behaviour. R12 changes it.
4. `docs/`, `docs/roadmap/`, `apps/` are NOT touched. No `.ts`, `.tsx` or React
   code is written: the frontend test runner is refused in this environment and
   code neither role can execute must not be certified.
5. No existing test, fixture constant, helper or import in
   `tests/orchestration/test_diff_parser.py` is weakened, deleted, renamed or
   reordered. C3 ADDS.
6. `.agent/live_review.md` is append-only. Nothing already in it is edited,
   renumbered or deleted, and no id other than `R-0721` is registered. NOTHING is
   resolved this round: `R-0721` is registered OPEN and stays open.
7. No PR is created and nothing is merged. The Open PR Gate is READ and reported.
8. Every destructive check runs inside a disposable `git worktree` under
   `.remedy-wt/`, never in the primary checkout, and the worktree is removed and
   pruned afterwards.
9. NO TEST ADDED THIS ROUND ASSERTS A TIMING FIGURE AS AN EQUALITY OR A TIGHT
   BOUND. The only wall-clock assertion permitted is the single generous ceiling
   SPEC S5 describes, whose purpose is to catch a change in COMPLEXITY CLASS, not
   to police a machine. A test that would go red on a runner three times slower
   than this one is a defect, not a budget.

## SPEC — C3, the huge-diff corpus shape

Read the whole of `tests/orchestration/test_diff_parser.py` first. At the base it
is 763 lines: a module docstring, `from __future__` , two stdlib imports, an
import block from `packages.orchestration.diff_parser`, a run of inline fixture
constants each introduced by a `#:` comment naming the shape it covers, small
module-level helpers, and module-level test FUNCTIONS — there is no test class in
this file. Match that idiom exactly.

Add a new section at the END of the file, introduced by the same
`# ---- #` banner comment style the file already uses between sections, titled for
the huge shape.

**S1 — the builders, not inline constants.** The file's docstring says every
fixture carries its diff text INLINE. A ten-thousand-line fixture cannot, and that
exception is DOCUMENTED rather than left for a reader to notice: add two
module-level builder functions whose docstrings say in one sentence why this shape
is generated where every other shape is literal. The first builds a single-file
diff of N changed body lines as alternating `-`/`+` pairs under one hunk header,
with a `diff --git` header pair. The second builds an N-file diff, each file with
one small hunk, so the many-files dimension is covered as well as the many-lines
one. Both take their size as a parameter and return diff TEXT.

**S2 — the ten-thousand-line shape parses completely.** A test asserting the
STRUCTURE, with no timing in it: the fixture parses to exactly one file entry,
whose hunks hold exactly as many body lines as were generated, whose `stats`
`added` and `deleted` each equal a recount of that file's own parsed line kinds,
and whose hunk ids are all distinct. Assert the PROPERTY against the generated
size, never a transcribed literal — the file's existing
`test_every_file_stats_equal_a_recount_of_its_own_parsed_lines` is the model.

**S3 — line numbering survives the whole file.** The same fixture, asserting that
the old-side line numbers of the `del` lines are strictly increasing across the
entire parsed file and likewise the new-side numbers of the `add` lines, and that
the LAST line of the file carries the line number its position implies. This is
the assertion that would catch a counter that drifts only after thousands of
lines — the shapes already in the corpus are far too short to reach it.

**S4 — the many-files shape.** The second builder at a size in the hundreds: the
parsed view holds exactly that many file entries, their paths are all distinct and
in input order, and no entry is a phantom with zero hunks. The doubled-header
collapse this parser performs is what makes this worth asserting at scale.

**S5 — the recorded budget, as a complexity guard.** One test that parses the
larger of the two sizes and asserts the elapsed wall-clock time is under a
GENEROUS absolute ceiling. Its docstring RECORDS, as prose, the figure measured
when the test was written, and names the machine class it was measured on, and
states plainly that the ceiling is not that figure: it is set roughly an order of
magnitude above it so that a slower runner passes while a change from linear to
quadratic cost fails. Say in the docstring what the quadratic figure would be, so
the next reader can see the ceiling separates the two cases rather than having to
trust that it does. Use `time.perf_counter`; add `time` to the stdlib imports in
the existing import block, in alphabetical order.

**S6 — nothing else changes.** The module docstring, the existing imports, every
fixture constant, every helper and all twenty-eight existing tests are untouched.

## Slices

<<<SLICE PLANF037R11
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/decisions.md` carries the DECISION series, F037 D1 through D4.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A4.

## Current Step
R11 closes the one shape T001's task slicing names and the corpus never grew —
the huge diff — and records the perf number Acceptance asks for. It changes no
parser behaviour. It also registers `R-0721`: nothing in F037 bounds the work one
diff can cost, and the contract's own `truncated` field is only ever relayed from
an upstream sentinel, never set by this feature.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R10 verdict and R-0721 | ordered | record first; nothing is resolved |
| C3 the huge-diff corpus shape | ordered | structure, numbering, scale, budget |
| C4 the handback | ordered | |

## Next Steps
1. R12 repairs `R-0721`: a line ceiling the parser enforces itself, setting the
   contract's `truncated` flag when it bites, with the ceiling above the 10k
   fixture Acceptance names so that fixture still renders in full.
2. R13 carries the same bound at the endpoint, where the artifact is read whole
   into memory before the parser ever sees it.
3. T002's rendering core and all of T003 stay BLOCKED. `npx vitest`, the `npm`
   script and the direct binary were each refused again while planning R10, for
   the reviewer, as they were for both roles at R8.

## Risks
- A wall-clock assertion is the flakiest thing a suite can hold. R11's ceiling is
  set an order of magnitude above the measured figure so it separates linear from
  quadratic cost and nothing finer; tightening it later would buy noise.
- The binding CSS defines no intraline treatment while Acceptance requires
  intraline emphasis. Inventing a colour early would breach the feature file's
  own banner, so it stays a question for the round that renders spans.
<<<END PLANF037R11

<<<SLICE GATER10
Gate: F037 R10 — the repair round that opened session 3, and the first round of this feature whose transport proof begins at a value the reviewer held BEFORE delegating. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all of them itself at `dc938d0e`. TRANSPORT IS PROVED END TO END, WHICH IS STRONGER THAN THE CHAIN R9 COULD OFFER: the block was written to the reviewer's gitignored scratch at `.remedy-wt/f037-r10-block.md` before the worker existed, measured there at sha256 `fd579581a57a690f379763b89d3404d51d7f8afe70ab44fada1ec1c8c9080335` over 25073 bytes and 301 lines, and the committed `.agent/authored/f037-r10.md` is byte-identical to that scratch original, so the FIRST link is measured rather than merely disclaimed; the saved copy and `.agent/last_block.md` are ONE git blob `12c20a91f4ea4e5477c1eba4a56725c2a5a22191`. EXTRACTION REPRODUCES THE BLOCK'S ARITHMETIC EXACTLY: 4 slices at 48, 1, 1 and 1 content lines, CONTENT 51 against TOTAL 301, PROSE 250, both caps holding. THE PLAN IS BYTE-EQUAL to PLANF037R10 with the trailing-newline negative control `False`, at 48 lines with one `## Goal` and one `## Next Steps` — and the block deliberately named no predicted line count for that slice, which is why the off-by-one that cost R8 a defect and R9 a declared deviation could not recur. ALL THREE APPENDS ARE PROVED BY BYTE IDENTITY re-read from disk, `result == before + b"\n" + slice`, applied in order GATER9 then FIND0720 at C2 and DONE0720 at C4, each negative control `False`, the base of `.agent/live_review.md` measured at 1176292 bytes exactly as the block named it, and the pre-round blob is a byte PREFIX of the result so nothing in the append-only record was rewritten. THE RECORD MOVED AS ORDERED AND ONLY AS ORDERED: `^- R-\d+ — ` 280 to 281, `^Done: R-\d+ — ` 28 to 29, `^Landed: R-` unmoved at 1, `^Gate: F\d+ R\d+ — ` 79 to 80, the single id added being `R-0720`, exactly `R-0720` resolved, every id distinct and the open set unmoved at 252. THE SUITES AND THE LINT ARE GREEN AT REAL EXIT CODES RE-RUN BY THE REVIEWER: `python3 -m pytest tests/ui_contracts/ -q` exit 0 at `588 passed, 4 skipped`, the delta of exactly one being C3's new test; `python3 -m ruff check tests/ui_contracts/test_diff_surface_css.py` exit 0 at `All checks passed!`; and the canary `python3 -m pytest tests/cli/test_golden_path.py -q` exit 0 at `42 passed`, matching the base figure. THE RED-PROOF REPRODUCES AND IT IS GENUINELY DISCRIMINATING, which is the whole point of this round: in a disposable worktree at the C3 tree with `__pycache__` purged and `python3 -B` used, the unmutated control is exit 0 at `8 passed`; the mutation is a PURE REORDER of the `.diffLine` rule — the reviewer verified the declaration MULTISET is identical before and after and only the order differs — and it comes back exit 1 at `1 failed, 7 passed` failing exactly `test_no_font_shorthand_follows_the_ligature_declaration`; and THE SAME REORDER RUN AGAINST THE GUARD AS IT STOOD AT THE BASE `c777fe83` comes back exit 0 at `7 passed`. That third reading is the one that matters: it proves the defect was real rather than asserted, and it proves the NEW assertion is what fires rather than an existing substring assertion the reorder happens to disturb. THE CODE MATCHES THE SPEC WITHOUT DRIFT: two module-level helpers with the same left-boundary guard the file's existing `_declaration` uses, one test covering BOTH `.diffLine` and `.hunkHead` because a shorthand could be introduced into either, and each assertion message naming the selector it is about; not one existing assertion was weakened, renamed or reordered, and the stylesheet itself is byte-identical, which the restricted `apps/` diff proves rather than claims. THE FIVE DECLARED DEVIATIONS ARE ALL HONEST AND NONE IS A DEFECT: a second `git worktree remove` returned exit 128 because the first had already succeeded, and the worker reported the failing call rather than only the good one; the base-guard negative control reused the one worktree via a detach-and-remutate rather than creating a second, which leaves constraint 8 intact because no mutation ever touched the primary checkout; the `tests/ui_contracts/` figure moved 587 to 588, for which the block predicted nothing; and the stated assumption about the shorthand's right boundary is correct and was verified behaviourally, since `.hunkHead` carries both `font-size` and `font-feature-settings` and stayed green throughout. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER10

<<<SLICE FIND0721
- R-0721 — Medium, NOTHING IN F037 BOUNDS THE WORK ONE DIFF CAN COST, AND THE CONTRACT FIELD THAT EXISTS TO SAY SO IS NEVER SET BY THIS FEATURE. Raised by the reviewer at the F037 R10 gate while sizing the huge-diff corpus round; no round was ordered to look for it. THE CONTRACT ALREADY HAS THE SEAM: `parse_unified_diff_to_view` returns a top-level `truncated` flag and `build_diff_view` copies it onto the envelope, but the ONLY thing that ever sets it True is the upstream `[DIFF TRUNCATED]` sentinel that some other producer wrote into the artifact first. F037 itself never truncates anything, so `truncated` is a relay, not a bound. NEITHER HALF OF THE FEATURE BOUNDS ANYTHING ELSE EITHER: `packages/orchestration/diff_view_source.py` reads the artifact with `artifact.read_text(encoding="utf-8")`, whole, with no size check before or after, and `packages/orchestration/diff_parser.py` splits that string and appends one dict per body line with no ceiling on the count. The endpoint then serialises the whole structure into a single response. MEASURED BY THE REVIEWER at `dc938d0e` on this host, parsing generated single-file diffs: 10004 input lines and 0.42 MB of text produce 10001 parsed line objects, 1.28 MB of JSON and a 5.1 MB peak allocation in 0.363 s; 20004 input lines produce 2.57 MB of JSON and a 10.3 MB peak in 0.740 s. COST IS LINEAR AND THAT IS THE GOOD NEWS — the reviewer measured 1k, 2k, 5k, 10k and 20k lines and the per-line cost is flat, and a 400-file shape scales the same way, so there is no quadratic defect hiding here and the JSON is a steady ~3.1x the input bytes. THE DEFECT IS THE ABSENCE OF A CEILING, NOT THE SLOPE: a linear function with no bound is still unbounded, and `workspace.diff` is a job's ENTIRE workspace diff, a size no code in this repository constrains. A job that rewrote a lockfile or vendored a dependency would have the server read the whole artifact into memory, build one dict per line, and serialise several tens of megabytes into one HTTP response, on a request any viewer makes automatically when the panel opens. MEDIUM AND NOT HIGH because nothing is wrong on disk today, no suite is red, no artifact in the repository is known to be that large, and the failure mode is degradation rather than incorrectness. NOT LOW because Acceptance names a recorded perf budget and there is nothing to record against, because the field that would express the bound already exists and is inert, and because the client half that would otherwise defend itself — virtual scrolling beyond 2k lines, per T003 — cannot be built in this environment while the frontend test runner is refused, so the server is the only place a bound can currently live. THIS IS NOT `R-0719`, a feature-file pointer to a design-reference section that does not exist, and not `R-0720`, a guard blind to declaration order: this is a missing bound in shipped production code. COUNTER-MEASURE: the parser enforces a ceiling on parsed body lines ITSELF and sets `truncated` True when it bites, with the ceiling set ABOVE the 10k-line fixture Acceptance names so that fixture still renders in full; the endpoint half follows, since the artifact is read whole before the parser ever sees it. F037 R11 records the measurements and adds the corpus shape and changes no behaviour; R12 carries the repair, which is a behaviour change and earns red-proofs of its own. OPEN.
<<<END FIND0721

## Gates — every command is RUN and its REAL exit code recorded

Eight gates. "Green" as a word is a finding; a gate that was not executed is
reported as not executed.

**G1 hygiene.** Read `.agent/STOP` from disk BEFORE C0a and again before C4, and
report the literal reading both times. Report `git rev-parse HEAD` before C0a and
state whether it equals the base above, and `git branch --show-current`. Report the
LINE COUNT of `git status --porcelain` after each of C0a, C0b, C1, C2 and C3.

**G2 transport, ONE digest comparison.** After C0b, report `git rev-parse` of both
`HEAD:.agent/authored/f037-r11.md` and `HEAD:.agent/last_block.md` and state
whether they are the same blob hash. Report the sha256, byte count and line count
of the working copy of `.agent/authored/f037-r11.md`. State plainly what the chain
covers: the saved copy and its mirror.

**G3 extraction and caps.** Extract every slice from the COMMITTED C0a blob by its
marker lines, in Python, and report each slice's line count, the CONTENT total, the
TOTAL line count of the blob and PROSE = TOTAL − CONTENT. State whether TOTAL is at
most 490 and PROSE at most 400. Measure the blob; carry no figure from this block's
prose into that table.

**G4 the plan at C1.** Report whether `.agent/plan.md` is byte-equal to the
PLANF037R11 slice, newline included, and a NEGATIVE CONTROL against the same slice
minus its trailing newline, which must read False. Report the count of lines
exactly matching `## Goal` and of lines exactly matching `## Next Steps`. Report
`wc -l` and state whether it is STRICTLY under 50. The binding clause is the strict
inequality; the measurement wins over any figure elsewhere and disagreement is
declared.

**G5 the record at C2.** For each of the two appends — GATER10 then FIND0721 —
report the file's byte size before and after and TWO independent readers. Reader
(a) is the BYTE IDENTITY `result == before + b"\n" + slice`, re-read from disk.
Reader (b) counts the N blank-line-separated units in the slice and compares the
LAST N units of the file against the slice's N units IN ORDER. Report a NEGATIVE
CONTROL per append flipping ONE byte INSIDE the first appended paragraph; BOTH
readers must come back False. Report whether the pre-round blob of
`.agent/live_review.md` is a byte PREFIX of the result.
Then report these counts over `.agent/live_review.md` after C2, line-anchored:
`^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`, `^Gate: F\d+ R\d+ — `, the size of
the open set, whether every id is distinct, whether `R-0721` occurs exactly once as
a registration, and whether it occurs ZERO times as a resolution — constraint 6
orders it left open.

**G6 the corpus round's red-proofs.** All of this runs inside a disposable
`git worktree` under `.remedy-wt/`, at the C3 tree, never in the primary checkout;
purge `__pycache__` and use `python3 -B` before EVERY run; restore the mutated file
between runs and verify each restore is byte-identical.

Report the UNMUTATED CONTROL first: `python3 -B -m pytest
tests/orchestration/test_diff_parser.py -q`, its REAL exit code and verbatim
summary line.

Then TWO mutations of `packages/orchestration/diff_parser.py`, each applied alone
and reverted before the next. Both are SILENT TRUNCATIONS — they cap the parser's
output at a size every fixture already in the corpus sits below, so the twenty-eight
existing tests cannot see either one. That is deliberate: it is what makes them
discriminators for the tests C3 adds rather than proofs that the old corpus works.
The reviewer measured both against the base corpus at `dc938d0e` and both came back
exit 0 at `28 passed`; C3's tests are the only thing that can turn them red.

For each, report the exact string replaced, the count of its occurrences in the file
BEFORE the edit, the REAL exit code, the verbatim summary line, and WHICH node ids
fail as measured. THE ORDERED PROPERTY IS THE COLOUR: each must be RED. Do not treat
any predicted name or count as the gate.

- **(a) a cap on parsed body lines.** Insert, immediately before the single
  `hunk["lines"].append(` statement and at that statement's own indentation, a guard
  that skips the append once the current hunk already holds 100 lines. Every fixture
  in the corpus is far shorter than 100 lines, so nothing already written can notice.
- **(b) a cap on file regions.** Replace the single `regions.append(current)`
  statement with the same append guarded by a check that fewer than 10 regions exist
  so far. The corpus's multi-file fixtures hold a handful of files, so again nothing
  already written can notice.

If a mutation comes back GREEN, STOP: report it, diagnose WHY the new assertions
could not see it, and declare it rather than substituting a different mutation. A
green here means C3's tests do not actually reach the scale they claim to.

Afterwards report `git worktree remove`, `git worktree prune`, the line count of
`git worktree list` and the line count of `git status --porcelain` in the primary
checkout.

**G7 suite, lint and canary at C3.** ONE pytest process at a time; never two in
parallel. Report the REAL exit code and verbatim summary of each:

- `python3 -m pytest tests/orchestration/test_diff_parser.py tests/orchestration/test_diff_view_source.py -q`, and the count of
  lines matching `^FAILED`. Report an EXTRACTOR-BLINDNESS CONTROL: run the same
  counter over a control string that does begin with `FAILED` and report a non-zero
  count, so a zero above is a measurement rather than a blind spot.
- `python3 -m pytest tests/orchestration/test_diff_parser.py --collect-only -q` and
  the COUNT of node ids it lists, together with the node ids of the tests C3 added.
  Never derive node ids by regexing `-v` output.
- `python3 -m ruff check tests/orchestration/test_diff_parser.py` under the
  repository's own configuration, with NO `--isolated`.
- The canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The base figure
  is `42 passed`; report the measured figure beside it and name any difference.
- REPORT THE WALL-CLOCK COST C3 ADDS: the verbatim `in <n>s` figure of the parser
  suite at the base commit `dc938d0e` and at C3, both measured, and state the
  difference. A corpus test that makes the suite several times slower is a finding
  even when it is green.

**G8 structure, artifacts and the Open PR Gate at C3.** Report
`git diff --name-only dc938d0e..<C3>` and both RESIDUES against the change set
above minus `.agent/handoff.md`: actual minus expected, and expected minus actual.
Report `git diff --stat` restricted to `packages/`, `docs/` and `apps/` — EACH MUST
BE EMPTY, and the `packages/` reading is the one that proves constraint 3 — and to
`tests/`, which must hold only `tests/orchestration/test_diff_parser.py`. Report
per-commit insertions from `git diff --numstat` for C0a through C3, each commit's
parent count, and whether each insertion count is under 500. Report a marker sweep
of `^<<<SLICE ` and `^<<<END ` over `.agent/plan.md` at C1 and `.agent/live_review.md`
at C2, and the SAME counter over the C0a blob, whose figures must be greater than
zero so the zeros are a measurement. Report `git ls-files .remedy-wt` line count.
Report the Open PR Gate verbatim:
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

## Done when

C0a, C0b, C1, C2, C3 and C4 are committed in that order, one commit each, the
branch is pushed, `.agent/handoff.md` is rewritten per
`docs/agents/handback_template.md` carrying the state block, the deviations, the
item-status table and the next steps, and every gate above is reported with its
REAL exit code. The handback names SESSION 3 of feature F037 and round 11, and it
states the measured wall-clock figures S5 recorded, so the next round reads them
without re-deriving them.

A gate that could not be run is reported as NOT RUN with the literal refusal or
error text — never as a pass, and never worked around.
