── STEP CLOSURE 1/3 — F022 Live cost ticker · Runde 17 ───────────────────────

Fortschritt: ~96 % (T001 fertig · T002 fertig · T003 fertig · Integration Gate
             bestanden · R16 gegatet mit PASS — diese Runde schreibt das
             R16-Urteil und zwei neue Findings auf Platte und bringt den
             Built-State der Feature-Datei auf Stand) — Schaetzung

Goal:        Record the R16 verdict, register the two findings R16 produced, and
             bring `docs/roadmap/features/T5_F022.md` current with a `## Built
             State` section — the closure protocol's precondition 4, which this
             file has never satisfied because the section does not exist. The
             closure commit may touch only STATUS.md, README.md and `.agent/`,
             so a Built State written at closure would break that rule; it is
             written HERE, in the last content round before the package.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 repair the round map for the three closure rounds · C3 the R16
             verdict and findings R-0674 and R-0675 · C4 the feature file's
             Built State · C5 the handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r17.md      (C0a)
               .agent/last_block.md             (C0b)
               .agent/plan.md                   (C1)
               .agent/live_review.md            (C2, C3)
               docs/roadmap/features/T5_F022.md (C4)
               .agent/handoff.md                (C5)
             This list bounds what you WRITE. It does not bound what you DO:
             G13 orders a push, and AGENTS.md Push Discipline binds whether or
             not any block names it. That distinction is finding R-0674, which
             this same block registers, applied to the block that registers it.

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The whole-text
slices are PLANF022R17, LEDGER17 and BUILT17. MAPFROM17 and MAPTO17 are the
halves of a FROM/TO pair, and this block carries no other pair. Every slice is
quoted WITHOUT its trailing newline; PLANF022R17 replaces its file whole, and
LEDGER17 and BUILT17 each land as one newline plus the slice plus one newline.

CONTAINMENT TEST, run by the reviewer on the final bytes, output quoted:
  MAPFROM17/MAPTO17 — `TO contains FROM: false` → REWRITE.
That is the reading for every pair this block carries, taken per pair.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your slices; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    registers findings, so the plan advances before anything else but the two
    block-save commits.
 3. COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5 and no other. Within
    `.agent/live_review.md` the pair at C2 precedes that file's append at C3
    (R-0639/R-0640), so the append reads a remainder no pair will change.
 4. LEDGER17 holds, in this order and separated by ONE blank line: the `- R-0674`
    record, the `- R-0675` record and the `Gate: R16` paragraph. It lands in ONE
    commit, C3, or none of it does: the gate paragraph states that both findings
    are registered in that same commit, and THIS constraint is what makes that
    true (§3 item 20, R-0524 carve-out).
 5. NO PRODUCTION CODE AND NO TESTS. Nothing under `apps/`, `packages/` or
    `tests/` is in the Change set. The one `docs/` path is the feature file,
    whose Built State is a closure precondition and not a repair.
 6. NO REPAIR of any open finding. R-0674 and R-0675 are RECORDED, not fixed.
    Their subjects are the reviewer's own R16 block and the R16 handback, and
    §3 item 20 forbids rewriting either.
 7. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback.
 8. Every numeral this block states about the ROUND BASE `acc27057` was produced
    by a reviewer script or tool run at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
 9. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 388 lines TOTAL with 126 CONTENT
    lines inside its slices, so PROSE is 262 — under DECISION F085 D6's
    490 and D5's 400.
10. The branch is TWO commits behind `origin/main`, which gained the packaging
    fix of pull request #212 after this branch was cut. This round does NOT
    merge or rebase `main` into it: F021's closure zip was built before #212
    existed, so R18 has a working precedent, and a merge commit here would be
    scope drift into a round whose Change set is state and one docs file.

─── Why this round exists ─────────────────────────────────────────────────────

R16 passed on every one of its eleven gates under the reviewer's own re-runs,
and its verdict is not on disk: DECISION F085 D9 rules that a PASS is written by
the NEXT round's ledger commit, so the last round of every session strands its
own. R16 also produced two findings, and §4 item 4 rules that findings persist
FIRST, in their own commit, before anything else is attempted with them.

The Built State is the other reason. `docs/roadmap/STATUS_closure_protocol.md`
precondition 4 requires the feature file's Built State section to be current,
and step 5 of the same algorithm restricts the closure commit to STATUS.md,
README.md and `.agent/`. `docs/roadmap/features/T5_F022.md` at `acc27057` has no
`## Built State` section at all — the reviewer measured its eight `^## `
headings and none of them is that one — so the section cannot be written at
closure without breaking the exact-paths rule, and it is written here instead.

Closure therefore runs over three rounds, which is what C2 repairs the map to
say: this one brings the content current, R18 runs the evidence job and builds
the review zip, and R19 authors the STATUS line from the values only that zip
can produce and creates the PR. A STATUS line naming a package SHA-256 that does
not yet exist is the R-0371 shape this workflow forbids outright, so the split
is not a convenience.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). Gates G1
through G12 all run after C4 and BEFORE C5, so the handback can quote every one
of them (§3 checklist item 31); G13 is the single exception and says so in its
own text. The round base is `acc27057` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C5.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a, C0b, C1, C2, C3 and C4.
 G2  TRANSPORT. sha256 over the block file at `.remedy-wt/f022-r17-final.md`, over the
     committed C0a blob, over the committed C0b blob and over
     `.agent/last_block.md` on disk: report all four digests, byte counts and
     line counts, and require them EQUAL. The digest the delegation names is the
     fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     PROSE is TOTAL minus CONTENT, so the marker lines count as prose. Report
     those against constraint 9's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R17 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, and `wc -l` STRICTLY UNDER 50 — AGENTS.md caps this file at fewer
     than 50 lines, so report the number you measure.
 G5  THE PAIR at C2 in `.agent/live_review.md`. Report the containment output
     and require it to match the convention block. MAPFROM17 1x at the round
     base and 0x at C2; MAPTO17 0x at base and 1x at C2; the file's byte length
     changing by exactly `len(MAPTO17) - len(MAPFROM17)`; `^## Steps$` still
     exactly once; and the committed file equal to the base file with only that
     replacement applied and nothing else. ALSO report the longest line length
     of the `## Steps` paragraph at C2: no line in it may exceed 84 characters
     (R-0431).
 G6  APPEND at C3, proved twice. The C2 blob is a byte-exact PREFIX of the
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
     ~20 bytes surrounding the flip. Remove the worktree BY ITS EXACT PATH,
     never by a glob (R-0662); `git worktree list` back to one line.
 G7  LEDGER INTEGRITY, base versus C3. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-` with its distinct ids, of `^Landed: `, of
     `^Recurrence: R-` with its DISTINCT ids, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and REMOVED as sets. At base the
     reviewer measured 234 records, all distinct, maximum `R-0673`, 2 `Done:`
     lines over `R-0653` and `R-0670`, 0 `Landed:`, 10 `Recurrence:` lines over
     8 DISTINCT ids, and 16 `Gate:` lines over 16 distinct keys, none of them
     `R16`. This round MINTS EXACTLY TWO IDS: the ids ADDED must be exactly
     `R-0674` and `R-0675`, the ids REMOVED the EMPTY SET, the record count 236,
     the maximum `R-0675`, the `Recurrence:` readings UNCHANGED at 10 over 8,
     and the `Gate:` keys must gain exactly `R16`. Report what you measure.
 G8  APPEND at C4 in `docs/roadmap/features/T5_F022.md`, proved by the SAME two
     readers and the same byte-flip control as G6, with the offset named and the
     worktree removed by its exact path. ALSO report, at the base and at C4: the
     count of `^## ` headings, and the count of `^## Built State$`, which must be
     0 at the base and 1 at C4. THEN, because the Change set holds a
     `docs/roadmap/**` path, run at C4 in the PRIMARY checkout and report the
     real exit code of `python3 -m pytest tests/docs/ -q` and of
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`.
     WHAT THOSE TWO SUITES DO AND DO NOT CERTIFY, measured by the reviewer at
     `acc27057` in a disposable worktree with three red controls: with this
     exact BUILT17 slice applied they read 295 and 30, both exit 0. Replacing
     the whole Built State BODY with unrelated text still reads 325 passed
     together, and changing the title's prose while keeping the id `T5_F022`
     also still reads 325 passed; only changing that id to `T5_F999` goes red,
     at 11 failed. So these suites key on the feature file's F-ID and are BLIND
     to the section you are adding. They are ordered because the docs-round gate
     requires them and because they prove the append broke no index consistency
     — they are NOT evidence that the Built State is correct. The two readers
     and the heading counts above are what carry that, which is why they come
     first in this gate. This is open finding R-0493 measured again at a new
     commit, not a new defect: mint no id for it.
 G9  THE FOUR STATE READERS plus THE CANARY, serially in the PRIMARY checkout at
     C4, exit 0: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, then
     `tests/cli/test_golden_path.py`. The reviewer ran all five itself at the
     round base and measured 470, 52, 21 and 16 for 559 across the four, and 42
     for the canary. Never run two pytest processes at once (R-0619). THE FULL
     SUITE IS NOT RE-RUN: R15 ran it twice, the reviewer re-ran it once itself,
     and closure re-confirms it.
 G10 STRUCTURE, reported for the commits BEFORE C5 and for the range as a whole
     (C5's own numbers belong to the next round's ledger entry, not here):
     every commit single-parent; each commit's INSERTION count, each under the
     500 cap; the range path set against the Change set above with the
     difference reported in BOTH directions; `git show --numstat` agreeing cell
     by cell with the handback's `## Commits` table; the LINE-ANCHORED patterns
     `^<<<SLICE ` and `^<<<END ` counting 0 in `.agent/plan.md`,
     `.agent/live_review.md` and `docs/roadmap/features/T5_F022.md`;
     `git ls-files .remedy-wt` 0; one worktree; and the round's reflog rows with
     amend, rebase and cherry counted IN THE OPERATION FIELD before the first
     colon (R-0613), each 0.
 G11 `gh pr list --state open --json number,headRefName`. Report it verbatim.
     Create no PR and merge nothing. CLOSURE HAS NOT RUN: the closure protocol
     creates the PR itself, at R19, after the evidence job and a FRESH zip.
 G12 STALENESS. Every sentence C1, C2, C3 and C4 land that states a fact about a
     file is re-measured at C4, and any that has gone stale is reported as a
     residual rather than repaired. Report explicitly that you checked, and name
     any residual. Slices are NEVER edited to fix one.
 G13 PUSH, ordered explicitly because R-0674 is what happens when it is not:
     after C5, run `git push origin feature/f022-live-cost-ticker` and report its
     REAL exit code and the remote tip afterwards from
     `git ls-remote origin feature/f022-live-cost-ticker`. No `--force`, no
     `--force-with-lease`, no history rewrite, no branch deletion. This is the
     ONLY gate that runs after C5, so its reading belongs in the handback's
     `## External actions` section as a stated intent plus the outcome, and NOT
     in a gate line whose value C5 would have had to know before it existed
     (§3 checklist item 31).

NOT A GATE and not run this round: `npm run lint`, `npm run typecheck` and
`npm run test:unit`. The Change set holds no file under `apps/`.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             every mandated section in order, one changed-files table per
             commit, an item-status row per Bundle item, the round base SHA,
             ONE line per gate, and the `Fortschritt:` block above carried
             VERBATIM across all four of its lines. Every count you report
             names the exact string or pattern counted and the file it was
             counted in (R-0442). The cap is 60 lines for this commit count;
             declare a DECISION D15 stated cause with your own measured numeral
             in the declaring line if the mandated content genuinely does not
             fit. Any commit you make BEYOND the sequence constraint 3 names gets
             its own `## Commits` row and its own item-status row, and the
             Deviations section says so in the same words: that omission is
             finding R-0675, which this block registers.
             `## Next` names R18: the evidence job and the review zip, per
             docs/roadmap/STATUS_closure_protocol.md steps 1 and 2 — a failing
             zip build is a closure BLOCKER, and the STATUS line is authored by
             the reviewer at R19 from the values only that zip produces.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R17
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
R17 records the R16 verdict, registers findings R-0674 and R-0675, repairs the
round map for a three-round closure, and writes the feature file's `## Built
State` section. It builds no product code: T001, T002 and T003 are complete and
the integration gate has passed.

## Next Steps
1. R18 the evidence job and a FRESH review zip, per
   docs/roadmap/STATUS_closure_protocol.md steps 1 and 2. A failing zip build is
   a closure BLOCKER, never a thing to work around.
2. R19 closure: the reviewer authors the STATUS line from the values only that
   zip produces, the worker commits it last with the README capability sync in
   the SAME commit, and creates the PR.

## Risks
- The closure PR is created but NOT merged by the round that makes it: it merges
  at the NEXT feature's Open PR Gate, which preserves the operator's window.
- Closure precondition 4 was never satisfiable at closure itself: the closure
  commit's allowed path set holds no feature file, so the Built State must land
  before the package. R17 is that round.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured; R-0431, R-0413 and R-0533 are recorded and
  already paid for; R-0674 and R-0675 are registered by this round and repaired
  by none, their subjects being landed append-only text; and R-0445 is a
  standing defect of `docs/agents/integration_gate.md`, routed by the finding
  itself to a follow-up branch rather than to this one.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
<<<END PLANF022R17

<<<SLICE MAPFROM17
R15 verdict and end that session at its round budget → R17 closure. This
section is the only place the round map is stated, per
<<<END MAPFROM17

<<<SLICE MAPTO17
R15 verdict and end that session at its round budget → R17 record the R16
verdict, register two findings and write the feature file's Built State → R18
the evidence job and the review zip → R19 closure. This
section is the only place the round map is stated, per
<<<END MAPTO17

<<<SLICE LEDGER17
- R-0674 — Medium, A BLOCK'S CHANGE-SET PATH LIST WAS READ AS BOUNDING THE ROUND'S ACTIONS, SO A SESSION ENDED WITH ITS WORK UNPUSHED UNTIL THE WORKER CLOSED THE GAP ON ITS OWN INITIATIVE. Raised by the reviewer while gating R16. THE MEASUREMENT, re-taken at `acc27057` by the session that registers it: the R16 block, committed at `43705254`, contains the string `push` ZERO times under a case-insensitive search of its 266 lines, and its `Change:` section names five `.agent/` paths under the words "Exactly these paths, nothing else". The R16 handback's FIRST version, committed at `f50615d8`, drew the conclusion the block invited and recorded it as a deviation: "The branch was NOT pushed: `git push` is outside this block's Change set and the block orders no push." THE RULE THAT CLAUSE CONTRADICTS is not obscure and is not in this document: AGENTS.md Push Discipline reads "After committing: git push -u origin <branch>", and its Task Completion Protocol reads "Do not treat local-only committed work as finished" and lists a pushed branch among the conditions for review-readiness. Both bind the WORKER directly and neither is conditional on any block naming them. WHY THIS IS THE REVIEWER'S DEFECT AND NOT THE WORKER'S: a change set is a list of files a round may WRITE, and it was read — reasonably, given the words "nothing else" — as a list of things the round may DO. The two are different kinds, and every block in this workflow states only the first while the worker is bound by both, so the ambiguity is structural rather than a slip of that one block. WHAT IT COST AND WHY MEDIUM RATHER THAN LOW: docs/agents/self_drive_protocol.md exists because the operator reaches this machine only over SSH from a phone, and the pushed branch plus the review zip are the operator's entire remote window into a run. A session that ends with six commits alive only in one local checkout has no return channel that survives the machine, which is the precise failure the protocol was written to prevent — and R16 was a session-ending round, so the gap would have persisted until the next session noticed it. THE WORKER CLOSED IT CORRECTLY AND SAID SO: it pushed after the reviewer's gate, exit 0, and rewrote the deviation into a disclosure at `08c3c22c`, naming the correction as a correction. The reviewer of that round confirmed the remote independently at `git ls-remote origin feature/f022-live-cost-ticker` reading `08c3c22cfbf52092853fba45594bcef830b61718`, which was R16's tip; the session registering this finding re-confirmed at `acc27057` that the local and remote tips of this branch are again equal, so nothing was ever lost and only the rule is. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED, as §3 checklist item 30 requires, and the nearest OPEN neighbour is R-0673, which is a reviewer gate forcing an edit the same block's change list did not LICENSE — a change set too NARROW for an ordered WRITE, where this is a change set read as forbidding an ACTION that no block needs to license. R-0673's counter-measure, running a whole-file absence over the file at the base first, does not reach this instance, so this is a distinct defect and not a second id for it. THE FIX, BINDING ON EVERY BLOCK THIS WORKFLOW EMITS FROM HERE: a block's Change set carries one sentence stating that it bounds what the worker WRITES and not what the worker DOES, and any round that ends a session ALSO carries an explicit push gate whose reading the handback reports. The R17 block that registers this finding carries both, which is the only reason this entry can claim the counter-measure exists rather than naming a round that will build it (§3 checklist item 11).

- R-0675 — Low, A CORRECTION COMMIT CHANGED THE ROUND'S OWN COMMIT SET AND LEFT THE CLAUSE DENYING IT STANDING TWO LINES ABOVE THE DISCLOSURE. Raised by the reviewer while gating R16. THE MEASUREMENT, taken at `08c3c22c` and re-taken at `acc27057` by the session that registers it: `git rev-list f51be462..08c3c22c` walks SEVEN commits, and the R16 block's Bundle names six — C0a, C0b, C1, C2, C3, C4. `.agent/handoff.md` at that same commit carries six `### ` per-commit sections and six item-status rows, so the seventh commit has neither a `## Commits` row nor an item-status row, against docs/agents/handback_template.md's per-commit table and AGENTS.md's "Every ordered item appears exactly once. No item may be silently absent." Its Deviations section reads "The ordered commit sequence C0a, C0b, C1, C2, C3, C4 was followed exactly. No extra commit, none dropped, no reordering." — and the NEXT bullet but one reads "this correction commit is pushed after it", so one file both denies and discloses the same commit. THE MECHANISM IS WHAT EARNS THE ID: the seventh commit is the one that REWROTE the handback, so it changed the very range the text it was writing quantifies over. Every clause of a handback that counts the round's commits is falsified by the act of correcting that handback, and the correcting commit is the last place anyone re-reads the sentences it did not come to change — R-0481's shape, a late change swept through what could be COUNTED and not through what was merely WRITTEN, arriving here through a self-correction rather than through a late finding. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED, as §3 checklist item 30 requires, and two OPEN neighbours are close enough to name. R-0605 is a GATE ordering a round's commit count as an equality the handback commit cannot reach, so the record understates its round by one; its counter-measure — a count gate names only the commits BEFORE the handback commit — would leave this instance untouched, because here no gate ordered the count and the extra commit is one the worker CHOSE to make after the text was fixed, which could have carried its own row. R-0557 is a block's Handback sentence saying seven over a Bundle naming eight, which is item 16's drifting-numeral class and not a range changed after the fact. Neither describes this defect, so the id is minted rather than the evidence being added to theirs. WHY LOW: nothing is fabricated, nothing is hidden, and no gate reading is touched. The reviewer re-ran all eleven of R16's gates and every one reproduced exactly, the extra commit is `+2/-2` over a path already in the Change set, and the same file discloses it in plain words. What landed is one false sentence in the map AGENTS.md's Session Resume tells the next session to read SECOND. THE FIX, BINDING ON THE NEXT BLOCK THAT ORDERS A HANDBACK: the Handback paragraph requires any commit beyond the ordered sequence to receive its own `## Commits` row and its own item-status row, and requires the Deviations section to say so in the same words rather than beside a clause that denies it. THE LANDED TEXT IS NOT REWRITTEN — §3 checklist item 20 forbids repairing an append-only record by overwriting it, and this dated entry is the counter-measure.

Gate: R16 — the F022 R16 entry. R16 PASSED ON EVERY ONE OF ITS ELEVEN GATES, AND THE SESSION WRITING THIS ENTRY RE-RAN THEM ITSELF AT `acc27057` RATHER THAN READING THE HANDBACK'S WORD FOR ANY OF THEM. THE ROUND BUILT NOTHING AND WAS NOT SUPPOSED TO: its five content commits carry only `.agent/` state, so the finding of this gate is that a session-ending record round put the R15 integration-gate verdict onto disk without touching a line of product. TRANSPORT HELD IN ITS STRONGEST FORM: the committed C0a blob at `43705254`, the committed C0b blob at `5953f84b`, and both `.agent/last_block.md` and `.agent/authored/f022-r16.md` at the branch tip `acc27057` are ALL sha256 `f4b61e421e29f166dd6ce4d3a9a80a8140732d2efd4e4281f1767f9843b8747f` over 24788 bytes and 266 lines, and C0a and C0b resolve to the SAME git blob `b380d020`. THE EXTRACTION printed 4 slices over 52 CONTENT lines against a TOTAL of 266, so PROSE is 214 and constraint 9 reproduces exactly. `.agent/plan.md` at `aa1206f8` is 2543 bytes, which is PLANF022R16's 2542 plus one newline, with `^## Goal$` and `^## Next Steps$` once each and 44 lines against the cap of 50. THE PAIR AT `44247805` IS A REWRITE and was proved as one: the containment test printed `TO contains FROM: false`, MAPFROM16 went 1 to 0 and MAPTO16 0 to 1, the file grew by exactly 72 bytes matching the length difference of the two halves, `^## Steps$` stayed at 1, the committed file equals the base file with only that replacement applied, and the longest line of the `## Steps` paragraph is 80 against the 84 cap. THE APPEND AT `c27f255e` HOLDS UNDER BOTH READERS: the C2 blob is a byte-exact PREFIX of the C3 file and the remainder is 7754 bytes, which is one newline plus LEDGER16's 7752 plus one newline, while an independent blank-line split counted N as 2 paragraphs and found the LAST 2 units equal to them IN ORDER, 278 units becoming 280. THE SETS MOVED EXACTLY WHERE THE ROUND PROMISED: 234 records at base and at C3, all DISTINCT at both with maximum `R-0673`, ids ADDED and ids REMOVED both the EMPTY SET so NO ID WAS MINTED, `^Recurrence: R-` 9 becoming 10 over 8 DISTINCT ids by gaining a SECOND `R-0445` line, `^Gate: R` 15 becoming 16 by gaining exactly the key `R15`, and `R-0445` still exactly one `^- R-\d+ — ` record. THE FOUR STATE READERS AND THE CANARY WERE RE-RUN SERIALLY BY THIS SESSION IN A DISPOSABLE WORKTREE AT `acc27057`, all exit 0: `tests/ui_server/` 470, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 for 559 across the four, and `tests/cli/test_golden_path.py` 42 — reproducing the handback cell for cell. STRUCTURE HELD: the anchored markers `^<<<SLICE ` and `^<<<END ` count 0 in both state files, `git ls-files .remedy-wt` is 0, one worktree, and amend, rebase and cherry are each 0 in the reflog's OPERATION field. THE OPEN PR GATE printed an empty JSON array and no PR was created. THE ROUND'S TWO DEFECTS ARE THE REVIEWER'S AND ARE REGISTERED IN THIS SAME COMMIT as R-0674 and R-0675, which block constraint 4 is what makes true: the block ordered no push and the branch was briefly local-only, and the worker's own correction commit left a clause denying its existence. Both were caught and disclosed by the WORKER before any reviewer read them, which is the second consecutive round in which the honest handback is what made the finding possible. THE VERDICT IS PASS: every gate reproduced under an independent re-run, no slice was edited, no id was minted by that round, and the R15 integration-gate verdict is now on disk where the next session can read it without paying for two more full-suite runs.
<<<END LEDGER17

<<<SLICE BUILT17
## Built State
Measured at `acc27057`, the branch tip this section was written against. The
F022 integration gate ran at `f51be462`, and every commit between the two
touches only `.agent/` state, so no file named below has changed since the gate.

- **T001 — the tick emission, its envelope and its catalog key:**
  `packages/orchestration/safe_points.py` gains `_budget_tick_payload` and
  `_emit_budget_tick`, both reached from `should_stop`, so the tick is emitted
  at the safe-point evaluation that already computed the figures and never on a
  cadence of its own. The payload carries `spent_tokens`, `unmeasured_calls` and
  the `basis` verbatim, with the currency fields present only when a price basis
  exists — no invented dollars. The SSE side is
  `packages/orchestration/ui_server.py`, where `BUDGET_TICK_EVENT` names the
  kind `budget.tick` and `_budget_tick_summary_payload` passes exactly the
  fields `BUDGET_TICK_SUMMARY_FIELDS` and `BUDGET_TICK_BASIS_FIELDS` whitelist,
  for that kind alone (DECISION F022 D3). The client vocabulary gains one key in
  `apps/ui/src/api/humanizeCatalog.ts`, which DECISION F022 D1 pins EQUAL to the
  Python set so neither may move alone.

- **T002 — the COST metric: one arithmetic home, one already-decided view:**
  `apps/ui/src/api/costMetric.ts` is the whole of the client's arithmetic and
  its only arithmetic is the fill ratio. `costMetricOf` turns budget-tick
  figures into a `CostMetricView` carrying `unit`, `level`, the `~` estimate
  marker from `isEstimated`, and already-worded tooltip lines from `limitLine`,
  `unmeasuredLine` and `basisLine`; the thresholds are that module's own
  `WARN_FILL` and `EXCEEDED_FILL`, so `level` arrives decided.
  `budgetTickFiguresOf` in `apps/ui/src/api/budgetTick.ts` is the only reader of
  the wire shape. `apps/ui/src/components/metrics/TopMetricsBar.tsx` renders
  from that view and classifies nothing: `costLevelClass` maps the view's own
  `level` onto the track treatment in `TopMetricsBar.module.css`, and
  `costLevelPhrase` puts the same band into the accessible name, because
  DECISION F022 D5 clause 3 forbids a state a reader can only see as a tint.

- **T003 — the live wiring and the terminal reconciliation:**
  `apps/ui/src/api/brainStream.ts` holds the latest tick as the single `budget`
  field of the stream state, folded behind the same reconnect-replay guard as
  the ring (DECISION F022 D6); a frame that is not a tick carries the previous
  figures forward BY REFERENCE, because the runner compares that field with
  `===` and a fresh equal object would announce a change nobody made.
  `metricsWithCostTicker` (`apps/ui/src/api/costTicker.ts`) composes the live
  tile, and `metricsWithCostReconciliation`
  (`apps/ui/src/api/costReconciliation.ts`) WRAPS that output and replaces the
  tile with the ledger's own figure once the job has stopped, adding
  `costFinalNote` only when the two displays differ (DECISION F022 D8). The
  ledger figure is the `budget_final` section built by `_build_budget_final` in
  `packages/orchestration/ui_server.py` from the last `budget.tick` in the job's
  run log: DECISION F022 D7 replaced the feature file's "stats endpoint", which
  `ui_server.py` does not dispatch, and made the delta a TRANSPORT statement —
  what the client received against what the ledger holds — rather than a second
  arithmetic. `apps/ui/src/components/shell/RemedyShell.tsx` composes the two in
  that order, and `remedyApi.ts` seeds the eighth tile `unknown` with an em dash
  while deliberately giving the degraded dashboard path no cost tile at all.

- **Where the tests live:** `tests/orchestration/test_budget_tick.py`,
  `tests/ui_server/test_budget_tick_envelope.py`,
  `tests/ui_server/test_budget_final_section.py` and
  `tests/ui_contracts/test_cost_metric_render.py` on the Python side; under
  `apps/ui/src/api/`, `budgetTick.test.ts`, `costMetric.test.ts`,
  `costTicker.test.ts`, `costReconciliation.test.ts`, `brainStream.test.ts`,
  `brainStreamRunner.test.ts` and `remedyApi.test.ts`.

- **Where the reasoning lives:** DECISIONs F022 D1 through D8 in
  `.agent/decisions.md` rule the tick envelope, the tick's writer, the
  whitelisted pass-through, the client's cost reading, the render contract,
  where the live tick is held, the reconciliation's source, and when the ledger
  figure replaces the live one.
<<<END BUILT17
