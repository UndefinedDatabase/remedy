── STEP DECIDE-INFRA — F021 ──
Goal:        Record the R7 verdict with the two readings §3 checklist item 31
             leaves to this gate, add the R7 evidence to the open finding
             R-0585, and RULE the two infrastructure DECISIONS T002 depends on
             — the frontend test environment and the single-subscription
             fan-out — so that the next round can build T002 without deciding
             anything. This round BUILDS NOTHING and touches no file under
             `apps/`, `packages/` or `tests/`.

Fortschritt: ~35 % (T001 fertig und verifiziert · T002 offen · T003 offen; R7
             schrieb das R6-Verdikt, R8 faellt die beiden Infrastruktur-
             ENTSCHEIDUNGEN, T002 wird in R9 gebaut) — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the two
             DECISIONS · C3 the R7 verdict with the R-0585 evidence · C4 the
             handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r8.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/decisions.md` (C2) ·
             `.agent/live_review.md` (C3) · `.agent/handoff.md` (C4).
             Resolve any count in this block against that list rather than
             against a numeral written elsewhere.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    both record commits because the plan must be current before them (§3
    checklist item 23). C2 precedes C3 because the `Gate: R8` paragraph states
    that this round's DECISIONS have landed, and §3 checklist item 20 as
    narrowed by R-0524 lets a slice describe the round's OWN change only by
    naming the ordering constraint that fixes it — this clause is that
    constraint. C4 carries only the handback.
    ROUND BASE is `fc56d4cc7b4aeccce460560ce1275192db0e8e10` and is the commit
    every "round base" in this block names.
 3. THIS ROUND MINTS NO FINDING ID AT ALL and resolves nothing. It writes no
    `Done:` line and no `Landed:` line. R-0649 stays the maximum registered id
    and R-0650 stays the next free one. The one defect R7 surfaced — its own
    constraint 7(c) contradicting its PLANF021R7 slice about which round rules
    these DECISIONS — is added as evidence to the OPEN finding R-0585 inside
    RECORD7 rather than under a new id, because §3 checklist item 30 requires
    the open set to be searched for the DEFECT first and that search returned
    R-0585 holding exactly the clause-versus-clause shape. That defect is the
    REVIEWER'S OWN.
 4. ONE WHOLE-FILE REPLACEMENT AND TWO APPENDS. PLANF021R8 replaces
    `.agent/plan.md` at C1 in full. DECIDE45 appends to `.agent/decisions.md`
    at C2 and RECORD7 appends to `.agent/live_review.md` at C3, both based on
    the ROUND BASE. There is NO FROM/TO pair this round, so no containment
    reading is owed and none is stated. Measured by the reviewer on the slices'
    own bytes before emission: RECORD7 is ONE blank-line unit and DECIDE45 is
    TEN, and G5's and G7's reader (b) depend on those counts.
 5. NO PRODUCTION FILE IS EDITED. You may READ anything. Do not create, modify
    or delete a file under `apps/`, `packages/` or `tests/`, and run no
    formatter or linter that rewrites a file in place. In particular: the two
    DECISIONS this round rules describe changes to `apps/ui/vitest.config.ts`
    and to the brain-stream modules, and NONE of those changes is made this
    round. R9 builds them.
 6. Do NOT create a pull request and do NOT merge one. The branch stays open and
    unmerged: F021 is mid-feature, so there is nothing to open a pull request
    for and nothing to merge. Push the branch.
 7. THE HANDBACK IS ALSO THE SESSION HANDOFF. Beyond the mandated sections it
    states, in its `## Next` section and in this order, the four things the next
    session needs and cannot recompute cheaply: (a) that the next session's
    FIRST action is docs/agents/self_drive_protocol.md Phase 1 rule 1, the
    `.agent/STOP` check, BEFORE rule 2's Open PR Gate — naming rule 1 ahead of
    rule 2 is required by that protocol's Phase 2 and by finding R-0347; (b)
    that the Open PR Gate will find NO open pull request, so rule 5 applies and
    F021 continues on `feature/f021-live-activity-feed`; (c) that the next
    build is T002 and that DECISIONS F021 D4 and D5, ruled at C2 of THIS round,
    are the ground it is built on, so T002 needs no further infrastructure
    ruling; (d) that the C4 handback commit of this round has never had its own
    `git status --porcelain` reading or insertion count recorded, because §3
    checklist item 31 orders them nowhere, and that the next reviewer takes both
    at its first gate and records them in that round's entry.
 8. Block size, measured on these final bytes AFTER the last edit: TOTAL 259
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 193 against DECISION F085 D5's 400. Marker lines count
    as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C4; the branch is `feature/f021-live-activity-feed`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2 and
     C3. C4's own reading is ordered NOWHERE — §3 checklist item 31 rules that
     the handback commit's own numbers are measured by the reviewer at the next
     gate and recorded there.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r8.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's own emitted copy still on disk at `.remedy-wt/f021-r8.md` are
     all equal. Write C0b FROM the committed C0a blob. Report the digest with
     the byte and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 8's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF021R8, proved with `cmp` at
     exit 0 against the slice extracted from the committed C0a blob, with a
     NEGATIVE CONTROL against RECORD7 that must exit 1. Report both exit codes,
     plus `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE DECISIONS APPEND at C2, under TWO INDEPENDENT READERS. Obtain the base
     blob with `git show <round base>:<path>` into memory or into scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision,
     which docs/agents/self_drive_protocol.md guardrail G5 forbids outright.
     Reader (a): the round-base blob of `.agent/decisions.md` is a byte-exact
     PREFIX of the C2 file and the remainder is EXACTLY one newline plus
     DECIDE45 — report the remainder's sha256, byte count and line count, and
     the file's byte and line counts before and after. Reader (b), the SET-WISE
     form: split BOTH blobs on the blank line into units and confirm the C2 unit
     LIST equals the base unit list followed by DECIDE45's own units, compared
     ELEMENTWISE over the whole list and not at the tail; report N at both
     points and DECIDE45's own unit count against constraint 4's TEN. NEGATIVE
     CONTROL: replace one printable byte of the FIRST paragraph of the C2 file
     at equal length and confirm BOTH readers REJECT that mutant while BOTH
     ACCEPT the true file; name the byte offset and the substitution.
 G6  THE DECISION KEYS, line-anchored at line start, at the round base then at
     C2: `^## DECISION ` headings; `^## DECISION F021 D4 `; `^## DECISION F021
     D5 `; and how many `^## DECISION ` headings are DISTINCT. Exactly two are
     added, so the heading total rises by 2, D4 and D5 each read 0 then 1, and
     the headings are DISTINCT at BOTH points. Report each at BOTH points.
 G7  THE LEDGER APPEND at C3, under the SAME two readers and the same negative
     control as G5, over `.agent/live_review.md` and RECORD7, based on the round
     base. Report the same values, with RECORD7's own unit count against
     constraint 4's ONE. Run the destructive halves of G5 and G7 inside a
     disposable worktree under `.remedy-wt/` whose name no directory already
     uses, and remove and prune it before the handback.
 G8  THE LEDGER SETS, line-anchored at line start, at the round base then at C3:
     `- R-` entries and how many are DISTINCT; `Done: R-` lines; `Landed: `
     lines; `Gate: R` keys and how many are DISTINCT; `Gate: R8` occurrences;
     and the MAXIMUM registered id. Report each at BOTH points. NO id is minted,
     so `- R-` reads 212 at BOTH points with both DISTINCT, the maximum reads
     R-0649 at BOTH points, `Gate: R` keys read 7 then 8 with both DISTINCT, and
     `Gate: R8` reads 0 then 1. Report `- R-0585 —` too, expected 1 at BOTH
     points because this round adds evidence to it and does not re-register it.
 G9  THE CONTRACT SUITES, run at C3 in the PRIMARY checkout and SERIALLY:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py -q -rf`. Report the exit code and
     the passed-plus-skipped total, counting BY PASSED PLUS SKIPPED. The
     reviewer measured exit 0 and 511 at the round base. No docs gate is owed:
     the `Change:` list holds no `docs/` path at all — check that against the
     list before you accept this sentence.
G10  CANARY, run at C3, serially, and after G9 has finished:
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report the exit
     code and the total. The reviewer measured exit 0 and 42 at the round base.
G11  THE T001 CONTRACT TEST STILL HOLDS, run at C3, serially, after G10:
     `python3 -m pytest tests/ui_contracts/ -q -rf`. Report the exit code and
     the passed-plus-skipped total; the reviewer measured exit 0 with 426 passed
     and 4 skipped at the round base. This round changes no file it reads, so a
     different reading is a regression from outside this round and is reported
     RED rather than explained.
G12  NO PRODUCTION FILE CHANGED: report that the range from the round base to C3
     holds 0 paths beginning `apps/`, `packages/` or `tests/`, and that
     `git ls-files .remedy-wt` reads 0.
G13  RANGE, executed at C3 and covering the round base to C3 — NOT to C4, because
     C4 writes the file that must quote this gate and §3 checklist item 31
     forbids ordering a reading the quoting artefact cannot yet hold. Report:
     the base-to-C3 path set against the five paths of this block's `Change:`
     list other than `.agent/handoff.md`, with the set difference EMPTY in both
     directions; every commit single-parent; `git show --numstat` and
     `git diff --numstat` agreeing cell by cell with the handback's `## Commits`
     table for C0a, C0b, C1, C2 and C3 (§3 checklist item 28); every insertion
     count under the 500 cap; leading `<<<SLICE ` and `<<<END ` reading 0 LINES
     in `.agent/plan.md`, `.agent/decisions.md` and `.agent/live_review.md`; and
     this round's reflog rows so far classified with `amend`, `rebase` and
     `cherry` each 0 in the operation field.
G14  NO PULL REQUEST: report `gh pr list --state open --json number,headRefName`
     and state that neither `gh pr create` nor `gh pr merge` was run. The
     expected reading is an EMPTY list, which is also the fact constraint 7(b)
     tells the next session to expect.
G15  THE HANDBACK carries every mandated section of
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

<<<SLICE PLANF021R8
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
R8 records the R7 verdict, adds the R7 evidence to R-0585, and rules the two
infrastructure DECISIONS T002 depends on: F021 D4 on the frontend test
environment and F021 D5 on the single-subscription fan-out. It mints no finding
id and builds nothing. The branch is mid-feature and carries no pull request by
design.

## Next Steps
1. R9 builds T002 on the ground D4 and D5 rule: the feed, its rows and the
   NowCard over fixture streams, with the scroll discipline that never yanks a
   reader who has scrolled up.
2. R10 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- T002's rules land in pure `.ts` modules under the node vitest D4 keeps, and
  its `.tsx` components are gated by a Python source contract under
  `tests/ui_contracts/`. A rule that reaches for the DOM is a sign it was put in
  the wrong half.
- The event ring D5 rules is the first state the brain-stream runner retains per
  event rather than in aggregate, so the view-identity contract that runner
  documents is the thing most likely to break under it.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- T001 is built and verified but its catalog covers only what a static walk can
  see. The generic line carries the eleven runtime-computed emitters, and R-0649
  records that the walk's roots also reach vendored third-party Python.
- The open set holds no code defect of F021; R-0403, R-0607, R-0608, R-0609,
  R-0611 and R-0613 stay routed to a paydown branch.
<<<END PLANF021R8

<<<SLICE DECIDE45
## DECISION F021 D4 (2026-08-22) — T002 adds no DOM test environment; its rules go into node-testable `.ts` modules and its components are gated by a Python source contract

CONTEXT, measured by the reviewer at `fc56d4cc`. `apps/ui/vitest.config.ts` sets `environment: "node"` with `include: ["src/**/*.test.ts"]`, so no `.tsx` test is collected and no DOM exists to render into; `find apps -name '*.test.tsx' -not -path '*/node_modules/*'` returns 0 files, and `jsdom`, `testing-library` and `happy-dom` occur 0 times in `apps/ui/package.json` and `apps/ui/vitest.config.ts`. T002 is component work, so the naive reading is that the environment must change. It must not, because this repository has already answered the question and written the answer down at the seam: the header comment of `apps/ui/src/api/useBrainStream.ts` states that it is "deliberately the ONLY part of it that is React at all: every rule this client has lives in brainStream.ts, brainStreamDriver.ts, brainStreamRunner.ts and brainStreamSession.ts, where the node-environment vitest can reach it", and that what remains is "gated by a tests/ui_contracts/ source contract, the style this repository uses for every React component". `tests/ui_contracts/` holds eleven such Python contract modules, `test_remedy_shell_stream.py` among them. The brain-stream family is that pattern at scale: six logic modules, each with a `.test.ts` neighbour the node vitest collects, behind one thin hook.

CHOSEN: T002 changes neither `environment` nor `include`. Every rule T002 needs becomes a pure module under `apps/ui/src/` with a `.test.ts` neighbour — the projection of a stream event into a feed row, the ACTION-class subset the NowCard shows, the recency state of the activity dot, and the scroll discipline as a `(pinnedToBottom, newEventArrived) -> shouldScroll` function. The `.tsx` components read an already-projected view and render it, and their structure is gated by a new Python source contract under `tests/ui_contracts/` written in the manner of `test_remedy_shell_stream.py`. The scroll rule is called out because it is the acceptance criterion that sounds least like a pure function and is one: "never yank a reader who has scrolled up" is entirely a decision about whether to scroll, and the only DOM left after that decision is a single `scrollTop` assignment no assertion is worth.

ALTERNATIVES CONSIDERED. Add `jsdom` and `@testing-library/react` and widen `include` to `.test.tsx`: rejected, it introduces a second test environment and three devDependencies into a package that deliberately has neither, to buy assertions about markup that the Python source contracts already make more cheaply and in the language every other gate in this repository is written in; it also stacks a React-DOM test suite on top of `apps/ui`'s lint config, which finding R-0622 measures as parsing none of the TypeScript it is aimed at, so the new files would be as unlinted as the old ones. Rewrite the components as render functions returning plain data: rejected, that is the chosen option with an extra layer of indirection and no additional coverage. Gate the feed through the Python source contracts ALONE: rejected, a source contract can assert that a component maps over its rows, and it cannot assert that the scroll never yanks — which the Acceptance section names outright.

REVERSE IT by adding `jsdom` and `@testing-library/react` to `apps/ui` devDependencies, setting `environment: "jsdom"` and widening `include` to `src/**/*.test.{ts,tsx}`. The `.ts` logic modules and their tests stay valid under that change, so the reversal is purely additive and costs no rewrite of anything T002 ships.

## DECISION F021 D5 (2026-08-22) — the fan-out is a bounded event ring inside the existing brain-stream runner, published on the existing view

CONTEXT, measured by the reviewer at `fc56d4cc`. The single subscription the feature file's Orchestrator brief demands ALREADY EXISTS and is not what is missing: `useBrainStream` occurs at three lines across `apps/ui/src/` — its definition, its import in `apps/ui/src/components/shell/RemedyShell.tsx`, and the one call in that shell — and the shell passes `stream.status` down into `RightLivePanel`. What is missing is the events themselves. `BrainStreamView` in `apps/ui/src/api/brainStreamRunner.ts` carries `status`, `lastSeq` and `gapDetected` and nothing else, and `BrainStreamState` in `apps/ui/src/api/brainStream.ts` adds only `attempt`: the runner dispatches every event and RETAINS none of them. That is why `ActivityFeedCard` is fed a `RemedyActivityItem[]` off the REST dashboard today — the current feed is a second DATA PATH rather than a second connection, and it is not live.

CHOSEN: T002 adds to `BrainStreamState` a `recent` ring of at most 500 projected rows, appended on dispatch and dropped from the front past the bound, and publishes it on `BrainStreamView` under the object-identity contract `createBrainStreamRunner` already documents — `view()` returns the SAME object until something visible changes, because `useSyncExternalStore` compares snapshots with `Object.is` and re-renders forever otherwise. The rows reach the feed and the NowCard by being passed down from the ONE `useBrainStream` call `RemedyShell` already makes, exactly as `stream.status` is passed down today. No second `useBrainStream` call, no new hook, and no `EventSource` constructed outside `apps/ui/src/api/brainStreamDeps.ts`. The drop past the bound is OBSERVABLE and never silent: once the ring has dropped anything, the feed says so and points at the timeline, which is what this feature file's own edge-case paragraph requires of a bounded window. The bound is a number rather than a promise because nothing upstream supplies one — `packages/orchestration/ui_server.py` caps concurrent streams per job at `SSE_MAX_STREAMS_PER_JOB = 4` and caps event COUNT nowhere — and 500 is far past the five rows the current card shows and far short of a memory concern.

ALTERNATIVES CONSIDERED. Call `useBrainStream` a second time in `RightLivePanel`: rejected outright, because that hook builds one session per call and each session opens its own `EventSource`, which is the second connection the Orchestrator brief rejects as an architecture line. A module-level singleton store outside React: rejected, it re-introduces exactly the connection-lifetime bug the cleanup comment in `useBrainStream` exists to prevent, and it makes two jobs on one page impossible. Keep feeding the feed from the REST dashboard's activity list: rejected, it is not the live stream, so the NowCard's recency dot would be honest about nothing and the feature's Goal — that the STREAM becomes a story a human can follow — would go unmet while looking met. An unbounded log: rejected, a long job grows it without limit and the feature file already calls for a bounded window.

REVERSE IT by deleting the `recent` field from `BrainStreamState` and `BrainStreamView` and restoring `ActivityFeedCard`'s dashboard-fed props. The graph, the status badge and the gap detection read none of it, so nothing else on the surface changes.
<<<END DECIDE45

<<<SLICE RECORD7
Gate: R8 — the R7 entry. R7 PASSED ON EVERY GATE, RE-MEASURED INDEPENDENTLY RATHER THAN READ BACK. R7 was a record-and-close round that built nothing, and every one of its thirteen gates reproduces under the reviewer's own execution. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f021-r7.md` at `487ac619`, `.agent/last_block.md` at `9bb77da3`, the working copy of `.agent/last_block.md`, and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f021-r7.md`, are all sha256 5d0eebbe12a16d57a1a3696944ef8f24f696e99ac1e2c69d990dde632b86957e over 21611 bytes and 223 lines, so §4.9's primary cmp-against-scratchpad proof was available and used rather than the digest fallback. SLICES: 2 over 47 CONTENT lines, TOTAL 223 against DECISION F085 D6's 490 and PROSE 176 against D5's 400, both equal to that block's constraint 8. THE WHOLE-FILE SLICE IS BYTE-EQUAL to what landed: `.agent/plan.md` at `0882ba7b` equals PLANF021R7 over 42 lines against the 50 cap, with RECORD6 as a negative control that differs. THE APPEND at `30a09f4b` is the round-base blob plus exactly one newline plus RECORD6, remainder sha256 2c4560714396bfc4c24d2ac451ca80f85324048fc9afdd98f48a706fc77a11ef over 7529 bytes, the file going 446046 bytes and 1080 lines to 453575 and 1086, units 221 plus RECORD6's own 3 to 224 with every base position equal elementwise. THE LEDGER SETS RECONCILE at this gate: 212 `- R-` entries all DISTINCT, maximum id R-0649, `Done: R-` 0 and `Landed: ` 0, and `Gate: R` keys R1 through R7 all DISTINCT. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout at `fc56d4cc`: the three contract suites exit 0 with 511 passed, the canary exit 0 with 42 passed, and `tests/ui_contracts/` exit 0 with 426 passed and 4 skipped — all three equal to R7's reported readings, so nothing regressed from outside that round. THE RANGE HELD: five commits every one single-parent, the path set EQUAL to that block's five `Change:` paths with both differences EMPTY, 0 paths beginning `apps/`, `packages/` or `tests/`, markers 0 in every file a slice landed in, `git ls-files .remedy-wt` 0, `git worktree list` ending with the primary checkout alone, and all five reflog rows `commit:` — amend 0, rebase 0, cherry 0, so no history was rewritten and nothing was force-pushed. THE TWO READINGS §3 CHECKLIST ITEM 31 LEAVES TO THIS GATE, taken here because the commits that would have had to state them are the very commits that wrote the quoting files: the R6 handback commit `6f5078d7` is single-parent, changes `.agent/handoff.md` alone at 72 insertions and 47 deletions, and the R7 handback commit `fc56d4cc` is single-parent, changes `.agent/handoff.md` alone at 39 insertions and 72 deletions — both far under the 500-insertion cap DECISION F104 D1 counts, and `git status --porcelain` reads 0 lines at `fc56d4cc`, which is the reading R7's G1 correctly declined to order for itself. WHY R7 IS PASS: every gate reproduces, the ledger arithmetic is exact, and the one deviation it declared is the reviewer's own block defect rather than a worker error. EVIDENCE FOR R-0585: the R7 block's constraint 7(c) ordered the handback to tell the next session that "R7 must FIRST rule the two infrastructure DECISIONS" while the block itself IS R7, states in its own Goal that it "BUILDS NOTHING", and ships a PLANF021R7 slice — committed at `0882ba7b` in that same round — assigning those DECISIONS to R8 and T002 to R9. Two clauses of one block, disagreeing about which round does the work, which is R-0585's exact clause-versus-clause shape; and the reach that finding already carries is the right one, because the list constraint 7(c) contradicts does not sit beneath it but fifty lines away inside a slice. Nothing false landed on disk: the worker wrote the substance of 7(c) into `## Next` without the round attribution, declared the contradiction, and left the numbering to this gate — which now settles it in the only direction the record permits, namely the plan's, since R7 demonstrably ruled neither DECISION and this round rules both.
<<<END RECORD7
