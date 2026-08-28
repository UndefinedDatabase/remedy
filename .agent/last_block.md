# STEP T003 (third round) — F037 Rendered diff viewer, round 19

BASE: `0a291411`. SESSION 5 of feature F037. This block carries no line that is a
run of a single repeated character, so nothing in its frame has a length a reader
must recover by eye.

## Goal

Close the two gaps the R18 gate found, then draw the file sidebar. The remainder
of finding `R-0725` — the task-run path's own ending, still pinned by nothing —
is scoped like its two siblings. Finding `R-0726` moves the "Open diff" button
out of the "Changed files" section, whose condition made the viewer's only entry
point invisible for a task run with a diff and no safe file list. Then
`buildDiffFileSummaries`, exported since R15 and drawn by nothing, becomes the
sidebar the feature file's Design names.

## Bundle

- C0a save this block verbatim to `.agent/authored/f037-r19.md`.
- C0b mirror the same bytes into `.agent/last_block.md`.
- C1 rewrite `.agent/plan.md` from the PLANF037R19 slice.
- C2 append GATER18, DONE725A and FINDING726 to `.agent/live_review.md`.
- C3 the `R-0725` remainder: SPEC S1, plus the `Landed:` line SPEC S5 describes.
- C4 the `R-0726` repair: SPEC S2, plus its own `Landed:` line per SPEC S5.
- C5 the sidebar: SPEC S3 and S4, in a NEW component file and in `DiffView.tsx`.
- C6 the guard: SPEC S6, in `tests/ui_contracts/test_diff_file_sidebar.py`, NEW.
- C7 rewrite `.agent/handoff.md` as the handback.

## Change set

Exactly these paths, and nothing outside them:

- `.agent/authored/f037-r19.md` (new)
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `tests/ui_contracts/test_diff_envelope_door.py`
- `apps/ui/src/components/detail/DetailPopover.tsx`
- `apps/ui/src/components/diff/DiffFileSidebar.tsx` (new)
- `apps/ui/src/components/diff/DiffView.tsx`
- `apps/ui/src/components/shell/RemedyShell.tsx`
- `tests/ui_contracts/test_diff_file_sidebar.py` (new)
- `.agent/handoff.md`

Push the branch after C7 with `git push -u origin feature/f037-rendered-diff-viewer`.
Create no PR. Merge nothing. Rewrite no history.

## Constraints

1. Apply every slice BYTE FOR BYTE. Never write a `<<<SLICE` or `<<<END` marker
   line into a target file. If a slice looks wrong, apply it and declare it.
2. The SPEC items describe PRODUCTION CODE and are not slices. The WHY comments
   they ask for are yours to word.
3. `apps/ui/src/api/` IS NOT EDITED THIS ROUND. `buildDiffFileSummaries` and
   `DiffFileSummary` already exist and already carry `rowKey`; the sidebar draws
   them and derives nothing. If the sidebar seems to need a model change, stop
   and declare it rather than making it.
4. Nothing under `packages/` changes.
5. NO NEW CSS AND NO NEW STYLESHEET. `DiffView.module.css` is a transcription of
   the binding CSS of `docs/roadmap/features/T5_F037.md`, whose vocabulary
   amendment A5 fixes, and the CANONICAL DESIGN REFERENCE banner forbids
   inventing a visual language. The Design section names "paths + stats bars"
   for the sidebar and the binding CSS defines no rule for either, so THIS ROUND
   SHIPS THE SIDEBAR AS SEMANTIC MARKUP ONLY — a list, real numbers, no class —
   and a WHY comment in the component says so and says that the visual treatment
   needs a ruling this round does not make. That is the same posture the panel
   wrapper and `DiffView`'s own root already take.
6. The four guards constraint 5 of the R18 block listed still bind
   `DetailPopover.tsx`: `remedy-detail-compact` and `Result` must survive,
   `Next safe action`, `next.command` and `@mui` must stay absent, the
   `blockedReason` / `completedAt` / changed-files fields must survive, and the
   words `rank`, `importance`, `node_type`, `present signals`, `missing signals`
   and `zone` must not appear, case-insensitively.
7. Order the commits exactly C0a, C0b, C1, C2, C3, C4, C5, C6, C7. C1 is the
   first substantive commit. C2 persists the record BEFORE C3 and C4 repair
   anything.
8. Every gate runs at a commit STRICTLY EARLIER than C7. G1's second STOP
   reading is the sole exception, taken immediately before C7.
9. Destructive verification runs ONLY inside a disposable worktree under
   `.remedy-wt/`. The primary checkout reads `git status --porcelain` empty
   after every commit.
10. NO TYPESCRIPT MUTATION RED-PROOF IS ORDERED; the GATER16 entry of
    `.agent/live_review.md` records why every route is blind or a startup error.
11. WRITE NO `Done:` PARAGRAPH. `Done:` is reserved for reviewer-authored text.
    Your marker for a landed fix is the `Landed:` line SPEC S5 describes.

## SPEC — the R-0725 remainder (C3)

S1. In `tests/ui_contracts/test_diff_envelope_door.py`,
`TestTheTaskRunScopeRouteAgrees::test_the_client_addresses_the_task_run_segment`
asserts `"task-runs" in client_code()` over the whole module and says nothing
about that path's ENDING. Measured by the reviewer at `a1d08610`: renaming the
task-run template's `/diff?` to `/diffs?` — leaving the job template alone —
keeps the whole guard GREEN at 39 passed, which is the same defect its two
siblings were repaired for at R18. Scope it as they were: read the body
`ts_function_body` returns for `diffEnvelopePath`, and assert the TASK-RUN
template specifically — the `task-runs` segment AND the `/diff?` ending that
follows it — in a form that renaming that template alone turns red. Change no
other assertion.

## SPEC — finding R-0726, the entry point (C4)

S2. In `apps/ui/src/components/detail/DetailPopover.tsx`, MOVE the "Open diff"
button out of the "Changed files" section and render it at POPOVER level,
after the `PromptTracePanel`. Keep its every other property: a real
`<button type="button">`, the label `Open diff`, `onOpenDiff(task.id)` passing
the task id, rendered only when there is both a resolved `task` and an
`onOpenDiff` handler, and no class.

WHY THE MOVE IS THE FIX AND NOT A PREFERENCE, which the WHY comment should say:
that section renders only when `changedFilesSafe` is a non-empty list, and
`packages/orchestration/ui_server.py` builds that list from
`patch_intent_applied` EVENTS while the diff the button opens is a separate
artifact under the job's evidence directory. The two genuinely diverge, so the
viewer's only entry point was invisible for a task run that has a diff and no
safe file list. `docs/ui/design_reference/component_spec.md:108` also lists the
popover's buttons as a PEER of its sections rather than inside one, so this
placement is what the design reference asked for in the first place.

## SPEC — the file sidebar (C5)

S3. A NEW component `apps/ui/src/components/diff/DiffFileSidebar.tsx`. It takes
the envelope and draws `buildDiffFileSummaries` of it — one entry per file, in
the model's order, DERIVING NOTHING, the same division `DiffView.tsx` states in
its own header. Each entry shows the file's `path`, its `status`, its `added`
and `deleted` counts, its `hunkCount`, its `oldPath` when the file carries one
(a rename's old name is the reader's only way to recognise the file), and its
`note` when it carries one. Each entry is a `<button type="button">` whose click
moves the reader to that file's row, keyed on the summary's own `rowKey` and
never on a path or an index this component computes. Per constraint 5 the markup
carries no class. An envelope with no files renders no list and says so in plain
words rather than an empty container.

S4. In `apps/ui/src/components/diff/DiffView.tsx`, give the FILE row a DOM
anchor so the sidebar has something to move to: the file row's element takes
`id={row.key}` beside the React `key` it already has. Those are two different
things and the WHY comment should say so — the React key is reconciliation and
never reaches the DOM, and `buildDiffFileSummaries` puts the SAME string in
`rowKey` precisely so the two halves agree without either recomputing it. Change
nothing else in that file.

S5. `RemedyShell.tsx` renders `DiffFileSidebar` beside `DiffView`, inside the
existing diff panel and under the same `available` condition, so the sidebar and
the body appear and disappear together.

For each of C3 and C4, append to `.agent/live_review.md` in that SAME commit one
line of your own wording, in exactly this form and nothing else:
`Landed: R-XXXX — <one sentence: what changed, and the commit>`.

## SPEC — the guard (C6)

S6. A NEW file `tests/ui_contracts/test_diff_file_sidebar.py`, reading
`DiffFileSidebar.tsx`, `DiffView.tsx` and `RemedyShell.tsx` AS TEXT, importing
nothing from `apps/`, every assertion over COMMENT-STRIPPED source, reusing the
`strip_ts_comments` shape of `test_diff_view_render.py`. SCOPE EVERY ASSERTION
TO A FUNCTION BODY OR AN ELEMENT TAG rather than to a whole file — that is
finding `R-0725`'s rule, and this guard is written after it. Assertions:
(a) a NOT-VACUOUS class first, in the shape `TestTheStripperIsNotVacuous` of
    `test_diff_view_render.py`: the stripper removes both comment forms, each
    file really loses text to it, and each scanner finds its subject;
(b) the sidebar calls `buildDiffFileSummaries` and reimplements no rule of the
    model — it must not name `.hunks.length`, `.stats.`, or `sort(`, which are
    the model's own derivations arriving under another name;
(c) every field S3 names is really read by the sidebar: `path`, `status`,
    `added`, `deleted`, `hunkCount`, `oldPath`, `note` and `rowKey`;
(d) the sidebar's entry is a `<button` carrying `type="button"`, scoped to the
    tag that names `rowKey`;
(e) the two halves agree: the string the sidebar navigates by and the string
    `DiffView.tsx` puts in the file row's `id` are both the model's `rowKey` /
    `row.key`, and `DiffView.tsx`'s file row really carries an `id`;
(f) `RemedyShell.tsx` renders `<DiffFileSidebar` and still renders `<DiffView`.

## Slice convention

Each slice sits between a `<<<SLICE <NAME>` line and a `<<<END <NAME>` line.
Neither marker line is part of the slice, and neither is ever written into a
target file. The slices this block carries are PLANF037R19, GATER18, DONE725A
and FINDING726. PLANF037R19 is a FULL REWRITE of `.agent/plan.md`. The other
three are APPENDS to `.agent/live_review.md`, applied IN THAT ORDER in the SAME
commit: join GATER18 to the file's current bytes with exactly one newline, then
DONE725A to the result with one newline, then FINDING726 with one newline.

<<<SLICE PLANF037R19
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
R19 closes the two gaps the R18 gate found and then draws the sidebar. The
remainder of `R-0725` is the task-run path's own ending, which no assertion
pins: renaming it alone left the guard green where its two repaired siblings now
go red. `R-0726` is sharper — the "Open diff" button sat inside the "Changed
files" section, which renders only on a non-empty `changedFilesSafe`, and that
list is built from apply EVENTS while the diff is a separate artifact, so the
viewer's only entry point was invisible for a task run holding a diff and no
safe file list. The button moves to popover level, which is where
`component_spec.md:108` lists it. Then `buildDiffFileSummaries`, exported since
R15 and drawn by nothing, becomes the file sidebar.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R18 verdict, R-0725 in part, R-0726 | ordered | record first |
| C3 the R-0725 remainder | ordered | after the record |
| C4 the R-0726 repair | ordered | the entry point becomes reachable |
| C5 the file sidebar and its DOM anchor | ordered | the drawing half |
| C6 the sidebar guard | ordered | nothing here can render a component |
| C7 the handback | ordered | |

## Next Steps
1. Virtual scrolling beyond two thousand lines, which the Design section names
   and which the row list already makes possible.
2. The lazy language bundles, and the perf fixture whose numbers Acceptance
   requires recorded.
3. A ruling on the sidebar's visual treatment: the Design names "paths + stats
   bars", the binding CSS defines neither, so R19 ships semantics only.

## Risks
- Round 19 of a 25-round soft limit, session 5 of 7. Virtual scrolling, the lazy
  bundles, the perf fixture and the sidebar's styling remain.
- Nothing in this repository renders a `.tsx` file, so every guard here reads
  text and `tsc --noEmit` does the rest.
<<<END PLANF037R19

<<<SLICE GATER18
Gate: F037 R18 — the round that mounted the viewer and repaired the reviewer's own guard. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran it independently at `0a291411`. RE-MEASURED, NOT ACCEPTED. The committed C0a blob is 29389 bytes, 385 lines, sha256 `42f16726baf7983cccab6f0dc17529c69a5f2f0a0dd9a558977792f0fffbb81b`, BYTE EQUAL to the reviewer's own scratch original `.remedy-wt/f037-r18-block.md`, so the chain covers the emission and not only the worker's self-consistency; at C0b both paths are one blob. Caps: CONTENT 55, TOTAL 385, PROSE 330. The plan at `a684321e` is byte equal to PLANF037R18 including its trailing newline, negative control False, 49 lines, one `## Goal`, one `## Next Steps`. Per-commit insertions over `5a4d5257..0a291411` are 385, 289, 26, 8, 45, 18, 67, 363 and 265, every one under five hundred and every one matching the `+/-` column of the handback's `## Commits` table cell by cell. The ledger at the tip reads 286 registered ids all distinct, 34 `Done:` lines, 2 `Landed:` lines, 88 `Gate:` entries and an open set of 253 by the reading §3 item 10 prescribes. RE-RUN SUITES, primary checkout, one process at a time, every one exit 0: `tests/ui_contracts/` 630 passed 4 skipped against 616 at base; `tests/ui_server/` 495 passed; `tests/regression/test_named_bugs.py` 64 passed 6 skipped; `tests/docs/` 295 passed; the canary 42 passed; and the typescript node 1 passed 73 deselected, PASSED and not skipped, which is most of this round's gate because the round is almost entirely `.tsx`. CONSTRAINTS 3 AND 4 HELD MECHANICALLY: `git diff --stat` over `apps/ui/src/api/` and over `packages/` is EMPTY for the whole range.

THE REPAIR OF `R-0725` WAS PROVED BY THE REVIEWER RATHER THAN ACCEPTED, in a disposable worktree at `a1d08610`, control exit 0 at 39 passed before and after every case. The two mutations that were GREEN at the pre-round base are now RED at exit 1, each on exactly the assertion that was blind: renaming the JOB path template alone, and replacing the try branch's `readDiffEnvelope` call with a bare cast while leaving the import and the catch branch in place. Replacing the CATCH branch's call instead is ALSO red, so both exits are covered rather than one. The worker's deviation 2 is the reason the second of those bites: SPEC S1(b) as the reviewer wrote it ordered the assertion scoped to `loadDiffEnvelope`'s BODY, and a body-wide reading would have stayed GREEN because the catch branch's own call survives inside that body — the worker measured this, split the body at `} catch` and required the reader in BOTH exits, which is strictly stronger than what it was told to do. The reviewer's spec would have shipped a gate that could not fail, and the round caught it before it landed.

TWO GAPS THE ROUND LEAVES OPEN, BOTH THE REVIEWER'S OWN AND BOTH REGISTERED BELOW RATHER THAN CARRIED FORWARD. The first is the REMAINDER of `R-0725`, found by a reviewer probe the R18 block did not order: renaming the TASK-RUN template's `/diff?` ending alone leaves the whole guard GREEN at 39 passed, because that path's assertion tests only the `task-runs` segment and does so over the whole module. It is resolved in part below and its remainder named, on the precedent `R-0721` set in this same record. The second is `R-0726`, which the WORKER raised as its deviation 3 rather than deciding it: the entry point it was told to place inside the "Changed files" section inherits that section's condition. Both are the reviewer's defects, and in each the worker did the right thing — it declared the conflict and left the ruling where it belongs.
<<<END GATER18

<<<SLICE DONE725A
Done: R-0725 — RESOLVED IN PART at F037 R18 by that round's C3, and the remaining part is named rather than left implied. `tests/ui_contracts/test_diff_envelope_door.py` at `a1d08610` no longer asserts either repaired property over the whole module: the job-scope assertion reads the body `ts_function_body` returns for `diffEnvelopePath` and pins `/api/jobs/${job}/diff?` inside it, and the reader assertion reads `loadDiffEnvelope`'s body, splits it at `} catch` and requires `readDiffEnvelope` in BOTH exits — which is more than the block ordered and is what makes it bite, since the catch branch's own call would otherwise satisfy a body-wide check. A vacuity test was added beside them proving `ts_function_body` really returns less than the whole module and does not reach `loadRemedyDashboard`, so the scoping cannot silently come undone. MEASURED BY THE REVIEWER in a disposable worktree at `a1d08610`, control exit 0 at 39 passed before and after: renaming the job template alone is now exit 1, replacing the try branch's reader call is exit 1, and replacing the catch branch's call instead is also exit 1 — the three readings the repair exists to produce. THE REMAINDER, and why it is not this paragraph's to close: `TestTheTaskRunScopeRouteAgrees::test_the_client_addresses_the_task_run_segment` still asserts `"task-runs" in client_code()` over the whole module and says nothing about that path's ENDING, so renaming the task-run template's `/diff?` to `/diffs?` while leaving the job template alone keeps the guard GREEN at 39 passed — measured in the same worktree at the same commit. That is this finding's own class surviving in the one assertion the R18 block did not name, because the reviewer's S1 named the two sites it had measured rather than the class it had found. It is scoped like its siblings by C3 of F037 R19, whose ordering constraint 7 puts that commit after this record. This is the SECOND resolution paragraph this id will carry, on the precedent `R-0721` set in this record; the first is above.
<<<END DONE725A

<<<SLICE FINDING726
- R-0726 — Medium, THE DIFF VIEWER'S ONLY ENTRY POINT WAS RENDERED INSIDE A SECTION WHOSE CONDITION IS AN UNRELATED FIELD, SO A TASK RUN WITH A DIFF AND NO SAFE FILE LIST OFFERS NO WAY IN. Raised by the WORKER as deviation 3 of F037 R18, which declared the conflict and explicitly declined to decide it, and registered here with the measurement the reviewer then took. The defect is the REVIEWER'S: SPEC S3 of the R18 block ordered the button rendered "ONLY when there is both a resolved `task` and an `onOpenDiff` handler" and, in the same item, ordered it placed "in the existing Changed files section" — two clauses that cannot both hold, because that section is itself guarded by `changedFiles && changedFiles.length > 0`. The worker obeyed the placement, kept both of S3's own conditions, and said so. MEASURED AT `a1d08610`: `apps/ui/src/components/detail/DetailPopover.tsx` renders the button inside that guarded section, and `packages/orchestration/ui_server.py` builds the list behind it in `_task_changed_files_safe`, which collects filenames from `patch_intent_applied` EVENTS and caps them at ten — while the diff the button opens is a separate artifact read by `build_diff_view` from the job's evidence directory. The two are produced by different mechanisms and genuinely diverge, so the condition gating the entry point is not a proxy for "this task run has a diff". MEDIUM AND NOT LOW because the effect is that F037's entire client surface — the door of R17, the mount of R18, the rendering core of R16 — is UNREACHABLE in that state, and this is the feature's only entry point; the R18 mount guard asserts that the button EXISTS in the source and cannot see the condition it renders under, so no gate in this repository would notice. MEDIUM AND NOT HIGH because nothing false is displayed, no data is wrong, and the state is a subset of task runs rather than all of them. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED (§3 item 30): the nearest neighbour is the R-0220 lesson that a green gate is not a working feature and that the CALLERS of new code must be checked, which is the same family but is a standing habit rather than an open finding, and `R-0725` is about an ASSERTION's scope rather than a rendered condition, so this takes its own id. THE FIX, which C4 of F037 R19 lands under that block's ordering constraint 7: the button moves to POPOVER level, after the prompt-trace panel, keeping every other property S3 gave it. That is also where `docs/ui/design_reference/component_spec.md:108` puts it, listing the popover's buttons as a peer of its sections rather than inside one — so the design reference had already answered this and the reviewer's placement instruction contradicted it. OPEN.
<<<END FINDING726

## Done when — the gates

Run every gate yourself and record its REAL exit code and REAL summary line.
"Green" as a word is a finding. One line per gate in the handback.

G1 HYGIENE. Read `.agent/STOP` from disk before C0a and again immediately before
C7; report ABSENT or PRESENT each time, and on PRESENT stop after the commit in
hand and hand off. `git rev-parse` before C0a must equal `0a291411`. Report
`git branch --show-current`. Report the `git status --porcelain` line count
after each of C0a through C6; each must be 0.

G2 TRANSPORT, one digest comparison. Report the byte count, line count and
sha256 of the committed C0a blob and compare all three against the three
readings the delegation named. Then report whether
`git rev-parse <C0b>:.agent/authored/f037-r19.md` and
`git rev-parse <C0b>:.agent/last_block.md` are the same blob.

G3 EXTRACTION AND CAPS, on the committed C0a blob. Report the content line count
of PLANF037R19, GATER18, DONE725A and FINDING726, their sum as CONTENT, the
blob's line count as TOTAL, and TOTAL minus CONTENT as PROSE. Report
TOTAL <= 490 and PROSE <= 400.

G4 THE PLAN AT C1. Extract PLANF037R19 from the committed C0a blob
programmatically. Report byte equality with `git show <C1>:.agent/plan.md`
INCLUDING the trailing newline, and the negative control against the slice minus
its trailing newline, which must be False. Report `wc -l`, strictly under 50,
and the count of lines exactly `## Goal` and exactly `## Next Steps`, each 1.

G5 THE RECORD AT C2. Extract the three record slices from the committed C0a
blob. Report reader (a): the pre-round blob
`git show 0a291411:.agent/live_review.md` plus one newline plus GATER18 plus one
newline plus DONE725A plus one newline plus FINDING726 equals
`git show <C2>:.agent/live_review.md`. Report reader (b): the last N
blank-line-separated units of the committed file equal the three slices' N units
IN ORDER, N counted by your script across all three. Report a negative control
for each reader flipping one byte inside the FIRST appended paragraph — that is
GATER18's first paragraph; both must be False. Report that the pre-round blob is
a byte PREFIX of the committed one. Then report, line-anchored over the
committed file, with the figure at `0a291411` beside each: `^- R-\d+ — ` (286 at
base), `^Done: R-\d+ — ` (34), `^Landed: R-` (2), `^Gate: F\d+ R\d+ — ` (88),
the open set as registered ids minus ids named by a `Done:` line (253 at base),
and whether every registered id is distinct. R-0726 is the only id this round
registers. `^Landed: R-` becomes 3 at C3 and 4 at C4.

G6 THE RED-PROOFS OF THE PYTHON GUARDS. All runs in a disposable worktree at the
C6 tree, `__pycache__` purged before every run, `python3 -B` throughout. Report
the UNMUTATED control for
`tests/ui_contracts/test_diff_envelope_door.py tests/ui_contracts/test_diff_file_sidebar.py tests/ui_contracts/test_diff_viewer_mount.py tests/ui_contracts/test_diff_view_render.py`
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
(a) THE C3 REPAIR'S OWN PROOF: in `remedyApi.ts`, rename the TASK-RUN path
    template's `/diff?` to `/diffs?`, leaving the job template untouched. This
    was GREEN before C3 and must now be RED.
(b) in `remedyApi.ts`, rename the JOB template's `/diff?` alone — still RED,
    which shows C3 did not repair one sibling by breaking another.
(c) THE C4 REPAIR'S OWN PROOF: in `DetailPopover.tsx`, move the button back
    inside the `changedFiles` section. The C6 guard must catch this, so if it
    comes back GREEN say so plainly — that is a true finding about the guard and
    the reviewer wants the true reading, not an adjusted test.
(d) in `DiffFileSidebar.tsx`, replace the `buildDiffFileSummaries` call with a
    direct walk of `envelope.files`.
(e) in `DiffFileSidebar.tsx`, navigate by the file's `path` instead of its
    `rowKey`.
(f) in `DiffView.tsx`, delete the file row's `id` attribute, leaving its React
    `key`.
Each of (a), (b), (d), (e) and (f) must be exit 1.

G7 SUITES, TYPES, LINT AND CANARY AT C6, primary checkout, ONE pytest process at
a time. Report exit code and summary line for each, with the base figure beside
it: `python3 -m pytest tests/ui_contracts/ -q` (630 passed, 4 skipped at base),
`python3 -m pytest tests/ui_server/ -q` (495 passed),
`python3 -m pytest tests/regression/test_named_bugs.py -q` (64 passed, 6
skipped), `python3 -m pytest tests/orchestration/test_test_runner.py -q` (52
passed), `python3 -m pytest tests/docs/ -q` (295 passed),
`python3 -m ruff check tests/ui_contracts/test_diff_file_sidebar.py tests/ui_contracts/test_diff_envelope_door.py`,
and the canary `python3 -m pytest tests/cli/test_golden_path.py -q` (42 passed).
State explicitly whether the typescript node inside `tests/ui_server/` PASSED or
SKIPPED — it skips only when `apps/ui/node_modules/.bin/tsc` is absent, and a
skip means this round's three `.tsx` files were never type-checked, which is
most of this round's gate.

G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C6. Report
`git diff --name-only 0a291411..<C6>` and set-difference it BOTH ways against
the Change set; ACTUAL MINUS EXPECTED must be empty and EXPECTED MINUS ACTUAL
must be `.agent/handoff.md` alone. Report `git diff --stat` restricted to
`packages/`, which must be EMPTY, and to `apps/ui/src/api/`, which must ALSO be
EMPTY — that is constraint 3 made mechanical. Report each commit's insertion
count from `git show --numstat`, each under 500, and confirm each matches the
`+/-` column of your own `## Commits` table cell by cell. Report the count of
lines matching `^<<<SLICE ` and `^<<<END ` in `.agent/plan.md`,
`.agent/live_review.md`, `apps/ui/src/components/diff/DiffFileSidebar.tsx` and
`tests/ui_contracts/test_diff_file_sidebar.py` — each must be 0 — with a CONTROL
count over the C0a blob, which must be non-zero. Report
`git ls-files .remedy-wt | wc -l`, which must be 0. Report
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

## Handback

Rewrite `.agent/handoff.md` at C7 per docs/agents/handback_template.md. It has no
length cap. It must carry: the Session line naming SESSION 5 of F037 and round
19; the review range; a `## Commits` section with one `+/-` table per commit; the
external actions; one Verification line per gate G1 through G8 with real exit
codes; the authored-text proofs; the deviations and assumptions; the item-status
table covering every C and every G exactly once; and the next expected action.
Derive the handback's own tier from AGENTS.md rather than from any number here.
