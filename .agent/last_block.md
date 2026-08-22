── STEP FEEDSCROLL — F021 ──
Goal:        Build the feed's scroll discipline as a PURE rule. component_spec.md
             line 86 binds the feed to pinned-to-newest-unless-scrolled-up with a
             new-rows pill, and T5_F021 line 59 asks for auto-scroll with a jump
             back to live. This round writes that decision as headless data —
             `feedScroll.ts` plus its vitest — and pins it with a source
             contract. NOTHING is wired into `ActivityFeedCard` this round: R15
             built the ACTION class before R16 wired it, and the same order holds
             here, because a scroll side effect cannot be tested in a repository
             with no DOM while a function over numbers can. The round also
             records the R16 verdict, which was PASS on all fifteen gates, and
             registers ONE finding against the NowCard R16 shipped.

Fortschritt: ~82 % (T002 — Feed und NowCard haengen am Stream, die Scroll-Regel
             liegt als reine Funktion vor; es fehlen ihre Verdrahtung, der
             Recency-Dot und T003) — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R16 verdict
             and R-0652 · C3 the scroll rule, its vitest and its contract · C4
             handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r17.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/api/feedScroll.ts` (NEW, C3) ·
             `apps/ui/src/api/feedScroll.test.ts` (NEW, C3) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C3) ·
             `.agent/handoff.md` (C4).
             Resolve any count in this block against that list.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). ROUND BASE is `0328426b40c633c479fd77085a5991eb280a75c9`, the R16
    handback commit, and it is the commit every "round base" in this block names.
 3. THIS ROUND REGISTERS EXACTLY ONE FINDING AND RESOLVES NONE. R16 passed every
    one of its fifteen gates under the reviewer's own re-measurement. Before this
    round: 214 open, maximum R-0651. RECORD17 registers R-0652 and records the
    R16 gate, so after C2: 215 open, maximum R-0652, next free R-0653. R-0652 is
    NEW rather than filed against an existing id because §3 checklist item 30's
    search of the open set for the DEFECT returned no hit: no open finding says
    the NowCard's live badge never returns to idle.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice is quoted WITHOUT a
    trailing newline. A WHOLE-FILE write (PLANF021R17, FEEDSCROLL,
    FEEDSCROLLTEST) is the slice PLUS one terminator. An APPEND (RECORD17,
    CONTRACTSCROLL) is one newline, then the slice, then one terminator, so the
    target keeps exactly one. A FROM/TO PAIR substitutes in place, neither side
    carrying a terminator and the file's own untouched. The gates match each
    kind.
 5. PAIRS BEFORE APPENDS, READ PER TARGET FILE. Within any ONE file every pair is
    applied before any append to that same file. ONE file takes both:
    `tests/ui_contracts/test_brain_stream_ring.py` takes CONTRACTPATHS4 first and
    CONTRACTSCROLL second, in that order. The two `feedScroll` files are
    whole-file writes and take no pair.
 6. HEADLESS THIS ROUND, WIRED LATER. Do not import `feedScroll.ts` from any
    component, do not edit `ActivityFeedCard.tsx`, `RightLivePanel.tsx`,
    `AgentNowCard.tsx`, `RemedyShell.tsx`, `brainStream.ts`, `feedRow.ts` or
    `actionClass.ts`, and do not add CSS for a pill. The module must import
    NOTHING: its contract asserts the token `import` is absent from it, so a
    single added import turns that gate red.
 7. NO NEW VISUAL VOCABULARY AND NO NEW ASSET. This round renders nothing, so no
    `assets_spec.md` update and no assumption-log entry is owed. Do not introduce
    the token `@mui` and do not introduce the token `POST`.
 8. Run no formatter or linter that rewrites a file in place; `npm run lint` in
    `apps/ui` is RED at base (R-0622), is not a gate here and must not be "fixed"
    in passing. Create and merge NO pull request: F021 is mid-feature. Push the
    branch after C4.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 465
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 264 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C4; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain` prints
     0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is ordered
     NOWHERE — §3 item 31 leaves it to the next round. Report also, as the
     reading THIS round owes from the last, that the R16 handback commit
     `0328426b` is single-parent and touches `.agent/handoff.md` alone at 36
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r17.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r17.md` are all equal. Write C0b
     FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their `<<<SLICE `/
     `<<<END ` marker LINES; report how many slices and how many CONTENT lines
     that extractor printed, and re-measure constraint 9's two numerals from that
     same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R17 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted from
     the committed C0a blob, with a NEGATIVE CONTROL against the bare slice that
     must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, remainder EXACTLY one newline plus RECORD17
     plus one newline — report its sha256, byte and line counts, and the file's
     byte and line counts before and after. Reader (b), SET-WISE: strip the one
     trailing terminator from BOTH blobs, split each on the blank line into units,
     and confirm the C2 unit LIST equals the base list followed by RECORD17's own
     units, ELEMENTWISE over the whole list, not at the tail; report N at both
     points and RECORD17's unit count, measured by the reviewer as THREE — the
     finding, its FIX line and the gate entry, the shape R-0650 and R-0651 already
     use. NEGATIVE CONTROL: alter one printable byte of the C2 file's FIRST
     paragraph at equal length; BOTH readers must REJECT it and ACCEPT the true
     file. Name the offset and the change.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R` keys
     and how many DISTINCT; `Gate: R17`; the MAXIMUM registered id. ONE id is
     minted and none resolved, so `- R-` reads 214 then 215 with both DISTINCT,
     the maximum R-0651 then R-0652, `Done: R-` and `Landed: ` 0 at both,
     `Gate: R` keys 16 then 17 both DISTINCT, `Gate: R17` 0 then 1.
 G7  THE ONE PAIR, at C3, counted by WHOLE-STRING search over raw bytes rather
     than line by line. CONTRACTPATHS4 is APPEND-SHAPED — its TO CONTAINS its
     FROM — so it reads FROM 1 and TO 0 at the round base and FROM 1 and TO 1 at
     C3, as the reviewer measured on its dry run; a gate demanding FROM 0 would
     fail on a correct application (R-0640). Report all four numbers. If the base
     FROM count is not 1, STOP and report rather than choosing an occurrence.
 G8  THE CONTRACT APPEND at C3: `tests/ui_contracts/test_brain_stream_ring.py` at
     the round base (10535 bytes, 236 lines) WITH CONTRACTPATHS4's substitution
     applied to it in memory (10570 bytes) is a byte-exact PREFIX of that file at
     C3, and the remainder is EXACTLY one newline plus CONTRACTSCROLL plus one
     newline. Say the prefix side is the substituted blob. The reviewer measured
     the file at C3 as 11962 bytes and 269 lines and the remainder as 1392 bytes,
     32 lines, sha256
     `224ed5417f81cc6a80dca71a5f0d756f631bc40a8180abd20cf29e857cf989f4`; report
     yours. Do NOT use a per-line count: code repeats lines structurally and a
     count-based reader is satisfied by the wrong bytes (R-0531).
 G9  PEP 8 SPACING. CONTRACTSCROLL opens a new top-level class and CARRIES ITS
     OWN LEADING BLANK LINE — its first line is empty on purpose, so the append's
     one newline plus that blank puts exactly two blank lines before `class`. Do
     not trim it. Report the count of blank lines immediately before
     CONTRACTSCROLL's `class ` line in the C3 file: it must be 2. Ruff here does
     not evaluate E301-E306 outside preview, so this is COUNTED and not delegated
     to the linter (R-0558).
G10  THE TWO NEW MODULES, at C3. `apps/ui/src/api/feedScroll.ts` equals FEEDSCROLL
     PLUS ONE TERMINATING NEWLINE and `apps/ui/src/api/feedScroll.test.ts` equals
     FEEDSCROLLTEST PLUS ONE TERMINATING NEWLINE, each by `cmp` at exit 0, each
     with a NEGATIVE CONTROL against its bare slice that must exit 1. Report all
     four exit codes and both sha256 values. The reviewer measured the module at
     2254 bytes, 50 lines, sha256
     `18ef679bdef07998b0179c5013056a67a0999671f377be2b215c50c34737e205` and the
     test at 2043 bytes, 64 lines, sha256
     `816df6037f463746aaedda9a7417ecb6595f0d24dc2a505699d84871acabbcd6`. BOTH
     paths are ABSENT from `git ls-tree <round base>`, so this round CREATES them
     and replaces nothing; report that reading for each.
G11  TYPECHECK, at C3, from `apps/ui` in the PRIMARY checkout: `npx tsc --noEmit`.
     Report the exit code and the working directory. This repository has NO DOM
     environment, so the typechecker and the source contracts are what stand
     between "published" and "correct". The reviewer typechecked the module in
     isolation on its dry run — `npx tsc --noEmit --strict --lib es2020` over
     `feedScroll.ts` alone, exit 0 with EMPTY output — but the whole-project run
     is this gate. If it goes RED, STOP and report: G8 of self_drive_protocol.md
     forbids widening scope to route around a red gate.
G12  VITEST, at C3, from `apps/ui` in the PRIMARY checkout, RUN AS
     `npm run test:unit`. That script is defined as literally `vitest run`
     (`apps/ui/package.json` line 11) and is the form the reviewer can execute
     too; the bare `npx vitest` spelling is denied to both session classes
     (R-0651). Report the exit code, the file count and the test count. The round
     base reads 13 files and 185 tests. FEEDSCROLLTEST adds ONE file and ELEVEN
     cases — the reviewer counted its cases by scanning for lines whose first
     non-blank text is `it(`, which read 11, the anchored form R-0651 requires
     because a raw substring count of `it(` also matches `await(`, `emit(` and
     `split(` — so the expected reading at C3 is 14 files and 196 tests. Any
     other number means something was added or dropped that this block did not
     order.
G13  THE RED CONTROL, on the Python contract, needing no `node_modules` (R-0518).
     In a disposable worktree under `.remedy-wt/` whose name no directory already
     uses, check out C3 and confirm
     `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf` is
     GREEN there first — an already-red tree cannot fail honestly (R-0364). The
     reviewer measured 28 passed. Then, in that worktree's
     `apps/ui/src/api/feedScroll.ts`, defeat the clearing rule by replacing
       `    return FEED_SCROLL_START;`
     with
       `    return prev;`
     and re-run. That is the defect this round exists to prevent: a reader who
     scrolls back to the newest edge keeps a stale unseen count, so the pill
     never goes away and stops meaning anything. Confirm the target occurs
     EXACTLY ONCE in that file, counted BOTH whole-line and indent-agnostic with
     the two counts agreeing, and report both. EXACTLY ONE test must fail, and it
     must be
     `TestTheFeedScrollRuleIsPureAndHeadless::test_the_unseen_count_clears_at_the_newest_edge`.
     Report the failing name, the pass and fail counts and the assertion text;
     the reviewer measured 1 failed, 27 passed. Prune the tree.
G14  THE PYTHON SUITES, at C3 in the PRIMARY checkout, SERIALLY, from the
     REPOSITORY ROOT — a shell left in `apps/ui` makes these exit 4 having run no
     test, which is vacuous and not green. Never run two at once. Report each
     one's exit code, the working directory, and the total, counting BY PASSED
     PLUS SKIPPED, because data-dependent skips make the split vary at an
     unchanged tree:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 454 at the round base,
       which the reviewer measured itself; CONTRACTSCROLL adds 4 test functions,
       so the total must read 458.
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511 at base, and they
       read `.agent/plan.md`, so they also guard C1.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/` path.
G15  RANGE, executed at C3 and covering the round base to C3 — NOT to C4, because
     C4 writes the file that must quote this gate and §3 checklist item 31
     forbids ordering a reading the quoting artefact cannot hold. Report: the
     base-to-C3 path set against the seven non-handoff paths of `Change:`, the
     difference EMPTY both ways; every commit single-parent; `git show --numstat`
     and `git diff --numstat` agreeing cell by cell with the handback's
     `## Commits` table (§3 item 28), any disagreement reported rather than
     reconciled; insertions under the 500 cap; `git ls-files .remedy-wt` 0;
     `git worktree list` ending with the primary checkout alone; and `gh pr list
     --state open --json number,headRefName` — expected EMPTY — with the
     statement that neither `gh pr create` nor `gh pr merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED: count lines whose FIRST CHARACTERS are
     `<<<SLICE ` or `<<<END `, never lines that merely CONTAIN either token.
     Under the containment reading `.agent/live_review.md` reads nonzero at the
     round base — prose in earlier entries quotes the marker text — so that
     clause would be red at base and could not fail honestly (R-0364). Report the
     LINE-ANCHORED count for every file a slice landed in; each must be 0.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog --format=%gs`,
     take the OPERATION only — the text BEFORE the first `:` — and scope to THIS
     ROUND'S rows, those from the round base forward. Report that every such
     row's operation is `commit` and that `amend`, `rebase` and `cherry` each
     occur 0 times in that OPERATION field. A substring count over whole rows is
     NOT this gate: this repository's commit subjects discuss amends by design.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, ONE LINE PER
            GATE with transcripts kept out of the file (R-0582), and the
            `Fortschritt:` line verbatim across all three of its lines. Report its
            own `wc -l` against the 60-line cap, with a DECISION D15 line
            declaring any overage and its mandated cause. Every `## Commits`
            heading carries that commit's FULL subject, and where a commit cannot
            name its own SHA the role and reason go INSIDE the heading (R-0494).
            `## Next` states that THIS SESSION ENDS with C4, that the next
            session's FIRST action is docs/agents/self_drive_protocol.md Phase 1
            rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate
            (R-0347), that rule 2 will find NO open pull request so rule 5 applies
            and F021 continues on this branch, that R17's own verdict is
            UNRECORDED and the next round's C2 owes it, and that R18 is the
            recency dot, which also owes the R-0652 repair.

<<<SLICE CONTRACTPATHS4 FROM
ACTION = API_DIR / "actionClass.ts"
<<<END CONTRACTPATHS4 FROM

<<<SLICE CONTRACTPATHS4 TO
ACTION = API_DIR / "actionClass.ts"
SCROLL = API_DIR / "feedScroll.ts"
<<<END CONTRACTPATHS4 TO

<<<SLICE FEEDSCROLL
// The rule that decides whether the live feed follows new rows or holds still.
// Remedy deliberately keeps this a PURE function over numbers rather than a
// component effect: this repository has no DOM environment, so a rule written
// as scroll side effects could not be tested at all, and the one behaviour that
// matters -- never yanking a reader who has scrolled up -- would ship unverified.

/** Px of slack that still counts as sitting at the newest edge. Sub-pixel
 *  layout rounding leaves a pinned viewport a fraction off zero, so an exact
 *  comparison would unpin a reader who never moved. */
export const NEWEST_EDGE_TOLERANCE_PX = 8;

/** What the feed carries besides its rows: how many rows arrived while the
 *  reader was away from the newest edge and has therefore not seen. */
export interface FeedScrollState {
  readonly unseenRows: number;
}

/** The state a feed starts in and returns to whenever the reader is pinned. */
export const FEED_SCROLL_START: FeedScrollState = { unseenRows: 0 };

/** True when the viewport still sits at the newest edge, within tolerance. */
export function isPinnedToNewest(distanceFromNewest: number): boolean {
  return distanceFromNewest <= NEWEST_EDGE_TOLERANCE_PX;
}

/** True when the feed may scroll itself to the newest row. A reader who has
 *  scrolled away is NEVER moved: that is the whole point of this module. */
export function shouldFollowNewest(distanceFromNewest: number): boolean {
  return isPinnedToNewest(distanceFromNewest);
}

/** The state after `arrived` rows reach a viewport `distanceFromNewest` px from
 *  the newest edge. A pinned reader sees them at once, so nothing is unseen; a
 *  reader who scrolled up accumulates them until returning to the edge. */
export function nextFeedScroll(
  prev: FeedScrollState,
  arrived: number,
  distanceFromNewest: number,
): FeedScrollState {
  if (isPinnedToNewest(distanceFromNewest)) {
    return FEED_SCROLL_START;
  }
  return { unseenRows: prev.unseenRows + arrived };
}

/** The "new rows" pill appears only once rows have arrived unseen. Returning to
 *  the newest edge clears it, through nextFeedScroll. */
export function shouldShowNewRowsPill(state: FeedScrollState): boolean {
  return state.unseenRows > 0;
}
<<<END FEEDSCROLL

<<<SLICE FEEDSCROLLTEST
import { describe, it, expect } from "vitest";
import {
  FEED_SCROLL_START,
  NEWEST_EDGE_TOLERANCE_PX,
  isPinnedToNewest,
  nextFeedScroll,
  shouldFollowNewest,
  shouldShowNewRowsPill,
} from "./feedScroll";

describe("isPinnedToNewest", () => {
  it("treats the exact edge as pinned", () => {
    expect(isPinnedToNewest(0)).toBe(true);
  });

  it("absorbs sub-pixel rounding up to the tolerance", () => {
    expect(isPinnedToNewest(NEWEST_EDGE_TOLERANCE_PX)).toBe(true);
  });

  it("treats a reader past the tolerance as scrolled away", () => {
    expect(isPinnedToNewest(NEWEST_EDGE_TOLERANCE_PX + 1)).toBe(false);
  });
});

describe("shouldFollowNewest", () => {
  it("follows for a pinned reader", () => {
    expect(shouldFollowNewest(0)).toBe(true);
  });

  it("never moves a reader who scrolled up", () => {
    expect(shouldFollowNewest(400)).toBe(false);
  });
});

describe("nextFeedScroll", () => {
  it("leaves a pinned reader with nothing unseen", () => {
    expect(nextFeedScroll(FEED_SCROLL_START, 3, 0)).toEqual({ unseenRows: 0 });
  });

  it("accumulates rows that arrive while the reader is away", () => {
    const after = nextFeedScroll(FEED_SCROLL_START, 2, 300);
    expect(nextFeedScroll(after, 3, 300)).toEqual({ unseenRows: 5 });
  });

  it("holds the count steady when a re-render brings no new row", () => {
    const away = nextFeedScroll(FEED_SCROLL_START, 4, 300);
    expect(nextFeedScroll(away, 0, 300)).toEqual({ unseenRows: 4 });
  });

  it("clears the count when the reader returns to the newest edge", () => {
    const away = nextFeedScroll(FEED_SCROLL_START, 7, 300);
    expect(nextFeedScroll(away, 0, 0)).toEqual({ unseenRows: 0 });
  });
});

describe("shouldShowNewRowsPill", () => {
  it("stays hidden until something arrives unseen", () => {
    expect(shouldShowNewRowsPill(FEED_SCROLL_START)).toBe(false);
  });

  it("appears once a row arrived while the reader was away", () => {
    expect(shouldShowNewRowsPill(nextFeedScroll(FEED_SCROLL_START, 1, 300))).toBe(true);
  });
});
<<<END FEEDSCROLLTEST

<<<SLICE CONTRACTSCROLL

class TestTheFeedScrollRuleIsPureAndHeadless:
    """The scroll half of T5_F021. component_spec.md line 86 binds the feed to
    pinned-to-newest-unless-scrolled-up with a new-rows pill, and the rule that
    decides it is a PURE function here because this repository has no DOM in
    which a scroll side effect could be tested at all."""

    def test_the_scroll_rule_is_headless_data(self):
        code = strip_ts_comments(SCROLL.read_text())
        assert "import" not in code, (
            "a rule that imports anything is a component effect in disguise"
        )

    def test_the_rule_never_follows_a_reader_who_scrolled_up(self):
        code = strip_ts_comments(SCROLL.read_text())
        assert "shouldFollowNewest" in code, (
            "the feed must ask before scrolling itself to the newest row"
        )
        assert "isPinnedToNewest" in code

    def test_the_unseen_count_clears_at_the_newest_edge(self):
        code = strip_ts_comments(SCROLL.read_text())
        assert "return FEED_SCROLL_START" in code, (
            "returning to the edge clears the unseen count rather than decrementing it"
        )

    def test_the_unseen_count_accumulates_while_away(self):
        code = strip_ts_comments(SCROLL.read_text())
        assert "prev.unseenRows + arrived" in code, (
            "rows arriving while the reader is away must accumulate unseen"
        )
<<<END CONTRACTSCROLL

<<<SLICE PLANF021R17
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
R17 writes the feed's scroll discipline as a PURE rule in `feedScroll.ts` with
its vitest and a source contract: a reader at the newest edge is followed, a
reader who scrolled up is never yanked, and rows arriving meanwhile accumulate
as an unseen count that clears only on return. Nothing is wired this round. It
also records the R16 verdict, which was PASS on all fifteen gates, and registers
R-0652.

## Next Steps
1. R18 adds the recency dot over a PURE time function, so the fade to idle after
   the quiet window is testable without a clock. It also OWES the R-0652 repair:
   the NowCard's live badge must fade with that same rule instead of latching on
   forever once any action has entered the ring.
2. R19 wires both pure rules into `ActivityFeedCard` — the scroll container, the
   new-rows pill component_spec.md line 86 binds, and the dot.
3. R20 gives each row its click-jump to the node, the graph-focus API T003 opens
   with, then T003: the disabled steering input with its honest tooltip.

## Risks
- No DOM environment exists in this repository, so components are gated by
  `npx tsc --noEmit` and by Python source contracts, and behaviour is put in
  PURE modules that vitest can reach. A rule expressed as a scroll side effect
  would be untestable here, which is why R17 lands headless.
- Vitest IS reviewer-runnable as `npm run test:unit` from `apps/ui`; only the
  bare `npx vitest` spelling is denied (R-0651). Gate it that way and re-run it
  at review. It stays vacuous in a fresh worktree, which has no `node_modules`
  (R-0518), unless that directory is symlinked in.
- Reflog gates name the OPERATION field, never the whole row, and marker sweeps
  are LINE-ANCHORED, never containment (R-0613, R-0364).
- R-0652 is the one open code defect of F021 and R18 owns it; R-0364, R-0403,
  R-0607, R-0608, R-0609, R-0611, R-0613, R-0622 and R-0651 stay routed to a
  paydown branch.
<<<END PLANF021R17

<<<SLICE RECORD17
- R-0652 — Low, THE NOWCARD'S LIVE BADGE LATCHES ON FOREVER ONCE ANY ACTION HAS ENTERED THE RING, SO A FINISHED JOB RENDERS A CARD THAT READS "IDLE" AND "LIVE" AT THE SAME TIME. Raised by the reviewer at the R16 gate against the component R16 shipped. R16 replaced the card's `isRunning` test with `isActive = isRunning || liveAction !== null`, where `liveAction` is `newestActionRow(recent ?? [])` over the stream ring the panel hands down. Traced at the gate: `recent` is only ever appended to and trimmed to its cap in `apps/ui/src/api/brainStream.ts` at the lines that build `appended` and slice it by `overflow`, and nothing clears it when the stream goes quiet or the job ends. So once one ACTION row is in the ring, `isActive` is permanently true, while `deriveAgentStatus` returns status "Idle" with detail "No active work." as soon as `dashboard.live.running` goes false. The card then shows the heading text, a "Live" badge, the word "Idle" and a stale action line together. Before R16 the badge meant strictly "the agent is running", so R16 changed an existing indicator's meaning as a side effect of wiring the detail line. T5_F021 line 63 binds the card's liveness signal to a recency rule that FADES TO IDLE after a quiet window, which is the recency dot R18 is scheduled to build; R16 therefore wired a liveness indicator one round ahead of the rule that makes it honest. Low rather than Medium because the branch carries no pull request and nothing has shipped to a user, and because the round that repairs it is the next one but one.

  FIX: at R18, drive the badge and the dot from the same PURE recency function rather than from the mere existence of an action row, so both return to idle after the quiet window; until then no round may treat `isActive` as a liveness signal.

Gate: R17 — the R16 entry. R16 PASSED ON EVERY ONE OF ITS FIFTEEN GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND IT SURFACES THE ONE FINDING REGISTERED IMMEDIATELY ABOVE. R16 wired `newestActionRow` into `AgentNowCard` through the ring `RightLivePanel` already receives, so the card's detail line is the newest ACTION the stream produced and falls back to the dashboard's own text when there is none, retiring the orphan R15 deliberately left. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own emitted `.remedy-wt/f021-r16.md`, `.agent/authored/f021-r16.md` at `5c0b114f` and `.agent/last_block.md` at `00535702` are ALL THREE byte-identical at sha256 20b0e961a63693b03ef3913d6947803545f5e9b4b75d19dcff3a9e68a91258a5 over 31506 bytes and 383 lines. SLICES: 8 over 109 CONTENT lines, TOTAL 383 against DECISION F085 D6's 490 and PROSE 274 against D5's 400, both equal to that block's constraint 9. EVERY SLICE APPLIED BYTE FOR BYTE, verified against slices the reviewer extracted mechanically from the committed C0a blob: `.agent/plan.md` at `3c90509c` equals PLANF021R16 plus one terminating newline and NOT the bare slice, at 42 lines with `## Goal` and `## Next Steps` once each; `AgentNowCard.tsx` at `e9b0dc0b` equals ANCFILE plus one terminator and not the bare slice, at 1517 bytes / 33 lines / sha256 0418f0805c142ca82beea3dfc249299fc6f5f061303faea09e313f13a4a238f0, against 1009 bytes and 26 lines at the round base where `git ls-tree` DOES list it, so it REPLACED a tracked file; the ledger append at `52d01adc` is the base blob plus one newline plus RECORD16 plus one newline, remainder sha256 51e76c6dfce675845102190ca27cce38c1560f4086cb60ec5f8f8cb6cb048e4d over 8272 bytes and 6 lines, units 234 to 237 ELEMENTWISE equal with RECORD16 exactly 3 units, and a negative control at offset 2 of the FIRST paragraph — the byte `L` set to `X` at equal length — that BOTH readers rejected while both accepted the true file; and the contract append is the CONTRACTPATHS3-substituted base blob (9431 bytes, from 9367 B / 210 L) plus one newline plus CONTRACTNOW plus one newline, remainder sha256 eff284d5939063acf1ce9f0d974160e2e5fc29806927e67aaa5232ff5cd5ea62 over 1104 bytes and 25 lines, with EXACTLY TWO blank lines before the new top-level class, counted rather than delegated to a linter that does not evaluate E301-E306 outside preview. THE TWO PAIRS BEHAVED BY SHAPE: CONTRACTPATHS3 is append-shaped and read FROM 1 / TO 0 at the round base and FROM 1 / TO 1 at C3, while the replacing RLP3 read FROM 1 / TO 0 then FROM 0 / TO 1; all eight numbers as predicted. THE LEDGER MOVED ONLY AS ORDERED: `- R-` 213 to 214 all DISTINCT at both points, maximum R-0650 to R-0651, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 15 to 16 both DISTINCT, `Gate: R16` 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially from the repository root and counting by passed plus skipped: `tests/ui_contracts/` 454, and the reviewer measured the round base ITSELF at 451 in a disposable worktree, so the rise of exactly 3 equals CONTRACTNOW's three cases — the skip split moved from 4 to 5 between those two runs, which is precisely why the count is passed-plus-skipped; the three state-reading suites 511; the canary 42; and `npx tsc --noEmit` in `apps/ui` exit 0 with output EMPTY. VITEST WAS EXECUTED BY THE REVIEWER, not corroborated: `npm run test:unit` in `apps/ui` read 13 files and 185 tests all passing, unchanged from the round base exactly as the block predicted for a round that adds no vitest case. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `e9b0dc0b`: green first at 24 passed, then with the card unwired to `<AgentNowCard dashboard={dashboard} />` — a target the reviewer confirmed occurs EXACTLY ONCE, whole-line and indent-agnostic counts agreeing — exactly 1 failed and 23 passed, the failure being `TestTheNowCardShowsTheNewestAction::test_the_panel_hands_the_ring_to_the_now_card` with the assertion "the NowCard is wired to nothing and shows the fallback forever". THE RANGE HELD: five commits base to C3, every one single-parent, the path set EQUAL to that block's seven non-handoff `Change:` paths with both differences EMPTY, `git show --numstat` and `git diff --numstat` agreeing cell by cell with the handback's table, insertions 383, 242, 16, 6 and 38 every one under the 500 cap, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone, `gh pr list --state open` EMPTY, and the reflog read BY OPERATION over this round's rows every one `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE MARKER SWEEP WAS LINE-ANCHORED AND THE REASON WAS MEASURED: 0 anchored in every one of the five files a slice landed in, while `.agent/live_review.md` reads 2 under the containment reading, so the clause that would be red at base under containment is clean under the reading the block ordered. THE WORKER DECLARED NO DEVIATION and none was found: the ordered commit sequence was followed exactly, only the paths in `Change:` were touched, and the handback's 82 lines against the 60-line cap are within the 100 AGENTS.md permits for more than five commits, with mandated content as the stated cause. WHY R16 IS PASS: every slice is byte-identical to the slices the reviewer extracted itself, every gate reproduces under the reviewer's own execution, the red control fails in the reviewer's own worktree on the one named test, and the two append digests the block had PREDICTED before delegation were reproduced exactly by the applied bytes. The one finding above is a defect in the shipped component, not a deviation by the worker, which applied the reviewer's own bytes faithfully.
<<<END RECORD17
