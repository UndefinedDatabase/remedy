STEP R4 / F032 — T001b THE EMIT GATE, LEGACY RENDERING AND THE CANARY
Goal:        WIRE THE SCHEMA IN WITHOUT BREAKING A SINGLE EXISTING PRODUCER.
             `HumanDecision` gains ONE optional field, `export_decision_json`
             gains THREE keys, and `list_decisions` gains the enforcement call
             DECISION F032 D1 puts at the emit point. Enforcement is opt-in PER
             TYPE and the opt-in set starts EMPTY, so every one of the eight
             existing producers keeps working and renders the honest legacy
             placeholder, while the gate is live and provably catches an
             omission from the first commit — that is what the canary pins.
             T002 adds a type to the set as it upgrades that producer. This
             round also carries `R-0710`'s fix, because it is the first round
             to edit `packages/orchestration/decision_queue.py` and that
             finding's clause binds it. YOU CREATE NO PULL REQUEST AND MERGE
             NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 DECISION F032 D5 · C3 the feature file's amendment A5 ·
             C4 the schema wiring and `R-0710`'s fix in `decision_queue.py` ·
             C5 the tests, including the canary · C6 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r4.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/decisions.md`,
             `docs/roadmap/features/T5_F032.md`,
             `packages/orchestration/decision_queue.py`,
             `packages/orchestration/decision_evidence.py`,
             `tests/orchestration/test_decision_evidence.py`,
             `.agent/handoff.md`. This list bounds what you WRITE INTO THE
             REPOSITORY. It does NOT bound what you DO: G6 orders a disposable
             worktree and G8 orders a push. NOTHING under `apps/` is written.
             NO EXISTING TEST FILE IS EDITED — if a guard in one of them goes
             red, that is a real finding and you hand back rather than edit it.
             `.agent/live_review.md` is NOT written: `R-0710` is FIXED here but
             only the reviewer may write its `Done:` text, so you mark the fix
             per constraint 7 and nowhere else.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f032-r4.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f032-r4.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own; G2 has you measure
    four points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice contradicts something you measure,
    apply it anyway and DECLARE the contradiction in the handback under
    Deviations. Declaring beats fixing every time.
 3. THE PRODUCTION CODE IS SPECIFIED, NOT SLICED. Items S1 through S10 describe
    what the code must DO and what names it must EXPORT. You write it, in the
    house style of the two modules you are editing.
 4. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6.
 5. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R3. That is
    ordered: the plan becomes current at C1.
 6. THE TWO APPENDS ARE APPENDS. `.agent/decisions.md` and
    `docs/roadmap/features/T5_F032.md` each end this round as their own
    pre-commit blob, byte for byte, plus ONE newline, plus the slice. Nothing
    already in either is rewritten, deleted or touched.
 7. YOU DO NOT WRITE THE FINDING RECORD. `R-0710` is fixed by S9 below, but
    only the reviewer's authored text may set a finding Resolved. Record the
    fix in your HANDBACK under Deviations, in one line naming what changed and
    which commit, and write nothing into `.agent/live_review.md`. You never
    mint a finding id and never author a `Done:` line.
 8. THE OPT-IN SET STARTS EMPTY AND THAT IS THE WHOLE SAFETY ARGUMENT. If you
    find yourself needing to add a type to it to make an existing test pass,
    STOP — something else is wrong and the reviewer wants to know.
 9. RE-READ `.agent/STOP` FROM DISK before C0a and again before C6. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
10. THE ONLY DESTRUCTIVE WORK IS G6's, AND IT IS ISOLATED. Mutation red-proofs
    run ONLY inside a disposable `git worktree` created under `.remedy-wt/`,
    never in the primary checkout, which reads `git status --porcelain` 0 lines
    at every commit. Remove the worktree and prune before the handback.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `4316e7f5` was
    measured by the reviewer at that commit. It is a REFERENCE to report
    against, NOT a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
13. THERE ARE NO FROM/TO REPLACEMENT PAIRS. PLANF032R4 is a whole-file
    replacement of `.agent/plan.md`; DEC5 and FEATA5 are appends.
14. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 1
    of F032 and that R4 is the round. The handback has NO LENGTH CAP —
    amend0827 rule 3 withdrew every tier — so do not declare, measure or
    apologise for its length.

Spec — what the code must do.
 S1. IN `packages/orchestration/decision_evidence.py`, add
     `DECISION_EVIDENCE_STATUS_PRESENT` with value `present` and
     `DECISION_EVIDENCE_STATUS_LEGACY` with value
     `recorded_before_evidence_requirements` — the honest placeholder
     `docs/roadmap/features/T5_F032.md:28-31` asks for, in those words. A WHY
     comment records that this is a PER-CARD marker and NOT a bump of
     `DECISION_INBOX_VERSION`, per DECISION F032 D5, because that constant has
     no reader anywhere in `packages/` or `apps/` and a migration story built
     on a stamp nothing reads would be a story nothing tells.
 S2. IN THE SAME MODULE, add `TRIPLE_REQUIRED_TYPES`, a `frozenset[str]` that
     is EMPTY at this commit. Its WHY comment states that a decision type is
     added here by T002 only when that producer actually carries a real triple,
     that the empty set is why this round changes no existing producer's
     behaviour, and that when all eight are in it the gate is fully live.
 S3. IN THE SAME MODULE, add `DecisionEvidenceError`, a `ValueError` subclass,
     and `enforce_decision_evidence(decisions)` which iterates decisions,
     and for each whose `type` is in `TRIPLE_REQUIRED_TYPES` runs
     `evidence_triple_problems` against its `evidence` and its options, and
     RAISES `DecisionEvidenceError` naming the decision id, its type and every
     problem sentence, if there are any. A decision whose type is NOT in the
     set is left alone entirely. Read the options from the decision's
     `payload["options"]` when present and use an empty list otherwise, which
     is what inventory Q5 measured the six optionless branches to have.
 S4. WHY IT RAISES RATHER THAN DROPS, and this belongs in the function's
     docstring because it is the question a reader will bring: dropping a
     tripleless decision would LOSE A HUMAN QUESTION, which is exactly what
     `decision_inbox.py` says it will not do; and a producer that ships an
     enforced type with no triple is a programming error, which is what
     `docs/roadmap/features/T5_F032.md:25` means by "fails CI". Because
     `TRIPLE_REQUIRED_TYPES` only ever holds types whose producer has been
     upgraded, the raise can fire only on a regression.
 S5. IN `packages/orchestration/decision_queue.py`, `HumanDecision` gains ONE
     field, `evidence`, typed `DecisionEvidenceTriple | None` with default
     `None`, declared AFTER `payload`. Its comment mirrors `payload`'s own
     additive note: every existing producer omits it and gets `None`. IT MUST
     HAVE A DEFAULT — twelve fields are positionally required today and a
     thirteenth without one would break all nine construction sites at once.
 S6. `export_decision_json` gains THREE keys and drops none: `evidence_refs`
     and `outcomes` from `export_decision_evidence(d.evidence)` when
     `d.evidence` is not None, and `evidence_status`, which is
     `DECISION_EVIDENCE_STATUS_PRESENT` when it is not None and
     `DECISION_EVIDENCE_STATUS_LEGACY` when it is. When it is None the two list
     keys are present and EMPTY — never absent, because a key that appears only
     sometimes forces every reader to branch, and never a fabricated triple,
     which is the failure mode `docs/roadmap/features/T5_F032.md:29-31` names.
 S7. `list_decisions` calls `enforce_decision_evidence` on its result list
     immediately before it returns, and returns that same list. This is the
     emit point DECISION F032 D1 names.
 S8. THE IMPORT DIRECTION IS ONE-WAY. `decision_queue` imports from
     `decision_evidence`; `decision_evidence` imports nothing from
     `decision_queue`, exactly as its own module docstring promises. If you
     find yourself needing the reverse, stop and hand back.
 S9. `R-0710`'s FIX, in the same file, at what is currently
     `packages/orchestration/decision_queue.py:223`. The memory-review branch
     selects with `e.validity in ("stale", "needs_review")`, but `validity` is
     `Literal["active", "stale", "superseded", "contradicted"]` at
     `packages/memory/models.py:44` and `needs_review` is a value of the
     SEPARATE field `review_status` at `:45`, so half the predicate is dead.
     Select on `e.validity == "stale"` OR `e.review_status == "needs_review"`,
     with a one-line WHY comment naming both fields so the conflation cannot
     recur, and pin it in S10.
 S10. TESTS, ADDED TO `tests/orchestration/test_decision_evidence.py` — you
     edit NO existing test file. Add: a test that an empty
     `TRIPLE_REQUIRED_TYPES` leaves a tripleless decision untouched, which is
     the safety property this whole round rests on; THE CANARY, a test-only
     decision whose type IS enforced and which omits a field, asserting
     `DecisionEvidenceError` is raised and that its message names the decision
     id and the missing field's problem sentence — patch or parametrize the
     required set locally, never edit the module constant; a test that an
     enforced decision WITH a complete triple raises nothing; a test that
     `export_decision_json` on a tripleless decision gives
     `evidence_refs == []`, `outcomes == []` and the LEGACY status literal; a
     test that on a decision WITH a triple it gives the PRESENT literal and the
     real refs; and for `R-0710`, two tests over the memory branch — one entry
     whose `validity` is `stale` and one whose `review_status` is
     `needs_review`, each of which must produce a `memory_review` decision,
     because the second is the half that was dead and a single test over the
     first would not have caught it.

Done when:
 G1. HYGIENE AND THE SENTINEL. Report `git rev-parse HEAD` before C0a, which
     must be `4316e7f5d5dd272d1d1b4456879850a2ca0cea04`, and
     `git branch --show-current`, which must be `feature/f032-evidence-triple`.
     Report `git status --porcelain` as a LINE COUNT after each of C0a through
     C6, each 0. Report `.agent/STOP` read from disk before C0a and before C6,
     both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f032-r4.md`, as saved at C0a, as mirrored at C0b and
     as read off disk at C5 — all four must be EQUAL — and say whether C0a and
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
 G4. THE PROSE WRITES AND THE DOCS GATE. `.agent/plan.md` at C1 is BYTE-EQUAL
     to PLANF032R4 under the newline-INCLUDED convention, negative control
     against the slice MINUS its trailing newline reported FALSE, `^## Goal$`
     1, `^## Next Steps$` 1, a match for `\bF\d{3}\b`, `wc -l` STRICTLY UNDER
     50. `.agent/decisions.md` at C2 equals its pre-commit blob plus ONE
     newline plus DEC5, and `docs/roadmap/features/T5_F032.md` at C3 equals its
     pre-commit blob plus ONE newline plus FEATA5; the reviewer measured those
     base blobs at `4316e7f5` as 636058 bytes and 8225 bytes. For EACH report
     both byte counts, the sum, and the byte-PREFIX reading. Report
     `^## DECISION F032 D\d+ ` moving 4 to 5 with the ADDED key exactly
     `## DECISION F032 D5`, and `^## Design amendments$` still exactly 1. Then
     run `python3 -m pytest tests/docs/ tests/orchestration/test_roadmap_index.py
     -q` and report the REAL exit code and the summary VERBATIM; the reviewer
     measured `325 passed` at a REAL exit 0 at the round base.
 G5. THE CODE, LINTED AND READ BACK BY IMPORT. After C4 run `python3 -m ruff
     check packages/orchestration/decision_queue.py
     packages/orchestration/decision_evidence.py` from the repository root and
     report the REAL exit code and output VERBATIM; the reviewer measured
     `All checks passed!` at exit 0 over both files at the round base, under
     the repository's own `pyproject.toml` and never `--isolated`. Then, by
     IMPORTING rather than grepping, report: the exact values of
     `DECISION_EVIDENCE_STATUS_PRESENT` and `DECISION_EVIDENCE_STATUS_LEGACY`;
     the members of `TRIPLE_REQUIRED_TYPES`, which must be EMPTY; that
     `DecisionEvidenceError` is a subclass of `ValueError`; the field names of
     `HumanDecision` in declaration order with the LAST one being `evidence`
     and its default being `None`; and the sorted key list
     `export_decision_json` returns for a decision constructed with NO
     `evidence` argument, together with the value of its `evidence_status`.
     Report the line of `decision_queue.py` carrying the memory-review
     predicate after S9's fix, VERBATIM.
 G6. THE TESTS, GREEN, THEN RED UNDER MUTATION, THE MUTATIONS ISOLATED. After
     C5 run `python3 -m pytest tests/orchestration/test_decision_evidence.py -q`
     and report the REAL exit code and summary VERBATIM. Then create ONE
     disposable worktree at the C5 commit under `.remedy-wt/`, run the SAME
     scoped command there UNMUTATED FIRST as the CONTROL and report its real
     exit code and summary — a colour with no baseline is not evidence — then,
     one at a time and restoring between each, apply these three mutations and
     report for EACH the REAL exit code and summary line: (i) make
     `enforce_decision_evidence` never raise; (ii) make `export_decision_json`
     report the PRESENT status when `evidence` is None; (iii) revert S9's fix
     to `e.validity in ("stale", "needs_review")`. REPORT THE COLOUR AND THE
     COUNT YOU OBSERVE — this block names no expected number of failures and no
     test name. IF ANY MUTATION LEAVES THE RUN GREEN, say so plainly rather
     than reassuring: that is a real finding about the tests. Remove the
     worktree and prune.
 G7. THE GUARDS THAT THE SCHEMA CHANGE COULD MOVE, AND THIS IS THE GATE THIS
     ROUND EXISTS FOR. Run, as ONE pytest process, `python3 -m pytest
     tests/orchestration/test_decision_inbox.py
     tests/orchestration/test_approval_queue.py
     tests/orchestration/test_budget_stop_integration.py
     tests/orchestration/test_escalation.py
     tests/orchestration/test_bundled_clarification.py
     tests/cli/test_plan_approval.py tests/orchestration/test_handoff.py
     tests/cli/test_decision_answers.py tests/cli/test_open_decisions_view.py
     -q` and report the REAL exit code, the summary VERBATIM and the COUNT of
     `^FAILED` lines, proving your extractor sighted on a string you know
     contains one. The reviewer measured `324 passed` at a REAL exit 0 at the
     round base. THESE ARE THE EXACT FILES INVENTORY Q8 NAMES AS CARRYING
     EQUALITY GUARDS OVER THE DECISION SCHEMA, including the self-adjusting
     card-key guard at `tests/orchestration/test_decision_inbox.py:305` and the
     NON-self-adjusting document-key guard at `:311`. IF THIS RUN IS RED, DO
     NOT EDIT ANY TEST — report the failing node ids VERBATIM with the
     assertion text and hand back; a guard going red here is the finding this
     gate is for.
 G8. STRUCTURE, ARTIFACTS, THE STATE READERS, THE OPEN PR GATE AND THE PUSH.
     Run, as ONE pytest process, `python3 -m pytest tests/ui_server/
     tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
     -q` and report the REAL exit code, the summary VERBATIM and the `^FAILED`
     count; the reviewer measured `620 passed` at a REAL exit 0 at the round
     base. Compare the path set of `git diff --name-only 4316e7f5..C5` BOTH
     WAYS against this round's expected set — the Change line's list MINUS
     `.agent/handoff.md` — and report both residues EMPTY. Report `git diff
     --stat 4316e7f5..C5` restricted to `apps/` and confirm it EMPTY. Report
     each commit's insertions from `git diff --numstat` for C0a through C5,
     confirm each single-parent and under 500. Line-anchored `^<<<SLICE ` and
     `^<<<END ` are 0 and 0 in every file this round writes other than the two
     block copies, against a CONTROL over the C0a blob which is not 0. Report
     `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line, and `git
     branch --list "tmp/*"` 0 lines. Run `gh pr list --state open --json
     number,headRefName,baseRefName,isDraft` and report it VERBATIM; the
     reviewer read `[]` at the round base; MERGE NOTHING and CREATE NOTHING.
     After C6, run `git push origin feature/f032-evidence-triple`. ITS OUTCOME
     IS NOT A VALUE OF ANY FILE THIS ROUND WRITES, so `.agent/handoff.md`
     states the push only as an INTENT under `## External actions`, with NO
     exit code and NO remote tip; report the real exit code and the resulting
     remote tip in your completion report instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C6: the `## Session` section constraint 14 orders, feature and
             round, branch, the round base SHA `4316e7f5`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item AND every spec item S1
             through S10, ONE LINE PER GATE for G1 through G8 with its real
             exit code, the open-findings count after this round, and the next
             expected action. C6 cannot table its own numstat — write `self` in
             that cell, as `R-0149` requires. UNDER DEVIATIONS state the three
             mutation results in one line each, say plainly whether any left
             the suite green, and carry the ONE LINE constraint 7 orders about
             `R-0710`'s fix.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.

<<<SLICE PLANF032R4
# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D5.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R4 is T001b: the emit gate, the legacy placeholder and the canary.
`HumanDecision` gains one optional field, `export_decision_json` gains three
keys, and `list_decisions` calls the enforcement DECISION F032 D1 puts at the
emit point. Enforcement is opt-in per type and the set starts EMPTY, so no
existing producer changes behaviour while the gate is live and pinned from the
first commit. `R-0710` is fixed here because this is the first round to edit
`packages/orchestration/decision_queue.py`.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 DECISION F032 D5 | ordered | per-card marker, opt-in enforcement |
| C3 the feature file amendment A5 | ordered | where a builder reads it |
| C4 the wiring and the R-0710 fix | ordered | S1 through S9 |
| C5 the tests and the canary | ordered | S10, then the red-proofs |
| C6 the handback | ordered | |

## Next Steps
1. T002: upgrade the producers one at a time, adding each type to
   `TRIPLE_REQUIRED_TYPES` only once its triple is real, with the content
   goldens and the anti-boilerplate assertions.
2. T003: card enrichment, the chips and the evidence-panel deep links.
3. The integration gate, then closure.

## Risks
- The opt-in set is what keeps this round safe. If a producer is added to it
  before its triple is real, every job carrying that decision type raises.
- The reviewer, not the worker, writes `R-0710`'s resolution; until then it
  stays open in the record even though the code is fixed.
<<<END PLANF032R4

<<<SLICE DEC5
## DECISION F032 D5 (2026-08-27) — the migration marker is PER CARD, and enforcement is opt-in per type

THE QUESTION, in two halves that share one answer. FIRST, how does a reader
tell a decision recorded before F032 from one that simply has poor receipts?
The feature file asks for a "migration story for legacy entries" and an honest
"recorded before evidence requirements" placeholder rather than fake triples
(`docs/roadmap/features/T5_F032.md:28-31`). The obvious carrier is the document
version stamp, and inventory Q7 measured that it cannot work: `DECISION_INBOX_VERSION`
(`packages/orchestration/decision_inbox.py:37`) is WRITE-ONLY — the only code
that compares it is the test that compares it against the constant the same
process just wrote, and the browser does not model the key at all
(`apps/ui/src/api/decisionCard.ts:124-126` declares the document with no
`version` key). A migration story told through a stamp nothing reads is a story
nothing tells. SECOND, DECISION F032 D1 puts the gate at `list_decisions`, and
if the gate became fatal the moment it landed, all eight existing producers
would fail at once, because not one of them carries a triple. T001 would then
either break the suite or ship a gate that gates nothing until T002 finished.

CHOSEN, AND THE TWO HALVES ARE ONE MECHANISM. Every card carries its own
`evidence_status`, either `present` or the literal
`recorded_before_evidence_requirements`, emitted by `export_decision_json`
beside an always-present `evidence_refs` and `outcomes` that are EMPTY when
there is no triple — never absent, because a key that appears only sometimes
forces every reader to branch, and never fabricated, which is the failure the
feature file names. And `TRIPLE_REQUIRED_TYPES` starts EMPTY: a decision type
enters it in T002, in the same commit that gives its producer a real triple, so
the gate is live and pinned by the canary from the first commit while changing
no existing producer's behaviour. When all eight types are in the set, the gate
is fully live and the opt-in set has become a formality — which is the point at
which it can be deleted.

WHY THE GATE RAISES RATHER THAN DROPS. Dropping a tripleless decision would
lose a human question, which is exactly what `decision_inbox.py:141-143` says
this subsystem will not do. A producer that ships an ENFORCED type with no
triple is a programming error, and "a canary producer missing a field fails CI"
(`docs/roadmap/features/T5_F032.md:25`) is a statement about CI, not about
runtime refusal. Because the set only ever holds upgraded types, the raise can
fire only on a regression.

ALTERNATIVES CONSIDERED. Bumping `DECISION_INBOX_VERSION` to 2: rejected on
Q7's measurement — it would have to acquire its first reader before it could
carry anything, and a per-card marker is needed regardless, since a single job
can hold legacy and upgraded decisions side by side. Making the gate fatal
immediately and upgrading all eight producers in T001: rejected because it
merges T001 and T002 into one unreviewable round, against the feature file's
own slicing and against AGENTS.md's change-size limits. A warning list instead
of a raise: rejected because nothing reads warnings and it would make the
canary unassertable.

REVERSE by deleting this decision, dropping `TRIPLE_REQUIRED_TYPES` and
`evidence_status`, and making the triple unconditionally required at the emit
point.
<<<END DEC5

<<<SLICE FEATA5
**A5 — the legacy marker is per card, and enforcement is opt-in per type
(DECISION F032 D5).** The migration story cannot ride on the document version
stamp: `DECISION_INBOX_VERSION` is write-only, read by no code in `packages/` or
`apps/`, and the browser does not model the key at all. So every card carries its
own `evidence_status`, either `present` or the literal
`recorded_before_evidence_requirements`, beside an `evidence_refs` and an
`outcomes` that are always present and EMPTY when there is no triple — never
absent and never fabricated. And the emit gate A1 places at `list_decisions`
enforces only types listed in `TRIPLE_REQUIRED_TYPES`, which starts EMPTY: a type
joins it in T002, in the same commit that gives its producer a real triple. The
gate is therefore live and pinned by the canary from T001b onward while no
existing producer changes behaviour, and it becomes fully live when the eighth
type joins. It RAISES rather than drops, because dropping a tripleless decision
would lose a human question and a missing triple on an enforced type is a
programming error — which is what this file means by "fails CI".
<<<END FEATA5
