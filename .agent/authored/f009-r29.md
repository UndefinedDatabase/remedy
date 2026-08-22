── STEP GATE (the integration gate — F009's full-suite run) — F009 ──
Goal:        Run the integration gate per docs/agents/integration_gate.md: the
             full suite on this branch, the full suite at the merge base
             `ce49348b` in a throwaway worktree with `apps/ui` build parity
             restored, and a per-id attribution of EVERY difference in BOTH
             directions. The round also records the R28 verdict, registers
             R-0644 against the reviewer's own R28 block, and appends the dated
             correction that block's DECISION F009 D25 needs.

Fortschritt: ~98 % (T001 gebaut · T002 gebaut · T003 gebaut und verifiziert:
             beide Kommandos dispatchen, melden sich auf dem SSE-Strom, sind
             import-seitig eingezäunt und jede andere mutierende Route ist
             begangen und beweisbar 405; offen bleiben nur dieses
             Integrations-Gate und die zwei Closure-Runden) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 register R-0644 ·
             C3 the R28 verdict · C4 the D25 correction · C5 the gate evidence ·
             C6 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r29.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2 and
             C3) · `.agent/decisions.md` (C4) · `.agent/gate_f009_r29/` (NEW,
             C5) · `.agent/handoff.md` (C6). NOTHING under `packages/`,
             `apps/`, `docs/` or `tests/` is touched: this round measures the
             tree, it does not change it.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and is not negotiable. C1
    precedes both ledger commits because the plan must be current before them
    (checklist item 23). C2 precedes C3 because a finding persists in its OWN
    commit BEFORE anything else in the round (§4.4, clause a).
 3. THIS ROUND MINTS R-0644 AND RESOLVES NOTHING. It writes no `Done:` line and
    no `Landed:` line. The next free id is R-0645 when the round ends. R-0644
    was minted only after the reviewer searched the OPEN set for the DEFECT
    rather than for an id (checklist item 30); FINDING644 states inside itself
    which OPEN finding is its nearest neighbour and why that one's clause does
    not reach it.
 4. THIS ROUND HAS NO FROM/TO PAIR. Every authored slice is either a WHOLE-FILE
    replacement (PLANF009R29) or an EOF APPEND (FINDING644, LEDGER29,
    CORRECTD25). Order no containment reading and no FROM count anywhere.
 5. THREE APPENDS, each based on a DIFFERENT commit, and the difference is the
    point. FINDING644 appends to `.agent/live_review.md` at C2 based on the
    ROUND BASE. LEDGER29 appends to `.agent/live_review.md` at C3 based on
    **C2**, not on the round base, because C2 already grew that file — a gate
    that reads C3 against the round base measures two slices and reports one
    (R-0368's class). CORRECTD25 appends to `.agent/decisions.md` at C4 based on
    the round base. The reviewer measured each target at the round base
    `986b40ee5784043a1f75c87d809892b641cb34d3`: `.agent/live_review.md` is
    552059 bytes over 1128 lines and `.agent/decisions.md` is 483709 bytes over
    6953 lines, and EACH ends in exactly ONE newline there. The worker measures
    the third target's newline for itself at C2. So each append is one newline
    followed by its slice.
 6. FINDING644 and LEDGER29 each carry ONE paragraph. CORRECTD25 carries more
    than one; count them with your script rather than from this sentence.
 7. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FIVE of its lines.
    Five is the reviewer's own count of this block's bytes.
 8. SIZE, measured at emission by reading it back out of the assembled bytes and
    computing PROSE as TOTAL minus the slices' CONTENT lines, with marker lines
    counted as prose per DECISION F085 D5: this block is 271 lines TOTAL against
    DECISION F085 D6's 490 cap, 225 of them PROSE against D5's 400. Re-measure
    both from the committed C0a blob; a disagreement is a finding.
 9. THE GATE VERDICT IS NOT YOURS. Report every reading and every attribution;
    do not write the words "integration gate PASSED" anywhere. Only the reviewer
    issues that verdict (docs/agents/integration_gate.md, header).

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C6: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1, C2, C3, C4 and C5. Report the round base
     SHA you read at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r29.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for all three. C0b is written FROM the committed
     C0a blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 8's two numbers from that same blob — TOTAL, and PROSE as TOTAL
     minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R29 — report `cmp` exit and
     both sha256, with a negative control against another file exiting non-zero
     — and `wc -l` against the 50-line cap of AGENTS.md. Line-anchored,
     `^## Goal$` and `^## Next Steps$` each read 1.
 G5  APPENDS, under TWO independent readers, each with a negative control on the
     FIRST appended paragraph (finding R-0631). Run this THREE times, and for
     each state which commit you based it on, exactly as constraint 5 fixes:
     FINDING644 at C2 based on the round base; LEDGER29 at C3 based on **C2**;
     CORRECTD25 at C4 based on the round base. For each: (a) the base blob is a
     byte-exact PREFIX and the remainder equals a newline plus that slice —
     report its sha256, bytes and lines; (b) N is counted BY YOUR SCRIPT and the
     last N blank-line units equal the slice's N paragraphs IN ORDER. Then flip
     one printable byte in the FIRST appended paragraph, at equal length, and
     report that BOTH readers REJECT the flip while both ACCEPT the true file.
     Report before/after bytes and lines for each of the three.
 G6  Line-anchored at line START over `.agent/live_review.md` at the round base,
     at C2 and at C3 (finding R-0630): a leading `- R-` id with every captured
     id DISTINCT at each; a leading `Done: R-` id; a leading `Landed: `; a
     leading `Gate: R` key over that many DISTINCT keys; the `Gate: R29` key;
     and a leading `- R-0644` entry. The reviewer's base readings, which yours
     must reproduce: entries 209, `Done:` 3, `Landed: ` 0, `Gate: R` keys 28,
     `Gate: R29` 0, `- R-0644` 0, max REGISTERED id R-0643, open 206. Report the
     max REGISTERED id and the open count by DECISION F009 D10's rule at all
     three points. Read every one of these at line START and not as a bare
     substring: this file legitimately QUOTES ids and gate keys inside its own
     verdict prose, so an unanchored scan reports a maximum that was never
     registered (finding R-0630).
 G7  BRANCH RUN, step 1 of docs/agents/integration_gate.md. From the repo root:
     `python3 -m pytest -n auto -q`. Record the REAL exit code, the wall time,
     the raw tail, and the full `FAILED` list sorted into `branch_failed.txt`.
     THE RAW LOG IS WRITTEN OUTSIDE THE REPO WORKTREE while the suite runs —
     `~/.cache/remedy-gate-f009-r29/` — because a log growing INSIDE the repo
     changes the worktree digest mid-run and fails the manifest-identity ids as
     FALSE positives (R-0176). PROBE that directory's writability at step 0 and
     report the result whichever way it falls. If it is NOT writable, use
     `.remedy-wt/gate-scratch/` instead, declare the substitution in the
     handback, and additionally attribute by direct evidence any
     manifest-identity or digest id that then appears in the branch-only set.
     The reviewer collected 17592 tests at the round base and predicts no
     pass count, no failure count and no duration: report the numbers the run
     itself printed.
 G8  BASE RUN, step 2. `git worktree add -b tmp/base-gate-f009r29
     .remedy-wt/basegate ce49348b8f5b0374417f5b6c47d8c04966e7108e` — ON A
     BRANCH and NEVER detached, because the self-dogfood branch guard refuses a
     detached HEAD by design and a detached base worktree fails the
     guard-dependent ids (DECISION D3). `ce49348b` is `git merge-base
     origin/main HEAD`, which the reviewer measured at the round base. RESTORE
     BUILD PARITY BY COPYING, never by symlinking, from the primary checkout:
     `shutil.copytree(src, dst, symlinks=True)` for `apps/ui/node_modules` and
     again for `apps/ui/dist`. `symlinks=True` IS THE ORDER AND NOT THE DEFAULT:
     `copytree` defaults to `symlinks=False`, which DEREFERENCES npm's bin shims
     and manufactures exactly the base-only failures the parity exists to
     prevent (finding R-0591). The reviewer confirmed the shims are real
     symlinks in the primary checkout at the round base — `.bin/vite`,
     `.bin/node-which`, `.bin/update-browserslist-db` and
     `.bin/baseline-browser-mapping` among them. Set `REMEDY_UI_NO_AUTO_BUILD=1`
     for the base run but do NOT trust it alone: take a recursive sha256 over
     `apps/ui/dist` in the base worktree BEFORE and AFTER that run and report
     both digests; a changed digest VOIDS the parity claim and you say so.
     Same command, same records, `base_failed.txt`. Then `git worktree remove
     --force`, `git worktree prune`, delete `tmp/base-gate-f009r29`, and report
     `git worktree list` at 1 line before C6.
 G9  COMPARE AND ATTRIBUTE, steps 3 and 4. `comm -13 base_failed.txt
     branch_failed.txt` is the branch-only set; `comm -23` is the other
     direction. ATTRIBUTE EVERY ID IN BOTH SETS BY DIRECT EVIDENCE, WHETHER OR
     NOT THE PARITY DIGESTS MATCHED — this obligation is UNCONDITIONAL and does
     not discharge on a held parity claim (finding R-0590,
     docs/agents/integration_gate.md step 3). For each branch-only id: re-run
     that exact node id SERIALLY; a serial PASS is the xdist-flake class,
     recorded and not a blocker; a serial FAIL is reproduced at
     `ce49348b8f5b0374417f5b6c47d8c04966e7108e` before the feature is blamed;
     and a reproducible branch-only failure coupled to feature code is a
     BLOCKER — STOP, write the handback, create no further commit beyond C5 and
     C6, and do not proceed. For each `comm -23` id: name the missing build
     artifact or the fixed defect, per id. An UNATTRIBUTED id in either set
     blocks the gate verdict. Report the size of both sets as the numbers your
     commands printed, and report the branch-only flake-class count whichever
     way it falls — the reviewer owes an operator flake-debt line above 10
     (planner_reviewer_prompt.md §2).
 G10 EVIDENCE, C5. Copy into `.agent/gate_f009_r29/`, AFTER both runs have
     exited and never during one: `branch_failed.txt`, `base_failed.txt`,
     `branch_only.txt`, `base_only.txt`, `attribution.txt` (one line per id in
     both sets, with its classification and its evidence) and `summary.txt`
     (both exit codes, both wall times, both raw tails, the two `apps/ui/dist`
     digests, the collected count each run printed). Evidence files are named
     `.txt` and NEVER `.log`: `.gitignore` drops `*.log` silently and the
     review-zip guard rejects any `\.log$` member (R-0169). The RAW logs stay in
     the scratch directory and are NOT committed; name their path and their line
     counts in the handback. If C5's insertions would exceed the 500-line cap of
     AGENTS.md DECISION F104 D1, SPLIT it by whole file into C5a, C5b and so on,
     keep every other constraint, and declare the split — do not truncate an
     evidence file to fit.
 G11 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` in the
     PRIMARY checkout, serially, never while another pytest process is alive
     (finding R-0518). Report its REAL exit code and the count IT printed. This
     is tier 2 of planner_reviewer_prompt.md §3 and is owed at every handback
     independently of the full-suite run above.
 G12 RANGE: the range from the round base to C5 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and 0 paths beginning `packages/`, `apps/`, `docs/` or
     `tests/`, which is this round's measure-only constraint as a measurement.
     Each commit has ONE parent; `git show --numstat` and `git diff --numstat`
     AGREE on every cell — invoke `git show` WITHOUT a `--` before the SHA,
     which turns it into a pathspec and prints nothing; every cell equals the
     `+/-` column of the handback's `## Commits` table (checklist item 28),
     compared cell by cell. Report each pre-handback commit's insertions against
     the 500 cap; the handback commit's own numbers belong in the round report
     (item 14). Leading `<<<SLICE ` and `<<<END ` read 0 LINES in every file a
     slice lands in, which are `.agent/plan.md`, `.agent/live_review.md` and
     `.agent/decisions.md`. `git ls-files .remedy-wt` reads 0. Classify THIS
     ROUND's reflog rows by the operation before the first `:` and report
     `amend`, `rebase` and `cherry` each 0; assert no total over the whole
     reflog (R-0601).
 G13 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3, C4, C5 and C6, the round base SHA, one line per gate with the
     transcripts in the round report and not in the file (R-0582), and this
     block's `Fortschritt:` line VERBATIM across all five of its lines. Report
     its `wc -l` against the 100-line cap AGENTS.md allows for a per-commit
     table of more than five commits, which the commit sequence constraint 2
     fixes is. EVERY numeral this file states about the round's own measurements
     is COUNTED mechanically before it is written, or no numeral is stated and
     the enumeration speaks (R-0404, R-0641).

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C6.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R29
# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI-exposed catalog subset, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through their
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R29 records the R28 verdict, registers R-0644 against the reviewer's own R28
block and appends the dated correction DECISION F009 D25's route inventory
needs, then runs the integration gate per docs/agents/integration_gate.md: the
full suite on this branch, the full suite at the merge base `ce49348b` in a
throwaway worktree with `apps/ui` build parity restored, and a per-id
attribution of every difference in both directions. T001, T002 and T003 are
built and verified; this is the last gate before closure.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md, in TWO rounds: the
   evidence job and a FRESH review zip first, then the authored STATUS line and
   the pull request.

## Risks
- Closure needs TWO rounds, not one: the evidence-and-zip round produces the
  values the STATUS line quotes, and a separate round commits that line. Ending
  right after a verdict strands it (DECISION F085 D9).
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- A reproducible branch-only failure coupled to feature code is a BLOCKER, and
  its fix is its own reviewer-gated round (integration_gate.md step 4).
<<<END PLANF009R29

<<<SLICE FINDING644
- R-0644 — Low — A REVIEWER-AUTHORED DECISION STATED THE COUNTS OF A SOURCE FILE'S ROUTES AND THE SOURCE CONTRADICTS THEM, IN A RECORD THAT IS APPEND-ONLY. The defect is the reviewer's, in the F009 R28 block saved at `f9f688d7`, and it landed verbatim in `.agent/decisions.md` at `51caddcb` as the opening paragraph of DECISION F009 D25, which the worker was right to apply unedited under that block's constraint 1. That paragraph says it was "Measured by the reviewer at `a164317b`, before this round was delegated, by reading `do_GET` end to end rather than by grepping it", then states that the server dispatches "four routes by a bare `path ==` or prefix comparison, thirteen job endpoints out of a single `handlers` dict literal, and six more STRUCTURALLY", and concludes that "an AST scan for `path ==` literals alone therefore finds four of twenty-three". The reviewer re-took the reading mechanically at `a164317b`, with the same AST predicate the round's own test uses: the literal-equality set is `/`, `/api/state` and `/api/layers` — THREE, not four, the remaining route in that clause being the `path.startswith("/assets/")` prefix, which no literal scan can reach, so the scan finds three; the `handlers` dict yields thirteen, which is right; and the structural routes the same sentence enumerates — `events-since`, `events/stream` and the three `nodes/<node>/…detail` routes — are FIVE, which is also exactly what `_walkable_paths` walks, so the walk covers twenty-two paths and sixty-six requests rather than twenty-three. WHY THIS IS LOW: nothing consumed the numerals. `LITERAL_GET_ROUTES` holds the correct three, the drift test compares the derived set against that three and passes, and D25's argument — that a literals-only inventory comes back confidently small and WRONG — is unchanged and slightly stronger at three of twenty-two than at four of twenty-three. WHY R-0392 DOES NOT REACH THIS, stated because it is the nearest OPEN neighbour and checklist item 30 requires the open set to be searched for the DEFECT before an id is minted: R-0392 is also a DECISION miscounting sites in a source file, but its cause and its fix clause are a `grep -c` whose own pattern swallowed the `def` line, and the standing rule it carries is R-0391's — count the WRITERS of a field mechanically before authoring against them. D25's numerals were not grep-derived at all; the paragraph expressly claims a hand reading, and a hand reading is the method R-0402's rule already forbids for a numeral. The gap this instance exposes is in §3 item 20, which makes a slice asserting a fact about a source file name the SHA its reading was taken at, and which is silent on whether that reading was ever mechanically TAKEN — so a reviewer who names the SHA has satisfied item 20 with a recollection, which is the one thing the checklist exists to prevent. STANDING RULE FROM HERE: a slice asserting a COUNT about a file outside the block names the SHA per item 20 AND has that count produced by a script at that SHA in the same pre-emission pass that measures the block's own size, or it states the enumeration and NO numeral at all (R-0402). The landed paragraph is NOT rewritten: this round appends a dated correction beneath D25 instead, because that record is append-only and a dated wrong sentence with a correction under it is worth more than a silently repaired one (§3 item 20). OPEN.
<<<END FINDING644

<<<SLICE LEDGER29
Gate: R29 — the R28 entry. R28 PASSED. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced; the round's one substantive defect is the reviewer's own block text, registered above as R-0644 and not counted against the round. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r28.md` at `f9f688d7`, `.agent/last_block.md` at `25d80e3a` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f009-r28.md`, are all sha256 535237356e288114fd0a99e2fbcea8c03862da88bee93132e59eba0c78cd7500 over 35494 bytes and 431 lines, compared against the emitted original rather than against a recorded digest. The reviewer's own extraction out of the committed C0a blob prints an aggregate of 6 slices over 189 CONTENT lines, and constraint 8's numerals re-measure as 431 TOTAL and 242 PROSE, both under DECISION F085 D6's 490 and D5's 400. `.agent/plan.md` at `3453b271` is BYTE-EQUAL to that round's PLANF009R28 slice, 37 lines against the 50-line cap, with `^## Goal$` and `^## Next Steps$` each reading 1 and a negative control against another file differing. THE APPLICATION IS PROVED IN THE STRONGEST FORM AVAILABLE, which is stronger than the gate the block ordered: the reviewer applied the COMMITTED WALK pair to the COMMITTED base blob with its own script and the result is BYTE-IDENTICAL to `tests/ui_server/test_command_channel.py` at `aa2b9048`, so no line of it was hand-edited, reflowed or reconciled anywhere in the round; base FROM reads 1 whole-line and 1 indent-agnostic with the two agreeing and TO reads 0, at C5 FROM reads 1 and TO reads 1, the containment reading printed `true`, and no FROM-zero count was ordered for an append-shaped pair. ORDERED EQUALITY HOLDS IN ITS POSITIONAL FORM: the region C5 inserts is 135 lines and equals the WALK_TO slice's first 135 lines IN ORDER as a list compare, `git show --numstat` reads 135 and 0, and the reviewer's own first alignment of the diff differed only because a blank line either side of the insertion point is interchangeable — a property of the differ, not of the bytes. ALL THREE APPENDS HOLD UNDER THE REVIEWER'S OWN TWO READERS, AND THE ONE THAT MATTERS MOST IS THE SECOND: FINDING643 at `72da8f6c` is based on the round base, 544465 to 546975 bytes and 1124 to 1126 lines, N counted at 1 BY THE SCRIPT; LEDGER28 at `4288bc91` is based on **C2** rather than on the round base, exactly as constraint 5 fixed, its base blob reading 546975 bytes and 1126 lines — the reading a round-base comparison would have got wrong by one whole slice — going to 552059 bytes and 1128 lines, N counted at 1; DECISION25 at `51caddcb` is based on the round base, 480292 to 483709 bytes and 6939 to 6953 lines, N counted at 7 BY THE SCRIPT. In all three an equal-length printable-byte flip in the FIRST appended paragraph makes BOTH readers REJECT while both ACCEPT the true file. THE SETS HELD line-anchored at line start across all THREE points: at the round base entries 208 all DISTINCT, `Done:` 3, `Landed: ` 0, `Gate: R` keys 27 over 27 DISTINCT, `Gate: R28` 0 and a leading `- R-0643` entry 0, max REGISTERED id R-0642, 205 open; at C2 entries 209 all DISTINCT with `- R-0643` at 1, max id R-0643 and 206 open; at C3 the `Gate: R` keys reach 28 over 28 DISTINCT keys with `Gate: R28` at 1 and 206 open. The ledger header was compared against the series it joins and `Gate: R28 — the R27 entry.` matches it. THE SUITES ARE THE REVIEWER'S OWN, re-run serially in the primary checkout: ruff over the changed path EXITS 0 at "All checks passed!", `test_command_channel.py` EXITS 0 at 100 passed, the canary EXITS 0 at 42 passed, and the four-path state-reader group EXITS 0 at 527 passed. THE RED PROOF IS THE REVIEWER'S OWN, re-run in a disposable worktree at `aa2b9048` under the ONE selection R28's G10 names — `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`, the whole file, no `-k` — with the unmutated baseline taken first at exit 0 and 100 passed. Each ordered FROM occurs 1 time whole-line and 1 indent-agnostic with the two agreeing, and each mutation was reverted to a file byte-equal to its C5 blob before the next. All three ordered sets reproduce EXACTLY and not merely as subsets: opening `do_PUT` reddens exactly `test_an_unknown_path_is_405_for_every_mutating_method`, `test_every_route_the_server_serves_refuses_post_put_and_delete` and `test_put_is_405_even_on_the_commands_path`; loosening the commands-path condition reddens exactly `test_a_near_miss_of_the_commands_path_is_405`; and adding an undeclared literal route to `do_GET` reddens exactly `test_the_walk_knows_every_route_the_source_dispatches`. THAT THIRD MUTATION IS THE ONE WORTH RECORDING: it proves the walk cannot silently stop covering the server, which is how a route-walking test usually dies, and it is why the drift test was written rather than assumed. IT ALSO SETTLES R-0643 IN PRACTICE: that finding's rule is that an expected-failure set names the selection it is measured under, R28's G10 is the first gate written under it, and naming the whole file is what made all three sets reproduce exactly instead of approximately. THE RANGE HELD: the range base→`aa2b9048` lists exactly the declared paths, set difference EMPTY in both directions, and 0 paths beginning `packages/`, `apps/` or `docs/`, which is that round's no-production-code constraint as a measurement; every commit has ONE parent; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own table, at 431/0, 273/280, 13/13, 2/0, 2/0, 14/0 and 135/0; pre-handback insertions 431, 273, 13, 2, 2, 14 and 135, every one under the 500 cap; zero leading `<<<SLICE ` and `<<<END ` LINES in all four slice targets; `git ls-files .remedy-wt` 0; this round's 8 reflog rows all classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree and a clean tree at the verdict. THE HANDBACK IS 84 LINES against the 100 AGENTS.md allows a per-commit table of more than five commits, so R-0582's repair has now held for three rounds running.
<<<END LEDGER29

<<<SLICE CORRECTD25
## CORRECTION to DECISION F009 D25 — its route inventory, re-measured (2026-08-22)

D25's opening paragraph gives the inventory as "four routes by a bare `path ==` or prefix comparison, thirteen job endpoints out of a single `handlers` dict literal, and six more STRUCTURALLY", and concludes "an AST scan for `path ==` literals alone therefore finds four of twenty-three". Re-measured at `a164317b` by script, with the same AST predicate `_do_get_route_facts` uses in `tests/ui_server/test_command_channel.py`: the literal-equality set is `/`, `/api/state` and `/api/layers` — THREE — the `/assets/` route being a `startswith` prefix no literal scan can reach; the `handlers` dict yields thirteen; and the structural routes are the FIVE that same sentence enumerates, which is also exactly what `_walkable_paths` walks. So the walk covers twenty-two paths and sixty-six requests, and a literals-only scan finds three of twenty-two.

Every CHOSEN clause of D25 stands unchanged, and so does its argument: a literals-only inventory still comes back confidently small and wrong, at three of twenty-two rather than four of twenty-three. Registered as finding R-0644. The original paragraph is left standing rather than repaired, because this record is append-only (docs/agents/planner_reviewer_prompt.md §3 item 20).
<<<END CORRECTD25
