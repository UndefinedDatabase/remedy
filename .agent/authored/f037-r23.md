# STEP T003 (seventh round) — F037 Rendered diff viewer, round 23

BASE: `815f7a30`. SESSION 6 of feature F037. This block carries no line that is a
run of a single repeated character, so nothing in its frame has a length a reader
must recover by eye.

## Goal

Fix a real defect the round that shipped it could not see. `diffLanguageForPath`
looks its extension up in a plain object literal, so an extension that names an
INHERITED property — `constructor`, `__proto__` — resolves to a value off
`Object.prototype` instead of to plain, and the importer is then called for a
file Acceptance says must never trigger a fetch. Measured, not reasoned. Then the
three comments R22's sweep reported are repaired, one of which the reviewer's own
R21 spec introduced.

## Bundle

- C0a save this block verbatim to `.agent/authored/f037-r23.md`.
- C0b mirror the same bytes into `.agent/last_block.md`.
- C1 rewrite `.agent/plan.md` from the PLANF037R23 slice.
- C2 append GATER22, DONE729, DONE730 and FINDING731 to `.agent/live_review.md`.
- C3 the `R-0731` fix and its vitest tests: SPEC S1 and S2, plus its `Landed:`
  line per SPEC S5.
- C4 the guard over the lookup: SPEC S3.
- C5 the three comment repairs: SPEC S4, plus its `Landed:` line per SPEC S5.
- C6 rewrite `.agent/handoff.md` as the handback.

## Change set

Exactly these paths, and nothing outside them:

- `.agent/authored/f037-r23.md` (new)
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `apps/ui/src/api/diffViewModel.ts`
- `apps/ui/src/api/diffViewModel.test.ts`
- `tests/ui_contracts/test_diff_view_model.py`
- `.agent/handoff.md`

Push the branch after C6 with `git push -u origin feature/f037-rendered-diff-viewer`.
Create no PR. Merge nothing. Rewrite no history.

## Constraints

1. Apply every slice BYTE FOR BYTE. Never write a `<<<SLICE` or `<<<END` marker
   line into a target file. If a slice looks wrong, apply it and declare it.
2. The SPEC items describe PRODUCTION CODE and are not slices. The WHY comments
   they ask for are yours to word.
3. NO COMPONENT IS WIRED THIS ROUND. Nothing under `packages/`,
   `apps/ui/src/components/` or `apps/ui/src/styles/` changes, and no CSS is
   touched.
4. NO EXISTING EXPORT changes its name, signature or observable behaviour EXCEPT
   the one defect S1 names. `DIFF_SUPPORTED_LANGUAGES` keeps every entry it has
   and its exported name; only HOW IT IS BUILT and HOW IT IS READ may change.
5. NO NETWORK, NO GLOBAL, NO MOCKING LIBRARY. There is no `vi.stubGlobal`,
   `vi.mock` or `vi.fn` anywhere in `apps/ui/src`, and C4's own guard now
   enforces that; a test needing to count calls writes its own counting function.
6. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and nothing is reordered.
   C4 MUST follow C3 — a guard committed before the code it reads is a guard that
   was red at its own commit.
7. Every destructive check runs ONLY inside a disposable `git worktree` under
   `.remedy-wt/`, never in the primary checkout. Remove it by its EXACT path and
   report `git worktree list` as one line BEFORE any pytest gate: a live worktree
   makes `tests/orchestration/test_test_runner.py` fail in the primary checkout,
   because that node shells out to `npx vitest run` and finds the worktree's own
   config. That red is an artifact of the measurement, not a regression.
8. TYPESCRIPT MUTATION RED-PROOFS ARE ORDERED AND MEASURABLE, per DECISION F037
   D10: spawn vitest FROM the primary checkout so it resolves its own package,
   and point `--root` at the worktree so the tree under test is the worktree's.
   Both flags are required. Direct `npx` or `node_modules/.bin/vitest` from a
   shell command is denied to this session class — drive it from a `python3`
   script under `.remedy-wt/`.
9. Do NOT author any `Done:` or `Gate:` paragraph. Those are the reviewer's and
   arrive only as the slices of C2. You author the two `Landed:` lines SPEC S5
   asks for, and nothing else in `.agent/live_review.md`.
10. STALENESS SWEEP. Re-read every WHY comment in each file you edit. Repair the
    three sites SPEC S4 names AND any comment THIS ROUND'S OWN CODE falsifies —
    that carve-out is the reading F037 R21 and R22 both used and the reviewer
    endorsed at their gates. Any OTHER stale claim: report it and leave it alone.

## SPEC

### S1 — the inherited-property defect, in `apps/ui/src/api/diffViewModel.ts`

MEASURED BY THE REVIEWER at `815f7a30`, by running the shipped function rather
than reading it. `DIFF_SUPPORTED_LANGUAGES` is `Object.freeze({...})`, an object
literal, so it INHERITS from `Object.prototype`, and `diffLanguageForPath` reads
it with `DIFF_SUPPORTED_LANGUAGES[extension]` and treats only `undefined` as
absent. Therefore:

- `src/x.constructor` returns the `Object` CONSTRUCTOR FUNCTION as a language id;
- `src/x.__proto__` returns `Object.prototype`;
- `src/x.toString`, `src/x.valueOf` and `src/x.hasOwnProperty` return `null`
  correctly, but ONLY BY ACCIDENT — the lower-casing turns them into `tostring`,
  `valueof` and `hasownproperty`, which are not inherited keys. The two that
  survive are the two that are already lower-case.

THE EFFECT IS ON THIS FEATURE'S OWN ACCEPTANCE SENTENCE, and the reviewer
measured that too: `loadDiffLanguageBundle("src/x.constructor", importer)` CALLS
the importer — counter at 1, `typeof language` is `"function"`, `bundle` is not
null — where Acceptance requires an unknown language to render plain WITHOUT a
bundle fetch. The whole vitest suite is GREEN with this defect present, which is
what makes it a gate gap and not merely a bug.

THE FIX, and it must close BOTH halves rather than one:

1. Build the mapping on a NULL PROTOTYPE, so there is nothing to inherit:
   `Object.freeze(Object.assign(Object.create(null), { ... }))` or equivalent.
   Keep every existing entry, the exported name, and the frozen-ness.
2. Read it with an OWN-PROPERTY check rather than by comparing to `undefined` —
   `Object.prototype.hasOwnProperty.call(map, extension)`, or a `Map`. Belt and
   braces is deliberate here: either change alone fixes today's defect, and a
   later refactor that undoes one silently restores it, so the WHY comment must
   say that both are load-bearing and why.

Say in the comment WHY a plain object literal is the wrong shape for a lookup
keyed by ARBITRARY EXTERNAL STRINGS — a diff path comes from a repository this
viewer does not control — and that this is the general rule, not a special case
for two names.

### S2 — the vitest tests for S1

In the existing `diffLanguageForPath` and `loadDiffLanguageBundle` describes.
Pin at minimum:

- `constructor`, `__proto__`, `toString`, `valueOf` and `hasOwnProperty` as
  extensions each resolve to `null`, asserted with `toBeNull()` so a returned
  function cannot pass as truthy or as "not undefined";
- the answer's TYPE for those paths is never a function — assert
  `typeof answer !== "function"` for at least the two that were really broken, so
  a future regression to a prototype value fails even if `null` is not restored;
- **THE ACCEPTANCE CASE, and it is the point of the round**: a counting importer
  records ZERO calls for `src/x.constructor` and for `src/x.__proto__`, exactly
  as it already does for an ordinary unknown extension;
- the mapping has NO inherited keys: assert `Object.getPrototypeOf` of it is
  `null`;
- every existing case still passes unchanged — add tests, edit none.

### S3 — the guard, in `tests/ui_contracts/test_diff_view_model.py`

Extend the existing module; add no new file. One new test class:

- the module builds its language mapping on a null prototype — assert the source
  contains an `Object.create(null)` (or the equivalent spelling actually used)
  INSIDE the `DIFF_SUPPORTED_LANGUAGES` declaration, scoped to that declaration's
  own region and not to the whole file;
- the lookup does not decide absence by comparing to `undefined` alone — scoped
  to `diffLanguageForPath`'s body;
- a vacuity assertion proving each new scoper returns strictly less than the
  whole file, as this module's existing classes do.

This guard is TEXT over a `.ts` file, which is weaker than the vitest tests of
S2. It is here for the reason this module exists at all: it states the STRUCTURAL
promise a future refactor must keep, where the vitest tests state the behaviour.
Say that in the class docstring, and say that S2 is the stronger of the two.

### S4 — the three comments R22 reported and left alone

All in `apps/ui/src/api/diffViewModel.ts`. This is `R-0730`'s remainder.

1. Around line 328, in the `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` comment: it lists
   the sites naming that constant as "`defaultCollapsedHunkIds`, `DiffView.tsx`,
   which renders these rows and has been mounted by `RemedyShell` since F037 R18,
   and both test files". `DiffView.tsx` DOES NOT NAME THIS CONSTANT — measured:
   `grep -rn DIFF_HUNK_COLLAPSE_THRESHOLD_LINES apps/ui/src/components/` is
   EMPTY. The sentence was introduced by F037 R21's C4 while repairing a
   different staleness, on the reviewer's own instruction, which is why it is
   called out here rather than left to a sweep. Name only sites that really name
   the constant, and verify each by grep before writing it.
2. Line 13: "`splitLineIntoIntralineSegments` returns at the foot of this file".
   It is not at the foot — the module has grown past it twice. Drop the location
   claim rather than replacing it with a new one; a line number or a position in
   a growing file is a fact that goes stale by itself, which is the lesson of
   this finding's whole history.
3. Around line 6: "the component that will draw it". `DiffView.tsx` has drawn
   these rows since F037 R16. Present tense, and name the component.

Change NO executable line in S4: comment text only.

### S5 — the two `Landed:` lines

One in the SAME commit as C3, beginning `Landed: R-0731 — `, naming the two
halves of the fix. One in the SAME commit as C5, beginning `Landed: R-0730 — `,
naming the three sites. Author no other line in `.agent/live_review.md`.

## Slices

<<<SLICE PLANF037R23
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
R23 fixes `R-0731`, a defect the round that shipped it could not see and its
whole green suite did not catch: the language mapping is a plain object literal,
so an extension naming an INHERITED property resolves off `Object.prototype`
instead of to plain, and `src/x.constructor` really does reach the bundle
importer that Acceptance says must not be called. The fix closes both halves —
a null-prototype map AND an own-property read — because either alone is undone
silently by a later refactor. Then `R-0730`'s remaining three comments are
repaired, one of them a sentence the reviewer's own R21 spec introduced.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R22 verdict, two resolutions, one finding | ordered | record first |
| C3 the `R-0731` fix and its tests | ordered | a measured defect |
| C4 the structural guard | ordered | after the code it reads |
| C5 the three comment repairs | ordered | closes `R-0730` |
| C6 the handback | ordered | |

## Next Steps
1. Wire highlighting into `DiffView` through `loadDiffLanguageBundle`.
2. The 10k-line perf fixture measured END TO END with its numbers recorded,
   which Acceptance requires and nothing has yet measured.
3. A ruling on the sidebar's visual treatment, still owed.

## Risks
- Round 23 of a 25-round soft limit, session 6 of 7. THREE named pieces remain
  and only two rounds are left inside the limit, so the session that reaches
  round 25 owes a SCOPE REPORT rather than more work — most likely proposing
  that the highlighting wiring and the perf fixture become their own STATUS
  line.
- Nothing here renders a `.tsx` file, so step 1 will be gated by text and
  `tsc --noEmit` alone, as every `.tsx` round of this feature has been.
<<<END PLANF037R23

<<<SLICE GATER22
Gate: F037 R22 — the round that built the lazy language bundles. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran it independently at `815f7a30`. TRANSPORT IS PROVED AT ITS STRONGEST AVAILABLE LINK: the committed C0a blob is 33754 bytes, 384 lines, sha256 `0e2cf6475dc53bfea5d7509bf7fc31693a0559e5af060b967ced3f47db15075e`, BYTE EQUAL to the reviewer's own scratch original, which existed before the worker did; at C0b both paths are ONE blob `16d14a50923cb0b97ee5896321c17002ca0299b9`. THE SLICES WERE RE-EXTRACTED FROM THE COMMITTED BLOB AND RE-APPLIED: the plan at `62aca836` is byte equal to PLANF037R22 including its trailing newline, negative control False, 47 lines, one `## Goal`, one `## Next Steps`; the three-slice append at `b634b8d6` satisfies the byte reader with its negative control False and the base blob a byte PREFIX. THE RECORD MOVED EXACTLY AS PREDICTED BEFORE THE ROUND RAN: registrations 289 to 291 and all 291 distinct, `^Done: R-\d+ — ` UNMOVED at 39, `^Landed: R-` 7 to 9 at the tip, `^Gate: F\d+ R\d+ — ` 91 to 92, and the OPEN SET computed AS A SET rose from 252 to 254, which is `R-0729` and `R-0730` registered and neither resolved. RE-RUN SUITES, primary checkout, one process at a time, base figures in brackets, every one exit 0: `tests/ui_contracts/` 651 passed 4 skipped [648, 4]; `tests/ui_server/` 495 passed [495]; `tests/orchestration/test_test_runner.py` with `tests/docs/` 347 passed [347]; ruff `All checks passed!`; the typescript node 1 passed 73 deselected, PASSED and not skipped; the canary 42 passed [42]; and the vitest TOTAL 609 passed across 32 files [592], measured through DECISION F037 D10's route. THE STRUCTURE IS CLEAN: path residue EMPTY in both directions, `packages/`, `apps/ui/src/components/` and `apps/ui/src/styles/` all EMPTY — constraint 3 measured rather than asserted — every commit single-parent and under 500 insertions, the marker sweep 0 in all five real targets against 8 in the C0a blob as its control, and `git ls-files .remedy-wt` 0.

THE CODE IS RIGHT WHERE THE BLOCK REACHED, AND THE REVIEWER READ IT. `diffLanguageForPath` is better than the SPEC asked for: the block said "the last dot", and the worker took the extension from the BASENAME first, so `a/b.c/d` correctly has no extension where a whole-string reading would have answered `c/d`. The dotfile rule `dot <= 0` is the discriminating one and the module's own comment names the discriminating example — a file called `.ts` is a hidden file named `ts`, not TypeScript. `loadDiffLanguageBundle` returns before touching the importer when the language is plain, which is Acceptance's sentence made observable; it caches the PROMISE rather than the bundle, so concurrent callers share one import; a rejection deletes the cache entry, so a failed language is retried rather than poisoned; and a synchronous throw from the importer is caught too, because the call sits inside the `try` before `Promise.resolve`. ALL FOUR OF THE REVIEWER'S OWN RED-PROOFS TURN OVER, in a disposable worktree at `69be112f`, control green first and last at 86 tests and the module restored to its pre-mutation sha256 each time: removing the plain early return is exit 1 on both zero-call tests; removing the cache lookup is exit 1 on the one-import test and on the reset test; reading the FIRST dot instead of the last is exit 1 on the basename test; and weakening the dotfile guard from `<= 0` to `< 0` is exit 1 on exactly the dotfile test. THE GATES ARE NOT VACUOUS.

THE WORKER FOUND A BLIND GUARD AND FIXED IT, WHICH IS THE ROUND'S BEST WORK AND WAS NOT ORDERED. The existing `exported_names` helper matched `^export (?:function|const) (\w+)`, which cannot match `export async function` — so the standing rule that every exported value is named in the vitest suite was BLIND to `loadDiffLanguageBundle`, this round's headline export, and would have passed a completely untested one. The worker widened the pattern and declared it. Its other declared additions are of the same kind and equally sound.

THE ONE UNORDERED COMMIT IS ACCEPTED. `b94a4bc9` is a one-line comment correction: C3's own repair text said `diffRowWindowForViewport` sits "at the foot of this file", and C4 and C5 then appended past it, so the round falsified a sentence the round itself wrote. Repairing it is the carve-out this reviewer endorsed at the R21 gate — constraint 10's "leave it alone" binds claims already stale at the sweep, not one the round's own code breaks — and the worker declared it, named the reading it relied on, and re-ran the gates it could touch. Its commit subject carries a typo, which stands because amending is history rewriting; that is the right trade. THE OTHER DEVIATIONS ARE HONEST: `importBundle` is REQUIRED rather than defaulted, because a throwing default would be swallowed by the degrade-to-plain rule and a caller would never learn it forgot the argument — the stronger choice, and declared; the mocking-token guard reads RAW text rather than comment-stripped, which is the safe direction for a FORBIDDING check and is declared with its consequence, that a comment naming the tokens would trip it.

ONE DEFECT SURVIVED EVERY GATE AND THE REVIEWER FOUND IT BY RUNNING THE CODE RATHER THAN READING IT. It is registered below as `R-0731` and it defeats this round's own Acceptance sentence. IT IS NOT A FAILURE OF THIS ROUND'S EXECUTION but of its gate design, and the design was the reviewer's: every test the block ordered asks what an UNSUPPORTED extension does, and none asks what an INHERITED one does, so a green suite of 86 tests says nothing about it. THE PLAN FILE'S ITEM TABLE STILL READS `ordered` FOR EVERY ITEM AT THE HANDBACK, which the worker declared: the plan is written byte for byte at C1 and the block orders no second write, so it describes the round's intent rather than its outcome. That is this workflow's standing shape rather than this round's defect, it is `.agent/` state rather than product state, and it earns no id under operator amendment amend0827-process-diet rule 2; it is noted so the next block that wants a live status table orders the second write explicitly. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER22

<<<SLICE DONE729
Done: R-0729 — RESOLVED at F037 R22 by that round's C3. The finding was that the module docstring of `tests/ui_contracts/test_diff_view_model.py` told every future reader that DECISION F037 D8 "records that a mutation red-proof of TypeScript is not orderable in this repository" — the belief that left this feature's `.ts` layer with no mutation proof from R8 to R20, and which DECISION F037 D10 had disproved on disk one round earlier. VERIFIED BY THE REVIEWER at `815f7a30`: the docstring no longer carries the claim, it names D10 and the route D10 records, and the three bullets above it — that vitest passes just as happily on a module pulling in React, that it cannot notice an untested export, and that it cannot notice a transcribed threshold — are unchanged, which matters because those three are still exact and are the real reason the guard is written in Python. THE REPAIR IS COMMENT TEXT ONLY: `git show` over C3 changes no executable line in that module, and the round's own gates re-ran green afterwards. THE FINDING'S REAL COST IS WORTH RECORDING RATHER THAN CLOSING SILENTLY: a false sentence in a docstring is not a wrong byte on a screen, it is a class of gate never ordered, and this one went unchallenged for thirteen rounds because each block inherited it from the last instead of re-running it. The counter-measure is already on disk as D10 and as the `R-0724` lesson it repeats — before writing that a tool cannot run here, run it.
<<<END DONE729

<<<SLICE DONE730
Done: R-0730 — RESOLVED IN PART at F037 R22 by that round's C3 and C6b, and FULLY at F037 R23 by that round's C5, which this block's ordering constraint 6 places after this record. The finding named two stale comments in `apps/ui/src/api/diffViewModel.ts`. BOTH ARE REPAIRED and the reviewer verified them at `815f7a30`: the `DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS` comment no longer says "the component that will consume it" and names `computeDiffRowWindow`, the real consumer, and the `computeDiffRowWindow` comment no longer claims its division is "the only untestable part of virtual scrolling", which stopped being true when F037 R21's C5 moved that division into `diffRowWindowForViewport`. The unordered `b94a4bc9` repaired a third of the same family that R22's own appends created. THE REMAINDER, named here rather than left implied, on the precedent `R-0721`, `R-0725` and `R-0727` all set in this record: the R22 worker's sweep reported THREE more sites of this same class and correctly left them alone, and the reviewer verified all three present at `815f7a30`. Line 13 says `splitLineIntoIntralineSegments` "returns at the foot of this file" — it does not, the module has grown past it twice. Line 6 says the rule lives in the model rather than "inside the component that will draw it" — `DiffView.tsx` has drawn these rows since F037 R16. And around line 328 the `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` comment lists `DiffView.tsx` among the sites that "name this constant", WHICH IT DOES NOT — `grep -rn DIFF_HUNK_COLLAPSE_THRESHOLD_LINES apps/ui/src/components/` is empty, measured by the reviewer. THAT THIRD SITE IS THE REVIEWER'S OWN, and recording it is the point of this paragraph: SPEC S1 item 5 of the F037 R21 block ordered the future tense repaired and the component NAMED, and naming it inside a sentence about which sites reference the constant asserted something that was never true. A correction that carries a new false fact is worse than the staleness it repaired, because it arrives wearing the authority of a fix. THE LESSON THIS FINDING LEAVES ACROSS ITS FOUR ROUNDS: a comment stating a LOCATION — a line, a position, "at the foot of this file", "the component that names this" — goes stale by itself, without anyone editing it, so the durable form states a RELATIONSHIP and lets a reader's grep find the position.
<<<END DONE730

<<<SLICE FINDING731
- R-0731 — Medium, THE LANGUAGE LOOKUP FALLS THROUGH TO `Object.prototype`, SO A FILE EXTENSION THAT NAMES AN INHERITED PROPERTY RESOLVES TO A FUNCTION AND REACHES THE BUNDLE IMPORTER THAT ACCEPTANCE SAYS MUST NOT BE CALLED. Found by the REVIEWER at the F037 R22 gate by RUNNING the shipped function rather than reading it, in a disposable worktree at `815f7a30` through DECISION F037 D10's route. MEASURED, every reading below taken and not reasoned: `diffLanguageForPath("src/x.constructor")` returns the `Object` CONSTRUCTOR FUNCTION — `typeof` is `"function"` — and `diffLanguageForPath("src/x.__proto__")` returns `Object.prototype`, because `DIFF_SUPPORTED_LANGUAGES` is `Object.freeze({...})` over an object LITERAL, which inherits, and the lookup treats only `undefined` as absent. `src/x.toString`, `src/x.valueOf` and `src/x.hasOwnProperty` correctly return `null`, BUT ONLY BY ACCIDENT: the function lower-cases the extension first, so those three become `tostring`, `valueof` and `hasownproperty`, which are not inherited keys — the two that survive are exactly the two that are already lower-case, which is luck rather than design and is why the fix must not be a deny-list. THE PRODUCT EFFECT IS THIS FEATURE'S OWN ACCEPTANCE SENTENCE: `loadDiffLanguageBundle("src/x.constructor", importer)` CALLS the importer — counter 1, `typeof language` `"function"`, `bundle` not null — where `docs/roadmap/features/T5_F037.md` requires that an unknown language render plain WITHOUT a bundle fetch. Downstream, a function is then handed on as a language id to code expecting a string. MEDIUM AND NOT LOW because it defeats a stated Acceptance criterion rather than merely looking wrong, and because the diff viewer renders paths from repositories this application does not control, so the input is external by construction; MEDIUM AND NOT HIGH because the affected extensions are rare in practice, nothing is executed, and the failure is a spurious fetch and a wrong id rather than data loss. IT IS A GATE GAP AND THE GATE DESIGN WAS THE REVIEWER'S: the F037 R22 block's SPEC S4 ordered a test for "an unsupported extension is plain" and none for an INHERITED one, so all 86 vitest tests and the whole Python guard pass with the defect present — the suite was green in the reviewer's own re-run at the same commit. THE OPEN SET WAS SEARCHED BEFORE THIS ID WAS MINTED (§3 item 30): no open finding concerns prototype inheritance or an object used as a map, and the nearest neighbours — `R-0725` on unanchored presence checks and `R-0728` on unanchored counts — are about ASSERTIONS being wrong, while this is shipped behaviour being wrong, so it takes its own id. THE FIX, which C3 of F037 R23 lands under that block's ordering constraint 6, closes BOTH halves deliberately: build the mapping on a null prototype so there is nothing to inherit, AND read it through an own-property check rather than an `undefined` comparison, because either alone repairs today's defect while a later refactor that undoes one silently restores it. THE GENERAL RULE THIS LEAVES: an object literal is the wrong shape for a lookup keyed by an ARBITRARY EXTERNAL STRING, in any language with prototype inheritance, and the tests that catch it are the ones that ask about keys nobody put there. OPEN.
<<<END FINDING731

## Done when

Every gate below is EXECUTED and its real exit code recorded in the handback.
"Green" as a word is a finding. Report one line per gate.

- **G1 HYGIENE.** `.agent/STOP` absent, read from disk before C0a and again
  before C6. `git rev-parse HEAD` before C0a equals BASE. Branch is
  `feature/f037-rendered-diff-viewer`. `git status --porcelain | wc -l` is 0
  after every commit.
- **G2 TRANSPORT.** Report the committed C0a blob's byte count, line count and
  sha256, and show `git rev-parse` of `.agent/authored/f037-r23.md` and
  `.agent/last_block.md` at C0b as ONE blob.
- **G3 THE PLAN AT C1.** Byte equality of PLANF037R23, extracted from the
  COMMITTED C0a blob, with `git show <C1>:.agent/plan.md`, including the trailing
  newline. Negative control: the same slice minus its trailing newline, which
  must be False. Report `wc -l`, that it is strictly under 50, and the count of
  lines exactly `## Goal` and exactly `## Next Steps`.
- **G4 THE RECORD AT C2.** The pre-round blob joined to GATER22, DONE729,
  DONE730 and FINDING731 in Bundle order with exactly one newline before each
  equals the C2 blob. Negative control: flip one byte inside GATER22's FIRST
  paragraph; it must be False. Show the pre-round blob is a byte PREFIX.
- **G5 THE LEDGER.** Line-anchored over the C2 blob, base figures from
  `815f7a30` in brackets: `^- R-\d+ — ` [291], `^Done: R-\d+ — ` [39],
  `^Landed: R-` [9], `^Gate: F\d+ R\d+ — ` [92], and the OPEN SET computed AS A
  SET [254]. Every registered id distinct. Registrations must rise by ONE to 292
  (`R-0731`); `Done:` rises by TWO to 41 (`R-0729`, `R-0730`); `Gate:` rises by
  one to 93; and the OPEN SET must FALL BY ONE to 253 — two resolved, one
  registered. `^Landed: R-` rises by two to 11 across C3 and C5. If any figure
  disagrees, STOP and report it.
- **G6 THE RED-PROOFS.** In a disposable worktree at the C4 tree, TypeScript
  driven per constraint 8, `__pycache__` purged and `python3 -B` for pytest.
  Count each replaced string at exactly 1 BEFORE editing; restore every file to
  its pre-mutation sha256 and show it. Control first and last.
  - (a) the null prototype removed, the mapping built as a plain object literal
    again while the own-property read STAYS. MUST be RED — and if it is GREEN,
    the own-property read alone is carrying the fix; report that rather than
    repairing it, because it changes which half S1 calls load-bearing.
  - (b) the own-property read replaced by an `undefined` comparison while the
    null prototype STAYS. Report its colour honestly: GREEN here is EXPECTED and
    is not a failure, because a null-prototype map has nothing to inherit — it is
    the measurement that shows the two halves are belt and braces rather than one
    fix written twice. Do NOT treat a green here as a red gate.
  - (c) BOTH halves removed together, restoring the exact `815f7a30` shape. MUST
    be RED on the inherited-key tests and on the zero-call Acceptance tests. This
    is the discriminator that proves S2 really reproduces the defect.
  - (d) one entry deleted from `DIFF_SUPPORTED_LANGUAGES`. MUST be RED, proving
    S2 still iterates the mapping.
  - (e) Python: the `Object.create(null)` spelling removed from the declaration.
    MUST be RED on the S3 guard.
  If any gate marked MUST be RED is not red, STOP and report it. Do not repair.
- **G7 SUITES, TYPES AND LINT AT C5.** Primary checkout, ONE pytest process at a
  time, the worktree removed and `git worktree list` reported as one line first.
  Base figures in brackets:
  - `python3 -m pytest tests/ui_contracts/ -q` [651 passed, 4 skipped]
  - `python3 -m pytest tests/ui_server/ -q` [495 passed]
  - `python3 -m pytest tests/orchestration/test_test_runner.py tests/docs/ -q` [347 passed]
  - `python3 -m ruff check tests/ui_contracts/test_diff_view_model.py`
  - the typescript node
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -k "typescript or tsc or noEmit" -q -rs`
    [1 passed, 73 deselected] — it must PASS and not SKIP. If `tsc --noEmit` is
    RED, STOP and report; do not repair.
  - the canary `python3 -m pytest tests/cli/test_golden_path.py -q` [42 passed]
  - the vitest TOTAL per constraint 8 with `--reporter=verbose` [32 files, 609
    tests], naming the new cases as executed.
- **G8 STRUCTURE AND THE OPEN PR GATE AT C5.** `git diff --name-only <BASE>..<C5>`
  equals the Change set minus `.agent/handoff.md`; report the residue both ways.
  `git diff --stat` restricted to each of `packages/`, `apps/ui/src/components/`
  and `apps/ui/src/styles/` is EMPTY. Per-commit insertions each under 500, each
  matching the handback's table. Lines matching `^<<<SLICE ` or `^<<<END ` are 0
  in every edited target EXCEPT `.agent/last_block.md`, which necessarily mirrors
  them, with the C0a blob as a NON-ZERO control.
  `git ls-files .remedy-wt | wc -l` is 0.
  `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, the SESSION NUMBER, branch, per-commit changed-files tables, the real
verification transcript one line per gate, constraint 10's staleness sweep,
deviations and assumptions, the item-status table covering every C and every G,
and the next expected action. Derive its length bound yourself from AGENTS.md.

THIS IS EXPECTED TO BE THE LAST DELEGATED ROUND OF SESSION 6. Say so in the
handback, and state plainly that the next session begins at ROUND 24 of a
25-round soft limit with three named pieces outstanding — the highlighting
wiring, the perf fixture and the sidebar ruling — so the session reaching round
25 owes a SCOPE REPORT rather than more work.

If any gate is RED, if a slice will not apply, or if anything here contradicts
itself: STOP, write the handback saying exactly what happened, and end.
