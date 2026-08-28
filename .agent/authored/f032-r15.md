STEP T003c / F032 — ROUND R15 — the receipt chip becomes the evidence entry point

BASE. This block is authored against `a4a24663eb3d99bdc9507d1877ba9e623462d598`,
the tip of `feature/f032-evidence-triple` and the commit that handed back R14.
Every reading below was taken there by the reviewer unless another SHA is named.

FRAME CONVENTION. Every rule line in this block is exactly ten hyphens, and no
other line is a run of one repeated character. Nothing in the frame is
appliable: the appliable bytes are the slices, each proved against its own
target by its own gate.

----------

GOAL

Close T003 by ruling its deep link honestly. The evidence panel the feature
file sends the chips to does not exist and is not F032's to build, so F032
ships the ENTRY POINT that F023 will wire: the card takes an optional handler,
a receipt is a control only when one is supplied, and a ref's raw `target`
still reaches no markup. The ruling is recorded as DECISION F032 D8 and as
amendment A7 in the feature file.

----------

WHAT THE REVIEWER READ BEFORE ORDERING ANY OF THIS

Stated here rather than left implied, because every order below rests on one of
these readings and a worker must be able to check them.

(a) `docs/roadmap/features/T5_F032.md` lines 16-25 make "the card's evidence
    chips deep-link into the evidence panel" part of Goal & Done, and line 54
    names the destination: "evidence panel deep links (the zoom feature's L3
    tabs)".
(b) `docs/roadmap/features/T5_F023.md` line 70 is "**T003** EvidencePanel +
    lazy tabs + deep links + cluster", and `docs/roadmap/STATUS.md` line 89 is
    `- [ ] F023 — Semantic zoom L0–L3`. Unclaimed, unbuilt.
(c) `apps/ui/src/components/detail/DetailPopover.tsx` is the only detail
    surface in `apps/ui/src`, and `docs/ui/design_reference/component_spec.md`
    line 103 names it the "DetailPanel / EvidencePanel entry". It renders a
    TASK's apply/test/proof status and a prompt trace. It has no tab, no route
    and no prop that accepts a decision's evidence ref.
(d) The same file, lines 113-120, rules how this repository handles an entry
    point whose destination is not built: the DiffViewer entry is "a button in
    DetailPopover emitting `onOpenDiff(taskId)` (no-op today)", and the
    RuntimePreview entry is "visible only when `dashboard` exposes a runtime
    URL (not yet). Disabled otherwise with tooltip."
(e) `apps/ui/src/components/panels/DecisionInboxCard.tsx` at `a4a24663`: the
    props are an inline object type at the `export function` line carrying
    `decisions`, `tasks`, `jobId`, `serverToken` and `onSelectNode`; the file
    already renders a chip-shaped control conditionally, `{jumpNodeId ? (
    <button … /> ) : null}`, under the comment "Only a decision that can really
    jump gets the control, so the affordance never lies"; and the receipts strip
    R14 added renders one `<span className={styles.decisionEvidenceChip}>` per
    ref inside a `<div role="group">`.
(f) `apps/ui/src/components/panels/RightLivePanel.module.css` at `a4a24663`
    carries `.decisionJumpChip` with `display: inline-flex`, `align-items:
    center`, `padding: 2px 8px`, `border-radius: var(--remedy-radius-pill)`,
    `background: var(--remedy-bg-2)`, `border: 1px solid
    var(--remedy-line-strong)`, `font-size: 11px`, `font-weight: 500`, `color:
    var(--remedy-muted)`, `cursor: pointer`, plus a `:hover` rule setting
    `border-color: var(--remedy-blue-strong)` and `color: var(--remedy-ink)`
    and a `:focus-visible` rule setting `outline: 2px solid
    var(--remedy-blue-strong)` and `outline-offset: 2px`. That is the button
    chip pattern this card already has, and S5 mirrors it rather than inventing
    a second one.
(g) THE GUARDS THAT ALREADY BIND THIS FILE, all in
    `tests/ui_contracts/test_decision_answer_wiring.py` at `a4a24663`, which is
    the only file under `tests/` naming `DecisionInboxCard`. These are
    whole-file counts over the comment-stripped source and every one of them
    binds the lines this round adds: `code.count("ANSWER_PENDING_TITLE") == 0`,
    `code.count("setSendingKeys(") == 2`,
    `code.count("clarification.defaultAnswer") == 1` and
    `code.count(".target") == 1`. Beside them is a whole-file absence,
    `assert "hidden" not in code`. And
    `jsx_between_answer_button_and_live_paragraph` reads the LAST
    `aria-live="polite"` in the file, requires a `<p` to open it, and slices
    back to the nearest PRECEDING `</button>` — so a control added ABOVE the
    answer strip leaves that reader aimed where it already aims, while a
    control or an `aria-live` added BELOW the outcome paragraph would break it.
(h) `apps/ui/src/styles/tokens.css` defines every custom property S5 uses:
    `--remedy-radius-pill`, `--remedy-bg-2`, `--remedy-line`,
    `--remedy-line-strong`, `--remedy-muted`, `--remedy-blue-strong` and
    `--remedy-ink`. There is NO `--remedy-focus` property, which is why the
    focus ring below is `--remedy-blue-strong` exactly as `.decisionJumpChip`
    already writes it.
(i) `.agent/live_review.md` at `a4a24663`, read mechanically: 274 paragraphs
    matching `^- R-\d+ — `, 24 lines matching `^Done: R-\d+ — `, so the OPEN
    SET is 250 and the maximum id is `R-0713`. This round registers no finding
    and resolves none, so no id is minted. The open set was searched for the
    defect this round rules on — an unbuilt deep-link destination — and holds
    none.

----------

BUNDLE

C0a  save this block verbatim to `.agent/authored/f032-r15.md`
C0b  mirror the same bytes over `.agent/last_block.md`
C1   `.agent/plan.md`, slice PLANF032R15 applied whole
C2   `.agent/live_review.md`, slice LEDGER15 appended
C3   `.agent/decisions.md` slice DECISION8 appended, and
     `docs/roadmap/features/T5_F032.md` slice AMEND7 appended
C4   the component and its styles, items S2 to S6
C5   the contract guards, item S7
C6   the handback

CHANGE SET. Exactly these paths, and nothing else is created, edited or
deleted: `.agent/authored/f032-r15.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`,
`docs/roadmap/features/T5_F032.md`,
`apps/ui/src/components/panels/DecisionInboxCard.tsx`,
`apps/ui/src/components/panels/RightLivePanel.module.css`,
`tests/ui_contracts/test_decision_answer_wiring.py`, `.agent/handoff.md`.

----------

CONSTRAINTS

1.  A slice is applied BYTE FOR BYTE. It is never retyped from memory, never
    reflowed, never trimmed and never corrected — if a slice looks wrong, apply
    it as given and say so in the handback's deviations.
2.  SLICE CONVENTION. A slice begins at the line after `<<<SLICE NAME>>>` and
    ends at the line before `<<<END NAME>>>`. The slice's bytes are those lines
    including the newline that ends the last of them. Extract them
    PROGRAMMATICALLY from the committed C0a blob — `git show
    <C0a>:.agent/authored/f032-r15.md` — never by retyping from this prompt.
    PLANF032R15 REPLACES `.agent/plan.md` whole. LEDGER15, DECISION8 and AMEND7
    are APPENDS: the target's existing bytes, then exactly one newline, then
    the slice.
3.  Production code is DESCRIBED by the SPEC below, not sliced. Write it in the
    file's own idiom — its comment density, its naming, its WHY-above-the-
    definition habit — and match the neighbours it sits between.
4.  The commits happen in the order the Bundle lists. C1 is the first
    substantive commit, so `.agent/plan.md` is current before anything else is
    committed.
5.  Every commit passes the AGENTS.md self-review loop and the Commit Gate, and
    the tree is clean after each. Commit subjects carry no leading-slash token,
    no absolute path and no secret-like string.
6.  Push after C6: `git push -u origin feature/f032-evidence-triple`. Create no
    pull request and merge nothing.
7.  Read `.agent/STOP` from disk twice — once before C0a and once before C6 —
    and report the exact command output both times. If it EXISTS at either
    reading, stop, write the handback, and end.
8.  Every destructive check runs in a disposable `git worktree` under
    `.remedy-wt/`, never in the primary checkout, and the worktree is removed
    and pruned before the handback.
9.  Where a command's exit code is needed and this session's shell refuses
    `$?`, chain `&& echo <MARKER>` and report whether the marker printed. Never
    report an exit code that was not observed.
10. A numeral this block states about a gate's expected result is the
    reviewer's measurement at `a4a24663` and is named as such. Where a gate
    below says REPORT, report the number measured; never predict one.

----------

SPEC — what the code must do

S1. READ FIRST, BEFORE EDITING ANYTHING. Re-read the guards named in (g) above
    in `tests/ui_contracts/test_decision_answer_wiring.py`, and the whole of
    `TestTheCardShowsTheEvidenceTriple` that R14 added. Everything S2 to S6
    writes lands inside their reach. State in the handback that this was done
    and what each of those readings was.

S2. THE PROP. `DecisionInboxCard` gains ONE optional prop, `onOpenEvidence`, in
    the inline props object type at its `export function` line, declared after
    `onSelectNode`. Its type is
    `((evidenceRef: DecisionEvidenceRef) => void) | undefined`, written in
    whichever of the two equivalent spellings reads better beside its
    neighbours. `DecisionEvidenceRef` is imported as a TYPE from
    `../../api/decisionCard`, joining the existing
    `import type { DecisionCardModel }` line rather than adding a second import
    from the same module. The prop carries a WHY comment above it saying what
    it is for and that nothing supplies it yet.

S3. THE RECEIPT RENDERS AS A CONTROL ONLY WHEN A HANDLER EXISTS. Inside the
    existing `decision.evidenceRefs.map(...)` the body becomes a conditional on
    the PRESENCE of `onOpenEvidence` — the same shape as the `jumpNodeId ? … :
    null` control the file already carries, and for the same stated reason:
    the affordance never lies. When the handler is present the receipt is a
    `<button type="button">` with the SAME `className={styles.decisionEvidenceChip}`
    and an `onClick` that calls `onOpenEvidence(evidenceRef)` — the WHOLE ref,
    so the panel that finally arrives receives `kind` and `target` without this
    component ever reading either. When it is absent the receipt is exactly the
    `<span>` R14 shipped, unchanged. The `key` stays on the outer element in
    both arms and keeps its current expression.

S4. NO RAW TARGET, STILL. Nothing this round adds may write `.target`, name a
    ref's `target` in any rendered text, or put it in a `title`, an
    `aria-label` or any other attribute a browser shows. Passing the whole ref
    to a handler is not rendering it. §17 of
    `docs/ui/design_reference/ux_spec.md` is the rule and guard (g)'s
    `code.count(".target") == 1` is its mechanical form.

S5. THE STYLES. `RightLivePanel.module.css` gains the button chrome
    `.decisionEvidenceChip` needs once it can be a `<button>`, written so the
    span case is untouched. Mirror `.decisionJumpChip` as (f) records it: the
    chip resets the browser's button chrome to the values
    `.decisionEvidenceChip` already sets, takes `cursor: pointer`, and gains a
    `:hover` and a `:focus-visible` rule using `var(--remedy-blue-strong)` for
    both the hover border and the 2px focus outline at `outline-offset: 2px`.
    Every value resolves to a custom property `apps/ui/src/styles/tokens.css`
    already defines (finding R-0661); (h) lists the ones available. Change no
    existing rule, and leave all four `:empty` collapse rules exactly as they
    are.

S6. NOTHING ELSE CHANGES. `apps/ui/src/api/` is not touched.
    `RightLivePanel.tsx` is not touched — the prop is OPTIONAL precisely so no
    call site has to change. The send flow, the in-flight key set, the jump
    chip, the clarification form, the outcome paragraph and the two stakes
    paragraphs are untouched.

S7. THE GUARDS. `tests/ui_contracts/test_decision_answer_wiring.py` gains a new
    class of its own, beside `TestTheCardShowsTheEvidenceTriple` and reusing
    that file's existing readers rather than writing new ones. It pins, each in
    its own test: that the props type declares `onOpenEvidence`; that
    `DecisionEvidenceRef` is imported as a type from `../../api/decisionCard`;
    that the receipt's control arm calls `onOpenEvidence(` with the whole ref
    and never with a field of it; that the span arm still exists, so a card
    with no handler renders no control; that both arms carry the SAME
    `styles.decisionEvidenceChip`; and that `.decisionEvidenceChip` has a
    `:focus-visible` rule with a real outline behind it, read with the file's
    own `css_rule_body`. Every assertion carries a message saying what breaks
    if it fails, in the file's established voice.

S8. THE SPEC AND THE BUNDLE AGREE. S2 to S6 are C4; S7 is C5. Nothing in this
    SPEC is performed by a commit the Bundle does not list.

----------

SLICES

<<<SLICE PLANF032R15>>>
# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D8.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R15 closes T003 and rules its deep link. The evidence panel the feature file
sends the chips to is `docs/roadmap/features/T5_F023.md` T003, and F023 is
unclaimed in `docs/roadmap/STATUS.md`, so F032 ships the ENTRY POINT rather
than a link to nothing: the card takes an optional `onOpenEvidence` handler, a
receipt renders as a control only when one is supplied and as the span R14
shipped when none is, and no ref's `target` reaches the markup either way.
DECISION F032 D8 and amendment A7 record the ruling and how to reverse it.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R14 verdict | ordered | the record is touched first |
| C3 the D8 ruling and the A7 amendment | ordered | |
| C4 the component and its styles | ordered | S2 to S6, one commit |
| C5 the contract guards | ordered | S7 |
| C6 the handback | ordered | |

## Next Steps
1. The integration gate — the full suite, per docs/agents/integration_gate.md.
2. The closure sequence: evidence job, a fresh review zip, the STATUS line and
   the pull request, per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The card's guards read the `.tsx` as TEXT, and the whole-file counts they
  carry bind every line this round adds as tightly as the markup they were
  written for.
- The handler's arm is unreached today, because nothing supplies the prop. It
  is typechecked and text-pinned, never behaviour-tested, and F023 is the
  feature that first runs it.
<<<END PLANF032R15>>>

<<<SLICE LEDGER15>>>
Gate: F032 R14 — the F032 T003b CARD-RENDER entry, and the first F032 round to touch `.tsx` and CSS. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all eight itself at `a4a24663`. TRANSPORT: sha256 `ab8e552d5733df15bb7fb17f4d2183ef077803649b81180459dbdc26521c23de` over 25057 bytes and 306 lines is carried by the reviewer's scratch original `.remedy-wt/f032-r14.md`, by the committed `.agent/authored/f032-r14.md` blob and by the committed `.agent/last_block.md` blob, the last two being the SAME git blob `16367574f3dcd28d5bca0f6f87bb7732871e1d25`. THAT CHAIN COVERS THE SCRATCH ORIGINAL, THE SAVED COPY AND THE MIRROR AND NOTHING ELSE: under docs/agents/self_drive_protocol.md there is no paste relay, so it says nothing about the bytes of any prompt, and no claim about a prompt is made here. WHAT THE REVIEWER MEASURED ITSELF, every number below being its own run and not the worker's: `npx tsc --noEmit` from `apps/ui` printed only the chained marker, so exit 0 with no output; `python3 -m pytest tests/ui_contracts/ -q` exit 0 at `574 passed, 4 skipped`, against the `566 passed, 4 skipped` the reviewer had taken at the base, so passed grew by exactly the eight new guards and skipped did not move; the golden-path canary exit 0 at `42 passed`; the PLAN at `83df7d73` byte-equal to slice `PLANF032R14` extracted from the committed C0a blob `True` with the trailing-newline negative control `False`, 46 lines, `^## Goal$` and `^## Next Steps$` one each; the LEDGER at `d29f0cbe` byte-identical to base plus one newline plus the slice `True`, with the base blob a byte PREFIX `True`; and the block's own caps, 306 total lines against 47 content lines in two regions, so 259 prose lines, under 400 and under 490. THE OPEN SET IS UNMOVED AND WAS RECOMPUTED RATHER THAN CARRIED: 274 paragraphs matching `^- R-\d+ — ` minus 24 lines matching `^Done: R-\d+ — ` gives 250 open, maximum id `R-0713`, ids added to the registered set `[]` and to the resolved set `[]`, while `^Gate: F\d+ R\d+ — ` went 65 to 66 adding exactly the `F032 R13` key. THE REVIEWER RAN TWO MUTATIONS OF ITS OWN CHOOSING, neither ordered by the block, in a disposable worktree at `a4a24663` with the exact byte string counted 1 in the named file before each was applied: deleting the render of `{decision.evidenceNote}` from `apps/ui/src/components/panels/DecisionInboxCard.tsx` gave exit 1 at `1 failed, 48 passed` naming `test_the_card_renders_the_note_that_says_why_there_are_none`; moving the two stakes paragraphs ABOVE the outcome paragraph in the same file gave exit 1 at `1 failed, 48 passed` naming `test_the_answer_stakes_sit_after_the_live_region_and_add_no_operator`, which is the guard whose reader is subtlest and which no ordered mutation had exercised; and the controls before the first mutation and after both restorations were a real exit 0 at `49 passed` with the worktree's `git status --porcelain` at 0 lines, after which it was removed and `git worktree list` returned to one line. SO THE ROUND'S OWN GUARDS BITE ON MORE THAN THE THREE MUTATIONS IT REPORTED. THE DESIGN REFERENCE WAS REALLY APPLIED AND THE REVIEWER CHECKED THE CLAIM: every custom property the new rules use — `--remedy-radius-pill`, `--remedy-bg-2`, `--remedy-line`, `--remedy-line-strong`, `--remedy-muted` and `--remedy-orange-400` — resolves in `apps/ui/src/styles/tokens.css`, the downside carries a left rule as well as the warn tint so §14's colour-alone prohibition is met, and §17 is met mechanically rather than by assertion, the only `.target` in the comment-stripped component being `const typed = event.target.value;`. THE TWO DECLARED DEVIATIONS ARE BOTH ACCEPTED. The FOURTH `:empty` rule, on `.decisionEvidence` itself, is right: `.decisionRow` is a column flex box with an 8px gap, so an empty strip would claim a band on every card carrying no receipts, and the rule uses the same out-of-flow mechanism the ordered three use. The `role="group"` carrying `DECISION_EVIDENCE_LABEL` is right for the reason finding R-0682 already records — an `aria-label` on a `generic` role is computed and dropped — and the label names what the chips are without naming a status, a schema key or a count. NOTHING ELSE MOVED: `git diff --name-only f28640ef..4b6a357a` is exactly the change set less `.agent/handoff.md` with both residues EMPTY, `packages/` and `docs/` EMPTY across the whole range, `apps/ui/src/api/` EMPTY, per-commit insertions 306, 226, 21, 2, 133, 125 and 212 each single-parent and each under 500 and each agreeing cell by cell with the handback's own `## Commits` column, `^<<<SLICE ` and `^<<<END ` zero in every written file against a control of two each over the C0a blob, `git ls-files .remedy-wt` 0 lines, `git worktree list` one line, `git branch --list "tmp/*"` empty, the remote tip equal to the local tip and the Open PR Gate `[]`. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER15>>>

<<<SLICE DECISION8>>>
## DECISION F032 D8 (2026-08-28) — the receipt chip is an ENTRY POINT F023 wires, not a link F032 invents

CONTEXT, measured at `a4a24663`. `docs/roadmap/features/T5_F032.md` makes "the
card's evidence chips deep-link into the evidence panel" part of Goal & Done,
and its Design section names the destination outright: "evidence panel deep
links (the zoom feature's L3 tabs)". That panel is
`docs/roadmap/features/T5_F023.md` T003 — "EvidencePanel + lazy tabs + deep
links + cluster" — and `docs/roadmap/STATUS.md` carries F023 as `[ ]`,
unclaimed. Nothing in `apps/ui/src` renders one. The only detail surface that
exists is `apps/ui/src/components/detail/DetailPopover.tsx`, which
`docs/ui/design_reference/component_spec.md` names the "DetailPanel /
EvidencePanel entry" and which shows a TASK's apply, test and proof status and
its prompt trace; it has no tab, no route and no prop that accepts a decision's
evidence ref. F032 depends on F031 alone. This is the same shape as amendment
A2, where the resolver and its staleness badges were found to be F066's unbuilt
spec, and it is settled the same way.

CHOSEN. `DecisionInboxCard` takes an OPTIONAL `onOpenEvidence` handler. A
receipt renders as a `<button>` calling it with the whole
`DecisionEvidenceRef` when a handler is supplied, and as the `<span>` R14
shipped when none is. Nothing supplies one in this release, so every card
renders spans today; F023 supplies the handler and the panel together, and the
wiring is one prop at one call site. A ref's `target` continues to reach no
markup, no text and no attribute a browser shows — it travels to the handler as
a field of the ref, which is not rendering.

WHY. Three reasons, in the order they bind. FIRST, the affordance never lies.
The card already states that rule at its jump chip — only a decision that can
really jump gets the control — and a chip that looks pressable while no panel
exists to receive the press is exactly the dishonest affordance finding R-0693
registered against the answer buttons. SECOND, this is the pattern the
canonical design reference itself prescribes for an entry point whose
destination is not built: `component_spec.md` gives the DiffViewer "a button in
DetailPopover emitting `onOpenDiff(taskId)` (no-op today)" and the
RuntimePreview a control "visible only when `dashboard` exposes a runtime URL
(not yet)". Shipping the entry point and letting the destination arrive later
is the house style, not an invention of this round. THIRD, it is the smallest
thing that makes F023 cheap. The alternative that ships nothing leaves F023 to
discover the receipts, design the payload and edit this component; the prop and
its call fix the contract now, while the reasoning that produced it is on this
page.

REJECTED, and why. (1) A `<button disabled>`
carrying an honest tooltip — "the evidence panel arrives with a later feature" —
which `ux_spec.md` §14 permits for a disabled control and which the ChatInput
already does for steering. Rejected because a disabled control is drawn at 45%
opacity, and the thing dimmed here would be the RECEIPT ITSELF, whose label is
the evidence and is fully present; F032 would ship the receipts it exists to
show and immediately style them as unavailable. A disabled button is also
removed from the tab order, so the honest tooltip is unreachable by exactly the
reader who most needs it. (2) Rendering nothing beyond R14's span and deferring
the entire item to F023. Rejected because the deep link is Goal & Done material
for F032 and handing the whole of it to an unclaimed feature would leave this
feature's own acceptance unmet with nothing on disk to show where it went.

REVERSE by deleting the `onOpenEvidence` prop from the props type of
`apps/ui/src/components/panels/DecisionInboxCard.tsx`, deleting its type-only
`DecisionEvidenceRef` import, collapsing the receipt's two arms back to the
single `<span>`, deleting the `.decisionEvidenceChip` button, hover and
focus-visible rules from
`apps/ui/src/components/panels/RightLivePanel.module.css`, and deleting the
guard class the F032 R15 block's item S7 adds to
`tests/ui_contracts/test_decision_answer_wiring.py`. No other change is
required, and amendment A7 of `docs/roadmap/features/T5_F032.md` is the text to
strike with it.
<<<END DECISION8>>>

<<<SLICE AMEND7>>>
**A7 — the chip's deep link is an ENTRY POINT, and the panel it opens belongs to
F023 (DECISION F032 D8).** "The card's evidence chips deep-link into the
evidence panel" names a destination this repository has not built: the panel is
`docs/roadmap/features/T5_F023.md` T003, F023 is unclaimed in
`docs/roadmap/STATUS.md`, and the only detail surface in `apps/ui/src` is the
per-task `DetailPopover`, which carries no tab and no prop for a decision's
evidence ref. F032 depends on F031 and does not own F023's panel. So F032 ships
the ENTRY POINT and F023 wires it: `DecisionInboxCard` takes an optional
`onOpenEvidence` handler, a receipt renders as a control when one is supplied
and as a plain chip when none is, and a ref's `target` reaches no markup either
way. This is amendment A2's shape a second time — there the resolver and its
staleness badges were F066's, here the panel is F023's — and it is settled the
same way, by shipping the honest half and naming the feature that completes it.
The Goal & Done bullet above is read accordingly: DONE for F032 means the entry
point exists, is typechecked and is pinned by a guard; the navigation itself is
F023 acceptance material.
<<<END AMEND7>>>

----------

DONE WHEN — the gates, in this order

Every gate is EXECUTED and its real output recorded. "Green" as a word is a
finding. Each gate runs at a commit strictly earlier than C6, so the handback
can quote all of them; C6's own numbers are not gated and are not owed.

G1 HYGIENE, BASE, SENTINEL. `git rev-parse HEAD` before C0a — REPORT it and
   confirm it equals the base this block names. `git rev-parse --abbrev-ref
   HEAD` is `feature/f032-evidence-triple`. `git status --porcelain | wc -l` is
   `0` after each of C0a, C0b, C1, C2, C3, C4 and C5. `ls -la .agent/STOP`
   before C0a and again before C6 — report the exact output of both.

G2 TRANSPORT. One digest comparison, disk to disk. Report `sha256sum` over the
   reviewer's gitignored scratch original `.remedy-wt/f032-r15.md`, over
   `.agent/authored/f032-r15.md` at C0a and over `.agent/last_block.md` at C0b —
   all three equal — plus the git blob id of the two committed paths, which must
   be one blob. That chain covers the original, the copy and the mirror, and
   makes no claim about any prompt's bytes.

G3 EXTRACTION AND CAPS, measured on the COMMITTED C0a blob. Report the content
   line count of EACH slice region found and how many regions there were, the
   block's TOTAL line count, and PROSE as TOTAL minus the content total. PROSE
   must be under 400 and TOTAL under 490.

G4 THE PLAN, at C1. `.agent/plan.md` is byte-equal to slice PLANF032R15
   extracted from the committed C0a blob — report `True`. NEGATIVE CONTROL: the
   same comparison with the slice's trailing newline removed — report `False`.
   Report `wc -l`, which must be under 50, and the counts of `^## Goal$` and
   `^## Next Steps$`, one each.

G5 THE THREE APPENDS, at C2 and C3, each read with `git show <base-sha>:<path>`
   so no tracked file is ever overwritten to get a baseline. For EACH of
   `.agent/live_review.md`, `.agent/decisions.md` and
   `docs/roadmap/features/T5_F032.md`: READER (a), byte identity — the
   post-commit bytes equal the pre-commit bytes plus one newline plus the
   slice — report `True`, and report the arithmetic as three numbers summing to
   the result, and that the pre-commit blob is a byte PREFIX. READER (b),
   structural — count N, the number of blank-line-separated paragraphs in the
   slice, and compare the LAST N blank-line units of the post-commit file
   against the slice's N paragraphs IN ORDER; report N and the result.
   NEGATIVE CONTROL for each: flip one byte IN MEMORY inside the FIRST appended
   paragraph and report that BOTH readers reject it. Then report, before and
   after C2: the counts of `^Gate: F\d+ R\d+ — `, `^- R-\d+ — `,
   `^Done: R-\d+ — ` and `^Landed: R-`, the size of the open set and the
   maximum id, the list of gate keys ADDED and the list of ids ADDED to the
   registered and resolved sets. The reviewer measured the open set at 250 and
   the maximum at `R-0713` at `a4a24663`; this round registers and resolves
   nothing, so both must be unmoved. Report `^## DECISION F032 D\d+ ` before
   and after C3, and the list of DECISION keys added.

G6 TYPECHECK AND THE TEXT READINGS, at C4. From `apps/ui`, `npx tsc --noEmit`
   chained with a marker — report whether the marker printed and whether any
   other output appeared; it must be exit 0 with no output. Then over
   `apps/ui/src/components/panels/DecisionInboxCard.tsx` at C4, with comments
   stripped by the module's own `strip_ts_comments`, report each of these
   numbers and the pass/fail against the value the guards require: the count of
   `hidden` (0), of `ANSWER_PENDING_TITLE` (0), of `setSendingKeys(` (2), of
   `clarification.defaultAnswer` (1), of `.target` (1) together with the full
   text of the line carrying it, and the count of `onOpenEvidence` (report the
   number measured). Report also that the LAST `aria-live="polite"` in the file
   is opened by a `<p` tag, and the exact string
   `jsx_between_answer_button_and_live_paragraph` returns, with its counts of
   `?`, `&&` and `||`.

G7 THE GUARDS, GREEN THEN RED, at C5. `python3 -m pytest
   tests/ui_contracts/test_decision_answer_wiring.py -q` — report exit code and
   the pass line. `python3 -m pytest tests/ui_contracts/ -q` — report exit code
   and the pass line; the reviewer measured `574 passed, 4 skipped` at
   `a4a24663`, so report the growth rather than predicting it. Then, in a
   disposable worktree created with `git worktree add --detach
   .remedy-wt/f032-r15-mut <C5>`, one mutation per run, each exact byte string
   counted in its named FILE before it is applied and that count reported:
   (a) delete the `onClick` that calls `onOpenEvidence` from
   `apps/ui/src/components/panels/DecisionInboxCard.tsx`; (b) delete the
   `onOpenEvidence` entry from the props type in the same file; (c) delete the
   `:focus-visible` rule the round adds for `.decisionEvidenceChip` from
   `apps/ui/src/components/panels/RightLivePanel.module.css`. For each report
   the exit code, the pass/fail line and every `^FAILED` name. Run an UNMUTATED
   CONTROL before the first mutation and again after all restorations, and
   report both exit codes and the worktree's `git status --porcelain` line
   count after each restoration. Purge `__pycache__` and pass `python3 -B`.
   Remove the worktree, prune, and report `git worktree list`.

G8 STRUCTURE, CANARY, DOCS AND THE PR GATE, at C5. `python3 -m pytest
   tests/cli/test_golden_path.py -q` — exit code and pass line. This round's
   change set includes `docs/roadmap/**`, so also `python3 -m pytest
   tests/docs/ -q` — exit code and pass line. `git diff --name-only
   a4a24663..<C5>` is exactly the Change set above less `.agent/handoff.md` —
   report BOTH residues. `git diff --stat a4a24663..<C5> -- packages/` and the
   same for `-- apps/ui/src/api/` are EMPTY. Report the insertion count of
   every commit from C0a through C5, each single-parent and each under 500, and
   compare them cell by cell against the `+/-` column the handback's
   `## Commits` table carries — the two readings must agree. Report
   `^<<<SLICE ` and `^<<<END ` counts in `.agent/plan.md`,
   `.agent/live_review.md`, `.agent/decisions.md`,
   `docs/roadmap/features/T5_F032.md`, `DecisionInboxCard.tsx`,
   `RightLivePanel.module.css` and
   `tests/ui_contracts/test_decision_answer_wiring.py`, against a CONTROL count
   over the committed C0a blob. Report `git ls-files .remedy-wt`, `git worktree
   list`, `git branch --list "tmp/*"`, and `gh pr list --state open --json
   number,headRefName,baseRefName,isDraft`.

----------

HANDBACK

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has no
length cap; it is valid when its mandated sections are present. It carries:
the feature and round, the SESSION NUMBER — this is SESSION 4 of F032, whose
rounds so far are R1 to R5 in session 1, R6 to R9 in session 2, R10 to R14 in
session 3, and R15 opening this one — the branch, the base and every commit
SHA, a per-commit changed-files table with the `+/-` column, ONE LINE PER GATE
G1 to G8 carrying its real readings, the item-status table covering C0a to C6
and S1 to S8 with every item present exactly once, the open-findings count, the
deviations and assumptions, and the next expected action. State plainly that no
pull request was created and nothing was merged.
