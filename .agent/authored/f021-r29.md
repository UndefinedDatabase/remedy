── STEP T002/BADGE — F021 ──
Goal:        Rule the NowCard badge's liveness source, which R28 deliberately
             left open, and apply the ruling. DECISION F021 D9 chooses the
             CONJUNCTION — the badge lights only when the agent is running AND
             the recency rule says something happened recently — so the badge
             and the dot can never claim opposite things and "Live" can never
             appear beside the word "Idle". The round also records R28 and adds
             this session's second reviewer-gate defect to R-0618, which already
             holds that class OPEN.

Fortschritt: ~96 % (T002 — Punkt und Badge verdrahtet und geregelt; es fehlt nur
             noch der Feed-Scroll)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R28 verdict
             and the R-0618 recurrence · C3 the DECISION · C4 the badge · C5 the
             pins · C6 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r29.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/decisions.md` (C3) ·
             `apps/ui/src/components/panels/AgentNowCard.tsx` (C4) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C5) ·
             `.agent/handoff.md` (C6). Resolve any count in this block against
             that list.

Constraints:
 1. Apply every slice and pair half BYTE FOR BYTE. Never retype, rewrap, reflow,
    reindent or whitespace-adjust one. If a slice looks wrong, STOP and say so in
    the handback rather than fixing it. R28's worker did exactly that and was
    right to; the gate was wrong and the slice was not.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and is not negotiable. C1
    precedes the ledger commit because the plan must be current before it (§3
    checklist item 23). THE DECISION LANDS BEFORE THE CODE IT RULES: C3 records
    why the badge changes, C4 changes it, C5 moves the pins that named the old
    rule. PLANF021R29 describes the state this round ENDS in, so it reads
    forward to commits this constraint fixes (§3 item 20, the R-0524 carve-out).
    ROUND BASE is `baf079b1` — resolve its full form with `git rev-parse`.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. Before it: 223 registered,
    maximum R-0660, `Done: R-` 1. After C2 all three are UNCHANGED. The R28 gate
    defect is a RECURRENCE of R-0618, which is open and already describes it
    exactly, so §3 checklist item 30 forbids a second id: the evidence is
    appended as a paragraph NAMING R-0618, and the `- R-` set does not grow.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice and pair half is quoted
    WITHOUT a trailing newline. A WHOLE-FILE write (PLANF021R29) is the slice
    PLUS one terminator. A LEDGER append (RECORD29 at C2) is ONE newline, then
    the slice, then one terminator. A PROSE-RECORD append (DECISION9 at C3) is
    TWO newlines — the blank line that separates entries in that file — then the
    slice, then one terminator. A PAIR is applied by replacing the FROM bytes
    with the TO bytes in place, adding no newline of its own.
 5. PAIR SHAPES, MEASURED NOT ASSERTED (§3 item 15). The reviewer ran the
    containment test on every pair and it printed `TO contains FROM: false` for
    BADGEIMPORT, `TO contains FROM: false` for BADGELEVEL, `TO contains FROM:
    false` for BADGEJSX, `TO contains FROM: false` for PINBADGE and `TO contains
    FROM: false` for PINDOTDOC. ALL FIVE ARE THEREFORE REWRITES and each carries
    the §4.9 FROM-zero reading. Each FROM was measured at exactly 1 occurrence in
    its target at the round base.
 6. APPLY THE PAIRS IN THE ORDER LISTED, and re-check uniqueness before each: a
    FROM must occur exactly 1 time in its target at the moment IT is applied, not
    merely at the round base. BADGELEVEL's TO introduces the token `isRunning &&`
    into the file, so BADGEJSX's FROM is quoted as its WHOLE line to stay unique
    after BADGELEVEL has landed. If any FROM does not read exactly 1 when you
    reach it, STOP and report.
 7. ONE FILE, ONE PROPERTY, ONE COMMIT (R-0657). C2 gives `.agent/live_review.md`
    ONE append and nothing else. C3 gives `.agent/decisions.md` ONE append. C4
    gives the card its pairs and nothing else. C5 gives the contract file its
    own pairs and nothing else.
 8. THE LEDGER AND THE DECISION FILE ARE APPEND-ONLY. No landed paragraph in
    either is edited — R-0618's own paragraph is NOT rewritten, and the
    recurrence is a NEW paragraph that names it (R-0470).
 9. NO COUNT GATE IN THIS BLOCK COUNTS A BARE SUBSTRING WHOSE NUMBER THIS
    BLOCK'S OWN SLICES CHANGE. That is the R-0618 defect this round records, and
    repeating it in the round that records it would be the third instance. Every
    count below is either LINE-ANCHORED, or scoped to a file no slice of this
    block writes, or ordered as "report the number YOU measure". Where a numeral
    appears it is a property of the TARGET, never of this block's prose.
10. THE CARD'S OTHER GUARDS SURVIVE. After C4 the COMMENT-STRIPPED card must
    still contain `newestActionRow`, `recent ?? []`,
    `liveAction ? liveAction.line : detail`, `recencyLevel(`,
    `data-recency={level}` and `setInterval`, and must still NOT contain
    `isActive`; the RAW card must still not contain `Builder is working` or
    `@mui`. `apps/ui/src/components/panels/RightLivePanel.tsx` is NOT touched by
    this round. G8 measures this rather than trusting it.
11. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide at every commit under R-0622 and is NOT a gate of this round —
    do not run it and do not report it. Create and merge NO pull request. Push
    the branch after C6. ONE disposable worktree is created for G11 and removed
    and pruned before C6; it runs PYTHON only, never vitest, so it needs no
    `node_modules` (R-0518).
12. Block size, measured on these final bytes AFTER the last edit: TOTAL 414
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice and
    pair CONTENT lines — 277 against DECISION F085 D5's 400. Markers count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C6; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2, C3, C4 and C5. C6's own
     reading is ordered NOWHERE — §3 item 31 leaves it to the next session.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r29.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r29.md` are all equal. Write
     C0b FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their marker LINES —
     `<<<SLICE `/`<<<END ` for the whole texts and `<<<PAIR `/`<<<FROM`/`<<<TO`/
     `<<<ENDPAIR` for the pairs. Report how many whole texts, how many pairs and
     how many CONTENT lines that extractor printed, each as a number YOU
     measured and never as one this block predicts, and re-measure constraint
     12's two numerals from that same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R29 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare slice
     that must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1. THE LINE-COUNT CLAUSE IS MEASURED:
     the reviewer counted PLANF021R29 at 47 lines, so `wc -l` must read EXACTLY
     47, satisfying AGENTS.md's "keep it short (<50 lines)". If the count you
     measure differs, STOP and report — do NOT trim the file to reach it, which
     is the error R-0654 records.
 G5  THE TWO PROSE APPENDS, each under TWO INDEPENDENT READERS: RECORD29 into
     `.agent/live_review.md` at C2, and DECISION9 into `.agent/decisions.md` at
     C3. Read each base blob with `git show <sha>:<path>` into memory or scratch
     under `.remedy-wt/`; never overwrite a tracked file to read an older
     revision. Reader (a): the earlier blob is a byte-exact PREFIX of the later
     file, and the remainder is EXACTLY the separator constraint 4 gives that
     slice's kind, plus the slice, plus one newline — report each remainder's
     sha256, byte and line counts, and the file's counts before and after.
     Reader (b), SET-WISE: strip the one trailing terminator from BOTH blobs,
     split each on the blank line into units, and confirm the later unit LIST
     equals the earlier list followed by that slice's own units, ELEMENTWISE
     over the whole list, not at the tail; report N at each point and each
     slice's unit count as the number YOU measured. NEGATIVE CONTROL, once, on
     the C3 file: alter one printable byte of its FIRST paragraph at equal
     length; BOTH readers must REJECT it and ACCEPT the true file. Name the
     offset and the change. Report that neither diff deletes a line.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base and at C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R`
     keys and how many DISTINCT; `Gate: R29`; the MAXIMUM registered id. So
     `- R-` reads 223 at BOTH points, all DISTINCT at both; the maximum R-0660
     at BOTH; `Done: R-` 1 at BOTH; `Landed: ` 0 at BOTH; `Gate: R` keys 27 then
     28, DISTINCT at both; `Gate: R29` 0 then 1. Report also, over the C2 blob,
     the line-anchored count of `- R-0661`, which must be 0: constraint 3 forbids
     the next id from being minted, and this is that constraint measured.
 G7  THE DECISION IS REACHABLE BY ITS OWN KEY, at C3, in `.agent/decisions.md`:
     report the line-anchored count of `^## DECISION F021 D9 ` — which must be 1
     — and of `^## DECISION F021 D` overall, and confirm that the D9 heading is
     the LAST such heading in the file. Report also that `D9` does not already
     appear as a heading at the round base, by the same line-anchored count
     reading 0 there.
 G8  THE CARD at C4. For EACH of BADGEIMPORT, BADGELEVEL and BADGEJSX report, in
     `apps/ui/src/components/panels/AgentNowCard.tsx`, FROM 1 at the round base
     and 0 at C4, TO 0 at the round base and 1 at C4. THEN MEASURE CONSTRAINT 10
     RATHER THAN TRUSTING IT, at C4: in the COMMENT-STRIPPED card — strip with
     the suite's own `strip_ts_comments`, not by eye — `newestActionRow`,
     `recent ?? []`, `liveAction ? liveAction.line : detail`, `recencyLevel(`,
     `data-recency={level}`, `setInterval` and `isRunning && isLiveByRecency(`
     each occur at least once, while `isActive` occurs 0 times; in the RAW card,
     `Builder is working` and `@mui` each occur 0 times. Report each count. In
     `apps/ui/src/components/panels/RightLivePanel.tsx`, report that the file is
     absent from this round's path set entirely.
 G9  THE PINS at C5. For EACH of PINBADGE and PINDOTDOC report, in
     `tests/ui_contracts/test_brain_stream_ring.py`, FROM 1 at the round base and
     0 at C5, TO 0 at the round base and 1 at C5. Report the file's line count
     before and after, and how many lines that commit's diff DELETES, which is
     not zero here — this commit REPLACES pin text and does not append, and a
     diff deleting 0 lines would mean a pair did not land.
G10  TYPECHECK, UNIT TESTS AND THE PYTHON SUITES, all at C5, in the PRIMARY
     checkout, run SERIALLY and never two at once. From `apps/ui`:
     `npx tsc --noEmit` must exit 0 with EMPTY output, and `npm run test:unit`
     must exit 0 — report the file and test totals it prints, which the reviewer
     read at 15 files and 212 tests at the round base and which this round adds
     no vitest case to. From the REPOSITORY ROOT — a shell left elsewhere makes
     these exit 4 having run no test, which is vacuous and not green — report
     each exit code, the working directory and the total, counting BY PASSED
     PLUS SKIPPED:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — the reviewer read 482 at
       the round base and this round REPLACES pin text without adding or
       removing a case, so report the total you measure and state whether it is
       unchanged; any movement is a finding, not something to accept.
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511, the gate that C1,
       C2 and C3 did not break the `.agent/` state readers.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/` path.
G11  THE RED CONTROL for the pin this round rewrites, because a pin that is
     edited rather than added has never been seen fail in its NEW form. Run it
     ONLY inside a disposable `git worktree` added at C5 under `.remedy-wt/`,
     never in the primary checkout (guardrail G5). In that worktree, and in the
     file `apps/ui/src/components/panels/AgentNowCard.tsx` alone, replace the
     single occurrence of the text isRunning && isLiveByRecency(level) with the
     text isLiveByRecency(level) — COUNT THE TARGET FIRST in that file,
     whole-line-containing and indent-agnostic, both readings agreeing at 1, and
     report both numbers (§3 item 25). That mutation is exactly the rejected
     option (a) of DECISION F021 D9, so the pin must reject it. Then run
     `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf` in
     that worktree and report the exit code and the NAMES of the failing tests,
     which must be non-empty. Restore nothing: remove and prune the worktree
     instead, and report `git worktree list` as the primary checkout ALONE
     afterwards. If the run is GREEN, the pin does not bind the ruling — STOP
     and report that, do not repair it.
G12  RANGE, executed at C5 and covering the round base to C5 — NOT to C6,
     because C6 writes the file that must quote these gates and §3 checklist
     item 31 forbids ordering a reading the quoting artefact cannot hold.
     Report: the base-to-C5 path set against the seven non-handoff paths of
     `Change:`, the difference EMPTY both ways; every commit single-parent;
     `git show --numstat` and `git diff --numstat` agreeing cell by cell with
     the handback's `## Commits` tables (§3 item 28), any disagreement reported
     rather than reconciled; every insertion count under the 500 cap;
     `git ls-files .remedy-wt` 0; and `gh pr list --state open --json
     number,headRefName` — expected EMPTY — with the statement that neither `gh
     pr create` nor `gh pr merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED and scoped to the files a slice or pair
     LANDED IN — `.agent/plan.md`, `.agent/live_review.md`,
     `.agent/decisions.md`, `apps/ui/src/components/panels/AgentNowCard.tsx` and
     `tests/ui_contracts/test_brain_stream_ring.py` — and covers EVERY marker
     prefix this block uses, which G3 names and you count for yourself: each
     must read 0, as must any line starting `<<<`. The two block mirrors ARE the
     block and read nonzero by construction.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog --format=%gs`,
     take the OPERATION only — the text BEFORE the first `:` — and scope to THIS
     ROUND'S rows. Report that every such row's operation is `commit` and that
     `amend`, `rebase` and `cherry` each occur 0 times in that OPERATION field.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a, C0b, C1, C2, C3, C4, C5 and C6, the round base SHA, ONE
            LINE PER GATE with transcripts kept out of the file (R-0582), and
            the `Fortschritt:` line verbatim across all three of its lines.
            Report its own `wc -l` against the 60-line cap, with a DECISION D15
            line declaring any overage and its mandated cause; where the count
            also passes the 100-line tier AGENTS.md grants for more than five
            commit tables, name BOTH bounds. Every `## Commits` heading carries
            that commit's FULL subject, and where a commit cannot name its own
            SHA the role and reason go INSIDE the heading (R-0494). `## Next`
            states that THIS SESSION IS OVER; that the NEXT session begins at
            docs/agents/self_drive_protocol.md Phase 1 rule 1 — the
            `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347); that
            R29's own verdict is UNRECORDED and the next round's ledger commit
            owes it, together with C6's own insertion count and line count,
            which C6 cannot state about itself; and that R30 wires
            `feedScroll.ts` into the feed's scroll container with the new-rows
            pill component_spec.md line 86 binds, the last rule this feature has
            built headless and left unread.

<<<SLICE PLANF021R29
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
R29 rules the NowCard badge's liveness source, the question R28 left open, and
applies the ruling. DECISION F021 D9 chooses the conjunction: the badge lights
only when the agent is RUNNING and the recency rule also reads live, so the
badge and the dot can never claim opposite things and "Live" can never render
beside the word "Idle". The round also records R28 and adds its own gate defect
to R-0618 rather than minting a second id for a class already open.

## Next Steps
1. R30: `feedScroll.ts` into the feed's scroll container with the new-rows pill
   component_spec.md line 86 binds. Headless since R17 and the last rule this
   feature has built and left unread.
2. R31: the row click-jump to the graph store, then T003's disabled steering
   input with the tooltip naming F030.
3. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round in this chain.
- The dot's fade is driven by an interval the card owns. No headless test can
  reach a React hook here, so its guard is the source contract plus the purity
  of `recency.ts`, which vitest does cover.
- `npm run lint` is RED tree-wide at every commit: the eslint config has no
  TypeScript parser, so it reports a parsing error per file and is blind to
  style. That is R-0622, still open.
- A worktree lacks `apps/ui/dist/`, so `tests/ui_contracts/` skips one more case
  there than in the primary checkout. COUNT BY PASSED PLUS SKIPPED.
- No code defect of F021 is open; R-0364, R-0403, R-0607 through R-0609,
  R-0611, R-0613, R-0618, R-0622, R-0651 and R-0653 through R-0659 stay routed
  to a paydown branch.
<<<END PLANF021R29

<<<SLICE RECORD29
- R-0618 RECURRED, third instance, in the reviewer's own F021 R28 block; NO NEW ID IS MINTED, because §3 checklist item 30 rules that an open finding already describing a defect takes the evidence rather than a second id, and R-0618 describes this one exactly: "A GATE ORDERED A STRING TO OCCUR EXACTLY ONCE IN A FILE WHILE THE SAME BLOCK'S OWN TO SLICE WROTE IT TWICE, SO THE COUNT WAS FALSE FOR EVERY POSSIBLE ROUND." THE INSTANCE: R28's G7, saved at `ae150fac`, ordered that `--remedy-live` occur "exactly 1 time" in `apps/ui/src/styles/tokens.css` at C3. It occurs TWICE, because that block's own TOKENSLIVE TO half names the token in its explanatory comment — "…the live-activity dot, 8px, --remedy-live," — beside the declaration it adds. Re-measured by the reviewer at `9cf01f6d`: the raw substring occurs 2 times at C3 and 0 at the round base, while the LINE-ANCHORED declaration reading `^\s*--remedy-live:` occurs exactly 1 — and the anchored reading is the one the round's own DOTCONTRACT asserts, through `"--remedy-live:" in tokens`, so nothing on disk is wrong and no gate protecting the tree was weakened. The R28 worker applied TOKENSLIVE byte for byte as constraint 1 required, measured 2, reported BOTH readings and declared the disagreement rather than deleting a comment to make the reviewer's arithmetic come true — the same behaviour that turned R-0618's first instance into a registration instead of a corrupted slice, and the behaviour this workflow depends on. WHAT IS NEW, and what R-0618's fix clause did not carry: both earlier instances were gates over a file the block wrote CODE into, and this one is a gate over a DESIGN TOKEN file where the token's own name is the natural subject of the comment that documents it — so the collision is not incidental but structural, and any block adding a documented token will meet it. ADDED TO R-0618'S FIX, binding the reviewer: a count gate names its ANCHOR in the gate text — `^\s*--remedy-live:` and never `--remedy-live` — whenever the counted token is a declared NAME, because a declaration's name recurs in the prose that explains it by construction. R-0424's standing rule already requires counting the string in the BLOCK's own slices before ordering a count; this instance shows that rule is not enough on its own, since the reviewer must also have chosen a reading the block's prose cannot move, and the anchor is that reading.

Gate: R29 — the R28 entry. R28 PASSED ON EVERY ONE OF ITS TWELVE GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, WITH THE SINGLE PREDICTED NUMERAL THE ENTRY ABOVE RECORDS. R28 IS THE ACTIVITY-DOT ROUND: `AgentNowCard` now ticks a clock of its own once a second, subtracts the newest ACTION row's `receivedAtMs` from it through `recencyLevel`, and renders the resulting level as `data-recency` on a plain 8px dot, with `--remedy-live` and `--remedy-dur-pulse` transcribed into the app's token file from `docs/ui/design_reference/tokens.css` so assets_spec.md line 178 finally names tokens that resolve — both values verified BYTE EQUAL against that reference at `9cf01f6d` rather than against the block's prose. THE BADGE WAS DELIBERATELY NOT RE-KEYED, and the reviewer's own dry run is why: applying the block's first draft turned `TestTheNowCardBadgeTracksTheAgent::test_the_badge_reads_the_running_flag` RED, which surfaced that feeding the badge from `isLiveByRecency` alone would light it for the whole quiet window after a job ends — R-0652 with a fuse rather than a latch — so the round shipped the dot alone and DECISION F021 D9 rules the badge one round later. TRANSPORT HELD ACROSS ALL FOUR COPIES at sha256 3289c55b7eb3bb1e3fd8cf9a41aac032f3da502d5db341541fffd5be783473e0 over 32905 bytes and 471 lines: the reviewer's own `.remedy-wt/f021-r28.md`, `.agent/authored/f021-r28.md` at `ae150fac` and `.agent/last_block.md` at `190776e5`, the last written FROM the committed C0a blob. SLICES: the reviewer's extractor read the whole texts PLANF021R28, RECORD28, NOWCARDTSX and DOTCONTRACT and the pairs TOKENSLIVE and DOTCSS over 203 CONTENT lines from that committed blob, with 0 stray `<<<` lines, TOTAL 471 against DECISION F085 D6's 490 and PROSE 268 against D5's 400 — both equal to that block's constraint 11. THE PLAN WRITE HELD: `.agent/plan.md` at `3705462a` is byte-equal to PLANF021R29's predecessor PLANF021R28 plus one terminating newline and NOT to the bare slice, `wc -l` exactly 48, `^## Goal$` and `^## Next Steps$` once each. THE LEDGER APPEND HELD UNDER BOTH READERS: remainder sha256 4225a477ec7a438dbfbd702634fcc9a9a2d5afe5127114a9deec612674c2af87 over 4715 bytes and 2 lines, the file 581080 B / 1180 L before and 585795 B / 1182 L after, units 271 to 272 ELEMENTWISE equal with RECORD28 exactly 1 unit, and a negative control at offset 4 of the FIRST paragraph REJECTED by both readers while both ACCEPTED the true file. THE SETS MOVED AS A ROUND MINTING NOTHING MUST: `- R-` 223 at BOTH points all DISTINCT, maximum R-0660 at BOTH, `Done: R-` 1 at BOTH, `Landed: ` 0 at BOTH, `Gate: R` keys 26 to 27 both DISTINCT, `Gate: R28` 0 to 1. BOTH PAIRS BEHAVED BY THEIR MEASURED SHAPE: each FROM 1 at the round base and 0 at `9cf01f6d`, each TO 0 then 1, the containment test having printed false for both before emission. THE CARD IS REPRODUCIBLE FROM THE BLOCK: `apps/ui/src/components/panels/AgentNowCard.tsx` at `253aad56` equals NOWCARDTSX plus one terminating newline and NOT the bare slice, and every guard the block promised to preserve was re-measured on the comment-stripped source — `newestActionRow` 2, `recent ?? []` 1, `liveAction ? liveAction.line : detail` 1, `{isRunning && <span` 1, `recencyLevel` 2, `isActive` 0 and `isLiveByRecency` 0, with `Builder is working` and `@mui` both 0 in the raw file and the panel's `<AgentNowCard dashboard={dashboard} recent={recent} />` line still exactly 1 in a file this round never touched. THE CONTRACT APPEND HELD AS ORDERED EQUALITY: the `253aad56` blob is a byte-exact PREFIX of the `05beb725` file, remainder sha256 a6ba8be591368206e844852201f3640ef20944b7c18b46b98b9a70bf111f5a31 over 2695 bytes and 58 lines, the file 428 to 486 lines, 0 deletions, and the 58 added lines are the two-newline separator plus the slice's lines ELEMENTWISE and IN ORDER. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY in the PRIMARY checkout: `npx tsc --noEmit` exit 0 with output EMPTY; `npm run test:unit` 15 files and 212 tests, unchanged as a round adding no vitest case must be; `tests/ui_contracts/` 478 passed plus 4 skipped = 482, the base's 476 plus DOTCONTRACT's 6; the three state-reading suites 511; the canary 42. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `baf079b1`: green first at 52 passed, then with the attribute text `data-recency={level}` deleted — a target the reviewer confirmed occurs EXACTLY ONCE, whole-line and indent-agnostic counts agreeing — exactly 1 failed and 51 passed, the failure being `TestTheActivityDotReadsTheRecencyRule::test_the_level_reaches_the_dom_as_data`, and the worktree was removed and pruned. THE RANGE HELD: eight commits base to C6, every one single-parent, the path set base-to-C5 EQUAL to the eight non-handoff `Change:` paths with both differences EMPTY, insertions 471, 400, 23, 2, 24, 30, 58 and 67 each under the 500 cap and each agreeing cell by cell with the handback's tables, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout ALONE, `gh pr list --state open` EMPTY, the marker sweep 0 line-anchored over all six prefixes in each of the six files a slice or pair landed in, and the reflog read BY OPERATION every row `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE OWED READINGS, which R28's own handback could not hold about itself (§3 item 31): its C6 `baf079b1` is single-parent and touches `.agent/handoff.md` ALONE at 67 insertions and 63 deletions, under the 500 cap, and that handback measures 91 lines by `wc -l` — over the 60-line baseline and WITHIN the 100-line tier AGENTS.md grants a handback whose per-commit tables cover more than five commits, which this one's eight do, declared with its mandated cause and no section dropped. WHY R28 IS PASS: every applied byte is reproducible from the committed block by the reviewer's own extractor, the ledger and contract remainders both matched digests the reviewer computed independently, the new contract fails under two separate mutations and recovers on restore, and the round's only disagreement was a defect in the reviewer's gate arithmetic that the worker measured, reported both ways and refused to paper over.
<<<END RECORD29

<<<SLICE DECISION9
## DECISION F021 D9 (2026-08-22) — the NowCard badge lights on RUNNING AND RECENT, never on either alone

CONTEXT, measured by the reviewer at `baf079b1`. `recency.ts` exports `isLiveByRecency`, whose own comment calls it "the single source R21 gives BOTH the badge and the dot", and until now nothing read it: R28 wired the DOT to `recencyLevel` and left the badge on `deriveAgentStatus`'s `isRunning`. The two candidate sources disagree in opposite directions, and each disagreement is visible on the same card. `isLiveByRecency` is true for `fresh` and `fading`, so it stays true for `QUIET_WINDOW_MS` — 30 seconds — after the last ACTION row arrived, INCLUDING after the job has ended; `deriveAgentStatus` returns `status: "Working"` if and only if `dashboard.live.running === true`, and "Idle" otherwise. So a badge fed by recency alone renders "Live" beside the word "Idle" for up to 30 seconds after every run — the exact rendering R-0652 was raised for, with a fuse instead of a latch — while a badge fed by `isRunning` alone renders "Live" beside a dot that has faded to idle whenever a running job has been quiet for 30 seconds.

CHOSEN: the CONJUNCTION. The badge lights only when `isRunning` AND `isLiveByRecency(level)`, so it can never contradict either the status word beside it or the dot below it. Because `deriveAgentStatus` returns "Working" on exactly the condition that makes `isRunning` true, the badge is now structurally incapable of appearing next to "Idle", "Blocked" or "Needs your decision" — the R-0652 guarantee is enforced by the conjunction rather than by a comment. The dot keeps reading the recency level ALONE and is unchanged: it answers "how long since the agent last did something", which stays a true and useful answer after a job ends, and it is the surface where the quiet window belongs.

ALTERNATIVES CONSIDERED. Recency alone: rejected, it reintroduces R-0652's rendering for 30 seconds after every run, and R28's reviewer dry run turned the existing pin red on exactly that change, which is how this question was found rather than shipped. `isRunning` alone, the status quo: rejected, it lets the badge claim life while the dot beside it has faded, so the card contradicts itself in the other direction and `isLiveByRecency` stays dead code the design reference calls load-bearing. Widening `QUIET_WINDOW_MS` or adding a job-ended reset to `recency.ts`: rejected, both push a UI concern into a pure rule whose whole value is that it is a function of two numbers, and neither removes the contradiction — they only shorten it.

REVERSE IT by restoring `{isRunning && <span` in `AgentNowCard.tsx` and the pin that names it in `tests/ui_contracts/test_brain_stream_ring.py`. The dot, the tokens, the CSS and `recency.ts` are untouched by this decision and by its reversal.
<<<END DECISION9

<<<PAIR BADGEIMPORT apps/ui/src/components/panels/AgentNowCard.tsx
<<<FROM
import { recencyLevel } from "../../api/recency";
<<<TO
import { recencyLevel, isLiveByRecency } from "../../api/recency";
<<<ENDPAIR

<<<PAIR BADGELEVEL apps/ui/src/components/panels/AgentNowCard.tsx
<<<FROM
  // Both instants subtracted here sit on ONE clock: `receivedAtMs` is the
  // arrival stamp the host took from this same `Date.now`, never the envelope's
  // server-clock string, which a server running behind would render as a dead
  // agent. Remedy deliberately does NOT feed the badge from this level yet: the
  // dot may say "acted 20s ago" while the job has ended, and a badge saying
  // "Live" beside the word "Idle" is the R-0652 defect. The badge keeps the
  // agent's own running flag until that trade-off is ruled on its own.
  const level = recencyLevel(liveAction ? liveAction.receivedAtMs : null, nowMs);
<<<TO
  // Both instants subtracted here sit on ONE clock: `receivedAtMs` is the
  // arrival stamp the host took from this same `Date.now`, never the envelope's
  // server-clock string, which a server running behind would render as a dead
  // agent.
  const level = recencyLevel(liveAction ? liveAction.receivedAtMs : null, nowMs);
  // DECISION F021 D9: RUNNING AND RECENT, never either alone. Recency alone
  // stays true for the whole quiet window after a job ends, which renders
  // "Live" beside the word "Idle" -- R-0652 with a fuse instead of a latch.
  // `isRunning` alone claims life while the dot below has already faded. The
  // conjunction cannot contradict either the status word or the dot, and
  // `deriveAgentStatus` says "Working" on exactly the condition that makes
  // `isRunning` true, so the badge structurally cannot sit beside "Idle".
  const isLive = isRunning && isLiveByRecency(level);
<<<ENDPAIR

<<<PAIR BADGEJSX apps/ui/src/components/panels/AgentNowCard.tsx
<<<FROM
        {isRunning && <span className={styles.liveSmall}><span /> Live</span>}
<<<TO
        {isLive && <span className={styles.liveSmall}><span /> Live</span>}
<<<ENDPAIR

<<<PAIR PINBADGE tests/ui_contracts/test_brain_stream_ring.py
<<<FROM
class TestTheNowCardBadgeTracksTheAgent:
    """R-0652. The card's live badge must key on the agent's own running flag
    and never on the stream ring: brainStream.ts only appends to `recent` and
    trims it, so a row outlives the job that produced it and a ring-keyed badge
    reads "Live" beside the word "Idle" forever."""

    def test_the_badge_is_not_keyed_to_the_ring(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "isActive" not in code, (
            "a badge keyed to the ring latches on once any action has arrived"
        )

    def test_the_badge_reads_the_running_flag(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "{isRunning && <span" in code, (
            "the live badge must track the agent, not the presence of a row"
        )
<<<TO
class TestTheNowCardBadgeTracksTheAgent:
    """R-0652 and DECISION F021 D9. The card's live badge must key on the
    agent's own running flag AND on the recency rule, never on the stream ring
    and never on either source alone: brainStream.ts only appends to `recent`
    and trims it, so a row outlives the job that produced it and a ring-keyed
    badge reads "Live" beside the word "Idle" forever, while recency alone
    reads live for the whole quiet window after a job has ended and renders the
    same words with a fuse instead of a latch."""

    def test_the_badge_is_not_keyed_to_the_ring(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "isActive" not in code, (
            "a badge keyed to the ring latches on once any action has arrived"
        )

    def test_the_badge_needs_running_and_recent_together(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "isRunning && isLiveByRecency(" in code, (
            "recency alone puts Live beside Idle for the whole quiet window"
        )
        assert "{isLive && <span" in code, (
            "the badge must render the conjunction, not one of its halves"
        )
<<<ENDPAIR

<<<PAIR PINDOTDOC tests/ui_contracts/test_brain_stream_ring.py
<<<FROM
    Both must sit on ONE clock -- the row's arrival stamp and a `Date.now` the
    card reads itself. The BADGE is deliberately not wired to this level yet:
    the dot may read fresh for the quiet window after a job has ended, and a
    badge saying "Live" beside the word "Idle" is exactly R-0652. That trade-off
    is ruled in its own round, and TestTheNowCardBadgeTracksTheAgent above still
    pins the badge to the agent's running flag until then."""
<<<TO
    Both must sit on ONE clock -- the row's arrival stamp and a `Date.now` the
    card reads itself. The DOT reads the recency level ALONE and answers how
    long since the agent last acted, which stays true after a job ends. The
    BADGE is the conjunction DECISION F021 D9 rules, pinned by
    TestTheNowCardBadgeTracksTheAgent above: recency alone would read live for
    the whole quiet window after a job ends, which is R-0652's rendering with a
    fuse instead of a latch."""
<<<ENDPAIR
