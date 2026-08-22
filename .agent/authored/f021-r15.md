── STEP ACTION-CLASS — F021 ──
Goal:        Give the NowCard the subset it is supposed to track. T5_F021 rules
             it over "a documented subset — heartbeats and bookkeeping
             excluded", and no such subset exists yet. This round builds it as
             DATA: `actionClass.ts` classifies a kind by EXCLUSION over a suffix
             rule, `newestActionRow` picks the newest ACTION row out of the
             oldest-first ring, and both are pinned by vitest and by a source
             contract. NOTHING RENDERS THIS ROUND — R16 wires it into
             `AgentNowCard`, the same build-then-wire rhythm R13 and R14 used,
             and the plan says so rather than leaving a module nobody calls.
             The round also records the R14 verdict, which was PASS.

Fortschritt: ~75 % (T002 zu drei Vierteln — der Live-Feed steht, die
             ACTION-Klasse ist jetzt definiert und getestet; es fehlen
             NowCard-Anbindung, Scroll-Disziplin und T003)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R14 verdict
             · C3 the action class, its vitest and its contract · C4 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r15.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/api/actionClass.ts` (NEW, C3) ·
             `apps/ui/src/api/actionClass.test.ts` (NEW, C3) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C3) ·
             `.agent/handoff.md` (C4).
             Resolve any count in this block against that list.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). ROUND BASE is `f5e42cec6e7d8908f695370aa302586268129e55` and is
    the commit every "round base" in this block names.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. R14 passed every one of
    its fourteen gates under the reviewer's own re-measurement. 213 open,
    maximum R-0650, next free R-0651. The ONE deviation R14 declared is
    recorded in RECORD14 AGAINST OPEN R-0364 rather than under a new id,
    because §3 checklist item 30 requires the open set to be searched for the
    DEFECT first and that search returned a hit: R-0364 is "a gate whose
    expected value the reviewer never measured at base, already red before the
    round began", which is exactly the marker clause's shape.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice is quoted WITHOUT a
    trailing newline. A WHOLE-FILE write (PLANF021R15, ACTIONCLASS, ACTIONTEST)
    is the slice PLUS one terminator. An APPEND (RECORD14, CONTRACTACTION) is
    one newline, then the slice, then one terminator, so the target keeps
    exactly one. A FROM/TO PAIR substitutes in place, neither side carrying a
    terminator and the file's own untouched. The gates match each kind.
 5. PAIRS BEFORE APPENDS, READ PER TARGET FILE. Within any ONE file every pair
    is applied before any append to that same file, because a pair can only be
    disturbed by an append to the file it matches in. ONE file takes both:
    `tests/ui_contracts/test_brain_stream_ring.py` takes CONTRACTPATHS2 first
    and CONTRACTACTION second, in that order. No pair touches
    `.agent/live_review.md`.
 6. THE MODULE STAYS HEADLESS AND THE ARCHITECTURE LINE HOLDS. `actionClass.ts`
    imports ONE type from `./feedRow` and nothing else. Import no component, no
    React hook and no CSS. Do not add a `useBrainStream` call, do not construct
    an `EventSource`, and do not edit `brainStream.ts`, `brainStreamRunner.ts`,
    `feedRow.ts`, `humanize.ts` or `humanizeCatalog.ts` — R12, R13 and R14
    built them and this round only READS the catalog, from its test.
 7. NO VISUAL CHANGE AT ALL. No `.tsx` file is touched, so no class, asset,
    icon or font is added and no `assets_spec.md` update or assumption-log
    entry is owed. `docs/ui/design_reference/` is untouched and binding.
 8. Run no formatter or linter that rewrites a file in place; `npm run lint` in
    `apps/ui` is RED at base (R-0622), is not a gate here and must not be
    "fixed" in passing. Create and merge NO pull request: F021 is mid-feature.
    Push the branch after C4.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 438
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 261 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C4; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is
     ordered NOWHERE — §3 item 31 leaves it to the next round. Report also, as
     the reading THIS round owes from the last, that the R14 handback commit
     `f5e42cec` is single-parent and touches `.agent/handoff.md` alone at 44
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r15.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r15.md` are all equal. Write
     C0b FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their `<<<SLICE `/
     `<<<END ` marker LINES; report how many slices and how many CONTENT lines
     that extractor printed, and re-measure constraint 9's two numerals from
     that same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R15 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare
     slice that must exit 1. Report both exit codes, that the last byte is a
     newline, `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, remainder EXACTLY one newline plus
     RECORD14 plus one newline — report its sha256, byte and line counts, and
     the file's byte and line counts before and after. Reader (b), SET-WISE:
     strip the one trailing terminator from BOTH blobs, split each on the blank
     line into units, and confirm the C2 unit LIST equals the base list
     followed by RECORD14's own units, ELEMENTWISE over the whole list, not at
     the tail; report N at both points and RECORD14's unit count, measured by
     the reviewer as ONE. NEGATIVE CONTROL: alter one printable byte of the C2
     file's FIRST paragraph at equal length; BOTH readers must REJECT it and
     ACCEPT the true file. Name the offset and the change.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R`
     keys and how many DISTINCT; `Gate: R15`; the MAXIMUM registered id.
     Nothing is minted, so `- R-` reads 213 at BOTH points with both DISTINCT,
     the maximum R-0650 at BOTH, `Done: R-` and `Landed: ` 0 at both, `Gate: R`
     keys 14 then 15 both DISTINCT, `Gate: R15` 0 then 1.
 G7  THE ONE PAIR, at C3, counted by WHOLE-STRING search over raw bytes rather
     than line by line. CONTRACTPATHS2 is APPEND-SHAPED — its TO text CONTAINS
     its FROM text — so a gate demanding FROM 0 would fail on a correct
     application (R-0640). The reviewer measured on its dry run: at the ROUND
     BASE the FROM reads 1 and the TO reads 0; at C3 the FROM reads 1 and the
     TO reads 1. Report all four numbers. If the FROM count at the round base
     is not 1, STOP and report rather than choosing an occurrence.
 G8  THE CONTRACT APPEND at C3: `tests/ui_contracts/test_brain_stream_ring.py`
     at the round base (7737 bytes, 175 lines) WITH CONTRACTPATHS2's
     substitution applied to it in memory is a byte-exact PREFIX of that file
     at C3, and the remainder is EXACTLY one newline plus CONTRACTACTION plus
     one newline. Say the prefix side is the substituted blob. The reviewer
     measured the remainder as 1594 bytes, 34 lines, sha256
     `20589d2a7ff05a9fd09b59730a37207cc6402d82ce7ffe86d521751168838bcf`; report
     yours. Do NOT use a per-line count: code repeats lines structurally and a
     count-based reader is satisfied by the wrong bytes (R-0531).
 G9  PEP 8 SPACING. CONTRACTACTION opens a new top-level class and CARRIES ITS
     OWN LEADING BLANK LINE — its first line is empty on purpose, so the
     append's one newline plus that blank puts exactly two blank lines before
     `class `. Do not trim it. Report the count of blank lines immediately
     before CONTRACTACTION's `class ` line in the C3 file: it must be 2. Ruff
     here does not evaluate E301-E306 outside preview, so this is COUNTED and
     not delegated to the linter (R-0558).
G10  THE TWO NEW FILES, at C3, each equal to its slice PLUS ONE TERMINATING
     NEWLINE by `cmp` at exit 0, each with a NEGATIVE CONTROL against the bare
     slice that must exit 1. Report four exit codes and both sha256 values. The
     reviewer measured `apps/ui/src/api/actionClass.ts` at 1836 bytes, 43 lines,
     sha256
     `4c07fc6479e952f3aa35b08863a8555601e361323157d2b663b2fecc92d71dc2`, and
     `apps/ui/src/api/actionClass.test.ts` at 2116 bytes, 53 lines, sha256
     `6be673a43de39507fca0a48afc4f3bc0bcbaccf678e37902902bf8464a64eaa4`. Both
     paths are NEW: `git ls-tree <round base>` must not list either.
G11  TYPECHECK, at C3, from `apps/ui` in the PRIMARY checkout: `npx tsc
     --noEmit`. Report the exit code and the working directory. The reviewer
     measured exit 0 with EMPTY output at the round base, so any output here is
     this round's doing. A FRESH WORKTREE CANNOT RUN THIS — it has no
     `node_modules` and prints "This is not the tsc command you are looking
     for", which the reviewer reproduced, so a worktree reading is vacuous and
     is not this gate (R-0518). If it goes RED, STOP and report: G8 of
     self_drive_protocol.md forbids widening scope to route around a red gate.
G12  VITEST, at C3, from `apps/ui` in the PRIMARY checkout: `npx vitest run`.
     Report the exit code, the file count and the test count. The round base
     reads 12 files and 177 tests; ACTIONTEST adds ONE file holding EIGHT
     cases, which the reviewer counted by an anchored scan for a line whose
     first non-blank text is `it(` over the committed test sources — that
     scanner reproduces 177 exactly at the base — so the expected reading is 13
     files and 185 tests. Report the ACTUAL numbers and do not reconcile a
     disagreement; its colour rests on your transcript, since `npx vitest` is
     denied to the reviewer's session class.
G13  THE RED CONTROL, on the Python contract, needing no `node_modules`. In a
     disposable worktree under `.remedy-wt/` whose name no directory already
     uses, check out C3 and confirm
     `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf`
     is GREEN there first — an already-red tree cannot fail honestly (R-0364).
     The reviewer measured 21 passed. Then, in that worktree's
     `apps/ui/src/api/actionClass.ts`, break the exclusion rule by replacing
       `  "_inspected", "_read", "_loaded", "_recalled", "_assessed",`
     with the same line WITHOUT its first suffix, that is
       `  "_read", "_loaded", "_recalled", "_assessed",`
     and re-run. That is the defect this round exists to prevent: a NowCard
     that narrates the agent reading files as though it were working. Confirm
     the target occurs EXACTLY ONCE in that file, counted BOTH whole-line and
     indent-agnostic with the two counts agreeing, and report both. EXACTLY ONE
     test must fail, and it must be
     `TestTheActionClassIsDocumentedAndHeadless::test_the_inspection_suffixes_are_excluded`.
     Report the failing name, the pass and fail counts and the assertion text;
     the reviewer measured 1 failed, 20 passed. Prune the tree.
G14  THE PYTHON SUITES, at C3 in the PRIMARY checkout, SERIALLY, from the
     REPOSITORY ROOT — a shell left in `apps/ui` makes these exit 4 having run
     no test, which is vacuous and not green. Never run two at once. Report
     each one's exit code, the working directory, and the total, counting BY
     PASSED PLUS SKIPPED, because data-dependent skips make the split vary at
     an unchanged tree:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 447 at the round base;
       CONTRACTACTION adds 4 test functions, which the reviewer counted on its
       dry run, so the total must read 451.
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
     THE MARKER CLAUSE IS LINE-ANCHORED, which is this round's counter-measure
     for the deviation R14 declared: count lines whose FIRST CHARACTERS are
     `<<<SLICE ` or `<<<END `, never lines that merely CONTAIN either token.
     Under the containment reading `.agent/live_review.md` reads 1 at the round
     base — line 1078, a `Gate: R5` entry whose PROSE quotes the marker — so
     that clause is already red at base and cannot fail honestly. Line-anchored
     it reads 0, which the reviewer verified at the base. Report the
     line-anchored count for every file a slice landed in; each must be 0.
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
            `Fortschritt:` line verbatim across all four of its lines. Report
            its own `wc -l` against the 60-line cap, with a DECISION D15 line
            declaring any overage and its mandated cause. Every `## Commits`
            heading carries that commit's FULL subject, and where a commit
            cannot name its own SHA the role and reason go INSIDE the heading
            (R-0494). `## Next` states that THIS SESSION ENDS with C4, that the
            next session's FIRST action is docs/agents/self_drive_protocol.md
            Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR
            Gate (R-0347), that rule 2 will find NO open pull request so rule 5
            applies and F021 continues on this branch, that R15's own verdict
            is UNRECORDED and the next round's C2 owes it, and that R16 wires
            `newestActionRow` into `AgentNowCard` with its recency dot.

<<<SLICE CONTRACTPATHS2 FROM
DEPS = API_DIR / "brainStreamDeps.ts"
<<<END CONTRACTPATHS2 FROM

<<<SLICE CONTRACTPATHS2 TO
DEPS = API_DIR / "brainStreamDeps.ts"
ACTION = API_DIR / "actionClass.ts"
<<<END CONTRACTPATHS2 TO

<<<SLICE ACTIONCLASS
// Which stream events count as the agent DOING something, for the NowCard.
// Remedy deliberately classifies by EXCLUSION over a suffix rule rather than by
// an allow-list of the catalog's kinds: eleven run-log writers compute their
// kind at runtime, so an allow-list would silently demote every kind it has not
// heard of and the NowCard would go quiet exactly when the agent did something
// new. An unknown kind is therefore an ACTION until it is proven bookkeeping.
import type { FeedRow } from "./feedRow";

/** Suffixes of kinds where the agent LOOKED at something rather than changed
 *  it. These are the bookkeeping half T5_F021 excludes from the NowCard. */
const BOOKKEEPING_SUFFIXES: readonly string[] = [
  "_inspected", "_read", "_loaded", "_recalled", "_assessed",
];

/** Bookkeeping kinds no suffix rule catches, named one by one so that adding
 *  one stays a decision someone made rather than a pattern that drifted. */
const BOOKKEEPING_KINDS: readonly string[] = [
  "brain_viewer_prepared",
  "context_budget_optimized",
  "source_context_injected",
  "stream_cap_reached",
  "token_policy_applied",
];

/** True when a kind is the agent acting. Unknown kinds are ACTION on purpose. */
export function isActionKind(kind: string): boolean {
  if (BOOKKEEPING_KINDS.includes(kind)) {
    return false;
  }
  return !BOOKKEEPING_SUFFIXES.some(suffix => kind.endsWith(suffix));
}

/** The newest row the NowCard should show, or null when the stream has produced
 *  nothing but bookkeeping. Scans from the END: `recent` is oldest-first, so the
 *  last ACTION row in it is the newest one. */
export function newestActionRow(recent: readonly FeedRow[]): FeedRow | null {
  for (let i = recent.length - 1; i >= 0; i -= 1) {
    if (isActionKind(recent[i].kind)) {
      return recent[i];
    }
  }
  return null;
}
<<<END ACTIONCLASS

<<<SLICE ACTIONTEST
import { describe, it, expect } from "vitest";
import { isActionKind, newestActionRow } from "./actionClass";
import { STREAM_EVENT_CATALOG } from "./humanizeCatalog";
import type { FeedRow } from "./feedRow";

function rowOf(seq: number, kind: string): FeedRow {
  return { seq, kind, line: kind, known: true, timestamp: "", outcome: "" };
}

describe("isActionKind", () => {
  it("counts an unknown kind as action rather than demoting it", () => {
    expect(isActionKind("a_kind_no_catalog_has_heard_of")).toBe(true);
  });

  it("excludes the inspection suffixes the NowCard stays quiet about", () => {
    expect(isActionKind("brain_node_inspected")).toBe(false);
    expect(isActionKind("git_status_read")).toBe(false);
    expect(isActionKind("project_constitution_loaded")).toBe(false);
    expect(isActionKind("project_memory_recalled")).toBe(false);
    expect(isActionKind("readiness_assessed")).toBe(false);
  });

  it("excludes the named bookkeeping kinds no suffix rule catches", () => {
    expect(isActionKind("stream_cap_reached")).toBe(false);
    expect(isActionKind("token_policy_applied")).toBe(false);
  });

  it("keeps the kinds a human would call the agent working", () => {
    expect(isActionKind("task_run_started")).toBe(true);
    expect(isActionKind("verification_failed")).toBe(true);
    expect(isActionKind("source_patch_applied")).toBe(true);
  });

  it("leaves most of the catalog in the action class", () => {
    const kinds = Object.keys(STREAM_EVENT_CATALOG);
    expect(kinds.filter(isActionKind).length).toBeGreaterThan(kinds.length / 2);
  });
});

describe("newestActionRow", () => {
  it("is null when the stream has produced nothing", () => {
    expect(newestActionRow([])).toBeNull();
  });

  it("is null when every row is bookkeeping", () => {
    expect(newestActionRow([rowOf(1, "git_status_read")])).toBeNull();
  });

  it("returns the newest action row, skipping bookkeeping after it", () => {
    const rows = [rowOf(1, "task_run_started"), rowOf(2, "builder_started"), rowOf(3, "git_status_read")];
    expect(newestActionRow(rows)?.seq).toBe(2);
  });
});
<<<END ACTIONTEST

<<<SLICE CONTRACTACTION

class TestTheActionClassIsDocumentedAndHeadless:
    """T5_F021 rules the NowCard over "a documented subset -- heartbeats and
    bookkeeping excluded". Behaviour is pinned by vitest in actionClass.test.ts;
    these pin the facts a behavioural test cannot see, against COMMENT-STRIPPED
    source so that prose above a definition cannot satisfy a guard (R-0584)."""

    def test_the_action_class_stays_headless(self):
        code = strip_ts_comments(ACTION.read_text())
        assert "components/" not in code, (
            "the action class is data the CLI can reuse, not a component import"
        )
        assert "useState" not in code and "useSyncExternalStore" not in code

    def test_the_inspection_suffixes_are_excluded(self):
        code = strip_ts_comments(ACTION.read_text())
        for suffix in ("_inspected", "_read", "_loaded", "_recalled", "_assessed"):
            assert '"' + suffix + '"' in code, (
                suffix + " is bookkeeping the NowCard must stay quiet about"
            )

    def test_an_unknown_kind_stays_in_the_action_class(self):
        code = strip_ts_comments(ACTION.read_text())
        assert "BOOKKEEPING_SUFFIXES.some" in code, (
            "classification is by EXCLUSION: an allow-list would demote every "
            "kind computed at runtime and the NowCard would go quiet"
        )

    def test_the_newest_scan_runs_backwards(self):
        code = strip_ts_comments(ACTION.read_text())
        assert "recent.length - 1" in code, (
            "recent is oldest-first, so the newest action is found from the end"
        )
<<<END CONTRACTACTION

<<<SLICE PLANF021R15
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
R15 builds the ACTION class T5_F021 rules the NowCard over — heartbeats and
bookkeeping excluded — as DATA in `actionClass.ts`, classified by EXCLUSION over
a suffix rule so a kind computed at runtime is never silently demoted. Nothing
renders it yet: R16 wires it, the build-then-wire rhythm R13 and R14 used. It
also records the R14 verdict, which was PASS on every gate.

## Next Steps
1. R16 wires `newestActionRow` into `AgentNowCard` with the recency dot, which
   is the first thing that RENDERS the class R15 built.
2. R17 adds the scroll discipline that never yanks a reader who has scrolled up.
3. R18 gives each row its click-jump to the node, the graph-focus API T003 opens
   with, then T003: the disabled steering input with its honest tooltip.

## Risks
- No DOM environment exists in this repository, so components are gated by
  `npx tsc --noEmit` and by Python source contracts. A contract that reads a
  prop name is the only thing standing between "published" and "rendered".
- A module nothing calls is the R-0220 blind spot. R15 is deliberately headless
  and R16 is the round that makes it load-bearing; if R16 does not happen, this
  plan is where that debt is visible.
- `npx vitest run` and `npx tsc` are BOTH vacuous in a fresh worktree, which has
  no `node_modules` (R-0518), so both run only in the primary checkout, and
  `npx vitest` is DENIED to the reviewer's session class besides.
- Reflog gates name the OPERATION field, never the whole row: this repository's
  commit subjects discuss amends by design (R-0613).
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613 and R-0622 stay routed to a paydown branch.
<<<END PLANF021R15

<<<SLICE RECORD14
Gate: R15 — the R14 entry. R14 PASSED ON EVERY ONE OF ITS FOURTEEN GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND IT MINTS NO FINDING. R14 made the activity feed LIVE: the bounded ring published on `BrainStreamView` at R13 now travels down the props the shell already passes, through `RightLivePanel`, into `ActivityFeedCard`, which renders the newest rows first and says so when the bound dropped some. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f021-r14.md` at `b71b15dc` and `.agent/last_block.md` at `9f8f8f75` are both sha256 c7010621d32bd48e2d90cff21665e4f96549302d9bee3071021ec56c75361ab5 over 30876 bytes and 440 lines, EQUAL byte for byte under the reviewer's own digest. SLICES: 17 over 161 CONTENT lines, TOTAL 440 against DECISION F085 D6's 490 and PROSE 279 against D5's 400, both equal to that block's constraint 9. EVERY SLICE APPLIED BYTE FOR BYTE, verified against slices the reviewer extracted mechanically from the committed C0a blob rather than against the worker's report: `.agent/plan.md` at `8c6a1225` equals PLANF021R14 plus one terminating newline and NOT the bare slice, at 44 lines with `## Goal` and `## Next Steps` each once; the ledger append at `a7641178` is the base blob plus one newline plus RECORD13 plus one newline, remainder sha256 5f1e83064ed6159319376ee06bfc63a6265766b4c508d8b8510d0b55b36fec96 over 5610 bytes and 2 lines, units 232 to 233 ELEMENTWISE equal, with a negative control at offset 2 of the FIRST paragraph that BOTH readers rejected while both accepted the true file; and the contract append at `e50e8fbe` is the CONTRACTPATHS-substituted base blob (5863 bytes) plus one newline plus CONTRACTFEED plus one newline, remainder sha256 e2c220f8385021ceba156ac14a11284830bc575ef70919bd765fa7cf38791cb1 over 1874 bytes and 42 lines, with EXACTLY TWO blank lines before its new top-level class, counted rather than delegated to a linter that does not evaluate E301-E306 outside preview. THE SEVEN PAIRS BEHAVED BY SHAPE, all twenty-one numbers exactly as that block's G7 predicted from the reviewer's dry run: every FROM 1 at the round base; at C3 the append-shaped AFC1, RLP0 and CONTRACTPATHS read FROM 1 and TO 1 while the replacing AFC2, RLP1, RLP2 and SHELL1 read FROM 0 and TO 1. THE LEDGER IS UNMOVED: `- R-` 213 at both points all DISTINCT, maximum R-0650 at both, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 13 to 14 both DISTINCT, `Gate: R14` 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially from the repository root and counting by passed plus skipped: `tests/ui_contracts/` 443 passed and 4 skipped for 447, the three state-reading suites 511, the canary 42, and `npx tsc --noEmit` in `apps/ui` exit 0 with stdout and stderr both EMPTY. THE GATE THE REVIEWER CANNOT RUN WAS CORROBORATED RATHER THAN ACCEPTED: `npx vitest` is denied to that session class, so the worker's reading of 12 files and 177 tests was checked by an ANCHORED scan for a line whose first non-blank text is `it(` over the committed test sources at both the round base and C3 — 12 files and 177 at both, a delta of exactly 0, which is the UNCHANGED reading that block ordered because R14 adds no vitest case. A raw substring count of `it(` reads 190 at both and is NOT that scanner: `await(`, `emit(` and `split(` all contain the token, so the delta survives the cruder reader while the absolute does not. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `e50e8fbe`: green first at 17 passed, then with the two new props removed from the single `RightLivePanel` line in `RemedyShell.tsx` — a target the reviewer confirmed occurs EXACTLY ONCE, whole-line and indent-agnostic counts agreeing — exactly 1 failed and 16 passed, the failure being `TestTheFeedIsFedFromTheStream::test_the_shell_hands_the_ring_to_the_panel` with the assertion "the ring is published on the view but never handed to the panel". THE RANGE HELD: five commits base to C3, every one single-parent, the path set EQUAL to that block's eight non-handoff `Change:` paths with both differences EMPTY, `git show --numstat` and `git diff --numstat` agreeing cell by cell with the handback's table, insertions 440, 318, 18, 2 and 101 every one under the 500 cap, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone, `gh pr list --state open` EMPTY, and the reflog read BY OPERATION over this round's six rows every one `commit` with `amend`, `rebase` and `cherry` each 0 in that field. ONE DEVIATION IS RECORDED HERE AGAINST OPEN R-0364 RATHER THAN UNDER A NEW ID, the open set having been searched for the DEFECT first as §3 checklist item 30 requires, and it is the reviewer's own block text rather than the worker's execution. That block's G15-equivalent marker clause ordered "`<<<SLICE `/`<<<END ` 0 LINES in every file a slice landed in" without saying whether LINES means line-anchored or merely containing. Read as containment, `.agent/live_review.md` reads 1 — line 1078, a pre-existing `Gate: R5` entry whose PROSE quotes the marker text — and it reads 1 at the ROUND BASE too, so the clause was already red before the round began and could not fail honestly, which is precisely what R-0364 registers. The worker took the containment reading, declared the clause unmeetable, named the line and its cause, and did NOT edit the ledger to make it green; the round's own delta is 0. Read line-anchored the clause is 0 in every file including the ledger, which the reviewer verified at the base. The counter-measure is APPLIED in the block that carries this entry, whose G15 states the line-anchored reading, names the containment reading it rejects, and says why. WHY R14 IS PASS: every slice is byte-identical to the slices the reviewer extracted itself, every runnable gate reproduces under the reviewer's own execution, the one unrunnable gate is corroborated by an independent anchored count that agrees exactly, the red control fails in the reviewer's own worktree on the one named test, and the single deviation is an ambiguity in the reviewer's gate prose that never reached a source file.
<<<END RECORD14
