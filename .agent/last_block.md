STEP T004/3 — F272 — round 21 — the operator-facing half of R-0823, and the guard widened to reach it

Base commit for every reading in this block: `5f4f0405`, the round 20 handback commit.
Every separator line below is exactly twenty `=` characters.

====================
Goal
====================

Round 20 repaired the five stale command advertisements in tracked `.py` and
shipped the guard that keeps them repaired. The guard's sweep is `.py`-only, and
the same defect is on disk in two other media the operator actually reads: the
smoke script INVOKES the deleted `remedy job run-loop`, and `docs/system/`
documents it as a live command. Widen the guard to those media and repair what
it finds.

====================
What the widened sweep finds, measured before this block was written
====================

The reviewer imported round 20's shipped `scan_advertised_commands` and ran it
over `git ls-files` listings at the base commit:

    scripts/*.sh                    15 files   88 advertisements   2 unresolved
    docs/system + docs/guides       88 files  318 advertisements   2 unresolved

    scripts/remedy_smoke.sh:1176   remedy job run-loop
    scripts/remedy_smoke.sh:1875   remedy job run-loop
    docs/system/architecture.md:926        remedy job run-loop
    docs/system/core-product-spine-v0.md:36  remedy approval summary

THE SMOKE SCRIPT IS BROKEN, NOT MERELY STALE. Line 1875 is
`remedy job run-loop "${JOB_ID}" --autonomy-level 0 --json | python3 -c "` whose
validator begins `json.load(sys.stdin)`. The command now exits 2 with empty
stdout, so section `12ae` raises rather than reporting. Line 1176 is section
`12h`, which ends `|| true`, so it degrades silently and then checks run-log
events that are never written.

`remedy approval summary` has NEVER existed — measured at the base commit, the
only `approval` commands are `approval.policy-list`, `policy-show`,
`policy-enable`, `policy-disable`, `policy-evaluate` and `policy-grant`. It is
step 7 of the seven-step flow `docs/system/core-product-spine-v0.md` calls the
core product spine. It is not F272's defect and it is repaired here for the same
reason round 20 repaired `remedy guide next`: the guard cannot be a zero-gate
while it stands, and a gate scoped to avoid its own findings protects nothing.

NOT FLAGGED, AND CORRECTLY SO — stated so their survival is not read as an
oversight. `docs/guides/simple-operator-quickstart-v0.md:108` is a MIGRATION
table row, `| job run-loop <id> | mission run ... |`, which documents what the
old command BECAME and must keep naming it. The six `active — job run-loop`
cells in `docs/system/architecture.md`'s event table carry no `remedy ` prefix
and so do not match; they are repaired anyway by P3 below, because they are the
same false claim in the same file.

====================
Bundle
====================

C0a  save this block verbatim to `.agent/authored/f272-r21.md`
C0b  mirror the same bytes to `.agent/last_block.md`
C1   `.agent/plan.md` replaced byte for byte with PLANF272R21
C2   `.agent/live_review.md` — append RECORDR21 (the round 20 PASS gate entry
     and the `Done:` resolving R-0823)
C3   the guard widening and the repairs, in ONE commit, per WIDENSPEC,
     SMOKESPEC and pairs P1 through P4
C4   `.agent/handoff.md` rewritten

====================
Change set — exactly these paths and nothing else
====================

    .agent/authored/f272-r21.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    tests/cli/test_advertised_commands.py
    scripts/remedy_smoke.sh
    docs/system/architecture.md
    docs/system/core-product-spine-v0.md
    .agent/handoff.md

If a measurement forces a path outside this list, APPLY IT AND DECLARE IT in the
handback with the measurement that forced it. Do not weaken a test or an
assertion to stay inside the list.

====================
Constraints
====================

1. This block is applied verbatim. If a slice or a spec is wrong, apply it as
   written and declare the disagreement in the handback; never silently correct
   it.
2. Every authored slice is extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f272-r21.md`, between its `<<<BEGIN NAME>>>` and
   `<<<END NAME>>>` lines. Never retype a slice. A slice is read INCLUSIVE of
   the newline ending its last content line.
3. C0a and C0b are `shutil.copyfile` of one source file.
4. Every one of P1 through P4 is a REWRITE. The containment test was RUN by the
   reviewer at the base commit and answered `TO contains FROM: false` for each;
   each FROM occurs exactly 1x in its file and each TO exactly 0x. The
   post-edit reading is therefore FROM 0x and TO 1x per file.
5. `.agent/prose_slips.md` is NOT in the change set: this round has no reviewer
   slip to record, and round 20's three were appended by round 20's own C3.
6. `.agent/decisions.md` is NOT in the change set. DECISION F272 D13, landed in
   round 20, already rules this class; nothing new is ruled here.
7. Destructive verification runs ONLY inside a disposable `git worktree`, per
   docs/agents/self_drive_protocol.md G5, removed afterwards BY EXACT PATH. The
   primary checkout satisfies `git status --porcelain` empty at every boundary.
8. Read `.agent/STOP` with `os.path.exists` before C0a, before C3 and before
   C4, and report all three readings.
9. The FULL SUITE is NOT ordered this round; the round gate is the scoped set in
   G5. This is a docs-and-script round, and its reach is bounded by the paths in
   the change set.

====================
WIDENSPEC — tests/cli/test_advertised_commands.py, widened
====================

The file's scanner, its three discriminators and its anti-blindness assertion
are UNCHANGED. What changes is the corpus.

W1. Keep `collect_command_advertisements()` as the production-`.py` sweep it is
    today, so nothing that already depends on it moves.

W2. Add a second collector over the OPERATOR-FACING corpus: every tracked `.sh`
    under `scripts/`, and every tracked `.md` under `docs/system/` and
    `docs/guides/`. Enumerate from `git ls-files`, never from a shell glob.

W3. Add ONE test for that corpus, shaped exactly like the existing zero-gate:
    an anti-blindness assertion first (the corpus must yield more than 100
    advertisements; the reviewer measured 88 plus 318 at the base commit, so
    the combined figure clears that floor with room), then the unresolved list
    asserted empty, with a failure message naming every `path:line: remedy
    <group> <sub>`.

W4. The module docstring gains one sentence: the sweep now covers the shell
    scripts and the operator-facing docs, because an operator reads a command
    line from a doc exactly as they read one from a terminal.

W5. THE FILE'S OWN DOCSTRING QUOTES THE STRINGS IT FORBIDS, which the round 20
    handback flagged. That is safe only while the corpus excludes `tests/`.
    Neither collector may reach `tests/`, and W3's test must not be satisfiable
    by narrowing the corpus. State this in a comment beside W2's path list.

====================
SMOKESPEC — scripts/remedy_smoke.sh
====================

Delete section `12h` and section `12ae` in full. Both exist only to exercise
`remedy job run-loop`, which round 19 deleted, and neither has a surviving
emitter: `remedy dev agent-loop` writes `agent_loop_inspected` alone, not the
cycle events 12h validates.

S1. Section `12h` begins at the comment rule line directly ABOVE the line
    `    # 12h. Agent loop run-log schema (Step 68.1 — per-event-type exact schemas)`
    and ends at the last line before the next `_SMOKE_SECTION=` assignment.
    Delete that whole span, its `echo` line, its `remedy job run-loop`
    invocation and its embedded `python3 -c` heredoc included.

S2. Section `12ae` begins at the line `    # Step 68: Autonomy Loop` and ends at
    the last line before the next `_SMOKE_SECTION=` assignment. Delete that
    whole span.

S3. Determine both spans BY READING THE FILE, not by the line numbers above:
    those numbers are the reviewer's reading at the base commit and are given so
    you can confirm you found the right sections, not so you can slice by index.

S4. Nothing else in the script changes. No section is renumbered — the section
    ids are historical labels, and renumbering them would be a rename as its own
    activity, which AGENTS.md Scope Control forbids.

====================
The documentation repairs
====================

P1 and P2 are `docs/system/core-product-spine-v0.md`. P1 replaces a step naming
a command that has never existed; `remedy patch approve <job_id>
<patch_intent_id>` is the measured replacement rather than a chosen one, because
`apps/cli/commands/job.py`'s `_cmd_job_status` already emits exactly that string
as its approval next-action, and `patch.approve` takes a job id, an intent id
and an optional reason. P2 removes the table row for the deleted command.

P3 is `docs/system/architecture.md`. It replaces the CLI bullet and the six
event-table rows in one span, so that the table stops attributing live status to
a deleted command while still naming the events, which still have schemas in
`packages/orchestration/event_schemas.py` and are still emitted by
`run_agent_loop()` — a function no production caller reaches at the base commit
and which DECISION F272 D13 assigns to T004's classic-runner deletion.

P4 corrects the heading directly beneath that table for the same reason.

<<<BEGIN P1 FROM path=docs/system/core-product-spine-v0.md>>>
7. Approve if needed  →  remedy approval summary --json
<<<END P1 FROM>>>
<<<BEGIN P1 TO>>>
7. Approve if needed  →  remedy patch approve <job_id> <patch_intent_id>
<<<END P1 TO>>>

<<<BEGIN P2 FROM path=docs/system/core-product-spine-v0.md>>>
| `job run-loop <id> --json` | Contract-gated autonomy loop | Metadata | No* |
<<<END P2 FROM>>>
<<<BEGIN P2 TO>>>
| `do job-run <id> --json` | Run pending tasks through Builder/Reviewer/Repair | Yes | Yes |
<<<END P2 TO>>>

<<<BEGIN P3 FROM path=docs/system/architecture.md>>>
- `remedy dev agent-loop <job_id>` — inspect-only: derives state, prints summary, writes `agent_loop_inspected` event.
- `remedy job run-loop <job_id>` — execution loop: runs cycles, emits structured events, stops on approval/block/completion.

**Run-log event names:**

| Event | Status | Description |
|-------|--------|-------------|
| `agent_loop_inspected` | active — `dev agent-loop` | Loop state snapshot |
| `agent_loop_started` | active — `job run-loop` | Loop begins |
| `agent_loop_cycle_started` | active — `job run-loop` | Each cycle begins |
| `agent_loop_decision` | active — `job run-loop` | Decision made (run_next_task, needs_planning) |
| `agent_loop_cycle_completed` | active — `job run-loop` | Each cycle ends |
| `agent_loop_paused` | active — `job run-loop` | Loop paused (needs_approval, blocked) |
| `agent_loop_completed` | active — `job run-loop` | Loop finished (all_done, max_cycles_reached) |
<<<END P3 FROM>>>
<<<BEGIN P3 TO>>>
- `remedy dev agent-loop <job_id>` — inspect-only: derives state, prints summary, writes `agent_loop_inspected` event.

The execution loop `remedy job run-loop <job_id>` was DELETED at F272 round 19.
The six cycle events below keep their schemas in
`packages/orchestration/event_schemas.py` and are still emitted by
`agent_loop.run_agent_loop()`, which no production caller reaches; DECISION F272
D13 assigns that function to T004's classic-runner deletion.

**Run-log event names:**

| Event | Status | Description |
|-------|--------|-------------|
| `agent_loop_inspected` | active — `dev agent-loop` | Loop state snapshot |
| `agent_loop_started` | no live emitter | Loop begins |
| `agent_loop_cycle_started` | no live emitter | Each cycle begins |
| `agent_loop_decision` | no live emitter | Decision made (run_next_task, needs_planning) |
| `agent_loop_cycle_completed` | no live emitter | Each cycle ends |
| `agent_loop_paused` | no live emitter | Loop paused (needs_approval, blocked) |
| `agent_loop_completed` | no live emitter | Loop finished (all_done, max_cycles_reached) |
<<<END P3 TO>>>

<<<BEGIN P4 FROM path=docs/system/architecture.md>>>
**`job run-loop` execution events — 10-key metadata schema (exact keyset):**
<<<END P4 FROM>>>
<<<BEGIN P4 TO>>>
**Agent-loop execution events — 10-key metadata schema (exact keyset):**
<<<END P4 TO>>>

====================
Done when — the gates
====================

Run every gate with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, no pipe between the
command and the echo. Report ONE LINE PER GATE in the handback with the
transcripts below it. Every gate runs before C4, the commit that writes the
handback.

G1 TRANSPORT. One digest comparison: `.agent/authored/f272-r21.md` and
   `.agent/last_block.md` share one sha256, one byte length and one line count
   with the file this block was delivered from. Report all three.

G2 THE RECORD, over the C2 append to `.agent/live_review.md`.
   (a) BYTE: report pre_len, pre_sha256, post_len, post_sha256, the terminal
       twelve bytes and trailing-newline run of each,
       `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and `POST_EQUALS_PRE_NL_SLICE`. At
       the base commit the pre-image is 1180176 bytes, sha256
       `a8a4a67b628e6cf2ec9dda440965beaab39a8b0fd099422d6b0a661804c73b3c`.
   (b) STRUCTURAL: strip the single terminal newline, split on blank lines,
       compare the LAST N units against the slice's paragraphs IN ORDER, where
       N is COUNTED BY YOUR SCRIPT from the slice and never taken from this
       block. Report N, units before, units after, `EVERYTHING_BEFORE_UNCHANGED`.
   (c) NEGATIVE CONTROL on the FIRST appended paragraph, in memory only, never
       on disk: flip one byte, require BOTH readers to reject it, then re-read
       the file and confirm it is byte-identical to the real post-image.
   (d) COUNTS before and after, each measured, none adjusted to agree:
           ^- R-\d{4} distinct        307 -> 307
           ^Done: R-\d{4} distinct    249 -> 250
           open set BY DISTINCT ID     58 -> 57
           ^Gate:                      43 -> 44
           ^Gate: F272 R20              0 -> 1
           ^Done: R-0823                0 -> 1
       Report OPEN FINDINGS BY DISTINCT ID with its arithmetic. NO id is minted
       this round; R-0824 stays free.

G3 THE PLAN. `.agent/plan.md` is byte-equal to PLANF272R21. Report its bytes,
   its line count against the AGENTS.md cap of 50, and that `## Goal` and
   `## Next Steps` are both present.

G4 THE WIDENED GUARD IS REAL — the ordered colour, CONTROL FIRST, in a
   disposable worktree detached at C3, never in the primary checkout.
   (i)   control: `python3 -B -m pytest tests/cli/test_advertised_commands.py -q
         -p no:randomly` is EXIT 0. Report the passed count.
   (ii)  revert EXACTLY ONE line: restore P1's TO back to P1's FROM in
         `docs/system/core-product-spine-v0.md`. That byte string occurs exactly
         1x in that file; assert the count is 1 before writing.
   (iii) the same command is now EXIT 1 and the failure names
         `docs/system/core-product-spine-v0.md` AND NO OTHER PATH. Report the
         full unresolved list the assertion printed.
   (iv)  restore, re-run, EXIT 0 again.
   Report the worktree path, that `apps.cli.command_catalog.__file__` resolved
   INSIDE it, the `__pycache__` count before the first run, and the exact
   removal command. Use `python3 -B` throughout.

G5 THE SWEEPS ARE ZERO AND NEITHER IS BLIND, in the PRIMARY checkout at C3.
   Run, serially, and report each exit code and count:
       python3 -B -m pytest tests/cli/test_advertised_commands.py -q -p no:randomly
       python3 -B -m pytest tests/cli/test_product_spine.py -q -p no:randomly
       python3 -B -m pytest tests/test_remedy_smoke_script.py -q -p no:randomly
       python3 -B -m pytest tests/docs/ -q -p no:randomly
       python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
   Separately PRINT, do not assert from this block, the advertisement count each
   collector saw. At the base commit the production-`.py` figure was 738.

G6 THE SHELL STILL PARSES AND THE COMMAND IS GONE.
   `bash -n scripts/remedy_smoke.sh` EXIT 0. Then, over the whole repository
   excluding `.agent/`, `.data/` and `docs/roadmap/`, report the count of the
   string `remedy job run-loop`: it must be 0 in `scripts/` and 0 in
   `docs/system/`. Report the file's line count before and after C3 and the
   number of `_SMOKE_SECTION=` assignments before and after — the latter must
   fall by exactly 2.

G7 RUFF. `python3 -m ruff check tests/cli/test_advertised_commands.py` EXIT 0,
   `All checks passed!`. No other `.py` is touched this round, so no other ruff
   reading is owed.

G8 THE TREE. `git status --porcelain` EMPTY at every commit boundary with the
   real output each time. `git ls-files .remedy-wt` empty. Per-commit insertions
   from `git diff --numstat <parent> <commit>` for C0a through C3 — C4 excluded,
   because a commit cannot count its own insertions while it is being written —
   each under the DECISION F104 D1 cap of 500. The three `.agent/STOP` readings.

====================
Handback
====================

Rewrite `.agent/handoff.md` completely: `SESSION 10 of feature F272 · round 21 ·
rounds so far 21`; the soft-limit reading under amend0906-triage-throughput,
which is 12 sessions and 40 rounds; one sentence of context self-assessment; the
range; a per-commit changed-files table whose `+/-` column comes from `git diff
--numstat` and is compared cell for cell against G8's figures; the item-status
table for C0a through C4; one line per gate with the transcripts below it; every
deviation and assumption; and the next expected action. It has no length cap.

<<<BEGIN PLANF272R21 target=.agent/plan.md>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 20 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001, T002 and T003
are COMPLETE. T004 is under way.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Repair the operator-facing half of R-0823 — the smoke script that invokes the
deleted `job run-loop` and the `docs/system/` pages that document it as live —
and widen the round 20 guard to sweep the shell scripts and those pages, so the
class is caught in every medium an operator reads.

## Next Steps

1. The classic store deletion, which now leads T004 rather than following it.
   Measured at `5f4f0405`: every next-action rail advertising `remedy job
   run-next` — in `cockpit.py`, `timeline.py`, `trust_report.py`,
   `dashboard.py`, `brain_detail.py`, `agent_loop.py` and `autonomy_loop.py` —
   sits in a function typed `job: Job`, the CLASSIC record. None takes a
   `JobPlan`, so none can point at `remedy do job-run`, whose id is a
   16-character JobPlan id. The advertisements therefore cannot move before the
   classic record does, and DECISION F272 D13 forbids deleting a command ahead
   of its advertisements.
2. `job.run-next` and `job.run` die inside that same commit range, with their
   rails. `job.run` is the catalog's only `is_expensive` command and three
   tests pin that, so F114's cost preview needs a carrier named before it goes.
3. `_cmd_job_resume` and `agent_loop.run_agent_loop`, the last production
   caller of `_cmd_run_next_task_local`, die with them per DECISION F272 D13.
4. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- The store deletion is 199 files by `.agent/f272_t004_deletion_inventory.md`,
  72 of them production, so it is many rounds and no single commit holds it.
- A half-performed deletion is the one state the Orchestrator brief says this
  work must not leave behind, so every deletion round ends with the full suite
  green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 10
  and round 21 the feature is inside it and no scope report is owed.
<<<END PLANF272R21>>>

<<<BEGIN RECORDR21 target=.agent/live_review.md mode=append>>>
Gate: F272 R20 — the F272 round 20 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `5f4f0405`. Range `8bcdc4dc`..`5f4f0405`, eight commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with the change set exactly the thirteen ordered paths and nothing else, `git status --porcelain` empty, `git ls-files .remedy-wt` empty, thirteen worktree entries being the primary plus the twelve pre-existing `remedy/job-*`, and per-commit insertions 463, 438, 22, 4, 6, 115 and 74 for C0a through C5, each under the DECISION F104 D1 cap of 500. G1 TRANSPORT IS A REAL CHAIN AND NOT MERELY SELF-CONSISTENT: the reviewer's own scratch original `.remedy-wt/f272-r20-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r20.md` and `.agent/last_block.md` are all 32027 bytes at 463 lines and all hash to `9a48d5ad812eaa278d703be4c29fd416a168d25f3f5e0fc50b3d79d323a9f83f`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces on every reader: `.agent/live_review.md` 1173866 to 1180176, the pre-image a byte-exact prefix, `post == pre + NL + slice` TRUE, N counted from the slice as 2 with units 719 to 721 and the last 2 equal to the slice's paragraphs in order, a byte flipped in the FIRST appended paragraph rejected by BOTH readers with the disk digest unmoved; and all five ordered counts reproduce exactly — registrations 306 to 307, resolutions 249 unchanged, open set BY DISTINCT ID 57 to 58, `^Gate: ` 42 to 43 and `^Gate: F272 R19 ` 0 to 1. G3 THE PROSE FILES: `.agent/plan.md` is 2213 bytes byte-equal to its slice at 45 lines against the cap of 50 with `## Goal` and `## Next Steps` both present, and `.agent/prose_slips.md` satisfies `post == pre + NL + slice` at 146054 to 147269. G4 THE GUARD IS REAL, re-run by the reviewer in its own disposable worktree detached at `a333617b`, zero `__pycache__` directories under it before any run, `python3 -B` throughout, and `apps.cli.command_catalog.__file__` confirmed to resolve INSIDE that worktree so no editable install could shadow it: the ORDERED COLOUR is control-first and reads EXIT 0 at 4 passed, then with P3's single line alone reverted EXIT 1 at 1 failed and 3 passed naming exactly `packages/orchestration/autonomy_readiness.py:315: remedy job run-loop` and no other path, then EXIT 0 at 4 passed restored, with the file byte-identical to C4's afterwards; the worktree was removed by exact path. G5 THE SWEEP: the shipped `collect_command_advertisements` reports 738 advertisements and an EMPTY unresolved list, so the zero-gate is met by a scan that is demonstrably not blind. G6 THE FULL SUITE, in the PRIMARY checkout: EXIT 0 at 19784 passed and 23 skipped with ZERO `FAILED` lines, and the arithmetic closes exactly — the base at `8bcdc4dc` was 19780 passed and an `ast` count gives the new file 4 test functions, so 19780 + 4 = 19784, which is what ran. G7 ruff EXIT 0 `All checks passed!` over the five edited modules and the new test; `tests/docs/` EXIT 0 at 303 passed for the `docs/roadmap/**` change; the canary EXIT 0 at 42 passed. G8 THE TREE holds at every boundary. THE PRODUCTION TEST WAS SPECIFIED, NOT SLICED, and the worker's implementation reproduces GUARDSPEC's own measurements independently: its scanner reports 738 advertisements and exactly the seven occurrences at the five sites at the base, RED at 1 failed and 3 passed, GREEN at 4 passed once the pairs land. THE WORKER DECLARED NO DEVIATION and none was owed; the reviewer read the whole diff and every pair landed byte-exact. ITS FIVE ASSUMPTIONS ARE ACCEPTED AS ASSUMPTIONS, and the fourth is the one worth carrying forward: the guard's own module docstring quotes the strings it forbids, which is safe only while the sweep excludes `tests/`, and the worker flagged it for any future round that widens the corpus — round 21 is that round, and its WIDENSPEC carries the constraint explicitly. The first assumption is also upheld on measurement: reading S1's "followed by" as skip-spaces-then-require is what reproduces the reviewer's own 738 and the exact seven-occurrence failure set, so it is the intended reading rather than a widening.

Done: R-0823 — RESOLVED at F272 round 20, commit `a333617b`, verified by the reviewer at `5f4f0405` by re-running the guard rather than reading it. Five production sites told the operator to run a command that does not exist: `apps/cli/commands/decision.py:292`, `apps/cli/commands/job.py:1598` and `packages/orchestration/autonomy_readiness.py:315` printed `remedy job run-loop`, whose catalog entry and handler round 19 deleted, and `packages/orchestration/model_route_tournament.py:322` and `packages/orchestration/worker_registry.py:717` returned a `remedy guide next` that has never existed. All five now name a command the catalog carries, and `tests/cli/test_advertised_commands.py` sweeps every tracked `.py` under `packages/` and `apps/` and fails on any advertised pair the catalog does not hold — which is exactly the RESOLVED-WHEN this finding was registered with, including its anti-blindness clause, met by an assertion that the scan saw more than 100 advertisements against a real figure of 738. THE REPLACEMENTS WERE MEASURED RATHER THAN CHOSEN: the level-4 readiness hint became `remedy dev agent-loop <job_id>` because that command's handler is the ONLY surviving emitter of an `agent_loop_*` event, which the reviewer confirmed by running the shipped predicate `_has_agent_loop` against the shipped kind `agent_loop_inspected` — True for it, False for an empty list, so the new hint is satisfiable and the predicate is not vacuous; and the two classic-job hints point at `remedy job run` rather than `remedy do job-run` because both sites hold a classic UUID job while `do job-run` takes a 16-character JobPlan id. THE DEFECT'S SECOND MEDIUM IS NOT COVERED BY THIS RESOLUTION and is fixed by round 21 under the ordering constraint that round's block carries: the sweep this finding asked for is `.py`-only, and the same false claim stands in `scripts/remedy_smoke.sh`, which INVOKES the deleted command and pipes its `--json` into a validator, and in `docs/system/architecture.md` and `docs/system/core-product-spine-v0.md`. That is a widening of one defect rather than a second one, so per §3 item 30 no second id is minted and the evidence is recorded here. THE LESSON, which is worth more than the five lines: round 19's deletion gate counted the DOTTED catalog id and the SYMBOL to zero over every tracked `.py`, and both readings were true — a command-deletion gate must sweep the form the OPERATOR types, and DECISION F272 D13 now binds that for the rest of T004.
<<<END RECORDR21>>>
