── STEP FEED — F021 ──
Goal:        Make the activity feed LIVE. The ring published on
             `BrainStreamView` at R13 travels down the props the shell already
             passes — one `useBrainStream` call, no second `EventSource` — and
             `ActivityFeedCard` renders those rows, newest first, with the
             dropped-rows notice `recentDropped` earns. No new CSS class, no
             new asset, no new font or glyph: every class the new markup uses
             already exists in `RightLivePanel.module.css`. The round also
             records the R13 verdict, which was PASS.

Fortschritt: ~70 % (T002 fertig — der Stream erreicht jetzt wirklich die
             Oberflaeche: Ring, View, Props und Feed haengen zusammen; es
             fehlen NowCard-Verfeinerung, Scroll-Disziplin und T003)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R13 verdict
             · C3 the live feed and its contract · C4 the handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r14.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/components/panels/ActivityFeedCard.tsx` (C3) ·
             `apps/ui/src/components/panels/RightLivePanel.tsx` (C3) ·
             `apps/ui/src/components/shell/RemedyShell.tsx` (C3) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C3) ·
             `.agent/handoff.md` (C4).
             Resolve any count in this block against that list.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). ROUND BASE is `9fcce96de76740dc21953d68214ec7a171a40b5f` and is
    the commit every "round base" in this block names.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. R13 passed every gate
    under the reviewer's own re-measurement, so RECORD13 registers nothing and
    writes no `Done:`/`Landed:` line. 213 open, max R-0650, next free R-0651.
    Two defects R13 surfaced are recorded in RECORD13 AGAINST OPEN FINDINGS —
    R-0613 and R-0639 — rather than under new ids, because §3 checklist item 30
    requires the open set to be searched for the DEFECT first and both searches
    returned a hit. Both defects are the reviewer's own block text.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice is quoted WITHOUT a
    trailing newline. A WHOLE-FILE replacement (PLANF021R14) is the slice PLUS
    one terminator. An APPEND (RECORD13, CONTRACTFEED) is one newline, then the
    slice, then one terminator, so the target keeps exactly one. A FROM/TO PAIR
    substitutes in place, neither side carrying a terminator and the file's own
    untouched. The gates match each kind.
 5. PAIRS BEFORE APPENDS, READ PER TARGET FILE (R-0639, and the imprecision R13
    surfaced). Within any ONE file, every pair is applied before any append to
    that same file — that is the whole of the rule, because a pair can only be
    disturbed by an append to the file it matches in. Across files the order is
    the commit order of constraint 2, which is why RECORD13's append at C2
    precedes C3's pairs and no contradiction arises. ONE file takes both a pair
    and an append: `tests/ui_contracts/test_brain_stream_ring.py` takes
    CONTRACTPATHS first and CONTRACTFEED second, in that order. No pair touches
    `.agent/live_review.md`.
 6. THE ARCHITECTURE LINE IS THE POINT. The rows reach the card by being passed
    DOWN from the single `useBrainStream` call `RemedyShell` already makes. Do
    not add a second call, do not add a hook, and do not construct an
    `EventSource` anywhere outside `apps/ui/src/api/brainStreamDeps.ts`. Do not
    edit `brainStream.ts` or `brainStreamRunner.ts`; R12 and R13 built them.
 7. NO NEW VISUAL VOCABULARY. `docs/ui/design_reference/` is binding and
    `assets_spec.md` is the asset authority. Every class the new markup uses —
    `card`, `cardHeader`, `activityList`, `activityItem`, `actorIcon`,
    `activityMeta`, `activityTag`, `emptyState` — already exists in
    `RightLivePanel.module.css`, and the glyph is `GearGlyph`, already
    imported. Add no CSS, no asset and no icon, so no `assets_spec.md` update
    and no assumption-log entry is owed. Do not introduce the token `@mui`, do
    not remove the word `Activity`, and do not introduce the token `POST`:
    `tests/ui_contracts/test_design_drift.py` and `test_responsive.py` assert
    all three about this exact file.
 8. Run no formatter or linter that rewrites a file in place; `npm run lint` in
    `apps/ui` is RED at base (R-0622), is not a gate here and must not be
    "fixed" in passing. Create and merge NO pull request: F021 is mid-feature.
    Push the branch.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 440
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 279 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C4; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is
     ordered NOWHERE — §3 item 31 leaves it to the next round's gate. Report
     also, as the reading THIS round owes from the last, that the R13 handback
     commit `9fcce96d` is single-parent and touches `.agent/handoff.md` alone
     at 47 insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r14.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r14.md` are all equal. Write
     C0b FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their `<<<SLICE `/
     `<<<END ` marker LINES; report how many slices and how many CONTENT lines
     that extractor printed, and re-measure constraint 9's two numerals from
     that same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R14 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare
     slice that must exit 1. Report both exit codes, that the last byte is a
     newline, `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, remainder EXACTLY one newline plus
     RECORD13 plus one newline — report its sha256, byte and line counts, and
     the file's byte and line counts before and after. Reader (b), SET-WISE:
     strip the one trailing terminator from BOTH blobs, split each on the blank
     line into units, and confirm the C2 unit LIST equals the base list
     followed by RECORD13's own units, ELEMENTWISE over the whole list, not at
     the tail; report N at both points and RECORD13's unit count, measured by
     the reviewer as ONE. NEGATIVE CONTROL: alter one printable byte of the C2
     file's FIRST paragraph at equal length; BOTH readers must REJECT it and
     ACCEPT the true file. Name the offset and the change.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R`
     keys and how many DISTINCT; `Gate: R14`; the MAXIMUM registered id.
     Nothing is minted, so `- R-` reads 213 at BOTH points with both DISTINCT,
     the maximum R-0650 at BOTH, `Done: R-` and `Landed: ` 0 at both, `Gate: R`
     keys 13 then 14 both DISTINCT, `Gate: R14` 0 then 1.
 G7  THE SEVEN PAIRS, at C3, counted by WHOLE-STRING search over raw bytes
     rather than line by line. Each FROM count in its target at the ROUND BASE
     must be exactly 1. At C3 the expected counts DIFFER BY PAIR SHAPE, as the
     reviewer measured on a dry run: AFC1, RLP0 and CONTRACTPATHS are
     APPEND-SHAPED — their TO text CONTAINS their FROM text — so each reads
     FROM 1 and TO 1, and a gate demanding FROM 0 would fail on a correct
     application (R-0640); AFC2, RLP1, RLP2 and SHELL1 are REPLACING and each
     reads FROM 0 and TO 1. Report all twenty-one numbers. If any FROM count at
     the round base is not 1, STOP and report rather than choosing an
     occurrence.
 G8  THE CONTRACT APPEND at C3: `tests/ui_contracts/test_brain_stream_ring.py`
     at the round base WITH CONTRACTPATHS's substitution applied to it in
     memory is a byte-exact PREFIX of that file at C3, and the remainder is
     EXACTLY one newline plus CONTRACTFEED plus one newline. Say the prefix
     side is the substituted blob. Report the remainder's sha256, byte and line
     counts. Do NOT use a per-line count: code repeats lines structurally and a
     count-based reader is satisfied by the wrong bytes (R-0531).
 G9  PEP 8 SPACING. CONTRACTFEED opens a new top-level class and CARRIES ITS
     OWN LEADING BLANK LINE — its first line is empty on purpose, so the
     append's one newline plus that blank puts exactly two blank lines before
     `class `. Do not trim it. Report the count of blank lines immediately
     before CONTRACTFEED's `class ` line in the C3 file: it must be 2. Ruff
     here does not evaluate E301-E306 outside preview, so this is COUNTED and
     not delegated to the linter (R-0558).
G10  TYPECHECK, at C3, from `apps/ui`: `npx tsc --noEmit`. Report the exit code
     and the working directory. The reviewer measured exit 0 with EMPTY output
     at the round base, so any output here is this round's doing. This is the
     load-bearing gate for the three `.tsx` files: this repository has NO DOM
     environment, so components are gated by the typechecker and by source
     contracts, never by rendering them.
G11  VITEST, at C3, from `apps/ui` in the PRIMARY checkout: `npx vitest run`. A
     fresh worktree has no `node_modules` and reports a vacuous red (R-0518),
     so this runs in the primary checkout and leaves the tree untouched. Report
     the exit code, the file count and the test count. This round adds NO
     vitest case, so the expected reading is UNCHANGED from the round base: 12
     files and 177 tests, which the reviewer measured by counting `it(` over
     the committed sources. A rise here means something was added that this
     block did not order. Its colour rests on your transcript — `npx vitest` is
     denied to the reviewer.
G12  THE RED CONTROL, on the Python contract, needing no `node_modules`. In a
     disposable worktree under `.remedy-wt/` whose name no directory already
     uses, check out C3 and confirm
     `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf`
     is GREEN there first — an already-red tree cannot fail honestly (R-0364).
     Then, in that worktree's `apps/ui/src/components/shell/RemedyShell.tsx`,
     break the single-subscription line by replacing
       `        <RightLivePanel dashboard={dashboard} onSelectNode={onSelectNode} streamStatus={stream.status} recent={stream.recent} recentDropped={stream.recentDropped} />`
     with the same line WITHOUT its two new props, that is
       `        <RightLivePanel dashboard={dashboard} onSelectNode={onSelectNode} streamStatus={stream.status} />`
     and re-run. That is the defect this round exists to prevent: a ring
     published on the view and never handed to the card. EXACTLY ONE test must
     fail, and it must be
     `TestTheFeedIsFedFromTheStream::test_the_shell_hands_the_ring_to_the_panel`.
     Report the failing name, the pass and fail counts and the assertion text;
     the reviewer measured 1 failed, 16 passed on the dry run. Prune the tree.
G13  THE PYTHON SUITES, at C3 in the PRIMARY checkout, SERIALLY, from the
     REPOSITORY ROOT — a shell left in `apps/ui` makes these exit 4 having run
     no test, which is vacuous and not green. Report each one's exit code, the
     working directory, and the total, counting BY PASSED PLUS SKIPPED:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 443 at the round base;
       CONTRACTFEED adds 4 test functions, which the reviewer counted by
       running that file alone on the dry run, so the total must read 447. This
       suite also holds `test_design_drift.py` and `test_responsive.py`, which
       assert the three tokens constraint 7 names about `ActivityFeedCard.tsx`.
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511 at base, and they
       read `.agent/plan.md`, so they also guard C1.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/` path.
G14  RANGE, executed at C3 and covering the round base to C3 — NOT to C4,
     because C4 writes the file that must quote this gate and §3 checklist item
     31 forbids ordering a reading the quoting artefact cannot hold. Report:
     the base-to-C3 path set against the eight non-handoff paths of `Change:`,
     the difference EMPTY both ways; every commit single-parent; `git show
     --numstat` and `git diff --numstat` agreeing cell by cell with the
     handback's `## Commits` table (§3 item 28), any disagreement reported
     rather than reconciled; insertions under the 500 cap; `<<<SLICE `/`<<<END `
     0 LINES in every file a slice landed in; `git ls-files .remedy-wt` 0;
     `git worktree list` ending with the primary checkout alone; and `gh pr
     list --state open --json number,headRefName` — expected EMPTY — with the
     statement that neither `gh pr create` nor `gh pr merge` was run.
     THE REFLOG CLAUSE NAMES ITS FIELD, which R-0613 requires and the R13 block
     failed to do: read `git reflog --format=%gs`, take the OPERATION only —
     the text BEFORE the first `:` — and scope to THIS ROUND'S rows, those from
     the round base forward. Report that every such row's operation is
     `commit` and that `amend`, `rebase` and `cherry` each occur 0 times in
     that OPERATION field. A substring count over whole rows is NOT this gate:
     this repository's commit subjects discuss amends by design, so that count
     is nonzero and says nothing about history rewriting.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, ONE LINE
            PER GATE with transcripts kept out of the file (R-0582), and the
            `Fortschritt:` line verbatim across all four of its lines. Report
            its own `wc -l` against the 60-line cap, with a DECISION D15 line
            declaring any overage and its mandated cause. Every `## Commits`
            heading carries that commit's FULL subject, and where a commit
            cannot name its own SHA the role and reason go INSIDE the heading
            (R-0494). `## Next` states that THIS SESSION ENDS with C4, that the
            next session's FIRST action is docs/agents/self_drive_protocol.md
            Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR
            Gate (R-0347), that rule 2 will find NO open pull request so rule 5
            applies and F021 continues on this branch, that R14's own verdict
            is UNRECORDED and the next round's C2 owes it, and that R15 is the
            scroll discipline plus the NowCard over the ACTION-class subset.

<<<SLICE AFC1 FROM
import type { RemedyActivityItem } from "../../api/types";
<<<END AFC1 FROM

<<<SLICE AFC1 TO
import type { RemedyActivityItem } from "../../api/types";
import type { FeedRow } from "../../api/feedRow";
<<<END AFC1 TO

<<<SLICE AFC2 FROM
export function ActivityFeedCard({ activity }: { activity: RemedyActivityItem[] }) {
  const hasActivity = activity.length > 0;

  return (
<<<END AFC2 FROM

<<<SLICE AFC2 TO
/** How many live rows the side panel shows. The ring holds up to
 *  BRAIN_RECENT_LIMIT; this card is a glance and the timeline is the archive. */
const LIVE_ROWS_SHOWN = 5;

/** The live half of the card: rows projected from the SSE stream, NEWEST
 *  FIRST. Remedy deliberately does not merge these with the dashboard's REST
 *  activity list — two clocks in one list would order neither honestly — so
 *  live rows REPLACE that list as soon as the stream has produced any. */
function LiveFeed({ recent, recentDropped }: { recent: readonly FeedRow[]; recentDropped: number }) {
  const newestFirst = recent.slice(-LIVE_ROWS_SHOWN).reverse();

  return (
    <div className={styles.activityList}>
      {recentDropped > 0 ? (
        <p className={styles.emptyState}>
          {recentDropped} earlier {recentDropped === 1 ? "event" : "events"} left this window — the timeline keeps them all.
        </p>
      ) : null}
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
    </div>
  );
}

export function ActivityFeedCard({ activity, recent, recentDropped }: { activity: RemedyActivityItem[]; recent?: readonly FeedRow[]; recentDropped?: number }) {
  const hasActivity = activity.length > 0;
  const live = recent ?? [];

  // The live path wins whenever the stream has produced a row. The dashboard
  // list below is the pre-stream fallback, not a second source of truth.
  if (live.length > 0) {
    return (
      <section className={styles.card}>
        <header className={styles.cardHeader}><h2>Activity</h2></header>
        <LiveFeed recent={live} recentDropped={recentDropped ?? 0} />
      </section>
    );
  }

  return (
<<<END AFC2 TO

<<<SLICE RLP0 FROM
import type { BrainStreamStatus } from "../../api/brainStream";
<<<END RLP0 FROM

<<<SLICE RLP0 TO
import type { BrainStreamStatus } from "../../api/brainStream";
import type { FeedRow } from "../../api/feedRow";
<<<END RLP0 TO

<<<SLICE RLP1 FROM
export function RightLivePanel({ dashboard, onSelectNode, streamStatus }: { dashboard: RemedyDashboard; onSelectNode: (nodeId: string | null) => void; streamStatus?: BrainStreamStatus | null }) {
<<<END RLP1 FROM

<<<SLICE RLP1 TO
export function RightLivePanel({ dashboard, onSelectNode, streamStatus, recent, recentDropped }: { dashboard: RemedyDashboard; onSelectNode: (nodeId: string | null) => void; streamStatus?: BrainStreamStatus | null; recent?: readonly FeedRow[]; recentDropped?: number }) {
<<<END RLP1 TO

<<<SLICE RLP2 FROM
      <ActivityFeedCard activity={dashboard.activity} />
<<<END RLP2 FROM

<<<SLICE RLP2 TO
      <ActivityFeedCard activity={dashboard.activity} recent={recent} recentDropped={recentDropped} />
<<<END RLP2 TO

<<<SLICE SHELL1 FROM
        <RightLivePanel dashboard={dashboard} onSelectNode={onSelectNode} streamStatus={stream.status} />
<<<END SHELL1 FROM

<<<SLICE SHELL1 TO
        <RightLivePanel dashboard={dashboard} onSelectNode={onSelectNode} streamStatus={stream.status} recent={stream.recent} recentDropped={stream.recentDropped} />
<<<END SHELL1 TO

<<<SLICE CONTRACTFEED

class TestTheFeedIsFedFromTheStream:
    """The surface half of DECISION F021 D5. The rows must reach the card by
    being passed DOWN from the one subscription the shell already holds, so
    these pin the path rather than the pixels — this repository has no DOM
    environment and never renders a component in a test."""

    def test_the_shell_hands_the_ring_to_the_panel(self):
        code = strip_ts_comments(SHELL.read_text())
        assert "recent={stream.recent}" in code, (
            "the ring is published on the view but never handed to the panel"
        )
        assert "recentDropped={stream.recentDropped}" in code

    def test_the_panel_hands_the_ring_to_the_card(self):
        code = strip_ts_comments(PANEL.read_text())
        assert "recent={recent}" in code
        assert "recentDropped={recentDropped}" in code

    def test_the_card_renders_the_rows_and_says_when_it_dropped_some(self):
        code = strip_ts_comments(CARD.read_text())
        assert "recent.slice(-LIVE_ROWS_SHOWN).reverse()" in code, (
            "the feed shows the newest rows first"
        )
        assert "recentDropped > 0" in code, (
            "a bounded window that never says it dropped anything is the "
            "silent drop D5 forbids"
        )

    def test_there_is_still_exactly_one_subscription(self):
        calls = 0
        for path in sorted(UI_SRC.rglob("*.ts")) + sorted(UI_SRC.rglob("*.tsx")):
            if path.name.endswith((".test.ts", ".test.tsx")):
                continue
            code = strip_ts_comments(path.read_text())
            calls += code.count("useBrainStream(")
            if path != DEPS:
                assert "EventSource" not in code, (
                    "only brainStreamDeps.ts may construct the transport"
                )
        assert calls == 2, "one definition plus one call, never a second"
<<<END CONTRACTFEED

<<<SLICE CONTRACTPATHS FROM
STATE = API_DIR / "brainStream.ts"
<<<END CONTRACTPATHS FROM

<<<SLICE CONTRACTPATHS TO
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
STATE = API_DIR / "brainStream.ts"
DEPS = API_DIR / "brainStreamDeps.ts"
CARD = UI_SRC / "components" / "panels" / "ActivityFeedCard.tsx"
PANEL = UI_SRC / "components" / "panels" / "RightLivePanel.tsx"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
<<<END CONTRACTPATHS TO

<<<SLICE PLANF021R14
# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210, which the reviewer merged at the Open PR Gate before
this branch was created. `.agent/live_review.md` is the source of truth for the
open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps event kinds to plain lines, a NowCard shows the newest ACTION-class
event with a recency dot, and feed rows carry their seq and click-jump to their
node. DONE when the catalog covers the kind set DECISION F021 D3 rules and an
unknown kind renders an honest generic line rather than vanishing, the feed
renders fixture streams per the binding CSS, jump-to-node focuses the right
node, and the steering input renders DISABLED with its tooltip until F030.

## Current Step
R14 makes the feed LIVE: the ring travels from the one `useBrainStream` call
down through `RightLivePanel` into `ActivityFeedCard`, which renders the newest
rows first and says so when the bound dropped some. It also records the R13
verdict, which was PASS on every gate.

## Next Steps
1. R15 adds the scroll discipline that never yanks a reader who has scrolled
   up, and the NowCard over the ACTION-class subset with its recency dot.
2. R16 gives each row its click-jump to the node, which is the graph-focus API
   T003 opens with.
3. R17 onward T003: the disabled steering input with its honest tooltip, and
   the additive envelope field DECISION F021 D2 permits.

## Risks
- No DOM environment exists in this repository, so components are gated by
  `npx tsc --noEmit` and by Python source contracts. A contract that reads a
  prop name is the only thing standing between "published" and "rendered".
- `useSyncExternalStore` compares with `Object.is`. Any later edit that rebuilds
  the view or the ring on every call re-renders forever; the contract tests in
  `tests/ui_contracts/test_brain_stream_ring.py` hold that line.
- `npx vitest run` is DENIED to the reviewer's session class, so a frontend
  round's vitest colour rests on the worker's transcript. Every such round
  carries a Python red control the reviewer reproduces itself.
- Reflog gates name the OPERATION field, never the whole row: this repository's
  commit subjects discuss amends by design (R-0613).
- No code defect of F021 is open; R-0403, R-0607, R-0608, R-0609, R-0611,
  R-0613 and R-0622 stay routed to a paydown branch.
<<<END PLANF021R14

<<<SLICE RECORD13
Gate: R14 — the R13 entry. R13 PASSED ON EVERY ONE OF ITS FOURTEEN GATES, RE-MEASURED INDEPENDENTLY RATHER THAN READ BACK, AND IT MINTS NO FINDING. R13 published the bounded ring on `BrainStreamView`. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f021-r13.md` at `80e0a880`, `.agent/last_block.md` at `0ad7eca0`, and the bytes the reviewer EMITTED at `.remedy-wt/f021-r13.md` are all sha256 8cb5ccdcf3799f7b1b6c607957576a682a8b99721571f16e4b340510cf28bdc8 over 26571 bytes and 415 lines. SLICES: 14 over 173 CONTENT lines, TOTAL 415 against DECISION F085 D6's 490 and PROSE 242 against D5's 400, both equal to that block's constraint 8. EVERY SLICE APPLIED BYTE FOR BYTE, verified against the reviewer's own emitted copy rather than against the worker's report: `.agent/plan.md` at `8c3a082a` equals PLANF021R13 plus one terminating newline and not the bare slice, at 43 lines; the ledger append at `665cded1` is the base blob plus one newline plus RECORD12 plus one newline, remainder sha256 f686d6a412e64e35 over 4200 bytes and 2 lines, units 231 to 232 elementwise equal; the vitest append at `9cda5c86` is the TESTIMPORT2-substituted base blob plus one newline plus TESTVIEW plus one newline over 1332 bytes; and the contract append is the base blob plus one newline plus CONTRACTVIEW plus one newline over 1721 bytes, with EXACTLY TWO blank lines before its new top-level class, which is the PEP 8 spacing that block's G9 counted rather than delegated to a linter that does not evaluate E301-E306 outside preview. THE FIVE PAIRS BEHAVED BY SHAPE, exactly as that block's G7 predicted from the reviewer's dry run: every FROM 1 at the round base; at C3 the append-shaped RUNNER1 and TESTIMPORT2 read FROM 1 and TO 1 while the replacing RUNNER2, RUNNER3 and RUNNER4 read FROM 0 and TO 1. THE LEDGER IS UNMOVED: `- R-` 213 at both points all DISTINCT, maximum R-0650 at both, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 12 to 13 both DISTINCT, `Gate: R13` 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially from the repository root: `tests/ui_contracts/` exit 0 with 439 passed and 4 skipped for 443, the three contract suites exit 0 with 511, the canary exit 0 with 42, and `npx tsc --noEmit` in `apps/ui` exit 0 with empty output. THE GATE THE REVIEWER CANNOT RUN WAS CORROBORATED RATHER THAN ACCEPTED: `npx vitest` is denied to that session class, so the worker's reading of 12 files and 177 tests against 173 at the round base was checked by counting `it(` over the committed test sources at both commits — 173 then 177, a rise of exactly 4, equal to TESTVIEW's four cases. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE: green first at 13 passed, then with `cachedView` seeded from a fresh array instead of the state exactly 1 failed and 12 passed, the failure being `TestViewPublishesTheRing::test_cached_view_is_seeded_from_the_state`. That mutation target occurs TWICE in the file and the worker reported the count and named which occurrence it changed, which is what makes a non-unique destructive target safe. THE RANGE HELD: six commits every one single-parent, the base-to-C3 path set EQUAL to that block's seven non-handoff `Change:` paths with both differences EMPTY, insertions 415, 267, 13, 2, 92 and 47 every one under the 500 cap, markers 0 in every file a slice landed in, `git ls-files .remedy-wt` 0, and `git worktree list` ending with the primary checkout alone. TWO DEFECTS ARE RECORDED HERE AGAINST OPEN FINDINGS RATHER THAN UNDER NEW IDS, the open set having been searched for the DEFECT first as §3 checklist item 30 requires, and BOTH are the reviewer's own block text rather than the worker's execution. FIRST, AGAINST R-0613: that block's G14 ordered "reflog rows with `amend`, `rebase`, `cherry` each 0" and named NO FIELD, which is precisely the defect R-0613 registers and whose fix R-0613 already states — a gate over reflog output names the operation, the text before the first `:` in `git reflog --format=%gs`. Measured over whole rows this repository reads amend 84, rebase 26 and cherry 60, because its commit SUBJECTS discuss amends by design and because unscoped rows predate the round, so the clause as written was unmeetable and the worker had to reinterpret it to pass. Measured by OPERATION and scoped to the round, all six rows read `commit` and the three tokens are 0, which the reviewer reproduced. The counter-measure is APPLIED in the block that carries this entry, whose G14 names the field, the scope, and why the substring reading is not the gate. SECOND, AGAINST R-0639: that block's constraint 5 ordered "the five pairs FIRST, then the three appends" while constraint 2 fixed a commit order in which an append at C2 precedes C3's pairs, so the two clauses cannot both hold under a whole-round reading. The worker read constraint 5 per TARGET FILE, declared the assumption rather than taking it silently, and that reading is correct — a pair can only be disturbed by an append to the file it matches in, and inside `brainStreamRunner.test.ts` the pair did precede the append, so R-0639's rationale is satisfied. This is R-0639's clause-against-clause class, not a new one. The counter-measure is APPLIED in this block's constraint 5, which states the per-file scope. WHY R13 IS PASS: every slice is byte-identical to the reviewer's own emitted bytes, every gate reproduces under the reviewer's own execution, the one unrunnable gate is corroborated by an independent static count that agrees exactly, and both defects are in the reviewer's gate prose rather than in anything that reached a source file.
<<<END RECORD13
