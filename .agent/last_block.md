STEP T004/6 — F272 — round 24 — the T004 staging ruling, measured rather than estimated

Base commit for every reading in this block: `81b2dc86`, the round 23 handback commit.
Every separator line below is exactly twenty `=` characters.

====================
Goal
====================

`.agent/f272_t004_deletion_inventory.md` measured WHAT references the classic job
store — 199 files — and closed by saying that "the division of T004 into rounds,
the order those rounds take, and which files travel together in a commit are the
NEXT BLOCK'S JOB". Six rounds later nothing has answered it, and round 23's
session had to re-derive the whole graph from scratch before it could choose a
round at all. This round writes the answer down.

THREE THINGS ARE SETTLED HERE, each from a reading taken at the base commit:

1. TWELVE of the 72 production consumers are on T005's cluster deletion list, so
   porting them is work the deletion round throws away. T004's real remaining
   size is 60 production files, not 72, and not the headline 199.
2. THE SIXTEEN `remedy job run-next` ADVERTISEMENTS ARE NOT BLOCKED BY THE STORE.
   Six of the eight modules carrying them never open the classic store; they are
   handed a `Job` and render it. T004 therefore stages BY CALLER, not by module.
3. `job.run-next` CANNOT DIE THE WAY `job.run-loop` DID, and the round 23 plan's
   Next Step 2 is corrected for saying it could. Every surviving `run-loop` site
   was PROSE describing history; every `run-next` site is LIVE OPERATOR GUIDANCE
   printed under "Run the next pending task:". Rewording those would leave a
   cockpit that tells the operator to continue and then does not say how.

This is a MEASUREMENT round in the shape round 18 established when it committed
the deletion inventory beside DECISION F272 D12. It is not a bookkeeping round
under amend0827 rule 1: its change set carries a new ruling in
`docs/roadmap/features/T2_F272.md` and a new measurement file, beside the verdict
booking that any round of this session would have carried anyway.

====================
What was measured before this block was written
====================

Every figure below was computed by the reviewer at `81b2dc86` in the primary
checkout, by cross-referencing the stored 199-file list in
`.agent/f272_t004_deletion_inventory.md` against the 24-module cluster list in
`docs/roadmap/features/T2_F260.md`'s Design section, and by reading the eight
rail modules directly.

    production consumers of the classic store   72
    also on T005's cluster list (die anyway)    12
    must MIGRATE                                60
    test consumers                             127

    rails that ARE classic-store consumers       2   (agent_loop, long_run_executor)
    rails that are NOT                           6

    rail -> cluster coupling: worker_recommend is reached by dashboard,
    agent_loop and autonomy_loop, and by no other rail.

The staging artifact this round commits carries all of it verbatim, including the
twelve file names and the eight per-rail readings.

====================
Bundle
====================

C0a  save this block verbatim to `.agent/authored/f272-r24.md`
C0b  mirror the same bytes to `.agent/last_block.md`
C1   `.agent/plan.md` replaced byte for byte with PLANF272R24
C2   `.agent/live_review.md` — append RECORDR24, the round 23 PASS gate entry
     owed by amend0827 rule 1. No finding is minted this round.
C3   `.agent/prose_slips.md` — append SLIPSR24, the one dated line round 23's
     worker declared and correctly declined to append on its own initiative
C4   `.agent/f272_t004_staging.md` — the measurement file, by `shutil.copyfile`
C5   `docs/roadmap/features/T2_F272.md` — append D14SLICE, the ruling
C6   `.agent/handoff.md` rewritten

====================
Change set — exactly these paths and nothing else
====================

    .agent/authored/f272-r24.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/f272_t004_staging.md
    docs/roadmap/features/T2_F272.md
    .agent/handoff.md

NOTHING under `packages/`, `apps/`, `tests/` or `scripts/` changes this round.
This round rules how the next rounds are staged; it moves no production line, so
no red-proof and no mutation is ordered or possible. If a measurement forces a
path outside this list, APPLY IT AND DECLARE IT.

====================
Constraints
====================

1. This block is applied verbatim. If a slice is wrong, apply it as written and
   declare the disagreement; never silently correct it.
2. Every authored slice is extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f272-r24.md`, between its `<<<BEGIN NAME>>>` and
   `<<<END NAME>>>` lines. Never retype a slice. A slice is read INCLUSIVE of
   the newline ending its last content line.
3. C0a and C0b are `shutil.copyfile` of `.remedy-wt/f272-r24-block.md`.
4. C4 IS `shutil.copyfile`, NEVER TEXT EXTRACTION:

       .remedy-wt/f272-r24-staging.md -> .agent/f272_t004_staging.md
           sha256 25ed0b5a1fc1180e4339e28b95bec986b9f51ccdc946d5a7f56de48e4d7ff526
           5921 bytes, 120 lines. This file is NEW; it does not exist at the base.

5. C5 IS AN APPEND to `docs/roadmap/features/T2_F272.md` and never a rewrite.
   That file is 52485 bytes and 736 lines at the base commit, ends in exactly one
   newline, and contains ZERO occurrences of three consecutive newlines, so a
   single blank line is its only section separator.
6. THIS ROUND MINTS NO FINDING ID. Round 23 PASSED; the one inaccuracy its worker
   declared is the reviewer's own block prose and damaged nothing on disk, so
   under amend0827 rule 2 it is a dated `.agent/prose_slips.md` line and never an
   id. `R-0826` must still be free when the round ends.
7. Read `.agent/STOP` with `os.path.exists` before C0a, before C5 and before C6,
   and report all three readings.
8. NO WORKTREE IS NEEDED OR PERMITTED THIS ROUND. Nothing destructive is ordered:
   no production file changes, so there is no colour to prove. The primary
   checkout satisfies `git status --porcelain` == empty at every commit boundary.
9. THE DOCS GATE APPLIES because the change set includes `docs/roadmap/**`:
   `tests/docs/` runs this round, per the verification tier 5 rule in
   docs/agents/planner_reviewer_prompt.md §3.

====================
Done when — the gates
====================

Run every gate with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, no pipe between the
command and the echo. Report ONE LINE PER GATE with the transcripts below it.
Every gate runs before C6, the commit that writes the handback.

G1 TRANSPORT. One digest comparison per artifact, over every artifact this block
   copies: the committed `.agent/authored/f272-r24.md` and `.agent/last_block.md`
   against the file this block was delivered from, and `.agent/f272_t004_staging.md`
   against the sha256 and byte length constraint 4 states. Report sha256, byte
   length and line count for every one, and report how many you compared.

G2 THE RECORD, over the single append at C2, against its own pre-image.
   (a) BYTE: report pre_len, pre_sha256, post_len, post_sha256, the terminal
       twelve bytes and trailing-newline run of each,
       `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and `POST_EQUALS_PRE_NL_SLICE`. At the
       base commit the pre-image is 1204799 bytes and its sha256 is
       `0a3287c979d7ebc5` in its first sixteen hex digits.
   (b) STRUCTURAL: strip the single terminal newline, split on `\n{2,}`, compare
       the LAST N units against the slice's paragraphs IN ORDER, where N is
       COUNTED BY YOUR SCRIPT from the slice and never taken from this block.
       Report N, units before, units after and `EVERYTHING_BEFORE_UNCHANGED`.
   (c) NEGATIVE CONTROL on the FIRST paragraph the append adds, in memory only,
       never on disk: flip one byte, require BOTH readers to reject it, then
       re-read the file and confirm it is byte-identical to the real post-image.
   (d) COUNTS, each measured, none adjusted to agree:
           ^- R-\d{4} distinct        309 -> 309
           ^Done: R-\d{4} distinct    252 -> 252
           open set BY DISTINCT ID     57 ->  57
           ^Gate:                      46 ->  47
           ^Gate: F272 R23              0 ->   1
           ^- R-0826                    0 ->   0
       Report OPEN FINDINGS BY DISTINCT ID with its arithmetic. Registrations and
       resolutions are BOTH unchanged because this round mints and resolves
       nothing; only the gate entry is added.

G3 THE TWO PROSE FILES. `.agent/plan.md` is byte-equal to PLANF272R24; report its
   bytes, its line count against the AGENTS.md cap of 50, and that `## Goal` and
   `## Next Steps` are both present. `.agent/prose_slips.md` gets the byte append
   check only — pre_len 148270 at the base commit, and `POST_EQUALS_PRE_NL_SLICE`
   for SLIPSR24. Report the line count it gains.

G4 THE FEATURE FILE. For C5 report pre_len, pre_sha256, post_len, post_sha256,
   `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and `POST_EQUALS_PRE_NL_SLICE`. Then report
   the count of `^### DECISION F272 D` headings before and after — it is 13 at the
   base commit — and confirm that each of `D1` through `D14` heads exactly one
   section, by listing the heading line of every one. A duplicated or skipped
   number is a STOP, not a note.

G5 NOTHING ELSE MOVED, and the docs gate. In the primary checkout at C5, run
   serially and report each exit code and count:
       python3 -B -m pytest tests/docs/ -q -p no:randomly
       python3 -B -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly
       python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
   The reviewer measured all three, WITH THIS ROUND'S D14 APPEND ALREADY APPLIED
   in a disposable worktree, at 303 for `tests/docs/`, 30 for the roadmap index
   and 42 for the canary. REPORT THE NUMBER YOU MEASURE for each. No `.py` file
   changes this round, so no ruff reading is owed and none is ordered.

G6 THE TREE. `git status --porcelain` EMPTY at every commit boundary with the
   real output each time. `git ls-files .remedy-wt` empty. `git worktree list`
   unchanged from the base, which is the primary plus the twelve pre-existing
   `remedy/job-*` entries. Per-commit insertions from
   `git diff --numstat <parent> <commit>` for C0a through C5 — C6 excluded,
   because a commit cannot count its own insertions while it is being written —
   each under the DECISION F104 D1 cap of 500. The three `.agent/STOP` readings.

====================
Handback
====================

Rewrite `.agent/handoff.md` completely: `SESSION 11 of feature F272 · round 24 ·
rounds so far 24`; the soft-limit reading under amend0906-triage-throughput,
which is 12 sessions and 40 rounds; one sentence of context self-assessment; the
range; a per-commit changed-files table whose `+/-` column comes from `git diff
--numstat` and is compared cell for cell against G6's figures; the item-status
table for C0a through C6; one line per gate with the transcripts below it; every
deviation and assumption; and the next expected action. It has no length cap.

<<<BEGIN PLANF272R24 target=.agent/plan.md>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 23 PASSED except round 2
(premise corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round
22). T001, T002 and T003 are COMPLETE. T004 is under way.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Settle how T004 is staged, which the deletion inventory deliberately left open
and which round 23's session had to re-derive from scratch. DECISION F272 D14
and `.agent/f272_t004_staging.md` record it: 60 production files migrate rather
than 72, the staging is BY CALLER, and `job.run-next` dies with the rail modules
rather than ahead of them.

## Next Steps

1. Migrate the classic-store consumers that feed the next-action rails, by
   caller, one consumer per commit range where the diff allows. Six of the eight
   rail modules never open the store; what blocks them is the record type their
   callers hand them.
2. Delete `job.run-next` and its sixteen advertisements in the commit range that
   migrates the last module advertising it, per DECISION F272 D13 and D14.
3. Name F114's cost-preview carrier BEFORE `job.run` goes. Measured at
   `67515ab7`: `apps/cli/commands/job.py:726` is the ONLY call site of
   `confirm_cost_preview` in the product and it sits inside the handler being
   deleted. `do.job-run` carries neither `is_expensive` nor `--yes`, and wiring
   the helper as-is would exit 2 on every non-tty run, so this needs a DECISION.
4. T005, the reachability test and the cluster deletion, which is never split.
   The twelve cluster-bound store consumers are NOT migrated; they wait for it.

## Risks

- 60 production and 127 test files still migrate. That does not fit the rounds
  F272 has left, so the session that reaches the soft limit executes the
  amend0905 split-and-close default from the scope report D14's figures supply.
- A half-performed deletion is the state the Orchestrator brief forbids, so every
  deletion round ends with the full suite green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 11
  and round 24 the feature is inside it and no scope report is owed yet.
<<<END PLANF272R24>>>

<<<BEGIN RECORDR24 target=.agent/live_review.md mode=append>>>
Gate: F272 R23 — the F272 round 23 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `81b2dc86`. Range `67515ab7`..`81b2dc86`, eight commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6. `git diff --stat` names exactly the ten declared paths and nothing else. G1 TRANSPORT IS A REAL CHAIN AND NOT MERELY SELF-CONSISTENT: the reviewer's own scratch original `.remedy-wt/f272-r23-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r23.md` and `.agent/last_block.md` are all 30290 bytes at 367 lines and all hash to `4463fbcc8c9cf39bc51056ccb43e9c6be9449f16686e6ddc4058c3c250c44a0f`; both test artefacts also match the reviewer's own pre-delegation originals byte for byte, at `573be054…` for the guard and `69e13d0d…` for the replaced file. Per §3 item 37 that chain covers those artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces on both appends: 1195379 to 1202061 to 1204799, each proved a byte-exact prefix of its successor, and every ordered count reproduces — registrations 308 to 309, resolutions BY DISTINCT ID 251 to 252 against 253 to 254 LINES, open set BY DISTINCT ID 57 unchanged, `^Gate: ` 45 to 46, `^Gate: F272 R22 ` 0 to 1, `^- R-0825 ` 0 to 1, `^Done: R-0825 ` 0 to 1, and R-0826 still free. G3 THE PLAN is 2592 bytes at 49 lines against the cap of 50 and byte-equal to its slice. G4 THE ORDERED COLOUR WAS REPRODUCED INDEPENDENTLY IN THE REVIEWER'S OWN DISPOSABLE WORKTREE AT THE BASE COMMIT, with only the two test artefacts copied in and both production files left at their base bytes: EXIT 1 at 3 failed and 14 passed, the failures being EXACTLY the three ordered node ids and no others, and the guard's message naming EXACTLY `apps/cli/commands/do_cmd.py:1456` and `packages/orchestration/job_evidence.py:1494` and no other site. In the primary checkout at the head the same selection is EXIT 0 at 17 passed. The worktree was removed by exact path. THE RED IS OBSERVED RATHER THAN MANUFACTURED — the defect was its own mutation — which is the strongest form this gate takes. G5 NOTHING ELSE MOVED: `tests/orchestration/` is EXIT 0 at 12861 passed and 10 skipped against the reviewer's OWN base measurement of 12856 passed and 10 skipped, a rise of exactly the five tests this round adds and nothing else; the two `do_cmd` CLI files, `tests/docs/` and the canary run EXIT 0 at 360 passed together. G6 ruff is EXIT 0 at `All checks passed!` over the four changed `.py` files with the repository's own configuration. G7 THE TREE: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, per-commit insertions at a maximum of 367, under the DECISION F104 D1 cap of 500. THE REPAIR IS BEHAVIOURAL AND THE PROOF IS BEHAVIOURAL, which is what this finding needed: a scan can only show that a spelling is absent, and the defect was a guard that was spelled correctly and never fired. THE WORKER'S CONDUCT IS UPHELD IN FULL AND ITS SECOND DEVIATION IS THE ROUND'S MOST VALUABLE OUTPUT. It found that this block's own measurement note 3 says `tests/orchestration/` is "EXIT 0 at 12855 passed and 10 skipped in a worktree, the single failure being `test_vitest_passes`", and a run with a failure exits 1, so the two clauses cannot describe one reading; the true worktree reading was EXIT 1 with that one known `apps/ui/node_modules` artefact failing. The worker applied nothing from that note, correctly identified it as reviewer prose that reached no file, and — correctly — DECLINED to append a third line to a `.agent/prose_slips.md` slice this block had already fixed, rather than editing the reviewer's ordered slice on its own initiative. That is exactly the discipline constraint 1 asks for, and the line it declined to write is written by round 24 instead. Its remaining deviations are accepted: pushing after C5 and again after C6, because a handback cannot transcribe a push of itself, which is the round 22 slip it deliberately avoided; and taking the `--collect-only` reading in the primary checkout rather than re-adding the worktree, which is sound because both files are byte-identical in the two trees by sha256 and the base run's 3 failed plus 14 passed accounts for all 17.
<<<END RECORDR24>>>

<<<BEGIN SLIPSR24 target=.agent/prose_slips.md mode=append>>>
2026-09-07, F272 round 23 — the block's measurement note 3 read "`tests/orchestration/` is EXIT 0 at 12855 passed and 10 skipped in a worktree, the single failure being `test_vitest_passes`"; a run with a failure exits 1, so the two clauses cannot describe one reading, and the true worktree reading was EXIT 1 with that one known `apps/ui/node_modules` artefact failing. The worker found it, applied nothing from it and declined to append a line to a slice the block had already fixed. When a reading is quoted with its exit code, quote the code the run actually returned rather than the colour the round wanted.
<<<END SLIPSR24>>>

<<<BEGIN D14SLICE target=docs/roadmap/features/T2_F272.md mode=append>>>
### DECISION F272 D14 (2026-09-07, F272 round 24) — T004 is staged BY CALLER, the twelve cluster-bound consumers are never migrated, and `job.run-next` dies WITH the rails rather than ahead of them

CONTEXT. `.agent/f272_t004_deletion_inventory.md` measured T004's blast radius at 199 files and closed by ruling that "the division of T004 into rounds, the order those rounds take, and which files travel together in a commit are the NEXT BLOCK'S JOB". No block took that job. Six rounds later the session opening round 23 had to re-derive the entire consumer graph from scratch before it could choose a round at all, which is the cost this decision exists to stop paying. The numbers below were computed at `81b2dc86` and are recorded in full in `.agent/f272_t004_staging.md`, which this round commits beside this ruling.

CHOSEN, IN THREE PARTS, EACH FROM A MEASUREMENT.

FIRST — THE TWELVE CLUSTER-BOUND CONSUMERS ARE NEVER MIGRATED. Cross-referencing the inventory's 72 production consumers against the 24-module cluster list in `docs/roadmap/features/T2_F260.md`'s Design section gives twelve files on both: `builder_routing.py`, `candidate_quality.py`, `dogfood_run.py`, `external_builder_sandbox.py`, `local_candidate_generator.py`, `overnight_executor.py`, `overnight_mission.py`, `overnight_readiness.py`, `provider_trust.py`, `provider_trust_verification.py`, `repair_loop_v2.py` and `review_bundle.py`. Porting any of them onto the unified record is work T005 throws away. They keep their classic-store imports until T005 deletes them, and no round spends a line on them. T004's real remaining size is therefore 60 production files beside the 127 under `tests/`, and that is the figure a scope report uses rather than the headline 199.

SECOND — THE STAGING IS BY CALLER, NOT BY MODULE. The eight modules carrying the sixteen `remedy job run-next` advertisements were each checked against the store inventory, and SIX OF THE EIGHT never open the classic store at all: `cockpit.py`, `timeline.py`, `trust_report.py`, `dashboard.py`, `brain_detail.py` and `autonomy_loop.py`. Only `agent_loop.py` and `long_run_executor.py` do. The other six are handed a `Job` by their callers and render it, so what blocks them is the RECORD TYPE their callers pass and not a store they never touch. A round therefore takes a classic-store CONSUMER, moves it to `load_job_plan`, and adapts every renderer it feeds inside the same commit range — which is also why the file-by-file order the inventory lists is not itself a plan. Their coupling to the cluster is almost nil and does not obstruct this: `worker_recommend` is reached by `dashboard`, `agent_loop` and `autonomy_loop` and by no other rail, and those three lose that call in T005 rather than having it ported now.

THIRD — `job.run-next` DIES WITH THE RAILS, AND THE ROUND 23 PLAN IS CORRECTED. That plan's Next Step 2 said the store migration is "NOT a prerequisite" for deleting `job.run-next`, reasoning from the `job.run-loop` precedent of rounds 20 through 22. That reasoning holds only for advertisements that are PROSE. Every surviving `run-loop` site was a sentence describing history — one in `docs/system/architecture.md`, one migration-table row under `docs/guides/` — and rewording it cost nothing. None of the sixteen `run-next` sites is prose: each is LIVE OPERATOR GUIDANCE printed under a heading like "Run the next pending task:", produced inside a function holding a classic job. Read at `81b2dc86`, `cockpit._derive_next_action` is typed `(job: Job, signals)` and branches on `job.tasks` and `RunState.PENDING`, and `trust_report`, `brain_detail`, `dashboard` and `autonomy_loop` do the same. Rewording those to avoid naming a command would leave a cockpit that tells the operator to continue and then does not say how, which is a product regression rather than a repair. So DECISION F272 D13's rule that a command's advertisements die in its own commit is satisfied the other way round: the COMMAND waits for the rails, and the rails move with the migration.

NOT CHANGED BY THIS RULING. T005 stays LAST and is never split, exactly as the Orchestrator brief requires: twelve files is a 17 percent reduction of T004 and nowhere near enough to justify breaking that brief's one hard rule. DECISION F260 D5's placement of the resolver collapse in the same commit range as the store deletion is untouched, as is D13's ordering rule itself, which this decision applies rather than amends.

ALTERNATIVES CONSIDERED. Deleting the cluster first so T004 shrinks — rejected on the measurement: it buys twelve files and costs the brief's only hard prohibition. Migrating file-by-file down the inventory's list — rejected: the list is alphabetical within its buckets and a renderer's caller commonly sits in the other bucket, so that order guarantees a half-migrated pair in almost every round. Rewording the sixteen rails now so `job.run-next` can go early — rejected above, on what the rails actually print. Leaving the staging unwritten and deciding it per round — rejected because that is the status quo, and it has now cost two sessions the same re-derivation.

CONSEQUENCE. The next round starts from a determined shape instead of a graph walk, and `.agent/f272_t004_staging.md` carries the twelve names, the eight per-rail readings and the 72/12/60 arithmetic so no later round re-measures them. REVERSE by deleting this section and that file, at which point T004's staging returns to being undecided and the next session re-derives it a third time.
<<<END D14SLICE>>>
