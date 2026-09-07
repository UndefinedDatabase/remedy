STEP T004/5 — F272 — round 23 — the rename left two silent readers behind, and a standing guard for the class

Base commit for every reading in this block: `67515ab77f0d6a9103cdb4c521182ead37663590`, the round 22 session-close commit.
Every separator line below is exactly twenty `=` characters.

====================
Goal
====================

F272 round 9 renamed `JobPlan.status` to `JobPlan.state`. DECISION F272 D7 ruled
that rename's site set is MEASURED by running the suites against a raising
`status` property, because `.status` is polymorphic in this repository. That
method is sound and it has exactly one blind spot: a read that names the
attribute as a STRING and supplies a default. `getattr(job, "status", "")`
raises nothing when the field is gone — it answers with the default — so the
probe stayed green while two production guards silently stopped working.

Both survivors were found at the base commit and both were proved by RUNNING the
shipped code, not by reading it:

    apps/cli/commands/do_cmd.py:1456
        F018's refusal of budget flags on a STOPPED job. The comparison became
        `"" == "stopped"`, so the refusal never fired: `remedy do job-run
        --max-cost-usd 5.0` on a stopped job RE-RAN IT under the new limits and
        printed "Cost recorded to the ledger", which is the exact override that
        guard exists to prevent.

    packages/orchestration/job_evidence.py:1494
        `_linked_job_summary` reported `status: "unknown"` for every linked job.
        Its own docstring reserves `unknown` for a job that is UNAVAILABLE, and
        the same summary reported `source: "persisted_job_state"` beside it — a
        document that contradicts itself in two adjacent keys.

This round repairs both, pins each with a behaviour test, and ships the standing
scan that makes the whole CLASS visible instead of these two instances. The
class guard is the half worth more than the two lines: a probe proves a spelling
raises, and only a scan proves a spelling is ABSENT.

====================
What was measured before this block was written
====================

Every reading below was taken by the reviewer at the base commit, and the
production change was APPLIED AND RUN in a disposable worktree before a line of
this block was authored.

1. THE CLASS IS EXACTLY TWO SITES. All 20 `getattr(<name>, "status", ...)` sites
   under `packages/` and `apps/` were resolved to their receiver. Eighteen read a
   `TaskEntry`, an argparse namespace, a budget inspection, a `TestRunRecord`, an
   HTTP response or a promotion attempt — all of which still HAVE a `status`.
   Two read a `JobPlan`, and those two are the ones repaired here.

2. THE ORDERED COLOUR, in a disposable worktree at the base commit with the two
   test artifacts copied in and the production files UNTOUCHED:
   EXIT 1, 3 failed, 14 passed. With both repairs applied: EXIT 0, 17 passed.
   The red is OBSERVED — the defect is its own mutation, nothing was invented.

3. NOTHING ELSE MOVES. With both repairs applied and no test added,
   `tests/orchestration/` is EXIT 0 at 12855 passed and 10 skipped in a
   worktree, the single failure being `test_vitest_passes`, the known absent
   `apps/ui/node_modules` artifact; `tests/cli/` is EXIT 0 at 1545 passed. In the
   PRIMARY checkout at the base commit `tests/orchestration/` is EXIT 0 at 12856
   passed and 10 skipped, which is that worktree reading plus the vitest test.

4. RUFF was run over all four changed files with the repository's own
   configuration, and it caught an `F541` in the new guard's assertion message,
   which is fixed in the artifact this block ships.

====================
Bundle
====================

C0a  save this block verbatim to `.agent/authored/f272-r23.md`
C0b  mirror the same bytes to `.agent/last_block.md`
C1   `.agent/plan.md` replaced byte for byte with PLANF272R23
C2   `.agent/live_review.md` — append RECORDR23 (the round 22 PASS gate entry,
     owed by amend0827 rule 1, and the R-0825 registration). FINDINGS PERSIST
     FIRST, before the repair.
C3   `.agent/prose_slips.md` — append SLIPSR23, the two dated lines round 22's
     handback records as owed by this round's first commits
C4   THE REPAIR, one commit: pairs P1 and P2, plus both test artifacts
C5   `.agent/live_review.md` — append DONER23, resolving R-0825
C6   `.agent/handoff.md` rewritten

====================
Change set — exactly these paths and nothing else
====================

    .agent/authored/f272-r23.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    apps/cli/commands/do_cmd.py
    packages/orchestration/job_evidence.py
    tests/orchestration/test_job_state_field.py
    tests/orchestration/test_job_plan_state_reads.py
    .agent/handoff.md

Nothing under `docs/`, `scripts/` or `apps/ui/` changes this round, and no
catalog entry, command or handler is deleted: this round repairs a regression
this feature introduced, ahead of the deletions the plan's Next Steps stage.
If a measurement forces a path outside this list, APPLY IT AND DECLARE IT.

====================
Constraints
====================

1. This block is applied verbatim. If a slice is wrong, apply it as written and
   declare the disagreement; never silently correct it.
2. Every authored slice is extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f272-r23.md`, between its `<<<BEGIN NAME>>>` and
   `<<<END NAME>>>` lines. Never retype a slice. A slice is read INCLUSIVE of
   the newline ending its last content line.
3. C0a and C0b are `shutil.copyfile` of `.remedy-wt/f272-r23-block.md`.
4. THE TEST ARTIFACTS ARE `shutil.copyfile`, NEVER TEXT EXTRACTION, because
   a whole Python file copied by digest is provable in one reading while a
   re-typed one is not. The reviewer wrote both, ran both, and linted both:

       .remedy-wt/f272-r23-new-guard.py   -> tests/orchestration/test_job_plan_state_reads.py
           sha256 573be0549248c8a7535d9bb2cd6e3ca68d32a31fd3c82dbad564cead2ff3bbf7
           6473 bytes, 155 lines. This file is NEW; it does not exist at the base.

       .remedy-wt/f272-r23-state-field.py -> tests/orchestration/test_job_state_field.py
           sha256 69e13d0d5e37156fece0d2979a3411072e356484d66852ec8a3569a8af8374f3
           8135 bytes, 169 lines. This REPLACES the existing 5812-byte, 119-line
           file. The replacement adds `import pytest`, adds one test class of two
           tests, and changes NOTHING else — `git diff` must show additions only
           plus the import line, and if it shows any other deletion, STOP and
           declare it.

5. P1 and P2 are both REWRITES. The containment test was RUN by the reviewer at
   the base commit and answered `TO contains FROM: false` for each; each FROM
   occurs exactly 1x in its target and each TO exactly 0x. The post-edit reading
   is FROM 0x, TO 1x, per pair.
6. C2 and C5 are TWO SEPARATE APPENDS to `.agent/live_review.md`, in that order,
   with C3 and C4 between them. Each is proved against its OWN pre-image. C2 must
   precede C4: §4 item 4 requires findings to persist before the repair, and
   DONER23 states a fact about C4's landed change, so it must follow it.
7. DONER23 names no SHA for the change it describes, because that commit does not
   exist when this block is written; it names constraint 6, which fixes the order
   — the §3 item 20 carve-out for a claim about the round's OWN commits.
8. Read `.agent/STOP` with `os.path.exists` before C0a, before C4 and before C6,
   and report all three readings.
9. THE ONLY DISPOSABLE WORKTREE THIS ROUND NEEDS IS G4(i)'s, and it is created at
   the BASE commit, not at HEAD, because the red must be measured with the tests
   present and the repairs ABSENT. Remove it by EXACT PATH, never by glob, and
   confirm `git worktree list` afterwards. The primary checkout satisfies
   `git status --porcelain` == empty at every commit boundary.
10. STATED SO THIS BLOCK DOES NOT REPEAT R-0824. The new guard's corpus is
    tracked `.py` under `packages/` and `apps/` ONLY. No TO in this block writes
    a matching read into that corpus: P1's TO writes `_existing.state`, P2's TO
    writes `getattr(_state, "value", _state)`, and `_state` is not bound from
    `load_job_plan`. The two FROMs DO contain the forbidden shape and are being
    REMOVED, which is the point. This block's own bytes land under `.agent/`,
    which the guard never reads. Any later round that widens that corpus to
    `.agent/` must re-read the landed record first, because it is append-only.

====================
The repair
====================

<<<BEGIN P1 FROM path=apps/cli/commands/do_cmd.py>>>
        from packages.orchestration.pingpong_job import load_job_plan
        _existing = load_job_plan(job_id)
        if _existing is not None and getattr(_existing, "status", "") == "stopped":
<<<END P1 FROM>>>
<<<BEGIN P1 TO>>>
        from packages.orchestration.pingpong_job import JOB_STOPPED, load_job_plan
        _existing = load_job_plan(job_id)
        if _existing is not None and _existing.state == JOB_STOPPED:
<<<END P1 TO>>>

<<<BEGIN P2 FROM path=packages/orchestration/job_evidence.py>>>
    status = str(getattr(j, "status", "") or "") or "unknown"
<<<END P2 FROM>>>
<<<BEGIN P2 TO>>>
    _state = getattr(j, "state", "")
    status = str(getattr(_state, "value", _state) or "") or "unknown"
<<<END P2 TO>>>

P2's TO is the idiom this repository already uses for the same job at
`packages/orchestration/job_evidence.py:2198` and
`packages/orchestration/run_manifest.py:6509`, both read at the base commit. It
is spelled that way rather than as `j.state.value` because `str(RunState.STOPPED)`
is `'RunState.STOPPED'` on this interpreter while `.value` is `'stopped'` — the
rendering trap DECISION F272 D6 records.

====================
Done when — the gates
====================

Run every gate with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, no pipe between the
command and the echo. Report ONE LINE PER GATE with the transcripts below it.
Every gate runs before C6, the commit that writes the handback. G4 ADDITIONALLY
RUNS BEFORE C5: DONER23 states G4's outcome, and an authored slice may claim what
a gate showed only when the gate precedes the commit writing it (§3 item 31).
G2's C5 half and G7 are the only readings that necessarily follow C5.

G1 TRANSPORT. One digest comparison per artifact, over every artifact this block
   copies: the committed `.agent/authored/f272-r23.md` and `.agent/last_block.md`
   against the file this block was delivered from, and each test artifact against
   the sha256 and byte length constraint 4 states for it. Report sha256, byte
   length and line count for every one, and report how many you compared.

G2 THE RECORD, over BOTH appends, each against its OWN pre-image.
   (a) BYTE, twice: for C2 and again for C5 report pre_len, pre_sha256, post_len,
       post_sha256, the terminal twelve bytes and trailing-newline run of each,
       `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and `POST_EQUALS_PRE_NL_SLICE`. At the
       base commit the C2 pre-image is 1195379 bytes and its sha256 is
       `88040b630cc1a85df824001c22d4a5736124d4a6e991c28829bf7f800b8efcb8`.
   (b) STRUCTURAL, twice: strip the single terminal newline, split on `\n{2,}`,
       compare the LAST N units against that slice's paragraphs IN ORDER, where N
       is COUNTED BY YOUR SCRIPT from the slice and never taken from this block.
       Report N, units before, units after and `EVERYTHING_BEFORE_UNCHANGED`.
   (c) NEGATIVE CONTROL on the FIRST paragraph appended by C2, in memory only,
       never on disk: flip one byte, require BOTH readers to reject it, then
       re-read the file and confirm it is byte-identical to the real post-image.
   (d) COUNTS across the whole round, each measured, none adjusted to agree:
           ^- R-\d{4} distinct        308 -> 309
           ^Done: R-\d{4} distinct    251 -> 252
           open set BY DISTINCT ID     57 -> 57
           ^Gate:                      45 -> 46
           ^Gate: F272 R22              0 -> 1
           ^- R-0825                    0 -> 1
           ^Done: R-0825                0 -> 1
       Report OPEN FINDINGS BY DISTINCT ID with its arithmetic. Resolutions are
       counted BY DISTINCT ID and not by line: 253 `Done:` LINES carry 251
       distinct ids at the base commit, because two ids each carry a
       two-paragraph resolution. The open set is UNCHANGED at 57 because this
       round both mints and resolves R-0825; R-0826 stays free.

G3 THE TWO PROSE FILES. `.agent/plan.md` is byte-equal to PLANF272R23; report its
   bytes, its line count against the AGENTS.md cap of 50, and that `## Goal` and
   `## Next Steps` are both present. `.agent/prose_slips.md` gets the byte
   append check only — pre_len 147269 at the base commit, and
   `POST_EQUALS_PRE_NL_SLICE` for SLIPSR23. Report the line count it gains.

G4 THE ORDERED COLOUR, on the SHIPPED tests, control beside mutation.
   (i)  In a disposable worktree at the BASE commit, `shutil.copyfile` ONLY the
        two test artifacts in, leaving `do_cmd.py` and `job_evidence.py` at their
        base bytes; purge every `__pycache__` under the worktree; then run, from
        the worktree root:
            python3 -B -m pytest tests/orchestration/test_job_state_field.py \
                tests/orchestration/test_job_plan_state_reads.py -q -p no:randomly
        It must be EXIT 1 with EXACTLY these three node ids failing and no
        others, and 14 passed:
            tests/orchestration/test_job_state_field.py::TestTheRenameLeftNoSilentReaderBehind::test_budget_flags_are_refused_on_a_stopped_job
            tests/orchestration/test_job_state_field.py::TestTheRenameLeftNoSilentReaderBehind::test_a_linked_job_that_loads_reports_its_real_state
            tests/orchestration/test_job_plan_state_reads.py::TestNoRetiredJobPlanStateReads::test_no_production_site_reads_the_retired_status_off_a_job_plan
        Report the guard's own failure message in full: it must name
        `apps/cli/commands/do_cmd.py:1456` and
        `packages/orchestration/job_evidence.py:1494` AND NO OTHER SITE.
   (ii) In the PRIMARY checkout at C4, the same command must be EXIT 0 at 17
        passed. Report the node ids from `--collect-only` so the two runs are
        demonstrably over the same tests.
   Then remove the worktree by exact path and report `git worktree list`.

G5 NOTHING ELSE MOVED. In the PRIMARY checkout at C4, run serially and report
   each exit code and count:
       python3 -B -m pytest tests/orchestration/ -q -p no:randomly
       python3 -B -m pytest tests/cli/test_do_cmd_cli_path.py -q -p no:randomly
       python3 -B -m pytest tests/cli/test_do_cmd_pingpong_budget.py -q -p no:randomly
       python3 -B -m pytest tests/docs/ -q -p no:randomly
       python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
   The reviewer measured `tests/orchestration/` at the base commit in the primary
   checkout as EXIT 0 with 12856 passed and 10 skipped. The EXPECTED reading at
   C4 is EXIT 0 with 12861 passed and 10 skipped: 12856 plus the five tests this
   round adds, being three in the new guard file and two in the replaced one.
   REPORT THE NUMBER YOU MEASURE. If it differs from 12861, that difference is a
   deviation to declare, not a number to adjust — EXIT 0 is the assertion, the
   count is the reading.

G6 RUFF, one invocation over every changed `.py` file, with the repository's own
   configuration and no `--isolated`:
       python3 -m ruff check apps/cli/commands/do_cmd.py \
           packages/orchestration/job_evidence.py \
           tests/orchestration/test_job_state_field.py \
           tests/orchestration/test_job_plan_state_reads.py
   It must be EXIT 0. The reviewer ran this exact command line over the exact
   bytes this block ships and it printed `All checks passed!`.

G7 THE TREE. `git status --porcelain` EMPTY at every commit boundary with the
   real output each time. `git ls-files .remedy-wt` empty. Per-commit insertions
   from `git diff --numstat <parent> <commit>` for C0a through C5 — C6 excluded,
   because a commit cannot count its own insertions while it is being written —
   each under the DECISION F104 D1 cap of 500. The three `.agent/STOP` readings.

====================
Handback
====================

Rewrite `.agent/handoff.md` completely: `SESSION 11 of feature F272 · round 23 ·
rounds so far 23`; the soft-limit reading under amend0906-triage-throughput,
which is 12 sessions and 40 rounds; one sentence of context self-assessment; the
range; a per-commit changed-files table whose `+/-` column comes from `git diff
--numstat` and is compared cell for cell against G7's figures; the item-status
table for C0a through C6; one line per gate with the transcripts below it; every
deviation and assumption; and the next expected action. It has no length cap.

<<<BEGIN PLANF272R23 target=.agent/plan.md>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 22 PASSED except round 2
(premise corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round
22). T001, T002 and T003 are COMPLETE. T004 is under way.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Repair R-0825: the round 9 rename of `JobPlan.status` to `state` left two
production guards reading the retired name through `getattr` with a default,
which answers silently rather than raising, so DECISION F272 D7's probe was
blind to them. Both are fixed, each pinned by a behaviour test, and a standing
scan now makes the class visible.

## Next Steps

1. Name F114's cost-preview carrier BEFORE `job.run` goes. Measured at
   `67515ab7`: `apps/cli/commands/job.py:726` is the ONLY call site of
   `confirm_cost_preview` in the product and it sits inside the handler being
   deleted, so the capability is lost silently unless `do.job-run` inherits it.
   `do.job-run` carries neither `is_expensive` nor `--yes`, and wiring the helper
   as-is would exit 2 on every non-tty run, so this needs a DECISION.
2. Delete `job.run-next` and `job.run` with their handlers and their sixteen
   advertisement sites. MEASURED at `67515ab7`: the store migration is NOT a
   prerequisite. DECISION F272 D13 requires a command's advertisements to DIE
   with it rather than be repointed, and rounds 20 through 22 established that
   shape for `job run-loop`. The classic runner is one connected component, so
   `_cmd_run_next_task_local`, `_cmd_job_run_cycles`, `_cmd_job_resume` and
   `agent_loop.run_agent_loop` fall together.
3. The classic store deletion: 199 files by
   `.agent/f272_t004_deletion_inventory.md`, staged in groups.
4. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- The store deletion is 199 files, 72 of them production, so it is many rounds
  and no single commit holds it.
- A half-performed deletion is the state the Orchestrator brief forbids, so every
  deletion round ends with the full suite green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 11
  and round 23 the feature is inside it and no scope report is owed.
<<<END PLANF272R23>>>

<<<BEGIN RECORDR23 target=.agent/live_review.md mode=append>>>
Gate: F272 R22 — the F272 round 22 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `b926992b`. Range `3ca66aac`..`b926992b`, seven commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5. The change set is exactly the six ordered paths and nothing else — `git diff --stat` names `.agent/authored/f272-r22.md`, `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and `docs/system/architecture.md` — and nothing under `tests/`, `packages/`, `apps/` or `scripts/` moved, which is the constraint that mattered most: THE GUARD WAS NOT EDITED. G1 TRANSPORT IS A REAL CHAIN AND NOT MERELY SELF-CONSISTENT: the reviewer's own scratch original `.remedy-wt/f272-r22-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r22.md` and `.agent/last_block.md` are all 22595 bytes at 277 lines and all hash to `13d10059a62be82131c8d5ea90f2a1fe419c8aa490f8a8b60c78d599942ad73b`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces on both appends: `.agent/live_review.md` 1186986 to 1193650 to 1195379, each proved against its own pre-image, and all seven ordered counts reproduce exactly — registrations 307 to 308, resolutions 250 to 251 BY DISTINCT ID, open set BY DISTINCT ID 57 unchanged, `^Gate: ` 44 to 45, `^Gate: F272 R21 ` 0 to 1, `^- R-0824 ` 0 to 1 and `^Done: R-0824 ` 0 to 1; the open set is unchanged because that round both minted and resolved the id, and the arithmetic closes at 308 minus 251 equals 57. G3 THE PLAN is 49 lines against the AGENTS.md cap of 50 and byte-equal to its slice. G4 THE ORDERED COLOUR IS OBSERVED, NOT MANUFACTURED, which is the strongest form that gate takes: the red existed on disk at `3ca66aac` before the round began — EXIT 1 with an unresolved list of exactly one entry, `docs/system/architecture.md:927: remedy job run-loop` — and at C3 the same node id is EXIT 0 at 5 passed. No mutation was invented, because the defect itself was the mutation. G5 and G6 were re-run by the reviewer as one serial invocation: 613 passed at EXIT 0 across `tests/cli/test_advertised_commands.py`, `tests/cli/test_product_spine.py`, `tests/test_remedy_smoke_script.py`, `tests/docs/` and `tests/cli/test_golden_path.py`, and the exact string `remedy job run-loop` counts 0 in `docs/system/` and 0 in `scripts/`. G7 THE TREE: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, and every per-commit insertion under the DECISION F104 D1 cap of 500 at a maximum of 277. THE REPAIR IS THE RIGHT ONE AND WAS VERIFIED BEFORE IT WAS ORDERED: the reviewer ran the SHIPPED `scan_advertised_commands` over P1's TO before emission and it yields ZERO advertisements, which is the check whose absence caused the round 21 failure, run this time against the widened corpus rather than the old one. THE WORKER'S DEVIATIONS ARE ACCEPTED AND ITS ONE DECLARED PROSE INACCURACY SPENDS NOTHING: deviation 1 is not a deviation but an honest arithmetic note, the operator-facing collector's `seen` falling 404 to 403 because the deleted string was itself one of those 404 matches, with both collectors staying far above their anti-blindness floors; and the note that the handback says "see the push transcript below" where no such transcript exists is correct, declared, and self-healing, since that file is rewritten every round, so under amend0827 rule 2 it earns no id and no round.

- R-0825 — Medium, THE ROUND 9 RENAME LEFT TWO PRODUCTION GUARDS READING THE RETIRED `status` SPELLING THROUGH A `getattr` DEFAULT, AND BOTH STOPPED WORKING SILENTLY. F272 round 9 renamed `JobPlan.status` to `state` and DECISION F272 D7 measured that rename's site set by running the suites against a RAISING `status` property, which is the only method that can see a polymorphic attribute. It is blind to exactly one shape: a read that names the attribute as a STRING and supplies a default. `getattr(job, "status", "")` raises nothing once the field is gone — it answers with the default — so the probe converged green with these two still on disk. MEASURED at `67515ab77f0d6a9103cdb4c521182ead37663590` by RUNNING the shipped code, never by reading it. FIRST, `apps/cli/commands/do_cmd.py:1456` carries F018's refusal of budget flags on a STOPPED job; with the dead read the comparison is `"" == "stopped"`, so calling the shipped `_cmd_do_job_run` with `max_cost_usd="5.0"` against a saved `JobPlan(state="stopped")` DID NOT RAISE `SystemExit`, ran the job, and printed "Cost recorded to the ledger" — the exact silent override that guard exists to prevent, and the F018 rule that changing a stopped job's limits requires a Decision answer is unenforced on the product's main runner. SECOND, `packages/orchestration/job_evidence.py:1494` in `_linked_job_summary` reports `status: "unknown"` for every linked job; running it against a saved `JobPlan(state="completed")` returns `{'job_id': '0123456789abcdee', 'provider_call_count': None, 'source': 'persisted_job_state', 'status': 'unknown'}`, so the document contradicts itself in two adjacent keys and the function's own docstring, which reserves `unknown` for a job that is UNAVAILABLE. THE CLASS WAS BOUNDED BEFORE THE ID WAS MINTED: all 20 `getattr(<name>, "status", ...)` sites under `packages/` and `apps/` were resolved to their receiver, and the other eighteen read a `TaskEntry`, an argparse namespace, a context-budget inspection, a `TestRunRecord`, an HTTP response or a promotion attempt, every one of which still HAS a `status`. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE MINTING, per §3 item 30, by grepping `.agent/live_review.md` for `getattr(_existing`, `_linked_job_summary`, `do_cmd.py:1456` and `budget limits cannot be changed`; no open finding describes it. R-0820 is the nearest neighbour and is NOT this defect: it records a static predicate under-selecting sites that read the LIVE name `state` and render it wrongly, while this is sites that read the RETIRED name `status` and get a default. WHY MEDIUM: two guards, both silent, neither crashing, and one of them on the path an operator uses to re-run a stopped job under new cost limits — real product effect under `apps/` and `packages/`, caught by no test because no test ever pinned either guard. RESOLVED WHEN both sites read `state`, a behaviour test pins each so the guard's FIRING is proved rather than its spelling, and a standing scan over tracked `.py` under `packages/` and `apps/` reports zero reads of the retired name off a value bound from `load_job_plan`.
<<<END RECORDR23>>>

<<<BEGIN SLIPSR23 target=.agent/prose_slips.md mode=append>>>
2026-09-07, F272 round 21 — SMOKESPEC's S1 and S2 bounded each deleted section as ending at "the last line before the next `_SMOKE_SECTION=` assignment", which swallows the FOLLOWING section's banner comment and contradicts the same spec's S4 and its own "delete section in full"; the worker measured the conflict and used the banner-to-banner reading, which is the one that satisfies both sentences. A span ordered for deletion is bounded by the anchor that OPENS the next unit, never by the assignment inside it.

2026-09-07, F272 round 21 — the block's change set omitted `tests/test_remedy_smoke_script.py` while ordering the deletion of the two smoke sections four of its tests pin by text, so the worker had to leave the declared change set to keep the suite green; `agent_loop` and `agent_loop_task_exit` both reach zero occurrences in the script, so at least two of those deletions were forced. Before ordering a section deleted, grep the suite for tests that assert that section's text.
<<<END SLIPSR23>>>

<<<BEGIN DONER23 target=.agent/live_review.md mode=append>>>
Done: R-0825 — RESOLVED at F272 round 23 by the commit this block's constraint 6 fixes as C4, the only commit of this round that touches `apps/cli/commands/do_cmd.py`, `packages/orchestration/job_evidence.py` or either test file. BOTH SITES NOW READ `state`. `do_cmd.py` compares `_existing.state == JOB_STOPPED` against the imported constant rather than a string literal, so the comparison cannot drift from the enum again; `job_evidence.py` uses `str(getattr(_state, "value", _state) or "")`, which is the idiom the same module already uses at line 2198 and `packages/orchestration/run_manifest.py` at 6509, and it is spelled that way rather than as `j.state.value` because `str(RunState.STOPPED)` renders `'RunState.STOPPED'` on this interpreter while `.value` renders `'stopped'` — the trap DECISION F272 D6 records. THE PROOF IS BEHAVIOURAL AND NOT A SPELLING CHECK, which is the half of this resolution worth more than the two lines. `tests/orchestration/test_job_state_field.py` gains two tests that drive the SHIPPED handler and the SHIPPED summary against a saved record and assert that the guard FIRES and that the summary names the real state; a scan can only ever prove a spelling is absent, and a guard that is spelled correctly and still never fires is exactly what this finding was. THE STANDING SCAN IS THE CLASS COUNTER-MEASURE. `tests/orchestration/test_job_plan_state_reads.py` parses every tracked `.py` under `packages/` and `apps/` with `ast` — enumerated from `git ls-files` and never from a shell glob, per DECISION F272 D2 — finds the locals bound from `load_job_plan(...)` in each function scope, and fails on any read of `status` off one of them, whether spelled as an attribute or as a `getattr` string. It ships with its own anti-blindness pair: one test requires the corpus to exceed 300 files so a collapsed scan cannot pass for the wrong reason, and one feeds it a synthetic source holding the defect and requires it to be seen, so the scan cannot be vacuously empty. THE ORDERED COLOUR WAS OBSERVED RATHER THAN MANUFACTURED: with the two test files present at the base commit and the production files untouched, the three named tests are the ONLY failures, and the guard's message names exactly `apps/cli/commands/do_cmd.py:1456` and `packages/orchestration/job_evidence.py:1494`. THE LESSON, and it is a reading of DECISION F272 D7 rather than a new rule: a raising-property probe measures the sites that EXECUTE the attribute, so it is complete for reads that raise and blind to reads that carry their own default. A rename of a widely read field therefore owes a second, static sweep for the retired name specifically — not to find the sites the probe found, but to find the ones it CANNOT.
<<<END DONER23>>>
