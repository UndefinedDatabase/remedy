STEP R10 / F032 — T002e: THE TWO PRODUCERS THAT CITE NOTHING
Goal:        UPGRADE THE DIRTY-REPO CARD AND THE MEMORY-REVIEW CARD, THE TWO
             BRANCHES THAT STILL CARRY NO RECEIPTS AT ALL, AND CLOSE `R-0713`
             IN THE RECORD. The dirty-repo card says "Target repository has
             uncommitted changes." and cites neither the reading it came from
             nor the fingerprint that reading recorded. The memory-review card
             names a key and states a reason — R5 gave it that — and cites
             neither. Both branches are optionless, so each owes exactly one
             unkeyed outcome. The round also books the R9 verdict and writes
             the `Done:` text for `R-0713`, which R9 fixed in code and left
             open in the record. SIX of the eight producing types are enforced
             when this round ends. SESSION 3 STARTS HERE; YOU CREATE NO PULL
             REQUEST AND MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the R9 verdict and `Done: R-0713` · C3 the repo-dirty
             triple and its gate entry · C4 the memory-review triple and its
             gate entry · C5 the tests for both and the two repointed guards ·
             C6 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r10.md`,
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
    bytes already end in a newline — they do; G5 proves the arithmetic.
 3. THE AUTHORED UNITS OF THIS BLOCK are the whole block itself, the slice
    PLANF032R10 and the slice LEDGER10. This paragraph gives no count of them;
    G3 reports the number the extraction measured.
 4. C0a IS A COPY, NOT A RETYPE. `.remedy-wt/f032-r10.md` exists on disk and
    holds this block. Copy that file to `.agent/authored/f032-r10.md` with a
    byte-preserving read-and-write and commit it. C0b then writes the SAME
    bytes to `.agent/last_block.md`. Do not reformat, rewrap or strip anything.
 5. PRODUCTION CODE IS DESCRIBED, NOT SLICED. Items S1 through S7 are a spec.
    You write the Python yourself, in the style of the branches already in
    `decision_queue.py`, and you carry the WHY into a comment above each change
    the way F032 R5, R7, R8 and R9 did in that same file.
 6. COMMENT DENSITY MATCHES THE FILE. Every producer upgraded so far carries a
    short comment naming the finding or task slice, why the guard is there, and
    what would break without it. Match that; do not exceed it.
 7. ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6, in that order and with no
    commit between them. C2 is the only commit touching `.agent/live_review.md`.
    C3 and C4 each land ONE producer's triple together with that type's entry in
    `TRIPLE_REQUIRED_TYPES` — never a type ahead of its triple, which is what
    DECISION F032 D5 requires and what the exact-membership test pins.
 8. THE `Done:` PARAGRAPH IN LEDGER10 DESCRIBES A FIX THAT ALREADY LANDED, at
    commit `f0ec4b09` on this branch, so it names that SHA and not `HEAD`.
 9. RE-READ `.agent/STOP` FROM DISK TWICE: once before C0a and once before C6.
    If it exists at either reading, stop, write the handback, and end.
10. MUTATION RUNS GO IN A DISPOSABLE WORKTREE. `git worktree add --detach
    .remedy-wt/f032-r10-mut <C5 sha>`, run the red-proofs there, restore the
    file after each one, remove the worktree and prune. The primary checkout
    satisfies `git status --porcelain` == empty at every commit.
11. PURGE `__pycache__` AND PASS `-B` BEFORE EVERY PYTEST RUN IN THE WORKTREE.
    An equal-length source swap otherwise leaves a stale module and reports the
    wrong colour; that cost F032 R7 a re-run.
12. THE ROUND BASE IS `0216c5bb`, the commit that closed session 2. Every
    numeral this block states about the base was measured there.
13. RUN THE SUITES SERIALLY. Never two pytest processes at once; concurrent
    runs in this repository produce false reds.

Spec — T002e, the dirty repo and the memory review.
 S1. READ FIRST, AND THE READINGS THAT MAKE THIS ROUND'S GUARDS LOAD-BEARING.
     Branch 4 of `list_decisions` selects the LAST `git_status_read` event and
     builds `id="dirty_repo"` when `metadata["dirty"]` is truthy. The ONLY
     emitter of that event outside `tests/` is `apps/cli/commands/repo.py`,
     which at `0216c5bb` writes `outcome` as a NAMED field of `RunLogWriter.log`
     — so it lands at the event's top level and NOT in `metadata` — and writes
     `is_git_repo`, `git_available`, `branch`, `head_sha`, `dirty`,
     `changed_file_count` and `status_hash` into `metadata`. THE FIXTURES DO NOT.
     `_fixture_repo_dirty` in `tests/orchestration/test_decision_inbox.py` at
     `0216c5bb` carries `metadata` `{"dirty": True}` and nothing else, and that
     fixture is driven through `list_decisions` by
     `test_card_appears_for_each_producing_type`, which is parametrized over
     every producing type. So a repo-dirty triple whose ONLY ref depends on a
     metadata key would emit zero refs there, rule (a) of
     `evidence_triple_problems` would fire, and that parametrization would go
     RED the moment `repo_dirty` joins the gate set. Branch 6 selects memory
     cards where `validity == "stale"` OR `review_status == "needs_review"`;
     `MemoryEntry.key` defaults to the empty string
     (`packages/memory/models.py`), so it is not guaranteed non-empty either.
 S2. THE REPO-DIRTY REFS. Emit a ref of kind `failure` whose target is the
     literal event name `git_status_read`, ALWAYS and unguarded, labelled as
     the run-log event that reported the working tree dirty. It is the one
     value this branch is guaranteed to have — the branch exists because that
     event was read — and it is what keeps the thin fixture of S1 valid. Then
     emit a SECOND ref of kind `failure` targeting the event metadata's
     `status_hash`, labelled as the status fingerprint that reading recorded,
     ONLY when that value is non-empty. Emit NO ref for `branch`, `head_sha` or
     `changed_file_count`: none of the four kinds in
     `DECISION_EVIDENCE_REF_KINDS` types a branch name, a commit or a count
     without lying about what it is, and A2 of
     `docs/roadmap/features/T5_F032.md` forbids inventing vocabulary here.
     Never emit a ref whose target is the empty string.
 S3. THE REPO-DIRTY OUTCOME IS UNKEYED. This branch carries no `payload` and its
     one `next_action` is an instruction rather than a choice, so DECISION F032
     D3's optionless case applies and rule (h) requires EXACTLY ONE outcome
     keyed `UNKEYED_OPTION`. Do NOT add a `payload` to this branch. The outcome
     says what committing or stashing the target repository's changes buys — a
     clean tree, so a later diff shows only what this job did — and what it
     costs: the job waits while that happens, and stashing work that is not this
     job's can hide changes their author still needs. THE EXACT WORDING IS
     YOURS, and neither half may be, or consist wholly of, a member of
     `BOILERPLATE_PHRASES`. In the SAME commit, `repo_dirty` joins
     `TRIPLE_REQUIRED_TYPES` in `packages/orchestration/decision_evidence.py`.
 S4. THE MEMORY-REVIEW REFS, ALL THREE GUARDED. Emit a ref of kind `decision`
     targeting `me.key`, labelled as the memory card this review is about, ONLY
     when the key is non-empty — `decision` is the kind the patch-approval
     branch already uses for a record identifier a human acts on. Emit a ref of
     kind `failure` targeting `me.validity`, labelled as the validity the card
     carries, ONLY when the card is stale. Emit a ref of kind `failure`
     targeting `me.review_status`, labelled as the review status the card
     carries, ONLY when the card is flagged for review. Reuse the two booleans
     R5 already computes for the summary rather than re-reading the fields.
     Rule (a) stays satisfiable with no key at all, because the branch's own
     selecting predicate guarantees at least one of the last two fires; say so
     in the comment, because that is the argument the guard rests on.
 S5. THE MEMORY-REVIEW OUTCOME IS UNKEYED, on the same grounds as S3 and with
     the same prohibitions. It says what opening the named card buys — what it
     claims and when it was last confirmed become visible, so it can be
     re-approved, corrected or superseded instead of trusted blind — and what it
     costs: reading it takes time now, and a card left in place while it is
     checked keeps feeding whatever already reads it. In the SAME commit,
     `memory_review` joins `TRIPLE_REQUIRED_TYPES`.
 S6. THE TWO GUARDS THIS ROUND FALSIFIES, AND THEY ARE REPOINTED, NEVER DELETED.
     At `0216c5bb`, `tests/orchestration/test_decision_evidence.py` uses
     `memory_review` as its example of a type the gate does NOT enforce, in
     `test_an_unenforced_tripleless_decision_is_left_alone` and in
     `test_a_tripleless_decision_exports_empty_lists_and_the_legacy_status`.
     C4 makes that false. Repoint BOTH to `flight_plan_approval`, which is still
     unenforced after this round, and correct the first one's docstring, which
     reads "No existing producer changes behaviour: none of their types is
     enforced" — four types were already enforced when this round began. Update
     the exact-membership assertion in
     `test_the_shipped_required_type_set_holds_exactly_the_upgraded_producers`
     to name every type the gate enforces once C3 and C4 have landed. These
     edits belong in C5 with the new tests.
 S7. THE NEW TESTS GO IN `tests/orchestration/test_decision_evidence.py` and
     nowhere else. Drive the REAL branches through `list_decisions`, as the
     T002a through T002d tests in that file already do. For the repo-dirty card:
     the THIN event of S1, carrying only `dirty`, must yield a valid card with
     the one unguarded ref; an event carrying the full metadata that
     `apps/cli/commands/repo.py` writes must yield both refs, in order, with
     their kinds, targets and labels asserted; a test must fail if the
     `status_hash` ref is emitted unconditionally. For the memory-review card:
     a stale-only card, a flagged-only card, a card that is both, and a card
     whose key is empty — asserting the ref list of each, so every one of the
     three guards is pinned in both directions. For both cards assert the single
     unkeyed outcome's option key and that neither half is empty, that no ref
     carries an empty target, that `evidence_triple_problems` returns the empty
     list, and that the exported card's `evidence_status` is `present`.

Done when. Report each gate as its own line in the handback, with the real
command, its exit code and the real output you saw. G1 through G7 are ordered
at commits STRICTLY EARLIER than C6, which is the commit that writes the
handback; C6's own numbers are not a value this round writes anywhere.
 G1. HYGIENE, BASE AND THE SENTINEL. Report `git rev-parse HEAD` before C0a and
     confirm it is the round base named in constraint 12; report the branch is
     `feature/f032-evidence-triple`; report the `git status --porcelain` line
     count after EACH of C0a through C6, each 0; report whether `.agent/STOP`
     exists at the two readings constraint 9 orders.
 G2. TRANSPORT. Report the sha256, byte count and line count of
     `.remedy-wt/f032-r10.md`, of the committed `.agent/authored/f032-r10.md`
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
     PLANF032R10 under the convention of constraint 2, and report the same
     comparison with the trailing newline removed as a NEGATIVE CONTROL, which
     must be FALSE. Report `wc -l` and that it is under 50, and the counts of
     `^## Goal$` and `^## Next Steps$`, each 1.
 G5. THE LEDGER APPEND. Read the pre-commit blob with `git show
     0216c5bb:.agent/live_review.md`, never by writing over the tracked file.
     Prove `.agent/live_review.md` at C2 equals that
     pre-commit blob plus ONE newline plus the LEDGER10 slice, byte for byte,
     and report the arithmetic as three numbers summing to the result; report
     that the pre-commit blob is a byte PREFIX of the result. The reviewer
     measured the base at `0216c5bb` as 1071711 bytes over 425 blank-line
     units. Then run a SECOND, INDEPENDENT structural reader: split the whole
     file on blank lines, let N be the number of paragraphs in the LEDGER10
     slice as YOUR script counts them, and compare the LAST N units of the file
     against those N paragraphs IN ORDER. As a NEGATIVE CONTROL flip ONE byte
     inside the FIRST appended paragraph, in memory only, and report that BOTH
     readers reject it. Then report, before and after C2, the counts of
     `^Gate: F\d+ R\d+ — `, `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-` and
     `^Gate: R\d+ — `, the size of the open set — every registered id minus
     every resolved id — the maximum id, the gate keys ADDED and the ids ADDED
     to the resolved set. The reviewer measured 61, 274, 23, 1 and 19 at the
     base, with the open set 251 and the maximum `R-0713`.
 G6. THE CODE, LINTED AND READ BACK. Run `python3 -m ruff check` over
     `packages/orchestration/decision_queue.py` and
     `packages/orchestration/decision_evidence.py` and report the exit code and
     the verbatim output. Then, at C4, call `list_decisions` yourself and report
     the refs as `(kind, target, label)` tuples and the outcomes as
     `(option, expected_outcome, downside)` tuples for each of these cases: the
     repo-dirty card built from the thin event of S1; the repo-dirty card from an
     event carrying the full metadata of S1; a stale-only memory card; a
     flagged-only memory card; a card that is both; and a stale card whose key
     is the empty string. Report `export_decision_json`'s `evidence_status` for
     one card of each type, and report the sorted members of
     `TRIPLE_REQUIRED_TYPES`.
 G7. TESTS GREEN, THEN RED UNDER MUTATION, AND THE GUARDS UNMOVED. Run
     `python3 -m pytest tests/orchestration/test_decision_evidence.py -q` in the
     PRIMARY checkout at C5 and report the exit code and the count line. Then in
     the disposable worktree of constraint 10, at C5, report the exit code, the
     count line and the number of `^FAILED` lines for: a CONTROL run before any
     mutation; mutation (a), the `status_hash` ref of S2 made unconditional;
     mutation (b), the `review_status` ref of S4 made unconditional; mutation
     (c), `repo_dirty` removed from `TRIPLE_REQUIRED_TYPES`; and a CONTROL run
     after all three restorations, with the worktree's `git status --porcelain`
     empty. Mutations (a) and (b) are applied to
     `packages/orchestration/decision_queue.py` and mutation (c) to
     `packages/orchestration/decision_evidence.py`; before applying each one,
     count its exact byte string IN THAT FILE and report that the count is 1,
     and restore the file byte for byte before the next. Then run
     `tests/orchestration/test_decision_evidence.py`,
     `tests/orchestration/test_decision_inbox.py` and
     `tests/orchestration/test_approval_queue.py` as ONE pytest process in the
     primary checkout and report the exit code, the count line and the number of
     `^FAILED` lines.
 G8. STRUCTURE, CANARY AND THE PR GATE. Run
     `python3 -m pytest tests/cli/test_golden_path.py -q` and report the exit
     code and the count line. Report the path set of `git diff --name-only
     0216c5bb..<C5 sha>` against the paths the Change set lists other than
     `.agent/handoff.md`, as the two residues, both of which must be EMPTY.
     Report that `git diff --stat 0216c5bb..<C5 sha> -- apps/` and the same for
     `-- docs/` are both EMPTY. Report the insertion count of each of C0a
     through C5, that each is single-parent, and that each is under 500. Those
     counts and the `+/-` column of the handback's `## Commits` section are one
     reading written twice: derive both from `git diff --numstat`, compare them
     cell by cell, and report that they agree. Report
     the counts of `^<<<SLICE ` and `^<<<END ` in `.agent/plan.md`,
     `.agent/live_review.md`, `packages/orchestration/decision_queue.py`,
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
its row — the item-status table covering every C and every S exactly once,
the deviations, the verification lines of G1 through G8 and the next steps. It
states that the feature is F032, that R10 is the round, and that this is
SESSION 3, whose first round is R10. Session 1 was R1 through R5 and session 2
was R6 through R9. Ten rounds across three sessions is inside the soft limit of
25 rounds or 7 sessions, so do NOT emit a limit report. The handback has NO
LENGTH CAP, so do not declare, measure or apologise for its length. Its `## Next`
section names Phase 1 rule 1 of docs/agents/self_drive_protocol.md — the
`.agent/STOP` re-read from disk — before anything else, then the Open PR Gate,
then the flight-plan approval and the task decision, the last two producers.
Then push the branch.

<<<SLICE PLANF032R10>>>
# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D6.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R10 opens session 3 with the two producers that cite nothing at all: the
dirty-repo card, whose whole evidence is one run-log event, and the
memory-review card, which names a key and states a reason it never cites. Both
branches are optionless, so each owes exactly one unkeyed outcome. The round
also books the R9 verdict and writes the `Done:` text for `R-0713`, fixed in
code at R9 and open in the record since. Six of the eight producing types are
enforced when it ends.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R9 verdict and `Done: R-0713` | ordered | the record is touched first |
| C3 the repo-dirty triple and its gate entry | ordered | S2 and S3 |
| C4 the memory-review triple and its gate entry | ordered | S4 and S5 |
| C5 the tests, and the two guards C4 falsifies | ordered | S6 and S7 |
| C6 the handback | ordered | |

## Next Steps
1. The flight-plan approval, whose PENDING arm carries `payload["options"]`
   while its RESOLVED arm carries none. The emit gate does not branch on
   status, so enforcing that type needs a ruling on what a resolved card owes.
2. The task decision, whose options come from the escalation record and are
   arbitrary, so its outcomes are built per option rather than written out.
   With it the gate set is complete and T002 ends.
3. T003 card enrichment and the chip deep links, then the integration gate.

## Risks
- Two tests in `tests/orchestration/test_decision_evidence.py` use
  `memory_review` as their example of an UNENFORCED type. C4 makes that false
  and C5 repoints both, so the pair has to land in one round.
- Six types are enforced from this round on, so a later change that regresses
  any of their triples raises instead of rendering. That is the intent.
<<<END PLANF032R10>>>

<<<SLICE LEDGER10>>>
Gate: F032 R9 — the F032 T002d STOP-REASON entry. THE ROUND PASSED. The reviewer re-ran the load-bearing gates itself at `0216c5bb` and reproduced every number the handback reports. TRANSPORT COVERS THREE ARTEFACTS AND IS NAMED AS SUCH: sha256 `80008f17ccd928a18b9530814ab7d805688e53eea89144e5f2ea0a2b6a933a33` over 29489 bytes and 350 lines is EQUAL across the committed `.agent/authored/f032-r9.md` blob at `3dee8a49`, the committed `.agent/last_block.md` blob at `80e3c96f` and the working copy read at `0216c5bb`, and the two committed paths are the SAME git blob. Under docs/agents/self_drive_protocol.md there is no paste relay, so that chain proves the saved copy, its mirror and the working copy agree and says NOTHING about the bytes any prompt carried; this entry claims no more. THE FIX FOR `R-0713` IS THE ONE LINE IT WAS SPECIFIED AS: `safe_summary` now interpolates `_pa_target_path or '?'`, the value R8 already computed for the ref guard directly above, so the placeholder finally shows on an intent that names no file. THE STOP-REASON BRANCH NOW CITES THE RECORD IT COPIES: a `failure` ref for `sr.id` unguarded, a `failure` ref for `sr.reason_code` and a `file` ref for `sr.related_file`, each of the last two emitted only when the value is non-empty — and the second guard is load-bearing rather than defensive, because no arm of `derive_stop_reasons` sets `related_file` at all. ONE UNKEYED OUTCOME, NO `payload`, which is DECISION F032 D3's optionless case applied exactly as R8 applied it to the patch approval: this branch copies the record's own `next_actions`, which are prose instructions rather than option words, so growing an options list would change what the browser renders as answers and amendment A3 puts that out of F032's scope. THE TYPE JOINED THE GATE SET IN THE COMMIT THAT GAVE ITS PRODUCER THE TRIPLE, `e26e95e0`, which is what DECISION F032 D5 requires. THE REVIEWER RAN THREE MUTATIONS IN ITS OWN DISPOSABLE WORKTREE AT `9aa51005`, with `__pycache__` purged and `-B` passed before each, and each exact byte string counted 1 before it was applied: reverting the `R-0713` fix to `pi.get('target_path', '?')` gave exit 1 at `1 failed, 62 passed`; making the `related_file` ref unconditional gave exit 1 at `4 failed, 59 passed`; removing `stop_reason` from `TRIPLE_REQUIRED_TYPES` gave exit 1 at `2 failed, 61 passed`; and the controls before and after all three restorations were a real exit 0 at `63 passed`, with the worktree's `git status --porcelain` empty. The third of those the block did not order and the reviewer added, because a type joining the gate set is the half of DECISION F032 D5 that no other gate pins. NOTHING ELSE MOVED: `ruff check` over both modules exit 0 with the verbatim output `All checks passed!`, the golden-path canary exit 0 at `42 passed`, both residues EMPTY against the seven-path change set, `apps/` and `docs/` both EMPTY, and insertions 350, 192, 21, 4, 9, 54, 176 and 161 across the eight commits, each single-parent and each under 500. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

Done: R-0713 — Resolved at `f0ec4b09`, one line, exactly as the finding specified. `safe_summary` in the patch-approval branch of `packages/orchestration/decision_queue.py` now reads `f"Patch intent for {_pa_target_path or '?'} awaits approval."`, so the fallback fires on the shape `list_patch_intents` actually yields — the key PRESENT and EMPTY — instead of on an absence that producer never emits. The reviewer confirmed both renderings by calling `list_decisions` at that commit: an intent naming no file reads `Patch intent for ? awaits approval.` and one naming `README.md` reads `Patch intent for README.md awaits approval.` Two tests in `tests/orchestration/test_decision_evidence.py` pin the pair, and reverting the expression to `pi.get('target_path', '?')` in a disposable worktree turns exactly one of them red. WHAT THE FAMILY LEAVES BEHIND is now stated once for all three of its members: `R-0711` read one field where two carried the reason, `R-0712` read a key no emitter writes, and `R-0713` guarded on absence where the real shape is present-and-empty. Each was written from an ASSUMED record shape rather than from the record the producer yields, and each was caught only by rendering the card. The counter-measure the remaining producer upgrades carry, and which R10 applies to the two thinnest branches in the queue, is to read the EMITTER and the FIXTURES before ordering a ref: `apps/cli/commands/repo.py` writes seven metadata keys that `_fixture_repo_dirty` does not, and a guard designed against either one alone would have been wrong about the other.
<<<END LEDGER10>>>
