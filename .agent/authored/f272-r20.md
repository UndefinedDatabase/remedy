STEP T004/2 — F272 — round 20 — the stale-advertisement repair and the guard that ends the class

Base commit for every reading in this block: `8bcdc4dce06271f949e35522b7aee135fc6b4273`.
Every separator line below is exactly twenty `=` characters.

====================
Goal
====================

Round 19 deleted the `job run-loop` command surface and left three production
strings still telling the operator to run it. Repair those, repair the two
`remedy guide next` strings the same measurement found, and ship the guard test
that makes this class impossible for the rest of T004 — every remaining T004
round deletes a command, and every one of them would otherwise leak the same
defect. Then record the ruling that fixes the ORDER of the remaining work.

====================
Why this round exists, and why it is not a bookkeeping round
====================

Measured by the reviewer at the base commit, before this block was written, by
running the shipped `apps/cli/command_catalog.py` against every tracked `.py`
under `packages/` and `apps/`: 738 strings of the form `remedy <group> <sub>`
are advertised to the operator, and SEVEN OCCURRENCES AT FIVE SITES name a
command that does not exist in the catalog. Three are round 19's debris. Two
predate it and were never noticed.

    apps/cli/commands/decision.py:292                    remedy job run-loop
    apps/cli/commands/job.py:1598                        remedy job run-loop
    packages/orchestration/autonomy_readiness.py:315     remedy job run-loop
    packages/orchestration/model_route_tournament.py:322 remedy guide next
    packages/orchestration/worker_registry.py:717        remedy guide next

`guide.next` has never existed; the only `guide` command is `guide.job`,
measured at the base commit. AGENTS.md Scope Control says "Replacing is
deleting" and that a closure leaving the old mechanism alive beside the new one
is not a closure. A command line printed for an operator IS the mechanism's
surviving surface, so this repair is inside T004 rather than beside it.

The round ships production code and a new guard test. It is not the pure
bookkeeping round amend0827 rule 1 forbids.

====================
Bundle
====================

C0a  save this block verbatim to `.agent/authored/f272-r20.md`
C0b  mirror the same bytes to `.agent/last_block.md`
C1   `.agent/plan.md` replaced byte for byte with PLANF272R20
C2   `.agent/live_review.md` — append RECORDR20 (the round 19 PASS gate entry
     and the R-0823 registration). Findings persist FIRST.
C3   `.agent/prose_slips.md` — append SLIPSR20
C4   the guard test and the five repairs, in ONE commit, per GUARDSPEC and
     pairs P1 through P5
C5   `docs/roadmap/features/T2_F272.md` — append DECISIONR20
C6   `.agent/handoff.md` rewritten

====================
Change set — exactly these paths and nothing else
====================

    .agent/authored/f272-r20.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    tests/cli/test_advertised_commands.py          (NEW FILE)
    apps/cli/commands/decision.py
    apps/cli/commands/job.py
    packages/orchestration/autonomy_readiness.py
    packages/orchestration/model_route_tournament.py
    packages/orchestration/worker_registry.py
    docs/roadmap/features/T2_F272.md
    .agent/handoff.md

If a measurement forces a path outside this list, APPLY IT AND DECLARE IT in the
handback with the measurement that forced it, exactly as round 19 did — do not
weaken a test to stay inside the list.

====================
Constraints
====================

1. This block is applied verbatim. If a slice is wrong, apply it as written and
   declare the disagreement in the handback; never silently correct it.
2. Every authored slice is extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f272-r20.md`, between its `<<<BEGIN NAME>>>` and
   `<<<END NAME>>>` lines. Never retype a slice. A slice is read INCLUSIVE of
   the newline ending its last content line.
3. C0a and C0b are `shutil.copyfile` of one source file. Not a rewrite.
4. Every one of P1 through P5 is a REWRITE. The containment test was RUN by the
   reviewer at the base commit and its output was `TO contains FROM: false` for
   each; each FROM occurs exactly 1x in its file and each TO exactly 0x, both
   measured at the base commit. So the post-edit reading is FROM 0x and TO 1x
   per file, and that reading is attainable.
5. The production code of C4's guard test is DESCRIBED by GUARDSPEC, not sliced.
   Write it in this repository's idiom; GUARDSPEC fixes the behaviour, the file
   path and the assertions, not the bytes.
6. `.agent/decisions.md` is NOT in the change set. DECISION F272 D13 goes into
   the feature file, where D1 through D12 already live.
7. Destructive verification — the G4 revert — runs ONLY inside a disposable
   `git worktree`, per docs/agents/self_drive_protocol.md G5. Remove it
   afterwards BY EXACT PATH. The primary checkout satisfies
   `git status --porcelain` empty at every commit boundary.
8. Read `.agent/STOP` with `os.path.exists` before C0a, before C4 and before
   C6, and report all three readings.
9. Purge every `__pycache__` under a worktree before running anything in it and
   use `python3 -B`. Confirm inside the worktree that
   `apps.cli.command_catalog.__file__` resolves INSIDE that worktree before
   trusting any colour from it.
10. The FULL SUITE runs in the PRIMARY CHECKOUT, never in a worktree: a fresh
    worktree has no `apps/ui/node_modules` and fails about ten tests for that
    reason alone. This is round 19's own measured lesson.

====================
GUARDSPEC — tests/cli/test_advertised_commands.py, a new file
====================

WHAT IT IS FOR, and the sentence the module docstring must carry in its own
words: deleting a command is not finished until the strings that tell an
operator to run it are gone too. Name F272 round 19 as the instance.

S1. A module-level scanner function taking a string and returning the
    `(group, subcommand)` pairs that string advertises as a command. It counts a
    `remedy <group> <sub>` pair ONLY when `<group>` is a key of `GROUPS` from
    `apps.cli.command_catalog` AND the pair is followed by an argument
    placeholder (`<` or `{`), an option (`--`), a quote, or the end of the
    string. That narrowing is what keeps ordinary prose out: measured at the
    base commit, the unnarrowed form reports `remedy init requires`,
    `remedy do v1` and `remedy output truncated` as commands, and the narrowed
    form reports none of them.

S2. THE ZERO-GATE. Over every tracked `.py` under `packages/` and `apps/`,
    enumerated from `git ls-files` and never from a shell glob, no advertised
    pair may be absent from `{(c.group_id, c.subcommand) for c in CATALOG}`.
    The failure message names every offending `path:line: remedy <g> <s>`.

S3. AN ANTI-BLINDNESS ASSERTION in that same test, BEFORE the zero-gate
    assertion: the number of advertisements the scan saw must exceed 100. A
    scan that matches nothing satisfies a zero-gate perfectly, and this is the
    only thing standing between this guard and that failure. At the base commit
    the real figure is 738, so 100 is a floor with room and not a pin.

S4. THREE DISCRIMINATORS, each its own test, because a guard with no
    discriminator cannot be shown to see anything:
    (a) the scanner returns `[("job", "no-such-subcommand")]` for a line
        advertising it, and that pair is not in the catalog;
    (b) the scanner returns nothing for `remedy init requires a git repository`;
    (c) the scanner finds `("job", "report")` in a real next-action f-string.

S5. Use `Path(__file__).resolve().parents[2]` for the repository root so the
    test does not depend on the working directory, and read every file with
    `encoding="utf-8"`.

MEASURED BEFORE THIS BLOCK WAS WRITTEN, in a disposable worktree at the base
commit, with a scanner written to this specification: RED at the base — one
failed and three passed, the failure naming exactly the seven occurrences at
the five sites listed above and nothing else — and GREEN once P1 through P5 are
applied, at four passed. The colour is therefore reachable in both directions,
and the guard is not one that cannot fail.

====================
The repairs, and why each replacement is the honest one
====================

P3 is the one that was measured rather than chosen. `autonomy_readiness`'s
`agent_loop` check is `_has_agent_loop(events)`, which is true of any event
whose kind starts `agent_loop_`. At the base commit the ONLY surviving emitter
of such an event is `apps/cli/commands/brain.py:514`, which logs
`agent_loop_inspected` and is reached by `remedy dev agent-loop <job_id>`. The
reviewer RAN the shipped predicate against that shipped kind at the base commit:
`_has_agent_loop([{"event": "agent_loop_inspected"}])` is True and
`_has_agent_loop([])` is False, so the new hint is satisfiable and the predicate
is not vacuous.

P1 and P2 point at `remedy job run`, NOT at `remedy do job-run`, and that is
deliberate. Both sites hold a CLASSIC job — `decision.py`'s branch calls
`save_job(job)`, and `job.py:1598` is inside `_cmd_job_status` — while
`do job-run` takes a 16-character `JobPlan` id, so `do job-run` would be a hint
the operator cannot use. `job.run` is itself scheduled for deletion later in
T004, and DECISIONR20 below rules that its advertisements move in the same
commit that deletes it. A hint naming a command that exists is strictly better
than one naming a command that does not.

P4 and P5 point the job branch at `guide.job`, the only `guide` command, and the
no-job branch at `job.list`, matching the surrounding style of those two
functions (`remedy review list --json`, `remedy worker registry-list --json`).
No test anywhere in the repository asserts either string; the reviewer grepped
`tests/` for `guide next` at the base commit and it returns nothing.

<<<BEGIN P1 FROM sha256=none path=apps/cli/commands/decision.py>>>
        print(f"Resume the run: remedy job run-loop {job_id_str} --json")
<<<END P1 FROM>>>
<<<BEGIN P1 TO>>>
        print(f"Resume the run: remedy job run {job_id_str} --json")
<<<END P1 TO>>>

<<<BEGIN P2 FROM path=apps/cli/commands/job.py>>>
        next_action = 'remedy job run-loop <job_id> --json'
<<<END P2 FROM>>>
<<<BEGIN P2 TO>>>
        next_action = 'remedy job run <job_id> --json'
<<<END P2 TO>>>

<<<BEGIN P3 FROM path=packages/orchestration/autonomy_readiness.py>>>
        _check("agent_loop", "remedy job run-loop <job_id>")
<<<END P3 FROM>>>
<<<BEGIN P3 TO>>>
        _check("agent_loop", "remedy dev agent-loop <job_id>")
<<<END P3 TO>>>

<<<BEGIN P4 FROM path=packages/orchestration/model_route_tournament.py>>>
        return f"remedy guide next {jid} --json" if job_id else "remedy guide next --json"
<<<END P4 FROM>>>
<<<BEGIN P4 TO>>>
        return f"remedy guide job {jid} --json" if job_id else "remedy job list --json"
<<<END P4 TO>>>

<<<BEGIN P5 FROM path=packages/orchestration/worker_registry.py>>>
        return f"remedy guide next {jid} --json" if job_id else "remedy guide next --json"
<<<END P5 FROM>>>
<<<BEGIN P5 TO>>>
        return f"remedy guide job {jid} --json" if job_id else "remedy job list --json"
<<<END P5 TO>>>

====================
Done when — the gates
====================

Run every gate with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, no pipe between the
command and the echo. Report ONE LINE PER GATE in the handback, and the
transcripts below it. Every gate runs before C6, which is the commit that writes
the handback.

G1 TRANSPORT. One digest comparison. `.agent/authored/f272-r20.md` and
   `.agent/last_block.md` share one sha256, one byte length and one line count
   with the file this block was delivered from. Report all three figures.

G2 THE RECORD, over the C2 append to `.agent/live_review.md`.
   (a) BYTE: pre-image read immediately before the write; report pre_len,
       pre_sha256, post_len, post_sha256, the terminal twelve bytes and the
       trailing-newline run of each, `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and
       `POST_EQUALS_PRE_NL_SLICE`. At the base commit the pre-image is
       1173866 bytes, sha256
       `8363661be8b7dbb9ebc0982b1e60fffab1cefbedb70c6a603a3a299d332b3236`,
       terminal twelve bytes `b'obe output.\n'`, trailing-newline run 1.
   (b) STRUCTURAL: strip the single terminal newline, split on blank lines,
       and compare the LAST N units against the slice's paragraphs IN ORDER,
       where N is COUNTED BY YOUR SCRIPT from the slice and never taken from
       this block. Report N, units before, units after, and
       `EVERYTHING_BEFORE_UNCHANGED`.
   (c) NEGATIVE CONTROL on the FIRST appended paragraph, in memory only, never
       on disk: flip one byte and require BOTH readers to reject it. Re-read
       the file afterwards and confirm it is byte-identical to the real
       post-image.
   (d) COUNTS before and after, each measured, none adjusted to agree:
           ^- R-\d{4} distinct        306 -> 307
           ^Done: R-\d{4} distinct    249 -> 249
           open set BY DISTINCT ID     57 -> 58
           ^Gate:                      42 -> 43
           ^Gate: F272 R19              0 -> 1
           ^- R-0823                    0 -> 1
       Report OPEN FINDINGS BY DISTINCT ID with its arithmetic. R-0823 is the
       only id this round mints.

G3 THE PROSE FILES. `.agent/plan.md` is byte-equal to PLANF272R20; report its
   bytes, its line count against the AGENTS.md cap of 50, and that `## Goal`
   and `## Next Steps` are both present. `.agent/prose_slips.md` satisfies
   `post == pre + NL + slice` for SLIPSR20; report pre and post byte lengths.
   At the base commit `.agent/prose_slips.md` is 146054 bytes.

G4 THE GUARD IS REAL — the ordered colour, CONTROL FIRST, in a disposable
   worktree detached at C4, never in the primary checkout.
   (i)   control: `python3 -B -m pytest tests/cli/test_advertised_commands.py -q
         -p no:randomly` is EXIT 0. Report the passed count.
   (ii)  revert EXACTLY ONE line — restore
         `packages/orchestration/autonomy_readiness.py`'s single occurrence of
         P3's TO back to P3's FROM. That byte string occurs exactly 1x in that
         file; assert the count is 1 before writing, and name the file in the
         report.
   (iii) the same command is now EXIT 1, and the failure message names
         `packages/orchestration/autonomy_readiness.py` AND NO OTHER PATH.
         Report the full unresolved list the assertion prints.
   (iv)  restore, re-run, EXIT 0 again.
   Report the worktree path, that `apps.cli.command_catalog.__file__` resolved
   inside it, and the exact removal command.

G5 THE SWEEP IS ZERO AND THE SCAN IS NOT BLIND. In the primary checkout at C4,
   run the shipped test file and report both the passed count and, separately,
   the number of advertisements the scan saw — print it, do not assert it from
   this block. At the base commit that figure was 738.

G6 THE FULL SUITE, in the PRIMARY CHECKOUT:
   `python3 -B -m pytest -n auto -q -p no:randomly`. Report the real exit code,
   the passed/skipped counts and `grep -c '^FAILED'`. RECONCILE rather than
   assert: the reviewer measured the base at `8bcdc4dc` as 19780 passed and 23
   skipped, and C4 adds four test functions by `ast` count, so the expected
   reading is 19784 passed. If the true figure differs, REPORT the difference
   and change nothing to make it agree.

G7 RUFF AND THE DOCS GATE. `python3 -m ruff check` over the five edited `.py`
   files and the new test file — EXIT 0, `All checks passed!`.
   `python3 -B -m pytest tests/docs/ -q` EXIT 0, because C5 touches
   `docs/roadmap/**`. The canary `python3 -B -m pytest
   tests/cli/test_golden_path.py -q` EXIT 0.

G8 THE TREE. `git status --porcelain` EMPTY at every commit boundary, with the
   real output each time. `git ls-files .remedy-wt` empty. Per-commit insertions
   from `git diff --numstat <parent> <commit>` for C0a through C5 — C6 excluded,
   because a commit cannot count its own insertions while it is being written —
   each under the DECISION F104 D1 cap of 500. The three `.agent/STOP` readings.
   The feature file's byte length and line count before and after C5.

====================
Handback
====================

Rewrite `.agent/handoff.md` completely. It carries: `SESSION 10 of feature F272
· round 20 · rounds so far 20`; the soft limit reading under
amend0906-triage-throughput, which is 12 sessions and 40 rounds; one sentence of
context self-assessment; the range; a per-commit changed-files table with the
`+/-` column taken from `git diff --numstat` and compared cell for cell against
the per-commit figures G8 reports; the item-status table for C0a through C6; one
line per gate followed by the transcripts; every deviation and assumption; and
the next expected action. It has no length cap.

<<<BEGIN PLANF272R20 target=.agent/plan.md>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 19 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001, T002 and T003
are COMPLETE. T004 is under way.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Repair the production strings that advertise commands which do not exist, and
ship the guard that keeps them repaired. Round 19 deleted `job run-loop` and
left three such strings; two more, naming a `guide next` that never existed,
were found by the same measurement.

## Next Steps

1. Delete the `job.run-next` command surface. Its catalog entry, its handler
   entry and one test pin are a clean cut, but sixteen other sites advertise
   `remedy job run-next` as a next action and both approval-gate tests in
   `tests/cli/test_plan_approval.py` shell out to it, so the advisory layer
   and those two tests move in the same commit.
2. Delete `job.run`. It is the catalog's ONLY `is_expensive` command and three
   tests pin that, so F114's cost preview needs a carrier before it goes.
3. Rule and delete the classic `_cmd_job_resume`, and with it
   `agent_loop.run_agent_loop`, which is the last production caller of
   `_cmd_run_next_task_local`.
4. The resolver collapse, which DECISION F260 D5 puts in the SAME commit range
   as the classic store deletion — 199 files by
   `.agent/f272_t004_deletion_inventory.md`, so many rounds.
5. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- A half-performed deletion is the one state the feature's Orchestrator brief
  says this work must not leave behind, so every deletion round ends with the
  full suite green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 10
  and round 20 the feature is inside it and no scope report is owed.
<<<END PLANF272R20>>>

<<<BEGIN RECORDR20 target=.agent/live_review.md mode=append>>>
Gate: F272 R19 — the F272 round 19 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `743c1e64`. Range `4c70ba90`..`743c1e64`, six commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4; the change set is the five ordered paths plus `apps/ui/src/api/humanizeCatalog.ts`, which deviation 1 declares. `git status --porcelain` empty, `git ls-files .remedy-wt` empty, thirteen worktree entries being the primary plus the twelve pre-existing `remedy/job-*`, and per-commit insertions 179, 151, 24, 2, 1 and 328, every one under the DECISION F104 D1 cap of 500. G1 TRANSPORT IS A REAL CHAIN: the reviewer's own scratch original `.remedy-wt/f272-r19-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r19.md` and `.agent/last_block.md` are all 14856 bytes at 179 lines and all hash to `90e7de9e0aa27c105b864fbb8d385e69b66f6c7af86a564202ff51d1d68f92c3`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces on every reader: `.agent/live_review.md` 1169833 to 1173866, the pre-image a byte-exact prefix, `post == pre + NL + slice` TRUE, N counted from the slice as 1 with units 718 to 719, and a byte flipped in the appended paragraph rejected by BOTH readers; all five ordered counts reproduce — registrations 306 unchanged, resolutions 249 unchanged, open set BY DISTINCT ID 57 unchanged, `^Gate: ` 41 to 42 and `^Gate: F272 R18 ` 0 to 1. G3 THE PLAN is 2179 bytes byte-equal to its slice at 43 lines against the cap of 50. G4 THE DELETION, by EXACT SYMBOL over every tracked `.py`: `_cmd_run_loop` and `job.run-loop` both reach 0, `packages/orchestration/autonomy_loop.py` still exists, and `job.run-next` and `job.run` are untouched. G5 THE FULL SUITE, re-run in the PRIMARY checkout: EXIT 0 at 19780 passed and 23 skipped with ZERO `FAILED` lines, and the arithmetic closes exactly — the base at `4c70ba90` was 19785 passed, an `ast` count gives the two touched test files 14 to 10 and 23 to 22, so five test functions were removed and 19785 − 5 = 19780. G6 ruff EXIT 0 with no F401 over the touched files. G7 THE TREE holds at every boundary and the three `.agent/STOP` readings are False. C3 IS A TRUE DELETION: across all five files its diff adds exactly ONE line, the corrected module docstring, against 182 deletions — no shim, no alias, no deprecation path. DEVIATION 1 IS UPHELD AND WAS THE RIGHT CALL: the reviewer verified the premise independently rather than accepting it, and at `4c70ba90` the only emitter of either `agent_loop_cycle_decision` or `agent_loop_stopped` was `apps/cli/commands/job.py` lines 1135 and 1146, both inside the deleted `_cmd_run_loop`, while `agent_loop_inspected` has a separate emitter at `apps/cli/commands/brain.py:514` and was correctly KEPT; the guard test was NOT edited, so the worker fixed the code the test measures rather than the test, and amend0906 names "deleted cockpit sections" as part of a deletion round's change set, which makes the fifth path IN SCOPE. DEVIATION 2 IS THE REVIEWER'S ARITHMETIC ERROR, correctly reported through the block's own RECONCILE clause with nothing adjusted to reach the block's number. DEVIATIONS 3 TO 9 ARE ACCEPTED. WHAT ROUND 20 FOUND THAT THIS GATE COULD NOT: round 19's grep gate swept the dotted command id `job.run-loop` and the symbol `_cmd_run_loop` and deliberately did not sweep the spaced form, so three production strings advertising `remedy job run-loop` survived the deletion and are registered below as R-0823. That is a defect of the ROUND rather than of this verdict, which measured exactly what it said it measured; the lesson is that a command-deletion gate must sweep the form the OPERATOR types, not only the form the code stores.

- R-0823 — Medium, FIVE PRODUCTION SITES TELL THE OPERATOR TO RUN A COMMAND THAT DOES NOT EXIST, THREE OF THEM CREATED BY ROUND 19'S OWN DELETION. MEASURED at `8bcdc4dce06271f949e35522b7aee135fc6b4273` by loading the shipped `apps/cli/command_catalog.py` and scanning every tracked `.py` under `packages/` and `apps/` enumerated from `git ls-files`: of 738 advertised `remedy <group> <sub>` strings, SEVEN OCCURRENCES AT FIVE SITES name a pair absent from the catalog — `apps/cli/commands/decision.py:292`, `apps/cli/commands/job.py:1598` and `packages/orchestration/autonomy_readiness.py:315` all print `remedy job run-loop`, whose catalog entry and handler round 19 deleted, and `packages/orchestration/model_route_tournament.py:322` and `packages/orchestration/worker_registry.py:717` both return `remedy guide next`, which has NEVER existed — the only `guide` command at that commit is `guide.job`. THE EFFECT IS USER-FACING AND EXACT: the CLI answers `Error: Unknown command 'run-loop'` and exits 2, so `decision.py`'s "Resume the run:" line after answering a decision, `_cmd_job_status`'s `next_action` field for a job with pending tasks, and `autonomy_readiness`'s level-4 remediation hint each hand the operator a command line that cannot run. WHY NO GATE SAW IT: round 19's deletion gate counted the dotted catalog id `job.run-loop` and the symbol `_cmd_run_loop` to zero over every tracked `.py`, and both readings were TRUE — the surviving strings spell the command the way an operator types it, with a space, and the block deliberately excluded the bare word from the sweep. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED, per §3 item 30, by grepping `.agent/live_review.md` for `run-loop`, `next_action`, `autonomy_readiness` and the stale-hint phrasings; no open finding describes it. WHY MEDIUM: nothing is corrupted and no data is lost, but Remedy's next-action rail is the product's own instruction to its operator, and an instruction that cannot be executed is worse than none — it is also the exact class every remaining T004 round will reproduce, since each deletes a command that some rail still advertises. RESOLVED WHEN all five sites name a command the catalog carries, AND a guard test enumerates every tracked production `.py` and fails on any advertised pair the catalog does not hold, AND that guard carries an anti-blindness assertion so that a scan matching nothing cannot satisfy it.
<<<END RECORDR20>>>

<<<BEGIN SLIPSR20 target=.agent/prose_slips.md mode=append>>>
2026-09-07, F272 round 19 — the block's C3 list named four paths and the deletion really reached five: `_cmd_run_loop` was the sole emitter of the two `humanizeCatalog.ts` entries `agent_loop_cycle_decision` and `agent_loop_stopped`, so deleting it orphaned them and the worker had to leave the declared change set to keep `tests/ui_contracts/test_humanize_catalog.py` green. Before ordering a deletion, grep the cockpit catalog for every event kind the deleted code is the only emitter of.

2026-09-07, F272 round 19 — the block's G5 predicted four removed test functions and 19781 passing; the true figures are five and 19780, because the reviewer read 13 test functions in `tests/test_agent_loop_execution.py` where the file held 14, having counted a run in which three of them were failing rather than counting by `ast`. Count a file's tests with `ast`, never from a pytest summary line.

2026-09-07, F272 round 19 — the block's framing paragraph said the previous round's verdict books "in this round's first commit" while its own bundle ordered it at C2; C2 is correct under §3 item 23 and the sentence was loose. A framing sentence about commit order must quote the bundle rather than paraphrase it.
<<<END SLIPSR20>>>

<<<BEGIN DECISIONR20 target=docs/roadmap/features/T2_F272.md mode=append>>>
### DECISION F272 D13 (2026-09-07, F272 round 20) — a command's ADVERTISEMENTS are deleted in the same commit as the command, and T004's remaining order is set by that rule rather than by the size of each handler

CONTEXT. Round 19 deleted the `job run-loop` command surface under
amend0906-triage-throughput's deletion-round rule, whose four measurements are the
import-reachability test, the full suite, "a repo-wide grep for every deleted
module and symbol at zero", and ruff. All four were run and all four were green.
Three production strings advertising `remedy job run-loop` nonetheless survived,
because the grep swept the DOTTED catalog id and the SYMBOL — the two spellings
the code stores — and not the SPACED form the operator types. Registered as
R-0823, together with two older sites naming a `guide next` that has never
existed.

CHOSEN, AND IT IS AN ORDERING RULE RATHER THAN A NEW GATE. A command's
advertisements die in the SAME COMMIT as the command. Under AGENTS.md's Scope
Control an advertisement IS the replaced mechanism's surviving surface, so a
deletion that leaves one behind is the "closure that leaves the old mechanism
alive" that section forbids. The measurement is the guard test round 20 ships,
`tests/cli/test_advertised_commands.py`, which fails on any `remedy <group>
<sub>` string in tracked production code whose pair the catalog does not carry;
amend0906's third measurement is read from here on as covering the operator's
spelling as well as the code's, and the guard is what performs that reading.

T004'S REMAINING ORDER FOLLOWS FROM THAT RULE, MEASURED AT
`8bcdc4dce06271f949e35522b7aee135fc6b4273` AND NOT ESTIMATED. `job.run-next` is
not the clean cut the round 19 handback expected: its catalog entry, its handler
entry and one pin in `tests/test_command_catalog.py` are three lines, but the
string `remedy job run-next` occurs SIXTEEN TIMES across EIGHT modules under
`packages/orchestration/` — `agent_loop.py`, `autonomy_loop.py`,
`brain_detail.py`, `cockpit.py`, `dashboard.py`, `long_run_executor.py`,
`timeline.py` and `trust_report.py` — TWICE MORE in `scripts/remedy_smoke.sh`,
and SIX TEST FILES assert that text, while both approval-gate tests in
`tests/cli/test_plan_approval.py` SHELL OUT to `remedy job run-next` to prove the
gate blocks execution. A dry run of the three-line cut, performed in a disposable
worktree before this block was written, turned exactly those two tests red with
`Error: Unknown command 'run-next'`, which is how the advisory layer was found at
all. `job.run` is harder still: it is
the catalog's ONLY `is_expensive` command, and `tests/test_command_catalog.py`
pins that in three tests, so F114's cost preview needs a carrier before it can go.

AND THE CLASSIC RUNNER IS ONE CONNECTED COMPONENT, WHICH CORRECTS THE ROUND 19
HANDBACK. `_cmd_job_run_cycles` calls `_cmd_run_next_task_local`;
`_cmd_job_resume` calls `_cmd_job_run_cycles`, `_resume_preview` and
`_print_resume_preview`; and `packages/orchestration/agent_loop.py`'s
`_run_next_task_step`, reached only from `run_agent_loop`, calls
`_cmd_run_next_task_local` too. So `run_agent_loop` MUST die in the same commit
range as the classic runner and belongs to T004, not to T005. The round 19
handback's sentence that "`agent_loop.py` is production-unreachable" is corrected
here rather than rewritten: the MODULE is reachable — `apps/cli/commands/brain.py`
imports `derive_agent_loop_state` and `summarize_agent_loop_state` from it for
`remedy dev agent-loop` — and only `run_agent_loop` and its two private helpers
are not. `agent_loop.py` therefore SURVIVES T004 with its inspection half intact.
F260's Design section, whose prototype-cluster list T005 executes, names neither
`agent_loop.py` nor `autonomy_loop.py`, so nothing is being taken away from T005
that it was ever given.

ALTERNATIVES CONSIDERED. Sweeping the spaced form in each deletion round's grep
instead of shipping a guard — rejected: that is the same per-instance fix that let
this class survive round 19, and a grep written by the round that must not miss
anything is exactly the gate that cannot fail. Repairing only the three
`run-loop` sites and leaving the two `guide next` ones — rejected: they are the
same defect, the guard cannot be a zero-gate while they stand, and a gate scoped
to avoid its own findings protects nothing. Pointing the two repaired classic-job
hints at `remedy do job-run` — rejected on measurement: both sites hold a classic
UUID job and `do job-run` takes a 16-character `JobPlan` id, so it would be a hint
the operator cannot use.

CONSEQUENCE. One guard test, five repaired lines, and an order for the rest of
T004 in which the advisory layer moves WITH each command rather than after it. No
behaviour changes for any command that still exists.

REVERSE by deleting this section and
`tests/cli/test_advertised_commands.py`, at which point the advertisements are
once again swept per round by whatever grep that round happens to write.
<<<END DECISIONR20>>>
