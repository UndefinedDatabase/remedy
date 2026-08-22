── STEP NOWCARD — F021 ──
Goal:        Make the NowCard show what the agent is ACTUALLY doing. R15 built
             the ACTION class and nothing rendered it; this round wires
             `newestActionRow` into `AgentNowCard` through the ring the panel
             already receives, so the card's detail line becomes the newest
             ACTION the stream produced and falls back to the dashboard's own
             text when the stream has produced none. That retires the orphan
             R15 deliberately left and the plan named. No new CSS class, asset,
             icon or font: `card`, `cardHeader`, `liveSmall`, `agentNow` and
             `actorIcon` all already exist in `RightLivePanel.module.css`, and
             both glyphs are already imported. The round also records the R15
             verdict, which was PASS, and registers ONE finding.

Fortschritt: ~80 % (T002 fast fertig — Feed und NowCard haengen jetzt beide am
             Stream; es fehlen Scroll-Disziplin, der Recency-Dot und T003)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R15 verdict
             and R-0651 · C3 the NowCard wiring and its contract · C4 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r16.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/components/panels/AgentNowCard.tsx` (C3) ·
             `apps/ui/src/components/panels/RightLivePanel.tsx` (C3) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C3) ·
             `.agent/handoff.md` (C4).
             Resolve any count in this block against that list.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). ROUND BASE is `2d0532dad72e74ed0e8ecb2dd6292d12e6144673` and is
    the commit every "round base" in this block names.
 3. THIS ROUND REGISTERS EXACTLY ONE FINDING AND RESOLVES NONE. R15 passed
    every one of its fifteen gates under the reviewer's own re-measurement.
    Before this round: 213 open, maximum R-0650. RECORD16 registers R-0651 and
    records the R15 gate, so after C2: 214 open, maximum R-0651, next free
    R-0652. R-0651 is NEW rather than filed against an existing id because §3
    checklist item 30's search of the open set for the DEFECT returned no hit:
    the defect is that the reviewer's own risk register asserted a verification
    gap — that a frontend round's vitest colour can only rest on the worker's
    transcript — which does not exist, and no open finding says that.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice is quoted WITHOUT a
    trailing newline. A WHOLE-FILE write (PLANF021R16, ANCFILE) is the slice
    PLUS one terminator. An APPEND (RECORD16, CONTRACTNOW) is one newline, then
    the slice, then one terminator, so the target keeps exactly one. A FROM/TO
    PAIR substitutes in place, neither side carrying a terminator and the
    file's own untouched. The gates match each kind.
 5. PAIRS BEFORE APPENDS, READ PER TARGET FILE. Within any ONE file every pair
    is applied before any append to that same file. ONE file takes both:
    `tests/ui_contracts/test_brain_stream_ring.py` takes CONTRACTPATHS3 first
    and CONTRACTNOW second, in that order. `RightLivePanel.tsx` takes only the
    RLP3 pair; `AgentNowCard.tsx` is a whole-file write, not a pair.
 6. THE ARCHITECTURE LINE HOLDS. The NowCard receives the ring as a PROP from
    `RightLivePanel`, which already receives it from the one `useBrainStream`
    call in `RemedyShell`. Do not add a second call, do not add a hook, do not
    construct an `EventSource`, and do not edit `RemedyShell.tsx`,
    `brainStream.ts`, `brainStreamRunner.ts`, `feedRow.ts`, `actionClass.ts` or
    `ActivityFeedCard.tsx` — earlier rounds built them all.
 7. NO NEW VISUAL VOCABULARY. `docs/ui/design_reference/` is binding and
    `assets_spec.md` is the asset authority. Every class ANCFILE uses — `card`,
    `cardHeader`, `liveSmall`, `agentNow`, `actorIcon` — already exists in
    `RightLivePanel.module.css`, and `SparkGlyph` and `TaskCurrentGlyph` are
    already imported by the file being replaced. Add no CSS, no asset and no
    icon, so no `assets_spec.md` update and no assumption-log entry is owed. Do
    not introduce the token `@mui`, do not introduce the token `POST`, and do
    not remove the heading text `Agent is doing now`.
 8. Run no formatter or linter that rewrites a file in place; `npm run lint` in
    `apps/ui` is RED at base (R-0622), is not a gate here and must not be
    "fixed" in passing. Create and merge NO pull request: F021 is mid-feature.
    Push the branch after C4.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 383
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 274 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C4; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is
     ordered NOWHERE — §3 item 31 leaves it to the next round. Report also, as
     the reading THIS round owes from the last, that the R15 handback commit
     `2d0532da` is single-parent and touches `.agent/handoff.md` alone at 43
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r16.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r16.md` are all equal. Write
     C0b FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their `<<<SLICE `/
     `<<<END ` marker LINES; report how many slices and how many CONTENT lines
     that extractor printed, and re-measure constraint 9's two numerals from
     that same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R16 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare
     slice that must exit 1. Report both exit codes, that the last byte is a
     newline, `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, remainder EXACTLY one newline plus
     RECORD16 plus one newline — report its sha256, byte and line counts, and
     the file's byte and line counts before and after. Reader (b), SET-WISE:
     strip the one trailing terminator from BOTH blobs, split each on the blank
     line into units, and confirm the C2 unit LIST equals the base list
     followed by RECORD16's own units, ELEMENTWISE over the whole list, not at
     the tail; report N at both points and RECORD16's unit count, measured by
     the reviewer as THREE — the finding, its FIX line and the gate entry, which
     is the shape R-0649 and R-0650 already use in this ledger. NEGATIVE
     CONTROL: alter one printable byte of the C2 file's FIRST paragraph at equal
     length; BOTH readers must REJECT it and ACCEPT the true file. Name the
     offset and the change.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R`
     keys and how many DISTINCT; `Gate: R16`; the MAXIMUM registered id. ONE id
     is minted and none resolved, so `- R-` reads 213 then 214 with both
     DISTINCT, the maximum R-0650 then R-0651, `Done: R-` and `Landed: ` 0 at
     both, `Gate: R` keys 15 then 16 both DISTINCT, `Gate: R16` 0 then 1.
 G7  THE TWO PAIRS, at C3, counted by WHOLE-STRING search over raw bytes rather
     than line by line. THE EXPECTED COUNTS DIFFER BY PAIR SHAPE, as the
     reviewer measured on its dry run. CONTRACTPATHS3 is APPEND-SHAPED — its TO
     CONTAINS its FROM — so it reads FROM 1 and TO 0 at the round base and FROM
     1 and TO 1 at C3; a gate demanding FROM 0 would fail on a correct
     application (R-0640). RLP3 is REPLACING and reads FROM 1 and TO 0 at the
     round base and FROM 0 and TO 1 at C3. Report all eight numbers. If either
     FROM count at the round base is not 1, STOP and report rather than
     choosing an occurrence.
 G8  THE CONTRACT APPEND at C3: `tests/ui_contracts/test_brain_stream_ring.py`
     at the round base (9367 bytes, 210 lines) WITH CONTRACTPATHS3's
     substitution applied to it in memory (9431 bytes) is a byte-exact PREFIX
     of that file at C3, and the remainder is EXACTLY one newline plus
     CONTRACTNOW plus one newline. Say the prefix side is the substituted blob.
     The reviewer measured the remainder as 1104 bytes, 25 lines, sha256
     `eff284d5939063acf1ce9f0d974160e2e5fc29806927e67aaa5232ff5cd5ea62`; report
     yours. Do NOT use a per-line count: code repeats lines structurally and a
     count-based reader is satisfied by the wrong bytes (R-0531).
 G9  PEP 8 SPACING. CONTRACTNOW opens a new top-level class and CARRIES ITS OWN
     LEADING BLANK LINE — its first line is empty on purpose, so the append's
     one newline plus that blank puts exactly two blank lines before `class `.
     Do not trim it. Report the count of blank lines immediately before
     CONTRACTNOW's `class ` line in the C3 file: it must be 2. Ruff here does
     not evaluate E301-E306 outside preview, so this is COUNTED and not
     delegated to the linter (R-0558).
G10  THE REPLACED COMPONENT, at C3:
     `apps/ui/src/components/panels/AgentNowCard.tsx` equals ANCFILE PLUS ONE
     TERMINATING NEWLINE by `cmp` at exit 0, with a NEGATIVE CONTROL against
     the bare slice that must exit 1. Report both exit codes and the sha256.
     The reviewer measured 1517 bytes, 33 lines, sha256
     `0418f0805c142ca82beea3dfc249299fc6f5f061303faea09e313f13a4a238f0`; at the
     round base the same path is 1009 bytes and 26 lines, so this REPLACES a
     tracked file and does not create one — `git ls-tree <round base>` DOES
     list it. Report both readings.
G11  TYPECHECK, at C3, from `apps/ui` in the PRIMARY checkout: `npx tsc
     --noEmit`. Report the exit code and the working directory. This is the
     load-bearing gate for the two `.tsx` files: this repository has NO DOM
     environment, so components are gated by the typechecker and by source
     contracts, never by rendering them. The reviewer measured exit 0 with
     EMPTY output on its dry run of these exact bytes. If it goes RED, STOP and
     report: G8 of self_drive_protocol.md forbids widening scope to route
     around a red gate.
G12  VITEST, at C3, from `apps/ui` in the PRIMARY checkout, RUN AS
     `npm run test:unit`. That script is defined as literally `vitest run`
     (`apps/ui/package.json` line 11), and it is the form the reviewer can also
     execute — the bare `npx vitest` spelling is denied to both session classes,
     which is the whole substance of R-0651 that this round registers. Report
     the exit code, the file count and the test count. This round adds NO
     vitest case, so the expected reading is UNCHANGED from the round base: 13
     files and 185 tests, which the reviewer measured by running that command
     itself. A rise here means something was added that this block did not
     order.
G13  THE RED CONTROL, on the Python contract, needing no `node_modules`. In a
     disposable worktree under `.remedy-wt/` whose name no directory already
     uses, check out C3 and confirm
     `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf`
     is GREEN there first — an already-red tree cannot fail honestly (R-0364).
     The reviewer measured 24 passed. Then, in that worktree's
     `apps/ui/src/components/panels/RightLivePanel.tsx`, unwire the card by
     replacing
       `      <AgentNowCard dashboard={dashboard} recent={recent} />`
     with the same line WITHOUT its new prop, that is
       `      <AgentNowCard dashboard={dashboard} />`
     and re-run. That is the defect this round exists to prevent: a NowCard
     wired to nothing, which renders the pre-stream fallback forever and looks
     exactly like a quiet agent. Confirm the target occurs EXACTLY ONCE in that
     file, counted BOTH whole-line and indent-agnostic with the two counts
     agreeing, and report both. EXACTLY ONE test must fail, and it must be
     `TestTheNowCardShowsTheNewestAction::test_the_panel_hands_the_ring_to_the_now_card`.
     Report the failing name, the pass and fail counts and the assertion text;
     the reviewer measured 1 failed, 23 passed. Prune the tree.
G14  THE PYTHON SUITES, at C3 in the PRIMARY checkout, SERIALLY, from the
     REPOSITORY ROOT — a shell left in `apps/ui` makes these exit 4 having run
     no test, which is vacuous and not green. Never run two at once. Report
     each one's exit code, the working directory, and the total, counting BY
     PASSED PLUS SKIPPED, because data-dependent skips make the split vary at
     an unchanged tree:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 451 at the round base;
       CONTRACTNOW adds 3 test functions, which the reviewer counted on its dry
       run, so the total must read 454.
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511 at base, and they
       read `.agent/plan.md`, so they also guard C1.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/` path.
G15  RANGE, executed at C3 and covering the round base to C3 — NOT to C4,
     because C4 writes the file that must quote this gate and §3 checklist item
     31 forbids ordering a reading the quoting artefact cannot hold. Report:
     the base-to-C3 path set against the seven non-handoff paths of `Change:`,
     the difference EMPTY both ways; every commit single-parent; `git show
     --numstat` and `git diff --numstat` agreeing cell by cell with the
     handback's `## Commits` table (§3 item 28), any disagreement reported
     rather than reconciled; insertions under the 500 cap; `git ls-files
     .remedy-wt` 0; `git worktree list` ending with the primary checkout alone;
     and `gh pr list --state open --json number,headRefName` — expected EMPTY —
     with the statement that neither `gh pr create` nor `gh pr merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED, as R15 established: count lines whose
     FIRST CHARACTERS are `<<<SLICE ` or `<<<END `, never lines that merely
     CONTAIN either token. Under the containment reading `.agent/live_review.md`
     reads nonzero at the round base — prose in earlier entries quotes the
     marker text — so that clause would be red at base and could not fail
     honestly (R-0364). Report the LINE-ANCHORED count for every file a slice
     landed in; each must be 0.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog
     --format=%gs`, take the OPERATION only — the text BEFORE the first `:` —
     and scope to THIS ROUND'S rows, those from the round base forward. Report
     that every such row's operation is `commit` and that `amend`, `rebase` and
     `cherry` each occur 0 times in that OPERATION field. A substring count
     over whole rows is NOT this gate: this repository's commit subjects
     discuss amends by design, so that count is nonzero and says nothing about
     history rewriting.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, ONE LINE
            PER GATE with transcripts kept out of the file (R-0582), and the
            `Fortschritt:` line verbatim across all three of its lines. Report
            its own `wc -l` against the 60-line cap, with a DECISION D15 line
            declaring any overage and its mandated cause. Every `## Commits`
            heading carries that commit's FULL subject, and where a commit
            cannot name its own SHA the role and reason go INSIDE the heading
            (R-0494). `## Next` states that THIS SESSION ENDS with C4, that the
            next session's FIRST action is docs/agents/self_drive_protocol.md
            Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR
            Gate (R-0347), that rule 2 will find NO open pull request so rule 5
            applies and F021 continues on this branch, that R16's own verdict
            is UNRECORDED and the next round's C2 owes it, and that R17 is the
            scroll discipline that never yanks a reader who has scrolled up.

<<<SLICE RLP3 FROM
      <AgentNowCard dashboard={dashboard} />
<<<END RLP3 FROM

<<<SLICE RLP3 TO
      <AgentNowCard dashboard={dashboard} recent={recent} />
<<<END RLP3 TO

<<<SLICE CONTRACTPATHS3 FROM
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
<<<END CONTRACTPATHS3 FROM

<<<SLICE CONTRACTPATHS3 TO
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
NOWCARD = UI_SRC / "components" / "panels" / "AgentNowCard.tsx"
<<<END CONTRACTPATHS3 TO

<<<SLICE ANCFILE
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
  const isActive = isRunning || liveAction !== null;

  return (
    <section className={styles.card}>
      <header className={styles.cardHeader}>
        <h2>Agent is doing now</h2>
        {isActive && <span className={styles.liveSmall}><span /> Live</span>}
      </header>
      <div className={styles.agentNow}>
        <div className={styles.actorIcon}>
          {isActive ? <TaskCurrentGlyph style={{ width: 16, height: 16, color: "white" }} /> : <SparkGlyph style={{ width: 16, height: 16, color: "white" }} />}
        </div>
        <div>
          <strong>{statusText}</strong>
          <p>{liveAction ? liveAction.line : detail}</p>
        </div>
      </div>
    </section>
  );
}
<<<END ANCFILE

<<<SLICE CONTRACTNOW

class TestTheNowCardShowsTheNewestAction:
    """The NowCard half of T5_F021. The card must read the ACTION class rather
    than the raw ring, and the panel must hand it the ring at all -- a card
    wired to nothing renders the pre-stream fallback forever."""

    def test_the_now_card_reads_the_action_class(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "newestActionRow" in code, (
            "the NowCard must select through the ACTION class, not the raw ring"
        )
        assert "recent ?? []" in code

    def test_the_panel_hands_the_ring_to_the_now_card(self):
        code = strip_ts_comments(PANEL.read_text())
        assert "<AgentNowCard dashboard={dashboard} recent={recent} />" in code, (
            "the NowCard is wired to nothing and shows the fallback forever"
        )

    def test_the_now_card_falls_back_when_nothing_acted(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "liveAction ? liveAction.line : detail" in code, (
            "with no action yet the card still says what the dashboard knows"
        )
<<<END CONTRACTNOW

<<<SLICE PLANF021R16
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
R16 wires `newestActionRow` into `AgentNowCard` through the ring the panel
already receives, so the card's detail line becomes the newest ACTION the stream
produced and falls back to the dashboard's own text when there is none. That
retires the orphan R15 left deliberately. It also records the R15 verdict, which
was PASS on every gate, and registers R-0651.

## Next Steps
1. R17 adds the scroll discipline that never yanks a reader who has scrolled up.
2. R18 adds the recency dot over a PURE time function, so the fade to idle after
   the quiet window is testable without a clock.
3. R19 gives each row its click-jump to the node, the graph-focus API T003 opens
   with, then T003: the disabled steering input with its honest tooltip.

## Risks
- No DOM environment exists in this repository, so components are gated by
  `npx tsc --noEmit` and by Python source contracts. A contract that reads a
  prop name is the only thing standing between "published" and "rendered".
- Vitest IS reviewer-runnable as `npm run test:unit` from `apps/ui`; only the
  bare `npx vitest` spelling is denied (R-0651). Gate it that way and re-run it
  at review. It stays vacuous in a fresh worktree, which has no `node_modules`
  (R-0518), unless that directory is symlinked in.
- Reflog gates name the OPERATION field, never the whole row, and marker sweeps
  are LINE-ANCHORED, never containment (R-0613, R-0364).
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622 and R-0651 stay routed to a paydown branch.
<<<END PLANF021R16

<<<SLICE RECORD16
- R-0651 — Low, THE REVIEWER'S OWN RISK REGISTER ASSERTED A VERIFICATION GAP THAT DOES NOT EXIST, SO ELEVEN FRONTEND ROUNDS ACCEPTED A WORKER'S TRANSCRIPT FOR A GATE THE REVIEWER COULD HAVE RUN ITSELF. Raised by the reviewer at the R15 gate against its own standing assumption. From R12 onward every F021 block carried a risk line saying `npx vitest run` is DENIED to the reviewer's session class and that a frontend round's vitest colour therefore "rests on the worker's transcript", and every such round fell back to corroborating the worker's numbers with a static count of `it(` over the committed test sources instead of executing the suite. Measured at the R15 gate: the bare `npx vitest run` spelling IS denied, but `npm run test:unit` from `apps/ui` is ALLOWED to the reviewer's session class and is defined in `apps/ui/package.json` line 11 as literally `vitest run` — the same binary, the same arguments, the same working directory. The reviewer ran it at `0e1fe68f` and read 13 files and 185 tests, which is exactly what R15's worker reported through the same substituted command as its declared deviation D1. So the evidence was recoverable all along and the gap was in the assumption, not in the sandbox. Low rather than Medium because no round was actually mis-verified — every affected round's static corroboration agreed with the transcript it corroborated, and R15's reading has now been reproduced directly — but the assumption weakened the evidence standard for eleven rounds and would have kept doing so. Two further facts belong with it: a fresh worktree still reports a vacuous vitest result because it has no `node_modules` (R-0518), unless that directory is symlinked in, which the reviewer did on its R16 dry run to typecheck a `.tsx` change outside the primary checkout; and the static corroborator must be ANCHORED — a raw substring count of `it(` reads 190 where the true count is 177, because `await(`, `emit(` and `split(` all contain the token, so only a scan for lines whose first non-blank text is `it(` reproduces the suite's own number.

  FIX: gate vitest as `npm run test:unit` from `apps/ui` in the PRIMARY checkout and re-run it at review rather than corroborating it; keep the anchored `it(` count as a cross-check, never as the primary evidence; and state in any risk register that only the `npx` spelling is denied.

Gate: R16 — the R15 entry. R15 PASSED ON EVERY ONE OF ITS FIFTEEN GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND IT SURFACES THE ONE FINDING REGISTERED IMMEDIATELY ABOVE. R15 built the ACTION class T5_F021 rules the NowCard over — heartbeats and bookkeeping excluded — as headless DATA in `apps/ui/src/api/actionClass.ts`, classified by EXCLUSION over a suffix rule so that a kind computed at runtime is never silently demoted, with `newestActionRow` scanning the oldest-first ring from its end. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own emitted `.remedy-wt/f021-r15.md`, `.agent/authored/f021-r15.md` at `f94b7c38` and `.agent/last_block.md` at `fde9a33c` are ALL THREE byte-identical at sha256 b88476eb2ec56f8b9fb9ec2d3e913534e71bc704b49d13baa4e9903853de3b45 over 31648 bytes and 438 lines. SLICES: 7 over 177 CONTENT lines, TOTAL 438 against DECISION F085 D6's 490 and PROSE 261 against D5's 400, both equal to that block's constraint 9. EVERY SLICE APPLIED BYTE FOR BYTE, verified against slices the reviewer extracted mechanically from the committed C0a blob: `.agent/plan.md` at `038d2814` equals PLANF021R15 plus one terminating newline and NOT the bare slice, at 44 lines; `actionClass.ts` and `actionClass.test.ts` at `0e1fe68f` each equal their slice plus one terminator and not the bare slice, at 1836 bytes / 43 lines / sha256 4c07fc6479e952f3aa35b08863a8555601e361323157d2b663b2fecc92d71dc2 and 2116 bytes / 53 lines / sha256 6be673a43de39507fca0a48afc4f3bc0bcbaccf678e37902902bf8464a64eaa4, both absent from `git ls-tree` at the round base; the ledger append at `7b8c6c11` is the base blob plus one newline plus RECORD14 plus one newline, remainder sha256 edf8b0f171147848dcad8942b9302b8aa97a563c7c755bbcedab7acba886f4fe over 6135 bytes and 2 lines, units 233 to 234 ELEMENTWISE equal, with a negative control at offset 2 of the FIRST paragraph that BOTH readers rejected while both accepted the true file; and the contract append is the CONTRACTPATHS2-substituted base blob (7773 bytes, from 7737) plus one newline plus CONTRACTACTION plus one newline, remainder sha256 20589d2a7ff05a9fd09b59730a37207cc6402d82ce7ffe86d521751168838bcf over 1594 bytes and 34 lines — a digest the reviewer had PREDICTED from its own dry run BEFORE delegating and which the applied bytes reproduced exactly — with EXACTLY TWO blank lines before the new top-level class, counted rather than delegated to a linter that does not evaluate E301-E306 outside preview. THE ONE PAIR BEHAVED BY SHAPE: CONTRACTPATHS2 is append-shaped and read FROM 1 / TO 0 at the round base and FROM 1 / TO 1 at C3, all four numbers as predicted. THE LEDGER MOVED ONLY AS ORDERED: `- R-` 213 at both points all DISTINCT, maximum R-0650 at both, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 14 to 15 both DISTINCT, `Gate: R15` 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially from the repository root and counting by passed plus skipped: `tests/ui_contracts/` 447 passed and 4 skipped for 451, a rise of exactly 4 over the base's 447 equal to CONTRACTACTION's four cases; the three state-reading suites 511; the canary 42; and `npx tsc --noEmit` in `apps/ui` exit 0 with output EMPTY. THE GATE EVERY PREVIOUS ROUND ONLY CORROBORATED WAS THIS TIME EXECUTED BY THE REVIEWER: `npm run test:unit` in `apps/ui` read 13 files and 185 tests, all passing, matching both the worker's D1 reading and the reviewer's anchored `it(` count of 13 files and 185 cases at C3 against 12 and 177 at the round base, a rise of exactly 8 equal to ACTIONTEST's eight cases. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `0e1fe68f`: green first at 21 passed, then with `"_inspected", ` dropped from the exclusion list — a target the reviewer confirmed occurs EXACTLY ONCE, whole-line and indent-agnostic counts agreeing — exactly 1 failed and 20 passed, the failure being `TestTheActionClassIsDocumentedAndHeadless::test_the_inspection_suffixes_are_excluded` with the assertion "_inspected is bookkeeping the NowCard must stay quiet about". THE RANGE HELD: five commits base to C3, every one single-parent, the path set EQUAL to that block's seven non-handoff `Change:` paths with both differences EMPTY, `git show --numstat` and `git diff --numstat` agreeing cell by cell with the handback's table at 438/0, 312/314, 18/18, 2/0 and 53/0 + 43/0 + 35/0, insertions 438, 312, 18, 2 and 131 every one under the 500 cap, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone, `gh pr list --state open` EMPTY, and the reflog read BY OPERATION over this round's rows every one `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE R14 COUNTER-MEASURE WORKED AND WAS MEASURED: R15's G15 ordered the marker sweep LINE-ANCHORED, and at C3 `.agent/live_review.md` reads 0 anchored while reading 2 under containment — the containment number having GROWN because RECORD14 itself quotes the marker text — so the clause that was unmeetable at R14 is clean at R15 for the reason the counter-measure predicted. R15's WORKER DECLARED TWO DEVIATIONS AND BOTH ARE SOUND: D1 substituted `npm run test:unit` for a denied `npx vitest run`, which the reviewer verified is the same script and then reproduced itself, and which is the substance of R-0651; D2 is a handback of 84 lines against the 60-line cap, within the 100 AGENTS.md permits for more than five commits, with mandated content as its stated cause and no section dropped. WHY R15 IS PASS: every slice is byte-identical to the slices the reviewer extracted itself, every gate reproduces under the reviewer's own execution including the one previous rounds could not run, the red control fails in the reviewer's own worktree on the one named test, the append digest matched a prediction made before delegation, and both declared deviations are accurate.
<<<END RECORD16
