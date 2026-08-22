── STEP RECENCY — F021 ──
Goal:        Build the activity dot's rule. T5_F021 line 63 gives the NowCard a
             dot that pulses on recency and FADES TO IDLE after a quiet window,
             and R-0652 showed what happens when a liveness signal has no such
             rule: the badge latched on forever. This round writes that rule as
             headless data — `recency.ts` plus its vitest — and pins it with a
             source contract. It is a PURE function of two numbers, `nowMs`
             passed in and never read, so the fade is testable without waiting
             and without faking a clock. NOTHING is wired this round: R20 gives
             the badge and the dot this ONE source, which is what stops them
             disagreeing. The round also records the R18 verdict, which was PASS
             on all fourteen gates.

Fortschritt: ~87 % (T002 — Feed, NowCard, Scroll-Regel und jetzt die
             Recency-Regel stehen als reine Funktionen; es fehlen nur noch ihre
             Verdrahtung und T003) — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R18 verdict ·
             C3 the recency rule, its vitest and its contract · C4 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r19.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/api/recency.ts` (NEW, C3) ·
             `apps/ui/src/api/recency.test.ts` (NEW, C3) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C3) ·
             `.agent/handoff.md` (C4).
             Resolve any count in this block against that list.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). ROUND BASE is `65931e3d7fc63ef5b177c080138e02ffb8b3b061`, the R18
    handback commit, and it is the commit every "round base" in this block names.
 3. THIS ROUND REGISTERS NO FINDING AND RESOLVES NONE. R18 passed every one of
    its fourteen gates under the reviewer's own re-measurement and left no defect
    behind, so RECORD19 is a GATE ENTRY ALONE — one unit, not three. The open set
    does not move: 216 open before and after, maximum R-0653 before and after,
    next free R-0654. An id is minted only when a defect is found, and inventing
    one to make a round look thorough would corrupt the count every later gate
    reads.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice is quoted WITHOUT a
    trailing newline. A WHOLE-FILE write (PLANF021R19, RECENCY, RECENCYTEST) is
    the slice PLUS one terminator. An APPEND (RECORD19, CONTRACTRECENCY) is one
    newline, then the slice, then one terminator, so the target keeps exactly
    one. A FROM/TO PAIR substitutes in place, neither side carrying a terminator
    and the file's own untouched. The gates match each kind.
 5. PAIRS BEFORE APPENDS, READ PER TARGET FILE. Within any ONE file every pair is
    applied before any append to that same file. ONE file takes both:
    `tests/ui_contracts/test_brain_stream_ring.py` takes CONTRACTPATHS5 first and
    CONTRACTRECENCY second, in that order. The two `recency` files are whole-file
    writes and take no pair.
 6. HEADLESS THIS ROUND, WIRED AT R20. Do not import `recency.ts` from any
    component, do not edit `AgentNowCard.tsx`, `RightLivePanel.tsx`,
    `ActivityFeedCard.tsx`, `RemedyShell.tsx`, `brainStream.ts`, `feedRow.ts`,
    `actionClass.ts` or `feedScroll.ts`, and do not add CSS for a dot. The module
    must import NOTHING and must read NO clock: its contract asserts that both
    the token `import` and the token `Date.now` are absent from it, so either one
    turns that gate red.
 7. NO NEW VISUAL VOCABULARY AND NO NEW ASSET. This round renders nothing, so no
    `assets_spec.md` update and no assumption-log entry is owed. Do not introduce
    the token `@mui` and do not introduce the token `POST`.
 8. Run no formatter or linter that rewrites a file in place; `npm run lint` in
    `apps/ui` is RED at base (R-0622), is not a gate here and must not be "fixed"
    in passing. Create and merge NO pull request: F021 is mid-feature. Push the
    branch after C4.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 457
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 270 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C4; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain` prints
     0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is ordered
     NOWHERE — §3 item 31 leaves it to the next round. Report also, as the
     reading THIS round owes from the last, that the R18 handback commit
     `65931e3d` is single-parent and touches `.agent/handoff.md` alone at 41
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r19.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r19.md` are all equal. Write C0b
     FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their `<<<SLICE `/
     `<<<END ` marker LINES; report how many slices and how many CONTENT lines
     that extractor printed, and re-measure constraint 9's two numerals from that
     same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R19 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted from
     the committed C0a blob, with a NEGATIVE CONTROL against the bare slice that
     must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, remainder EXACTLY one newline plus RECORD19
     plus one newline — report its sha256, byte and line counts, and the file's
     byte and line counts before and after. Reader (b), SET-WISE: strip the one
     trailing terminator from BOTH blobs, split each on the blank line into units,
     and confirm the C2 unit LIST equals the base list followed by RECORD19's own
     units, ELEMENTWISE over the whole list, not at the tail; report N at both
     points and RECORD19's unit count, which is ONE this round because constraint
     3 registers no finding — the entry is the gate paragraph alone. NEGATIVE
     CONTROL: alter one printable byte of the C2 file's FIRST paragraph at equal
     length; BOTH readers must REJECT it and ACCEPT the true file. Name the offset
     and the change.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R` keys
     and how many DISTINCT; `Gate: R19`; the MAXIMUM registered id. NO id is
     minted and none resolved, so `- R-` reads 216 at BOTH points with both
     DISTINCT and the maximum R-0653 at BOTH, `Done: R-` and `Landed: ` 0 at both,
     while `Gate: R` keys move 18 to 19 both DISTINCT and `Gate: R19` 0 to 1. A
     round that records a verdict without finding a defect moves the gate keys and
     nothing else; if `- R-` moves, something was registered that this block did
     not order.
 G7  THE ONE PAIR, at C3, counted by WHOLE-STRING search over raw bytes rather
     than line by line. CONTRACTPATHS5 is APPEND-SHAPED — its TO CONTAINS its FROM
     — so it reads FROM 1 and TO 0 at the round base and FROM 1 and TO 1 at C3, as
     the reviewer measured on its dry run; a gate demanding FROM 0 would fail on a
     correct application (R-0640). Report all four numbers. If the base FROM count
     is not 1, STOP and report rather than choosing an occurrence.
 G8  THE CONTRACT APPEND at C3: `tests/ui_contracts/test_brain_stream_ring.py` at
     the round base (13034 bytes, 294 lines) WITH CONTRACTPATHS5's substitution
     applied to it in memory (13067 bytes) is a byte-exact PREFIX of that file at
     C3, and the remainder is EXACTLY one newline plus CONTRACTRECENCY plus one
     newline. Say the prefix side is the substituted blob. The reviewer measured
     the file at C3 as 14374 bytes and 326 lines and the remainder as 1307 bytes,
     31 lines, sha256
     `e1212600fdfe595b3c02e3bacb1d3fa777ec9523ad158fd11e55ce9417ee5a88`; report
     yours. Do NOT use a per-line count: code repeats lines structurally and a
     count-based reader is satisfied by the wrong bytes (R-0531).
 G9  PEP 8 SPACING. CONTRACTRECENCY opens a new top-level class and CARRIES ITS
     OWN LEADING BLANK LINE — its first line is empty on purpose, so the append's
     one newline plus that blank puts exactly two blank lines before `class`. Do
     not trim it. Report the count of blank lines immediately before
     CONTRACTRECENCY's `class ` line in the C3 file: it must be 2. Ruff here does
     not evaluate E301-E306 outside preview, so this is COUNTED and not delegated
     to the linter (R-0558).
G10  THE TWO NEW MODULES, at C3. `apps/ui/src/api/recency.ts` equals RECENCY PLUS
     ONE TERMINATING NEWLINE and `apps/ui/src/api/recency.test.ts` equals
     RECENCYTEST PLUS ONE TERMINATING NEWLINE, each by `cmp` at exit 0, each with
     a NEGATIVE CONTROL against its bare slice that must exit 1. Report all four
     exit codes and both sha256 values. The reviewer measured the module at 2012
     bytes, 44 lines, sha256
     `1a25f7aa1af1adc4e1cff8605b5dc2c52121f3cd6d8a3d69a0db11aa9a8d38f9` and the
     test at 1643 bytes, 58 lines, sha256
     `d7a227d3dd4fe4734f5aa8b12bb52cdf4ac83f876a5820d5382cdc7503a93913`. BOTH
     paths are ABSENT from `git ls-tree <round base>`, so this round CREATES them
     and replaces nothing; report that reading for each.
G11  TYPECHECK, at C3, from `apps/ui` in the PRIMARY checkout: `npx tsc --noEmit`.
     Report the exit code and the working directory. The reviewer typechecked the
     module in isolation on its dry run — `npx tsc --noEmit --strict --lib es2020`
     over `recency.ts` alone, exit 0 with EMPTY output — but the whole-project run
     is this gate, and the reviewer re-runs it itself at review because a fresh
     worktree cannot host it (R-0518). If it goes RED, STOP and report: G8 of
     self_drive_protocol.md forbids widening scope to route around a red gate.
G12  VITEST, at C3, from `apps/ui` in the PRIMARY checkout, RUN AS
     `npm run test:unit`. That script is defined as literally `vitest run`
     (`apps/ui/package.json` line 11); the bare `npx vitest` spelling is denied to
     both session classes (R-0651). Report the exit code, the file count and the
     test count. The round base reads 14 files and 196 tests. RECENCYTEST adds ONE
     file and ELEVEN cases — the reviewer counted its cases by scanning for lines
     whose first non-blank text is `it(`, which read 11, the ANCHORED form R-0651
     requires because a raw substring count of `it(` also matches `await(`,
     `emit(` and `split(` — so the expected reading at C3 is 15 files and 207
     tests. Note, per R-0653, that this gate can only ever be run GREEN: no vitest
     case in this repository has been mutation-proved, because a worktree has no
     `node_modules`. The contract below is the mutation-proved guard.
G13  THE RED CONTROL, on the Python contract, needing no `node_modules` (R-0518).
     In a disposable worktree under `.remedy-wt/` whose name no directory already
     uses, check out C3 and confirm
     `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf` is
     GREEN there first — an already-red tree cannot fail honestly (R-0364). The
     reviewer measured 35 passed. Then, in that worktree's
     `apps/ui/src/api/recency.ts`, collapse the pre-stream state into idle by
     replacing
       `    return "none";`
     with
       `    return "idle";`
     and re-run. That is the defect this level exists to prevent: a card that
     cannot tell "nothing has happened yet" from "the agent acted and went
     quiet", which is how a dot starts lying on the very first render. Confirm the
     target occurs EXACTLY ONCE in that file, counted BOTH whole-line and
     indent-agnostic with the two counts agreeing, and report both. EXACTLY ONE
     test must fail, and it must be
     `TestTheRecencyRuleIsPureAndHeadless::test_the_pre_stream_state_is_not_idle`.
     Report the failing name, the pass and fail counts and the assertion text; the
     reviewer measured 1 failed, 34 passed. NOTE WHY THAT TEST ASSERTS THE WHOLE
     RETURN STATEMENT and not the bare token `"none"`: the token also appears in
     the `RecencyLevel` union, so a looser guard would survive this exact mutation
     — the reviewer measured that on its dry run before choosing the assertion.
     Prune the tree.
G14  THE PYTHON SUITES, at C3 in the PRIMARY checkout, SERIALLY, from the
     REPOSITORY ROOT — a shell left in `apps/ui` makes these exit 4 having run no
     test, which is vacuous and not green. Never run two at once. Report each
     one's exit code, the working directory, and the total, counting BY PASSED
     PLUS SKIPPED, because data-dependent skips make the split vary at an
     unchanged tree:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 461 at the round base,
       which the reviewer measured itself; CONTRACTRECENCY adds 4 test functions,
       so the total must read 465.
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511 at base, and they
       read `.agent/plan.md`, so they also guard C1.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/` path.
G15  RANGE, executed at C3 and covering the round base to C3 — NOT to C4, because
     C4 writes the file that must quote this gate and §3 checklist item 31 forbids
     ordering a reading the quoting artefact cannot hold. Report: the base-to-C3
     path set against the seven non-handoff paths of `Change:`, the difference
     EMPTY both ways; every commit single-parent; `git show --numstat` and `git
     diff --numstat` agreeing cell by cell with the handback's `## Commits` table
     (§3 item 28), any disagreement reported rather than reconciled; insertions
     under the 500 cap; `git ls-files .remedy-wt` 0; `git worktree list` ending
     with the primary checkout alone; and `gh pr list --state open --json
     number,headRefName` — expected EMPTY — with the statement that neither `gh pr
     create` nor `gh pr merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED: count lines whose FIRST CHARACTERS are
     `<<<SLICE ` or `<<<END `, never lines that merely CONTAIN either token. Under
     the containment reading `.agent/live_review.md` reads nonzero at the round
     base — prose in earlier entries quotes the marker text — so that clause would
     be red at base and could not fail honestly (R-0364). Report the LINE-ANCHORED
     count for every file a slice landed in; each must be 0.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog --format=%gs`,
     take the OPERATION only — the text BEFORE the first `:` — and scope to THIS
     ROUND'S rows, those from the round base forward. Report that every such row's
     operation is `commit` and that `amend`, `rebase` and `cherry` each occur 0
     times in that OPERATION field. A substring count over whole rows is NOT this
     gate: this repository's commit subjects discuss amends by design.

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
            and F021 continues on this branch, that R19's own verdict is
            UNRECORDED and the next round's C2 owes it, and that R20 wires BOTH
            pure rules — recency for the badge and the dot, scroll for the feed.

<<<SLICE CONTRACTPATHS5 FROM
SCROLL = API_DIR / "feedScroll.ts"
<<<END CONTRACTPATHS5 FROM

<<<SLICE CONTRACTPATHS5 TO
SCROLL = API_DIR / "feedScroll.ts"
RECENCY = API_DIR / "recency.ts"
<<<END CONTRACTPATHS5 TO

<<<SLICE RECENCY
// How fresh the newest ACTION is, as a PURE function of two numbers. T5_F021
// gives the NowCard an activity dot that pulses on recency and fades to idle
// after a quiet window; Remedy deliberately keeps the RULE separate from the
// clock, so the fade is testable without waiting and without faking time. The
// caller passes `nowMs`; this module never reads a clock itself.

/** Inside this many ms of the newest action the dot pulses: the agent is
 *  visibly doing something right now. */
export const FRESH_WINDOW_MS = 5000;

/** After this many ms of quiet the dot is idle. Between the two windows it
 *  fades, which is the motion the design reference asks for. */
export const QUIET_WINDOW_MS = 30000;

/** What the dot shows. `none` is the pre-stream state, before any action has
 *  arrived at all, and is NOT the same as `idle`, which means the agent acted
 *  and then went quiet. */
export type RecencyLevel = "none" | "fresh" | "fading" | "idle";

/** The dot's level for a newest action stamped `lastActionAtMs`, seen at
 *  `nowMs`. A null stamp means nothing has acted yet. */
export function recencyLevel(lastActionAtMs: number | null, nowMs: number): RecencyLevel {
  if (lastActionAtMs === null) {
    return "none";
  }
  const elapsed = nowMs - lastActionAtMs;
  // A stamp in the future means the clocks disagree, not that the agent is
  // idle. Remedy reports fresh rather than idle here on purpose: under skew the
  // honest failure is to over-report life, never to declare a working agent dead.
  if (elapsed < FRESH_WINDOW_MS) {
    return "fresh";
  }
  if (elapsed < QUIET_WINDOW_MS) {
    return "fading";
  }
  return "idle";
}

/** Whether the card may call itself live. This is the single source R20 gives
 *  BOTH the badge and the dot, so the two can never disagree -- the defect
 *  R-0652 recorded was exactly a badge with a liveness rule of its own. */
export function isLiveByRecency(level: RecencyLevel): boolean {
  return level === "fresh" || level === "fading";
}
<<<END RECENCY

<<<SLICE RECENCYTEST
import { describe, it, expect } from "vitest";
import {
  FRESH_WINDOW_MS,
  QUIET_WINDOW_MS,
  isLiveByRecency,
  recencyLevel,
} from "./recency";

const T0 = 1_700_000_000_000;

describe("recencyLevel", () => {
  it("reports none before anything has acted", () => {
    expect(recencyLevel(null, T0)).toBe("none");
  });

  it("reports fresh at the moment of the action", () => {
    expect(recencyLevel(T0, T0)).toBe("fresh");
  });

  it("stays fresh just inside the fresh window", () => {
    expect(recencyLevel(T0, T0 + FRESH_WINDOW_MS - 1)).toBe("fresh");
  });

  it("starts fading exactly at the fresh boundary", () => {
    expect(recencyLevel(T0, T0 + FRESH_WINDOW_MS)).toBe("fading");
  });

  it("still fades just inside the quiet window", () => {
    expect(recencyLevel(T0, T0 + QUIET_WINDOW_MS - 1)).toBe("fading");
  });

  it("goes idle exactly at the quiet boundary", () => {
    expect(recencyLevel(T0, T0 + QUIET_WINDOW_MS)).toBe("idle");
  });

  it("stays idle long after the quiet window", () => {
    expect(recencyLevel(T0, T0 + QUIET_WINDOW_MS * 100)).toBe("idle");
  });

  it("reports fresh rather than idle when the clocks disagree", () => {
    expect(recencyLevel(T0 + 60_000, T0)).toBe("fresh");
  });
});

describe("isLiveByRecency", () => {
  it("counts fresh and fading as live", () => {
    expect(isLiveByRecency("fresh")).toBe(true);
    expect(isLiveByRecency("fading")).toBe(true);
  });

  it("counts idle as not live", () => {
    expect(isLiveByRecency("idle")).toBe(false);
  });

  it("counts the pre-stream state as not live", () => {
    expect(isLiveByRecency("none")).toBe(false);
  });
});
<<<END RECENCYTEST

<<<SLICE CONTRACTRECENCY

class TestTheRecencyRuleIsPureAndHeadless:
    """The dot's half of T5_F021 line 63: the activity dot pulses on recency
    and fades to idle after a quiet window. The rule is a PURE function of two
    numbers, so the fade is testable without waiting and without faking time,
    and it never reads a clock of its own."""

    def test_the_recency_rule_is_headless_data(self):
        code = strip_ts_comments(RECENCY.read_text())
        assert "import" not in code, (
            "a rule that imports anything is a component effect in disguise"
        )

    def test_the_rule_reads_no_clock_of_its_own(self):
        code = strip_ts_comments(RECENCY.read_text())
        assert "Date.now" not in code, (
            "now is passed in; a rule reading the clock cannot be tested without one"
        )

    def test_the_pre_stream_state_is_not_idle(self):
        code = strip_ts_comments(RECENCY.read_text())
        assert 'return "none";' in code, (
            "nothing-has-acted-yet is a distinct level from acted-then-went-quiet"
        )

    def test_one_liveness_source_feeds_badge_and_dot(self):
        code = strip_ts_comments(RECENCY.read_text())
        assert "isLiveByRecency" in code, (
            "the badge and the dot must share one rule or they will disagree (R-0652)"
        )
<<<END CONTRACTRECENCY

<<<SLICE PLANF021R19
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
R19 writes the activity dot's rule as a PURE function in `recency.ts` with its
vitest and a source contract: `none` before anything has acted, `fresh` inside
the fresh window, `fading` until the quiet window closes, `idle` after it, and
`fresh` rather than `idle` when the clocks disagree. `nowMs` is passed in and no
clock is read. Nothing is wired this round. It also records the R18 verdict,
which was PASS on all fourteen gates.

## Next Steps
1. R20 wires BOTH pure rules: `recency.ts` becomes the ONE liveness source for
   the NowCard's badge AND its new dot, which is what keeps them from
   disagreeing, and `feedScroll.ts` drives the feed's scroll container and the
   new-rows pill component_spec.md line 86 binds.
2. R21 gives each row its click-jump to the node, the graph-focus API T003 opens
   with, then T003: the disabled steering input with its honest tooltip.
3. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists in this repository, so components are gated by
  `npx tsc --noEmit` and by Python source contracts, and behaviour is put in
  PURE modules that vitest can reach. Wiring rounds are therefore the risky
  ones, and R20 is the last of them.
- Vitest IS reviewer-runnable as `npm run test:unit` from `apps/ui` (R-0651),
  but ONLY green: a fresh worktree has no `node_modules` (R-0518) and the
  symlink that would supply them is denied, so no vitest case has ever been
  mutation-proved. Every pure module therefore also carries a Python source
  contract whose red control IS runnable — that is the compensating control,
  and R-0653 records it.
- A source contract must assert a discriminating string. `"none"` also appears
  in the `RecencyLevel` union, so the pre-stream guard asserts the whole return
  statement; a looser guard survives the mutation it exists to catch.
- Reflog gates name the OPERATION field, never the whole row, and marker sweeps
  are LINE-ANCHORED, never containment (R-0613, R-0364).
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651 and R-0653 stay routed to a paydown branch.
<<<END PLANF021R19

<<<SLICE RECORD19
Gate: R19 — the R18 entry. R18 PASSED ON EVERY ONE OF ITS FOURTEEN GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND IT REGISTERS NO FINDING BECAUSE IT LEFT NO DEFECT. R18 retired R-0652: the NowCard's live badge went back to the agent's own `isRunning` flag, R16's detail line `liveAction ? liveAction.line : detail` untouched, and the repair is pinned by a contract whose red control RESTORES the latching form and fails on it. THE REPAIR IS MEASURED, NOT ASSERTED: at C3 the token `isActive` occurs 0 times in `AgentNowCard.tsx` while `newestActionRow` still occurs twice, so the ring still feeds the detail line and no longer feeds the badge. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own emitted `.remedy-wt/f021-r18.md`, `.agent/authored/f021-r18.md` at `824387a8` and `.agent/last_block.md` at `a451ac73` are ALL FOUR byte-identical, counting the received bytes, at sha256 907d24aff162f3aa88e53145319d222a582e4f1e6db60d47252901fee225a85f over 30318 bytes and 357 lines. SLICES: 4 over 114 CONTENT lines, TOTAL 357 against DECISION F085 D6's 490 and PROSE 243 against D5's 400, both equal to that block's constraint 8. EVERY SLICE APPLIED BYTE FOR BYTE, verified against slices the reviewer extracted mechanically from the committed C0a blob: `.agent/plan.md` at `2d4cc31b` equals PLANF021R18 plus one terminating newline and NOT the bare slice, at 48 lines with `## Goal` and `## Next Steps` once each; `AgentNowCard.tsx` at `674d1420` equals ANCFILE2 plus one terminator and not the bare slice, at 1859 bytes / 37 lines / sha256 f1e4e3fd72aa18402660e1f96933deca007d78543509b65ac9e71943247febee against 1517 bytes and 33 lines at the round base where `git ls-tree` DOES list it, so it REPLACED a tracked file; the ledger append at `9b4b37e8` is the base blob plus one newline plus RECORD18 plus one newline, remainder sha256 a22bd1349739924a8e42817ae890cfdb4f24b5e950bef23aedcb90eec71c5c83 over 7898 bytes and 6 lines, units 240 to 243 ELEMENTWISE equal with RECORD18 exactly 3 units, and a negative control at offset 2 of the FIRST paragraph — the byte `L` set to `X` at equal length — that BOTH readers rejected while both accepted the true file; and the contract append needed NO pair, the base blob itself being the byte-exact prefix, remainder sha256 8ec6fe0866ae7fc87263f43289894e80dfa4f81e7b8dcedf389bd0e5f2ae23c8 over 1072 bytes and 25 lines — A DIGEST THE REVIEWER PREDICTED FROM ITS OWN DRY RUN BEFORE DELEGATING AND WHICH THE APPLIED BYTES REPRODUCED EXACTLY — with EXACTLY TWO blank lines before the new top-level class, counted rather than delegated to a linter that does not evaluate E301-E306 outside preview. THE LEDGER MOVED ONLY AS ORDERED: `- R-` 215 to 216 all DISTINCT at both points, maximum R-0652 to R-0653, `Done: R-` and `Landed: ` 0 at both — this ledger has no such line convention, which is why the R-0652 repair is stated in the Gate paragraph and R-0652's own paragraph is NOT edited, per R-0470 — `Gate: R` keys 17 to 18 both DISTINCT, `Gate: R18` 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially from the repository root and counting by passed plus skipped: `tests/ui_contracts/` 461 at 457 passed and 4 skipped, the ordered rise of exactly 3 over the base's 458 that CONTRACTBADGE's three cases predict; the three state-reading suites 511; the canary 42; `npx tsc --noEmit` in `apps/ui` exit 0 with output EMPTY; and `npm run test:unit` 14 files and 196 tests, UNCHANGED from the round base exactly as a round that adds no vitest case must read. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `674d1420`: green first at 31 passed, then with the badge line replaced by the latching form R16 had shipped — a target the reviewer confirmed occurs EXACTLY ONCE, whole-line and indent-agnostic counts agreeing — exactly 1 failed and 30 passed, the failure being `TestTheNowCardBadgeTracksTheAgent::test_the_badge_reads_the_running_flag` with the assertion "the live badge must track the agent, not the presence of a row". THE RANGE HELD: five commits base to C3, every one single-parent, the path set EQUAL to that block's six non-handoff `Change:` paths with both differences EMPTY, `git show --numstat` and `git diff --numstat` agreeing cell by cell with the handback's tables, insertions 357, 238, 21, 6 and 32 every one under the 500 cap, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone, `gh pr list --state open` EMPTY, and the reflog read BY OPERATION over this round's rows every one `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE MARKER SWEEP WAS LINE-ANCHORED: 0 anchored in every one of the four files a slice landed in, while `.agent/live_review.md` reads 2 under the containment reading. THE WORKER DECLARED NO DEVIATION and none was found; its handback's 93 lines against the 60-line cap are within the 100 AGENTS.md permits for more than five commits, with mandated content as the stated cause. WHY R18 IS PASS: every slice is byte-identical to the slices the reviewer extracted itself, both predicted digests were reproduced by the applied bytes, the red control fails in the reviewer's own worktree on the one named test, and the defect R-0652 named is measurably gone rather than merely described as fixed.
<<<END RECORD19
