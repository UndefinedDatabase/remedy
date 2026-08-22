── STEP T002/DOT — F021 ──
Goal:        Give the NowCard the activity dot T5_F021 line 62 asks for, driven
             by the pure rule `recency.ts` has held unread since R21. The card
             subtracts the newest ACTION row's `receivedAtMs` from a clock it
             ticks itself and renders the level as a data attribute the CSS
             selects on. The CSS is transcribed from the binding design
             reference, tokens included. THE BADGE IS NOT RE-KEYED — see
             constraint 8, which is a scope line and not an oversight.

Fortschritt: ~95 % (T002 — Uhr, Ring und NowCard-Punkt verdrahtet; es fehlt nur
             noch der Feed-Scroll)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R27 verdict
             · C3 tokens and dot CSS · C4 the card · C5 the source contract ·
             C6 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r28.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/styles/tokens.css` (C3) ·
             `apps/ui/src/components/panels/RightLivePanel.module.css` (C3) ·
             `apps/ui/src/components/panels/AgentNowCard.tsx` (C4) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C5) ·
             `.agent/handoff.md` (C6). Resolve any count in this block against
             that list.

Constraints:
 1. Apply every slice and pair half BYTE FOR BYTE. Never retype, rewrap, reflow,
    reindent or whitespace-adjust one. If a slice looks wrong, STOP and say so in
    the handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and is not negotiable. C1
    precedes the ledger commit because the plan must be current before it (§3
    checklist item 23). CSS PRECEDES THE CARD so the classes the card names
    already exist, and THE CONTRACT FOLLOWS THE CARD because a contract landing
    first would be red at its own commit. PLANF021R28 describes the state this
    round ENDS in, so it reads forward to commits this constraint fixes (§3 item
    20, the R-0524 carve-out). ROUND BASE is `2b8830ac` — resolve its full form
    with `git rev-parse`.
 3. THIS ROUND REGISTERS NOTHING AND RESOLVES NOTHING. Before it: 223
    registered, maximum R-0660, `Done: R-` 1. After C2 those three are
    UNCHANGED; only the `Gate:` series grows. R27 PASSED, so there is no finding
    to mint, and a round that mints one anyway is registering a defect it has
    not found.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice and pair half is quoted
    WITHOUT a trailing newline. A WHOLE-FILE write (PLANF021R28, NOWCARDTSX) is
    the slice PLUS one terminator. A LEDGER append (RECORD28 at C2) is ONE
    newline, then the slice, then one terminator. A CODE append (DOTCONTRACT at
    C5) is TWO newlines — the blank line PEP 8 puts between top-level
    definitions — then the slice, then one terminator. A PAIR is applied by
    replacing the FROM bytes with the TO bytes in place, adding no newline.
 5. PAIR SHAPES, MEASURED NOT ASSERTED (§3 item 15). The reviewer ran the
    containment test on each pair and it printed `TO contains FROM: false` for
    TOKENSLIVE and `TO contains FROM: false` for DOTCSS. BOTH ARE THEREFORE
    REWRITES and both carry the §4.9 FROM-zero reading. Each FROM was measured
    at exactly 1 occurrence in its target at the round base. Both FROMs SPAN TO
    THE END OF THEIR RUN — across the blank line into the next block — which is
    the R-0660 counter-measure: an insertion after an anchor is read against
    what FOLLOWS that anchor, never against the anchor's uniqueness alone.
 6. ONE FILE, ONE PROPERTY, ONE COMMIT (R-0657). C2 gives `.agent/live_review.md`
    ONE append and nothing else. C5 gives the contract file ONE append. C4 gives
    the card its whole-file write alone.
 7. THE LEDGER IS APPEND-ONLY. No landed paragraph is edited.
 8. THE CARD'S EXISTING GUARDS SURVIVE, AND THE BADGE IS NOT TOUCHED. Assertions
    already on disk read `AgentNowCard.tsx` and the panel, and NOWCARDTSX was
    written to keep every one of them true: `newestActionRow`, `recent ?? []`,
    `liveAction ? liveAction.line : detail` and `{isRunning && <span` must still
    occur in the COMMENT-STRIPPED card, `isActive` must still NOT occur there,
    `Builder is working` and `@mui` must still not occur in the raw card,
    `Agent` must still occur, and the panel's own line
    `<AgentNowCard dashboard={dashboard} recent={recent} />` is NOT touched by
    this round — the card takes no new prop, because the clock it needs is bound
    inside it. THIS ROUND ADDS THE DOT AND NOTHING ELSE: the badge keeps reading
    `isRunning`, because the recency level reads live for the whole quiet window
    after a job ends and a badge saying "Live" beside the word "Idle" is the
    R-0652 defect itself. Re-keying the badge is a user-visible semantic change
    that gets its own round and its own DECISION; the reviewer's dry run found
    the guard that says so. G8 measures all of this rather than trusting it.
 9. NO NEW DESIGN TOKEN IS INVENTED. `--remedy-live` and `--remedy-dur-pulse`
    are TRANSCRIBED from `docs/ui/design_reference/tokens.css`, where they are
    defined at `#34c27e` and `1600ms`; the app's own token file simply lacked
    them, so assets_spec.md line 178 named a token that could not resolve. This
    is the reference being satisfied, not deviated from, so NO assumption_log
    entry is owed and none is written.
10. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide at every commit under R-0622 and is NOT a gate of this round —
    do not run it and do not report it. Create and merge NO pull request. Push
    the branch after C6. ONE disposable worktree is created for G11 and removed
    and pruned before C6; it runs PYTHON only, never vitest, so it needs no
    `node_modules` (R-0518).
11. Block size, measured on these final bytes AFTER the last edit: TOTAL 471
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice and
    pair CONTENT lines — 268 against DECISION F085 D5's 400. Markers count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C6; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2, C3, C4 and C5. C6's own
     reading is ordered NOWHERE — §3 item 31 leaves it to the next session.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r28.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r28.md` are all equal. Write
     C0b FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their marker LINES —
     `<<<SLICE `/`<<<END ` for the whole texts and `<<<PAIR `/`<<<FROM`/`<<<TO`/
     `<<<ENDPAIR` for the pairs. Report how many whole texts, how many pairs and
     how many CONTENT lines that extractor printed, each as a number YOU
     measured and never as one this block predicts, and re-measure constraint
     11's two numerals from that same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R28 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare slice
     that must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1. THE LINE-COUNT CLAUSE IS MEASURED:
     the reviewer counted PLANF021R28 at 48 lines, so `wc -l` must read EXACTLY
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
     LIST equals the base list followed by RECORD28's own units, ELEMENTWISE
     over the whole list, not at the tail; report N at both points and the
     slice's unit count as the number YOU measured. NEGATIVE CONTROL against the
     C2 file: alter one printable byte of its FIRST paragraph at equal length;
     BOTH readers must REJECT it and ACCEPT the true file. Name the offset and
     the change. Report also that the C2 diff deletes no line.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base and at C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R`
     keys and how many DISTINCT; `Gate: R28`; the MAXIMUM registered id. So
     `- R-` reads 223 at BOTH points, all DISTINCT at both; the maximum R-0660
     at BOTH; `Done: R-` 1 at BOTH; `Landed: ` 0 at BOTH; `Gate: R` keys 26 then
     27, DISTINCT at both; `Gate: R28` 0 then 1. A round that registers nothing
     must move exactly one of these series and no other.
 G7  THE PAIRS at C3. For EACH of TOKENSLIVE and DOTCSS report, in its own
     target file, FROM 1 at the round base and 0 at C3, TO 0 at the round base
     and 1 at C3. Report also that `--remedy-live` and `--remedy-dur-pulse` each
     occur 0 times in `apps/ui/src/styles/tokens.css` at the round base and
     exactly 1 time at C3, and that the two values they take there are BYTE
     EQUAL to the values the same two names carry in
     `docs/ui/design_reference/tokens.css` at C3 — read that reference file and
     compare, rather than comparing against this block's prose.
 G8  THE CARD at C4. `apps/ui/src/components/panels/AgentNowCard.tsx` equals
     NOWCARDTSX PLUS ONE TERMINATING NEWLINE by `cmp` at exit 0, with a NEGATIVE
     CONTROL against the bare slice that must exit 1; report both exit codes.
     THEN MEASURE CONSTRAINT 8 RATHER THAN TRUSTING IT, at C4: in the
     COMMENT-STRIPPED card, `newestActionRow`, `recent ?? []`,
     `liveAction ? liveAction.line : detail` and `{isRunning && <span` each
     occur at least once while `isActive` occurs 0 times; in the RAW card,
     `Builder is working` and `@mui` each occur 0 times and `Agent` at least
     once; and in `apps/ui/src/components/panels/RightLivePanel.tsx` the line
     `<AgentNowCard dashboard={dashboard} recent={recent} />` occurs exactly
     once and that file is absent from this round's path set entirely. Report
     each count. Report also that `recencyLevel` occurs at least once in the
     comment-stripped card — the wiring this round exists to add — and that
     `isLiveByRecency` occurs 0 times in it, which is constraint 8's deferral
     measured rather than described.
 G9  THE CONTRACT APPEND at C5, as ORDERED EQUALITY and never as a per-line
     count — this slice is CODE and repeats blank lines and `assert` lines
     structurally (§4.9, R-0531). Report: the C4 blob of
     `tests/ui_contracts/test_brain_stream_ring.py` is a byte-exact PREFIX of
     the C5 file; the remainder is EXACTLY two newlines plus DOTCONTRACT plus
     one newline, with its sha256, byte and line counts; the file's line count
     before and after; that the C5 diff deletes 0 lines; and that the lines that
     diff ADDS are exactly the remainder's lines IN ORDER, elementwise.
G10  TYPECHECK, UNIT TESTS AND THE PYTHON SUITES, all at C5, in the PRIMARY
     checkout, run SERIALLY and never two at once. From `apps/ui`:
     `npx tsc --noEmit` must exit 0 with EMPTY output, and `npm run test:unit`
     must exit 0 — report the file and test totals it prints, which the reviewer
     read at 15 files and 212 tests at the round base and which this round adds
     no vitest case to. From the REPOSITORY ROOT — a shell left elsewhere makes
     these exit 4 having run no test, which is vacuous and not green — report
     each exit code, the working directory and the total, counting BY PASSED
     PLUS SKIPPED:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 476 at the round base
       plus DOTCONTRACT's own cases; report the total you measure and the number
       of cases DOTCONTRACT contributes, and state that the two agree.
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511, the gate that C1
       and C2 did not break the `.agent/` state readers.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/` path.
G11  THE RED CONTROL for the contract this round adds, because a contract that
     lands AFTER the code it pins has never been seen fail. Run it ONLY inside a
     disposable `git worktree` added at C5 under `.remedy-wt/`, never in the
     primary checkout (guardrail G5). In that worktree, and in the file
     `apps/ui/src/components/panels/AgentNowCard.tsx` alone, delete the single
     occurrence of the attribute text data-recency={level} — COUNT IT FIRST in
     that file, whole-line-containing and indent-agnostic, both readings
     agreeing at 1, and report both numbers (§3 item 25). Then run
     `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf` in
     that worktree and report the exit code and the NAMES of the failing tests,
     which must be non-empty. Restore nothing: remove and prune the worktree
     instead, and report `git worktree list` as the primary checkout ALONE
     afterwards. If the run is GREEN, the contract is vacuous — STOP and report
     that, do not repair it.
G12  RANGE, executed at C5 and covering the round base to C5 — NOT to C6,
     because C6 writes the file that must quote these gates and §3 checklist
     item 31 forbids ordering a reading the quoting artefact cannot hold.
     Report: the base-to-C5 path set against the eight non-handoff paths of
     `Change:`, the difference EMPTY both ways; every commit single-parent;
     `git show --numstat` and `git diff --numstat` agreeing cell by cell with
     the handback's `## Commits` tables (§3 item 28), any disagreement reported
     rather than reconciled; every insertion count under the 500 cap;
     `git ls-files .remedy-wt` 0; and `gh pr list --state open --json
     number,headRefName` — expected EMPTY — with the statement that neither `gh
     pr create` nor `gh pr merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED and scoped to the files a slice or pair
     LANDED IN — `.agent/plan.md`, `.agent/live_review.md`,
     `apps/ui/src/styles/tokens.css`,
     `apps/ui/src/components/panels/RightLivePanel.module.css`,
     `apps/ui/src/components/panels/AgentNowCard.tsx` and
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
            R28's own verdict is UNRECORDED and the next round's ledger commit
            owes it, together with C6's own insertion count and line count,
            which C6 cannot state about itself; and that R29 rules the badge's
            liveness source with a DECISION in `.agent/decisions.md`, the
            question this round deliberately left open in constraint 8.

<<<SLICE PLANF021R28
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
R28 wires the activity dot. `recency.ts` has held the rule since R21 with no
reader; the card now subtracts the newest ACTION row's `receivedAtMs` from a
clock it ticks itself, and renders the level as a data attribute the CSS
selects on. The dot's CSS and the two tokens it needs are transcribed from the
binding design reference, which defines both. The BADGE is not re-keyed here.

## Next Steps
1. R29: rule the badge's liveness source. `isLiveByRecency` reads live for the
   whole quiet window after a job ends, so feeding the badge from it puts "Live"
   beside the word "Idle" — R-0652 with a 30-second fuse. The round records a
   DECISION in `.agent/decisions.md` and updates the pin naming the choice.
2. R30: `feedScroll.ts` into the feed's scroll container with the new-rows pill
   component_spec.md line 86 binds; then the row click-jump and T003's disabled
   steering input.
3. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round in this chain.
- The dot's own fade is driven by an interval the card owns. No headless test
  can reach a React hook here, so its guard is the source contract plus the
  purity of `recency.ts`, which vitest does cover.
- `npm run lint` is RED tree-wide at every commit: the eslint config has no
  TypeScript parser, so it reports a parsing error per file and is blind to
  style. That is R-0622, still open.
- A worktree lacks `apps/ui/dist/`, so `tests/ui_contracts/` skips one more case
  there than in the primary checkout. COUNT BY PASSED PLUS SKIPPED.
- No code defect of F021 is open; R-0364, R-0403, R-0607 through R-0609,
  R-0611, R-0613, R-0622, R-0651 and R-0653 through R-0659 stay routed to a
  paydown branch.
<<<END PLANF021R28

<<<SLICE RECORD28
Gate: R28 — the R27 entry. R27 PASSED ON EVERY ONE OF ITS TEN GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK. R27 recorded R26 and repaired R-0660, the reviewer's own pair-design defect, in the order §4.4 requires: C2 registered the finding, C3 moved the nine lines, C4 resolved it, so a session dying mid-round would have left the finding on disk rather than a silent repair. TRANSPORT HELD ACROSS FOUR COPIES at sha256 ef9c3549c0fa1a040369f5d6b57eea48d430a10b456b0b447bb35701de8fc94a over 26266 bytes and 274 lines: the reviewer's own `.remedy-wt/f021-r27.md`, `.agent/authored/f021-r27.md` at `4c6aea98` and `.agent/last_block.md` at `2b62c498`, the last written FROM the committed C0a blob. SLICES: the reviewer's extractor read the whole texts PLANF021R27, RECORD27 and DONE660 and the single pair SHIMMOVE over 72 CONTENT lines from that committed blob, with 0 stray `<<<` lines, TOTAL 274 against DECISION F085 D6's 490 and PROSE 202 against D5's 400 — both equal to that block's constraint 9. THE PLAN WRITE HELD: `.agent/plan.md` at `15814e4c` is byte-equal to PLANF021R27 plus one terminating newline and NOT to the bare slice, `wc -l` exactly 48, `^## Goal$` and `^## Next Steps$` once each. BOTH LEDGER APPENDS HELD UNDER BOTH READERS: RECORD27's remainder is sha256 a7008d2cd7f36abbb1a7e01f12f4d7244657ff5609f1dc78f855aa6e925c2d4c over 8100 bytes and 6 lines, the file 572216 B / 1172 L before and 580316 B / 1178 L after; DONE660's is 9d29c35494ae66d3136f0133174c17d1d91aed271ef8d239e1744088442ba0c5 over 764 bytes and 2 lines, the file 580316 B / 1178 L to 581080 B / 1180 L; units read 267, 270 then 271, ELEMENTWISE equal at each step with RECORD27 exactly 3 units and DONE660 exactly 1; and a negative control on the C4 file — byte `v` at offset 4 of the FIRST paragraph changed to `X` at equal length — was REJECTED by reader (a) on its prefix clause and by reader (b) at unit index 0, while both ACCEPTED the true file. Neither diff deleted a line. THE SETS MOVED EXACTLY AS A ONE-FINDING ROUND MUST: `- R-` 222, 223, 223, all DISTINCT at all three points; maximum R-0659, R-0660, R-0660, next free R-0661; `Landed: ` 0 throughout; `Gate: R` keys 25, 26, 26, DISTINCT at all three; `Gate: R27` 0, 1, 1; and `Done: R-` 0, 0, 1 — the FIRST `Done:` line this ledger has ever carried, naming R-0660. THE REPAIR IS PROVABLY A MOVE: SHIMMOVE's FROM occurred 1 time at the base and 0 at `92ed0455`, its TO 0 then 1, the file is 3093 bytes and 79 lines at BOTH points, and the SORTED MULTISET of its lines is IDENTICAL at both — so nothing but order changed. The defect is visible in the numbers it fixes: at the base the `^import ` lines were 1, 2 and 10 with `function feedRowOf` at 7, and at `92ed0455` the imports are 1, 2 and 3 with the function at 8, every import above the definition. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY in the PRIMARY checkout: `npx tsc --noEmit` exit 0 with output EMPTY; `npm run test:unit` 15 files and 212 tests, UNCHANGED from the base as a behaviour-free move must be; `tests/ui_contracts/` 472 passed plus 4 skipped = 476; the three state-reading suites 511; the canary 42. THE RANGE HELD: seven commits base to C5, every one single-parent, the path set base-to-C4 EQUAL to the five non-handoff `Change:` paths with both differences EMPTY, insertions 274, 169, 23, 6, 1, 2 and 42 each under the 500 cap and each agreeing cell by cell with the handback's tables, the aggregate `+8/-0` on the ledger being exactly C2's +6 plus C4's +2, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout ALONE, `gh pr list --state open` EMPTY, the marker sweep 0 line-anchored over all six prefixes in each of the three files a slice or pair landed in, and the reflog read BY OPERATION every row `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE OWED READINGS, which R27's own handback could not hold about itself (§3 item 31): its C5 `2b8830ac` is single-parent and touches `.agent/handoff.md` ALONE at 42 insertions and 56 deletions, far under the 500 cap, and that handback measures 87 lines by `wc -l` — over the 60-line baseline and WITHIN the 100-line tier AGENTS.md grants a handback whose per-commit tables cover more than five commits, which this one's seven do, declared with its mandated cause and no section dropped. WHY R27 IS PASS: every applied byte is reproducible from the committed block by the reviewer's own extractor, both ledger remainders matched digests the reviewer computed independently, the repair is proven behaviour-free by a sorted-multiset identity rather than by a green test alone, and the round declared no deviation because it took none.
<<<END RECORD28

<<<PAIR TOKENSLIVE apps/ui/src/styles/tokens.css
<<<FROM
  --remedy-red-500: #ef6363;

  --remedy-line: rgba(44, 82, 150, 0.14);
<<<TO
  --remedy-red-500: #ef6363;

  /* Liveness and its pulse, transcribed from docs/ui/design_reference/tokens.css
     so assets_spec.md line 178 -- the live-activity dot, 8px, --remedy-live,
     1.6s pulse -- names a token that resolves. Same value as --remedy-green by
     the reference's own definition; the two spellings are the design system's,
     not a drift this file introduced. */
  --remedy-live: #34c27e;
  --remedy-dur-pulse: 1600ms;

  --remedy-line: rgba(44, 82, 150, 0.14);
<<<ENDPAIR

<<<PAIR DOTCSS apps/ui/src/components/panels/RightLivePanel.module.css
<<<FROM
.liveSmall span { width: 7px; height: 7px; border-radius: 50%; background: var(--remedy-green); }

.agentNow { display: flex; gap: 12px; align-items: flex-start; }
<<<TO
.liveSmall span { width: 7px; height: 7px; border-radius: 50%; background: var(--remedy-green); }

/* The NowCard's activity dot (assets_spec.md line 178). The level lives in a
   data attribute rather than in the class name, so the rule that computes it
   stays in recency.ts and this file only says what each level LOOKS like.
   Reduced motion needs no rule here: globals.css already flattens every
   animation to a single 0.001ms iteration. */
.activityDot { width: 8px; height: 8px; border-radius: 50%; background: var(--remedy-live); align-self: center; margin-left: auto; flex: 0 0 auto; }
.activityDot[data-recency="none"] { background: var(--remedy-faint); opacity: 0.45; }
.activityDot[data-recency="fresh"] { animation: remedyLivePulse var(--remedy-dur-pulse) ease-in-out infinite; }
.activityDot[data-recency="fading"] { opacity: 0.55; }
.activityDot[data-recency="idle"] { background: var(--remedy-faint); opacity: 0.7; }

@keyframes remedyLivePulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.45; transform: scale(0.82); }
}

.agentNow { display: flex; gap: 12px; align-items: flex-start; }
<<<ENDPAIR

<<<SLICE NOWCARDTSX
import { useEffect, useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import type { FeedRow } from "../../api/feedRow";
import { newestActionRow } from "../../api/actionClass";
import { recencyLevel } from "../../api/recency";
import { deriveAgentStatus } from "../../cockpitLogic";
import { SparkGlyph, TaskCurrentGlyph } from "../icons/RemedyGlyphs";
import styles from "./RightLivePanel.module.css";

/** How often the card re-reads the clock. The dot fades on its own between
 *  FRESH_WINDOW_MS and QUIET_WINDOW_MS with no new event to re-render it, so
 *  the card must ask the time again; one second is far finer than the
 *  five-second window the fade begins at and costs one state write per second. */
const RECENCY_TICK_MS = 1000;

/** The clock, bound HERE because this is the edge that has one. recency.ts
 *  stays a pure function of two numbers and never reads a clock itself, which
 *  is what lets the fade be tested without waiting for it. */
function useRecencyNowMs(): number {
  const [nowMs, setNowMs] = useState(() => Date.now());
  useEffect(() => {
    const timer = window.setInterval(() => { setNowMs(Date.now()); }, RECENCY_TICK_MS);
    return () => { window.clearInterval(timer); };
  }, []);
  return nowMs;
}

export function AgentNowCard({ dashboard, recent }: { dashboard: RemedyDashboard; recent?: readonly FeedRow[] }) {
  const { status: statusText, detail, isRunning } = deriveAgentStatus(dashboard);
  // The newest ACTION the stream has produced, which is what this card is FOR.
  // Bookkeeping is excluded on purpose (actionClass.ts): a card that narrated
  // the agent reading files would report motion where there was none.
  const liveAction = newestActionRow(recent ?? []);
  const nowMs = useRecencyNowMs();
  // Both instants subtracted here sit on ONE clock: `receivedAtMs` is the
  // arrival stamp the host took from this same `Date.now`, never the envelope's
  // server-clock string, which a server running behind would render as a dead
  // agent. Remedy deliberately does NOT feed the badge from this level yet: the
  // dot may say "acted 20s ago" while the job has ended, and a badge saying
  // "Live" beside the word "Idle" is the R-0652 defect. The badge keeps the
  // agent's own running flag until that trade-off is ruled on its own.
  const level = recencyLevel(liveAction ? liveAction.receivedAtMs : null, nowMs);

  return (
    <section className={styles.card}>
      <header className={styles.cardHeader}>
        <h2>Agent is doing now</h2>
        {isRunning && <span className={styles.liveSmall}><span /> Live</span>}
      </header>
      <div className={styles.agentNow}>
        <div className={styles.actorIcon}>
          {isRunning ? <TaskCurrentGlyph style={{ width: 16, height: 16, color: "white" }} /> : <SparkGlyph style={{ width: 16, height: 16, color: "white" }} />}
        </div>
        <div>
          <strong>{statusText}</strong>
          <p>{liveAction ? liveAction.line : detail}</p>
        </div>
        <span className={styles.activityDot} data-recency={level} aria-hidden="true" />
      </div>
    </section>
  );
}
<<<END NOWCARDTSX

<<<SLICE DOTCONTRACT
class TestTheActivityDotReadsTheRecencyRule:
    """T5_F021 line 62: the NowCard's activity dot pulses on recency and fades
    to idle after a quiet window. The rule is `recency.ts` and it is pure, so
    what a behavioural test cannot see is WHERE the card gets its two operands.
    Both must sit on ONE clock -- the row's arrival stamp and a `Date.now` the
    card reads itself. The BADGE is deliberately not wired to this level yet:
    the dot may read fresh for the quiet window after a job has ended, and a
    badge saying "Live" beside the word "Idle" is exactly R-0652. That trade-off
    is ruled in its own round, and TestTheNowCardBadgeTracksTheAgent above still
    pins the badge to the agent's running flag until then."""

    def test_the_card_reads_the_shared_recency_rule(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "recencyLevel(" in code, (
            "the dot must ask recency.ts rather than compare instants itself"
        )

    def test_the_dot_subtracts_the_arrival_stamp(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "liveAction.receivedAtMs" in code, (
            "the dot's operand is the arrival stamp, never the server's string"
        )

    def test_the_card_ticks_its_own_clock(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "setInterval" in code, (
            "with no tick the dot cannot fade until an unrelated render happens"
        )
        assert "clearInterval" in code, (
            "an interval a component never clears outlives the component"
        )

    def test_the_level_reaches_the_dom_as_data(self):
        code = strip_ts_comments(NOWCARD.read_text())
        assert "data-recency={level}" in code, (
            "the level must reach the markup, or the CSS has nothing to select"
        )

    def test_the_dot_css_covers_every_level(self):
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        for level in ("none", "fresh", "fading", "idle"):
            assert f'.activityDot[data-recency="{level}"]' in css, (
                f"the {level} level renders unstyled"
            )
        assert "--remedy-dur-pulse" in css, (
            "the pulse must use the motion token, not a literal duration"
        )

    def test_the_liveness_tokens_resolve(self):
        tokens = (UI_SRC / "styles" / "tokens.css").read_text()
        assert "--remedy-live:" in tokens, (
            "assets_spec.md line 178 names a token this file must define"
        )
        assert "--remedy-dur-pulse:" in tokens, (
            "motion_spec.md line 13 gives the LIVE dot a 1600ms pulse token"
        )
<<<END DOTCONTRACT
