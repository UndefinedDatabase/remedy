STEP R14 / F032 — T003b: THE CARD RENDERS ITS RECEIPTS
Goal:        SHOW THE OPERATOR WHAT THE PRODUCERS WROTE. R13 put the triple on
             the card model — `evidenceRefs`, `evidenceNote`, and each answer's
             own `expectedOutcome` and `downside` — and nothing renders any of
             it. This round projects all four in
             `apps/ui/src/components/panels/DecisionInboxCard.tsx`, gives them
             rules in that panel's stylesheet, and adds the contract guards
             that pin the markup. Consent reads before it clicks: the outcome
             and the downside sit under the answer they belong to, which is why
             R13 attached them to the ANSWER rather than to the card. THIS IS
             THE ROUND THE CANONICAL DESIGN REFERENCE BINDS, and §17 of
             `docs/ui/design_reference/ux_spec.md` is the clause that decides
             its markup. SESSION 3 CONTINUES; YOU CREATE NO PULL REQUEST AND
             MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the R13 verdict · C3 the component and its styles · C4
             the contract guards · C5 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r14.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `apps/ui/src/components/panels/DecisionInboxCard.tsx`,
             `apps/ui/src/components/panels/RightLivePanel.module.css`,
             `tests/ui_contracts/test_decision_answer_wiring.py`,
             `.agent/handoff.md`. NOTHING under `packages/`, and
             `apps/ui/src/api/` is NOT touched — the model R13 shipped is used
             exactly as it stands. Nothing under `docs/`, so no docs-round gate
             is owed.

Constraints.
 1. YOU DO NOT EDIT ANY SLICE. A `<<<SLICE NAME>>>` line and its `<<<END NAME>>>`
    line delimit text you apply byte for byte. If a slice looks wrong, apply it
    anyway and say so in the handback's deviations. The marker lines are NEVER
    written into any file.
 2. SLICE CONVENTION. A slice's content is every line strictly between its two
    marker lines. When the slice replaces a whole file, the file's bytes are
    those lines joined with `\n` plus ONE trailing `\n`. When the slice is
    appended, the file's new bytes are its old bytes plus ONE `\n` plus that
    joined text plus ONE trailing `\n`, applied only if the old bytes already
    end in a newline — `.agent/live_review.md` does; G5 proves the arithmetic.
 3. THE AUTHORED UNITS OF THIS BLOCK are the whole block itself and the slices
    PLANF032R14 and LEDGER14. This paragraph gives no count of them; G3 reports
    the number the extraction measured.
 4. C0a IS A COPY, NOT A RETYPE. `.remedy-wt/f032-r14.md` holds this block.
    Copy it to `.agent/authored/f032-r14.md` byte-preserving; C0b writes the
    SAME bytes to `.agent/last_block.md`.
 5. PRODUCTION CODE IS DESCRIBED, NOT SLICED. Items S1 through S7 are a spec.
    You write the TSX, the CSS and the Python yourself, matching the style and
    the comment density of the files you are editing.
 6. ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, in that order and with no
    commit between them. C2 is the only commit touching `.agent/live_review.md`.
    C3 CARRIES THE COMPONENT AND ITS STYLESHEET TOGETHER: a class the component
    names but the stylesheet lacks is an unstyled node, and an existing guard
    already reads the two against each other.
 7. RE-READ `.agent/STOP` FROM DISK TWICE: once before C0a and once before C5.
 8. THE ROUND BASE IS `f28640ef`. Every numeral this block states about the base
    was measured there.
 9. RUN THE SUITES SERIALLY. Never two test processes at once.
10. THE HANDBACK IS NOT AN APPEND-ONLY RECORD. It is rewritten in full every
    round, so a numeral you find false in your own committed handback is
    corrected by a deviation line in the NEXT round's handback and NEVER by a
    commit of its own. This is the rule the R12 gate entry recorded as binding
    on the next block that orders a handback, and this is that block.

Spec — T003b, the component.
 S1. READ FIRST, AND THESE GUARDS ARE THE SHAPE OF THE ROUND.
     `tests/ui_contracts/test_decision_answer_wiring.py` at `f28640ef` reads
     `DecisionInboxCard.tsx` as TEXT, with comments stripped first, and four of
     its assertions bind everything you write. (a) `assert "hidden" not in code`
     — WHOLE FILE, comments already removed, so no class name, no attribute and
     no identifier you add may contain that substring. (b)
     `jsx_between_answer_button_and_live_paragraph` takes the LAST
     `aria-live="polite"` in the file and asserts the tag opening it is `<p`, so
     you may NOT add an `aria-live` anywhere after the existing outcome
     paragraph; and the source between the last `</button>` and that `<p` must
     contain no `?`, no `&&` and no `||`. (c) the card may not contain
     `decision.type ===`, `=== decision.type`, `decision.status` or `switch (`.
     (d) `code.count("setSendingKeys(") == 2` and
     `code.count("clarification.defaultAnswer") == 1`, so leave both alone.
     The stylesheet is `RightLivePanel.module.css`; it already collapses an
     empty live region OUT OF FLOW with `.decisionOutcomeQuiet { position:
     absolute; }` rather than with `display: none`, `visibility: hidden` or the
     `hidden` attribute, because each of those takes the node out of the
     accessibility tree (finding R-0686).
 S2. THE RECEIPTS RIDE THE CARD, ABOVE THE ANSWER STRIP. In the article body,
     AFTER the existing `styles.decisionChips` row and BEFORE the clarifications
     block, render the card's receipts: one element per entry of
     `decision.evidenceRefs`, each showing that ref's `label` AND NOTHING ELSE,
     followed by `decision.evidenceNote`. NEVER RENDER A REF'S `target`, in text,
     in a `title` or in any other attribute a browser shows: §17 of
     `docs/ui/design_reference/ux_spec.md` forbids the default UI to show raw
     ids and a target is frequently exactly one, which is why R13's model
     scrubbed the label and left the target for the deep link T003c will add.
     Both regions are rendered UNCONDITIONALLY — `evidenceRefs` is an empty
     array and `evidenceNote` an empty string when a card has no receipts, so a
     `.map` over the first yields no nodes and the second yields no text, and
     NO conditional operator is needed anywhere. Give the note its own element
     so the stylesheet can collapse it when empty.
 S3. THE OUTCOME SITS UNDER THE ANSWER IT BELONGS TO. Inside the existing
     `decision.answers.map`, render `answer.expectedOutcome` and
     `answer.downside` as two elements, AFTER the existing outcome paragraph in
     source order — that placement is not cosmetic, it is what keeps the LAST
     `aria-live` in the file the outcome paragraph's, per S1 (b). Render both
     UNCONDITIONALLY and with NO conditional operator: R13 guarantees each is a
     string and empty rather than absent, which is precisely what makes an
     unguarded render correct here. Do NOT put an `aria-live` on either.
 S4. THE STYLES GO IN `RightLivePanel.module.css`, in the region that already
     styles the decision card, and they follow that file's own conventions: the
     chip scale `.decisionChip` sets, the panel's `--remedy-*` tokens and no
     literal colour. AN EMPTY RECEIPT NOTE, AN EMPTY EXPECTED OUTCOME AND AN
     EMPTY DOWNSIDE ARE COLLAPSED WITH `:empty` SELECTORS THAT TAKE THE NODE OUT
     OF FLOW THE WAY `.decisionOutcomeQuiet` ALREADY DOES — never `display:
     none`, never `visibility: hidden`, for the reason S1 gives. Carry that
     reason in a comment, as the neighbouring rules already do.
 S5. THE COPY RULES BIND THE STATIC TEXT TOO. Any label you introduce is a
     module-level constant beside the file's existing ones rather than an inline
     literal, and it says what the thing IS in the operator's words. Do not name
     a status, a schema key or a field name in anything rendered.
 S6. THE NEW GUARDS GO IN `tests/ui_contracts/test_decision_answer_wiring.py`,
     in a class of their own, and they pin what this round adds: that the card
     renders `answer.expectedOutcome` and `answer.downside`; that it renders
     `decision.evidenceNote` and maps `decision.evidenceRefs`; that the stripped
     source carries the substring `.target` EXACTLY ONCE and that the surviving
     occurrence is the clarification input's `event.target.value`, which is how
     a ref's target reaching the markup is caught without depending on the name
     the map's variable happens to have; that every CSS class the new
     markup names really exists in `RightLivePanel.module.css`, the way the
     existing tone-to-class guard already checks its three; that the new
     collapse rules use neither `display: none` nor `visibility: hidden` nor the
     `hidden` attribute; and that the region added by S3 introduces no
     conditional operator between the answer button and the live paragraph — for
     that last one, REUSE the module's existing
     `jsx_between_answer_button_and_live_paragraph` helper rather than writing a
     second reader of the same shape. Read the existing tests first and follow
     their method and their message style.
 S7. NOTHING ELSE CHANGES. `apps/ui/src/api/` is not touched. The send flow, the
     in-flight set, the jump chip, the clarification form and the outcome
     paragraph keep their current behaviour, their current markup and their
     current classes.

Done when. Report each gate as its own line in the handback, with the real
command, its exit code and the real output you saw. G1 through G8 are ordered at
commits STRICTLY EARLIER than C5, which writes the handback; G1 therefore stops
at C4.
 G1. HYGIENE, BASE AND THE SENTINEL. Report `git rev-parse HEAD` before C0a and
     confirm it is the base of constraint 8; report the branch is
     `feature/f032-evidence-triple`; report the `git status --porcelain` line
     count after EACH of C0a through C4, each 0; report whether `.agent/STOP`
     exists at the two readings constraint 7 orders.
 G2. TRANSPORT. Report the sha256, byte count and line count of
     `.remedy-wt/f032-r14.md`, of the committed `.agent/authored/f032-r14.md`
     blob and of the committed `.agent/last_block.md` blob, and whether all
     three are EQUAL. Report the git blob hash of the C0a and C0b paths and
     whether they are the SAME blob. State plainly that this proves the
     reviewer's scratch original, the saved copy and the mirror agree, and says
     NOTHING about the bytes of any prompt.
 G3. EXTRACTION AND CAPS. From the COMMITTED C0a blob, extract every region
     between a `^<<<SLICE ` line and its `^<<<END ` line. Report the NAME and
     content-line count of each, the number of regions, the CONTENT total, the
     TOTAL line count and PROSE as TOTAL minus CONTENT. Report whether PROSE is
     under 400 and TOTAL under 490. Report the numbers YOU measured.
 G4. THE PLAN. Report whether `.agent/plan.md` at C1 is byte-equal to slice
     PLANF032R14 under the convention of constraint 2, and the same comparison
     with the trailing newline removed as a NEGATIVE CONTROL, which must be
     FALSE. Report `wc -l` and that it is under 50, and the counts of
     `^## Goal$` and `^## Next Steps$`, each 1.
 G5. THE LEDGER APPEND. Read the pre-commit blob with `git show
     f28640ef:.agent/live_review.md`, never by writing over the tracked file.
     Prove `.agent/live_review.md` at C2 equals that blob plus ONE newline plus
     the LEDGER14 slice, byte for byte; report the arithmetic as three numbers
     summing to the result and that the pre-commit blob is a byte PREFIX. Then
     run a SECOND, INDEPENDENT structural reader: split the whole file on blank
     lines, let N be the number of paragraphs in the LEDGER14 slice as YOUR
     script counts them, and compare the LAST N units against those N paragraphs
     IN ORDER. As a NEGATIVE CONTROL flip ONE byte inside the FIRST appended
     paragraph, in memory only, and report that BOTH readers reject it. The
     reviewer measured the base at `f28640ef` as 1091935 bytes over 430
     blank-line units. Then report, before and after C2, the counts of
     `^Gate: F\d+ R\d+ — `, `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-` and
     `^Gate: R\d+ — `, the size of the open set, the maximum id, the gate keys
     ADDED and the ids ADDED to the resolved set. The reviewer measured 65, 274,
     24, 1 and 19 at the base, with the open set 250 and the maximum `R-0713`.
 G6. THE TYPECHECK, AND THE FOUR TEXT READINGS S1 BINDS. From `apps/ui`, run
     `npx tsc --noEmit` and report the exit code and verbatim output; the
     reviewer ran that exact command at `f28640ef` and it exited 0 with NO
     output, so any output is this round's. Then, at C3, over
     `DecisionInboxCard.tsx` WITH COMMENTS STRIPPED by the module's own
     `strip_ts_comments`, report: the count of the substring `hidden`, which
     must be 0; whether the LAST `aria-live="polite"` in the file is opened by a
     `<p` tag; the exact text the module's
     `jsx_between_answer_button_and_live_paragraph` returns, and the count of
     `?`, `&&` and `||` within it, each 0; and the counts of `setSendingKeys(`
     and `clarification.defaultAnswer`, which must be 2 and 1. Report also the
     count of the substring `.target` in that stripped source, which must be
     EXACTLY 1, and quote the line carrying it: at `f28640ef` the file's only
     occurrence is `const typed = event.target.value;` in the clarification
     input's `onChange`, which is the DOM event's target and has nothing to do
     with a ref's. A count of 2 or more means a ref's target reached the markup,
     which is the leak S2 forbids.
 G7. THE GUARDS, GREEN THEN RED. Run `python3 -m pytest
     tests/ui_contracts/test_decision_answer_wiring.py -q` at C4 and report the
     exit code and count line, then `python3 -m pytest tests/ui_contracts/ -q`
     and report the same; the reviewer measured the whole directory at
     `f28640ef` as exit 0, `566 passed, 4 skipped`, and this round ADDS tests to
     it, so the passed count must GROW and the skipped count must not. Then, in
     a disposable worktree created with `git worktree add --detach
     .remedy-wt/f032-r14-mut <C4 sha>`, report the exit code, count line and
     `^FAILED` count for: a CONTROL run of that one test file before any
     mutation; mutation (a), the render of `answer.downside` deleted from the
     component; mutation (b), a ref's `target` rendered beside its label;
     mutation (c), the `:empty` collapse rule of S4 replaced by `display: none`;
     and a CONTROL after all three restorations, with the worktree's `git status
     --porcelain` empty. Name the FILE each mutation is applied to, count its
     exact byte string IN THAT FILE before applying it and report the count is
     1, and restore the file byte for byte before the next. Then remove the
     worktree and prune.
 G8. STRUCTURE, CANARY AND THE PR GATE. Run `python3 -m pytest
     tests/cli/test_golden_path.py -q` and report the exit code and count line.
     Report the path set of `git diff --name-only f28640ef..<C4 sha>` against the
     paths the Change set lists other than `.agent/handoff.md`, as the two
     residues, both EMPTY. Report that `git diff --stat f28640ef..<C4 sha> --
     packages/`, the same for `-- docs/`, and `git diff --name-only
     f28640ef..<C4 sha> -- apps/ui/src/api/` are ALL EMPTY. Report the insertion
     count of each of C0a through C4, that each is single-parent and each under
     500; those counts and the `+/-` column of the handback's `## Commits`
     section are one `git diff --numstat` reading written twice, compared cell by
     cell, and they must agree. Report the counts of `^<<<SLICE ` and `^<<<END `
     in `.agent/plan.md`, `.agent/live_review.md`,
     `apps/ui/src/components/panels/DecisionInboxCard.tsx`,
     `apps/ui/src/components/panels/RightLivePanel.module.css` and
     `tests/ui_contracts/test_decision_answer_wiring.py`, each 0, against a
     CONTROL over the committed C0a blob, which must be non-zero. Report `git
     ls-files .remedy-wt` as 0 lines, `git worktree list` as 1 line and `git
     branch --list "tmp/*"` as 0 lines. Report the output of `gh pr list --state
     open --json number,headRefName,baseRefName,isDraft`; merge nothing and
     create nothing.

Handback: rewrite `.agent/handoff.md` as C5, per
docs/agents/handback_template.md. It carries the mandated sections — the state
block, the commits table with each commit's real `+/-` read from `git diff
--numstat` for C0a through C4 — C5 cannot table its own numstat and says so in
its row — the item-status table covering every C and every S exactly once, the
deviations, the verification lines of G1 through G8 and the next steps. It states
that the feature is F032, that R14 is the round, and that this is SESSION 3,
which began at R10. Session 1 was R1 through R5 and session 2 was R6 through R9.
Fourteen rounds across three sessions is inside the soft limit of 25 rounds or 7
sessions, so do NOT emit a limit report. The handback has NO LENGTH CAP. BECAUSE
THIS IS THE FIRST F032 ROUND THE CANONICAL DESIGN REFERENCE BINDS, the handback
states which of its rules governed a choice this round made and whether ANY
visual deviation was taken; if one was, it goes in the assumption_log with its
technical reason, and if none was, say that plainly. Its `## Next` section names
Phase 1 rule 1 of docs/agents/self_drive_protocol.md — the `.agent/STOP` re-read
from disk — before anything else, then the Open PR Gate, then T003c: the chips
become deep links into the evidence panel, which is the slice that finally uses
the `target` this round deliberately does not render. Then push the branch.

<<<SLICE PLANF032R14>>>
# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D7.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R14 renders what R13's model carries: the receipts as chips on the card, the
honest note when a card has none, and each answer's expected outcome and
downside under the answer they belong to. It is the first F032 round the
canonical design reference binds, and §17 of its `ux_spec.md` decides the
markup — a ref's scrubbed label is shown, its raw target never is. The
component's existing contract guards read it as text, so this round adds its
own guards rather than leaving new markup unpinned.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R13 verdict | ordered | the record is touched first |
| C3 the component and its styles | ordered | S2 to S5, one commit |
| C4 the contract guards | ordered | S6 |
| C5 the handback | ordered | |

## Next Steps
1. T003c: the chips become deep links into the evidence panel, the slice that
   finally uses the `target` R14 deliberately does not render.
2. The integration gate — the full suite, per docs/agents/integration_gate.md.
3. The closure sequence: evidence job, a fresh review zip, the STATUS line and
   the pull request, per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The card's guards read the `.tsx` as TEXT, so a class name or an attribute
  carrying the substring `hidden`, or an `aria-live` added after the outcome
  paragraph, turns a guard red for a reason unrelated to what it protects.
- The empty cases are collapsed out of flow rather than removed, because the
  node has to stay in the accessibility tree; that is finding R-0686's lesson
  and the neighbouring rules already carry it.
<<<END PLANF032R14>>>

<<<SLICE LEDGER14>>>
Gate: F032 R13 — the F032 T003a CARD-MODEL entry, and the first round of T003. THE ROUND PASSED, AND THIS ENTRY STATES EXACTLY WHICH GATES THE REVIEWER RE-RAN AND WHICH IT COULD NOT. The reviewer re-ran G1 through G6 and G8 itself at `f28640ef`. It could NOT re-run G7: `npx vitest` and `node` are both refused by this session's sandbox, and after the refusal the reviewer stopped probing rather than routing around it, so THE VITEST COLOURS IN THIS ENTRY REST ON THE WORKER'S TRANSCRIPT AND NOT ON THE REVIEWER'S OWN RUN. That is the honest boundary of this verdict and it is stated here rather than left to be inferred. WHAT THE REVIEWER DID MEASURE ITSELF: `npx tsc --noEmit` from `apps/ui` at exit 0 with NO output, at the base AND at the tip; `python3 -m pytest tests/ui_contracts/ -q` at exit 0, `566 passed, 4 skipped`, IDENTICAL to the reading it took at the base before ordering the gate; the golden-path canary at exit 0, `42 passed`; and every structural gate. TRANSPORT IS PROVED FROM A VALUE THE REVIEWER HELD BEFORE DELEGATING: sha256 `35bccbc815fdae5117a4c88155c7a26027bfc03c4695e87f7df32d0d29108119` over 26943 bytes and 321 lines, carried by the committed `.agent/authored/f032-r13.md` blob at `7f1da6e6` and the committed `.agent/last_block.md` blob at `3bc7141f`, both the SAME git blob `755261e837a5`. THE ROUND'S DESIGN MOVE IS THE ONE THAT MATTERS AND IT IS RIGHT: an option's outcome is attached to ITS OWN ANSWER inside `decisionAnswers`, matched by the answer's `value` against the outcome's `option`, with a single unkeyed outcome applying to every answer when no key matches. That is the shape five of the eight producers emit, and it means the component T003b writes needs no matching logic and therefore no branch — which is what DECISION F031 D5 requires of that layer. The free-text fallback's `value` is the empty string, which IS `UNKEYED_OPTION`, so the optionless case reaches its outcome through the SAME match every other answer uses rather than through a special case. §17 OF THE DESIGN REFERENCE IS ENFORCED IN THE MODEL, WHICH IS THE CORRECT LAYER FOR IT: a ref's `label` is routed through `scrubUiText` and is the only one of the three fields a renderer may show, the `target` is carried untrimmed for the deep link T003c will add but is displayed nowhere, and `evidence_status` — which is literally the present/missing signal §17 forbids — never reaches the model at all, becoming a sentence instead. The reviewer confirmed all three by reading the committed source: `scrubUiText` is imported and applied to the label, and no `evidenceStatus` field exists on the model. A REF WHOSE TARGET IS BLANK IS DROPPED, which is the right call for a chip that will become a link, and a label that scrubs away falls back to a word rather than costing the receipt. THE WORKER DECLARED FIVE DEVIATIONS AND EVERY ONE WAS THE HONEST CALL. Two are worth recording. It could not run `npx vitest` either and ran `npm run test:unit -- <args>`, which echoes its resolved body into each transcript — the same binary, arguments and working directory — and it said so rather than reporting a command it had not run. And it produced G6's read-back at C4 rather than at the ordered C3, because doing it at C3 needed a denied ad-hoc TypeScript runner; it argued the values are still the C3 model's because `decisionCard.ts` is byte-identical at both commits, AND THE REVIEWER CHECKED THAT CLAIM RATHER THAN ACCEPTING IT: `git rev-parse` gives blob `39ce58ff77014cd86db6f57c75b88419860cb2ec` for that path at BOTH `5284ba66` and `8694120b`, so the argument holds. THE LEDGER MOVED EXACTLY AS ORDERED: 1086751 + 1 + 5183 = 1091935 with the base a byte PREFIX, both readers rejecting a byte flipped inside the FIRST appended paragraph, `^Gate: F\d+ R\d+ — ` 64 to 65 adding exactly `F032 R12`, and `^- R-\d+ — `, `^Done: R-\d+ — `, the open set at 250 and the maximum `R-0713` all unmoved. NOTHING ELSE MOVED: both path residues EMPTY, `packages/`, `tests/` and `docs/` EMPTY across the whole range, no `.tsx` and no `.css` touched, insertions 321, 252, 23, 2, 225, 407 and 305 across the seven commits, each single-parent and under 500, markers 0 and 0 in all four written files against a CONTROL of 2 and 2, `.remedy-wt` 0 tracked, `git worktree list` 1 line, the remote tip equal to the local tip and the Open PR Gate `[]`. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER14>>>
