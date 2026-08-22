── STEP T002-SCROLL — F021 ──
Goal:        Wire `feedScroll.ts` into the live feed's scroll container with the
             feature file's "jump to live" affordance, so the one rule this
             feature built and left unread becomes reachable in the product;
             and record R30, which PASSED, correcting the one defect it
             surfaced. That defect is the REVIEWER's and mints no id: R-0644 is
             open and its standing rule names this exact failure, so §3
             checklist item 30 routes the evidence there.

Fortschritt: ~98 % (T002 — Feed-Scroll verdrahtet; es fehlt nur noch T003:
             Klick-Sprung und der deaktivierte Steuer-Eingang)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R30 verdict
             and the R-0644 correction · C3 DECISION F021 D10 · C4 the CSS
             scroll container and pill · C5 the card wiring · C6 the contract
             pins · C7 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r31.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/decisions.md` (C3) ·
             `apps/ui/src/components/panels/RightLivePanel.module.css` (C4) ·
             `apps/ui/src/components/panels/ActivityFeedCard.tsx` (C5) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C6) ·
             `.agent/handoff.md` (C7). Resolve any count in this block against
             that list. `apps/ui/src/api/feedScroll.ts` is NOT edited: this
             round wires the rule that file already holds and changes none of
             it.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it. The workers of R28, R29 and R30 each did
    exactly that against a faulty gate of mine and were right every time.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6, C7 and is not negotiable.
    C1 precedes the ledger commit because the plan must be current before it
    (§3 checklist item 23). C4 precedes C5 so the class names the card
    references exist when it references them. C6 lands the pins AFTER the code
    they pin. ROUND BASE is `d63d29e8` — resolve its full form with
    `git rev-parse`.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. Before it: 223 registered
    under the canonical pattern `^- R-\d+ — `, maximum R-0660, `Done: R-` 1.
    After C2 all three are UNCHANGED. The correction names OPEN finding R-0644
    rather than a new id, per §3 checklist item 30.
 4. NO PARAGRAPH OF RECORD31 BEGINS WITH THE BYTES `- R-`. That prefix is this
    file's REGISTRATION shape, and a non-registration paragraph wearing it
    lands a line a loose reader counts as a registration — the R29 defect R30
    recorded. The correction opens with `Recurrence: R-0644 — `, matching the
    prefix R30 introduced for exactly this kind. G7 measures this.
 5. THE NEWLINE CONVENTION, one reading, stated twice so the halves cannot
    disagree. Every slice and every pair half is quoted WITHOUT a trailing
    newline. A WHOLE-FILE write (PLANF021R31) is the slice PLUS one terminator.
    EVERY APPEND — RECORD31 at C2, DECISION10 at C3, PINSLICE at C6 — is
    EXACTLY ONE ADDED NEWLINE, then the slice, then one terminator, so the
    boundary carries EXACTLY ONE BLANK LINE. For `.agent/decisions.md` that one
    blank line is the convention 114 of its 115 earlier entries use, a number I
    measured at `d938b34c` with a script rather than by eye — which is the
    correction this round's own C2 lands.
 6. THE LEDGER AND THE DECISION RECORD ARE APPEND-ONLY. Neither R-0644's own
    paragraph nor any landed `Gate:` entry nor DECISION F021 D9 is edited. A
    dated correction that names the landed text is how these records stay
    honest; overwriting is worse than a wrong sentence (§3 item 20).
 7. NO COUNT GATE IN THIS BLOCK COUNTS A STRING WHOSE NUMBER THIS BLOCK'S OWN
    SLICES CHANGE, AND EVERY LEDGER COUNT NAMES THE PATTERN IT IS READ UNDER.
    Where a count could be read two ways, BOTH are ordered and reported side by
    side.
 8. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide at every commit under R-0622 and is NOT a gate of this round —
    do not run it and do not report it. Create and merge NO pull request. Push
    the branch after C7.
 9. THE PAIR SHAPES ARE MEASURED, NOT ASSERTED. I ran the containment test over
    each pair's own bytes before emission, and it printed, per pair:
    CSSPAIR — `TO contains FROM: false`. CARDIMPORT — `TO contains FROM: false`.
    CARDFEED — `TO contains FROM: false`. All three are therefore REWRITES, and
    G6 orders the FROM-zero count that only a rewrite can meet (§3 items 4 and
    15). Each FROM occurs exactly once in its target at the round base, a count
    my script printed whole-line and indent-agnostic with both agreeing.
10. Block size, measured on these final bytes AFTER the last edit: TOTAL 480
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice and
    pair CONTENT lines — 270 against DECISION F085 D5's 400. Markers count as
    prose.
11. THE CARD KEEPS EVERY STRING ITS EXISTING GUARDS READ. I grepped the suite
    for tests reading `ActivityFeedCard.tsx` before authoring these pairs (§3
    checklist item 7) and there are five: the comment-stripped source must hold
    `recent.slice(-LIVE_ROWS_SHOWN).reverse()` and `recentDropped > 0`
    (tests/ui_contracts/test_brain_stream_ring.py), the raw source must hold
    `No activity yet` or `emptyState` (tests/ui_server/test_dashboard_contract.py)
    and `Activity`, and must hold NEITHER `@mui` NOR `POST`
    (tests/ui_contracts/test_design_drift.py, tests/ui_contracts/test_responsive.py).
    The pairs preserve all of them and G8 measures each rather than trusting it.
    No test pins the VALUE of `LIVE_ROWS_SHOWN`, which is why D10 may change it.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C7; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a through C6. C7's own reading is ordered
     NOWHERE — §3 item 31 leaves it to the next session.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r31.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over my emitted
     copy at `.remedy-wt/f021-r31.md` are all equal. Write C0b FROM the
     committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their marker LINES,
     `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO `. Report how many whole texts,
     how many pairs and how many CONTENT lines the extractor printed — each a
     number YOU measured, not one I named — and re-measure constraint 10's two
     numerals from that same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R31 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare slice
     that must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1, and the `wc -l` YOU measure against
     AGENTS.md's "keep it short (<50 lines)". If that count is 50 or more, STOP
     and report — do NOT trim the file to reach it, the error R-0654 records.
 G5  THE TWO APPENDS, at C2 (`.agent/live_review.md`) and C3
     (`.agent/decisions.md`), EACH under TWO INDEPENDENT READERS. Read each base
     blob with `git show <sha>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision.
     Reader (a): the base blob is a byte-exact PREFIX of the committed file and
     the remainder is EXACTLY one newline plus the slice plus one newline —
     report each remainder's sha256, byte and line counts, and each file's
     counts before and after. Reader (b), SET-WISE: strip the one trailing
     terminator from BOTH blobs, split each on the blank line into units, and
     confirm the new unit LIST equals the base list followed by the slice's own
     units, ELEMENTWISE OVER THE WHOLE LIST, not at the tail; report N at both
     points and each slice's unit count as the number YOU measured. REPORT ALSO
     the BLANK LINES at each join — between the base blob's last non-empty line
     and the slice's first line — which constraint 5 fixes at 1 for both.
     NEGATIVE CONTROL, per file: alter one printable byte of that file's FIRST
     paragraph at equal length; BOTH readers must REJECT it and ACCEPT the true
     file. Name the offset and the change. Report that neither diff deletes a
     line.
 G6  THE THREE PAIRS, each a REWRITE by constraint 9's measured shape, so for
     each report the FROM string occurring EXACTLY 1x in its target at the round
     base and EXACTLY 0x after its commit, and the TO string 0x then 1x:
     CSSPAIR at C4 over the CSS, CARDIMPORT and CARDFEED at C5 over the card.
     Both base readings are taken with `git show <base>:<path>`, never by
     writing a tracked file. Report also, at C4, that `max-height: 52vh` occurs
     1x and `overflow: auto` 1x — the container the feature file's binding CSS
     block fixes — and that `.jumpToLivePill` occurs 1x as a selector at line
     start.
 G7  THE LEDGER SETS AND THE CORRECTION SHAPE, at the round base and at C2, EACH
     UNDER BOTH READINGS: the CANONICAL pattern `^- R-\d+ — ` and the LOOSE
     prefix `- R-` at line start. Report for both patterns at both commits: the
     count, how many DISTINCT ids, and the MAXIMUM id. The canonical reading
     must be 223, all DISTINCT, maximum R-0660, AT BOTH COMMITS — that set is
     the one §3 item 10 derives the open set from and this round does not move
     it. Report the loose reading as the number YOU measure and state whether it
     moved. Report also, line-anchored: `Done: R-` 1 at both; `Landed: ` 0 at
     both; `Gate: R` keys 29 then 30, DISTINCT at both; `Gate: R31` 0 then 1;
     `- R-0661` 0 at both, which is constraint 3 measured; the number of
     RECORD31 lines beginning with the bytes `- R-`, which must be 0, which is
     constraint 4 measured; `^Recurrence: R-0644 — ` 0 then 1; `^Recurrence: `
     2 then 3; and `- R-0644 — ` exactly 1 at BOTH commits, since the correction
     names that finding and must not disturb its registration.
     For `.agent/decisions.md` at C3, report `^## DECISION F021 D10 ` exactly 1,
     that it is the LAST `^## DECISION ` heading in the file, and the blank
     lines directly above it, which must be 1.
 G8  THE CARD'S EXISTING GUARDS, measured at C5 rather than trusted, which is
     constraint 11. Over
     `apps/ui/src/components/panels/ActivityFeedCard.tsx`, report each of these
     as a count: in the COMMENT-STRIPPED source (strip `//` and `/* */`, the
     same rule tests/ui_contracts/test_brain_stream_ring.py uses)
     `recent.slice(-LIVE_ROWS_SHOWN).reverse()` 1 and `recentDropped > 0` 1; in
     the RAW source `emptyState` at least 1, `No activity yet` 1, `Activity` at
     least 1, `@mui` 0 and `POST` 0. Report also, in the comment-stripped
     source, `shouldFollowNewest` 2, `shouldShowNewRowsPill` 2, `nextFeedScroll`
     3, `FEED_SCROLL_START` 3 and `scrollTop` 3 — the wiring this round exists
     to land, the first four counted INCLUDING their occurrence on the import
     line — and `from "../../api/feedScroll"` exactly 1. I measured all nine of
     these by applying this block's own pairs in a disposable worktree at
     `d63d29e8` and running the suite's own `strip_ts_comments` over the result.
 G9  THE TYPECHECK AND THE SUITES, at C6 in the PRIMARY checkout, SERIALLY, from
     the REPOSITORY ROOT unless a line below names another directory — a shell
     left elsewhere makes the Python suites exit 4 having run no test, which is
     vacuous and not green. Report each exit code, the working directory and
     each total, counting BY PASSED PLUS SKIPPED:
       `npx tsc --noEmit` run from `apps/ui` — exit 0 with EMPTY output. This is
       the load-bearing gate of the round: vitest does not typecheck, and no DOM
       test in this repository can reach a React hook.
       `npm run test:unit` from `apps/ui` — the vitest suite, which covers
       `feedScroll.ts` itself and must be UNCHANGED in file and test counts by a
       round that adds no vitest case. Report both numbers. Use `npm run
       test:unit`, never `npx vitest`, which this session's guard denies
       (R-0651).
       `python3 -m pytest tests/ui_contracts/ -q -rf` — the contract suite,
       whose total MUST rise by exactly the number of test functions PINSLICE
       adds, a number YOU count from the committed slice rather than one I name.
       Report the base total, the C6 total and their difference.
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511, the gate that the
       `.agent/` state readers still parse what C1, C2 and C3 wrote.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/` path.
G10  THE RED CONTROL FOR THE NEW PINS, inside a DISPOSABLE `git worktree` under
     `.remedy-wt/` at C6 and NEVER in the primary checkout (§4.10, guardrail
     G5). A pin that cannot fail proves nothing. In that worktree delete the
     single line holding the bytes
     `if (shouldFollowNewest(distance) && boxRef.current) {`
     from `apps/ui/src/components/panels/ActivityFeedCard.tsx` — a string I
     measured to occur EXACTLY ONCE in that file at C5, whole-line and
     indent-agnostic counts agreeing — plus the TWO LINES DIRECTLY BELOW IT,
     which are that branch's single body statement and its closing brace, so the
     file still parses; three deleted lines in all, and re-run
     `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf`.
     Report the GREEN count before the edit and, after it, the ORDERED COLOUR
     RED with the failing node id NAMED. Report the count you measured for that
     byte string. Then remove and prune the worktree and report
     `git worktree list` as the primary checkout ALONE.
G11  RANGE, executed at C6 and covering the round base to C6 — NOT to C7,
     because C7 writes the file that must quote these gates and §3 checklist
     item 31 forbids ordering a reading the quoting artefact cannot hold.
     Report: the base-to-C6 path set against the eight non-handoff paths of
     `Change:`, the difference EMPTY both ways; every commit single-parent;
     `git show --numstat` and `git diff --numstat` agreeing cell by cell with
     the handback's `## Commits` tables (§3 item 28), any disagreement reported
     rather than reconciled; every insertion count under the 500 cap;
     `git ls-files .remedy-wt` 0; and `gh pr list --state open --json
     number,headRefName` — expected EMPTY — with the statement that neither `gh
     pr create` nor `gh pr merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED and scoped to the files a slice or pair
     LANDED IN — `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`,
     the CSS, the card and the contract test — and covers EVERY marker prefix
     this block uses, which G3 names and you count for yourself: each must read
     0, as must any line starting `<<<`. The two block mirrors ARE the block and
     read nonzero by construction.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog --format=%gs`,
     take the OPERATION only — the text BEFORE the first `:` — and scope to THIS
     ROUND'S rows. Report that every such row's operation is `commit` and that
     `amend`, `rebase` and `cherry` each occur 0 times in that OPERATION field.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a through C7, the round base SHA, ONE LINE PER GATE with
            transcripts kept out of the file (R-0582), and the `Fortschritt:`
            line verbatim across all three of its lines. Report its own `wc -l`
            against the 60-line cap, with a DECISION D15 line declaring any
            overage and its mandated cause; a handback whose per-commit tables
            cover more than five commits may reach 100. Every `## Commits`
            heading carries that commit's FULL subject, and where a commit
            cannot name its own SHA the role and reason go INSIDE the heading
            (R-0494). `## Next` states that R31's own verdict is UNRECORDED and
            the next round's ledger commit owes it, together with C7's own
            insertion count and line count, which C7 cannot state about itself;
            and that R32 is T003 — the row click-jump to the graph store and the
            disabled steering input with the tooltip naming F030.

<<<SLICE PLANF021R31
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
R31 wires `feedScroll.ts` into the live feed's scroll container — the rule this
feature built at R17 and has left unread since — with the "jump to live"
affordance the feature file binds, the 52vh scroll box its binding CSS fixes,
and contract pins plus a red control, because no DOM test here can reach a
React hook. The same round records R30, which PASSED, and appends the one
correction it owes: a count RECORD30 stated about `.agent/decisions.md` was
hand-read and is wrong by one in both numerals, which is open finding R-0644's
standing rule failing while its SHA clause was obeyed. No id is minted.

## Next Steps
1. R32: T003 — the row click-jump to the graph store, then the disabled
   steering input with the tooltip naming F030.
2. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- The scroll wiring is a React effect over a ref. Nothing here can execute it,
  so its guard is the source contract plus the purity of `feedScroll.ts`, which
  vitest does cover, plus a red control that deletes the follow branch.
- `npm run lint` is RED tree-wide at every commit: the eslint config has no
  TypeScript parser, so it reports a parsing error per file and is blind to
  style. That is R-0622, still open.
- This ledger carries two `- R-0618` lines under a LOOSE `- R-` reading and one
  under the canonical `^- R-\d+ — ` pattern. The canonical reading is the open
  set; R30's C2 says so on disk.
- No code defect of F021 is open; R-0364, R-0403, R-0587, R-0607 through R-0609,
  R-0611, R-0613, R-0618, R-0622, R-0630, R-0644, R-0651 and R-0653 through
  R-0659 stay routed to a paydown branch.
<<<END PLANF021R31

<<<SLICE RECORD31
Recurrence: R-0644 — A COUNT ABOUT A FILE OUTSIDE THE BLOCK WAS HAND-READ, NAMED ITS SHA, AND IS WRONG BY ONE IN BOTH NUMERALS. Second instance, in the reviewer's own F021 R30 block; NO NEW ID IS MINTED, because R-0644 already rules that "a slice asserting a COUNT about a file outside the block names the SHA per item 20 AND has that count produced by a script at that SHA in the same pre-emission pass that measures the block's own size, or it states the enumeration and NO numeral at all" — and this is that rule failing while its SHA half was obeyed (§3 checklist item 30). THE INSTANCE: RECORD30, applied at `e92189bb`, corrects R29's `.agent/decisions.md` separator and says "Re-measured by the reviewer at `d938b34c`: the D9 heading is preceded by 3 newlines where 113 of that file's 114 earlier entries use 2 and exactly one earlier entry already uses 3". The SHA is named and the reading was still not taken by a script. Re-measured at `d938b34c` by walking every `^## DECISION ` heading and counting the newlines directly above each: there are 116 such headings, so 115 are EARLIER than D9, and their distribution is 114 with 2 newlines and 1 with 3 — not 113 of 114. The same walk under a second reading, counting BLANK LINES rather than newlines, gives 114 with one blank line and 1 with two, which agrees. Every plausible alternative reading of "entry" was tested and none produces 113 of 114: `^## DECISION F` gives 112 earlier with 111 at the convention, and `^## ` gives 423 earlier. WHAT IS UNHARMED: the sentence's CONCLUSION is exactly right and is the half that carried the argument — the landed D9 separator matches a pre-existing outlier rather than the convention, one earlier entry already used 3 newlines, and R30's own constraint 5 was written from that correct conclusion and is itself correct. Nothing consumed the two numerals. WHY THIS IS RECORDED RATHER THAN REWRITTEN: `.agent/live_review.md` is append-only and §3 item 20 rules that a dated correction is how it stays honest, so RECORD30's paragraph stands and the measured values are here. THE CORRECTED VALUES: at `d938b34c`, 114 of the 115 entries earlier than D9 use the two-newline convention and exactly one already used three. ADDED TO R-0644'S FIX, binding the reviewer: the script that produces such a count runs in the SAME pre-emission pass that measures the block's own size, and the block reports the count it PRINTED — never a numeral re-typed from a reading taken in an earlier turn, which is the form both instances took.

Gate: R31 — the R30 entry. R30 PASSED ON EVERY GATE WHOSE SUBJECT IS THE WORK, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND ITS ONE RED CLAUSE IS THE REVIEWER'S OWN, RECORDED IN THE ENTRY ABOVE. R30 IS THE RECORD-AND-CORRECT ROUND: it recorded R29's PASS and appended two corrections that mint no id, routing a mis-anchored ledger count to R-0630 and a registration-shaped paragraph plus a self-contradicting append convention to R-0587. TRANSPORT HELD ACROSS ALL FOUR COPIES at sha256 8c253cacaed190df11989abc8b5abb369703f179666591fb3d855481b1ed41ad over 25620 bytes and 245 lines: my own `.remedy-wt/f021-r30.md`, `.agent/authored/f021-r30.md` at `8f43f78f` and `.agent/last_block.md` at `df79260c`, the last written FROM the committed C0a blob. SLICES: my extractor read the whole texts PLANF021R30 and RECORD30 and 0 pairs over 53 CONTENT lines from that committed blob, with 4 marker lines and no stray `<<<`, TOTAL 245 against DECISION F085 D6's 490 and PROSE 192 against D5's 400 — both equal to that block's constraint 9. THE PLAN WRITE HELD: `.agent/plan.md` at `d47c58bc` is byte-equal to that block's plan slice plus one terminating newline and NOT to the bare slice, `wc -l` exactly 48. THE LEDGER APPEND HELD UNDER BOTH READERS: at `e92189bb` the base blob is a byte-exact prefix, the remainder is exactly one newline plus the slice plus one newline at sha256 32e75c01eb324eb919b3058a303930fce2d678ad91116f8685232c3910d4b56f over 9568 bytes and 6 lines, the file went 594466 B/1186 L to 604034 B/1192 L, the unit list went 274 to 277 ELEMENTWISE with RECORD30 measuring 3 units, the join carries exactly ONE blank line, and a negative control at offset 2 of the FIRST paragraph — `L` to `Z` at equal length — was REJECTED by both readers while both ACCEPTED the true file. THE SETS DID NOT MOVE: the canonical `^- R-\d+ — ` reads 223, all DISTINCT, maximum R-0660, at the round base AND at C2; the loose `- R-` reads 224 at both with `R-0618` twice, unmoved because R29 landed that line and R30's constraint 6 forbade editing it; `Done: R-` 1 at both, `Landed: ` 0 at both, `Gate: R` keys 28 then 29 DISTINCT, `Gate: R30` 0 then 1, `- R-0661` 0 at both. THE CORRECTION SHAPE HELD: 0 RECORD30 lines begin `- R-`, `^Recurrence: R-0630 — ` and `^Recurrence: R-0587 — ` each 1 at C2 against 0 at the base, `^Recurrence: ` 0 then 2, and `- R-0630 — ` and `- R-0587 — ` each still exactly 1 at BOTH commits. THE SUITES ARE MY OWN, run SERIALLY in the PRIMARY checkout from the repository root: the three state-reading suites 511 passed plus 0 skipped, and the canary 42 passed plus 0 skipped. THE RANGE HELD: five commits base to C3, every one single-parent, the path set base-to-C2 EQUAL to the four non-handoff `Change:` paths with both differences EMPTY, insertions 245, 167, 15 and 6 each under the 500 cap and each agreeing cell by cell with the handback's tables, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout ALONE, `gh pr list --state open` EMPTY, the marker sweep 0 line-anchored in both files a slice landed in, and the reflog read BY OPERATION every row `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE OWED READINGS, which R30's own handback could not hold about itself (§3 item 31): its C3 `d63d29e8` is single-parent and touches `.agent/handoff.md` ALONE at 35 insertions and 55 deletions, under the 500 cap, and that handback measures 69 lines by `wc -l` — over the 60-line baseline, declared under DECISION D15 with its mandated cause named, which is what that rule asks of a round whose five commits do not reach the 100-line tier. WHY R30 IS PASS: every applied byte is reproducible from the committed block by my own extractor, both append readers agreed with a negative control that really rejects, the corrections name open findings instead of minting ids, and the one defect the round carries is a numeral in my own text that no gate it ordered could have caught.
<<<END RECORD31

<<<SLICE DECISION10
## DECISION F021 D10 (2026-08-22) — the feed's newest edge is the TOP, and the live window is deliberately taller than its box

CONTEXT: `apps/ui/src/api/feedScroll.ts` has existed since R17 as a pure rule — `shouldFollowNewest`, `nextFeedScroll`, `shouldShowNewRowsPill` over a `distanceFromNewest` in pixels — and nothing imported it. R31 wires it into `ActivityFeedCard.tsx`. Two things had to be ruled before that wiring could be written, because the design sources disagree in wording and the built feed disagrees with both in direction. CHOSEN: (1) `distanceFromNewest` is `scrollTop`, because the live feed renders NEWEST FIRST — `recent.slice(-LIVE_ROWS_SHOWN).reverse()`, a line tests/ui_contracts/test_brain_stream_ring.py has pinned since R16 — so the newest row sits at the TOP of the box and offset 0 IS the newest edge. docs/ui/design_reference/component_spec.md says "autoscroll pinned-to-bottom" and docs/roadmap/features/T5_F021.md says "auto-scroll pinned to newest"; the second is the roadmap layer, which AGENTS.md's documentation-boundary rule makes the authority for planning, and "newest" resolves correctly in a newest-first list while "bottom" does not. (2) The affordance is labelled `Jump to live` with the unseen count beside it, the exact wording T5_F021.md binds, rather than component_spec.md's "↓ new" pill — an arrow pointing down would point AWAY from the newest edge under (1), and taking the roadmap file's wording introduces no glyph, no icon and no asset, so no assets_spec.md change and no design-fidelity deviation is owed. (3) `LIVE_ROWS_SHOWN` rises from 5 to 40. The feature file's binding CSS gives the feed `max-height:52vh;overflow:auto`, and a window of 5 rows can never overflow a box that tall, so the never-yank rule and the pill would both remain unreachable in the product — headless in a second sense, after having been headless in the first since R17. The ring still holds BRAIN_RECENT_LIMIT at 500 and the timeline is still the archive. ALTERNATIVES CONSIDERED: flipping the feed to newest-LAST to match component_spec.md's "bottom" wording literally, rejected because it would rewrite behaviour R16 pinned and vitest covers, to gain nothing an axis convention does not already give; and keeping 5 rows with a shorter box, rejected because the box height is the one thing the feature file states as binding CSS. HOW TO REVERSE: (1) and (2) reverse together by rendering the feed newest-last, passing `scrollHeight - clientHeight - scrollTop` as `distanceFromNewest` and restoring the "↓ new" label; (3) reverses by restoring the constant to 5. `feedScroll.ts` itself changes under none of these — it is a pure function of a distance, and which end of the box that distance is measured from is this decision, not that module's.
<<<END DECISION10

<<<FROM CSSPAIR
.activityList { display: flex; flex-direction: column; gap: 14px; }
<<<TO CSSPAIR
/* DECISION F021 D10: the 52vh box the feature file's binding CSS fixes. The
   feed renders newest-first, so the newest edge is scrollTop 0; the pill is
   sticky at the TOP of the box, which is the edge it invites a jump back to. */
.activityList { display: flex; flex-direction: column; gap: 14px; max-height: 52vh; overflow: auto; }
.jumpToLivePill {
  position: sticky;
  top: 0;
  align-self: center;
  border: 0;
  cursor: pointer;
  padding: 4px 12px;
  border-radius: var(--remedy-radius-pill);
  font: 500 12px/1.4 var(--remedy-font-ui);
  background: var(--remedy-blue);
  color: var(--remedy-ink-strong);
}
<<<END CSSPAIR

<<<FROM CARDIMPORT
import type { RemedyActivityItem } from "../../api/types";
import type { FeedRow } from "../../api/feedRow";
import { BuilderGlyph, ReviewerGlyph, PersonGlyph, GearGlyph } from "../icons/RemedyGlyphs";
import styles from "./RightLivePanel.module.css";
<<<TO CARDIMPORT
import { useCallback, useEffect, useRef, useState } from "react";
import type { RemedyActivityItem } from "../../api/types";
import type { FeedRow } from "../../api/feedRow";
import { FEED_SCROLL_START, nextFeedScroll, shouldFollowNewest, shouldShowNewRowsPill } from "../../api/feedScroll";
import { BuilderGlyph, ReviewerGlyph, PersonGlyph, GearGlyph } from "../icons/RemedyGlyphs";
import styles from "./RightLivePanel.module.css";
<<<END CARDIMPORT

<<<FROM CARDFEED
/** How many live rows the side panel shows. The ring holds up to
 *  BRAIN_RECENT_LIMIT; this card is a glance and the timeline is the archive. */
const LIVE_ROWS_SHOWN = 5;

/** The live half of the card: rows projected from the SSE stream, NEWEST
 *  FIRST. Remedy deliberately does not merge these with the dashboard's REST
 *  activity list — two clocks in one list would order neither honestly — so
 *  live rows REPLACE that list as soon as the stream has produced any. */
function LiveFeed({ recent, recentDropped }: { recent: readonly FeedRow[]; recentDropped: number }) {
  const newestFirst = recent.slice(-LIVE_ROWS_SHOWN).reverse();

  return (
    <div className={styles.activityList}>
<<<TO CARDFEED
/** How many live rows the side panel keeps. DECISION F021 D10 raised this from
 *  5 to 40 deliberately: the feature file's binding CSS gives the feed a 52vh
 *  box, and a window that always fits inside its box can never scroll, which
 *  would leave feedScroll.ts's never-yank rule unreachable in the product. The
 *  ring still holds BRAIN_RECENT_LIMIT and the timeline is still the archive. */
const LIVE_ROWS_SHOWN = 40;

/** The live half of the card: rows projected from the SSE stream, NEWEST
 *  FIRST. Remedy deliberately does not merge these with the dashboard's REST
 *  activity list — two clocks in one list would order neither honestly — so
 *  live rows REPLACE that list as soon as the stream has produced any.
 *
 *  Because rows render newest FIRST, the newest edge is the TOP of the box, so
 *  `distanceFromNewest` is `scrollTop` (DECISION F021 D10). feedScroll.ts owns
 *  every decision about following and unseen counts; this component owns only
 *  the DOM reads that rule cannot make, which is what keeps the rule testable
 *  in a repository with no DOM. */
function LiveFeed({ recent, recentDropped }: { recent: readonly FeedRow[]; recentDropped: number }) {
  const newestFirst = recent.slice(-LIVE_ROWS_SHOWN).reverse();
  const boxRef = useRef<HTMLDivElement | null>(null);
  const [scrollState, setScrollState] = useState(FEED_SCROLL_START);
  // What the reader has already been shown. A ref rather than state: it is read
  // and written inside the arrival effect and must never itself cause a render.
  const seenCountRef = useRef(recent.length);

  const readDistanceFromNewest = useCallback((): number => {
    return boxRef.current ? boxRef.current.scrollTop : 0;
  }, []);

  useEffect(() => {
    const arrived = Math.max(0, recent.length - seenCountRef.current);
    seenCountRef.current = recent.length;
    if (arrived === 0) {
      return;
    }
    const distance = readDistanceFromNewest();
    setScrollState(prev => nextFeedScroll(prev, arrived, distance));
    // NEVER YANK: only a reader already at the newest edge is moved. A reader
    // who scrolled up keeps their position and accumulates an unseen count.
    if (shouldFollowNewest(distance) && boxRef.current) {
      boxRef.current.scrollTop = 0;
    }
  }, [recent.length, readDistanceFromNewest]);

  // Returning to the edge clears the unseen count, through the same rule that
  // accumulated it: no row arrives here, so `arrived` is 0.
  const handleFeedScroll = useCallback(() => {
    setScrollState(prev => nextFeedScroll(prev, 0, readDistanceFromNewest()));
  }, [readDistanceFromNewest]);

  const jumpToLive = useCallback(() => {
    if (boxRef.current) {
      boxRef.current.scrollTop = 0;
    }
    setScrollState(FEED_SCROLL_START);
  }, []);

  return (
    <div className={styles.activityList} ref={boxRef} onScroll={handleFeedScroll}>
      {shouldShowNewRowsPill(scrollState) ? (
        <button type="button" className={styles.jumpToLivePill} onClick={jumpToLive}>
          Jump to live · {scrollState.unseenRows} new
        </button>
      ) : null}
<<<END CARDFEED

<<<SLICE PINSLICE
class TestTheFeedScrollRuleIsWiredToTheCard:
    """DECISION F021 D10 and T5_F021's scroll clause. feedScroll.ts was pure and
    UNIMPORTED from R17 until R31: every function it exports was covered by
    vitest and reachable from no screen, which is a rule that ships unread. This
    suite pins the wiring a repository with no DOM cannot execute."""

    def test_the_card_imports_the_rule_rather_than_reimplementing_it(self):
        code = strip_ts_comments(CARD.read_text())
        assert 'from "../../api/feedScroll"' in code, (
            "the scroll rule lives in feedScroll.ts; a card that re-derives it "
            "leaves the tested copy unread"
        )

    def test_the_card_never_scrolls_without_asking_the_rule(self):
        code = strip_ts_comments(CARD.read_text())
        assert "shouldFollowNewest(distance)" in code, (
            "the follow branch must be guarded by the rule, or a reader who "
            "scrolled up gets yanked to the newest row"
        )

    def test_the_distance_is_measured_from_the_edge_the_rows_render_at(self):
        code = strip_ts_comments(CARD.read_text())
        assert "recent.slice(-LIVE_ROWS_SHOWN).reverse()" in code
        assert "boxRef.current.scrollTop" in code, (
            "rows render newest FIRST, so the newest edge is scrollTop 0 "
            "(DECISION F021 D10); measuring from the bottom would invert the rule"
        )

    def test_the_unseen_count_comes_from_the_rule(self):
        code = strip_ts_comments(CARD.read_text())
        assert "nextFeedScroll(prev" in code, (
            "the unseen count must come from the pure rule, which clears it at "
            "the edge, rather than from a counter the component increments"
        )

    def test_the_jump_to_live_affordance_is_rendered(self):
        code = strip_ts_comments(CARD.read_text())
        assert "shouldShowNewRowsPill(scrollState)" in code, (
            "the pill appears only when the rule says rows went unseen"
        )
        assert "Jump to live" in code, (
            "T5_F021 binds the wording; an arrow pointing down would point away "
            "from the newest edge under DECISION F021 D10"
        )

    def test_the_feed_box_can_actually_scroll(self):
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert "max-height: 52vh" in css, (
            "T5_F021's binding CSS fixes the feed box at 52vh"
        )
        assert "overflow: auto" in css, (
            "a box that cannot overflow makes every scroll rule unreachable"
        )
<<<END PINSLICE
