── STEP DECIDE — F021 ──
Goal:        Record the R2 verdict, then repair the specification R2 measured
             false. Two DECISIONS are ruled and the feature file is amended to
             match the source, so R4 can build T001 against a contract that
             exists. This round RULES and RECORDS; it builds nothing and touches
             no file under `apps/`, `packages/` or `tests/`.

Fortschritt: ~10 % (T001 offen · T002 offen · T003 offen; R1 beansprucht, R2
             vermessen, R3 entscheidet und korrigiert die Spezifikation —
             gebaut wird ab R4) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R2 verdict ·
             C3 the two DECISIONS · C4 the feature-file amendment and the
             handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r3.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/decisions.md` (C3) · `docs/roadmap/features/T5_F021.md`
             and `.agent/handoff.md` (BOTH in C4).
             That list is SEVEN paths; resolve any count in this block against
             this list rather than against a numeral written elsewhere.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). C4 is last and carries the handback, so its own row is measured on
    staged content.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NOTHING. It writes no `- R-`
    entry, no `Done:` line and no `Landed:` line. R-0648 stays the maximum
    registered id and R-0649 is the next free one. The specification defects R2
    measured are ruled as DECISIONS rather than registered as findings, which is
    what docs/agents/planner_reviewer_prompt.md §4 item 7 requires of a wrong
    spec: the reviewer authors the concrete amendment, records an
    operator-visible DECISION, and proceeds under it. The operator's veto is any
    later relay.
 4. TWO APPENDS, ONE WHOLE-FILE REPLACEMENT AND THREE FROM/TO PAIRS.
    PLANF021R3 replaces `.agent/plan.md` at C1 in full. RECORD2 appends to
    `.agent/live_review.md` at C2, based on the ROUND BASE. DECIDE1 appends to
    `.agent/decisions.md` at C3, based on the ROUND BASE. The three pairs all
    apply at C4 to `docs/roadmap/features/T5_F021.md`.
 5. THE PAIRS, with the containment reading PRINTED BY THE REVIEWER'S OWN SCRIPT
    against the target at the round base `4a7b5cbf` and recorded here one per
    pair (§3 checklist item 15): AMENDA `TO contains FROM: false`, so REWRITE;
    AMENDB `TO contains FROM: false`, so REWRITE; AMENDC `TO contains FROM:
    false`, so REWRITE. All three are rewrites, so order the FROM-zero count for
    each and none of them carries the §4.9 append obligation. Each pair's FROM
    occurs EXACTLY ONCE in that file at `4a7b5cbf` — the reviewer's script
    printed 1 for all three. Apply each with `count=1` and report the occurrence
    count you measured BEFORE each replacement. Apply them in the order AMENDA,
    AMENDB, AMENDC.
 6. THE AMENDMENTS ARE CORRECTIONS OF FACT, and each is anchored to the commit
    its reading was taken at, because a sentence about a source file that names
    no commit is stale before the round ends (§3 item 20). AMENDA replaces the
    claim that events already carry the graph linkage. AMENDB replaces the
    coverage test's reference to a "Part E kind list" that does not exist. AMENDC
    narrows the Do-not-touch ban on the event schema, which as written forbade
    the only route to this feature's own acceptance criterion.
 7. NO PRODUCTION FILE IS EDITED. You may READ anything. Do not create, modify
    or delete a file under `apps/`, `packages/` or `tests/`, and run no
    formatter or linter that rewrites a file in place.
 8. Do NOT create a pull request and do NOT merge one. F021 opens its pull
    request at closure.
 9. Block size, measured on these final bytes: TOTAL 274 lines against DECISION
    F085 D6's 490, and PROSE — TOTAL minus the slice CONTENT lines — 180
    against DECISION F085 D5's 400. Marker lines count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C4; the branch is `feature/f021-live-activity-feed`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2 and
     C3. C4's own reading goes in the round report (§3 checklist item 14).
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r3.md` at C0a, over
     `.agent/last_block.md` at C0b, and over the bytes you received are all
     equal. Write C0b FROM the committed C0a blob. Report the digest with the
     byte and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 9's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF021R3, proved with `cmp` at
     exit 0 against the slice extracted from the committed C0a blob, with a
     NEGATIVE CONTROL against RECORD2 that must exit 1. Report both exit codes,
     plus `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE TWO APPENDS, each under TWO INDEPENDENT READERS. For C2 over
     `.agent/live_review.md` and for C3 over `.agent/decisions.md`, both based on
     the round base: reader (a) the round-base blob is a byte-exact PREFIX and
     the remainder is EXACTLY one newline plus the slice — report each
     remainder's sha256, byte count and line count, and each file's byte and
     line counts before and after; reader (b) split BOTH blobs on the blank line
     into units, report N at each point, and confirm the LAST unit equals the
     slice while the base's last unit does not. NEGATIVE CONTROL, run for BOTH
     files: replace one printable byte of the FIRST paragraph at equal length
     and confirm BOTH readers REJECT that mutant while BOTH ACCEPT the true file
     (R-0631). Run the destructive half inside a disposable worktree under
     `.remedy-wt/`, never in the primary checkout, and remove and prune it
     before the handback.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then at C2:
     `- R-` entries and how many are DISTINCT; `Done: R-` lines; `Landed: `
     lines; `Gate: R` keys and how many are DISTINCT; `Gate: R3` occurrences;
     and the MAXIMUM registered id. Report each at BOTH points. Nothing is
     minted, so the maximum reads R-0648 at both.
 G7  THE DECISION HEADINGS, line-anchored over `.agent/decisions.md` at the
     round base then at C3: `^## DECISION ` total, `^## DECISION F021 D1 ` and
     `^## DECISION F021 D2 `. Report all three at both points. The base reads 0
     for both F021 headings, so a reading of 1 each at C3 proves the append
     landed once and not twice.
 G8  THE THREE PAIRS at C4 over `docs/roadmap/features/T5_F021.md`: report each
     FROM's occurrence count measured BEFORE its replacement, which must be 1,
     and AFTER C4 report each FROM reading 0 and each TO reading 1. Report
     `git show --numstat` for that path at C4.
 G9  THE DOCS GATES, both, run serially after C4 because C4 touches
     `docs/roadmap/features/**`: `python3 -m pytest tests/docs/ -q -rf` and
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`.
     Report both exit codes and both totals. The second is ordered because
     `tests/docs/` asserts nothing about a feature file's BODY, which is finding
     R-0493 and is exactly the case this round is in.
 G10 THE CONTRACT SUITES, run in the PRIMARY checkout and SERIALLY after G9:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py -q -rf`. Report the exit code and
     the passed-plus-skipped total, counting BY PASSED PLUS SKIPPED.
 G11 CANARY, run serially and after G10 has finished:
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report the exit
     code and the total.
 G12 NO PRODUCTION FILE CHANGED: report that the range from the round base to C4
     holds 0 paths beginning `apps/`, `packages/` or `tests/`, and that
     `git ls-files .remedy-wt` reads 0.
 G13 RANGE, executed after C4: the range from the round base to C4 lists exactly
     the paths of this block's `Change:` list, with the set difference EMPTY in
     both directions. Report both differences. Then: every commit single-parent;
     `git show --numstat` and `git diff --numstat` agreeing cell by cell with
     the handback's own `## Commits` table (§3 checklist item 28); every
     insertion count under the 500 cap; leading `<<<SLICE ` and `<<<END `
     reading 0 LINES in each of the four files a slice lands in; and this
     round's reflog rows classified with `amend`, `rebase` and `cherry` each 0.
 G14 NO PULL REQUEST: report `gh pr list --state open --json number,headRefName`
     and state that neither `gh pr create` nor `gh pr merge` was run.
 G15 THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3 and C4, the round base SHA, ONE LINE PER GATE with the
     transcripts kept in the round report rather than in the file (R-0582), and
     the block's `Fortschritt:` line verbatim across all three of its lines. Its
     own `wc -l` is reported, with a DECISION D15 line declaring any overage and
     naming the mandated content that caused it. Every commit heading in the
     `## Commits` table carries that commit's FULL subject, and where a commit
     cannot name its own SHA the role and the reason are written INSIDE the
     heading rather than left to a channel that ends with this session — that
     omission is finding R-0494.

Handback:   completion report + rewrite `.agent/handoff.md`.

<<<SLICE PLANF021R3
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
kind set DECISION F021 D1 rules and an unknown kind renders an honest generic
line rather than vanishing, the feed renders fixture streams per the binding CSS,
jump-to-node focuses the right node, and the steering input renders DISABLED with
its honest tooltip until F030 lands.

## Current Step
R3 records the R2 verdict, rules DECISIONS F021 D1 and D2 on the ground R2
measured, and amends `docs/roadmap/features/T5_F021.md` so its coverage-test
contract, its jump-to-node premise and its Do-not-touch ban match the source. It
builds nothing.

## Next Steps
1. R4 builds T001 headless-first: the humanize catalog module, the coverage test
   D1 rules, the honest generic line for an unrecognised kind, and goldens.
2. R5 rules the two remaining infrastructure DECISIONS on the same measured
   ground before T002 needs them — the frontend test environment, which today
   collects no component test, and the single-subscription fan-out.
3. R6 onward T002 then T003, in the feature file's Task slicing order.

## Risks
- T002 cannot be tested until the frontend test environment changes: measured at
  `4a7b5cbf`, `apps/ui/vitest.config.ts` sets `environment: "node"` and
  `include: ["src/**/*.test.ts"]`, so no `.test.tsx` is collected at all. R5
  rules it; R4 does not need it because T001 is a pure module.
- Jump-to-node needs an additive field on the SSE envelope, which DECISION F021
  D2 permits and AMENDC carves out of the feature file's Do-not-touch. That is
  the one production seam this feature must open, and it stays one field.
- The open set carried into this record at R1 holds no code defect of F021;
  R-0403, R-0607, R-0608, R-0609, R-0611 and R-0613 stay routed to a paydown
  branch.
<<<END PLANF021R3

<<<SLICE RECORD2
Gate: R3 — the R2 entry. R2 PASSED, AND ITS DELIVERABLE IS A SPECIFICATION DEFECT RATHER THAN A LINE OF CODE. The reviewer re-executed the round's gates off disk and additionally re-measured the inventory's load-bearing readings against the SOURCE, because G7 was written as a SHAPE check and says so in its own text: a green G7 proves five sections exist and cites files, never that a reading is true. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f021-r2.md` at `78afebcc`, `.agent/last_block.md` at `2a5e6611` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f021-r2.md`, are all sha256 9e0b791a263135fd11d1502b45d5c4c87722ed31988145375d8f114f0214e4da over 19837 bytes and 226 lines, so §4.9's primary cmp-against-scratchpad proof was available and used rather than the digest fallback. `.agent/plan.md` at `41bb3bf2` is byte-equal to PLANF021R2 at 44 lines against the 50-line cap. THE APPEND HELD under the reviewer's own two readers: at `2488ff1d` the round-base blob is a byte-exact PREFIX and the remainder is exactly one newline plus RECORD1. THE SETS HELD line-anchored at C2: 211 entries all DISTINCT, `Done: R-` 0, `Landed: ` 0, `Gate: R` keys 2 over 2 DISTINCT, `Gate: R2` 1, maximum registered id R-0648 — nothing was minted. THE RANGE HELD: five commits, every one single-parent, the range path set EQUAL to the block's declared six with the difference empty in both directions, and 0 paths beginning `apps/`, `packages/` or `tests/`, which is the property a measurement round most needs to prove about itself. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: `tests/ui_server/` with `test_test_runner.py` and `test_resource_safety.py` at exit 0 and 511 passed, and the canary `tests/cli/test_golden_path.py` at exit 0 and 42 passed. THREE OF THE INVENTORY'S READINGS WERE RE-MEASURED BY THE REVIEWER AGAINST THE SOURCE AND ALL THREE HOLD, which is why the DECISIONS below rest on them. FIRST, THE ENVELOPE: `_safe_event_summary` in `packages/orchestration/ui_server.py`, read at `4a7b5cbf`, returns exactly the four keys `seq`, `event`, `timestamp` and `outcome`, and its own docstring states that it has ONE writer and that a field added there reaches both the cursor endpoint and the SSE stream. No node id and no task id is present, so a feed row has nothing to resolve to a graph node. SECOND, THE TEST ENVIRONMENT: `apps/ui/vitest.config.ts` at that same commit sets `environment: "node"` and `include: ["src/**/*.test.ts"]`, so a `.test.tsx` file is not collected and no component test is expressible today. THIRD, THE FOCUS SURFACE: the three modules under `apps/ui/src/components/graph/` export `ForceBrainGraph`, `buildForceBrainModel` and the `forceBrainTypes` types and NOTHING that focuses a node — the only focus surface is an `onSelectNode` callback prop threaded from a parent's state, exactly as the inventory reports. THE FEATURE FILE IS WRONG IN THREE PLACES AND CONTRADICTS ITSELF IN ONE, which is a spec defect routed to planning under §4 item 7 rather than a finding against the worker, and the round that measured it deviated from nothing. Its "How it fits" states that events already carry the linkage the reducer used and that jump-to-node should reuse that mapping; measured, they carry no such field. Its T001 slice specifies a coverage test against "the Part E kind list"; measured, no such list exists — `RunEvent.event` is an unvalidated free string, the four defined kind sets are pairwise disjoint, and of the distinct literals actually emitted only one appears in any of them, so a coverage test written as specified would have been green against almost nothing. And its Do-not-touch bans the event schema outright while its own Goal & Done requires jump-to-node, so the file forbade the only route to its own acceptance criterion. DECISIONS F021 D1 and D2 are ruled in `.agent/decisions.md` by the block this entry is committed by, and the same block amends the feature file to match the source; both are operator-visible and reversible by any later relay, and neither widens this feature's scope beyond the one additive field D2 names. THE VERDICT IS PASS: R2 was ordered to measure and it measured, it wrote no production file, it minted no id, and the inconvenient result it returned is the reason the round was worth running.
<<<END RECORD2

<<<SLICE DECIDE1
## DECISION F021 D1 (2026-08-22) — the humanize catalog's coverage test is keyed on the kinds the STREAM can carry, because no "Part E kind list" exists

CONTEXT, measured at `4a7b5cbf` and recorded in `.agent/f021_inventory.md`: the feature file's T001 slice orders "coverage test against the Part E kind list", and there is no such list. `RunEvent.event` is an unvalidated free string; four defined kind sets exist — `NARRATED_EVENTS`, `EVENT_METADATA_SCHEMAS`, `TRACE_EVENT_KINDS` and `_STREAM_EVENT_KINDS` — and they are pairwise disjoint; and of the distinct literals actually passed at run-log emission sites, only one appears in any of those four sets. A coverage test written against any one of them would pass while covering almost nothing that reaches a reader, which is the silently-vacuous-gate class of R-0438 arriving through a specification instead of a gate.

CHOSEN: T001 defines its own authoritative constant — the set of kinds the humanize catalog claims to cover — in the humanize module itself, and the coverage test asserts that the catalog's key set EQUALS that constant, so a kind added to one and not the other goes red. That constant is seeded from the emission literals that can be enumerated STATICALLY. The emission sites that compute their kind name at runtime cannot be enumerated by any test, and they are covered instead by the feature file's own unknown-kind rule: an unrecognised kind renders an honest generic line and is never dropped. That rule therefore stops being a nicety and becomes the load-bearing half of the contract, so T001 ships a test for the generic path beside the coverage test.

ALTERNATIVES CONSIDERED. Key the test on the union of the four defined sets: rejected, because the union describes almost nothing the stream actually carries, so the test would be green and worthless. Make `RunEvent.event` a closed enum at the source: rejected for THIS feature, because it edits the event schema far beyond the one field D2 permits and would touch every emission site; it is the right long-term fix and belongs to a feature that owns the schema. Skip the coverage test: rejected, the feature file names drift protection as T001's purpose.

REVERSE IT by deleting the constant and the equality assertion; the catalog and the generic-line rule stand without them.

## DECISION F021 D2 (2026-08-22) — jump-to-node gets ONE additive field on the SSE envelope, and the feature file's Do-not-touch is narrowed to permit exactly it

CONTEXT, measured at `4a7b5cbf`: `_safe_event_summary` in `packages/orchestration/ui_server.py` returns exactly `seq`, `event`, `timestamp` and `outcome`, dropping `RunEvent.task_id` and the event metadata. The feature file's "How it fits" asserts that events already carry the linkage the reducer used; they do not. Its Goal & Done requires feed rows to click-jump to their node, and its Do-not-touch bans the event schema, so as written the file forbids the only route to its own acceptance criterion — a contradiction internal to the specification, not a trade-off.

CHOSEN: add ONE additive field carrying the task or node linkage to `_safe_event_summary`, and narrow the Do-not-touch ban to permit exactly that field and nothing else. The seam is the right one and says so in its own docstring: it has ONE writer, and a field added there reaches the cursor endpoint and the SSE stream together, so the two transports cannot drift. The field is additive, so every existing consumer keeps working. The client side must also stop discarding the payload, which is a client change and not a schema one.

ALTERNATIVES CONSIDERED. Drop jump-to-node from F021: rejected, it is named in Goal & Done and in T003, so dropping it silently reduces the feature to less than its acceptance criteria. Resolve the node client-side by matching on timestamp or seq: rejected, it invents a second mapping the reducer does not use, which is exactly the "one source" property the feature file asks for and would be wrong whenever two events share a timestamp. Add the whole event metadata blob: rejected, it widens the schema change from one field to an unbounded one and carries data the feed does not need.

REVERSE IT by removing the field and restoring the blanket Do-not-touch line; jump-to-node then has to leave the feature with it.
<<<END DECIDE1

<<<SLICE AMENDAFROM
verbose views. Jump-to-node targets the reducer's node ids
(events already carry the linkage the reducer used — reuse the
same mapping, one source). The steering input is a design
<<<END AMENDAFROM

<<<SLICE AMENDATO
verbose views. Jump-to-node needs a node id the stream does not
carry today: measured at 4a7b5cbf, `_safe_event_summary` in
`packages/orchestration/ui_server.py` emits exactly seq, event,
timestamp and outcome and drops the task linkage, so DECISION
F021 D2 adds ONE additive field at that single-writer seam rather
than inventing a second client-side mapping. The steering input
is a design
<<<END AMENDATO

<<<SLICE AMENDBFROM
- **T001** the humanize catalog + coverage test against the Part
  E kind list (a new kind without a template fails the coverage
  test — drift protection) + goldens.
<<<END AMENDBFROM

<<<SLICE AMENDBTO
- **T001** the humanize catalog + coverage test against the kind
  set DECISION F021 D1 rules, because no "Part E kind list"
  exists: measured at 4a7b5cbf, `RunEvent.event` is an
  unvalidated free string and the four defined kind sets are
  pairwise disjoint. A kind in that set without a template fails
  the coverage test (drift protection), and the emission sites
  that compute their kind at runtime are covered by the
  unknown-kind generic line instead + goldens.
<<<END AMENDBTO

<<<SLICE AMENDCFROM
## Do not touch
Steering's backend (F030), event schema, graph internals beyond
the focus API. Suggested tests: frontend tests per conventions +
humanize goldens.
<<<END AMENDCFROM

<<<SLICE AMENDCTO
## Do not touch
Steering's backend (F030), graph internals beyond the focus API,
and the event schema EXCEPT the single additive field DECISION
F021 D2 rules onto `_safe_event_summary` — the blanket ban as
first written forbade the only route to this feature's own
jump-to-node acceptance criterion. Suggested tests: frontend
tests per conventions + humanize goldens.
<<<END AMENDCTO
