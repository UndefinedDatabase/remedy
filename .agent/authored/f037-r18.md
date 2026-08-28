# STEP T003 (second round) — F037 Rendered diff viewer, round 18

BASE: `5a4d5257`. SESSION 5 of feature F037. This block carries no line that is a
run of a single repeated character, so nothing in its frame has a length a reader
must recover by eye.

## Goal

Make the viewer REAL. The "Open diff" button that
`docs/ui/design_reference/component_spec.md:113-116` puts in `DetailPopover`
starts emitting `onOpenDiff(taskId)`, `RemedyShell` holds which task run is open
and fetches its envelope through the door R17 built, and `DiffView` — on disk
since R16 and mounted by nothing — is finally drawn. The round also repairs
finding `R-0725`, which the reviewer raised against R17's own guard.

## Bundle

- C0a save this block verbatim to `.agent/authored/f037-r18.md`.
- C0b mirror the same bytes into `.agent/last_block.md`.
- C1 rewrite `.agent/plan.md` from the PLANF037R18 slice.
- C2 append the GATER17 and FINDING725 slices to `.agent/live_review.md`.
- C3 repair `R-0725`: SPEC S1, plus the `Landed:` line SPEC S2 describes.
- C4 the entry point: SPEC S3 in `apps/ui/src/components/detail/DetailPopover.tsx`.
- C5 the mount: SPEC S4 through S6 in
  `apps/ui/src/components/shell/RemedyShell.tsx`.
- C6 the guard: SPEC S7 in `tests/ui_contracts/test_diff_viewer_mount.py`, a NEW
  file.
- C7 rewrite `.agent/handoff.md` as the handback.

## Change set

Exactly these paths, and nothing outside them:

- `.agent/authored/f037-r18.md` (new)
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `tests/ui_contracts/test_diff_envelope_door.py`
- `apps/ui/src/components/detail/DetailPopover.tsx`
- `apps/ui/src/components/shell/RemedyShell.tsx`
- `tests/ui_contracts/test_diff_viewer_mount.py` (new)
- `.agent/handoff.md`

Push the branch after C7 with `git push -u origin feature/f037-rendered-diff-viewer`.
Create no PR. Merge nothing. Rewrite no history.

## Constraints

1. Apply every slice BYTE FOR BYTE. Do not edit, reflow, correct or re-wrap a
   slice, and never write a `<<<SLICE` or `<<<END` marker line into a target
   file. If a slice looks wrong, apply it anyway and declare it in the handback.
2. The SPEC items describe PRODUCTION CODE and are not slices. Write that code
   yourself, in this repository's idiom. The WHY comments are yours to word.
3. `apps/ui/src/api/remedyApi.ts`, `apps/ui/src/api/diffViewModel.ts` and
   `apps/ui/src/components/diff/DiffView.tsx` are NOT edited this round. This
   round MOUNTS what they already export and changes none of them. If the mount
   seems to need a change inside one of them, stop and declare it rather than
   making it.
4. Nothing under `packages/` changes.
5. FOUR GUARDS ALREADY BIND `DetailPopover.tsx` AND YOU MUST NOT BREAK THEM.
   `tests/ui_contracts/test_ux_quality.py` requires the string
   `remedy-detail-compact` to survive and forbids, case-insensitively, the words
   `rank`, `importance`, `node_type`, `present signals`, `missing signals` and
   `zone` anywhere in that file — mind this when wording a button label or a
   comment. `tests/ui_contracts/test_design_drift.py` requires `Result` and
   forbids `Next safe action` and `next.command`.
   `tests/ui_server/test_dashboard_contract.py` requires `blockedReason`,
   `completedAt` and a changed-files field, and forbids `@mui` in both this file
   and `RemedyShell.tsx`. `tests/regression/test_named_bugs.py` requires
   `remedy-detail-compact` again.
6. No new npm dependency, no new config file, no new CSS file, and no change to
   `apps/ui/src/styles/tokens.css`. `DiffView.module.css` already carries the
   diff surface and amendment A5 of `docs/roadmap/features/T5_F037.md` fixes its
   vocabulary; a layout class for the panel is NOT authorised by this round, so
   the panel's wrapper is an unclassed landmark exactly as `DiffView`'s own root
   is, and you say so in a comment beside it.
7. Order the commits exactly C0a, C0b, C1, C2, C3, C4, C5, C6, C7. C1 is the
   first substantive commit, which is what keeps `.agent/plan.md` true before
   every later commit's gate. C2 persists the finding BEFORE C3 repairs it.
8. Every gate below runs at a commit STRICTLY EARLIER than C7, so the handback
   can quote all of them. G1's second STOP reading is the sole exception and is
   taken immediately before C7 is written.
9. Destructive verification runs ONLY inside a disposable worktree under
   `.remedy-wt/`. The primary checkout reads `git status --porcelain` empty
   after every commit.
10. NO TYPESCRIPT MUTATION RED-PROOF IS ORDERED and this round does not retry
    the route; the GATER16 entry of `.agent/live_review.md` records why every
    variant is either blind or a startup error. The `.tsx` layer is covered by
    `tsc --noEmit` and by text guards, and by nothing else.

## SPEC — the repair of finding R-0725 (C3)

S1. In `tests/ui_contracts/test_diff_envelope_door.py`, scope the two
WHOLE-FILE presence assertions to the function whose behaviour they exist to
pin, using the `ts_function_body` helper THAT FILE ALREADY DEFINES and already
uses correctly for the token and the catch clause. Change no other assertion.
(a) `TestTheJobScopeRouteAgrees::test_the_client_addresses_the_diff_endpoint`
    reads the body of `diffEnvelopePath` rather than the whole module, and
    asserts the JOB-scope path specifically — the literal `/api/jobs/` followed
    by the interpolated job id and then `/diff?` — in a form that a rename of
    the job template alone turns red;
(b) `TestTheDoorNormalizesThroughOneFunction::test_every_payload_leaves_the_door_through_the_reader`
    reads the body of `loadDiffEnvelope` rather than the whole module, so the
    `import` line naming `readDiffEnvelope` can no longer satisfy it.
Add to `TestTheStripperIsNotVacuous` one test proving the SCOPING is real: the
body `ts_function_body` returns for `diffEnvelopePath` is strictly shorter than
the whole module and does not contain the string `loadRemedyDashboard`. Without
it, a helper that silently returned the whole file would restore the very defect
this repair removes.

S2. Append to `.agent/live_review.md`, in the SAME commit as S1, one line of
your own wording in exactly this form and nothing else:
`Landed: R-0725 — <one sentence: what changed, and the commit>`.
Write NO `Done:` paragraph. `Done:` is reserved for reviewer-authored text, and
a surviving `Landed:` line is exactly what an unreviewed fix should look like.

## SPEC — the entry point (C4)

S3. `apps/ui/src/components/detail/DetailPopover.tsx` takes a new OPTIONAL prop
`onOpenDiff?: (taskId: string) => void` and renders a button that calls it. The
button:
(a) is a real `<button type="button">`, for the reason the hunk head is one —
    `tests/ui_contracts/test_diff_view_render.py` pins that rule for this
    feature's other control;
(b) renders ONLY when there is both a resolved `task` and an `onOpenDiff`
    handler, so a popover opened on a node that carries no task run, or mounted
    by a caller that does not handle the event, shows no control that would do
    nothing;
(c) carries the label `Open diff`, which is the label
    `docs/ui/design_reference/component_spec.md:108` names;
(d) passes `task.id` — the task id, which is what `onOpenDiff(taskId)` means in
    `component_spec.md:113-116` and what the server's task-run route keys on.
Place it in the existing "Changed files" section, which is the section about the
change it opens. Keep every string constraint 5 lists.

## SPEC — the mount (C5)

All of S4 through S6 land in `apps/ui/src/components/shell/RemedyShell.tsx`.

S4. State: which task run's diff is open, as `string | null`, starting `null`;
and the envelope last read, as `DiffEnvelope | null`, starting `null`. Pass a
handler to `DetailPopover` that sets the first.

S5. The read. When the open task id becomes non-null, call `loadDiffEnvelope`
from `../../api/remedyApi` with `jobId` `dashboard.jobId`, `token` the shell's
own `serverToken` prop, and `taskId` the open id, and store what it resolves to.
Use an effect keyed on the open task id. TWO PROPERTIES THE EFFECT MUST HAVE,
both because a viewer that lies is worse than one that is slow: a response that
arrives after the open task id has changed again is DISCARDED rather than shown
under the new task, and closing the panel clears the stored envelope so the next
open cannot flash the previous task's diff. `loadDiffEnvelope` never throws, so
no error branch is needed and none is written.

S6. The drawing. When a task is open, render `DiffView` with the envelope, in an
unclassed wrapper per constraint 6, together with a control that closes the
panel by setting the open task id back to `null`. Until the envelope arrives the
panel says so in plain words rather than rendering an empty `DiffView`; an
envelope whose `available` is false says THAT, and names its `reason` when the
envelope carries one, because `readDiffEnvelope` guarantees both fields exist.

## SPEC — the guard (C6)

S7. A NEW file `tests/ui_contracts/test_diff_viewer_mount.py`. It reads
`DetailPopover.tsx`, `RemedyShell.tsx` and `DiffView.tsx` AS TEXT, imports
nothing from `apps/`, and runs every assertion over COMMENT-STRIPPED source —
reuse the `strip_ts_comments` shape of `test_diff_view_render.py`. SCOPE EVERY
ASSERTION TO A FUNCTION BODY OR AN ELEMENT TAG rather than to a whole file, for
the reason finding `R-0725` records; a whole-file `in` check is what that
finding is about, and this guard is written after it. Assertions:
(a) a NOT-VACUOUS class first, in the shape `TestTheStripperIsNotVacuous` of
    `test_diff_view_render.py`: the stripper removes both comment forms, each of
    the three components really loses text to it, and each scanner below finds
    its subject on both sides;
(b) `DetailPopover` declares the `onOpenDiff` prop and its button is a
    `<button` carrying `type="button"` — scoped to the tag that names
    `onOpenDiff`, not to the file, which already holds a close button;
(c) the popover's button passes the TASK id and not the node id: the tag naming
    `onOpenDiff` also names `task.id`, and does not name `selectedNode`;
(d) `RemedyShell` imports `DiffView` and `loadDiffEnvelope` and really renders
    `<DiffView`, and passes an `onOpenDiff` to `DetailPopover`;
(e) the stale-response rule of S5 is IN THE CODE: the effect body naming
    `loadDiffEnvelope` also carries a cancellation flag it checks before storing,
    and returns a cleanup function. Assert the shape you actually wrote, and if
    you cannot assert it without pinning a variable name, pin the name and say
    so in the docstring;
(f) `DiffView.tsx` is not edited by this round: assert it still names
    `buildDiffRowModels`, `defaultCollapsedHunkIds`, `toggleHunkCollapse` and
    `splitLineIntoIntralineSegments`, which is constraint 3 made mechanical.

## Slice convention

Each slice below sits between a `<<<SLICE <NAME>` line and a `<<<END <NAME>`
line. Neither marker line is part of the slice, and neither is ever written into
a target file. The slices this block carries are PLANF037R18, GATER17 and
FINDING725. PLANF037R18 is a FULL REWRITE of `.agent/plan.md`. GATER17 and
FINDING725 are APPENDS to `.agent/live_review.md`, applied in that order in the
SAME commit: join GATER17 to the file's current bytes with exactly one newline,
then join FINDING725 to the result with exactly one newline.

<<<SLICE PLANF037R18
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
R18 makes the viewer real. `DiffView` has been on disk since R16 and mounted by
nothing; this round opens the door to it. `DetailPopover` grows the "Open diff"
button `component_spec.md` names, emitting `onOpenDiff(taskId)`; `RemedyShell`
holds which task run is open, reads its envelope through the door R17 built, and
draws `DiffView` behind it. A response arriving after the selection changed is
discarded rather than shown under the wrong task. The round also repairs finding
`R-0725`, the reviewer's own: two presence assertions in R17's cross-language
guard searched the whole module where they meant one function, so renaming the
job path alone, or replacing the reader call while keeping its import, left the
guard green.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R17 verdict and finding R-0725 | ordered | findings persist first |
| C3 the R-0725 repair | ordered | after the record, before the new work |
| C4 the entry point in DetailPopover | ordered | the button the spec names |
| C5 the mount in RemedyShell | ordered | state, read, drawing |
| C6 the mount guard | ordered | nothing here can render a component |
| C7 the handback | ordered | |

## Next Steps
1. The file sidebar over `buildDiffFileSummaries`, which the model already
   exports and nothing yet draws.
2. Virtual scrolling beyond two thousand lines, the lazy language bundles, and
   the perf fixture whose numbers Acceptance requires recorded.

## Risks
- Round 18 of a 25-round soft limit, session 5 of 7. The sidebar, the virtual
  scrolling, the lazy bundles and the perf fixture remain, so a round closing
  none of them is the one to stop and re-scope after.
- Nothing in this repository renders a `.tsx` file. This round's wiring is
  covered by `tsc --noEmit` and by text guards, and by nothing else — which is
  why the guard scopes to function bodies rather than to files.
<<<END PLANF037R18

<<<SLICE GATER17
Gate: F037 R17 — the round that opened T003 by building the diff envelope door in the api client. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran it independently at `5a4d5257` rather than reading the handback's numbers. RE-MEASURED, NOT ACCEPTED. The committed C0a blob `git show 02a1686f:.agent/authored/f037-r17.md` is 25246 bytes, 362 lines, sha256 `4dcbeecf2ac614c28f55206d91447fe5779b3f7c9560f9b362e4303959d42fa9`, and is BYTE EQUAL to the reviewer's own scratch original `.remedy-wt/f037-r17-block.md`, so under docs/agents/self_drive_protocol.md this chain covers the emission itself and not only the worker's self-consistency; at C0b `.agent/authored/f037-r17.md` and `.agent/last_block.md` are one blob `a0a8dc82`. Caps: CONTENT 49, TOTAL 362, PROSE 313, both bounds held. `.agent/plan.md` at `637c2822` is byte equal to PLANF037R17 including its trailing newline, negative control False, 46 lines, one `## Goal`, one `## Next Steps`. The GATER16 append satisfies reader (a) and reader (b) at a script-counted N of 2, both negative controls placed on the FIRST appended paragraph are False, and the base blob is a byte prefix. Per-commit insertions over `44a8493b..5a4d5257` are 362, 339, 23, 4, 149, 245 and 201, every one under five hundred and every one matching the `+/-` column of the handback's `## Commits` table cell by cell. RE-RUN SUITES, primary checkout, one process at a time, every one exit 0: `tests/ui_contracts/` 616 passed 4 skipped against 603 at base, the difference being this round's 13 new tests and nothing else; `tests/orchestration/test_test_runner.py` 52 passed; `tests/docs/` 295 passed; the typescript node 1 passed 73 deselected, PASSED and not skipped, so `tsc --noEmit` really type-checked the new door; ruff `All checks passed!`; the canary 42 passed. The new vitest `describe` was confirmed EXECUTED rather than merely shipped: run with the repository's own config against `src/api/remedyApi.test.ts`, all eight of its assertions report a passing line by name and the file totals 64 passed.

THE OPEN-SET DISCREPANCY THE WORKER FLAGGED IS RESOLVED, AND THE WORKER WAS RIGHT TO FLAG IT RATHER THAN CHOOSE A NUMBER QUIETLY. Measured at `f63d1d15`: the registered set holds 285 ids, all distinct; there are 34 `Done:` lines but only 33 DISTINCT ids among them, because `R-0721` legitimately carries TWO resolution paragraphs — a partial one at F037 R12 and the remainder at R14, the second saying so in its own words; and the single `Landed:` line names `R-0711`, which also has a `Done:` paragraph. So the subtraction 285 minus 34 minus 1 double-counts twice and yields 250, while the SET reading — registered ids minus ids named by a `Done:` line — yields 252 at the base and at C2 alike. The set reading is the one §3 item 10 of docs/agents/planner_reviewer_prompt.md prescribes, and 252 is the open count of record.

THE REVIEWER'S OWN RED-PROOFS WENT WHERE THE BLOCK'S DID NOT, and this is what produced finding `R-0725` below. The block's four mutations were all on the CLIENT side plus `DiffView.tsx`, so the SERVER half of a guard whose entire purpose is a cross-language agreement was never proved. Measured in a disposable worktree at `91f7d8bd`, control exit 0 at 25 passed before and after: renaming the handler key `"diff": _build_diff_json`, renaming `parts[4] == "task-runs"`, and renaming `parts[6] == "diff"` in `packages/orchestration/ui_server.py` each turn the guard RED at exit 1 on exactly the intended node, so the server half really bites. A SCOPING CONTROL was run too, and it is the reading that matters most: dropping the token parameter from `loadRemedyDashboard` ALONE leaves the guard GREEN at 25 passed, which proves `TestTheTokenTravelsOnTheDiffRoute` really is scoped to `diffEnvelopePath`'s body rather than swept over the module. Two assertions were then found NOT to have that scoping, which is `R-0725`.
<<<END GATER17

<<<SLICE FINDING725
- R-0725 — Low, TWO PRESENCE ASSERTIONS IN THE CROSS-LANGUAGE DIFF GUARD SEARCH THE WHOLE MODULE WHERE THEY MEAN ONE FUNCTION, SO A SECOND OCCURRENCE ELSEWHERE IN THE FILE SATISFIES THEM. Raised by the reviewer at the F037 R17 gate, by mutations the R17 block did not order. The defect is the REVIEWER'S OWN: items S7(a) and S7(d) of the R17 block ordered exactly the whole-file wording that landed, the worker implemented what it was given, and its handback declared the scoping it DID apply elsewhere. MEASURED IN A DISPOSABLE WORKTREE AT `91f7d8bd`, unmutated control exit 0 at 25 passed before and after every case. FIRST, `TestTheJobScopeRouteAgrees::test_the_client_addresses_the_diff_endpoint` asserts `"/diff?" in client_code()` over the whole of `apps/ui/src/api/remedyApi.ts`, where that substring occurs TWICE — once in each path template. Renaming the JOB template alone to `/diffs?` leaves the guard GREEN at 25 passed; only renaming BOTH templates turns it red. SECOND, `TestTheDoorNormalizesThroughOneFunction::test_every_payload_leaves_the_door_through_the_reader` asserts `"readDiffEnvelope" in client_code()` over the same whole module, where that name occurs four times. Replacing the real call `return readDiffEnvelope(payload);` with a bare `return payload as DiffEnvelope;` — which removes the totalisation the whole door exists to perform — leaves the guard GREEN at 25 passed, because the `import` line still names the symbol. THE SECOND IS THE SHARPER ONE: that class's own docstring says the property "is a property of the CODE, and the door's comment claiming it is exactly what this assertion must not be satisfied by", and the assertion is instead satisfied by an import, which is the same defect one layer over from the one it names. WHY LOW AND NOT MEDIUM: vitest backstops both by exact-value assertions — the job path is compared against a full literal string, and a raw cast makes `available` undefined where `toBe(false)` is expected — so neither defect could ship silently, and nothing on disk under `apps/` or `packages/` is wrong. It is a finding rather than a prose slip under operator amendment amend0827-process-diet rule 2 because it is a gate over production code demonstrably blind, and the file states a reach it does not have. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED (§3 item 30): `R-0613` is the nearest neighbour, a gate forbidding three operation words that never named the reflog FIELD they had to appear in, and `R-0630` requires a count over a self-quoting record file to name its anchor — both are about a REVIEWER-ORDERED gate's wording and route their fixes to `docs/agents/planner_reviewer_prompt.md`, while this is a landed assertion in `tests/` with a repair in the feature's own change set, so it takes its own id on the precedent by which `R-0572` and `R-0573` were registered separately. THE FIX, which C3 of F037 R18 lands: both assertions read the body `ts_function_body` returns for the function they are about — a helper THE SAME FILE ALREADY DEFINES AND ALREADY USES CORRECTLY for the token parameter and the catch clause, which is why this is a two-line repair rather than a redesign — together with a vacuity test proving that helper really returns less than the whole module. THE GENERAL RULE, and the reason this is worth an id at all: a presence assertion naming a symbol that legitimately occurs more than once in its file pins nothing unless it is scoped to the site whose behaviour it means, and an import, a type annotation and a second call site are all such occurrences. OPEN.
<<<END FINDING725

## Done when — the gates

Run every gate yourself and record its REAL exit code and its REAL summary line.
"Green" as a word is a finding. One line per gate in the handback.

G1 HYGIENE. Read `.agent/STOP` from disk before C0a and again immediately before
C7; report ABSENT or PRESENT each time, and on PRESENT stop after finishing the
commit in hand and hand off. `git rev-parse` before C0a must equal `5a4d5257`.
Report `git branch --show-current`. Report the `git status --porcelain` line
count after each of C0a through C6; each must be 0.

G2 TRANSPORT, one digest comparison. Report the byte count, line count and
sha256 of the committed C0a blob (`git show <C0a>:.agent/authored/f037-r18.md`)
and compare all three against the three readings the delegation named. Then
report whether `git rev-parse <C0b>:.agent/authored/f037-r18.md` and
`git rev-parse <C0b>:.agent/last_block.md` are the same blob.

G3 EXTRACTION AND CAPS, measured on the committed C0a blob. Report the content
line count of PLANF037R18, of GATER17 and of FINDING725, their sum as CONTENT,
the blob's line count as TOTAL, and TOTAL minus CONTENT as PROSE. Report
TOTAL <= 490 and PROSE <= 400.

G4 THE PLAN AT C1. Extract PLANF037R18 from the committed C0a blob
programmatically — never retype it — and report whether
`git show <C1>:.agent/plan.md` is byte equal to it INCLUDING the trailing
newline. Report the negative control against that slice minus its trailing
newline; it must be False. Report the file's `wc -l` and that it is strictly
under 50, and the count of lines exactly `## Goal` and exactly `## Next Steps`;
each must be 1.

G5 THE RECORD AT C2. Extract GATER17 and FINDING725 from the committed C0a blob.
Report reader (a): the pre-round blob `git show 5a4d5257:.agent/live_review.md`
plus one newline plus GATER17 plus one newline plus FINDING725 equals
`git show <C2>:.agent/live_review.md`. Report reader (b): the last N
blank-line-separated units of the committed file equal the two slices' N units
IN ORDER, where N is a number your script COUNTS across both slices. Report a
negative control for each reader, flipping one byte inside the FIRST appended
paragraph — that is GATER17's first paragraph, not FINDING725's; both must be
False. Report that the pre-round blob is a byte PREFIX of the committed one.
Then report, line-anchored over the committed file, with the figure at
`5a4d5257` beside each: lines matching `^- R-\d+ — ` (285 at base),
`^Done: R-\d+ — ` (34), `^Landed: R-` (1), `^Gate: F\d+ R\d+ — ` (87), the open
set computed as registered ids minus ids named by a `Done:` line (252 at base),
and whether every registered id is distinct. R-0725 is the only id this round
registers, and `^Landed: R-` becomes 2 at C3, not at C2.

G6 THE RED-PROOFS OF THE PYTHON GUARDS. All runs in a disposable worktree at the
C6 tree, `__pycache__` purged before every run, `python3 -B` throughout. Report
the UNMUTATED control for
`tests/ui_contracts/test_diff_envelope_door.py tests/ui_contracts/test_diff_viewer_mount.py tests/ui_contracts/test_diff_view_render.py`
before any mutation and again after the last restore; both must be exit 0.

UNIQUENESS, PER FINDING `R-0629`, WHICH IS OPEN AND BINDING ON ANY BLOCK THAT
ORDERS A DESTRUCTIVE CONTROL. Every target below is code THIS ROUND WRITES or
repairs, so no count can exist while this block is written and the reviewer
states none. YOU take each reading: count the replaced string in the named file
before editing and report the count. If it is not 1, EXTEND the string with the
characters around it until it reads 1 in that file, report the extended string
and its count, and mutate that.

Then, one at a time, each mutation restored byte-identically to its pre-mutation
sha256 before the next, reporting the REAL exit code, the summary line and the
failing node ids:
(a) THE REPAIR ITSELF, which is the reason C3 exists: in `remedyApi.ts`, rename
    the JOB path template alone from `/diff?` to `/diffs?`, leaving the task-run
    template untouched. Before C3 this was GREEN; it must now be RED.
(b) ALSO THE REPAIR: in `remedyApi.ts`, replace the reader call inside
    `loadDiffEnvelope`'s try branch with a bare cast, leaving the `import` line
    and the catch branch's call in place. Before C3 this was GREEN; it must now
    be RED.
(c) in `DetailPopover.tsx`, change the button's `type="button"` to `type="submit"`.
(d) in `DetailPopover.tsx`, pass `selectedNode.nodeId` where the button passes
    the task id.
(e) in `RemedyShell.tsx`, delete the `<DiffView` element so the panel renders
    nothing.
(f) in `RemedyShell.tsx`, remove the stale-response guard S5 requires, so a late
    response is stored unconditionally.
Each of (a) through (f) must be exit 1. If any is GREEN, say so plainly and do
NOT adjust the test to suit it — a green mutation is a true finding about the
guard, and the reviewer wants the true reading. For (a) and (b) especially,
report the colour you measured; those two are the finding's own proof.

G7 SUITES, TYPES, LINT AND CANARY AT C6, primary checkout, ONE pytest process at
a time. Report exit code and summary line for each, with the base figure beside
it: `python3 -m pytest tests/ui_contracts/ -q` (616 passed, 4 skipped at base),
`python3 -m pytest tests/ui_server/ -q` (495 passed),
`python3 -m pytest tests/orchestration/test_test_runner.py -q` (52 passed),
`python3 -m pytest tests/regression/test_named_bugs.py -q` (64 passed, 6 skipped),
`python3 -m pytest tests/docs/ -q` (295 passed),
`python3 -m ruff check tests/ui_contracts/test_diff_viewer_mount.py tests/ui_contracts/test_diff_envelope_door.py`,
and the canary `python3 -m pytest tests/cli/test_golden_path.py -q` (42 passed).
`tests/ui_server/` and `tests/regression/test_named_bugs.py` are in this list
because constraint 5 names them as guards over the two components this round
edits. State explicitly whether the typescript node inside `tests/ui_server/`
PASSED or SKIPPED — it skips only when `apps/ui/node_modules/.bin/tsc` is
absent, and a skip means this round's `.tsx` edits were never type-checked,
which is most of this round's gate.

G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C6. Report
`git diff --name-only 5a4d5257..<C6>` and set-difference it BOTH ways against
the Change set above; ACTUAL MINUS EXPECTED must be empty and EXPECTED MINUS
ACTUAL must be `.agent/handoff.md` alone. Report `git diff --stat` restricted to
`packages/`, which must be EMPTY, and to `apps/ui/src/api/`, which must ALSO be
EMPTY — that is constraint 3 made mechanical. Report each commit's insertion
count from `git show --numstat`, each under 500, and confirm each matches the
`+/-` column of your own `## Commits` table cell by cell. Report the count of
lines matching `^<<<SLICE ` and `^<<<END ` in `.agent/plan.md`,
`.agent/live_review.md`, `apps/ui/src/components/shell/RemedyShell.tsx` and
`tests/ui_contracts/test_diff_viewer_mount.py` — each must be 0 — with a CONTROL
count over the C0a blob, which must be non-zero. Report
`git ls-files .remedy-wt | wc -l`, which must be 0. Report
`gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

## Handback

Rewrite `.agent/handoff.md` at C7 per docs/agents/handback_template.md. It has no
length cap. It must carry: the Session line naming SESSION 5 of F037 and round
18; the review range; a `## Commits` section with one `+/-` table per commit; the
external actions; one Verification line per gate G1 through G8 with real exit
codes; the authored-text proofs; the deviations and assumptions; the item-status
table covering every C and every G exactly once; and the next expected action.
Derive the handback's own tier from AGENTS.md rather than from any number here.
