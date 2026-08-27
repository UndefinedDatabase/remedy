STEP R12 / F032 — T002g: THE LAST PRODUCER, AND THE GATE GOES FULLY LIVE
Goal:        UPGRADE `task_decision`, THE EIGHTH AND LAST PRODUCING TYPE, AND
             CLOSE T002. This branch is the only one whose options are not
             known when the code is written: they come from the escalation
             record and are arbitrary strings, so its outcomes are BUILT per
             option rather than written out, and the same branch must satisfy
             rule (g) when the record offers choices and rule (h) when it
             offers none. It is also the branch that drops the record's
             `impact` field, which amendment A3 of
             `docs/roadmap/features/T5_F032.md` carried forward to T002 as the
             nearest thing to an `expected_outcome` already on disk — this
             round finally uses it. When `task_decision` joins the set all
             EIGHT producing types are enforced and the emit gate is fully
             live, which is the state `TRIPLE_REQUIRED_TYPES` documents as its
             own end condition. SESSION 3 CONTINUES; YOU CREATE NO PULL
             REQUEST AND MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the R11 verdict · C3 the task-decision triple, the gate
             entry and the constant's own comment · C4 the tests · C5 the
             handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r12.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `packages/orchestration/decision_queue.py`,
             `packages/orchestration/decision_evidence.py`,
             `tests/orchestration/test_decision_evidence.py`,
             `.agent/handoff.md`. Nothing under `apps/` and nothing under
             `docs/` is touched, so no docs-round gate is owed.

Constraints.
 1. YOU DO NOT EDIT ANY SLICE. A `<<<SLICE NAME>>>` line and its `<<<END NAME>>>`
    line delimit text you apply byte for byte. If a slice looks wrong, apply it
    anyway and say so in the handback's deviations; the reviewer repairs it in
    the next round. The marker lines themselves are NEVER written into any file.
 2. SLICE CONVENTION. A slice's content is every line strictly between its two
    marker lines. When the slice replaces a whole file, the file's bytes are
    those lines joined with `\n` plus ONE trailing `\n` and nothing more. When
    the slice is appended, the file's new bytes are its old bytes plus ONE `\n`
    plus that same joined text plus ONE trailing `\n`, applied only if the old
    bytes already end in a newline — `.agent/live_review.md` does; G5 proves the
    arithmetic.
 3. THE AUTHORED UNITS OF THIS BLOCK are the whole block itself and the slices
    PLANF032R12 and LEDGER12. This paragraph gives no count of them; G3 reports
    the number the extraction measured.
 4. C0a IS A COPY, NOT A RETYPE. `.remedy-wt/f032-r12.md` exists on disk and
    holds this block. Copy that file to `.agent/authored/f032-r12.md` with a
    byte-preserving read-and-write and commit it. C0b then writes the SAME
    bytes to `.agent/last_block.md`. Do not reformat, rewrap or strip anything.
 5. PRODUCTION CODE IS DESCRIBED, NOT SLICED. Items S1 through S7 are a spec.
    You write the Python yourself, in the style of the branches already in
    `decision_queue.py`, and you carry the WHY into a comment above each change
    the way F032 R5, R7, R8, R9, R10 and R11 did in that same file.
 6. COMMENT DENSITY MATCHES THE FILE. Match the surrounding branches; do not
    exceed them.
 7. ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, in that order and with no
    commit between them. C2 is the only commit touching `.agent/live_review.md`.
    C3 CARRIES THE TRIPLE AND THE GATE ENTRY TOGETHER, per DECISION F032 D5.
 8. THE RESOLVED ARM IS ALREADY RULED ON. DECISION F032 D7, on disk at
    `09f0ebaf`, records that the emit gate selects by TYPE ALONE and never reads
    `status`, so both arms of this branch are enforced together and the resolved
    arm's outcome speaks of the answer already recorded. Do not re-derive it and
    do not add a `status` branch to `enforce_decision_evidence`.
 9. RE-READ `.agent/STOP` FROM DISK TWICE: once before C0a and once before C5.
    If it exists at either reading, stop, write the handback, and end.
10. MUTATION RUNS GO IN A DISPOSABLE WORKTREE. `git worktree add --detach
    .remedy-wt/f032-r12-mut <C4 sha>`, run the red-proofs there, restore the
    file byte for byte after each one, remove the worktree and prune. The
    primary checkout satisfies `git status --porcelain` == empty at every
    commit.
11. PURGE `__pycache__` AND PASS `-B` BEFORE EVERY PYTEST RUN IN THE WORKTREE.
12. THE ROUND BASE IS `da6b64fc`, the commit that handed back R11. Every numeral
    this block states about the base was measured there.
13. RUN THE SUITES SERIALLY. Never two pytest processes at once.

Spec — T002g, the task decision.
 S1. READ FIRST, AND THE MEASUREMENTS THE DESIGN RESTS ON. Branch 8 of
     `list_decisions` iterates `escalation_records(job)` and builds ONE
     `HumanDecision` per record, choosing between an OPEN and a RESOLVED shape
     inside a single `decisions.append` call. It reads `decision_id`, `task_id`,
     `question`, `options`, `answer`, `answer_source`, `safe_default` and
     `cross_references`, and its `payload` ALWAYS carries an `options` key whose
     value is the record's own list — EMPTY when the record offered no choices.
     So the gate reads this branch through rule (g) when that list is non-empty
     and through rule (h) when it is not, and BOTH shapes must come out of the
     same code. `packages/orchestration/escalation.py::enqueue_task_decision` is
     the only writer of these records and always sets `decision_id`,
     `safe_default`, `impact` and `cross_references`, defaulting the last three
     to the empty string, the empty string and a list. The reviewer checked at
     `da6b64fc` that every suite which drives branch 8 through the QUEUE —
     `tests/orchestration/test_decision_inbox.py`,
     `tests/orchestration/test_run_report.py`,
     `tests/orchestration/test_watchdog.py`,
     `tests/orchestration/test_mission_e2e.py`,
     `tests/cli/test_open_decisions_view.py` and
     `tests/ui_server/test_command_channel.py` — builds its records through that
     function rather than by hand, so `decision_id` is guaranteed non-empty on
     every record this branch can reach.
 S2. THE REFS COME FROM THE RECORD, AND ONE IS UNGUARDED. Emit a ref of kind
     `decision` targeting `decision_id`, ALWAYS, labelled as the escalation
     record this decision was raised from — S1 is why it needs no guard, and it
     is the value the card's own `id` is already built from. Then emit ONE ref
     of kind `decision` per entry of `cross_references`, labelled as the same
     question raised again and cross-referenced by the queue, skipping any entry
     that is empty. Then, for a RESOLVED record only, emit a ref of kind
     `decision` targeting `answer` labelled as the answer that was recorded, and
     a ref of kind `decision` targeting `answer_source` labelled as where that
     answer came from — each ONLY when its value is non-empty, because an OPEN
     record carries both as the empty string and rule (c) of
     `evidence_triple_problems` refuses a ref pointing at nothing. Never emit a
     ref whose target is the empty string.
 S3. THE OUTCOMES ARE BUILT, NOT WRITTEN OUT, and this is the only producer in
     the feature where that is true. When the record's options list is NON-EMPTY,
     emit EXACTLY ONE `DecisionOptionOutcome` per option, keyed with that
     option's own string — rule (g) compares the keys against
     `payload["options"]` in BOTH directions, so the list the outcomes are built
     from must be the SAME list the payload carries, not a re-read of the
     record. When it is EMPTY, emit exactly one outcome keyed `UNKEYED_OPTION`,
     per rule (h).
 S4. WHAT EACH BUILT OUTCOME SAYS. The record knows two things that distinguish
     one option from another, and the text uses both. FIRST, whether the option
     IS the record's `safe_default`: the default's expected outcome says that
     answering it is the course the task itself proposed as safe, so the waiting
     branch resumes on the path the run was already prepared for, and its
     downside says that a default accepted without reading the question is how
     an assumption nobody checked becomes a finished result. A NON-default
     option's expected outcome says the waiting branch resumes on that course
     instead of the one the task proposed, and its downside says the run departs
     from what the task prepared for, so work already done for that path may be
     spent again. When `safe_default` is EMPTY no option is the default, and
     every option gets the neutral pair: the waiting branch resumes on the
     chosen course, at the cost that the tasks blocked behind this question stay
     blocked until it is answered and a course chosen without reading the
     question is paid for downstream. SECOND, the record's own `impact`: when it
     is non-empty, append it to EVERY option's expected outcome as the
     consequence the task itself stated, which is the use amendment A3 carried
     forward to T002. The UNKEYED case of S3 says that answering in free text
     resumes the waiting branch, at the cost that a question left unanswered
     blocks everything behind it. THE EXACT WORDING IS YOURS. No half of any
     outcome may be, or consist wholly of, a member of `BOILERPLATE_PHRASES` —
     and note that an option word may itself be a member, so build the sentence
     around the option rather than emitting the option alone.
 S5. `task_decision` JOINS `TRIPLE_REQUIRED_TYPES` IN C3, the same commit as its
     triple. THAT MAKES ALL EIGHT PRODUCING TYPES ENFORCED, so in the SAME
     commit update the constant's own comment in
     `packages/orchestration/decision_evidence.py`, which at `da6b64fc` reads
     that the gate is fully live "when all eight types are in the set" and that
     the constant "has become a formality, which is when it can be deleted".
     State that this is now the case, keep the entry rule that got it there, and
     say why the constant is NOT deleted in this round: the two types in
     `DECISION_TYPES` with no producer at all — `worker_approval` and
     `revert_missing`, per DECISION F031 D3 — are the reason a set is still
     needed rather than an unconditional check, and two tests in
     `tests/orchestration/test_decision_evidence.py` depend on
     `revert_missing` staying outside it.
 S6. DO NOT CHANGE `payload`, `next_actions`, `safe_summary`, the id, the status
     or the severity of this branch. The round adds `evidence` and nothing else
     to the card.
 S7. THE NEW TESTS GO IN `tests/orchestration/test_decision_evidence.py` and
     nowhere else, driving the REAL branch through `list_decisions` with records
     built by `enqueue_task_decision`, as S1 describes the rest of the suite
     doing. Cover: an open record with two options and a `safe_default` naming
     one of them, asserting the outcome keys are exactly those two options and
     that the default's text differs from the other's; an open record with two
     options and NO `safe_default`, asserting both get the neutral pair; an open
     record with NO options, asserting exactly one outcome keyed
     `UNKEYED_OPTION`; a record carrying a non-empty `impact`, asserting that
     text appears in EVERY option's expected outcome; a record whose question
     duplicates an earlier open one, so `cross_references` is non-empty,
     asserting the extra refs; and a RESOLVED record, asserting the `answer` and
     `answer_source` refs appear and that an OPEN record has neither. For every
     case assert that no ref carries an empty target, that
     `evidence_triple_problems` returns the empty list WHEN GIVEN THAT CARD'S
     OWN OPTIONS — pass `decision.payload["options"]`, or the check silently
     tests the wrong rule — and that the exported card's `evidence_status` is
     `present`. Add a test that a `task_decision` card with its triple dropped
     raises `DecisionEvidenceError`, and update the exact-membership assertion
     in `test_the_shipped_required_type_set_holds_exactly_the_upgraded_producers`
     to name every producing type. The two guards R11 repointed to
     `revert_missing` are CORRECT AND STAY — do not move them again.

Done when. Report each gate as its own line in the handback, with the real
command, its exit code and the real output you saw. G1 through G8 are ordered at
commits STRICTLY EARLIER than C5, which writes the handback; C5's own readings
are not values this round writes anywhere, and G1 therefore stops at C4.
 G1. HYGIENE, BASE AND THE SENTINEL. Report `git rev-parse HEAD` before C0a and
     confirm it is the round base named in constraint 12; report the branch is
     `feature/f032-evidence-triple`; report the `git status --porcelain` line
     count after EACH of C0a through C4, each 0; report whether `.agent/STOP`
     exists at the two readings constraint 9 orders.
 G2. TRANSPORT. Report the sha256, byte count and line count of
     `.remedy-wt/f032-r12.md`, of the committed `.agent/authored/f032-r12.md`
     blob and of the committed `.agent/last_block.md` blob, and report whether
     all three are EQUAL. Report the git blob hash of the C0a and C0b paths and
     whether they are the SAME blob. State plainly that this proves the
     reviewer's scratch original, the saved copy and the mirror agree, and says
     NOTHING about the bytes of any prompt.
 G3. EXTRACTION AND CAPS. From the COMMITTED C0a blob, extract every region
     between a `^<<<SLICE ` line and its `^<<<END ` line. Report the NAME and
     the content-line count of each region you find, the number of regions, the
     CONTENT total, the block's TOTAL line count, and PROSE as TOTAL minus
     CONTENT. Report whether PROSE is under 400 and TOTAL under 490. Report the
     numbers YOU measured; this block states none of them.
 G4. THE PLAN. Report whether `.agent/plan.md` at C1 is byte-equal to slice
     PLANF032R12 under the convention of constraint 2, and report the same
     comparison with the trailing newline removed as a NEGATIVE CONTROL, which
     must be FALSE. Report `wc -l` and that it is under 50, and the counts of
     `^## Goal$` and `^## Next Steps$`, each 1.
 G5. THE LEDGER APPEND. Read the pre-commit blob with `git show
     da6b64fc:.agent/live_review.md`, never by writing over the tracked file.
     Prove `.agent/live_review.md` at C2 equals that blob plus ONE newline plus
     the LEDGER12 slice, byte for byte; report the arithmetic as three numbers
     summing to the result and report that the pre-commit blob is a byte PREFIX.
     Then run a SECOND, INDEPENDENT structural reader: split the whole file on
     blank lines, let N be the number of paragraphs in the LEDGER12 slice as
     YOUR script counts them, and compare the LAST N units of the file against
     those N paragraphs IN ORDER. As a NEGATIVE CONTROL flip ONE byte inside the
     FIRST appended paragraph, in memory only, and report that BOTH readers
     reject it. The reviewer measured the base at `da6b64fc` as 1081523 bytes
     over 428 blank-line units. Then report, before and after C2, the counts of
     `^Gate: F\d+ R\d+ — `, `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-` and
     `^Gate: R\d+ — `, the size of the open set — every registered id minus
     every resolved id — the maximum id, the gate keys ADDED and the ids ADDED
     to the resolved set. The reviewer measured 63, 274, 24, 1 and 19 at the
     base, with the open set 250 and the maximum `R-0713`.
 G6. THE CODE, LINTED AND READ BACK. Run `python3 -m ruff check` over
     `packages/orchestration/decision_queue.py` and
     `packages/orchestration/decision_evidence.py` and report the exit code and
     the verbatim output. Then, at C3, call `list_decisions` yourself and report
     the refs as `(kind, target, label)` tuples and the outcomes as
     `(option, expected_outcome, downside)` tuples for each of these cases: an
     open record with two options and a `safe_default` naming one; an open
     record with two options and no `safe_default`; an open record with no
     options at all; a record with a non-empty `impact`; a record whose
     `cross_references` is non-empty; and a RESOLVED record. For each, report
     the card's own `payload["options"]`, what `evidence_triple_problems`
     returns when passed those options, and `export_decision_json`'s
     `evidence_status` and `status`. Report the sorted members of
     `TRIPLE_REQUIRED_TYPES` and state whether every type in
     `PRODUCING_DECISION_TYPES` of `tests/orchestration/test_decision_inbox.py`
     is now in it.
 G7. TESTS GREEN, THEN RED UNDER MUTATION, AND THE WIDER SUITES UNMOVED. Run
     `python3 -m pytest tests/orchestration/test_decision_evidence.py -q` in the
     PRIMARY checkout at C4 and report the exit code and the count line. Then in
     the disposable worktree of constraint 10, at C4, report the exit code, the
     count line and the number of `^FAILED` lines for: a CONTROL run before any
     mutation; mutation (a), the built outcome keyed with a constant string
     instead of with the option it was built for, which is a rule (g) violation
     in both directions — the payload offers an option no outcome answers, and
     an outcome names an option the payload does not offer; mutation (b),
     the `answer` ref of S2 emitted unconditionally; mutation (c),
     `task_decision` removed from `TRIPLE_REQUIRED_TYPES`; mutation (d), the
     safe-default branch of S4 removed so every option gets the neutral pair;
     and a CONTROL run after all four restorations, with the worktree's `git
     status --porcelain` empty. Name the FILE each mutation is applied to,
     count its exact byte string IN THAT FILE before applying it and report that
     the count is 1, and restore the file byte for byte before the next. Then
     run `tests/orchestration/test_decision_evidence.py`,
     `tests/orchestration/test_decision_inbox.py`,
     `tests/orchestration/test_run_report.py`,
     `tests/orchestration/test_watchdog.py` and
     `tests/cli/test_open_decisions_view.py` as ONE pytest process in the
     primary checkout and report the exit code, the count line and the number of
     `^FAILED` lines.
 G8. STRUCTURE, CANARY AND THE PR GATE. Run
     `python3 -m pytest tests/cli/test_golden_path.py -q` and report the exit
     code and the count line. Report the path set of `git diff --name-only
     da6b64fc..<C4 sha>` against the paths the Change set lists other than
     `.agent/handoff.md`, as the two residues, both of which must be EMPTY.
     Report that `git diff --stat da6b64fc..<C4 sha> -- apps/` and the same for
     `-- docs/` are both EMPTY. Report the insertion count of each of C0a
     through C4, that each is single-parent, and that each is under 500. Those
     counts and the `+/-` column of the handback's `## Commits` section are one
     reading written twice: derive both from `git diff --numstat`, compare them
     cell by cell, and report that they agree. Report the counts of
     `^<<<SLICE ` and `^<<<END ` in `.agent/plan.md`, `.agent/live_review.md`,
     `packages/orchestration/decision_queue.py`,
     `packages/orchestration/decision_evidence.py` and
     `tests/orchestration/test_decision_evidence.py`, each 0, against a CONTROL
     count over the committed C0a blob, which must be non-zero. Report `git
     ls-files .remedy-wt` as 0 lines, `git worktree list` as 1 line and `git
     branch --list "tmp/*"` as 0 lines. Report the output of `gh pr list --state
     open --json number,headRefName,baseRefName,isDraft`; merge nothing and
     create nothing.

Handback: rewrite `.agent/handoff.md` as C5, per
docs/agents/handback_template.md. It carries the mandated sections — the state
block, the commits table with each commit's real `+/-` read from `git diff
--numstat` for C0a through C4 — C5 cannot table its own numstat and says so in
its row — the item-status table covering every C and every S exactly once, the
deviations, the verification lines of G1 through G8 and the next steps. It
states that the feature is F032, that R12 is the round, and that this is SESSION
3, which began at R10. Session 1 was R1 through R5 and session 2 was R6 through
R9. Twelve rounds across three sessions is inside the soft limit of 25 rounds or
7 sessions, so do NOT emit a limit report. The handback has NO LENGTH CAP, so do
not declare, measure or apologise for its length. It states plainly that T002 IS
COMPLETE and that the emit gate is fully live over all eight producing types.
Its `## Next` section names Phase 1 rule 1 of
docs/agents/self_drive_protocol.md — the `.agent/STOP` re-read from disk —
before anything else, then the Open PR Gate, then T003: card enrichment and the
chip deep links, which is the first F032 work to touch `apps/` and therefore the
first bound by the canonical design reference in `docs/ui/design_reference/`.
Then push the branch.

<<<SLICE PLANF032R12>>>
# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D7.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R12 upgrades `task_decision`, the eighth and last producing type, and ends
T002. It is the only branch whose options are not known when the code is
written — they come from the escalation record — so its outcomes are BUILT per
option and the same code must satisfy rule (g) when the record offers choices
and rule (h) when it offers none. It is also the branch that drops the record's
`impact`, which amendment A3 carried forward to T002, and this round uses it.
When the type joins the set the emit gate is fully live.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R11 verdict | ordered | the record is touched first |
| C3 the triple, the gate entry and the comment | ordered | S2 to S6 |
| C4 the tests | ordered | S7 |
| C5 the handback | ordered | |

## Next Steps
1. T003: card enrichment and the chip deep links. It is the first F032 work to
   touch `apps/`, so it is the first round bound by the canonical design
   reference in `docs/ui/design_reference/`, and its rounds carry the
   assumption_log obligation that comes with it.
2. The integration gate — the full suite, run per docs/agents/integration_gate.md.
3. The closure sequence: evidence job, a fresh review zip, the STATUS line and
   the pull request, per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Built outcomes are keyed with values the code never chose, so an option
  string that is itself a member of `BOILERPLATE_PHRASES` would be a legal key
  with an illegal-looking outcome; the text is built around the option rather
  than from it, which is what keeps rule (f) clear of the key.
- All eight producing types are enforced from this round on, so any later
  change that regresses a triple raises instead of rendering. That is the
  intent, and it is what the constant was created to reach.
<<<END PLANF032R12>>>

<<<SLICE LEDGER12>>>
Gate: F032 R11 — the F032 T002f FLIGHT-PLAN entry, both arms. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all eight itself at `da6b64fc`. TRANSPORT IS PROVED FROM A VALUE THE REVIEWER HELD BEFORE DELEGATING: sha256 `fefaa48f3641824d64c93247a7517f36042f7ee6bae6fa801ccf4bc15d2f7761` over 32994 bytes and 415 lines was computed on the scratch original at authoring time, and the committed `.agent/authored/f032-r11.md` blob at `cd88a6c6` and the committed `.agent/last_block.md` blob at `7b4c3c65` both carry exactly it, as the SAME git blob `9f8f4292d0fd`. That chain runs from an independently held digest through the saved copy to its mirror; under docs/agents/self_drive_protocol.md there is no paste relay, so it says NOTHING about the bytes of any prompt and this entry claims no more. THIS IS THE FIRST TWO-ARMED PRODUCER, AND BOTH ARMS LANDED IN ONE COMMIT, `8b115a64`, together with the type's entry in `TRIPLE_REQUIRED_TYPES` — which is not ceremony but the only order that never lands a commit where the resolved arm raises, because `enforce_decision_evidence` selects by type and never reads `status`. THE PENDING ARM IS THE FEATURE'S SECOND KEYED PRODUCER: `payload["options"]` is set on every pass, so rule (g) rather than rule (h) applies, and it compares the outcome keys against that list in BOTH directions. The reviewer proved that bidirectionality with a mutation the block did not order — re-keying the `reject` outcome to `decline` — and it went red at `12 failed, 96 passed`, so the round's tests pin the rule and not merely the shape. THE ALWAYS-REF IS LOAD-BEARING AND WAS ALSO PROVED BY AN UNORDERED MUTATION: removing the unguarded `fp:approval` ref went red at `9 failed, 99 passed`, which is what keeps rule (a) satisfied for the minimal job `tests/orchestration/test_mission_state.py` builds, `Job(name="t", flight_plan={"_approval": "pending"})`, carrying no clarifications and no intake at all. THE FOUR ORDERED MUTATIONS ALL KILLED TESTS, each exact byte string counted 1 before it was applied and the file restored after, `__pycache__` purged and `-B` passed before every run, in the reviewer's own disposable worktree at `0d027074`: the non-empty-`id` guard removed gave exit 1 at `4 failed, 104 passed`; the `mode` ref made unconditional gave exit 1 at `4 failed, 104 passed`; `flight_plan_approval` removed from the gate set gave exit 1 at `3 failed, 105 passed`; the `reject` outcome deleted gave exit 1 at `12 failed, 96 passed`; and the controls before and after all five restorations were a real exit 0 at `108 passed`, with the worktree's `git status --porcelain` empty. DECISION F032 D7 LANDED AT `09f0ebaf` AND IS THE ROUND'S DURABLE OUTPUT: the gate keeps its type-only selection, a resolved card carries a real triple whose refs are the audit trail the answer left, and its single unkeyed outcome speaks of the answer already recorded. Its REJECTED option — guarding the gate with `status == "open"` — is recorded with the reversal recipe, so a later reader can undo it in one edit. THE GUARD CHURN IS OVER. The two tests needing an unenforced example named `memory_review` until R10 and `flight_plan_approval` until this round; they now name `revert_missing`, which DECISION F031 D3 records as having NO PRODUCER AT ALL, so it can never join a set whose entry rule is "in the same commit that gives its producer a real triple". THE RECORD MOVED EXACTLY AS ORDERED, and both appends were proved twice over: `.agent/live_review.md` 1076472 + 1 + 5050 = 1081523 and `.agent/decisions.md` 642072 + 1 + 3617 = 645690, each with the base a byte PREFIX, each with a structural reader comparing the last N units in order, and each with a byte flipped inside the FIRST appended paragraph rejected by both readers. `^Gate: F\d+ R\d+ — ` went 62 to 63 adding exactly `F032 R10`; `^- R-\d+ — ` stayed 274, `^Done: R-\d+ — ` stayed 24, and the open set stayed 250 with the maximum `R-0713`, because this round registered no finding and resolved none. `^## DECISION F032 D\d+ ` went 6 to 7. NOTHING ELSE MOVED: `ruff check` over both modules exit 0 with the verbatim output `All checks passed!`, the four decision suites as one process exit 0 at `263 passed`, the golden-path canary exit 0 at `42 passed`, both path residues EMPTY over the nine-path change set, `apps/` and `docs/` EMPTY, insertions 415, 301, 23, 8, 54, 115, 354 and 215 across the eight commits, each single-parent and under 500, markers 0 and 0 in all seven written files against a CONTROL of 4 and 4 over the C0a blob, `.remedy-wt` 0 tracked, `git worktree list` 1 line, the remote tip equal to the local tip and the Open PR Gate `[]`. THE WORKER DECLARED ONE ADDITION BEYOND THE SPEC AND WAS RIGHT TO MAKE IT: `tests/orchestration/test_decision_evidence.py` now imports `replace` from `dataclasses`, because S8 orders a test over a RESOLVED card with its triple dropped while the file's local helper hardcodes `status="open"` on a frozen dataclass. That is the smallest correct way to reach the ordered case. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER12>>>
