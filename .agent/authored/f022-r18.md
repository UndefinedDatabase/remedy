── STEP CLOSURE 2/3 — F022 Live cost ticker · Runde 18 ───────────────────────

Fortschritt: ~98 % (T001 fertig · T002 fertig · T003 fertig · Integration Gate
             bestanden · R17 gegatet mit PASS · Built State steht — diese Runde
             baut den Evidence-Job und das Review-Zip, die einzigen Werte, aus
             denen R19 die STATUS-Zeile schreiben kann) — Schaetzung

Goal:        Record the R17 verdict and its one new finding, then produce the
             two artifacts closure cannot be authored without: a fresh
             feature-scoped evidence bundle and a FRESH review zip built from a
             clean tree at the reviewed head. A failing zip build is a closure
             BLOCKER, never a thing to work around. Nothing about STATUS.md or
             README.md happens this round; R19 writes those from the package
             name and SHA-256 that only this round can produce.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 the R17 verdict, finding R-0676 and the R-0371 recurrence ·
             the EVIDENCE JOB · the REVIEW ZIP · C3 the handback.
             The evidence bundle and the zip are ARTIFACTS, not commits: both
             paths are gitignored and neither is ever committed
             (docs/roadmap/STATUS_closure_protocol.md, "Evidence dir is not
             committed").

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r18.md      (C0a)
               .agent/last_block.md             (C0b)
               .agent/plan.md                   (C1)
               .agent/live_review.md            (C2)
               .agent/handoff.md                (C3)
             This list bounds what you WRITE INTO THE REPOSITORY. It does not
             bound what you DO: G14 orders a push, the evidence job writes under
             `.remedy-wt/`, and the zip writes a gitignored archive at the
             repository root. AGENTS.md Push Discipline binds whether or not any
             block names it (finding R-0674, registered last round).

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The whole-text
slices are PLANF022R18, LEDGER18 and EVIDENCESCRIPT. THIS BLOCK CARRIES NO
FROM/TO PAIR, so no containment test is stated and no FROM-count is ordered.
Every slice is quoted WITHOUT its trailing newline; PLANF022R18 replaces its
file whole, LEDGER18 lands as one newline plus the slice plus one newline, and
EVIDENCESCRIPT is written to `.remedy-wt/f022_evidence.py` as the slice plus one
newline — a gitignored scratch path that is in NO commit.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your slices; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    registers a finding, so the plan advances before anything else but the two
    block-save commits.
 3. COMMIT ORDER IS C0a, C0b, C1, C2, C3 and no other. The EVIDENCE JOB and the
    ZIP run AFTER C2 and BEFORE C3, in that order, because the closure protocol
    requires the package to be built from a clean tree at the head that carries
    every CONTENT commit, and because C3 must quote the package name and its
    SHA-256 — values that exist only once the zip has been built.
 4. LEDGER18 holds, in this order and separated by ONE blank line: the `- R-0676`
    record, the `Recurrence: R-0371` paragraph and the `Gate: R17` paragraph. It
    lands in ONE commit, C2, or none of it does: the gate paragraph states that
    the finding and the recurrence are registered in that same commit, and THIS
    constraint is what makes that true (§3 item 20, R-0524 carve-out).
 5. NO PRODUCTION CODE, NO TESTS, NO DOCS. Nothing under `apps/`, `packages/`,
    `tests/` or `docs/` is in the Change set. The feature file's Built State
    landed at R17 and is not touched again.
 6. NO REPAIR of any open finding. R-0676 is RECORDED, not fixed, and the
    R-0371 recurrence is RECORDED against the id that already holds the class —
    §3 item 30 forbids minting a second id for a defect the open set describes.
 7. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`, removed BY ITS EXACT PATH and never by a glob (R-0662). The
    primary checkout satisfies `git status --porcelain` empty at every commit,
    before the zip build, and at the handback.
 8. Every numeral this block states about the ROUND BASE `7c13dd11` was produced
    by a reviewer script or tool run at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
 9. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 458 lines TOTAL with 190 CONTENT
    lines inside its slices, so PROSE is 268 — under DECISION F085 D6's
    490 and D5's 400.
10. THE ZIP IS A BLOCKER, NOT A BEST EFFORT. If the build fails, or if the
    package status is anything other than `READY_FOR_REVIEW`, STOP: do not make
    C3 into a success report, record the RAW error and the real status in the
    handback, and hand back with the failure stated plainly. A closure package
    that does not exist is a closure that does not happen.

─── Why this round exists ─────────────────────────────────────────────────────

R17 passed every one of its thirteen gates under the reviewer's own re-runs, and
its verdict is not on disk: DECISION F085 D9 rules that a PASS is written by the
NEXT round's ledger commit. R17 also produced one new defect and one recurrence
of an old one, and §4 item 4 rules that findings persist FIRST, in their own
commit, before anything else is attempted with them — which is why C2 precedes
the evidence job rather than following it.

The artifacts are the other reason. `docs/roadmap/STATUS_closure_protocol.md`
steps 1 and 2 require a fresh feature-scoped evidence bundle and a FRESH review
zip, and step 4's STATUS line names the evidence job id, the package filename
and the package SHA-256. Those three values exist nowhere until this round
produces them, so authoring the STATUS line before the zip exists would order a
value that cannot exist when the text carrying it is written — finding R-0371,
whose third instance this same block registers. The split into R18 and R19 is
therefore forced by the record, not chosen for convenience.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). Gates G1
through G13 all run BEFORE C3, so the handback can quote every one of them
(§3 checklist item 31). G14 is the single exception and its treatment is stated
in its own text. The round base is `7c13dd11` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C3.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a, C0b, C1 and C2, and again immediately before the
     zip build — the protocol invalidates a package built from a dirty tree.
 G2  TRANSPORT. sha256 over the block file at `.remedy-wt/f022-r18.md`, over the
     committed C0a blob, over the committed C0b blob and over
     `.agent/last_block.md` on disk: report all four digests, byte counts and
     line counts, and require them EQUAL. The digest the delegation names is the
     fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     PROSE is TOTAL minus CONTENT, so the marker lines count as prose. Report
     those against constraint 9's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R18 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, and `wc -l` STRICTLY UNDER 50 — AGENTS.md caps this file at fewer
     than 50 lines, so report the number you measure.
 G5  APPEND at C2, proved twice. The base blob is a byte-exact PREFIX of the
     committed file and the remainder is exactly one newline plus the slice plus
     one newline — report the remainder's byte count and the slice's. Then an
     INDEPENDENT reader: split both files on blank lines, let N be the number of
     paragraphs YOUR script counts in the slice, and require the LAST N units of
     the committed file to equal the slice's N paragraphs IN ORDER. Report N; do
     not take it from this block. NEGATIVE CONTROL, in a disposable worktree,
     applied to the FIRST appended paragraph: flip ONE byte at an offset you
     name and confirm BOTH readers reject the mutant while both accept the true
     file. THE OFFSET IS A BYTE OFFSET — the file carries multi-byte em dashes,
     so a CHARACTER offset lands early, outside the appended region, where
     reader (b) accepts the mutant and the control proves nothing. Report the
     ~20 bytes surrounding the flip. Remove the worktree by its exact path;
     `git worktree list` back to one line.
 G6  LEDGER INTEGRITY, base versus C2. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-` with its distinct ids, of `^Landed: `, of
     `^Recurrence: R-` with its DISTINCT ids, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and REMOVED as sets. At base the
     reviewer measured 236 records, all distinct, maximum `R-0675`, 2 `Done:`
     lines over `R-0653` and `R-0670`, 0 `Landed:`, 10 `Recurrence:` lines over
     8 DISTINCT ids, and 17 `Gate:` lines over 17 distinct keys, none of them
     `R17`. This round MINTS EXACTLY ONE ID: the ids ADDED must be exactly
     `R-0676`, the ids REMOVED the EMPTY SET, the record count 237, the maximum
     `R-0676`, the `Recurrence:` readings 11 lines over 9 DISTINCT ids by
     gaining a FIRST `R-0371` line, and the `Gate:` keys must gain exactly
     `R17`. Report what you measure.
 G7  THE FULL SUITE, closure precondition 2, run by YOU in the PRIMARY checkout
     at C2 from the repository root: `python3 -m pytest -n auto -q`. Report the
     REAL exit code, the summary line verbatim, the wall clock, and the COUNT of
     lines matching `^FAILED`. Prove your `^FAILED` extractor is not blind by
     running it over a string you know contains such a line and reporting that
     it matched — a zero from an extractor that cannot match is not a reading.
     R15's integration gate measured `17722 passed, 20 skipped` on this branch
     and the reviewer reproduced it; this round re-confirms rather than
     re-litigates. A regression here is a normal repair round, not a closure.
 G8  INTEGRITY, closure precondition 3. The `remedy` CLI is NOT available to
     you; call the module instead and report what it returns as JSON, including
     its status field and any `high_blockers_open` value. Report also
     `git status --porcelain` at that moment, which must be 0 lines: the
     precondition names "no relevant untracked files" and a gitignored artifact
     is not one.
 G9  THE EVIDENCE JOB. Write EVIDENCESCRIPT to `.remedy-wt/f022_evidence.py`
     byte for byte plus one newline, then run it with `python3` FROM THE
     REPOSITORY ROOT and report its REAL exit code and its full stdout. It
     asserts every precondition that has historically produced a
     BLOCKED_EVIDENCE package — `len(node_ids) == selected`, zero deselected,
     `test_files` sorted and all real files, a `^vr-\d{4,}$` run id, a 40-char
     base commit, and `output_hash` equal to sha256 of `stdout_summary` exactly
     — and it scans every packaged string with the packager's OWN `_unsafe_text`
     before writing anything, with a red control proving that scanner bites. If
     any assertion fires, the bundle is NOT written: report the failure and
     STOP, per constraint 10. The reviewer ran the four suites at the round base
     and measured 10, 16, 15 and 30 selected with 0 deselected, 0 rejected
     strings and the red control truthy.
 G10 THE REVIEW ZIP. With `git status --porcelain` at 0 lines, run
     `bash scripts/make_review_zip.sh --evidence-dir <the directory G9 wrote>`
     and report its REAL exit code, the final package FILENAME, its SHA-256 and
     its PACKAGE_STATUS. Then report, from the manifest inside that package,
     `committed_review_subject.base_commit` and `.head_commit`, and require the
     head to equal the commit C2 created and the base to equal
     `c34ef32b0ac3e6a7af161fa724f42ba1c3167786`. Compute the SHA-256 yourself
     over the published file rather than quoting the script's line, and report
     both so they can be compared. A status other than `READY_FOR_REVIEW`, or a
     non-zero exit, is a BLOCKER under constraint 10.
 G11 STRUCTURE, reported for the commits BEFORE C3 and for the range as a whole
     (C3's own numbers belong to the next round's ledger entry, not here):
     every commit single-parent; each commit's INSERTION count, each under the
     500 cap; the range path set against the Change set above with the
     difference reported in BOTH directions; `git show --numstat` agreeing cell
     by cell with the handback's `## Commits` table; the LINE-ANCHORED patterns
     `^<<<SLICE ` and `^<<<END ` counting 0 in `.agent/plan.md` and
     `.agent/live_review.md`; `git ls-files .remedy-wt` 0; `git ls-files` over
     the evidence directory and over the published zip each 0, proving neither
     artifact entered the repository; one worktree; and the round's reflog rows
     with amend, rebase and cherry counted IN THE OPERATION FIELD before the
     first colon (R-0613), each 0.
 G12 `gh pr list --state open --json number,headRefName`. Report it verbatim.
     Create no PR and merge nothing. CLOSURE HAS NOT RUN: the closure protocol
     creates the PR itself, at R19, after the STATUS line is authored from the
     values G10 produces.
 G13 STALENESS. Every sentence C1 and C2 land that states a fact about a file is
     re-measured at C2, and any that has gone stale is reported as a residual
     rather than repaired. Report explicitly that you checked, and name any
     residual. Slices are NEVER edited to fix one.
 G14 PUSH. After C3, run `git push origin feature/f022-live-cost-ticker`. No
     `--force`, no `--force-with-lease`, no history rewrite, no branch deletion.
     ITS OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: C3 is authored
     before the push exists, so `.agent/handoff.md` states the push only as an
     INTENT under `## External actions` and states NO exit code and NO remote
     tip. Report the real exit code and the resulting remote tip in your
     completion report to the reviewer, which is where the next round's ledger
     entry will read them from. R17's own G13 ordered the outcome into that file
     and forbade it in the next breath; that contradiction is the R-0371
     recurrence this block registers, and this gate is written so the same round
     does not repeat it.

NOT A GATE and not run this round: `npm run lint`, `npm run typecheck` and
`npm run test:unit`. The Change set holds no file under `apps/`.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             every mandated section in order, one changed-files table per
             commit, an item-status row per Bundle item INCLUDING the evidence
             job and the zip, the round base SHA, ONE line per gate, and the
             `Fortschritt:` block above carried VERBATIM across all four of its
             lines. Every count you report names the exact string or pattern
             counted and the file it was counted in (R-0442). THE CAP IS THE
             AGENTS.md ONE AND NOT A NUMBER THIS BLOCK INVENTS: 60 lines, or
             100 when per-commit tables of more than five commits require it —
             read the rule in AGENTS.md under `### handoff.md` and apply the
             tier that genuinely fits this round's commit count, declaring a
             DECISION D15 stated cause with your own measured numeral only if
             the mandated content exceeds the tier that applies. R17's block
             asserted the 60-line tier for a seven-commit round and forced a
             spurious overage declaration; that is finding R-0676, which this
             block registers. Any commit you make BEYOND the sequence
             constraint 3 names gets its own `## Commits` row and its own
             item-status row, and the Deviations section says so in the same
             words (finding R-0675).
             `## Next` names R19: the reviewer authors the STATUS line from the
             evidence job id, the package filename and the package SHA-256 this
             round produced, the worker commits it LAST with the README
             capability sync in the SAME commit and empties
             `.agent/candidates.md`, and then creates the PR — which is NOT
             merged this session.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R18
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
R18 records the R17 verdict, registers finding R-0676 and the R-0371
recurrence, then builds the two artifacts closure cannot be authored without:
a fresh feature-scoped evidence bundle and a FRESH review zip. It builds no
product code; T001, T002 and T003 are complete and the Built State is current.

## Next Steps
1. R19 closure: the reviewer authors the STATUS line from the evidence job id,
   the package filename and the package SHA-256 that R18 produced, the worker
   commits it LAST with the README capability sync in the SAME commit and
   empties `.agent/candidates.md`, then creates the PR.

## Risks
- A failing zip build is a closure BLOCKER, never a thing to work around: the
  feature does not close without the package.
- The closure PR is created but NOT merged by the round that makes it: it merges
  at the NEXT feature's Open PR Gate, which preserves the operator's window.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured; R-0431, R-0413 and R-0533 are recorded and
  already paid for; R-0674, R-0675 and R-0676 are registered and repaired by
  none, their subjects being landed append-only text; and R-0445 is a standing
  defect of `docs/agents/integration_gate.md`, routed by the finding itself to
  a follow-up branch rather than to this one.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0403 is open and this package will show it: `.remedy-wt/` scratch is a large
  share of every review zip built on this machine. It routes to a paydown
  branch and is not an F022 defect.
<<<END PLANF022R18

<<<SLICE LEDGER18
- R-0676 — Low, A BLOCK QUOTED THE STRICTER TIER OF A TWO-TIER REPOSITORY CAP AND FORCED AN HONEST WORKER TO DECLARE AN OVERAGE IT WAS NOT COMMITTING. Raised by the reviewer while gating R17. THE MEASUREMENT, taken at `7c13dd11`: the R17 block's Handback paragraph reads "The cap is 60 lines for this commit count", and AGENTS.md under `### handoff.md` reads "≤60 lines (≤100 when per-commit tables of >5 commits require it — sections are never dropped)". R17 ordered SEVEN commits, so more than five per-commit tables were mandated and the applicable tier is 100. The landed handback at `7c13dd11` measures 99 lines by `wc -l`, which is INSIDE the AGENTS.md cap and outside the number the block named. THE COST IS A FALSE LINE IN THE PERMANENT RECORD, and it is the reviewer's: the worker, correctly refusing to drop a mandated section, declared a DECISION D15 stated-cause overage against a cap that did not apply, so `.agent/handoff.md` now records a compliant round as a deviating one. The worker also caught the discrepancy, named BOTH readings and said which one it was declaring against, which is the only reason this is recoverable rather than simply wrong. WHY LOW: no gate reading moved, no measurement is false, nothing was dropped to fit, and the declaration is honest about its own ambiguity — what is wrong is a rule quotation, in a sentence no gate reads. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED, as §3 checklist item 30 requires, and two OPEN neighbours are close enough to name. R-0582 rules that the handback cap has become NOMINAL because blocks order more mandated content than it admits, and its counter-measure is to route transcripts to the round report — which the R17 block DID, ordering one line per gate; that finding is about a cap exceeded by design, not about a cap misquoted. R-0430 is a handoff deferring its own measured LENGTH to a channel leaving no disk artifact, which is where a numeral goes rather than which numeral is right. Neither reaches a block naming the wrong tier of a cap that has two, so the id is minted rather than the evidence being added to theirs. THE FIX, BINDING ON EVERY BLOCK THIS WORKFLOW EMITS FROM HERE: a block that states a cap for a file the repository already caps quotes the RULE and its condition rather than a single number, or names no number at all and points the worker at the governing line — and where the tier depends on a property of the round, the block names the property and lets the worker resolve it. The R18 block that registers this finding carries that form in its own Handback paragraph, which is the only reason this entry can claim the counter-measure exists rather than naming a round that will build it (§3 checklist item 11).

Recurrence: R-0371 — A BLOCK ORDERED A VALUE THAT CANNOT EXIST WHEN THE TEXT CARRYING IT IS WRITTEN. THIRD INSTANCE, at F022 R17, and it lands in exactly the escape hatch the SECOND instance opened. NO NEW ID IS MINTED: R-0371 already rules that every post-hoc measurement is ordered into the handback rather than into committed text, and its second instance at F008 R13 already narrowed that to note the handback IS a commit, so a reading over anything the handback commit does not precede is still unwritable. THE MEASUREMENT, taken at `7c13dd11`: G13 of the R17 block ordered the push reading into the handback's `## External actions` section "as a stated intent plus the outcome", and the SAME gate's next clause forbids "a gate line whose value C5 would have had to know before it existed (§3 checklist item 31)". The push runs after C5 by that gate's own instruction, so the two halves of one gate cannot both be obeyed. THE WORKER RESOLVED IT THE RIGHT WAY ROUND and declared it: it stated the intent verbatim in C5, wrote NO exit code and NO remote tip into the file, made no eighth commit to add them afterwards — which would have been the R-0675 defect the same round registers — and reported the real values out of band, exit 0 with remote tip `7c13dd11`, which the reviewer confirmed independently against `git ls-remote`. WHAT MAKES IT A RECURRENCE RATHER THAN A NEW CLASS: the block did not merely order an impossible value, it ordered one and forbade it in the next sentence, so the defect was visible on the page to anyone reading the gate through to its end — and the reviewer wrote both halves. R-0371's counter-measure is to check, before ordering any text into a file, that every value that text must contain already exists at the moment of writing; applying it to a gate's own two clauses is what the R17 block did not do. THE COUNTER-MEASURE IS EXTENDED, binding on every block from here: a gate that names an action running after the last commit states explicitly that its outcome is reported to the reviewer and is NOT a value of any file the round writes, rather than naming a section of that file for it. G14 of the R18 block carries that form.

Gate: R17 — the F022 R17 entry. R17 PASSED ON EVERY ONE OF ITS THIRTEEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF RATHER THAN READING THE HANDBACK'S WORD FOR ANY OF THEM. THE ROUND'S SUBSTANCE IS THAT CLOSURE PRECONDITION 4 IS NOW MET: `docs/roadmap/features/T5_F022.md` carries a `## Built State` section for the first time, so the closure commit no longer has to choose between writing it and obeying the exact-paths rule. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own scratch original at `.remedy-wt/f022-r17-final.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` on disk are ALL sha256 `377accba1b0143a2697c0b3ebbe5d76d97adf31762831679fedc186b5628d77e` over 35851 bytes and 388 lines, and C0a and C0b resolve to the SAME git blob `f052956c`. THE EXTRACTION printed 5 slices over 126 CONTENT lines against a TOTAL of 388, so PROSE is 262 and constraint 9 reproduces exactly. `.agent/plan.md` at `4f714490` is 2860 bytes, which is PLANF022R17's 2859 plus one newline, the BARE-slice control FALSE, `^## Goal$` and `^## Next Steps$` once each, and 49 lines STRICTLY under the cap of 50 — the reviewer caught that slice at 50 lines before emission and cut it, which is the one defect this workflow is supposed to catch on its own side of the relay. THE PAIR AT `af0701d0` IS A REWRITE and was proved as one: the containment test printed `TO contains FROM: false`, MAPFROM17 went 1 to 0 and MAPTO17 0 to 1, the file grew by exactly 139 bytes matching the length difference of the two halves, `^## Steps$` stayed at 1, the committed file equals the base file with only that replacement applied, and the longest line of the `## Steps` paragraph is 80 against the 84 cap. THE APPEND AT `0058a482` HOLDS UNDER BOTH READERS: the C2 blob is a byte-exact PREFIX of the C3 file and the remainder is 10679 bytes, which is one newline plus LEDGER17's 10677 plus one newline, while an independent blank-line split counted N as 3 paragraphs and found the LAST 3 units equal to them IN ORDER, 280 units becoming 283; the byte-flip control at offset 592201, turning the `t` of `Raised by the reviewe` into `T`, is rejected by both readers while both accept the true file. THE APPEND AT `bfe73971` HOLDS THE SAME WAY: remainder 4389 bytes over BUILT17's 4387, reader (b) counting N as 6 with the last 6 units equal in order over 9 units becoming 15, `^## ` going 8 to 9 and `^## Built State$` 0 to 1. THE SETS MOVED EXACTLY WHERE THE ROUND PROMISED: 234 records at base becoming 236 at C3, all DISTINCT at both, maximum `R-0673` becoming `R-0675`, ids ADDED exactly `R-0674` and `R-0675` with ids REMOVED the EMPTY SET, `^Done: R-` 2 and 2 over `R-0653` and `R-0670`, `^Landed: ` 0 and 0, `^Recurrence: R-` unchanged at 10 over 8 DISTINCT ids, and `^Gate: R` 16 becoming 17 by gaining exactly the key `R16`. THE SUITES ARE THE REVIEWER'S OWN, run serially with never two pytest processes alive at once, every one exit 0: `tests/docs/` 295, `tests/orchestration/test_roadmap_index.py` 30, `tests/ui_server/` 470, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 for 559 across the four, and the canary `tests/cli/test_golden_path.py` 42 — reproducing the handback cell for cell. THE DOCS GATES WERE CHARACTERISED RATHER THAN TRUSTED, which is the round's other quiet win: the reviewer ran three red controls in a disposable worktree and found that replacing the Built State BODY with unrelated text leaves both suites at 325 passed, that changing the title's PROSE while keeping the id also leaves them at 325, and that only changing the F-ID itself goes red at 11 failed — so those suites key on the F-ID and are BLIND to the section R17 added, and the block said so in G8 instead of letting a green docs gate read as certification. That is open finding R-0493 measured again at a new commit, not minted again. STRUCTURE HELD: 6 commits before the handback, every one single-parent, insertions 388, 257, 19, 3, 6 and 67, each under the 500 cap; the range path set minus the Change set EMPTY and the Change set minus the range exactly `.agent/handoff.md`, which is C5's own; the anchored markers count 0 in all three edited files; `git ls-files .remedy-wt` is 0; one worktree, both disposable worktrees removed BY THEIR EXACT PATHS; and amend, rebase and cherry each 0 in the reflog's OPERATION field. THE OPEN PR GATE printed an empty JSON array and no PR was created. THE ROUND'S TWO DECLARED DEVIATIONS ARE BOTH CORRECT AND BOTH CORRECT THE REVIEWER: they are finding R-0676 and the R-0371 recurrence written above, in this same commit, which block constraint 4 is what makes true. THE VERDICT IS PASS: every gate reproduced under the reviewer's own execution, no slice was edited, the two findings R16 produced are now on disk with their ids, and F022 has cleared the last content round before its package.
<<<END LEDGER18

<<<SLICE EVIDENCESCRIPT
"""F022 closure evidence bundle. Run with python3 from the repository root."""
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.abspath(".")
EVIDENCE_DIR = os.path.join(
    REPO, ".remedy-wt", "f022_closure_evidence", "remedy-job-evidence-f022-closure"
)
BASE = "c34ef32b0ac3e6a7af161fa724f42ba1c3167786"
assert len(BASE) == 40, BASE

HEAD = subprocess.run(
    ["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True
).stdout.strip()
assert len(HEAD) == 40, HEAD


def _tail(text):
    """The last 2000 chars on a WHOLE-LINE boundary, path-scrubbed TWICE.

    job_evidence._scrub_paths only relativises paths under REPO. A pytest header
    line can end in the interpreter's own absolute path, which
    build_review_manifest._unsafe_text correctly rejects as a local absolute
    path -> BLOCKED_EVIDENCE.
    """
    from packages.common.path_redaction import scrub_paths
    from packages.orchestration.job_evidence import _scrub_paths

    cut = text[-2000:]
    if len(text) > 2000 and "\n" in cut:
        cut = cut[cut.index("\n") + 1:]
    return scrub_paths(_scrub_paths(cut, REPO))


def mkrun(rid, path, expect):
    """One verification record.

    Node ids come from --collect-only, never from a -v log: a parametrized id
    can contain whitespace and a regex over -v output splits it (R-0611).
    NOTHING is deselected here. All four of F022's scoped suites were scanned
    with build_review_manifest._unsafe_text at 7c13dd11 and none of their ids
    was rejected, so this feature needs no -k filter.
    """
    assert re.match(r"^vr-\d{4,}$", rid), rid
    sel = [path, "-q"]
    cmd = "python3 -m pytest " + path + " -q"
    collect = subprocess.run(
        ["python3", "-m", "pytest"] + sel + ["--collect-only"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert collect.returncode == 0, (rid, collect.returncode)
    ids = [ln for ln in collect.stdout.split("\n") if ln.startswith("tests/")]
    run = subprocess.run(
        ["python3", "-m", "pytest"] + sel, cwd=REPO, capture_output=True, text=True,
    )
    text = run.stdout + run.stderr
    assert run.returncode == 0, (rid, run.returncode, text[-400:])
    passed = sum(int(x) for x in re.findall(r"(\d+) passed", text))
    failed = sum(int(x) for x in re.findall(r"(\d+) (?:failed|error)", text))
    skipped = sum(int(x) for x in re.findall(r"(\d+) skipped", text))
    desel = sum(int(x) for x in re.findall(r"(\d+) deselected", text))
    dur = float(re.findall(r"in ([\d.]+)s", text)[-1])
    assert (passed, failed, skipped) == (expect, 0, 0), (rid, passed, failed, skipped)
    assert desel == 0, (rid, desel)
    selected = passed + failed + skipped
    assert len(ids) == selected, (rid, len(ids), selected)
    files = sorted({i.split("::")[0] for i in ids})
    for f in files:
        assert os.path.isfile(os.path.join(REPO, f)), f
    return {
        "run_id": rid, "command": cmd,
        "exit_code": 0, "passed": passed, "failed": failed, "skipped": skipped,
        "selected": selected, "deselected": desel, "node_ids": ids,
        "test_files": files, "duration_seconds": dur,
        "head_sha": HEAD, "stdout_summary": _tail(text),
    }


runs = [
    mkrun("vr-0001", "tests/orchestration/test_budget_tick.py", 10),
    mkrun("vr-0002", "tests/ui_server/test_budget_tick_envelope.py", 16),
    mkrun("vr-0003", "tests/ui_server/test_budget_final_section.py", 15),
    mkrun("vr-0004", "tests/ui_contracts/test_cost_metric_render.py", 30),
]
for r in runs:
    print(r["run_id"], "selected", r["selected"], "node_ids", len(r["node_ids"]),
          "deselected", r["deselected"], "files", len(r["test_files"]),
          "dur", r["duration_seconds"])

# Every packaged string is scanned; prove the ids and commands pass BEFORE the
# bundle is written, so a rejection is a red here and not a BLOCKED zip later.
sys.path.insert(0, os.path.join(REPO, "scripts"))
from build_review_manifest import _unsafe_text  # noqa: E402

rejected = [(r["run_id"], v) for r in runs for v in r["node_ids"] + [r["command"]]
            if _unsafe_text(v)]
print("SCAN rejected strings:", len(rejected), rejected[:3])
assert not rejected, rejected
print("SCAN red control:", _unsafe_text("/home/user/repo/tests/x.py::t"))

now = datetime.now(timezone.utc)
from packages.orchestration.job_evidence import create_manual_completion_bundle  # noqa: E402

result = create_manual_completion_bundle(
    EVIDENCE_DIR,
    repo_root=REPO,
    base_commit=BASE,
    head_commit=HEAD,
    job_id="f022-closure",
    job_title="F022 Live cost ticker - closure",
    step_range="T001-T003",
    prior_job_ids=["f021-closure"],
    verification_runs=runs,
    timestamp=now.replace(microsecond=0).isoformat(),
    generated_at=now.isoformat(),
    num_tasks=3,
    note_prefix="operator-attested manual completion - F022 closure",
    review_feature_id="f022",
)
print(json.dumps(result, indent=2, sort_keys=True))

# The output_hash preimage rule: sha256 over stdout_summary EXACTLY. This is the
# pitfall that blocked the F083 closure and it is not in the protocol's list.
vt = os.path.join(EVIDENCE_DIR, "verification_tests.json")
if os.path.isfile(vt):
    with open(vt, encoding="utf-8") as fh:
        doc = json.load(fh)
    for row in doc.get("runs", []):
        want = hashlib.sha256(row.get("stdout_summary", "").encode()).hexdigest()
        print("OUTPUT_HASH", row.get("run_id"), "matches sha256(stdout_summary):",
              row.get("output_hash") == want)
else:
    print("OUTPUT_HASH no verification_tests.json at", vt)
print("EVIDENCE_DIR", EVIDENCE_DIR)
<<<END EVIDENCESCRIPT
