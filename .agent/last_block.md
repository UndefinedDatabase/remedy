STEP T002 — F037 Rendered diff viewer — ROUND 16

Goal: finish T002. The view model exists; this round draws it. `DiffView.tsx`
renders file rows, hunk heads that collapse on click, and line rows against the
binding CSS, and the last named piece of T002 — intraline emphasis — is ruled
rather than deferred again: Acceptance requires it, all three binding
authorities are silent about it, and DECISION F037 D9 settles the treatment
without inventing a hue or a token.

Base: the round starts from `68680786` on branch
`feature/f037-rendered-diff-viewer`. Nothing else is in flight.

Bundle, one commit each, in this order:
- C0a save this block verbatim to `.agent/authored/f037-r16.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 apply PLANF037R16 to `.agent/plan.md`
- C2 append GATER15 to `.agent/live_review.md` and SLIPR16 to
  `.agent/prose_slips.md`
- C3 append DECISION9 to `.agent/decisions.md` and AMENDA5 to
  `docs/roadmap/features/T5_F037.md`
- C4 write SPEC S1 and S2 into `apps/ui/src/api/diffViewModel.ts` and SPEC S3
  into `apps/ui/src/api/diffViewModel.test.ts`
- C5 write SPEC S4 into
  `apps/ui/src/components/diff/DiffView.module.css`
- C6 write SPEC S5 through S9 into a NEW file
  `apps/ui/src/components/diff/DiffView.tsx`
- C7 write SPEC S10 into a NEW file
  `tests/ui_contracts/test_diff_view_render.py`
- C8 rewrite `.agent/handoff.md` as the handback

Change set, and nothing outside it: `.agent/authored/f037-r16.md`,
`.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
`.agent/prose_slips.md`, `.agent/decisions.md`, `.agent/handoff.md`,
`docs/roadmap/features/T5_F037.md`, `apps/ui/src/api/diffViewModel.ts`,
`apps/ui/src/api/diffViewModel.test.ts`,
`apps/ui/src/components/diff/DiffView.module.css`,
`apps/ui/src/components/diff/DiffView.tsx`,
`tests/ui_contracts/test_diff_view_render.py`. Push the branch after C8. Create
no PR, merge nothing.

Constraints:
1. A slice between the markers is applied BYTE FOR BYTE. Never edit a slice,
   never reflow it, never fix a typo in it. If a slice looks wrong, apply it and
   say so in the handback's Deviations.
2. Production code and test code are DESCRIBED by the SPEC below, not sliced.
   Write them yourself. `apps/ui/src/api/diffViewModel.ts` is the idiom for the
   model half; `apps/ui/src/components/panels/DecisionInboxCard.tsx` is the
   idiom for a component in this package — read it before writing C6.
3. NO EXISTING DECLARATION in `DiffView.module.css` changes. S4 APPENDS rules;
   the five rules that stylesheet carries at `68680786` keep every byte,
   including the order of `font` and `font-feature-settings` that finding
   `R-0720` pinned.
4. The new CSS introduces NO `var()` and NO new custom property.
   `tests/ui_contracts/test_diff_surface_css.py` asserts that every token the
   sheet references is defined in `apps/ui/src/styles/tokens.css`, and
   `tokens.css` is the operator's design system, which this feature does not
   edit. The literal values in S4 are the reason that constraint is satisfiable.
5. Nothing in `packages/`, nothing in `tests/orchestration/`, nothing in
   `tests/ui_server/`, and no other file under `apps/ui/` is touched.
6. `apps/ui/src/api/diffViewModel.ts` still imports NOTHING after C4. The rule
   `tests/ui_contracts/test_diff_view_model.py` pins is unchanged and must stay
   green.
7. `DiffView.tsx` is NOT mounted anywhere this round, and that is deliberate,
   not an omission: `component_spec.md:113-116` puts the entry point in
   `DetailPopover` behind `onOpenDiff(taskId)`, and the feature file's Task
   slicing puts the L3 tab integration in T003. Say so in the component's own
   header comment so a reader does not file it as dead code.
8. Ruff runs under this repository's own configuration — line length 120, rules
   `E`, `F`, `W`, `I`, `UP`. Never `--isolated`.
9. Every destructive check runs inside a disposable `git worktree` under
   `.remedy-wt/`, never in the primary checkout, which reads
   `git status --porcelain` empty after every commit.
10. NO mutation red-proof of TypeScript is ordered — DECISION F037 D8 records
    why one cannot be run here, and gate G6 re-measures it rather than citing
    it. The red-proofs this round orders are of the PYTHON guard.

SPEC — `apps/ui/src/api/diffViewModel.ts`

S1. `export interface DiffLineSegment { text: string; marked: boolean }` and
    `export function splitLineIntoIntralineSegments(line: DiffLine):
    DiffLineSegment[]` — the line's `content` cut into consecutive segments, the
    marked ones being exactly the characters its `intraline` spans cover. WHY
    THIS IS HERE AND NOT IN THE COMPONENT: it is the last decidable rule of the
    rendering core, and DECISION F031 D5 keeps decidable rules in the layer the
    node-environment vitest config reaches. TOTAL, and this is the whole of its
    difficulty — the spans arrive from a payload and nothing upstream has
    checked their ARITHMETIC, only their shape. A span starting past the end of
    the content is dropped; a span running past the end is clamped to it; a
    negative or zero length is dropped; OVERLAPPING and out-of-order spans are
    resolved by marking the UNION of the characters they cover, so no character
    is ever emitted twice and the concatenation of every segment's `text` equals
    `content` exactly. An empty `intraline` yields one unmarked segment, and an
    empty `content` yields the empty array.

S2. The module header gains one sentence: the segments this function returns are
    what `DiffView.tsx` wraps in the intraline mark, and DECISION F037 D9 rules
    what that mark looks like.

S3. Vitest tests for `splitLineIntoIntralineSegments` in
    `apps/ui/src/api/diffViewModel.test.ts`, appended as a new `describe` and
    changing no existing test. Cover at least: no spans yields one unmarked
    segment; one span in the middle yields unmarked, marked, unmarked; a span at
    offset zero yields no leading empty segment; two overlapping spans mark
    their union once; two out-of-order spans mark both regions; a span past the
    end is dropped; a span running past the end is clamped; a zero-length and a
    negative-length span are dropped; and — as the property that catches every
    arithmetic slip at once — for each of those cases the concatenation of the
    segment texts equals the input `content`.

SPEC — `apps/ui/src/components/diff/DiffView.module.css`

S4. APPEND two rules and a WHY comment. The rules are, exactly:

        .diffLine.add .intraline { background: rgba(56,217,169,.32); border-radius: 2px; }
        .diffLine.del .intraline { background: rgba(247,103,7,.30); border-radius: 2px; }

    The comment above them carries three facts: DECISION F037 D9 rules this
    treatment, and the feature file's amendment A5 records it where a builder
    looks; the two hues are the binding CSS's OWN added and removed colours, at
    a higher alpha, so the emphasis introduces NO new hue into the sheet; and
    the deliberate-absence paragraph the file already carries — that Remedy does
    not style intraline spans — is SUPERSEDED by these two rules and by nothing
    else, so replace that paragraph's claim rather than leaving a comment that
    contradicts the rules beneath it. That replacement is the ONLY edit to
    existing bytes constraint 3 permits, and it touches no declaration.

SPEC — `apps/ui/src/components/diff/DiffView.tsx`, a NEW file

S5. A header comment: this draws the rows `diffViewModel.ts` builds, it derives
    nothing itself, and it is NOT MOUNTED yet — `component_spec.md:113-116` puts
    the entry point in `DetailPopover` behind `onOpenDiff(taskId)` and the
    feature file's Task slicing puts that integration in T003, so a reader
    finding no caller has found the plan rather than dead code. Name
    `tests/ui_contracts/test_diff_view_render.py` as what gates this file,
    since no test in this repository can render it.

S6. `export interface DiffViewProps { envelope: DiffEnvelope }` and
    `export function DiffView({ envelope }: DiffViewProps)`. The component takes
    an ALREADY-READ envelope: `readDiffEnvelope` is the door a payload comes
    through and the round that fetches will call it, so this component is never
    the second place a malformed payload is handled.

S7. Collapse state: `useState` initialised from `defaultCollapsedHunkIds(envelope)`
    with the lazy initialiser form, and a `useEffect` that RESETS it whenever
    `envelope` changes — a viewer switched from one task run to another must not
    keep the previous diff's collapse set, whose hunk ids mean nothing in the new
    one. A hunk head's click calls `setCollapsed((current) =>
    toggleHunkCollapse(current, hunkId))`, using the updater form so two clicks
    in one render cannot lose one.

S8. The rows. Walk `buildDiffRowModels(envelope, collapsed)` once and render each
    row by its `kind`, using each row's `key` as the React key and nothing else.
    A `file` row renders the path, the status, the added and deleted counts and
    the note when there is one. A `hunkHead` row is a `<button type="button">`
    carrying `styles.hunkHead`, because it is clickable and a div is not
    reachable by keyboard; it renders the header VERBATIM, carries
    `aria-expanded` reflecting the collapse state, and when collapsed also says
    how many lines it is hiding, taken from the row's `hiddenLineCount` and never
    recomputed. A `line` row renders `styles.diffLine` plus `styles.add` or
    `styles.del` for those two kinds and neither for `ctx`, then the two gutter
    cells with `styles.ln` — the old number, the new number, each blank when its
    value is null — and then the content.

S9. The content cell renders `splitLineIntoIntralineSegments(row.line)`: an
    unmarked segment as plain text, a marked one wrapped in a `<mark>` carrying
    `styles.intraline`. When the envelope's `truncated` is true the component
    renders one trailing notice saying the view is a prefix and why — that is
    the flag DECISION F037 D5, D6 and D7 all feed, and a viewer that silently
    shows part of a diff is the failure those three ceilings exist to avoid.

SPEC — `tests/ui_contracts/test_diff_view_render.py`, a NEW file

S10. A Python guard reading `DiffView.tsx` and `DiffView.module.css` AS TEXT,
    importing nothing from `apps/`, over COMMENT-STRIPPED source, with a module
    docstring saying why it is Python: nothing in this repository can render
    this component — `apps/ui/vitest.config.ts` collects `src/**/*.test.ts` in a
    NODE environment — so its wiring is gated by reading it, exactly as
    `tests/ui_contracts/test_decision_answer_wiring.py` gates the decision
    inbox. Assert, each with a message naming its authority: (a) the component
    DERIVES nothing — it names `buildDiffRowModels`, `defaultCollapsedHunkIds`,
    `toggleHunkCollapse` and `splitLineIntoIntralineSegments`, and contains no
    literal `200`, no `.length >` comparison against a threshold and no `sort(`,
    because a rule reimplemented here is a rule no gate can execute; (b) every
    class the component names is one the stylesheet really defines, computed by
    scanning `styles.<name>` in the component and the rule selectors in the CSS,
    so a typo cannot render an unstyled diff; (c) the hunk head is a `button`
    with `type="button"` and an `aria-expanded`, not a div; (d) the intraline
    mark exists — the component names `splitLineIntoIntralineSegments` and
    `styles.intraline`, and BOTH `.diffLine.add .intraline` and
    `.diffLine.del .intraline` are rules in the stylesheet — which is amendment
    A5's requirement expressed where it can fail; (e) the truncation notice
    exists: the component reads `envelope.truncated`.

Slice convention: each authored text sits between a line beginning `<<<SLICE `
and a line beginning `<<<END `, both carrying the slice's name. The marker lines
are NEVER written into any target file. The slices are PLANF037R16, GATER15,
SLIPR16, DECISION9 and AMENDA5.

<<<SLICE PLANF037R16
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
R16 finishes T002. `DiffView.tsx` draws the rows `diffViewModel.ts` builds —
file rows, hunk heads that collapse on click, line rows against the binding CSS
— and the last named piece of T002 is ruled rather than deferred: Acceptance
requires intraline emphasis, the three binding authorities say nothing about it,
and DECISION F037 D9 settles it as the binding CSS's own two hues at a higher
alpha, so no new hue and no new token enters the sheet. Amendment A5 records
that in the feature file. The component is deliberately not mounted yet.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R15 verdict and the type-gate slip | ordered | record first |
| C3 DECISION F037 D9 and amendment A5 | ordered | the ruling before what it governs |
| C4 the intraline segmentation and its tests | ordered | the last decidable rule |
| C5/C6 the stylesheet and the component | ordered | the drawing half |
| C7 the render guard | ordered | nothing here can render it |
| C8 the handback | ordered | |

## Next Steps
1. T003 mounts what T002 built: the entry point `component_spec.md` names —
   `onOpenDiff(taskId)` from `DetailPopover` — the fetch through `remedyApi.ts`
   calling `readDiffEnvelope`, and the file sidebar over
   `buildDiffFileSummaries`.
2. T003 then carries virtual scrolling beyond two thousand lines and the lazy
   language bundles, which are its last two named pieces.

## Risks
- Round 16 of a 25-round soft limit. T003 is three or four rounds of work, so
  the feature fits only if T003's rounds each close a named piece; the session
  that reaches round 21 with T003 unfinished owes a scope report instead.
- Nothing in this repository can execute a `.tsx` file. `tsc --noEmit` type-
  checks it through `tests/ui_server/test_dashboard_contract.py` and
  `tests/ui_contracts/` reads it as text, and those two are the whole of the
  gate; a rendering defect that both admit is invisible until the L3 tab exists.
<<<END PLANF037R16

<<<SLICE GATER15
Gate: F037 R15 — the round that lifted the blocked premise and landed the first client-side module of this feature. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all of the load-bearing ones itself at `68680786`. TRANSPORT IS PROVED FROM A VALUE THE REVIEWER HELD BEFORE DELEGATING: the block was written to the gitignored scratch `.remedy-wt/f037-r15-block.md` and measured there at sha256 `960fc3cf13b3e99888585bf800afd8f49cd95b10199e82d6f18ceb8695aa5868` over 38414 bytes and 453 lines, and the committed `.agent/authored/f037-r15.md` is byte-identical to that original, with the saved copy and `.agent/last_block.md` one git blob. EXTRACTION REPRODUCES: slices at 48, 1, 1, 1, 65, 1 and 1 content lines, CONTENT 118 against TOTAL 453, PROSE 335, both caps holding, and the plan byte-equal to PLANF037R15 at 48 lines with the trailing-newline control False. THE RECORD MOVED AS ORDERED: registrations 283 to 285 and all 285 distinct, `^Done: R-\d+ — ` 32 to 34, `^Gate: F\d+ R\d+ — ` 84 to 85, open set unmoved at 252, and the single repeating resolution id is `R-0721`, carried in from R14 rather than added here. `.agent/decisions.md` is at 174 headings with `F037 D8` exactly once. CONSTRAINT 3 IS PROVED BY A STRONGER READING THAN THE ONE ORDERED: the block asked for a comment-stripped comparison of `packages/orchestration/diff_parser.py`, and the reviewer additionally compared the two blobs' ABSTRACT SYNTAX TREES, which is immune to a bug in a comment stripper — `ast.dump` of the `0d750765` blob and of the C3 blob are equal while the raw blobs differ, so the repair really did change comment text and nothing else. BOTH STALE CLAIMS ARE GONE AND THEIR REPLACEMENTS ARE TRUE: the parser's DELIBERATE ABSENCE paragraph now names `DIFF_VIEW_MAX_ARTIFACT_BYTES` and DECISION F037 D7 as the input bound, and the CSS guard's docstring now gives the real reason it is written in Python — the node-environment vitest config reaches no stylesheet whatever the runner's availability. THE VIEW MODEL IS SOUND AND THE REVIEWER READ IT LINE BY LINE, because no mutation of it can be run here and a review is therefore the gate: `readDiffEnvelope` is total and is the single door a malformed payload stops at; the three line kinds it accepts are exactly the `ctx`, `add` and `del` that `diff_parser.py` defines, which the reviewer checked against the constants themselves rather than against the docstring, and both sides pin those literals in their own tests so neither can drift silently; row keys are prefixed per kind and derived from the server's hunk id, so a collapse renumbers nothing; and `toggleHunkCollapse` returns a new set, which is what makes it usable as React state at all. THE SUITES ARE GREEN AT REAL EXIT CODES RE-RUN BY THE REVIEWER: `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_contracts/ -q` exit 0 at `643 passed, 4 skipped`, and that range includes the node which RUNS `npx vitest run`, so the new vitest suite is executed and green rather than merely shipped. ALL THREE ORDERED RED-PROOFS OF THE PYTHON GUARD REPRODUCE, in a disposable worktree at `68680786` with `python3 -B`, each replaced string counted at exactly 1 and each file restored byte-identically: control exit 0 at `3 passed`; an added import, a renamed export and a transcribed threshold literal are each exit 1 at `1 failed, 2 passed`. THE REVIEWER ADDED A FOURTH THE BLOCK DID NOT ORDER — a JSX construct inserted into the module — and it is exit 1 on the same guard, so the `.tsx`-construct half of that assertion is not the dead clause it could have been. THE BLOCK'S OWN OMISSION IS RECORDED IN `.agent/prose_slips.md` RATHER THAN AS A FINDING, because nothing landed wrong: the block ordered no type gate and declared TypeScript untypecheckable here, and `tests/ui_server/test_dashboard_contract.py` runs the repository's local `tsc --noEmit` from pytest — the reviewer ran that node at `68680786` and it is REAL EXIT CODE 0, so the new module and its tests do type-check and the handback's contrary sentence is the reviewer's omission surfacing in the worker's honest report. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER15

<<<SLICE SLIPR16
- 2026-08-28 · F037 R15 · The R15 block declared that the round's TypeScript
  could not be type-checked here and ordered no gate for it, and the worker
  reported the same in its deviations after `tsc --noEmit` was refused from its
  shell. Both are wrong about the environment rather than about the code:
  `tests/ui_server/test_dashboard_contract.py` runs the repository's LOCAL
  `apps/ui/node_modules/.bin/tsc --noEmit` from pytest and skips only when that
  binary is absent, and the reviewer measured it at `68680786` as exit 0 with
  the new module on disk. This is the second time in two rounds that a tool was
  called unavailable after being refused from ONE caller, the first being the
  vitest runner that `R-0724` records: before writing that a tool cannot run
  here, grep `tests/` for a node that already runs it.
<<<END SLIPR16

<<<SLICE DECISION9
## DECISION F037 D9 — intraline emphasis is the binding CSS's own two hues at a higher alpha, and no new hue, token or type treatment enters the sheet

**Date:** 2026-08-28 · **Round:** F037 R16 · **Slice:** T002

**The question this settles.** The Goal & Done of
`docs/roadmap/features/T5_F037.md` requires that "intraline markers highlight
word-level changes", its Acceptance requires that "intraline spans match a
word-diff fixture", and its Design section lists "intraline emphasis on the
marked spans". Its binding CSS block defines no intraline rule, and the same
file's CANONICAL DESIGN REFERENCE banner forbids inventing a visual language.
Measured by the reviewer at `68680786`: `intraline` occurs ZERO times in
`docs/ui/design_reference/component_spec.md` and ZERO times in
`assets_spec.md`, the two design-reference files amendment A4 names as binding
for this surface, and neither of the binding CSS's two colours is a named token
in `apps/ui/src/styles/tokens.css`. So the requirement exists, the authority for
how to meet it does not, and F037 R9 through R15 each deferred it.

**The choice.** The marked span inside a changed line takes that line's OWN
background colour at roughly three times the alpha —
`rgba(56,217,169,.32)` inside an added line and `rgba(247,103,7,.30)` inside a
removed one, against the binding block's `.12` and `.10` for the whole row —
with a two-pixel corner radius so a span reads as one mark rather than as a
ragged run of characters.

**Why this is a derivation and not an invention.** The two hues are the binding
CSS's own, transcribed unchanged; only the alpha differs, and the alpha is what
makes an emphasis inside an already-tinted row legible at all. Nothing new is
named: no hue a designer did not choose, no token, and no change to
`apps/ui/src/styles/tokens.css`, which is the operator's design system and is
not this feature's to edit. A `var()` would in fact turn
`tests/ui_contracts/test_diff_surface_css.py` RED, because that guard asserts
every referenced token is defined in the shipped sheet — so the literal values
are what makes the existing guard satisfiable, rather than a shortcut around it.

**Why not weight, underline or a border.** Bold competes with the syntax
highlighting T003 lazily loads onto the same characters, and the two would be
indistinguishable in a monospace face. Underline collides with the underscore,
which is a character diffs are full of. A border adds a pixel of width per span
and would break the alignment of the two gutter columns the binding grid fixes
at `56px 56px`. A background is the only treatment that composes with a
per-token colour arriving later.

**On the assumption_log the banner requires.** The banner directs any visual
deviation to "the assumption_log". Measured at `68680786`, no file of that name
exists anywhere in this repository. The DECISION series in `.agent/decisions.md`
is what this repository actually uses for exactly this purpose — D3 and D4 of
this feature are both design rulings recorded there — and amendment A5 puts the
same ruling into the feature file, which is where a T003 builder looks first.
This decision claims nothing about what the banner should say; it records where
the reasoning went, and it went to both places.

**Alternatives rejected.** (1) Ship no intraline emphasis and mark Acceptance
short — rejected: it is a named line of Goal & Done, it has been deferred since
R9, and deferring it a seventh time is how a feature reaches its round limit
with a hole in the middle. (2) Ask the operator — forbidden by
`docs/agents/planner_reviewer_prompt.md` §2, which requires a loud, persisted,
reversible ruling instead of a question. (3) Add two tokens to `tokens.css` —
rejected as an edit to the design system by a feature that the banner binds TO
that system.

**How to reverse.** Delete the two `.intraline` rules from
`apps/ui/src/components/diff/DiffView.module.css`, restore the
deliberate-absence paragraph above them from git history at `68680786`, drop
`splitLineIntoIntralineSegments` and its `<mark>` from `DiffView.tsx`, and
delete amendment A5. The parser's `intraline` spans are unaffected: they are
contract data and predate this decision by fourteen rounds.
<<<END DECISION9

<<<SLICE AMENDA5
**A5 — intraline emphasis is this file's own added and removed colours at a
higher alpha (DECISION F037 D9).** The Goal & Done above requires intraline
markers to highlight word-level changes and the Design section lists "intraline
emphasis on the marked spans", while the binding CSS block defines no intraline
rule. Measured at `68680786`, the word `intraline` occurs ZERO times in both
design-reference files amendment A4 names as binding for this surface,
`component_spec.md` and `assets_spec.md`, so there is no treatment to follow
there. The treatment T002 ships, and which T003 keeps: the marked span inside a
changed line takes that line's own background hue at roughly three times the
alpha — `rgba(56,217,169,.32)` inside an added line, `rgba(247,103,7,.30)`
inside a removed one, against `.12` and `.10` for the whole row — with a
two-pixel corner radius.

This introduces NO new hue, NO new custom property and NO change to
`apps/ui/src/styles/tokens.css`: the two colours are this file's own binding CSS
values and only their alpha differs. The banner's prohibition on inventing a
visual language therefore stands unweakened, and the banner's assumption_log
requirement is met by DECISION F037 D9, which also records that no file of that
name exists in this repository.
<<<END AMENDA5

Done when — the gates below, every one executed with its REAL exit code
recorded, one line per gate in the handback. G1 through G8 run at the commits
named; none of them runs after C8, so the handback can quote every one of them.

G1 HYGIENE. Read `.agent/STOP` from disk before C0a and again before C8 and
report both readings. Report `git rev-parse HEAD` before C0a and state whether
it equals `68680786`, `git branch --show-current`, and the `git status
--porcelain` line count after each of C0a through C7.

G2 TRANSPORT, ONE DIGEST COMPARISON. Report sha256, byte count and line count of
the committed `.agent/authored/f037-r16.md` blob, and state whether they equal
the reviewer's scratch original at `.remedy-wt/f037-r16-block.md` — compare the
two files directly, disk to disk. Report `git rev-parse <C0b>:.agent/authored/f037-r16.md`
and `git rev-parse <C0b>:.agent/last_block.md` and whether they are the same
blob. State what the chain covers and what it does not.

G3 EXTRACTION AND CAPS, measured on the COMMITTED C0a blob and never on the
prose. For each slice report its content line count; report TOTAL lines of the
blob, CONTENT as their sum, PROSE as TOTAL minus CONTENT, and whether TOTAL is
at most 490 and PROSE at most 400.

G4 THE PLAN AT C1, AND THE STYLESHEET'S UNTOUCHED DECLARATIONS AT C5. Report
whether `.agent/plan.md` is byte-equal to the PLANF037R16 slice extracted from
the committed C0a blob, including the trailing newline, plus the negative
control against that slice minus its trailing newline; the count of lines
exactly `## Goal` and exactly `## Next Steps`; and `wc -l` with whether it is
strictly under 50. Then, for `apps/ui/src/components/diff/DiffView.module.css`,
report the five existing rule bodies — `.diffLine`, `.diffLine.add`,
`.diffLine.del`, `.diffLine .ln` and `.hunkHead` — extracted from the C5 blob
and from the `68680786` blob, and whether each pair is byte-identical, which is
constraint 3. Report the same comparison for the WHOLE file, which must be
False, so the first reading is shown not to be a comparison that cannot fail.

G5 THE RECORD AT C2 AND C3. For each of the four appends — GATER15 into
`.agent/live_review.md`, SLIPR16 into `.agent/prose_slips.md`, DECISION9 into
`.agent/decisions.md`, AMENDA5 into `docs/roadmap/features/T5_F037.md` — report
reader (a), `result == before + b"\n" + slice` re-read from disk; reader (b),
which COUNTS the blank-line-separated units of the slice and compares the LAST
that many units of the file against them IN ORDER, reporting the count it
measured; and a negative control for both readers that flips one byte inside the
FIRST appended paragraph. Report whether each file's pre-round blob is a byte
PREFIX of the result, reading that blob with `git show 68680786:<path>` into
memory and never over the tracked file. Then report, line-anchored over
`.agent/live_review.md` after C3 with the base figure beside each:
`^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`, `^Gate: F\d+ R\d+ — `, the
open-set size, and whether every REGISTERED id is distinct. Over
`.agent/decisions.md`, report `^## DECISION ` and the count of `F037 D9`. Over
`docs/roadmap/features/T5_F037.md`, report the count of lines beginning
`**A` — one per amendment.

G6 THE RED-PROOFS, WHICH ARE OF THE PYTHON GUARD AND OF NOTHING ELSE. FIRST
re-measure the reason, rather than citing DECISION F037 D8: in a disposable
worktree at the C7 tree, run `python3 -B -m pytest
tests/orchestration/test_test_runner.py -q -k vitest` with the worktree as the
working directory, and report its REAL exit code and whether the failure is a
STARTUP error naming `vitest` rather than a test result. Then, in that same
worktree with `__pycache__` purged and `python3 -B` for every run, red-prove
`tests/ui_contracts/test_diff_view_render.py`, the file restored between runs
and each restore verified byte-identical by sha256. Report the UNMUTATED
CONTROL's exit code and summary line first, then for each mutation the
occurrences of the replaced string BEFORE the edit, which must be 1, the REAL
exit code, the summary line and the failing node ids:
(a) in `DiffView.tsx`, replace the call to `splitLineIntoIntralineSegments` with
a plain render of the line's `content`. Expect RED.
(b) in `DiffView.tsx`, change the hunk head's `<button` to `<div`. Expect RED.
(c) in `DiffView.module.css`, delete the `.diffLine.del .intraline` rule.
Expect RED.
(d) in `DiffView.tsx`, rename one `styles.<name>` reference to a class the
stylesheet does not define. Expect RED.
The ordered property is the COLOUR: report the names and counts you measure
rather than any this block predicts.

G7 SUITES, TYPES, LINT AND CANARY AT C7, IN THE PRIMARY CHECKOUT. One pytest
process at a time; never two at once. Report the REAL exit code and the full
summary line of each: `python3 -m pytest tests/ui_server/test_dashboard_contract.py
-q -k typescript`, which is the node that runs this repository's LOCAL
`apps/ui/node_modules/.bin/tsc --noEmit` and therefore TYPE-CHECKS the new
`.tsx` — report whether it PASSED or SKIPPED, because it skips when the UI
toolchain is absent and a skip is not a type check; `python3 -m pytest
tests/orchestration/test_test_runner.py -q`, the node that RUNS vitest, whose
base figure at `68680786` is `52 passed`; `python3 -m pytest tests/ui_contracts/
-q`, whose base figure is `591 passed, 4 skipped`; `python3 -m pytest
tests/docs/ -q`, which this round owes because its change set includes
`docs/roadmap/**` and whose base figure at `68680786` is `295 passed`;
`python3 -m ruff check tests/ui_contracts/test_diff_view_render.py`;
and the canary `python3 -m pytest tests/cli/test_golden_path.py -q`, whose base
figure is `42 passed`.

G8 STRUCTURE, ARTIFACTS AND THE OPEN PR GATE AT C7. Report `git diff
--name-only 68680786..<C7>` and both residues against the change set above —
actual minus expected and expected minus actual, with `.agent/handoff.md`
expected to be the only member of the second because C8 writes it. Report `git
diff --stat` restricted to `packages/`, which must be EMPTY, to `tests/`, which
must hold `tests/ui_contracts/test_diff_view_render.py` alone, and to `apps/`.
Report each commit's insertion count from `git show --numstat` for C0a through
C7 and whether each is under 500, and check those figures cell by cell against
the `+/-` column of the handback's own `## Commits` table. Report the count of
lines matching `^<<<SLICE ` and `^<<<END ` in `.agent/plan.md`,
`.agent/live_review.md`, `docs/roadmap/features/T5_F037.md` and
`apps/ui/src/components/diff/DiffView.tsx`, and the same counts over the C0a
blob as the control that the counter is not blind. Report
`git ls-files .remedy-wt` line count. Run `gh pr list --state open --json
number,headRefName,baseRefName,isDraft` verbatim and report its exit code and
stdout.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It
carries the SESSION NUMBER of this feature — session 4 — the round, the range
`68680786..<C8>`, a per-commit changed-files table with the `+/-` column, one
line per gate G1 through G8 with its real result, the authored-text proofs, the
deviations, the item-status table covering C0a through C8 and G1 through G8, and
the next expected action. Derive any cap it must respect from AGENTS.md
yourself; this block states none. Then push the branch.
