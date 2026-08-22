── STEP RECORD-AND-CLOSE — F021 ──
Goal:        Record the R6 verdict, register the one new finding R6 surfaced,
             add evidence to two open ones, and close this SESSION cleanly at
             its stated round cap with the verdict on disk and a handoff naming
             the next session's first action — which
             docs/agents/self_drive_protocol.md guardrail G7 calls a SUCCESS
             rather than a failure. This round BUILDS NOTHING and touches no
             file under `apps/`, `packages/` or `tests/`.

Fortschritt: ~30 % (T001 fertig und verifiziert · T002 offen · T003 offen; R6
             lieferte Modul, Katalog und den Contract-Test, R7 schreibt das
             Verdikt und schließt die Session — T002 beginnt in R8) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R6 verdict
             with R-0649 and the R-0449 and R-0585 evidence · C3 the session
             handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r7.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/handoff.md` (C3).
             Resolve any count in this block against that list rather than
             against a numeral written elsewhere.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3 and is not negotiable. C1 precedes the
    ledger commit because the plan must be current before it (§3 checklist item
    23). C3 carries only the handback.
    ROUND BASE is `6f5078d77c3fb3e2e60a0aa32c8e0e49d9aef391` and is the commit
    every "round base" in this block names.
 3. THIS ROUND MINTS EXACTLY ONE FINDING ID, R-0649, and resolves nothing. It
    writes no `Done:` line and no `Landed:` line. R-0649 becomes the maximum
    registered id and R-0650 is the next free one. The two other defects R6
    surfaced are added as evidence to the OPEN findings R-0449 and R-0585
    inside RECORD6 rather than under new ids, because §3 checklist item 30
    requires the open set to be searched for the DEFECT first and that search
    returned both holding exactly those shapes. All three defects are the
    REVIEWER'S OWN.
 4. ONE WHOLE-FILE REPLACEMENT AND ONE APPEND. PLANF021R7 replaces
    `.agent/plan.md` at C1 in full. RECORD6 appends to `.agent/live_review.md`
    at C2, based on the ROUND BASE. There is NO FROM/TO pair this round, so no
    containment reading is owed and none is stated. Measured by the reviewer on
    the slice's own bytes before emission: RECORD6 is THREE blank-line units —
    the `Gate: R7` paragraph, the `- R-0649` paragraph and its fix clause — and
    G5's reader (b) depends on that count.
 5. NO PRODUCTION FILE IS EDITED. You may READ anything. Do not create, modify
    or delete a file under `apps/`, `packages/` or `tests/`, and run no
    formatter or linter that rewrites a file in place.
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
    F021 continues on `feature/f021-live-activity-feed`; (c) that R8's work is
    T002 — the feed, its rows and the NowCard over fixture streams with the
    scroll discipline — but that R7 must FIRST rule the two infrastructure
    DECISIONS T002 depends on, the frontend test environment which collects no
    component test today and the single-subscription fan-out; (d) that the
    R6 handback commit `6f5078d7` has never had its own `git status
    --porcelain` reading or insertion count recorded, because §3 checklist item
    31 orders them nowhere, and that the next reviewer takes both at its first
    gate and records them in that round's entry.
 8. Block size, measured on these final bytes AFTER the last edit: TOTAL 223
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 176 against DECISION F085 D5's 400. Marker lines count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C3; the branch is `feature/f021-live-activity-feed`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1 and C2.
     C3's own reading is ordered NOWHERE — §3 checklist item 31, which landed at
     `426ee2a1`, rules that the handback commit's own numbers are measured by
     the reviewer at the next gate and recorded there.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r7.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's own emitted copy still on disk at `.remedy-wt/f021-r7.md` are
     all equal. Write C0b FROM the committed C0a blob. Report the digest with
     the byte and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 8's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF021R7, proved with `cmp` at
     exit 0 against the slice extracted from the committed C0a blob, with a
     NEGATIVE CONTROL against RECORD6 that must exit 1. Report both exit codes,
     plus `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE APPEND at C2, under TWO INDEPENDENT READERS. Obtain the base blob with
     `git show <round base>:<path>` into memory or into scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision,
     which docs/agents/self_drive_protocol.md guardrail G5 forbids outright.
     Reader (a): the round-base blob is a byte-exact PREFIX of the C2 file and
     the remainder is EXACTLY one newline plus RECORD6 — report the remainder's
     sha256, byte count and line count, and the file's byte and line counts
     before and after. Reader (b), the SET-WISE form: split BOTH blobs on the
     blank line into units and confirm the C2 unit LIST equals the base unit
     list followed by RECORD6's own units, compared ELEMENTWISE over the whole
     list and not at the tail; report N at both points and RECORD6's own unit
     count against constraint 4's THREE. NEGATIVE CONTROL: replace one printable
     byte of the FIRST paragraph of the C2 file at equal length and confirm BOTH
     readers REJECT that mutant while BOTH ACCEPT the true file; name the byte
     offset and the substitution. Run the destructive half inside a disposable
     worktree under `.remedy-wt/` whose name no directory already uses, and
     remove and prune it before the handback.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then at C2:
     `- R-` entries and how many are DISTINCT; `Done: R-` lines; `Landed: `
     lines; `Gate: R` keys and how many are DISTINCT; `Gate: R7` occurrences;
     and the MAXIMUM registered id. Report each at BOTH points. Exactly one id
     is minted, so `- R-` reads 211 then 212 with both DISTINCT, the maximum
     reads R-0648 then R-0649, and `Gate: R7` reads 0 then 1. Report
     `- R-0649 —` too, expected 0 then 1, and `- R-0449 —` and `- R-0585 —`,
     each expected 1 at BOTH points because this round adds evidence to them
     and re-registers neither.
 G7  THE CONTRACT SUITES, run at C2 in the PRIMARY checkout and SERIALLY:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py -q -rf`. Report the exit code and
     the passed-plus-skipped total, counting BY PASSED PLUS SKIPPED. The
     reviewer measured exit 0 and 511 at the round base. No docs gate is owed:
     the `Change:` list holds no `docs/` path at all — check that against the
     list before you accept this sentence.
 G8  CANARY, run at C2, serially, and after G7 has finished:
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report the exit
     code and the total.
 G9  THE NEW CONTRACT TEST STILL HOLDS, run at C2, serially, after G8:
     `python3 -m pytest tests/ui_contracts/ -q -rf`. Report the exit code and
     the passed-plus-skipped total; the reviewer measured exit 0 with 426 passed
     and 4 skipped at the round base. This round changes no file it reads, so a
     different reading is a regression from outside this round and is reported
     RED rather than explained.
G10  NO PRODUCTION FILE CHANGED: report that the range from the round base to C2
     holds 0 paths beginning `apps/`, `packages/` or `tests/`, and that
     `git ls-files .remedy-wt` reads 0.
G11  RANGE, executed at C2 and covering the round base to C2 — NOT to C3, because
     C3 writes the file that must quote this gate and §3 checklist item 31
     forbids ordering a reading the quoting artefact cannot yet hold. Report:
     the base-to-C2 path set against the four paths of this block's `Change:`
     list other than `.agent/handoff.md`, with the set difference EMPTY in both
     directions; every commit single-parent; `git show --numstat` and
     `git diff --numstat` agreeing cell by cell with the handback's `## Commits`
     table for C0a, C0b, C1 and C2 (§3 checklist item 28); every insertion count
     under the 500 cap; leading `<<<SLICE ` and `<<<END ` reading 0 LINES in
     `.agent/plan.md` and `.agent/live_review.md`; and this round's reflog rows
     so far classified with `amend`, `rebase` and `cherry` each 0 in the
     operation field.
G12  NO PULL REQUEST: report `gh pr list --state open --json number,headRefName`
     and state that neither `gh pr create` nor `gh pr merge` was run. The
     expected reading is an EMPTY list, which is also the fact constraint 7(b)
     tells the next session to expect.
G13  THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2 and C3, the round base SHA, ONE LINE PER GATE with the transcripts
     kept in the round report rather than in the file (R-0582), the block's
     `Fortschritt:` line verbatim across all three of its lines, and the four
     items constraint 7 requires in its `## Next` section. Its own `wc -l` is
     reported against the 60-line cap a five-commit round allows, with a
     DECISION D15 line declaring any overage and naming the mandated content
     that caused it. Every commit heading in the `## Commits` table carries that
     commit's FULL subject, and where a commit cannot name its own SHA the role
     and the reason are written INSIDE the heading rather than left to a channel
     that ends with this session — that omission is finding R-0494.

Handback:   completion report + rewrite `.agent/handoff.md`.

<<<SLICE PLANF021R7
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
R7 records the R6 verdict, registers R-0649, adds evidence to R-0449 and R-0585,
and closes the reviewer's session at its stated round cap. It builds nothing. The
branch is mid-feature and carries no pull request by design.

## Next Steps
1. R8 rules the two infrastructure DECISIONS T002 depends on: the frontend test
   environment, which collects no component test at all today, and the
   single-subscription fan-out. T002 cannot be written before both.
2. R9 builds T002: the feed, its rows and the NowCard over fixture streams, with
   the scroll discipline that never yanks a reader who has scrolled up.
3. R10 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- T002 cannot be tested until the frontend test environment changes: measured at
  `6f5078d7`, `apps/ui/vitest.config.ts` sets `environment: "node"` and
  `include: ["src/**/*.test.ts"]`, so no `.test.tsx` is collected at all.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- T001 is built and verified but its catalog covers only what a static walk can
  see. The generic line carries the eleven runtime-computed emitters, and R-0649
  records that the walk's roots also reach vendored third-party Python.
- The open set holds no code defect of F021; R-0403, R-0607, R-0608, R-0609,
  R-0611 and R-0613 stay routed to a paydown branch.
<<<END PLANF021R7

<<<SLICE RECORD6
Gate: R7 — the R6 entry. R6 PASSED ON EVERY GATE, RE-MEASURED INDEPENDENTLY RATHER THAN READ BACK, AND IT IS THE FIRST ROUND OF F021 TO SHIP PRODUCTION CODE. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f021-r6.md` at `1fe225c0`, `.agent/last_block.md` at `757094ce` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f021-r6.md`, are all sha256 08dbd76e98e0ace307889876d49ff897cf5b2e2531daf2a72f17a45156bbbd77 over 28636 bytes and 357 lines, so §4.9's primary cmp-against-scratchpad proof was available and used rather than the digest fallback. SLICES: 5 over 106 CONTENT lines, TOTAL 357 against DECISION F085 D6's 490 and PROSE 251 against D5's 400. THE TWO WHOLE-FILE SLICES ARE BYTE-EQUAL to what landed: `.agent/plan.md` at `7c3eb24d` equals PLANF021R6 at 44 lines under the 50 cap, and `apps/ui/src/api/humanize.ts` at `e9568263` equals HUMANIZE, each with the other slice as a negative control at exit 1. THE APPEND at `5d4e3bef` is the base blob plus one newline plus RECORD5, remainder sha256 3567c4a03d02248b04258ba786445ab4295860bfc7e6996ac233a61c89b9061c over 5706 bytes, the file going 440340 bytes and 1078 lines to 446046 and 1080, units 220 plus 1 to 221 with every position equal, and the first-paragraph mutant REJECTED by both readers. THE PAIR at `426ee2a1` held under the §4.9 APPEND obligation: CHECKFROM reads 1 at the round base and 1 at C3 because the TO contains it, all 24 TO-ONLY lines occur exactly 1x among the lines that commit's diff adds, `^  31\. \*\*` goes 0 to 1 while `^  32\. \*\*` stays 0, and the reviewer confirmed the strongest form of all — applying CHECKFROM to CHECKTO over the base blob reproduces the committed file BYTE FOR BYTE. THE CATALOG IS THE POINT OF THE ROUND AND IT MEASURES CLEAN at `9c782704`: one exported symbol, 83 keys all DISTINCT and ASCII-sorted, 83 values all DISTINCT, 0 empty, 0 not ending in a full stop, and 0 equal to the `<key> event` generic form that would have been a stub wearing a catalog entry's clothes. THE EQUALITY IS THE REVIEWER'S OWN: an independent AST derivation over `packages/`, `apps/` and `scripts/` returns 82 call sites, 60 distinct literals, 11 runtime-computed names and a static stream vocabulary of 83, and that set EQUALS the catalog's key set with both differences EMPTY. THE DRIFT PROTECTION DISCRIMINATES IN BOTH DIRECTIONS, which is more than the block ordered: deleting the `staging_promoted` entry in a disposable worktree fails `test_catalog_keys_equal_the_static_stream_vocabulary` naming that key, and the REVERSE control the reviewer added — inserting a `zz_phantom_kind` entry no emitter produces — fails naming that key too, so the assertion is vacuous in neither direction. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: `npx tsc --noEmit` exit 0, `npx vitest run` exit 0 with 11 files and 160 tests against 10 and 152 at the round base, `tests/ui_contracts/` exit 0 with 426 passed and 4 skipped against 417 and 4, the three contract suites exit 0 with 511 passed, and the canary exit 0 with 42 passed. THE RANGE HELD: ten commits every one single-parent, the path set EQUAL to the block's ten with both differences EMPTY, markers 0 in every file a slice landed in, `git ls-files .remedy-wt` 0, and all ten reflog rows `commit:`. WHY R6 IS PASS: every gate reproduces under the reviewer's own execution, the code is honest — the generic line really is reached, the prototype-key case really is handled, and the contract test really can fail — and the worker declared all three deviations it hit before the reviewer read the diff. TWO OF THOSE THREE ARE THE REVIEWER'S OWN BLOCK DEFECTS, and both are recorded against OPEN findings rather than under new ids, because §3 checklist item 30 requires the open set to be searched for the DEFECT first. EVIDENCE FOR R-0449: the R6 block's G15 ordered the RANGE reading "at C8" while its G17 required the handback — written BY C8 — to carry one line per gate, so the reading could not exist when the quoting file was authored. That is the same shape as the R5 instance and the R4 one before it, and it occurred in the very block that promoted the counter-measure into §3 as item 31: the item was applied to G10 through G14 and missed the range gate, which is precisely the gate whose natural phrasing is "at the last commit". The worker resolved it correctly, measuring the range over the base to C7 plus the one path C8 writes, then re-running in full afterwards with both readings agreeing. From here the rule's application names RANGE gates explicitly, and this block's own G11 runs the range at C2 and says so. EVIDENCE FOR R-0585: the same block's G17 called the round "a nine-commit bundle" while its `Bundle` and `Change` lists name ten commits and ten paths, and G17 itself asks for ten item-status rows — a done-when gate counting a list that lives in another section of the same block, which is R-0585's exact shape and which item 16's check does not reach. Nothing false landed on disk: the worker measured against the 100-line allowance the sentence names, wrote all ten rows, and declared the contradiction.

- R-0649 — Low, A DERIVATION THAT DEFINES A PRODUCTION CONSTANT WALKS VENDORED THIRD-PARTY PYTHON, SO A DEPENDENCY CAN INJECT AN EVENT KIND REMEDY NEVER EMITS. The defect is the reviewer's, in the F021 R6 block's G5, and it landed in `tests/ui_contracts/test_humanize_catalog.py` at `2750a726` as `EMITTER_ROOTS = ("packages", "apps", "scripts")` walked with `rglob("*.py")`. `apps/ui/node_modules` sits under one of those roots and is gitignored build output rather than Remedy source. Measured by the reviewer at `6f5078d7`: the walk visits 374 Python files of which exactly 1 is vendored — `apps/ui/node_modules/flatted/python/flatted.py` — it contributes 0 emission call sites, and the derived vocabulary is 83 with it and 83 without it, both sets identical, so nothing is wrong on disk today and the test is stable whether or not `npm ci` has run. That is why this is Low. The exposure is structural: the set that defines which event kinds `apps/ui/src/api/humanizeCatalog.ts` MUST contain is not a property of Remedy alone, so a future dependency shipping a `.py` with a `<writer>.log("some_name")` call would turn the contract test red for a reason no Remedy commit caused, and the repair a reader reaches for first — adding a catalog entry — would put a line in the catalog for a kind this system never emits. The worker found this while implementing the ordered predicate, refused to widen the block's scope on its own initiative, and said so; that refusal was correct and is why the finding exists at review time rather than in six months.

  FIX: exclude gitignored build output from the walk by skipping any path with `node_modules` among its parts, in `emission_literals()` and in any later derivation that reuses these roots, and add a test that the exclusion really removes a file the walk would otherwise visit — a red control, since an exclusion nothing exercises is indistinguishable from one that never matches. Do it in the round that next touches that file. R-0518 is the nearest OPEN neighbour and does not reach this: it records a gated test that REQUIRES `apps/ui/node_modules` and therefore goes red in a fresh worktree, while this test needs none of it — the reviewer ran it in a disposable worktree with no `node_modules` and all 9 tests passed. One finding is about the directory being absent, this one about its contents being present.
<<<END RECORD6
