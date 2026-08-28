### STEP T004 — F256 Diff viewer completion, round 8 (THE RECORDED MEASUREMENT)

Goal: write the three pieces F256 built, and the numbers rounds 6 and 7 measured,
into a Built State section of `docs/roadmap/features/T5_F256.md`. F037's
Acceptance asks for "a recorded measurement, not a claim", and until this round
the numbers live only in test docstrings. This is the last piece of F256's scope
before the integration gate and the closure sequence.

Base: `b8a918a1`, the tip of `feature/f256-diff-viewer-completion`. Every reading
below was taken there by the reviewer.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f256-r8.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 append the R7 verdict to `.agent/live_review.md` and one dated line to
  `.agent/prose_slips.md`
- C3 append the Built State section to `docs/roadmap/features/T5_F256.md`
- C4 rewrite `.agent/handoff.md`

Change set, these paths and nothing else:

- `.agent/authored/f256-r8.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/prose_slips.md`
- `docs/roadmap/features/T5_F256.md`
- `.agent/handoff.md`

NO CODE IS EDITED BY THIS ROUND. Nothing under `apps/`, `packages/` or `tests/`
changes by a byte, and no file under `docs/` other than the one named above.
`docs/roadmap/STATUS.md` and `docs/roadmap/ROADMAP.md` are NOT touched — the
STATUS flip belongs to the closure sequence, not here, and AGENTS.md forbids
editing `ROADMAP.md` without an explicit operator request.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName`.
   Do NOT create or merge a pull request. Stay on
   `feature/f256-diff-viewer-completion`; do not branch, never work on `main`.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f256-r8.md`, never from this prompt's text.
4. AGENTS.md binds in full: self-review before every commit, one logical step per
   commit, `.agent/plan.md` current before every commit, clean tree, push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under the
   gitignored `.remedy-wt/`. This round orders none: it ships no code, so there is
   no mutation red-proof to run and none is expected in the handback.
6. Shell forms rejected by this session's guard are RE-EXPRESSED as a script file
   under `.remedy-wt/` run with `python3`, never skipped and never weakened.
   Report each one.
7. `.agent/prose_slips.md` is APPEND ONLY and is never rewritten or renumbered.
   Its entries are separated by a blank line and carry no id and no severity.
8. NO NUMBER IN THE BUILT STATE SLICE IS YOURS TO ADJUST. Every figure in it was
   measured by round 6 and round 7 and re-measured by the reviewer. If G6's
   cross-check shows one of them is NOT in the file that produced it, STOP and
   hand back with the mismatch stated — do not "correct" either side.
9. NO EXISTING LINE OF `docs/roadmap/features/T5_F256.md` IS CHANGED. The Built
   State is an APPEND: the pre-round blob must remain a byte PREFIX of the result.

### SPEC — there is no code in this round

C3 is the single append described by the `BUILTF256` slice below. There is no
production code, no test, and no new file. The three sections it adds correspond
one-for-one to the three pieces the feature file's "The three pieces" section
already names, in the same order — T001, T002, T003 — so a reader meets them in
the order the scope was written in.

### The authored slices

<<<SLICE PLANF256R8
# Plan — F256 Diff viewer completion

Branch: feature/f256-diff-viewer-completion, cut from `main` at `0e8ab5b4`.
F256 was claimed by Rule A5 as the first unchecked line of Package 1 in
`docs/roadmap/STATUS.md`.

## Goal
Finish the rendered diff viewer F037 shipped: highlighting actually rendered
rather than only modelled, the 10k-line budget measured and recorded, and the
file sidebar's visual treatment ruled by a named authority.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 wire the highlighting | done | `678bc698`, `8bcff3db`, DECISIONS D1 D2 |
| T003 rule on the sidebar's treatment | done | `1b70fb02`, DECISION F256 D3 |
| T002 measure, server half | done | `4aea7ba2`, DECISION F256 D4 |
| T002 measure, client half | done | `95ecaf14`, DECISIONS F256 D5 D6 |
| T002 record the numbers | done | this round |
| the integration gate | open | next round |
| the closure sequence | open | needs two rounds |

## Next Steps
1. Run the integration gate over the whole branch.
2. Build the closure evidence and the review zip.
3. Commit the STATUS closure in a round of its own, per the closure protocol.

## Risks
- The closure sequence needs TWO rounds — evidence and zip, then the STATUS
  commit — and a STATUS `[x]` flip needs its README and ledger pins in the same
  commit or `tests/docs/` goes red.
- `.agent/candidates.md` is empty and must stay empty through closure.
<<<END PLANF256R8

<<<SLICE GATEF256R7
Gate: F256 R7 — the CLIENT MEASUREMENT round, which measured the Acceptance fixture through the row model and guarded it with an exact invariant rather than a duration. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran each one independently at `b8a918a1`.

TRANSPORT COVERS THE EMISSION: the reviewer's own scratch original `.remedy-wt/f256-r7-block.md` predates the worker, and the committed `.agent/authored/f256-r7.md` blob at `029f4119` is BYTE EQUAL to it at 28746 bytes, sha256 `f4a0bae315e3514acc14eb85a606ea6c95a49cc0c4c3ee079359da678d3477f4`. `.agent/plan.md` at `68d945ba` is byte-equal to its slice at 37 lines. At `7ae7400c` the two appends reconstruct byte for byte — `.agent/live_review.md` from the base blob plus a newline plus GATEF256R6, and `.agent/decisions.md` from the base blob plus a newline plus DECF256D5 plus a newline plus DECF256D6 — each pre-round blob is a byte PREFIX, each negative control is REJECTED, and `## DECISION F256 D5` and `## DECISION F256 D6` occur exactly once each with D5 before D6. The ledger moved as a round that registers and resolves nothing should: registrations 293 and all DISTINCT, `^Done:` 43, `^Landed:` 11, the OPEN SET as a set 252, and `^Gate: F\d+ R\d+ — ` alone rising by one to 103, with `Gate: F256 R6` occurring exactly once.

THE EXACT FIGURES AGREE AND THE DURATIONS DO NOT, WHICH IS WHAT DECISION F256 D5 PREDICTS. Re-running the module at `b8a918a1` the reviewer measured 10,002 rows built, 48 rows drawn at 10,002 and 48 at 100,020, a default-collapsed set of size 1 and a first paint of 2 rows — every one identical to the figures the test's comments record. The durations came out 0.826 ms median against the recorded 0.678 ms, with a minimum of 0.323 ms and a maximum of 1.767 ms against 0.271 ms and 1.408 ms. That is the fivefold intra-run spread D5 measured, and it is exactly why the assertions are on the invariant and not on the time.

THE RED-PROOF PROVES THE NEW GUARD AND NOT MERELY THE FILE. In a disposable worktree at `95ecaf14`, run through DECISION F256 D6's route: control 93 passed; gutting `buildDiffRowModels` to return an empty array turned 10 tests RED; changing the unmeasured-viewport fallback from `DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS` to `totalRows` turned 3 tests RED, among them the new `draws the SAME bounded window at ten times the Acceptance size`, and the printed line under that mutation reads `10002 drawn@10002 100020 drawn@100020` — the window really did start following the document, which is the single failure that assertion exists to catch. The control passed 93 again and the primary checkout read `git status --porcelain` EMPTY throughout, which is the property `cacheDir` is in D6 for.

RE-RUN IN THE PRIMARY CHECKOUT, each exit 0 and each equal to the handback's figure: `npx vitest run` 631 passed in 33 files against 628 at the base, `npx tsc --noEmit` clean, `tests/orchestration/test_test_runner.py` 52 passed in 5.5 s against its 30-second timeout, `tests/ui_contracts/` 664 passed with 4 skipped, `tests/ui_server/` 497 passed, and the canary `tests/cli/test_golden_path.py` 42 passed. The change set is six paths with both residues empty, every commit single-parent and under 500 insertions, C3 is +189 / −0 so no existing assertion moved, and NO file under `packages/`, `docs/` or `apps/ui/src/api/diffViewModel.ts` changed by a byte. The branch tip equals `origin/feature/f256-diff-viewer-completion`, the primary checkout is clean, and `gh pr list --state open` is `[]`.

TWO DECLARED DEVIATIONS ARE ACCEPTED AND ONE OF THEM IS THE REVIEWER'S OWN FAULT. The worker reported that its first G4(b) spelling compared blank-line units unstripped and returned `False` for both files, re-measured stripped, got `True` at N of 7 and 16, and reported BOTH readings; the reviewer's independent stripped comparison agrees, and nothing on disk was ever wrong. The worker also reported that the block quoted the mutation anchor inside a four-space-indented code block, so the printed line carried eight leading spaces where the file on disk carries four; it asserted uniqueness on the correct four-space form and declared the difference. That is a reviewer prose slip, it damaged nothing on disk, and it is recorded in `.agent/prose_slips.md` this round under operator amendment amend0827 rule 2 rather than spending an id.
<<<END GATEF256R7

<<<SLICE SLIPF256R7
2026-08-28 · F256 R7 · The block's G7 mutation (ii) quoted its anchor inside a four-space-indented code block, so the line it displayed carried eight leading spaces where `apps/ui/src/api/diffViewModel.ts` carries four; the worker asserted uniqueness on the correct four-space form, applied it and declared the difference, so nothing on disk was affected.
<<<END SLIPF256R7

<<<SLICE BUILTF256
## Built State (F256, 2026-08-28)

What exists on disk at the close of F256, so a later reader need not reconstruct
it from the roadmap's future tense. This section is what the Acceptance bullet
"the numbers are written into this file's Built State section — a recorded
measurement, not a claim" asks for.

**T001 — the highlighting, RENDERED and not merely modelled.**
`apps/ui/src/api/diffHighlight.ts` carries the per-line highlight model and
`apps/ui/src/api/diffHighlightGrammars.ts` carries the grammar tables, split into
their own module so `DiffView.tsx` reaches them by a dynamic `import(` alone and
they leave the main bundle — the repair of finding `R-0732`, measured at the time
as a separate emitted chunk. `DiffView.tsx` wires `loadDiffLanguageBundle` and
maps the four coloured token kinds to the four `.tok*` rules of
`DiffView.module.css`, which DECISION F256 D2 rules from custom properties the
shipped token sheet already defines; a fifth kind, `plain`, is deliberately given
no rule and no class, so an unknown language and a not-yet-arrived answer both
render exactly as the viewer rendered them before F256. DECISION F256 D1 records
why Remedy writes its own bundles rather than adding a third-party highlighter.
Tests: `apps/ui/src/api/diffHighlight.test.ts`,
`apps/ui/src/api/diffViewModel.test.ts`,
`tests/ui_contracts/test_diff_view_render.py` and
`tests/ui_contracts/test_diff_surface_css.py`.

**T002 — the 10k-line fixture, MEASURED end to end, with the numbers.** All
figures below were measured on 2026-08-28 on the machine this feature was built
on — a Linux x86-64 development workstation, CPython 3 and Node v22, unloaded —
and every one of them was re-measured independently by the reviewer at review
time. The exact figures agreed on every re-run; the durations moved by the
ordinary run-to-run spread, which is recorded here rather than hidden.

The PARSER, recorded in
`tests/orchestration/test_diff_parser.py::test_the_huge_diff_parses_inside_the_recorded_perf_budget`:
a median of 0.105 s for 10,000 body lines, against 0.010 s at 1,000 and 0.021 s
at 2,000 — linear at roughly ten microseconds per body line — held under a
generous absolute ceiling of 0.5 s that sits between the linear case and where a
quadratic parser would land.

The SERVER PATH end to end, recorded in
`tests/ui_server/test_diff_endpoint.py::TestDiffEndpointPerfBudget`: a 10,000
body-line `workspace.diff` on disk, served over real HTTP through `ui_server`,
answered in a median of 0.1331 s over five requests, minimum 0.1282 s, maximum
0.1489 s, for a serialised JSON response of 1,045,960 bytes. The envelope arrives
whole — `available` true, `truncated` false, one file, 10,000 body lines — because
`DIFF_VIEW_MAX_BODY_LINES` is 20,000 and the fixture is asserted strictly below
it. The parse is about nine tenths of that cost and everything composed around it
is the rest. What is ASSERTED is not the duration but the SHAPE: the same route
measured at 1,000 and at 10,000 body lines answered at a ratio of 4.97, against a
ceiling of 20 that DECISION F256 D4 rules and derives. A ratio taken on one
machine in one run divides every constant factor out, so the guard cannot become
a report on machine speed.

The CLIENT MODEL, recorded in `apps/ui/src/api/diffViewModel.test.ts` under
"the ten-thousand-line diff through the client model": building every row of the
same fixture took a median of 0.678 ms over seven builds, minimum 0.271 ms,
maximum 1.408 ms, producing 10,002 rows. What is ASSERTED here is an exact
invariant rather than a duration, because the fastest and slowest samples inside
one run differ more than fivefold and a bound on that would report the JIT:
the virtual-scroll window draws 48 rows at 10,002 and the SAME 48 at 100,020, so
the drawn row count does not follow the document. DECISION F256 D5 records that
choice and the measurements behind it. Two facts are pinned beside it because
both are easy to get wrong: a hunk of 10,000 lines arrives COLLAPSED, so the
viewer's first paint of the Acceptance fixture is TWO rows and the ten thousand
appear only when the reader expands it; and a benchmark built with the default
collapsed set therefore measures two rows however large the fixture is.

DECISION F256 D6 records how a vitest test in this repository is red-proved at
all, since `git worktree` carries no `node_modules`: the mutation lives in the
worktree, vitest runs from the primary `apps/ui`, and `cacheDir` is redirected so
the primary checkout stays clean.

**T003 — the file sidebar's visual treatment, RULED.** DECISION F256 D3 ends the
deferral `DiffFileSidebar.tsx` carried in its own header since F037 and derives
the treatment from the diff body's own vocabulary rather than inventing one:
`.filePath` takes the mono family with ligatures off, `.fileMeta` takes the same
de-emphasis the sheet already gives the line-number gutter, and `.statAdd` and
`.statDel` take the product's own green and orange — the two hues the added and
removed rows are already tinted with. No new hue and no new custom property
entered the product, and `apps/ui/src/styles/tokens.css` is unchanged. Remedy
deliberately does NOT draw a proportional stats bar here: the two counts carry
the magnitude exactly rather than approximately, and a bar would need a track, a
fill, a minimum width and a pure-deletion rule that no authority in this
repository defines. Tests:
`tests/ui_contracts/test_diff_file_sidebar.py`, whose
`TestTheSidebarWearsTheRuledTreatment` fails any class the component names
without a rule behind it.
<<<END BUILTF256

`PLANF256R8` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF256R7`,
`SLIPF256R7` and `BUILTF256` are APPENDS to `.agent/live_review.md`,
`.agent/prose_slips.md` and `docs/roadmap/features/T5_F256.md`. For each, append
exactly what gate G4 and gate G6 measure — the pre-round blob, one newline, then
the slice — whatever blank lines that file already ends with.

### Done when

G1 HYGIENE AND STRUCTURE. Read `.agent/STOP` with `os.path.exists` before C0a and
again before C3; report both, and stop after the commit in hand if it exists.
Report `git rev-parse HEAD` before C0a — it must equal `b8a918a1` —
`git branch --show-current`, and `git status --porcelain | wc -l` after each of
C0a, C0b, C1, C2 and C3. Then, over `b8a918a1..<C3>` — the range ending BEFORE the
handback commit, so `.agent/handoff.md` is expected in the change set but not in
this range — report `git diff --name-only` and both residues against the change
set with `.agent/handoff.md` set aside, printed in both directions and both
expected empty. Report each commit's insertions from `git diff --numstat`, each
under 500, and that each of C0a, C0b, C1, C2 and C3 is single-parent. Report the
counts of lines beginning `<<<SLICE ` and `<<<END ` in every target other than
`.agent/authored/f256-r8.md` and `.agent/last_block.md` — each expected 0 — beside
those two as the non-zero control. Report `git ls-files .remedy-wt | wc -l`,
expected 0. Report `git diff --name-only b8a918a1..HEAD -- apps/ packages/ tests/
docs/roadmap/STATUS.md docs/roadmap/ROADMAP.md`, expected EMPTY.

G2 TRANSPORT. One digest comparison: sha256 of
`git show <C0a>:.agent/authored/f256-r8.md` against the reviewer's own original at
`.remedy-wt/f256-r8-block.md`, reporting both digests, the byte length and
equality; that original predates this worker, so say the reading covers more than
self-consistency. Report that `<C0b>:.agent/authored/f256-r8.md` and
`<C0b>:.agent/last_block.md` are ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF256R8 including the trailing
newline — report `True` or `False` — with `wc -l` under 50 and the counts of lines
exactly `## Goal` and exactly `## Next Steps`.

G4 THE RECORD AT C2, two readers per appended file. (a) The `b8a918a1` blob plus a
newline plus the slice equals the C2 blob, reported separately for
`.agent/live_review.md` with GATEF256R7 and `.agent/prose_slips.md` with
SLIPF256R7; NEGATIVE CONTROL for each, flipping one byte at an offset your script
confirms lies INSIDE THE FIRST appended paragraph and reporting the equality now
`False`. (b) Let N be each slice's paragraph count, COUNTED BY YOUR SCRIPT from
the slice and never taken from this block, ignoring an empty trailing unit; report
N and that the LAST N blank-line units of each file match those paragraphs IN
ORDER. Report each pre-round blob is a byte PREFIX. Report that
`.agent/prose_slips.md` gained exactly ONE line matching `^\d{4}-\d{2}-\d{2} · F`
and that no existing such line changed.

G5 THE LEDGER AT C2. Over the C2 blob and the `b8a918a1` blob beside it, report
`^- R-\d+ — ` and whether all DISTINCT, `^Done: R-\d+ — `, `^Landed: R-`,
`^Gate: F\d+ R\d+ — `, and the OPEN SET as a set. This round registers and
resolves nothing, so every figure is UNMOVED except `^Gate: F\d+ R\d+ — `, which
rises by exactly ONE. Report that `Gate: F256 R7` occurs exactly 1 time.

G6 THE BUILT STATE AT C3, and its CROSS-CHECK, which is the gate this round
exists for. First: the `b8a918a1` blob of `docs/roadmap/features/T5_F256.md` plus
a newline plus BUILTF256 equals the C3 blob — report `True` or `False` — the
pre-round blob is a byte PREFIX, and `## Built State` occurs exactly once in the
result. Then the CROSS-CHECK: for each figure below, report the count of that
literal in the C3 blob of the feature file AND in the file named beside it, and
that BOTH are at least 1. A recorded number that is not in the file that produced
it is a false record, and constraint 8 tells you what to do about it.

- `0.1331`, `0.1282`, `0.1489`, `1,045,960` and `4.97` in
  `tests/ui_server/test_diff_endpoint.py`
- `0.678`, `0.271`, `1.408`, `10,002`, `100,020` in
  `apps/ui/src/api/diffViewModel.test.ts`
- `0.105` in `tests/orchestration/test_diff_parser.py`
- `.filePath`, `.fileMeta`, `.statAdd`, `.statDel` in
  `apps/ui/src/components/diff/DiffView.module.css`

Additionally report that `DIFF_VIEW_MAX_BODY_LINES` really is 20,000 in
`packages/orchestration/diff_parser.py`, that
`DIFF_ENDPOINT_SCALE_RATIO_CEILING` really is 20 and
`HUGE_DIFF_PARSE_CEILING_SECONDS` really is 0.5, and that
`apps/ui/src/api/diffHighlightGrammars.ts` and
`apps/ui/src/api/diffHighlight.test.ts` both EXIST — every one of these is a
claim the slice makes in prose.

G7 THE SUITES AT C3. One pytest process at a time, from the repository root, each
with its exit code and its own passed/failed line: `tests/docs/` in full — this
round edits a documentation file, so that suite is the one most likely to have an
opinion about it; `tests/ui_contracts/`; `tests/ui_server/`;
`tests/orchestration/test_diff_parser.py`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. If any is red, STOP and
write the handback with the FULL untruncated failure list.

### Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md. It
carries: `SESSION 2 of feature F256 · round 8`; the range `b8a918a1..HEAD`; a
per-commit changed-files table with `+/-` from `git diff --numstat` compared cell
by cell against G1's figures; ONE LINE PER GATE G1 through G7 with its real
result; the deviations, including every guard re-expression constraint 6 required;
the item-status table with every C-item and every gate appearing exactly once; and
the next expected action, which is the integration gate over the whole branch,
followed by the two-round closure sequence.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — only
reviewer-authored text sets those. GATEF256R7 above is reviewer-authored and
applied as a slice, which is not the same thing.

After C4: push with `git push -u origin feature/f256-diff-viewer-completion` and
report the outcome. Do NOT create a pull request and do NOT merge anything.
