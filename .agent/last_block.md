── STEP RECENCY2 — F021 ──
Goal:        Build the activity dot's rule, the work R19 halted before reaching.
             T5_F021 line 63 gives the NowCard a dot that pulses on recency and
             FADES TO IDLE after a quiet window, and R-0652 showed what happens
             to a liveness signal with no such rule. This round writes it as
             headless data — `recency.ts` plus its vitest — pinned by a source
             contract. It is a PURE function of two numbers, `nowMs` passed in
             and never read, so the fade is testable without waiting. NOTHING is
             wired: R21 gives the badge and the dot this ONE source. The round
             also records R19, which HALTED at a gate whose two clauses could
             not both hold, and registers the finding for that.

Fortschritt: ~87 % (T002 — Feed, NowCard, Scroll-Regel und jetzt die
             Recency-Regel stehen als reine Funktionen; es fehlen nur noch ihre
             Verdrahtung und T003) — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R19 halt
             record and R-0654 · C3 the recency rule, its vitest and its
             contract · C4 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r20.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/api/recency.ts` (NEW, C3) ·
             `apps/ui/src/api/recency.test.ts` (NEW, C3) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C3) ·
             `.agent/handoff.md` (C4).
             Resolve any count in this block against that list.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it. R19's worker did exactly this and was right
    to; the fault was the block's, not its own.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). ROUND BASE is `45a437dc558e3f31f96e1058662b001b68d24083`, the R19
    halt handback, and it is the commit every "round base" in this block names.
 3. THIS ROUND REGISTERS EXACTLY ONE FINDING AND RESOLVES NONE. Before this
    round: 216 open, maximum R-0653. RECORD20 registers R-0654 and records the
    R19 halt, so after C2: 217 open, maximum R-0654, next free R-0655. R-0654 is
    NEW rather than filed against an existing id because §3 checklist item 30's
    search of the open set for the DEFECT returned no hit for a gate whose own
    two clauses contradict each other in THIS reviewer's blocks. NOTE that
    `Gate: R19` never appears in the ledger and never will: R19 halted before its
    C2, so its record is the `Gate: R20` entry this round writes.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice is quoted WITHOUT a
    trailing newline. A WHOLE-FILE write (PLANF021R20, RECENCY, RECENCYTEST) is
    the slice PLUS one terminator. An APPEND (RECORD20, CONTRACTRECENCY) is one
    newline, then the slice, then one terminator, so the target keeps exactly
    one. A FROM/TO PAIR substitutes in place, neither side carrying a terminator
    and the file's own untouched. The gates match each kind.
 5. PAIRS BEFORE APPENDS, READ PER TARGET FILE. Within any ONE file every pair is
    applied before any append to that same file. ONE file takes both:
    `tests/ui_contracts/test_brain_stream_ring.py` takes CONTRACTPATHS5 first and
    CONTRACTRECENCY second, in that order. The two `recency` files are whole-file
    writes and take no pair.
 6. HEADLESS THIS ROUND, WIRED AT R21. Do not import `recency.ts` from any
    component, do not edit `AgentNowCard.tsx`, `RightLivePanel.tsx`,
    `ActivityFeedCard.tsx`, `RemedyShell.tsx`, `brainStream.ts`, `feedRow.ts`,
    `actionClass.ts` or `feedScroll.ts`, and do not add CSS for a dot. The module
    must import NOTHING and must read NO clock: its contract asserts that both
    the token `import` and the token `Date.now` are absent from it.
 7. NO NEW VISUAL VOCABULARY AND NO NEW ASSET. This round renders nothing, so no
    `assets_spec.md` update and no assumption-log entry is owed. Do not introduce
    the token `@mui` and do not introduce the token `POST`.
 8. Run no formatter or linter that rewrites a file in place; `npm run lint` in
    `apps/ui` is RED at base (R-0622), is not a gate here and must not be "fixed"
    in passing. Create and merge NO pull request: F021 is mid-feature. Push the
    branch after C4.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 459
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 276 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C4; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain` prints
     0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is ordered
     NOWHERE — §3 item 31 leaves it to the next round. Report also, as the
     reading THIS round owes from the last, that the R19 halt handback
     `45a437dc` is single-parent and touches `.agent/handoff.md` alone at 69
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r20.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r20.md` are all equal. Write C0b
     FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their `<<<SLICE `/
     `<<<END ` marker LINES; report how many slices and how many CONTENT lines
     that extractor printed, and re-measure constraint 9's two numerals from that
     same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R20 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted from
     the committed C0a blob, with a NEGATIVE CONTROL against the bare slice that
     must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1. THE LINE-COUNT CLAUSE IS MEASURED,
     NOT WISHED: the reviewer counted PLANF021R20 at 43 lines, so the file is 43
     lines and `wc -l` must read EXACTLY 43, which satisfies AGENTS.md's "keep it
     short (<50 lines)" with room to spare. This gate is written this way because
     R19 died on its predecessor: that block ordered `cmp` against a 51-line
     slice AND `wc -l` at most 50 in the same gate, two clauses that could not
     both hold, and the worker correctly refused to choose between them (R-0654).
     If the count you measure is not 43, STOP and report — do NOT trim the file
     to reach it, because that would break the cmp clause exactly as before.
 G5  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, remainder EXACTLY one newline plus RECORD20
     plus one newline — report its sha256, byte and line counts, and the file's
     byte and line counts before and after. Reader (b), SET-WISE: strip the one
     trailing terminator from BOTH blobs, split each on the blank line into units,
     and confirm the C2 unit LIST equals the base list followed by RECORD20's own
     units, ELEMENTWISE over the whole list, not at the tail; report N at both
     points and RECORD20's unit count, measured by the reviewer as THREE — the
     finding, its FIX line and the gate entry. NEGATIVE CONTROL: alter one
     printable byte of the C2 file's FIRST paragraph at equal length; BOTH readers
     must REJECT it and ACCEPT the true file. Name the offset and the change.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R` keys
     and how many DISTINCT; `Gate: R20`; the MAXIMUM registered id. ONE id is
     minted and none resolved, so `- R-` reads 216 then 217 with both DISTINCT,
     the maximum R-0653 then R-0654, `Done: R-` and `Landed: ` 0 at both,
     `Gate: R` keys 18 then 19 both DISTINCT, `Gate: R20` 0 then 1. `Gate: R19`
     reads 0 at BOTH points, per constraint 3.
 G7  THE ONE PAIR, at C3, counted by WHOLE-STRING search over raw bytes rather
     than line by line. CONTRACTPATHS5 is APPEND-SHAPED — its TO CONTAINS its FROM
     — so it reads FROM 1 and TO 0 at the round base and FROM 1 and TO 1 at C3, as
     the reviewer measured on its dry run; a gate demanding FROM 0 would fail on a
     correct application (R-0640). Report all four numbers. If the base FROM count
     is not 1, STOP and report rather than choosing an occurrence.
 G8  THE CONTRACT APPEND at C3: `tests/ui_contracts/test_brain_stream_ring.py` at
     the round base (13034 bytes, 294 lines — UNCHANGED by R19, whose C3 never
     ran) WITH CONTRACTPATHS5's substitution applied to it in memory (13067 bytes)
     is a byte-exact PREFIX of that file at C3, and the remainder is EXACTLY one
     newline plus CONTRACTRECENCY plus one newline. Say the prefix side is the
     substituted blob. The reviewer measured the file at C3 as 14374 bytes and 326
     lines and the remainder as 1307 bytes, 31 lines, sha256
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
     `14f990bd090c7c858bb51ba6222203fd32b5811f53eae086c69c2d70775e2d49` and the
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
            and F021 continues on this branch, that R20's own verdict is
            UNRECORDED and the next round's C2 owes it, and that R21 wires BOTH
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

/** Whether the card may call itself live. This is the single source R21 gives
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

<<<SLICE PLANF021R20
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
R20 builds the activity dot's rule as a PURE function in `recency.ts` with its
vitest and a source contract — the work R19 halted before reaching. It also
records R19, which HALTED at a self-contradicting gate of the reviewer's own
making, and registers R-0654.

## Next Steps
1. R21 wires BOTH pure rules: `recency.ts` becomes the ONE liveness source for
   the NowCard's badge AND its dot, and `feedScroll.ts` drives the feed's scroll
   container and the new-rows pill component_spec.md line 86 binds.
2. R22 gives each row its click-jump to the node, then T003: the disabled
   steering input with its honest tooltip.
3. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts, and behaviour lives in PURE modules vitest can
  reach. The wiring round is the risky one.
- Vitest is reviewer-runnable as `npm run test:unit` (R-0651) but only GREEN: a
  worktree has no `node_modules` (R-0518), so no vitest case has been
  mutation-proved. The Python contract is the mutation-proved guard (R-0653).
- A source contract must assert a DISCRIMINATING string: `"none"` also appears
  in the `RecencyLevel` union, so the pre-stream guard asserts the whole return
  statement rather than the bare token.
- A plan slice is MEASURED before its gate is written: R19 died because its gate
  demanded a line count its own slice could not have (R-0654).
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651 and R-0653 stay routed to a paydown branch.
<<<END PLANF021R20

<<<SLICE RECORD20
- R-0654 — Medium, A GATE'S TWO CLAUSES CONTRADICTED EACH OTHER, SO THE ROUND COULD NOT BE COMPLETED BY ANY CORRECT WORKER. R19's G4 ordered `.agent/plan.md` to equal the PLANF021R19 slice plus one terminating newline, verified by `cmp` at exit 0, AND to read `wc -l` at most 50. The slice is 51 lines, so the file the first clause demands is necessarily 51 lines and the second clause is necessarily red. The worker applied the slice byte for byte, measured 51, reported the contradiction and STOPPED at C1 without making C2 or C3 — exactly what block constraint 1 and guardrail G8 require, and the correct outcome: any worker that had trimmed a line to reach 50 would have broken the cmp clause instead, and one that had reported 50 would have lied. Raised by the reviewer against its OWN block. The defect is not the number but the method: R17's and R18's plan slices happened to be 48 lines and the `at most 50` clause happened to hold, so three rounds of the same wording passed on luck rather than on measurement, and the first slice that grew past the threshold exposed it. This is the clause-versus-clause class the §3 checklist has never caught: every clause of R19's G4 was individually true and checkable, and only their CONJUNCTION was unsatisfiable. Medium rather than Low because a whole round was spent to discover it and the branch was left with a `.agent/plan.md` that describes work no commit performed — a state AGENTS.md's Session Resume reads second — and Medium rather than High because nothing false was published, no test was weakened, and the worker's halt preserved every invariant.

  FIX, applied in the SAME round that registers this finding: a gate that names a line count MEASURES that count on the slice it also orders byte-equality against, and states the two together as ONE reading — this block's G4 says the slice is 47 lines, so the file is 47, and orders `wc -l` to read EXACTLY 47 rather than a bound the slice was never checked against. A bound clause and an equality clause over the same file are written only when the bound has been evaluated against the measured equality target. Standing, binding the reviewer: never write a cap into a gate whose other clause fixes the value; write the measured value.

Gate: R20 — the R19 entry. R19 HALTED AND DID NOT PASS, AND THE FAULT WAS THE REVIEWER'S BLOCK RATHER THAN THE WORKER'S EXECUTION. R19 landed C0a `9d6b087a`, C0b `cd139caa` and C1 `c239b75c`, then stopped: C2 and C3 were never made, no worktree was created, no pull request was touched, and the branch was pushed at `45a437dc`. THE HALT IS THE CORRECT OUTCOME AND IS CONFIRMED BY THE REVIEWER'S OWN MEASUREMENT: the PLANF021R19 slice extracted mechanically from the committed C0a blob is 51 lines, `.agent/plan.md` at `c239b75c` is byte-equal to that slice plus one terminating newline and reads `wc -l` 51, and R19's G4 ordered at most 50 — so the gate was unsatisfiable and the finding registered immediately above records it. WHAT R19 DID LAND WAS SOUND: TRANSPORT HELD across all four copies — the received bytes, the reviewer's emitted `.remedy-wt/f021-r19.md`, `.agent/authored/f021-r19.md` at C0a and `.agent/last_block.md` at C0b — at sha256 f515556e6419bacd6f93a3dcd2c5c7797504f4d48267736e6b7fbed224e86983 over 31368 bytes and 457 lines; the marker-LINE extractor over the committed C0a blob printed 7 slices and 187 CONTENT lines, TOTAL 457 against DECISION F085 D6's 490 and PROSE 270 against D5's 400, both equal to that block's constraint 9; and G4's other three clauses were green, the cmp exit 0, the bare-slice negative control exit 1, `## Goal` and `## Next Steps` once each. THE OPEN SET DID NOT MOVE, as a round whose C2 never ran cannot move it: 216 open at both ends, maximum R-0653, and `Gate: R19` never appears in this ledger and never will, because R19's record is THIS entry. THE TREE WAS LEFT CLEAN: `git status --porcelain` 0 lines, `git worktree list` the primary checkout alone, `git ls-files .remedy-wt` 0, four commits every one single-parent with insertions 457, 318, 19 and 69, all under the 500 cap, and the reflog read BY OPERATION over those rows every one `commit`. THE ONE CONSEQUENCE TO CARRY: between `c239b75c` and this block's C1, `.agent/plan.md` described recency work that no commit had performed, which is why this round's C1 rewrites it before its C2 rather than after. WHY R19 IS NOT A FAIL AGAINST ITS WORKER: it applied every slice it did apply byte for byte from the mechanical extractor, it refused to fix a slice constraint 1 forbade it to fix, it refused to choose between two clauses it could not jointly satisfy, it declared the truncated sequence as a deviation, and it wrote a handback naming exactly what the reviewer owed next. That is the behaviour the halt rule exists to produce.
<<<END RECORD20
