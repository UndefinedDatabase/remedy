STEP CLOSURE 3/4 — F272 — round 28 — the self-use precondition: generate, plan, RUN, and report the defects

Base commit for every reading in this block: `b865f001`, the round 27 handback commit.
Every separator line below is exactly twenty `=` characters.

====================
Goal
====================

CLOSURE PRECONDITION 6 of `docs/roadmap/STATUS_closure_protocol.md`: exactly one self-use
item is consumed by this close. Remedy is used on Remedy, and that precondition exists
because "Remedy is used on Remedy" rots the moment it depends on someone remembering.

THE QUEUE HOLDS NO PENDING ITEM. All eleven items in `scripts/self_use_queue.json` carry a
non-empty `consumed_by` — SU-001 through SU-011, spent by F257, F258, F106, F108, F109,
F110, F112, F114, F262, F259 and F260. Precondition 6 says that when the queue holds no
pending item the session calls
`packages.orchestration.self_use_generator.generate_and_append_if_empty` FIRST, and only
if THAT also answers `None` is the track exhausted.

THE REVIEWER RAN THAT GENERATOR AS A PURE PROBE at `b865f001` and it does NOT answer
`None`: its Tier 1, the oldest open Low or Medium finding in `.agent/live_review.md`,
offers `SU-012`, "Address ledger finding R-0445", provenance
`generated (self-use-generator tier 1, ledger scan, R-0445)`, with 2486 characters of job
markdown. The probe wrote nothing — `pending_self_use_items` read 0 before and 0 after and
`git status --porcelain` was empty — because `generate_self_use_item` and
`append_generated_item` are separate seams. So the track is NOT exhausted and this round
consumes a real item.

R-0445 is a fitting one to have drawn. It is the standing defect that the canonical
integration-gate procedure manufactures false base failures on every run, and round 27
measured exactly that: 126 base-only failures, every one attributed to a stale
`apps/ui/dist/index.html`, all 126 re-running green once the staleness alone was removed.

THIS ROUND DOES NOT REGISTER THE FINDINGS THE RUN PRODUCES, AND THAT IS DELIBERATE.
Precondition 6 requires every string
`packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the
run's own `JobPlan` to be registered as a normal R-id finding. Only reviewer-authored text
may register a finding (planner_reviewer_prompt.md §4 item 4), and the reviewer cannot
author text for strings that do not exist until this run produces them. So THIS round runs
and REPORTS them verbatim; the NEXT round registers them in reviewer-authored text. Do not
invent an R-id, do not write a `- R-XXXX` line, and do not write a `Done:` paragraph. The
next free id is `R-0826` and it must still be free when this round ends.

====================
Bundle
====================

C0a  save this block verbatim to `.agent/authored/f272-r28.md`
C0b  mirror the same bytes to `.agent/last_block.md`
C1   `.agent/plan.md` replaced byte for byte with PLANF272R28
C2   `.agent/live_review.md` — append RECORDR28, the round 27 PASS gate entry
C3   `.agent/prose_slips.md` — append SLIPSR28, one dated line
C4   `scripts/self_use_queue.json` — the SU-012 append, written BY THE SHIPPED FUNCTION
C5   the self-use evidence directory `.agent/selfuse_f272_r28/`
C6   `.agent/handoff.md` rewritten

====================
Change set — exactly these paths and nothing else
====================

    .agent/authored/f272-r28.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    scripts/self_use_queue.json
    .agent/selfuse_f272_r28/                 (NEW DIRECTORY, created by C5)
    .agent/handoff.md

NOTHING under `packages/`, `apps/`, `tests/` or `docs/` changes this round, and no STATUS
line is touched. No production line moves, so no red-proof is ordered or possible. The run
at G5 writes into the data root `/home/decodeux/Repos/remedy/.data`, which `.gitignore`
line 211 excludes, so it cannot dirty the tree; if it nonetheless does, APPLY NOTHING,
STOP and report. If a measurement forces a path outside this list, APPLY IT AND DECLARE IT.

====================
Constraints
====================

1. This block is applied verbatim. If a slice is wrong, apply it as written and declare
   the disagreement; never silently correct it.
2. Every authored slice is extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f272-r28.md`, between its `<<<BEGIN NAME>>>` and `<<<END NAME>>>`
   lines, exclusive of both marker lines and INCLUSIVE of the newline ending its last
   content line. This round carries no FROM/TO pair. Never retype a slice.
3. C0a and C0b are `shutil.copyfile` of `.remedy-wt/f272-r28-block.md`.
4. BOTH APPENDS TO PROSE ARE `post == pre + b"\n" + slice`. Each target ends in EXACTLY ONE
   newline at the base commit, measured per file: occurrences of three consecutive newlines
   at `b865f001` are 0 in `.agent/live_review.md` and 1 in `.agent/prose_slips.md` (offset
   39213, pre-existing). Neither is load-bearing and neither is repaired.
5. C4 IS WRITTEN BY THE SHIPPED FUNCTION AND NEVER BY HAND. Call
   `packages.orchestration.self_use_generator.generate_and_append_if_empty()` with no
   arguments so it resolves the repository's own queue, and commit whatever it writes. Do
   NOT hand-edit the JSON, do NOT set `consumed_by`, and do NOT reformat the file. The
   `consumed_by` edit that names F272 belongs to the CLOSURE commit, which is a later
   round, and setting it here would consume the item before it has been run.
6. THE RUN USES A REAL PROVIDER AND NEVER `fake`. `resolve_role_config` answers `ollama`
   with model `muse-glimmer:latest` for both `builder` and `reviewer`, measured by the
   reviewer at `b865f001`, and the ollama daemon answered `/api/tags` with 8 models
   including that one. Call `run_next_self_use_item` WITHOUT `builder_name` or
   `reviewer_name` so it resolves the product default itself. If it raises
   `SelfUseRunError` because no usable real provider resolves, STOP and hand back — do NOT
   fall back to `fake`, because a `fake` run does not exercise the product and a
   precondition met by a fake run is a precondition not met.
7. THE RUN GOES TO THE APPROVAL GATE AND IS NEVER APPLIED. `JOB_COMPLETED` and
   `JOB_BLOCKED` are both legitimate outcomes and neither is a failure of this round.
8. THE PRODUCT CREATES ITS OWN WORKTREE AND THAT IS EXPECTED, NOT A GUARDRAIL BREACH.
   `packages/orchestration/worktrees.py` runs every job inside
   `<repo>/.remedy-wt/job-<job-id>` on branch `remedy/job-<job-id>`. `git worktree list` is
   13 entries at the base — the primary plus twelve pre-existing `remedy/job-*` left by
   earlier runs — and will read 14 after the run. DO NOT REMOVE IT and do not remove any of
   the twelve: they are product state, not verification scratch, and every earlier
   self-use closure left its own in place. YOU MAY CREATE NO OTHER WORKTREE; the
   self_drive_protocol.md G5 prohibition binds your own verification, not the product's.
9. THIS ROUND MINTS NO FINDING ID, per the Goal's last paragraph. `R-0826` is the next free
   id and must still be free when the round ends: `^- R-0826 ` is 0 at the base and must be
   0 at the end.
10. Read `.agent/STOP` with `os.path.exists` before C0a, before C4 and before C6, and
    report all three readings.

====================
Done when — the gates
====================

Run every gate with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, NO PIPE between the command and
the echo — a pipe reports the exit code of the pipeline's last stage and not of the command
you meant to read. Report ONE LINE PER GATE with the transcripts below it. Every gate runs
before C6, the commit that writes the handback.

G1 TRANSPORT. One digest comparison: `.remedy-wt/f272-r28-block.md` as delivered against
   the committed `.agent/authored/f272-r28.md` and the committed `.agent/last_block.md`.
   Report sha256, byte length and line count for each of the three.

G2 THE FINDING RECORD, over the single append at C2, against its own pre-image.
   (a) BYTE: pre_len, pre_sha256, post_len, post_sha256, the terminal twelve bytes and
       trailing-newline run of each, `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and
       `POST_EQUALS_PRE_NL_SLICE`. At the base the pre-image is 1220698 bytes, 2135 lines,
       sha256 beginning `0f2924505f470394`.
   (b) STRUCTURAL: strip the single terminal newline, split on blank lines, compare the
       LAST N units against the slice's paragraphs IN ORDER, where N is COUNTED BY YOUR
       SCRIPT from the slice and never taken from this block. Report N, units before, units
       after and `EVERYTHING_BEFORE_UNCHANGED`.
   (c) NEGATIVE CONTROL on the FIRST paragraph the append adds, in memory only, never on
       disk: flip one byte, require BOTH readers to reject it, then re-read the file and
       confirm it is byte-identical to the real post-image.
   (d) COUNTS, each measured, none adjusted to agree:
           ^- R-\d{4} distinct        309 -> 309
           ^Done: R-\d{4} distinct    252 -> 252
           open set BY DISTINCT ID     57 ->  57
           ^Gate:                      50 ->  51
           ^Gate: F272 R27              0 ->   1
           ^- R-0826                    0 ->   0
       Report OPEN FINDINGS BY DISTINCT ID with its arithmetic.

G3 THE TWO PROSE FILES. `.agent/plan.md` is byte-equal to PLANF272R28; report its bytes,
   its line count against the AGENTS.md cap of 50, and that `## Goal` and `## Next Steps`
   are both present. `.agent/prose_slips.md` gets the byte append check only — pre_len
   151498 and pre_lines 565 at the base, and `POST_EQUALS_PRE_NL_SLICE` for SLIPSR28.

G4 THE QUEUE, over C4. At the base `scripts/self_use_queue.json` is 33722 bytes at 94 lines
   and holds 11 items, every one with a non-empty `consumed_by`, and
   `pending_self_use_items()` is empty. Report, from the SHIPPED readers and not from your
   own JSON parsing where a shipped reader exists:
       item count           11 -> 12
       the appended id, its title, its provenance, and its `consumed_by`, which MUST be
       the empty string
       `next_self_use_item()` answers the appended id
       `pending_self_use_items()` length 0 -> 1
       `body["schema_version"]` is 2 both before and after
   The reviewer's probe named SU-012, "Address ledger finding R-0445"; REPORT WHAT YOU
   MEASURE, and a different id is a DECLARED DEVIATION rather than a stop, because the
   generator reads a ledger this round's own C2 has already appended to.

G5 THE RUN — the gate this round exists for.
       from packages.orchestration.self_use_runner import run_next_self_use_item
       entry, job_file_path, result = run_next_self_use_item(dest_dir, repo_path=".")
   with `dest_dir` inside `.agent/selfuse_f272_r28/`. Report ALL of:
   (a) the entry id, the job file path, and the job file's byte length and sha256;
   (b) `result.state` — the literal value — and `result.job_id`;
   (c) `result.execution_config`, and from it WHICH PROVIDER ACTUALLY RAN. A value of
       `fake` anywhere in the builder or reviewer provider is a STOP under constraint 6;
   (d) the wall-clock time of the call and the provider-call count if the result carries
       one;
   (e) `describe_self_use_run_defects(result)` — its tuple LENGTH, and then EVERY STRING IT
       RETURNS, VERBATIM AND IN FULL, NEVER TRUNCATED AND NEVER SUMMARISED. This is the
       single most important output of the round: the next round's findings are authored
       from these exact strings, so a paraphrase costs a round. An empty tuple is a
       legitimate result and means there is nothing to register — report `()` and say so
       explicitly rather than leaving the reading absent.
   Write (a) through (e) into `.agent/selfuse_f272_r28/` as `.txt` files at C5, together
   with the job file itself. Every evidence file is named `.txt` and NEVER `.log`:
   `.gitignore` drops `*.log` silently and the review-zip guard rejects any `\.log$`
   member (R-0169).

G6 THE SUITES. In the primary checkout at C5, run serially and report each exit code and
   count:
       python3 -B -m pytest tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_job.py tests/orchestration/test_self_use_runner.py -q -p no:randomly
       python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
   The reviewer ran the first in a disposable worktree with C4's append applied and
   measured 72 passed at exit 0, and confirmed the gate can FAIL by corrupting the appended
   id to `SU-12` in that same worktree, which reddened 5 of
   `tests/orchestration/test_self_use_queue.py` including
   `test_shipped_ids_are_unique_and_match_the_pattern`. The canary measured 42 at
   `b865f001`. REPORT WHAT YOU MEASURE.

G7 THE TREE. `git status --porcelain` EMPTY at every commit boundary with the real output
   each time — the run's own writes go to the gitignored `.data/` and `.remedy-wt/`, so an
   empty reading is the expected one and a non-empty reading is a STOP. `git ls-files
   .remedy-wt` empty. `git worktree list` 13 before the run and 14 after, the new entry
   being the product's own `remedy/job-*`, which is NOT removed per constraint 8; name it.
   Per-commit insertions from `git diff --numstat <parent> <commit>` for C0a through C5 —
   C6 excluded, because a commit cannot count its own insertions while it is being written
   — each under the DECISION F104 D1 cap of 500. The three `.agent/STOP` readings.

====================
Handback
====================

Rewrite `.agent/handoff.md` completely: `SESSION 12 of feature F272 · round 28 · rounds so
far 28`; the soft-limit reading; one sentence of context self-assessment; the range; a
per-commit changed-files table whose `+/-` column comes from `git diff --numstat` and is
compared cell for cell against G7's figures; the item-status table for C0a through C6; one
line per gate with the transcripts below it; every deviation and assumption. It has no
length cap.

IT MUST ALSO CARRY, IN ITS OWN SECTION, THE COMPLETE G5(e) OUTPUT — every defect string
verbatim, or the explicit statement that the tuple was empty. `.agent/handoff.md` is the
only return channel this workflow has, so a string that is not in it does not reach the
round that must register it.

<<<BEGIN PLANF272R28 target=.agent/plan.md>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 27 PASSED except round 2 (premise
corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round 22). T001, T002 and
T003 are COMPLETE; T004's remainder and T005 are F274's, split off in round 26 by DECISION
F272 D16.

## Goal

Close F272 at the self-consistent scope DECISION F272 D16 fixed. Session 12 reached the
soft limit of 12 sessions, so the remaining work is the closure sequence of
`docs/roadmap/STATUS_closure_protocol.md` and no further building.

## Current Step

Round 28, closure precondition 6: the self-use item. The queue holds no pending item, so
`generate_and_append_if_empty` supplies one from its ledger tier, and the round plans it
and RUNS it to the approval gate under the product's own provider. The defects the run
reports are carried to the next round in the handback, because only reviewer-authored text
registers a finding.

## Next Steps

1. Register every string `describe_self_use_run_defects` returned, in reviewer-authored
   text, starting at the next free id `R-0826`. An empty tuple means nothing to register.
2. The evidence job and a FRESH review zip. Its `base_commit` is the FORK POINT
   `b18fad57`, never `git merge-base`, which differs on this branch and packages
   BLOCKED_EVIDENCE.
3. Ledger rotation by `scripts/rotate_live_review.py`, as its own commit, after the verdict
   bookings and before the STATUS flip.
4. The closure commit: the STATUS `[x]` line, the README capability sync and SU-012's
   `consumed_by` in the SAME commit, then the PR. The PR is NOT merged this session.

## Risks

- Four open findings are High — R-0803, R-0804, R-0806 and R-0807 — all four booked to
  F273's T001 by the 2026-09-06 triage. The close is PASS_WITH_RISKS and names them.
- A failing review-zip build is a closure BLOCKER; the round that hits one stops.
- Precondition 2 is MET: round 27's integration gate found zero branch-only failures, with
  all 126 base-only ids attributed and a repaired control re-running them green.
<<<END PLANF272R28>>>

<<<BEGIN RECORDR28 target=.agent/live_review.md mode=append>>>
Gate: F272 R27 — the F272 round 27 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `b865f001`. THIS IS F272'S INTEGRATION-GATE ROUND AND IT DISCHARGES CLOSURE PRECONDITION 2, which was genuinely unmet before it: at `412ce673` the ledger held 26 `Gate: F272 ` entries and not ONE of them claimed the full suite, measured as zero matches of `^Gate: F272 R.*full suite`. Range `412ce673`..`b865f001`, eight commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with `git diff --name-only` naming exactly the fifteen declared paths and nothing under `packages/`, `apps/`, `tests/`, `scripts/` or `README.md`. G1 TRANSPORT IS A REAL CHAIN: the reviewer's own scratch original `.remedy-wt/f272-r27-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r27.md` and `.agent/last_block.md` are all 24499 bytes at 319 lines and all hash to `94e540c1ae7a3f167be0321e8c3d1e43a629ead7282123a01e2196ad303b8ef2`; per §3 item 37 that chain covers those artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD: 1215841 to 1220698 bytes, pre-image a byte-exact prefix, `POST_EQUALS_PRE_NL_SLICE` true, structural N counted from the slice as 1 with units 732 to 733 and everything before unchanged, and a byte flipped inside the FIRST appended paragraph rejected by BOTH readers while both accept the real post-image; registrations 309 unchanged, resolutions BY DISTINCT ID 252 unchanged, open set 57 unchanged, `^Gate: ` 49 to 50, `^Gate: F272 R26 ` 0 to 1, `^- R-0826 ` 0 to 0. G3 THE PROSE FILES: the plan is 1988 bytes at 39 lines against the cap of 50 and byte-equal to its slice. G4 THE FEATURE FILE gained its Built State section: 62897 to 66178 bytes with the pre-image a byte-exact prefix, `### DECISION F272 D` headings 15 to 15 because the slice carries none, and `^## Built State` 0 to 1 — so closure precondition 4 is discharged too, and the section names which slices moved to F274 and points a reader at DECISION F272 D16 in `.agent/decisions.md`. G5 THE BRANCH RUN, RE-RUN BY THE REVIEWER AT `b865f001` AND NOT MERELY READ: `python3 -B -m pytest -n auto -q` exits 0 at 19786 passed, 23 skipped, 1 warning in 138.13s, with a `^FAILED` count of ZERO, reproducing the worker's 19786/23/0 at 115.98s cell for cell on every count. G6 THE BASE RUN was taken at the FORK POINT `b18fad576252f7f2739a5807b6408031da8fcde6` and never at `git merge-base`, which differs on this branch: at the fork point `rev-list --ancestry-path` and plain `rev-list` both answer 213, while at the merge-base `148fbd0b` they answer 184 and 205 — the unequal shape that packaged F260's round 22 attempt as BLOCKED_EVIDENCE, and the reviewer measured both independently. Artefact parity was restored with `shutil.copytree(src, dst, symlinks=True)`, the argument ordered rather than the function, preserving 27 symlinks against the primary's 27; the R-0444 event measurement reports zero files under `apps/ui/dist` with an mtime inside the 167.35s run window and zero with a changed mtime, so the parity claim HOLDS by measurement of the event rather than of the outcome. G7 THE COMPARISON IS THE VERDICT AND IT IS CLEAN: `comm -13` gives ZERO branch-only ids, with the committed `branch_failed.txt` a zero-byte file, which is what a branch run of zero failures must produce. The 126 base-only ids, all under `tests/ui_server/`, are attributed to ONE class by direct evidence rather than by assertion: every one carries the identical error `Failed: Server did not start in time`, the named stale artefact is `apps/ui/dist/index.html` whose copied mtime predates the `git worktree add` stamp on all 142 `apps/ui/src` files, so `_frontend_is_stale()` is True while `REMEDY_UI_NO_AUTO_BUILD=1` suppresses the rebuild — AND THE WORKER PROVED IT RATHER THAN ARGUING IT, re-running the same 126 ids in the same worktree at the same commit with only the staleness removed and no code change, at exit 0 and 126 passed in 2.78s. That is the strongest form this attribution has ever taken in this repository, and it is the same defect the open finding R-0445 describes. G8 THE TREE: porcelain empty at every boundary, `git ls-files .remedy-wt` empty, worktrees 13 to 14 to 13 with the throwaway branch deleted and no `tmp/*` branch surviving, per-commit insertions 319, 243, 25, 2, 2, 51 and 461 for C0a through C5, every one under the DECISION F104 D1 cap of 500; C6 is 637 insertions and is the verbatim rewrite of a SINGLE `.agent/**` state file, `.agent/handoff.md` being its only path, which DECISION F104 D1 exempts by name. THE WORKER'S ONE DECLARED DISAGREEMENT IS UPHELD AND IT IS THE REVIEWER'S ERROR: the block's Goal said the ledger held `Gate: F272 R1` through `Gate: F272 R26` at the base, and the reviewer confirms 26 entries whose HIGHEST is R25, `^Gate: F272 R26 ` reading 0 there because this round's own C2 adds it. The load-bearing half of that sentence — that no entry claimed the full suite — is true and measured at zero. Reviewer prose that reached no product state, so one dated `.agent/prose_slips.md` line under amend0827 rule 2, no id, no correction round.
<<<END RECORDR28>>>

<<<BEGIN SLIPSR28 target=.agent/prose_slips.md mode=append>>>
2026-09-07, F272 round 27 — the block's Goal stated that the ledger held `Gate: F272 R1` through `Gate: F272 R26` at the base commit, and it held 26 entries whose highest was R25; the R26 entry is the one that round's own C2 appended. The load-bearing half of the sentence was true and separately measured — zero entries matching `^Gate: F272 R.*full suite`, which is what made closure precondition 2 unmet — but the range was written from the round NUMBER rather than from the record. A sentence naming the span of entries a ledger already holds is measured against the ledger at the base commit, never derived from the round the block is being written for, because the round's own entry does not exist yet.
<<<END SLIPSR28>>>
