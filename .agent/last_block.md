STEP CLOSURE 4/5 — F272 — round 29 — register what the self-use run found, and rule closure precondition 1

Base commit for every reading in this block: `f321fefc`, the round 28 handback commit.
Every separator line below is exactly twenty `=` characters.

====================
Goal
====================

ROUND 28's SELF-USE RUN DID ITS JOB, AND WHAT IT FOUND HAS TO BE REGISTERED. The run
consumed SU-012 under the product's own provider — ollama `muse-glimmer:latest`, six real
provider calls, 251.76 seconds — and `describe_self_use_run_defects` answered the empty
tuple. Closure precondition 6 says in terms that an empty tuple "means nothing to
register, not that nothing was checked". The reviewer checked, and the run surfaced three
defects the describer cannot see. THAT BLINDNESS IS ITSELF ONE OF THEM.

THREE IDS ARE MINTED, AND EACH WAS SEARCHED FOR BY DEFECT BEFORE IT WAS MINTED, per §3
item 30 — not merely for a free id. The reviewer searched the 57-strong open set at
`f321fefc` for `describe_self_use_run_defects`, `self_use_findings`, `ollama-legacy`,
`transport mode`, `call lineage is invalid`, `run_manifest_write_failed`,
`manifest corruption`, `complete call coverage`, `budget_exhausted`, `stop_reason` and
`RunState.RUNNING`. R-0784 came back for the first term and is a DIFFERENT defect — a
self-use run that BLOCKED, where the describer DID return two strings — so it is not this
one. Everything under the manifest and budget terms came back empty.

A FOURTH OBSERVATION IS DELIBERATELY NOT GIVEN AN ID, and that is item 30 working as
intended. The run recorded `provider_call_count 6` against `actual_call_count 0`,
`total_tokens 0` and `unmeasured_call_count 6` — six real calls, nothing measured. The
same search found R-0807 (High, OPEN, "THE TOKEN LEDGER RECORDED ONE CALL FOR A REAL RUN
THAT MADE AT LEAST SIX") and R-0753 (Medium, OPEN, the persisted actuals carry no money).
That is the defect the open set already holds, so this round adds its new evidence to the
RECORD ENTRY naming both ids and mints NO fourth id.

CLOSURE PRECONDITION 1 MUST BE RULED ON, NOT STEPPED AROUND. `.agent/review_protocol.md`
scores FAIL for "any Blocker or High finding remains open", and precondition 1 wants every
finding "Resolved or listed as a documented Medium/Low risk". Four High findings are
already open before this round — R-0803, R-0804, R-0806, R-0807 — and R-0827 below makes
five. On a literal reading F272 cannot close; nor could F274, F261 or any other feature,
because those four are booked to F273, which sits far down the STATUS order and cannot be
reached first. That is a deadlock in the spec, and §4 item 7 routes a wrong spec to a
loud, persisted, reversible DECISION rather than to a question. D17SLICE is that ruling.

====================
Bundle
====================

C0a  save this block verbatim to `.agent/authored/f272-r29.md`
C0b  mirror the same bytes to `.agent/last_block.md`
C1   `.agent/plan.md` replaced byte for byte with PLANF272R29
C2   `.agent/live_review.md` — append FINDINGSR29: R-0826, R-0827, R-0828. FINDINGS
     PERSIST FIRST, IN THEIR OWN COMMIT, per planner_reviewer_prompt.md §4 item 4
C3   `.agent/live_review.md` — append RECORDR29, the round 28 PASS gate entry, which also
     carries the R-0807 and R-0753 corroboration that mints no id
C4   `.agent/decisions.md` — append D17SLICE, the closure-precondition-1 ruling
C5   `.agent/prose_slips.md` — append SLIPSR29, one dated line
C6   `.agent/handoff.md` rewritten

====================
Change set — exactly these paths and nothing else
====================

    .agent/authored/f272-r29.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md          (TWO appends, in TWO commits: C2 then C3)
    .agent/decisions.md
    .agent/prose_slips.md
    .agent/handoff.md

NOTHING under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/` changes this round, and
no STATUS line is touched. THIS ROUND REGISTERS DEFECTS AND REPAIRS NONE OF THEM: the three
findings are carried, not fixed, and no production line moves, so no red-proof is ordered
or possible. If a measurement forces a path outside this list, APPLY IT AND DECLARE IT.

====================
Constraints
====================

1. This block is applied verbatim. If a slice is wrong, apply it as written and declare the
   disagreement; never silently correct it.
2. Every authored slice is extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f272-r29.md`, between its `<<<BEGIN NAME>>>` and `<<<END NAME>>>`
   lines, exclusive of both marker lines and INCLUSIVE of the newline ending its last
   content line. This round carries no FROM/TO pair. Never retype a slice.
3. C0a and C0b are `shutil.copyfile` of `.remedy-wt/f272-r29-block.md`.
4. EVERY APPEND IS `post == pre + b"\n" + slice`, and C2's post-image is C3's pre-image —
   two appends to one file in two commits, each proved against the image that precedes IT
   and never against the base. Each target ends in EXACTLY ONE newline at the base commit,
   measured per file: three consecutive newlines at `f321fefc` occur 0 times in
   `.agent/live_review.md`, 1 time in `.agent/prose_slips.md` (offset 39213) and 5 times in
   `.agent/decisions.md` (offsets 411259, 500136, 689970, 715876, 845071). All are
   pre-existing, none is load-bearing, none is repaired here.
5. C2 IS THE FIRST SUBSTANTIVE COMMIT AFTER THE PLAN, because §4 item 4 requires authored
   findings to persist FIRST, in their own commit, so nothing is lost if the session dies.
   C3 must NOT be folded into it: the gate entry is a verdict and the findings are a
   registration, and the round that loses one must not lose the other.
6. THE THREE FINDINGS ARE REGISTRATIONS ONLY. Do not write a `Done:` paragraph for any of
   them, do not write a `Landed:` line, and do not attempt a repair. Their fix clauses bind
   the feature that takes them, not this round.
7. FINDING IDS ARE `R-0826`, `R-0827` AND `R-0828`, in that order, and each occurs EXACTLY
   ONCE as a `^- R-XXXX ` registration when the round ends. At `f321fefc` all three read 0
   as registrations; `R-0826` additionally occurs 7 times in the file as PROSE, in earlier
   entries that say the id is free, and those occurrences are untouched and must not be
   counted as registrations. `R-0829` must still be free at the end.
8. Read `.agent/STOP` with `os.path.exists` before C0a, before C2 and before C6, and report
   all three readings.
9. NO WORKTREE IS CREATED OR REMOVED THIS ROUND. `git worktree list` is 14 entries at the
   base — the primary plus thirteen `remedy/job-*`, the newest being
   `remedy/job-020c1ef366af4f07`, which round 28's product run created and constraint 8 of
   that round retained — and must still be 14 at the end. Do not remove any of them.

====================
Done when — the gates
====================

Run every gate with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, NO PIPE between the command and
the echo. Report ONE LINE PER GATE with the transcripts below it. Every gate runs before
C6, the commit that writes the handback.

G1 TRANSPORT. One digest comparison: `.remedy-wt/f272-r29-block.md` as delivered against
   the committed `.agent/authored/f272-r29.md` and the committed `.agent/last_block.md`.
   Report sha256, byte length and line count for each of the three.

G2 THE FINDINGS APPEND at C2, against the file as it stands at C1.
   (a) BYTE: pre_len, pre_sha256, post_len, post_sha256, the terminal twelve bytes and
       trailing-newline run of each, `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and
       `POST_EQUALS_PRE_NL_SLICE`. At `f321fefc` the pre-image is 1225920 bytes, 2137
       lines, sha256 beginning `495c5cea046dfe0a`.
   (b) STRUCTURAL: strip the single terminal newline, split on blank lines, compare the
       LAST N units against the slice's paragraphs IN ORDER, where N is COUNTED BY YOUR
       SCRIPT from the slice and never taken from this block. Report N, units before, units
       after and `EVERYTHING_BEFORE_UNCHANGED`.
   (c) NEGATIVE CONTROL on the FIRST paragraph the append adds — which is R-0826's, not
       R-0828's — in memory only, never on disk: flip one byte, require BOTH readers to
       reject it, then re-read the file and confirm it is byte-identical to the real
       post-image.
   (d) COUNTS across C2 alone, each measured:
           ^- R-\d{4} distinct        309 -> 312
           ^Done: R-\d{4} distinct    252 -> 252
           open set BY DISTINCT ID     57 ->  60
           ^- R-0826                    0 ->   1
           ^- R-0827                    0 ->   1
           ^- R-0828                    0 ->   1
           ^- R-0829                    0 ->   0
       Report OPEN FINDINGS BY DISTINCT ID with its arithmetic, and report that no
       `^Done: ` line was added.

G3 THE GATE-ENTRY APPEND at C3, against the file as it stands at C2 — NOT against the base.
   Report pre_len, pre_sha256, post_len, post_sha256,
   `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and `POST_EQUALS_PRE_NL_SLICE`, and the counts
   `^Gate:` 51 -> 52 and `^Gate: F272 R28 ` 0 -> 1. Confirm the three registration counts
   are UNCHANGED by C3 at 1, 1 and 1, and that the open set is 60 both before and after it.

G4 THE DECISION RECORD at C4. Report pre_len, pre_sha256, post_len, post_sha256,
   `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and `POST_EQUALS_PRE_NL_SLICE`. At `f321fefc` the
   pre-image is 865296 bytes and 10873 lines. Report `^## DECISION F272 D` 1 -> 2 and
   confirm `^## DECISION F272 D17 ` heads exactly one section. A duplicated D17 is a STOP.

G5 THE TWO PROSE FILES. `.agent/plan.md` is byte-equal to PLANF272R29; report its bytes,
   its line count against the AGENTS.md cap of 50, and that `## Goal` and `## Next Steps`
   are both present. `.agent/prose_slips.md` gets the byte append check only — pre_len
   152214 and pre_lines 567 at `f321fefc`, and `POST_EQUALS_PRE_NL_SLICE` for SLIPSR29.

G6 THE CANARY. In the primary checkout at C5:
       python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
   The reviewer measured 42 passed at exit 0 at `b865f001`. REPORT WHAT YOU MEASURE. No
   `.py` file changes this round, so no ruff reading is owed and none is ordered.

G7 THE TREE. `git status --porcelain` EMPTY at every commit boundary with the real output
   each time. `git ls-files .remedy-wt` empty. `git worktree list` 14 entries, unchanged
   from the base per constraint 9. Per-commit insertions from
   `git diff --numstat <parent> <commit>` for C0a through C5 — C6 excluded, because a
   commit cannot count its own insertions while it is being written — each under the
   DECISION F104 D1 cap of 500. The three `.agent/STOP` readings.

====================
Handback
====================

Rewrite `.agent/handoff.md` completely: `SESSION 12 of feature F272 · round 29 · rounds so
far 29`; the soft-limit reading; one sentence of context self-assessment; the range; a
per-commit changed-files table whose `+/-` column comes from `git diff --numstat` and is
compared cell for cell against G7's figures; the item-status table for C0a through C6; one
line per gate with the transcripts below it; every deviation and assumption. It has no
length cap. State the OPEN FINDINGS COUNT as 60 by distinct id, with its arithmetic, and
name the three ids this round minted — the closure round reads that count from here.

<<<BEGIN PLANF272R29 target=.agent/plan.md>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 28 PASSED except round 2 (premise
corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round 22). T001, T002 and
T003 are COMPLETE; T004's remainder and T005 are F274's, split off in round 26 by DECISION
F272 D16.

## Goal

Close F272 at the self-consistent scope DECISION F272 D16 fixed. Session 12 reached the
soft limit of 12 sessions, so the remaining work is the closure sequence of
`docs/roadmap/STATUS_closure_protocol.md` and no further building.

## Current Step

Round 29: register the three defects round 28's self-use run surfaced and its describer
could not see — R-0826, R-0827, R-0828 — and rule closure precondition 1 as DECISION F272
D17, because five open High findings would otherwise deadlock every feature behind F273.
Nothing is repaired here; the findings are carried.

## Next Steps

1. The evidence job and a FRESH review zip. `base_commit` is the FORK POINT `b18fad57`,
   never `git merge-base`, which differs on this branch and packages BLOCKED_EVIDENCE.
2. Ledger rotation by `scripts/rotate_live_review.py`, as its own commit, after the verdict
   bookings and before the STATUS flip.
3. The closure commit: the STATUS `[x]` line, the README capability sync and SU-012's
   `consumed_by` in the SAME commit, then the PR. The PR is NOT merged this session.

## Risks

- Five open High findings — R-0803, R-0804, R-0806, R-0807 and the new R-0827. The close is
  PASS_WITH_RISKS and names every one with its owner; DECISION F272 D17 rules why that is
  the honest reading rather than a stop.
- `remedy integrity check` PASSES, but its `high_blockers_open` check reports "no open
  blocker/high findings" while five are open. That is the already-open R-0648, and the
  closure states it rather than leaning on it.
- A failing review-zip build is a closure BLOCKER; the round that hits one stops.
<<<END PLANF272R29>>>

<<<BEGIN FINDINGSR29 target=.agent/live_review.md mode=append>>>
- R-0826 — Medium, THE SELF-USE TRACK'S OWN DEFECT REPORTER IS BLIND TO A BUDGET STOP AND TO A FAILED RUN-MANIFEST WRITE, SO CLOSURE PRECONDITION 6's GATE ANSWERED "NOTHING TO REGISTER" FOR A RUN THAT BURNED ITS WHOLE BUDGET AND PUBLISHED NO MANIFEST. Raised by the REVIEWER at F272 round 29 from the run round 28 performed. MEASURED at `f321fefc`: `packages/orchestration/self_use_findings.py` defines `describe_self_use_run_defects(result)` and its body reads exactly two things — `result.error`, and `task.error` for each task. The SU-012 run persisted as job `020c1ef366af4f07` has `error` blank and its single task T001 has `error` blank, so the function answers `()`. Everything that actually went wrong is in fields it never reads: `stop_reason` is `budget_exhausted:max_provider_calls`, `stop_source` is `budget`, `stopped_at` is set, T001 carries `status='pending'` with `final_status='stopped'` and `repair_rounds_used=2`, and `run_manifest_path` is empty because `run_manifest_write_failed` holds a `ManifestError`. THE CONSEQUENCE IS EXACTLY THE ONE THE PRECONDITION EXISTS TO PREVENT: `docs/roadmap/STATUS_closure_protocol.md` precondition 6 requires every string this function returns to be registered before a close, and says an empty tuple "means nothing to register, not that nothing was checked" — but a closing session that trusts the function reads a clean bill for a run that failed. This is a gate over production code shown to be blind, which is what operator amendment amend0827-process-diet rule 2 reserves an id for; it is Medium and not High because no state on disk is wrong and the underlying facts are all persisted and readable. The module's own docstring shows the premise that slipped: it says the runner answers "``JOB_COMPLETED`` or ``JOB_BLOCKED``", and this run answered neither. FIX, BINDING ON THE FEATURE THAT TAKES THIS ID: `describe_self_use_run_defects` also reports, in the job's own words and without summarising, a non-blank `stop_reason` together with `stop_source`, a non-blank `run_manifest_write_failed`, and any task whose `final_status` is not a completed state while its `error` is blank. The red-proof is the persisted plan `020c1ef366af4f07` itself: the repaired function must answer a non-empty tuple for it, and the unrepaired one answers `()`, so the control is a real run rather than a fixture. Searched before minting per §3 item 30: `describe_self_use_run_defects`, `self_use_findings`, `run_manifest_write_failed`, `manifest corruption` and `complete call coverage` over the 57 open findings at `f321fefc`; the only open hit is R-0784, which is a DIFFERENT defect — a self-use run that BLOCKED and for which this same function DID return two strings — so no id was reused and none was duplicated.

- R-0827 — High, NO RUN MANIFEST CAN EVER BE PUBLISHED FOR A RUN ON THE `ollama` PROVIDER, BECAUSE THE MODE THAT PROVIDER STAMPS ON EVERY CALL IS NOT IN THE MANIFEST'S OWN SET OF VALID MODES. Raised by the REVIEWER at F272 round 29 from the run round 28 performed. MEASURED at `f321fefc`, by reading both sides of the contract rather than by inferring one from the other: `packages/orchestration/pingpong_provider.py` stamps `mode="ollama-legacy"` on its prepared input at two call sites, lines 1721 and 1768; `packages/orchestration/run_manifest.py` line 3754 defines `VALID_CALL_MODES = frozenset({"api-structured", "api-legacy", "cli-native", "cli-legacy", "fake"})`, and line 3800 rejects any call whose `mode` is outside it. `ollama-legacy` is not a member — the reviewer imported the constant and printed it, and the set has exactly those five values. The SU-012 run is the demonstration: `run_manifest_write_failed` reads `ManifestError: invalid run manifest (write (bound)): a published stopped reference manifest must have complete call coverage; incomplete coverage is manifest corruption (task T001: call lineage is invalid: call calls/builder/round-01/attempt prepared_input.mode 'ollama-legacy' is not a supported transport mode; task T001: call lineage is invalid: stored sequence 2 != )`, and `run_manifest_path` is empty in consequence. WHY HIGH. This is the proof chain, which is the product's central claim, and it fails for the provider this repository's own `resolve_role_config` returns for both `builder` and `reviewer` — so the default local configuration cannot produce the evidence artefact that every downstream gate reads. It is not merely unreported: the failure is loud and recorded, which is the one thing keeping it from Blocker. FIX, BINDING ON THE FEATURE THAT TAKES THIS ID: decide whether `ollama-legacy` joins `VALID_CALL_MODES` or whether the provider stamps an existing mode, and make the two files agree in ONE commit — a test that pins the provider's stamped mode as a member of `VALID_CALL_MODES` is the guard, because the defect is precisely that no test relates the two. The second clause of the same error, `stored sequence 2 !=`, is part of this id and not a separate one until a measurement shows it independent. Searched before minting per §3 item 30: `ollama-legacy`, `transport mode`, `call lineage is invalid`, `supported transport mode`, `run_manifest_write_failed`, `manifest corruption` and `complete call coverage` over the 57 open findings at `f321fefc`, and every one of those terms came back with no open finding and no resolved one.

- R-0828 — Medium, A JOB STOPPED BY ITS OWN BUDGET IS LEFT RECORDED AS `RUNNING` WITH A BLANK `finished_at`, ALTHOUGH THE VOCABULARY HAS A `STOPPED` STATE AND THE EVIDENCE LAYER TREATS ONLY `COMPLETED` AND `STOPPED` AS TERMINAL. Raised by the REVIEWER at F272 round 29 from the run round 28 performed. MEASURED at `f321fefc`: the SU-012 run, re-read from disk through the shipped `packages.orchestration.pingpong_job.load_job_plan('020c1ef366af4f07')`, has `state = RunState.RUNNING`, `finished_at = ''`, and at the same time `stop_reason = 'budget_exhausted:max_provider_calls'`, `stop_source = 'budget'`, `stopped_at = '2026-09-07T15:03:52.142876+00:00'` and a task whose `final_status` is `'stopped'`. The vocabulary is not missing the state: `packages/core/models.py` declares `RunState.STOPPED = "stopped"` and `packages/orchestration/pingpong_job.py` line 73 binds `JOB_STOPPED = RunState.STOPPED`, while `packages/orchestration/long_run_executor.py` lines 110 to 112 already map `TERMINAL_BUDGET_EXHAUSTED` to `JOB_STOPPED` — so one executor agrees with the vocabulary and the ping-pong path does not. THE CONSEQUENCE IS NOT COSMETIC: `packages/orchestration/job_evidence.py` decides terminality with `getattr(job, "state", "") in (JOB_COMPLETED, JOB_STOPPED)` at lines 2185 and 2288, so a budget-stopped ping-pong job is classified as still running and its evidence handling takes the non-terminal path forever. This is wrong state on disk under `packages/`, which is what amend0827 rule 2 reserves an id for. It is Medium rather than High because the stop IS recorded in four other fields, so no information is lost and a reader who knows to look can recover the truth. FIX, BINDING ON THE FEATURE THAT TAKES THIS ID: the ping-pong run path sets `state` to `JOB_STOPPED` and fills `finished_at` when it stops on budget, deadline or operator request, matching what `long_run_executor` already does; the red-proof runs a job against a `max_provider_calls` budget it must exhaust and asserts the persisted state, and the same persisted plan `020c1ef366af4f07` is the negative control, because it reads `RUNNING` today. Searched before minting per §3 item 30: `budget_exhausted`, `stop_reason`, `RunState.RUNNING`, `finished_at` and `terminal` over the 57 open findings at `f321fefc`; `stop_reason` returned R-0811, which is about bare `remedy do` not attaching a repository and is a different defect, and the rest returned nothing.
<<<END FINDINGSR29>>>

<<<BEGIN RECORDR29 target=.agent/live_review.md mode=append>>>
Gate: F272 R28 — the F272 round 28 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `f321fefc`. THIS IS THE ROUND THAT DISCHARGED CLOSURE PRECONDITION 6. Range `b865f001`..`f321fefc`, eight commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with `git diff --name-only` naming exactly the sixteen declared paths and nothing under `packages/`, `apps/`, `tests/` or `docs/`. G1 TRANSPORT IS A REAL CHAIN: the reviewer's own scratch original `.remedy-wt/f272-r28-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r28.md` and `.agent/last_block.md` are all 22575 bytes at 281 lines and all hash to `79c944de68ea99589234068b62c33aa4591f32efaa1f2364bd7c3e343258685c`; per §3 item 37 that chain covers those artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD: 1220698 to 1225920 bytes, pre-image a byte-exact prefix, `POST_EQUALS_PRE_NL_SLICE` true, structural N counted from the slice as 1 with units 733 to 734 and everything before unchanged, and a byte flipped inside the FIRST appended paragraph rejected by BOTH readers; registrations 309 unchanged, resolutions BY DISTINCT ID 252 unchanged, open set 57 unchanged, `^Gate: ` 50 to 51, `^Gate: F272 R27 ` 0 to 1, `^- R-0826 ` 0 to 0. G3 THE PROSE FILES: the plan is 2075 bytes at 40 lines against the cap of 50 and byte-equal to its slice. G4 THE QUEUE, the gate this precondition turns on: `scripts/self_use_queue.json` went 33722 to 38741 bytes and 11 to 12 items, the appended entry is `SU-012` titled "Address ledger finding R-0445" with provenance `generated (self-use-generator tier 1, ledger scan, R-0445)` and `consumed_by` the EMPTY STRING, `next_self_use_item()` answers SU-012, `pending_self_use_items()` went 0 to 1, `schema_version` is 2 on both sides, the eleven earlier items are a byte-exact prefix so the generator reformatted nothing, and every id is unique and matches `^SU-\d{3}$`. The reviewer independently confirms SU-012 is the ONLY item with a blank `consumed_by`, which is what leaves it available for the closure commit to consume. G5 THE RUN WAS REAL AND THE PROVIDER WAS NOT `fake`: `ExecutionConfig(builder='ollama', builder_source='cli', reviewer='ollama', reviewer_source='cli')` with `provider_versions {'ollama': 'ollama version is 0.32.9'}`, six provider calls in 251.76 seconds against a `max_provider_calls` budget of 6, two repair rounds used, job id `020c1ef366af4f07`. G6 THE SUITES: the four self-use suites exit 0 at 72 passed and the canary exit 0 at 42 passed. G7 THE TREE: porcelain empty at every boundary, `git ls-files .remedy-wt` empty, worktrees 13 to 14 — the new entry being the PRODUCT's own `remedy/job-020c1ef366af4f07`, which the block deliberately retained because a job worktree is product state and not verification scratch — and per-commit insertions 281, 188, 16, 2, 2, 8 and 87 for C0a through C5, every one under the DECISION F104 D1 cap of 500. THE WORKER'S DECLARED DISAGREEMENT WITH CONSTRAINT 7 IS UPHELD AND IT IS THE REVIEWER'S ERROR: the constraint named `JOB_COMPLETED` and `JOB_BLOCKED` as the run's legitimate outcomes, and the run produced NEITHER, stopping on budget with `RunState.RUNNING`. The worker applied the constraint as written, reported the literal state as G5 ordered, and declined to invent a STOP the block had not stated — which is exactly right, and it is recorded as a dated prose-slip line rather than an id because it is the reviewer's prose. THE EMPTY DEFECT TUPLE IS NOT A CLEAN BILL, AND THIS ENTRY SAYS SO: `describe_self_use_run_defects` answered `()`, and closure precondition 6 states in terms that an empty tuple means nothing to register rather than that nothing was checked, so the reviewer checked the run itself and registered R-0826, R-0827 and R-0828 in this round's own C2. ONE FURTHER OBSERVATION IS DELIBERATELY GIVEN NO ID, per §3 item 30: the run recorded `provider_call_count 6` against `actual_call_count 0`, `total_tokens 0` and `unmeasured_call_count 6`, so six real calls measured nothing — and that is the defect R-0807 (High, open, "THE TOKEN LEDGER RECORDED ONE CALL FOR A REAL RUN THAT MADE AT LEAST SIX") and R-0753 (Medium, open, the persisted actuals carry no money) already hold. This run is fresh corroboration of BOTH from a real local-provider job, recorded here against those two ids so that whoever repairs them has a second reproduction, and no fourth id was minted for it.
<<<END RECORDR29>>>

<<<BEGIN D17SLICE target=.agent/decisions.md mode=append>>>
## DECISION F272 D17 — F272 closes PASS_WITH_RISKS with five open High findings, each named with its owner, because the literal precondition deadlocks the roadmap (2026-09-07)

CONTEXT. `docs/roadmap/STATUS_closure_protocol.md` precondition 1 asks that every `R-XXXX` finding be "Resolved or listed as a documented Medium/Low risk", and `.agent/review_protocol.md` scores FAIL for "any Blocker or High finding remains open". At F272's closure five High findings are open: R-0803, R-0804, R-0806 and R-0807, all four registered on 2026-09-05 by operator order amend0905-testlog from the operator's own `tests.md` run and all four booked to F273's T001 by the 2026-09-06 triage; and R-0827, registered by this feature's round 29 from its own self-use run. On a literal reading F272 cannot close.

THE LITERAL READING DEADLOCKS THE ROADMAP, AND THAT IS THE ACTUAL PROBLEM. The four inherited Highs are owned by F273, "Findings paydown v1". F273 sits in the STATUS order after F271, and Rule A5 proposes the first unchecked feature, which after this close is F274. So F273 cannot be reached until F274, F261, F266, F268, F269, F270 and F271 have closed — and under the literal reading NONE of them may close while those four are open, because none of them owns the fix. The rule as written therefore forbids every close until a feature nobody may start has finished. F260 met the same wall on 2026-09-06 and closed PASS_WITH_RISKS with those same four open; this decision states the reasoning that close left implicit rather than quietly repeating it.

CHOSEN. F272 CLOSES WITH LIVE REVIEW `PASS_WITH_RISKS`, and its closure paragraph NAMES ALL FIVE High findings with the feature that owns each. The four inherited ones are F273's, by the 2026-09-06 triage. The three this feature registered — R-0826, R-0827 and R-0828 — are also F273's, and no feature file needs editing to say so, because F273's own "Goal & Done" already defines its scope as the triage set "plus anything registered after 2026-09-06", which these are by construction. The closure additionally states that `remedy integrity check` PASSES while its `high_blockers_open` check reports "no open blocker/high findings" — which is FALSE and is the already-open R-0648 — so the close rests on the named list above and NOT on that check's word.

WHAT THIS DECISION DOES NOT DO. It does not weaken the severity scale, does not re-grade any finding to Medium to fit, and does not touch `.agent/review_protocol.md`. R-0827 is recorded High on its merits: it breaks run-manifest publication for the provider this repository's own role config returns. A rule that would be satisfied by re-grading is a rule being gamed, and the honest move is to close against a stated list and let the operator see it.

ALTERNATIVES CONSIDERED. Mark F272 `[!] blocked` — rejected: nothing is blocked, three task slices are complete and green, the full suite passes at 19786, and `[!]` would misdescribe a feature that delivered them while doing nothing to advance F273. Re-grade R-0827 to Medium so the count reads four instead of five — rejected as gaming the scale; it would also not help, because four is still not zero. Repair the five Highs inside F272 — rejected: they are another feature's registered scope, repairing them here is the scope drift AGENTS.md forbids, and R-0827's own fix requires a ruling on whether `ollama-legacy` joins `VALID_CALL_MODES` or the provider changes what it stamps. Reorder F273 to the front of the STATUS order — rejected: that is a roadmap edit, and AGENTS.md forbids editing `docs/roadmap/ROADMAP.md` without an explicit operator request, while amend0906-split-placement fixes F274's position directly after its parent.

CONSEQUENCE. Every future closure faces this same wall until F273 runs, and this decision is the standing answer: name the open Highs and their owner, state that the integrity check's high-blocker reading is vacuous per R-0648, and close. The operator who disagrees reverses it here. REVERSE by deleting this section, at which point F272's close must either wait for F273 or be re-argued from precondition 1's literal text.
<<<END D17SLICE>>>

<<<BEGIN SLIPSR29 target=.agent/prose_slips.md mode=append>>>
2026-09-07, F272 round 28 — the block's constraint 7 stated that `JOB_COMPLETED` and `JOB_BLOCKED` are both legitimate outcomes of the self-use run "and neither is a failure of this round", and the run produced NEITHER: it stopped on its own `max_provider_calls` budget with `RunState.RUNNING`, `finished_at` blank and its task still pending. The constraint was copied from the premise in `packages/orchestration/self_use_findings.py`'s docstring, which says the runner answers one of those two, instead of from the runner's own budget-stop path — and that premise turned out to be a product defect, now registered as R-0828. A constraint enumerating the outcomes a call may return is read against the code that RETURNS them, not against a neighbouring module's prose about it; where the enumeration is not certain, order the worker to report the literal value and say that any value is acceptable.
<<<END SLIPSR29>>>
