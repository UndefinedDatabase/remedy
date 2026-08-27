STEP R11 / F032 — T002f: THE FLIGHT PLAN, BOTH ARMS, AND THE RULING THEY NEED
Goal:        UPGRADE THE SEVENTH PRODUCING TYPE, WHICH IS THE FIRST ONE WITH
             TWO ARMS. The flight-plan branch builds an OPEN card when
             `_approval` is `pending`, carrying the two options the write door
             accepts, and a RESOLVED card when the plan was already approved,
             carrying no options and no next actions. The emit gate selects on
             TYPE ALONE and never reads `status`, so both arms are enforced the
             moment the type joins the set. This round gives the pending arm
             outcomes keyed to `approve` and `reject`, gives the resolved arm
             its own refs and one unkeyed outcome, and records the ruling that
             says why a resolved card owes a triple at all. It also books the
             R10 verdict and ends a churn this workflow has now paid for twice.
             SEVEN of the eight producing types are enforced when it ends.
             SESSION 3 CONTINUES; YOU CREATE NO PULL REQUEST AND MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the R10 verdict and one prose-slip line · C3 DECISION
             F032 D7 · C4 both flight-plan arms and the gate entry · C5 the
             tests and the permanently repointed guards · C6 the handback ·
             then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r11.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`, `.agent/decisions.md`,
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
    bytes already end in a newline — all three append targets do; G5 proves the
    arithmetic for two of them and G4 the third.
 3. THE AUTHORED UNITS OF THIS BLOCK are the whole block itself and the slices
    PLANF032R11, LEDGER11, SLIP11 and DECISION11. This paragraph gives no count
    of them; G3 reports the number the extraction measured.
 4. C0a IS A COPY, NOT A RETYPE. `.remedy-wt/f032-r11.md` exists on disk and
    holds this block. Copy that file to `.agent/authored/f032-r11.md` with a
    byte-preserving read-and-write and commit it. C0b then writes the SAME
    bytes to `.agent/last_block.md`. Do not reformat, rewrap or strip anything.
 5. PRODUCTION CODE IS DESCRIBED, NOT SLICED. Items S1 through S8 are a spec.
    You write the Python yourself, in the style of the branches already in
    `decision_queue.py`, and you carry the WHY into a comment above each change
    the way F032 R5, R7, R8, R9 and R10 did in that same file.
 6. COMMENT DENSITY MATCHES THE FILE. Every producer upgraded so far carries a
    short comment naming the task slice, why each guard is there, and what
    would break without it. Match that; do not exceed it.
 7. ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6, in that order and with no
    commit between them. C2 is the only commit touching `.agent/live_review.md`
    and `.agent/prose_slips.md`; C3 is the only commit touching
    `.agent/decisions.md`. C4 CARRIES BOTH ARMS AND THE GATE ENTRY TOGETHER —
    splitting them would land a commit where the resolved arm raises, because
    the gate does not read `status`.
 8. THE RULING IS ALREADY MADE. Slice DECISION11 is DECISION F032 D7 and it is
    the authority for S5. Do not re-derive it, do not weaken it, and do not add
    a `status` branch to `enforce_decision_evidence`.
 9. RE-READ `.agent/STOP` FROM DISK TWICE: once before C0a and once before C6.
    If it exists at either reading, stop, write the handback, and end.
10. MUTATION RUNS GO IN A DISPOSABLE WORKTREE. `git worktree add --detach
    .remedy-wt/f032-r11-mut <C5 sha>`, run the red-proofs there, restore the
    file byte for byte after each one, remove the worktree and prune. The
    primary checkout satisfies `git status --porcelain` == empty at every
    commit.
11. PURGE `__pycache__` AND PASS `-B` BEFORE EVERY PYTEST RUN IN THE WORKTREE.
12. THE ROUND BASE IS `91b00286`, the commit that handed back R10. Every
    numeral this block states about the base was measured there.
13. RUN THE SUITES SERIALLY. Never two pytest processes at once.

Spec — T002f, the flight-plan approval.
 S1. READ FIRST, AND THE READINGS THAT MAKE THIS ROUND'S GUARDS LOAD-BEARING.
     Branch 7 of `list_decisions` reads `job.flight_plan` and splits on
     `_approval`. The PENDING arm always sets `payload["options"]` to exactly
     `["approve", "reject"]`, and adds `clarifications` and `mission_offer`
     only when the plan and the intake supply them. The RESOLVED arm is reached
     when `_approval` is `approved` AND `_approval_audit` is truthy; it passes
     NO payload, sets `next_actions` to the empty tuple and `status` to
     `resolved`. AT `91b00286` BOTH ARMS ARE DRIVEN THROUGH `list_decisions` BY
     TESTS THAT SUPPLY ALMOST NOTHING: `tests/orchestration/test_mission_state.py`
     builds `Job(name="t", flight_plan={"_approval": "pending"})` with no
     clarifications and no intake, and
     `tests/orchestration/test_decision_inbox.py` builds the resolved arm with
     `_approval_audit` `{"reason": "approved"}` and no `mode` key. So a ref that
     depended on a clarification, on an intake or on the audit's `mode` would
     point at nothing there, rule (c) of `evidence_triple_problems` would fire,
     and those suites would go RED the moment this type joins the gate set.
     `open_clarification_questions` returns records carrying `id`, `question`,
     `default_answer` and `impact`.
 S2. THE PENDING ARM'S REFS. Emit a ref of kind `decision` whose target is the
     literal `fp:approval`, ALWAYS and unguarded, labelled as the flight-plan
     approval this job is waiting on. It is the card's own id and the one value
     this arm is guaranteed to have, and it is what keeps the minimal job of S1
     valid. Then emit ONE ref per open clarification question, kind `decision`,
     target that question's `id`, labelled as the open question that ships with
     this plan — emitted only for questions whose `id` is non-empty, because
     `open_clarification_questions` defaults that field to the empty string.
     Emit no ref for the mission offer: it is an OFFER attached to this card
     rather than evidence for the plan, and A2 of
     `docs/roadmap/features/T5_F032.md` forbids inventing vocabulary to carry
     it. Never emit a ref whose target is the empty string.
 S3. THE PENDING ARM'S OUTCOMES ARE KEYED, and this is the first producer since
     the budget stop where rule (g) rather than rule (h) applies. The payload
     already lists `approve` and `reject`, so emit EXACTLY ONE
     `DecisionOptionOutcome` per option, keyed with those two words and no
     others — rule (g) compares the outcome keys against the options list in
     BOTH directions. Do NOT change `payload`, `next_actions` or the summary.
     The `approve` outcome says what starting the run buys — the plan's tasks
     execute in the order it records — and what it costs: work begins against
     whatever the plan assumed, and an assumption nobody checked is paid for in
     rework. The `reject` outcome says that nothing executes and the plan goes
     back for revision, so a wrong scope costs a replan rather than a run, at
     the cost that the job makes no progress until a new plan is approved and
     the context this planning built is spent again. THE EXACT WORDING IS
     YOURS, and no half may be, or consist wholly of, a member of
     `BOILERPLATE_PHRASES`.
 S4. THE RESOLVED ARM'S REFS. Emit the same unguarded `decision` ref targeting
     `fp:approval`, labelled as the flight-plan approval this record answers.
     Then emit a ref of kind `decision` targeting the audit's `reason`, labelled
     as the reason recorded when the plan was approved, ONLY when that value is
     non-empty — the branch already computes `reason` with a default, so reuse
     that variable rather than re-reading the dict. Then emit a ref of kind
     `decision` targeting the audit's `mode`, labelled as how the approval was
     given, ONLY when the audit carries a non-empty `mode`; the resolved-arm
     test of S1 supplies no `mode`, so that guard is load-bearing rather than
     defensive.
 S5. THE RESOLVED ARM'S OUTCOME IS UNKEYED, AND DECISION F032 D7 IS WHY. That
     arm passes no payload, so the gate reads it as optionless and rule (h)
     requires exactly one outcome keyed `UNKEYED_OPTION`. It states the
     consequence of the answer that WAS recorded rather than of one still to
     come: the run executes the plan this approval named, so its tasks are the
     agreed scope, at the cost that a plan approved on an assumption which has
     since changed keeps the run pointed at the old scope until someone
     revisits it. Same prohibitions as S3.
 S6. `flight_plan_approval` JOINS `TRIPLE_REQUIRED_TYPES` IN C4, the same commit
     that gives BOTH arms their triples, per constraint 7 and DECISION F032 D5.
 S7. END THE GUARD CHURN, PERMANENTLY. Two tests in
     `tests/orchestration/test_decision_evidence.py` need a decision type the
     gate does NOT enforce:
     `test_an_unenforced_tripleless_decision_is_left_alone` and
     `test_a_tripleless_decision_exports_empty_lists_and_the_legacy_status`.
     They named `memory_review` until R10 enforced it, they name
     `flight_plan_approval` at `91b00286`, and C4 falsifies that too — the
     second time this pair has moved in two rounds, and pointing them at
     `task_decision` would only schedule a third. Repoint BOTH to
     `revert_missing`, and say in the docstring WHY it is stable: DECISION F031
     D3 records that `revert_missing` and `worker_approval` have NO PRODUCER AT
     ALL, so neither can ever join a set whose entry rule is "in the same commit
     that gives its producer a real triple". Also update the exact-membership
     assertion in
     `test_the_shipped_required_type_set_holds_exactly_the_upgraded_producers`.
 S8. THE NEW TESTS GO IN `tests/orchestration/test_decision_evidence.py` and
     nowhere else, driving the REAL branches through `list_decisions` as every
     T002 test in that file already does. For the PENDING arm: the minimal job
     of S1 must yield a valid card carrying the one unguarded ref; a plan
     carrying two open clarifications must yield three refs in order, with
     kinds, targets and labels asserted; and a plan carrying a clarification
     whose `id` is the EMPTY STRING must yield ONLY the unguarded ref, which
     pins the id guard in both directions. Assert the outcome
     keys are exactly `approve` and `reject`, that neither half of either is
     empty, and that `evidence_triple_problems` returns the empty list WHEN
     GIVEN THAT CARD'S OWN OPTIONS — pass `decision.payload["options"]`, not an
     empty list, or the check silently tests rule (h) instead of rule (g). For
     the RESOLVED arm: the audit of S1 carrying only `reason` must yield two
     refs; an audit carrying `reason` and `mode` must yield three; a test must
     fail if the `mode` ref is emitted unconditionally. Assert its single
     unkeyed outcome, that its `status` is `resolved` and that it is still
     enforced — a card of this type with its triple dropped must raise
     `DecisionEvidenceError` on EACH arm. For both arms assert no ref carries an
     empty target and that the exported card's `evidence_status` is `present`.

Done when. Report each gate as its own line in the handback, with the real
command, its exit code and the real output you saw. G1 through G8 are ordered at
commits STRICTLY EARLIER than C6, which writes the handback; C6's own readings
are not values this round writes anywhere, and G1 therefore stops at C5.
 G1. HYGIENE, BASE AND THE SENTINEL. Report `git rev-parse HEAD` before C0a and
     confirm it is the round base named in constraint 12; report the branch is
     `feature/f032-evidence-triple`; report the `git status --porcelain` line
     count after EACH of C0a through C5, each 0; report whether `.agent/STOP`
     exists at the two readings constraint 9 orders.
 G2. TRANSPORT. Report the sha256, byte count and line count of
     `.remedy-wt/f032-r11.md`, of the committed `.agent/authored/f032-r11.md`
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
 G4. THE PLAN AND THE SLIP. Report whether `.agent/plan.md` at C1 is byte-equal
     to slice PLANF032R11 under the convention of constraint 2, and report the
     same comparison with the trailing newline removed as a NEGATIVE CONTROL,
     which must be FALSE. Report `wc -l` and that it is under 50, and the counts
     of `^## Goal$` and `^## Next Steps$`, each 1. Then report whether
     `.agent/prose_slips.md` at C2 equals its pre-commit blob plus ONE newline
     plus slice SLIP11, byte for byte.
 G5. THE TWO RECORD APPENDS. For `.agent/live_review.md` at C2 and
     `.agent/decisions.md` at C3, each read with `git show <sha>:<path>` and
     never by writing over the tracked file: prove the file equals its
     pre-commit blob plus ONE newline plus its slice, byte for byte, report the
     arithmetic as three numbers summing to the result, and report that the
     pre-commit blob is a byte PREFIX. Then run a SECOND, INDEPENDENT structural
     reader over EACH: split the whole file on blank lines, let N be the number
     of paragraphs in that slice as YOUR script counts them, and compare the
     LAST N units against those N paragraphs IN ORDER. As a NEGATIVE CONTROL
     flip ONE byte inside the FIRST appended paragraph of each, in memory only,
     and report that BOTH readers reject it. The reviewer measured
     `.agent/live_review.md` at `91b00286` as 1076472 bytes over 427 blank-line
     units. Then report, before and after C2, the counts of
     `^Gate: F\d+ R\d+ — `, `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-` and
     `^Gate: R\d+ — `, the size of the open set — every registered id minus
     every resolved id — the maximum id, the gate keys ADDED and the ids ADDED
     to the resolved set. The reviewer measured 62, 274, 24, 1 and 19 at the
     base, with the open set 250 and the maximum `R-0713`. Report the count of
     `^## DECISION F032 D\d+ ` in `.agent/decisions.md` before and after C3.
 G6. THE CODE, LINTED AND READ BACK. Run `python3 -m ruff check` over
     `packages/orchestration/decision_queue.py` and
     `packages/orchestration/decision_evidence.py` and report the exit code and
     the verbatim output. Then, at C4, call `list_decisions` yourself and report
     the refs as `(kind, target, label)` tuples and the outcomes as
     `(option, expected_outcome, downside)` tuples for each of these cases: the
     minimal pending job of S1; a pending job whose plan carries two open
     clarifications; the resolved arm with an audit carrying only `reason`; and
     the resolved arm with an audit carrying `reason` and `mode`. For each,
     report what `evidence_triple_problems` returns when passed that card's OWN
     options, and report `export_decision_json`'s `evidence_status` and
     `status`. Report the sorted members of `TRIPLE_REQUIRED_TYPES`.
 G7. TESTS GREEN, THEN RED UNDER MUTATION, AND THE WIDER SUITES UNMOVED. Run
     `python3 -m pytest tests/orchestration/test_decision_evidence.py -q` in the
     PRIMARY checkout at C5 and report the exit code and the count line. Then in
     the disposable worktree of constraint 10, at C5, report the exit code, the
     count line and the number of `^FAILED` lines for: a CONTROL run before any
     mutation; mutation (a), the non-empty-`id` guard of S2 removed so every
     clarification emits a ref — which turns the empty-id case of S8 into a ref
     targeting nothing, and rule (c) then refuses the whole card;
     mutation (b), the `mode` ref of S4 emitted unconditionally; mutation (c),
     `flight_plan_approval` removed from `TRIPLE_REQUIRED_TYPES`; mutation (d),
     the `reject` outcome of S3 deleted so the pending arm keys only `approve`;
     and a CONTROL run after all four restorations, with the worktree's `git
     status --porcelain` empty. Mutations (a), (b) and (d) are applied to
     `packages/orchestration/decision_queue.py` and mutation (c) to
     `packages/orchestration/decision_evidence.py`; before applying each one,
     count its exact byte string IN THAT FILE and report that the count is 1.
     Then run `tests/orchestration/test_decision_evidence.py`,
     `tests/orchestration/test_decision_inbox.py`,
     `tests/orchestration/test_mission_state.py` and
     `tests/orchestration/test_bundled_clarification.py` as ONE pytest process
     in the primary checkout and report the exit code, the count line and the
     number of `^FAILED` lines.
 G8. STRUCTURE, CANARY AND THE PR GATE. Run
     `python3 -m pytest tests/cli/test_golden_path.py -q` and report the exit
     code and the count line. Report the path set of `git diff --name-only
     91b00286..<C5 sha>` against the paths the Change set lists other than
     `.agent/handoff.md`, as the two residues, both of which must be EMPTY.
     Report that `git diff --stat 91b00286..<C5 sha> -- apps/` and the same for
     `-- docs/` are both EMPTY. Report the insertion count of each of C0a
     through C5, that each is single-parent, and that each is under 500. Those
     counts and the `+/-` column of the handback's `## Commits` section are one
     reading written twice: derive both from `git diff --numstat`, compare them
     cell by cell, and report that they agree. Report the counts of
     `^<<<SLICE ` and `^<<<END ` in `.agent/plan.md`, `.agent/live_review.md`,
     `.agent/prose_slips.md`, `.agent/decisions.md`,
     `packages/orchestration/decision_queue.py`,
     `packages/orchestration/decision_evidence.py` and
     `tests/orchestration/test_decision_evidence.py`, each 0, against a CONTROL
     count over the committed C0a blob, which must be non-zero. Report `git
     ls-files .remedy-wt` as 0 lines, `git worktree list` as 1 line and `git
     branch --list "tmp/*"` as 0 lines. Report the output of `gh pr list --state
     open --json number,headRefName,baseRefName,isDraft`; merge nothing and
     create nothing.

Handback: rewrite `.agent/handoff.md` as C6, per
docs/agents/handback_template.md. It carries the mandated sections — the state
block, the commits table with each commit's real `+/-` read from `git diff
--numstat` for C0a through C5 — C6 cannot table its own numstat and says so in
its row — the item-status table covering every C and every S exactly once, the
deviations, the verification lines of G1 through G8 and the next steps. It
states that the feature is F032, that R11 is the round, and that this is SESSION
3, which began at R10. Session 1 was R1 through R5 and session 2 was R6 through
R9. Eleven rounds across three sessions is inside the soft limit of 25 rounds or
7 sessions, so do NOT emit a limit report. The handback has NO LENGTH CAP, so do
not declare, measure or apologise for its length. Its `## Next` section names
Phase 1 rule 1 of docs/agents/self_drive_protocol.md — the `.agent/STOP` re-read
from disk — before anything else, then the Open PR Gate, then `task_decision`,
the last producer, whose options come from the escalation record and are
arbitrary strings, so its outcomes are built per option rather than written out.
Then push the branch.

<<<SLICE PLANF032R11>>>
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
R11 upgrades the flight-plan approval, the first producing type with TWO arms:
a pending card carrying the two options the write door accepts, and a resolved
card carrying none. The emit gate selects on type alone and never reads
`status`, so both arms are enforced together — DECISION F032 D7 records why
that is the right reading and what a resolved card's outcome then means. The
round also books the R10 verdict and repoints the two unenforced-type guards to
a type with no producer, so they stop moving every round.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R10 verdict and one prose-slip line | ordered | the record first |
| C3 DECISION F032 D7 | ordered | the ruling S5 rests on |
| C4 both arms and the gate entry | ordered | S2 to S6, one commit |
| C5 the tests and the repointed guards | ordered | S7 and S8 |
| C6 the handback | ordered | |

## Next Steps
1. The task decision, the last producing type. Its options come from the
   escalation record and are arbitrary strings, so its outcomes are built per
   option rather than written out, and it has a resolved arm that DECISION
   F032 D7 already rules on. With it the gate set is complete and T002 ends.
2. T003 card enrichment and the chip deep links, which is the first F032 work
   to touch `apps/` and therefore the design reference.
3. The integration gate, then the closure sequence.

## Risks
- Rule (g) compares outcome keys against the options list in both directions,
  so the pending arm is the first producer where a mis-keyed outcome raises
  rather than merely reading oddly.
- Seven types are enforced from this round on, so a later change that regresses
  any of their triples raises instead of rendering. That is the intent.
<<<END PLANF032R11>>>

<<<SLICE LEDGER11>>>
Gate: F032 R10 — the F032 T002e REPO-DIRTY AND MEMORY-REVIEW entry. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all eight itself at `91b00286`. TRANSPORT IS PROVED FROM A VALUE THE REVIEWER HELD BEFORE DELEGATING: sha256 `bd2560b02c3bfd65c497fcde4ce0811f30013658040703fdfd0f7aa950990a4a` over 27191 bytes and 332 lines was computed on the scratch original at authoring time, and the committed `.agent/authored/f032-r10.md` blob at `b1790261` and the committed `.agent/last_block.md` blob at `83529164` both carry exactly it, as the SAME git blob `a991368a80c9`. That chain runs from an independently held digest through the saved copy to its mirror; under docs/agents/self_drive_protocol.md there is no paste relay, so it says NOTHING about the bytes of any prompt and this entry claims no more. THE TWO THINNEST BRANCHES NOW CITE WHAT THEY HAVE. The dirty-repo card emits an unguarded `failure` ref targeting the literal `git_status_read` — the one receipt that branch is guaranteed, because the branch exists only because that event was read — plus a guarded `failure` ref for `status_hash`. THAT GUARD IS THE ROUND'S REAL FINDING, and it was designed from the emitter and the fixture together rather than from either alone: `apps/cli/commands/repo.py` writes seven metadata keys, `_fixture_repo_dirty` in `tests/orchestration/test_decision_inbox.py` writes only `dirty`, and that fixture is driven through `list_decisions` by a parametrization over every producing type — so a triple resting on any metadata key would have turned that suite red the moment the type joined the gate set. The memory-review card emits three refs, EVERY ONE GUARDED, because `MemoryEntry.key` defaults to the empty string and each field ref belongs to the arm that selected the card; rule (a) survives a keyless card because the selecting predicate guarantees at least one of the two field refs fires, and the reviewer confirmed that case by reading the card back. Both cards carry exactly one outcome keyed `UNKEYED_OPTION` and no `payload`, which is DECISION F032 D3's optionless case. THE REVIEWER RAN FIVE MUTATIONS IN ITS OWN DISPOSABLE WORKTREE AT `0a6c17bf`, `__pycache__` purged and `-B` passed before each, each exact byte string counted 1 before it was applied and the file restored after: the `status_hash` ref made unconditional gave exit 1 at `3 failed, 83 passed`; the `review_status` ref made unconditional gave exit 1 at `2 failed, 84 passed`; removing `repo_dirty` from `TRIPLE_REQUIRED_TYPES` gave exit 1 at `2 failed, 84 passed`; removing `memory_review` from it, which the block did NOT order, gave exit 1 at `2 failed, 84 passed`; and emptying the memory-review refs gave exit 1 at `18 failed, 68 passed`. Controls before and after all five were a real exit 0 at `86 passed`, with the worktree's `git status --porcelain` empty. THE LAST OF THOSE SETTLES THE ROUND'S OWN OPEN QUESTION, which the worker raised as deviation 5 rather than assuming: branch 6 runs inside `except (ImportError, ValueError, OSError)` and `DecisionEvidenceError` subclasses `ValueError`, so a reader could reasonably fear the gate is swallowed there. It is not — the gate runs after every branch's `try`, and the reviewer read the propagated error text, `decision 'mem:deploy-target' of type 'memory_review' carries no acceptable evidence triple`, out of `list_decisions` itself. NOTHING ELSE MOVED: `ruff check` over both modules exit 0 with the verbatim output `All checks passed!`, the three decision suites as one process exit 0 at `146 passed`, the golden-path canary exit 0 at `42 passed`, both path residues EMPTY, `apps/` and `docs/` EMPTY, insertions 332, 274, 22, 4, 48, 55, 341 and 244 across the eight commits, each single-parent and under 500, markers 0 and 0 in all five edited files against a CONTROL of 2 and 2 over the C0a blob, `.remedy-wt` 0 tracked, `git worktree list` 1 line, the remote tip equal to the local tip and the Open PR Gate `[]`. THE LEDGER MOVED EXACTLY AS ORDERED: 1071711 + 1 + 4760 = 1076472 with the base a byte PREFIX, both readers rejecting a byte flipped inside the FIRST appended paragraph, `^Gate: F\d+ R\d+ — ` 61 to 62 adding exactly `F032 R9`, `^Done: R-\d+ — ` 23 to 24 adding exactly `R-0713`, `^- R-\d+ — ` steady at 274, and the open set 250. ONE GATE THIS BLOCK ORDERED WAS UNMEETABLE AS WRITTEN, and the worker was right to declare it rather than fake it: G1 asked for the porcelain count after C6 while the Done-when preamble put every gate strictly earlier than C6, so no reading after the handback commit can appear in the file that commit writes. The reviewer measured it instead, at `91b00286`, and it is 0. That is a defect of the reviewer's prose with nothing wrong on disk, so under operator amendment amend0827 rule 2 it spends no id and is recorded as one dated line in `.agent/prose_slips.md`. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER11>>>

<<<SLICE SLIP11>>>
- 2026-08-28 · F032 R10 · The block's Done-when preamble put every gate at a
  commit strictly earlier than C6 while G1 asked for the `git status
  --porcelain` count after C6, so one clause of one gate was unmeetable by
  construction; the worker declared it and reported the reading outside the
  file, and the reviewer measured it at `91b00286` as 0.
<<<END SLIP11>>>

<<<SLICE DECISION11>>>
## DECISION F032 D7 (2026-08-28) — a RESOLVED card owes the same triple as an open one, and its outcome speaks of the answer already recorded

CONTEXT, measured at `91b00286`. Two of the eight producing branches of
`packages/orchestration/decision_queue.py::list_decisions` have TWO ARMS. Branch
7 builds an open `flight_plan_approval` when the plan's `_approval` is
`pending`, and a card whose `status` is `resolved`, whose `next_actions` are
empty and which carries no `payload` at all when the plan was already approved
and left an `_approval_audit`. Branch 8 has the same shape for `task_decision`.
`decision_evidence.enforce_decision_evidence` selects the decisions it checks by
TYPE ALONE and never reads `status`, so the moment either type joins
`TRIPLE_REQUIRED_TYPES` both of its arms are enforced together. The resolved arm
is not hypothetical: `tests/orchestration/test_decision_inbox.py` drives it
directly. The question this decision settles is what a triple MEANS on a card
whose question has already been answered, since `expected_outcome` and
`downside` are written in the language of a choice still to come.

CHOSEN. The gate keeps its type-only selection, and a resolved card carries a
real triple like any other. Its REFS are the audit trail the answer actually
left — the card's own id, and the recorded reason and mode where the record
carries them. Its single outcome, keyed `UNKEYED_OPTION` because the arm passes
no payload, states the consequence of the answer THAT WAS RECORDED rather than
of one still open: what the run now proceeds to do, and what it costs if the
ground the answer rested on has since moved.

WHY. Three reasons, in the order they bind. FIRST, the gate's reach would
otherwise depend on a field each producer sets on its own: `status` is written
independently by eight branches, and a gate that reads it becomes eight gates
whose behaviour a reader has to reconstruct per branch, where today the entry
rule is one sentence — a type is enforced or it is not. SECOND, a resolved card
is still RENDERED. `build_decision_inbox` returns it, the browser draws it, and
a reader looking at a plan that was auto-approved has exactly the question the
triple answers: on what, and at what cost. Enforcement that stopped at
`status == "open"` would leave that card carrying the honest-legacy placeholder
forever, which is a false statement about a card this feature did upgrade.
THIRD, the alternative silently halves the enforcement of both two-armed types:
`flight_plan_approval` and `task_decision` would report as enforced while the
arm nobody tested went unchecked, and `docs/roadmap/features/T5_F032.md` makes
"a canary producer missing a field fails CI" the acceptance criterion, not "a
canary producer missing a field on one arm".

REJECTED, and why. Guarding the gate with `status == "open"`, so a resolved card
is left entirely alone. It is the smaller diff and it reads as principled — the
triple exists so a human can decide, and a resolved card asks nothing. It was
rejected because the card is still shown, because it makes the enforced set a
weaker statement than it appears, and because the audit refs a resolved card
carries are the most checkable evidence in this whole feature: they are the only
place the record says what was actually answered.

REVERSE by adding `if _text(getattr(decision, "status", None)) != "open":
continue` to the loop in `enforce_decision_evidence` and deleting the resolved
arms' triples from branches 7 and 8; no other change is required, and the
per-arm tests named in the F032 R11 and R12 blocks are the ones that then go
red.
<<<END DECISION11>>>
