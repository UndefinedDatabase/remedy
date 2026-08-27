STEP R1 / F032 — APPROVAL WITH THE EVIDENCE TRIPLE
Goal:        CLAIM F032. Cut the branch, flip `docs/roadmap/STATUS.md` from
             `[ ]` to `[~]`, reset the live-review header for the new feature
             carrying every finding record forward, and put the F032 SOURCE
             INVENTORY on disk. The inventory is this round's substance, not
             its bookkeeping: the feature file calls the enforcement point "the
             enqueue seam every producer already funnels through", and the
             eight producing branches of `decision_queue.list_decisions` derive
             from eight different subsystems. Whether such a seam exists at all
             is a MEASUREMENT this feature must take before it plans T001.
             YOU CREATE NO PULL REQUEST THIS ROUND AND YOU MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan and the context · C2 the STATUS claim · C3 the live-review
             header reset · C4 the inventory · C5 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r1.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/context.md`,
             `docs/roadmap/STATUS.md`, `.agent/live_review.md`,
             `.agent/f032_inventory.md`, `.agent/handoff.md`. This list bounds
             what you WRITE INTO THE REPOSITORY. It does NOT bound what you DO:
             G8 orders a branch creation and a push. NOTHING under `apps/`,
             `packages/` or `tests/` is written, and under `docs/` ONLY
             `docs/roadmap/STATUS.md`.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f032-r1.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f032-r1.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own, because a digest
    written inside the text it measures cannot be true; G2 has you measure four
    points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice contradicts something you measure,
    apply it anyway and DECLARE the contradiction in the handback under
    Deviations — a corrected slice destroys the transport proof. Declaring
    beats fixing every time, because a declared contradiction reaches a
    reviewer who can measure it while a silent fix reaches nobody.
 3. THE BRANCH IS CUT BEFORE C0a. From `main` at `a399a330`, which is where
    your `git rev-parse HEAD` must already stand, run
    `git checkout -b feature/f032-evidence-triple`. Every commit of this round
    lands on that branch. NEVER COMMIT ON `main`.
 4. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5. Every sentence in
    PLANF032R1 that describes THIS round's own landed change depends on that
    order, and this constraint is what fixes it.
 5. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES THE amend0827
    ORDER. That is ordered: the plan becomes current at C1, which is the FIRST
    substantive commit of the round.
 6. NOTHING IS EDITED OUT OF THE FINDINGS REGION. `.agent/live_review.md` is
    append-only from its `## Findings` heading down. This round rewrites ONLY
    the header region ABOVE that heading, via the single LFROM/LTO pair. No
    finding paragraph, no `Done:` line and no `Gate:` paragraph is rewritten,
    deleted, renumbered or touched, and NO finding is registered or resolved
    this round.
 7. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Gate:` paragraph of
    your own, never mint a finding id and never author a `Done:` line. If you
    find a defect, report it in the handback under Deviations and let the
    reviewer rule on it.
 8. THE INVENTORY IS YOURS TO WRITE AND IT IS THE ONLY SUCH FILE. Everything
    in `.agent/f032_inventory.md` is YOUR OWN MEASUREMENT, written by you, not
    a slice. Every answer cites `path:line` or a command and its real output.
    WHERE YOU CANNOT MEASURE SOMETHING, WRITE THAT YOU COULD NOT AND WHY —
    an honest gap is worth more to the next round than a confident guess, and
    a guess in an inventory becomes a wrong T001 plan.
 9. RE-READ `.agent/STOP` FROM DISK before C0a and again before C5. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
10. NOTHING DESTRUCTIVE IS ORDERED THIS ROUND. Create no worktree. The primary
    checkout reads `git status --porcelain` 0 lines at every commit.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `a399a330` was
    measured by the reviewer at that commit. It is a REFERENCE to report
    against, NOT a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
13. THE TWO REPLACEMENT PAIRS ARE CLASSIFIED BY A MECHANICAL CONTAINMENT TEST
    THE REVIEWER RAN, one reading per pair, and the output is printed here.
    LFROM/LTO — `TO contains FROM: false`, so REWRITE. SFROM/STO —
    `TO contains FROM: false`, so REWRITE. Both therefore carry the FROM-zero
    obligation of §4.9 and neither carries the append obligation.
14. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 1
    of F032 and that R1 is the round. The handback has NO LENGTH CAP — operator
    amendment amend0827 rule 3 withdrew every tier — so do not declare, measure
    or apologise for its length. It is VALID when its mandated sections are
    present, and DROPPING one is the finding the cap used to stand in for.

Inventory spec — `.agent/f032_inventory.md`, answer each, MEASURED:
 Q1. THE ENFORCEMENT POINT, which is the question that decides T001. For EACH
     of the eight numbered producing branches of
     `packages/orchestration/decision_queue.py::list_decisions`, name the
     branch number, the decision `type` it mints, the id prefix it uses, and
     the module and function that CREATES the underlying record it derives
     from. Then answer in one sentence: is there a single function every one of
     the eight passes through on the way in? If there is not, say so plainly
     and name every distinct creation site, because the feature file's design
     assumes there is one.
 Q2. THE SCHEMA AS BUILT. The full field list of `HumanDecision`, what
     `export_decision_json` emits, and whether `payload` is the only additive
     slot. State whether any producer writes `payload` today and which.
 Q3. WHERE A DECISION IS PERSISTED. The feature file's Do-not-touch names
     "queue storage". Name what storage exists, in which module, and whether
     `list_decisions` reads it or derives around it. Cite the file.
 Q4. THE EVIDENCE-REF VOCABULARY. Find the typed provenance vocabulary the
     feature file names ("file/failure/decision kinds") and its resolver, with
     the module path, the type names and the badge values the resolver
     produces. If no such vocabulary exists under that name, say so and name
     the nearest thing that does.
 Q5. THE OPTIONS LIST. `expected_outcome` and `downside` are keyed PER OPTION,
     so name where a decision's options come from today: the `options` field of
     an escalation record, `next_actions`, or both, and whether every one of
     the eight branches has options at all.
 Q6. THE CARD SURFACE. In `apps/ui/src/api/decisionCard.ts`, name what a card
     renders today, which fields it reads, and where a chip row would attach.
     Name the test file that pins it.
 Q7. THE MIGRATION PRECEDENT. Find how this repository has versioned a payload
     before — `DECISION_INBOX_VERSION` is one; name every other you find — and
     state in one sentence what a v1 record looks like to a v2 reader today.
 Q8. THE GUARDS A SCHEMA CHANGE MUST SATISFY. Run
     `rg -ln 'decision_queue|HumanDecision|export_decision_json' tests/` and,
     for what it returns, list every assertion that COUNTS something over a
     whole file or pins an exact field set or an exact list of types — the
     equality guards a new required field would turn red. Cite `path:line` for
     each.

Done when:
 G1. HYGIENE, THE BRANCH AND THE SENTINEL. Report `git rev-parse HEAD` BEFORE
     the branch is cut, which must be `a399a3304f9d962cd920c251488c40c486b35fdc`,
     and `git branch --show-current` after C0a, which must be
     `feature/f032-evidence-triple`. Report `git status --porcelain` as a LINE
     COUNT after each of C0a, C0b, C1, C2, C3, C4 and C5, each 0. Report
     `.agent/STOP` read from disk before C0a and before C5, both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f032-r1.md`, as saved at C0a, as mirrored at C0b and
     as read off disk at C4 — all four must be EQUAL — and say whether C0a and
     C0b are the same git blob. Report whether any line of the block as saved
     is a run of a single repeated character at length 4 or more, which must
     come back as none. THEN STATE IN ONE SENTENCE WHAT THIS PROOF COVERS: the
     scratch file, the saved copy, its mirror and the working copy, and NOT the
     bytes of any prompt.
 G3. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES. Report how many slices your extractor printed, each
     slice's own line count, the CONTENT total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE at most 400, TOTAL at
     most 490.
 G4. THE PLAN AND THE CONTEXT. `.agent/plan.md` at C1 is BYTE-EQUAL to
     PLANF032R1 and `.agent/context.md` at C1 is BYTE-EQUAL to CTXF032R1, both
     under the newline-INCLUDED convention. Run the negative control against
     each slice MINUS its trailing newline and report both FALSE. Then report
     the contract readings: in `.agent/plan.md`, `^## Goal$` 1, `^## Next Steps$`
     1, a match for `\bF\d{3}\b`, and `wc -l` STRICTLY UNDER 50; in
     `.agent/context.md`, `^## Active Branch$` 1, a match for `feature/`, a
     match for `\bF\d{3}\b`, and the substring `Steps` present.
 G5. THE LEDGER RESET, AND THE FINDINGS REGION PROVED UNTOUCHED. Apply the
     LFROM/LTO pair to `.agent/live_review.md`. Then, comparing the pre-commit
     blob with the file at C3: report that LFROM occurs EXACTLY ONCE before and
     0 times after, and LTO 0 times before and EXACTLY ONCE after. Report the
     byte count and sha256 of everything from the first byte of the line
     `## Findings` to end of file, at BOTH points, and prove them EQUAL — the
     reviewer measured that region at the round base as 1023923 bytes,
     sha256 `3c0dac3dd2b4a9292722f0ec94598b9aa4c34e0ba255a28aaf896865699081d1`.
     Report the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — ` at both points;
     the reviewer measured 270, 21, 0, 19 and 53 at the base and EVERY ONE MUST
     BE UNCHANGED. Report the finding ids and the resolved ids ADDED and
     REMOVED as SETS — all four must be EMPTY — whether all ids are DISTINCT,
     the maximum id at each point, which is `R-0709`, and the open set at each
     point, which is 249. Report that `^## Findings$` occurs exactly 1 at both
     points and that `Steps` is present at both.
 G6. THE STATUS CLAIM AND THE DOCS GATE. Apply the SFROM/STO pair, then BEFORE
     committing C2 run, as ONE pytest process, `python3 -m pytest tests/docs/
     tests/orchestration/test_roadmap_index.py -q` from the repository root and
     report the REAL exit code and the summary line VERBATIM; the reviewer
     measured `325 passed` at a real exit 0 at the round base. Then report, for
     `docs/roadmap/STATUS.md` at C2: SFROM occurs 0 times and STO occurs
     EXACTLY ONCE; the line-anchored counts of `^- \[ \] `, `^- \[x\] ` and
     `^- \[~\] ` at both points, which the reviewer measured as 197, 58 and 0
     at the base and which must read 196, 58 and 1 after; and that the total
     count of lines matching `^- \[` is UNCHANGED at both points.
 G7. THE STATE READERS AND THE CANARY, run AFTER C4 and BEFORE C5. This round
     rewrites `.agent/` state, so `.agent/context.md`'s standing constraint
     binds: run, as ONE pytest process and never two at once, `python3 -m
     pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
     -q` from the repository root. Report the REAL exit code, the summary line
     VERBATIM, and the COUNT of lines matching `^FAILED`. PROVE YOUR `^FAILED`
     EXTRACTOR IS NOT BLIND by running it over a string you know contains such
     a line and reporting that it matched. The reviewer measured `620 passed`
     at a REAL exit 0 with zero `^FAILED` lines at the round base. IF YOUR RUN
     IS RED, report the failing node ids VERBATIM and hand back.
 G8. STRUCTURE, ARTIFACTS, THE OPEN PR GATE AND THE PUSH. Compare the path set
     of `git diff --name-only a399a330..C4` BOTH WAYS against this round's
     expected set — the Change line's list MINUS `.agent/handoff.md`, which C5
     writes — and report both residues EMPTY. Report `git diff --stat
     a399a330..C4` restricted to `apps/`, `packages/`, `tests/` and `docs/` —
     the last WHOLE — and confirm the first three EMPTY and the fourth holding
     `docs/roadmap/STATUS.md` alone. Report each commit's insertions from `git
     diff --numstat` for C0a through C4, confirm each single-parent and under
     500. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
     `.agent/plan.md`, `.agent/context.md` and `.agent/live_review.md` at their
     commits, against a CONTROL over the C0a blob which is not 0. Report `git
     ls-files .remedy-wt` 0 lines, `git worktree list` 1 line, and `git branch
     --list "tmp/*"` 0 lines. Run `gh pr list --state open --json
     number,headRefName,baseRefName,isDraft` and report it VERBATIM; the
     reviewer read `[]` at the round base; MERGE NOTHING and CREATE NOTHING.
     After C5, run `git push -u origin feature/f032-evidence-triple`. ITS
     OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: C5 is authored
     before the push exists, so `.agent/handoff.md` states the push only as an
     INTENT under `## External actions`, with NO exit code and NO remote tip.
     Report the real exit code and the resulting remote tip in your completion
     report instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C5: the `## Session` section constraint 14 orders, feature and
             round, branch, the round base SHA `a399a330`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item AND every Q1-Q8 inventory
             question, ONE LINE PER GATE for G1 through G8 with its real exit
             code, the open-findings count after this round, and the next
             expected action. C5 cannot table its own numstat — write `self` in
             that cell, as `R-0149` requires, and put C5's own numbers nowhere.
             STATE PLAINLY in the Deviations section what Q1 measured about the
             enqueue seam, because that answer decides whether the feature
             file's Design survives contact with the source and the reviewer
             rules on it next round.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.

<<<SLICE PLANF032R1
# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the orchestrator brief.

## Current Step
R1 claims F032 in the roadmap ledger, cuts the branch, resets this record set
for the new feature and puts the F032 source inventory on disk. The inventory
is the round's substance: the feature file's design names one enqueue seam
"every producer already funnels through", while the eight producing branches of
`decision_queue.list_decisions` derive from eight different subsystems, so
where the gate can live at all is a measurement this feature takes before it
plans T001.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 plan and context for F032 | ordered | first substantive commit |
| C2 STATUS claim, open to active | ordered | |
| C3 live-review header reset | ordered | findings carried forward |
| C4 the F032 source inventory | ordered | Q1-Q8, each measured |
| C5 the handback | ordered | |

## Next Steps
1. Book R1's verdict into `.agent/live_review.md` and plan T001 against the
   inventory — the schema, and the enforcement point the inventory names.
2. T001: schema v2, the enforcement gate, legacy rendering, the CI canary and
   its unit tests.
3. T002 the per-producer upgrades, then T003 card enrichment and chip
   deep links.

## Risks
- The feature file's Design names one enqueue seam. If the inventory measures
  none, the spec is wrong and the reviewer rules a DECISION under §4 item 7
  rather than widening scope silently.
- `.agent/live_review.md` is append-only below `## Findings`. R1 rewrites the
  header region and nothing else, and that region is proved byte-identical.
<<<END PLANF032R1

<<<SLICE CTXF032R1
# Context — F032 Approval with the evidence triple

## Active Branch
feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge commit
of pull request #216 which closed the amend0827 process-diet order.

## Scope
Feature F032 per `docs/roadmap/features/T5_F032.md`: the evidence triple —
`evidence_refs[]`, `expected_outcome`, `downside` — becomes a required part of
every decision a human is asked to answer, enforced at the point the inventory
measures such a point to be, rendered by the inbox card, and pinned by a canary
producer that must fail CI when a field is missing.

## Do not touch
The feature file's own list: the decision ANSWERING flow, queue STORAGE and the
provenance RESOLVER. R1 additionally writes no file under `packages/`, `apps/`
or `tests/` at all.

## Assumptions
- Rule A5 chose F032: `docs/roadmap/STATUS.md` carried no `[~]` and no `[!]`
  line and F032 was the first `[ ]`, measured at `a399a330`.
- `.agent/candidates.md` is EMPTY at the claim, so no block condition stands.
- The feature file's Design is a SUGGESTED shape, not a settled spec; the
  inventory measures the real one before T001 is planned.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced. They are not this feature's, and
deleting them with the rest of a rewrite is what cost an earlier round a red
CI run.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The full contract those
  readers hold over the three state files, so a rewrite is checked against it
  directly rather than rediscovered from a red: this file carries
  `## Active Branch`, a `feature/` branch name, a roadmap feature id matching
  `\bF\d{3}\b` and the word `Steps`; `.agent/plan.md` carries `## Goal`,
  `## Next Steps` and a feature id; `.agent/live_review.md` carries `Steps`.

## Steps
The round map for this feature lives in the `## Steps` section of
`.agent/live_review.md`, and the current round's items in the `## Current Step`
table of `.agent/plan.md`. This file deliberately restates neither — a second
copy of the map is what fell out of step and cost F022 a finding.
<<<END CTXF032R1

<<<SLICE LFROM
# Live Review — F031 Decision inbox

> Round-by-round review record for the F031 branch, reset at the feature claim.
> The F022 record closed with pull request #213, merged into `main` at this
> feature's Open PR Gate as `6325ac2f` after CI run 32639191630 concluded
> SUCCESS on `45e4691f`. That branch's LAST round, R19, has no gate entry in its
> own record by construction, because a round's verdict is written by the NEXT
> reviewed round (DECISION F085 D9) and R19 was the last round F022 had; its
> entry is therefore the first `Gate:` paragraph below. Finding ids continue the
> monotonic R-XXXX series across the reset, and every finding record F022
> carried is carried forward unchanged.

## Steps

R1 claim F031 in the roadmap ledger, create the branch, reset this record
carrying every finding record forward, gate F022 R19 and register the one
candidate F022 carried as R-0677, emptying the carrier in the same round → R2
record the R1 verdict on disk and rule how the open set is to be derived, the
gap R1's plan records → R3 the decision-inbox inventory: the file-based queue
store and its CLI, every producer that writes a decision, the DAG module's
blocked-subtree entry point, and the decision event kinds the stream carries
today on the Python and the TypeScript side, each MEASURED in the source, plus
whether F050 and F051 are built → the T-slices follow the feature file's Task
slicing and are planned once that inventory is on disk.
<<<END LFROM

<<<SLICE LTO
# Live Review — F032 Approval with the evidence triple

> Round-by-round review record for the F032 branch, reset at the feature claim.
> The F031 record closed with pull request #215, merged into `main` as
> `f4eae1d4`, and the operator collection order amend0827 which followed it
> merged as pull request #216 at `a399a330`, this branch's point. F031's LAST
> round has no gate entry in its own record by construction, because a round's
> verdict is written by the NEXT reviewed round (DECISION F085 D9) and it was
> the last round F031 had; the amend0827 order was a single-session micro-round
> whose verdict lives in its own handback and in pull request #216, and it
> appended its notes to this file without a gate entry for the same reason.
> Finding ids continue the monotonic R-XXXX series across the reset, and every
> finding record F031 carried is carried forward unchanged: measured at
> `a399a330`, 270 findings, 21 resolved, 249 open, the maximum id `R-0709`.

## Steps

R1 claim F032 in the roadmap ledger, cut the branch, reset this record carrying
every finding record forward, and put the F032 source inventory on disk — the
eight producing branches of `decision_queue.list_decisions`, the record each
derives from, whether any enqueue seam is common to them, the evidence-ref
vocabulary and its resolver, the options a decision offers, the card's
rendering surface, the migration precedent and the guards a schema change must
satisfy → R2 book the R1 verdict and plan T001 against that inventory → T001
the schema, the enforcement point, legacy rendering and the CI canary → T002
the per-producer upgrades → T003 card enrichment and the chip deep links.
<<<END LTO

<<<SLICE SFROM
- [ ] F032 — Approval with the evidence triple
<<<END SFROM

<<<SLICE STO
- [~] F032 — Approval with the evidence triple
<<<END STO
