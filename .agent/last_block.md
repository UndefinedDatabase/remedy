── STEP R2/1 — F008 SSE event stream ─────────────────────────
Goal:        Record the R1 verdict and repair the red R1 could not fix.
             R1's own block ordered the F008 claim while forbidding every
             path under tests/, and one line of tests/docs/ pins F008 to
             the UNSTARTED marker — so the claim and the gate were
             mutually unsatisfiable and the worker was right to stop. This
             round retires that pin in favour of the invariant the
             workflow actually holds, and records R1 in the ledger.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 record the R1 verdict · C3 repair the F008 pin ·
             C4 write the handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r2.md              (C0a, new file)
             - .agent/last_block.md                    (C0b, full rewrite)
             - .agent/plan.md                          (C1, full rewrite)
             - .agent/live_review.md                   (C2, append only)
             - tests/docs/test_docs_consistency.py     (C3, the pin pair)
             - .agent/handoff.md                       (C4, full rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r2.md, extracted by its marker lines. No slice is
    retyped, rewrapped, reflowed or edited. A slice that looks wrong is
    APPLIED AS WRITTEN and the objection goes in the handback.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines
    strictly between its `<<<SLICE X` and `<<<END X` markers. PLANF008R2,
    PINFROM and PINTO are applied with their trailing newline INCLUDED —
    PINFROM and PINTO are whole-line blocks, so including the terminator
    is what keeps the surrounding indentation intact. RECORDR1 is applied
    as `\n` plus its single line, appended to the end of the record after
    exactly one blank line, and the file ends with exactly one newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4. `.agent/plan.md`
    is advanced at C1, the first substantive commit — only the two
    block-save commits may precede it (checklist item 23).
 4. Pair shape, from a containment test the reviewer ran before emission.
    PINFROM/PINTO: `TO contains FROM: false` — therefore a REWRITE, so the
    obligation is FROM 1x→0x and TO 0x→1x in
    tests/docs/test_docs_consistency.py, and NO append reading is owed.
 5. The C3 edit replaces ONLY the two lines PINFROM names. The line
    `        assert re.search(r"^- \[x\] F017 —", text, re.M)` that follows
    them is NOT part of the pair and stays exactly where it is.
 6. Destructive checks (G9) run ONLY inside a disposable git worktree
    created with `git worktree add .remedy-wt/redctl-r2 <C3 sha> --detach`,
    never in the primary checkout, and the worktree is removed with
    `git worktree remove .remedy-wt/redctl-r2 --force` before the handback.
    `git status --porcelain` is empty after every commit and at the
    handback.
 7. Two pytest processes never run at once. G8, G10 and G11 run in the
    PRIMARY checkout. G9 runs in the worktree of constraint 6: the
    reviewer measured `tests/docs/` passing at 295 inside a fresh
    worktree, so that suite needs no `apps/ui/node_modules` and this is
    not the R-0518 case.
 8. No production code. No path under packages/ or apps/ is touched. The
    ONE tests/ path in the Change set is the pin this round exists to
    repair; nothing else under tests/ is touched.
 9. An assertion is never weakened to buy a green. PINTO is strictly
    STRONGER than the sentence it retires: the reviewer proved in a
    disposable worktree that it goes red both when NO feature is claimed
    and when a SECOND one is, where the retired pin could only catch the
    first. If you disagree, apply it as written and say so in the
    handback.
10. The reviewer's readings before this block was emitted, so a
    pre-existing state is not read as this round's: at `05894327`
    `python3 -m pytest tests/docs/ -q -rf` exits 1 at 1 failed and 294
    passed; `tests/orchestration/test_roadmap_index.py` exits 0 at 30
    passed; the state-reader four exit 0 at 160 passed; the canary exits 0
    at 42 passed; `ruff check tests/docs/test_docs_consistency.py` reports
    `All checks passed!`.

Done when:
 G1  `.agent/STOP` is absent, checked immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback; `git worktree list` names the
     primary checkout alone at the handback. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of
     .remedy-wt/f008-r2.md, of .agent/authored/f008-r2.md at C0a and of
     .agent/last_block.md at C0b, and state whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     .agent/authored/f008-r2.md by their marker lines, take the COUNT from
     that listing, and report per slice its newline-INCLUDED sha256, byte
     count and line count.
 G4  Plan. Report the sha256, byte count and line count of .agent/plan.md
     at C1 and whether it is byte-equal to PLANF008R2. Its line count is
     under 50. `## Goal` and `## Next Steps` each occur exactly once as
     line-anchored headings and `F008` occurs at least once. C1 is the
     first commit after C0a and C0b.
 G5  The verdict append, measured two ways that must agree. In
     .agent/live_review.md at C2: (a) the blob at C1 is a byte-exact
     PREFIX of the blob at C2, and the remainder equals `\n` plus RECORDR1
     exactly — report the remainder's sha256, byte count and line count;
     (b) split the C2 file on blank lines with an INDEPENDENT extractor and
     report that its LAST unit equals RECORDR1. Then run a NEGATIVE
     CONTROL: flip one byte of the remainder in memory and report that
     both readings now REJECT it.
 G6  The sets. Report line-anchored counts in .agent/live_review.md at C1
     and at C2: `^- R-\d+ — ` is 183 at both, `^Done: R-\d+ — ` is 0 at
     both, `^Landed: ` is 0 at both — a `Gate:` paragraph is neither kind
     of line. `^Gate: R\d+ — ` reads 1 then 2, the two keys are DISTINCT,
     and `Gate: R2 — the R1 entry.` occurs 0 times at C1 and exactly 1 time
     at C2 as a LINE-ANCHORED reading. No new finding id is minted this
     round: report that `R-0612` occurs exactly 1 time in that file at BOTH
     C1 and C2 — the reviewer measured 1 at `05894327` — and that the sole
     occurrence is the header's `> Next free id: R-0612.` line, so the
     count is unchanged and no `^- R-0612 — ` line exists at either commit.
 G7  The pin pair. In tests/docs/test_docs_consistency.py, count PINFROM
     and PINTO as exact multi-line blocks at `05894327` and at C3: FROM
     reads 1 then 0, TO reads 0 then 1. Report the containment test's own
     output for the pair. Confirm that the line
     `        assert re.search(r"^- \[x\] F017 —", text, re.M)` occurs
     exactly 2 times in that file at BOTH commits: the reviewer measured 2
     at `05894327`, the other at line 281 inside a different test method,
     so this round leaves that count UNCHANGED rather than at one. Report
     both readings.
 G8  The repair, in the primary checkout, run SERIALLY:
     `python3 -m pytest tests/docs/ -q -rf`
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`
     Report each exit code and each passed count. Both exit 0 and the
     first reports 295 passed — the same total as the base, one test
     repaired and none lost.
 G9  Red control, in the disposable worktree of constraint 6 and never in
     the primary checkout, proving the new pin BINDS. At the worktree,
     with C3 applied: (a) rewrite the single line
     `- [~] F008 — SSE event stream` in `docs/roadmap/STATUS.md` to
     `- [ ] F008 — SSE event stream` — the reviewer measured that line
     occurring exactly once in that file at C3 — and report that
     `python3 -m pytest tests/docs/test_docs_consistency.py -q -rf` now
     exits 1; (b) restore that line, then rewrite the single line
     `- [ ] F009 —` to `- [~] F009 —` and report that the same command
     exits 1 again; (c) restore, and report that it exits 0. Report all
     three exit codes and the last line of each run, then remove the
     worktree.
 G10 State-reader gate and canary, in the primary checkout, SERIALLY and
     never alongside G8:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
     Report each exit code and each passed count. Both exit 0.
 G11 Scoped lint. Run
     `python3 -m ruff check tests/docs/test_docs_consistency.py` at
     `05894327` and at C3, reading the base copy WITHOUT writing to the
     tracked file — use `git show 05894327:tests/docs/test_docs_consistency.py`
     piped to `python3 -m ruff check --stdin-filename tests/docs/test_docs_consistency.py -`
     so per-file-ignores still resolve by path. Report each exit code and
     the RULE-CODE MULTISET of each; the two multisets are equal. Do not
     order exit 0 from the count alone.
 G12 Range. With BASE `05894327`, run `git diff --name-only BASE..C4` and
     report that its output equals the Change list above with no path on
     either side alone. Every commit in BASE..C4 has exactly one parent.
     Report each commit's INSERTION count from `git show --numstat`, all
     under 500, and compare those numbers cell by cell against the `+/-`
     column of the handback's `## Commits` table, reporting that the two
     readings agree. C4's own numbers belong to the round report, not to
     its own table cell (finding R-0149).
 G13 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` — the
     line-anchored reading, because RECORDR1 legitimately quotes neither
     but the block mirrors do — in .agent/plan.md at C1,
     .agent/live_review.md at C2, tests/docs/test_docs_consistency.py at
     C3 and .agent/handoff.md at C4. Every count is 0.
 G14 History. Over this round's OWN reflog entries only, report the count
     containing `amend`, `rebase` or `cherry`; it is 0. Do not order that
     every entry read `commit:` (finding R-0601), and do not count an
     unstage as a rewrite (finding R-0608). State NO entry total: this
     round's handback cannot count the entries its own commits create.
 G15 Handback. .agent/handoff.md at C4 carries the sections
     docs/agents/handback_template.md mandates and an item-status table
     naming C0a, C0b, C1, C2, C3 and C4 exactly once each. Report its line
     count; the cap for this round is 100, this round having more than
     five commits.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 4 % (F008 beansprucht · das R21-Urteil und das
            R1-Urteil stehen im Ledger · der Pin, den R1 nicht reparieren
            durfte, ist ersetzt und schärfer als zuvor · die
            Stream-Inventur R3 misst, hat noch nicht begonnen) — Schätzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R2
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, for the next free finding id and for the round map; this file
repeats none of them.

## Goal
A per-job SSE endpoint that streams the event ledger from a cursor — the
ledger's own monotonic seq carried and never renumbered, a 15 s heartbeat, and
Last-Event-ID resume replaying exactly the missed span — plus a client hook
with reconnect backoff, gap detection and an honest polling fallback that
labels itself delayed. DONE when a fake job streams into a test client with
zero gaps across forced disconnects, the client transcript byte-equals the
ledger's envelope sequence, the heartbeat holds cadence, and the fallback
engages on a disabled EventSource and recovers to live.

## Current Step
R2 records the R1 verdict and repairs the red R1 was forbidden to touch. R1
claimed F008 correctly, but one line of `tests/docs/test_docs_consistency.py`
pinned F008 to the UNSTARTED marker, so the claim had to turn that suite red
while R1's own change set excluded every path under `tests/`. This round
replaces that pin with the invariant the workflow actually holds — exactly one
`[~]` entry exists and F008 is its holder — which is strictly stronger than
the sentence it retires. No production code is written here either.

## Next Steps
1. R3 inventories the ground the feature file's "How it fits" section names,
   MEASURED in the source rather than read off the feature file: whether
   ledger entries already carry a monotonic index, how the UI server serves a
   long-lived response and whether it is threaded, what the Part E envelope
   contract fixes, and how the existing state endpoint authenticates.
2. R4 records R3 and rules the stream's shape as a DECISION — threading, the
   heartbeat cadence, the max-connections guard and the fallback's contract —
   before any endpoint is written.
3. R5 onward builds T001, T002 and T003 in the feature file's own order.

## Risks
- The server-capability finding gates everything: the feature file's
  Orchestrator brief dispatches it first, and a stream built on an unthreaded
  stdlib server would block every other request the cockpit makes.
- 183 findings stay open and none is a code defect of F008. R1's red was a
  recurrence of R-0387, not a new id; promoting that finding's clause into the
  §3 checklist edits `docs/agents/**` and is routed to the paydown branch that
  already carries R-0403, R-0607, R-0608, R-0609 and R-0611.
<<<END PLANF008R2

<<<SLICE PINFROM
        # ...and nothing after F012 has been started, except F017 (accepted).
        assert re.search(r"^- \[ \] F008 —", text, re.M)
<<<END PINFROM

<<<SLICE PINTO
        # ...and nothing after F012 has been started except F017 (accepted) and
        # the ONE feature currently claimed. R-0387 recurrence, F008 R1: this pin
        # read `[ ]` F008, so it asserted that NO feature was in progress and the
        # next claim had to break it. The invariant this workflow really holds is
        # that exactly one `[~]` entry exists (planner_reviewer_prompt.md §1), so
        # pin that and name its holder instead.
        in_progress = re.findall(r"^- \[~\] F\d{3} —", text, re.M)
        assert len(in_progress) == 1, f"exactly one feature is in progress, found {in_progress}"
        assert re.search(r"^- \[~\] F008 —", text, re.M)
<<<END PINTO

<<<SLICE RECORDR1
Gate: R2 — the R1 entry. R1'S GOAL IS MET, ITS SEVEN COMMITS ARE ALL CORRECT, AND ITS ROUND GATE IS RED — three independent clauses, all three load-bearing. R1 IS THEREFORE NOT A PASS, because §4 item 6 fixes a round PASS as scoped commands green plus a clean diff and `python3 -m pytest tests/docs/ -q -rf` exits 1 at `05894327`; but NO finding is registered against the worker, and the defect is the reviewer's own block, recorded below as fresh recurrence evidence for R-0387 rather than as a new id. WHAT THE ROUND DELIVERED, re-measured by the reviewer off disk rather than read back out of the handback: pull request #208 merged at the Open PR Gate into the merge commit `7c03adfa`, which is the tip the branch was pulled to and an ancestor of it; F008 claimed in the ledger; the review record reset for the new branch; and the F255 R21 verdict recorded, which is the entry directly above this one and the reason R21's terminator is a terminator rather than a stranded verdict. THE TRANSPORT AND THE SLICES HELD: `.remedy-wt/f008-r1.md`, `.agent/authored/f008-r1.md` at `cb225825` and `.agent/last_block.md` at `be6d50ff` are all sha256 caeb7a6e132513192c7786c3d9bbf9da64bf272ef639ad8c2cd544f23ec08d47 over 24762 B and 357 lines, three-way EQUAL and equal to the digest stated at delegation; SEVEN slices, a count taken from the reviewer's own ordered extraction out of the committed C0a file — PLANF008R1 9f4d537e, LRHEADER bdcba417, GATE1 6fa28da2, STATUSFROM dbd421b5, STATUSTO 9cb58ff9, CONTEXTF008 da39de3b and RESETSCRIPT 1b48eeea. THE PLAN LANDED FIRST at `5c4840e2`, byte-equal to PLANF008R1 over 2390 B and 42 lines, under the 50-line cap, which is checklist item 23 met rather than asserted. THE RESET IS EXACT AND WAS MEASURED THREE WAYS: `.agent/live_review.md` at `3a0fa900` BEGINS with LRHEADER and ENDS with GATE1 byte for byte; its line-anchored counts read 183 registered, 0 `Done:`, 0 `Landed:` and 1 `Gate:`; and the set of ids carried is EQUAL to the set registered-and-unresolved at `8e08c0da`, symmetric difference EMPTY, with all 183 paragraphs byte-equal to their pre-reset originals and a deliberate one-byte flip in R-0361 caught by that same comparison — the negative control without which 183 equalities prove only that the comparison ran. THE CLAIM PAIR APPLIED CLEANLY: in `docs/roadmap/STATUS.md` the FROM reads 1 then 0 and the TO reads 0 then 1 as whole lines between `8e08c0da` and `aa15ab4f`; the count of line-anchored accepted entries is 53 at BOTH, so claiming F008 moved nothing into the accepted set; and README.md is correctly absent from the change set, which is what a claim round owes and a closure round does not. THE RANGE HOLDS: seven single-parent commits over exactly the seven declared paths with no path on either side alone, insertions 357, 340, 31, 17, 31, 68 and 3, every one under the 500 cap; zero marker lines leaked into any target; `.agent/context.md` at `aa15ab4f` byte-equal to CONTEXTF008 and carrying all four assertions the live state readers make of that path; a 99-line handback under its 100-line cap with every mandated section present exactly once; and the tree clean with `git worktree list` naming the primary checkout alone. THE RED, EXACTLY: `tests/docs/test_docs_consistency.py` line 307 at `7c03adfa` asserts `^- \[ \] F008 —` and so pins F008 to the UNSTARTED marker, while the block's own C3 ordered that same line rewritten to `- [~] F008 — SSE event stream` and its constraint 8 forbade every path under `tests/`. The two orders are mutually unsatisfiable by construction — the claim the round exists to make MUST turn that suite red, and the worker was forbidden to repair it. Re-run by the reviewer at `05894327`: exit 1 at 1 failed and 294 passed, which totals the base 295, so exactly one test flipped and none was lost. THIS IS R-0387 HAPPENING AGAIN AND IS NOT A NEW DEFECT, and the open set was searched for the DEFECT before any id was considered, as item 30 requires: R-0387 is OPEN, it states that the reviewer ran pre-emission checklist item 7 too narrowly and that the round ended red because of it, and it names this exact cost — a worker left holding a red suite it was explicitly forbidden to fix. R1 is that defect one degree worse, because item 7 was not run narrowly but not run AT ALL: no grep of the suite for tests reading `docs/roadmap/STATUS.md` preceded the block, and a single line of a single test was the entire guard. R-0387's fix clause reaches only a block that ADDS an entry to an APPEND-ONLY record, and a ledger MARKER rewrite is neither an addition nor append-only, so that clause was true, open, and still did not bind — the R-0452 and R-0454 shape, a rule living in a finding body rather than in the checklist the next block actually reads. THE COUNTER-MEASURE IS WIDER THAN THE REPAIR AND ONLY THE REPAIR LANDS HERE: R2 retires that pin for the invariant the workflow really holds — exactly one `[~]` entry exists and F008 is its holder — which is strictly STRONGER than the sentence it replaces, the reviewer having proved in a disposable worktree that it goes red both when NO feature is claimed and when a SECOND one is, where the old pin could only ever catch the first. Promoting R-0387's clause into §3 item 7 itself edits `docs/agents/planner_reviewer_prompt.md`, a path outside this feature's change set, and is NOT claimed here: it is named for the paydown branch that already carries R-0403, R-0607, R-0608, R-0609 and R-0611, on the precedent R-0493 set for exactly this situation. WHAT THE WORKER DID RIGHT IS WHY THE REPAIR COSTS ONE ROUND AND NOT A FEATURE: it applied the slice as written, did not touch the test, did not weaken an assertion to buy a green, stopped at the handback, and stated the contradiction as an objection under constraint 1 with both halves named — and it then caught a false numeral in its OWN handback, a reflog entry TOTAL of 9 measured before the commit that would make it 10, and struck it in a seventh declared commit rather than leaving it standing or quietly correcting it into a second wrong number. That seventh commit departs from the ordered sequence, is declared with its reason, touches `.agent/handoff.md` alone, and is the right call: a total the reporting file cannot count is the R-0371 class, and striking the numeral rather than correcting it is what checklist item 14 prescribes.
<<<END RECORDR1
