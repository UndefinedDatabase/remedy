# STEP T003 (sixth round) — F037 Rendered diff viewer, round 22

BASE: `665be6ef`. SESSION 6 of feature F037. This block carries no line that is a
run of a single repeated character, so nothing in its frame has a length a reader
must recover by eye.

## Goal

Take the last named build piece: lazy language bundles. Acceptance asks for one
property above all — "unknown language renders plain WITHOUT a bundle fetch" —
and that is a decidable rule, so it is built in `diffViewModel.ts` where vitest
executes it, with the importer INJECTED exactly as `loadDiffEnvelope` injects its
fetcher. No component is wired this round. Three comments this feature's own
progress falsified are repaired first.

## Bundle

- C0a save this block verbatim to `.agent/authored/f037-r22.md`.
- C0b mirror the same bytes into `.agent/last_block.md`.
- C1 rewrite `.agent/plan.md` from the PLANF037R22 slice.
- C2 append GATER21, FINDING729 and FINDING730 to `.agent/live_review.md`.
- C3 the three comment repairs: SPEC S1, plus the two `Landed:` lines of SPEC S5.
- C4 the language rule and its vitest tests: SPEC S2 and S4.
- C5 the lazy bundle loader and its vitest tests: SPEC S3 and S4.
- C6 the guards: SPEC S6.
- C7 rewrite `.agent/handoff.md` as the handback.

## Change set

Exactly these paths, and nothing outside them:

- `.agent/authored/f037-r22.md` (new)
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `apps/ui/src/api/diffViewModel.ts`
- `apps/ui/src/api/diffViewModel.test.ts`
- `tests/ui_contracts/test_diff_view_model.py`
- `.agent/handoff.md`

Push the branch after C7 with `git push -u origin feature/f037-rendered-diff-viewer`.
Create no PR. Merge nothing. Rewrite no history.

## Constraints

1. Apply every slice BYTE FOR BYTE. Never write a `<<<SLICE` or `<<<END` marker
   line into a target file. If a slice looks wrong, apply it and declare it.
2. The SPEC items describe PRODUCTION CODE and are not slices. The WHY comments
   they ask for are yours to word.
3. NO COMPONENT IS WIRED THIS ROUND. `DiffView.tsx` is NOT in the change set and
   is not edited. Nothing under `packages/`, `apps/ui/src/components/` or
   `apps/ui/src/styles/` changes, and no CSS anywhere is touched.
4. `diffViewModel.ts` gains code by APPENDING. No existing export changes its
   name, signature, value or behaviour; the only edit above the append is the
   two comment repairs of SPEC S1.
5. NO NETWORK, NO GLOBAL, NO MOCKING LIBRARY. The bundle importer is a function
   ARGUMENT with a default, exactly as `loadDiffEnvelope` takes `fetchPayload`.
   There is no `vi.stubGlobal`, no `vi.mock` and no `vi.fn` anywhere in
   `apps/ui/src`, and this round starts none: a test that needs to count calls
   writes its own counting function.
6. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6, C7, and nothing is
   reordered. C6 MUST follow C4 and C5 — a guard committed before the code it
   reads is a guard that was red at its own commit.
7. Every destructive check — every mutation of any file — runs ONLY inside a
   disposable `git worktree` under `.remedy-wt/`, never in the primary checkout.
   Remove the worktree by its EXACT path and report `git worktree list` as one
   line BEFORE running any pytest gate in the primary checkout: a live worktree
   makes `tests/orchestration/test_test_runner.py` fail there, because that node
   shells out to `npx vitest run` and discovers the worktree's own config. That
   red is an artifact of the measurement, not a regression.
8. TYPESCRIPT MUTATION RED-PROOFS ARE ORDERED AND THEY ARE MEASURABLE. DECISION
   F037 D10, landed at F037 R21, records the route: spawn vitest FROM the primary
   checkout so it resolves its own package, and point `--root` at the worktree so
   the tree under test is the worktree's. Both flags are required. Direct `npx`
   or `node_modules/.bin/vitest` from a shell command is denied to this session
   class — drive it from a `python3` script under `.remedy-wt/`.
9. Do NOT author any `Done:` or `Gate:` paragraph. Those are the reviewer's and
   arrive only as the slices of C2. You author the two `Landed:` lines SPEC S5
   asks for, and nothing else in `.agent/live_review.md`.
10. STALENESS SWEEP. Re-read every WHY comment in each file you edit. Repair the
    three sites SPEC S1 names. Any OTHER stale claim you find: report it in the
    handback and leave it alone.

## SPEC

### S1 — the three claims this feature's own progress falsified

All three were reported by the R21 worker's sweep and left alone correctly; the
reviewer registered them as `R-0729` and `R-0730`.

In `tests/ui_contracts/test_diff_view_model.py`, the module docstring — this is
`R-0729` and it is the load-bearing one:

1. It states that DECISION F037 D8 "records that a mutation red-proof of
   TypeScript is not orderable in this repository", and gives the gitignored
   `node_modules` as the reason. That is FALSE at HEAD: DECISION F037 D10, landed
   at F037 R21, records the route that makes it orderable, and that round took
   six such red-proofs. Replace the claim with what is now true — a TypeScript
   red-proof IS orderable via D10's route, and this guard is Python for the
   reason D8 really gives, which is that vitest cannot see these structural facts
   about itself. Keep the three bullets above it unchanged; they are still exact.

In `apps/ui/src/api/diffViewModel.ts` — this is `R-0730`:

2. Line 512, in the `DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS` comment: "the component
   that will consume it". Wrong twice over. The future tense outlived F037 R21's
   C6, and the component does not name this constant at all — it calls
   `diffRowWindowForViewport`, and `tests/ui_contracts/test_diff_view_render.py`
   now FORBIDS the component naming the row-height constant. Name the real
   consumer, which is `computeDiffRowWindow` in this same module.
3. Line 555, in the `computeDiffRowWindow` comment: "That division is the only
   untestable part of virtual scrolling". False since R21's C5 moved the division
   into `diffRowWindowForViewport`, where vitest executes it. What remains
   untestable here is the DOM READ alone — `scrollTop` and `clientHeight`. Say
   that instead.

Change NO executable line in S1: comment, docstring and message text only.

### S2 — the language rule, in `apps/ui/src/api/diffViewModel.ts`

Appended. Two new exports.

`DIFF_SUPPORTED_LANGUAGES` — the SMALL supported set the Design section names
("a small supported set; unknown languages render plain — honest, fast"), as a
frozen mapping from a lower-case file extension WITHOUT its dot to a language id.
Include at most a dozen entries covering what this repository itself is written
in and what its diffs carry: `ts`, `tsx`, `js`, `jsx`, `py`, `json`, `css`, `md`,
`sh`, `yml`, `yaml`, `toml`. Say in the comment that the set is deliberately
small because every entry is a bundle someone must ship, and that the honest
answer for anything else is plain text rather than a guess.

`diffLanguageForPath(path: string): string | null` — TOTAL: no input throws, and
`null` is the plain answer rather than an error. It must resolve, and the WHY
comment must say why each is decided the way it is:

- the extension is what follows the LAST dot, lower-cased, so `App.TSX` and
  `a/b.c/d.ts` both resolve correctly;
- a path with NO dot, an empty path, or a path whose last dot is the FIRST
  character of the basename — a dotfile such as `.gitignore` — has no extension
  and is plain. A dotfile is the case a naive `split(".").pop()` gets wrong, and
  it must be pinned;
- a path ENDING in a dot has an empty extension and is plain;
- an extension not in the supported set is plain. This is Acceptance's sentence,
  and the next item is what makes it observable.

### S3 — the lazy bundle loader, in the same file

`DiffLanguageBundleImporter` — an exported type: a function taking a language id
and returning a promise of the bundle. It is a TYPE and nothing more; this module
ships no real bundles and imports nothing.

`loadDiffLanguageBundle(path, importBundle)` — returns a promise of
`{ language: string | null; bundle: unknown }`, `bundle` being `null` whenever
the answer is plain. `importBundle` has NO default that performs a real import:
give the parameter an explicit default that throws only if called, or make it
required — choose one, say which in the comment, and make the choice consistent
with the guard S6 orders. It must satisfy, and the comment must name each:

- **THE ACCEPTANCE PROPERTY.** For a path whose language is plain, `importBundle`
  IS NEVER CALLED — not called and discarded, not called and awaited: never
  invoked at all. The answer is `{ language: null, bundle: null }`. This is the
  one behaviour Acceptance states in so many words, and S4 pins it with a
  counter.
- **A FAILING IMPORT DEGRADES TO PLAIN.** If `importBundle` rejects or throws,
  the answer is `{ language, bundle: null }` — the language is still reported,
  because it was resolved from the path and remains true, but the bundle is
  absent. Nothing throws out of this function, exactly as `loadDiffEnvelope`
  never throws.
- **ONE IMPORT PER LANGUAGE.** A language already loaded is not imported again;
  keep a module-level cache keyed by language id. Export a
  `resetDiffLanguageBundleCache()` so a test can start from a known state, and
  say in its comment that it exists FOR THE TESTS and why that is honest here —
  a module-level cache is otherwise unobservable, and an unobservable cache is
  one no gate can hold to its promise.
- **A FAILED IMPORT IS NOT CACHED AS A SUCCESS.** A language whose import
  rejected may be retried later. State which of the two you implement — retry, or
  cache the failure — and pin it in S4 either way.

### S4 — the vitest tests, in `apps/ui/src/api/diffViewModel.test.ts`

New `describe` blocks beside the existing ones. Pin at minimum:

- every entry of `DIFF_SUPPORTED_LANGUAGES` resolves from a path bearing its
  extension, iterated FROM the mapping rather than transcribed, so an added entry
  cannot go untested;
- an UPPER-CASE extension, a multi-dot path, a dotfile, a path with no dot, an
  empty path and a path ending in a dot — each named separately;
- an unsupported extension is plain;
- **THE ACCEPTANCE TEST, and it is the round's centre**: for an unknown language,
  a counting importer written in the test file records ZERO calls and the answer
  is `{ language: null, bundle: null }`. Assert the count is exactly 0, not
  merely falsy;
- a supported language calls the importer exactly ONCE and returns its bundle;
- a second call for the same language leaves the count at 1 — the cache;
- a rejecting importer yields `{ language, bundle: null }` and does not throw;
- whichever retry-or-cache rule S3 chose, asserted directly;
- `resetDiffLanguageBundleCache()` really restores the pre-load state, shown by a
  count that rises again after it.

Reference the mapping and the constants BY NAME; transcribe no extension list.

### S5 — the two `Landed:` lines

In the SAME commit as C3, append TWO lines to `.agent/live_review.md`, one
beginning `Landed: R-0729 — ` and one beginning `Landed: R-0730 — `, each naming
the sites repaired and the commit that repaired them. Author no other line in
that file.

### S6 — the guards, in `tests/ui_contracts/test_diff_view_model.py`

Extend the existing module; add no new file. This module already proves the
structural facts vitest cannot see about itself, and these are of that kind:

- the module declares no import of any real syntax-highlighting package — the
  bundle importer is a parameter, and a static import would put a bundle in the
  main chunk, which is the whole point of "lazy". Assert over the module's
  COMMENT-STRIPPED import section, not the whole file;
- `DIFF_SUPPORTED_LANGUAGES` is declared exactly once and every language id in it
  is also named in the vitest suite, so no entry ships untested;
- there is no `vi.stubGlobal`, `vi.mock` or `vi.fn` anywhere in
  `apps/ui/src/api/diffViewModel.test.ts` — constraint 5 made mechanical;
- a vacuity assertion beside each new scoper, proving it returns strictly less
  than the whole file, exactly as this module's existing classes do.

## Slices

<<<SLICE PLANF037R22
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
R22 builds the last named piece, lazy language bundles, in the layer vitest
executes. Acceptance states one property in so many words — an unknown language
renders plain WITHOUT a bundle fetch — so the loader takes its importer as an
ARGUMENT, the way `loadDiffEnvelope` takes its fetcher, and a counting importer
in the test proves the count is zero rather than merely that the answer is
plain. No component is wired this round. Three comments R21's own code falsified
are repaired first: `R-0729`, a docstring telling future rounds that a
TypeScript red-proof cannot be ordered, which DECISION F037 D10 disproved, and
`R-0730`, two stale sentences in the model.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R21 verdict and two findings | ordered | record first |
| C3 the three comment repairs | ordered | one misleads future rounds |
| C4 the language rule and its tests | ordered | |
| C5 the lazy loader and its tests | ordered | the Acceptance property |
| C6 the guards | ordered | after the code they read |
| C7 the handback | ordered | |

## Next Steps
1. Wire highlighting into `DiffView`, and the 10k-line perf fixture measured END
   TO END with its numbers recorded, which Acceptance requires.
2. A ruling on the sidebar's visual treatment, still owed.
3. Then T003 is complete and the closure sequence can begin.

## Risks
- Round 22 of a 25-round soft limit, and session 6 of 7. Three named pieces
  remain across two Next Steps. If they do not fit by round 25, the session that
  reaches it owes a SCOPE REPORT rather than more work.
- Nothing here renders a `.tsx` file, so the wiring of step 1 will be gated by
  text and `tsc --noEmit` alone, as every `.tsx` round of this feature has been.
<<<END PLANF037R22

<<<SLICE GATER21
Gate: F037 R21 — the round that gave the windowing rule its caller and closed the two findings R20 raised. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran it independently at `835ba84b` rather than reading the handback's numbers. TRANSPORT IS PROVED AT ITS STRONGEST AVAILABLE LINK: the committed C0a blob is 38781 bytes, 490 lines, sha256 `212f83b8a43a0bfe07fb1e5b2f55fa1142a5e7b9bece95c3eb02b26d207f7252`, and is BYTE EQUAL to the reviewer's own scratch original `.remedy-wt/f037-r21-block.md`, which existed before the worker did — so this chain covers the emission and not merely the worker's self-consistency; at C0b both paths are ONE blob `3d1f37a3e7b5df7b13f0646c7213da951f67217e`. Caps: CONTENT 103, TOTAL 490, PROSE 387. EVERY SLICE WAS RE-EXTRACTED FROM THE COMMITTED BLOB AND RE-APPLIED BY THE REVIEWER: `.agent/plan.md` at `68d29e36` is byte equal to PLANF037R22's predecessor PLANF037R21 including its trailing newline, negative control False, 48 lines, one `## Goal`, one `## Next Steps`; the three-slice append to `.agent/live_review.md` at `cebca097` satisfies the byte reader with its negative control False and the base blob a byte prefix; the PROSESLIP append to `.agent/prose_slips.md` satisfies the same reader, taking `^- 2026-` from 19 to 20; and the DECISIOND10 append to `.agent/decisions.md` at `f2b96d03` takes `^## DECISION ` from 175 to 176 with `F037 D10` occurring exactly once. THE RECORD MOVED AS ORDERED AND ONLY AS ORDERED: registrations UNMOVED at 289 and all distinct, `^Done: R-\d+ — ` 37 to 39, `^Landed: R-` 6 to 7 at the tip, `^Gate: F\d+ R\d+ — ` 90 to 91, and the OPEN SET computed AS A SET fell from 254 to 252, which is `R-0727` and `R-0728` each named by a `Done:` line for the first time and no id registered — exactly the movement the block predicted before the round ran.

THE CODE IS RIGHT AND THE REVIEWER READ IT RATHER THAN THE SUMMARY. `diffRowWindowForViewport` resolves all three arguments through `wholeRowCount`, floors the scroll division and ceilings the height division, falls back to `DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS` only when the resolved height is exactly 0 — a height of 1 through 19 still ceilings to one visible row, which is the correct boundary — and delegates the window itself to `computeDiffRowWindow`, reimplementing none of its rules. THE TRAP THE ROUND EXISTED TO CLOSE IS REALLY CLOSED: an unmeasured panel reports `clientHeight` 0, 0 divides to a visible count of 0, `computeDiffRowWindow` answers 0 visible rows with an EMPTY window by its own third rule, an empty window draws nothing, a panel with nothing in it never scrolls, and a panel that never scrolls is never measured — the viewer would have been blank forever, and the fallback is what stops it. `DiffView.tsx` derives nothing: it holds `scrollTop` and `clientHeight`, hands both to the model, slices by the window's own two indices, sizes both spacers from the model's pixel answers, renders neither spacer when the list is not virtualized, and keeps the truncation notice OUTSIDE the window so virtualization cannot scroll the one warning that a diff is incomplete out of existence.

THE STALENESS REPAIR IS PROVED MECHANICALLY RATHER THAN BY EYE. `tests/ui_contracts/test_diff_viewer_mount.py` at C4 differs from its parent as raw bytes, and its ABSTRACT SYNTAX TREE with every string and f-string literal blanked is EQUAL — so the commit changed docstrings, comments and assertion messages and nothing else, with every `assert` expression intact. The negative control, renaming one test method, makes that comparison False, so the blanking is not vacuous. All five sites the block named were verified present at HEAD before the round and absent after it.

ALL SIX ORDERED RED-PROOFS REPRODUCE, run by the reviewer in a disposable worktree at `835ba84b` per DECISION F037 D10, each replaced string counted at exactly 1 before its edit and each file restored to its pre-mutation sha256, with the unmutated controls green first and last at 69 vitest tests and 33 pytest tests: the unmeasured-viewport fallback removed is exit 1 on the fallback case; the scroll division's floor turned to ceil and the height division's ceil turned to floor are each exit 1 on exactly their own rounding test; a spacer height forced to 0 is exit 1 on the spacer test and on the ten-thousand-row scale test; the model call replaced by in-component arithmetic is exit 1 on three guards including the new delegation guard; and the row height moved from 20 to 24 is exit 1 on exactly the stylesheet-agreement test, which is the discriminator proving that test really parses `12.5px/1.6` out of `DiffView.module.css` rather than transcribing a number. THE REVIEWER ADDED FOUR THE BLOCK DID NOT ORDER, because a gate list is only as good as the mutations nobody thought to try: dropping the overscan from the delegation is exit 1 on four cases, forcing the TRAILING spacer to 0 is exit 1 on two, and slicing the drawn rows from index 0 instead of the window start is exit 1 on two including the new slice guard. THE FOURTH CAME BACK GREEN AND IS REPORTED RATHER THAN BURIED: passing `rowCount` to `computeDiffRowWindow` UNRESOLVED, dropping the outer `wholeRowCount` call, leaves all 69 tests passing. That is NOT a gate gap — `computeDiffRowWindow` resolves its own first argument on its first line, so the outer call is redundant by construction and the mutation changes no behaviour a test could observe. It is noted here as a small piece of dead defensiveness rather than registered, because it has no product effect and removing it would be churn.

THE SUITES ARE GREEN AT REAL EXIT CODES RE-RUN BY THE REVIEWER, primary checkout, one pytest process at a time, base figures in brackets: `tests/ui_contracts/` 648 passed 4 skipped [642, 4]; `tests/ui_server/` 495 passed [495]; `tests/orchestration/test_test_runner.py` with `tests/docs/` 347 passed [347]; ruff over both edited test modules `All checks passed!`; the typescript node 1 passed 73 deselected, PASSED and not skipped, which is most of this round's gate because C6 is `.tsx`; and the canary 42 passed [42]. THE VITEST TOTAL IS 592 PASSED ACROSS 32 FILES [584], measured by the reviewer through D10's route with `--reporter=verbose`, with all eight new `diffRowWindowForViewport` cases printed by name as EXECUTED — including the ten-thousand-row scale case, which is the first evidence in this feature that the window really bounds what a large diff draws. THE STRUCTURE IS CLEAN: the path residue is EMPTY in both directions over eleven paths, `packages/` is empty, `apps/ui/src/components/detail/` and `.../shell/` are empty, `tokens.css` and `DiffView.module.css` are UNTOUCHED — constraints 3 and 4 measured rather than asserted — `apps/ui/src/components/` names `DiffView.tsx` alone, every commit is single-parent and under 500 insertions, the marker sweep is 0 in all nine targets against 12 in the C0a blob as its control, and `git ls-files .remedy-wt` is 0.

THE WORKER'S TWO DEVIATIONS ARE BOTH HONEST AND THE FIRST SHOWS GOOD JUDGEMENT. It repaired one comment outside SPEC S1: `DiffView.tsx`'s header named "the virtual scrolling and the lazy language bundles" as outstanding, and C6 lands the virtual scrolling, so leaving it would have shipped a false sentence in the very commit that falsified it. Reading constraint 10's "leave it alone" as binding on claims already stale at the sweep rather than on one the round's own code breaks is the correct reading, and it declared the call rather than making it quietly. The second is that the `Landed:` line names its commit by role rather than by SHA, which is unavoidable for a line written into the commit it describes and is the form every other such line in this record uses. THREE STALE CLAIMS IT FOUND AND CORRECTLY LEFT ALONE ARE REGISTERED BELOW as `R-0729` and `R-0730`. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER21

<<<SLICE FINDING729
- R-0729 — Medium, A GUARD'S DOCSTRING TELLS EVERY FUTURE ROUND THAT A TYPESCRIPT MUTATION RED-PROOF CANNOT BE ORDERED HERE, WHICH IS THE EXACT BELIEF THAT BLINDED THIS FEATURE'S `.ts` LAYER FOR THIRTEEN ROUNDS AND WHICH THE SAME ROUND DISPROVED. Raised by the WORKER of F037 R21 in its staleness sweep, which found it and correctly left it alone because that round's constraint 10 permitted repairing only the sites SPEC S1 named, and registered here with the reviewer's own reading. MEASURED AT `835ba84b`: the module docstring of `tests/ui_contracts/test_diff_view_model.py` states that DECISION F037 D8 "records that a mutation red-proof of TypeScript is not orderable in this repository", giving the gitignored `apps/ui/node_modules` and guardrail G5's disposable worktree as the reason. At that same commit DECISION F037 D10 is on disk, landed by C3 of the same round, recording the route that makes it orderable — vitest spawned FROM the primary checkout so it resolves its own package, with `--root` pointed at the worktree so the tree under test is the worktree's — and G6 of that round took SIX such red-proofs through it, every one of them red, plus four more the reviewer added. So the sentence is not merely stale: it is contradicted by a DECISION in the same repository, and it cites the wrong decision as its authority. MEDIUM AND NOT LOW because of WHO READS IT AND WHEN: this docstring is the first thing a builder or reviewer of the diff view model reads, it is phrased as a settled repository-wide fact, and believing it is what caused F037 R8 through R20 to ship `.ts` code with no mutation proof at all — the cost is not a wrong byte on screen but a whole class of gate never ordered, which is the most expensive kind of stale claim this repository can carry. MEDIUM AND NOT HIGH because nothing on a user's screen is wrong, no suite is red, and the guard the docstring introduces is itself correct and green. THE OPEN SET WAS SEARCHED BEFORE THIS ID WAS MINTED (§3 item 30): `R-0727` is the nearest neighbour and is the same FAMILY — a stale claim about what exists — but it is a different sentence, a different file and a different fact, and it is fully resolved, so this takes its own id rather than a third resolution paragraph. THE FIX, which C3 of F037 R22 lands under that block's ordering constraint 6: replace the claim with what D10 established, keep the three bullets above it, which remain exact, and change no executable line. OPEN.
<<<END FINDING729

<<<SLICE FINDING730
- R-0730 — Low, TWO WHY COMMENTS IN THE VIEW MODEL WERE FALSIFIED BY THE VERY ROUND THAT WROTE THE CODE BESIDE THEM. Raised by the WORKER of F037 R21 in its staleness sweep and correctly left alone under that round's constraint 10, registered here with the reviewer's own reading, and verified present at `835ba84b`. THE FIRST is at line 512, inside the `DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS` comment, which lists the sites naming that constant as "the function below, the component that will consume it, and the vitest suite". It is wrong in TWO ways rather than one: the future tense outlived C6 of that round, which wired the window; and the component does not name this constant AT ALL, then or now — it calls `diffRowWindowForViewport`, and `tests/ui_contracts/test_diff_view_render.py` gained a guard in the same round FORBIDDING the component to name the row-height constant, so the sentence describes an arrangement the round's own gates now prohibit. The real consumer is `computeDiffRowWindow`, in that same module. THE SECOND is at line 555, in the `computeDiffRowWindow` comment: "That division is the only untestable part of virtual scrolling". True when written at R20, false since C5 of R21 moved the division into `diffRowWindowForViewport`, where vitest executes it and where the reviewer's own red-proofs turned both of its roundings red. What remains untestable is the DOM READ alone — `scrollTop` and `clientHeight` — which is a narrower and more useful thing to tell a reader. LOW because no behaviour is affected, no gate is blind and no suite is red; both are comments, and the code they sit beside is correct. IT IS STILL AN ID AND NOT A PROSE SLIP because it is wrong state on disk under `apps/`, which is what operator amendment amend0827-process-diet rule 2 reserves an id for, and because AGENTS.md's Code Discoverability Conventions make these comments load-bearing: a WHY comment that answers a reader's question with a confident falsehood is worse than no comment, since the reader has no reason to doubt it. THE OPEN SET WAS SEARCHED BEFORE THIS ID WAS MINTED (§3 item 30): it is `R-0727`'s family and `R-0729`'s round, but a different file and different sentences from both, and both of those are resolved. THE PATTERN WORTH RECORDING, because this is the third staleness finding in three rounds: a round that MOVES a rule into a new function falsifies every comment that described where that rule used to live, and the sweep that catches it must read the comments AROUND the change and not only the lines the diff touched. THE FIX, which C3 of F037 R22 lands under that block's ordering constraint 6: name `computeDiffRowWindow` as the consumer, and narrow the untestable part to the DOM read. OPEN.
<<<END FINDING730

## Done when

Every gate below is EXECUTED and its real exit code recorded in the handback.
"Green" as a word is a finding. Report one line per gate.

- **G1 HYGIENE.** `.agent/STOP` absent, read from disk before C0a and again
  before C7. `git rev-parse HEAD` before C0a equals BASE. Branch is
  `feature/f037-rendered-diff-viewer`. `git status --porcelain | wc -l` is 0
  after every commit.
- **G2 TRANSPORT.** Report the committed C0a blob's byte count, line count and
  sha256, and show `git rev-parse` of `.agent/authored/f037-r22.md` and
  `.agent/last_block.md` at C0b as ONE blob.
- **G3 THE PLAN AT C1.** Byte equality of PLANF037R22, extracted from the
  COMMITTED C0a blob, with `git show <C1>:.agent/plan.md`, including the trailing
  newline. Negative control: the same slice minus its trailing newline, which
  must be False. Report `wc -l`, that it is strictly under 50, and the count of
  lines exactly `## Goal` and exactly `## Next Steps`.
- **G4 THE RECORD AT C2.** The pre-round blob joined to GATER21, FINDING729 and
  FINDING730 in Bundle order with exactly one newline before each equals the C2
  blob. Negative control: flip one byte inside GATER21's FIRST paragraph; it must
  be False. Show the pre-round blob is a byte PREFIX of the committed one.
- **G5 THE LEDGER.** Line-anchored over the C2 blob, each with its base figure
  from `665be6ef` in brackets: `^- R-\d+ — ` [289], `^Done: R-\d+ — ` [39],
  `^Landed: R-` [7], `^Gate: F\d+ R\d+ — ` [91], and the OPEN SET computed AS A
  SET — registered ids minus ids named by a `Done:` line, never by subtraction
  [252]. Report that every registered id is distinct. Registrations must RISE BY
  TWO to 291 and the open set must RISE BY TWO to 254, because `R-0729` and
  `R-0730` are registered here and neither is resolved this round; `Done:` is
  UNMOVED at 39 and `Gate:` rises by one to 92. `^Landed: R-` rises by two to 9
  at C3, per SPEC S5. If any figure disagrees, STOP and report it.
- **G6 THE RED-PROOFS.** In a disposable worktree at the C6 tree, `__pycache__`
  purged before every run and `python3 -B` throughout, TypeScript driven per
  constraint 8. Count each replaced string at exactly 1 BEFORE editing; restore
  every file to its pre-mutation sha256 and show the restore. Report the
  UNMUTATED control first and again last.
  - (a) the plain-language early return removed, so `importBundle` is called for
    an unknown language too. MUST be RED on the zero-call Acceptance test, and it
    is the single most important reading of this round.
  - (b) the cache lookup removed, so a repeated language imports twice. MUST be
    RED on the cache test.
  - (c) the `try`/`catch` around `importBundle` removed. MUST be RED on the
    rejecting-importer test.
  - (d) the extension taken from the FIRST dot rather than the last. MUST be RED
    on the multi-dot case.
  - (e) the dotfile guard removed, so `.gitignore` resolves to a language. MUST
    be RED on the dotfile case.
  - (f) one entry deleted from `DIFF_SUPPORTED_LANGUAGES`. MUST be RED, and it is
    the discriminator proving S4 iterates the mapping rather than transcribing it.
  - (g) Python: a `vi.fn()` inserted into the vitest test file. MUST be RED on
    the S6 guard forbidding it.
  If any of the seven is NOT red, STOP and report it. Do not repair it.
- **G7 SUITES, TYPES AND LINT AT C6.** Primary checkout, ONE pytest process at a
  time, the worktree removed and `git worktree list` reported as one line first.
  Each with its base figure in brackets:
  - `python3 -m pytest tests/ui_contracts/ -q` [648 passed, 4 skipped]
  - `python3 -m pytest tests/ui_server/ -q` [495 passed]
  - `python3 -m pytest tests/orchestration/test_test_runner.py tests/docs/ -q` [347 passed]
  - `python3 -m ruff check tests/ui_contracts/test_diff_view_model.py`
  - the typescript node
    `python3 -m pytest tests/ui_server/test_dashboard_contract.py -k "typescript or tsc or noEmit" -q -rs`
    [1 passed, 73 deselected] — it must PASS and not SKIP. If `tsc --noEmit` is
    RED, STOP and report; do not repair.
  - the canary `python3 -m pytest tests/cli/test_golden_path.py -q` [42 passed]
  - the vitest TOTAL, driven per constraint 8 with `--reporter=verbose` against
    the PRIMARY tree, reporting the test-file and test counts [32 files, 592
    tests] and naming the new cases as executed.
- **G8 STRUCTURE AND THE OPEN PR GATE AT C6.** `git diff --name-only <BASE>..<C6>`
  equals the Change set minus `.agent/handoff.md`; report ACTUAL MINUS EXPECTED
  and EXPECTED MINUS ACTUAL. `git diff --stat` restricted to each of `packages/`,
  `apps/ui/src/components/` and `apps/ui/src/styles/` is EMPTY. Per-commit
  insertions from `git show --numstat`, each under 500, each matching the
  handback's table. Lines matching `^<<<SLICE ` or `^<<<END ` are 0 in every
  edited target, with the C0a blob as a NON-ZERO control.
  `git ls-files .remedy-wt | wc -l` is 0.
  `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, the SESSION NUMBER, branch, per-commit changed-files tables, the real
verification transcript one line per gate, constraint 10's staleness sweep,
deviations and assumptions, the item-status table covering every C and every G,
and the next expected action. Derive its length bound yourself from AGENTS.md.

If any gate is RED, if a slice will not apply, or if anything here contradicts
itself: STOP, write the handback saying exactly what happened, and end.
