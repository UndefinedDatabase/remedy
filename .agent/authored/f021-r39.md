── STEP RECORD THE GATE — F021 ──
Goal:        Record R38's PASS and register what F021's integration gate and its
             acceptance read turned up. THE GATE IS GREEN: the branch-only
             failure set is empty against the merge base and no acceptance
             clause is UNSATISFIED, so the next round is the evidence round.
             The ids constraint 3 names are minted; three further candidates
             deliberately are not, because R-0445, R-0444 and R-0645 already
             describe them, and two of those three get a Recurrence entry
             instead. This round writes no product code and repairs nothing.

Fortschritt: 100 % der Bauarbeit; Integrations-Gate gelaufen und gruen, Evidenz-
             Runde und STATUS-Runde stehen noch aus — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R38 verdict,
             the four registrations and the two recurrences · C3 the handoff.

Change:      Exactly these paths. `.agent/authored/f021-r39.md` (NEW, C0a) ·
             `.agent/last_block.md` (C0b) · `.agent/plan.md` (C1) ·
             `.agent/live_review.md` (C2) · `.agent/handoff.md` (C3). NO file
             under `apps/`, `packages/`, `tests/` or `docs/` is touched, and
             nothing under `.agent/gate_f021_r38/` is edited. Report the counts
             YOU measure.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3 and is not negotiable. ROUND BASE is
    `2428f021` — resolve its full form with `git rev-parse`.
 3. THIS ROUND MINTS EXACTLY THE IDS RECORD39 CARRIES — R-0662, R-0663, R-0664
    and R-0665 — AND RESOLVES NONE. Before it: 224 registered under
    `^- R-\d+ — `, maximum R-0661, `^Done: R-` 1. After C2: 228, ALL DISTINCT,
    maximum R-0665, `^Done: R-` still 1.
 4. RECORD39 IS A SEQUENCE OF PARAGRAPHS SEPARATED BY EXACTLY ONE BLANK LINE
    EACH. Every paragraph opens with the bytes `- R-`, with `Recurrence: ` or
    with `Gate: R39 — ` and with nothing else. Extract them BOTH by splitting on
    a blank line AND by counting lines matching `^- R-\d+ — `, `^Recurrence: `
    and `^Gate: R`; report the number YOU measured each way and that the two
    AGREE.
 5. THE APPEND CONVENTION for `.agent/live_review.md` at C2: the slice is quoted
    WITHOUT a trailing newline; add EXACTLY ONE newline, then RECORD39, then one
    terminator, so the join carries EXACTLY ONE BLANK LINE. A WHOLE-FILE write
    (PLANF021R39) is the slice PLUS one terminator.
 6. THE LEDGER IS APPEND-ONLY. No landed paragraph, `Gate:` or `Recurrence:`
    entry is edited — R-0445, R-0444 and R-0645 are reached by APPENDING, never
    by rewriting what they already say.
 7. EVERY LEDGER COUNT NAMES ITS PATTERN, ANCHORED. No unanchored count is
    ordered over `.agent/live_review.md`, which quotes the tokens a gate might
    count (R-0630).
 8. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide under R-0622 and is NOT a gate — do not run it. Create and
    merge NO pull request. Push the branch after C3. Create NO worktree: this
    round changes no control flow, so no red-proof is owed and none is ordered.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 181
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 125 against DECISION F085 D5's 400. Markers count as prose.
10. C3 IS A ROUND HANDBACK. Its commit tables earn the ≤60-line tier; a DECISION
    D15 line declares any overage with its mandated cause and NO section is
    dropped. The `+/-` cells of its `## Commits` table are the `git diff
    --numstat` readings and are compared cell by cell against the numbers G5
    reports, because a value written twice is derived twice (§3 item 28).

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C3; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1 and C2. C3's own reading is
     ordered NOWHERE — §3 item 31 leaves it to the next session.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r39.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over my emitted
     copy at `.remedy-wt/f021-r39.md` are all equal. Write C0b FROM the
     committed C0a blob. Report the digest, bytes and lines. Then extract the
     slices from the COMMITTED C0a blob by their marker LINES, `<<<SLICE ` and
     `<<<END `, and report how many whole texts and how many CONTENT lines your
     extractor printed — numbers YOU measured — re-measuring constraint 9's two
     numerals from that same blob against their caps.
 G3  `.agent/plan.md` at C1 equals PLANF021R39 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0, with a NEGATIVE CONTROL against the bare slice that must
     exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1, and the `wc -l` YOU measure against
     AGENTS.md's "keep it short (<50 lines)". If that count is 50 or more, STOP
     and report — do NOT trim the file to reach it (R-0654).
 G4  THE LEDGER, at C2, every count naming its anchored pattern, base then C2:
     canonical `^- R-\d+ — ` 224 then 228, ALL DISTINCT at both, maximum R-0661
     then R-0665; loose `^- R-` 225 then 229, gap 1 at both; `^Done: R-` 1 then
     1; `^Gate: R` 37 then 38, DISTINCT at both; `^Gate: R39` 0 then 1;
     `^Recurrence: ` 14 then 16; `^Recurrence: R-0445 — ` 0 then 1;
     `^Recurrence: R-0645 — ` 0 then 1; and each of `^- R-0662 — `,
     `^- R-0663 — `, `^- R-0664 — ` and `^- R-0665 — ` 0 then 1. Report that the
     base blob is a byte-exact PREFIX of the C2 blob, that the remainder is
     EXACTLY one newline plus RECORD39 plus one newline, and — the reader
     constraint 4 orders — that the paragraph split and the anchored line counts
     AGREE, naming the FIRST paragraph's opening bytes explicitly so the region
     is covered from its start and not only in total (R-0631).
 G5  STRUCTURE. `git diff --name-only 2428f021..HEAD` at C2 EQUALS the FOUR
     non-handoff paths of the `Change:` list, and at C3 those plus
     `.agent/handoff.md`; report the count YOU measure at each and both set
     differences, which must be EMPTY at both. As many commits as the `Bundle:`
     list names, every one single-parent; `git show --numstat` and `git diff
     --numstat` agree cell by cell; insertions under 500 for every commit BEFORE
     C3, each number reported, C3's own left to the next round (§3 item 14) —
     and note that `--stat` may print a larger figure than `--numstat` for a
     whole-file rewrite under rename detection, which `.agent/last_block.md` is.
     Marker sweep, LINE-ANCHORED, 0 for each of `<<<SLICE ` and `<<<END ` over
     `.agent/plan.md` and `.agent/live_review.md`. No unanchored `<<<` count is
     ordered over either (R-0630). Reflog read BY OPERATION: every one of this
     round's rows is `commit`, with `amend`, `rebase` and `cherry` 0 each in
     that field. `gh pr list --state open` reported verbatim; it must print
     `[]`, and NEITHER `gh pr create` NOR `gh pr merge` is run this round.
 G6  THE SUITES, SERIAL, in the PRIMARY checkout, never two at once. This round
     rewrites `.agent/` state and touches nothing else, so it gates ALL FOUR
     state readers and the canary and NOTHING MORE — no `tsc`, no vitest, no
     `ruff`, because no file those read is touched, and R-0364 forbids ordering
     a gate whose subject this round does not change.
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py -q -rf` — I measured 528 at the
     round base. `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — 42
     at the base. Report both numbers YOU measure. If either differs, STOP and
     report the difference rather than explaining it away.

<<<SLICE PLANF021R39
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
R39 records R38's PASS and registers what the integration gate and the
acceptance read turned up. THE GATE IS GREEN: the branch-only failure set is
empty against the merge base `4548995d` and no acceptance clause is UNSATISFIED.
Four ids are minted — R-0662, R-0663, R-0664 and R-0665 — and three further
candidates are not, because R-0445, R-0444 and R-0645 already describe them.
The round writes no product code.

## Next Steps
1. The evidence round: the closure bundle and a fresh review zip, per
   docs/roadmap/STATUS_closure_protocol.md.
2. The STATUS-commit round; the two are never one round.
3. The pull request, opened at closure and merged only at the Open PR Gate.

## Risks
- R-0663 is an ACCEPTANCE deviation rather than a process one: the closure round
  must either rule the CSS-module realization sufficient for "per the binding
  CSS" or order the one-line repair in its own reviewer-gated round.
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK.
- Nothing here renders CSS. R-0661's pin proves the unresolved-property SET has
  not grown; it cannot prove any rule's computed value.
- `npm run lint` is RED tree-wide under R-0622, still open.
- No code defect of F021 blocks the gate. R-0364, R-0369, R-0402, R-0403,
  R-0419, R-0439, R-0444, R-0445, R-0587, R-0607 through R-0609, R-0611,
  R-0613, R-0618, R-0622, R-0629, R-0630, R-0644, R-0645, R-0651, R-0653
  through R-0659, R-0661, R-0662, R-0664 and R-0665 stay routed to a paydown
  branch.
<<<END PLANF021R39

<<<SLICE RECORD39
- R-0662 — Low, A GATE ORDERED EVERY PIN THROUGH A MECHANISM THAT CANNOT PRODUCE ONE THIRD OF THEM, AND THE ONLY OTHER STATUS IT OFFERED WAS FALSE OF THEM. Raised by the reviewer against its own F021 R38 block; found first by the WORKER and declared as that round's deviation 1. G6 ordered the acceptance read to name, for every SATISFIED clause, a test node id taken from `python3 -m pytest --collect-only -q`, and offered SATISFIED-WITHOUT-A-TEST only for a clause "no suite in this repository reaches". Five of the eighteen clauses — GD3, GD6, A2, A3 and A5 — are pinned ONLY by vitest, which that command cannot enumerate, while vitest IS a suite this repository runs and gates, so the second status is false of them and the block left no legal route. The worker took those ids from `npm run test:unit -- --reporter=json` (exit 0, 218 of 218 passed), prefixed them `vitest:`, and spent a declared deviation on a command the block never ordered. NOTHING WAS MISMEASURED, and the reviewer re-resolved every cited pin at `2428f021`: the eleven pytest ids are all present among the 499 ids `--collect-only -q` reports for `tests/ui_contracts/`, and all five vitest names are traceable in `apps/ui/src/api/feedRow.test.ts`, `humanize.test.ts` and `feedFocus.test.ts`. THE DEFECT IS §3 CHECKLIST ITEM 8'S CLASS IN A TWO-RUNNER REPOSITORY: a gate naming ONE runner's enumeration mechanism silently excludes everything the other runner owns, and the escape hatch it offers alongside is worded for tests that do not exist rather than for tests it cannot enumerate. THE FIX, binding the reviewer: a gate ordering node ids here names BOTH mechanisms — `pytest --collect-only -q` for the Python suites and `npm run test:unit -- --reporter=json` for vitest — and says which prefix marks which. Low, not Medium: the omission cost one declared deviation and produced no false reading, and the substitution the worker chose is the one the fix clause names.

- R-0663 — Low, THE SHIPPED FEED ROW DIVERGES FROM THE STYLESHEET ITS OWN ACCEPTANCE CLAUSE CALLS BINDING. Raised by the reviewer while gating F021 R38's acceptance read; the divergence itself was found by the WORKER and reported without an id under that block's constraint 3. `docs/roadmap/features/T5_F021.md` Goal & Done requires the feed to render "per the binding CSS", and that file's Design section fixes the row as `.feed-row{display:flex;gap:10px;padding:9px 14px;font:500 13px/1.45 var(--remedy-font-ui);color:var(--remedy-ink)}`. Measured by the reviewer at `2428f021` over `apps/ui/src/components/panels/RightLivePanel.module.css`: the shipped row is `.activityItem { display: flex; gap: 12px; }`, so the gap DIVERGES by 2px, and neither the padding nor the `font:` shorthand sits on that selector — the row's typography lives on `.activityMeta strong`, `.activityItem p` and `.activityTag` instead. The scroll box itself holds what it should: `.activityList` carries `max-height: 52vh` and `overflow: auto`, both pinned as literal text by `tests/ui_contracts/test_brain_stream_ring.py::TestTheFeedScrollRuleIsWiredToTheCard::test_the_feed_box_can_actually_scroll`. Low and not Medium because nothing here is a false green — the divergence is measured, on disk, and now recorded — and a 2px gap inside a CSS-module realization of a spec snippet is plausibly the realization rather than a defect. THE FIX IS A RULING RATHER THAN A PATCH, and it belongs to F021's closure round: either that round records a DECISION that the module realization satisfies the clause, naming the restructured typography as the reason, or it orders the one-line `gap` repair in its own reviewer-gated round. It may not do both and it may not do neither.

- R-0664 — Low, TWO ACCEPTANCE CLAUSES ARE PINNED AT THE DATA LAYER WHILE THE RENDER SITE THAT MAKES EACH ONE TRUE IS ASSERTED BY NOTHING. Raised by the reviewer while gating F021 R38's acceptance read; both instances were found by the WORKER and reported without an id under that block's constraint 3. FIRST INSTANCE: Goal & Done's "feed rows carry their seq" is pinned by `apps/ui/src/api/feedRow.test.ts` proving that `feedRowOf` puts the frame's own seq on the row, and by nothing else, while `apps/ui/src/components/panels/ActivityFeedCard.tsx` is where the seq is actually printed — a card that stopped printing it would leave every suite in this repository green. SECOND INSTANCE: "jump-to-node focuses correctly" is true only because `apps/ui/src/components/shell/RemedyShell.tsx` hands the SAME `onSelectNode` to `BrainGraphStage` and to `RightLivePanel`; `tsc` forces the shell to pass SOMETHING because the prop is required, but measured by the reviewer at `2428f021` the token `onSelectNode` occurs exactly TWICE in all of `tests/ui_contracts/`, both inside the card-and-panel pair, so nothing asserts that the two callbacks are one. ONE ID AND NOT TWO, per §3 checklist item 30: the defect is single — an acceptance clause whose proof stops at the pure module and never reaches the component that makes it observable — and the two clauses are its instances. Low: no test is wrong and no claim is false, the coverage simply ends one layer short, which is exactly what an acceptance read exists to surface. THE FIX belongs in `tests/ui_contracts/test_brain_stream_ring.py`, the file that already reads these components as source text, and not in a DOM harness this repository does not have.

- R-0665 — Low, EVERY UI FEATURE IS ROUTED TO DOCUMENT ITS VISUAL DEVIATIONS IN A FILE THAT DOES NOT EXIST. Raised by the reviewer while gating F021 R38, when R-0663 needed the route this repository mandates for exactly that case and there was none. `docs/roadmap/features/T5_F021.md`'s own header rules that "any visual deviation must be documented in the assumption_log with a technical reason", and the same clause is standard boilerplate across the roadmap. Measured by the reviewer at `2428f021` with `git grep -l assumption_log 2428f021 -- docs/`: SEVENTY-SIX tracked files under `docs/` name it, sixty-four of them roadmap feature files and the rest including `docs/agents/handback_template.md`, `docs/agents/worker_conventions.md`, `docs/agents/reviewer_conventions.md`, `docs/roadmap/ROADMAP.md` and four files inside `docs/ui/design_reference/` itself. Measured in the same breath with `git ls-tree -r --name-only 2428f021`: NO tracked path in this repository contains the string `assumption_log` in its name. The obligation is therefore unmeetable by construction, and has been for every UI feature that carried the boilerplate. Low and not Medium because no green depends on it and no claim is falsified by it: a deviation that cannot be logged in the named file is still recorded in the finding ledger, which is where R-0663 now sits. THE FIX IS REPOSITORY-WIDE AND BELONGS TO A PAYDOWN BRANCH, not to F021: either create `docs/ui/design_reference/assumption_log.md` and register it in `docs/README.md` as the boilerplate promises, or amend the boilerplate to name the ledger it actually uses. Creating a doc that seventy-six files reference is not a change a feature branch may make on the way past.

Recurrence: R-0445 — THE CANONICAL INTEGRATION-GATE PROCEDURE'S PARITY COPY MANUFACTURES BASE FAILURES, AND THE NUMBER MEASURED AT THIS BRANCH IS 78 AGAINST 0. Second instance, at F021 R38, and the first to run BOTH routes over the same tree. NO NEW ID IS MINTED: R-0445 already rules that `docs/agents/integration_gate.md` step 3's copy of `apps/ui/dist` leaves the copied build older than the freshly checked-out sources, so `_frontend_is_stale` returns True and the server thread dies. THE TWO READINGS: the reviewer executed the COPY route in a disposable worktree at merge base `4548995d`, which it created for the purpose and has since removed and pruned, and measured 78 base-only failures; the round then took the BUILD route the same step also offers — `npm run build` inside the base worktree, exit 0, 962 modules — and measured 0 failures over 17572 passed and 20 skipped. WHAT THIS ADDS TO R-0445 IS THE SCALE AND THE REMEDY. R-0445 names EIGHT ids in `tests/ui_server/test_live_state.py::TestUIServerIntegration`, and this instance produced 78 across `tests/ui_server/`, so the blast radius is an order of magnitude wider than the finding states; and R-0445's own parenthetical alternative, "or build in the worktree", is the half that works and is now measured rather than proposed. THE REPAIR REMAINS ROUTED to a paydown branch: step 3 still lists `apps/ui/dist` among the artifacts to COPY, and rewriting a process doc from inside a feature branch is scope drift.

Recurrence: R-0645 — THE INTEGRATION GATE INFERS A BRANCH-ONLY SET FROM ONE SAMPLE, AND THE REVIEWER'S RE-RUN AGAIN FOUND AN ID THE WORKER'S RUN DID NOT. Second instance, at F021 R38, on ONE OF THE SAME TWO NODE IDS as the first. NO NEW ID IS MINTED: R-0645 already rules that step 1's single branch run is a SAMPLE, and that an empty branch-only set reads on the page as "this branch introduces no failures" when what was measured is "this run introduced none". THE TWO READINGS: the worker's branch run at `dee2e6d8` exited 0 with 17651 passed and 20 skipped and an EMPTY `branch_failed.txt`; the reviewer's run of the identical command from the same primary checkout at `2428f021` exited 1 with 1 failed, 17650 passed and 20 skipped, the single id being `tests/cli/test_job_rerun_workspace_identity.py::TestNoFalseWorkspaceDrift::test_a_mutated_workspace_shows_blocking_drift`, which is the first of the two ids R-0645's own instance names. CLASSIFIED AND NOT BLOCKING: the reviewer re-ran that id SERIALLY TEN TIMES and it exited 0 on all ten, which is the xdist-flake class `docs/agents/integration_gate.md` step 4 records rather than blocks on, and the file lives under `tests/cli/` where F021's change set touches nothing at all. WHAT THIS ADDS TO R-0645: the same id recurring at a different feature and a different head is evidence its pair was not incidental to F009, and ten serial passes bound the flake to the parallel runner rather than to the test's own logic.

Gate: R39 — the R38 entry. R38 PASSED ON EVERY GATE, EACH RE-MEASURED BY THE REVIEWER FROM THE COMMITTED BLOBS AND BY RE-EXECUTING THE SUITES ITSELF RATHER THAN READING THE HANDBACK BACK, AND ALL FIVE OF ITS DECLARED DEVIATIONS ARE ACCEPTED — ONE OF THEM IS THE REVIEWER'S OWN BLOCK DEFECT AND IS RECORDED ABOVE AS R-0662. R38 IS F021'S INTEGRATION GATE AND IT IS GREEN. THE GATE ITSELF, RE-RUN INDEPENDENTLY: the reviewer's own branch run of `python3 -m pytest -n auto -q` at `24a6b899` exited 0 with 17651 passed and 20 skipped in 150.3 s, equal to the worker's reading at `dee2e6d8`; the reviewer's own base run at merge base `4548995d`, parity restored by the BUILD route, exited 0 with 17572 passed and 20 skipped, equal to the worker's; `comm -13` and `comm -23` are both EMPTY on both sides, and the worker RED-CONTROLLED both of those empty readings on its own initiative with a real two-test module and a synthetic comm pair the block never ordered — which is the behaviour this protocol exists to produce and is worth more than the gate it was attached to. The canary read 42 passed. TRANSPORT HELD at sha256 `42def0677ea427b885a201c86285b3d1b24e0eb5d9680d0bf9347e1f8d3ff37c` over 19303 bytes and 243 lines across the reviewer's emitted copy, `.agent/authored/f021-r38.md` at `a5b6cdb0` and `.agent/last_block.md` at `11c20d0f`; the extractor printed 2 whole texts over 43 CONTENT lines beside 4 marker lines, TOTAL 243 against 490 and PROSE 200 against 400. THE PLAN WRITE HELD: `.agent/plan.md` at `94d4b0b2` is byte-equal to its slice plus one terminating newline and NOT to the bare slice, `wc -l` 42 under AGENTS.md's 50. THE APPEND HELD: at `dee2e6d8` the `24a6b899` blob is a byte-exact PREFIX and the remainder is EXACTLY one newline plus RECORD38 plus one newline over 3072 bytes. THE SETS DID NOT MOVE: canonical `^- R-\d+ — ` 224 then 224 all DISTINCT, maximum R-0661 at both; `^Gate: R` 36 then 37; `^Gate: R38` 0 then 1; `^Recurrence: ` 14 then 14; `^Done: R-` 1 then 1. THE ACCEPTANCE READ WAS RE-RESOLVED, NOT READ BACK: 18 clauses at 17 SATISFIED, 1 SATISFIED-WITHOUT-A-TEST and 0 UNSATISFIED, and the reviewer independently confirmed at `2428f021` that `.activityItem` really sets `gap: 12px`, that `onSelectNode` really occurs exactly twice in `tests/ui_contracts/`, and that the seq is really printed through `styles.activityTag` in `ActivityFeedCard.tsx` — the three disk claims the read's own reported-not-minted section rests on, now registered as R-0663 and R-0664. STRUCTURE: seven commits over `24a6b899..2428f021`, every one single-parent, `git show --numstat` and `git diff --numstat` agreeing cell by cell, insertions 243, 186, 12, 2, 222, 84 and 107, each under 500; 16 paths at `af5bac0a` and 17 at `2428f021`, every one inside the block's three declared classes and NONE under `apps/`, `packages/`, `tests/` or `docs/`; the marker sweep 0 for each of `^<<<SLICE ` and `^<<<END ` over `.agent/plan.md` and `.agent/live_review.md`; every reflog row of the round carrying `commit` in its operation field; `gh pr list --state open` printing `[]`; `git worktree list` one entry and no `tmp/` branch surviving. OWED TO THIS ENTRY BECAUSE C5 COULD NOT STATE THEM ABOUT ITSELF: C5's SHA is `2428f021`, its insertion count is 107, and `git status --porcelain` printed 0 lines at it. THE SIZE DEVIATION IS ACCEPTED: 143 lines against the ≤100 tier its seven commits earn, with DECISION D15's cause naming the seven commit tables, the item-status table, the seven gate lines carrying both suite figures and both comm sets, the authored-text section and the reported-not-minted list constraint 3 required it to carry.
<<<END RECORD39
