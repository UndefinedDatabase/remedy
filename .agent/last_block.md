── STEP FEED LINKAGE — F021 ──
Goal:        Record R33, which PASSED, and land the CLIENT half of the linkage
             R33 put on the wire: `FeedRow` carries `taskId`, and a new pure
             module resolves a row to the graph node it belongs to. NO
             component is wired this round — R35 does that — because the block
             cap cannot hold the resolver, its tests and the JSX in one round,
             and splitting on that seam keeps every commit green. THREE
             corrections are appended naming OPEN findings R-0369, R-0419 and
             R-0630; NONE mints an id, and all three are the REVIEWER's own
             defects in the R33 block.

Fortschritt: ~98 % (T003 zur Haelfte: Server-Feld steht, Aufloeser folgt hier;
             es fehlen die Verdrahtung und der Steuer-Eingang)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R33 verdict
             and the three corrections · C3 the row field and the resolver with
             its tests · C4 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r34.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/api/feedRow.ts` (C3) ·
             `apps/ui/src/api/feedFocus.ts` (NEW, C3) ·
             `apps/ui/src/api/feedFocus.test.ts` (NEW, C3) ·
             `apps/ui/src/api/actionClass.test.ts` (C3) · `.agent/handoff.md`
             (C4). Resolve any count in this block against that list. NEITHER
             `ActivityFeedCard.tsx` NOR `RightLivePanel.tsx` NOR any `.css`
             file is touched this round.

Constraints:
 1. Apply every slice and pair half BYTE FOR BYTE. Never retype, rewrap,
    reflow, reindent or whitespace-adjust one. If a slice looks wrong, STOP and
    say so in the handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). ROUND BASE is `a14f0294` — resolve its full form with
    `git rev-parse`.
 3. C3 IS ONE COMMIT. `actionClass.test.ts` is in it for a reason that is not
    optional: `rowOf` there RETURNS a `FeedRow` under an explicit return-type
    annotation, so the moment `taskId` becomes a required field of that
    interface, that file stops typechecking. The field, the resolver and that
    one-line repair are a single typechecking unit; splitting them guarantees a
    commit whose own `tsc` gate is red. I found this by grepping every
    construction site of `FeedRow` rather than by running into it.
 4. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. Before it, in
    `.agent/live_review.md`: 224 registered under the canonical pattern
    `^- R-\d+ — `, maximum R-0661, `Done: R-` 1. After C2: still 224, still all
    DISTINCT, still maximum R-0661, `Done: R-` still 1. All three corrections
    name OPEN findings rather than new ids, per §3 checklist item 30, and each
    of `^- R-0369 — `, `^- R-0419 — ` and `^- R-0630 — ` stays at exactly 1
    across C2.
 5. NO PARAGRAPH OF RECORD34 BEGINS WITH THE BYTES `- R-`. Three open with
    `Recurrence: ` and the verdict opens `Gate: R34 — `. G5 measures this
    rather than trusting it. RECORD34's four paragraphs are separated from one
    another by EXACTLY ONE BLANK LINE.
 6. THE APPEND CONVENTION FOR `.agent/live_review.md` AT C2: the slice is
    quoted WITHOUT a trailing newline; add EXACTLY ONE newline, then RECORD34,
    then one terminator, so the join carries EXACTLY ONE BLANK LINE. A
    WHOLE-FILE write (PLANF021R34) is the slice PLUS one terminator. A NEW FILE
    (FEEDFOCUS, FEEDFOCUSTEST) is likewise the slice PLUS one terminator, and
    nothing else — no header, no generated banner.
 7. THE LEDGER IS APPEND-ONLY. No landed paragraph, `Gate:` entry or
    `Recurrence:` entry is edited.
 8. NO COUNT GATE IN THIS BLOCK COUNTS A STRING WHOSE NUMBER THIS BLOCK'S OWN
    SLICES CHANGE, AND EVERY LEDGER COUNT NAMES THE PATTERN IT IS READ UNDER.
    R33's G4 broke the first half of this rule twice and its G8 broke it once;
    those are the three entries C2 records, so this round is the wrong one in
    which to repeat them.
 9. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide at every commit under R-0622 and is NOT a gate of this round
    — do not run it and do not report it. Create and merge NO pull request.
    Push the branch after C4. ONE worktree under `.remedy-wt/` is ordered, for
    G6's red-proof alone; remove it and prove the tree clean afterwards.
10. THE THREE PAIRS ARE ROWFIELD, ROWPROJECT and ACTIONROW, and their shapes
    are MEASURED, not asserted: my script printed `TO contains FROM: False` for
    all three, so NONE is append-shaped and a FROM-zero count IS orderable for
    each. Each FROM occurs EXACTLY ONCE in its target at the round base, a
    reading that script printed over the bytes this block prints. ROWFIELD and
    ROWPROJECT edit the SAME file and do not overlap; apply ROWFIELD first.
11. WHAT I COULD AND COULD NOT DRY-RUN, stated so you do not read more
    assurance into this block than it earned. I applied all four texts in a
    worktree at `a14f0294` and ran the new test file against the REAL module
    through `npm run test:unit -- --root <worktree>/apps/ui --config
    <primary>/apps/ui/vitest.config.ts`: `1 passed`, `6 passed`. I also ran the
    mutation G6 orders and measured `2 failed | 4 passed`. I could NOT run a
    clean `tsc` in a worktree — it has no `node_modules`, and a symlink is
    denied to this session — so THE WORKER'S `tsc` RUN IN THE PRIMARY CHECKOUT
    IS THE FIRST HONEST EXECUTION OF THAT GATE. If it is red, STOP and report
    it; do not repair it, because a type error there is my defect and not
    yours.
12. Block size, measured on these final bytes AFTER the last edit: TOTAL 358
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice and
    pair CONTENT lines — 206 against DECISION F085 D5's 400. Markers count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C4; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is
     ordered NOWHERE — §3 item 31 leaves it to the next session.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r34.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over my
     emitted copy at `.remedy-wt/f021-r34.md` are all equal. Write C0b FROM the
     committed C0a blob. Report the digest, bytes and lines. Then extract the
     slices and pairs from the COMMITTED C0a blob by their marker LINES,
     `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO `, and report how many whole
     texts, how many pairs and how many CONTENT lines your extractor printed —
     each a number YOU measured, not one I named — re-measuring constraint 12's
     two numerals from that same blob against their caps.
 G3  `.agent/plan.md` at C1 equals PLANF021R34 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare
     slice that must exit 1. Report both exit codes, that the last byte is a
     newline, `^## Goal$` 1 and `^## Next Steps$` 1, and the `wc -l` YOU
     measure against AGENTS.md's "keep it short (<50 lines)". If that count is
     50 or more, STOP and report — do NOT trim the file to reach it (R-0654).
 G4  THE SLICES AND PAIRS AT C3. For EACH of ROWFIELD, ROWPROJECT and ACTIONROW
     report its FROM occurring EXACTLY 1x in its target at the round base and
     EXACTLY 0x at C3 — none is append-shaped (constraint 10), so the zero IS
     owed. For the two NEW files report that neither path existed at the round
     base, by `git cat-file -e a14f0294:<path>` failing, and that each equals
     its slice plus exactly one terminating newline by `cmp` at exit 0 with a
     negative control against the bare slice at exit 1. Report `wc -l` for both
     new files. Then report, over the lines C3's diff ADDS, that each TO-only
     line appears exactly once (§4.9). Do NOT count `taskId` in either target
     as a base-zero reading: it is a substring of prose this block also writes,
     and R33's G4 lost a clause to exactly that.
 G5  THE LEDGER, at C2, every count naming its pattern, base then C2:
     canonical `^- R-\d+ — ` 224 then 224, ALL DISTINCT at both, maximum
     R-0661 at both; loose `^- R-` 225 then 225, its gap to the canonical
     reading 1 at both; `Done: R-` 1 then 1; `^Gate: R` 32 then 33, DISTINCT at
     both; `^Gate: R34` 0 then 1; `^Recurrence: ` 7 then 10;
     `^Recurrence: R-0369 — ` 0 then 1; `^Recurrence: R-0419 — ` 0 then 1; and
     `^Recurrence: R-0630 — ` **1 then 2**, which is NOT a zero-then-one like
     the other two — that file already carries one R-0630 recurrence and I
     measured it rather than assuming the pattern. `^- R-0369 — `,
     `^- R-0419 — ` and `^- R-0630 — ` 1 then 1 each. Report also that the
     number of RECORD34 paragraphs opening with the bytes `- R-` is 0, and that
     the base blob is a byte-exact PREFIX of the C2 blob whose remainder is
     EXACTLY one newline plus RECORD34 plus one newline.
 G6  THE RED-PROOF, in a disposable worktree at C3 under `.remedy-wt/`, never
     in the primary checkout. There, replace `owner.nodeId` with `owner.id` in
     `feedFocus.ts` — the single mutation that makes the resolver return the
     TASK id instead of the NODE id, which is the one confusion this module
     exists to prevent — and run the new test file. Report the failure count
     and the failing test names; they MUST include the test whose name says the
     resolver never assumes the two are equal. I measured `2 failed | 4 passed`
     for this mutation. Then remove the worktree and report
     `git status --porcelain` at 0 lines and `git worktree list` naming the
     primary checkout alone.
 G7  THE SUITES, SERIAL, in the PRIMARY checkout, never two at once.
     `npm run test:unit` from `apps/ui` — I measured 15 files and 212 tests
     passing at the round base; report the file count and test count YOU
     measure, and the difference, which should be one file and the six tests
     FEEDFOCUSTEST carries. `npx tsc --noEmit` from `apps/ui` — exit 0 and
     EMPTY output, and see constraint 11 before you run it. Then, because this
     round rewrites `.agent/` state, ALL FOUR state readers:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py -q -rf` — I measured 528 at the
     round base. Then `python3 -m pytest tests/ui_contracts/ -q -rf`, which
     this round owes because it touches `apps/` — 486 passed and 4 skipped at
     the base. Then the canary, `python3 -m pytest tests/cli/test_golden_path.py
     -q -rf` — 42 at the base. No ruff gate is ordered: this round touches no
     Python.
 G8  STRUCTURE. `git diff --name-only a14f0294..HEAD` at C3 EQUALS the seven
     non-handoff `Change:` paths, both set differences reported EMPTY; at C4 it
     is those seven plus `.agent/handoff.md`, and BOTH readings are reported
     because no single commit shows both. 6 commits, every one single-parent;
     `git show --numstat` and `git diff --numstat` agree cell by cell; every
     commit's insertions under 500, each number reported. Marker sweep,
     LINE-ANCHORED, 0 for each of `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO `
     over EXACTLY these five: `.agent/plan.md`, `.agent/live_review.md`,
     `apps/ui/src/api/feedRow.ts`, `apps/ui/src/api/feedFocus.ts` and
     `apps/ui/src/api/feedFocus.test.ts`. An UNANCHORED `<<<` count is ordered
     over the three `apps/` files ONLY, where it must be 0; it is NOT ordered
     over `.agent/live_review.md`, which legitimately quotes marker text and
     where R33's G8 made that clause unmeetable — finding R-0630, recorded
     again this round. Reflog read BY OPERATION: every one of this round's rows
     is `commit`, with `amend`, `rebase` and `cherry` 0 each in that field.
     `gh pr list --state open` reported verbatim.

<<<SLICE PLANF021R34
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
R34 records R33 and takes the client half of T003 as far as one round's cap
allows: `FeedRow` gains `taskId` from the envelope field R33 landed, and the new
pure module `apps/ui/src/api/feedFocus.ts` resolves a row to a graph node
through the task list the dashboard already carries — never by matching on seq
or timestamp, which DECISION F021 D2 rejected. `actionClass.test.ts` rides along
because it constructs a `FeedRow` under an explicit return type and would
otherwise stop typechecking. Three corrections are appended against OPEN
findings R-0369, R-0419 and R-0630, none minting an id.

## Next Steps
1. R35: the wiring — `ActivityFeedCard` renders a resolvable row as a button
   that emits `onSelectNode`, `RightLivePanel` passes the task list down, and a
   `tests/ui_contracts/` source contract pins that the component really calls
   the resolver.
2. R36: the steering input, rendered DISABLED with the tooltip naming F030.
3. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- `feedFocus.ts` lands this round with NO caller. That is deliberate and is
  bounded to one round by the step above; it is not the R17 drift, where
  `feedScroll.ts` sat unimported for fourteen rounds before R31 wired it.
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- A worktree has no `node_modules`, so neither `tsc` nor a full vitest run can
  be dry-run there. The primary checkout is the only honest place for both.
- `npm run lint` is RED tree-wide at every commit under R-0622, still open.
- No code defect of F021 is open. R-0364, R-0369, R-0403, R-0419, R-0587,
  R-0607 through R-0609, R-0611, R-0613, R-0618, R-0622, R-0629, R-0630,
  R-0644, R-0651, R-0653 through R-0659 and R-0661 stay routed to a paydown
  branch.
<<<END PLANF021R34

<<<SLICE RECORD34
Recurrence: R-0369 — A COUNT GATE COUNTED A STRING THAT THE SAME BLOCK'S OWN SLICE WRITES INTO THE SAME FILE, TWICE IN ONE GATE. Second and third instances, both in the reviewer's own F021 R33 block, and the block's own constraint 8 forbade exactly this in the same breath. NO NEW ID IS MINTED: R-0369 already rules the class (§3 checklist item 30). THE INSTANCES, both in G4 and both found by the worker. First, the clause ordering the string `, "outcome": "ok"}` to read 5 then 5 in `tests/ui_server/test_sse_stream.py`, "UNCHANGED, which is the proof GOLDENPAIR did not bulk-replace the three input fixtures": measured 5 then 3, because GOLDENPAIR's own TO rewrites that exact tail on both `GOLDEN_STREAM` lines, so the count cannot survive its own pair. The PROPERTY the clause existed to protect does hold and the worker proved it a better way — the three survivors are the three INPUT fixtures at unchanged lines 19, 76 and 89, and 5 − 2 = 3 accounts for the whole delta — which is the reading the clause should have ordered. Second, the clause ordering `"task_id"` to read 0 at the base in the same file, which is the same defect in the other direction and is recorded under R-0419 below. THE FIX IS THE ONE R-0369 ALREADY NAMES: a count gate over a file the round edits is written against a string the round's own slices do NOT contain, or it is written as a DELTA with the pair's own contribution named.

Recurrence: R-0419 — A GATE ASSERTED AN ABSENCE ACROSS A FILE THE REVIEWER NEVER SEARCHED. Second instance, in the reviewer's own F021 R33 block. NO NEW ID IS MINTED: R-0419 already rules that a block asserting a fact about this repository measures it first. THE INSTANCE: G4 ordered `task_id` to occur "0 at base" in `packages/orchestration/ui_server.py`. Measured by the worker and confirmed by the reviewer at `6e529304`: it is 44 at the base and 48 at C3, and the name has been in that file since long before F021 — lines 104, 223, 275 and onward — because `_load_job_plan_events` has always read a task id out of trace metadata. The reviewer wrote "0" from the shape of the ROUND rather than from the CONTENT of the file, having read that same function forty minutes earlier while designing the very two-source resolution the round shipped. The delta of 4 is what the pair really contributes and is what the clause should have ordered. Nothing about the round is unsound because of it: the gate that matters — the pair's FROM at 1 then 0 — was correct and was measured.

Recurrence: R-0630 — A COUNT GATE OVER `.agent/live_review.md` WAS ORDERED WITHOUT AN ANCHOR, OVER A FILE THAT LEGITIMATELY QUOTES THE VERY TOKEN BEING COUNTED. Second instance, in the reviewer's own F021 R33 block; the FIRST is already recorded in this file, which is why the R34 block's G5 orders this recurrence as 1 then 2 rather than 0 then 1. NO NEW ID IS MINTED. THE INSTANCE: G8 ordered a marker sweep "LINE-ANCHORED, 0 for each of `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO `, and 0 for any `<<<` at all" over four files including `.agent/live_review.md`. The line-anchored halves are all 0 and were met. The unanchored half is UNMEETABLE: that file carries 18 occurrences of `<<<` at the round base and 18 at C2, RECORD33 contributing none, and reaching 0 would require editing landed ledger text, which the same block's constraint 7 forbids. The reviewer had ALREADY narrowed this clause once in the same block, excluding the two block copies for precisely this reason, and stopped one file short. R34's G8 states the rule the two instances share: an unanchored token count belongs only to files that do not quote the token, and the ledger always quotes it.

Gate: R34 — the R33 entry. R33 PASSED ON EVERY GATE WHOSE SUBJECT IS THE WORK, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND ALL THREE DECLARED DEVIATIONS ARE THE REVIEWER'S OWN DEFECTS, RECORDED IN THE THREE ENTRIES ABOVE. R33 IS THE ROUND THAT PUT THE TASK LINKAGE ON THE WIRE: `_safe_event_summary` in `packages/orchestration/ui_server.py` — the ONE writer the cursor endpoint and the SSE stream share — now emits DECISION F021 D2's single additive field `task_id`, resolved from the TOP LEVEL where the run log carries it and from `metadata` where `_load_job_plan_events` nests it, so jump-to-node will work for trace-driven jobs and run-log jobs alike rather than for only half of them. THE TWO-SOURCE READING IS THE ROUND'S REAL CONTENT and it came from reading both event producers before writing the field, not from a test going red. RE-MEASURED GATES: `tests/ui_server/` 439 passed against 438 at the base, the difference being the one new test; all four state readers 528; the canary 42; `ruff` clean on both touched files, which it also was at the base, so exit 0 was an honest demand. THE LEDGER held at 224 under `^- R-\d+ — `, all distinct, maximum R-0661 — R33 minted no id and resolved none, exactly as ordered. TRANSPORT held at sha256 `8b2ac868303ef15f1b8deb954b43aa8e33dbff00fcaa33a978aed0eed50ae5ce` over 23727 bytes and 312 lines across the reviewer's copy, `.agent/authored/f021-r33.md` at C0a and `.agent/last_block.md` at C0b, both blob `d4f63ac2`. THE RED-PROOF WAS REAL AND THE REVIEWER RAN IT TWICE: with the two test pairs applied and the source pair withheld, `tests/ui_server/test_sse_stream.py` prints `4 failed, 62 passed`, and the failures include the test that exists only to prove the two-source resolution. STRUCTURE: six commits, every one single-parent, insertions 312, 252, 22, 6, 40 and 78, each under 500. C4's own three readings, which no handback can state about itself, are `a14f0294`, +78/-46, and 115 lines — over the 100-line tier, with the cause declared in the file as DECISION D15 requires.
<<<END RECORD34

<<<FROM ROWFIELD
  timestamp: string;
  outcome: string;
}
<<<TO ROWFIELD
  timestamp: string;
  outcome: string;
  /** The task this event belongs to, or "" when it belongs to none. Carried by
   *  the envelope since DECISION F021 D2; `feedFocus.ts` turns it into the
   *  graph node a row click jumps to. */
  taskId: string;
}
<<<END ROWFIELD

<<<FROM ROWPROJECT
    timestamp: stringField(envelope, "timestamp"),
    outcome: stringField(envelope, "outcome"),
  };
<<<TO ROWPROJECT
    timestamp: stringField(envelope, "timestamp"),
    outcome: stringField(envelope, "outcome"),
    taskId: stringField(envelope, "task_id"),
  };
<<<END ROWPROJECT

<<<FROM ACTIONROW
  return { seq, kind, line: kind, known: true, timestamp: "", outcome: "", receivedAtMs: 0 };
<<<TO ACTIONROW
  return { seq, kind, line: kind, known: true, timestamp: "", outcome: "", receivedAtMs: 0, taskId: "" };
<<<END ACTIONROW

<<<SLICE FEEDFOCUS
// Resolving one activity-feed row to the graph node it belongs to. T003's
// click-jump lives here rather than in the component so the node environment's
// vitest can reach it, which is the pattern DECISION F021 D4 fixed for this
// feature.
import type { FeedRow } from "./feedRow";

/** The only two fields of a dashboard task this resolution reads. Narrowed on
 *  purpose: the rule is about ids, and a resolver taking the whole
 *  `RemedyTaskItem` would churn every time an unrelated task field moved. */
export interface FocusableTask {
  id: string;
  nodeId: string;
}

/** The graph node a feed row jumps to, or null when it cannot jump.
 *
 *  Remedy deliberately resolves this through the task list the dashboard
 *  already carries, rather than by matching a row against the graph on seq or
 *  timestamp: DECISION F021 D2 rejected inventing a second client-side mapping
 *  for exactly this, and two events sharing a timestamp would make that one
 *  wrong. `related_node_id` is what `remedyApi.ts` reads a task's `nodeId`
 *  from, so this lands on a node the graph really has.
 *
 *  A null is not a failure. Heartbeats and job-level events carry no task
 *  linkage at all, and a row that cannot jump must render as a row that does
 *  not OFFER the jump — never as one that jumps somewhere arbitrary. */
export function nodeIdForFeedRow(
  row: Pick<FeedRow, "taskId">,
  tasks: readonly FocusableTask[],
): string | null {
  if (!row.taskId) {
    return null;
  }
  const owner = tasks.find(task => task.id === row.taskId);
  return owner ? owner.nodeId : null;
}
<<<END FEEDFOCUS

<<<SLICE FEEDFOCUSTEST
import { describe, it, expect } from "vitest";
import { nodeIdForFeedRow } from "./feedFocus";

const TASKS = [
  { id: "T-1", nodeId: "node-T-1" },
  { id: "T-2", nodeId: "node-T-2" },
];

describe("nodeIdForFeedRow", () => {
  it("resolves a row to the node of the task that owns it", () => {
    expect(nodeIdForFeedRow({ taskId: "T-2" }, TASKS)).toBe("node-T-2");
  });

  it("returns null for a row that carries no linkage", () => {
    // Heartbeats and job-level events are the normal case here, not an error.
    expect(nodeIdForFeedRow({ taskId: "" }, TASKS)).toBeNull();
  });

  it("returns null when the linkage names a task the dashboard lacks", () => {
    // The stream and the dashboard are two reads of one job and can disagree
    // for a moment. A stale id must not jump to the wrong node.
    expect(nodeIdForFeedRow({ taskId: "T-9" }, TASKS)).toBeNull();
  });

  it("returns null against an empty task list rather than throwing", () => {
    expect(nodeIdForFeedRow({ taskId: "T-1" }, [])).toBeNull();
  });

  it("does not resolve through inherited object properties", () => {
    // `taskId` reaches this rule from parsed JSON the client does not control,
    // so a name like `constructor` must miss rather than match something on
    // the prototype. `find` compares values, which is why this holds.
    expect(nodeIdForFeedRow({ taskId: "constructor" }, TASKS)).toBeNull();
  });

  it("reads the task's nodeId and never assumes it equals the task id", () => {
    // `remedyApi.ts` falls back to the task id only when `related_node_id` is
    // absent, so the two are equal today and are not the same field.
    const renamed = [{ id: "T-1", nodeId: "some-other-node" }];
    expect(nodeIdForFeedRow({ taskId: "T-1" }, renamed)).toBe("some-other-node");
  });
});
<<<END FEEDFOCUSTEST
