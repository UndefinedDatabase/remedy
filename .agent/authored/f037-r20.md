# STEP T003 (fourth round) — F037 Rendered diff viewer, round 20

BASE: `fe3f1179`. SESSION 5 of feature F037, and the LAST delegated round of this
session. This block carries no line that is a run of a single repeated character,
so nothing in its frame has a length a reader must recover by eye.

## Goal

Close what R19 left open, then take the first half of virtual scrolling. Two
findings the reviewer raised at the R19 gate are repaired: a WHY comment in
`DiffView.tsx` that still tells the reader the component is not mounted, and a
count guard that goes falsely RED on any new constant whose digits contain the
collapse threshold's. The `R-0726` repair, which landed in source at R19 but is
caught by no gate, gets one. Then the windowing rule the Design section's
"virtual scrolling >2k lines" names is built in the layer vitest reaches.

## Bundle

- C0a save this block verbatim to `.agent/authored/f037-r20.md`.
- C0b mirror the same bytes into `.agent/last_block.md`.
- C1 rewrite `.agent/plan.md` from the PLANF037R20 slice.
- C2 append GATER19, DONE725B, DONE726, FINDING727 and FINDING728 to
  `.agent/live_review.md`.
- C3 the `R-0727` repair: SPEC S1, plus its `Landed:` line per SPEC S6.
- C4 the `R-0728` repair: SPEC S2, plus its `Landed:` line per SPEC S6.
- C5 the `R-0726` gate: SPEC S3.
- C6 the windowing rule: SPEC S4 and S5.
- C7 rewrite `.agent/handoff.md` as the handback.

## Change set

Exactly these paths, and nothing outside them:

- `.agent/authored/f037-r20.md` (new)
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `apps/ui/src/components/diff/DiffView.tsx`
- `tests/ui_contracts/test_diff_view_model.py`
- `tests/ui_contracts/test_diff_viewer_mount.py`
- `apps/ui/src/api/diffViewModel.ts`
- `apps/ui/src/api/diffViewModel.test.ts`
- `.agent/handoff.md`

Push the branch after C7 with `git push -u origin feature/f037-rendered-diff-viewer`.
Create no PR. Merge nothing. Rewrite no history.

## Constraints

1. Apply every slice BYTE FOR BYTE. Never write a `<<<SLICE` or `<<<END` marker
   line into a target file. If a slice looks wrong, apply it and declare it.
2. The SPEC items describe PRODUCTION CODE and are not slices. The WHY comments
   they ask for are yours to word.
3. NO COMPONENT IS WIRED TO THE WINDOW THIS ROUND. C6 builds the RULE and its
   vitest tests only; `DiffView.tsx` keeps rendering every row it is given, and
   the only edit it takes this round is the comment repair of C3. Wiring is the
   next round's, with the perf fixture that measures it.
4. Nothing under `packages/` changes, and no component other than
   `DiffView.tsx` is edited.
5. NO NEW CSS, no new stylesheet, no change to `apps/ui/src/styles/tokens.css`.
6. TWO GUARDS BIND `apps/ui/src/api/diffViewModel.ts` AND C6 MUST SATISFY BOTH.
   `tests/ui_contracts/test_diff_view_model.py` requires that EVERY exported
   value name appears in `diffViewModel.test.ts`, and it reads that test file
   COMMENT-STRIPPED — so a new export named only in a comment does NOT count and
   the guard will be red. It also requires the collapse threshold's literal to
   occur exactly once across both files; C4 repairs the anchoring of that count
   BEFORE C6 adds a constant, which is why the commit order is what it is.
7. Order the commits exactly C0a, C0b, C1, C2, C3, C4, C5, C6, C7. C1 is the
   first substantive commit. C2 persists the record BEFORE any repair. C4
   precedes C6 for the reason constraint 6 gives.
8. Every gate runs at a commit STRICTLY EARLIER than C7. G1's second STOP
   reading is the sole exception, taken immediately before C7.
9. Destructive verification runs ONLY inside a disposable worktree under
   `.remedy-wt/`. The primary checkout reads `git status --porcelain` empty
   after every commit.
10. NO TYPESCRIPT MUTATION RED-PROOF IS ORDERED; the GATER16 entry of
    `.agent/live_review.md` records why every route is blind or a startup error.
11. WRITE NO `Done:` PARAGRAPH. `Done:` is reserved for reviewer-authored text.
    Your marker for a landed fix is the `Landed:` line SPEC S6 describes.
12. STANDING STALENESS SWEEP, and it is why C3 exists at all. Before C7, re-read
    every WHY comment in each file this round edits and report any sentence that
    the branch has since made FALSE. Report them; repair only the one C3 names.
    A comment asserting a fact about the codebase is a claim, and this round is
    repairing one that outlived its round by two.

## SPEC — finding R-0727, the stale header (C3)

S1. `apps/ui/src/components/diff/DiffView.tsx` opens with a paragraph beginning
`THIS COMPONENT IS NOT MOUNTED YET, AND THAT IS THE PLAN RATHER THAN AN
OMISSION`, which continues `A reader who greps for a caller of ` and tells that
reader they will find none. Both sentences are FALSE: R18's C5 mounted the
component in `apps/ui/src/components/shell/RemedyShell.tsx`, which imports it and
renders `<DiffView` inside the shell's diff panel. REPLACE that paragraph with
one that tells the truth and keeps the useful half — that the entry point is the
`Open diff` button in `DetailPopover` emitting `onOpenDiff(taskId)`, that
`RemedyShell` holds the open task and reads the envelope through
`loadDiffEnvelope`, and that this component is drawn inside that panel. Keep the
first paragraph and the `NOTHING IN THIS REPOSITORY CAN RENDER THIS FILE`
paragraph as they stand — both are still true — and change no code in the file.

## SPEC — finding R-0728, the unanchored count (C4)

S2. In `tests/ui_contracts/test_diff_view_model.py`,
`test_collapse_threshold_literal_occurs_exactly_once` counts the threshold's
literal with `module_text.count(literal) + tests_text.count(literal)`, a BARE
SUBSTRING count. The literal is `200`, so any future constant whose digits
contain it — `2000` is the one this feature needs next — makes the count 2 and
turns the guard RED for a change that broke nothing. Repair it by counting the
literal only where it stands as a WHOLE NUMBER: compile a pattern from
`re.escape(literal)` fenced so that neither a word character nor a `.` may
precede or follow it, and count with that pattern over both texts instead. Keep
everything else about the test, including its message and its reason.

THE REVIEWER MEASURED THIS REPAIR at `fe3f1179` in a disposable worktree, and
these are the three readings it must reproduce: the repair ALONE leaves the guard
GREEN at 3 passed; the repair plus an `export const … = 2000;` constant no longer
fails this test; and a bare `200` transcribed elsewhere in the module STILL turns
this test RED, so the anchor does not weaken what the guard was for.

## SPEC — the R-0726 gate (C5)

S3. R19's C4 moved the `Open diff` button to popover level, which is the repair
of `R-0726`, and NO GATE CATCHES IT: the reviewer measured at `7e263ea5` that
moving the button back inside the `changedFiles` section leaves every guard
GREEN, because `tests/ui_contracts/test_diff_viewer_mount.py` scopes to the
button's own opening tag — which the move does not alter — and
`tests/ui_contracts/test_diff_envelope_door.py` never reads that file.

Add to `tests/ui_contracts/test_diff_viewer_mount.py` one test pinning the
button's PLACEMENT rather than its shape. Read `DetailPopover.tsx`
comment-stripped, take the region AFTER the `changedFiles` section's guarded
block closes, and assert the tag naming `onOpenDiff` lies inside that region and
not within the guarded section. Assert the shape you actually wrote; if pinning
it requires naming a marker in the component, name the marker and say so in the
docstring. The test must go RED when the button moves back inside the section —
gate G6(c) is that proof, and if it comes back GREEN say so plainly rather than
adjusting anything.

## SPEC — the windowing rule (C6)

S4. In `apps/ui/src/api/diffViewModel.ts`, add the rule that decides WHICH rows
a virtualized viewer draws. It derives from the row COUNT and the viewport, never
from pixels — this module is pure data in, pure data out, and it imports nothing.
Export a threshold constant named for what it governs, declared with the literal
`2000` exactly once and referenced BY NAME everywhere else, the same discipline
`DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` already follows; the Design section of
`docs/roadmap/features/T5_F037.md` names "virtual scrolling >2k lines" and this
is that number. Export a result type and a TOTAL function taking the row count,
the first visible row index, the visible row count and an optional overscan.
Its rules:
(a) at or below the threshold the viewer is NOT virtualized — the window is
    every row, and the counts before and after it are zero;
(b) above the threshold the window is the visible range widened by the overscan
    at both ends and CLAMPED to the list;
(c) every hostile input is resolved rather than trusted, because nothing
    upstream checks these numbers: a negative or non-finite index, a
    non-positive visible count, a negative overscan, an index past the end;
(d) the invariant a caller may rely on, and which the tests must pin: the rows
    before the window, the rows in it, and the rows after it sum to the row
    count exactly, and the start is never past the end.

S5. A new `describe` at the END of `apps/ui/src/api/diffViewModel.test.ts`,
changing no existing test, covering every clause of S4 — including the sum
invariant checked across a range of inputs, and each hostile case of (c) by name.
It must NAME the new exports in CODE, not only in a comment: constraint 6's guard
reads that file comment-stripped.

S6. For each of C3 and C4, append to `.agent/live_review.md` in that SAME commit
one line of your own wording, in exactly this form and nothing else:
`Landed: R-XXXX — <one sentence: what changed, and the commit>`.

## Slice convention

Each slice sits between a `<<<SLICE <NAME>` line and a `<<<END <NAME>` line.
Neither marker line is part of the slice, and neither is ever written into a
target file. The slices this block carries are PLANF037R20, GATER19, DONE725B,
DONE726, FINDING727 and FINDING728. PLANF037R20 is a FULL REWRITE of
`.agent/plan.md`. The other five are APPENDS to `.agent/live_review.md`, applied
IN THE ORDER JUST LISTED in the SAME commit, each joined to the growing file with
exactly one newline.

<<<SLICE PLANF037R20
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D9.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A5.

## Current Step
R20 closes what R19 left open and starts the last named piece. `DiffView.tsx`
still tells its reader the component is not mounted, two rounds after R18
mounted it, which is `R-0727`. The collapse-threshold count guard counts a bare
substring, so the `2000` this feature needs next would turn it red for breaking
nothing — `R-0728`, measured rather than predicted. The `R-0726` repair landed in
source at R19 and no gate catches the button moving back, so it gets one. Then
the windowing rule of "virtual scrolling >2k lines" is built in `diffViewModel.ts`
where vitest really runs it; no component is wired to it this round.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R19 verdict, two resolutions, two findings | ordered | record first |
| C3 the R-0727 comment repair | ordered | it has been false for two rounds |
| C4 the R-0728 count-anchor repair | ordered | before C6 needs it |
| C5 the R-0726 placement gate | ordered | the repair is real but ungated |
| C6 the windowing rule and its vitest tests | ordered | the last named piece |
| C7 the handback | ordered | |

## Next Steps
1. Wire the window into `DiffView`, with the perf fixture Acceptance requires:
   the 10k-line fixture within budget, and the numbers recorded.
2. The lazy language bundles, unknown languages rendering plain with no bundle
   fetch, which Acceptance also names.
3. A ruling on the sidebar's visual treatment, still owed.

## Risks
- Round 20 of a 25-round soft limit, and this is the last round of session 5 of
  7. If the wiring, the perf fixture and the lazy bundles do not all fit in the
  next session, the one after it owes a scope report rather than more work.
- Nothing in this repository renders a `.tsx` file, so the wiring of step 1 will
  be gated by text and `tsc --noEmit` alone, as every `.tsx` round here has been.
<<<END PLANF037R20

<<<SLICE GATER19
Gate: F037 R19 — the round that closed both gaps the R18 gate found and drew the file sidebar. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran it independently at `fe3f1179`. RE-MEASURED, NOT ACCEPTED. The committed C0a blob is 28730 bytes, 365 lines, sha256 `6dad1fd45d087522d29428da793120aa5e3f84af2a3837ab20750c6481f4f7ef`, BYTE EQUAL to the reviewer's own scratch original `.remedy-wt/f037-r19-block.md`, so the chain covers the emission and not only the worker's self-consistency. Caps: CONTENT 56, TOTAL 365, PROSE 309. Per-commit insertions over `0a291411..fe3f1179` are 365, 245, 25, 10, 15, 27, 120, 340 and 241, every one under five hundred and every one matching the `+/-` column of the handback's `## Commits` table cell by cell. The ledger at the tip reads 287 registered ids all distinct, 35 `Done:` lines, 4 `Landed:` lines, 89 `Gate:` entries and an open set of 253. RE-RUN SUITES, primary checkout, one process at a time, every one exit 0: `tests/ui_contracts/` 641 passed 4 skipped against 630 at base; `tests/ui_server/` 495 passed; `tests/docs/` 295 passed; the canary 42 passed; and the typescript node 1 passed 73 deselected, PASSED and not skipped. `git diff --stat` over `apps/ui/src/api/` and over `packages/` is EMPTY for the whole range, which is constraints 3 and 4 measured rather than asserted.

BOTH REPAIRS WERE PROVED BY THE REVIEWER RATHER THAN ACCEPTED, in a disposable worktree at `7e263ea5`, control exit 0 at 50 passed. Renaming the TASK-RUN template's `/diff?` ending alone — GREEN before this round's C3 — is now exit 1 on exactly `TestTheTaskRunScopeRouteAgrees::test_the_client_addresses_the_task_run_segment`, and renaming the JOB template's ending is still exit 1 on its own node, so the remainder was closed without breaking the sibling repaired before it. Deleting the entry-point button outright is exit 1 on three nodes, so the button's EXISTENCE is gated.

WHAT IS NOT GATED IS THE BUTTON'S PLACEMENT, and the worker raised it as its deviation 1 rather than leaving it to be found later. Moving the button back inside the `changedFiles` section leaves every guard GREEN at 50 passed — measured by the reviewer in the same worktree at the same commit. THE CAUSE IS IN THE REVIEWER'S BLOCK: SPEC S6 of the R19 block defined the new guard as reading `DiffFileSidebar.tsx`, `DiffView.tsx` and `RemedyShell.tsx`, and `DetailPopover.tsx` — the only file that mutation touches — is not among the three, so the check was invisible by construction. The mount guard of R18 does not close it either, because it scopes to the button's own opening tag and the move leaves that tag identical. So the `R-0726` repair is REAL IN THE SOURCE and was UNGATED for one round; C5 of F037 R20 gates it, under that block's ordering constraint 7. The worker widened nothing on its own initiative, which was right: the block named its guard's three files and widening them would have been the silent scope change the block conditions forbid.
<<<END GATER19

<<<SLICE DONE725B
Done: R-0725 — FULLY RESOLVED at F037 R19 by that round's C3, which closed the remainder the first resolution paragraph above named. `tests/ui_contracts/test_diff_envelope_door.py` at `7e263ea5` no longer asserts `"task-runs" in client_code()` over the whole module: `TestTheTaskRunScopeRouteAgrees::test_the_client_addresses_the_task_run_segment` now reads the body `ts_function_body` returns for `diffEnvelopePath` and matches `task-runs/[^`]*/diff\?` inside it, so the segment and the ENDING are pinned together — a segment leading nowhere the server routes is not an agreement, which is the sentence the repair's own comment gives. MEASURED BY THE REVIEWER in a disposable worktree at `7e263ea5`, control exit 0 at 50 passed before and after: renaming this template's ending alone is exit 1 on this node, where it was GREEN at the R18 tip, and renaming the JOB template's ending is exit 1 on ITS node, so neither sibling was repaired at the other's expense. ALL THREE SITES OF THIS FINDING ARE NOW SCOPED — the job path, the task-run path and the reader call — and a vacuity test pins that `ts_function_body` really returns less than the whole module. THE GENERAL RULE THIS FINDING LEAVES BEHIND, which is why it was worth two rounds: a presence assertion naming a symbol that legitimately occurs more than once in its file pins nothing unless it is scoped to the site whose behaviour it means, and an import, a type annotation, a second call site and a second template literal are all such occurrences. `R-0728`, registered below, is that same root cause in the COUNT direction, where the failure is a false red rather than a false green.
<<<END DONE725B

<<<SLICE DONE726
Done: R-0726 — RESOLVED at F037 R19 by that round's C4, and GATED by C5 of F037 R20, which this block's ordering constraint 7 places after this record. `apps/ui/src/components/detail/DetailPopover.tsx` at `7c0d52a8` renders the `Open diff` button at POPOVER level, after `PromptTracePanel`, under the condition `task && onOpenDiff` and nothing else — so the entry point no longer inherits the `changedFilesSafe` condition of the "Changed files" section, and a task run holding a diff with no safe file list can now be opened. Every other property the R18 spec gave the button survives the move: a real `<button type="button">`, the label `Open diff`, `onOpenDiff(task.id)` passing the task id rather than the graph node id, and no class. The placement is also what `docs/ui/design_reference/component_spec.md:108` asked for, listing the popover's buttons as a peer of its sections rather than inside one. THE RESOLUTION IS RECORDED WITH ITS OWN GAP NAMED, because the fix landed one round before the gate did: measured by the reviewer at `7e263ea5`, moving the button back inside the section left every guard GREEN at 50 passed, so for one round this repair was real in the source and caught by nothing. The gate C5 adds pins the button's PLACEMENT rather than its shape, and G6(c) of this round is its red-proof; a resolution whose gate is ordered in the same block as the resolution is the narrowest form of the `R-0524` carve-out, and the ordering constraint is what makes it honest rather than a promise.
<<<END DONE726

<<<SLICE FINDING727
- R-0727 — Low, A WHY COMMENT IN A PRODUCTION COMPONENT STILL TELLS ITS READER THE COMPONENT IS NOT MOUNTED, TWO ROUNDS AFTER IT WAS MOUNTED. Raised by the WORKER as observation 3 of F037 R19, which noticed it and correctly left it alone because that round's SPEC S4 said "change nothing else in that file", and registered here with the reviewer's own reading. MEASURED AT `fe3f1179`: `apps/ui/src/components/diff/DiffView.tsx` opens its second paragraph with `THIS COMPONENT IS NOT MOUNTED YET, AND THAT IS THE PLAN RATHER THAN AN OMISSION` and continues `A reader who greps for a caller of ` the component `and finds none has found the task slicing, not dead code`. Both sentences are false at that commit: `apps/ui/src/components/shell/RemedyShell.tsx` imports the component and renders it inside the diff panel, landed by C5 of F037 R18. A reader who runs that grep finds a caller, and the paragraph tells them they will not. WHY THIS IS A FINDING AND NOT A NOTE: the Code Discoverability Conventions of AGENTS.md make these comments load-bearing — "Deliberate absences are documented where a reader would search for them", precisely because text search cannot find code that does not exist — so a deliberate-absence paragraph that outlives its absence is worse than none, since it answers the reader's question with a confident falsehood. It is wrong state on disk under `apps/`, which is what operator amendment amend0827-process-diet rule 2 reserves an id for, and it is not reviewer prose. LOW because no behaviour is affected, no gate is blind, and the paragraph beside it — that nothing in this repository can render the file — remains true. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED (§3 item 30): the staleness family is `R-0582`'s, whose counter-measure is a standing staleness gate carried by every block, and the reason this instance survived two rounds is that neither the R18 nor the R19 block carried one — a reviewer omission, not a new class. THE FIX, which C3 of F037 R20 lands, replaces the paragraph with the wiring that now exists rather than deleting it, and constraint 12 of that block is the standing sweep restored. OPEN.
<<<END FINDING727

<<<SLICE FINDING728
- R-0728 — Low, A COUNT GUARD OVER THE COLLAPSE THRESHOLD COUNTS A BARE SUBSTRING, SO THE NEXT CONSTANT THIS FEATURE NEEDS TURNS IT RED FOR BREAKING NOTHING. Raised by the reviewer while planning F037 R20, by running the guard against the change it was about to order rather than reasoning about it — checklist item 7 of docs/agents/planner_reviewer_prompt.md, which exists for exactly this. MEASURED AT `fe3f1179` in a disposable worktree: `tests/ui_contracts/test_diff_view_model.py::test_collapse_threshold_literal_occurs_exactly_once` computes `module_text.count(literal) + tests_text.count(literal)` where `literal` is the text `200`, and it is GREEN at 3 passed today. Adding `export const DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS = 2000;` to `apps/ui/src/api/diffViewModel.ts` makes that count 2 — because `200` is a SUBSTRING of `2000` — and the guard goes RED naming the collapse threshold, over a change that neither transcribes nor drifts from the collapse rule. Constants of `2048` and `1500` leave the count at 1, which confirms the digits and not the addition are what the guard is reacting to. THE EFFECT IS ON THE FEATURE'S REMAINING SCOPE: the Design section of `docs/roadmap/features/T5_F037.md` names "virtual scrolling >2k lines", so `2000` is the number the next piece of work has to declare, and a builder meeting this red has two honest routes — pick a wrong number, or repair the guard — while a third and worse one, deleting the guard, is always available. THIS IS `R-0725`'S ROOT CAUSE IN THE OTHER DIRECTION, and the open set was searched before the id was minted (§3 item 30): R-0725 is an unanchored substring PRESENCE check satisfied by an unrelated occurrence, a false GREEN, and its fix is scoping to a function body; this is an unanchored substring COUNT inflated by an unrelated occurrence, a false RED, and its fix is anchoring the pattern. `R-0630` requires a count over a file that quotes its own record format to name its anchor, which is the same lesson for `.agent/live_review.md` and routes its fix to `docs/agents/planner_reviewer_prompt.md`; this is a landed assertion in `tests/` with a repair in this feature's own change set, so it takes its own id. LOW because the guard is green today and the failure is a false red on work not yet done, which is the safe direction and is visible the moment it happens. THE FIX, which C4 of F037 R20 lands and which the reviewer measured before ordering: count the literal only where it stands as a whole number, with neither a word character nor a `.` adjacent. The repair alone leaves the guard GREEN at 3 passed; with it, the `2000` constant no longer trips this test; and a bare `200` transcribed elsewhere in the module still turns it RED, so the anchor removes the false positive without weakening what the guard was written for. OPEN.
<<<END FINDING728

## Done when — the gates

Run every gate yourself and record its REAL exit code and REAL summary line.
"Green" as a word is a finding. One line per gate in the handback.

G1 HYGIENE. Read `.agent/STOP` from disk before C0a and again immediately before
C7; report ABSENT or PRESENT each time, and on PRESENT stop after the commit in
hand and hand off. `git rev-parse` before C0a must equal `fe3f1179`. Report
`git branch --show-current`. Report the `git status --porcelain` line count after
each of C0a through C6; each must be 0.

G2 TRANSPORT, one digest comparison. Report the byte count, line count and
sha256 of the committed C0a blob and compare all three against the readings the
delegation named. Then report whether
`git rev-parse <C0b>:.agent/authored/f037-r20.md` and
`git rev-parse <C0b>:.agent/last_block.md` are the same blob.

G3 EXTRACTION AND CAPS, on the committed C0a blob. Report the content line count
of each of the six slices, their sum as CONTENT, the blob's line count as TOTAL,
and TOTAL minus CONTENT as PROSE. Report TOTAL <= 490 and PROSE <= 400.

G4 THE PLAN AT C1. Extract PLANF037R20 from the committed C0a blob
programmatically. Report byte equality with `git show <C1>:.agent/plan.md`
INCLUDING the trailing newline, and the negative control against the slice minus
its trailing newline, which must be False. Report `wc -l`, strictly under 50, and
the count of lines exactly `## Goal` and exactly `## Next Steps`, each 1.

G5 THE RECORD AT C2. Extract the five record slices from the committed C0a blob.
Report reader (a): the pre-round blob
`git show fe3f1179:.agent/live_review.md`, joined to the five slices in the
Bundle's order with exactly one newline before each, equals
`git show <C2>:.agent/live_review.md`. Report reader (b): the last N
blank-line-separated units of the committed file equal the five slices' N units
IN ORDER, N counted by your script across all five. Report a negative control for
each reader flipping one byte inside the FIRST appended paragraph — that is
GATER19's first paragraph; both must be False. Report that the pre-round blob is
a byte PREFIX of the committed one. Then report, line-anchored over the committed
file, with the figure at `fe3f1179` beside each: `^- R-\d+ — ` (287 at base),
`^Done: R-\d+ — ` (35), `^Landed: R-` (4), `^Gate: F\d+ R\d+ — ` (89), the open
set as registered ids minus ids named by a `Done:` line (253 at base), and
whether every registered id is distinct. This round registers R-0727 and R-0728
and resolves R-0725 and R-0726. `^Landed: R-` becomes 5 at C3 and 6 at C4.

G6 THE RED-PROOFS OF THE PYTHON GUARDS. All runs in a disposable worktree at the
C6 tree, `__pycache__` purged before every run, `python3 -B` throughout. Report
the UNMUTATED control for
`tests/ui_contracts/test_diff_view_model.py tests/ui_contracts/test_diff_viewer_mount.py tests/ui_contracts/test_diff_envelope_door.py tests/ui_contracts/test_diff_file_sidebar.py tests/ui_contracts/test_diff_view_render.py`
before any mutation and again after the last restore; both must be exit 0.

UNIQUENESS, PER FINDING `R-0629`, WHICH IS OPEN AND BINDING ON ANY BLOCK THAT
ORDERS A DESTRUCTIVE CONTROL. Every target below is code THIS ROUND writes or
repairs, so no count can exist while this block is written and the reviewer
states none. YOU take each reading: count the replaced string in the named file
before editing and report it. If it is not 1, EXTEND the string until it reads 1
in that file, report the extended string and its count, and mutate that.

Then, one at a time, each mutation restored byte-identically to its pre-mutation
sha256 before the next, reporting the REAL exit code, the summary line and the
failing node ids:
(c) THE C5 GATE'S OWN PROOF: in `DetailPopover.tsx`, move the whole `Open diff`
    button block back inside the `changedFiles` section, exactly where R18 had
    it. This was GREEN before C5 and must now be RED. If it is GREEN, say so
    plainly and change nothing.
(g) in `diffViewModel.ts`, make the windowing function ignore its threshold, so
    a short list is reported as virtualized.
(h) in `diffViewModel.ts`, drop the clamp that keeps the window inside the list,
    so an index past the end produces an end index beyond the row count.
(i) in `test_diff_view_model.py`, revert C4's anchored pattern to the bare
    `.count(literal)` form, then ALSO add `const transcribed = 200;` to
    `diffViewModel.ts` — the guard must be RED, which shows C4 kept the check it
    was anchoring rather than removing it.
Each of (c), (g), (h) and (i) must be exit 1. For (g) and (h), the node that
fails is a vitest test rather than a pytest one, so those two are measured
DIFFERENTLY: see G7's vitest reading and report the vitest exit code and its
failing test names instead.

G7 SUITES, TYPES, LINT AND CANARY AT C6, primary checkout, ONE pytest process at
a time. Report exit code and summary line for each, with the base figure beside
it: `python3 -m pytest tests/ui_contracts/ -q` (641 passed, 4 skipped at base),
`python3 -m pytest tests/ui_server/ -q` (495 passed),
`python3 -m pytest tests/orchestration/test_test_runner.py -q` (52 passed),
`python3 -m pytest tests/docs/ -q` (295 passed),
`python3 -m ruff check tests/ui_contracts/test_diff_view_model.py tests/ui_contracts/test_diff_viewer_mount.py`,
and the canary `python3 -m pytest tests/cli/test_golden_path.py -q` (42 passed).
State explicitly whether the typescript node inside `tests/ui_server/` PASSED or
SKIPPED. `tests/orchestration/test_test_runner.py` is the node that runs
`npx vitest run`, so state that the new `describe` really EXECUTED and give the
vitest test total it reports.

G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C6. Report
`git diff --name-only fe3f1179..<C6>` and set-difference it BOTH ways against the
Change set; ACTUAL MINUS EXPECTED must be empty and EXPECTED MINUS ACTUAL must be
`.agent/handoff.md` alone. Report `git diff --stat` restricted to `packages/`,
which must be EMPTY, and to `apps/ui/src/components/`, which must name
`DiffView.tsx` and NOTHING ELSE — that is constraints 3 and 4 made mechanical.
Report each commit's insertion count from `git show --numstat`, each under 500,
and confirm each matches the `+/-` column of your own `## Commits` table cell by
cell. Report the count of lines matching `^<<<SLICE ` and `^<<<END ` in
`.agent/plan.md`, `.agent/live_review.md`, `apps/ui/src/api/diffViewModel.ts` and
`tests/ui_contracts/test_diff_viewer_mount.py` — each must be 0 — with a CONTROL
count over the C0a blob, which must be non-zero. Report
`git ls-files .remedy-wt | wc -l`, which must be 0. Report
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

## Handback

Rewrite `.agent/handoff.md` at C7 per docs/agents/handback_template.md. It has no
length cap. It must carry: the Session line naming SESSION 5 of F037 and round
20; the review range; a `## Commits` section with one `+/-` table per commit; the
external actions; one Verification line per gate G1 through G8 with real exit
codes; the authored-text proofs; the deviations and assumptions; the item-status
table covering every C and every G exactly once; constraint 12's staleness sweep
report; and the next expected action.

THIS IS THE LAST ROUND OF SESSION 5, so the handback's `## Next` section names
what the NEXT session does first: re-read `.agent/STOP` from disk (Phase 1 rule
1), then the Open PR Gate, then review THIS round at its C6 commit and book the
verdict in the first substantive commit of round 21. Say plainly that this
round's own gate entry is not on disk yet, because the reviewer writes it next
session.
