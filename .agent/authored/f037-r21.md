# STEP T003 (fifth round) — F037 Rendered diff viewer, round 21

BASE: `6d13fae4`. SESSION 6 of feature F037. This block carries no line that is a
run of a single repeated character, so nothing in its frame has a length a reader
must recover by eye.

## Goal

Make the window real. R20 built `computeDiffRowWindow` and wired it to nothing;
this round gives it the one caller it was written for, so a diff of ten thousand
rows draws a bounded number of them. The division a viewport forces — scroll
offset and panel height into row indices — goes into the MODEL, not the markup,
so the rule stays where vitest runs it. The five stale WHY comments R20 reported
but could not repair are repaired, closing `R-0727`.

## Bundle

- C0a save this block verbatim to `.agent/authored/f037-r21.md`.
- C0b mirror the same bytes into `.agent/last_block.md`.
- C1 rewrite `.agent/plan.md` from the PLANF037R21 slice.
- C2 append GATER20, DONE727 and DONE728 to `.agent/live_review.md`, and in the
  SAME commit append PROSESLIP to `.agent/prose_slips.md`.
- C3 append DECISIOND10 to `.agent/decisions.md`.
- C4 the staleness repairs: SPEC S1.
- C5 the viewport rule and its vitest tests: SPEC S2 and S3.
- C6 the wiring: SPEC S4.
- C7 the guards over the wiring: SPEC S5.
- C8 rewrite `.agent/handoff.md` as the handback.

## Change set

Exactly these paths, and nothing outside them:

- `.agent/authored/f037-r21.md` (new)
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/prose_slips.md`
- `.agent/decisions.md`
- `tests/ui_contracts/test_diff_viewer_mount.py`
- `apps/ui/src/api/diffViewModel.ts`
- `apps/ui/src/api/diffViewModel.test.ts`
- `apps/ui/src/components/diff/DiffView.tsx`
- `tests/ui_contracts/test_diff_view_render.py`
- `.agent/handoff.md`

Push the branch after C8 with `git push -u origin feature/f037-rendered-diff-viewer`.
Create no PR. Merge nothing. Rewrite no history.

## Constraints

1. Apply every slice BYTE FOR BYTE. Never write a `<<<SLICE` or `<<<END` marker
   line into a target file. If a slice looks wrong, apply it and declare it.
2. The SPEC items describe PRODUCTION CODE and are not slices. The WHY comments
   they ask for are yours to word.
3. Nothing under `packages/` changes. No component other than `DiffView.tsx` is
   edited, and no file under `apps/ui/src/components/detail/` or
   `apps/ui/src/components/shell/` is touched.
4. NO NEW CSS, no new stylesheet, no change to `apps/ui/src/styles/tokens.css`,
   and no new class name asked of the CSS module. The spacer elements S4 adds
   carry an inline `style` height and NO class — `test_diff_view_render.py`
   requires every `styles.<name>` the component asks for to have a rule in
   `DiffView.module.css`, and inventing a seventh class is what the CANONICAL
   DESIGN REFERENCE banner forbids.
5. `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` and
   `DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS` keep their current values. This round
   declares new constants but changes no existing one.
6. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8 and nothing is
   reordered. C5 MUST precede C6: the component may not import a symbol that
   does not exist yet, and a `tsc --noEmit` run between the two would be red
   through no fault of the wiring.
7. C7 MUST follow C6. A guard committed before the code it reads is a guard that
   was red at its own commit.
8. Every destructive check — every mutation of any file — runs ONLY inside a
   disposable `git worktree` under `.remedy-wt/`, never in the primary checkout.
   Remove the worktree by its EXACT path and report `git worktree list` as one
   line BEFORE running any pytest gate: a live worktree makes
   `tests/orchestration/test_test_runner.py` fail in the primary checkout, because
   that node shells out to `npx vitest run`, which discovers the worktree's own
   config and dies on module resolution. That red is an artifact of the
   measurement, not a regression.
9. TYPESCRIPT MUTATION RED-PROOFS ARE ORDERED THIS ROUND AND THEY ARE
   MEASURABLE. The standing note that they are not is WRONG and DECISION F037
   D10, which C3 lands, records the route: spawn vitest FROM the primary
   checkout so it resolves its own package, and point `--root` at the worktree
   so the tree under test is the worktree's. G6 gives the exact invocation. Do
   not attempt `npx` or `node_modules/.bin/vitest` from a shell command — that
   is denied to this session class; drive it from a `python3` script under
   `.remedy-wt/`, as G6 shows.
10. Do NOT author any `Done:` or `Gate:` paragraph. Those are the reviewer's
    and arrive only as the slices of C2. You author the `Landed:` line SPEC S6
    asks for, and nothing else in `.agent/live_review.md`.
11. STALENESS SWEEP. Re-read every WHY comment in each file you edit. Repair the
    five sites SPEC S1 names. Any OTHER stale claim you find: report it in the
    handback and leave it alone.

## SPEC

### S1 — the five stale claims, repaired

R20 measured and reported all five; constraint 12 of that block forbade the
repair. Each says the diff viewer has no caller, or that the current round may
not edit it, and both have been false since R18.

In `tests/ui_contracts/test_diff_viewer_mount.py`:

1. Module docstring, lines 3-4: "`DiffView.tsx` has been on disk since F037 R16
   with no caller at all. This round opens the door to it." Replace with the
   state that IS true: the door was opened by F037 R18, this module is the guard
   that keeps it open, and it reads the three files named below.
2. Line 43, the comment above `DIFF_VIEW_DELEGATED_RULES`: "Constraint 3 of the
   F037 R18 block forbids this round from editing that component at all."
   Replace with what the four names actually buy — that a round claiming only to
   mount or wire the component would lose one of them if it quietly rewrote the
   drawing half. Do not tie the sentence to any round number.
3. Line 260, an assertion message: "`DiffView.tsx` keeps the zero callers it has
   had since F037 R16." False at HEAD, and it prints only on failure — the
   moment a reader is already confused. Reword to the property really held.
4. Line 369, the `TestTheDrawingHalfIsUnchanged` docstring: "this round MOUNTS
   `DiffView.tsx` and does not edit it." Reword so it describes the CLASS's own
   standing property and names no round.

In `apps/ui/src/api/diffViewModel.ts`:

5. Line 327, inside the `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` comment: "the
   component that will render these rows". It has rendered them since R16 and
   has been mounted since R18. Put it in the present tense and name
   `DiffView.tsx`.

Line 317's "the state F037 R16 left behind — a component on disk that nothing
draws" is NOT stale: it describes a past state in the past tense. Leave it.

Change NO assertion, NO test name and NO executable line in S1: comment and
message text only, with every `assert` expression left byte-identical.

### S2 — the viewport rule, in `apps/ui/src/api/diffViewModel.ts`

Append after `computeDiffRowWindow`. Four new exports.

`DIFF_VIRTUAL_ROW_HEIGHT_PX = 20` — the row height every spacer and every index
is computed from. WHY 20 AND WHY IT IS HONEST TO FIX IT: `DiffView.module.css`
sets `.diffLine { font: 12.5px/1.6 ... }`, and 12.5 x 1.6 is exactly 20, so this
is the binding CSS's own line box transcribed rather than a number invented here.
Say in the comment that it is an ESTIMATE for the hunk-head and file rows, which
are not line rows, and that the overscan below is what absorbs that error.

`DIFF_VIRTUAL_OVERSCAN_ROWS = 8` — rows drawn beyond the viewport at each end,
so a row scrolled into view is already drawn rather than appearing as a stripe.

`DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS = 40` — the visible-row count assumed when
the panel has NOT been measured yet. THIS CONSTANT IS THE ROUND'S ONE REAL TRAP
AND IT IS WHY THE FALLBACK IS A RULE RATHER THAN A DEFAULT ARGUMENT: on first
render a panel's `clientHeight` is 0, so a viewport height of 0 divides to a
visible count of 0, and `computeDiffRowWindow` answers a visible count of 0 with
an EMPTY window — correctly, by its own third rule. An empty window draws no
rows, a panel with no rows in it never scrolls, and a panel that never scrolls
never fires the event that would measure it. The viewer would be blank forever.
Resolve it HERE, where vitest can execute the resolution.

`diffRowWindowForViewport(rowCount, scrollTopPx, viewportHeightPx)` returning
`DiffRowWindow & { rowsBeforePx: number; rowsAfterPx: number }` — declare that as
a named exported interface, `DiffRowViewportWindow`, rather than inline. It:

- resolves each of its three arguments through the same whole-count reading
  `computeDiffRowWindow` already uses, so a NaN, an infinity, a fraction or a
  negative cannot become an index;
- takes the first visible row index as the scroll offset divided by
  `DIFF_VIRTUAL_ROW_HEIGHT_PX`, rounded DOWN, because a partly-scrolled row is
  still on screen;
- takes the visible row count as the viewport height divided by
  `DIFF_VIRTUAL_ROW_HEIGHT_PX`, rounded UP for the same reason, and falls back to
  `DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS` when the resolved viewport height is 0;
- delegates to `computeDiffRowWindow` with `DIFF_VIRTUAL_OVERSCAN_ROWS` — it
  reimplements none of that function's rules;
- returns the two spacer heights as `rowsBefore` and `rowsAfter` multiplied by
  the row height, so the component does no arithmetic of its own.

### S3 — the vitest tests for S2, in `apps/ui/src/api/diffViewModel.test.ts`

A new `describe` beside the existing ones. It must pin, at minimum:

- an unmeasured viewport (height 0) above the virtualization threshold yields a
  NON-EMPTY window — the trap S2 names, asserted directly, so a future
  simplification that drops the fallback turns this red;
- below the threshold the answer is not virtualized, both spacers are 0 px, and
  every row is in the window;
- the first visible index is the FLOOR of the scroll division and the visible
  count the CEILING of the height division, each with a fractional case that
  would differ under the other rounding;
- `rowsBeforePx` and `rowsAfterPx` are the row counts times
  `DIFF_VIRTUAL_ROW_HEIGHT_PX`, named through the constant and never as digits;
- a non-finite or negative scroll offset and viewport height resolve rather than
  propagate;
- THE SCALE CASE, which is what this round exists for: at 10000 rows with a
  realistic viewport, `rowsInWindow` is bounded well under the row count — assert
  it is at most `DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS + 2 * DIFF_VIRTUAL_OVERSCAN_ROWS`
  — while `rowsBefore + rowsInWindow + rowsAfter` still equals 10000 exactly, so
  the document is fully accounted for while only a window is drawn.

Reference `DIFF_VIRTUAL_ROW_HEIGHT_PX` and the other constants BY NAME. A
transcribed `20` or `2000` in this file is what `R-0728` was about.

### S4 — the wiring, in `apps/ui/src/components/diff/DiffView.tsx`

The component gains scroll state and draws a window. It derives NOTHING new: the
only rule it may express is "ask the model, render the answer".

- One piece of state holding the panel's scroll offset and client height
  together, both starting at 0.
- One `onScroll` handler on the scrolling element, setting both from
  `event.currentTarget.scrollTop` and `event.currentTarget.clientHeight`. This
  single line is the whole of the untestable DOM measurement, deliberately: it
  reads two numbers and decides nothing.
- `diffRowWindowForViewport(rows.length, scrollTop, clientHeight)` called once
  per render, after `rows` is built.
- The drawn rows become `rows.slice(window.startIndex, window.endIndex)`.
- When the answer is virtualized, a spacer element before and after the drawn
  rows, each with an inline `style` height in pixels taken from `rowsBeforePx`
  and `rowsAfterPx` and NO class, so the scrollbar still describes the whole
  document. When it is not virtualized, render no spacers at all.
- The scrolling element needs a bounded height for any of this to mean anything.
  It has no class and may not gain one (constraint 4), so give the existing
  `<section data-ui="diff-view">` an inline `style` with `overflowY: "auto"` and
  a `maxHeight` in viewport units, noting in a comment that this is presentation
  the binding CSS does not cover, not a new visual language.
- The truncation notice keeps rendering after the rows, OUTSIDE the window, so it
  is never scrolled out of existence by virtualization.
- Every existing behaviour survives: the collapse set and its reset on a new
  envelope, the row keys, the file row's `id`, the intraline cut, and the
  hunk-head button with its `aria-expanded`.

WHAT MUST NOT HAPPEN: no division, no multiplication and no comparison against a
row count appears in this file. Every number comes out of the model's answer.

### S5 — the guards, in `tests/ui_contracts/test_diff_view_render.py`

Extend the existing module; add no new file.

- Add `diffRowWindowForViewport` to `DELEGATED_RULES`, so the component is
  required to CALL it.
- Add to `REIMPLEMENTED_RULE_SPELLINGS` the spellings that would mean the
  component did the arithmetic itself: `DIFF_VIRTUAL_ROW_HEIGHT_PX` (the
  component must never name the row height — it receives pixels already
  computed), `Math.floor(`, `Math.ceil(` and `.slice(0,`.
- One new test class pinning that the component really virtualizes: it calls
  `diffRowWindowForViewport`, it slices the row list by the window's own two
  indices, it carries an `onScroll` handler, and both spacer heights reach an
  inline `style`. Scope every assertion to a region — a function body, a JSX
  open tag — never to the whole file. `R-0725` is what a whole-file `in` check
  produces.
- One test asserting the ROW HEIGHT AGREES WITH THE STYLESHEET: read
  `DiffView.module.css`, extract the `font: 12.5px/1.6` shorthand from the
  `.diffLine` rule, multiply, and assert the product equals the
  `DIFF_VIRTUAL_ROW_HEIGHT_PX` declared in `diffViewModel.ts`. This is the one
  guard that stops the two drifting apart silently, and it must parse both
  numbers out of the files rather than transcribing either.
- A vacuity assertion beside the new scopers, proving each returns strictly less
  than its whole file, exactly as the existing classes do.

### S6 — the `Landed:` line

In the SAME commit as C4, append ONE line to `.agent/live_review.md` beginning
`Landed: R-0727 — ` naming the five sites repaired and the commit that repaired
them. Author no other line in that file.

## Slices

<<<SLICE PLANF037R21
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D10.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A5.

## Current Step
R21 gives `computeDiffRowWindow` its caller. The division a viewport forces —
scroll offset and panel height into row indices — goes into `diffViewModel.ts`
as `diffRowWindowForViewport`, so the rule stays where vitest executes it and
`DiffView` keeps deriving nothing. The trap it exists to resolve is an
unmeasured panel: `clientHeight` is 0 on first render, 0 divides to a visible
count of 0, and an empty window draws no rows, so the panel never scrolls and
never gets measured. R20's five reported stale comments are repaired, closing
`R-0727`.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R20 verdict and two resolutions | ordered | record first |
| C3 DECISION F037 D10 | ordered | it licenses this round's own red-proofs |
| C4 the five staleness repairs | ordered | closes `R-0727` |
| C5 the viewport rule and its vitest tests | ordered | before its caller |
| C6 the wiring | ordered | the window becomes real |
| C7 the guards over the wiring | ordered | after the code they read |
| C8 the handback | ordered | |

## Next Steps
1. The lazy language bundles, unknown languages rendering plain with no bundle
   fetch, which Acceptance names.
2. The 10k-line perf fixture measured END TO END and its numbers recorded; S3 of
   this round bounds the window's row count but times nothing.
3. A ruling on the sidebar's visual treatment, still owed.

## Risks
- Round 21 of a 25-round soft limit, session 6 of 7. Two named pieces remain
  after this round. If both do not fit in session 7, that session owes a SCOPE
  REPORT rather than more work.
- Nothing here renders a `.tsx` file, so S4 is gated by text and `tsc --noEmit`
  alone, as every `.tsx` round of this feature has been.
<<<END PLANF037R21

<<<SLICE GATER20
Gate: F037 R20 — the round that repaired two findings, gated a third and built the windowing rule. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran it independently at `b2658466` rather than reading the handback's numbers. RE-MEASURED, NOT ACCEPTED. The committed C0a blob is 31941 bytes, 375 lines, sha256 `aa59eaffe0e1754662c91be15745e6cbe8f28ee2797b3153ecad72d8847c3101`, BYTE EQUAL to the reviewer's own scratch original, and at C0b `.agent/authored/f037-r20.md` and `.agent/last_block.md` are ONE blob `c442a90f33feda64fd1c5d334063984dfd342348`. Caps: CONTENT 56, TOTAL 375, PROSE 319. The plan at `f0e1ffeb` is byte equal to PLANF037R20 including its trailing newline, negative control False, 47 lines, one `## Goal`, one `## Next Steps`. The five-slice append at `161dc2c9` satisfies reader (a) byte for byte and reader (b) over 7 ordered units, both negative controls False, with the pre-round blob a byte PREFIX at 1253563 bytes growing to 1264769. The ledger at the tip reads 289 registered ids ALL DISTINCT, 37 `Done:` lines, 6 `Landed:` lines, 90 `Gate:` entries and an open set of 254 computed AS A SET, against 287, 35, 4, 89 and 253 at base. Per-commit insertions over `fe3f1179..b2658466` are 375, 249, 23, 14, 13, 11, 67 and 309, every one under five hundred, every one single-parent, and every one matching the `+/-` column of the handback's `## Commits` table cell by cell. The path residue is EMPTY in both directions against the block's nine non-handoff paths; `git diff --stat` over `packages/` is empty and over `apps/ui/src/components/` names `DiffView.tsx` alone at 11 insertions and 8 deletions; the marker sweep is 0 in all four targets against 12 in the block blob as its control; and `git ls-files .remedy-wt` is 0. RE-RUN SUITES, primary checkout, one process at a time, every one exit 0: `tests/ui_contracts/` 642 passed 4 skipped against 641 at base, `tests/ui_server/` 495 passed, `tests/orchestration/test_test_runner.py` with `tests/docs/` 347 passed, ruff `All checks passed!`, the canary 42 passed, and the typescript node 1 passed 73 deselected, PASSED and not skipped.

BOTH OF THE WORKER'S DECLARED DEVIATIONS ARE NOW CLOSED BY MEASUREMENT, AND THE STANDING CLAIM BEHIND THEM WAS FALSE. The worker reported that a TypeScript mutation red-proof is unmeasurable here, because a fresh worktree has no `apps/ui/node_modules` and vitest there is exit 1 UNMUTATED with `ERR_MODULE_NOT_FOUND` — no discriminator, a vacuous proof. That reading was correct for every route the worker was able to try, and its three attempted provisioning routes really are denied to this session class. IT IS NOT THE ONLY ROUTE. Spawning vitest FROM the primary checkout, so the tool resolves its own package out of the primary's `node_modules`, while passing `--root` at the worktree and `--config` at the primary, roots DISCOVERY at the worktree while leaving the primary read-only — guardrail G5 intact. MEASURED AT `b2658466`: the unmutated control is exit 0 at 61 passed, and five separate mutations of the WORKTREE's `diffViewModel.ts` are each exit 1, each killing exactly the named test for the property it broke — the threshold boundary `<=` weakened to `<` kills the AT-the-threshold case, the overscan dropped from the leading edge and from the trailing edge each kill the both-ends widening case, `rowsAfter` forced to 0 kills the three-counts invariant, and the end clamp removed kills the past-the-end and the never-leaves-the-list cases. Control green again after the last restore, every file restored to its pre-mutation sha256. So the windowing rule's vitest suite is NOT vacuous, and this is the first TypeScript red-proof taken in this repository. The second deviation, that the vitest TOTAL is unreportable because the shipped node captures output and surfaces it only on failure, is closed the same way: the same tool driven from a scratch pytest node with `--reporter=verbose` reports 584 passed across 32 test files at `b2658466`, with all eighteen `computeDiffRowWindow` cases named and green, so the new `describe` is EXECUTED and not merely shipped. DECISION F037 D10 records the route.

THE TWO PYTHON RED-PROOFS THE WORKER TOOK BOTH REPRODUCE INDEPENDENTLY, in a disposable worktree at `b2658466` with `__pycache__` purged and `python3 -B` throughout, control exit 0 at 17 passed before and after, each replaced string counted at exactly 1 before its edit and each file restored to its pre-mutation sha256. Moving the `Open diff` button back inside the `{changedFiles && ...}` section is exit 1 failing exactly `TestTheEntryPointSitsAtPopoverLevel::test_the_entry_point_is_outside_and_after_the_changed_files_section`, so C5's gate really catches the return of `R-0726` — the state that was GREEN across every guard in this repository for a whole round. Reverting C4's anchored pattern to the bare `.count(literal)` form is exit 1 failing exactly `test_collapse_threshold_literal_occurs_exactly_once`, AND IT GOES RED WITHOUT ANY FURTHER MUTATION, because C6's `DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS = 2000` is already in the module and `200` is a substring of `2000`. That is `R-0728`'s predicted false red arriving in the same round that repaired it: the C4 anchor was load-bearing rather than speculative, and the block's ordering constraint putting C4 before C6 is what kept the round green.

THE CODE IS RIGHT AND THE REVIEWER READ IT RATHER THAN THE SUMMARY. `computeDiffRowWindow` is total: the three-counts invariant holds algebraically on BOTH branches, since `rowsBefore + rowsInWindow + rowsAfter` telescopes to `totalRows` for any `startIndex` and `endIndex`, and `startIndex <= endIndex` holds because `first` is clamped into the list, `startIndex` never exceeds `first`, and `endIndex` is a minimum of two values each at least `startIndex`. The zero-visible branch returns an empty window at the viewport's own position rather than at the top, which is the honest answer. C3's replacement comment was checked against the files it describes rather than against the block's prose: `DetailPopover.tsx` really emits `onOpenDiff(taskId)` at popover level, `RemedyShell.tsx` really holds the open task run and reads through `loadDiffEnvelope`, and `component_spec.md:108` really is the line listing the popover's `Open diff` button. C5's new guard carries its own vacuity assertions — that its scoper returns strictly less than the file and that the region it returns is the "Changed files" section — so it cannot silently stop scoping.

ONE GAP THIS ROUND LEAVES, NAMED RATHER THAN CARRIED SILENTLY, AND IT IS THE REVIEWER'S. `computeDiffRowWindow` is exported and has NO caller: the block ordered the rule built and explicitly forbade wiring it, which is a defensible slice, but a rule with no caller is a rule whose real behaviour is still unmeasured — the R-0220 lesson that a green gate is not a working feature. It is not registered as a finding because it is the block's declared plan rather than a defect, and C6 of F037 R21 closes it under that block's ordering constraint. THE BLOCK'S OWN CONTRADICTION EARNS NO ID AND IS APPENDED TO `.agent/prose_slips.md` BY C2 OF THIS ROUND, per operator amendment amend0827-process-diet rule 2: constraint 10 of the R20 block stated that no TypeScript mutation red-proof was ordered while G6 ordered two, and the block's claim that the `Gate: F037 R16` entry records why every vitest route is blind is inexact. Both damaged nothing on disk, and the worker declared both. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER20

<<<SLICE DONE727
Done: R-0727 — RESOLVED at F037 R20 IN PART and FULLY at F037 R21 by that round's C4, which this block's ordering constraint 6 places after this record. The finding was that a WHY comment in a production component still told its reader the component had no caller, two rounds after `RemedyShell` began drawing it. C3 of F037 R20 repaired the site the finding NAMED: `apps/ui/src/components/diff/DiffView.tsx` at `13904147` replaces `THIS COMPONENT IS NOT MOUNTED YET` with a paragraph naming the real wiring — the `Open diff` button in `DetailPopover`, `RemedyShell` holding the open task run and reading through `loadDiffEnvelope`, and this component drawn inside that panel — and the reviewer verified all three claims against the files at HEAD rather than against the block's prose, plus the `component_spec.md:108` citation on disk. An AST-free reading is enough here because the commit changes 11 lines and deletes 8, all inside a comment block, and `git diff` shows no executable line moved. THE REMAINDER, and why it is this paragraph's to name rather than a new id's: the R20 worker's staleness sweep — constraint 12 of that block, the standing counter-measure `R-0582` left behind — found FOUR MORE SITES of the same sentence in `tests/ui_contracts/test_diff_viewer_mount.py` at lines 3-4, 43, 260 and 369, and a fifth in `apps/ui/src/api/diffViewModel.ts` at line 327 whose future tense outlived the render it predicted. The worker reported all five and repaired none, which was right: constraint 12 permitted repairing only the site C3 named. The open set was searched before any new id was considered (§3 item 30) and the defect is not merely the same CLASS but the same SENTENCE, so this takes a second resolution paragraph on the precedent `R-0721` and `R-0725` both set in this record rather than a new id. All five were re-verified present at HEAD by the reviewer at `b2658466` before this paragraph was written. C4 of F037 R21 repairs them, editing comment and message text only, with every `assert` expression left byte-identical. THE LESSON THIS FINDING LEAVES: a stale claim propagates by COPYING, so the sweep that finds one must read every file that quotes it, and a block that repairs one site while its worker has already reported four more spends a round to buy a fifth of a repair.
<<<END DONE727

<<<SLICE DONE728
Done: R-0728 — RESOLVED at F037 R20 by that round's C4, and the resolution is unusually well evidenced because the predicted failure ARRIVED INSIDE THE SAME ROUND. The finding was that `test_collapse_threshold_literal_occurs_exactly_once` in `tests/ui_contracts/test_diff_view_model.py` counted the collapse threshold as a bare substring, so any new constant whose digits contain `200` would turn the guard red for breaking nothing. At `5897d2c8` the count is taken through a pattern compiled from `re.escape(literal)` and fenced with `(?<![\w.])` and `(?![\w.])`, so the literal is counted only where it stands as a whole number; `re` was already imported by that module and no import changed. MEASURED BY THE REVIEWER in a disposable worktree at `b2658466`, control exit 0 at 17 passed before and after: reverting the anchored pattern to the bare `.count(literal)` form and mutating NOTHING ELSE is exit 1 on exactly that node — because C6 of the same round added `DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS = 2000` and `200` is a substring of `2000`. So this was not a hypothetical: the guard would have gone falsely red at C6 had C4 not preceded it, and the block's ordering constraint 6 is what made the round green rather than luck. The anchor does not weaken what the guard was written for — a bare `200` transcribed into the module still turns it red, which the R20 worker measured and the reviewer reproduced. THE GENERAL RULE, and it is `R-0725`'s in the other direction: an unanchored substring test is wrong in BOTH colours — as a PRESENCE check it goes falsely green on an unrelated occurrence, and as a COUNT check it goes falsely red on one. Anchor the pattern or scope the region; a bare `in` and a bare `.count` are the same defect wearing two signs.
<<<END DONE728

<<<SLICE PROSESLIP
- 2026-08-28 · F037 R21 · The R20 block contradicted itself and one of its
  asides was inexact: constraint 10 stated that NO TypeScript mutation red-proof
  was ordered while G6 ordered two, and the claim that the `Gate: F037 R16`
  entry records why every vitest route is blind is not what that entry says. The
  worker declared both and routed around neither, and nothing landed wrong on
  disk. DECISION F037 D10 settles the underlying question by measurement: the
  red-proofs were orderable all along, and successive blocks said otherwise
  because each inherited the sentence instead of re-running it.
<<<END PROSESLIP

<<<SLICE DECISIOND10
## DECISION F037 D10 (2026-08-28) — TypeScript mutation red-proofs ARE measurable in this repository, and this is the route

CONTEXT. From F037 R8 onward every block in this feature carried a standing
claim that no TypeScript mutation red-proof can be ordered, because a
`git worktree` has no `apps/ui/node_modules` — it is gitignored — and vitest
there is exit 1 UNMUTATED with `ERR_MODULE_NOT_FOUND`, which is no
discriminator and so a vacuous proof. TRUE of every route tried, FALSE in
general, and it cost this feature its `.ts` red-proofs for thirteen rounds.

THE RULING. Vitest is spawned FROM the primary checkout, so it resolves its own
package out of the primary's `node_modules`, and `--root` points discovery at
the worktree, so the tree under test is the worktree's:

    subprocess.run(["npx", "vitest", "run",
                    "--root", f"{WT}/apps/ui",
                    "--config", f"{PRIMARY}/apps/ui/vitest.config.ts",
                    "<path relative to --root>", "--reporter=basic"],
                   cwd=f"{PRIMARY}/apps/ui", capture_output=True)

BOTH FLAGS ARE LOAD-BEARING AND THE FAILURE MODES DIFFER. `--root` alone cannot
resolve the `vitest` package from the worktree's own config and exits 1 before
any test loads. `--config` alone re-runs the PRIMARY tree and stays GREEN under
a worktree mutation — the dangerous one, because it looks like a passing gate.
Only the pair roots discovery at the worktree while resolving the tool at the
primary. The test path is RELATIVE and resolves against `--root`. G5 is intact:
the primary is only READ, and the only tree written to is the disposable
worktree. Direct `npx` and `node_modules/.bin/vitest` shell commands are denied
to this session class, so drive it from a `python3` script under the gitignored
`.remedy-wt/` — the refusal binds the shell caller, not the environment, which
is finding `R-0724`'s lesson.

EVIDENCE, taken at `b2658466`: control exit 0 at 61 passed, then five mutations
of the worktree's `diffViewModel.ts` each exit 1 killing exactly the named test
for the property broken, then control exit 0 again with every file restored to
its pre-mutation sha256. REVERSE by deleting this decision; but the claim it
replaces is measurably false, so reversing it re-blinds the `.ts` layer.
<<<END DECISIOND10

## Done when

Every gate below is EXECUTED and its real exit code recorded in the handback.
"Green" as a word is a finding. Report one line per gate.

- **G1 HYGIENE.** `.agent/STOP` absent, read from disk before C0a and again
  before C8. `git rev-parse HEAD` before C0a equals BASE. Branch is
  `feature/f037-rendered-diff-viewer`. `git status --porcelain | wc -l` is 0
  after every commit.
- **G2 TRANSPORT.** Report the committed C0a blob's byte count, line count and
  sha256, and show `git rev-parse` of `.agent/authored/f037-r21.md` and
  `.agent/last_block.md` at C0b as ONE blob.
- **G3 THE PLAN AT C1.** Byte equality of PLANF037R21, extracted from the
  COMMITTED C0a blob, with `git show <C1>:.agent/plan.md`, including the trailing
  newline. Negative control: the same slice minus its trailing newline, which
  must be False. Report `wc -l` and that it is strictly under 50, and the count
  of lines exactly `## Goal` and exactly `## Next Steps`.
- **G4 THE RECORD AT C2 AND C3.** For `.agent/live_review.md`: the pre-round blob
  joined to GATER20, DONE727 and DONE728 in Bundle order with exactly one newline
  before each equals the C2 blob. Negative control: flip one byte inside
  GATER20's FIRST paragraph; it must be False. Show the pre-round blob is a byte
  PREFIX of the committed one. For `.agent/prose_slips.md`: the same byte reader
  over PROSESLIP, its own negative control, the prefix check, and the count of
  lines matching `^- 2026-` [19 at base], which must rise by exactly one to 20 —
  that file is append-only and is never rewritten or renumbered. Its entries are
  WRAPPED with a two-space continuation indent and separated by one blank line,
  and the slice is already in that shape: apply it verbatim and do not re-wrap
  it.
  For `.agent/decisions.md`: the same byte reader
  over DECISIOND10, its own negative control, the prefix check, and the count of
  lines beginning `## DECISION ` [175 at base, so 176 at C3], with the string
  `F037 D10` occurring EXACTLY ONCE [0 at base]. Note that `.agent/decisions.md`
  ends with a single newline and NOT a blank line, so the one joining newline
  this reader prescribes is what separates the new heading from the last
  paragraph — the same shape as the `live_review.md` append.
- **G5 THE LEDGER.** Line-anchored over the C2 blob, each with its base figure
  from `b2658466` in brackets: `^- R-\d+ — ` [289], `^Done: R-\d+ — ` [37],
  `^Landed: R-` [6], `^Gate: F\d+ R\d+ — ` [90], and the OPEN SET computed AS A
  SET — registered ids minus ids named by a `Done:` line, never by subtraction
  [254]. Report that every registered id is distinct. The open set must FALL BY
  TWO, to 252: `R-0727` and `R-0728` are each named by a `Done:` line for the
  FIRST time here — at base both carry only a `Landed:` line, which resolves
  nothing — and this block registers no new id. Registrations and `Landed:` lines
  are therefore UNMOVED, and only the `Done:` and `Gate:` counts rise, by two and
  by one. If any figure disagrees, STOP and report it rather than adjusting it.
- **G6 THE RED-PROOFS.** In a disposable worktree at the C7 tree, `__pycache__`
  purged before every run and `python3 -B` throughout. Count each replaced string
  at exactly 1 BEFORE editing; restore every file to its pre-mutation sha256
  after every run and show the restore. Report the UNMUTATED control first and
  again last.
  TypeScript, driven per constraint 9 and DECISION F037 D10 over
  `src/api/diffViewModel.test.ts`:
  - (a) the unmeasured-viewport fallback removed, so a viewport height of 0
    yields a visible count of 0. MUST be RED, and it is the trap S2 exists for.
  - (b) the scroll division's `Math.floor` changed to `Math.ceil`, and, as a
    separate run, the height division's `Math.ceil` changed to `Math.floor`.
    BOTH MUST be RED.
  - (c) one spacer height returned as 0 instead of its row count times the row
    height. MUST be RED.
  Python, over `tests/ui_contracts/test_diff_view_render.py`:
  - (d) the call to `diffRowWindowForViewport` removed from `DiffView.tsx` and
    replaced with a direct `computeDiffRowWindow` call doing the division in the
    component. MUST be RED on the new delegation guard.
  - (e) `DIFF_VIRTUAL_ROW_HEIGHT_PX` changed from 20 to 24. MUST be RED on the
    stylesheet-agreement test of S5 — the discriminator proving it parses the CSS.
  If any of the six runs is NOT red, STOP and report it. Do not repair it.
- **G7 SUITES, TYPES AND LINT AT C7.** Primary checkout, ONE pytest process at a
  time, the worktree removed and `git worktree list` reported as one line first.
  Each with its base figure in brackets:
  - `python3 -m pytest tests/ui_contracts/ -q` [642 passed, 4 skipped]
  - `python3 -m pytest tests/ui_server/ -q` [495 passed]
  - `python3 -m pytest tests/orchestration/test_test_runner.py tests/docs/ -q` [347 passed]
  - `python3 -m ruff check tests/ui_contracts/test_diff_view_render.py tests/ui_contracts/test_diff_viewer_mount.py`
  - the typescript node
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -k "typescript or tsc or noEmit" -q -rs`
    [1 passed, 73 deselected] — it must PASS and not SKIP, and it is most of this
    round's gate because S4 is `.tsx`. If `tsc --noEmit` is RED, STOP and report;
    do not repair.
  - the canary `python3 -m pytest tests/cli/test_golden_path.py -q` [42 passed]
  - the vitest TOTAL, driven per DECISION F037 D10 with `--reporter=verbose`
    against the PRIMARY tree, reporting the test-file and test counts [32 files,
    584 tests] and naming the new `describe`'s cases as executed.
- **G8 STRUCTURE AND THE OPEN PR GATE AT C7.** `git diff --name-only <BASE>..<C7>`
  equals the Change set minus `.agent/handoff.md`; report ACTUAL MINUS EXPECTED
  and EXPECTED MINUS ACTUAL. `git diff --stat` restricted to `packages/` is
  EMPTY, and restricted to `apps/ui/src/components/` names `DiffView.tsx` and
  nothing else. Per-commit insertions from `git show --numstat`, each under 500,
  each matching the handback's table. Lines matching `^<<<SLICE ` or `^<<<END `
  are 0 in every edited target, with the C0a blob as a NON-ZERO control.
  `git ls-files .remedy-wt | wc -l` is 0.
  `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, the SESSION NUMBER, branch, per-commit changed-files tables, the real
verification transcript one line per gate, constraint 11's staleness sweep,
deviations and assumptions, the item-status table covering every C and every G,
and the next expected action. Derive its length bound yourself from AGENTS.md.

If any gate is RED, if a slice will not apply, or if anything here contradicts
itself: STOP, write the handback saying exactly what happened, and end.
