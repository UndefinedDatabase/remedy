### STEP T001b — F256 Diff viewer completion, round 2

Goal: book the R1 verdict into the record, then compose the TOKEN cut with the
INTRALINE cut in the model layer, so one changed line can carry word-level
emphasis and syntax colour at once without either losing a character.

Base: `7b23c46a`, the tip of `feature/f256-diff-viewer-completion`. Every
reading below was taken there.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f256-r2.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 append the R1 verdict to `.agent/live_review.md` and the slips to
  `.agent/prose_slips.md`
- C3 the composition and its vitest tests
- C4 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f256-r2.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/prose_slips.md`
- `apps/ui/src/api/diffHighlight.ts`
- `apps/ui/src/api/diffHighlight.test.ts`
- `.agent/handoff.md`

`.agent/plan.md` is advanced BEFORE the record commit, which is the order
docs/agents/planner_reviewer_prompt.md §3 item 23 requires of any round that
touches the finding ledger.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName`.
   It was `[]` when this block was written. Do NOT create or merge a pull
   request this round. Stay on `feature/f256-diff-viewer-completion`; do not
   branch, and never work on `main`.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations; the record is repaired by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f256-r2.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under
   the gitignored `.remedy-wt/`. The primary checkout satisfies
   `git status --porcelain` empty at every commit.
6. Shell forms rejected by this session's guard are RE-EXPRESSED, never skipped
   and never weakened. Route such work through `python3 - <<'PY'`, and report
   every re-expression in the handback.
7. `apps/ui/src/api/diffHighlight.ts` is swept by repo-wide guards that name no
   diff path and would still fail on it. Measured at `7b23c46a`:
   `tests/ui_contracts/test_brain_stream_ring.py` forbids `EventSource` and
   counts `useBrainStream(` across every non-test `.ts`/`.tsx` under
   `apps/ui/src`; `tests/ui_contracts/test_ux_quality.py` forbids the substring
   `scanline`; `tests/ui_contracts/test_cost_metric_render.py` requires that no
   file but `apps/ui/src/api/costMetric.ts` contains `spent_usd`,
   `spent_tokens`, `limit_usd` or `limit_tokens`.
8. This round adds NO CSS and edits NO component. `DiffView.tsx`,
   `DiffView.module.css` and `DiffFileSidebar.tsx` are untouched, and
   `apps/ui/src/api/diffViewModel.ts` is NOT edited either.
9. `apps/ui/src/api/diffHighlight.ts` keeps the property its own header comment
   states at `7b23c46a`: it imports NOTHING at runtime. The new function
   therefore takes the intraline segments as an ARGUMENT rather than importing
   `splitLineIntoIntralineSegments`, and any type it needs from the model is
   declared structurally in this module.

### SPEC — the production code of C3

Production code is DESCRIBED here, not sliced: write it in this repository's
idiom, with the one-line WHY comment above each definition that AGENTS.md's
discoverability conventions ask for.

S1. In `apps/ui/src/api/diffHighlight.ts`, export
`interface DiffHighlightRun { text: string; marked: boolean; kind:
DiffHighlightTokenKind }` — one run of a line that is uniform in BOTH
dimensions.

S2. Export `interface DiffMarkedSegment { text: string; marked: boolean }`, the
structural shape `splitLineIntoIntralineSegments` in
`apps/ui/src/api/diffViewModel.ts` already returns at `7b23c46a`. Declaring it
structurally is what keeps constraint 9 true; the WHY comment says so and names
that function as the producer.

S3. Export `composeHighlightedRuns(segments: readonly DiffMarkedSegment[],
language: string | null): readonly DiffHighlightRun[]`.

S4. TOTAL. No input throws, for any segment list and any language id. An empty
list, and a list whose texts are all empty, both yield the EMPTY ARRAY — there
is no run to describe and a run carrying the empty string would render an
element around nothing, which is the same ruling
`splitLineIntoIntralineSegments` makes for empty content at `7b23c46a`.

S5. THE COMPOSITION. Join the segments' `text` in order to recover the line,
tokenize that ONCE with `tokenizeDiffLine`, and cut at every boundary of EITHER
partition. Build it from per-character maps rather than by merging two run
lists, for the reason `splitLineIntoIntralineSegments` gives for its own
coverage map at `7b23c46a`: a character can then be neither dropped nor emitted
twice however the two cuts interleave.

S6. THE LOAD-BEARING INVARIANTS, each of which the vitest suite pins
separately:
 (a) joining the returned runs' `text` reproduces the joined input exactly;
 (b) for every character position, the run covering it carries the SAME
     `marked` as the input segment covering it;
 (c) for every character position, the run covering it carries the SAME `kind`
     as the segment `tokenizeDiffLine` gives that position for the same
     language.

S7. Adjacent runs are MERGED when they agree on BOTH `marked` and `kind`, so no
two consecutive runs share both, and a renderer draws one element per visible
run.

S8. Extend `apps/ui/src/api/diffHighlight.test.ts` — do not create a second test
file. It pins, each as its own test: S6 (a), (b) and (c) over a table that
includes a marked run falling INSIDE a token, a token falling inside a marked
run, and boundaries that cross at an offset belonging to neither cut; the S7
merge rule; the S4 empty cases; and totality over an unknown language, where
every run must come back `plain` while the `marked` flags still survive
unchanged.

### The authored slices

<<<SLICE PLANF256R2
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
| claim F256 and retarget the state | done | `d4c00438` |
| the per-line highlight model | done | `apps/ui/src/api/diffHighlight.ts` |
| compose the token cut with the intraline cut | done | this round |
| lazy bundles, DiffView wiring, the palette | open | the composition is its input |
| rule on the sidebar's treatment | open | a ruling to record, not code |
| measure the 10k-line fixture | open | needs a real fixture and a real run |

## Next Steps
1. Ship the lazy per-language bundles and wire `loadDiffLanguageBundle` into
   `DiffView`, rendering one element per composed run, with a palette derived
   from custom properties already defined under `apps/ui/src` rather than
   invented.
2. Rule on the file sidebar's visual treatment and record the authority.
3. Measure the 10k-line fixture end to end and record the numbers in the
   feature file's Built State.

## Risks
- The palette may name only custom properties defined under `apps/ui/src`;
  `tests/ui_contracts/test_design_drift.py` fails any that is not.
- Wiring `DiffView` changes a file gated by
  `tests/ui_contracts/test_diff_view_render.py`, which reads its
  comment-stripped source and requires every class it names to have a rule in
  `DiffView.module.css`.
<<<END PLANF256R2

<<<SLICE GATEF256R1
Gate: F256 R1 — the CLAIM round, and the first round of F256. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran each independently at `7b23c46a` rather than reading the handback's numbers.

TRANSPORT IS PROVED AT ITS STRONGEST AVAILABLE LINK, and the distinction matters because docs/agents/planner_reviewer_prompt.md §3 item 37 records that this workflow's usual chain proves only the worker's self-consistency. The reviewer's own scratch original `.remedy-wt/f256-r1-block.md` was written BEFORE the worker existed and is not the worker's output, and the committed `.agent/authored/f256-r1.md` blob at `6f5916bb` is BYTE EQUAL to it at 21445 bytes, sha256 `270fb5dade65ca8e2e7ace8888c6755205c4d25fbca0d80313efabb716ef68fc`. So this reading covers the EMISSION. At `5b3c02a0` the authored path and `.agent/last_block.md` are ONE blob `111985b6be13`.

THE RECORD AND THE CLAIM WERE RE-MEASURED BY THE REVIEWER, not accepted. The `0e8ab5b4` blob of `.agent/decisions.md` plus a newline plus the DECF256R1 slice equals the `9c05aea3` blob exactly, the pre-round blob is a byte PREFIX of it at 687668 bytes growing to 689972, and a byte flipped inside the FIRST appended paragraph is REJECTED. Over `docs/roadmap/STATUS.md` at `d4c00438` the retired `[ ]` line occurs 0 times, the claimed `[~]` line occurs exactly 1 time as a WHOLE LINE, lines matching `^- \[~\] F\d{3} — ` number 1 — which is what `tests/docs/test_docs_consistency.py` bounds at most one — and lines matching `^- \[x\] F\d{3} — ` are UNMOVED at 60.

THE SHIPPED FUNCTION WAS RUN BY THE REVIEWER ON INPUTS THE ROUND NEVER TRIED, which is the half of a verdict that a re-read of the diff cannot supply. In a disposable worktree at `6581eec4`, driven by the DECISION F037 D10 recipe: every VALUE of `DIFF_SUPPORTED_LANGUAGES` in `apps/ui/src/api/diffViewModel.ts` is an own key of `DIFF_HIGHLIGHT_GRAMMARS`, the uncovered set printing empty, so no supported language silently renders plain; and over 4000 generated lines built from an alphabet of quotes, backslashes, comment openers, digits and braces, scanned against every declared grammar, the S7 concatenation invariant held with ZERO violations and the merge rule produced no two adjacent `plain` runs. The worktree was removed and the primary checkout reads `git status --porcelain` empty.

THE SUITES WERE RE-RUN IN THE PRIMARY CHECKOUT, one pytest process at a time, each exit 0 and each equal to the handback's figure: `tests/orchestration/test_test_runner.py` 52 passed, `tests/docs/` 295 passed, `tests/orchestration/test_roadmap_index.py` 30 passed, `tests/ui_contracts/test_diff_view_model.py` with `tests/ui_contracts/test_diff_view_render.py` 27 passed, and the canary `tests/cli/test_golden_path.py` 42 passed. THE STRUCTURE IS CLEAN: the path set over `0e8ab5b4..7b23c46a` is exactly the nine files the handback names, insertions per commit are 400, 379, 87, 1, 398 and 219 — each under 500 — every commit is single-parent, `.agent/live_review.md` is untouched by the range, and the committed handback carries no line beginning with either reviewer-only verdict marker. `git rev-parse` of the branch tip equals `origin/feature/f256-diff-viewer-completion`, so the push landed, and `gh pr list --state open` is `[]`.

THREE SLIPS ARE RECORDED IN `.agent/prose_slips.md` RATHER THAN AS FINDINGS, under operator amendment amend0827-process-diet rule 2, because each is reviewer prose that left nothing wrong on disk under `packages/`, `apps/`, `tests/` or `docs/`. All three are the reviewer's own, not the worker's, and the worker declared two of them unprompted — which is the round catching the block, and is why they are cheap.
<<<END GATEF256R1

<<<SLICE SLIPSF256R1
2026-08-28 · F256 R1 · The PLANF256R1 slice's Current Step table read `the per-line highlight model | done` at C1, where the slice lands and the model does not yet exist; it became true at C3 within the same round. The worker applied it byte for byte per constraint 1 and declared it.
2026-08-28 · F256 R1 · The block listed `.agent/handoff.md` in its change set while fixing G8's range to end at C3, which cannot reach the commit that writes the handback; the worker reported both readings rather than the convenient one.
2026-08-28 · F256 R1 · The G4 reader (b) counted N as 7 blank-line units where the DECF256R1 slice holds 6 paragraphs plus an empty trailing unit; the comparison still covered the whole appended region, so the obligation of §3 item 36 was met.
<<<END SLIPSF256R1

`PLANF256R2` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF256R1` is an
APPEND to `.agent/live_review.md`, separated from the existing final line by
exactly one blank line. `SLIPSF256R1` is an APPEND to `.agent/prose_slips.md`,
separated the same way; that file is append-only and is never rewritten.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C3; report both answers. If it exists at either reading, finish the
commit in hand, write the handback and stop. Report `git rev-parse HEAD` before
C0a — it must equal `7b23c46a` — `git branch --show-current`, and
`git status --porcelain | wc -l` after each of C0a, C0b, C1, C2 and C3.

G2 TRANSPORT. One digest comparison. Compute sha256 of the committed blob
`git show <C0a>:.agent/authored/f256-r2.md` and of the reviewer's own original
at `.remedy-wt/f256-r2-block.md`, and report both digests, the byte length and
whether they are equal. That original was written before this worker existed, so
the reading covers more than self-consistency; say so. Then report that
`git rev-parse <C0b>:.agent/authored/f256-r2.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. Byte-equality only: `.agent/plan.md` at C1 equals PLANF256R2
including the trailing newline — report `True` or `False`. Report `wc -l`, which
must be under 50 (AGENTS.md), and the count of lines exactly `## Goal` and
exactly `## Next Steps`.

G4 THE RECORD AT C2, two readers, for each of the two appended files
separately. (a) The `7b23c46a` blob, plus a newline, plus the slice equals the
C2 blob — report `True` or `False` for `.agent/live_review.md` with GATEF256R1
and for `.agent/prose_slips.md` with SLIPSF256R1. NEGATIVE CONTROL for each:
flip one byte at an offset your script confirms lies INSIDE THE FIRST appended
paragraph, recompute, and report that the equality is now `False`. (b) Split
each C2 blob on blank lines; let N be the number of paragraphs in that file's
slice, COUNTED BY YOUR SCRIPT from the slice itself and never taken from this
block, ignoring any empty trailing unit; report N, and report that the LAST N
units match those paragraphs IN ORDER, unit by unit. Report that each pre-round
blob is a byte PREFIX of its C2 blob, with both byte lengths.

G5 THE LEDGER AT C2. Report over the C2 blob of `.agent/live_review.md`: the
count of lines matching `^- R-\d+ — ` and whether they are all DISTINCT; the
count of `^Done: R-\d+ — `; the count of `^Landed: R-`; the count of
`^Gate: F\d+ R\d+ — `; and the OPEN SET computed AS A SET. Report each of the
same figures over the `7b23c46a` blob beside it. This round registers no finding
and resolves none, so every figure must be UNMOVED except
`^Gate: F\d+ R\d+ — `, which rises by exactly ONE. Report that
`Gate: F256 R1` occurs exactly 1 time in the C2 blob.

G6 THE COMPOSITION RED-PROOF AT C3, in a disposable worktree, following
DECISION F037 D10 and never in the primary checkout. Report the UNMUTATED
CONTROL FIRST in that same worktree — a control with no baseline is not evidence
— then each mutation, reporting exit code and passed/failed counts for every
run. Drive it from `python3`, with

    ["npx", "vitest", "run", "--root", f"{WT}/apps/ui",
     "--config", f"{PRIMARY}/apps/ui/vitest.config.ts",
     "src/api/", "--reporter=basic"], cwd=f"{PRIMARY}/apps/ui"

Both flags are load-bearing and the run is SCOPED to `src/api/`. THE MUTATIONS,
each applied alone and reverted before the next, each in
`apps/ui/src/api/diffHighlight.ts` inside the worktree, and each of which must
turn the suite RED: (i) break S6(b) by giving every emitted run `marked: false`;
(ii) break S6(c) by giving every emitted run the kind `plain`; (iii) break S7 by
emitting runs unmerged. Report the control again, green, with every file
restored. Report `git worktree list` and `git status --porcelain | wc -l` in the
primary after removal.

G7 THE SUITES AT C3. One pytest process at a time, from the repository root, in
the PRIMARY checkout, each with its exit code and its own passed/failed line.
`tests/orchestration/test_test_runner.py` (it spawns `npx vitest run` under a
30-second timeout, so report the wall clock too); the state readers
`tests/ui_server/`, `tests/regression/test_resource_safety.py` and
`tests/orchestration/test_integrity_gate.py`; the sweeps constraint 7 names,
`tests/ui_contracts/test_brain_stream_ring.py`,
`tests/ui_contracts/test_cost_metric_render.py` and
`tests/ui_contracts/test_ux_quality.py`; the diff contracts
`tests/ui_contracts/test_diff_view_model.py` and
`tests/ui_contracts/test_diff_view_render.py`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. If any is red, STOP
and write the handback with the full untruncated failure list.

G8 STRUCTURE, over `7b23c46a..<C3>` — the range that ends BEFORE the handback
commit, because C4's own numbers cannot exist while C4 is being written, and
`.agent/handoff.md` is therefore expected in the change set but NOT in this
range. Report `git diff --name-only` and both residues against the change set
above with `.agent/handoff.md` set aside, printed in both directions and both
expected empty. Report each commit's insertions from `git diff --numstat`, each
under 500, and that each of C0a, C0b, C1, C2 and C3 is single-parent. Report,
counted affirmatively over each file's C3 content, the number of lines beginning
`<<<SLICE ` and `<<<END ` in `.agent/plan.md`, `.agent/live_review.md`,
`.agent/prose_slips.md`, `apps/ui/src/api/diffHighlight.ts` and
`apps/ui/src/api/diffHighlight.test.ts` — each expected 0 — beside the same
counts over `.agent/authored/f256-r2.md` as the non-zero control. Report
`git ls-files .remedy-wt | wc -l`, expected 0.

### Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md. It
carries: `SESSION 1 of feature F256 · round 2`; the range `7b23c46a..HEAD`; a
per-commit changed-files table with the `+/-` cells taken from
`git diff --numstat` and compared cell by cell against the figures G8 reports;
ONE LINE PER GATE G1 through G8 with its real result; the deviations, including
every guard re-expression constraint 6 required; the item-status table with
every C-item and every gate appearing exactly once; and the next expected
action.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — only
reviewer-authored text sets those. GATEF256R1 above is reviewer-authored and is
applied as a slice, which is not the same thing.

After C4: push with `git push -u origin feature/f256-diff-viewer-completion` and
report the outcome. Do NOT create a pull request and do NOT merge anything.
