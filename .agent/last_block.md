── STEP REGISTER-AND-CLOSE — F021 ──
Goal:        Record the R10 verdict, register the one defect R10 LANDED ON DISK
             — `.agent/plan.md` lost its terminating newline because the
             reviewer's own newline convention swept a slice class it was not
             written for — restore that newline in the same round, and close
             this SESSION. This round ships no feature code and touches no file
             under `apps/`, `packages/` or `tests/`.

Fortschritt: ~40 % (T001 fertig · T002 begonnen — die Projektion Frame→Zeile
             ist gebaut und verifiziert, Ring und Komponenten folgen; R11
             registriert einen Reviewer-Defekt und schliesst die Session)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan, with its terminating
             newline restored · C2 the R10 verdict and the new finding R-0650 ·
             C3 the session handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r11.md` (NEW, C0a) · `.agent/last_block.md`
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
    23), and because the R-0650 paragraph C2 writes states that the newline was
    restored — a claim about THIS round's own change, which §3 checklist item 20
    as narrowed by R-0524 permits only by naming the ordering constraint that
    fixes it. This clause is that constraint. C3 carries only the handback.
    ROUND BASE is `4f504337efac50667a346c3964b7b047728bcf1d` and is the commit
    every "round base" in this block names.
 3. THIS ROUND MINTS EXACTLY ONE FINDING ID, R-0650, and resolves nothing. It
    writes no `Done:` line and no `Landed:` line — this ledger carries 212 open
    findings and zero of either, and this round does not start a new convention
    while closing a session. R-0650 becomes the maximum registered id and R-0651
    the next free one.
 4. THE CORRECTED NEWLINE CONVENTION, which is the substance of R-0650 and is
    applied here rather than only described. Every slice below is quoted WITHOUT
    a trailing newline. How that slice is written depends on its KIND, and the
    R10 block's error was stating the convention once for all kinds:
      - a WHOLE-FILE replacement is written as the slice PLUS one terminating
        newline, because a text file in this repository ends with one and
        `.agent/plan.md` is the only `.agent/` state file that currently does
        not;
      - an APPEND is written as one newline, then the slice, then one
        terminating newline, so the file keeps exactly one terminator.
    G4 and G5 below are worded to match, and they disagree deliberately: G4
    compares against the slice PLUS a newline, G5's remainder is a newline plus
    the slice plus a newline.
 5. ONE WHOLE-FILE REPLACEMENT AND ONE APPEND. PLANF021R11 replaces
    `.agent/plan.md` at C1 in full. RECORD10 appends to `.agent/live_review.md`
    at C2, based on the ROUND BASE. There is NO FROM/TO pair this round, so no
    containment reading is owed and none is stated. Measured by the reviewer on
    the slice's own bytes before emission: RECORD10 is THREE blank-line units
    under the convention constraint 4 states — the `Gate: R11` paragraph, the
    `- R-0650` paragraph and its `FIX:` clause — and G5's reader (b) depends on
    that count.
 6. NO PRODUCTION FILE IS EDITED. You may READ anything. Do not create, modify
    or delete a file under `apps/`, `packages/` or `tests/`, and run no
    formatter or linter that rewrites a file in place.
 7. Do NOT create a pull request and do NOT merge one. The branch stays open and
    unmerged: F021 is mid-feature. Push the branch.
 8. THE HANDBACK IS ALSO THE SESSION HANDOFF, and this session ENDS with it, so
    it is the only thing the next session reads. Beyond the mandated sections it
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
    31 orders them nowhere, and that BOTH it and the R10 handback commit
    `4f504337` are owed those readings at the next reviewer's first gate.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 250
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 197 against DECISION F085 D5's 400. Marker lines count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C3; the branch is `feature/f021-live-activity-feed`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1 and C2.
     C3's own reading is ordered NOWHERE — §3 checklist item 31 rules that the
     handback commit's own numbers are measured at the next gate.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r11.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's own emitted copy still on disk at `.remedy-wt/f021-r11.md` are
     all equal. Write C0b FROM the committed C0a blob. Report the digest with
     the byte and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 9's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R11 PLUS ONE TERMINATING NEWLINE —
     constraint 4, and the difference from the R10 block that this round exists
     to correct. Prove it with `cmp` at exit 0 against that byte string, built
     from the slice extracted from the committed C0a blob, with a NEGATIVE
     CONTROL against the bare slice WITHOUT the newline that must exit 1.
     Report both exit codes, and report explicitly that the file's last byte is
     a newline and that `git diff` prints no `\ No newline at end of file` for
     it. Report `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE APPEND at C2, under TWO INDEPENDENT READERS, both measured under the
     convention constraint 4 states. Obtain the base blob with
     `git show <round base>:<path>` into memory or into scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision,
     which docs/agents/self_drive_protocol.md guardrail G5 forbids outright.
     Reader (a): the round-base blob is a byte-exact PREFIX of the C2 file and
     the remainder is EXACTLY one newline plus RECORD10 plus one newline —
     report the remainder's sha256, byte count and line count, and the file's
     byte and line counts before and after. Reader (b), the SET-WISE form: strip
     the one trailing terminator newline from BOTH blobs, split each on the
     blank line into units, and confirm the C2 unit LIST equals the base unit
     list followed by RECORD10's own units, compared ELEMENTWISE over the whole
     list and not at the tail; report N at both points and RECORD10's own unit
     count against constraint 5's THREE. NEGATIVE CONTROL: replace one printable
     byte of the FIRST paragraph of the C2 file at equal length and confirm BOTH
     readers REJECT that mutant while BOTH ACCEPT the true file; name the byte
     offset and the substitution. Run the destructive half inside a disposable
     worktree under `.remedy-wt/` whose name no directory already uses, and
     remove and prune it before the handback.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then at C2:
     `- R-` entries and how many are DISTINCT; `Done: R-` lines; `Landed: `
     lines; `Gate: R` keys and how many are DISTINCT; `Gate: R11` occurrences;
     and the MAXIMUM registered id. Report each at BOTH points. Exactly one id
     is minted, so `- R-` reads 212 then 213 with both DISTINCT, the maximum
     reads R-0649 then R-0650, `Gate: R` keys read 10 then 11 with both
     DISTINCT, `Gate: R11` reads 0 then 1, and `- R-0650 —` reads 0 then 1.
     `Done: R-` and `Landed: ` read 0 at BOTH points.
 G7  THE CONTRACT SUITES, run at C2 in the PRIMARY checkout, SERIALLY, and from
     the REPOSITORY ROOT — a shell left inside `apps/ui` makes this exit 4
     having run no test, which is a vacuous reading and not a green one:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py -q -rf`. Report the exit code, the
     working directory, and the passed-plus-skipped total, counting BY PASSED
     PLUS SKIPPED. The reviewer measured exit 0 and 511 at the round base. These
     suites read `.agent/plan.md`, so they are also the guard on C1's newline
     change. No docs gate is owed: the `Change:` list holds no `docs/` path —
     check that against the list before you accept this sentence.
 G8  CANARY, run at C2, serially, after G7, from the repository root:
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report the exit
     code and the total. The reviewer measured exit 0 and 42 at the round base.
 G9  THE T001 AND T002 CONTRACT TESTS STILL HOLD, run at C2, serially, after G8,
     from the repository root: `python3 -m pytest tests/ui_contracts/ -q -rf`.
     Report the exit code and the passed-plus-skipped total; the reviewer
     measured exit 0 with 426 passed and 4 skipped at the round base.
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
     table for C0a, C0b, C1 and C2 (§3 checklist item 28), with any disagreement
     from `git commit`'s own rewrite-detected summary reported rather than
     reconciled; every insertion count under the 500 cap; leading `<<<SLICE `
     and `<<<END ` reading 0 LINES in `.agent/plan.md` and
     `.agent/live_review.md`; and this round's reflog rows so far classified
     with `amend`, `rebase` and `cherry` each 0 in the operation field.
G12  NO PULL REQUEST: report `gh pr list --state open --json number,headRefName`
     and state that neither `gh pr create` nor `gh pr merge` was run. The
     expected reading is an EMPTY list, which is also the fact constraint 8(b)
     tells the next session to expect.
G13  THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2 and C3, the round base SHA, ONE LINE PER GATE with the transcripts
     kept out of the file (R-0582), the block's `Fortschritt:` line verbatim
     across all four of its lines, and the four items constraint 8 requires in
     its `## Next` section. Its own `wc -l` is reported against the 60-line cap,
     with a DECISION D15 line declaring any overage and naming the mandated
     content that caused it. Every commit heading in the `## Commits` table
     carries that commit's FULL subject, and where a commit cannot name its own
     SHA the role and the reason are written INSIDE the heading rather than left
     to a channel that ends with this session — that omission is finding R-0494.

Handback:   completion report + rewrite `.agent/handoff.md`.

<<<SLICE PLANF021R11
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
R11 records the R10 verdict, registers R-0650 — the reviewer's own newline
convention, stated for all slice kinds at R10, stripped the terminator from this
file — restores that terminator, and closes the session. It ships no feature
code.

## Next Steps
1. R12 builds the bounded ring DECISION F021 D5 rules: `recent` on
   `BrainStreamState` and on `BrainStreamView`, appended inside
   `receiveBrainFrame` rather than in the runner's `dispatch`, so a reconnect
   replay cannot duplicate a row. `feedRowOf` is the projection it feeds.
2. R13 builds the feed and NowCard components over fixture streams, with the
   scroll discipline that never yanks a reader who has scrolled up, gated by a
   Python source contract under `tests/ui_contracts/`.
3. R14 onward T003: graph-focus wiring, the disabled steering input, and the
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
- A block's newline convention is stated PER SLICE KIND, never once for all of
  them: R-0650 is that rule arriving the expensive way.
- The open set holds no code defect of F021; R-0403, R-0607, R-0608, R-0609,
  R-0611 and R-0613 stay routed to a paydown branch.
<<<END PLANF021R11

<<<SLICE RECORD10
Gate: R11 — the R10 entry. R10 PASSED ON EVERY GATE, RE-MEASURED INDEPENDENTLY RATHER THAN READ BACK, AND IT LANDED ONE DEFECT ON DISK WHICH IS REGISTERED BELOW AS R-0650. R10 was a record-and-close round that built nothing. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f021-r10.md` at `e6f8d721`, `.agent/last_block.md` at `626382b8`, the working copy of `.agent/last_block.md`, and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f021-r10.md`, are all sha256 ec4443a926c18e1c8c98f4b608d8b25b168cb0a8a698a2ab47b1b51b0a8febda over 22336 bytes and 244 lines, so §4.9's primary cmp-against-scratchpad proof was available and used rather than the digest fallback. SLICES: 2 over 49 CONTENT lines, TOTAL 244 against DECISION F085 D6's 490 and PROSE 195 against D5's 400, both equal to that block's constraint 9. THE APPEND at `b1bf9350` is the round-base blob plus exactly one newline plus RECORD9, remainder sha256 f5029795657bee4bfb086399c6547a3a02a67199a0a7473476796932433f7528 over 6186 bytes, the file going 461661 bytes to 467847, units 226 plus RECORD9's own 1 to 227 with every base position equal elementwise under the stripped convention. THE REVIEWER REPRODUCED THE WORKER'S DECLARED UNSTRIPPED READING TOO: splitting both blobs on the blank line WITHOUT first removing the single terminator rejects the TRUE file at element index 225, exactly as that block's constraint 5 predicted, which is what makes the stated convention a fix rather than a preference. THE LEDGER SETS ARE UNMOVED, as a round minting nothing requires: 212 `- R-` entries all DISTINCT at both points, maximum id R-0649 at both, `Done: R-` 0 and `Landed: ` 0 at both, `- R-0437 —` 1 at both, and `Gate: R` keys 9 to 10 with `Gate: R10` going 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially from the repository root at `4f504337`: the three contract suites exit 0 with 511 passed, the canary exit 0 with 42 passed, and `tests/ui_contracts/` exit 0 with 426 passed and 4 skipped — all equal to the round-base readings. THE RANGE HELD: five commits every one single-parent, the base-to-C2 path set EQUAL to that block's four non-handoff `Change:` paths with both differences EMPTY, 0 paths beginning `apps/`, `packages/` or `tests/`, insertions 244, 158, 15 and 2 every one under the 500 cap, markers 0 in every file a slice landed in, `git ls-files .remedy-wt` 0, `git worktree list` ending with the primary checkout alone, and all five reflog rows `commit:` — amend 0, rebase 0, cherry 0. THE READING §3 CHECKLIST ITEM 31 LEAVES TO THIS GATE: the R9 handback commit `7823005d` is single-parent and changes `.agent/handoff.md` alone at 69 insertions and 57 deletions, under the 500-insertion cap, and `git status --porcelain` reads 0 lines at it. The R10 handback commit `4f504337` is owed the same pair and they are NOT stated here, because this entry is written by the round that follows R10 and that commit's readings belong beside the round that follows R11. WHY R10 IS PASS: every gate reproduces under the reviewer's own execution, the ledger arithmetic is exact, and the one defect it landed was declared by the worker before the reviewer read the diff rather than discovered afterwards.

- R-0650 — Low, A NEWLINE CONVENTION STATED ONCE FOR ALL SLICE KINDS STRIPPED THE TERMINATOR FROM A WHOLE-FILE TARGET. The defect is the reviewer's, in the F021 R10 block's constraint 5, and it landed in `.agent/plan.md` at `b33f0305`. That constraint reads "Every slice in this block is quoted WITHOUT a trailing newline" and then describes only how an APPEND is written; the block also carried a WHOLE-FILE replacement, and its G4 ordered `cmp` at exit 0 against the extracted slice. Both clauses together admit exactly one reading — write the file as the bare slice — so the worker wrote it that way, `cmp` passed, and `.agent/plan.md` became the ONLY file under `.agent/` with no terminating newline. Measured by the reviewer at `4f504337`: that file's last byte is not a newline while `live_review.md`, `handoff.md`, `last_block.md`, `context.md` and `decisions.md` all end with one, and at the round base `7823005d` the same file DID end with one. WHY LOW: nothing is red — the three contract suites, the canary and `tests/ui_contracts/` all pass at `4f504337` — and the cost is a `\ No newline at end of file` marker plus one extra changed line in the next diff that rewrites the file. WHY IT IS REGISTERED AT ALL: the convention would have kept stripping it on every future round, because a block that rewrites `.agent/plan.md` every round would have carried the same sentence forward, and the worker's declared deviation lives in a handback that the NEXT handback overwrites. The deeper cause is the one R-0437 names and this instance widens: a text property that depends on the newline convention must be stated per MEASUREMENT, and R10 corrected R9's under-specification by over-generalising in the opposite direction — the R-0526 shape, a universal asserted over the author's own slices where only one kind was meant.

  FIX: state the convention PER SLICE KIND — a whole-file replacement is the slice plus one terminating newline, an append is one newline plus the slice plus one terminating newline — and word the `cmp` gate to match the kind it proves. The F021 R11 block does both, and its C1 restores the terminator to `.agent/plan.md`; constraint 2 of that block fixes that C1 precedes this entry, which is how this paragraph can state the restoration at all (§3 checklist item 20 as narrowed by R-0524). Promoting the per-kind rule into the §3 pre-emission checklist needs a round with `docs/` in its change set and is NOT claimed to have happened here.
<<<END RECORD10
