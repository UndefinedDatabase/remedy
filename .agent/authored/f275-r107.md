── STEP CLOSURE — F275 — ROUND 107 ──
Goal: Book round 106's verdict and the integration gate's; re-assign the 22 open findings this
feature raised to F273; generate the self-use item and run it to the approval gate under the
configured real provider, never applying it; run the full suite once. Nothing is repaired.

Base commit: `50171d2f`. Round type: SPLIT. Operator amendment amend0914-f275-sprint in
`docs/agents/self_drive_protocol.md` governs the suite run, and precondition 6 of
`docs/roadmap/STATUS_closure_protocol.md` governs the self-use item; read both first.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r107.md`, the block as received
C0b `.agent/last_block.md`, the block as received
C1 THE BOOKKEEPING COMMIT: `.agent/plan.md` gets slice PLAN107 as a full replacement;
   `.agent/live_review.md` gets SPEC O's owner endings and then slice RECORD107 appended;
   `.agent/prose_slips.md` gets slice SLIP107 appended; `.agent/decisions.md` gets slice DEC107
   appended
C2 THE SELF-USE ITEM, per SPEC U: `scripts/self_use_queue.json` and `.agent/selfuse_f275/`
C3 `.agent/authored/f275-r107-suite.txt`, per SPEC S
C4 `.agent/handoff.md`, the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths, with `.agent/selfuse_f275/` holding only the files SPEC U names.

## SPEC O — the owner endings, inside C1

For each of `R-0840`, `R-0842`, `R-0844`, `R-0845`, `R-0846`, `R-0848`, `R-0849`, `R-0850`,
`R-0851`, `R-0852`, `R-0853`, `R-0854`, `R-0856`, `R-0857`, `R-0860`, `R-0863`, `R-0865`,
`R-0866`, `R-0867`, `R-0868`, `R-0869` and `R-0880`: the one line of `.agent/live_review.md`
starting `- <id> — ` gains ` Owner: F273.`, a space and then that word, at its end, before
its newline. No other byte of the file changes before RECORD107 is appended.

## SPEC U — the self-use item, after C1 and before C2

U1 GENERATE. Call `packages.orchestration.self_use_generator.generate_and_append_if_empty` with
the TRACKED `scripts/self_use_queue.json` as `queue_path` and `.agent/live_review.md` as
`ledger_path`. Never hand-edit the queue file.
U2 RUN. Create a disposable worktree ON A THROWAWAY BRANCH, `git worktree add -b
tmp/f275-r107-selfuse <path> <C1>`, with `<path>` under `.remedy-wt/r107w/`. Call
`packages.orchestration.self_use_runner.run_next_self_use_item` with `dest_dir` a directory
under `.remedy-wt/r107w/`, `repo_path` that worktree, `queue_path` the tracked queue file, and
the function's default budgets. The job goes to the approval gate and stops; its change is NOT
applied, and `consumed_by` is NOT set. Then remove the worktree without `--force`, prune, and
delete the temporary branch.
U3 THE EVIDENCE, written after the run exited, all `.txt`: `entry_and_job_file.txt` (the
appended entry's id, title, provenance and `consumed_by`, and the job file path);
`result_state.txt` (the `JobPlan`'s `job_id` and `state`, and each task's `task_id` and
`status`); `execution_config.txt` (the `JobPlan`'s `execution_config` verbatim, then the line
`FAKE_APPEARS_IN_EXECUTION_CONFIG: <True|False>`); `timing.txt` (the wall clock and the
`JobPlan`'s `budgets`); `run_defects.txt` (the length of
`packages.orchestration.self_use_findings.describe_self_use_run_defects(<the JobPlan>)`, then
each string on its own line, verbatim, or the words `the tuple is empty`); `full_transcript.txt`
(the run's own stdout and stderr).

## SPEC S — the suite, once, after C2 and before C3

The round's FIRST AND ONLY full-suite run, from the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with
`PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`,
stdout and stderr saved under `.remedy-wt/r107w/`. A bad node is the text after a line-initial
`FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The transcript file holds: line 1
`EXIT=<pytest's return code>`; line 2 the run's last output line with its leading and trailing
`=` and spaces stripped; then every distinct bad node, sorted, one per line.

## Constraints

1. NO SLICE IS EDITED. PLAN107, RECORD107, SLIP107 and DEC107 land byte for byte; a discrepancy
   is DECLARED, never repaired.
2. READ `.agent/STOP` before C0a, before U2 and before C4, with real exit codes. If it appears,
   finish the commit in hand, write the handback and end.
3. THIS ROUND REPAIRS NOTHING and APPLIES NOTHING the self-use job proposes. A run that errors
   or blocks is a result to record verbatim in `run_defects.txt` and the handback.
4. No `.py` file under `.agent/`; scratch under `.remedy-wt/r107w/`, uncommitted, every output
   path absolute. The reviewer's `.remedy-wt/r101/` is not opened.
5. The appends of C1 delete nothing except as SPEC O's line endings require. Every commit stays
   under 500 insertions.
6. No `gh`, no `remedy`, no pull request, no merge, NEVER a force-push, no history rewrite. The
   one branch created and deleted is `tmp/f275-r107-selfuse`. Push after C1, C2, C3 and C4.
   `git worktree list` shows one row at C0a and at C4.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 222 lines TOTAL and 157 lines of
   PROSE, against the caps of 490 and 400.
8. GATE ORDER. G1 runs at C1, G2 and G3 after U3 and before C2, G4 after the suite with its
   committed-transcript reading at C3, and G5 after C3 and before C4. No gate runs after C4.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT AND BOOKKEEPING, at C1. The sha256 of `.agent/authored/f275-r107.md` at C0a equals
the block digest received, and `.agent/last_block.md` at C0b is byte-identical to it. Extract
the slices by their markers, report how many were FOUND, and check each against its
BEGIN-marker sha256. `.agent/plan.md` at C1 is byte-identical to PLAN107, with at most 50 lines,
one `## Goal` and one `## Next Steps`. `.agent/live_review.md` at C1 has the sha256
e9b6d00bcda855dd5e05a1331a519c01e2d16f8668119e6e7d9136997923929a, 1195998 bytes, the reviewer's own application of SPEC O and RECORD107
to its blob at `50171d2f`. For `.agent/prose_slips.md` and `.agent/decisions.md`, the blob at `50171d2f`
followed by the slice equals the file at C1. Lines matching `^Gate: F\d+ R\d+ — ` read 128 at
`50171d2f` and 129 at C1, with `Gate: F275 R106 — ` once. The open set BY DISTINCT ID, the ids of
`^- R-\d{4} — ` paragraphs minus the ids of `^Done: R-\d{4}` lines, reads 89 at both with
identical membership, and each of SPEC O's ids has exactly one `Owner: F273.` on its line.

G2 THE GENERATION, through `packages.orchestration.self_use_queue`'s loaders, never the JSON by
hand. (a) `pending_self_use_items()` and `next_self_use_item()` before U1: the reviewer read an
empty tuple and `None`. (b) The returned entry's `id`, `title`, `provenance` and `consumed_by`:
the reviewer, against a copy, read `SU-014`, `Address ledger finding R-0445`,
`generated (self-use-generator tier 1, ledger scan, R-0445)` and the empty string. (c) The
queue file's byte count and item count before and after: the reviewer read 43768 to 48787 bytes
and 13 to 14 items. (d) Pending items after: `SU-014` alone. REPORT every reading.

G3 THE RUN. REPORT, and match nothing: (a) the exact call; (b) the `JobPlan`'s `job_id`,
`state`, and each task's `task_id` and `status`; (c) the `execution_config` and whether the
string `fake` appears in it — it MUST NOT, and if it does the gate FAILS and the round hands back
without re-running; (d) the wall clock and `budgets`; (e) the defect tuple's length and every
string verbatim; (f) that nothing was applied: `git status --porcelain` in the primary checkout
names only `scripts/self_use_queue.json` and `.agent/selfuse_f275/` before C2, and the worktree
and temporary branch are gone.

G4 THE SUITE, per SPEC S. Report pytest's real exit code, the summary line and every bad node
with its last `E   ` line. Each bad node is re-run ALONE three times with SPEC S's environment
and reported FLAKY with the three tallies only if all three pass. Bad nodes less FLAKY: MUST be
none. At C3 the committed transcript equals the file rebuilt from the saved stdout.

G5 TREE, PATH SET, OPEN SET, CAP, after C3. `git status --porcelain` prints `''`, `git worktree
list` one row, `git branch --list 'tmp/*'` nothing. The changed-path set of `50171d2f`..C3
against the Bundle's paths other than `.agent/handoff.md`: MISSING and EXTRA by name. The open
set at C3 equals C1's. One row per commit of `50171d2f`..C3 with insertions, deletions and
staged path count, and the commits reaching 500 insertions, named.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 35 of feature F275 · round 107 · rounds so far 107`; the Commits table read from
`git show --numstat` and compared cell by cell against G5, C4's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; one sentence of context self-assessment;
`## Next` stating `Operator questions open: 1`. NO SCOPE REPORT AND NO SESSION-LIMIT BANNER,
by amendment amend0911-f275-to-scope.

── SLICE PLAN107 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN107 sha256=b212befa3f261d17f45008a931b5417af7b61c29fbd41522d2493c67f115e0c0
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001, T002 and T003 are DONE, the feature file's Built
State is current, and the integration gate passed in round 106.

## Current Step

ROUND 107 IS THE SELF-USE PRECONDITION AND THE FINDING RE-ASSIGNMENT. It books round 106's
verdict and the integration gate's, re-assigns the 22 open findings this feature raised and did
not resolve to the findings-paydown feature F273, records that the §3 checklist consolidation
pass merges nothing, and generates the tier-1 self-use item, runs it to the approval gate under
the configured real provider without applying it, and commits the run's evidence under
`.agent/selfuse_f275/`.

## Next Steps

1. CLOSURE ROUND A: register every defect string the self-use run returned, rotate the ledger,
   run the evidence job and build a fresh review package from a clean tree at the accepted head.
2. CLOSURE ROUND B: the STATUS line, the README sync and the self-use item's `consumed_by` in one
   commit, then the pull request.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE SELF-USE RUN NEEDS THE LOCAL MODEL SERVER: role config resolves builder and reviewer to
  a local `ollama` model, and the runner refuses to run on the fake provider.
- THE CLOSURE NEEDS COMMANDS THIS ENVIRONMENT DENIES: the `remedy` command line is refused
  here, so every closure step is run through the scripts and modules it calls.
- A SERVER-START RACE: a command-channel test read its server's info file before the server
  wrote it once in the reviewer's full run after the flip and passed ten times alone.
- The open set is 89 by distinct id, with `R-0809`, `R-0880`, `R-0883` and `R-0884` open.
  Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN107

── SLICE RECORD107 ── target `.agent/live_review.md` ── APPEND, after SPEC O ──
BEGIN RECORD107 sha256=69d8ebed04bed5728bd6b1e6cbf58426ad28f5f43aaa8f0b26d696cf17d0350b

Gate: F275 R106 — the F275 round 106 entry. VERDICT PASS, AND THE INTEGRATION GATE OF `docs/agents/integration_gate.md` PASSES. Written by the planner and reviewer of session 35 after reading the committed range `d8674d8d`..`50171d2f` and re-deriving every reading that bears on the verdict; the worker's report and its transcripts were evidence for no line below. It is booked here by the first commit of round 107 that writes the record, per operator amendment amend0827-process-diet rule 1. Only this entry may carry the full-suite claim, and it carries it.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r106.md` and `.agent/last_block.md` equal the reviewer's original at 18186 bytes at `50171d2f`; `.agent/plan.md` equals PLAN106; `.agent/live_review.md` at `0cc69cbb` equals its blob at `d8674d8d` followed by RECORD106, and `docs/roadmap/features/T2_F275.md` at `64674850` equals its blob at `d8674d8d` followed by BUILT106. The open set went from 91 to 89 by distinct id, `R-0887` and `R-0888` resolved and none added. No path outside `.agent/` and that feature file changes in the range.

THE GATE. The branch run, `python3 -m pytest -n auto -q -rfE` in the primary checkout at `64674850`, read exit 0 with 18442 passed and 23 skipped and no failed node, and its evidence under `.agent/gate_f275_r106/` says so; the reviewer's own run of the same command at `50171d2f`, the third and last full-suite run amendment amend0914-f275-sprint rule 4 grants the reviewer, read exit 0 with 18442 passed and 23 skipped and no failed node. BRANCH-ONLY is therefore empty. The base run, in a throwaway worktree at the merge base `d0aa833b` with `apps/ui/node_modules` and `apps/ui/dist` copied at equal file and symlink counts and the build stamped newer than every source, read exit 1 with 13 failed and 19758 passed; no dist file's mtime fell inside its window and `React UI not built` appears 0 times. All 13 are BASE-ONLY, and `.agent/gate_f275_r106/attribution.txt` attributes each by a direct reading. Eleven — the eight of `tests/test_command_discovery.py`, two of `tests/test_test_runner.py` and `test_permit_runtime_stderr` of `tests/orchestration/test_test_runner.py` — fail alone in the gate's environment and pass alone with `PYTHONPATH` pinned to the base worktree, because a command-line subprocess started from outside that worktree imports this primary checkout through the editable install, the class session 33 of this feature measured. Two — `test_a_clean_app_passes` of `tests/orchestration/test_product_smoke.py`, whose port was taken, and `test_timeout_raises_with_cleanup` of `tests/cli/test_review_bundle_runtime.py`, which matches processes machine-wide — pass alone. The reviewer rules all 13 environment-class and none a genuine base failure. The passed counts differ by 1316, and `git diff --name-status d0aa833b 64674850 -- tests/` lists 47 test files deleted, 5 added, 201 modified and 1 renamed on the branch.

ONE DEFECT OF THE BLOCK, declared by the worker. SPEC G offered only a missing base-worktree artifact as the environment class for a BASE-ONLY id, while the editable-install class was already measured on this branch; the worker attributed every id with direct evidence and declared that none fitted the class as worded. It is booked as one line in `.agent/prose_slips.md` by the commit that books this entry.
END RECORD107

── SLICE SLIP107 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIP107 sha256=73a5053f5d5b2dbe34a9df1264b91206aeb2c1c60a633c650d46016268569a71

2026-09-14 · F275 R106 · SPEC G of the round 106 block named a missing artifact of the base worktree as the only environment class a BASE-ONLY id could be attributed to, while this branch had already measured a second class, a command-line subprocess importing the primary checkout through the editable install; all 11 such ids and 2 contention ids therefore fitted no class as worded, and the worker attributed them by direct evidence and declared it. THE RULE THAT FOLLOWS: an attribution clause lists every environment class already measured on the branch, and otherwise orders the evidence rather than the class.
END SLIP107

── SLICE DEC107 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC107 sha256=2f929a850b7c0a99c64e3807e8fe80880b0cbccb49463134f4f109f72d92ae7e

## DECISION F275 D79 (2026-09-14, F275 round 107) — the closure's open findings go to the findings-paydown feature, the checklist consolidation pass merges nothing, and the self-use precondition is met by the generated tier-1 item

CONTEXT. The closure protocol, `docs/roadmap/STATUS_closure_protocol.md`, requires before the STATUS flip that every open finding this feature owned and did not resolve be re-assigned to the next findings-paydown feature, that the self-use precondition be met, and — per operator amendment amend0827-process-diet rule 4 — that the §3 pre-emission checklist of `docs/agents/planner_reviewer_prompt.md` be consolidated once inside the closure sequence, coming out the same length or shorter. The reviewer measured at `50171d2f` which open findings this feature owns: those whose registration line was first added by a commit on this branch and not on `main`, 24 in all, of which `R-0883` and `R-0884` already carry `Owner: F273`.

CHOSEN, FIRST: THE OTHER 22 ARE RE-ASSIGNED TO F273, the unclaimed findings-paydown feature, by ` Owner: F273.` appended to each registration line in the commit that lands this paragraph: `R-0840`, `R-0842`, `R-0844`, `R-0845`, `R-0846`, `R-0848`, `R-0849`, `R-0850`, `R-0851`, `R-0852`, `R-0853`, `R-0854`, `R-0856`, `R-0857`, `R-0860`, `R-0863`, `R-0865`, `R-0866`, `R-0867`, `R-0868`, `R-0869` and `R-0880`. Each is Medium or Low, so each stands as a documented risk at the close, per the protocol's first precondition. ALTERNATIVE: naming the feature each lost behaviour's text points at as its owner, rejected because the protocol's re-assignment step names the paydown feature, and a later claim of that feature re-routes what fits another feature's planned scope.

CHOSEN, SECOND: THE CONSOLIDATION PASS MERGES NO ITEM, and the list stays at 35. F275 added no item while it was open, as rule 4 requires, and its lessons went to `.agent/prose_slips.md`. A merge must choose which number to retire by counting the references each number has landed in the record, its archive and the slips, as F260's pass measured before merging item 19 into item 31; this closure does not take that measurement, so it merges nothing rather than re-pointing references it has not counted. The next consolidation measures against 35, as the checklist's own paragraph already states.

CHOSEN, THIRD: THE SELF-USE ITEM IS THE GENERATOR'S. The queue holds no pending item at `50171d2f`, so `generate_and_append_if_empty` runs first; against a copy of the queue the reviewer read it append `SU-014`, "Address ledger finding R-0445", from the generator's tier 1. That item is planned and run through `run_next_self_use_item` to the approval gate under the configured real provider and never applied, its `consumed_by` stays empty until the closure commit, and every defect string the run's own `JobPlan` yields is registered by the next round, which writes the record before the close.

CONSEQUENCE. F275's open-findings ownership is empty after this paragraph's commit apart from findings F273 owns. `R-0809` stays open, owned by the acceptance line its registration placed in `docs/roadmap/features/T2_F261.md`.

HOW TO REVERSE. Delete this paragraph block, remove the 22 appended `Owner: F273.` endings, and revert round 107's queue commit; the findings are then ownerless again, and the self-use precondition is unmet.
END DEC107
