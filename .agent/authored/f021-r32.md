── STEP RECORD+TOKEN — F021 ──
Goal:        Record R31, which PASSED, register and FIX the one live defect it
             shipped — a CSS custom property the shipped stylesheet never
             defines, so the jump-to-live pill renders square — and append the
             two corrections R31's other defects owe. All three defects are the
             REVIEWER's. Only the CSS one mints an id: the other two are already
             ruled by OPEN findings R-0629 and R-0587, so §3 checklist item 30
             routes the evidence there.

Fortschritt: ~98 % (T002 fertig und verdrahtet; es fehlt nur noch T003:
             Klick-Sprung und der deaktivierte Steuer-Eingang)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R31 verdict,
             the R-0661 registration and the two corrections · C3 the token
             definition · C4 the resolution pin · C5 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r32.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/styles/tokens.css` (C3) ·
             `tests/ui_contracts/test_design_drift.py` (C4) ·
             `.agent/handoff.md` (C5). Resolve any count in this block against
             that list. NEITHER `RightLivePanel.module.css` NOR
             `ActivityFeedCard.tsx` is touched: R31 landed both correctly and
             the defect is the MISSING DEFINITION, not the use.

Constraints:
 1. Apply every slice and pair half BYTE FOR BYTE. Never retype, rewrap,
    reflow, reindent or whitespace-adjust one. If a slice looks wrong, STOP and
    say so in the handback rather than fixing it. R31's worker did exactly that
    three times against my own faulty text and was right all three times, which
    is why this round exists at all.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. C1
    precedes the ledger commit because the plan must be current before it (§3
    checklist item 23). C3 lands the token BEFORE C4 pins it. ROUND BASE is
    `8efdb7ea` — resolve its full form with `git rev-parse`.
 3. THIS ROUND MINTS EXACTLY ONE FINDING ID AND RESOLVES NONE. Before it: 223
    registered under the canonical pattern `^- R-\d+ — `, maximum R-0660,
    `Done: R-` 1. After C2: 224 registered, all DISTINCT, maximum R-0661,
    `Done: R-` still 1. The two corrections name OPEN findings rather than new
    ids, per §3 checklist item 30.
 4. EXACTLY ONE PARAGRAPH OF RECORD32 BEGINS WITH THE BYTES `- R-`, and it is
    the R-0661 REGISTRATION, which is what that prefix means in this file. The
    two corrections open with `Recurrence: `, the prefix R30 introduced for
    exactly this kind, and the verdict opens `Gate: R32 — `. G5 measures this
    rather than trusting it.
 5. THE APPEND CONVENTION IS STATED PER TARGET FILE, because the two targets
    have DIFFERENT ones and R31 lost a deviation to assuming they were the same
    (that is the R-0587 half this round records). Every slice and pair half is
    quoted WITHOUT a trailing newline.
      `.agent/live_review.md` at C2: EXACTLY ONE ADDED NEWLINE, then RECORD32,
      then one terminator, so the join carries EXACTLY ONE BLANK LINE — the
      separator every entry in that file already uses.
      `tests/ui_contracts/test_design_drift.py` at C4: EXACTLY TWO ADDED
      NEWLINES, then PINSLICE2, then one terminator, so the join carries
      EXACTLY TWO BLANK LINES — PEP 8 E302, which all 19 of that file's
      existing top-level classes obey, a number I measured at `8efdb7ea` with a
      script rather than by eye. `ruff` cannot see this rule (E301-E306 are
      preview-only), so the convention is met by construction here or not at
      all.
    A WHOLE-FILE write (PLANF021R32) is the slice PLUS one terminator.
 6. THE LEDGER IS APPEND-ONLY. No landed paragraph, `Gate:` entry or
    `Recurrence:` entry is edited. A dated correction that names the landed text
    is how this record stays honest (§3 item 20).
 7. NO COUNT GATE IN THIS BLOCK COUNTS A STRING WHOSE NUMBER THIS BLOCK'S OWN
    SLICES CHANGE, AND EVERY LEDGER COUNT NAMES THE PATTERN IT IS READ UNDER.
    Where a count could be read two ways, BOTH are ordered and reported side by
    side.
 8. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide at every commit under R-0622 and is NOT a gate of this round —
    do not run it and do not report it. Create and merge NO pull request. Push
    the branch after C5. Create NO worktree: this round adds no branch to any
    control flow, so no red-proof is owed and none is ordered.
 9. THE ONE PAIR IS TOKENPAIR, AND ITS SHAPE IS MEASURED, NOT ASSERTED. I ran
    the containment test over its own bytes before emission and it printed
    `TO contains FROM: true`, so TOKENPAIR is APPEND-SHAPED. §4.9 therefore
    FORBIDS ordering a FROM-zero count for it, and G4 orders the append
    obligation instead. Its FROM occurs exactly once in its target at the round
    base, whole-line and indent-agnostic counts AGREEING at 1 — a reading I took
    over the bytes this block PRINTS, including their two leading spaces, which
    is the distinction R31's G10 got wrong and this round records.
10. Block size, measured on these final bytes AFTER the last edit: TOTAL 330
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice and
    pair CONTENT lines — 225 against DECISION F085 D5's 400. Markers count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C5; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2, C3 and C4. C5's own reading
     is ordered NOWHERE — §3 item 31 leaves it to the next session.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r32.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over my emitted
     copy at `.remedy-wt/f021-r32.md` are all equal. Write C0b FROM the
     committed C0a blob. Report the digest, bytes and lines. Then extract the
     slices and the pair from the COMMITTED C0a blob by their marker LINES,
     `<<<SLICE `, `<<<END `, `<<<FROM `, `<<<TO `, and report how many whole
     texts, how many pairs and how many CONTENT lines your extractor printed —
     each a number YOU measured, not one I named — re-measuring constraint 10's
     two numerals from that same blob against their caps.
 G3  `.agent/plan.md` at C1 equals PLANF021R32 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare slice
     that must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1, and the `wc -l` YOU measure against
     AGENTS.md's "keep it short (<50 lines)". If that count is 50 or more, STOP
     and report — do NOT trim the file to reach it (R-0654).
 G4  THE TOKEN, at C3 over `apps/ui/src/styles/tokens.css`. TOKENPAIR is
     APPEND-SHAPED by constraint 9's measured containment, so DO NOT count the
     FROM to zero — it is still present by construction. Report instead: the
     FROM string occurring EXACTLY 1x at the round base AND EXACTLY 1x at C3;
     `--remedy-radius-pill` occurring 0x at the round base and EXACTLY 1x at C3;
     and, over the lines THAT COMMIT'S DIFF ADDS, each TO-ONLY line exactly once
     (§4.9). Report also that the value written is `999px`, which is what
     `docs/ui/design_reference/tokens.css` has defined for that token since the
     design pack landed — quote both sides. The base reading is taken with
     `git show <base>:<path>`, never by writing a tracked file.
 G5  THE LEDGER, at the round base and at C2, EACH UNDER BOTH READINGS: the
     CANONICAL pattern `^- R-\d+ — ` and the LOOSE prefix `- R-` at line start.
     Report for both patterns at both commits: the count, how many DISTINCT ids,
     and the MAXIMUM id. The canonical reading must be 223 at the base and 224
     at C2, all DISTINCT at both, maximum R-0660 then R-0661 — this round adds
     exactly one registration and constraint 3 is that sentence measured.
     Report the loose reading as the number YOU measure and state whether its
     gap to the canonical reading changed. Report also, line-anchored:
     `Done: R-` 1 at both; `Landed: ` 0 at both; `Gate: R` keys 30 then 31,
     DISTINCT at both; `Gate: R32` 0 then 1; `- R-0661 — ` 0 then 1;
     `- R-0662` 0 at both; the number of RECORD32 paragraphs beginning with the
     bytes `- R-`, which must be 1, which is constraint 4 measured;
     `^Recurrence: R-0629 — ` and `^Recurrence: R-0587 — ` each 0 then 1;
     `^Recurrence: ` 3 then 5; and `- R-0629 — ` and `- R-0587 — ` each exactly
     1 at BOTH commits, since the corrections name those findings and must not
     disturb their registrations.
 G6  THE RESOLUTION SET, at C4. Run the pin you just landed and, separately,
     report the measurement it makes: over every `.css` file under
     `apps/ui/src`, the set of `--remedy-*` custom properties USED in a
     `var(...)` minus the set DEFINED by a `--name:` declaration. At the round
     base that difference is EXACTLY these five — `--remedy-mono`,
     `--remedy-radius-pill`, `--remedy-warning-bg`, `--remedy-warning-border`
     and `--remedy-warning-fg` — and at C3 it is EXACTLY the four other than
     `--remedy-radius-pill`. Report both sets in full, sorted, as the values
     YOUR script printed. The four survivors are PRE-EXISTING, are registered
     by this round as part of R-0661 and are NOT fixed here: a repository-wide
     "every var resolves" gate is RED at the round base, and R-0364 forbids
     ordering a gate that was already red before the round began.
 G7  THE SUITES, at C4 in the PRIMARY checkout, SERIALLY, from the REPOSITORY
     ROOT unless a line below names another directory — a shell left elsewhere
     makes the Python suites exit 4 having run no test, which is vacuous and not
     green. Report each exit code, the working directory and each total,
     counting BY PASSED PLUS SKIPPED:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 488 at the round base,
       rising by exactly the number of test functions PINSLICE2 adds, a number
       YOU count from the committed slice rather than one I name. Report the
       base total, the C4 total and their difference.
       `npx tsc --noEmit` from `apps/ui` — exit 0, EMPTY output. Ordered because
       C3 touches a file the UI build reads, even though it adds no type.
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511, the gate that the
       `.agent/` state readers still parse what C1 and C2 wrote.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No vitest run is owed: the `Change:` list holds no path under `apps/ui/src`
     that vitest covers, and no docs gate is owed: it holds no `docs/` path.
 G8  THE PIN CAN FAIL. Prove it WITHOUT a worktree and WITHOUT touching a
     tracked file: run the pin's own measurement in a scratch copy under
     `.remedy-wt/`, made with `git show <sha>:<path>`, taking the tokens file at
     the ROUND BASE `8efdb7ea` — where `--remedy-radius-pill` is undefined — and
     report that the unresolved set computed from that base copy CONTAINS
     `--remedy-radius-pill` while the set computed at C3 does NOT. That is the
     same discriminator the pin asserts, evaluated at a commit where it is
     false, which is what makes the green at C4 mean something. Delete the
     scratch copy afterwards and report `git status --porcelain` as 0 lines.
 G9  RANGE, executed at C4 and covering the round base to C4 — NOT to C5,
     because C5 writes the file that must quote these gates and §3 checklist
     item 31 forbids ordering a reading the quoting artefact cannot hold.
     Report: the base-to-C4 path set against the six non-handoff paths of
     `Change:`, the difference EMPTY both ways; every commit single-parent;
     `git show --numstat` and `git diff --numstat` agreeing cell by cell with
     the handback's `## Commits` tables (§3 item 28), any disagreement reported
     rather than reconciled; every insertion count under the 500 cap;
     `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout
     ALONE, none having been created, which is constraint 8 measured; and
     `gh pr list --state open --json number,headRefName` — expected EMPTY — with
     the statement that neither `gh pr create` nor `gh pr merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED and scoped to the files a slice or pair
     LANDED IN — `.agent/plan.md`, `.agent/live_review.md`, the tokens file and
     the drift test — and covers EVERY marker prefix this block uses, which G2
     names and you count for yourself: each must read 0, as must any line
     starting `<<<`. The two block mirrors ARE the block and read nonzero by
     construction.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog --format=%gs`,
     take the OPERATION only — the text BEFORE the first `:` — and scope to THIS
     ROUND'S rows. Report that every such row's operation is `commit` and that
     `amend`, `rebase` and `cherry` each occur 0 times in that OPERATION field.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a through C5, the round base SHA, ONE LINE PER GATE with
            transcripts kept out of the file (R-0582), and the `Fortschritt:`
            line verbatim across all three of its lines. Report its own `wc -l`
            against the 60-line cap, with a DECISION D15 line declaring any
            overage and its mandated cause. Every `## Commits` heading carries
            that commit's FULL subject, and where a commit cannot name its own
            SHA the role and reason go INSIDE the heading (R-0494). `## Next`
            states that R32's own verdict is UNRECORDED and the next round's
            ledger commit owes it, together with C5's own insertion count and
            line count, which C5 cannot state about itself; that the four
            surviving unresolved custom properties are registered under R-0661
            and routed to the paydown branch, NOT to F021; and that R33 is T003
            — the row click-jump to the graph store and the disabled steering
            input with the tooltip naming F030 — after which F021 reaches its
            integration-gate round.

<<<SLICE PLANF021R32
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
R32 records R31, which PASSED, and pays for the one live defect it shipped: the
jump-to-live pill asked for `--remedy-radius-pill`, which the design reference
has always defined and the shipped stylesheet never adopted, so the property
resolved to nothing and the pill rendered square. This round defines the token,
pins the unresolved-custom-property set so it can never grow silently, and
registers the class as R-0661 — four OTHER properties were already unresolved
before F021 began. R31's two text defects are appended as corrections naming
open findings R-0629 and R-0587; neither mints an id.

## Next Steps
1. R33: T003 — the row click-jump to the graph store, then the disabled
   steering input with the tooltip naming F030.
2. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- Nothing in this repository renders CSS, so a custom property that resolves to
  nothing is invisible to every suite. R-0661's pin closes that for the SET but
  still cannot prove any rule's computed value.
- `npm run lint` is RED tree-wide at every commit: the eslint config has no
  TypeScript parser, so it reports a parsing error per file and is blind to
  style. That is R-0622, still open.
- This ledger carries two `- R-0618` lines under a LOOSE `- R-` reading and one
  under the canonical `^- R-\d+ — ` pattern. The canonical reading is the open
  set; R30's C2 says so on disk.
- No code defect of F021 is open once R-0661's own use is fixed; R-0364,
  R-0403, R-0587, R-0607 through R-0609, R-0611, R-0613, R-0618, R-0622,
  R-0629, R-0630, R-0644, R-0651, R-0653 through R-0659 and R-0661's four
  surviving properties stay routed to a paydown branch.
<<<END PLANF021R32

<<<SLICE RECORD32
Recurrence: R-0629 — A DESTRUCTIVE CONTROL ASSERTED THAT TWO UNIQUENESS READINGS AGREE, AND THEY CANNOT AGREE FOR AN INDENTED LINE. Second instance, in the reviewer's own F021 R31 block; NO NEW ID IS MINTED, because R-0629 already rules that a destructive control must MEASURE the uniqueness it asserts rather than declare it (§3 checklist item 30, and §3 item 25). THE INSTANCE: R31's G10, saved at `bd732c0b`, ordered the mutation target `if (shouldFollowNewest(distance) && boxRef.current) {` deleted from `ActivityFeedCard.tsx` and described it as "a string I measured to occur EXACTLY ONCE in that file at C5, whole-line and indent-agnostic counts agreeing". The bytes the block PRINTS carry no leading whitespace, and the line in the file is indented four spaces, so the WHOLE-LINE count of those bytes is 0 while the indent-agnostic count is 1: the two readings disagree by construction and the clause was unmeetable as written. Re-measured by the reviewer at `d1951b00`: whole-line 0, indent-agnostic 1, substring 1. WHAT IS UNHARMED, and why the round still stands: the target IS unique under both readings that can be nonzero, so the worker resolved it correctly, deleted the intended three lines, and the red control did what it was for — 58 green became 1 failed and 57 passed, naming `TestTheFeedScrollRuleIsWiredToTheCard::test_the_card_never_scrolls_without_asking_the_rule`. The reviewer reproduced that same red independently before delegating. The defect is the claim, not the control. WHERE MY OWN MEASUREMENT WENT WRONG, which is the part R-0629's fix clause does not carry: I DID run the count before emission, and I ran it over the INDENTED form while writing the UNINDENTED form into the block, so a real measurement certified a string it had never been taken over. ADDED TO R-0629'S FIX, binding the reviewer: the uniqueness count is taken over the EXACT byte string the block prints, extracted from the block's own text rather than retyped into the probe, and where indentation makes whole-line and indent-agnostic disagree the control says which reading it means instead of claiming both.

Recurrence: R-0587 — AN APPEND CONVENTION WAS CARRIED FROM ONE TARGET FILE TO ANOTHER WHOSE SEPARATOR CONVENTION IS DIFFERENT. Fourth instance, in the reviewer's own F021 R31 block; NO NEW ID IS MINTED, because R-0587's fix clause — added one round earlier, at `433daa59` — already rules that "a slice joining a repeating record format is compared against its neighbours for SEPARATOR as well as header" (§3 checklist item 30, and §3 item 26). THE INSTANCE: R31's constraint 5, saved at `bd732c0b`, fixed EVERY append in that block at one added newline and one resulting blank line, and applied that single convention to three different files. It is right for `.agent/live_review.md` and for `.agent/decisions.md`, whose entries are separated by one blank line. It is WRONG for `tests/ui_contracts/test_brain_stream_ring.py`, where PEP 8 E302 puts two blank lines before a top-level class: measured by the reviewer at `b9c7d726`, that file now holds 15 top-level classes, 14 with two blank lines above and exactly one — `TestTheFeedScrollRuleIsWiredToTheCard`, the class R31 appended — with one. THE WORKER APPLIED IT LITERALLY, as constraint 1 required, and declared it. NOTHING IS RED AND NOTHING IS REPAIRED HERE: `ruff check` is exit 0 over that file because E301 through E306 are preview-only rules this repository does not enable, so no gate sees it; the landed class is NOT re-indented or moved, because a corrective commit would edit a file to fix one blank line, and the record carries the correction instead. THIS ROUND IS THAT RULE APPLIED TO ITSELF: constraint 5 above states the convention PER TARGET FILE and gives `tests/ui_contracts/test_design_drift.py` two added newlines against `.agent/live_review.md`'s one. ADDED TO R-0587'S FIX, binding the reviewer: an append convention is stated per TARGET PATH and never once for a block, and where the target is source code the convention is the LANGUAGE's, measured against that file's existing members rather than inherited from the state files the same block also writes.

- R-0661 — Low, THE SHIPPED STYLESHEET USES FIVE CUSTOM PROPERTIES IT NEVER DEFINES, AND NOTHING IN THIS REPOSITORY CAN SEE IT. Raised by the reviewer while gating F021 R31, whose own CSS slice added the fifth. `apps/ui/src/styles/tokens.css` is the shipped token sheet and `docs/ui/design_reference/tokens.css` is the binding design authority; the second defines `--remedy-radius-pill: 999px` and the first has never adopted it, so R31's jump-to-live pill asked for a value that resolves to nothing and rendered with square corners. Measured by the reviewer at `8efdb7ea` by taking, over every `.css` file under `apps/ui/src`, the set of `--remedy-*` names used inside `var(...)` minus the set declared as `--name:`: the difference is exactly five — `--remedy-mono` in `PromptTracePanel.module.css`, `--remedy-radius-pill` in `RightLivePanel.module.css`, and `--remedy-warning-bg`, `--remedy-warning-border` and `--remedy-warning-fg` in `DegradedBanner.module.css`. FOUR OF THE FIVE PREDATE F021 ENTIRELY and are not this feature's to fix; only the pill is, and C3 of this round defines that token with the design reference's own value. WHY NOTHING CAUGHT IT: no test in this repository resolves a CSS variable, `npm run lint` is blind under R-0622, and a browser silently drops a declaration whose `var()` has no definition and no fallback — so the failure mode is a visual one in a repository with no renderer, which is the same blind spot the design-drift suite exists to narrow. THE COUNTER-MEASURE, landed at C4 rather than owed: `tests/ui_contracts/test_design_drift.py` pins the unresolved set as an explicit allowlist of the four survivors, so the set can shrink freely and cannot GROW without turning that suite red. It is an allowlist rather than an emptiness assertion because a repository-wide "every var resolves" gate is RED at this round's base and R-0364 forbids ordering a gate that was already red. THE FOUR SURVIVORS ROUTE TO THE PAYDOWN BRANCH: each needs a value decided against the design reference, which is a design question and not F021's scope. OPEN.

Gate: R32 — the R31 entry. R31 PASSED ON EVERY GATE WHOSE SUBJECT IS THE WORK, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND ALL THREE OF ITS DECLARED DEVIATIONS ARE THE REVIEWER'S OWN DEFECTS, RECORDED IN THE THREE ENTRIES ABOVE. R31 IS THE ROUND THAT MADE THE SCROLL RULE REACHABLE: `apps/ui/src/api/feedScroll.ts` had been pure, vitest-covered and IMPORTED BY NOTHING since R17, and at `d1951b00` `ActivityFeedCard.tsx` imports it and asks it before it scrolls. TRANSPORT HELD ACROSS ALL FOUR COPIES at sha256 517a68fabc2a291a6ceaf75deab36b032e0e2c98d20da974f94293c9fcba4abd over 37455 bytes and 480 lines: my own `.remedy-wt/f021-r31.md`, `.agent/authored/f021-r31.md` at `bd732c0b` and `.agent/last_block.md` at `834f53f5`, the last written FROM the committed C0a blob. SLICES: 4 whole texts and 3 pairs over 210 CONTENT lines, TOTAL 480 against DECISION F085 D6's 490 and PROSE 270 against D5's 400, both equal to that block's constraint 10. THE PLAN WRITE HELD: `.agent/plan.md` at `ff4c687f` is byte-equal to that block's plan slice plus one terminating newline and NOT to the bare slice, `wc -l` 47. BOTH APPENDS HELD UNDER BOTH READERS: at `433daa59` the ledger's base blob is a byte-exact prefix, the remainder is exactly one newline plus the slice plus one newline, units 277 to 279 ELEMENTWISE with RECORD31 measuring 2, one blank line at the join; at `c70a6e87` `.agent/decisions.md` behaves identically, units 1240 to 1242, and DECISION F021 D10 is the LAST `^## DECISION ` heading with one blank line above it. THE SETS DID NOT MOVE: canonical `^- R-\d+ — ` 223 all DISTINCT maximum R-0660 at base AND C2; loose `- R-` 224 at both with `R-0618` twice; `Done: R-` 1, `Landed: ` 0, `Gate: R` keys 29 then 30 DISTINCT, `Gate: R31` 0 then 1, `- R-0661` 0 at both. THE PAIRS BEHAVED BY THEIR MEASURED SHAPE: all three FROMs occurred exactly once at the round base and 0 after, every TO 0 then 1, the containment test having printed false for all three before emission. THE CARD IS WHAT D10 RULES: at `d1951b00` the comment-stripped source holds `recent.slice(-LIVE_ROWS_SHOWN).reverse()` 1, `recentDropped > 0` 1, `shouldFollowNewest` 2, `shouldShowNewRowsPill` 2, `nextFeedScroll` 3, `FEED_SCROLL_START` 3, `scrollTop` 3 and `from "../../api/feedScroll"` 1, and the raw file holds `No activity yet` 1, `@mui` 0 and `POST` 0 — every guard that already read this file still satisfied. THE SUITES ARE MY OWN, run SERIALLY in the PRIMARY checkout: `npx tsc --noEmit` exit 0 with output EMPTY; `npm run test:unit` 15 files and 212 tests, unchanged as a round adding no vitest case must be; `tests/ui_contracts/` 484 passed plus 4 skipped = 488 against 482 at the base, a difference of exactly 6, which is PINSLICE's six test functions; the three state-reading suites 511; the canary 42. THE RED CONTROL REPRODUCED IN MY OWN DISPOSABLE WORKTREE at `d63d29e8` before delegation: green at 58, then with the follow branch's three lines deleted exactly 1 failed and 57 passed, the failure being `TestTheFeedScrollRuleIsWiredToTheCard::test_the_card_never_scrolls_without_asking_the_rule`; the worktree was removed and pruned and `git worktree list` reads the primary checkout ALONE. THE RANGE HELD: nine commits base to C7, every one single-parent, the path set base-to-C6 EQUAL to the eight non-handoff `Change:` paths with both differences EMPTY, insertions 480, 409, 19, 4, 4, 16, 58 and 54 each under the 500 cap and each agreeing cell by cell with the handback's tables, `git ls-files .remedy-wt` 0, `gh pr list --state open` EMPTY, the marker sweep 0 line-anchored in all six files a slice or pair landed in, and the reflog read BY OPERATION every row `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE OWED READINGS, which R31's own handback could not hold about itself (§3 item 31): its C7 `8efdb7ea` is single-parent and touches `.agent/handoff.md` ALONE at 69 insertions and 42 deletions, under the 500 cap, and that handback measures 96 lines by `wc -l` — over the 60-line baseline and WITHIN the 100-line tier AGENTS.md grants a handback whose per-commit tables cover more than five commits, which this one's nine do. WHY R31 IS PASS DESPITE SHIPPING A DEFECT: every applied byte is reproducible from the committed block by my own extractor, the typecheck and all four suites are green, the new pins fail under the exact mutation they exist to catch, and the one defect that reached the product is a missing token DEFINITION that the round's own use made visible — the worker measured all three defects, declared them, and repaired none of them, which under constraint 1 is exactly right and is why they are recorded here rather than papered over.
<<<END RECORD32

<<<FROM TOKENPAIR
  --remedy-radius-sm: 10px;
<<<TO TOKENPAIR
  --remedy-radius-sm: 10px;
  /* The pill radius the design reference has always carried. Added at F021 R32
     because the shipped sheet had never adopted it, so every `var()` naming it
     resolved to nothing and the rule was silently dropped (R-0661). */
  --remedy-radius-pill: 999px;
<<<END TOKENPAIR

<<<SLICE PINSLICE2
class TestEveryCustomPropertyResolves:
    """R-0661. A `var(--x)` with no definition and no fallback makes a browser
    drop the whole declaration silently, and nothing in this repository renders
    CSS, so the failure is invisible to every other suite. F021 R31 shipped
    exactly that and the pill rendered square.

    This is an ALLOWLIST rather than an emptiness assertion on purpose: four
    properties were already unresolved before F021 began, each needing a value
    decided against the design reference, and R-0364 forbids ordering a gate
    that is red before the round that adds it. The set may shrink freely; it
    cannot grow without turning this red."""

    KNOWN_UNRESOLVED = {
        "--remedy-mono",
        "--remedy-warning-bg",
        "--remedy-warning-border",
        "--remedy-warning-fg",
    }

    def _unresolved(self):
        css_root = ROOT / "apps" / "ui" / "src"
        defined, used = set(), {}
        for path in sorted(css_root.rglob("*.css")):
            text = path.read_text(encoding="utf-8")
            defined.update(re.findall(r"(--remedy-[a-z0-9-]+)\s*:", text))
            for name in re.findall(r"var\(\s*(--remedy-[a-z0-9-]+)", text):
                used.setdefault(name, set()).add(path.name)
        return {name: files for name, files in used.items() if name not in defined}

    def test_the_unresolved_set_has_not_grown(self):
        unresolved = self._unresolved()
        new = set(unresolved) - self.KNOWN_UNRESOLVED
        assert not new, (
            "these custom properties are used but never defined under "
            f"apps/ui/src, so the declarations using them are dropped: "
            f"{ {name: sorted(unresolved[name]) for name in sorted(new)} }"
        )

    def test_the_pill_radius_is_defined(self):
        tokens = (ROOT / "apps" / "ui" / "src" / "styles" / "tokens.css").read_text()
        assert "--remedy-radius-pill:" in tokens, (
            "the jump-to-live pill (DECISION F021 D10) asks for this token; "
            "docs/ui/design_reference/tokens.css defines it as 999px"
        )
<<<END PINSLICE2
