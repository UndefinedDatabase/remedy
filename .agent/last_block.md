── STEP STEERING INPUT — F021 ──
Goal:        Record R35, which PASSED, and build the LAST unbuilt item of this
             feature: the steering input, rendered VISIBLE and DISABLED with
             the honest reason its not-yet backend warrants. A new
             `ChatInput.tsx`, the CSS ux_spec.md §11.3 binds, both branches of
             the activity card, a contract that pins all of it, and DECISION
             F021 D11 recording which of two conflicting tooltip wordings ships
             and why. TWO corrections are appended naming OPEN findings R-0439
             and R-0402; NEITHER mints an id, and both are the REVIEWER's own
             defects in the R35 block.

Fortschritt: ~100 % der Bauarbeit (nach dieser Runde ist jedes Teil von T001
             bis T003 gebaut; es folgen nur noch die Abschlussrunden)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R35 verdict
             and the two corrections · C3 DECISION F021 D11 · C4 the component,
             the CSS and both render sites · C5 the contract · C6 handback.

Change:      Exactly these paths. I COUNTED this list mechanically rather than
             describing it, because miscounting this very sentence is what C2
             records twice: the list holds TEN entries, of which NINE are not
             the handoff.
             `.agent/authored/f021-r36.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/decisions.md` (C3) ·
             `apps/ui/src/components/panels/ChatInput.tsx` (NEW, C4) ·
             `apps/ui/src/components/panels/ActivityFeedCard.tsx` (C4) ·
             `apps/ui/src/components/panels/RightLivePanel.module.css` (C4) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C5) ·
             `.agent/handoff.md` (C6). Report the counts YOU measure at both
             readings rather than confirming mine.

Constraints:
 1. Apply every slice and pair half BYTE FOR BYTE. Never retype, rewrap,
    reflow, reindent or whitespace-adjust one. If a slice looks wrong, STOP and
    say so in the handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and is not negotiable. C3
    lands the DECISION BEFORE the code that cites it, so the comment in
    ActivityFeedCard.tsx never points at a record that does not exist. C4 lands
    the surface BEFORE C5 pins it. ROUND BASE is `78c72880` — resolve its full
    form with `git rev-parse`.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. Before it, in
    `.agent/live_review.md`: 224 registered under the canonical pattern
    `^- R-\d+ — `, maximum R-0661, `Done: R-` 1. After C2: still 224, still all
    DISTINCT, still maximum R-0661, `Done: R-` still 1. Both corrections name
    OPEN findings (§3 checklist item 30), and `^- R-0439 — ` and
    `^- R-0402 — ` each stay at exactly 1 across C2.
 4. NO PARAGRAPH OF RECORD36 BEGINS WITH THE BYTES `- R-`. Two open
    `Recurrence: ` and the verdict opens `Gate: R36 — `. The three paragraphs
    are separated by EXACTLY ONE BLANK LINE. G5 measures this.
 5. THE APPEND CONVENTION, STATED PER TARGET FILE because the three differ.
      `.agent/live_review.md` at C2 and `.agent/decisions.md` at C3: the slice
      is quoted WITHOUT a trailing newline; add EXACTLY ONE newline, then the
      slice, then one terminator, so each join carries EXACTLY ONE BLANK LINE.
      I measured both files: each ends in a single newline at the round base,
      and each already separates its entries by one blank line.
      `tests/ui_contracts/test_brain_stream_ring.py` at C5: EXACTLY TWO ADDED
      NEWLINES, then CONTRACTSLICE36, then one terminator — PEP 8 E302, which
      `ruff` cannot see because E301-E306 are preview-only. NOT to be repaired:
      that file already carries ONE class with a single blank line above it,
      `TestTheFeedScrollRuleIsWiredToTheCard`, landed at R31.
    A WHOLE-FILE write (PLANF021R36) and a NEW FILE (CHATINPUT) are each the
    slice PLUS one terminator, and nothing else.
 6. BOTH `.agent/live_review.md` AND `.agent/decisions.md` ARE APPEND-ONLY. No
    landed paragraph, `Gate:`, `Recurrence:` or `## DECISION` entry is edited.
 7. NO COUNT GATE IN THIS BLOCK COUNTS A STRING WHOSE NUMBER THIS BLOCK'S OWN
    SLICES CHANGE, AND EVERY LEDGER COUNT NAMES ITS PATTERN, ANCHORED. An
    UNANCHORED count is never ordered over `.agent/live_review.md` or
    `.agent/decisions.md`, both of which quote the tokens a gate might count
    (R-0630). This rule is why G4 counts `<ChatInput disabled` in the CARD and
    not in this block.
 8. NO PER-LINE UNIQUENESS COUNT IS ORDERED OVER ANY PAIR'S TO THIS ROUND.
    §4.9's "each TO-only line exactly once" is a PROSE rule and code repeats
    lines structurally — R-0439, which C2 records, and which R35's G4 hit on
    `}) {` and `        );`. G4 orders an ORDERED-EQUALITY REPLAY instead:
    re-applying the pairs to the base blobs must reproduce the committed blobs
    byte for byte. That is a stronger property and it cannot be defeated by a
    repeated line.
 9. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide at every commit under R-0622 and is NOT a gate of this round
    — do not run it and do not report it. Create and merge NO pull request.
    Push the branch after C6. ONE worktree under `.remedy-wt/` is ordered, for
    G6's red-proof alone; remove it and prove the tree clean afterwards.
10. THE SIX PAIRS AND THEIR SHAPES, ALL MEASURED BY MY SCRIPT. Each FROM occurs
    EXACTLY ONCE in its target at the round base. FOUR ARE APPEND-SHAPED —
    CHATIMPORTPAIR, REASONPAIR, CHATCSSPAIR and CHATCONSTPAIR, each TO opening
    with its own FROM — so §4.9 FORBIDS a FROM-zero count for them. TWO ARE NOT
    — LIVEBRANCHPAIR and FALLBACKBRANCHPAIR — and their FROM-zero IS owed. My
    script printed each of these six shapes; I did not infer one of them from
    another. Four pairs edit `ActivityFeedCard.tsx`: apply them in the order
    CHATIMPORTPAIR, REASONPAIR, LIVEBRANCHPAIR, FALLBACKBRANCHPAIR. None
    overlaps another. WARNING, measured: a FROM's uniqueness here is stated
    PER TARGET FILE and not tree-wide — R35's worker found IMPORTPAIR's FROM
    verbatim in three files — so resolve every pair against the ONE file the
    Change list names for it, never by searching the tree.
11. WHAT I DRY-RAN AND WHAT I COULD NOT. In a worktree at `78c72880` I applied
    all six pairs, CHATINPUT and CONTRACTSLICE36 and measured:
    `tests/ui_contracts/` 494 passed and 5 skipped, against 489 and 5 at the
    base IN THAT WORKTREE — the fifth skip is a worktree artifact, `dist/assets/
    not built`, and is why the PRIMARY numbers G7 names are 4 skips, not 5.
    The contract file alone printed 67 passed against 62. G6's red-proof
    printed `1 failed, 66 passed`. I could NOT run `tsc` cleanly in a worktree
    — no `node_modules`, symlink denied — though I did confirm the filtered
    error list for the two touched `.tsx` files is EMPTY once the missing-module
    cascades are removed. THE WORKER'S `tsc` RUN IS STILL THE FIRST HONEST
    EXECUTION. If it is red, STOP and report; a type error there is my defect.
12. THE TOOLTIP WORDING IS A REAL CONFLICT AND C3 IS WHERE IT IS SETTLED, not
    a choice made silently in a slice. `docs/ui/design_reference/ux_spec.md`
    §11.3 quotes one sentence; `docs/roadmap/features/T5_F021.md` quotes a
    shorter paraphrase naming F030. `.agent/context.md` makes the design
    reference BINDING for every visual surface, so the reference's sentence
    ships. Do not substitute the other, and do not merge them.
13. Block size, measured on these final bytes AFTER the last edit: TOTAL 448
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice and
    pair CONTENT lines — 255 against DECISION F085 D5's 400. Markers count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C6; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2, C3, C4 and C5. C6's own
     reading is ordered NOWHERE — §3 item 31 leaves it to the next session.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r36.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over my
     emitted copy at `.remedy-wt/f021-r36.md` are all equal. Write C0b FROM the
     committed C0a blob. Report the digest, bytes and lines. Then extract the
     slices and pairs from the COMMITTED C0a blob by their marker LINES,
     `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO `, and report how many whole
     texts, how many pairs and how many CONTENT lines your extractor printed —
     each a number YOU measured — re-measuring constraint 13's two numerals
     from that same blob against their caps.
 G3  `.agent/plan.md` at C1 equals PLANF021R36 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0, with a NEGATIVE CONTROL against the bare slice that must
     exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1, and the `wc -l` YOU measure against
     AGENTS.md's "keep it short (<50 lines)". If that count is 50 or more, STOP
     and report — do NOT trim the file to reach it (R-0654).
 G4  THE SIX PAIRS AND THE NEW FILE, read against constraint 10's measured
     shapes. For LIVEBRANCHPAIR and FALLBACKBRANCHPAIR report the FROM at
     EXACTLY 1x at the round base and EXACTLY 0x at C4. For CHATIMPORTPAIR,
     REASONPAIR, CHATCSSPAIR and CHATCONSTPAIR report the FROM at EXACTLY 1x at
     the base AND EXACTLY 1x after its own commit — they are append-shaped and
     the zero is NOT owed; note CHATCONSTPAIR lands at C5, not C4, so read it
     there. THEN THE REPLAY, which constraint 8 orders in place of a per-line
     count: take each edited file's blob at the round base and apply that
     file's OWN transformation — for `ActivityFeedCard.tsx` its four pairs in
     constraint 10's order, for `RightLivePanel.module.css` CHATCSSPAIR alone,
     and for `test_brain_stream_ring.py` CHATCONSTPAIR followed by constraint
     5's two-newline append of CONTRACTSLICE36 — and report that each result is
     BYTE-IDENTICAL to that file's committed blob at the commit that lands it.
     Report `git cat-file -e 78c72880:apps/ui/src/components/panels/
     ChatInput.tsx` FAILING at the base, and `cmp` at exit 0 between the
     committed file and CHATINPUT plus one newline, with a negative control at
     exit 1. Report `<ChatInput disabled` occurring 0x in `ActivityFeedCard.tsx`
     at the base and a number YOU count at C4, and `.chatInput` 0x in the CSS at
     the base and a number YOU count.
 G5  THE LEDGER AND THE DECISION RECORD, every count naming its anchored
     pattern. In `.agent/live_review.md`, base then C2: canonical `^- R-\d+ — `
     224 then 224, ALL DISTINCT at both, maximum R-0661 at both; loose `^- R-`
     225 then 225, gap 1 at both; `^Done: R-` 1 then 1; `^Gate: R` 34 then 35,
     DISTINCT at both; `^Gate: R36` 0 then 1; `^Recurrence: ` 11 then 13;
     `^Recurrence: R-0439 — ` 0 then 1; `^Recurrence: R-0402 — ` 1 then 2 —
     NOT a zero-then-one, because R35's C2 already landed one; `^- R-0439 — `
     and `^- R-0402 — ` 1 then 1 each. RECORD36 paragraphs opening `- R-`: 0.
     In `.agent/decisions.md`, base then C3: `^## DECISION ` 117 then 118;
     `^## DECISION F021 D11` 0 then 1; `^## DECISION F021 D10` 1 then 1. For
     BOTH files report that the base blob is a byte-exact PREFIX of the new one
     and that the remainder is EXACTLY one newline plus the slice plus one
     newline.
 G6  THE RED-PROOF, in a disposable worktree at C5 under `.remedy-wt/`, never
     in the primary checkout. There, DELETE the single line
     `      <ChatInput disabled reason={STEERING_DISABLED_REASON} />` that sits
     immediately above the `    </section>` of the PRE-STREAM FALLBACK branch —
     the branch a reader sees before any job runs — leaving the live branch's
     copy untouched, and run `python3 -m pytest
     tests/ui_contracts/test_brain_stream_ring.py -q -rf`. Report the failure
     count and the failing node id, which MUST be
     `TestTheSteeringInputIsHonestlyDisabled::test_the_card_renders_it`. I
     measured `1 failed, 66 passed`. This mutation is chosen because it is the
     one a reviewer reading a running cockpit would never see. Then remove the
     worktree and report `git status --porcelain` at 0 lines and
     `git worktree list` naming the primary checkout alone.
 G7  THE SUITES, SERIAL, in the PRIMARY checkout, never two at once. Count by
     PASSED PLUS SKIPPED, which `.agent/context.md` requires.
     `python3 -m pytest tests/ui_contracts/ -q -rf` — I measured 490 passed and
     4 skipped at the round base, so 494; C5 adds CONTRACTSLICE36's FIVE tests,
     so I expect 495 passed and 4 skipped; report what YOU measure and the
     difference. `npm run test:unit` from `apps/ui` — 16 files and 218 tests at
     the base, and this round adds no `.test.ts`, so the SAME numbers are
     expected and a change is a finding. `npx tsc --noEmit` from `apps/ui` —
     exit 0 and EMPTY output; read constraint 11 first. Then, because this
     round rewrites `.agent/` state, ALL FOUR state readers:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py -q -rf` — 528 at the base. Then
     the canary, `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — 42
     at the base. Then `python3 -m ruff check
     tests/ui_contracts/test_brain_stream_ring.py`, GREEN at the base, so exit
     0 is honest. No ruff gate for the `apps/` files, which are not Python.
 G8  STRUCTURE. `git diff --name-only 78c72880..HEAD` at C5 EQUALS the NINE
     non-handoff paths of the `Change:` list, and at C6 those plus
     `.agent/handoff.md` for TEN; report the count YOU measure at each and both
     set differences, which must be EMPTY at both. 8 commits, every one
     single-parent; `git show --numstat` and `git diff --numstat` agree cell by
     cell; every commit's insertions under 500, each number reported — note
     that `--stat` may print a larger figure than `--numstat` for a whole-file
     rewrite under rename detection, and the numstat pair is what this gate
     orders. Marker sweep, LINE-ANCHORED, 0 for each of `<<<SLICE `, `<<<END `,
     `<<<FROM `, `<<<TO ` over EXACTLY these six: `.agent/plan.md`,
     `.agent/live_review.md`, `.agent/decisions.md`, `ChatInput.tsx`,
     `ActivityFeedCard.tsx` and `test_brain_stream_ring.py`. An UNANCHORED
     `<<<` count is ordered over the three `apps/` files and the contract file
     ONLY, where it must be 0 (R-0630). Reflog read BY OPERATION: every one of
     this round's rows is `commit`, with `amend`, `rebase` and `cherry` 0 each
     in that field. `gh pr list --state open` reported verbatim.

<<<SLICE PLANF021R36
# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210. `.agent/live_review.md` is the source of truth for
the open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps event kinds to plain lines, a NowCard shows the newest ACTION-class
event with a recency dot, and feed rows carry their seq and click-jump to their
node. DONE when the catalog covers the kind set DECISION F021 D3 rules and an
unknown kind renders an honest generic line rather than vanishing, the feed
renders fixture streams per the binding CSS, jump-to-node focuses the right
node, and the steering input renders DISABLED with its tooltip until F030.

## Current Step
R36 records R35 and builds the LAST unbuilt item of this feature. The steering
input ships as `components/panels/ChatInput.tsx`, the file component_spec.md
names, rendered VISIBLE and DISABLED in BOTH branches of the activity card with
the sentence ux_spec.md §11.3 binds — announced through `aria-describedby` and
not only through a tooltip a keyboard reader never sees. DECISION F021 D11
records which of two conflicting wordings ships and why. After this round every
item of T001, T002 and T003 is built.

## Next Steps
1. The integration-gate round: the whole suite at the branch tip, the feature
   file's Goal & Done read clause by clause against what is on disk.
2. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- A source contract sees the text of a call, never its effect. Nothing here
  proves the disabled input REMAINS inert at runtime; it proves the two
  `disabled` attributes and the announced reason are in the source.
- A worktree has no `node_modules`, so neither `tsc` nor a full vitest run can
  be dry-run there. The primary checkout is the only honest place for both.
- `npm run lint` is RED tree-wide at every commit under R-0622, still open.
- No code defect of F021 is open. R-0364, R-0369, R-0402, R-0403, R-0419,
  R-0439, R-0587, R-0607 through R-0609, R-0611, R-0613, R-0618, R-0622,
  R-0629, R-0630, R-0644, R-0651, R-0653 through R-0659 and R-0661 stay routed
  to a paydown branch.
<<<END PLANF021R36

<<<SLICE RECORD36
Recurrence: R-0439 — A PER-LINE UNIQUENESS COUNT WAS ORDERED OVER LINES THAT CANNOT BE UNIQUELY COUNTED, THIS TIME OVER CODE. Second instance, in the reviewer's own F021 R35 block, found by the WORKER while proving G4. NO NEW ID IS MINTED: R-0439 already rules the class, having been raised when a gate ordered a per-line count for two append-shaped pairs whose lines repeat by construction (§3 checklist item 30). THE INSTANCE: G4 of the R35 block ordered, for all seven pairs, that "each TO-only line appears exactly once" over the lines C3's diff adds. TWO of the fifty distinct TO-only lines are structural repeats that no correct application can avoid — `}) {` closes BOTH LIVEFEEDPAIR's and CARDSIGPAIR's rewritten signature, and `        );` closes both the `const body = (` and the ternary INSIDE ROWSPAIR's own TO. The clause is therefore red as written against a perfectly applied round. WHAT THE WORKER DID INSTEAD IS THE FIX AND IS NOW THE RULE: it measured the MULTISET of C3's 52 added lines against the multiset of the 52 TO-only lines and found them EQUAL, and then replayed all seven pairs against the three base blobs and reproduced the three committed blobs BYTE FOR BYTE. Ordered equality is a strictly stronger property than per-line uniqueness and it is immune to a repeated line, so the R36 block's constraint 8 forbids the per-line count outright and its G4 orders the replay.

Recurrence: R-0402 — A BLOCK STATED THE COUNT OF ITS OWN ENUMERATION AND CONTRADICTED ITSELF WITHIN ONE SENTENCE, IN THE BLOCK THAT RECORDS R-0402'S SECOND INSTANCE. Third instance, and the most instructive of the three, in the reviewer's own F021 R35 block; found by the WORKER. NO NEW ID IS MINTED. THE INSTANCE: the R35 `Change:` section opens "it names EIGHT paths, of which SEVEN are not the handoff" and closes, of the same list, "That is NINE entries and EIGHT non-handoff paths". The closing clause is correct — the list holds nine entries and eight non-handoff paths — so a block written expressly to correct a path miscount shipped the same miscount in its opening clause and the right figure in its closing one. G8 then inherited the wrong numeral twice. Constraint 9 of that block repeated the shape a third time, saying "Four pairs edit ActivityFeedCard.tsx" and then naming five. THE CAUSE IS THE ONE R-0486 NAMES AND R-0402 DOES NOT: the correcting sentence was added to a paragraph that already carried the old count, and only one of the two was re-measured. THE LOAD-BEARING HALVES SURVIVED EVERY TIME — the gate compares SETS and the worker applied the five pairs it measured rather than the four I claimed — which is exactly why this class keeps recurring: it never costs a round, so nothing forces the habit. THE COUNTER-MEASURE APPLIED IN THE R36 BLOCK: its `Change:` sentence states one count once, and its G8 orders the worker to report the number IT measures at both readings rather than to confirm mine.

Gate: R36 — the R35 entry. R35 PASSED ON EVERY GATE WHOSE SUBJECT IS THE WORK, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER, AND ALL THREE OF ITS DECLARED DEVIATIONS ARE THE REVIEWER'S OWN BLOCK DEFECTS, TWO OF THEM RECORDED ABOVE. R35 IS THE ROUND THAT FINISHED T003'S CLICK-JUMP: a feed row that resolves to a graph node now renders as a BUTTON that emits `onSelectNode`, a row that resolves to nothing stays the `<article>` it always was, `RightLivePanel` hands the card the task list and the focus callback the checklist beside it already used, and `.activityItemJump` strips the button chrome using NO custom property at all, deliberately, so that R-0661's class cannot recur through this round's own CSS. THE CONTRACT IS THE PART WORTH KEEPING AND IT WAS VACUOUS IN ITS FIRST DRAFT: the reviewer's own assertion searched the WHOLE panel file for `tasks={dashboard.tasks}`, which the `TaskChecklistCard` line one row below has carried since long before F021, so it passed at a base where the feed got nothing. The mutation caught it, the shipped assertion reads the `<ActivityFeedCard` LINE alone, and G6 proved it can fail: `1 failed, 61 passed`, the sole failure being the panel test. RE-MEASURED GATES: `tests/ui_contracts/` 490 passed and 4 skipped against 486 and 4 at the base, the difference being the contract's four tests; `npm run test:unit` 16 files and 218 tests, UNCHANGED, as a round adding no `.test.ts` must be; `npx tsc --noEmit` exit 0 with EMPTY output; all four state readers 528; the canary 42. THE LEDGER held at 224 under `^- R-\d+ — `, all distinct, maximum R-0661. STRUCTURE: seven commits, every one single-parent, insertions 399, 316, 20, 4, 52, 49 and 85, each under 500. C5's own three readings are `78c72880`, +85/-73, and 127 lines, over the 100-line tier with the cause declared. ONE STANDING NOTE THE WORKER RAISED AND THE REVIEWER CONFIRMED: a pair's FROM uniqueness is a PER-TARGET property, and IMPORTPAIR's FROM occurs verbatim in three files under `apps/ui/src`. Nothing went wrong because the applier resolved by target file; a target-blind applier would have corrupted `RightLivePanel.tsx`, and R36's constraint 10 says so where the next worker will read it.
<<<END RECORD36

<<<SLICE DECISIOND11
## DECISION F021 D11 (2026-08-22) — the disabled steering input ships the design reference's sentence, not the feature file's paraphrase

CONTEXT, measured at `78c72880`: two binding-looking documents give this one tooltip two different texts. `docs/ui/design_reference/ux_spec.md` §11.3 specifies the activity card's input as "DISABLED until steering exists (tooltip: "Steering arrives with a later feature — watching only for now.")". `docs/roadmap/features/T5_F021.md` says instead: 'Steering input: rendered, disabled, tooltip "steering lands with F030"'. Both want an honest disabled control; they disagree on the words a user reads.

CHOSEN: the ux_spec sentence ships verbatim, as the constant `STEERING_DISABLED_REASON` in `ActivityFeedCard.tsx`. `.agent/context.md` states the precedence this feature works under — "docs/ui/design_reference/ is binding for every visual surface" — and a tooltip is a visual surface. The feature file's own Goal states the requirement as "the steering input renders DISABLED with the honest tooltip until its backing feature exists", which is a property and not a string; its quoted phrase reads as a paraphrase of that property rather than as competing copy. The reference sentence is also the better one for the reader it addresses: it says what will happen and what is happening now, and it does not make a user decode a roadmap id.

ALTERNATIVES CONSIDERED. Ship the feature file's phrase: rejected, it inverts the stated precedence and would put the shipped surface at odds with the document the round is gated against. Merge both, naming F030 inside the reference sentence: rejected, it edits binding copy to carry an internal identifier, which is the same category error as the first. Ship neither and hide the input until F030: rejected outright, because ux_spec §11.3 places the control on this surface and the feature file's own brief calls for "visible honesty over hidden UI".

REVERSE IT by changing the constant and the contract's `REASON` together; they are asserted equal, so neither can drift alone.
<<<END DECISIOND11

<<<SLICE CHATINPUT
import styles from "./RightLivePanel.module.css";

/** The steering input, rendered but DISABLED until its backing feature exists.
 *
 *  Remedy deliberately ships this VISIBLE AND INERT rather than hiding it.
 *  ux_spec.md §11.3 places it at the bottom of the activity card, and the
 *  design reference's rule for a not-yet feature is visible honesty over
 *  hidden UI: a reader who can see the box and read why it is off learns
 *  something a missing box would have hidden.
 *
 *  `onSend` is declared and deliberately NOT destructured. component_spec.md
 *  ("SteeringInput / ChatInput") fixes the props so that enabling this later
 *  is a change here and not at every call site, but this component cannot
 *  honestly call a handler while it has no text to send — it holds no state,
 *  because a disabled input has nothing to hold. F030 adds the state and the
 *  call together; `noUnusedLocals` is why the binding is absent rather than
 *  unused. */
export function ChatInput({ disabled, reason }: {
  disabled: boolean;
  reason: string;
  onSend?: (text: string) => void;
}) {
  return (
    <div className={styles.chatInputRow}>
      <input
        className={styles.chatInput}
        type="text"
        placeholder="Ask something…"
        disabled={disabled}
        title={disabled ? reason : undefined}
        aria-describedby={disabled ? "remedy-chat-input-reason" : undefined}
      />
      <button
        type="button"
        className={styles.chatSend}
        disabled={disabled}
        title={disabled ? reason : undefined}
        aria-label="Send"
      >
        ↑
      </button>
      {disabled ? (
        <p id="remedy-chat-input-reason" className={styles.chatInputReason}>{reason}</p>
      ) : null}
    </div>
  );
}
<<<END CHATINPUT

<<<FROM CHATIMPORTPAIR
import { BuilderGlyph, ReviewerGlyph, PersonGlyph, GearGlyph } from "../icons/RemedyGlyphs";
<<<TO CHATIMPORTPAIR
import { BuilderGlyph, ReviewerGlyph, PersonGlyph, GearGlyph } from "../icons/RemedyGlyphs";
import { ChatInput } from "./ChatInput";
<<<END CHATIMPORTPAIR

<<<FROM REASONPAIR
const LIVE_ROWS_SHOWN = 40;
<<<TO REASONPAIR
const LIVE_ROWS_SHOWN = 40;

/** The disabled steering input's honest reason, quoted from ux_spec.md
 *  §11.3, which is binding for this surface. DECISION F021 D11 records why
 *  this wording rather than the feature file's shorter paraphrase. */
const STEERING_DISABLED_REASON =
  "Steering arrives with a later feature — watching only for now.";
<<<END REASONPAIR

<<<FROM LIVEBRANCHPAIR
        <LiveFeed recent={live} recentDropped={recentDropped ?? 0}
          tasks={tasks ?? []} onSelectNode={onSelectNode ?? (() => {})} />
      </section>
<<<TO LIVEBRANCHPAIR
        <LiveFeed recent={live} recentDropped={recentDropped ?? 0}
          tasks={tasks ?? []} onSelectNode={onSelectNode ?? (() => {})} />
        <ChatInput disabled reason={STEERING_DISABLED_REASON} />
      </section>
<<<END LIVEBRANCHPAIR

<<<FROM FALLBACKBRANCHPAIR
          <p className={styles.emptyState}>No activity yet. Events will appear here as the agent works.</p>
        )}
      </div>
    </section>
<<<TO FALLBACKBRANCHPAIR
          <p className={styles.emptyState}>No activity yet. Events will appear here as the agent works.</p>
        )}
      </div>
      <ChatInput disabled reason={STEERING_DISABLED_REASON} />
    </section>
<<<END FALLBACKBRANCHPAIR

<<<FROM CHATCSSPAIR
.activityItemJump:hover { background: rgba(76, 131, 255, 0.06); border-radius: 8px; }
<<<TO CHATCSSPAIR
.activityItemJump:hover { background: rgba(76, 131, 255, 0.06); border-radius: 8px; }
/* The steering input (ux_spec.md §11.3): 40px field, radius 12, bg-2 fill,
   1px line border, 36px send button. Every custom property named here is
   defined in the shipped tokens sheet — checked, because an unresolved one
   renders nothing and only R-0661's pin would ever notice. */
.chatInputRow { display: flex; gap: 8px; align-items: center; margin-top: 12px; flex-wrap: wrap; }
.chatInput { flex: 1; min-width: 0; height: 40px; border-radius: 12px;
  background: var(--remedy-bg-2); border: 1px solid var(--remedy-line);
  padding: 0 14px; font: 500 13px/1.45 var(--remedy-font-ui); color: var(--remedy-ink); }
.chatInput:disabled { cursor: not-allowed; }
.chatSend { width: 36px; height: 36px; border-radius: 12px; border: 0;
  background: var(--remedy-blue); color: #fff; font-size: 15px; cursor: pointer; }
.chatSend:disabled { cursor: not-allowed; opacity: 0.5; }
.chatInputReason { flex-basis: 100%; margin: 0; font-size: 11px; color: var(--remedy-ink-soft); }
<<<END CHATCSSPAIR

<<<FROM CHATCONSTPAIR
CARD = UI_SRC / "components" / "panels" / "ActivityFeedCard.tsx"
<<<TO CHATCONSTPAIR
CARD = UI_SRC / "components" / "panels" / "ActivityFeedCard.tsx"
CHAT_INPUT = UI_SRC / "components" / "panels" / "ChatInput.tsx"
<<<END CHATCONSTPAIR

<<<SLICE CONTRACTSLICE36
class TestTheSteeringInputIsHonestlyDisabled:
    """The steering input ships VISIBLE and INERT until F030 gives it a back
    end. ux_spec.md §11.3 is binding for this surface and fixes both the
    placement and the sentence; DECISION F021 D11 records why that wording
    rather than the feature file's shorter paraphrase."""

    REASON = "Steering arrives with a later feature — watching only for now."

    def test_the_component_exists_where_the_spec_puts_it(self):
        assert CHAT_INPUT.exists(), (
            "component_spec.md names components/panels/ChatInput.tsx so that "
            "enabling steering later is a change in one file"
        )

    def test_the_input_and_its_button_are_both_disabled(self):
        code = strip_ts_comments(CHAT_INPUT.read_text())
        # Two controls, so two disabled attributes: an enabled send button
        # beside a dead field would still promise something it cannot do.
        assert code.count("disabled={disabled}") == 2, (
            "the field and the send button are both inert until F030"
        )

    def test_the_reason_is_the_binding_sentence(self):
        card = strip_ts_comments(CARD.read_text())
        assert self.REASON in card, (
            "ux_spec.md §11.3 fixes this sentence; a paraphrase would make the "
            "design reference and the shipped surface disagree"
        )

    def test_the_reason_reaches_the_reader_and_not_only_the_tooltip(self):
        code = strip_ts_comments(CHAT_INPUT.read_text())
        # A title attribute alone is invisible to a keyboard or screen-reader
        # user, which is the reader most likely to wonder why nothing happens.
        assert "aria-describedby" in code, (
            "the honest reason is announced, not only hovered"
        )

    def test_the_card_renders_it(self):
        card = strip_ts_comments(CARD.read_text())
        # Both branches: the live feed and the pre-stream fallback. A reader
        # who has not started a job must see the same honest surface.
        assert card.count("<ChatInput disabled") == 2, (
            "the input belongs to the card, not to one of its two branches"
        )
<<<END CONTRACTSLICE36
