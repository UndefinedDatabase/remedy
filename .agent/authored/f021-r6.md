── STEP T001 — F021 ──
Goal:        Build T001 on the ground R5 corrected: the humanize catalog and its
             honest generic line, the vitest behaviour tests, and the contract
             test DECISION F021 D3 rules, which re-derives the stream's kind
             vocabulary from the Python emitters and asserts it EQUALS the
             catalog's key set so drift goes red from either side. This round
             also records the R5 verdict and promotes the rule R-0449 and
             R-0494 have now cost three rounds into the §3 checklist, because a
             rule that lives only in a finding body binds nothing.

Fortschritt: ~30 % (T001 gebaut · T002 offen · T003 offen; R1-R5 Anspruch,
             Vermessung, Entscheidung, Verdikt und Korrektur — R6 ist die erste
             Runde, die Produktionscode liefert) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R5 verdict
             with the R-0449 and R-0494 evidence · C3 the §3 checklist item ·
             C4 the humanize module · C5 the catalog data · C6 the vitest
             behaviour tests · C7 the contract test · C8 the handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r6.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `docs/agents/planner_reviewer_prompt.md` (C3) ·
             `apps/ui/src/api/humanize.ts` (NEW, C4) ·
             `apps/ui/src/api/humanizeCatalog.ts` (NEW, C5) ·
             `apps/ui/src/api/humanize.test.ts` (NEW, C6) ·
             `tests/ui_contracts/test_humanize_catalog.py` (NEW, C7) ·
             `.agent/handoff.md` (C8).
             Resolve any count in this block against that list rather than
             against a numeral written elsewhere.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8 and is not
    negotiable. C1 precedes the ledger commit because the plan must be current
    before it (§3 checklist item 23). C3 precedes the code because RECORD5 says
    the checklist edit is ordered by this block and C2 must not be the last word
    on it. C8 carries only the handback.
    ROUND BASE is `82fcc7c0272d366e36ebda5020dbc1697d98e32b` and is the commit
    every "round base" in this block names.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NOTHING. It writes no `- R-`
    entry, no `Done:` line and no `Landed:` line. R-0648 stays the maximum
    registered id and R-0649 is the next free one. The two defects this round
    records are the REVIEWER'S OWN and are added as evidence to the OPEN
    findings R-0449 and R-0494 rather than under new ids, because §3 checklist
    item 30 requires the open set to be searched for the DEFECT first and that
    search returned both holding exactly these shapes.
 4. SLICE SHAPES. PLANF021R6 replaces `.agent/plan.md` at C1 in full and
    HUMANIZE creates `apps/ui/src/api/humanize.ts` at C4 in full; both are
    proved with `cmp`. RECORD5 appends to `.agent/live_review.md` at C2, based
    on the ROUND BASE. CHECKFROM and CHECKTO are the ONE FROM/TO pair of this
    round, applied to `docs/agents/planner_reviewer_prompt.md` at C3. The
    reviewer ran the containment test on that pair before emission and its
    output is `TO contains FROM: true`, so the pair is APPEND-shaped and the
    §4.9 append obligation applies to it — FROM exactly 1x, and each TO-ONLY
    line exactly 1x among the lines C3's diff ADDS. Do NOT order or report a
    "FROM 0x" count for it; that count is unattainable for an append by
    construction. Measured by the reviewer on the slices' own bytes before
    emission: RECORD5 is ONE blank-line unit.
 5. THE CATALOG IS YOURS TO WRITE; ITS KEY SET IS NOT. `humanizeCatalog.ts` at
    C5 exports exactly one symbol, `STREAM_EVENT_CATALOG`, typed
    `Readonly<Record<string, string>>`. Its keys are EXACTLY the static stream
    vocabulary G5 derives, ASCII-sorted, one entry per line in the form
    `  "<key>": "<line>",` — two-space indent, double-quoted key, colon, one
    space, double-quoted value, trailing comma — because the contract test
    extracts keys by scanning those lines and a different shape silently
    shrinks the set it reads. Each value is a complete English sentence ending
    in a full stop, non-empty, and the values are DISTINCT from one another. No
    value may equal `<key> event`: that is the generic form the module produces
    for kinds nobody can enumerate, and using it as a template is a stub
    wearing a catalog entry's clothes.
 6. WRITE THE TESTS YOURSELF, to the conventions the repository already uses.
    `humanize.test.ts` at C6 follows the vitest style of
    `apps/ui/src/components/graph/buildForceBrainModel.test.ts` — no fakes, one
    invariant per `it`. `tests/ui_contracts/test_humanize_catalog.py` at C7
    follows `tests/ui_contracts/test_brain_stream_hook.py`: it reads SOURCE
    TEXT, it strips comments before asserting on it, and it carries a test that
    proves its own stripper really removes a comment the file really carries
    (finding R-0584). It must ALSO prove its own key extractor: a test that the
    extractor finds a key the catalog really carries, and a test that a key
    written only inside a comment is NOT extracted.
 7. THE CONTRACT TEST ASSERTS SET EQUALITY, NEVER A LITERAL COUNT. It derives
    the kind set from the Python sources by the G5 predicate and asserts that
    set EQUALS the catalog's extracted key set, reporting the symmetric
    difference by name on failure, and it separately asserts both sets are
    non-empty. It must NOT hard-code 83 or any other size: a literal there
    becomes a second source of truth that drifts, and the equality is what the
    drift protection actually needs.
 8. NO OTHER PRODUCTION FILE IS EDITED. You may READ anything. Beyond the four
    NEW files this block names, do not create, modify or delete anything under
    `apps/`, `packages/` or `tests/`, and run no formatter or linter that
    rewrites a file in place.
 9. Do NOT create a pull request and do NOT merge one. The branch stays open and
    unmerged: F021 is mid-feature. Push the branch.
10. Block size, measured on these final bytes AFTER the last edit: TOTAL 357
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 251 against DECISION F085 D5's 400. Marker lines count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C8; the branch is `feature/f021-live-activity-feed`; and
     `git status --porcelain` prints 0 lines after each of C0a through C7. C8's
     own reading is ordered NOWHERE — the reviewer measures it at the next gate
     and records it there, which is the counter-measure the §3 item C3 adds
     states and which R-0494 exists because two rounds did not apply.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r6.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's own emitted copy still on disk at `.remedy-wt/f021-r6.md` are
     all equal. Write C0b FROM the committed C0a blob. Report the digest with
     the byte and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 10's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF021R6 and
     `apps/ui/src/api/humanize.ts` at C4 is byte-equal to HUMANIZE, each proved
     with `cmp` at exit 0 against the slice extracted from the committed C0a
     blob, each with a NEGATIVE CONTROL against the other slice that must exit
     1. Report all four exit codes, plus `^## Goal$` 1, `^## Next Steps$` 1 and
     `wc -l` at most 50 for the plan.
 G5  THE EMITTER DERIVATION, taken by YOU. Walk `packages/`, `apps/` and
     `scripts/` with `ast.parse` over every `*.py` that parses, and count a call
     site when the callee is an attribute named `log` or `append_run_event`, or
     a bare name `append_run_event`, AND an event argument is present — the
     first positional argument for `log`, or the `event=` keyword for either.
     The STATIC STREAM VOCABULARY is: the distinct string-constant names from
     that walk, plus `TRACE_EVENT_KINDS`, plus the VALUES of
     `_STREAM_EVENT_KINDS` (both in
     `packages/orchestration/agent_run_trace.py`), plus the value of the
     module constant `COMMAND_ACCEPTED_EVENT` in
     `packages/orchestration/ui_server.py`. Report its size, expected 83, and
     the four G5 readings DECISION F021 D3 states — 82 call sites, 60 distinct
     literals, 11 non-constant event arguments, 15 names inside the union of
     the four defined sets. A disagreement is reported RED and the round stops.
 G6  THE APPEND at C2 over `.agent/live_review.md`, under TWO INDEPENDENT
     READERS. Obtain the base blob with `git show <round base>:<path>` into
     memory or into scratch under `.remedy-wt/`; never overwrite a tracked file
     to read an older revision, which docs/agents/self_drive_protocol.md
     guardrail G5 forbids outright. Reader (a): the round-base blob is a
     byte-exact PREFIX of the committed file and the remainder is EXACTLY one
     newline plus RECORD5 — report the remainder's sha256, byte count and line
     count, and the file's byte and line counts before and after. Reader (b),
     the SET-WISE form: split BOTH blobs on the blank line into units and
     confirm the new unit LIST equals the base unit list followed by RECORD5's
     own units, compared ELEMENTWISE over the whole list and not at the tail;
     report N at both points. NEGATIVE CONTROL: replace one printable byte of
     the FIRST paragraph of the committed file at equal length and confirm BOTH
     readers REJECT that mutant while BOTH ACCEPT the true file; name the byte
     offset and the substitution. Run every destructive step inside a
     disposable worktree under `.remedy-wt/`, and remove and prune it before
     the handback.
 G7  THE PAIR at C3 over `docs/agents/planner_reviewer_prompt.md`, under the
     §4.9 APPEND obligation constraint 4 fixes: report CHECKFROM's occurrence
     count in the file at the ROUND BASE, which must be 1, and its count at C3,
     which must also be 1 because the TO contains it; then report, over the
     lines C3's diff ADDS, that each TO-ONLY line occurs exactly 1x. Report the
     file's line count before and after and `git show --numstat` for C3. Also
     report `^  31\. \*\*` in that file, expected 0 at the base and 1 at C3, and
     `^  32\. \*\*`, expected 0 at both.
 G8  THE LEDGER SETS, line-anchored at line start, at the round base then at C2:
     `- R-` entries and how many are DISTINCT; `Done: R-` lines; `Landed: `
     lines; `Gate: R` keys and how many are DISTINCT; `Gate: R6` occurrences;
     and the MAXIMUM registered id. Report each at BOTH points. Nothing is
     minted, so the maximum reads R-0648 at both and `Gate: R6` reads 0 then 1.
     Report `- R-0449 —` and `- R-0494 —` at both points as well; each must
     read 1 at both, since this round adds evidence and re-registers nothing.
 G9  THE CATALOG, measured at C5 from the committed blob: the number of exported
     symbols, expected 1; the number of extracted keys, which must EQUAL the G5
     vocabulary size; that the key list is ASCII-sorted and holds no duplicate;
     that the values are DISTINCT and their count equals the key count; that
     every value is non-empty and ends in a full stop; and that 0 values equal
     `<key> event` for their own key. Report every one of those numbers.
G10  TYPECHECK, in the PRIMARY checkout: `npx tsc --noEmit` with cwd `apps/ui`.
     Report the exit code at the ROUND BASE and at C7. The reviewer measured
     exit 0 at the round base, so a non-zero reading at C7 is this round's own
     regression and is reported RED rather than explained.
G11  VITEST, in the PRIMARY checkout, run at C7: `npx vitest run` with cwd
     `apps/ui`. Report the exit code, the test-file count and the test count at
     the ROUND BASE and at C7. The reviewer measured exit 0, 10 files and 152
     tests at the round base; the file count must therefore read 11 at C7 and
     the test count must exceed 152. Report the wall time too, because
     `tests/orchestration/test_test_runner.py` runs this same command under a
     hard 30-second timeout.
G12  THE NEW CONTRACT TEST, run at C7 in the PRIMARY checkout:
     `python3 -m pytest tests/ui_contracts/ -q -rf`. Report the exit code and
     the passed-plus-skipped total; the reviewer measured exit 0 with 417
     passed and 4 skipped, so the total must exceed 421 by the number of tests
     C7 adds, which you also report. RED CONTROL, inside a disposable worktree
     at C7 and never in the primary checkout: delete ONE entry line from
     `apps/ui/src/api/humanizeCatalog.ts` and re-run
     `python3 -m pytest tests/ui_contracts/test_humanize_catalog.py -q -rf`.
     It must FAIL, and the failure output must NAME the key you deleted. Report
     the key, the exit code and the naming line. A green run here means the
     equality assertion is vacuous and the round stops RED.
G13  THE CONTRACT SUITES, run at C7 in the PRIMARY checkout and SERIALLY:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py -q -rf`. Report the exit code and
     the passed-plus-skipped total, counting BY PASSED PLUS SKIPPED. The
     reviewer measured exit 0 and 511 at the round base. No docs gate is owed:
     the `Change:` list holds a `docs/agents/` path and no `docs/roadmap/**`
     path — check that against the list before you accept this sentence.
G14  CANARY, run at C7, serially, and after G13 has finished:
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report the exit
     code and the total.
     Gates G10 through G14 run at C7 and NOT after C8, so every reading the
     handback states already exists when C8 writes it. That ordering is the
     whole point of the §3 item C3 adds; do not defer any of them past C8.
G15  RANGE, executed at C8: the range from the round base to C8 lists exactly
     the paths of this block's `Change:` list, with the set difference EMPTY in
     both directions. Report both differences. Then: every commit single-parent;
     `git show --numstat` and `git diff --numstat` agreeing cell by cell with
     the handback's own `## Commits` table (§3 checklist item 28); every
     insertion count for C0a through C7 under the 500 cap; leading `<<<SLICE `
     and `<<<END ` reading 0 LINES in every file a slice lands in; and this
     round's reflog rows classified with `amend`, `rebase` and `cherry` each 0
     in the operation field. `git ls-files .remedy-wt` reads 0.
G16  NO PULL REQUEST: report `gh pr list --state open --json number,headRefName`
     and state that neither `gh pr create` nor `gh pr merge` was run. The
     expected reading is an EMPTY list.
G17  THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a
     through C8, the round base SHA, ONE LINE PER GATE with the transcripts kept
     in the round report rather than in the file (R-0582), the block's
     `Fortschritt:` line verbatim across all three of its lines, and a `## Next`
     section naming R7 and T002. Its own `wc -l` is reported against the
     100-line allowance a nine-commit bundle carries, with a DECISION D15 line
     declaring any overage and naming the mandated content that caused it.
     Every commit heading in the `## Commits` table carries that commit's FULL
     subject, and where a commit cannot name its own SHA the role and the reason
     are written INSIDE the heading rather than left to a channel that ends with
     this session — that omission is finding R-0494.

Handback:   completion report + rewrite `.agent/handoff.md`.

<<<SLICE PLANF021R6
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
R6 builds T001: the humanize module with its honest generic line, the catalog
data whose key set the contract test pins to the Python emitters, the vitest
behaviour tests, and that contract test. It also records the R5 verdict and
promotes the rule R-0449 and R-0494 carry into the §3 pre-emission checklist.

## Next Steps
1. R7 rules the frontend test environment, which today collects no component
   test at all, and the single-subscription fan-out — both are infrastructure
   DECISIONS T002 needs before it can be written.
2. R8 builds T002: the feed, its rows and the NowCard over fixture streams, with
   the scroll discipline that never yanks a reader who has scrolled up.
3. R9 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- T002 cannot be tested until the frontend test environment changes: measured at
  `82fcc7c0`, `apps/ui/vitest.config.ts` sets `environment: "node"` and
  `include: ["src/**/*.test.ts"]`, so no `.test.tsx` is collected at all. R7
  rules it.
- The catalog cannot cover the kinds whose names are computed at runtime; G5
  measures eleven such writers. The generic line is the whole of their coverage,
  which is why T001 ships its test rather than treating it as a nicety.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- The open set holds no code defect of F021; R-0403, R-0607, R-0608, R-0609,
  R-0611 and R-0613 stay routed to a paydown branch.
<<<END PLANF021R6

<<<SLICE RECORD5
Gate: R6 — the R5 entry. R5 PASSED ON EVERY GATE, RE-MEASURED INDEPENDENTLY RATHER THAN READ BACK, AND IT SURFACED TWO DEFECTS THAT ARE BOTH THE REVIEWER'S. THE ARTEFACTS WERE REBUILT, NOT CHECKED: the reviewer re-derived every applied artefact from the round base `91d14c88` and each is byte-identical to what landed. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f021-r5.md` at `d5f9d141`, `.agent/last_block.md` at `464bab56` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f021-r5.md`, are all sha256 8a489735b3da1261ad4ada770591a063bca6fcd03c635d77c8c1e15e9312950b over 23112 bytes and 238 lines, so §4.9's primary cmp-against-scratchpad proof was available and used rather than the digest fallback. SLICES: 3 over 52 CONTENT lines, TOTAL 238 against DECISION F085 D6's 490 and PROSE 186 against D5's 400. PLAN: `.agent/plan.md` at `f8705c3e` is byte-equal to PLANF021R5 at 42 lines under the 50 cap, with `^## Goal$` and `^## Next Steps$` each 1 and the negative control against DECIDE3 differing at byte 2. THE TWO APPENDS HELD UNDER BOTH READERS, AND THE STRONGEST EVIDENCE IS THAT THE REVIEWER PREDICTED THEIR REMAINDER DIGESTS BEFORE DELEGATING: `.agent/live_review.md` at `c8cfd46d` is the base blob plus one newline plus RECORD4, remainder sha256 c727dc5be62ed3976394b220fbf05b4ddd73776638a866e278a59aa3b193f459 over 4730 bytes, the file going 435610 bytes and 1076 lines to 440340 and 1078, units 219 plus 1 to 220 with every position equal; `.agent/decisions.md` at `03421366` is the base blob plus one newline plus DECIDE3, remainder sha256 5eb1fee3bfbe4c5b88a949985669db9d7cf2940629a5d56f736fa88051dbdca0 over 3644 bytes, the file going 489346 bytes and 6979 lines to 492990 and 6989, units 1220 plus 5 to 1225 with every position equal. Both first-paragraph mutants at byte offset 2 are REJECTED by both readers and both true files ACCEPTED. THE EMITTER RE-DERIVATION REPRODUCED EXACTLY, which is the reading DECISION F021 D3 rests on: 82 call sites, 60 distinct literals, 11 non-constant event arguments and 15 names inside the four defined sets over `packages/`, `apps/` and `scripts/`, against 35, 23, 10 and 1 for the `packages/`-only red control, with a static stream vocabulary of 83 and an empty intersection between the literals and the trace sets. THE SETS HELD line-anchored: 211 entries all DISTINCT at both points, `Done: R-` 0, `Landed: ` 0, `Gate: R` keys 4 to 5 all DISTINCT, `Gate: R5` 0 then 1, maximum registered id R-0648 at both, `- R-0419 —` 1 at both; and `^## DECISION ` went 112 to 113 with `^## DECISION F021 D3 ` 0 to 1. THE RANGE HELD: six commits every one single-parent, the path set EQUAL to the block's six with both differences EMPTY, 0 paths beginning `apps/`, `packages/` or `tests/`, `git ls-files .remedy-wt` 0, markers 0 in all three files a slice landed in, and every reflog row `commit:`. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: the three contract suites at exit 0 and 511 passed, and the canary `tests/cli/test_golden_path.py` at exit 0 and 42 passed. NEW EVIDENCE FOR THE OPEN FINDING R-0449, added here rather than under a new id because §3 checklist item 30 requires the open set to be searched for the DEFECT first: R-0449's standing rule is that before ordering any value INTO an artefact the block names the commit that writes the artefact and the step that produces the value, and that if the producer is not strictly earlier than the writer the block orders the value reported elsewhere. The R5 block broke it. Its G14 required `.agent/handoff.md` — written at C4 — to carry ONE LINE PER GATE, while its G9, G10 and G12 ordered the suites and the range reading AFTER C4, so the numbers those gate lines had to state did not exist when the file was authored. The worker resolved it correctly and declared it, running the suites once on the C3 tree so the handback could state a MEASURED total and once again where the block ordered them, both readings agreeing at 511 and 42. This is the SECOND consecutive instance: the R4 handback declared the same contradiction as a MEASUREMENT-ORDER NOTE, and the R4 verdict did not act on it. NEW EVIDENCE FOR THE OPEN FINDING R-0494, on the same commits and for the same reason: R-0494 records that under self-drive a gate reading routed to the "round report" is written to a channel that dies with the session, and its own text declares the counter-measure APPLIED in the block that registered it — the handback commit's own numbers are ordered nowhere and the reviewer measures them at the next gate. The R5 block ordered C4's `git status --porcelain` reading and C4's insertion count into the round report anyway, which is the THIRD instance and the first one committed by the reviewer who registered the finding. Measured rather than assumed, and this is why the cost is real: those two readings exist nowhere on disk, and the reviewer re-took them at this gate — `git status --porcelain` is 0 lines at `82fcc7c0` and C4's insertion count is 69, both under the 500 cap. WHY R5 IS PASS AND NOT FAIL: neither defect is the worker's, neither put a false sentence on disk, every gate the block did order reproduces under the reviewer's own execution, and the worker declared the one contradiction it hit before the reviewer read the diff — which is the behaviour this workflow exists to produce. THE COUNTER-MEASURE IS PROMOTED, NOT RESTATED: both findings already carried this rule in their bodies and both were broken under it, so the block committing this entry orders the rule into the §3 pre-emission checklist as a numbered item, because a rule that lives only in a finding body is a rule the next block does not read.
<<<END RECORD5

<<<SLICE CHECKFROM
  Why this is on disk and not a habit: item 2 has recurred six times across
  F104 and F105, and R20 hit four of them in one block. A check that lives
  only in reviewer session memory is the A1 trap §0 names, and this list is the
  standing counter-example to it.
<<<END CHECKFROM

<<<SLICE CHECKTO
  31. **A gate whose reading the handback must carry runs at a commit STRICTLY
      EARLIER than the handback commit.** Findings R-0449 and R-0494. When a block
      requires the handback to state a gate's result — "one line per gate" is the
      usual form — every one of those gates is ordered at a commit that precedes
      the commit writing the handback, and the block says which commit that is. A
      gate ordered "after the last commit" cannot be quoted by a file that last
      commit already wrote, so the worker must either run it twice or commit a
      number it has not seen, and only the first is honest. The same clause
      settles where the handback commit's OWN numbers go: nowhere. Under
      self-drive there is no second window, and docs/agents/self_drive_protocol.md
      rules that the handoff is the only return channel, so a value routed to the
      "round report" — item 14's answer for the two-window relay — is written to a
      channel that ends with the session. The reviewer measures those numbers at
      the next gate and records them in that round's ledger entry instead. Item 13
      governs the ORDER a block imposes on the worker's runs and item 14 which
      commits a per-commit gate can honestly reach; neither reaches this one,
      because here the gate's own sequence is sound and its range is right, and
      the defect is that the ARTEFACT quoting it is written first. This is an item
      rather than a habit for the reason the list itself exists: R-0449 and R-0494
      each stated exactly this counter-measure in a finding BODY, R-0494 declared
      it already applied in the block that registered it, and the class then
      recurred in two consecutive rounds — the second of them authored by the
      reviewer who had registered it.

  Why this is on disk and not a habit: item 2 has recurred six times across
  F104 and F105, and R20 hit four of them in one block. A check that lives
  only in reviewer session memory is the A1 trap §0 names, and this list is the
  standing counter-example to it.
<<<END CHECKTO

<<<SLICE HUMANIZE
// The catalog turns a raw stream event into a sentence a human can read.
// Remedy deliberately keeps the catalog DATA in humanizeCatalog.ts: its key set is
// gated against the Python run-log emitters by
// tests/ui_contracts/test_humanize_catalog.py, and a data-only module keeps that
// extractor's job a line scan rather than a parse.
import { STREAM_EVENT_CATALOG } from "./humanizeCatalog";

/** One humanized stream event: the line a feed row renders, and whether the
 *  catalog recognised the kind at all. `known` is what a dev console note counts. */
export interface HumanizedStreamEvent {
  line: string;
  known: boolean;
}

// The honest generic line, and the load-bearing half of this module's contract.
// Eleven run-log writers compute their event name at runtime, so no static
// catalog can ever be complete; an unrecognised kind renders as itself rather
// than vanishing from the story the feed is supposed to tell.
export function humanizeStreamEvent(kind: unknown): HumanizedStreamEvent {
  if (typeof kind !== "string" || kind === "") {
    return { line: "unknown event", known: false };
  }
  // hasOwnProperty, never a bare lookup: a kind named `toString` or `constructor`
  // resolves against Object.prototype and would be reported as known.
  if (!Object.prototype.hasOwnProperty.call(STREAM_EVENT_CATALOG, kind)) {
    return { line: `${kind} event`, known: false };
  }
  return { line: STREAM_EVENT_CATALOG[kind], known: true };
}
<<<END HUMANIZE
