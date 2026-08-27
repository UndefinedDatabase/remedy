STEP R13 / F032 — T003a: THE CARD MODEL LEARNS THE TRIPLE
Goal:        CARRY THE EVIDENCE TRIPLE INTO THE BROWSER'S CARD MODEL. The wire
             has carried `evidence_refs`, `outcomes` and `evidence_status`
             since T001b, and at `4b1b2e99` NOTHING in `apps/ui/src` reads any
             of the three: the receipts eight producers now write are invisible
             to the operator they were written for. This round projects them in
             `apps/ui/src/api/decisionCard.ts`, the layer DECISION F031 D5 puts
             ALL branching in, and attaches each option's expected outcome and
             downside TO ITS OWN ANSWER so the component that renders them
             needs no branch of its own. IT TOUCHES NO `.tsx` AND NO CSS: the
             projection into the card component is the next round, and keeping
             it out of this one is what lets every line this round ships be
             covered by the vitest suite the shipped config collects.
             SESSION 3 CONTINUES; YOU CREATE NO PULL REQUEST AND MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the R12 verdict · C3 the model and its types · C4 its
             tests · C5 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r13.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `apps/ui/src/api/decisionCard.ts`,
             `apps/ui/src/api/decisionCard.test.ts`, `.agent/handoff.md`.
             NOTHING under `packages/`, nothing under `tests/`, no `.tsx`, no
             `.css`. Nothing under `docs/`, so no docs-round gate is owed.

Constraints.
 1. YOU DO NOT EDIT ANY SLICE. A `<<<SLICE NAME>>>` line and its `<<<END NAME>>>`
    line delimit text you apply byte for byte. If a slice looks wrong, apply it
    anyway and say so in the handback's deviations. The marker lines themselves
    are NEVER written into any file.
 2. SLICE CONVENTION. A slice's content is every line strictly between its two
    marker lines. When the slice replaces a whole file, the file's bytes are
    those lines joined with `\n` plus ONE trailing `\n` and nothing more. When
    the slice is appended, the file's new bytes are its old bytes plus ONE `\n`
    plus that same joined text plus ONE trailing `\n`, applied only if the old
    bytes already end in a newline — `.agent/live_review.md` does; G5 proves the
    arithmetic.
 3. THE AUTHORED UNITS OF THIS BLOCK are the whole block itself and the slices
    PLANF032R13 and LEDGER13. This paragraph gives no count of them; G3 reports
    the number the extraction measured.
 4. C0a IS A COPY, NOT A RETYPE. `.remedy-wt/f032-r13.md` exists on disk and
    holds this block. Copy that file to `.agent/authored/f032-r13.md` with a
    byte-preserving read-and-write and commit it. C0b then writes the SAME
    bytes to `.agent/last_block.md`.
 5. PRODUCTION CODE IS DESCRIBED, NOT SLICED. Items S1 through S8 are a spec.
    You write the TypeScript yourself, in the style of the module you are
    editing, and you carry the WHY into a doc comment above each addition the
    way that module already does for every field it has.
 6. THE MODULE'S OWN CONTRACT BINDS THIS ROUND, and it is stated in its header
    comment: every branch a card needs lives in `decisionCard.ts` so the `.tsx`
    stays a thin projection, and `decisionAnswers` MUST NOT branch on
    `card.type` — the type is data, never control flow. Nothing you add may
    branch on a decision's type either. Every reader you add is TOTAL: a
    missing, null, or wrongly-typed value falls back, exactly as
    `cardClarifications` and `payloadOptions` already do, and NO input makes the
    model throw.
 7. ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, in that order and with no
    commit between them. C2 is the only commit touching `.agent/live_review.md`.
 8. RE-READ `.agent/STOP` FROM DISK TWICE: once before C0a and once before C5.
 9. MUTATION RUNS GO IN A DISPOSABLE WORKTREE, and vitest needs help to run in
    one: `apps/ui/node_modules` is gitignored, so a fresh worktree carries
    neither the runner nor a config that can import it. Run it from the PRIMARY
    checkout's `apps/ui` directory with `--root <worktree>/apps/ui` and
    `--config <primary>/apps/ui/vitest.config.ts`, SCOPED to
    `src/api/decisionCard.test.ts` and nothing else — an unscoped run collects
    files that fail to resolve under `--root` and reports a worktree artifact
    rather than a result. Report the UNMUTATED control from the SAME worktree
    beside every mutated run: a colour with no baseline is not evidence.
10. THE ROUND BASE IS `4b1b2e99`. Every numeral this block states about the
    base was measured there.
11. RUN THE SUITES SERIALLY. Never two test processes at once.
12. THIS ROUND SHIPS NO VISUAL CHANGE. It adds no component, no element, no
    class and no token, so the canonical design reference imposes no visual
    decision on it and NOTHING is owed to an assumption_log. Say that plainly
    in the handback rather than leaving it unmentioned.

Spec — T003a, the model.
 S1. READ FIRST. `apps/ui/src/api/decisionCard.ts` at `4b1b2e99` exports
     `DecisionAnswerKind`, `DecisionAnswer`, `DecisionClarification`,
     `DecisionCardModel`, `DecisionInboxEntry`, `DecisionInboxDocument`,
     `decisionAgeLabel`, `decisionBlockedLabel`, `decisionAnswers`,
     `buildDecisionCardModel`, `decisionCardModels` and `countOpenDecisions`.
     `decisionAnswers` derives affordances in the order options, then next
     actions, then a free-text fallback, stamping one card-wide `posts` on each.
     `export_decision_json` in `packages/orchestration/decision_queue.py` puts
     `evidence_refs`, `outcomes` and `evidence_status` on every card, ALWAYS
     present and EMPTY rather than absent when there is no triple. A ref is
     `{kind, target, label}`; an outcome is `{option, expected_outcome,
     downside}`; an optionless decision keys its single outcome with the EMPTY
     STRING, which is `UNKEYED_OPTION`.
 S2. THE COPY RULE IS THE LOAD-BEARING CONSTRAINT OF THIS ROUND, and it is why
     the model decides the display text rather than the component. §17 of
     `docs/ui/design_reference/ux_spec.md` forbids the default UI to show raw
     UUIDs, raw JSON, metadata and present/missing signals. A ref's `target` is
     frequently exactly that — a test run id, an escalation id like `td:1`, a
     stop record id — and `evidence_status` is literally a present/missing
     signal. So: THE CHIP'S TEXT IS THE REF'S `label`, which every producer
     writes as a human sentence, and never its `target`. Route that label
     through `scrubUiText` from `../copy/humanCopy`, which §17 names as the only
     way human phrasing is produced and which already rejects both the forbidden
     words and a bare hex id. The `target` is still CARRIED on the model,
     because the next round's deep link needs it, but nothing this round writes
     displays it.
 S3. THE REF PROJECTION. Add an exported interface for one projected ref
     carrying `kind`, `target` and `label` — the first two exactly as the
     endpoint sent them, the third the scrubbed text of S2 — and a `chipLabel`
     is NOT a separate field: `label` IS what a renderer shows. Project the
     card's `evidence_refs` into a new `evidenceRefs` field on
     `DecisionCardModel`, EMPTY for a card with no triple so a renderer needs no
     branch. A non-array value gives no refs; a non-object entry is skipped; a
     ref whose `target` is blank after trimming is DROPPED, because a chip that
     points at nothing cannot be followed and the next round's deep link would
     have nothing to open. A ref whose `label` scrubs to the fallback still
     renders — losing the receipt entirely would be worse than showing a generic
     word — so pass a fallback of your choosing that reads as a receipt.
 S4. THE OUTCOME REACHES ITS ANSWER, which is the round's real design move.
     Give `DecisionAnswer` two new fields, `expectedOutcome` and `downside`,
     both the EMPTY STRING when the card carries no triple. Match them by the
     answer's own `value` against each outcome's `option`. When NO outcome
     matches by key AND the card carries exactly one outcome whose `option` is
     the empty string, that unkeyed outcome applies to EVERY answer of the card
     — that is the shape five of the eight producers emit. When neither holds,
     both fields stay empty. Do this inside `decisionAnswers` so that a card and
     its answers can never disagree, exactly as the `posts` comment in that
     function already argues for the reading it stamps. THE FUNCTION STILL MUST
     NOT BRANCH ON `card.type`.
 S5. THE STATUS BECOMES A SENTENCE, NEVER A SIGNAL. Add an `evidenceNote` field
     to `DecisionCardModel`: the EMPTY STRING when the card's `evidence_status`
     is `present`, and a short human sentence when it is anything else,
     including absent — a card recorded before the requirement says so in words
     the operator can read. Do NOT put the raw status string on the model and do
     NOT name either status constant in any text a renderer shows; S2 is why.
     Carry no boolean beside it: the empty string already tells a renderer there
     is nothing to say, and a second field would let the two disagree.
 S6. NOTHING ELSE ON THE MODEL CHANGES. `answers`, `clarifications`,
     `answerableByDecisionResolve`, the labels and the counts keep their current
     behaviour and their current types, and `decisionCardModels` and
     `countOpenDecisions` are untouched.
 S7. THE INTERFACE `DecisionInboxEntry` gains the three endpoint keys as
     OPTIONAL and UNTRUSTED — `evidence_refs?: unknown`, `outcomes?: unknown`,
     `evidence_status?: unknown` — for the reason its own comment already gives:
     the payload comes from a producer this module does not control and must
     still type-check. Do not rename a key on the way in.
 S8. THE TESTS GO IN `apps/ui/src/api/decisionCard.test.ts` and nowhere else.
     Cover: a card with two options and two keyed outcomes, asserting each
     answer carries ITS option's expected outcome and downside; a card with one
     unkeyed outcome and several next-action commands, asserting every answer
     carries that one outcome's text; a card with NO triple, asserting every
     answer carries two empty strings and `evidenceRefs` is empty; a card whose
     outcome keys match none of its options, asserting both fields stay empty; a
     card whose refs include one with a blank target, asserting it is dropped
     and the others survive; a ref whose label is a bare hex id, asserting the
     scrubbed fallback is shown and the raw id is NOT; the three
     `evidence_status` cases of S5 — present, legacy, absent; and the totality
     rule, driving a non-array `evidence_refs`, a non-array `outcomes`, a
     non-object ref entry and a null payload through
     `buildDecisionCardModel` and asserting it returns a model rather than
     throwing. Assert also that `decisionCard.ts` still contains no `card.type`
     branch, in whatever way that file's existing tests already measure the
     refusal its header describes — read them first and follow that method
     rather than inventing a second one.

Done when. Report each gate as its own line in the handback, with the real
command, its exit code and the real output you saw. G1 through G8 are ordered at
commits STRICTLY EARLIER than C5, which writes the handback; G1 therefore stops
at C4.
 G1. HYGIENE, BASE AND THE SENTINEL. Report `git rev-parse HEAD` before C0a and
     confirm it is the base of constraint 10; report the branch is
     `feature/f032-evidence-triple`; report the `git status --porcelain` line
     count after EACH of C0a through C4, each 0; report whether `.agent/STOP`
     exists at the two readings constraint 8 orders.
 G2. TRANSPORT. Report the sha256, byte count and line count of
     `.remedy-wt/f032-r13.md`, of the committed `.agent/authored/f032-r13.md`
     blob and of the committed `.agent/last_block.md` blob, and whether all
     three are EQUAL. Report the git blob hash of the C0a and C0b paths and
     whether they are the SAME blob. State plainly that this proves the
     reviewer's scratch original, the saved copy and the mirror agree, and says
     NOTHING about the bytes of any prompt.
 G3. EXTRACTION AND CAPS. From the COMMITTED C0a blob, extract every region
     between a `^<<<SLICE ` line and its `^<<<END ` line. Report the NAME and
     content-line count of each, the number of regions, the CONTENT total, the
     block's TOTAL line count and PROSE as TOTAL minus CONTENT. Report whether
     PROSE is under 400 and TOTAL under 490. Report the numbers YOU measured.
 G4. THE PLAN. Report whether `.agent/plan.md` at C1 is byte-equal to slice
     PLANF032R13 under the convention of constraint 2, and the same comparison
     with the trailing newline removed as a NEGATIVE CONTROL, which must be
     FALSE. Report `wc -l` and that it is under 50, and the counts of
     `^## Goal$` and `^## Next Steps$`, each 1.
 G5. THE LEDGER APPEND. Read the pre-commit blob with `git show
     4b1b2e99:.agent/live_review.md`, never by writing over the tracked file.
     Prove `.agent/live_review.md` at C2 equals that blob plus ONE newline plus
     the LEDGER13 slice, byte for byte; report the arithmetic as three numbers
     summing to the result and that the pre-commit blob is a byte PREFIX. Then
     run a SECOND, INDEPENDENT structural reader: split the whole file on blank
     lines, let N be the number of paragraphs in the LEDGER13 slice as YOUR
     script counts them, and compare the LAST N units against those N paragraphs
     IN ORDER. As a NEGATIVE CONTROL flip ONE byte inside the FIRST appended
     paragraph, in memory only, and report that BOTH readers reject it. The
     reviewer measured the base at `4b1b2e99` as 1086751 bytes over 429
     blank-line units. Then report, before and after C2, the counts of
     `^Gate: F\d+ R\d+ — `, `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-` and
     `^Gate: R\d+ — `, the size of the open set, the maximum id, the gate keys
     ADDED and the ids ADDED to the resolved set. The reviewer measured 64, 274,
     24, 1 and 19 at the base, with the open set 250 and the maximum `R-0713`.
 G6. THE TYPECHECK, AND THE MODEL READ BACK. From `apps/ui`, run
     `npx tsc --noEmit` and report the exit code and the verbatim output. The
     reviewer ran that exact command at `4b1b2e99` and it exited 0 with NO
     output, so any output at all is this round's. Then, at C3, report for each
     of these cards the `answers` array as `(kind, value, expectedOutcome,
     downside)` tuples, the `evidenceRefs` as `(kind, target, label)` tuples and
     the `evidenceNote`: a two-option card with two keyed outcomes; a card with
     one unkeyed outcome and two next actions; a card with no triple at all; and
     a card carrying a ref with a blank target beside a valid one.
 G7. THE MODEL'S TESTS, GREEN THEN RED. From `apps/ui` in the PRIMARY checkout
     at C4, run `npx vitest run src/api/decisionCard.test.ts` and report the
     exit code and the full count line. Then, using the worktree recipe of
     constraint 9, report the exit code and count line for: the UNMUTATED
     CONTROL in that worktree; mutation (a), the unkeyed-outcome fallback of S4
     removed so only exact key matches carry text; mutation (b), the blank-target
     drop of S3 removed so such a ref survives; mutation (c), the `scrubUiText`
     call of S2 replaced by the raw label so a bare hex id would reach a
     renderer; and the CONTROL again after all three restorations, with the
     worktree's `git status --porcelain` empty. Name the FILE each mutation is
     applied to, count its exact byte string IN THAT FILE before applying it and
     report that the count is 1, and restore the file byte for byte before the
     next.
 G8. THE GUARDS, THE CANARY AND THE PR GATE. Run
     `python3 -m pytest tests/ui_contracts/ -q` from the repository root and
     report the exit code and the count line; the reviewer ran that exact
     command at `4b1b2e99` and it exited 0 at `566 passed, 4 skipped`. This
     round adds no Python test and changes no `.tsx`, so any other reading is
     this round's to explain. Run `python3 -m pytest tests/cli/test_golden_path.py -q` and
     report the exit code and count line. Report the path set of `git diff
     --name-only 4b1b2e99..<C4 sha>` against the paths the Change set lists other
     than `.agent/handoff.md`, as the two residues, both EMPTY. Report that `git
     diff --stat 4b1b2e99..<C4 sha> -- packages/`, the same for `-- tests/`, the
     same for `-- docs/`, and `git diff --name-only 4b1b2e99..<C4 sha> -- 'apps/**/*.tsx' 'apps/**/*.css'`
     are ALL EMPTY. Report the insertion count of each of C0a through C4, that
     each is single-parent and each under 500; those counts and the `+/-` column
     of the handback's `## Commits` section are one `git diff --numstat` reading
     written twice, compared cell by cell, and they must agree. Report the counts
     of `^<<<SLICE ` and `^<<<END ` in `.agent/plan.md`, `.agent/live_review.md`,
     `apps/ui/src/api/decisionCard.ts` and `apps/ui/src/api/decisionCard.test.ts`,
     each 0, against a CONTROL over the committed C0a blob, which must be
     non-zero. Report `git ls-files .remedy-wt` as 0 lines, `git worktree list`
     as 1 line and `git branch --list "tmp/*"` as 0 lines. Report the output of
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`;
     merge nothing and create nothing.

Handback: rewrite `.agent/handoff.md` as C5, per
docs/agents/handback_template.md. It carries the mandated sections — the state
block, the commits table with each commit's real `+/-` read from `git diff
--numstat` for C0a through C4 — C5 cannot table its own numstat and says so in
its row — the item-status table covering every C and every S exactly once, the
deviations, the verification lines of G1 through G8 and the next steps. It states
that the feature is F032, that R13 is the round, and that this is SESSION 3,
which began at R10. Session 1 was R1 through R5 and session 2 was R6 through R9.
Thirteen rounds across three sessions is inside the soft limit of 25 rounds or 7
sessions, so do NOT emit a limit report. The handback has NO LENGTH CAP. It states
plainly what constraint 12 requires about the design reference. Its `## Next`
section names Phase 1 rule 1 of docs/agents/self_drive_protocol.md — the
`.agent/STOP` re-read from disk — before anything else, then the Open PR Gate,
then T003b: the card component projecting what this round's model now carries,
which is the round that touches `.tsx` and CSS and is therefore the one bound by
the canonical design reference, and which must first read the source-counting
guards in `tests/ui_contracts/test_decision_answer_wiring.py`. Then push the
branch.

<<<SLICE PLANF032R13>>>
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
T002 is COMPLETE: all eight producing types carry real triples and the emit
gate is fully live. R13 opens T003 on the browser side, where nothing has read
`evidence_refs`, `outcomes` or `evidence_status` since T001b put them on the
wire. It projects all three in `apps/ui/src/api/decisionCard.ts` — the layer
DECISION F031 D5 puts all branching in — and attaches each option's outcome to
ITS OWN answer. No `.tsx` and no CSS this round.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R12 verdict | ordered | the record is touched first |
| C3 the model and its types | ordered | S2 to S7 |
| C4 its tests | ordered | S8 |
| C5 the handback | ordered | |

## Next Steps
1. T003b: the card component projects what the model now carries — chips for
   the refs, each option's outcome and downside under its own answer. It is
   the round that touches `.tsx` and CSS, so it is bound by the canonical
   design reference, and it must first read the source-counting guards in
   `tests/ui_contracts/test_decision_answer_wiring.py`.
2. T003c: the chips deep-link into the evidence panel.
3. The integration gate, then the closure sequence.

## Risks
- §17 of `docs/ui/design_reference/ux_spec.md` forbids the UI to show raw ids
  or present/missing signals, and a ref's `target` is often exactly a raw id.
  The model therefore decides the display text and routes it through
  `scrubUiText`; a renderer that reached for `target` instead would reintroduce
  the leak the model exists to prevent.
- The model is the only layer the shipped vitest config can cover, so keeping
  the component out of this round is what makes every line of it testable.
<<<END PLANF032R13>>>

<<<SLICE LEDGER13>>>
Gate: F032 R12 — the F032 T002g TASK-DECISION entry, and the close of T002. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all eight itself at `4b1b2e99`. TRANSPORT IS PROVED FROM A VALUE THE REVIEWER HELD BEFORE DELEGATING: sha256 `54d38edecca151a2d01a5c59dc0369dcba942975eeaaef718e4e13e021b9217d` over 29343 bytes and 357 lines was computed on the scratch original at authoring time, and the committed `.agent/authored/f032-r12.md` blob at `9857f7ee` and the committed `.agent/last_block.md` blob at `7f1ca6f6` both carry exactly it, as the SAME git blob `be1d3fe9c07c`. That chain runs from an independently held digest through the saved copy to its mirror, and under docs/agents/self_drive_protocol.md there is no paste relay, so it says NOTHING about the bytes of any prompt. T002 IS COMPLETE, AND THE REVIEWER MEASURED THE CLAIM RATHER THAN READING IT: `sorted(TRIPLE_REQUIRED_TYPES)` equals `sorted(PRODUCING_DECISION_TYPES)` from `tests/orchestration/test_decision_inbox.py` exactly, and the only members of `DECISION_TYPES` outside the enforced set are `worker_approval` and `revert_missing`, the two DECISION F031 D3 records as having no producer at all. THE LAST PRODUCER IS THE ONLY ONE WHOSE OPTIONS THE CODE NEVER SEES, and it is right that it was left for last: the escalation record supplies arbitrary strings, so the outcomes are BUILT in a loop and the same code satisfies rule (g) when the record offers choices and rule (h) when it offers none. The outcomes are built from `options`, THE SAME LIST THE PAYLOAD CARRIES, which is what makes the bidirectional key comparison safe by construction rather than by luck. THE TEXT TURNS ON THE TWO THINGS THE RECORD ACTUALLY KNOWS: whether an option is the `safe_default`, and the record's own `impact` — the field amendment A3 carried forward to T002 twelve rounds ago as the nearest thing to an `expected_outcome` already on disk, and which this round finally uses. THE REVIEWER RAN SIX MUTATIONS IN ITS OWN DISPOSABLE WORKTREE AT `a83abda3`, four ordered and two not, `__pycache__` purged and `-B` passed before each, every exact byte string counted 1 before it was applied and the file restored and re-compared afterwards: keying a built outcome with a constant gave exit 1 at `20 failed, 114 passed`; the `answer` ref made unconditional gave exit 1 at `21 failed, 113 passed`; `task_decision` removed from the gate set gave exit 1 at `2 failed, 132 passed`; `safe_default` forced empty gave exit 1 at `2 failed, 132 passed`; dropping the `impact` note gave exit 1 at `1 failed, 133 passed`; and removing the unkeyed fallback, which is the rule (h) half nothing else pins, gave exit 1 at `5 failed, 129 passed`. The controls before and after all six restorations were a real exit 0 at `134 passed`, with the worktree's `git status --porcelain` empty. THE WORKER CAUGHT A COLLISION THE BLOCK DID NOT ANTICIPATE and fixed it before committing: its first draft named a test factory `_resolved_decision`, which shadowed the flight-plan helper R11 had added to the same file and turned eight R11 tests red with a `TypeError`; it renamed its own six factories and altered no R11 test, which is the correct direction of repair. NOTHING ELSE MOVED: `ruff check` over both modules exit 0 with the verbatim output `All checks passed!`, the five decision suites as one process exit 0 at `303 passed`, the golden-path canary exit 0 at `42 passed`, both path residues EMPTY, `apps/` and `docs/` EMPTY across the whole range, markers 0 and 0 in all five written files against a CONTROL of 2 and 2, `.remedy-wt` 0 tracked, `git worktree list` 1 line, the remote tip equal to the local tip and the Open PR Gate `[]`. THE LEDGER MOVED EXACTLY AS ORDERED: 1081523 + 1 + 5227 = 1086751 with the base a byte PREFIX, both readers rejecting a byte flipped inside the FIRST appended paragraph, `^Gate: F\d+ R\d+ — ` 63 to 64 adding exactly `F032 R11`, and `^- R-\d+ — `, `^Done: R-\d+ — `, the open set at 250 and the maximum `R-0713` all unmoved, because this round registered no finding and resolved none. ONE EXTRA COMMIT WAS MADE AND DECLARED, `4b1b2e99`, correcting a false numeral the worker found in its own committed handback during self-review — it had written that G1 covered five readings where it covers six. The reviewer accepts it and records the rule it should have followed instead, BINDING ON THE NEXT BLOCK THAT ORDERS A HANDBACK: `.agent/handoff.md` is rewritten in full every round and is not an append-only record, so a false numeral in it is corrected by a deviation line in the NEXT handback and never by a commit of its own. Operator amendment amend0827 rule 1 removes pure bookkeeping ROUNDS for exactly this reason, and the same argument reaches a bookkeeping COMMIT whose target the next round overwrites anyway. The insertion counts across the whole range were 357, 244, 25, 2, 145, 296, 252 and 12, each single-parent and each under 500, and the correction commit changed no path outside the change set. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER13>>>
