### STEP T003 — F256 Diff viewer completion, round 5 (THE SIDEBAR RULING)

Goal: rule on the file sidebar's visual treatment, record the ruling as a
DECISION, and ship it — so the deferral `DiffFileSidebar.tsx` has carried in its
own header since F037 is discharged rather than deferred a further time.

Base: `78e71b3c`, the tip of `feature/f256-diff-viewer-completion`. Every
reading below was taken there.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f256-r5.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 append the R4 verdict to `.agent/live_review.md` and DECISION F256 D3 to
  `.agent/decisions.md`
- C3 the sidebar rules in `DiffView.module.css` and the classes in
  `DiffFileSidebar.tsx`
- C4 the contract-test extension
- C5 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f256-r5.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/decisions.md`
- `apps/ui/src/components/diff/DiffView.module.css`
- `apps/ui/src/components/diff/DiffFileSidebar.tsx`
- `tests/ui_contracts/test_diff_file_sidebar.py`
- `.agent/handoff.md`

`DiffView.tsx`, `apps/ui/src/api/diffHighlight.ts`,
`apps/ui/src/api/diffHighlightGrammars.ts` and `RemedyShell.tsx` are NOT edited.

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
   `git show <C0a>:.agent/authored/f256-r5.md`, never from this prompt's text.
4. AGENTS.md binds in full: self-review before every commit, one logical step
   per commit, `.agent/plan.md` current before every commit, clean tree, push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under
   the gitignored `.remedy-wt/`. The primary checkout satisfies
   `git status --porcelain` empty at every commit.
6. Shell forms rejected by this session's guard are RE-EXPRESSED through
   `python3 - <<'PY'`, never skipped and never weakened. Report each one.
7. READ `tests/ui_contracts/test_diff_file_sidebar.py` IN FULL BEFORE EDITING
   `DiffFileSidebar.tsx`. Its `TestTheSidebarDerivesNothing` class forbids a set
   of spellings in that component's comment-stripped source and its
   `TestEverySummaryFieldIsReallyDrawn` class requires every summary field to be
   read. Report the forbidden set you found and the count of each after C3; none
   may be introduced, and no field may stop being drawn.
8. NO EXISTING ASSERTION IS WEAKENED, DELETED OR RELAXED to make a gate pass.
   If an existing guard genuinely contradicts this block, STOP and hand back
   with the contradiction stated.
9. `tests/ui_contracts/test_design_drift.py` fails any `var(--remedy-…)` used
   under `apps/ui/src` but defined nowhere there. Every custom property the new
   rules name is already defined in `apps/ui/src/styles/tokens.css` at
   `78e71b3c`; introduce no new one.
10. The sidebar's classes ship in the SAME commit as the rules that define them,
    for the reason `DiffView.tsx` already lives under: a CSS module hands back
    `undefined` for a name with no rule, and the element then ships unstyled.

### SPEC — the production code of C3

S1. In `apps/ui/src/components/diff/DiffView.module.css`, add the sidebar rules
DECISION F256 D3 rules, using ONLY custom properties already defined in
`apps/ui/src/styles/tokens.css` at `78e71b3c`:
`.filePath` → the mono family via `var(--remedy-font-mono, …)` with the same
literal stack fallback the rules above it use, and `font-feature-settings:
"liga" 0` declared AFTER any `font` shorthand;
`.fileMeta` → `color: var(--remedy-ink-soft, #6f82a8)`;
`.statAdd` → `color: var(--remedy-green-500, #34c27e)`;
`.statDel` → `color: var(--remedy-orange-400, #f5a34e)`.
A comment above the block records that these are DECISION F256 D3's mapping,
that no new hue and no new custom property enters the sheet, that ligatures are
off on this surface for the reason `assets_spec.md` section 2 already gives the
diff rows, and how to reverse it.

S2. In `DiffFileSidebar.tsx`, import the sheet and put those classes on the
elements that already exist: the path `strong` takes `.filePath`; the status,
the old-path span and the hunk-count span take `.fileMeta`; the `+N` span takes
`.statAdd` and the `-N` span takes `.statDel`. The note span takes `.fileMeta`.
NO ELEMENT IS ADDED, REMOVED OR REORDERED and no text changes — this round
dresses the markup that is already there.

S3. THE DEFERRAL IN THE HEADER IS REPLACED, NOT LEFT STANDING. The paragraph
beginning "NO CLASS ON ANY ELEMENT BELOW" is now false and must be rewritten to
record the ruling instead: that DECISION F256 D3 rules this surface, that the
treatment is DERIVED from the diff body's own vocabulary rather than invented,
and — as a deliberate absence a reader will search here for — that Remedy does
NOT draw a proportional stats bar, because the two counts already carry the
magnitude and a bar would be a visual primitive no authority defines. Cite D3.

### SPEC — the contract test of C4

S4. Extend `tests/ui_contracts/test_diff_file_sidebar.py` with one class that:
scans the classes `DiffFileSidebar.tsx` names and the classes
`DiffView.module.css` defines, and asserts the first is a SUBSET of the second,
printing any difference; asserts each of the four class names S1 introduces is
really named by the component; and asserts the component contains no
`aria-hidden` and no element added beyond those it already draws, by pinning
that the count of `<span` in the comment-stripped source is UNCHANGED from
`78e71b3c` — report that base count and use it.

S5. Write the two scanners this file does not yet have — one for
`styles.<name>` in the component and one for `.<name>` rules in the stylesheet —
modelled on the ones already in `tests/ui_contracts/test_diff_view_render.py`,
and pin each with a NOT-VACUOUS test proving it returns a non-empty set on the
real files, in the shape `TestTheStripperIsNotVacuous` already uses in this
file. A scanner that silently returns nothing would make every assertion above
pass over an empty set.

### The authored slices

<<<SLICE PLANF256R5
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
| make the lazy load real, repairing `R-0732` | done | `8bcff3db` |
| rule on the sidebar's treatment | done | this round |
| measure the 10k-line fixture | open | needs a real fixture and a real run |

## Next Steps
1. Measure the 10k-line fixture end to end and record the numbers in the
   feature file's Built State, which is F256's last unbuilt piece.
2. Update `docs/roadmap/features/T5_F256.md` Built State with the three pieces
   and their test files.
3. Run the integration gate, then the closure sequence.

## Risks
- `tests/ui_contracts/test_diff_file_sidebar.py` and
  `tests/ui_contracts/test_diff_view_render.py` both read comment-stripped
  sources; a class and its rule must land in one commit or the element ships
  unstyled.
- The 10k-line measurement must be a real run against a real fixture; a budget
  is re-derived from a re-measured maximum and never raised by hand.
<<<END PLANF256R5

<<<SLICE GATEF256R4
Gate: F256 R4 — the REPAIR round, which registered `R-0732` and fixed it in the same round. THE ROUND PASSED on every gate its block ordered, G1 through G10, and the reviewer re-ran each independently at `78e71b3c`.

TRANSPORT COVERS THE EMISSION: the reviewer's own scratch original `.remedy-wt/f256-r4-block.md` predates the worker, and the committed `.agent/authored/f256-r4.md` blob at `47fbc7e9` is BYTE EQUAL to it at 21034 bytes, sha256 `a7e58e46339fe1458d0b0d478bea25662cf0dfc81250196178b3bb9c97d6d4b8`. Both appends at `f996e727` reconstruct byte for byte from the `e23dad09` blob plus a newline plus their slice, each pre-round blob is a byte PREFIX, and in each a byte flipped inside the FIRST appended paragraph is REJECTED.

THE LEDGER MOVED EXACTLY AS A REGISTERING ROUND SHOULD: registrations 292 to 293 and all DISTINCT, the OPEN SET computed AS A SET 251 to 252, `^Gate: F\d+ R\d+ — ` 99 to 100, `^Done: R-\d+ — ` and `^Landed: R-` both UNMOVED, `Gate: F256 R3` occurring exactly once, and `R-0732` present as exactly one registration carrying no `Done:` and no `Landed:` line — which is the correct disk state for a finding whose repair has landed but whose resolution only a reviewer may author.

`R-0732` IS GENUINELY REPAIRED, AND THE REVIEWER MEASURED THE REPAIR RATHER THAN THE INTENTION. At `78e71b3c` the reviewer ran `npx vite build` itself: exit 0, and the count of output lines carrying both `dynamically imported` and `statically imported` is ZERO, against 1 at `e23dad09`. The build emits a real separate chunk, `dist/assets/diffHighlightGrammars-o9XqnLhb.js` at 1.70 kB, so the grammar tables genuinely left the main bundle rather than being re-described as having left it. In `DiffView.tsx` the grammar module is named only by a dynamic `import(` and by a `typeof import(…)` TYPE position, which carries no `from` clause and links nothing — the static imports there name `diffHighlight` alone.

THE REFACTOR CHANGED NO VALUE, and the reviewer proved it by EXECUTING both tables rather than by reading them. In two disposable worktrees, the grammar mapping was dumped from `apps/ui/src/api/diffHighlight.ts` at `e23dad09` and from `apps/ui/src/api/diffHighlightGrammars.ts` at `78e71b3c` and compared field by field: the language id sets are IDENTICAL at 11 ids, no id's comment openers, string delimiters or keyword set differs, and the total keyword count is 271 on both sides. A refactor that quietly drops a keyword is the one failure this comparison exists to catch, and it did not happen.

RE-RUN IN THE PRIMARY CHECKOUT, one pytest process at a time, each exit 0 and each equal to the handback's figure: `tests/ui_contracts/` 659 passed with 4 skipped — four more than the round before, which is the new module's own coverage — `tests/orchestration/test_test_runner.py` 52 passed, the canary `tests/cli/test_golden_path.py` 42 passed, and `tsc --noEmit` exit 0. The branch tip equals `origin/feature/f256-diff-viewer-completion`, the primary checkout reads `git status --porcelain` empty, and `gh pr list --state open` is `[]`.

THE WORKER RETARGETED ONE ASSERTION AND WEAKENED NONE, which is the distinction constraint 8 of that block exists to force: the dynamic-import test now names the grammar module, and the specifier constant it used survives as the subject of the NEW test that pins `R-0732`'s property in the static direction. `DELEGATED_RULES` and `REIMPLEMENTED_RULE_SPELLINGS` are untouched. The worker also flagged, without acting on it, that `diffHighlightGrammarFor` is covered from `diffHighlight.test.ts` rather than from a test file named after its own source; that sits at an angle to the AGENTS.md discoverability convention and is recorded here as a known, deliberate consequence of the block's closed change set rather than as a defect.
<<<END GATEF256R4

<<<SLICE DECF256R3
## DECISION F256 D3 (2026-08-28, F256 R5) — the diff file sidebar takes its treatment from the diff body's own vocabulary, and Remedy draws no proportional stats bar

CONTEXT. `apps/ui/src/components/diff/DiffFileSidebar.tsx` has carried a
DEFERRAL in its own header since F037 built it: semantic markup, real numbers,
no class, because the binding CSS of `docs/roadmap/features/T5_F037.md` defines
no rule for a sidebar and the CANONICAL DESIGN REFERENCE banner forbids
inventing a visual language. Measured at `78e71b3c`: no file under
`docs/ui/design_reference/` contains the word "syntax" or rules this surface,
and the only sidebar `component_spec.md` names is `BrandSidebar`, which is the
left brand rail and not this panel. F256's own feature file states in as many
words that the ruling is this feature's to make and to record.

CHOSEN, by DERIVATION rather than invention, which is the same method DECISION
F037 D9 used for intraline emphasis and DECISION F256 D2 used for the syntax
palette. The sidebar borrows the vocabulary the diff body has already taught the
reader: a file path is set in the mono family with ligatures OFF, for the reason
`assets_spec.md` section 2 gives every diff surface — a path must render as the
characters that are really in it; the added and removed counts take the
product's own green and orange, the same two hues the diff rows tint with; and
every other piece of metadata takes `--remedy-ink-soft`, the same rank of
de-emphasis this sheet already gives the line-number gutter. No new custom
property is introduced and `apps/ui/src/styles/tokens.css` is not extended.

THE DELIBERATE ABSENCE, recorded because a reader will search for it and text
search cannot find code that does not exist: Remedy does NOT draw a proportional
stats bar in this sidebar. The feature file's Design section says "paths + stats
bars", and this decision reads that as satisfied by the counts themselves. A bar
is a visual primitive no authority in this repository defines — it needs a
track, a fill, a minimum width for a one-line change and a rule for what happens
when a file is pure deletion — and inventing all four here is exactly what the
banner forbids. The counts already carry the magnitude, and they carry it
exactly rather than approximately.

ALTERNATIVES CONSIDERED. (a) Draw the bar anyway. Rejected: four undefined
sub-decisions, and a bar that lies at small widths is worse than a number that
does not. (b) Defer the ruling again. Rejected because F037 already deferred it
once, F256 exists to close exactly that kind of deferral, and a second deferral
would make the promise permanent. (c) Ask the operator to rule it. Rejected
because docs/agents/planner_reviewer_prompt.md §2 forbids a ruling request and
§4 item 7 requires the reviewer to rule loudly and reversibly instead.

CONSEQUENCE. The sidebar stops shipping unstyled, and the ruling is enforced by
guards that already exist: `tests/ui_contracts/test_design_drift.py` fails any
custom property used but not defined under `apps/ui/src`, and the contract test
this round extends fails any class the component names without a rule behind it.
The absence of the bar is enforced by nothing, which is why it is written down
here and in the component's header rather than left to be rediscovered.

REVERSE by deleting this decision and the sidebar rules it authorises from
`apps/ui/src/components/diff/DiffView.module.css`, and restoring the deferral
paragraph in `DiffFileSidebar.tsx` from git history at `78e71b3c`; the sidebar
then returns to semantic markup with no class, which is a state it is known to
work in.
<<<END DECF256R3

`PLANF256R5` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF256R4` and
`DECF256R3` are APPENDS to `.agent/live_review.md` and `.agent/decisions.md`.
For each, append exactly what gate G4(a) measures — the pre-round blob, one
newline, then the slice — whatever blank lines that file already ends with.

### Done when

G1 HYGIENE. Read `.agent/STOP` with `os.path.exists` before C0a and again
before C3; report both, and stop after the commit in hand if it exists. Report
`git rev-parse HEAD` before C0a — it must equal `78e71b3c` —
`git branch --show-current`, and `git status --porcelain | wc -l` after each of
C0a, C0b, C1, C2, C3 and C4.

G2 TRANSPORT. One digest comparison: sha256 of
`git show <C0a>:.agent/authored/f256-r5.md` against the reviewer's own original
at `.remedy-wt/f256-r5-block.md`, reporting both digests, the byte length and
equality; that original predates this worker, so say the reading covers more
than self-consistency. Report that `<C0b>:.agent/authored/f256-r5.md` and
`<C0b>:.agent/last_block.md` are ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF256R5 including the
trailing newline — report `True` or `False` — with `wc -l` under 50 and the
counts of lines exactly `## Goal` and exactly `## Next Steps`.

G4 THE RECORD AT C2, two readers per appended file. (a) The `78e71b3c` blob plus
a newline plus the slice equals the C2 blob, reported separately for
`.agent/live_review.md` with GATEF256R4 and `.agent/decisions.md` with
DECF256R3; NEGATIVE CONTROL for each, flipping one byte at an offset your script
confirms lies INSIDE THE FIRST appended paragraph and reporting the equality now
`False`. (b) Let N be each slice's paragraph count, COUNTED BY YOUR SCRIPT from
the slice and never taken from this block, ignoring an empty trailing unit;
report N and that the LAST N blank-line units of each file match those
paragraphs IN ORDER. Report each pre-round blob is a byte PREFIX.

G5 THE LEDGER AT C2. Over the C2 blob and the `78e71b3c` blob beside it, report
`^- R-\d+ — ` and whether all DISTINCT, `^Done: R-\d+ — `, `^Landed: R-`,
`^Gate: F\d+ R\d+ — `, and the OPEN SET as a set. This round registers and
resolves nothing, so every figure is UNMOVED except `^Gate: F\d+ R\d+ — `,
which rises by exactly ONE. Report that `Gate: F256 R4` occurs exactly 1 time,
and that `R-0732` still carries no `Done:` and no `Landed:` line.

G6 THE SIDEBAR GUARDS AT C3. Over the comment-stripped `DiffFileSidebar.tsx` at
C3, report: the count of each spelling `TestTheSidebarDerivesNothing` forbids,
each of which must be 0; that every summary field
`TestEverySummaryFieldIsReallyDrawn` requires is still read; the count of
`<span` beside the same count at `78e71b3c`, which must be EQUAL; and the set of
`styles.<name>` the component names beside the set of classes
`DiffView.module.css` defines at C3, with confirmation that the first is a
SUBSET of the second and the difference printed. Report every `var(--remedy-…)`
the new rules name and that each is defined under `apps/ui/src`.

G7 THE RED-PROOF AT C4, in a disposable worktree, never in the primary
checkout. Report the UNMUTATED CONTROL FIRST, then each mutation, with exit code
and passed/failed counts, using

    ["python3", "-m", "pytest", "tests/ui_contracts/test_diff_file_sidebar.py", "-q"]

with `cwd` set to the WORKTREE. THE MUTATIONS, each applied alone and reverted
before the next, inside the worktree, each of which must turn that file RED:
(i) delete the `.statAdd` rule from
`apps/ui/src/components/diff/DiffView.module.css` while the component still
names the class; (ii) remove the `.filePath` class from the path element in
`DiffFileSidebar.tsx`. Report the control again, green, and `git worktree list`
plus `git status --porcelain | wc -l` in the primary after removal.

G8 THE SUITES AT C4. One pytest process at a time, from the repository root, in
the PRIMARY checkout, each with exit code and its own passed/failed line:
`tests/ui_contracts/` in full; `tests/orchestration/test_test_runner.py` (it
spawns `npx vitest run` under a 30-second timeout — report the wall clock, and
warm `apps/ui/dist` first if `src` is newer, declaring it); `tests/ui_server/`;
`tests/regression/test_resource_safety.py`;
`tests/orchestration/test_integrity_gate.py`; and the canary
`tests/cli/test_golden_path.py`. Additionally run `tsc --noEmit` in `apps/ui`
and report its real exit code. Every one must be exit 0. If any is red, STOP and
write the handback with the full untruncated failure list.

G9 STRUCTURE, over `78e71b3c..<C4>` — the range ending BEFORE the handback
commit, so `.agent/handoff.md` is expected in the change set but NOT in this
range, and `.agent/last_block.md` mirrors the authored blob by construction.
Report `git diff --name-only` and both residues against the change set with
`.agent/handoff.md` set aside, printed in both directions and both expected
empty. Report each commit's insertions from `git diff --numstat`, each under
500, and that each of C0a, C0b, C1, C2, C3 and C4 is single-parent. Report the
counts of lines beginning `<<<SLICE ` and `<<<END ` in every target other than
`.agent/authored/f256-r5.md` and `.agent/last_block.md` — each expected 0 —
beside those two as the non-zero control. Report
`git ls-files .remedy-wt | wc -l`, expected 0.

### Handback

Rewrite `.agent/handoff.md` in C5 per docs/agents/handback_template.md. It
carries: `SESSION 1 of feature F256 · round 5`; the range `78e71b3c..HEAD`; a
per-commit changed-files table with `+/-` from `git diff --numstat` compared
cell by cell against G9's figures; ONE LINE PER GATE G1 through G9 with its real
result; the deviations, including every guard re-expression constraint 6
required; the item-status table with every C-item and every gate appearing
exactly once; and the next expected action, which is the 10k-line measurement.

THIS IS THE LAST ROUND OF THIS SESSION. The handback additionally states that
rounds 1 through 4 were reviewed and PASSED, that this round awaits review, and
that the next session's FIRST action is Phase 1 rule 1 — read `.agent/STOP` —
BEFORE rule 2, the Open PR Gate.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — only
reviewer-authored text sets those. GATEF256R4 above is reviewer-authored and
applied as a slice, which is not the same thing.

After C5: push with `git push -u origin feature/f256-diff-viewer-completion` and
report the outcome. Do NOT create a pull request and do NOT merge anything.
