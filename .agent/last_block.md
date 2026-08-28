### STEP T001c — F256 Diff viewer completion, round 3 (THE WIRING)

Goal: wire `loadDiffLanguageBundle` into `DiffView` so a diff of a supported
language really renders with highlight spans in the DOM, while an unknown
language still renders plain and asks for no bundle at all.

Base: `2251c6d4`, the tip of `feature/f256-diff-viewer-completion`. Every
reading below was taken there.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f256-r3.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 append the R2 verdict and the correction to `.agent/live_review.md`, the
  slip to `.agent/prose_slips.md`, and DECISION F256 D2 to `.agent/decisions.md`
- C3 the palette rules in `DiffView.module.css` and the wiring in `DiffView.tsx`
- C4 the contract-test extension
- C5 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f256-r3.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/prose_slips.md`
- `.agent/decisions.md`
- `apps/ui/src/components/diff/DiffView.module.css`
- `apps/ui/src/components/diff/DiffView.tsx`
- `tests/ui_contracts/test_diff_view_render.py`
- `.agent/handoff.md`

`apps/ui/src/api/diffHighlight.ts`, `apps/ui/src/api/diffViewModel.ts`,
`apps/ui/src/components/shell/RemedyShell.tsx` and
`apps/ui/src/components/diff/DiffFileSidebar.tsx` are NOT edited. The importer
lives in `DiffView.tsx`, which is what keeps the shell out of this round.

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
   `git show <C0a>:.agent/authored/f256-r3.md`, never from this prompt's text.
4. AGENTS.md binds in full: self-review before every commit, one logical step
   per commit, `.agent/plan.md` current before every commit, clean tree, push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under
   the gitignored `.remedy-wt/`. The primary checkout satisfies
   `git status --porcelain` empty at every commit.
6. Shell forms rejected by this session's guard are RE-EXPRESSED through
   `python3 - <<'PY'`, never skipped and never weakened. Report each one.
7. THE GUARD THIS ROUND IS MOST LIKELY TO BREAK, named because a round already
   shipped a red tip this way (finding `R-0697`).
   `tests/ui_contracts/test_diff_view_render.py` at `2251c6d4` requires
   `DiffView.tsx` to CALL every name in its `DELEGATED_RULES` tuple, and
   `splitLineIntoIntralineSegments` is one of them. The wiring therefore
   COMPOSES that call rather than replacing it —
   `composeHighlightedRuns(splitLineIntoIntralineSegments(row.line), language)` —
   and the string `splitLineIntoIntralineSegments(` still occurs in the
   comment-stripped source afterwards. Report that count.
8. THE SECOND GUARD ON THE SAME FILE. That test's
   `REIMPLEMENTED_RULE_SPELLINGS` tuple forbids the comment-stripped source of
   `DiffView.tsx` from containing `200`, `.length >`, `sort(`,
   `DIFF_VIRTUAL_ROW_HEIGHT_PX`, `Math.floor(`, `Math.ceil(` or `.slice(0,`.
   None of them may be introduced. Report the count of each after C3.
9. THE THIRD GUARD. That test also requires every `styles.<name>` the component
   names to have a real rule in `DiffView.module.css`. Every class the wiring
   introduces therefore ships in the SAME commit as the rule that defines it.
10. THE CSS GUARD. `tests/ui_contracts/test_design_drift.py` fails any
    `var(--remedy-…)` used under `apps/ui/src` but defined nowhere there. Every
    custom property the new rules name is already defined in
    `apps/ui/src/styles/tokens.css` at `2251c6d4`; introduce no new one.

### SPEC — the production code of C3

Production code is DESCRIBED here, not sliced.

S1. In `DiffView.module.css`, add one rule per highlighted token kind, using
ONLY the custom properties DECISION F256 D2 names, each already defined in
`apps/ui/src/styles/tokens.css` at `2251c6d4`:
`.tokComment` → `color: var(--remedy-ink-soft, #6f82a8)`;
`.tokString` → `color: var(--remedy-green-500, #34c27e)`;
`.tokNumber` → `color: var(--remedy-orange-400, #f5a34e)`;
`.tokKeyword` → `color: var(--remedy-blue-700, #2459d6)`.
Each carries the literal fallback its token already uses elsewhere in this
sheet's idiom. `plain` gets NO rule and NO class: it inherits the row's colour,
which is what makes an unhighlighted run indistinguishable from today's output.
A comment above the block records that these four are DECISION F256 D2's
mapping, that no new hue and no new custom property enters the sheet, and how to
reverse it.

S2. In `DiffView.tsx`, add a module-level importer constant whose body is
`() => import("../../api/diffHighlight")`. A DYNAMIC import is what makes the
tokenizer a lazy chunk rather than main-chunk weight, which is the whole of what
DECISION F256 D1 promised; the WHY comment says so and names D1.

S3. Add a module-level `Record<DiffHighlightTokenKind, string>` mapping each
kind to its class, with `plain` mapped to the EMPTY STRING — the same shape and
the same reason as the existing `DIFF_LINE_KIND_CLASS` above it, which maps
`ctx` to the empty string because an unchanged line wears no extra class.

S4. `DiffView` holds a per-path language map in state, keyed by file path, whose
value is the language id or `null`. A `useEffect` keyed on the envelope asks
`loadDiffLanguageBundle(path, importer)` once per DISTINCT file path in the
envelope and stores the answer's `language`. The effect declares a cancellation
flag, checks it before storing, and returns a cleanup that sets it — the same
shape `RemedyShell.tsx`'s read effect uses at `2251c6d4` and that
`tests/ui_contracts/test_diff_viewer_mount.py` pins there. A NEW ENVELOPE STARTS
A NEW MAP, for the reason the collapse set is already reset on a new envelope.

S5. THE ACCEPTANCE PROPERTY, and the reason the importer is passed rather than
called directly: for a path that renders plain, `importBundle` IS NEVER INVOKED.
`loadDiffLanguageBundle` already guarantees it and its vitest suite pins the
call count at zero; this round must not defeat it by asking for the bundle
before asking for the language.

S6. A line row renders `composeHighlightedRuns(splitLineIntoIntralineSegments(
row.line), language)`, where `language` is the map's entry for that row's file
path, or `null` while the answer has not arrived. Each run becomes ONE element:
a run with `marked` true stays the `mark` element wearing `styles.intraline` it
is today, and every run additionally wears its kind's class when that class is
non-empty. The existing intraline behaviour is preserved exactly — this round
adds colour to the runs, it does not change which characters are marked.

S7. A row whose file path has no entry yet, or whose language is `null`, renders
exactly as it does today: `plain` carries no class, so the DOM for an
unhighlighted line is unchanged and the truncation notice, the spacers, the hunk
heads and the two gutters are untouched.

### SPEC — the contract test of C4

S8. Extend `tests/ui_contracts/test_diff_view_render.py`. Add one class holding
tests that: the component CALLS `loadDiffLanguageBundle` and
`composeHighlightedRuns`; the importer is a DYNAMIC `import(` of the highlight
module rather than a static import of it; every class in the new kind mapping
has a real rule in `DiffView.module.css`, reusing that file's existing
`css_class_names` scanner rather than a second one; and `plain` maps to the
empty string, so no rule is demanded for it. Each assertion reads the
COMMENT-STRIPPED source through the scanners already in that file.

S9. Do NOT weaken, delete or relax any existing assertion in that file, and do
not add `loadDiffLanguageBundle` or `composeHighlightedRuns` to
`DELEGATED_RULES` — that tuple is the model's decidable rules, and widening it
would change what an existing test means.

### The authored slices

<<<SLICE PLANF256R3
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
| lazy bundles, DiffView wiring, the palette | done | this round |
| rule on the sidebar's treatment | open | a ruling to record, not code |
| measure the 10k-line fixture | open | needs a real fixture and a real run |

## Next Steps
1. Rule on the file sidebar's visual treatment and record the authority, which
   is the last of F256's three pieces that is a ruling rather than code.
2. Measure the 10k-line fixture end to end and record the numbers in the
   feature file's Built State.
3. Run the integration gate, then the closure sequence.

## Risks
- `tests/ui_contracts/test_diff_view_render.py` reads the comment-stripped
  source of `DiffView.tsx` and requires every `styles.` class it names to have
  a rule in `DiffView.module.css`, so a class and its rule land together.
- Nothing in this repository renders `DiffView.tsx`, so the wiring is gated by
  that source contract and by `tsc --noEmit`, never by a DOM test.
<<<END PLANF256R3

<<<SLICE GATEF256R2
Gate: F256 R2 — the COMPOSITION round. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran each independently at `2251c6d4` rather than reading the handback's numbers.

TRANSPORT AGAIN COVERS THE EMISSION rather than only the worker's self-consistency, which docs/agents/planner_reviewer_prompt.md §3 item 37 requires a verdict to distinguish: the reviewer's own scratch original `.remedy-wt/f256-r2-block.md` existed before the worker did, and the committed `.agent/authored/f256-r2.md` blob at `8ba2684a` is BYTE EQUAL to it at 19466 bytes, sha256 `449a54ea4a2b799b8687a9c649133fc5bb87c6d463a066cf137cb0c7704f88ae`. At `06ee19ea` that path and `.agent/last_block.md` are ONE blob.

BOTH APPENDS WERE RECONSTRUCTED BY THE REVIEWER. For `.agent/live_review.md` and for `.agent/prose_slips.md` alike, the `7b23c46a` blob plus a newline plus the round's slice equals the `5ae8b0af` blob exactly, the pre-round blob is a byte PREFIX of it — 1335995 growing to 1339712 and 12776 growing to 13551 — and in each file a byte flipped inside the FIRST appended paragraph is REJECTED. THE LEDGER MOVED EXACTLY AS THE BLOCK PREDICTED BEFORE THE ROUND RAN: registrations UNMOVED at 292 and all DISTINCT, `^Done: R-\d+ — ` UNMOVED at 43, `^Landed: R-` UNMOVED at 11, the OPEN SET computed AS A SET UNMOVED at 251, and `^Gate: F\d+ R\d+ — ` rising by exactly ONE from 97 to 98, with `Gate: F256 R1` occurring exactly once.

THE COMPOSITION WAS RUN BY THE REVIEWER AGAINST THE REAL INTRALINE PRODUCER, not against a synthetic segment list, which is the only way to learn whether the two cuts really compose. In a disposable worktree at `739d31e0` under the DECISION F037 D10 recipe, `splitLineIntoIntralineSegments` was fed hostile span tables — overlapping, out of order, negative, zero-length and running past the end — and its real output was composed with the token cut over the same line. Across 5000 generated cases, of which 3514 carried at least one marked character and 2976 carried BOTH marked and unmarked characters in the same line, there were ZERO violations of all three invariants: the runs' concatenation reproduced the content, every character kept the `marked` the producer gave it, and every character kept the `kind` `tokenizeDiffLine` gave that position. No two adjacent runs agreed on both fields. The probe carried its own coverage assertion, so a run in which the marked cases collapsed to zero would have FAILED rather than passed quietly.

A CORRECTION TO THE R1 ENTRY, appended here rather than by editing it, because that record is append-only and item 20 forbids rewriting landed text. The R1 entry reports a 4000-line fuzz of the tokenizer "scanned against every declared grammar". The generator behind that reading used a 32-bit LCG evaluated in double-precision floating point, where the multiply exceeds 2^53 and the low bits degenerate, so neither the language selection nor the character selection was as varied as the sentence implies and the grammar coverage it claims was not in fact measured. THE PROPERTY ITSELF STANDS AND IS NOW MEASURED PROPERLY: re-run at `739d31e0` with a 32-bit xorshift generator, the tokenizer's concatenation invariant and its merge rule held with ZERO violations over 4452 DISTINCT lines across every declared grammar. The separate R1 reading that every VALUE of `DIFF_SUPPORTED_LANGUAGES` is an own key of `DIFF_HIGHLIGHT_GRAMMARS` is unaffected: it iterated the key set directly and used no generator at all.

THE SUITES WERE RE-RUN IN THE PRIMARY CHECKOUT, one pytest process at a time, each exit 0 and each equal to the handback's figure: `tests/orchestration/test_test_runner.py` 52 passed, the two diff contracts 27 passed, the three repo-wide sweeps 222 passed with 2 skipped, `tests/orchestration/test_integrity_gate.py` with `tests/regression/test_resource_safety.py` 37 passed, and the canary `tests/cli/test_golden_path.py` 42 passed. THE STRUCTURE IS CLEAN: the path set over `7b23c46a..2251c6d4` is exactly the eight files the handback names, insertions per commit are 301, 183, 13, 16, 327 and 121 — each under 500 — every commit is single-parent, `apps/ui/dist` is untracked so the unordered warm build the worker declared left the tree clean, and `git rev-parse` of the branch tip equals `origin/feature/f256-diff-viewer-completion`.

THE WORKER'S UNORDERED ACTION WAS CORRECT AND IS RECORDED AS SUCH. It ran a vite build before the suites because C3 made `src` newer than `dist/index.html`, which would have pushed the `tests/ui_server/` supervisors into an auto-build inside their start budget — the class finding `R-0708` describes. The block did not order it, the worker declared it, and the reviewer confirms `apps/ui/dist` is gitignored and `git ls-files` over it is empty, so nothing entered the index.
<<<END GATEF256R2

<<<SLICE SLIPSF256R2
2026-08-28 · F256 R2 · The reviewer's R1 fuzz probe used a 32-bit LCG evaluated in floating point, so its low bits degenerated and its language and character coverage were narrower than the R1 entry's wording implies; re-measured with a xorshift generator at F256 R2, the property held over 4452 distinct lines. The correction is appended to the record in the R2 entry.
<<<END SLIPSF256R2

<<<SLICE DECF256R2
## DECISION F256 D2 (2026-08-28, F256 R3) — the diff surface's syntax palette is four custom properties the shipped token sheet already defines, and no new hue enters the product

CONTEXT. A rendered highlight needs colour, and colour on this surface needs an
authority. Measured at `2251c6d4`: no file under `docs/ui/design_reference/`
contains the word "syntax", and amendment A4 of
`docs/roadmap/features/T5_F037.md` names the authorities that bind this surface
— that file's own binding CSS, `component_spec.md` for the entry point and
`assets_spec.md` for the mono family — none of which rules a token palette. The
CANONICAL DESIGN REFERENCE banner forbids inventing a visual language, so the
palette is DERIVED or it does not ship.

CHOSEN, and it is a derivation in the same sense DECISION F037 D9 was when it
ruled intraline emphasis from this sheet's own two hues: each token kind takes a
custom property `apps/ui/src/styles/tokens.css` ALREADY defines — `comment` to
`--remedy-ink-soft`, the property this sheet already gives the line-number
gutter, so a comment reads as the same rank of de-emphasis; `string` to
`--remedy-green-500`, `number` to `--remedy-orange-400` and `keyword` to
`--remedy-blue-700`, the product's own accent, which is why it goes to the kind
a reader scans for first. `plain` takes NO rule and NO class and simply inherits
the row's colour. No new custom property is introduced and the token sheet is
not extended.

ALTERNATIVES CONSIDERED. (a) Import a highlighter's theme. Rejected: DECISION
F256 D1 already rules out the dependency, and a second colour system in a
product that has one is exactly what the banner forbids. (b) Ask the operator to
rule the palette. Rejected because docs/agents/planner_reviewer_prompt.md §2
forbids a ruling request and §4 item 7 requires the reviewer to rule loudly and
reversibly instead. (c) Colour more kinds. Rejected because the token set is
closed at five by DECISION F256 D1 and a distinction with no property behind it
would have to invent one.

CONSEQUENCE. The mapping is enforced by a guard that already exists rather than
by discipline: `tests/ui_contracts/test_design_drift.py` fails any
`var(--remedy-…)` used under `apps/ui/src` but defined nowhere there, and
`tests/ui_contracts/test_diff_view_render.py` fails any `styles.` class the
component names without a rule behind it. The palette is also DELIBERATELY
COARSE — four coloured kinds — and a reader wanting per-language precision will
not find it here, because the tokenizer behind it is per-line by ruling.

REVERSE by deleting this decision and the four rules it authorises from
`apps/ui/src/components/diff/DiffView.module.css`; the runs then render in the
row's own colour and the wiring stays intact, because the class mapping maps
`plain` to the empty string already.
<<<END DECF256R2

`PLANF256R3` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF256R2`,
`SLIPSF256R2` and `DECF256R2` are APPENDS to `.agent/live_review.md`,
`.agent/prose_slips.md` and `.agent/decisions.md`, each separated from its
file's existing final line by exactly one blank line.

### Done when

G1 HYGIENE. Read `.agent/STOP` with `os.path.exists` before C0a and again
before C3; report both answers, and stop after the commit in hand if it exists.
Report `git rev-parse HEAD` before C0a — it must equal `2251c6d4` —
`git branch --show-current`, and `git status --porcelain | wc -l` after each of
C0a, C0b, C1, C2, C3 and C4.

G2 TRANSPORT. One digest comparison: sha256 of
`git show <C0a>:.agent/authored/f256-r3.md` against the reviewer's own original
at `.remedy-wt/f256-r3-block.md`, reporting both digests, the byte length and
equality. That original predates this worker, so the reading covers more than
self-consistency; say so. Report that `<C0b>:.agent/authored/f256-r3.md` and
`<C0b>:.agent/last_block.md` are ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF256R3 including the
trailing newline — report `True` or `False` — with `wc -l` under 50 and the
counts of lines exactly `## Goal` and exactly `## Next Steps`.

G4 THE RECORD AT C2, two readers per appended file. (a) The `2251c6d4` blob plus
a newline plus the slice equals the C2 blob, reported separately for
`.agent/live_review.md` with GATEF256R2, `.agent/prose_slips.md` with
SLIPSF256R2 and `.agent/decisions.md` with DECF256R2; NEGATIVE CONTROL for each,
flipping one byte at an offset your script confirms lies INSIDE THE FIRST
appended paragraph and reporting the equality now `False`. (b) Let N be the
paragraph count of each slice, COUNTED BY YOUR SCRIPT from the slice and never
taken from this block, ignoring an empty trailing unit; report N and that the
LAST N blank-line units of each file match those paragraphs IN ORDER. Report
each pre-round blob is a byte PREFIX, with both lengths.

G5 THE LEDGER AT C2. Over the C2 blob of `.agent/live_review.md` and over the
`2251c6d4` blob beside it, report: `^- R-\d+ — ` and whether all DISTINCT;
`^Done: R-\d+ — `; `^Landed: R-`; `^Gate: F\d+ R\d+ — `; and the OPEN SET as a
set. This round registers and resolves nothing, so every figure is UNMOVED
except `^Gate: F\d+ R\d+ — `, which rises by exactly ONE. Report that
`Gate: F256 R2` occurs exactly 1 time.

G6 THE GUARDS ON `DiffView.tsx` AT C3, which is where this round is most likely
to ship a red tip. Over the COMMENT-STRIPPED source at C3, using the scanners in
`tests/ui_contracts/test_diff_view_render.py` itself, report: the count of
`splitLineIntoIntralineSegments(`, which must be at least 1 (constraint 7); the
count of each forbidden spelling constraint 8 lists, each of which
must be 0; the set of `styles.<name>` the component names and the set of classes
`DiffView.module.css` defines, and that the first is a SUBSET of the second,
printing any difference; and the set of `var(--remedy-…)` the stylesheet names
at C3 with confirmation that each is defined under `apps/ui/src`.

G7 THE RED-PROOF AT C4, in a disposable worktree, following DECISION F037 D10
and never in the primary checkout. Report the UNMUTATED CONTROL FIRST in that
worktree, then each mutation, with exit code and passed/failed counts for every
run, using

    ["python3", "-m", "pytest", "tests/ui_contracts/test_diff_view_render.py", "-q"]

run with `cwd` set to the WORKTREE. THE MUTATIONS, each applied alone and
reverted before the next, inside the worktree, each of which must turn that file
RED: (i) delete the `.tokKeyword` rule from
`apps/ui/src/components/diff/DiffView.module.css` while the component still
names the class; (ii) replace the dynamic `import(` in the importer with a
static import of the same module. Report the control again, green. Report
`git worktree list` and `git status --porcelain | wc -l` in the primary after
removal.

G8 THE SUITES AT C4. One pytest process at a time, from the repository root, in
the PRIMARY checkout, each with its exit code and its own passed/failed line:
`tests/ui_contracts/` in full; `tests/orchestration/test_test_runner.py` (it
spawns `npx vitest run` under a 30-second timeout — report the wall clock, and
warm `apps/ui/dist` first if `src` is newer, declaring it); `tests/ui_server/`;
`tests/regression/test_resource_safety.py`;
`tests/orchestration/test_integrity_gate.py`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. Additionally run
`tsc --noEmit` in `apps/ui` and report its real exit code. If any is red, STOP
and write the handback with the full untruncated failure list.

G9 STRUCTURE, over `2251c6d4..<C4>` — the range ending BEFORE the handback
commit, so `.agent/handoff.md` is expected in the change set but NOT in this
range. Report `git diff --name-only` and both residues against the change set
with `.agent/handoff.md` set aside, printed in both directions and both expected
empty. Report each commit's insertions from `git diff --numstat`, each under
500, and that each of C0a, C0b, C1, C2, C3 and C4 is single-parent. Report,
counted affirmatively over each file's C4 content, the number of lines beginning
`<<<SLICE ` and `<<<END ` in every non-authored target — each expected 0 —
beside the same counts over `.agent/authored/f256-r3.md` as the non-zero
control. Report `git ls-files .remedy-wt | wc -l`, expected 0.

### Handback

Rewrite `.agent/handoff.md` in C5 per docs/agents/handback_template.md. It
carries: `SESSION 1 of feature F256 · round 3`; the range `2251c6d4..HEAD`; a
per-commit changed-files table with `+/-` from `git diff --numstat` compared
cell by cell against G9's figures; ONE LINE PER GATE G1 through G9 with its real
result; the deviations, including every guard re-expression constraint 6
required; the item-status table with every C-item and every gate appearing
exactly once; and the next expected action.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — only
reviewer-authored text sets those. GATEF256R2 above is reviewer-authored and
applied as a slice, which is not the same thing.

After C5: push with `git push -u origin feature/f256-diff-viewer-completion` and
report the outcome. Do NOT create a pull request and do NOT merge anything.
