── STEP GATE/3 — F022 Live cost ticker · Runde 15 ────────────────────────────

Fortschritt: ~95 % (T001 fertig · T002 fertig · T003 fertig — diese Runde baut
             nichts, sie MISST: das Integration Gate ueber die ganze Suite, plus
             das R14-Urteil auf Platte) — Schaetzung

Goal:        Run the integration gate exactly as docs/agents/integration_gate.md
             prescribes — branch run, base run at the merge base with restored
             parity, compare, attribute every branch-only id — and record the
             R14 verdict with its two recurrences. This round MEASURES. It fixes
             nothing.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 the R14 verdict and two recurrences · C3 the gate evidence ·
             C4 the handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r15.md    (C0a)
               .agent/last_block.md           (C0b)
               .agent/plan.md                 (C1)
               .agent/live_review.md          (C2)
               .agent/gate_f022_r15/**        (C3, evidence files you author)
               .agent/handoff.md              (C4)

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The whole-text
slices are PLANF022R15 and LEDGER15. This block carries NO FROM/TO pair at all,
so it states no containment reading: there is nothing to classify. Every slice
is quoted WITHOUT its trailing newline; PLANF022R15 replaces its file whole, and
LEDGER15 lands as one newline plus the slice plus one newline.

THE EVIDENCE FILES OF C3 ARE NOT SLICES. They are your own measurements, written
in the shape named below. Only the two `.agent/` texts above are byte-for-byte
transport.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your Change set; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    touches the finding ledger, so the plan advances before anything else but
    the two block-save commits.
 3. COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4 and no other.
 4. NO PRODUCTION CODE, NO TESTS, NO `docs/`. Nothing under `apps/`,
    `packages/`, `tests/` or `docs/` is in the Change set. This round measures
    the suite; it does not repair it. Per docs/agents/integration_gate.md step
    4, a REPRODUCIBLE branch-only failure coupled to feature code is a BLOCKER:
    stop, write the handback naming the id and its evidence, and end the round.
    A repair is its own reviewer-gated round and never this one.
 5. THE BASE WORKTREE IS CREATED ON A BRANCH, never detached:
    `git worktree add -b tmp/f022-r15-base <path> c34ef32b`. The self-dogfood
    branch guard refuses a detached HEAD BY DESIGN, so a detached base worktree
    fails the guard-dependent ids and produces a base failure list that is an
    artefact of the method (DECISION D3, F053 R2). Delete that branch when you
    remove the worktree.
 6. BASE PARITY IS RESTORED BY COPY WITH SYMLINKS PRESERVED. Copy the primary
    checkout's `apps/ui/node_modules` and `apps/ui/dist` into the base worktree
    with `shutil.copytree(src, dst, symlinks=True)` — NEVER symlink the
    directories themselves, and NEVER accept copytree's default. That default is
    `symlinks=False`, which DEREFERENCES symlinks: `apps/ui/node_modules/.bin`
    holds 23 of them, measured by the reviewer at `8d5c73c4`, and dereferencing
    them CAUSED 7 base-only failures at F085 R23 — the parity restore itself
    became the defect (R-0591). Order the argument, not the function.
 7. EVIDENCE FILES ARE `.txt`, NEVER `.log`: `.gitignore` drops `*.log`
    silently and the review-zip guard rejects any member ending `.log` (R-0169).
    While a suite RUNS, its live log is written under `.remedy-wt/`, which is
    gitignored, and copied into `.agent/gate_f022_r15/` only AFTER that run has
    exited — a log growing inside the tracked tree during a run changes the
    worktree digest mid-run and fails the manifest-identity ids as FALSE
    positives (R-0176).
 8. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback.
 9. Every numeral this block states about the ROUND BASE `8d5c73c4` was produced
    by a reviewer script or tool run at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
10. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 296 lines TOTAL with 47 CONTENT
    lines inside its slices, so PROSE is 249 — under DECISION F085 D6's
    490 and D5's 400.

─── What C3 writes ────────────────────────────────────────────────────────────

`.agent/gate_f022_r15/`, modelled file for file on `.agent/gate_f021_r38/`,
which is the last integration gate this repository ran and is on disk to read:

  branch_run.txt   command, cwd, commit, exit code, wall time, the raw tail
  branch_failed.txt  the sorted `^FAILED` lines of the branch run
  base_run.txt     command, cwd, the merge base as `git merge-base` resolved it,
                   exit code, wall time, the raw tail
  base_failed.txt  the sorted `^FAILED` lines of the base run
  parity.txt       what was copied, by which call, with `symlinks=True` shown,
                   and the symlink count in `.bin` on BOTH sides
  auto_build_neutralization.txt  the mtime reading of G9, with the run window
  comm.txt         both `comm` directions with their counts and lists
  attribution.txt  one entry per branch-only id, per G11
  canary.txt       the canary run
  controls.txt     the red controls of G8 and G12
  summary.txt      the gate's own one-page result

Every one of those files names the command that produced it and its real exit
code. A file that states a conclusion without the command that produced it is
the thing this directory exists to prevent.

─── Why this round exists ─────────────────────────────────────────────────────

T003 is complete, so every clause of the feature's Goal now has code answering
it. What no round has measured is whether F022 broke anything ELSE: each round
gated only its own scoped commands, which is the whole point of tier 1, and the
full suite has not run on this branch even once. The integration gate is the
tier-3 run that turns "every scoped gate was green" into "this branch introduces
no failures", and it is the only round permitted to make that second claim.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582) — they belong
in `.agent/gate_f022_r15/`. G1 through G15 run after C3 and BEFORE C4, so the
handback can quote all of them (§3 checklist item 31). The round base is
`8d5c73c4` throughout and the merge base is `c34ef32b`.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C4.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a, C0b, C1, C2 and C3.
 G2  TRANSPORT. sha256 over the block file at `.remedy-wt/f022-r15.md`, over the
     committed C0a blob, over the committed C0b blob and over
     `.agent/last_block.md` on disk: report all four digests, byte counts and
     line counts, and require them EQUAL. The digest the delegation names is the
     fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     Report those against constraint 10's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R15 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, `wc -l` at most 50.
 G5  THE APPEND at C2 into `.agent/live_review.md`, proved twice. Reader (a):
     the C1 blob is a byte-exact PREFIX of the committed file and the remainder
     is exactly one newline plus the slice plus one newline — report the
     remainder's byte count and the slice's. Reader (b), INDEPENDENT: split both
     files on blank lines, let N be the number of paragraphs YOUR script counts
     in the slice, and require the LAST N units of the committed file to equal
     the slice's N paragraphs IN ORDER. Report N; do not take it from this
     block. NEGATIVE CONTROL, in a disposable worktree, applied to the FIRST
     appended paragraph: flip ONE byte at an offset you name and confirm BOTH
     readers reject the mutant while both accept the true file. THE OFFSET IS A
     BYTE OFFSET — the file carries multi-byte em dashes, so a CHARACTER offset
     lands early, outside the appended region, where reader (b) accepts the
     mutant and the control proves nothing. Report the ~20 bytes surrounding the
     flip. Remove the worktree.
 G6  LEDGER INTEGRITY, base versus C2. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-` with its distinct ids, of `^Landed: `, of
     `^Recurrence: R-` with its distinct ids, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and REMOVED as sets. At base the
     reviewer measured 234 records, all distinct, maximum `R-0673`, 2 `Done:`
     lines over `R-0653` and `R-0670`, 0 `Landed:`, 8 `Recurrence:` lines over 8
     DISTINCT ids, and 14 `Gate:` lines over 14 distinct keys. This round MINTS
     NO NEW ID: it is expected to add no record, to take `^Recurrence: R-` to 9
     by gaining a SECOND `R-0672` line — so the count of DISTINCT recurrence ids
     STAYS 8 — and to add exactly the key `R14`. `R-0672` must still occur
     exactly once as a `^- R-\d+ — ` record. Report what you measure.
 G7  THE BRANCH RUN, docs/agents/integration_gate.md step 1, from the repository
     root in the PRIMARY checkout at C2: `python3 -m pytest -n auto -q`. Record
     the raw tail, the FULL `^FAILED` list sorted into `branch_failed.txt`, the
     exit code and the wall time.
 G8  THE BASE RUN, step 2, in the disposable branch worktree of constraint 5 at
     `c34ef32b`, with parity restored per constraint 6 FIRST and
     `REMEDY_UI_NO_AUTO_BUILD=1` set: the identical pytest command. Record the
     same four things into `base_run.txt` and `base_failed.txt`. RED CONTROL for
     the parity restore, reported in `controls.txt`: before copying, count the
     symlinks under `apps/ui/node_modules/.bin` in the base worktree — it must
     be 0, because the directory is absent — and after copying it must equal the
     primary's 23. A restore that cannot be seen to have happened proves
     nothing.
 G9  THE PARITY PROOF, step 3's R-0444 clause, MEASURED BY THE EVENT and never
     by the outcome. Record the mtime of EVERY file under the base worktree's
     `apps/ui/dist` immediately before the base run and again immediately after,
     and report the run's own start and end epoch as the window. ANY mtime
     falling inside that window VOIDS the parity claim and forces per-id
     attribution of every `comm -23` id by direct evidence. A content hash may
     accompany the reading but NEVER stands alone: equal content is consistent
     both with no rebuild and with a byte-identical one, which is the case F009
     R29 actually hit.
 G10 THE COMPARE, step 3. `comm -13 base_failed.txt branch_failed.txt` is the
     branch-only set; `comm -23` is what the base fails and the branch does not.
     Report BOTH with their counts and their full lists. An UNATTRIBUTED
     `comm -23` id counts as a genuine base failure and blocks the verdict.
 G11 THE ATTRIBUTION, step 4, FOR EVERY BRANCH-ONLY ID, unconditionally — do not
     read this gate as discharged by an empty set, report the empty set as the
     reading it is. Re-run each id SERIALLY by its exact node id and classify:
     serial-pass is the xdist-flake class and is RECORDED, not a blocker;
     serial-fail is reproduced at `c34ef32b` before the feature is blamed; a
     reproducible branch-only failure coupled to feature code is a BLOCKER and
     ends the round under constraint 4. Where an id passes serially, run it at
     least 10 times before calling it a flake — 5 of 5 is not determinism.
 G12 THE CANARY, serial, primary checkout at C2:
     `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer measured
     42 at the round base. RED CONTROL, reported in `controls.txt`: in a
     disposable worktree, break one assertion in that file on purpose and
     confirm the command really goes red, then discard the worktree. A command
     that cannot fail proves nothing when it passes.
 G13 STRUCTURE, reported for the commits BEFORE C4 and for the range as a whole
     (C4's own numbers belong to the next round's ledger entry, not here):
     every commit single-parent; each commit's INSERTION count, each under the
     500 cap; the range path set against the Change set above with the
     difference reported in BOTH directions; `git show --numstat` agreeing cell
     by cell with the handback's `## Commits` table; the LINE-ANCHORED patterns
     `^<<<SLICE ` and `^<<<END ` counting 0 in `.agent/plan.md` and
     `.agent/live_review.md`; `git ls-files .remedy-wt` 0; `git worktree list`
     back to ONE line with `tmp/f022-r15-base` deleted; and the round's reflog
     rows with amend, rebase and cherry counts, each 0.
 G14 `gh pr list --state open --json number,headRefName`. Report it verbatim.
     Create no PR and merge nothing: the closure protocol creates the PR at
     closure, which is R16.
 G15 STALENESS. Every sentence C1 and C2 land that states a fact about a file is
     re-measured at C3, and any that has gone stale is reported as a residual
     rather than repaired. Report explicitly that you checked, and name any
     residual. Slices are NEVER edited to fix one.

WALL-CLOCK NOTE, not a gate: the suite is large and runs TWICE this round. If
either run exceeds ~5 minutes, say so in the handback — docs/agents/
integration_gate.md step 5 turns that into a perf-pass note, not a failure.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             every mandated section in order, one changed-files table per
             commit, an item-status row per Bundle item, the round base SHA,
             ONE line per gate, and the `Fortschritt:` block above carried
             VERBATIM across all three of its lines. Every count you report
             names the exact string or pattern counted and the file it was
             counted in (R-0442). The cap is 60 lines for this commit count;
             declare a DECISION D15 stated cause with your own measured numeral
             in the declaring line if the mandated content genuinely does not
             fit. `## Next` names R16, closure, per
             docs/roadmap/STATUS_closure_protocol.md — unless G11 found a
             blocker, in which case it names the blocker and the repair round
             that must precede closure.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R15
# Plan — F022 Live cost ticker

Branch: feature/f022-live-cost-ticker, cut from `main` at `c34ef32b`, the merge
commit of pull request #211. `.agent/live_review.md` is the source of truth for
the open set, the round map and the finding-id ceiling.

## Goal
Money is visible while it burns, honestly: the MetricsBar's COST metric renders
from budget tick events {spent, limit, basis} — bar fill against the limit, a
'~' prefix plus tooltip whenever the basis is estimated, warn colour at ≥85% —
and the final figure reconciles with the ledger at terminal. DONE when the
ticker tracks a fixture stream exactly, basis changes flip the prefix and
tooltip live, the warn threshold triggers per tokens, limitless jobs render the
spent-only variant with no fake denominator, and the terminal reconciliation
displays the ledger figure with any delta labelled.

## Current Step
R15 runs the integration gate over the whole suite, branch against base, and
records the R14 verdict with two recurrences. It builds nothing: T001, T002 and
T003 are all complete, and what remains unmeasured is whether this branch broke
anything outside its own scoped gates.

## Next Steps
1. R16 closure, per docs/roadmap/STATUS_closure_protocol.md — evidence job, a
   FRESH review zip, the authored STATUS line, and the PR created last.

## Risks
- A branch-only failure that reproduces serially and touches feature code is a
  BLOCKER, not a note. It ends R15 and buys its own reviewer-gated repair round
  before closure can start.
- The base worktree needs `apps/ui/node_modules` copied with its symlinks
  PRESERVED. Dereferencing them is what turned a parity restore into 7 base-only
  failures at F085 R23, and the copy call's default is the dereferencing one.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured, and R-0672 gained a third instance at R14;
  R-0431, R-0413 and R-0533 are reviewer-block defects already recorded and
  already paid for.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
<<<END PLANF022R15

<<<SLICE LEDGER15
Recurrence: R-0672 — A LANDED DECISION'S REVERSAL INSTRUCTION AGAIN NAMES FEWER THINGS THAN ITS OWN ROUND ADDED, AND THIS TIME THE SENTENCE THAT BREAKS THE RULE IS THE SENTENCE THAT CITES IT. Third instance, at F022 R14, in the reviewer's own DECISION text. NO NEW ID IS MINTED, and the search that establishes that is worth stating because it very nearly went the other way: §3 checklist item 30 requires the OPEN SET searched for the DEFECT before an id, and the two ids this reviewer first reached for — R-0585 for the miscount and R-0526 for the false universal — are the classes named in the CHECKLIST rather than records in THIS ledger. Measured at `8d5c73c4`, `^- R-0526 — ` and `^- R-0530 — ` are each 0 records here, because the F022 R1 reset carried the open set forward rather than the whole history, exactly as the R-0533 recurrence recorded one round earlier. R-0672 is the record that carries this ground, and it says so itself: its body reads "This is the R-0526 class — a slice asserting a universal over its own round — arriving in the clause that matters most, because a DECISION's reversal instruction is the one part of it a later reader executes rather than reads." Both instances below are that clause failing again, so both are registered here and no second id is minted for the half that wears a different name. THE FIRST INSTANCE, THE MISCOUNT: DECISION F022 D8's REVERSE IT paragraph, committed at `5c6d4fc6`, tells a reverser to remove from `apps/ui/src/api/remedyApi.test.ts` "its three cases". MEASURED over the diff `c2e78b32..318a85a1`, that commit added FOUR `it(` cases — the mapped figure, the null section, the absent key, and a fourth pinning `normalizeApiFailure` returning `budgetFinal: null`, which the worker had to add for `tsc --noEmit` to pass once the field became non-optional on `RemedyDashboard`, and which therefore could not exist when the DECISION text was written. A literal reversal removes three of four and leaves a test naming a field the same reversal has just deleted, so it does not compile — the SAME consequence R-0672's original instance names, arriving through a count instead of through an omitted file. THE SECOND INSTANCE, THE FALSE UNIVERSAL: the same paragraph closes "That is every path this round's Change set holds, which is what R-0672 and its recurrence require of a reversal instruction." MEASURED at `8d5c73c4`, the paragraph names TEN paths and the R14 block's Change set holds FOURTEEN; the four unnamed are `.agent/authored/f022-r14.md`, `.agent/last_block.md`, `.agent/decisions.md` and `.agent/handoff.md`. The sentence is defensible in spirit — those four are the round's own bookkeeping, and reversing a decision does not mean deleting the record that it was made, which is the reasoning the paragraph states EXPLICITLY for `.agent/plan.md` and `.agent/live_review.md` two sentences earlier — and it is false as written, because the reasoning was applied to two paths and the universal was claimed over fourteen. FOUND BY THE WORKER on both counts: it declared the miscount as a constraint-1 contradiction and reported the universal as an observation, applying the slice byte for byte as required — the seventh consecutive round in which a worker's declaration rather than a gate is what put a reviewer-authored defect on the record. WHY LOW, twice over: every path a reverser actually needs IS named, so the instruction works, and the missing case is discovered by the first `tsc` run. THE LANDED PARAGRAPH IS NOT REWRITTEN, per §3 item 20: this correction is dated by the commit that carries it, and the count a reverser should use is FOUR. WHAT THIS ADDS TO R-0672, and it is the reason a third instance earns a clause rather than a sigh: the first instance was fixed by naming the round's Change set, and this instance NAMED the Change set and still failed, in two different ways, so naming is not enough. A reversal instruction states the paths it deliberately EXCLUDES and why, and gives no COUNT of anything its own round is still free to grow — a DECISION is authored before the change set it rules has landed, so every numeral in it is a prediction. The exclusion is the half a later reader needs and it is the half that keeps being left implicit.

Gate: R14 — the F022 R14 entry. R14 PASSED ON EVERY ONE OF ITS THIRTEEN GATES, AND THE REVIEWER RE-EXECUTED EVERY ONE OF THEM ITSELF AND ADDED SEVEN MUTATIONS THE BLOCK NEVER ORDERED, FIVE OF THEM UNORDERED. THE ROUND'S SUBSTANCE IS THAT THE LEDGER'S FINAL FIGURE NOW REACHES A SCREEN. `costReconciliation.ts` swaps the COST tile to the ledger's own view at terminal and names a delta when the two displays differ; `budgetFinal` carries the payload opaquely into `RemedyDashboard`; and `RemedyShell.tsx` WRAPS the live seam rather than replacing it, so the running job keeps its ticking tile. That closes T003b and with it the last clause of the feature's Goal that no code answered. TRANSPORT HELD IN ITS STRONGEST FORM, disk to disk and not by the digest fallback: the reviewer's own scratch original at `.remedy-wt/f022-r14.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` on disk are ALL sha256 `1c827a3f558a485b97d5f25d8fe855a17f22fcd356b434c4b8e134a1f3eeb5b5` over 30949 bytes and 393 lines, and C0a and C0b resolve to the SAME git blob `ac070803`. THE EXTRACTION printed 3 slices over 116 CONTENT lines against a TOTAL of 393, so PROSE is 277 and constraint 10 reproduces exactly. `.agent/plan.md` at `ca3273be` is 2608 bytes = PLANF022R14's 2607 plus one newline, the BARE-slice control FALSE, headings once each, 45 lines against the cap of 50. BOTH APPENDS HOLD UNDER BOTH READERS: at `39d07ada` the remainder is 5004 = 1 + LEDGER14's 5002 + 1 with N=1 paragraph equal in order over 275 units becoming 276, and at `5c6d4fc6` the remainder is 4512 = 1 + DEC14's 4510 + 1 with N=9 over 1310 becoming 1319. THE SETS MOVED EXACTLY WHERE THE ROUND PROMISED: 234 records at base and at C2, all DISTINCT at both with maximum `R-0673`, ids ADDED and ids REMOVED both the EMPTY SET so NO ID WAS MINTED, `^Done: R-` 2 and 2, `^Landed: ` 0 and 0, `^Recurrence: R-` 8 and 8, and `^Gate: R` 13 becoming 14 by gaining exactly the key `R13`. THE ARITHMETIC HOME DID NOT MOVE, AND THE REVIEWER MEASURED IT RATHER THAN READING THE GATE'S WORD FOR IT: over the 61 shipped `.ts`/`.tsx` files under `apps/ui/src`, comments stripped, the list of files whose CODE names `spent_usd`, `spent_tokens`, `limit_usd` or `limit_tokens` is exactly `apps/ui/src/api/costMetric.ts`, and `costReconciliation.ts` is IN the scanned set with its RAW source naming a field and its STRIPPED code naming none — so the comment-stripping half of that guard is non-vacuous rather than merely green. THE SUITES ARE THE REVIEWER'S OWN, run serially with never two pytest processes alive at once: `npx vitest run` in `apps/ui` at 20 files and 285 tests against the base's 19 and 268, `npx tsc --noEmit` at exit 0 with no output, `tests/ui_contracts/` at 525 passed and 4 skipped against the base's 518 and 4, the four state readers at 470, 52, 21 and 16 for 559, and the canary at 42 — every one exit 0 and every one matching the block's reference figure. THE MUTATIONS ARE WHERE THIS VERDICT IS EARNED. All seven ran in a disposable worktree at `8d5c73c4` with the primary checkout never written, against a positive control of 13 passed in the module's own suite and 30 passed in the contract file. The two the block ORDERED went red as ordered: deleting the equal-displays guard failed 1 naming `says NOTHING when the two displays are equal`, and deleting the running guard failed 1 naming `a RUNNING job gets the SAME array, so nothing claims finality mid-run`. THE FIVE THE BLOCK DID NOT ORDER MATTER MORE: deleting the null-ledger guard failed 1 naming `a null ledger figure gets the SAME array, so the live tile stands`; rendering the RECEIVED figure instead of the ledger's failed 3, which is the feature's whole point and is therefore the mutation most worth having; SWAPPING the note's two operands failed 1 naming `names BOTH displays when they differ`, so the label's direction is pinned and not merely its presence; deleting the note render from `TopMetricsBar.tsx` failed `test_the_bar_renders_the_note_off_its_own_field`; and naming a figure field in the module's CODE failed `test_the_figure_fields_have_a_single_home`, which proves the single-home guard genuinely bites the new file rather than merely listing it. Every property this round claims is guarded by a test that fails when the property is broken. STRUCTURE HELD: 8 commits before the handback, every one single-parent, insertions 393, 291, 11, 2, 71, 219, 45 and 92, each under the 500 cap; the range path set is exactly the 14 declared paths with the difference EMPTY in BOTH directions; `git show --numstat` agrees cell by cell with every `## Commits` row; the anchored markers count 0 in all three state files; `git ls-files .remedy-wt` is 0; one worktree; and all 9 reflog rows of the round carry the action `commit`, with amend, rebase and cherry each 0. THE HANDBACK at `8d5c73c4` IS COMPLIANT at 148 lines with a DECISION D15 stated cause naming that same 148, every mandated section present exactly once and in order, and the three-line `Fortschritt:` block byte-identical to the block's. THE OPEN PR GATE printed an empty JSON array and no PR was created. THE ROUND'S TWO DECLARED CONTRADICTIONS ARE BOTH CORRECT AND BOTH CORRECT THE REVIEWER: they are the two instances of the R-0672 recurrence written above, in this same commit. THE VERDICT IS PASS: every numeral R14 states reproduced under the reviewer's own measurement, seven mutations went red against the right tests, no slice was edited, no id was minted, and the ledger figure that R12 served to nobody now has a reader, a renderer and a guard.
<<<END LEDGER15
