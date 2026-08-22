── STEP INTEGRATION GATE — F021 ──
Goal:        Run F021's INTEGRATION GATE and read its acceptance criteria against
             what is on disk. The full suite runs at the branch tip and at the
             merge base per docs/agents/integration_gate.md, and the feature
             file's Goal & Done is resolved clause by clause to the file, the
             symbol and the test node id that satisfy it. THIS ROUND MAY ONLY
             CONFIRM: it writes no product code and repairs nothing. R37's PASS
             is recorded at C2, before any of this round's own gates run.

Fortschritt: 100 % der Bauarbeit; vom Abschluss erledigt diese Runde das
             Integrations-Gate, waehrend Evidenz-Runde und STATUS-Runde noch
             ausstehen — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R37 verdict ·
             C3 the gate evidence · C4 the acceptance read · C5 the handoff.

Change:      Exactly these paths and nothing else. `.agent/authored/f021-r38.md`
             (NEW, C0a) · `.agent/last_block.md` (C0b) · `.agent/plan.md` (C1) ·
             `.agent/live_review.md` (C2) · files under the NEW directory
             `.agent/gate_f021_r38/` (C3 and C4) · `.agent/handoff.md` (C5). NO
             file under `apps/`, `packages/`, `tests/` or `docs/` is touched.
             Report the counts YOU measure.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. ROUND
    BASE is `24a6b899` — resolve its full form with `git rev-parse`.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. Before it: 224 registered
    under `^- R-\d+ — `, maximum R-0661, `^Done: R-` 1. After C2: still 224,
    still all DISTINCT, still maximum R-0661, `^Done: R-` still 1. A defect the
    gate or the read turns up is REPORTED in the handback; minting its id
    belongs to the reviewer's next round and not to this one. The handback also
    carries the copy-route trap G5(c) names, so that round can mint it.
 4. THE ROUND MAY ONLY CONFIRM. No file under `apps/`, `packages/`, `tests/` or
    `docs/` is created, edited or deleted, whatever the gate shows. A
    reproducible branch-only failure coupled to F021 code, or a Goal & Done
    clause nothing on disk satisfies, ENDS the round at the handback — its
    repair is a later reviewer-gated round.
 5. RECORD38 IS THE R37 VERDICT AND CARRIES NO READING FROM THIS ROUND'S OWN
    GATE. C2 precedes every gate run this round orders, so R38's own result is
    recorded by the NEXT round's ledger entry (§3 item 31) and travels in the
    handback until then.
 6. THE APPEND CONVENTION for `.agent/live_review.md` at C2: the slice is quoted
    WITHOUT a trailing newline; add EXACTLY ONE newline, then RECORD38, then one
    terminator, so the join carries EXACTLY ONE BLANK LINE. A WHOLE-FILE write
    (PLANF021R38) is the slice PLUS one terminator.
 7. THE LEDGER IS APPEND-ONLY. No landed paragraph, `Gate:` or `Recurrence:`
    entry is edited.
 8. EVERY LEDGER COUNT NAMES ITS PATTERN, ANCHORED. No unanchored count is
    ordered over `.agent/live_review.md`, which quotes the tokens a gate might
    count (R-0630).
 9. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide under R-0622 and is NOT a gate — do not run it. Create and
    merge NO pull request. Push the branch after C5.
10. EXACTLY ONE disposable worktree exists this round, the base-run worktree of
    G5, and it is removed, pruned and its branch deleted before C5. TWO PYTEST
    PROCESSES NEVER RUN AT ONCE (F085 R64) — every suite in this block is
    serial.
11. Block size, measured on these final bytes AFTER the last edit: TOTAL 243
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 200 against DECISION F085 D5's 400. Markers count as prose.
12. C5 IS A ROUND HANDBACK AND CARRIES THIS ROUND'S GATE READINGS, because C2
    could not. Its commit tables earn the ≤100-line tier; a DECISION D15 line
    declares any overage with its mandated cause and NO section is dropped. The
    `+/-` cells of its `## Commits` table are the `git diff --numstat` readings
    and are compared cell by cell against the numbers G7 reports, because a
    value written twice is derived twice (§3 item 28).

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C5; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2, C3 and C4. C5's own reading
     is ordered NOWHERE — §3 item 31 leaves it to the next session.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r38.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over my emitted
     copy at `.remedy-wt/f021-r38.md` are all equal. Write C0b FROM the
     committed C0a blob. Report the digest, bytes and lines. Then extract the
     slices from the COMMITTED C0a blob by their marker LINES, `<<<SLICE ` and
     `<<<END `, and report how many whole texts and how many CONTENT lines your
     extractor printed — numbers YOU measured — re-measuring constraint 11's two
     numerals from that same blob against their caps.
 G3  `.agent/plan.md` at C1 equals PLANF021R38 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0, with a NEGATIVE CONTROL against the bare slice that must
     exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1, and the `wc -l` YOU measure against
     AGENTS.md's "keep it short (<50 lines)". If that count is 50 or more, STOP
     and report — do NOT trim the file to reach it (R-0654).
 G4  THE LEDGER, at C2, every count naming its anchored pattern, base then C2:
     canonical `^- R-\d+ — ` 224 then 224, ALL DISTINCT at both, maximum R-0661
     at both; loose `^- R-` 225 then 225, gap 1 at both; `^Done: R-` 1 then 1;
     `^Gate: R` 36 then 37, DISTINCT at both; `^Gate: R38` 0 then 1;
     `^Recurrence: ` 14 then 14. Report that the number of RECORD38 paragraphs
     opening with the bytes `- R-` is 0, that the base blob is a byte-exact
     PREFIX of the C2 blob, and that the remainder is EXACTLY one newline plus
     RECORD38 plus one newline.
 G5  THE INTEGRATION GATE, executed per docs/agents/integration_gate.md, which
     this block deliberately does not restate. Its evidence lands under
     `.agent/gate_f021_r38/` at C3, every file named `.txt` and never `.log`
     (R-0169). AN EVIDENCE FILE CARRIES THE READINGS AND NOT THE PROGRESS
     OUTPUT: the last twenty lines of a run, its exit code, its wall time, the
     sorted `^FAILED` list, the `comm` outputs and the mtime readings — never
     the thousands of dots `-q` prints, which would push C3 over AGENTS.md's
     500-insertion cap for no evidentiary gain. These additions are ORDERED on
     top of that procedure:
     (a) BRANCH RUN `python3 -m pytest -n auto -q` from the repository root in
         the PRIMARY checkout. Record the raw tail, the sorted `^FAILED` list,
         the exit code and the wall time. This run SUBSUMES the four state
         readers `.agent/context.md` scopes to a state round, because it is
         strictly larger; run the canary `python3 -m pytest
         tests/cli/test_golden_path.py -q -rf` separately and serially anyway,
         as verification tier 2 requires of every handback, and report both
         numbers YOU measure.
     (b) BASE RUN at the merge base. Resolve it yourself with `git merge-base
         main HEAD` and report what you resolved. Create the worktree ON A
         BRANCH — `git worktree add -b tmp/f021-r38-base
         .remedy-wt/base-gate-f021-r38 <merge-base>` — because the self-dogfood
         guard refuses a detached HEAD by design.
     (c) PARITY BEFORE THE BASE RUN, BY THE BUILD ROUTE AND NOT THE COPY ROUTE.
         Copy ONLY `apps/ui/node_modules` from the primary checkout into that
         worktree with `shutil.copytree(src, dst, symlinks=True)`. THE
         `symlinks=True` ARGUMENT IS ORDERED, NOT OPTIONAL: `copytree` defaults
         to `False` and dereferencing npm's bin shims once CAUSED seven of the
         base-only failures the parity exists to prevent (R-0591). Report the
         number of symlinks under `apps/ui/node_modules/.bin` in the copy and in
         the primary checkout, and that the two agree. DO NOT COPY
         `apps/ui/dist`: it is built from BRANCH sources, so the base run
         rebuilds it mid-flight and the content-identity checks watch their own
         assets change under them. The reviewer executed exactly that copy route
         at `24a6b899`, in a worktree it created for the purpose and has since
         removed and pruned, and measured 78 base-only failures from it. Take
         the second route docs/agents/integration_gate.md step 3 offers instead:
         `npm run build` — `vite build` — inside the base worktree BEFORE the
         base run, so `apps/ui/dist` there corresponds to base sources. Report
         that build's exit code and the digests it produced.
     (d) NEUTRALIZE THE AUTO-BUILD with `REMEDY_UI_NO_AUTO_BUILD=1` for the base
         run and VERIFY IT BY THE EVENT, NOT THE OUTCOME (R-0444): record the
         mtime of every file under the BASE worktree's `apps/ui/dist` before and
         after that run, and report the run window together with both readings.
         ANY mtime falling inside the window VOIDS the parity claim and forces
         per-id attribution under (g) — which §3 item 27 makes unconditional
         anyway, so nothing about (g) turns on this reading. Report the content
         digests BESIDE the mtimes and never instead of them: equal content with
         a moved mtime is a byte-identical rebuild rather than an absent one,
         and only the two together say which happened.
     (e) LOGS: while a suite runs its log is written OUTSIDE the repository
         worktree and copied into `.agent/gate_f021_r38/` only after that run
         exits (R-0176). `~/remedy-gate-scratch/` is writable — the reviewer
         wrote and read a probe file there at `24a6b899` — and reading it back
         needs Python rather than a shell pager in this session class.
     (f) COMPARE with `comm -13 base_failed.txt branch_failed.txt` for the
         branch-only ids and `comm -23` for the ids the branch fixed or the base
         lacks. Report BOTH counts YOU measure and BOTH lists.
     (g) ATTRIBUTION IS UNCONDITIONAL AND RUNS IN BOTH DIRECTIONS (§3 item 27).
         EVERY `comm -23` id is attributed to the environment class by direct
         evidence naming the missing artifact for that id, whether or not the
         parity claim held; an unattributed one counts as a genuine base failure
         and BLOCKS the verdict. EVERY `comm -13` id is re-run SERIALLY by its
         exact node id and classified per that file's step 4. Take every node id
         from `python3 -m pytest --collect-only -q`, never by regex over a `-v`
         run, because a parametrized id can hold whitespace (R-0611).
     (h) REMOVE and PRUNE the worktree and DELETE `tmp/f021-r38-base`, and prove
         both with `git worktree list` and `git branch --list 'tmp/*'`.
     (i) Wall clock over about five minutes on either run is NOTED for a perf
         pass, per that file's step 5. It is not a blocker.
 G6  THE ACCEPTANCE READ, at C4, into `.agent/gate_f021_r38/acceptance_read.md`.
     Read the `## Goal & Done` and `## Acceptance` sections of
     `docs/roadmap/features/T5_F021.md` and split them into their individual
     clauses. The file names the SHA it read the tree at, and gives one row per
     clause carrying: the clause by its distinguishing words; the PATH plus the
     SYMBOL on disk that satisfies it, never a bare line number (§3 item 9); and
     one of three statuses. SATISFIED additionally names the test NODE ID that
     pins it, taken from `--collect-only -q` as in G5(g). SATISFIED-WITHOUT-A-
     TEST names the path and symbol and the reason no suite in this repository
     reaches it — no DOM environment and nothing here renders CSS are the two
     this branch already knows. UNSATISFIED names what is missing, and it STOPS
     the round under constraint 4 rather than being built. Report the number of
     clauses YOU split the two sections into and the count in each status.
 G7  STRUCTURE. `git diff --name-only 24a6b899..HEAD` at C4 and again at C5:
     report the count YOU measure at each, and that every path either is one of
     `.agent/authored/f021-r38.md`, `.agent/last_block.md`, `.agent/plan.md` or
     `.agent/live_review.md`, or is `.agent/handoff.md` at C5, or begins with
     `.agent/gate_f021_r38/`, with NO path outside those classes. As many
     commits as the `Bundle:` list names, every one single-parent; `git show
     --numstat` and `git diff --numstat` agree cell by cell; insertions under
     500 for every commit BEFORE C5, each number reported, C5's own left to
     the next round (§3 item 14). Marker sweep, LINE-ANCHORED, 0 for each of
     `<<<SLICE ` and `<<<END ` over `.agent/plan.md` and `.agent/live_review.md`.
     No unanchored `<<<` count is ordered over either (R-0630). Reflog read BY
     OPERATION: every one of this round's rows is `commit`, with `amend`,
     `rebase` and `cherry` 0 each in that field. `gh pr list --state open`
     reported verbatim; it must print `[]`, and NEITHER `gh pr create` NOR `gh
     pr merge` is run this round.

<<<SLICE PLANF021R38
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
R38 is the INTEGRATION-GATE round, the first of the three that close F021. The
full suite runs at the branch tip and at the merge base in a disposable worktree
per docs/agents/integration_gate.md, and the feature file's Goal & Done is
resolved clause by clause to the path, symbol and test node id that satisfy it.
The round MAY ONLY CONFIRM: it writes no product code, mints no finding id, and
hands back on the first branch-only failure coupled to F021 code or the first
clause nothing on disk satisfies. R37's PASS is recorded at C2.

## Next Steps
1. The evidence round, then the STATUS-commit round
   (docs/roadmap/STATUS_closure_protocol.md; the two are never one round).
2. The pull request, opened at closure and merged only at the Open PR Gate.

## Risks
- A green gate is not an accepted feature. Only the clause-by-clause read can
  show that an acceptance criterion has nothing on disk behind it, and a suite
  that passes says nothing about a criterion no test reaches.
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK.
- Nothing here renders CSS. R-0661's pin proves the unresolved-property SET has
  not grown; it cannot prove any rule's computed value.
- `npm run lint` is RED tree-wide under R-0622, still open.
- No code defect of F021 is open. R-0364, R-0369, R-0402, R-0403, R-0419,
  R-0439, R-0587, R-0607 through R-0609, R-0611, R-0613, R-0618, R-0622,
  R-0629, R-0630, R-0644, R-0651, R-0653 through R-0659 and R-0661 stay routed
  to a paydown branch.
<<<END PLANF021R38

<<<SLICE RECORD38
Gate: R38 — the R37 entry. R37 PASSED ON EVERY GATE, EACH RE-MEASURED BY THE REVIEWER FROM THE COMMITTED BLOBS RATHER THAN READ BACK FROM THE HANDBACK, AND IT DECLARED ONE DEVIATION, WHICH IS ACCEPTED. TRANSPORT HELD at sha256 `6c329bba6c6d3765471d3c34d504f35140d5f63fae047d6b00e7305545e9e045` over 15202 bytes and 168 lines, equal across `.agent/authored/f021-r37.md` at `e14f399e`, `.agent/last_block.md` at `12d1a17d` and the working copy the reviewer read at `24a6b899`; my extractor printed 2 whole texts over 47 CONTENT lines beside 4 marker lines, so TOTAL 168 against DECISION F085 D6's 490 and PROSE 121 against D5's 400, both equal to that block's constraint 10. THE PLAN WRITE HELD: `.agent/plan.md` at `51133c1e` is byte-equal to PLANF021R37 plus one terminating newline and NOT to the bare slice, `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 44 under AGENTS.md's 50. THE APPEND HELD: at `a39fa546` the `dc9e72bf` blob is a byte-exact PREFIX of the C2 blob and the remainder is EXACTLY one newline plus RECORD37 plus one newline over 4826 bytes, with 0 of RECORD37's 2 paragraphs opening with the bytes `- R-` and one blank line at the join. THE SETS DID NOT MOVE: canonical `^- R-\d+ — ` 224 then 224, all DISTINCT at both, maximum R-0661 at both; loose `^- R-` 225 then 225; `^Done: R-` 1 then 1; `^Gate: R` 35 then 36, DISTINCT at both; `^Gate: R37` 0 then 1; `^Recurrence: ` 13 then 14; `^Recurrence: R-0629 — ` 1 then 2, which is the second instance of a destructive control whose uniqueness readings disagree and which the WORKER found in the reviewer's own R36 block; `^- R-0629 — ` 1 then 1. THE SUITES WERE RE-RUN BY THE REVIEWER, SERIAL, IN THE PRIMARY CHECKOUT: the four state readers of `tests/ui_server/`, `tests/orchestration/test_test_runner.py`, `tests/regression/test_resource_safety.py` and `tests/orchestration/test_integrity_gate.py` 528 passed, and the canary `tests/cli/test_golden_path.py` 42 passed. STRUCTURE: five commits over `dc9e72bf..24a6b899`, every one single-parent, `git show --numstat` and `git diff --numstat` agreeing cell by cell on all five, insertions 168, 120, 19, 4 and 49, each under 500; the path set is exactly the four non-handoff `Change:` paths at `a39fa546` and those plus `.agent/handoff.md` at `24a6b899`, both set differences EMPTY at both readings; the marker sweep is 0 for each of `^<<<SLICE ` and `^<<<END ` over `.agent/plan.md` and `.agent/live_review.md`; every reflog row of the round carries `commit` in its operation field, with `amend`, `rebase` and `cherry` 0 there; `gh pr list --state open` printed `[]`. OWED TO THIS ENTRY BECAUSE C3 COULD NOT STATE THEM ABOUT ITSELF: C3's SHA is `24a6b899` and its insertion count is 49. THE ONE DECLARED DEVIATION IS ACCEPTED: the handback measures 87 lines against the tier its five commits earn, and DECISION D15's stated cause names the five commit tables, the item-status table, the six gate lines, the authored-text section and the session content constraint 9 required — no mandated section was dropped and no transcript was restated in it.
<<<END RECORD38
