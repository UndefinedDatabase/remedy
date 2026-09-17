── STEP T001/7 — F280 — ROUND 7 ──
Goal: Book round 6's independently-reviewed PASS and register R-0938, record DECISION F280 D5
and operator question Q4, then rename the `FlightPlan`/`FlightPlanClarification` class
identifiers to `TaskPlan`/`TaskPlanClarification` wherever the name is not a persisted value or
an accepted history file; run the suite once.

Base commit: `1805b05fae0ee25295e3ed5e0ce5c11ef295a7de`, on
`feature/f280-cli-vocabulary-v2-part-two`. SESSION 3 of F280. Read AGENTS.md and
docs/agents/self_drive_protocol.md before C0a.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is
two or more characters long is a run of a single repeated character, and every box-drawing rule
inside the STEP header line is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)`, `$?` and `$VAR` expansions in a command are refused by form, so write such
checks as Python scripts under `.remedy-wt/f280r7w/`, never named after a standard-library
module, and use absolute paths rather than `cd x && ...`; a pipe into `tail` hides pytest's exit
code. Never call `run_job`, `run_job_fulfill` or any runner yourself; `git branch --list
'remedy/job-*'` reads 17 lines now, keep it so. `python3 -m ruff check` NEVER names a `.sh` path.

WHY THREE PATCHES, NOT ONE: the rename's real change (150 insertions, 142 deletions over 24
files) fits comfortably under constraint 5's 500-insertion cap, but a unified diff of that many
renamed identifiers is 1190 lines of patch TEXT, and a brand-new patch file's own line count
counts as insertions for the commit that adds it (`git show --numstat` on a new file reads its
whole line count as inserted) — so ONE patch-plus-application commit would read roughly 1340
insertions, well over the cap. The reviewer split the single diff into three files by exact
file list, each applied and committed in its own sub-step (C2a, C2b, C2c); the reviewer verified
in its own disposable worktrees, twice, that applying all three in order (a then b then c)
reconstructs byte-identical trees to applying the original single diff, on every named subtree.
No file's own diff is split across two patches.

WHY NO RED-PROOF THIS ROUND: every edit is a mechanical rename of one class identifier to
another, with no field, function, module or persisted literal changed — DECISION F280 D5 is
the record of exactly which occurrences this round touches and which it does not. A rename has
no new behaviour to prove red before green; the equivalent proof is that a STALE reference would
either fail import (`ImportError: cannot import name 'FlightPlan'`) or fail ruff's undefined-name
check, so a clean `ruff check`, a zero-count sweep for the bare old token outside accepted
history, and the full targeted test selection passing together are the completeness proof this
round orders in place of a mutation.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f280-r7.md`, the block file the delegating message names, by
    `shutil.copyfile`, in its OWN commit
C0b `.agent/last_block.md`, the same bytes, in its OWN commit — do not combine C0a and C0b
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN7; slice RECORD7 is appended to
    `.agent/live_review.md`; slice DECISIONS7 is appended to `.agent/decisions.md`; slice OPQ4
    is appended to `.agent/operator_questions.md`
C2a THE FIRST PATCH: copy `.remedy-wt/f280-block/f280-r7-taskplan-a.patch` to
    `.agent/authored/f280-r7-taskplan-a.patch`, `git apply --check` it against the tree at C1,
    then `git apply` it, then `git add -A` and commit, in one commit
C2b THE SECOND PATCH: the same three steps for
    `.remedy-wt/f280-block/f280-r7-taskplan-b.patch`, applied against the tree at C2a
C2c THE THIRD PATCH: the same three steps for
    `.remedy-wt/f280-block/f280-r7-taskplan-c.patch`, applied against the tree at C2b
C3  `.agent/handoff.md`, the handback; then `git push origin
    feature/f280-cli-vocabulary-v2-part-two`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f280-r7.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/operator_questions.md`. C2a:
`.agent/authored/f280-r7-taskplan-a.patch`, `tests/schemas/test_flight_plan_schema.py`,
`tests/orchestration/test_flight_plan.py`, `packages/orchestration/dod_compiler.py`,
`docs/system/roadmap-mirror-v1.md`, `docs/system/vocabulary.md`. C2b:
`.agent/authored/f280-r7-taskplan-b.patch`, `packages/orchestration/flight_plan.py`,
`tests/cli/test_plan_approval.py`, `packages/orchestration/schemas/models.py`,
`packages/orchestration/feature_mission_adapter.py`, `packages/orchestration/mission_compiler.py`,
`packages/orchestration/dag_schedule.py`, `packages/orchestration/planner_models.py`,
`tests/orchestration/test_mission_compiler.py`. C2c:
`.agent/authored/f280-r7-taskplan-c.patch`, `tests/orchestration/test_dod_compiler.py`,
`packages/orchestration/task_granularity.py`, `tests/orchestration/test_bundled_clarification.py`,
`tests/orchestration/test_product_smoke.py`, `tests/orchestration/test_task_granularity.py`,
`packages/orchestration/mission_plan_schema.py`, `tests/cli/test_decision_answers.py`,
`tests/cli/test_golden_path.py`, `apps/cli/commands/do_cmd.py`,
`tests/orchestration/test_mission_e2e.py`, `docs/roadmap/features/T2_F280.md`. C3:
`.agent/handoff.md`.

## The appends

Each of RECORD7, DECISIONS7 and OPQ4 begins with an empty line, and its target ends in a
newline at the base: an append is the file's bytes followed by the slice's bytes, and nothing
else. PLAN7 is a FULL REPLACEMENT of `.agent/plan.md`.

## THE THREE PATCHES

Verify each sha256 before copying: `f280-r7-taskplan-a.patch`
`66db070861f230d6dcd5369289bf3e65073afe3fe49349058482d66ea2a02c81`; `f280-r7-taskplan-b.patch`
`79c2eed1f1bd52f4db3d28f855f38e430ca4db6bd3124125f85540288808bb26`; `f280-r7-taskplan-c.patch`
`0bf905a25855f6bdd0ab573db3eadcec8f046a4fa3c2124ae040ba926f141af2`. From the repository root, at
each sub-step's own tree: `git apply --check <patch>` must exit 0 before `git apply` runs it for
real; either exiting non-zero is a STOP — touch nothing further in that sub-step, commit nothing
of that patch, and hand back with the raw output. All three patches are the reviewer's own diff,
split from one, built and dry-run applied and tested by the reviewer, twice independently and
once more in sequence, on its own trees before delegation, whose objects the worker's own
sequential apply must equal.

## SPEC S — the suite, once, after C2c and before C3

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f280r7w/`. Report pytest's return code, the run's last output line, and every distinct
bad node. Re-run each bad node alone, once, the same way, and report that return code beside it.
A bad node whose lone re-run exits 0 and whose file is untouched by this round's own change set
is reported as such and is not a STOP, per the fresh-worktree vitest artifact this feature's own
record already carries; any other bad node is a STOP.

## Constraints

1. NO SLICE AND NO CARRIER IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before each of C2a/C2b/C2c and before C3, with real exit
   codes. If it exists: finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f280r7w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f280-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No
   `remedy`. Write no `Gate:`, `Done:`, DECISION or operator-question paragraph of your own
   beyond RECORD7, DECISIONS7 and OPQ4, which are the reviewer's, already written.
7. THE BLOCK'S OWN SIZE, measured on its final bytes, against the caps of 490 and 400 where
   PROSE is every line that is not a line of slice CONTENT (the `BEGIN`/`END` marker lines
   count as prose).
8. GATE ORDER. G1 and G2 after C1; G3 and G4 after C2c; then SPEC S, whose result is G5; G6
   after C3 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f280-r7.md` at C0a equals the digest the
delegating message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices
FOUND, each matching its BEGIN-marker sha256; each committed patch's sha256 equals the value
named in "THE THREE PATCHES" above, in patch order a, b, c.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN7, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its base blob
followed by RECORD7. `.agent/decisions.md` equals its base blob followed by DECISIONS7.
`.agent/operator_questions.md` equals its base blob followed by OPQ4. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 32 at the base and 33 at C1, with
`Gate: F280 R6 — ` 0 times at the base and once at C1; distinct `^- R-\d+ — ` ids 133 at the
base and 134 at C1, the delta exactly `R-0938`; distinct `^Done: R-\d+ — ` ids 6 at both; the
open set by distinct id 127 at the base and 128 at C1.

G3 THE PATCHES. `git diff --no-renames --name-only` from C2a's parent to C2c prints exactly the
three patch files and the 24 paths the Change section names, no other. `git rev-parse
<commit>:<object>` for `apps`, `packages`, `tests` and `docs`, in that order, at C2c, equals the
reviewer's own three independent reconstructions (single-diff apply, twice, and the three-patch
sequential apply, all agreeing): `fd491168bfcfa326d29e86613a7423891c75b1f7`,
`b84ab78e653f074cc3c628155b82111f3034b88e`, `f318e34d01b756196b507732c85689c29fac50ed`,
`20041918c6442233eae2bc9c9550b358a299ee60`. Report the insertions and deletions of C2a, C2b and
C2c per constraint 5; the reviewer's own dry-run reads 483 (429 patch + 54 real, 5 files) for
C2a, 470 (421 patch + 49 real, 8 files) for C2b, 387 (340 patch + 47 real, 11 files) for C2c.
`python3 -m ruff check` over the nine edited `.py` paths under `apps` and `packages` exits 0
(one pre-existing, unrelated `UP035` finding in `dag_schedule.py` is present at the base too and
is not this round's).

G4 THE SWEEP, at C2c. `git grep -n -I -E '\bFlightPlan\b|\bFlightPlanClarification\b' <rev> --
apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'`: 0 lines at C2c
(135 at the base). The same pattern restricted to `docs/roadmap/features/T1_F014.md`,
`T1_F016.md`, `T1_F034.md`, `T1_F080.md`, `T1_F252.md` reads 12 lines at C2c, unchanged from the
base, confirming the accepted-history exemption held.

G5 THE TARGETED TESTS, at C2c: `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider
--tb=short -rfEs tests/cli/test_decision_answers.py tests/cli/test_golden_path.py
tests/cli/test_plan_approval.py tests/orchestration/test_bundled_clarification.py
tests/orchestration/test_dod_compiler.py tests/orchestration/test_flight_plan.py
tests/orchestration/test_mission_compiler.py tests/orchestration/test_mission_e2e.py
tests/orchestration/test_product_smoke.py tests/orchestration/test_task_granularity.py
tests/schemas/test_flight_plan_schema.py tests/docs/` exits 0; report the count (828 in the
reviewer's own dry run).

G6 THE SUITE, SPEC S at C2c: must exit 0 with no bad node beyond the named fresh-worktree
exception; report the last output line.

G7 THE TREE, after C3 and the push. `git status --porcelain` prints `''`; C0a to C3 are
single-parent commits in that order on the base; `git rev-parse HEAD` equals `git rev-parse
origin/feature/f280-cli-vocabulary-v2-part-two`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 17 lines.

## The handback, C3

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line `SESSION 3 of feature
F280 · round 7 · rounds so far 1`, with one sentence of context self-assessment. `## Commits`
lists C0a, C0b, C1, C2a, C2b and C2c, each row's `+/-` cell equal to constraint 5's reading of
that commit and its deletions column, RE-DERIVED FROM `git show --numstat` DIRECTLY rather than
copied from any draft. C3's own numbers appear nowhere, per item 31 of §3. `## Verification`
gives G1 to G6 with real exit codes. It states the open findings at 128 by distinct id, with the
High ids R-0803, R-0804 and R-0807, and `Operator questions open: 2`. Its `## Next` names, in
order: Phase 1 rule 1; the reviewer's verdict on round 7; `propose`, once operator question Q4
is answered.

── SLICE PLAN7 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN7 sha256=d896003845f1533cb48a3bbaf89bc2de25974860718a9eab19fcce032436778a
# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 7 books round 6's independently-reviewed PASS and registers R-0938 (a handback numstat
misreport, no code fix owed), records DECISION F280 D5 (the `FlightPlan` to `TaskPlan` class
rename and the boundary it does not cross) and operator question Q4 (whether `propose` may keep
a CLI surface at all, since DECISION F261 D22 found deleting it strands `self execute`'s
approved-for-build gate and the cockpit's `can_finalize` hold with no operator-facing heir), then
renames the `FlightPlan`/`FlightPlanClarification` class identifiers to
`TaskPlan`/`TaskPlanClarification` everywhere they are not a persisted value or an accepted
history file, per DECISION F280 D5.

## Next Steps

1. `propose`, once operator question Q4 is answered.
2. The rest of the `flight_plan` rename DECISION F280 D5 deferred: the module
   `flight_plan.py` to `job_plan.py` (with `FlightPlanResult` and its lowercase function names),
   then the persisted job key, schema tag and decision-type literals, then the surviving
   English prose.
3. `worker doctor` and `job run --tasks`, D4 words no feature owns yet.
4. `job attach-repo` and `job permit`, only once a DECISION gives the repository attach and the
   capability grants another writer, as DECISION F280 D4 requires.
5. T002, which also re-derives the root help's quick start with the README quickstart (R-0895)
   and closes the flag scanner's blind spot (R-0934).

## Risks

- 128 findings are open by distinct id after this round's record; three are High, R-0803,
  R-0804 and R-0807, none of them this feature's.
- R-0899 (open, owned F273): section 3 of `scripts/remedy_smoke.sh` reads a `state` key `job show`
  does not print, so its planned-state check fails wherever the script is actually run.
- R-0937 (open, owned F273): five comment/message lines in `tests/test_remedy_smoke_script.py`
  still name the retired `--task-type`/`--task-description` flags. R-0938 (open, owned F280):
  round 6's own handback misreports one commit's insertion/deletion counts; nothing to fix.
- `job attach-repo` and `job permit` are the only command-line writers of a job's repository
  and of its test and revert grants, so the Acceptance line naming them cannot hold until a
  later DECISION supplies a writer.
- R-0935: the run contract never inherits a job's F018 token and wall-clock budgets, so what
  `job budget <id> set` writes into the contract is not overwritten by them either. Operator
  question Q4 is open: `propose`'s deletion (DECISION amend0905-vocab D4) is blocked on an answer.
END PLAN7

── SLICE RECORD7 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD7 sha256=1c912da073b1e611f76f6805ca5a7ba20cc051d238c63e6260724a727d2b0cf7

Gate: F280 R6 — round 6, booking its own verdict. VERDICT PASS, WITH ONE LOW FINDING (R-0938). Written by the planner and reviewer of session 45 after reading the committed range `e81c8e94`..`0cd36183` (commits `fbdd634c`, `974ee226`, `621ee7ef`, `0cd36183`) and independently re-deriving every reading below in its own disposable worktrees, per Phase 1 rule 4 of `docs/agents/self_drive_protocol.md` — round 6 was authored and reviewed by session 44's own planner-reviewer with no second reader, so this is the first independent re-review. THE TRANSPORT: `.agent/authored/f280-r6.md` sha256 `466a2b09450b5f12032c7195a013cd93b915ccce2434ffedda3820b94d4bd504` and `.agent/last_block.md` byte-identical to it; the committed patch `.agent/authored/f280-r6-deletejobcreate.patch` sha256 `063e220ea405d9a5fa79a459fcd4c8aad696af91c32aa656497281f4533dbef3`, matching the round's own block exactly. THE RECORD: over `.agent/live_review.md` at `621ee7ef`, `^Gate: F\d+ R\d+ — ` reads 32 (31 at base plus the `Gate: F280 R4` entry), distinct `^- R-\d+ — ` ids 133 (delta exactly `R-0937`), distinct `^Done: R-\d+ — ` ids 6 (`R-0721`, `R-0725`, `R-0767`, `R-0894`, `R-0906`, `R-0909`, each counted once though `R-0721` and `R-0725` each carry two resolution paragraphs), open set by distinct id 127 — all four numbers reproduced exactly by the reviewer's own count, independent of the block's or the handback's claim. THE PATCH: the reviewer applied `.agent/authored/f280-r6-deletejobcreate.patch` in two independent disposable worktrees at `621ee7ef`; both applications agreed byte-for-byte on every named subtree (`apps` `e236db2d080e1307f936446a2d1f24e8e0f5b8a8`, `packages` `905f8acfa8e41b944133a841aa0c451620618c5b`, `scripts` unchanged `bde7eae195226e4567a0cdde74c54e51e735b137`, `tests` `f7d5bf6dbe99b6c85c1bb670826d12192b16cc8f`, `docs/guides` `9c86d25d406764a55bdaf4cee06f01ee14e2b5ab`, `docs/system` `4e35fafb4567ba17c51f1961deaec6607c709922`, `docs/README.md`/`README.md`/`.claude` unchanged), every one equal to the block's own predicted digest; `git show --numstat --format= 0cd36183` reads 12 files outside `.agent/`, 35 insertions and 66 deletions, matching G3 exactly; `python3 -m ruff check` over the eight edited `.py` paths reads `All checks passed!`. THE SWEEP: the CLI-dispatch pattern reads 0 lines at `0cd36183`, unchanged from the base; the second sweep, taken on the applied working tree before `git add`, reads 1 surviving line, `README.md:269:remedy job create --plan plan.yaml         # create a job from a plan`, the one the block names for R-0895/T002; the 896-test targeted selection the block names reads `896 passed` in the reviewer's own run. THE SUITE: the round's own worker ran SPEC S in the primary checkout and committed the transcript, `17642 passed, 23 skipped, 1 warning`, 0 bad nodes — the reviewer did not re-run that exact command, per the pattern this feature's rounds already record, but did independently run the full suite once more itself, in a disposable worktree freshly created at `1805b05f` with no prior run (`apps/ui/node_modules` and `apps/ui/dist` absent, per the fresh-worktree lesson this feature's memory already carries): `1 failed, 17635 passed, 29 skipped, 1 warning in 1290.64s`, the one failure `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`, which asserts `npx vitest run` exits 0 from `cwd=apps/ui` with no guard for a missing toolchain (confirmed by reading the test's own source, lines 405 to 413) — a worktree artifact of the missing install, not a regression this round's diff could cause, since the round touches no file under `apps/ui`. THE TREE: `git status --porcelain` empty; C0a to C3 read `fbdd634c` then `974ee226` then `621ee7ef` then `0cd36183` then `1805b05f`, five single-parent commits in that order; `git rev-parse HEAD` equals `origin/feature/f280-cli-vocabulary-v2-part-two`; `git worktree list` one row (the reviewer's own disposable worktrees were removed after use); `git branch --list 'remedy/job-*'` 17 lines. THE ONE DEFECT FOUND is R-0938, registered below: the handback's own `## Commits` table misreports commit `621ee7ef`'s insertion and deletion counts for `.agent/plan.md`, and its "Total" line matches neither the truth nor its own table — confined to the handback's prose, no gate this round certifies reads it as evidence. WHY PASS: every gate the round's own block ordered is independently reproduced exactly by the reviewer, in its own hand, in its own disposable worktrees, and the one defect found is a reporting slip that changes no committed byte outside `.agent/handoff.md` and blocks nothing.

- R-0938 — Low, ROUND 6'S OWN HANDBACK MISREPORTS ITS C1 COMMIT'S INSERTION AND DELETION COUNTS, AND ITS OWN "TOTAL C0a TO C2" LINE DOES NOT SUM EVEN ITS OWN WRONG TABLE. Raised by the planner and reviewer of session 45 while independently reviewing round 6, from a reading taken directly at `621ee7ef` after searching the open set for a handback numstat finding under §3 item 30: none exists. THE DEFECT: `.agent/handoff.md`'s `## Commits` table for `621ee7ef F280 R6 C1` reads `.agent/plan.md | 42+/45- |`, but `git show --numstat --format= 621ee7ef` reads `14	16	.agent/plan.md` — the true insertion and deletion counts are 14 and 16, not 42 and 45 (42 is the line count of the new file, a different measurement the handback's own instructions do not call for there); the handback's "Total C0a to C2: 400 insertions, 266 deletions" line matches neither the true total (727 insertions, 170 deletions, confirmed by `git diff --stat e81c8e94..0cd36183` and by summing every commit's own real numstat) nor even its own mistaken per-commit table (222+164+42+4+323=755, not 400). Every other row of the table, and every gate this round's own block ordered, is independently reproduced correct by the reviewer — transport digests, tree hashes, sweeps, targeted and full-suite tests all hold exactly as claimed — so this is a reporting error confined to the handback's own prose, not a defect in any committed file the round's gates certify. WHY LOW: no gate reads the handback's numstat table as evidence; every constraint-5 check in this and future rounds is the reviewer's own re-derivation from `git show --numstat`, never the table. FIX: none needed on any file the block names; a future handback-authoring round takes more care computing constraint 5's own reading before writing the table, and this finding is discharged the next time a round's own handback table is read against its commits and found to agree. Owner: F280.
END RECORD7

── SLICE DECISIONS7 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DECISIONS7 sha256=68312e75e6de6ab08d47cef2b5bc4f3c563c16e2a3dbc2bce17c3aada949631a

## DECISION F280 D5 (2026-09-16, F280 round 7) — the class name that replaces `FlightPlan`, and the boundary this round's rename does not cross

CONTEXT. DECISION amend0905-vocab D6 names the module target — `packages/orchestration/flight_plan.py` becomes `job_plan.py`, and the noun "flight plan" is deleted from code, catalog, docs and feature files — but leaves the CLASS name open; `.agent/f261_t003_inventory.md`'s own ruling 9 states the replacement is not yet chosen. `docs/system/vocabulary.md`'s Plan row confirms `JobPlan` (the persisted job record, `packages/orchestration/pingpong_job.py`) and `FlightPlan` (the LLM planner's structured output schema, `packages/orchestration/schemas/models.py:178`, a DAG of `PlannedTask`s stored inside `JobPlan.flight_plan`) are two distinct concepts, not a merge candidate. Measured at `1805b05f` by the reviewer directly, twice, in two independent disposable worktrees whose applications of the same patch produced byte-identical subtrees (`apps` `fd491168bfcfa326d29e86613a7423891c75b1f7`, `packages` `b84ab78e653f074cc3c628155b82111f3034b88e`, `tests` `f318e34d01b756196b507732c85689c29fac50ed`, `docs/system` `40f4896bbecc1664b99e24315a7b08cb00fc43db`): the exact-token class name `FlightPlan`/`FlightPlanClarification` (word-boundary, case-sensitive) occurs 147 times across 27 files; 12 of those lines are in five accepted `[x]` feature files (`docs/roadmap/features/T1_F014.md`, `T1_F016.md`, `T1_F034.md`, `T1_F080.md`, `T1_F252.md`), which DECISION amend0905-vocab D6's own history rule exempts from editing; the remaining 135 lines across 23 files are the class name used as a Python type or as English prose describing it, never as a persisted string — the one quoted occurrence, `packages/orchestration/schemas/models.py:201`'s `f"FlightPlan exceeds..."`, is a runtime error message, not stored data.

CHOSEN, FIRST: the class becomes `TaskPlan`, and `FlightPlanClarification` becomes `TaskPlanClarification` — "a DAG of PlannedTasks" (the class's own docstring) is literally a plan of tasks, `TaskPlan` is unused anywhere else in the repository today, and it reads unambiguously beside the persisted `JobPlan` record it is one field of. This round renames exactly the 135 non-exempt lines the measurement above counts, in one commit, and touches nothing else: no module is renamed (`flight_plan.py` stays `flight_plan.py` until a later round takes DECISION amend0905-vocab D6's module move), no function or module-level constant spelled in lowercase (`map_flight_plan_to_tasks`, `flight_plan_blocks_execution`, `resolve_flight_plan_approval`, `auto_approve_flight_plan`, `FLIGHT_PLAN_SCHEMA_V`, `_MAX_FLIGHT_PLAN_TASKS`) is touched, `FlightPlanResult` (a distinct dataclass wrapping a planner call's outcome, `packages/orchestration/flight_plan.py:35`) is untouched, and no lowercase `flight_plan` occurrence — the persisted job-record key and attribute `JobPlan.flight_plan`, the schema tag value `"flight_plan_v1"`, the decision type `"flight_plan_approval"` and its sibling literals in `packages/orchestration/decision_queue.py`, and the prompt text quoting the schema tag — is touched, because every one of those is either a value persisted in an existing job record or a name entangled with one, and DECISION amend0905-vocab D6 gives their round no number yet.

CHOSEN, SECOND: the five accepted `[x]` feature files stay byte-identical, per D6's own history rule; no per-file vocabulary note is added, because D6 already states the blanket exemption once.

CONSEQUENCE. `TaskPlan`/`TaskPlanClarification` are the schema's class names from this commit forward; `FlightPlan`/`FlightPlanClarification` as Python identifiers exist nowhere outside accepted history. Owed by a later round, in the order DECISION amend0905-vocab D6 and the stale inventory's ruling 9 already imply: the module rename `flight_plan.py` to `job_plan.py` (with `FlightPlanResult` and its lowercase function names following it), the persisted literals (job key, schema tag, decision type), and the surviving English-prose noun "flight plan" outside a Python identifier. HOW TO REVERSE: revert the round's rename commit.
END DECISIONS7

── SLICE OPQ4 ── target `.agent/operator_questions.md` ── APPEND ──
BEGIN OPQ4 sha256=9618ae9b88f6c91d4ad69772890052ba512ab5b4d4111e9201f7f952e6e646fb

### Q4 — Whether `propose` may stay a real command (2026-09-16, F280, round 7)

What needs deciding. The vocabulary cleanup's master list marks the command group that lets an operator review and approve a suggested next task for deletion. Looking at the actual code, I found that deleting it would leave two other features stuck with no way forward: the self-drive execution command would permanently refuse to run any task it hasn't been told is approved, and a job's build and finalize steps would stay stuck at pending forever once even one suggestion exists for it, because nothing else in the running system ever marks a suggestion resolved. A job accumulates one of these suggestions automatically every time a task finishes successfully, so this is not a rare edge case.

Why it matters. If I delete the group to satisfy the cleanup list, every job that finishes a task afterward gets permanently stuck unable to reach done, with no command-line way out. If I instead keep the whole group alive to avoid that, the vocabulary cleanup's own finish line — every word on its retirement list is actually gone — stays unmet, and two already-written acceptance criteria for this feature go permanently unsatisfiable without a further change to them.

My recommendation. Keep the review-and-approve part of the group alive under a different name attached to an existing surviving word, rather than deleting it outright or leaving it exactly as it is. That satisfies both concerns: the old top-level word disappears as the cleanup intends, and the two stuck safety gates keep a real, reachable way to be resolved. Building that replacement command and choosing its exact name is more design work than a naming decision, so I have not built it without your sign-off.

What happens if you say nothing. I will leave the group exactly as it is today, unresolved, and move on to other work this session can still finish; the two acceptance criteria that assume its deletion stay open, and the next session picks this back up.
END OPQ4
