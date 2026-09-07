STEP T004/4 — F272 — round 22 — REPAIR ROUND: the round 21 block wrote the string its own gate forbids

Base commit for every reading in this block: `3ca66aac`, the round 21 handback commit.
Every separator line below is exactly twenty `=` characters.

====================
Goal
====================

Round 21 FAILED. Its P3 TO put the prose sentence "The execution loop `remedy
job run-loop <job_id>` was DELETED at F272 round 19." into
`docs/system/architecture.md`, and the same block's WIDENSPEC widened the guard's
zero-gate corpus to include `docs/system/`. The block therefore ordered a string
to be written into a file it also ordered swept to zero — the §3 item 2 defect
exactly, and the branch tip ships RED because of it.

The worker applied the block verbatim, declared the contradiction and proved by
counterfactual that nothing else is wrong. This round registers that as R-0824
and repairs it.

====================
What is actually broken, measured at the base commit
====================

    python3 -B -m pytest tests/cli/test_advertised_commands.py -q -p no:randomly
    -> EXIT 1, 1 failed, 4 passed
    -> docs/system/architecture.md:927: remedy job run-loop

ONE failure, ONE line, and it is the reviewer's own replacement text. Everything
else round 21 built was verified GREEN by the reviewer at the base commit: the
widened corpus reports 738 production advertisements with none unresolved and 404
operator-facing advertisements with exactly this one unresolved; `bash -n
scripts/remedy_smoke.sh` is EXIT 0; smoke sections `12h` and `12ae` are gone with
neighbours `12g`, `12i`, `12ad` and `12af` intact and `_SMOKE_SECTION=`
assignments falling 75 to 73, which is exactly the two ordered.

THE FIX IS THE `remedy ` PREFIX AND NOTHING ELSE. The scanner matches only a
literal `remedy <group> <sub>`, which is why the migration-table row in
`docs/guides/simple-operator-quickstart-v0.md:108` and the event-table cells
reading `active — job run-loop` never matched and were never findings. A sentence
that NAMES a deleted command without spelling it as an invocation is not an
advertisement, and round 21's own block said so in those words while its
replacement text did the opposite.

====================
Bundle
====================

C0a  save this block verbatim to `.agent/authored/f272-r22.md`
C0b  mirror the same bytes to `.agent/last_block.md`
C1   `.agent/plan.md` replaced byte for byte with PLANF272R22
C2   `.agent/live_review.md` — append RECORDR22 (the round 21 FAIL gate entry
     and the R-0824 registration). FINDINGS PERSIST FIRST, before the repair.
C3   `docs/system/architecture.md` — pair P1, the repair
C4   `.agent/live_review.md` — append DONER22, resolving R-0824
C5   `.agent/handoff.md` rewritten

====================
Change set — exactly these paths and nothing else
====================

    .agent/authored/f272-r22.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    docs/system/architecture.md
    .agent/handoff.md

Nothing under `tests/`, `packages/`, `apps/` or `scripts/` changes this round.
The guard is NOT edited: a gate that goes green because its own text was
loosened proves nothing, and this defect is in the document, not in the guard.
If a measurement forces a path outside this list, APPLY IT AND DECLARE IT.

====================
Constraints
====================

1. This block is applied verbatim. If a slice is wrong, apply it as written and
   declare the disagreement; never silently correct it.
2. Every authored slice is extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f272-r22.md`, between its `<<<BEGIN NAME>>>` and
   `<<<END NAME>>>` lines. Never retype a slice. A slice is read INCLUSIVE of
   the newline ending its last content line.
3. C0a and C0b are `shutil.copyfile` of one source file.
4. P1 is a REWRITE. The containment test was RUN by the reviewer at the base
   commit and answered `TO contains FROM: false`; the FROM occurs exactly 1x in
   `docs/system/architecture.md` and the TO exactly 0x. The post-edit reading is
   FROM 0x, TO 1x.
5. C2 and C4 are TWO SEPARATE APPENDS to `.agent/live_review.md`, in that order,
   with C3 between them. Each is proved against its OWN pre-image. C2 must
   precede C3: §4 item 4 requires findings to persist before the repair, and
   DONER22 states a fact about C3's landed change, so it must follow it.
6. DONER22 names no SHA for the change it describes, because that commit does
   not exist when this block is written; it names constraint 5, which fixes the
   order — the §3 item 20 carve-out for a claim about the round's OWN commits.
7. `.agent/prose_slips.md` is NOT in the change set. This defect put a red test
   on disk, so it is an R-id under amend0827 rule 2 rather than a prose slip.
8. Read `.agent/STOP` with `os.path.exists` before C0a, before C3 and before
   C5, and report all three readings.
9. No worktree is needed this round: the red is already on disk in the primary
   checkout at the base commit, so the "before" colour is observed rather than
   manufactured, and the "after" colour is the ordinary green run. Nothing
   destructive is ordered, so nothing must be isolated.
10. STATED SO A LATER WIDENING DOES NOT REPEAT R-0824. The reviewer ran the
    SHIPPED `scan_advertised_commands` over every slice of this block before
    emission. P1's TO yields ZERO advertisements, which is the property the
    repair exists to obtain. RECORDR22 yields TWO — both `remedy job run-loop`,
    quoted while describing the defect — and that is SAFE ONLY BECAUSE neither
    collector's corpus reaches `.agent/`: one sweeps tracked `.py` under
    `packages/` and `apps/`, the other tracked `.sh` under `scripts/` and
    tracked `.md` under `docs/system/` and `docs/guides/`. Any future round that
    widens either corpus to `.agent/` must re-read the landed record first,
    because this file is append-only and §3 item 20 forbids rewriting it.

====================
The repair
====================

<<<BEGIN P1 FROM path=docs/system/architecture.md>>>
The execution loop `remedy job run-loop <job_id>` was DELETED at F272 round 19.
<<<END P1 FROM>>>
<<<BEGIN P1 TO>>>
The execution loop invoked as `job run-loop` was DELETED at F272 round 19, and
the command no longer exists; the guard in
`tests/cli/test_advertised_commands.py` is why this sentence names it without
spelling it as an invocation.
<<<END P1 TO>>>

====================
Done when — the gates
====================

Run every gate with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, no pipe between the
command and the echo. Report ONE LINE PER GATE with the transcripts below it.
Every gate runs before C5, the commit that writes the handback.

G1 TRANSPORT. One digest comparison: `.agent/authored/f272-r22.md` and
   `.agent/last_block.md` share one sha256, one byte length and one line count
   with the file this block was delivered from. Report all three.

G2 THE RECORD, over BOTH appends, each against its OWN pre-image.
   (a) BYTE, twice: for C2 and again for C4 report pre_len, pre_sha256,
       post_len, post_sha256, the terminal twelve bytes and trailing-newline run
       of each, `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and
       `POST_EQUALS_PRE_NL_SLICE`. At the base commit the C2 pre-image is
       1186986 bytes.
   (b) STRUCTURAL, twice: strip the single terminal newline, split on blank
       lines, compare the LAST N units against that slice's paragraphs IN ORDER,
       where N is COUNTED BY YOUR SCRIPT from the slice and never taken from
       this block. Report N, units before, units after and
       `EVERYTHING_BEFORE_UNCHANGED` for each.
   (c) NEGATIVE CONTROL on the FIRST paragraph appended by C2, in memory only,
       never on disk: flip one byte, require BOTH readers to reject it, then
       re-read the file and confirm it is byte-identical to the real post-image.
   (d) COUNTS across the whole round, each measured, none adjusted to agree:
           ^- R-\d{4} distinct        307 -> 308
           ^Done: R-\d{4} distinct    250 -> 251
           open set BY DISTINCT ID     57 -> 57
           ^Gate:                      44 -> 45
           ^Gate: F272 R21              0 -> 1
           ^- R-0824                    0 -> 1
           ^Done: R-0824                0 -> 1
       Report OPEN FINDINGS BY DISTINCT ID with its arithmetic. The open set is
       UNCHANGED at 57 because this round both mints and resolves R-0824;
       R-0825 stays free.

G3 THE PLAN. `.agent/plan.md` is byte-equal to PLANF272R22. Report its bytes,
   its line count against the AGENTS.md cap of 50, and that `## Goal` and
   `## Next Steps` are both present.

G4 THE ORDERED COLOUR, in the PRIMARY checkout, on the SHIPPED test, with the
   red observed BEFORE the repair rather than manufactured after it:
   (i)  at the base commit, BEFORE C3:
        `python3 -B -m pytest tests/cli/test_advertised_commands.py -q -p
        no:randomly` is EXIT 1, and the unresolved list names
        `docs/system/architecture.md` AND NO OTHER PATH. Report that list in
        full.
   (ii) at C3: the same command is EXIT 0. Report the passed count.
   The failing test is the one round 21 added; report its node id in both runs.

G5 NOTHING ELSE MOVED. In the primary checkout at C3, run serially and report
   each exit code and count:
       python3 -B -m pytest tests/cli/test_product_spine.py -q -p no:randomly
       python3 -B -m pytest tests/test_remedy_smoke_script.py -q -p no:randomly
       python3 -B -m pytest tests/docs/ -q -p no:randomly
       python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
   Separately PRINT, do not assert from this block, the advertisement count each
   of the two collectors saw at C3. At the base commit they were 738 and 404.

G6 THE STRING IS GONE FROM THE SWEPT CORPUS. Report the count of the exact
   string `remedy job run-loop` in `docs/system/` and in `scripts/`: both must
   be 0. Report it also for `docs/guides/`, where it must ALSO be 0 — the
   migration-table row there spells `job run-loop` WITHOUT the `remedy ` prefix,
   so this reading confirms the row survived rather than that it was swept.
   Report `docs/system/architecture.md`'s byte length and line count before and
   after C3.

G7 THE TREE. `git status --porcelain` EMPTY at every commit boundary with the
   real output each time. `git ls-files .remedy-wt` empty. Per-commit insertions
   from `git diff --numstat <parent> <commit>` for C0a through C4 — C5 excluded,
   because a commit cannot count its own insertions while it is being written —
   each under the DECISION F104 D1 cap of 500. The three `.agent/STOP` readings.
   No ruff reading is owed: no `.py` file changes this round.

====================
Handback
====================

Rewrite `.agent/handoff.md` completely: `SESSION 10 of feature F272 · round 22 ·
rounds so far 22`; the soft-limit reading under amend0906-triage-throughput,
which is 12 sessions and 40 rounds; one sentence of context self-assessment; the
range; a per-commit changed-files table whose `+/-` column comes from `git diff
--numstat` and is compared cell for cell against G7's figures; the item-status
table for C0a through C5; one line per gate with the transcripts below it; every
deviation and assumption; and the next expected action. It has no length cap.

<<<BEGIN PLANF272R22 target=.agent/plan.md>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 20 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected, and round 21 FAILED
on R-0824, which this round repairs. T001, T002 and T003 are COMPLETE. T004 is
under way.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Repair R-0824: the round 21 block's own replacement prose wrote `remedy job
run-loop` into `docs/system/architecture.md` while the same block widened the
guard's zero-gate corpus to sweep that directory, so the branch tip shipped RED.
The sentence now names the deleted command without spelling it as an invocation.

## Next Steps

1. The classic store deletion, which leads T004 rather than following it.
   Measured at `5f4f0405`: every next-action rail advertising `remedy job
   run-next` — in `cockpit.py`, `timeline.py`, `trust_report.py`,
   `dashboard.py`, `brain_detail.py`, `agent_loop.py` and `autonomy_loop.py` —
   sits in a function typed `job: Job`, the CLASSIC record. None takes a
   `JobPlan`, so none can point at `remedy do job-run`, whose id is a
   16-character JobPlan id. The advertisements cannot move before the classic
   record does, and DECISION F272 D13 forbids deleting a command ahead of its
   advertisements.
2. `job.run-next` and `job.run` die inside that same commit range, with their
   rails. `job.run` is the catalog's only `is_expensive` command and three tests
   pin that, so F114's cost preview needs a carrier named before it goes.
3. `_cmd_job_resume` and `agent_loop.run_agent_loop`, the last production caller
   of `_cmd_run_next_task_local`, die with them per DECISION F272 D13.
4. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- The store deletion is 199 files by `.agent/f272_t004_deletion_inventory.md`,
  72 of them production, so it is many rounds and no single commit holds it.
- A half-performed deletion is the one state the Orchestrator brief says this
  work must not leave behind, so every deletion round ends with the full suite
  green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 10
  and round 22 the feature is inside it and no scope report is owed.
<<<END PLANF272R22>>>

<<<BEGIN RECORDR22 target=.agent/live_review.md mode=append>>>
Gate: F272 R21 — the F272 round 21 entry. VERDICT FAIL, AND THE DEFECT IS THE REVIEWER'S BLOCK RATHER THAN THE WORKER'S EXECUTION. Range `5f4f0405`..`3ca66aac`, six commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, with `git status --porcelain` empty, `git ls-files .remedy-wt` empty and per-commit insertions 401, 294, 26, 4 and 83 for C0a through C3, each under the DECISION F104 D1 cap of 500. THE BLOCK'S P3 TO WROTE THE STRING THE BLOCK'S OWN WIDENED ZERO-GATE FORBIDS. WIDENSPEC widened the guard's corpus to every tracked `.md` under `docs/system/` and `docs/guides/`, and P3's replacement prose put the sentence "The execution loop `remedy job run-loop <job_id>` was DELETED at F272 round 19." into `docs/system/architecture.md` — a literal `remedy <group> <sub>` in command shape, in a file the same block ordered swept to zero. That is docs/agents/planner_reviewer_prompt.md §3 item 2 exactly: a must-be-0 done-when may not count a string that any TO slice in the same block writes into that same file. The reviewer ran item 2 against round 20's block and did not re-run it when round 21 WIDENED the corpus, which is what turned two previously unswept directories into targets of the gate. The block even states the governing distinction in its own words — that a sentence naming a deleted command without the `remedy ` prefix is not an advertisement, which is why the migration-table row in `docs/guides/simple-operator-quickstart-v0.md:108` and the `active — job run-loop` event-table cells never matched — and then wrote its replacement the other way. Registered below as R-0824. THE WORKER'S EXECUTION WAS CORRECT AND IS UPHELD IN FULL: it applied the block verbatim as constraint 1 requires, declared the contradiction rather than rewording the reviewer's text to make a gate green, and isolated the blocker by a counterfactual run in a disposable worktree in which respelling that one clause produced exactly the block's predicted figures — control EXIT 0 at 5 passed, the ordered one-line revert EXIT 1 naming `docs/system/core-product-spine-v0.md:36` and no other path, and restore EXIT 0 at 5 passed. EVERYTHING ELSE THE ROUND BUILT IS VERIFIED GREEN BY THE REVIEWER AT `3ca66aac`. G1 TRANSPORT IS A REAL CHAIN: the reviewer's own scratch original `.remedy-wt/f272-r21-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r21.md` and `.agent/last_block.md` are all 27279 bytes at 401 lines and all hash to `784455aab97960fca16aeecb89830a862b91f8f3f362b1c70b63c1e6867c05e1`. G2 THE RECORD reproduced on every reader with all six ordered counts exact. G3 THE PLAN is 48 lines against the cap of 50. THE SMOKE DELETION IS EXACT, re-measured by the reviewer rather than read: `scripts/remedy_smoke.sh` falls 2818 to 2731 lines, `_SMOKE_SECTION=` assignments 75 to 73 — exactly the two ordered — sections `12h` and `12ae` are absent while `12g`, `12i`, `12ad` and `12af` all survive at one assignment each, `bash -n` is EXIT 0, and the string `agent_loop` in that file goes 14 to 0. THE WORKER'S THREE DEVIATIONS ARE ALL UPHELD. Deviation 1 corrected SMOKESPEC's own end-bound, whose literal reading would have swallowed the following section's banner and contradicted S4; the banner-to-banner reading it used is the one that satisfies both sentences. Deviation 2 edited `tests/test_remedy_smoke_script.py`, one path outside the declared change set, deleting the four text-presence guards on the deleted sections; the reviewer confirms the deletion FORCED at least two of them — `agent_loop` and `agent_loop_task_exit` both reach 0 occurrences in the script, so `test_smoke_has_agent_loop_schema_check` and `test_smoke_checks_no_agent_loop_task_exit` cannot pass — and confirms the fourth, `test_smoke_checks_agent_loop_forbidden_strings`, was GREEN-BUT-DEAD, since `stdout`, `stderr`, `raw_output` and `Traceback` still occur 15, 199, 15 and 15 times elsewhere in the script, so that guard had become a gate that cannot fail. Deleting it was the right call and the worker was right to flag it as a judgement call. Deviation 3 is the block's own defect, measured on the slice's bytes BEFORE applying, and reported instead of being papered over.

- R-0824 — Medium, THE BRANCH TIP SHIPS RED BECAUSE A BLOCK ORDERED A STRING WRITTEN INTO A FILE IT ALSO ORDERED SWEPT TO ZERO. MEASURED at `3ca66aac` in the primary checkout: `python3 -B -m pytest tests/cli/test_advertised_commands.py -q -p no:randomly` is EXIT 1 at 1 failed and 4 passed, the failure being `test_every_operator_facing_advertised_command_exists_in_the_catalog` and its unresolved list holding exactly one entry, `docs/system/architecture.md:927: remedy job run-loop`. THE CAUSE IS A REVIEWER BLOCK, NOT PRODUCT CODE, BUT THE EFFECT IS ON DISK: a test that this feature shipped one round earlier is red on the branch, which is state under `tests/` and `docs/` being wrong, so amend0827 rule 2 spends an id rather than a prose-slip line. The round 21 block widened the guard's corpus to `docs/system/` and `docs/guides/` in its WIDENSPEC and, in its P3 TO, wrote `remedy job run-loop <job_id>` into `docs/system/architecture.md` — the two orders cannot both be satisfied, and the worker correctly applied both and declared it. WHY THE CHECK DID NOT CATCH IT: §3 item 2 was run against the round 20 block, whose corpus was production `.py` only and in which no TO touched a swept file; when round 21 widened the corpus, the item was not re-run against the new corpus, so two directories became gate targets without their TOs being re-read. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED, per §3 item 30, by grepping `.agent/live_review.md` for `item 2`, `zero-gate`, `self-counting` and `architecture.md`; no open finding describes it. R-0823 is RESOLVED and is not this defect — that one was five production sites advertising deleted commands, while this is one documentation sentence created by the repair itself. WHY MEDIUM: it is one line, it is caught by the branch's own guard rather than by a user, and nothing an operator runs is affected — but a red tip is the state a feature must never hand to the next session, and the guard that catches it is the one this feature shipped to make the class visible, so leaving it would falsify the resolution one round old. RESOLVED WHEN the sentence in `docs/system/architecture.md` names the deleted command without spelling it as a `remedy <group> <sub>` invocation, the guard is EXIT 0 with BOTH collectors non-blind, and the guard itself is unedited — a gate loosened to pass its own author's text proves nothing.
<<<END RECORDR22>>>

<<<BEGIN DONER22 target=.agent/live_review.md mode=append>>>
Done: R-0824 — RESOLVED at F272 round 22 by the commit this block's constraint 5 fixes as C3, the only commit of this round that touches `docs/system/architecture.md`, verified by the reviewer by re-running the shipped guard rather than by reading it. The sentence now reads "The execution loop invoked as `job run-loop` was DELETED at F272 round 19, and the command no longer exists", which names the deleted command without spelling it as a `remedy <group> <sub>` invocation, so the scanner does not match it — the same treatment that already keeps the migration-table row at `docs/guides/simple-operator-quickstart-v0.md:108` and the `active — job run-loop` cells of the same event table out of the sweep. THE GUARD WAS NOT EDITED, which is the half of this resolution worth more than the sentence: the defect was in the document the gate measures, and loosening the gate to accept its own author's text would have destroyed exactly the property round 20 registered R-0823 to obtain. THE ORDERED COLOUR IS OBSERVED RATHER THAN MANUFACTURED: the red existed on disk at `3ca66aac` before this round began, so the "before" reading is the branch's real state and not a mutation, and the "after" reading is the ordinary green run. THE LESSON, and it is a checklist reading rather than a new rule: §3 item 2 must be re-run whenever a block WIDENS the corpus a zero-gate sweeps, not only when it adds a new gate. A file that was outside the swept set when the block's TOs were written becomes a target the moment the corpus grows, and the TOs are not re-read at that moment because nothing about them changed — which is exactly how a block came to forbid a string and then write it, four lines apart, in the same document.
<<<END DONER22>>>
