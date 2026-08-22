── STEP FEED WIRING — F021 ──
Goal:        Record R34, which PASSED, and wire the resolver R34 landed: a feed
             row that resolves to a graph node renders as a button and emits
             `onSelectNode`, a row that does not stays the article it always
             was, and a `tests/ui_contracts/` source contract pins that the
             COMPONENT really calls the rule — the half no vitest run can see.
             This completes T003's click-jump. ONE correction is appended
             naming OPEN finding R-0402; it mints no id and it is the
             REVIEWER's own defect in the R34 block.

Fortschritt: ~99 % (T003 Klick-Sprung fertig nach dieser Runde; es fehlt nur
             noch der deaktivierte Steuer-Eingang)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R34 verdict
             and the one correction · C3 the component, the panel and the CSS ·
             C4 the source contract · C5 handback.

Change:      Exactly these paths, and nothing else. I have COUNTED this list
             rather than describing it: it names EIGHT paths, of which SEVEN
             are not the handoff — `.agent/authored/f021-r35.md` (NEW, C0a) ·
             `.agent/last_block.md` (C0b) · `.agent/plan.md` (C1) ·
             `.agent/live_review.md` (C2) ·
             `apps/ui/src/components/panels/ActivityFeedCard.tsx` (C3) ·
             `apps/ui/src/components/panels/RightLivePanel.tsx` (C3) ·
             `apps/ui/src/components/panels/RightLivePanel.module.css` (C3) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C4) ·
             `.agent/handoff.md` (C5). That is NINE entries and EIGHT
             non-handoff paths — the miscount of exactly this sentence in the
             R34 block is the correction C2 records, so resolve every path
             count in this block against the list above and report the number
             YOU count.

Constraints:
 1. Apply every slice and pair half BYTE FOR BYTE. Never retype, rewrap,
    reflow, reindent or whitespace-adjust one. If a slice looks wrong, STOP and
    say so in the handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. C1
    precedes the ledger commit (§3 checklist item 23). C3 lands the wiring
    BEFORE C4 pins it, so C4's contract is green the moment it exists. ROUND
    BASE is `83a03ba1` — resolve its full form with `git rev-parse`.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. Before it, in
    `.agent/live_review.md`: 224 registered under the canonical pattern
    `^- R-\d+ — `, maximum R-0661, `Done: R-` 1. After C2: still 224, still all
    DISTINCT, still maximum R-0661, `Done: R-` still 1. The correction names an
    OPEN finding rather than a new id (§3 checklist item 30), and
    `^- R-0402 — ` stays at exactly 1 across C2.
 4. NO PARAGRAPH OF RECORD35 BEGINS WITH THE BYTES `- R-`. One opens
    `Recurrence: ` and the verdict opens `Gate: R35 — `. G5 measures this. The
    two paragraphs are separated by EXACTLY ONE BLANK LINE.
 5. THE APPEND CONVENTION IS STATED PER TARGET FILE, because the two append
    targets differ and R31 lost a deviation to assuming they were the same.
      `.agent/live_review.md` at C2: EXACTLY ONE ADDED NEWLINE, then RECORD35,
      then one terminator, so the join carries EXACTLY ONE BLANK LINE.
      `tests/ui_contracts/test_brain_stream_ring.py` at C4: EXACTLY TWO ADDED
      NEWLINES, then CONTRACTSLICE, then one terminator, so the join carries
      EXACTLY TWO BLANK LINES — PEP 8 E302. `ruff` CANNOT see this rule, since
      E301-E306 are preview-only, so it is met by construction here or not at
      all. NOTE, measured and NOT to be repaired: that file already carries ONE
      top-level class with a single blank line above it,
      `TestTheFeedScrollRuleIsWiredToTheCard`, landed at R31. It is not this
      round's to fix and no gate below counts it.
    A WHOLE-FILE write (PLANF021R35) is the slice PLUS one terminator.
 6. THE LEDGER IS APPEND-ONLY. No landed paragraph, `Gate:` entry or
    `Recurrence:` entry is edited.
 7. NO COUNT GATE IN THIS BLOCK COUNTS A STRING WHOSE NUMBER THIS BLOCK'S OWN
    SLICES CHANGE, AND EVERY LEDGER COUNT NAMES THE PATTERN IT IS READ UNDER,
    ANCHORED. An UNANCHORED count is never ordered over `.agent/live_review.md`
    (R-0630, recorded twice already).
 8. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide at every commit under R-0622 and is NOT a gate of this round
    — do not run it and do not report it. Create and merge NO pull request.
    Push the branch after C5. ONE worktree under `.remedy-wt/` is ordered, for
    G6's red-proof alone; remove it and prove the tree clean afterwards.
 9. THE SEVEN PAIRS AND THEIR SHAPES, ALL MEASURED BY MY SCRIPT AND NOT ONE OF
    THEM ASSERTED. Each FROM occurs EXACTLY ONCE in its target at the round
    base. FIVE are NOT append-shaped — LIVEFEEDPAIR, ROWSPAIR, CARDSIGPAIR,
    LIVEFEEDUSEPAIR, PANELPAIR — and their FROM-zero count IS owed at C3. TWO
    ARE APPEND-SHAPED, IMPORTPAIR and CSSPAIR, because each TO opens with its
    own FROM; §4.9 therefore FORBIDS ordering a FROM-zero for them and G4 orders
    the append obligation instead. Four pairs edit ActivityFeedCard.tsx; apply
    them in the order IMPORTPAIR, LIVEFEEDPAIR, ROWSPAIR, CARDSIGPAIR,
    LIVEFEEDUSEPAIR, and none overlaps another.
10. WHAT I DRY-RAN AND WHAT I COULD NOT. In a worktree at `83a03ba1` I applied
    all seven pairs and the contract slice and measured: `tests/ui_contracts/`
    green; the contract file 62 passed; and the RED-PROOF G6 orders, which
    printed `1 failed, 61 passed`. I could NOT run `tsc` in a worktree — it has
    no `node_modules` and a symlink is denied to this session — so THE WORKER'S
    `tsc` RUN IN THE PRIMARY CHECKOUT IS THE FIRST HONEST EXECUTION OF THAT
    GATE. If it is red, STOP and report; a type error there is my defect.
11. WHY G6 MUTATES THE PANEL AND NOT THE CARD, stated because the first version
    of this contract was VACUOUS and I caught it only by running the mutation.
    `RightLivePanel.tsx` renders `TaskChecklistCard` one line below
    `ActivityFeedCard`, and that line has carried BOTH `tasks={dashboard.tasks}`
    and `onSelectNode={onSelectNode}` since long before F021. A file-wide
    substring search for either therefore passes at a base where the FEED gets
    neither. The shipped assertion reads the `<ActivityFeedCard` LINE alone,
    which is what makes G6 able to fail at all.
12. Block size, measured on these final bytes AFTER the last edit: TOTAL 399
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice and
    pair CONTENT lines — 227 against DECISION F085 D5's 400. Markers count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C5; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2, C3 and C4. C5's own reading
     is ordered NOWHERE — §3 item 31 leaves it to the next session.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r35.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over my
     emitted copy at `.remedy-wt/f021-r35.md` are all equal. Write C0b FROM the
     committed C0a blob. Report the digest, bytes and lines. Then extract the
     slices and pairs from the COMMITTED C0a blob by their marker LINES,
     `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO `, and report how many whole
     texts, how many pairs and how many CONTENT lines your extractor printed —
     each a number YOU measured — re-measuring constraint 12's two numerals
     from that same blob against their caps.
 G3  `.agent/plan.md` at C1 equals PLANF021R35 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare
     slice that must exit 1. Report both exit codes, that the last byte is a
     newline, `^## Goal$` 1 and `^## Next Steps$` 1, and the `wc -l` YOU
     measure against AGENTS.md's "keep it short (<50 lines)". If that count is
     50 or more, STOP and report — do NOT trim the file to reach it (R-0654).
 G4  THE SEVEN PAIRS AT C3, read against constraint 9's measured shapes. For
     LIVEFEEDPAIR, ROWSPAIR, CARDSIGPAIR, LIVEFEEDUSEPAIR and PANELPAIR report
     the FROM at EXACTLY 1x at the round base and EXACTLY 0x at C3. For
     IMPORTPAIR and CSSPAIR report the FROM at EXACTLY 1x at the base AND
     EXACTLY 1x at C3 — they are append-shaped and the zero is NOT owed. For
     all seven report, over the lines C3's diff ADDS, that each TO-only line
     appears exactly once (§4.9). Report also `nodeIdForFeedRow` occurring 0x
     in `ActivityFeedCard.tsx` at the base and a number YOU count at C3, and
     `.activityItemJump` 0x at the base in the CSS and a number YOU count at
     C3.
 G5  THE LEDGER, at C2, every count naming its pattern, base then C2:
     canonical `^- R-\d+ — ` 224 then 224, ALL DISTINCT at both, maximum
     R-0661 at both; loose `^- R-` 225 then 225, gap 1 at both; `^Done: R-` 1
     then 1; `^Gate: R` 33 then 34, DISTINCT at both; `^Gate: R35` 0 then 1;
     `^Recurrence: ` 10 then 11; `^Recurrence: R-0402 — ` 0 then 1;
     `^- R-0402 — ` 1 then 1. Report that the number of RECORD35 paragraphs
     opening with the bytes `- R-` is 0, and that the base blob is a byte-exact
     PREFIX of the C2 blob whose remainder is EXACTLY one newline plus RECORD35
     plus one newline.
 G6  THE RED-PROOF, in a disposable worktree at C4 under `.remedy-wt/`, never
     in the primary checkout. There, in `RightLivePanel.tsx`, replace the whole
     `<ActivityFeedCard ... />` element with the form it had at the round base
     — that is, DELETE ` tasks={dashboard.tasks} onSelectNode={onSelectNode}`
     from that ONE line, leaving `TaskChecklistCard` untouched — and run
     `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf`.
     Report the failure count and the failing node id, which MUST be
     `TestAFeedRowJumpsToItsNode::test_the_panel_hands_the_card_what_the_rule_
     needs`. I measured `1 failed, 61 passed`. Constraint 11 says why this
     mutation and not another. Then remove the worktree and report
     `git status --porcelain` at 0 lines and `git worktree list` naming the
     primary checkout alone.
 G7  THE SUITES, SERIAL, in the PRIMARY checkout, never two at once. Count by
     PASSED PLUS SKIPPED, which `.agent/context.md` requires.
     `python3 -m pytest tests/ui_contracts/ -q -rf` — I measured 486 passed and
     4 skipped at the round base, so 490; C4 adds CONTRACTSLICE's FOUR tests
     and I expect 490 passed and 4 skipped, but report the numbers YOU measure
     and the difference. `npm run test:unit` from `apps/ui` — 16 files and 218
     tests at the base, and this round adds no `.test.ts`, so the SAME numbers
     are expected; a change here is a finding, not a pass. `npx tsc --noEmit`
     from `apps/ui` — exit 0 and EMPTY output; see constraint 10 first. Then,
     because this round rewrites `.agent/` state, ALL FOUR state readers:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py -q -rf` — 528 at the base. Then
     the canary, `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — 42
     at the base. No ruff gate is ordered for the `apps/` files, which are not
     Python; DO run `python3 -m ruff check tests/ui_contracts/test_brain_stream_
     ring.py`, which I measured GREEN at the round base, so exit 0 is honest.
 G8  STRUCTURE. `git diff --name-only 83a03ba1..HEAD` at C4 EQUALS the SEVEN
     non-handoff paths of the `Change:` list, both set differences reported
     EMPTY; at C5 it is those seven plus `.agent/handoff.md` for EIGHT, and
     BOTH readings are reported because no single commit shows both. Report the
     path count YOU measure at each. 7 commits, every one single-parent;
     `git show --numstat` and `git diff --numstat` agree cell by cell; every
     commit's insertions under 500, each number reported, and note that
     `--stat` may print a larger figure for a whole-file rewrite under rename
     detection — the numstat pair is what this gate orders. Marker sweep,
     LINE-ANCHORED, 0 for each of `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO `
     over EXACTLY these five: `.agent/plan.md`, `.agent/live_review.md`,
     `ActivityFeedCard.tsx`, `RightLivePanel.module.css` and
     `test_brain_stream_ring.py`. An UNANCHORED `<<<` count is ordered over the
     three `apps/` files and the contract file ONLY, where it must be 0, and is
     NOT ordered over `.agent/live_review.md` (R-0630). Reflog read BY
     OPERATION: every one of this round's rows is `commit`, with `amend`,
     `rebase` and `cherry` 0 each in that field. `gh pr list --state open`
     reported verbatim.

<<<SLICE PLANF021R35
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
R35 records R34 and finishes T003's click-jump by wiring the resolver R34
landed. `ActivityFeedCard` renders a row that resolves to a node as a BUTTON
that emits `onSelectNode`, and a row that resolves to nothing as the article it
always was, so the affordance never claims a jump the row cannot make.
`RightLivePanel` hands the card the task list and the focus callback the
checklist beside it already uses. A `tests/ui_contracts/` source contract pins
that the component really calls the rule — the half no vitest run can see, and
the half that was missing while `feedScroll.ts` sat unimported for fourteen
rounds. One correction is appended against OPEN finding R-0402.

## Next Steps
1. R36: the steering input, rendered DISABLED with the tooltip naming F030 —
   the last unbuilt item of T003 and of the feature.
2. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- A source contract can only see the text of a call, never its effect. This one
  asserts against COMMENT-STRIPPED source (R-0584) and reads the
  `<ActivityFeedCard` line rather than the whole panel file, because the
  TaskChecklistCard line beside it carries the same two props.
- A worktree has no `node_modules`, so neither `tsc` nor a full vitest run can
  be dry-run there. The primary checkout is the only honest place for both.
- `npm run lint` is RED tree-wide at every commit under R-0622, still open.
- No code defect of F021 is open. R-0364, R-0369, R-0402, R-0403, R-0419,
  R-0587, R-0607 through R-0609, R-0611, R-0613, R-0618, R-0622, R-0629,
  R-0630, R-0644, R-0651, R-0653 through R-0659 and R-0661 stay routed to a
  paydown branch.
<<<END PLANF021R35

<<<SLICE RECORD35
Recurrence: R-0402 — A BLOCK STATED THE COUNT OF ITS OWN ENUMERATION AND THE ENUMERATION CONTRADICTS IT. Second instance, in the reviewer's own F021 R34 block, found by the WORKER and confirmed by the reviewer against the block's committed bytes. NO NEW ID IS MINTED: R-0402 already rules the class, having been raised when an R19 block "twice stated a COUNT of its own enumerations and both counts were wrong" (§3 checklist item 30). THE INSTANCE: G8 of the R34 block ordered `git diff --name-only a14f0294..HEAD` to equal "the seven non-handoff `Change:` paths". That block's `Change:` section names NINE paths, of which EIGHT are not the handoff — `.agent/authored/f021-r34.md`, `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`, `apps/ui/src/api/feedRow.ts`, `apps/ui/src/api/feedFocus.ts`, `apps/ui/src/api/feedFocus.test.ts` and `apps/ui/src/api/actionClass.test.ts` — so the numeral is short by one. THE LOAD-BEARING HALF OF THE GATE WAS UNHARMED and the worker reported it correctly: the clause that matters is the two SET DIFFERENCES, both of which it measured EMPTY at C3 and at C4, and a set comparison does not consult the cardinality the prose guessed. THE CAUSE IS THE ONE R-0402 NAMES: the numeral was written while the list was still being drafted and was never re-counted after the last path went in — `actionClass.test.ts` was added to that block LATE, for the typechecking reason constraint 3 of the same block explains at length. THE COUNTER-MEASURE, applied in the R35 block rather than owed: its `Change:` section states the count and the reading it was counted under IN THE SAME SENTENCE as the list, and its G8 orders the worker to report the number IT counts rather than to confirm mine.

Gate: R35 — the R34 entry. R34 PASSED ON EVERY GATE WHOSE SUBJECT IS THE WORK, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND ITS ONE SUBSTANTIVE DEVIATION IS THE REVIEWER'S OWN DEFECT, RECORDED IN THE ENTRY ABOVE. R34 IS THE ROUND THAT GAVE THE CLIENT THE LINKAGE R33 PUT ON THE WIRE: `FeedRow` gained `taskId` from the envelope, and `apps/ui/src/api/feedFocus.ts` — 36 lines, NEW — resolves a row to a graph node through the task list the dashboard already carries, which is the resolution DECISION F021 D2 ruled and not the seq-or-timestamp match it rejected. `actionClass.test.ts` rode along for a reason the reviewer verified by grepping every construction site of `FeedRow` before authoring: `rowOf` there returns one under an explicit return-type annotation, so a required new field stops that file typechecking, and the three files are one typechecking unit. RE-MEASURED GATES: `npm run test:unit` 16 files and 218 tests against 15 and 212 at the base, the difference being FEEDFOCUSTEST's six; `npx tsc --noEmit` exit 0 with EMPTY output, its first honest execution, since a worktree has no `node_modules` and the reviewer said so in the block rather than claiming a dry run it never had; all four state readers 528; `tests/ui_contracts/` 486 passed and 4 skipped; the canary 42. BOTH NEW FILES ARE BYTE-IDENTICAL TO THEIR SLICES, verified by the reviewer as slice-plus-one-newline rather than by reading the handback's `cmp` exit codes. THE RED-PROOF WAS REAL: mutating `owner.nodeId` to `owner.id` — the single confusion the module exists to prevent — printed `2 failed | 4 passed`, and the failures include the test whose name says the resolver never assumes the two are equal. THE LEDGER held at 224 under `^- R-\d+ — `, all distinct, maximum R-0661, and `^Recurrence: R-0630 — ` moved 1 to 2 rather than 0 to 1, which is the asymmetry the R34 block measured rather than assumed. STRUCTURE: six commits, every one single-parent, insertions 358, 268, 23, 8, 84 and 69, each under 500. C4's own three readings are `83a03ba1`, +69/-69, and 115 lines, over the 100-line tier with the cause declared.
<<<END RECORD35

<<<FROM IMPORTPAIR
import type { FeedRow } from "../../api/feedRow";
<<<TO IMPORTPAIR
import type { FeedRow } from "../../api/feedRow";
import type { FocusableTask } from "../../api/feedFocus";
import { nodeIdForFeedRow } from "../../api/feedFocus";
<<<END IMPORTPAIR

<<<FROM LIVEFEEDPAIR
function LiveFeed({ recent, recentDropped }: { recent: readonly FeedRow[]; recentDropped: number }) {
<<<TO LIVEFEEDPAIR
function LiveFeed({ recent, recentDropped, tasks, onSelectNode }: {
  recent: readonly FeedRow[];
  recentDropped: number;
  tasks: readonly FocusableTask[];
  onSelectNode: (nodeId: string | null) => void;
}) {
<<<END LIVEFEEDPAIR

<<<FROM ROWSPAIR
      {newestFirst.map(row => (
        <article key={row.seq} className={styles.activityItem}>
          <div className={styles.actorIcon}><GearGlyph style={{ width: 16, height: 16, color: "white" }} /></div>
          <div>
            <div className={styles.activityMeta}>
              <strong>{row.kind || "event"}</strong>
              {row.timestamp ? <span>{row.timestamp}</span> : null}
              <span className={styles.activityTag}>#{row.seq}</span>
              {row.outcome ? <span className={styles.activityTag}>{row.outcome}</span> : null}
            </div>
            <p>{row.line}</p>
          </div>
        </article>
      ))}
<<<TO ROWSPAIR
      {newestFirst.map(row => {
        const nodeId = nodeIdForFeedRow(row, tasks);
        const body = (
          <>
            <div className={styles.actorIcon}><GearGlyph style={{ width: 16, height: 16, color: "white" }} /></div>
            <div>
              <div className={styles.activityMeta}>
                <strong>{row.kind || "event"}</strong>
                {row.timestamp ? <span>{row.timestamp}</span> : null}
                <span className={styles.activityTag}>#{row.seq}</span>
                {row.outcome ? <span className={styles.activityTag}>{row.outcome}</span> : null}
              </div>
              <p>{row.line}</p>
            </div>
          </>
        );
        // A row with no node renders as the article it always was. Only a row
        // that can really jump becomes a button, so the affordance never lies.
        return nodeId ? (
          <button key={row.seq} type="button" title="Show this task in the graph"
            className={`${styles.activityItem} ${styles.activityItemJump}`}
            onClick={() => onSelectNode(nodeId)}>
            {body}
          </button>
        ) : (
          <article key={row.seq} className={styles.activityItem}>{body}</article>
        );
      })}
<<<END ROWSPAIR

<<<FROM CARDSIGPAIR
export function ActivityFeedCard({ activity, recent, recentDropped }: { activity: RemedyActivityItem[]; recent?: readonly FeedRow[]; recentDropped?: number }) {
<<<TO CARDSIGPAIR
export function ActivityFeedCard({ activity, recent, recentDropped, tasks, onSelectNode }: {
  activity: RemedyActivityItem[];
  recent?: readonly FeedRow[];
  recentDropped?: number;
  tasks?: readonly FocusableTask[];
  onSelectNode?: (nodeId: string | null) => void;
}) {
<<<END CARDSIGPAIR

<<<FROM LIVEFEEDUSEPAIR
        <LiveFeed recent={live} recentDropped={recentDropped ?? 0} />
<<<TO LIVEFEEDUSEPAIR
        <LiveFeed recent={live} recentDropped={recentDropped ?? 0}
          tasks={tasks ?? []} onSelectNode={onSelectNode ?? (() => {})} />
<<<END LIVEFEEDUSEPAIR

<<<FROM PANELPAIR
      <ActivityFeedCard activity={dashboard.activity} recent={recent} recentDropped={recentDropped} />
<<<TO PANELPAIR
      <ActivityFeedCard activity={dashboard.activity} recent={recent} recentDropped={recentDropped} tasks={dashboard.tasks} onSelectNode={onSelectNode} />
<<<END PANELPAIR

<<<FROM CSSPAIR
.activityItem { display: flex; gap: 12px; }
<<<TO CSSPAIR
.activityItem { display: flex; gap: 12px; }
/* A feed row that can jump is a button, so it needs the button chrome
   removed before it can look like the article beside it. No custom property
   is used here on purpose: an unresolved one renders nothing and no suite in
   this repository would see it (R-0661). */
.activityItemJump { width: 100%; padding: 0; border: 0; background: none;
  font: inherit; color: inherit; text-align: left; cursor: pointer; }
.activityItemJump:hover { background: rgba(76, 131, 255, 0.06); border-radius: 8px; }
<<<END CSSPAIR

<<<SLICE CONTRACTSLICE
class TestAFeedRowJumpsToItsNode:
    """T003's click-jump, gated by source because there is no DOM here.

    The rule itself is `nodeIdForFeedRow` and has its own vitest neighbour.
    What no vitest run can see is whether the COMPONENT calls it, which is the
    half that was missing when `feedScroll.ts` sat pure, tested and imported by
    nothing for fourteen rounds."""

    def test_the_card_resolves_a_row_through_the_rule(self):
        code = strip_ts_comments(CARD.read_text())
        assert "nodeIdForFeedRow(row, tasks)" in code, (
            "the row must be resolved by the shared rule, not by a second "
            "mapping the component invents (DECISION F021 D2)"
        )

    def test_only_a_resolvable_row_becomes_a_button(self):
        code = strip_ts_comments(CARD.read_text())
        assert "onClick={() => onSelectNode(nodeId)}" in code, (
            "a clickable row emits focus for the node it resolved"
        )
        # The conditional is the honesty: a row that cannot jump must not
        # render an affordance that says it can.
        assert "return nodeId ? (" in code, (
            "a row with no linkage stays the article it always was"
        )

    def test_the_panel_hands_the_card_what_the_rule_needs(self):
        # Anchored to the ActivityFeedCard ELEMENT, never to the file: the
        # TaskChecklistCard line beside it has carried both of these props
        # since long before F021, so a file-wide search would pass at a base
        # where the feed gets neither.
        panel = strip_ts_comments(PANEL.read_text())
        element = [l for l in panel.splitlines() if "<ActivityFeedCard" in l]
        assert len(element) == 1, "expected exactly one ActivityFeedCard element"
        assert "tasks={dashboard.tasks}" in element[0], (
            "the resolution reads the task list the dashboard already carries"
        )
        assert "onSelectNode={onSelectNode}" in element[0], (
            "the feed focuses the same graph store the checklist already does"
        )

    def test_the_jump_row_has_its_button_reset(self):
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert ".activityItemJump" in css, (
            "a button carrying a row needs its chrome removed or the feed "
            "renders two visually different kinds of row"
        )
<<<END CONTRACTSLICE
