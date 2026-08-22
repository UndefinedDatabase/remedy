── STEP T002-A — F021 ──
Goal:        Record the R8 verdict and ship the FIRST production code of T002 on
             the ground DECISION F021 D4 rules: one pure module that projects a
             brain-stream frame into the row an activity feed renders, plus its
             node-vitest tests. It adds no DOM, no component and no state; the
             ring DECISION F021 D5 rules is R10's work and is NOT built here.

Fortschritt: ~40 % (T001 fertig · T002 begonnen — die Projektion Frame→Zeile
             landet in dieser Runde, der Ring und die Komponenten folgen in R10
             und R11; T003 offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the feedRow
             module and its tests · C3 the R8 verdict · C4 the handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r9.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `apps/ui/src/api/feedRow.ts` (NEW,
             C2) · `apps/ui/src/api/feedRow.test.ts` (NEW, C2) ·
             `.agent/live_review.md` (C3) · `.agent/handoff.md` (C4).
             Resolve any count in this block against that list rather than
             against a numeral written elsewhere.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it. This binds the two CODE slices most of all:
    the reviewer typechecked those exact bytes and a reformatting would void
    that evidence.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). C2 ships both new files in ONE commit because the test is the
    module's only caller and a commit holding the module alone would add
    unreached code. C4 carries only the handback.
    ROUND BASE is `f5f0158526342247abf4f8215b7dbdfbd007789c` and is the commit
    every "round base" in this block names.
 3. THIS ROUND MINTS NO FINDING ID and resolves nothing. It writes no `Done:`
    line and no `Landed:` line. R-0649 stays the maximum registered id and
    R-0650 stays the next free one.
 4. ONE WHOLE-FILE REPLACEMENT, TWO NEW FILES AND ONE APPEND. PLANF021R9
    replaces `.agent/plan.md` at C1 in full. FEEDROW and FEEDROWTEST are the
    ENTIRE contents of two files that do not exist at the round base, created
    at C2. RECORD8 appends to `.agent/live_review.md` at C3, based on the ROUND
    BASE. There is NO FROM/TO pair this round, so no containment reading is
    owed and none is stated. Measured by the reviewer on the slices' own bytes
    before emission: RECORD8 is ONE blank-line unit, and G6's reader (b)
    depends on that count.
 5. NO EXISTING PRODUCTION FILE IS EDITED. The two files C2 creates are new;
    nothing already under `apps/`, `packages/` or `tests/` is modified or
    deleted, and no import of `feedRow` is added to any existing module. The
    module is deliberately UNCALLED by production code this round — its caller
    arrives with the ring in R10 — so do not wire it into anything to make it
    look used. Run no formatter or linter that rewrites a file in place.
 6. Do NOT create a pull request and do NOT merge one. The branch stays open and
    unmerged: F021 is mid-feature. Push the branch.
 7. THE HANDBACK IS ALSO THE SESSION HANDOFF. Beyond the mandated sections it
    states, in its `## Next` section and in this order, the four things the next
    session needs and cannot recompute cheaply: (a) that the next session's
    FIRST action is docs/agents/self_drive_protocol.md Phase 1 rule 1, the
    `.agent/STOP` check, BEFORE rule 2's Open PR Gate — required by that
    protocol's Phase 2 and by finding R-0347; (b) that the Open PR Gate will
    find NO open pull request, so rule 5 applies and F021 continues on
    `feature/f021-live-activity-feed`; (c) that R10's work is the bounded ring
    DECISION F021 D5 rules — `recent` on `BrainStreamState` and on
    `BrainStreamView` — and that the append belongs inside `receiveBrainFrame`
    in `apps/ui/src/api/brainStream.ts` rather than in the runner's `dispatch`,
    because that function already drops a frame whose `seq` is not ahead of
    `lastSeq` and an append in `dispatch` would duplicate a row on every
    reconnect replay; (d) that the C4 handback commit of this round has never
    had its own `git status --porcelain` reading or insertion count recorded,
    because §3 checklist item 31 orders them nowhere, and that the next
    reviewer takes both at its first gate and records them in that round's
    entry.
 8. WHAT THE REVIEWER COULD AND COULD NOT PRE-EXECUTE, stated so no gate below
    is read as carrying more evidence than it does. `npx tsc --noEmit` WAS run
    by the reviewer over these exact authored bytes, in a disposable worktree
    at the round base with `apps/ui/node_modules` symlinked in, and exited 0;
    that worktree was removed and pruned. `npx vitest run` is DENIED to the
    reviewer's session and was NOT run by it at all, so G9's colour is ordered
    on the strength of G10's red control rather than on a reviewer measurement,
    and G10 is therefore not optional.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 389
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 221 against DECISION F085 D5's 400. Marker lines count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C4; the branch is `feature/f021-live-activity-feed`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2 and
     C3. C4's own reading is ordered NOWHERE — §3 checklist item 31 rules that
     the handback commit's own numbers are measured by the reviewer at the next
     gate and recorded there.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r9.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's own emitted copy still on disk at `.remedy-wt/f021-r9.md` are
     all equal. Write C0b FROM the committed C0a blob. Report the digest with
     the byte and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 9's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF021R9, proved with `cmp` at
     exit 0 against the slice extracted from the committed C0a blob, with a
     NEGATIVE CONTROL against RECORD8 that must exit 1. Report both exit codes,
     plus `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE TWO NEW FILES at C2 are byte-equal to their slices. Confirm with
     `git ls-tree <round base> -- apps/ui/src/api/feedRow.ts
     apps/ui/src/api/feedRow.test.ts` that BOTH are ABSENT at the round base,
     then `cmp` each committed file against its slice extracted from the C0a
     blob at exit 0, each with the OTHER slice as a negative control at exit 1.
     Report all four exit codes and both files' line counts.
 G6  THE LEDGER APPEND at C3, under TWO INDEPENDENT READERS. Obtain the base
     blob with `git show <round base>:<path>` into memory or into scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision,
     which docs/agents/self_drive_protocol.md guardrail G5 forbids outright.
     Reader (a): the round-base blob of `.agent/live_review.md` is a byte-exact
     PREFIX of the C3 file and the remainder is EXACTLY one newline plus
     RECORD8 — report the remainder's sha256, byte count and line count, and the
     file's byte and line counts before and after. Reader (b), the SET-WISE
     form: split BOTH blobs on the blank line into units and confirm the C3 unit
     LIST equals the base unit list followed by RECORD8's own units, compared
     ELEMENTWISE over the whole list and not at the tail; report N at both
     points and RECORD8's own unit count against constraint 4's ONE. NEGATIVE
     CONTROL: replace one printable byte of the FIRST paragraph of the C3 file
     at equal length and confirm BOTH readers REJECT that mutant while BOTH
     ACCEPT the true file; name the byte offset and the substitution.
 G7  THE LEDGER SETS, line-anchored at line start, at the round base then at C3:
     `- R-` entries and how many are DISTINCT; `Done: R-` lines; `Landed: `
     lines; `Gate: R` keys and how many are DISTINCT; `Gate: R9` occurrences;
     and the MAXIMUM registered id. Report each at BOTH points. NO id is minted,
     so `- R-` reads 212 at BOTH points with both DISTINCT, the maximum reads
     R-0649 at BOTH points, `Gate: R` keys read 8 then 9 with both DISTINCT, and
     `Gate: R9` reads 0 then 1.
 G8  TYPECHECK, run at C2 from `apps/ui` in the PRIMARY checkout:
     `npx tsc --noEmit`. Report the exit code, which must be 0. The reviewer
     measured exit 0 over these exact authored bytes at the round base — see
     constraint 8 for how, and for what it does not cover.
 G9  THE FRONTEND SUITE, run at C2 from `apps/ui` in the PRIMARY checkout and
     SERIALLY, never while a pytest process is alive: `npx vitest run`. Report
     the exit code, the FILE count and the TEST count. Take the SAME reading at
     the ROUND BASE as well, by stashing nothing and instead reading the base in
     a disposable worktree under `.remedy-wt/` with `apps/ui/node_modules`
     SYMLINKED in — never copied, because a copy dereferences npm's bin shims
     (finding R-0591) — and report both readings. The file count must rise by
     exactly 1 and the test count by exactly 8, those being the one file and the
     eight `it(` blocks FEEDROWTEST contains. Do NOT report a base reading you
     did not take.
G10  THE RED CONTROL, and it is not optional — G9's colour is ordered on its
     strength (constraint 8). In a disposable worktree under `.remedy-wt/` whose
     name no directory already uses, at C2, with `apps/ui/node_modules`
     SYMLINKED in: in `apps/ui/src/api/feedRow.ts` replace the single line
     `    seq: frame.seq,` with `    seq: 0,` and run `npx vitest run` again.
     That byte string occurs exactly ONCE in that file, counted whole-line and
     ignoring indentation, both readings agreeing. Report that the run goes RED
     and NAME the failing test; the reviewer expects
     `carries the frame's own seq rather than any envelope field` among the
     failures. Then restore the worktree file and confirm the run is GREEN
     again, so the control discriminates in both directions. Remove and prune
     that worktree before the handback; the PRIMARY checkout is never mutated.
G11  THE CONTRACT SUITES, run at C3 in the PRIMARY checkout and SERIALLY, after
     every `npx vitest` process has exited:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py -q -rf`. Report the exit code and
     the passed-plus-skipped total, counting BY PASSED PLUS SKIPPED. The
     reviewer measured exit 0 and 511 at the round base. No docs gate is owed:
     the `Change:` list holds no `docs/` path at all — check that against the
     list before you accept this sentence.
G12  CANARY, run at C3, serially, after G11 has finished:
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report the exit
     code and the total. The reviewer measured exit 0 and 42 at the round base.
G13  THE T001 CONTRACT TESTS STILL HOLD, run at C3, serially, after G12:
     `python3 -m pytest tests/ui_contracts/ -q -rf`. Report the exit code and
     the passed-plus-skipped total; the reviewer measured exit 0 with 426 passed
     and 4 skipped at the round base. This round adds no catalog entry and no
     Python emitter, so the humanize-catalog equality must be UNCHANGED; a
     different reading is reported RED rather than explained.
G14  RANGE, executed at C3 and covering the round base to C3 — NOT to C4, because
     C4 writes the file that must quote this gate and §3 checklist item 31
     forbids ordering a reading the quoting artefact cannot yet hold. Report:
     the base-to-C3 path set against the six paths of this block's `Change:`
     list other than `.agent/handoff.md`, with the set difference EMPTY in both
     directions; every commit single-parent; `git show --numstat` and
     `git diff --numstat` agreeing cell by cell with the handback's `## Commits`
     table for C0a, C0b, C1, C2 and C3 (§3 checklist item 28); every insertion
     count under the 500 cap; leading `<<<SLICE ` and `<<<END ` reading 0 LINES
     in `.agent/plan.md`, `.agent/live_review.md` and BOTH new files; that the
     base-to-C3 range MODIFIES no path that existed at the round base under
     `apps/`, `packages/` or `tests/` — the only two such paths in the range are
     ADDED (status `A` in `git diff --name-status`); `git ls-files .remedy-wt`
     reading 0; and this round's reflog rows so far classified with `amend`,
     `rebase` and `cherry` each 0 in the operation field.
G15  NO PULL REQUEST: report `gh pr list --state open --json number,headRefName`
     and state that neither `gh pr create` nor `gh pr merge` was run. The
     expected reading is an EMPTY list, which is also the fact constraint 7(b)
     tells the next session to expect.
G16  THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3 and C4, the round base SHA, ONE LINE PER GATE with the
     transcripts kept out of the file (R-0582), the block's `Fortschritt:` line
     verbatim across all three of its lines, and the four items constraint 7
     requires in its `## Next` section. Its own `wc -l` is reported against the
     60-line cap, with a DECISION D15 line declaring any overage and naming the
     mandated content that caused it. Every commit heading in the `## Commits`
     table carries that commit's FULL subject, and where a commit cannot name
     its own SHA the role and the reason are written INSIDE the heading rather
     than left to a channel that ends with this session — that omission is
     finding R-0494.

Handback:   completion report + rewrite `.agent/handoff.md`.

<<<SLICE PLANF021R9
# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210, which the reviewer merged at the Open PR Gate before
this branch was created. `.agent/live_review.md` is the source of truth for the
open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps the streamed event kinds to plain lines, a NowCard shows the newest
ACTION-class event with a recency-driven activity dot, and feed rows carry their
seq and click-jump to their node in the graph. DONE when the catalog covers the
kind set DECISION F021 D3 rules and an unknown kind renders an honest generic
line rather than vanishing, the feed renders fixture streams per the binding CSS,
jump-to-node focuses the right node, and the steering input renders DISABLED with
its honest tooltip until F030 lands.

## Current Step
R9 records the R8 verdict and ships T002's first production code: the pure
projection from a brain-stream frame to a feed row, with its node-vitest tests,
under the test discipline DECISION F021 D4 rules. It mints no finding id. The
module is deliberately uncalled until R10 wires it to the ring.

## Next Steps
1. R10 builds the bounded ring DECISION F021 D5 rules: `recent` on
   `BrainStreamState` and on `BrainStreamView`, appended inside
   `receiveBrainFrame` rather than in the runner's `dispatch`, so a reconnect
   replay cannot duplicate a row.
2. R11 builds the feed and NowCard components over fixture streams, with the
   scroll discipline that never yanks a reader who has scrolled up, gated by a
   Python source contract under `tests/ui_contracts/`.
3. R12 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- The ring is the one place a reconnect can duplicate rows. `receiveBrainFrame`
  already drops a frame whose seq is not ahead of `lastSeq`; an append written
  anywhere else silently bypasses that guard.
- The view-identity contract `createBrainStreamRunner` documents is what R10 is
  most likely to break: `useSyncExternalStore` compares with `Object.is`, so a
  freshly built array on every call re-renders forever.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- The catalog covers only what a static walk can see. The generic line carries
  the eleven runtime-computed emitters, and R-0649 records that the walk's roots
  also reach vendored third-party Python.
- The open set holds no code defect of F021; R-0403, R-0607, R-0608, R-0609,
  R-0611 and R-0613 stay routed to a paydown branch.
<<<END PLANF021R9

<<<SLICE FEEDROW
// One activity-feed row, projected from one brain-stream frame. T002's rows
// render THIS and never the raw envelope, so the naming trap below is resolved
// once here instead of in every component that reads a stream event.
import { humanizeStreamEvent } from "./humanize";
import type { BrainStreamFrame } from "./brainStream";

/** What one activity-feed row shows. `seq` is the ledger position the row
 *  carries and jumps to; `known` is what a dev console note counts. */
export interface FeedRow {
  seq: number;
  kind: string;
  line: string;
  known: boolean;
  timestamp: string;
  outcome: string;
}

// The naming trap this module exists to resolve, measured at `f5f01585` in
// `_safe_event_summary` (packages/orchestration/ui_server.py): a frame's
// `event` field holds the whole SAFE ENVELOPE — seq, event, timestamp and
// outcome — and the envelope's OWN `event` field is the kind string. The kind
// is therefore `frame.event.event`, which reads like a typo and is not one.
function envelopeOf(frame: BrainStreamFrame): Record<string, unknown> {
  return typeof frame.event === "object" && frame.event !== null
    ? frame.event as Record<string, unknown>
    : {};
}

/** Read one envelope field as a string, defaulting to "" for anything else.
 *  The envelope is parsed JSON from a server this client does not control, so
 *  every field is CHECKED rather than asserted. */
function stringField(envelope: Record<string, unknown>, name: string): string {
  const value = envelope[name];
  return typeof value === "string" ? value : "";
}

/** Project one frame into the row a feed renders. Total by construction: every
 *  frame yields a row, because an event the catalog cannot name still happened
 *  and a feed that dropped it would tell a story with holes in it. */
export function feedRowOf(frame: BrainStreamFrame): FeedRow {
  const envelope = envelopeOf(frame);
  const kind = stringField(envelope, "event");
  const humanized = humanizeStreamEvent(kind);
  return {
    seq: frame.seq,
    kind,
    line: humanized.line,
    known: humanized.known,
    timestamp: stringField(envelope, "timestamp"),
    outcome: stringField(envelope, "outcome"),
  };
}
<<<END FEEDROW

<<<SLICE FEEDROWTEST
import { describe, it, expect } from "vitest";
import { feedRowOf } from "./feedRow";
import { STREAM_EVENT_CATALOG } from "./humanizeCatalog";

/** A frame as `framesOf` builds one: the envelope IS the frame's event field. */
function frameOf(seq: number, envelope: unknown) {
  return { seq, event: envelope };
}

describe("feedRowOf over a well-formed envelope", () => {
  it("carries the frame's own seq rather than any envelope field", () => {
    const row = feedRowOf(frameOf(41, { seq: 7, event: "task_run_started" }));
    expect(row.seq).toBe(41);
  });

  it("resolves the kind from the envelope's own event field", () => {
    const row = feedRowOf(frameOf(1, { event: "task_run_started" }));
    expect(row.kind).toBe("task_run_started");
    expect(row.line).toBe(STREAM_EVENT_CATALOG["task_run_started"]);
    expect(row.known).toBe(true);
  });

  it("carries timestamp and outcome through unchanged", () => {
    const row = feedRowOf(frameOf(2, {
      event: "task_run_started", timestamp: "2026-08-22T10:00:00Z", outcome: "ok",
    }));
    expect(row.timestamp).toBe("2026-08-22T10:00:00Z");
    expect(row.outcome).toBe("ok");
  });
});

describe("feedRowOf on envelopes the client does not control", () => {
  it("an uncatalogued kind still yields a row, on the generic line", () => {
    const row = feedRowOf(frameOf(3, { event: "some_runtime_computed_kind" }));
    expect(row.line).toBe("some_runtime_computed_kind event");
    expect(row.known).toBe(false);
    expect(row.seq).toBe(3);
  });

  it("a non-object event field yields a row rather than throwing", () => {
    for (const broken of [null, "a string", 7, undefined]) {
      const row = feedRowOf(frameOf(4, broken));
      expect(row.kind).toBe("");
      expect(row.line).toBe("unknown event");
      expect(row.known).toBe(false);
    }
  });

  it("missing string fields read as the empty string, never undefined", () => {
    const row = feedRowOf(frameOf(5, { event: "task_run_started" }));
    expect(row.timestamp).toBe("");
    expect(row.outcome).toBe("");
  });

  it("a non-string field is rejected rather than coerced", () => {
    const row = feedRowOf(frameOf(6, { event: 42, timestamp: 1, outcome: [] }));
    expect(row.kind).toBe("");
    expect(row.timestamp).toBe("");
    expect(row.outcome).toBe("");
  });

  it("a kind colliding with an Object prototype member is not reported known", () => {
    const row = feedRowOf(frameOf(7, { event: "constructor" }));
    expect(row.known).toBe(false);
    expect(row.line).toBe("constructor event");
  });
});
<<<END FEEDROWTEST

<<<SLICE RECORD8
Gate: R9 — the R8 entry. R8 PASSED ON EVERY GATE, RE-MEASURED INDEPENDENTLY RATHER THAN READ BACK. R8 was a decide-and-record round that built nothing, and every one of its fifteen gates reproduces under the reviewer's own execution. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f021-r8.md` at `741923b9`, `.agent/last_block.md` at `b9f8f136`, the working copy of `.agent/last_block.md`, and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f021-r8.md`, are all sha256 a9d295e3283d08603d50f62407c95f81628545aeecb5adff4be5099135c3b1f4 over 26644 bytes and 259 lines, so §4.9's primary cmp-against-scratchpad proof was available and used rather than the digest fallback. SLICES: 3 over 66 CONTENT lines, TOTAL 259 against DECISION F085 D6's 490 and PROSE 193 against D5's 400, both equal to that block's constraint 8. THE WHOLE-FILE SLICE IS BYTE-EQUAL to what landed: `.agent/plan.md` at `fd1e3b4f` equals PLANF021R8 over 46 lines against the 50 cap, with RECORD7 as a negative control that differs. THE TWO APPENDS HELD UNDER THE REVIEWER'S OWN READERS. `.agent/decisions.md` at `9c7fdfc2` is the round-base blob plus exactly one newline plus DECIDE45, remainder sha256 f128493ecd04a7d2a9c9172cfa2f27da1826955eb9777c5e88fa80136aa39f2c over 7147 bytes and 20 lines, the file going 492990 bytes and 6989 lines to 500137 and 7009, units 1225 plus DECIDE45's own 10 to 1235 with every base position equal elementwise, and `## DECISION ` headings 113 to 115, all DISTINCT at both points, with F021 D4 and D5 each reading 0 then 1. `.agent/live_review.md` at `17b9fce7` is the round-base blob plus exactly one newline plus RECORD7, remainder sha256 d2c9ec8f5ae67ca84d9cf4514e368254af95f379c696baaed7a926b60ab2c323 over 4075 bytes, units 224 plus RECORD7's own 1 to 225, again elementwise. THE REVIEWER RE-RAN BOTH NEGATIVE CONTROLS ITSELF rather than accepting the worker's: mutating byte offset 2 of each file — `D` to `Q` in `.agent/decisions.md` and `L` to `Q` in `.agent/live_review.md` — is REJECTED by reader (a) and reader (b) alike, while the true file is ACCEPTED by both, which is the same offset and the same outcome the worker reported. THE LEDGER SETS ARE UNMOVED, as a round minting nothing requires: 212 `- R-` entries all DISTINCT at both points, maximum id R-0649 at both, `Done: R-` 0 and `Landed: ` 0 at both, `- R-0585 —` 1 at both, and `Gate: R` keys 7 to 8 with `Gate: R8` going 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout at `f5f01585`: the three contract suites exit 0 with 511 passed, the canary exit 0 with 42 passed, and `tests/ui_contracts/` exit 0 with 426 passed and 4 skipped — all three equal to the round-base readings, so nothing regressed. THE RANGE HELD: six commits every one single-parent, the base-to-C3 path set EQUAL to that block's five non-handoff `Change:` paths with both differences EMPTY, 0 paths beginning `apps/`, `packages/` or `tests/`, insertions 259, 161, 16, 20 and 2 every one far under the 500 cap, markers 0 in every file a slice landed in, `git ls-files .remedy-wt` 0, `git worktree list` ending with the primary checkout alone, and all six reflog rows `commit:` — amend 0, rebase 0, cherry 0. THE READING §3 CHECKLIST ITEM 31 LEAVES TO THIS GATE: the R8 handback commit `f5f01585` is single-parent and changes `.agent/handoff.md` alone at 47 insertions and 38 deletions, far under the 500-insertion cap, and `git status --porcelain` reads 0 lines at that commit. That numstat is NOT the file's line counts — the handoff went from 88 lines to 97 — and the difference is git's matched-line accounting rather than a defect; §3 checklist item 28 exists because those two readings diverge exactly here, and the worker flagged the divergence itself before the reviewer looked. WHY R8 IS PASS: every gate reproduces, the ledger arithmetic is exact, the two DECISIONS it ruled rest on measurements the reviewer took first-hand, and the round declared no deviation because it needed none.
<<<END RECORD8
