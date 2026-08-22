── STEP BADGETRUTH — F021 ──
Goal:        Retire R-0652. R16 replaced the NowCard's `isRunning` badge test
             with `isActive = isRunning || liveAction !== null`, and because
             `brainStream.ts` only appends to `recent` and trims it, a row
             outlives the job that produced it: once one ACTION has entered the
             ring the badge latches on and the card renders "Live" beside the
             word "Idle" forever. This round puts the badge back on the agent's
             own running flag and pins that with a contract whose red control
             reproduces the latch. The recency dot T5_F021 line 63 binds the
             liveness signal to is R19's work, and it needs a clock inside the
             component, which is why it is not folded in here. The round also
             records the R17 verdict, which was PASS on all fifteen gates, and
             registers ONE finding about the evidence standard for vitest.

Fortschritt: ~84 % (T002 — Feed, NowCard und die reine Scroll-Regel stehen, das
             Badge sagt wieder die Wahrheit; es fehlen Recency-Dot, die
             Verdrahtung der Scroll-Regel und T003) — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R17 verdict,
             R-0653 and the R-0652 repair record · C3 the badge repair and its
             contract · C4 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r18.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/components/panels/AgentNowCard.tsx` (C3) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C3) ·
             `.agent/handoff.md` (C4).
             Resolve any count in this block against that list.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). ROUND BASE is `9dff7937b6b2d0a843713e89f0310fe08e7d0fdf`, the R17
    handback commit, and it is the commit every "round base" in this block names.
 3. THIS ROUND REGISTERS EXACTLY ONE FINDING AND EDITS NO EXISTING ENTRY. Before
    this round: 215 open, maximum R-0652. RECORD18 registers R-0653 and records
    the R17 gate, so after C2: 216 open, maximum R-0653, next free R-0654. The
    R-0652 REPAIR IS RECORDED IN THE NEW ENTRY'S PROSE, never by editing R-0652's
    own paragraph: R-0470 settled that closing the distance between a claim and
    the bytes by editing the bytes is how a record stops being one. This ledger
    has no `Done: R-` or `Landed: ` line convention — both keys read 0 throughout
    and stay 0 — so the Gate entry is where a repair is stated.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice is quoted WITHOUT a
    trailing newline. A WHOLE-FILE write (PLANF021R18, ANCFILE2) is the slice
    PLUS one terminator. An APPEND (RECORD18, CONTRACTBADGE) is one newline, then
    the slice, then one terminator, so the target keeps exactly one. THIS ROUND
    HAS NO FROM/TO PAIR: `tests/ui_contracts/test_brain_stream_ring.py` already
    declares `NOWCARD`, so the contract needs no new path constant and takes an
    append alone.
 5. THE BADGE IS THE ONLY BEHAVIOUR THAT CHANGES. ANCFILE2 keeps R16's detail
    line exactly — `liveAction ? liveAction.line : detail` — and keeps
    `newestActionRow(recent ?? [])`. Only the two `isActive` readings become
    `isRunning`, and the binding `const isActive = ...` disappears with them. Do
    not touch `RightLivePanel.tsx`, `actionClass.ts`, `feedScroll.ts`,
    `brainStream.ts` or `ActivityFeedCard.tsx`, and do not build the recency rule
    here — R19 owns it.
 6. NO NEW VISUAL VOCABULARY AND NO NEW ASSET. `card`, `cardHeader`, `liveSmall`,
    `agentNow` and `actorIcon` already exist in `RightLivePanel.module.css`, and
    both glyphs are already imported by the file being replaced. Add no CSS, no
    asset and no icon, so no `assets_spec.md` update and no assumption-log entry
    is owed. Do not introduce the token `@mui`, do not introduce the token
    `POST`, and do not remove the heading text `Agent is doing now`.
 7. Run no formatter or linter that rewrites a file in place; `npm run lint` in
    `apps/ui` is RED at base (R-0622), is not a gate here and must not be "fixed"
    in passing. Create and merge NO pull request: F021 is mid-feature. Push the
    branch after C4.
 8. Block size, measured on these final bytes AFTER the last edit: TOTAL 357
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 243 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C4; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain` prints
     0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is ordered
     NOWHERE — §3 item 31 leaves it to the next round. Report also, as the
     reading THIS round owes from the last, that the R17 handback commit
     `9dff7937` is single-parent and touches `.agent/handoff.md` alone at 63
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r18.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r18.md` are all equal. Write C0b
     FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their `<<<SLICE `/
     `<<<END ` marker LINES; report how many slices and how many CONTENT lines
     that extractor printed, and re-measure constraint 8's two numerals from that
     same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R18 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted from
     the committed C0a blob, with a NEGATIVE CONTROL against the bare slice that
     must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, remainder EXACTLY one newline plus RECORD18
     plus one newline — report its sha256, byte and line counts, and the file's
     byte and line counts before and after. Reader (b), SET-WISE: strip the one
     trailing terminator from BOTH blobs, split each on the blank line into units,
     and confirm the C2 unit LIST equals the base list followed by RECORD18's own
     units, ELEMENTWISE over the whole list, not at the tail; report N at both
     points and RECORD18's unit count, measured by the reviewer as THREE — the
     finding, its FIX line and the gate entry. NEGATIVE CONTROL: alter one
     printable byte of the C2 file's FIRST paragraph at equal length; BOTH readers
     must REJECT it and ACCEPT the true file. Name the offset and the change.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R` keys
     and how many DISTINCT; `Gate: R18`; the MAXIMUM registered id. ONE id is
     minted and no entry is edited, so `- R-` reads 215 then 216 with both
     DISTINCT, the maximum R-0652 then R-0653, `Done: R-` and `Landed: ` 0 at
     BOTH points — constraint 3 explains why those two stay 0 — `Gate: R` keys 17
     then 18 both DISTINCT, `Gate: R18` 0 then 1.
 G7  THE CONTRACT APPEND at C3, with NO pair to apply first:
     `tests/ui_contracts/test_brain_stream_ring.py` at the round base (11962
     bytes, 269 lines) is itself the byte-exact PREFIX of that file at C3, and the
     remainder is EXACTLY one newline plus CONTRACTBADGE plus one newline. The
     reviewer measured the file at C3 as 13034 bytes and 294 lines and the
     remainder as 1072 bytes, 25 lines, sha256
     `8ec6fe0866ae7fc87263f43289894e80dfa4f81e7b8dcedf389bd0e5f2ae23c8`; report
     yours. Do NOT use a per-line count: code repeats lines structurally and a
     count-based reader is satisfied by the wrong bytes (R-0531).
 G8  PEP 8 SPACING. CONTRACTBADGE opens a new top-level class and CARRIES ITS OWN
     LEADING BLANK LINE — its first line is empty on purpose, so the append's one
     newline plus that blank puts exactly two blank lines before `class`. Do not
     trim it. Report the count of blank lines immediately before CONTRACTBADGE's
     `class ` line in the C3 file: it must be 2. Ruff here does not evaluate
     E301-E306 outside preview, so this is COUNTED and not delegated to the
     linter (R-0558).
 G9  THE REPLACED COMPONENT, at C3:
     `apps/ui/src/components/panels/AgentNowCard.tsx` equals ANCFILE2 PLUS ONE
     TERMINATING NEWLINE by `cmp` at exit 0, with a NEGATIVE CONTROL against the
     bare slice that must exit 1. Report both exit codes and the sha256. The
     reviewer measured 1859 bytes, 37 lines, sha256
     `f1e4e3fd72aa18402660e1f96933deca007d78543509b65ac9e71943247febee`; at the
     round base the same path is 1517 bytes and 33 lines and `git ls-tree <round
     base>` DOES list it, so this REPLACES a tracked file and creates nothing.
     Report both readings. Report also, over the C3 file, that the token
     `isActive` occurs 0 times and that `newestActionRow` still occurs.
G10  TYPECHECK, at C3, from `apps/ui` in the PRIMARY checkout: `npx tsc --noEmit`.
     Report the exit code and the working directory. This is the load-bearing
     gate for the `.tsx` change: this repository has NO DOM environment, so
     components are gated by the typechecker and by source contracts, never by
     rendering them. The reviewer could NOT dry-run this one — a fresh worktree
     has no `node_modules` (R-0518) and the symlink that would supply them is
     denied to its session class — so it re-runs this gate itself in the primary
     checkout at review. If it goes RED, STOP and report: G8 of
     self_drive_protocol.md forbids widening scope to route around a red gate.
G11  VITEST, at C3, from `apps/ui` in the PRIMARY checkout, RUN AS
     `npm run test:unit`. That script is defined as literally `vitest run`
     (`apps/ui/package.json` line 11); the bare `npx vitest` spelling is denied to
     both session classes (R-0651). Report the exit code, the file count and the
     test count. This round adds NO vitest case and removes none, so the expected
     reading is UNCHANGED from the round base: 14 files and 196 tests, which the
     reviewer measured by running that command itself at `cd1d56e2`. A change here
     means something was touched that this block did not order.
G12  THE RED CONTROL, on the Python contract, needing no `node_modules` (R-0518).
     In a disposable worktree under `.remedy-wt/` whose name no directory already
     uses, check out C3 and confirm
     `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf` is
     GREEN there first — an already-red tree cannot fail honestly (R-0364). The
     reviewer measured 31 passed. Then, in that worktree's
     `apps/ui/src/components/panels/AgentNowCard.tsx`, RESTORE THE DEFECT by
     replacing the badge line
       `        {isRunning && <span className={styles.liveSmall}><span /> Live</span>}`
     with the latching form R16 shipped, that is
       `        {(isRunning || liveAction !== null) && <span className={styles.liveSmall}><span /> Live</span>}`
     and re-run. That is exactly the defect R-0652 names: a badge keyed to a ring
     that never empties. Confirm the target occurs EXACTLY ONCE in that file,
     counted BOTH whole-line and indent-agnostic with the two counts agreeing, and
     report both. EXACTLY ONE test must fail, and it must be
     `TestTheNowCardBadgeTracksTheAgent::test_the_badge_reads_the_running_flag`.
     Report the failing name, the pass and fail counts and the assertion text; the
     reviewer measured 1 failed, 30 passed. Prune the tree.
G13  THE PYTHON SUITES, at C3 in the PRIMARY checkout, SERIALLY, from the
     REPOSITORY ROOT — a shell left in `apps/ui` makes these exit 4 having run no
     test, which is vacuous and not green. Never run two at once. Report each
     one's exit code, the working directory, and the total, counting BY PASSED
     PLUS SKIPPED, because data-dependent skips make the split vary at an
     unchanged tree:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 458 at the round base,
       which the reviewer measured itself; CONTRACTBADGE adds 3 test functions,
       so the total must read 461.
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511 at base, and they
       read `.agent/plan.md`, so they also guard C1.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/` path.
G14  RANGE, executed at C3 and covering the round base to C3 — NOT to C4, because
     C4 writes the file that must quote this gate and §3 checklist item 31 forbids
     ordering a reading the quoting artefact cannot hold. Report: the base-to-C3
     path set against the six non-handoff paths of `Change:`, the difference EMPTY
     both ways; every commit single-parent; `git show --numstat` and `git diff
     --numstat` agreeing cell by cell with the handback's `## Commits` table (§3
     item 28), any disagreement reported rather than reconciled; insertions under
     the 500 cap; `git ls-files .remedy-wt` 0; `git worktree list` ending with the
     primary checkout alone; and `gh pr list --state open --json
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
            and F021 continues on this branch, that R18's own verdict is
            UNRECORDED and the next round's C2 owes it, and that R19 is the
            recency dot's pure time rule and its wiring.

<<<SLICE ANCFILE2
import type { RemedyDashboard } from "../../api/types";
import type { FeedRow } from "../../api/feedRow";
import { newestActionRow } from "../../api/actionClass";
import { deriveAgentStatus } from "../../cockpitLogic";
import { SparkGlyph, TaskCurrentGlyph } from "../icons/RemedyGlyphs";
import styles from "./RightLivePanel.module.css";

export function AgentNowCard({ dashboard, recent }: { dashboard: RemedyDashboard; recent?: readonly FeedRow[] }) {
  const { status: statusText, detail, isRunning } = deriveAgentStatus(dashboard);
  // The newest ACTION the stream has produced, which is what this card is FOR.
  // Bookkeeping is excluded on purpose (actionClass.ts): a card that narrated
  // the agent reading files would report motion where there was none.
  const liveAction = newestActionRow(recent ?? []);
  // The badge tracks the AGENT, never the ring. brainStream.ts only appends to
  // `recent` and trims it, so a row outlives the job that produced it; a badge
  // keyed to the ring latched on and rendered "Live" beside the word "Idle"
  // forever (R-0652). T5_F021 gives liveness to the recency dot, whose pure
  // rule R19 builds and wires -- until then the honest signal is the agent's.

  return (
    <section className={styles.card}>
      <header className={styles.cardHeader}>
        <h2>Agent is doing now</h2>
        {isRunning && <span className={styles.liveSmall}><span /> Live</span>}
      </header>
      <div className={styles.agentNow}>
        <div className={styles.actorIcon}>
          {isRunning ? <TaskCurrentGlyph style={{ width: 16, height: 16, color: "white" }} /> : <SparkGlyph style={{ width: 16, height: 16, color: "white" }} />}
        </div>
        <div>
          <strong>{statusText}</strong>
          <p>{liveAction ? liveAction.line : detail}</p>
        </div>
      </div>
    </section>
  );
}
<<<END ANCFILE2

<<<SLICE CONTRACTBADGE

class TestTheNowCardBadgeTracksTheAgent:
    """R-0652. The card's live badge must key on the agent's own running flag
    and never on the stream ring: brainStream.ts only appends to `recent` and
    trims it, so a row outlives the job that produced it and a ring-keyed badge
    reads "Live" beside the word "Idle" forever."""

    def test_the_badge_is_not_keyed_to_the_ring(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "isActive" not in code, (
            "a badge keyed to the ring latches on once any action has arrived"
        )

    def test_the_badge_reads_the_running_flag(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "{isRunning && <span" in code, (
            "the live badge must track the agent, not the presence of a row"
        )

    def test_the_detail_line_still_prefers_the_newest_action(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "liveAction ? liveAction.line : detail" in code, (
            "the R16 wiring stays; only the badge changes"
        )
<<<END CONTRACTBADGE

<<<SLICE PLANF021R18
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
R18 retires R-0652: the NowCard's live badge goes back to the agent's own
running flag, because a badge keyed to the stream ring latched on forever once
any action had arrived and rendered "Live" beside the word "Idle". R16's detail
line is unchanged. It also records the R17 verdict, which was PASS on all
fifteen gates, and registers R-0653.

## Next Steps
1. R19 builds the recency dot's PURE time rule — a function of the last action's
   arrival and a passed-in now, so the fade to idle after the quiet window is
   testable without a clock — and wires it, giving the badge and the dot one
   honest liveness source per T5_F021 line 63.
2. R20 wires the scroll rule into `ActivityFeedCard`: the scroll container, and
   the new-rows pill component_spec.md line 86 binds.
3. R21 gives each row its click-jump to the node, the graph-focus API T003 opens
   with, then T003: the disabled steering input with its honest tooltip.

## Risks
- No DOM environment exists in this repository, so components are gated by
  `npx tsc --noEmit` and by Python source contracts, and behaviour is put in
  PURE modules that vitest can reach.
- Vitest IS reviewer-runnable as `npm run test:unit` from `apps/ui` (R-0651),
  but ONLY green: a fresh worktree has no `node_modules` (R-0518) and the
  symlink that would supply them is denied, so no vitest case has ever been
  mutation-proved. Every pure module therefore also carries a Python source
  contract whose red control IS runnable — that is the compensating control,
  and R-0653 records it.
- Reflog gates name the OPERATION field, never the whole row, and marker sweeps
  are LINE-ANCHORED, never containment (R-0613, R-0364).
- No code defect of F021 is open once R18 lands; R-0364, R-0403, R-0607,
  R-0608, R-0609, R-0611, R-0613, R-0622, R-0651 and R-0653 stay routed to a
  paydown branch.
<<<END PLANF021R18

<<<SLICE RECORD18
- R-0653 — Low, THE VITEST SUITE IS GATED GREEN-ONLY: NO VITEST CASE IN THIS REPOSITORY HAS EVER BEEN SHOWN TO FAIL WHEN THE CODE IT COVERS IS BROKEN. Raised by the reviewer at the R17 gate against its own evidence standard, and a direct descendant of R-0651. R-0651 established that `npm run test:unit` from `apps/ui` IS runnable by both session classes, and since R15 the reviewer has executed it every frontend round — 13 files and 185 tests at R16, 14 and 196 at R17. But a suite that only ever runs GREEN proves that the tests pass, not that they would fail; the red control is what separates a test from a decoration, and this repository's guardrail G5 requires destructive checks to run in a disposable worktree. Measured at the R17 gate: a fresh worktree has no `node_modules` (R-0518), `npm run test:unit -- --root <worktree>` fails at startup with `Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'vitest'` because the config's own import cannot resolve, and the `ln -s` that would supply the directory is denied to the reviewer's session class — so the mutation cannot be run anywhere that guardrail G5 permits. The reviewer verified this rather than assuming it, by attempting the run. THE COMPENSATING CONTROL IS ALREADY IN PLACE AND IS WHY THIS IS LOW: every pure module this feature has landed carries a Python source contract as well as its vitest, and the contract's red control IS runnable in a worktree — R17's mutation of `return FEED_SCROLL_START;` to `return prev;` failed exactly one named contract test in the reviewer's own disposable tree. So each rule has one mutation-proved guard; what is missing is proof that the BEHAVIOURAL half would also catch it. Low and not Medium because no test is known to be vacuous, the anchored `it(` count corroborates the suite's own numbers, and the contracts carry the load; but the gap is real and should not be discovered later as a surprise.

  FIX: keep pairing every pure module with a Python source contract whose red control runs in a worktree, and treat the contract as the load-bearing guard while vitest is green-only; if the sandbox ever permits `node_modules` inside a worktree, add a mutation round that red-proves the vitest half and retire this finding.

Gate: R18 — the R17 entry. R17 PASSED ON EVERY ONE OF ITS FIFTEEN GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK. R17 wrote the feed's scroll discipline as a PURE rule in `apps/ui/src/api/feedScroll.ts` — pinned readers are followed, a reader who scrolled up is NEVER moved, and rows arriving meanwhile accumulate as an unseen count that clears only on return to the newest edge — with its vitest and a source contract, and wired nothing, the same headless-then-wire order R15 and R16 used. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own emitted `.remedy-wt/f021-r17.md`, `.agent/authored/f021-r17.md` at `8f676acb` and `.agent/last_block.md` at `8223f301` are ALL FOUR byte-identical, counting the received bytes, at sha256 7732815b36f47b159610793c81933df3973e7d22266ef6be0f5487229a4e75e3 over 33614 bytes and 465 lines. SLICES: 7 over 201 CONTENT lines, TOTAL 465 against DECISION F085 D6's 490 and PROSE 264 against D5's 400, both equal to that block's constraint 9. EVERY SLICE APPLIED BYTE FOR BYTE, verified against slices the reviewer extracted mechanically from the committed C0a blob: `.agent/plan.md` at `b45d0242` equals PLANF021R17 plus one terminating newline and NOT the bare slice, at 48 lines with `## Goal` and `## Next Steps` once each; `feedScroll.ts` at `cd1d56e2` is 2254 bytes / 50 lines / sha256 18ef679bdef07998b0179c5013056a67a0999671f377be2b215c50c34737e205 and `feedScroll.test.ts` 2043 bytes / 64 lines / sha256 816df6037f463746aaedda9a7417ecb6595f0d24dc2a505699d84871acabbcd6, each equal to its slice plus one terminator and not to the bare slice, and BOTH ABSENT from `git ls-tree` at the round base, so the round created them; the ledger append at `bbf28b28` is the base blob plus one newline plus RECORD17 plus one newline, remainder sha256 14feb550812a3b6cd59b96cfa13341d9c8d72591053057c7ac3d9dc230f81dc3 over 7534 bytes and 6 lines, units 237 to 240 ELEMENTWISE equal with RECORD17 exactly 3 units, and a negative control at offset 2 of the FIRST paragraph — the byte `L` set to `X` at equal length — that BOTH readers rejected while both accepted the true file; and the contract append is the CONTRACTPATHS4-substituted base blob (10570 bytes, from 10535 B / 236 L) plus one newline plus CONTRACTSCROLL plus one newline, remainder sha256 224ed5417f81cc6a80dca71a5f0d756f631bc40a8180abd20cf29e857cf989f4 over 1392 bytes and 32 lines — A DIGEST THE REVIEWER PREDICTED FROM ITS OWN DRY RUN BEFORE DELEGATING AND WHICH THE APPLIED BYTES REPRODUCED EXACTLY — with EXACTLY TWO blank lines before the new top-level class, counted rather than delegated to a linter that does not evaluate E301-E306 outside preview. THE ONE PAIR BEHAVED BY SHAPE: CONTRACTPATHS4 is append-shaped and read FROM 1 / TO 0 at the round base and FROM 1 / TO 1 at C3, all four numbers as predicted. THE LEDGER MOVED ONLY AS ORDERED: `- R-` 214 to 215 all DISTINCT at both points, maximum R-0651 to R-0652, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 16 to 17 both DISTINCT, `Gate: R17` 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially from the repository root and counting by passed plus skipped: `tests/ui_contracts/` 458, the ordered rise of exactly 3 over the base's 454 that CONTRACTSCROLL's three cases predict; the three state-reading suites 511; the canary 42; and `npx tsc --noEmit` in `apps/ui` exit 0 with output EMPTY. THE ONE GATE THE REVIEWER COULD NOT DRY-RUN WAS EXECUTED AT REVIEW AND CONFIRMED ITS PREDICTION: `npm run test:unit` in `apps/ui` read 14 files and 196 tests, exactly the round base's 13 and 185 plus one file and the eleven cases an ANCHORED `it(` scan of FEEDSCROLLTEST had counted before delegation. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `cd1d56e2`: green first at 28 passed, then with `    return FEED_SCROLL_START;` replaced by `    return prev;` — a target the reviewer confirmed occurs EXACTLY ONCE, whole-line and indent-agnostic counts agreeing — exactly 1 failed and 27 passed, the failure being `TestTheFeedScrollRuleIsPureAndHeadless::test_the_unseen_count_clears_at_the_newest_edge`. THE RANGE HELD: five commits base to C3, every one single-parent, the path set EQUAL to that block's seven non-handoff `Change:` paths with both differences EMPTY, `git show --numstat` and `git diff --numstat` agreeing cell by cell with the handback's tables, insertions 465, 378, 19, 6 and 147 every one under the 500 cap, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone, `gh pr list --state open` EMPTY, and the reflog read BY OPERATION over this round's rows every one `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE MARKER SWEEP WAS LINE-ANCHORED: 0 anchored in every one of the five files a slice landed in, while `.agent/live_review.md` reads 2 under the containment reading. THE WORKER DECLARED NO DEVIATION and none was found; its handback's 94 lines against the 60-line cap are within the 100 AGENTS.md permits for more than five commits, with mandated content as the stated cause. WHY R17 IS PASS: every slice is byte-identical to the slices the reviewer extracted itself, both predicted digests were reproduced by the applied bytes, the red control fails in the reviewer's own worktree on the one named test, and the single gate that could not be dry-run was run at review and matched. R-0652 IS REPAIRED BY C3 OF THIS BLOCK, which puts the NowCard's badge back on `isRunning` and pins it with a contract whose own red control restores the latching form and fails on it; R-0652's original paragraph is deliberately NOT edited, per R-0470.
<<<END RECORD18
