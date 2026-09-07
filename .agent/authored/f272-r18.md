STEP T003 close + T004 scope — F272 One world completion — ROUND 18

EVERY RULE LINE IN THIS BLOCK IS EXACTLY SIX U+2500 CHARACTERS, so no run of
repeated characters in this frame has a length a reader has to recover by eye.

You are the WORKER for one round of docs/agents/self_drive_protocol.md.
AGENTS.md binds you in full: the self-review loop before EVERY commit, small
commits, `.agent/plan.md` current, a clean tree, a push at the end, and a
rewritten `.agent/handoff.md`. You write everything; the reviewer writes nothing
and will re-run every gate below itself before any verdict.

SESSION 9 of F272, round 18. The base of this round is `7b1590dc`. F272's soft
limit is 12 sessions and 40 rounds under operator amendment
amend0906-triage-throughput, so the feature is inside it and no scope report is
owed.

THIS ROUND SHIPS NO PRODUCTION CODE, and that is deliberate rather than thin. It
performs the ruling docs/agents/planner_reviewer_prompt.md §4 item 7 requires
when a spec is wrong — F272's Acceptance currently demands items another feature
owns — and it commits the MEASUREMENT that bounds T004, taken by running a probe
rather than by reading greps. Both are prerequisites for the next round, and
neither is a verdict, a registration or a correction, so operator amendment
amend0827 rule 1 is not engaged.

SANDBOX NOTES, so you do not rediscover them. Env-var assignment is denied in
every shell form — `VAR=x cmd`, `env VAR=x cmd` and `export VAR=x; cmd` all
fail — so set anything in-process through `os.environ`. `cp` is denied; copy
with `python3 -c "import shutil; shutil.copyfile(a, b)"`. The Bash tool does not
surface non-zero exits, so capture every gate's REAL code as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'` with NO pipe between the command and the
echo — a pipe reports the last stage's code, not the command's. Anything
involving counting, hashing or line endings is most reliable from a small
script file run as `python3 <path>`.

Goal
──────
Rule the boundary between F272's Acceptance and the 2026-09-06 triage, which
currently give the same five finding ids to two different features, so that
F272 can be closed self-consistently; record that T003 is complete; and commit
the probe-measured inventory that bounds T004's deletion.

Bundle, in this commit order
──────
C0a  save this block verbatim to `.agent/authored/f272-r18.md`
C0b  mirror the same bytes into `.agent/last_block.md`
C1   REPLACE `.agent/plan.md` with the PLANF272R18 slice
C2   APPEND the RECORDR18 slice to `.agent/live_review.md`
C3   APPEND the SLIPSR18 slice to `.agent/prose_slips.md`
C4   `docs/roadmap/features/T2_F272.md` — the ACCEPTPAIR replacement AND the
     DECISIONF272D12 append, both in this one commit
C5   NEW FILE `.agent/f272_t004_deletion_inventory.md`, written from the output
     of the INVPROBE script you run — a MEASUREMENT, not prose you compose
C6   rewrite `.agent/handoff.md`

Change set — these paths and nothing else
──────
  .agent/authored/f272-r18.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  docs/roadmap/features/T2_F272.md
  .agent/f272_t004_deletion_inventory.md
  .agent/handoff.md

Constraints
──────
1. A SLICE IS APPLIED BYTE FOR BYTE. Extract each one PROGRAMMATICALLY from
   `.agent/authored/f272-r18.md`, between its `<<<BEGIN NAME>>>` and
   `<<<END NAME>>>` lines. Never retype, reflow, re-indent or "correct" a slice.
   If a slice looks wrong, apply it anyway and DECLARE it in the handback.
2. NO MARKER LINE REACHES A TARGET FILE. After C5, the line-anchored count of
   `^<<<(BEGIN|END) .*>>>$` is 0 in each of `.agent/plan.md`,
   `.agent/live_review.md`, `.agent/prose_slips.md` and
   `docs/roadmap/features/T2_F272.md`. Measured by the reviewer at `7b1590dc`:
   that count is already 0 in all four, while `.agent/live_review.md` contains
   15 MID-LINE `<<<` substrings inside older records' prose. Those are
   PRE-EXISTING, they are not marker lines, and the line-anchored reading is the
   one that binds — round 14's accepted deviation 2 established exactly this.
3. ZERO finding ids are minted this round. The next free id is R-0823 and it
   stays free. The `job stop` prefix defect this round's DECISION mentions is
   NOT given an id: `- R-0809` already describes it and is OPEN, so §3 item 30
   forbids a second id for one defect.
4. C4 EDITS ONE FILE TWICE AND BOTH EDITS LAND IN THAT ONE COMMIT. Apply the
   ACCEPTPAIR replacement FIRST and the DECISIONF272D12 append SECOND, so the
   append's pre-image is the file the pair already produced.
5. READ `.agent/STOP` with `os.path.exists` at each of these points and report
   every reading: before C0a, before C4, and before C6. If it exists at any of
   them, finish the commit in flight, write the handoff, and stop.
6. C2 and C3 ARE EACH APPENDED AS `pre + b"\n" + slice`, against a pre-image you
   READ immediately before that write rather than one you assume.

The ACCEPTPAIR — a REWRITE, not an append
──────
Applied to `docs/roadmap/features/T2_F272.md`. The reviewer RAN the containment
test rather than judging it by eye, and records its output here:

    TO contains FROM verbatim: False   ->  therefore this pair is a REWRITE

Because it is a rewrite, the obligation is the FROM-zero count: after C4 the
FROM string occurs 0 times in that file and the TO string occurs exactly 1.
Measured by the reviewer at `7b1590dc`, the FROM string occurs exactly 1 time
there. The FROM deliberately spans forward to the `## Do not touch` heading, so
the insertion point is fixed by what FOLLOWS it and not by a line number.

<<<BEGIN ACCEPTPAIR_FROM>>>
task) and R-0812 (the narration table covers every emitted event kind).

## Do not touch
<<<END ACCEPTPAIR_FROM>>>

<<<BEGIN ACCEPTPAIR_TO>>>
task) and R-0812 (the narration table covers every emitted event kind).

THOSE FIVE IDS ARE F273'S AND NOT THIS FEATURE'S — see DECISION F272 D12 at the
end of this file, which rules the conflict between this section and the
2026-09-06 triage rather than leaving a reader to pick one. They are named above
so a reader can still find them by id.

## Do not touch
<<<END ACCEPTPAIR_TO>>>

Slices
──────

<<<BEGIN PLANF272R18>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 17 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001, T002 and now
T003 are COMPLETE.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Ruling the boundary this feature could not close over. F272's Acceptance names
five tests.md ids that the 2026-09-06 triage gives to F273 T001, and one of
them, R-0804, is the `ui_server.py` adapter that was the last unmoved item on
T003's list. DECISION F272 D12 rules the triage the winner, which closes T003 at
round 17's `job context` move and hands the cockpit adapter to F273. The same
round commits the probe-measured inventory that bounds T004.

## Next Steps

1. T004, the classic runner and the resolver collapse, staged from
   `.agent/f272_t004_deletion_inventory.md` rather than from any grep. That
   inventory is why T004 is many rounds and not one: 199 tracked files
   reference a classic job-store symbol by AST reading, 72 of them under
   `packages/` and `apps/`. DECISION F260 D5 keeps the resolver collapse in
   the SAME commit range as the store deletion.
2. T005, the reachability test and the cluster deletion. The Orchestrator
   brief's one hard rule: NEVER SPLIT INSIDE T005, so a session splits before
   it and never within it.

## Risks

- T004 is the largest remaining slice and its blast radius is measured rather
  than estimated. A round that tries to take it whole will exceed the
  DECISION F104 D1 insertion cap; the inventory exists to stage it.
- F272's soft limit is 12 sessions and 40 rounds under operator amendment
  amend0906-triage-throughput. At session 9 and round 18 the feature is
  inside it and no scope report is owed.
<<<END PLANF272R18>>>

<<<BEGIN DECISIONF272D12>>>
### DECISION F272 D12 (2026-09-07, F272 round 18) — the 2026-09-06 triage wins over this file's Acceptance, so the five tests.md ids are F273's; T003 is COMPLETE, and T004's blast radius is measured rather than estimated

CONTEXT. This file's "## Acceptance" section adopts `docs/roadmap/features/T2_F260.md`'s Acceptance list in full, and names five ids raised by the operator's tests.md run of 2026-09-05 — R-0803, R-0804, R-0807, R-0810 and R-0812 — as items of it. The 2026-09-06 triage recorded in `.agent/live_review.md` routes R-0803 through R-0812, those five among them, to **F273 T001** with the words "BOOK, do not build". F273 — Findings paydown v1 — is registered at `docs/roadmap/STATUS.md:40` and its file exists. So two live instruments give the same five ids to two different features, and F272 cannot be closed self-consistently while both stand. Round 16's handback named this and correctly declined to guess at it.

CHOSEN. THE TRIAGE WINS, and this feature's Acceptance is read as NOT requiring those five ids. Three reasons, none of them a preference. FIRST, the triage is the LATER instrument and the MORE SPECIFIC one: it was written on 2026-09-06 with all ten ids in front of it and assigned each to a task of a named feature, while this file's sentence names five of them in passing, to help a reader find them by id. SECOND, it is the instrument with somewhere to put them — F273 T001 exists, is unstarted, and is exactly "the findings owned by another feature". THIRD, and decisively, R-0804 asks for a COCKPIT change: `packages/orchestration/ui_server.py`'s `_JobPlanTaskAdapter` deleted rather than fixed, and every cockpit read endpoint answering 200 for a ping-pong-created job. This feature's own "## Do not touch" forbids it no more than the triage does, but F272's mandate is the JOB RECORD and its consumers, not the cockpit's rendering layer, and DECISION F272 D8 already had to rule on where a cockpit vocabulary change stops.

CONSEQUENCE, AND IT IS THE POINT OF THE RULING: **T003 IS COMPLETE.** Measured at `7b1590dc` over the consumer list `docs/roadmap/features/T2_F260.md`'s Design section names, `apps/cli/commands/job_context_cmd.py` was the last consumer this feature owed and round 17 moved it. Of the other three the re-grep found, `packages/orchestration/ui_server.py` is R-0804 and is F273's by this ruling; `apps/cli/commands/teach_cmd.py`'s `resolve_any_job_id` sites and `apps/cli/commands/job_stop_cmd.py`'s `_CoreJobAdapter` both belong to T004 by DECISION F260 D5, which places the resolver collapse in the same commit range as the store deletion because the collapse is a behaviour change to a shared error path and is harmless only once that store is gone. Nothing on T003's list is left unmoved and unassigned.

T004'S BLAST RADIUS, MEASURED AT `7b1590dc` AND NOT ESTIMATED, by the method DECISION F272 D7 established for the rename: an `ast` reading over every tracked `.py` from `git ls-files`, counting a file as a consumer only when it IMPORTS one of `save_job`, `load_job`, `load_job_safe`, `list_jobs`, `list_jobs_safe`, `JobNotFoundError` or `JobStoreError` FROM `packages.orchestration.storage`, or reads one of them off that module — so that same-stem names such as `load_job_plan` cannot be miscounted, which a substring grep does. The result is **199 files: 72 under `packages/` and `apps/`, 127 under `tests/`, and none under `scripts/`**, with `save_job` in 152 of them and `load_job` in 105. That is why T004 is MANY ROUNDS AND NOT ONE, and why the inventory is committed as `.agent/f272_t004_deletion_inventory.md` beside this ruling rather than re-derived per round: a 199-file deletion cannot be staged from a number nobody measured, and no single commit holds it under the DECISION F104 D1 cap of 500 insertions.

NOT RULED HERE. Whether F273 should ALSO inherit R-0805 through R-0811, which the same triage line routes to F273 T001 and which this file never named — those were never F272's and need no ruling. Nor is the ORDER of T004's rounds fixed here; the inventory bounds the work and the next block stages it.

A DEFECT FOUND WHILE MEASURING, DELIBERATELY NOT GIVEN AN ID. `remedy job stop --status <prefix>` exits 3 with a `job_not_found` document for a ping-pong job that exists, because `apps/cli/commands/job_stop_cmd.py` falls back to `resolve_job_id`, which searches the classic store alone; the same job's FULL id answers correctly. Proven by running the shipped handler at `7b1590dc`. No id is minted: `- R-0809` is OPEN and already describes this defect in these words — "a real id of the other store is rejected as unknown", with `Error: no job matches prefix 'f7dac0c55d474e4b'` as its own measured evidence — so §3 item 30 routes the new evidence to that finding rather than to a second one. R-0809 carries an acceptance line on `docs/roadmap/features/T2_F261.md` and is triaged to F273 T001, so it is not F272's to fix either.

ALTERNATIVES CONSIDERED. Reading this file's Acceptance as binding and building the five items here — rejected: it would have F272 delete the cockpit adapter that F273 T001 is registered to delete, which is two features owning one change, the exact defect this feature exists to remove. Referring the conflict to the operator — rejected by §4 item 7, which requires the reviewer to rule, record the ruling as operator-visible and proceed, because the operator's veto is any later relay and nothing waits for an answer. Editing the triage record instead — rejected outright: `.agent/live_review.md` is append-only and §3 item 20 forbids overwriting landed text.

REVERSE by deleting this section and the paragraph the same round added to "## Acceptance", at which point those five ids are claimed by both features again and F272 cannot close.
<<<END DECISIONF272D12>>>

<<<BEGIN RECORDR18>>>
Gate: F272 R17 — the F272 round 17 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `7b1590dc`. Range `5964aa76`..`7b1590dc`, seven commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, with the change set exactly the seven ordered paths and nothing else, `git status --porcelain` empty and every commit's insertions under the DECISION F104 D1 cap of 500 at a maximum of 392. G1 TRANSPORT IS A REAL CHAIN AND NOT MERELY SELF-CONSISTENT: the reviewer's own scratch original `.remedy-wt/f272-r17-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r17.md` and `.agent/last_block.md` are all 26723 bytes at 392 lines and all hash to `eea9a264fe7d48826689f97d9865d75114aea08cb0962adef0e97acc1e835d6f`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces on every reader: `.agent/live_review.md` 1157784 to 1163718, the pre-image a byte-exact prefix of the post-image, `post == pre + NL + slice` TRUE, N counted from the slice as 2 with units 715 to 717 and the last 2 equal to the slice's paragraphs in order, a byte flipped in the FIRST appended paragraph rejected by BOTH readers and accepted by both once restored with the on-disk digest unmoved; and all seven ordered counts reproduce exactly — registrations 306 unchanged, resolutions 248 to 249, open set BY DISTINCT ID 58 to 57, `^Gate: ` 39 to 40, `^Gate: F272 R16 ` 0 to 1, `^Done: R-0822 ` 0 to 1, and `^Landed: R-0822 ` 1 to 1, which is the DECISION F272 D10 reading that the `Landed:` line SURVIVES beside the resolution rather than being written over. G3 THE PLAN is 2167 bytes byte-equal to its slice at 44 lines against the cap of 50. G4 THE MOVE IS REAL, run against the SHIPPED module rather than read: with a `JobPlan` persisted through `save_job_plan`, `_cmd_job_context(job_id, task_ref="T001", json_output=True)` raised NOTHING and printed `job_id` equal to the minted 16-hex id, `task_id` and `task_label` both `T001`, `fenced_paths` `['alpha.py']` and the fenced file at tier 1 with its import neighbour at tier 2; a classic UUID job in the same data root still answers with its own UUID as `job_id`, its task's UUID as `task_id` and `T001` as its label, so no regression; an unknown short hex exits 1 with `Error: no job matches prefix`, an unknown UUID exits 1 with `Job not found:`, and a unified job with an empty `repo_path` exits 2 with `has no target_repo attached`, so all three documented exit paths hold across both stores; and over that file `resolve_job_id(` is 0 while `resolve_any_job_id(` is 1. G5 THE SUITES, re-run serially by the reviewer: `tests/cli/` EXIT 0 at 1541 passed, reconciled rather than asserted — an `ast` count of `tests/cli/test_job_context_cmd.py` gives 9 test functions at `7b9bf290` and 12 at `335be882`, so 1538 + 3 = 1541 and the difference is 0; `tests/ui_server/` EXIT 0 at 515; `tests/orchestration/test_test_runner.py` EXIT 0 at 52; `tests/regression/test_resource_safety.py` EXIT 0 at 21; `tests/orchestration/test_integrity_gate.py` EXIT 0 at 16; `tests/cli/test_golden_path.py` EXIT 0 at 42 — the last five identical to the base the reviewer measured at `5964aa76`, so nothing regressed. G6 THE RED-PROOF was re-run by the reviewer in its own disposable worktree detached at `335be882`, with zero `__pycache__` directories under it before any run, `python3 -B` throughout, and provenance confirmed to resolve INSIDE the worktree so no editable install could shadow it; the ORDERED COLOUR is control-first and reads EXIT 0 at 12 passed, then with C3's file ALONE reverted to its `5964aa76` blob EXIT 1 at 2 failed and 10 passed, the two failures being exactly `test_a_ping_pong_created_job_compiles_context_like_a_classic_one` and `test_a_ping_pong_job_without_a_repo_path_exits_two` and carrying the real defect `Error: no job matches prefix` for a job that exists, then EXIT 0 at 12 passed restored; `test_an_unknown_job_of_either_shape_still_exits_one` PASSED in the reverted run exactly as the block predicted, because it is a regression pin rather than a discriminator, and the block said so before the run. G7 ruff EXIT 0 `All checks passed!` over both changed files and integrity EXIT 0 with `"passed": true`, `"fail_count": 0` and `"check_count": 5`. G8 THE TREE: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, and thirteen worktree entries being the primary plus the twelve pre-existing `remedy/job-*`. THE GUARD SLICE LANDED BYTE-IDENTICAL TO THE REVIEWER'S OWN DRY-RUN BYTES, sha256 `ff2aff4ed6b9ee17de81ada420962c66989fc570283a103b4e9924c83979765d`, which is the strongest form this proof takes: the tests the reviewer ran in a worktree BEFORE authoring are the tests on disk. THE WORKER'S TWO DECLARED DEVIATIONS ARE BOTH UPHELD AND NEITHER SPENDS AN ID. Deviation 1, correcting the module docstring's claim that the fenced scope is "exactly the task's `inputs["flight"]["files_hint"]`", is IN SCOPE and right: S5 falsified that sentence exactly as S6 says S4 falsified `_task_label`'s, and leaving it would have put a false sentence in the file the change was made in. Deviation 2 reports the insertion counts differing from the reviewer's dry run — 62 and 10 against 56 and 15 — and changed nothing to make them agree, which is what the block ordered; the reviewer read the whole diff and the difference is comment wrapping and deviation 1, with no behavioural line differing from the dry run. Its three assumptions are accepted AS assumptions: the C4 separator was derived from the target's own two-blank-line convention and is confirmed by the slice landing byte-identical; the Commit Gate reading at C0a and C0b is the conservative one; and placing `resolve_any_job_id` inside the existing `try` is behaviour-neutral, which the reviewer confirmed BY RUNNING it rather than by reading — the resolver's `SystemExit` propagates past an `except JobNotFoundError` and the short-hex exit 1 still carries the resolver's own message.
<<<END RECORDR18>>>

<<<BEGIN SLIPSR18>>>
2026-09-07, F272 round 17 — the block's production SPEC was inconsistent about docstrings it falsified: S6 ordered `_task_label`'s docstring corrected because the change made it wrong, while S4 widened `_task_planned_id` and left its docstring still attributing the planned id to `map_flight_plan_to_tasks` alone, and S5 widened `_task_files_hint` while the module docstring still said the fenced scope is exactly the flight block. The worker caught the module-docstring case and spent a declared deviation on it; nothing wrong reached disk that the round did not also fix, so no id is spent. The lesson for the next SPEC that widens an accessor: sweep every docstring the widening falsifies, not the one the reviewer happened to notice.
<<<END SLIPSR18>>>

<<<BEGIN INVPROBE>>>
"""Bound T004 by SYMBOL, not by substring.

For every tracked `.py`, decide by `ast` whether it references a CLASSIC job
store name: it counts only when the file imports one of the names below FROM
`packages.orchestration.storage`, or reads one of them off that module object.
A substring grep cannot do this — `load_job_plan` contains `load_job` and is the
UNIFIED reader, the opposite of what is being counted.
"""
import ast
import collections
import pathlib
import subprocess

R = pathlib.Path("/home/decodeux/Repos/remedy")

SYMS = {"save_job", "load_job", "load_job_safe", "list_jobs", "list_jobs_safe",
        "JobNotFoundError", "JobStoreError"}

# `git ls-files` is the enumeration DECISION F272 D2 requires — never a shell
# glob. The BYTES then come from the working tree rather than from a revision:
# the tree is clean at every commit boundary of this round, so the two agree,
# and reading the tree avoids naming a revision that re-resolves as the round
# proceeds (the identifier §3 item 20 forbids in anything durable).
files = subprocess.run(["git", "-C", str(R), "ls-files", "*.py"],
                       capture_output=True).stdout.decode().split()

prod, tests, scripts = {}, {}, {}
for rel in files:
    src = (R / rel).read_text(encoding="utf-8", errors="replace")
    if "storage" not in src:
        continue
    try:
        tree = ast.parse(src)
    except SyntaxError:
        continue
    used, modaliases = set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.endswith("orchestration.storage"):
                for a in node.names:
                    if a.name in SYMS:
                        used.add(a.name)
            elif node.module.endswith("packages.orchestration"):
                for a in node.names:
                    if a.name == "storage":
                        modaliases.add(a.asname or "storage")
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.endswith("orchestration.storage"):
                    modaliases.add(a.asname or "storage")
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) \
                and node.value.id in modaliases and node.attr in SYMS:
            used.add(node.attr)
    if not used:
        continue
    bucket = tests if rel.startswith("tests/") else (
        scripts if rel.startswith("scripts/") else prod)
    bucket[rel] = sorted(used)

print("production %d" % len(prod))
print("tests %d" % len(tests))
print("scripts %d" % len(scripts))
print("total %d" % (len(prod) + len(tests) + len(scripts)))
freq = collections.Counter()
for d in (prod, tests, scripts):
    for v in d.values():
        freq.update(v)
for s, n in freq.most_common():
    print("symbol %s %d" % (s, n))
for label, d in (("PROD", prod), ("TEST", tests), ("SCRIPT", scripts)):
    for rel, syms in sorted(d.items()):
        print("%s %s %s" % (label, rel, ",".join(syms)))
<<<END INVPROBE>>>

C5 — what the inventory file must contain
──────
Save the INVPROBE slice to `.remedy-wt/f272_t004_probe.py` — which is gitignored
and is NOT part of the change set — and RUN it with `python3` from the primary
checkout. Then write `.agent/f272_t004_deletion_inventory.md` carrying, in your
own words for the prose and the probe's own output for the numbers:

  * a title naming the feature, the task and the commit the reading was taken
    at, which is the C4 commit's SHA;
  * WHAT WAS COUNTED and WHY BY AST — that a file counts only when it imports
    one of the seven names from `packages.orchestration.storage` or reads one
    off that module, and that a substring grep miscounts because `load_job_plan`
    contains `load_job` and is the UNIFIED reader;
  * the three bucket counts and the total, verbatim from the probe;
  * the per-symbol frequency table, verbatim from the probe;
  * the full PROD list, one file per line with the symbols each uses, verbatim
    from the probe — never truncated, never summarised;
  * the full TEST list in the same form, likewise never truncated;
  * one closing paragraph stating that this is a MEASUREMENT and not a plan, and
    that the staging of T004 into rounds is the next block's job.

Do not sort, filter, abbreviate or "tidy" the probe's output. If a list is long,
that length is the finding.

Done when — every gate below is RUN, with its REAL exit code recorded
──────
Run G1 through G7 BEFORE C6, so the handback can quote them.

G1 TRANSPORT — ONE digest comparison. `.remedy-wt/f272-r18-block.md`,
   `.agent/authored/f272-r18.md` and `.agent/last_block.md` share ONE sha256,
   ONE byte length and ONE line count. Hash the source file on arrival, BEFORE
   any other work, and report the three figures. C0a and C0b are both
   `shutil.copyfile` of that source — a byte copy, never a retype.

G2 THE RECORD — the readers below, over the C2 append, each reported separately.
   (a) BYTE: report the pre-image's length, sha256, terminal twelve bytes and
       trailing-newline run; then that `pre` is a byte-exact PREFIX of `post`
       and `post == pre + b"\n" + slice`.
   (b) STRUCTURAL: strip the file's single terminal newline BEFORE splitting on
       blank lines, and say so. N is COUNTED BY YOUR SCRIPT from the slice's own
       blank-line paragraphs and is never taken from this block. Report the unit
       count before and after, that the LAST N units equal the slice's N
       paragraphs IN ORDER, and that everything before them is unchanged.
   (c) NEGATIVE CONTROL on the FIRST appended paragraph: flip one byte inside it
       IN MEMORY and never on disk, and report that reader (a) rejects, reader
       (b) rejects, both accept once restored, and the on-disk sha256 is
       identical before and after the control.
   (d) COUNTS, before C2 and after C2, every one measured:
           ^- R-\d{4} distinct        306 -> 306
           ^Done: R-\d{4} distinct    249 -> 249
           open set BY DISTINCT ID     57 ->  57
           ^Gate:                      40 ->  41
           ^Gate: F272 R17              0 ->   1
       Where any measurement differs from these figures, REPORT THE DIFFERENCE
       and adjust nothing to make them agree.
   Run the same byte reader (a) over the C3 append to `.agent/prose_slips.md`
   and report it on its own line; that file gets no structural proof and no
   control, per the amend0827 rule 5 gate budget.

G3 THE PLAN — `.agent/plan.md` byte-equals the PLANF272R18 slice; report its
   byte length and its line count against the AGENTS.md cap of 50, and that
   `## Goal` and `## Next Steps` are both present.

G4 THE FEATURE FILE — over `docs/roadmap/features/T2_F272.md`, all measured:
   the ACCEPTPAIR_FROM string occurs 1 time BEFORE C4 and 0 times after; the
   ACCEPTPAIR_TO string occurs 0 times before and exactly 1 after; the
   DECISIONF272D12 slice was appended as `pre + b"\n" + slice` against the
   pre-image the pair produced, and `post == pre + b"\n" + slice` is TRUE for
   that second edit; the count of lines matching `^### DECISION F272 D` goes
   from 11 to 12; and `D12` appears in exactly one heading. Report the file's
   byte length and line count before and after.

G5 THE INVENTORY — re-runnable, which is the whole point. Report the probe's
   three bucket counts, its total and its per-symbol frequency table as the
   probe printed them, and report that every line of the probe's PROD and TEST
   output appears in `.agent/f272_t004_deletion_inventory.md`. State the count
   of PROD lines and TEST lines in the committed file and that they equal the
   probe's. The reviewer measured this at `7b1590dc` as production 72, tests
   127, scripts 0, total 199, with `save_job` 152 and `load_job` 105; report
   what YOU measure and change nothing to agree.

G6 THE DOCS ROUND GATE plus the canary — this round's change set includes
   `docs/roadmap/**`, so both are mandatory:
       python3 -B -m pytest tests/docs/ -q -p no:randomly
       python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
   The reviewer measured 303 and 42 respectively at `7b1590dc`, both EXIT 0.
   Report the real exit codes and counts; report any difference and change
   nothing.

G7 INTEGRITY — `python3 -m apps.cli.grouped integrity check --json`. Report the
   real exit code, `passed`, `fail_count` and `check_count`. Do not edit a
   finding to move any of them. No `.py` under `packages/`, `apps/` or `tests/`
   is in this round's change set, so no ruff run is ordered over the change set;
   if you touch a `.py` anywhere outside `.remedy-wt/`, that is a deviation and
   you lint it and say so.

G8 THE TREE — run `git status --porcelain` at EVERY commit boundary and report
   its real output each time; it must be empty every time and empty at the end.
   Report `git ls-files .remedy-wt` (expected empty) and `git worktree list`
   (expected 13 entries: the primary plus twelve pre-existing `remedy/job-*`).
   Then the per-commit insertion counts from
   `git diff --numstat <parent> <commit>`, C6 EXCLUDED because a handback cannot
   count its own insertions, each against the DECISION F104 D1 cap of 500 —
   which counts INSERTIONS only. Report the `.agent/STOP` readings constraint 5
   orders.

Handback
──────
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has NO
length cap. It must carry: the SESSION NUMBER (9) and the round (18); the range
and the branch; a per-commit changed-files table whose `+/-` column is taken
from `git diff --numstat` and NOT from any file's line counts, matching G8's
readings cell for cell; an item-status table holding every one of C0a, C0b, C1,
C2, C3, C4, C5, C6 exactly once as done, skipped or deviated with a reason; the
open-findings count BY DISTINCT ID with the arithmetic that produced it; ONE
LINE PER GATE carrying its real exit code; every deviation and assumption; the
external actions you took; and one sentence of context self-assessment, which
operator amendment amend0905-throughput requires in the Session section.

DO NOT create a PR. DO NOT merge anything. DO NOT force-push. Push the branch
and stop.
