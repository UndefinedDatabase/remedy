# STEP SCOPE REPORT — F037 Rendered diff viewer, round 24

BASE: `82d3d584`. SESSION 7 of feature F037, which IS the seven-session soft
limit of operator amendment amend0827-process-diet rule 6. This block carries no
line that is a run of a single repeated character, so nothing in its frame has a
length a reader must recover by eye.

## Goal

The session soft limit is reached, so this round performs the obligation that
limit creates instead of more feature work. It books the R23 verdict, resolves
`R-0731`, RULES on the remaining scope as a DECISION rather than asking anyone,
amends the feature file to match that ruling, and writes the SCOPE REPORT into
the handback. No production code and no test changes.

## Bundle

- C0a save this block verbatim to `.agent/authored/f037-r24.md`.
- C0b mirror the same bytes into `.agent/last_block.md`.
- C1 rewrite `.agent/plan.md` from the PLANF037R24 slice.
- C2 append GATER23 and DONE731 to `.agent/live_review.md`, in that order.
- C3 append DECISIOND11 to `.agent/decisions.md`.
- C4 append AMENDMENTA6 to `docs/roadmap/features/T5_F037.md`.
- C5 rewrite `.agent/handoff.md` as the handback, carrying SCOPEREPORT verbatim.

## Change set

Exactly these paths, and nothing outside them:

- `.agent/authored/f037-r24.md` (new)
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/decisions.md`
- `docs/roadmap/features/T5_F037.md`
- `.agent/handoff.md`

Push the branch after C5 with `git push -u origin feature/f037-rendered-diff-viewer`.
Create no PR. Merge nothing. Rewrite no history.

## Constraints

1. Apply every slice BYTE FOR BYTE. Never write a `<<<SLICE` or `<<<END` marker
   line into a target file. If a slice looks wrong, apply it and declare it.
2. NOTHING UNDER `apps/`, `packages/` OR `tests/` CHANGES THIS ROUND. If you
   believe a code change is needed, STOP and say so in the handback instead.
3. Every append slice goes to the END of its target file, separated from the
   text already there by exactly one newline, and no line already in any target
   is edited, reordered or deleted.
4. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and nothing is reordered. C4
   MUST follow C3: the amendment cites the decision, so a reader landing between
   them must never find the citation without its target.
5. Do NOT author any `Done:` or `Gate:` paragraph, and add no `Landed:` line.
   Everything entering `.agent/live_review.md` this round is the two slices of
   C2, applied byte for byte.
6. This round IS a permitted bookkeeping-shaped round and you should not flag it
   as a contradiction: operator amendment amend0827-process-diet rule 6 makes the
   SCOPE REPORT the obligation at the soft limit, and rule 1's ban is on a round
   whose whole change set is verdicts, registrations or corrections — C3 and C4
   are neither, and C4 lands under `docs/roadmap/`.
7. Because C4 touches `docs/roadmap/`, the docs-round gate applies and G7 orders
   `tests/docs/` for it.
8. Run every pytest command SERIALLY, one process at a time, in the primary
   checkout. No `git worktree` is needed this round; create none.

## Slices

<<<SLICE PLANF037R24
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D11.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse and
virtual scrolling. `docs/roadmap/features/T5_F037.md` holds Goal & Done, the task
slicing, the binding CSS and the design amendments A1 through A6, the last of
which records what this feature deliberately no longer ships.

## Current Step
R24 is the SCOPE REPORT round. F037 has reached session 7 of a seven-session soft
limit, so operator amendment amend0827-process-diet rule 6 makes a report the
next obligation rather than more work. This round books the R23 verdict, resolves
`R-0731`, records DECISION F037 D11 splitting the three unbuilt pieces out of the
feature, amends the feature file to say so, and writes the report into the
handback. Nothing under `apps/`, `packages/` or `tests/` is touched.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R23 verdict and one resolution | ordered | record first |
| C3 DECISION F037 D11 | ordered | the ruling, not a question |
| C4 the feature-file amendment A6 | ordered | after the decision it cites |
| C5 the handback carrying the scope report | ordered | |

## Next Steps
1. The closure sequence for F037 as amended by A6: the integration-gate round,
   then the evidence-and-zip round, then the STATUS round.
2. The split-off scope — wiring `loadDiffLanguageBundle` into `DiffView`, the
   10k-line perf measurement, and the sidebar visual ruling — wants its own
   STATUS line. That is a PROPOSAL to the operator and is not executed here.

## Risks
- A6 narrows what F037 ships. Reversing it is one paragraph in each of
  `.agent/decisions.md` and the feature file, both named in D11.
- `loadDiffLanguageBundle` has NO production caller at `82d3d584`, measured by
  the reviewer with `git grep -l`: the lazy-bundle model is complete and unwired,
  and A6 exists so that gap is stated rather than silent.
<<<END PLANF037R24

<<<SLICE GATER23
Gate: F037 R23 — the round that closed the prototype-inheritance defect and the last of `R-0730`'s stale comments. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran it independently at `82d3d584` rather than reading the handback's numbers. TRANSPORT IS REPORTED FOR EXACTLY WHAT IT COVERS, per §3 item 37: no reviewer scratch original of the R23 block survives into this session, so the chain walked here runs from the committed C0a blob to its C0b mirror and no further — the committed `.agent/authored/f037-r23.md` blob is 32100 bytes, 353 lines, sha256 `2793ac9e5c51c397364f1fd75b5bf6b4759ccdd6d003b6645eabc21b49fad185`, and at `ce7f54ce` that path and `.agent/last_block.md` are ONE blob `190eb058387b0dc0bf9574f91e33ecd12952866c`. That proves the worker was SELF-CONSISTENT and says nothing about the emitted bytes, which this workflow cannot measure and which this verdict therefore does not claim. THE RECORD MOVED EXACTLY AS THE BLOCK PREDICTED BEFORE THE ROUND RAN, every figure re-measured by the reviewer: registrations 291 to 292 and all 292 DISTINCT, `^Done: R-\d+ — ` 39 to 41, `^Gate: F\d+ R\d+ — ` 92 to 93, `^Landed: R-` 9 to 11 across `8bb2ab6a` and `4f8a9088`, and the OPEN SET computed AS A SET fell from 254 to 253. The plan at `ab85ce02` is 47 lines with exactly one `## Goal` and one `## Next Steps`, and the pre-round `.agent/live_review.md` blob is a byte PREFIX of the `b9fb06ec` blob, 1292757 bytes growing to 1306220.

THE FIX IS RIGHT, AND THE REVIEWER PROVED THE NEW GUARD IS NOT VACUOUS WITH ITS OWN RED-PROOF rather than accepting the worker's. In a disposable worktree at `82d3d584`, removed afterwards by exact path with `git worktree list` back to one line: the unmutated control is `tests/ui_contracts/test_diff_view_model.py` at 8 passed, and restoring `apps/ui/src/api/diffViewModel.ts` to its `815f7a30` blob — both halves of the fix removed together — turns BOTH methods of `TestLanguageLookupIsSafeForArbitraryKeys` RED, `test_the_supported_set_is_built_on_a_null_prototype` and `test_the_lookup_decides_absence_by_own_property`, at 2 failed and 6 passed. The class reproduces the defect rather than describing it. THE CODE READS CORRECTLY WHERE THE DIFF DID NOT SETTLE IT: `DIFF_SUPPORTED_LANGUAGES` keeps all twelve entries, its exported name and its frozen-ness, built as `Object.freeze(Object.assign(Object.create(null) as Record<string, string>, { ... }))`; the lookup returns early on a failed `Object.prototype.hasOwnProperty.call`; and the mapping's only readers at `82d3d584` are `diffLanguageForPath` and the two test files, measured with `git grep -n`, so no second site reads it unguarded.

THE ONE DECLARED DEVIATION IS THE ROUND'S BEST JUDGEMENT AND THE REVIEWER VERIFIED IT AT THE COMMIT IT NAMES. C3 carried one path beyond its bundle, `tests/ui_contracts/test_diff_view_model.py`, because the existing `supported_languages_block` scoper matched `= Object\.freeze\(\{` LITERALLY and S1's ordered shape change would otherwise have left that guard RED at C3. Measured by the reviewer in a disposable worktree at `8bb2ab6a`: that file's guards are 6 passed, so C3 was GREEN at its own commit and constraint 6's promise held. The repair re-anchors the scoper on the declaration's own boundaries rather than on one spelling of the initialiser, weakens no assertion, and the worker's mutation (e) shows the new region scoper still bites. Carrying the forced repair with the change that forced it was the correct call, not a scope drift.

RE-RUN SUITES, primary checkout, ONE pytest process at a time, base figures from `815f7a30` in brackets, every one exit 0: `tests/ui_contracts/` 653 passed 4 skipped [651, 4]; `tests/ui_server/` 495 passed with ZERO skips [495], which is where the `tsc --noEmit` node `TestJobSummaryCommandContract::test_typescript_compiles` lives and is how it is shown to have PASSED rather than skipped; `tests/orchestration/test_test_runner.py` with `tests/docs/` 347 passed [347], the vitest node among them, 4 passed on a `-k vitest` selection of that file; `ruff check tests/ui_contracts/test_diff_view_model.py` `All checks passed!`; and the canary 42 passed [42]. THE STRUCTURE IS CLEAN: `git diff --name-only 815f7a30..82d3d584` is exactly the block's eight paths with EMPTY residue in both directions, every commit single-parent, per-commit insertions 353, 241, 24, 16, 140, 129, 21 and 268 — each under five hundred and each matching the handback's `## Commits` table cell by cell — the marker sweep 0 in all five real targets against 10 in `.agent/authored/f037-r23.md` and in `.agent/last_block.md` as its non-zero control, `git ls-files .remedy-wt` 0, and `gh pr list --state open` empty. THE WORKER AUTHORED NO `Done:` AND NO `Gate:` PARAGRAPH: its only additions to the record are the two `Landed:` lines SPEC S5 ordered, read line by line by the reviewer. NO BLOCK CONDITION AROSE — nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER23

<<<SLICE DONE731
Done: R-0731 — RESOLVED at F037 R23 by that round's C3 and C4, and verified by the reviewer at `82d3d584` by RE-RUNNING the proof rather than reading the handback. The finding was that `DIFF_SUPPORTED_LANGUAGES` was an object LITERAL, so `diffLanguageForPath` answered the `Object` constructor for `src/x.constructor` and `Object.prototype` for `src/x.__proto__`, and `loadDiffLanguageBundle` then CALLED the importer for a path this feature's Acceptance says renders plain WITHOUT a fetch. BOTH HALVES OF THE FIX ARE ON DISK, which is what the finding asked for and why it asked for two: the mapping is built on `Object.create(null)` inside a still-frozen declaration keeping all twelve entries and the exported name, and absence is decided by `Object.prototype.hasOwnProperty.call(DIFF_SUPPORTED_LANGUAGES, extension)` rather than by comparing the read value to `undefined`. THE GUARDS ARE MEASURED, NOT ASSUMED: restoring the `815f7a30` blob of `apps/ui/src/api/diffViewModel.ts` in a disposable worktree at `82d3d584` turns both methods of `TestLanguageLookupIsSafeForArbitraryKeys` RED at 2 failed and 6 passed, against an unmutated control of 8 passed. The worker's own five mutations agree, including the ordered GREEN of removing the own-property read ALONE, which is the reading that shows the two halves are belt and braces rather than one fix written twice — and it is why both WHY comments say neither may be dropped as redundant. THE TWO GUARDS DELIBERATELY OVERLAP, for the first time in that module: the vitest cases state the BEHAVIOUR — five inherited spellings resolve to `null`, no answer is a function, and a counting importer records ZERO calls for `src/x.constructor` and `src/x.__proto__` — while the Python class states the SHAPE that behaviour rests on, and both files say in their own words which is the stronger. THE LESSON WORTH CARRYING OUT OF F037: an object literal is the wrong shape for a lookup keyed by an ARBITRARY EXTERNAL STRING, and a suite that only ever asks about keys nobody put there in an ORDINARY way — an unsupported extension — stays green in exactly the case that matters. It was found by RUNNING the shipped function, not by reading it.
<<<END DONE731

<<<SLICE DECISIOND11
## DECISION F037 D11 (2026-08-28) — F037 ships the diff viewer it has built, and the highlighting wiring, the perf measurement and the sidebar ruling are split off

CONTEXT. F037 reached round 24 of a twenty-five-round soft limit in session 7 of
seven. Operator amendment amend0827-process-diet rule 6 makes the obligation at
that point a SCOPE REPORT with a proposal, not more work. Three pieces of T003
are outstanding and are named in `.agent/plan.md` at `82d3d584`, as they were in
the two rounds before it: the WIRING of `loadDiffLanguageBundle` into
`DiffView`, the 10k-line perf fixture measured end to end with its numbers
recorded, and a ruling on the sidebar's visual treatment. Measured at
`82d3d584` with `git grep -l`, `loadDiffLanguageBundle` has NO caller outside
`apps/ui/src/api/diffViewModel.ts` and its two test files: the lazy-bundle model
is complete, tested and UNWIRED. Finishing all three and then running F037's
closure sequence needs roughly five to seven further rounds, which is twice the
budget that remains.

THE RULING, made under docs/agents/planner_reviewer_prompt.md §4 item 7 and
under the fix clause of finding `R-0709`, which binds the next block whose round
turns on a judgement the operator has not made: the reviewer rules and records,
and never asks. The three pieces LEAVE F037's scope. Feature-file amendment A6
states this in `docs/roadmap/features/T5_F037.md`, so the narrowing is on the
roadmap rather than only in this file, and F037's remaining work is its closure
sequence. The alternative rule 6 also offers — splitting F037 into two STATUS
lines — is a DOCUMENTED PROPOSAL TO THE OPERATOR, carried in this round's
handback, and is NOT executed here, because rule 6 forbids executing it on the
session's own authority.

ALTERNATIVES CONSIDERED. (1) Row on to round 25 and beyond: forbidden by rule 6
in as many words, and it would still not finish, because three pieces plus a
closure sequence do not fit in one round. (2) Keep the scope and close F037 with
the Acceptance bullets unmet: dishonest, and exactly the "green gate is not a
working feature" failure this record already carries as `R-0220`. (3) Drop the
pieces silently: worse than either, because nothing on the roadmap would ever
record that a diff viewer shipped with its highlighting unwired.

CONSEQUENCE, stated plainly because it is a real narrowing. F037 ships a diff
viewer whose syntax highlighting is BUILT AND NOT WIRED, and whose 10k-line perf
budget is UNMEASURED. The Acceptance bullet "unknown language renders plain
without a bundle fetch" is met and proved at the model layer; the Goal & Done
clause "the client renders it with syntax highlighting" and the Acceptance bullet
"10k-line fixture within the perf budget (recorded)" are NOT met, and A6 says so
rather than leaving a reader to discover it. Nothing already built is removed.

REVERSE by deleting this decision and amendment A6 from
`docs/roadmap/features/T5_F037.md`; the three pieces then return to F037's scope
and the soft-limit obligation returns with them.
<<<END DECISIOND11

<<<SLICE AMENDMENTA6
**A6 — the highlighting WIRING, the 10k-line perf measurement and the sidebar's
visual ruling leave this feature's scope (DECISION F037 D11).** Recorded at F037
R24, on reaching the seven-session soft limit of operator amendment
amend0827-process-diet rule 6. Three pieces of T003 are built no further here:

1. WIRING `loadDiffLanguageBundle` into `DiffView`. The lazy-bundle model is
   complete and tested — `diffLanguageForPath`, `loadDiffLanguageBundle`, the
   promise cache, the retry-after-rejection rule and the supported set — and
   measured at `82d3d584` it has NO caller outside
   `apps/ui/src/api/diffViewModel.ts` and its two test files. What ships is the
   model, not the rendered highlight.
2. The 10k-line perf fixture measured END TO END with its numbers recorded. The
   parser is bounded in both dimensions by DECISIONS F037 D5, D6 and D7, and
   virtual scrolling is built and guarded, but no end-to-end measurement has been
   taken, so the Acceptance bullet naming a recorded perf budget is UNMET.
3. A ruling on the sidebar's visual treatment. `DiffFileSidebar.tsx` exists and
   renders paths with change stats; amendment A4 names the three design
   authorities that bind this surface, and none of them rules on the sidebar.

CONSEQUENCE FOR THE Goal & Done AND Acceptance SECTIONS ABOVE, which are left as
written per this section's own convention: the clause "the client renders it with
syntax highlighting" and the bullet "10k-line fixture within the perf budget
(recorded)" are NOT met by F037 and are not claimed to be. Everything else in
those sections stands, including "unknown language renders plain without a bundle
fetch", which is met and proved at the model layer by
`apps/ui/src/api/diffViewModel.test.ts` and by
`tests/ui_contracts/test_diff_view_model.py`.

THE SPLIT-OFF SCOPE WANTS ITS OWN STATUS LINE, immediately before F033. That is a
PROPOSAL TO THE OPERATOR recorded here and in F037 R24's handback; rule 6 forbids
a session from executing a STATUS split on its own authority, so
`docs/roadmap/STATUS.md` is NOT edited by this amendment.
<<<END AMENDMENTA6

<<<SLICE SCOPEREPORT
## Scope report — F037 at the soft limit

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

F037 has reached SESSION 7 of a seven-session soft limit at round 24 of
twenty-five. Operator amendment amend0827-process-diet rule 6 makes this report
the obligation, not more feature work.

WHAT IS FINISHED. T001 the parser and the read endpoint, with its corpus tests
and the bounds of DECISIONS F037 D5, D6 and D7. T002 the rendering core — lines,
intraline spans, hunk heads, collapse — against the feature file's binding CSS.
T003 in the greater part: the file sidebar, virtual scrolling and its windowing
rule, the door and mount into `RemedyShell`, and the lazy language-bundle model
with its promise cache, its retry-after-rejection rule and the prototype-safe
lookup that finding `R-0731` forced.

WHAT IS MISSING, and none of it is discovered late — all three have stood under
Next Steps in `.agent/plan.md` at `82d3d584` and in the two rounds before it:

1. `loadDiffLanguageBundle` is UNWIRED. Measured at `82d3d584`, it has no caller
   outside its own module and its two test files, so highlighting is built and
   not rendered.
2. The 10k-line perf fixture is UNMEASURED end to end, so the Acceptance bullet
   naming a recorded perf budget is unmet.
3. The sidebar's visual treatment is unruled; amendment A4's three design
   authorities are silent on it.

WHAT THIS SESSION DID ABOUT IT. DECISION F037 D11 rules the three pieces OUT of
F037's scope and feature-file amendment A6 records that on the roadmap, so the
narrowing is visible where a later reader looks rather than only in a session
log. F037's remaining work is its closure sequence: the integration-gate round,
the evidence-and-zip round, then the STATUS round.

THE PROPOSAL TO THE OPERATOR, which this session does NOT execute because rule 6
reserves it: give the split-off scope its own STATUS line immediately before
F033 — the highlighting wiring, the 10k-line perf measurement and the sidebar
ruling, as one line of about three to four rounds. The alternative is to reject
A6, in which case reversing it is one paragraph in each of `.agent/decisions.md`
and `docs/roadmap/features/T5_F037.md`, and F037 continues past its soft limit
with the operator's knowledge rather than without it.
<<<END SCOPEREPORT

## Done when

Every gate below is EXECUTED and its real exit code recorded in the handback.
"Green" as a word is a finding. Report one line per gate.

- **G1 HYGIENE.** `.agent/STOP` absent, read from disk before C0a and again
  before C5. `git rev-parse HEAD` before C0a equals BASE. Branch is
  `feature/f037-rendered-diff-viewer`. `git status --porcelain | wc -l` is 0
  after every commit.
- **G2 TRANSPORT.** Report the committed C0a blob's byte count, line count and
  sha256, and show `git rev-parse` of `.agent/authored/f037-r24.md` and
  `.agent/last_block.md` at C0b as ONE blob. State in the same line that this
  chain covers the saved copy and its mirror ONLY, and not the emitted bytes.
- **G3 THE PLAN AT C1.** Byte equality of PLANF037R24, extracted from the
  COMMITTED C0a blob, with `git show <C1>:.agent/plan.md`, including the trailing
  newline. Negative control: the same slice minus its trailing newline, which
  must be False. Report `wc -l`, that it is strictly under 50, and the count of
  lines exactly `## Goal` and exactly `## Next Steps`.
- **G4 THE RECORD AT C2.** Two readers, and report both. Read every non-current
  revision with `git show <sha>:<path>` into memory; write nothing over a tracked
  file. (a) The pre-round blob joined to GATER23 then DONE731 with exactly one
  newline before each equals the C2 blob; negative control, flip one byte inside
  GATER23 — the FIRST appended paragraph — and it must be False. (b)
  Independently, split the C2 blob on blank lines, count the appended units
  yourself, and compare that many trailing units against the slices' paragraphs
  IN ORDER; report the count YOUR script measured. Show the pre-round blob is a
  byte PREFIX of the C2 blob.
- **G5 THE LEDGER.** Line-anchored over the C2 blob, base figures from
  `82d3d584` in brackets: `^- R-\d+ — ` [292], `^Done: R-\d+ — ` [41],
  `^Landed: R-` [11], `^Gate: F\d+ R\d+ — ` [93], and the OPEN SET computed AS A
  SET [253]. Every registered id distinct. Registrations must be UNMOVED at 292;
  `^Done: R-\d+ — ` rises by ONE to 42 for `R-0731`; `^Gate: F\d+ R\d+ — ` rises
  by ONE to 94; `^Landed: R-` is UNMOVED at 11; and the OPEN SET must FALL BY ONE
  to 252. Also report that `Gate: F037 R23` occurs exactly once in the C2 blob.
  If any figure disagrees, STOP and report it.
- **G6 THE DECISION AT C3 AND THE AMENDMENT AT C4.** For each of the two commits:
  the pre-commit blob is a byte PREFIX of the post-commit blob, and the
  post-commit blob equals the pre-commit blob joined to the slice with exactly
  one newline before it. Negative control on each: flip one byte inside that
  slice's FIRST paragraph, which must be False. Over the C3 blob report
  `^## DECISION ` [176] rising by ONE to 177, and the count of `F037 D11`, which
  must be exactly 1. Over the C4 blob report the count of lines starting `**A6`,
  which must be exactly 1, and the count of lines starting `**A5 `, which must
  still be exactly 1.
- **G7 SUITES AND THE DOCS GATE AT C4.** Primary checkout, ONE pytest process at
  a time, run after C4 and before C5. Base figures from `82d3d584` in brackets:
  - `python3 -m pytest tests/ui_contracts/ -q` [653 passed, 4 skipped]
  - `python3 -m pytest tests/ui_server/ -q` [495 passed, 0 skipped]
  - `python3 -m pytest tests/orchestration/test_test_runner.py tests/docs/ -q`
    [347 passed] — this is constraint 7's docs-round gate
  - the canary `python3 -m pytest tests/cli/test_golden_path.py -q` [42 passed]
  If any of the four is RED, STOP and report it; do not repair, and do not edit
  a test to make it green.
- **G8 STRUCTURE AND THE OPEN PR GATE AT C4.** `git diff --name-only <BASE>..<C4>`
  equals the Change set minus `.agent/handoff.md`; report the residue both ways.
  `git diff --stat <BASE>..<C4>` restricted to each of `apps/`, `packages/` and
  `tests/` is EMPTY — measure it, do not assert it. Per-commit insertions for C0a
  through C4, each under 500 and each matching the handback's `## Commits` table
  cell by cell; C5's own numbers are NOT ordered here, because a commit cannot
  count itself. Lines matching `^<<<SLICE ` or `^<<<END ` are 0 in
  `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md` and
  `docs/roadmap/features/T5_F037.md`, with `.agent/authored/f037-r24.md` as the
  NON-ZERO control. `git ls-files .remedy-wt | wc -l` is 0.
  `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, the SESSION NUMBER, branch, per-commit changed-files tables, the real
verification transcript one line per gate, deviations and assumptions, the
item-status table covering every C and every G, and the next expected action.
Derive its length bound yourself from AGENTS.md.

The handback MUST carry the SCOPEREPORT slice VERBATIM as a section of its own.
That slice is the operator's report and this is the only channel it travels on.

Per the fix clause of finding `R-0675`, which binds the next block that orders a
handback: ANY COMMIT BEYOND THE ORDERED SEQUENCE receives its own `## Commits`
row AND its own item-status row, and the Deviations section says so in those same
words rather than beside a clause that denies it.

THIS IS THE LAST DELEGATED ROUND OF SESSION 7 AND OF THIS SESSION. Say so, and
state that F037 stands at the soft limit with DECISION F037 D11 and amendment A6
recorded, its remaining work being the closure sequence, and one proposal open to
the operator that no session may execute for them.

If any gate is RED, if a slice will not apply, or if anything here contradicts
itself: STOP, write the handback saying exactly what happened, and end.
