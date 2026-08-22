── STEP RECORD+CORRECT — F021 ──
Goal:        Record R29, which PASSED, and correct the two defects it surfaced
             — both the REVIEWER's, both in the round that was itself recording
             a reviewer defect. Neither mints an id: R-0630 and R-0587 are open
             and each describes its half exactly, so §3 checklist item 30 routes
             the evidence to them. The corrections are APPENDED paragraphs that
             name the landed text; nothing landed is rewritten.

Fortschritt: ~96 % (T002 — Punkt und Badge verdrahtet und geregelt; es fehlt nur
             noch der Feed-Scroll)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R29 verdict
             and the two corrections · C3 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r30.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/handoff.md` (C3). Resolve any count in this block against
             that list. NO source file and NO test file is touched: this round
             changes no behaviour and runs no typecheck.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it. R28's and R29's workers each did exactly
    that against a faulty gate of mine and were right both times.
 2. Commit order is C0a, C0b, C1, C2, C3 and is not negotiable. C1 precedes the
    ledger commit because the plan must be current before it (§3 checklist item
    23). ROUND BASE is `881f0509` — resolve its full form with `git rev-parse`.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. Before it: 223 registered
    under the canonical pattern, maximum R-0660, `Done: R-` 1. After C2 all
    three are UNCHANGED. Both corrections name an OPEN finding rather than a new
    id, per §3 checklist item 30.
 4. NO PARAGRAPH OF RECORD30 BEGINS WITH THE BYTES `- R-`. That prefix is this
    file's REGISTRATION shape, and R29 proved that a non-registration paragraph
    wearing it lands a second `- R-0618` line that a loose reader counts as a
    registration. The two corrections therefore open with `Recurrence: R-0630 — `
    and `Recurrence: R-0587 — `, a prefix no existing record kind in this file
    uses. G7 measures this rather than trusting it.
 5. THE NEWLINE CONVENTION. Every slice is quoted WITHOUT a trailing newline. A
    WHOLE-FILE write (PLANF021R30) is the slice PLUS one terminator. THE LEDGER
    APPEND (RECORD30 at C2) IS EXACTLY ONE ADDED NEWLINE, then the slice, then
    one terminator — so the boundary carries ONE blank line, which is the
    separator every entry in that file already uses. R29's C3 landed TWO added
    newlines into `.agent/decisions.md` because this constraint said "TWO
    newlines" while its own gloss said "the blank line", singular; the count
    here is stated as ADDED NEWLINES and as the resulting BLANK LINE COUNT, so
    the two cannot disagree.
 6. THE LEDGER IS APPEND-ONLY. Neither R-0630's nor R-0587's own paragraph is
    edited, and neither is the `- R-0618 RECURRED` paragraph R29 landed. A
    dated correction that names the landed text is how this record stays honest;
    overwriting it is worse than a wrong sentence (§3 item 20).
 7. NO COUNT GATE IN THIS BLOCK COUNTS A STRING WHOSE NUMBER THIS BLOCK'S OWN
    SLICES CHANGE, AND EVERY LEDGER COUNT NAMES THE PATTERN IT IS READ UNDER.
    That is the R-0630 half of what this round records, and repeating it here
    would be its next instance. Where a count could be read two ways, BOTH are
    ordered and reported side by side.
 8. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide at every commit under R-0622 and is NOT a gate of this round —
    do not run it and do not report it. Create and merge NO pull request. Push
    the branch after C3. Create NO worktree: this round is behaviour-free, so no
    destructive check is owed and none is ordered.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 245
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 192 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C3; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1 and C2. C3's own reading is
     ordered NOWHERE — §3 item 31 leaves it to the next session.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r30.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r30.md` are all equal. Write
     C0b FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their marker LINES,
     `<<<SLICE ` and `<<<END `. This block carries no pair, so no pair marker
     appears; report that as a number YOU measured rather than assuming it.
     Report how many whole texts and how many CONTENT lines the extractor
     printed, and re-measure constraint 9's two numerals from that same blob
     against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R30 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare slice
     that must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1. THE LINE-COUNT CLAUSE IS MEASURED:
     the reviewer counted PLANF021R30 at 48 lines, so `wc -l` must read EXACTLY
     48, satisfying AGENTS.md's "keep it short (<50 lines)". If the count you
     measure differs, STOP and report — do NOT trim the file to reach it, which
     is the error R-0654 records.
 G5  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <sha>:<path>` into memory or scratch under `.remedy-wt/`;
     never overwrite a tracked file to read an older revision. Reader (a): the
     base blob is a byte-exact PREFIX of the C2 file and the remainder is
     EXACTLY one newline plus the slice plus one newline — report the
     remainder's sha256, byte and line counts, and the file's counts before and
     after. Reader (b), SET-WISE: strip the one trailing terminator from BOTH
     blobs, split each on the blank line into units, and confirm the C2 unit
     LIST equals the base list followed by RECORD30's own units, ELEMENTWISE
     over the whole list, not at the tail; report N at both points and the
     slice's unit count as the number YOU measured. REPORT ALSO the number of
     BLANK LINES at the join — the count between the base blob's last non-empty
     line and RECORD30's first line — which constraint 5 fixes at 1; this is the
     reading R29's `.agent/decisions.md` append got wrong and no gate caught.
     NEGATIVE CONTROL: alter one printable byte of the C2 file's FIRST paragraph
     at equal length; BOTH readers must REJECT it and ACCEPT the true file. Name
     the offset and the change. Report that the C2 diff deletes no line.
 G6  THE LEDGER SETS, at the round base and at C2, EACH UNDER BOTH READINGS,
     because R29 proved the two differ and only one is the registration set:
     the CANONICAL pattern `^- R-\d+ — ` — a line beginning `- R-`, then digits,
     then a space, an em dash and a space — and the LOOSE prefix `- R-` at line
     start. Report, for both patterns at both commits: the count, how many
     DISTINCT ids, and the MAXIMUM id. The canonical reading must be 223, all
     DISTINCT, maximum R-0660, AT BOTH COMMITS — that set is the one §3 item 10
     derives the open set from and this round does not move it. The loose
     reading is 224 at BOTH commits with `R-0618` appearing twice, unchanged by
     this round because R29 already landed that line and constraint 6 forbids
     editing it; report it as the number YOU measure and state whether it moved.
     Report also, line-anchored: `Done: R-` 1 at both; `Landed: ` 0 at both;
     `Gate: R` keys 28 then 29, DISTINCT at both; `Gate: R30` 0 then 1; and
     `- R-0661` 0 at both, which is constraint 3 measured.
 G7  THE CORRECTION SHAPE, over the COMMITTED C0a blob's RECORD30 slice and over
     the C2 file, which is constraint 4 measured rather than trusted. Report:
     the number of RECORD30 lines that begin with the bytes `- R-`, which must
     be 0; the line-anchored count of `^Recurrence: R-0630 — ` and of
     `^Recurrence: R-0587 — ` in the C2 file, each of which must be 1; and the
     line-anchored count of `^Recurrence: ` in the file at the round base, which
     must be 0, since this round introduces that record kind. Report also that
     both `- R-0630 — ` and `- R-0587 — ` still occur exactly once each,
     line-anchored, at BOTH commits: the corrections name those findings and
     must not have disturbed their registrations.
 G8  THE PYTHON SUITES, at C2 in the PRIMARY checkout, SERIALLY, from the
     REPOSITORY ROOT — a shell left elsewhere makes these exit 4 having run no
     test, which is vacuous and not green. Report each exit code, the working
     directory and the total, counting BY PASSED PLUS SKIPPED:
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511, the gate that C1
       and C2 did not break the `.agent/` state readers, and the gate that the
       new `Recurrence: ` record kind is not something a reader chokes on.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/` path. No
     typecheck and no vitest run is owed or ordered: the `Change:` list holds no
     path under `apps/`.
 G9  RANGE, executed at C2 and covering the round base to C2 — NOT to C3,
     because C3 writes the file that must quote these gates and §3 checklist
     item 31 forbids ordering a reading the quoting artefact cannot hold.
     Report: the base-to-C2 path set against the four non-handoff paths of
     `Change:`, the difference EMPTY both ways; every commit single-parent;
     `git show --numstat` and `git diff --numstat` agreeing cell by cell with
     the handback's `## Commits` tables (§3 item 28), any disagreement reported
     rather than reconciled; every insertion count under the 500 cap;
     `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout
     ALONE, no worktree having been created; and `gh pr list --state open --json
     number,headRefName` — expected EMPTY — with the statement that neither `gh
     pr create` nor `gh pr merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED and scoped to the files a slice LANDED
     IN — `.agent/plan.md` and `.agent/live_review.md` — and covers EVERY marker
     prefix this block uses, which G3 names and you count for yourself: each
     must read 0, as must any line starting `<<<`. The two block mirrors ARE the
     block and read nonzero by construction.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog --format=%gs`,
     take the OPERATION only — the text BEFORE the first `:` — and scope to THIS
     ROUND'S rows. Report that every such row's operation is `commit` and that
     `amend`, `rebase` and `cherry` each occur 0 times in that OPERATION field.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a, C0b, C1, C2 and C3, the round base SHA, ONE LINE PER
            GATE with transcripts kept out of the file (R-0582), and the
            `Fortschritt:` line verbatim across all three of its lines. Report
            its own `wc -l` against the 60-line cap, with a DECISION D15 line
            declaring any overage and its mandated cause. Every `## Commits`
            heading carries that commit's FULL subject, and where a commit
            cannot name its own SHA the role and reason go INSIDE the heading
            (R-0494). `## Next` states that THIS SESSION IS OVER, having reached
            the round cap it declared at its start; that the NEXT session begins
            at docs/agents/self_drive_protocol.md Phase 1 rule 1 — the
            `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347), which
            will find NO open pull request so rule 5 applies and F021 continues
            on this branch; that R30's own verdict is UNRECORDED and the next
            round's ledger commit owes it, together with C3's own insertion
            count and line count, which C3 cannot state about itself; and that
            R31 wires `feedScroll.ts` into the feed's scroll container with the
            new-rows pill component_spec.md line 86 binds, the last rule this
            feature has built headless and left unread.

<<<SLICE PLANF021R30
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
R30 records R29, which PASSED, and corrects the two defects it surfaced. Both
are the reviewer's and neither mints an id: a ledger count gate anchored on the
loose `- R-` prefix rather than on the registration pattern goes to R-0630, and
a correction paragraph that wore the registration shape — plus an append
convention that landed two blank lines into `.agent/decisions.md` — goes to
R-0587. The corrections are appended and name the landed text.

## Next Steps
1. R31: `feedScroll.ts` into the feed's scroll container with the new-rows pill
   component_spec.md line 86 binds. Headless since R17 and the last rule this
   feature has built and left unread.
2. R32: the row click-jump to the graph store, then T003's disabled steering
   input with the tooltip naming F030.
3. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- The dot's fade is driven by an interval the card owns. No headless test can
  reach a React hook here, so its guard is the source contract plus the purity
  of `recency.ts`, which vitest does cover.
- `npm run lint` is RED tree-wide at every commit: the eslint config has no
  TypeScript parser, so it reports a parsing error per file and is blind to
  style. That is R-0622, still open.
- This ledger now carries two `- R-0618` lines under a LOOSE `- R-` reading and
  one under the canonical `^- R-\d+ — ` pattern. The canonical reading is the
  open set; C2 of this round says so on disk.
- No code defect of F021 is open; R-0364, R-0403, R-0587, R-0607 through R-0609,
  R-0611, R-0613, R-0618, R-0622, R-0630, R-0651 and R-0653 through R-0659 stay
  routed to a paydown branch.
<<<END PLANF021R30

<<<SLICE RECORD30
Recurrence: R-0630 — A COUNT GATE OVER THIS FILE NAMED AN ANCHOR THAT IS NOT THE REGISTRATION PATTERN, AND THE BLOCK'S OWN SLICE MOVED THE NUMBER. Second instance, in the reviewer's own F021 R29 block; NO NEW ID IS MINTED, because R-0630 already rules that "A UNIQUENESS OR COUNT GATE OVER `.agent/live_review.md` MUST NAME THE ANCHOR IT IS READ UNDER" and this is that rule failing while being obeyed (§3 checklist item 30). THE INSTANCE: R29's G6, saved at `02fb2407`, ordered line-anchored `- R-` to read 223 at the round base and at C2, all DISTINCT. R29's own RECORD29 slice opens its first paragraph with `- R-0618 RECURRED, third instance,`, which begins with those exact bytes at line start, so C2 necessarily reads 224 with `R-0618` twice and the gate was unmeetable from the moment the block was written. Re-measured by the reviewer at `a8270b96` under BOTH readings: the LOOSE prefix `- R-` gives 224 with `R-0618` duplicated, while the CANONICAL registration pattern `^- R-\d+ — ` gives 223, all DISTINCT, maximum `R-0660` — identical to the round base under that same pattern. WHAT IS NEW, and what R-0630's fix clause did not carry: R-0630's counter-measure is to NAME the anchor, and R29's gate DID name one — it said line-anchored and it was read line-anchored. Naming an anchor is not sufficient; the anchor must be the pattern that DEFINES the record kind being counted, which for a registration is the id followed by a space, an em dash and a space, because `- R-` alone matches any prose that opens by naming a finding. ADDED TO R-0630'S FIX, binding the reviewer: a gate counting registrations in this file quotes `^- R-\d+ — ` in the gate text, and where a looser reading could differ, orders BOTH and requires them reported side by side. THE OPEN SET IS UNHARMED: §3 item 10 derives it from `^- R-\d+ — ` paragraphs, which is the canonical reading, so no id was registered twice and no finding was lost. The R29 worker applied RECORD29 byte for byte as constraint 1 required, measured both readings, reported the clause RED and repaired nothing — the third consecutive round in which a worker declined to make a reviewer's arithmetic come true, and the reason nothing false is on disk.

Recurrence: R-0587 — AN AUTHORED PARAGRAPH WORE ANOTHER RECORD KIND'S SHAPE, AND AN APPEND CONVENTION CONTRADICTED THE FILE IT APPENDED TO. Second and third instances, both in the reviewer's own F021 R29 block; NO NEW ID IS MINTED, because R-0587 already rules that an authored entry's shape is compared MECHANICALLY against the entries it joins before emission, which §3 checklist item 26 states as the general rule (§3 checklist item 30). INSTANCE ONE, the SHAPE: RECORD29's recurrence paragraph opens `- R-0618 RECURRED, third instance,` — the REGISTRATION shape of this file, used for a paragraph that registers nothing. R-0587's first instance duplicated a KEY within one record kind; this one crosses record KINDS, which is worse in one respect and better in another — worse because a loose reader counts a registration that never happened, better because the canonical pattern rejects it, since `RECURRED,` is not ` — `. The landed paragraph is NOT rewritten (§3 item 20, constraint 6); this correction names it, and R30's own corrections open with `Recurrence: `, a prefix no other record kind in this file uses. INSTANCE TWO, the SEPARATOR: R29's constraint 4 ordered the `.agent/decisions.md` append as "TWO newlines — the blank line that separates entries in that file", whose two halves specify different things — two ADDED newlines produce TWO blank lines, while "the blank line", singular, is one. The worker applied the literal half and declared the contradiction. Re-measured by the reviewer at `d938b34c`: the D9 heading is preceded by 3 newlines where 113 of that file's 114 earlier entries use 2 and exactly one earlier entry already uses 3, so the landed separator matches a pre-existing outlier rather than the convention. Nothing is broken — `## DECISION F021 D9 ` occurs once, is the last such heading, and every suite is green — and it is NOT repaired, because a corrective commit would put a deletion into an append-only record to fix one blank line. ADDED TO R-0587'S FIX, binding the reviewer: a slice joining a repeating record format is compared against its neighbours for SEPARATOR as well as header, and an append convention states the count as ADDED NEWLINES **and** as the resulting BLANK LINE COUNT, so the two halves cannot specify different things. R30's constraint 5 is that rule applied to itself.

Gate: R30 — the R29 entry. R29 PASSED ON EVERY GATE WHOSE SUBJECT IS THE WORK, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND ITS TWO RED CLAUSES ARE THE REVIEWER'S OWN, RECORDED IN THE TWO ENTRIES ABOVE. R29 IS THE BADGE-RULING ROUND: DECISION F021 D9, committed at `d938b34c`, rules that the NowCard badge lights on `isRunning` AND `isLiveByRecency(level)` and never on either alone, because recency alone reads live for the whole quiet window after a job ends — R-0652's rendering with a fuse instead of a latch — while the running flag alone claims life beside a dot that has already faded; `deriveAgentStatus` returns "Working" on exactly the condition making `isRunning` true, so the conjunction makes the R-0652 rendering structurally impossible rather than merely commented against. TRANSPORT HELD ACROSS ALL FOUR COPIES at sha256 723b3bd9dc70e692938d908f9464cb67b09a6eb4bc8b604a1c32fcd490fa1ada over 36795 bytes and 414 lines: the reviewer's own `.remedy-wt/f021-r29.md`, `.agent/authored/f021-r29.md` at `02fb2407` and `.agent/last_block.md` at `e64de319`, the last written FROM the committed C0a blob. SLICES: the reviewer's extractor read the whole texts PLANF021R29, RECORD29 and DECISION9 and the pairs BADGEIMPORT, BADGELEVEL, BADGEJSX, PINBADGE and PINDOTDOC over 137 CONTENT lines from that committed blob, with 0 stray `<<<` lines, TOTAL 414 against DECISION F085 D6's 490 and PROSE 277 against D5's 400 — both equal to that block's constraint 12. THE PLAN WRITE HELD: `.agent/plan.md` at `8af9d825` is byte-equal to that block's plan slice plus one terminating newline and NOT to the bare slice, `wc -l` exactly 47. EVERY PAIR BEHAVED BY ITS MEASURED SHAPE: all five FROMs occurred exactly once in their targets at the round base and 0 after, every TO 0 then 1, the containment test having printed false for all five before emission — and the reviewer re-checked uniqueness AT APPLY TIME in the ordered sequence, because BADGELEVEL's TO introduces `isRunning &&` into the file BADGEJSX then edits. THE CARD IS WHAT D9 RULES: at `d876d8ce` the comment-stripped source holds `isRunning && isLiveByRecency(` once and `{isLive && <span` once, with `newestActionRow` 2, `recent ?? []` 1, `liveAction ? liveAction.line : detail` 1, `recencyLevel(` 1, `data-recency={level}` 1, `setInterval` 1 and `isActive` 0, and the raw file holds neither `Builder is working` nor `@mui`. THE PINS MOVED WITH IT: at `4bdc5b10` the contract file carries the conjunction assertion once, at 19 insertions and 12 deletions, a REPLACEMENT rather than an append as a pin rewrite must be. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY in the PRIMARY checkout: `npx tsc --noEmit` exit 0 with output EMPTY; `npm run test:unit` 15 files and 212 tests; `tests/ui_contracts/` 478 passed plus 4 skipped = 482, UNCHANGED from the round base as a round that rewrites pin text without adding a case must be; the three state-reading suites 511; the canary 42. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `881f0509`: green first at 52 passed, then with `isRunning && isLiveByRecency(level)` — confirmed to occur EXACTLY ONCE, whole-line and indent-agnostic counts agreeing — replaced by `isLiveByRecency(level)`, which is precisely the option D9 rejects, exactly 1 failed and 51 passed, the failure being `TestTheNowCardBadgeTracksTheAgent::test_the_badge_needs_running_and_recent_together`; the worktree was removed and pruned. THE RANGE HELD: eight commits base to C6, every one single-parent, the path set base-to-C5 EQUAL to the seven non-handoff `Change:` paths with both differences EMPTY, insertions 414, 249, 16, 4, 11, 11, 19 and 63 each under the 500 cap and each agreeing cell by cell with the handback's tables, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout ALONE, `gh pr list --state open` EMPTY, the marker sweep 0 line-anchored over all six prefixes in each of the five files a slice or pair landed in, and the reflog read BY OPERATION every row `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE OWED READINGS, which R29's own handback could not hold about itself (§3 item 31): its C6 `881f0509` is single-parent and touches `.agent/handoff.md` ALONE at 63 insertions and 65 deletions, under the 500 cap, and that handback measures 89 lines by `wc -l` — over the 60-line baseline and WITHIN the 100-line tier AGENTS.md grants a handback whose per-commit tables cover more than five commits, which this one's eight do. WHY R29 IS PASS: every applied byte is reproducible from the committed block by the reviewer's own extractor, the ledger remainder matched a digest the reviewer computed independently, the ruling it lands is pinned by a test that fails under the exact alternative the ruling rejects, and both of its red clauses were defects in the reviewer's own text that the worker measured, reported under both readings and refused to paper over.
<<<END RECORD30
