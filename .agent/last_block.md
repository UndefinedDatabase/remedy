### STEP T001d — F256 Diff viewer completion, round 4 (THE REPAIR)

Goal: make the lazy load REAL. The grammar tables move to their own module, so
the module `DiffView` imports dynamically is one it does NOT also import
statically, and `loadDiffLanguageBundle` fetches something that was genuinely
not in the main chunk. This repairs finding `R-0732`, which this round also
registers.

Base: `e23dad09`, the tip of `feature/f256-diff-viewer-completion`. Every
reading below was taken there.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f256-r4.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 append the R3 verdict and the registration of `R-0732` to
  `.agent/live_review.md`, and the slips to `.agent/prose_slips.md`
- C3 the grammar module, the scanner change and the vitest suite
- C4 the `DiffView` rewiring and the contract-test update
- C5 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f256-r4.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/prose_slips.md`
- `apps/ui/src/api/diffHighlightGrammars.ts`
- `apps/ui/src/api/diffHighlight.ts`
- `apps/ui/src/api/diffHighlight.test.ts`
- `apps/ui/src/components/diff/DiffView.tsx`
- `tests/ui_contracts/test_diff_view_render.py`
- `.agent/handoff.md`

`DiffView.module.css` is NOT edited — the palette DECISION F256 D2 ruled stands
unchanged, and this round moves code rather than colour.

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
   `git show <C0a>:.agent/authored/f256-r4.md`, never from this prompt's text.
4. AGENTS.md binds in full: self-review before every commit, one logical step
   per commit, `.agent/plan.md` current before every commit, clean tree, push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under
   the gitignored `.remedy-wt/`. The primary checkout satisfies
   `git status --porcelain` empty at every commit.
6. Shell forms rejected by this session's guard are RE-EXPRESSED through
   `python3 - <<'PY'`, never skipped and never weakened. Report each one.
7. THE GUARDS ON `DiffView.tsx`, unchanged from last round and still the most
   likely red. `tests/ui_contracts/test_diff_view_render.py` at `e23dad09`
   requires the comment-stripped source to CALL every name in `DELEGATED_RULES`
   — `splitLineIntoIntralineSegments` among them — and forbids the spellings in
   `REIMPLEMENTED_RULE_SPELLINGS`: `200`, `.length >`, `sort(`,
   `DIFF_VIRTUAL_ROW_HEIGHT_PX`, `Math.floor(`, `Math.ceil(`, `.slice(0,`. It
   also requires every `styles.<name>` the component names to have a rule in
   `DiffView.module.css`. Neither tuple may be edited.
8. NO EXISTING ASSERTION IS WEAKENED, DELETED OR RELAXED to make a gate pass.
   Where this round's design genuinely changes what a test should say — the
   dynamic-import target moves from `diffHighlight` to `diffHighlightGrammars` —
   the assertion is RETARGETED, not dropped, and the handback names it.
9. `.agent/decisions.md` is NOT in this change set. DECISION F256 D1 stated a
   main-chunk benefit that `R-0732` records as unmet; this round MAKES IT TRUE
   rather than amending it, so no decision text needs editing. Say so in the
   handback if you disagree; do not edit the file.

### SPEC — the production code

S1. New file `apps/ui/src/api/diffHighlightGrammars.ts`. It holds what
`diffHighlight.ts` currently exports as `DIFF_HIGHLIGHT_GRAMMARS`, moved
VERBATIM — the same language ids, the same comment openers, string delimiters
and keyword sets, the same `Object.create(null)` construction and the same
freezing helper. Moving it must change no value; a keyword added or dropped here
would be a behaviour change smuggled into a refactor.

S2. That module also exports
`diffHighlightGrammarFor(language: string | null): DiffHighlightGrammar | null`,
which answers `null` for `null` and for any id the mapping does not OWN, read
through `Object.prototype.hasOwnProperty.call`. The null-prototype and
own-property reasoning currently written above the mapping moves WITH it, since
it is the reason the construction looks as it does.

S3. It imports the `DiffHighlightGrammar` TYPE from `./diffHighlight`. A type
import is erased at build time, so it creates no runtime edge and cannot pull
the scanner back into this chunk.

S4. In `diffHighlight.ts`, `DIFF_HIGHLIGHT_GRAMMARS` and the local keyword
constants are REMOVED, and `tokenizeDiffLine` changes signature to
`tokenizeDiffLine(text: string, grammar: DiffHighlightGrammar | null)`. A `null`
grammar yields a single `plain` segment carrying the whole text, which is
exactly the answer an unowned language id produced before. Empty text still
yields the empty array. Every other rule — first match wins, the string
delimiter precedence, the digit and identifier runs, the merge of adjacent
`plain` — is unchanged.

S5. `composeHighlightedRuns` changes its second parameter the same way, to
`grammar: DiffHighlightGrammar | null`, and passes it through. Its three
invariants are unchanged and stay pinned.

S6. THE WHY COMMENTS CARRY THE REASON, in `diffHighlight.ts` and in the new
module: the grammar tables are the LAZY half and the scanner is the eager half,
because `DiffView` needs the scanner synchronously to render a row and needs a
grammar only once a file's language is known. Name finding `R-0732` and record
that a module imported both statically and dynamically by the same file is not
code-split at all — which is what the previous shape did, and what this shape
exists to prevent.

S7. In `DiffView.tsx`: the importer becomes
`() => import("../../api/diffHighlightGrammars")`, and `diffHighlight` is
imported STATICALLY only. The per-path state now holds the resolved
`DiffHighlightGrammar | null` rather than a language id — take it from the
bundle `loadDiffLanguageBundle` returns, via that module's
`diffHighlightGrammarFor`, and pass it to `composeHighlightedRuns`. The
cancellation-flag effect shape, the reset on a new envelope, and S5's Acceptance
property that a plain path never invokes the importer are all unchanged.

S8. `apps/ui/src/api/diffHighlight.test.ts` is updated to the new signature.
Cases that named a language id now name the grammar
`diffHighlightGrammarFor` answers for it, so the suite still covers every
grammar; the unknown-language cases pass `null`. THE INHERITED-PROPERTY TESTS
MOVE RATHER THAN DISAPPEAR: `constructor`, `__proto__`, `toString` and
`hasOwnProperty` are now asserted against `diffHighlightGrammarFor`, which must
answer `null` for each. That is the same `R-0731` property at its new home, and
losing it would be the round's worst outcome.

S9. `tests/ui_contracts/test_diff_view_render.py` has its dynamic-import
assertion RETARGETED to `diffHighlightGrammars`, and gains one test asserting
that `DiffView.tsx` does NOT statically import the module it imports
dynamically — the `R-0732` property, expressed over the comment-stripped source
by checking that no `import … from "…/diffHighlightGrammars"` statement exists
while the dynamic `import(` of it does.

### The authored slices

<<<SLICE PLANF256R4
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
| compose the token cut with the intraline cut | done | `739d31e0` |
| the DiffView wiring and the derived palette | done | `678bc698` |
| make the lazy load real, repairing `R-0732` | done | this round |
| rule on the sidebar's treatment | open | a ruling to record, not code |
| measure the 10k-line fixture | open | needs a real fixture and a real run |

## Next Steps
1. Rule on the file sidebar's visual treatment and record the authority.
2. Measure the 10k-line fixture end to end and record the numbers in the
   feature file's Built State.
3. Run the integration gate, then the closure sequence.

## Risks
- `tests/ui_contracts/test_diff_view_render.py` reads the comment-stripped
  source of `DiffView.tsx`; its `DELEGATED_RULES` and
  `REIMPLEMENTED_RULE_SPELLINGS` tuples are not to be edited.
- Moving the grammar tables must change no value in them, or a refactor has
  silently changed what a language highlights as.
<<<END PLANF256R4

<<<SLICE GATEF256R3
Gate: F256 R3 — the WIRING round, in which the diff surface first renders coloured runs. THE ROUND PASSED on every gate its block ordered, G1 through G9, and the reviewer re-ran each independently at `e23dad09`. THE WORKER ALSO DECLARED A DEFECT IN THE BLOCK RATHER THAN PAPERING OVER IT, which is registered below as `R-0732` and is the reviewer's error and not the round's.

TRANSPORT COVERS THE EMISSION rather than only the worker's self-consistency: the reviewer's own scratch original `.remedy-wt/f256-r3-block.md` predates the worker, and the committed `.agent/authored/f256-r3.md` blob at `b1c24555` is BYTE EQUAL to it at 24546 bytes, sha256 `ccc593d323c1200288f6184e8b9ce7a98467406ad82e59b49677e2ed89e8a26b`. At `b30a5a89` that path and `.agent/last_block.md` are ONE blob.

ALL THREE APPENDS WERE RECONSTRUCTED BY THE REVIEWER at `4bd65c04`: for `.agent/live_review.md`, `.agent/prose_slips.md` and `.agent/decisions.md` alike, the `2251c6d4` blob plus a newline plus the round's slice equals the C2 blob exactly, each pre-round blob is a byte PREFIX — 1339712 to 1344549, 13551 to 13924 and 689972 to 692805 — and in each file a byte flipped inside the FIRST appended paragraph is REJECTED. THE LEDGER MOVED AS PREDICTED: registrations UNMOVED at 292 and all DISTINCT, the OPEN SET computed AS A SET UNMOVED at 251, `^Landed: R-` UNMOVED at 11, and `^Gate: F\d+ R\d+ — ` rising by exactly ONE from 98 to 99, with `Gate: F256 R2` occurring exactly once.

THE GUARD THIS ROUND WAS MOST LIKELY TO BREAK HELD, and the reviewer measured it rather than reading it: over the comment-stripped `DiffView.tsx` at `678bc698` the string `splitLineIntoIntralineSegments(` still occurs, so the wiring COMPOSED that call instead of replacing it and the `DELEGATED_RULES` tuple is satisfied by a real call; every forbidden spelling of `REIMPLEMENTED_RULE_SPELLINGS` counts zero; and the classes the component names are exactly the classes `DiffView.module.css` defines, with the residue empty. RE-RUN IN THE PRIMARY CHECKOUT, one pytest process at a time, each exit 0 and each equal to the handback's figure: `tests/ui_contracts/` 658 passed with 4 skipped, `tests/ui_server/` 495 passed, the canary `tests/cli/test_golden_path.py` 42 passed, and `tsc --noEmit` exit 0.

- R-0732 — MEDIUM. `apps/ui/src/components/diff/DiffView.tsx` imports `apps/ui/src/api/diffHighlight` STATICALLY, for `composeHighlightedRuns`, and DYNAMICALLY in the same file, as the bundle importer passed to `loadDiffLanguageBundle`. A module imported both ways by the same file is not code-split at all, so the dynamic import buys nothing: the tokenizer and every grammar table ship in the main chunk. The reviewer reproduced it directly at `e23dad09` — `npx vite build` exits 0 and warns that the module `is dynamically imported by DiffView.tsx but also statically imported`, and that the dynamic import `will not move module into another chunk`. THE DEFECT IS THE REVIEWER'S: the F256 R3 block's S2 ordered the dynamic importer while its S6 and S8 ordered the static call, and the worker implemented both exactly as written and declared the contradiction with the bundler's own words rather than hiding it. WHAT IS AND IS NOT BROKEN: the Acceptance property that a plain path never invokes the importer still HOLDS and is still pinned by the vitest suite, because `loadDiffLanguageBundle` resolves the language before asking for a bundle; what is unmet is DECISION F256 D1's stated benefit of no main-chunk weight. FIX: give the lazy half its own module, so the file that dynamically imports it does not also statically import it — the grammar tables move to `apps/ui/src/api/diffHighlightGrammars.ts`, the scanner stays eager because a row cannot render without it, and a contract test pins that the dynamically imported module is imported no other way. This finding is registered and repaired in the SAME round that follows it, and the repair is verified by the absence of that build warning.
<<<END GATEF256R3

<<<SLICE SLIPSF256R3
2026-08-28 · F256 R3 · The block's prose ordered `.agent/decisions.md`'s append "separated by exactly one blank line" while its gate G4(a) ordered `base + newline + slice`, and that file's blob already ended with a blank line; the two are unsatisfiable together, the worker obeyed the gate and declared it, so D2's heading is preceded by two blank lines.
2026-08-28 · F256 R3 · The block's G9 marker sweep expected 0 in "every non-authored target", which cannot hold for `.agent/last_block.md` because C0b and G2 require that file to be the identical blob to the authored control; the worker reported 4 and declared it.
<<<END SLIPSF256R3

`PLANF256R4` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF256R3` and
`SLIPSF256R3` are APPENDS to `.agent/live_review.md` and `.agent/prose_slips.md`.
For each, append exactly what gate G4(a) below measures — the pre-round blob,
one newline, then the slice — whatever blank lines that file already ends with.

### Done when

G1 HYGIENE. Read `.agent/STOP` with `os.path.exists` before C0a and again
before C3; report both, and stop after the commit in hand if it exists. Report
`git rev-parse HEAD` before C0a — it must equal `e23dad09` —
`git branch --show-current`, and `git status --porcelain | wc -l` after each of
C0a, C0b, C1, C2, C3 and C4.

G2 TRANSPORT. One digest comparison: sha256 of
`git show <C0a>:.agent/authored/f256-r4.md` against the reviewer's own original
at `.remedy-wt/f256-r4-block.md`, reporting both digests, the byte length and
equality; that original predates this worker, so say the reading covers more
than self-consistency. Report that `<C0b>:.agent/authored/f256-r4.md` and
`<C0b>:.agent/last_block.md` are ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF256R4 including the
trailing newline — report `True` or `False` — with `wc -l` under 50 and the
counts of lines exactly `## Goal` and exactly `## Next Steps`.

G4 THE RECORD AT C2, two readers per appended file. (a) The `e23dad09` blob plus
a newline plus the slice equals the C2 blob, reported separately for
`.agent/live_review.md` with GATEF256R3 and `.agent/prose_slips.md` with
SLIPSF256R3; NEGATIVE CONTROL for each, flipping one byte at an offset your
script confirms lies INSIDE THE FIRST appended paragraph and reporting the
equality now `False`. (b) Let N be each slice's paragraph count, COUNTED BY YOUR
SCRIPT from the slice and never taken from this block, ignoring an empty
trailing unit; report N and that the LAST N blank-line units of each file match
those paragraphs IN ORDER. Report each pre-round blob is a byte PREFIX.

G5 THE LEDGER AT C2. Over the C2 blob and the `e23dad09` blob beside it, report
`^- R-\d+ — ` and whether all DISTINCT, `^Done: R-\d+ — `, `^Landed: R-`,
`^Gate: F\d+ R\d+ — `, and the OPEN SET as a set. This round REGISTERS ONE
finding and resolves none, so registrations rise by exactly ONE, the open set
rises by exactly ONE, `^Gate: F\d+ R\d+ — ` rises by exactly ONE, and the other
figures are UNMOVED. Report that `R-0732` occurs exactly once as a registration
and carries no `Done:` and no `Landed:` line, and that `Gate: F256 R3` occurs
exactly 1 time.

G6 THE MOVE CHANGED NO VALUE, measured and not asserted. In a `python3` script,
parse the grammar table out of `apps/ui/src/api/diffHighlight.ts` at `e23dad09`
and out of `apps/ui/src/api/diffHighlightGrammars.ts` at C3, and report that the
set of language ids is IDENTICAL and that for each id the comment openers, the
string delimiters and the keyword set are identical, printing any difference. A
refactor that quietly drops a keyword is the failure this gate exists to catch.

G7 THE `R-0732` PROPERTY AT C4, which is what this round exists to repair.
Report, over `apps/ui/src/components/diff/DiffView.tsx` at C4: the count of
dynamic `import(` naming `diffHighlightGrammars`, which must be at least 1; the
count of STATIC `import` statements naming `diffHighlightGrammars`, which must
be 0; and the count of static imports naming `diffHighlight`, which must be at
least 1. Then run `npx vite build` in `apps/ui` from a `python3` script,
report its real exit code, and report the count of lines in its combined output
containing both `dynamically imported` and `statically imported`, which must now
be 0 — beside the reviewer's reading of that same count at `e23dad09`, which was
1. Report the full warning line if any remains.

G8 THE RED-PROOF AT C4, in a disposable worktree, never in the primary
checkout. Report the UNMUTATED CONTROL FIRST, then each mutation, with exit code
and passed/failed counts, using

    ["python3", "-m", "pytest", "tests/ui_contracts/test_diff_view_render.py", "-q"]

with `cwd` set to the WORKTREE. THE MUTATIONS, each applied alone and reverted
before the next, inside the worktree, each of which must turn that file RED:
(i) add a static import of `diffHighlightGrammars` to `DiffView.tsx` beside the
dynamic one — the exact shape `R-0732` describes, which the new test must
catch; (ii) point the dynamic importer back at `../../api/diffHighlight`.
Report the control again, green, and `git worktree list` plus
`git status --porcelain | wc -l` in the primary after removal.

G9 THE SUITES AT C4. One pytest process at a time, from the repository root, in
the PRIMARY checkout, each with exit code and its own passed/failed line:
`tests/ui_contracts/` in full; `tests/orchestration/test_test_runner.py` (it
spawns `npx vitest run` under a 30-second timeout — report the wall clock, and
warm `apps/ui/dist` first if `src` is newer, declaring it); `tests/ui_server/`;
`tests/regression/test_resource_safety.py`;
`tests/orchestration/test_integrity_gate.py`; and the canary
`tests/cli/test_golden_path.py`. Additionally run `tsc --noEmit` in `apps/ui`
and report its real exit code. Every one must be exit 0. If any is red, STOP and
write the handback with the full untruncated failure list.

G10 STRUCTURE, over `e23dad09..<C4>` — the range ending BEFORE the handback
commit, so `.agent/handoff.md` is expected in the change set but NOT in this
range, and `.agent/last_block.md` mirrors the authored blob by construction.
Report `git diff --name-only` and both residues against the change set with
`.agent/handoff.md` set aside, printed in both directions and both expected
empty. Report each commit's insertions from `git diff --numstat`, each under
500, and that each of C0a, C0b, C1, C2, C3 and C4 is single-parent. Report the
counts of lines beginning `<<<SLICE ` and `<<<END ` in every target other than
`.agent/authored/f256-r4.md` and `.agent/last_block.md` — each expected 0 —
beside those two as the non-zero control. Report `git ls-files .remedy-wt | wc -l`,
expected 0.

### Handback

Rewrite `.agent/handoff.md` in C5 per docs/agents/handback_template.md. It
carries: `SESSION 1 of feature F256 · round 4`; the range `e23dad09..HEAD`; a
per-commit changed-files table with `+/-` from `git diff --numstat` compared
cell by cell against G10's figures; ONE LINE PER GATE G1 through G10 with its
real result; the deviations, including every guard re-expression constraint 6
required and every assertion constraint 8 made you RETARGET; the item-status
table with every C-item and every gate appearing exactly once; and the next
expected action, which is the sidebar ruling.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — only
reviewer-authored text sets those. GATEF256R3 above is reviewer-authored and
applied as a slice, which is not the same thing.

After C5: push with `git push -u origin feature/f256-diff-viewer-completion` and
report the outcome. Do NOT create a pull request and do NOT merge anything.
