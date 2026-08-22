── STEP RECORD-AND-CLOSE — F021 ──
Goal:        Record the R9 verdict, add R9's one surfaced defect as evidence to
             the OPEN finding R-0437, and close this SESSION cleanly at its
             stated round cap with the verdict on disk and a handoff naming the
             next session's first action — which
             docs/agents/self_drive_protocol.md guardrail G7 calls a SUCCESS
             rather than a failure. This round BUILDS NOTHING and touches no
             file under `apps/`, `packages/` or `tests/`.

Fortschritt: ~40 % (T001 fertig · T002 begonnen — die Projektion Frame→Zeile
             ist gebaut und verifiziert, Ring und Komponenten folgen; R10
             schreibt das Verdikt und schliesst die Session) — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R9 verdict
             with the R-0437 evidence · C3 the session handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r10.md` (NEW, C0a) · `.agent/last_block.md`
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
    ROUND BASE is `7823005d7fd11ed5f98082cd867c97d22f820505` and is the commit
    every "round base" in this block names.
 3. THIS ROUND MINTS NO FINDING ID and resolves nothing. It writes no `Done:`
    line and no `Landed:` line. R-0649 stays the maximum registered id and
    R-0650 stays the next free one. The one defect R9 surfaced — the reviewer's
    own G6 reader (b), which ordered a unit-list equality without stating the
    trailing-newline convention that equality depends on — is added as evidence
    to the OPEN finding R-0437 inside RECORD9 rather than under a new id,
    because §3 checklist item 30 requires the open set to be searched for the
    DEFECT first and that search returned R-0437 holding exactly this cause.
    That defect is the REVIEWER'S OWN.
 4. ONE WHOLE-FILE REPLACEMENT AND ONE APPEND. PLANF021R10 replaces
    `.agent/plan.md` at C1 in full. RECORD9 appends to `.agent/live_review.md`
    at C2, based on the ROUND BASE. There is NO FROM/TO pair this round, so no
    containment reading is owed and none is stated. Measured by the reviewer on
    the slice's own bytes before emission: RECORD9 is ONE blank-line unit under
    the convention constraint 5 states, and G5's reader (b) depends on it.
 5. THE TRAILING-NEWLINE CONVENTION, stated here because R9 proved that a
    unit-list equality is undefined without it and because finding R-0437 rules
    that a measurement whose result depends on this convention must declare it.
    Every slice in this block is quoted WITHOUT a trailing newline; the append
    writes one newline BEFORE the slice and one newline AFTER it, so the file
    keeps exactly one terminator. For reader (b) the convention is: a single
    trailing terminator newline TERMINATES the last line and does NOT open a new
    unit, so BOTH blobs have that one terminator stripped BEFORE they are split
    on the blank line. Splitting without stripping rejects the TRUE file at the
    final base unit and is the reading R9 had to declare; do not report it as a
    failure, report both forms if you like, but the convention above is the one
    the gate is measured under.
 6. NO PRODUCTION FILE IS EDITED. You may READ anything. Do not create, modify
    or delete a file under `apps/`, `packages/` or `tests/`, and run no
    formatter or linter that rewrites a file in place.
 7. Do NOT create a pull request and do NOT merge one. The branch stays open and
    unmerged: F021 is mid-feature, so there is nothing to open a pull request
    for and nothing to merge. Push the branch.
 8. THE HANDBACK IS ALSO THE SESSION HANDOFF. Beyond the mandated sections it
    states, in its `## Next` section and in this order, the four things the next
    session needs and cannot recompute cheaply: (a) that the next session's
    FIRST action is docs/agents/self_drive_protocol.md Phase 1 rule 1, the
    `.agent/STOP` check, BEFORE rule 2's Open PR Gate — required by that
    protocol's Phase 2 and by finding R-0347; (b) that the Open PR Gate will
    find NO open pull request, so rule 5 applies and F021 continues on
    `feature/f021-live-activity-feed`; (c) that the next build is the bounded
    ring DECISION F021 D5 rules — `recent` on `BrainStreamState` and on
    `BrainStreamView` — that its append belongs inside `receiveBrainFrame` in
    `apps/ui/src/api/brainStream.ts` rather than in the runner's `dispatch`
    because that function already drops a frame whose `seq` is not ahead of
    `lastSeq`, and that `feedRowOf` in `apps/ui/src/api/feedRow.ts` is the
    projection it feeds and is deliberately uncalled until then; (d) that the C3
    handback commit of this round has never had its own `git status
    --porcelain` reading or insertion count recorded, because §3 checklist item
    31 orders them nowhere, and that the next reviewer takes both at its first
    gate and records them in that round's entry.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 244
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 195 against DECISION F085 D5's 400. Marker lines count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C3; the branch is `feature/f021-live-activity-feed`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1 and C2.
     C3's own reading is ordered NOWHERE — §3 checklist item 31 rules that the
     handback commit's own numbers are measured by the reviewer at the next gate
     and recorded there.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r10.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's own emitted copy still on disk at `.remedy-wt/f021-r10.md` are
     all equal. Write C0b FROM the committed C0a blob. Report the digest with
     the byte and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 9's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF021R10, proved with `cmp` at
     exit 0 against the slice extracted from the committed C0a blob, with a
     NEGATIVE CONTROL against RECORD9 that must exit 1. Report both exit codes,
     plus `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE APPEND at C2, under TWO INDEPENDENT READERS, both measured under the
     trailing-newline convention constraint 5 states. Obtain the base blob with
     `git show <round base>:<path>` into memory or into scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision,
     which docs/agents/self_drive_protocol.md guardrail G5 forbids outright.
     Reader (a): the round-base blob is a byte-exact PREFIX of the C2 file and
     the remainder is EXACTLY one newline plus RECORD9 plus one newline — report
     the remainder's sha256, byte count and line count, and the file's byte and
     line counts before and after. Reader (b), the SET-WISE form: strip the one
     trailing terminator newline from BOTH blobs, split each on the blank line
     into units, and confirm the C2 unit LIST equals the base unit list followed
     by RECORD9's own units, compared ELEMENTWISE over the whole list and not at
     the tail; report N at both points and RECORD9's own unit count against
     constraint 4's ONE. NEGATIVE CONTROL: replace one printable byte of the
     FIRST paragraph of the C2 file at equal length and confirm BOTH readers
     REJECT that mutant while BOTH ACCEPT the true file; name the byte offset
     and the substitution. Run the destructive half inside a disposable worktree
     under `.remedy-wt/` whose name no directory already uses, and remove and
     prune it before the handback.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then at C2:
     `- R-` entries and how many are DISTINCT; `Done: R-` lines; `Landed: `
     lines; `Gate: R` keys and how many are DISTINCT; `Gate: R10` occurrences;
     and the MAXIMUM registered id. Report each at BOTH points. NO id is minted,
     so `- R-` reads 212 at BOTH points with both DISTINCT, the maximum reads
     R-0649 at BOTH points, `Gate: R` keys read 9 then 10 with both DISTINCT,
     and `Gate: R10` reads 0 then 1. Report `- R-0437 —` too, expected 1 at BOTH
     points because this round adds evidence to it and does not re-register it.
 G7  THE CONTRACT SUITES, run at C2 in the PRIMARY checkout, SERIALLY, and from
     the REPOSITORY ROOT — a shell left inside `apps/ui` by an earlier command
     makes this exit 4 with no test run, which is a vacuous reading rather than
     a green one, and the reviewer hit exactly that this session:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py -q -rf`. Report the exit code, the
     working directory it ran in, and the passed-plus-skipped total, counting BY
     PASSED PLUS SKIPPED. The reviewer measured exit 0 and 511 at the round base.
     No docs gate is owed: the `Change:` list holds no `docs/` path at all —
     check that against the list before you accept this sentence.
 G8  CANARY, run at C2, serially, after G7 has finished, from the repository
     root: `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report the
     exit code and the total. The reviewer measured exit 0 and 42 at the base.
 G9  THE T001 AND T002 CONTRACT TESTS STILL HOLD, run at C2, serially, after G8,
     from the repository root: `python3 -m pytest tests/ui_contracts/ -q -rf`.
     Report the exit code and the passed-plus-skipped total; the reviewer
     measured exit 0 with 426 passed and 4 skipped at the round base. This round
     changes no file it reads, so a different reading is a regression from
     outside this round and is reported RED rather than explained.
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
     table for C0a, C0b, C1 and C2 (§3 checklist item 28) — and where `git
     commit`'s own summary line disagrees with those two under rewrite
     detection, the numstat readings are the ones the table carries and the
     divergence is reported rather than reconciled; every insertion count under
     the 500 cap; leading `<<<SLICE ` and `<<<END ` reading 0 LINES in
     `.agent/plan.md` and `.agent/live_review.md`; and this round's reflog rows
     so far classified with `amend`, `rebase` and `cherry` each 0 in the
     operation field.
G12  NO PULL REQUEST: report `gh pr list --state open --json number,headRefName`
     and state that neither `gh pr create` nor `gh pr merge` was run. The
     expected reading is an EMPTY list, which is also the fact constraint 8(b)
     tells the next session to expect.
G13  THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2 and C3, the round base SHA, ONE LINE PER GATE with the transcripts
     kept out of the file (R-0582), the block's `Fortschritt:` line verbatim
     across all three of its lines, and the four items constraint 8 requires in
     its `## Next` section. Its own `wc -l` is reported against the 60-line cap,
     with a DECISION D15 line declaring any overage and naming the mandated
     content that caused it. Every commit heading in the `## Commits` table
     carries that commit's FULL subject, and where a commit cannot name its own
     SHA the role and the reason are written INSIDE the heading rather than left
     to a channel that ends with this session — that omission is finding R-0494.

Handback:   completion report + rewrite `.agent/handoff.md`.

<<<SLICE PLANF021R10
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
R10 records the R9 verdict, adds R9's one surfaced defect as evidence to R-0437,
and closes the reviewer's session at its stated round cap of three delegated
rounds. It builds nothing and mints no finding id. The branch is mid-feature and
carries no pull request by design.

## Next Steps
1. R11 builds the bounded ring DECISION F021 D5 rules: `recent` on
   `BrainStreamState` and on `BrainStreamView`, appended inside
   `receiveBrainFrame` rather than in the runner's `dispatch`, so a reconnect
   replay cannot duplicate a row. `feedRowOf` is the projection it feeds.
2. R12 builds the feed and NowCard components over fixture streams, with the
   scroll discipline that never yanks a reader who has scrolled up, gated by a
   Python source contract under `tests/ui_contracts/`.
3. R13 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- The ring is the one place a reconnect can duplicate rows. `receiveBrainFrame`
  already drops a frame whose seq is not ahead of `lastSeq`; an append written
  anywhere else silently bypasses that guard.
- The view-identity contract `createBrainStreamRunner` documents is what the
  ring round is most likely to break: `useSyncExternalStore` compares with
  `Object.is`, so a freshly built array on every call re-renders forever.
- `npx vitest run` is DENIED to the reviewer's session class, so a frontend
  round's colour rests on the worker's transcript plus a red control the
  reviewer can verify from the authored bytes. Order the red control every time.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- The open set holds no code defect of F021; R-0403, R-0607, R-0608, R-0609,
  R-0611 and R-0613 stay routed to a paydown branch.
<<<END PLANF021R10

<<<SLICE RECORD9
Gate: R10 — the R9 entry. R9 PASSED ON EVERY GATE, RE-MEASURED INDEPENDENTLY RATHER THAN READ BACK, AND IT IS THE FIRST ROUND OF T002 TO SHIP PRODUCTION CODE. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f021-r9.md` at `02749b50`, `.agent/last_block.md` at `66a18dca`, the working copy of `.agent/last_block.md`, and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f021-r9.md`, are all sha256 bcff6f7bf4e1ab3802ae77933dc7fb920ec0716baa0b2b6ec6cc2437a32caa91 over 26224 bytes and 389 lines, so §4.9's primary cmp-against-scratchpad proof was available and used rather than the digest fallback. SLICES: 4 over 168 CONTENT lines, TOTAL 389 against DECISION F085 D6's 490 and PROSE 221 against D5's 400, both equal to that block's constraint 9. THE WHOLE-FILE SLICE IS BYTE-EQUAL to what landed: `.agent/plan.md` at `347a68db` equals PLANF021R9 over 48 lines against the 50 cap, with RECORD8 as a negative control that differs. THE TWO NEW FILES ARE BYTE-EQUAL TO THEIR SLICES AND ABSENT AT THE BASE: `git ls-tree` at `f5f01585` returns nothing for either path, and `apps/ui/src/api/feedRow.ts` at `40965b8d` equals FEEDROW over 52 lines while `apps/ui/src/api/feedRow.test.ts` equals FEEDROWTEST over 67 lines, each with the other slice as a negative control. THE APPEND at `4df4a3bd` is the round-base blob plus exactly one newline plus RECORD8, remainder sha256 1f79c8b91ddd720d0d7cad8e22296cf14521be10e4a632921b7e6d5aa018d8b6 over 4011 bytes, the file going 457650 bytes and 1088 lines to 461661 and 1090, units 225 plus RECORD8's own 1 to 226 with every base position equal elementwise. THE LEDGER SETS ARE UNMOVED, as a round minting nothing requires: 212 `- R-` entries all DISTINCT at both points, maximum id R-0649 at both, `Done: R-` 0 and `Landed: ` 0 at both, and `Gate: R` keys 8 to 9 with `Gate: R9` going 0 to 1. THE TYPECHECK IS THE REVIEWER'S OWN: `npx tsc --noEmit` from `apps/ui` in the primary checkout exits 0 over the landed bytes, and the reviewer had already run the same command to exit 0 over those exact authored bytes BEFORE emission, in a disposable worktree at the round base with `apps/ui/node_modules` symlinked rather than copied. THE FRONTEND SUITE IS NOT THE REVIEWER'S OWN and this entry says so rather than implying otherwise: `npx vitest run` is DENIED to the reviewer's session class, so G9's exit 0 with 12 files and 168 tests against the base's 11 and 160 rests on the worker's transcript. WHAT MAKES THAT GREEN TRUSTWORTHY IS G10, THE RED CONTROL, AND THE REVIEWER VERIFIED ITS AUTHENTICITY FROM THE AUTHORED BYTES: the worker mutated the unique line `    seq: frame.seq,` — line 45 of `feedRow.ts`, occurring exactly once whole-line and once indent-agnostic, both readings agreeing — to `    seq: 0,` and reported exit 1 with 2 failures of 168, naming `carries the frame's own seq rather than any envelope field` and `an uncatalogued kind still yields a row, on the generic line`. The reviewer parsed the committed test file and finds that EXACTLY TWO of its eight `it(` blocks assert on `row.seq`, and they are exactly those two — a detail no summary could invent and one the block never predicted, since the reviewer had named only the first. Restoring the line returned the suite to 168 passed, so the control discriminates in both directions. THE PYTHON SUITES ARE THE REVIEWER'S OWN, run serially from the repository root at `7823005d`: the three contract suites exit 0 with 511 passed, the canary exit 0 with 42 passed, and `tests/ui_contracts/` exit 0 with 426 passed and 4 skipped — all equal to the round-base readings. THE RANGE HELD: six commits every one single-parent, the base-to-C3 path set EQUAL to that block's six non-handoff `Change:` paths with both differences EMPTY, the only two paths under `apps/` both status `A` so no existing production file was touched, insertions 389, 273, 21, 119 and 2 every one under the 500 cap with C2's 119 equal to 52 plus 67, markers 0 in every file a slice landed in, `git ls-files .remedy-wt` 0, `git worktree list` ending with the primary checkout alone, and all six reflog rows `commit:` — amend 0, rebase 0, cherry 0. THE READING §3 CHECKLIST ITEM 31 LEAVES TO THIS GATE: the R9 handback commit `7823005d` is single-parent and changes `.agent/handoff.md` alone at 69 insertions and 57 deletions, under the 500-insertion cap, and `git status --porcelain` reads 0 lines at that commit. WHY R9 IS PASS: every gate the reviewer could execute reproduces, the one it could not is anchored by a red control it verified from the code, and the module does what its tests say — a frame's own seq wins over the envelope's, an uncatalogued kind still yields a row, and a non-object envelope yields a row rather than throwing. EVIDENCE FOR R-0437: the R9 block's G6 reader (b) ordered the C3 unit LIST to equal the base unit list followed by the slice's own units, compared elementwise, and never stated whether the trailing terminator newline opens a unit. It does not, but a reader that splits on the blank line WITHOUT stripping it first rejects the TRUE file at the final base unit, because the base blob's last unit carries the terminator and the appended file's corresponding unit does not. The worker measured both forms, got 225, 226 and 1 either way, stated the convention it had to invent, and declared the gap rather than silently normalising — which is the correct handling and still costs the round a declared deviation. R-0437's standing rule binds PAIR slices to state their newline convention; this is the same cause reaching a THIRD measurement, after the slice COUNTS of F082 R5 and R6 and the pair SHAPES of R18, and R-0437's own body already warns that "a rule recorded for one measurement does not cover the other measurement it also governs". The fix clause therefore widens from pair slices to ANY authored measurement whose result depends on the convention — unit-list equality above all — and the block that records this applies it in its own G5 rather than only describing it. Promoting the widened clause into the §3 pre-emission checklist needs a round with `docs/` in its change set and is NOT claimed to have happened here.
<<<END RECORD9
