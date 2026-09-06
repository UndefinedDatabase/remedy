── STEP T002 (part 2) — F260 ─────────────────────────────────
Goal:        Put the four REMAINING hand-built evidence paths onto
             `data_paths.job_evidence_dir`, so DECISION F260 D1's layout has one
             spelling in every module that owns a job's evidence, and widen the
             guard from one module to that whole set.
Bundle:      C0a save this block · C0b mirror it · C1 the record (the R6 gate
             entry) · C2 one reviewer slip · C3 the plan · C4 the four call
             sites and the widened guard · C5 the handback
(§3 item 37: the STEP line above is 62 characters ending in a run of U+2500,
 and the rule line below is 62 copies of U+2500 and nothing else)
──────────────────────────────────────────────────────────────

## Where this round starts

Continuing on `feature/f260-one-world` at `99ca6406`, already pushed. Do NOT
create a branch, do NOT merge, do NOT open a pull request.

Round 6 PASSED. The reviewer re-ran all eight gates itself, reproduced the ledger
and feature-file arithmetic byte for byte, re-ran the four mutations in its own
disposable worktree and re-ran all eight suites at 730 tests. Your deviation 1 is
UPHELD and is the reason C2 exists: `.agent/prose_slips.md` did NOT end with a
newline at `3aaeb042`, so the round-6 recipe fused three slips into one
blank-line unit. That is a defect in the reviewer's recipe, not in your
application of it, and this block's C2 carries the counter-measure as a gate.
Your deviations 2 through 7 are all accepted as recorded; the root-override test
you strengthened beyond the block — pointing the env root and the argument root
at DIFFERENT directories — is better than what was ordered, and the reviewer
reproduced it catching mutation (iii).

## Change set — nothing outside this list

    .agent/authored/f260-r7.md                   (new, C0a)
    .agent/last_block.md                         (C0b)
    .agent/live_review.md                        (C1)
    .agent/prose_slips.md                        (C2)
    .agent/plan.md                               (C3)
    packages/orchestration/job_evidence.py       (C4)
    packages/orchestration/repair_attest.py      (C4)
    apps/cli/commands/do_cmd.py                  (C4)
    tests/test_data_paths.py                     (C4)
    .agent/handoff.md                            (C5)

`.remedy-wt/` scratch stays untracked; `git ls-files .remedy-wt` returns nothing.

## C0a / C0b — save and mirror

The block is at `.remedy-wt/f260-r7-block.md`; the delegating prompt states its
sha256 (BLOCK_SHA — a file cannot carry its own digest). COPY it to
`.agent/authored/f260-r7.md` with `shutil.copyfile`, commit alone; copy the same
bytes to `.agent/last_block.md`, commit alone. Do not retype either.

## C1 — the record

APPEND to `.agent/live_review.md`, in one commit of its own, exactly the bytes
`"\n"` + the GATE_R6 slice + `"\n"`. A slice is the bytes between its markers
EXCLUDING the newline that ends its last content line. Measured at `99ca6406`:
the file is 887129 bytes, ends with EXACTLY ONE newline, and holds 424
blank-line units. After the append it ends with exactly one newline and holds
425.

## C2 — the slip

APPEND to `.agent/prose_slips.md`, in one commit of its own, exactly the bytes
`"\n"` + the SLIP6 slice + `"\n"`.

READ THE TERMINAL BYTE FIRST, and report it — this is the whole point of the
round-6 defect. Measured at `99ca6406`: the file is 92673 bytes, ends with
EXACTLY ONE newline, and holds 128 blank-line units. Because it ends with a
newline, the leading `"\n"` of the recipe above creates a real blank-line
SEPARATOR and the unit count rises to 129. At `3aaeb042` that same file ended
with NO newline, which is why the identical recipe produced no separator and left
the count at 128. If your own reading of the terminal byte disagrees with this
paragraph, say so and apply the recipe that yields a separator, then declare it.

## C3 — the plan

REPLACE `.agent/plan.md` entirely with the PLANF260R7 slice plus one trailing
newline. Commit alone.

## C4 — what to build

Round 6 gave `data_paths` the one spelling of DECISION F260 D1's layout and moved
`pingpong_job`'s two evidence paths onto it. FOUR hand-built spellings remain.
Each is literally `jobs_dir() / <id> / "evidence"` with an optional tail, so each
swap returns the identical path and changes no behaviour. The reviewer read all
four at `99ca6406` and applied them in its own dry run; re-grep each before
editing rather than trusting a line number.

  * `packages/orchestration/job_evidence.py`, in the attestation-snapshot reader:
    `ev_base = jobs_dir() / job.job_id / "evidence"` → `job_evidence_dir(job.job_id)`.
  * `packages/orchestration/job_evidence.py`, in the task-stream export:
    `src_task = jobs_dir() / job_id / "evidence" / "task_runs" / task_id / "streams"`
    → `job_evidence_dir(job_id) / "task_runs" / task_id / "streams"`.
  * `packages/orchestration/repair_attest.py`:
    `base = jobs_dir() / job_id / "evidence"` → `job_evidence_dir(job_id)`. Its
    `jobs_dir` import is MODULE-LEVEL (`repair_attest.py:34` at `99ca6406`); the
    other three are function-scoped. Keep each module's existing import style.
  * `apps/cli/commands/do_cmd.py`, in the task-stream trace reader:
    `_task_ev_dir = jobs_dir() / job_id / "evidence" / "task_runs" / task.task_id`
    → `job_evidence_dir(job_id) / "task_runs" / task.task_id`.

EACH SWAP RETIRES THAT MODULE'S LAST USE OF `jobs_dir`, so the import must move
to `job_evidence_dir` in the same edit or ruff reports an unused import. Verify
that per module before removing anything: the reviewer measured, by AST at
`99ca6406`, that these three modules reference `jobs_dir` ONLY at the four sites
above. Note that `job_evidence.py` also names `_jobs_dir` — `pingpong_job`'s
module-local helper, a DIFFERENT symbol that merely contains the same substring.
Leave it alone; it moves with the ping-pong store in a later round.

DO NOT TOUCH `packages/orchestration/checkpoints.py` OR
`packages/orchestration/storage.py`. Both still call `jobs_dir`, and correctly:
they name the CLASSIC store `<data_root>/jobs/<uuid>.json`, which is a FILE per
job and a different concept from a job's evidence directory. That store is
deleted in T004, not here.

THE GUARD — widen the existing
`TestJobAndRunLayout::test_pingpong_job_no_longer_spells_the_evidence_path_itself`
in `tests/test_data_paths.py` from one module to the SET of modules that own a
job's evidence. Define the set SEMANTICALLY in the test — the modules F260 has
migrated onto `data_paths.job_evidence_dir` — and parametrize over it:
`pingpong_job.py`, `job_evidence.py`, `repair_attest.py`, `do_cmd.py`. Assert each
has ZERO `jobs_dir` references, keeping the AST reading you built in round 6
(`Name`, `Attribute` or `alias` resolving to exactly `jobs_dir`), which is what
makes `_jobs_dir` correctly invisible to it.

The test must also state, in its docstring, WHY `checkpoints.py` and `storage.py`
are excluded — they name the classic store, not the evidence directory — because
an exclusion a later reader cannot justify is one a later reader deletes. Add a
NON-VACUITY assertion: the module set is non-empty and every module in it
imports. Keep the value-equality readings that already exist; the equality test
cannot see a regression to the hand-built path, which is why both readings ship.

## Constraints

1. Apply every authored slice BYTE FOR BYTE. If a slice looks wrong, apply it
   anyway and say so in the handback's deviations — do not repair it.
2. Nothing outside the change set above is created, edited or deleted.
3. Commit order is C0a, C0b, C1, C2, C3, C4, C5, each its own commit. C4 is ONE
   commit: the four swaps and the widened guard land together.
4. Every mutation of G6 runs ONLY inside a disposable `git worktree` under
   `.remedy-wt/` (self_drive_protocol.md G5), removed with
   `git worktree remove --force` before C5. Never `git checkout --` a mutated
   primary file. Pick a worktree name that does not already exist under
   `.remedy-wt/` — several unrelated scratch directories live there — and delete
   nothing you did not create.
5. Purge `__pycache__` or run `python3 -B` for every mutation run.
6. Gates G1 through G8 all run AT C4, before C5 is written (§3 item 31). The
   handback commit's own numbers are owed by no one.
7. `git status --porcelain` is empty at C5. Re-read `.agent/STOP` from disk before
   C4; if it exists, finish the commit in hand, write the handback and stop.
8. Push after C5: `git push origin feature/f260-one-world`. Never force-push.

## Done when — eight gates, each run and its real exit code recorded

G1 TRANSPORT (one digest). `sha256sum` over `.remedy-wt/f260-r7-block.md`,
   `.agent/authored/f260-r7.md` and `.agent/last_block.md` returns ONE value equal
   to BLOCK_SHA. Report the digest.

G2 THE RECORD. At C1: report `.agent/live_review.md` before and after and that the
   growth equals the appended byte count exactly. Prove (a) the 887129-byte
   pre-image is a byte-exact PREFIX; (b) the remainder is exactly `"\n"` + the
   GATE_R6 slice + `"\n"`; (c) the file's LAST blank-line unit equals the GATE_R6
   slice. Two negative controls, in a scratch copy, one per region: a byte flipped
   INSIDE the appended paragraph must make (c) reject, and a byte flipped inside
   the PRE-IMAGE region must make (a) reject. Report the blank-line unit count
   before and after — 424 then 425 — and that the file ends with exactly one
   newline. Report that `^- R-[0-9]{4} — ` still matches 299 and
   `^Done: R-[0-9]{4} — ` still matches 4, the count of `^Gate: ` headers, and
   that they are all distinct.

G3 THE PROSE FILES. At C2: report `.agent/prose_slips.md`'s LAST BYTE before the
   append, its byte length before and after, that the pre-image is a byte-exact
   prefix, that the remainder is exactly `"\n"` + SLIP6 + `"\n"`, and its
   blank-line unit count before and after — which must RISE BY EXACTLY ONE, to
   129. That last reading is the one the round-6 recipe would have failed. At C3,
   `.agent/plan.md` equals the PLANF260R7 slice plus exactly one trailing newline;
   report its line count, which must be under 50.

G4 THE SWAPS ARE VALUE-PRESERVING. At C4, in a Python process with
   `REMEDY_DATA_DIR` set to a temporary directory, show that for a sample job id
   and task id each of the four migrated expressions equals what it returned
   before — that is, `data_paths.job_evidence_dir(j)` equals
   `data_paths.jobs_dir() / j / "evidence"`, and the two `task_runs` tails equal
   their hand-built forms. This is the property the swaps rest on; report the
   paths, not just the booleans.

G5 THE CODE. At C4, all three readings:
   (a) `python3 -m ruff check packages/orchestration/job_evidence.py
       packages/orchestration/repair_attest.py apps/cli/commands/do_cmd.py`
       exits 0;
   (b) by AST, the count of references resolving to exactly `jobs_dir` is 0 in
       each of `pingpong_job.py`, `job_evidence.py`, `repair_attest.py` and
       `do_cmd.py`, and is NON-ZERO in each of `checkpoints.py` and `storage.py`
       — report all six numbers. The second half is the non-vacuity reading: a
       guard that found zero everywhere would be measuring nothing;
   (c) `git diff --numstat 99ca6406..C4` reports exactly four paths. Report all
       four rows.

G6 THE MUTATION RED-PROOF (production code — mandatory in full). In a disposable
   worktree at C4, run the UNMUTATED CONTROL FIRST and report its exit code and
   pass count; then break these three PROPERTIES one at a time, restoring between
   each, and report each run's exit code and every failing node id:
   (i) `job_evidence.py` no longer spells the evidence path itself — break it by
       putting the hand-built expression back at the attestation-snapshot site;
   (ii) the same for `repair_attest.py`;
   (iii) the guard's own SET is non-empty and real — break it by making
         `data_paths.job_evidence_dir` return
         `jobs_dir(root) / "evidence" / job_id`, which must turn the round-6
         layout tests red and prove the widened guard did not replace them.
   The control must be GREEN before and after each. Report `git worktree list`
   after the removal.

G7 THE SUITES, run SERIALLY in the primary checkout at C4, each exit code
   recorded separately — never through a pipe:
   `tests/test_data_paths.py`, `tests/orchestration/test_job_evidence.py`,
   `tests/orchestration/test_repair_attest.py`,
   `tests/orchestration/test_stream_export_e2e.py`,
   `tests/orchestration/test_evidence_index.py`, `tests/test_do_job_flow.py`,
   `tests/orchestration/test_pingpong_cli.py`, and the canary
   `tests/cli/test_golden_path.py`. Report each suite's count and exit code.

G8 THE TREE AND THE CHANGE SET. At C4: `git status --porcelain` empty,
   `git ls-files .remedy-wt` empty, `.agent/STOP` absent, and `git worktree list`
   holds no worktree this round created. `git diff --name-only 99ca6406..C4` lists
   exactly the eight paths of the change set above other than `.agent/handoff.md`,
   which C5 adds; report the list as the command printed it. Report
   `python3 -m apps.cli.grouped integrity check --json` with its `passed` and
   `fail_count`.

## Handback

Rewrite `.agent/handoff.md` in C5 per docs/agents/handback_template.md: feature
and round, `SESSION 2 of feature F260`, branch, the per-commit SHAs with each
commit's insertion count from `git diff --numstat` (the `+` column), the
changed-files table, ONE LINE PER GATE G1 to G8 with its real exit code, the
open-findings count, the item-status table, and the next expected action. It has
no length cap. Declare every deviation, including any place this block is wrong.

<<<BEGIN PLANF260R7>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 6 are reviewed; 2 through 6 PASSED. T001 is
CLOSED. T002 is open: `data_paths` now holds the one spelling of DECISION F260
D1's layout, and DECISION F260 D4 records why the resolver waits for the store.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Finish the layout consolidation. The four remaining hand-built
`jobs_dir() / <id> / "evidence"` expressions — two in `job_evidence.py`, one in
`repair_attest.py`, one in `do_cmd.py` — move onto
`data_paths.job_evidence_dir`, and the round-6 guard widens from one module to
the whole set that owns a job's evidence. `checkpoints.py` and `storage.py` keep
their `jobs_dir` calls: they name the CLASSIC store, which T004 deletes.

## Next Steps

- The unified Job record and its writer under `jobs/<16hex>/job.json`, moving
  `_persist_job` and `load_job_plan` off `task_jobs/` and DELETING
  `pingpong_job._jobs_dir`. Finding R-0814 is resolved there, against the fix
  clause it already carries.
- The ONE resolver, in the same round group as that writer, because 40 of the
  42 job-taking call sites take a `UUID` today (DECISION F260 D4).
- Then `runs/<run_id>/` keyed by run id, T003 consumer by consumer, T004 the
  classic runner, T005 the reachability test and the cluster deletion.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer, or a run
  log becomes unreadable between two commits.
- `job_record_path` names a path nothing writes yet; its docstring says so and
  the writer round is what makes it live.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
<<<END PLANF260R7>>>

<<<BEGIN GATE_R6>>>
Gate: R6 — the F260 R6 entry. R6 RULED DECISION F260 D4 AND GAVE `data_paths` THE ONE SPELLING OF DECISION F260 D1'S LAYOUT — `job_dir`, `job_record_path`, `job_evidence_dir` AND `run_dir` — THEN PUT `pingpong_job`'S TWO HAND-BUILT EVIDENCE PATHS ONTO IT. VERDICT PASS. Range 3aaeb042..99ca6406, eight commits, all single-parent, pushed to `origin/feature/f260-one-world`, no pull request created; the largest commit is 364 insertions and is a single `.agent/**` state write, the largest code commit 168, both under the AGENTS.md 500-insertion cap. THE REVIEWER RE-RAN ALL EIGHT GATES ITSELF. TRANSPORT: one digest `868a89bb4df7d29a92ef1b5654ed0d344932db534e9f56c434178e7840feb00c` across the reviewer's scratch original, the worker's saved copy at `.agent/authored/f260-r6.md` and the mirror at `.agent/last_block.md`; per §3 item 37 that chain covers those three artefacts and is NOT a claim about the bytes emitted into the worker's prompt. THE RECORD: `.agent/live_review.md` went 881955 to 887129, growth 5174 equal to `"\n"` plus a 5172-byte slice plus `"\n"`; the pre-image is a byte-exact PREFIX, the last blank-line unit equals the slice, and the TWO negative controls now sit one per region — a flip inside the appended paragraph is rejected by the last-unit reading and a flip inside the pre-image region is rejected by the prefix reading, which is the split the round-5 worker's deviation 2 earned. Registrations stayed 299, `Done:` stayed 4, and there are fifteen `Gate:` headers, all distinct. THE DECISION: `docs/roadmap/features/T2_F260.md` went 22955 to 25427 bytes and reconstructs BYTE-EXACTLY from its pre-image with the single D4PAIR substitution applied; the pair was classified MECHANICALLY, not by eye — the reviewer's own pre-emission run printed `TO contains FROM: false`, correcting the block's first draft, which had labelled an insertion APPEND-shaped because both anchors survive it while the FROM's bytes are contiguous and the inserted paragraph splits them (§3 item 15, caught before emission rather than after). As a REWRITE the §4.9 counts are attainable and were taken: FROM 1x before and 0x after, TO 0x before and 1x after, with `^### DECISION F260 D` matching five times and D0, D1, D2, D3 and D4 each appearing exactly once. THE SHIPPED CODE WAS RUN, NOT READ: with `REMEDY_DATA_DIR` pointed at a scratch directory the reviewer read `job_record_path(j).parent == job_evidence_dir(j).parent == job_dir(j)` as True — D1's whole claim, that a job's record and its evidence share ONE root — `run_dir(r).parent == runs_dir()` with `jobs_dir()` nowhere in its parents, the `root` argument honoured, and both `pingpong_job` equalities True, which is the no-behaviour-change property the two call-site swaps rest on. `ruff check` over both modules exits 0. `git diff --numstat` over the range reports `data_paths.py` at 42/0, `pingpong_job.py` at 13/5 and `tests/test_data_paths.py` at 113/0, and the range's path set is the ten files the block named. THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY: in a disposable worktree at `a02c25b3`, module resolving from that worktree so no install shadowed it, the unmutated control is exit 0 at 35 passed, and each of the four ordered properties turns the suite RED — keying `run_dir` under `jobs_dir` fails `test_a_run_hangs_under_runs_dir_and_never_under_jobs_dir`, moving the evidence out from beside the record fails `test_the_record_and_the_evidence_share_one_root`, ignoring the `root` argument fails `test_the_root_override_is_honoured_by_all_four`, and restoring the hand-built expression in `pingpong_job` fails `test_pingpong_job_no_longer_spells_the_evidence_path_itself` — with the control green again after each restore. THE FOURTH MUTATION IS THE INSTRUCTIVE ONE and the block predicted it exactly: only the AST guard fired, and the value-equality test beside it stayed GREEN, because the hand-built path is genuinely EQUAL to the new one. An equality reading cannot see a second spelling of a correct path; only reading the module can. That is why the block ordered both readings, and the mutation is the proof that neither is redundant. THE SUITES, re-run serially by the reviewer, all exit 0 at 35, 37, 37, 93, 5, 178, 303 and 42 — 730 tests, including the docs-round gate this change set's `docs/roadmap/` path required — and `integrity check --json` returned `"passed": true` with `"fail_count": 0` over 5 checks at handlers=342. THE WORKER CORRECTED THE REVIEWER AGAIN AND THE CORRECTION IS UPHELD. Its deviation 1 caught a defect in the block's own C2 recipe: `.agent/prose_slips.md` did NOT end with a newline at `3aaeb042` — 89710 bytes ending `iet rule 2).` — so the recipe `"\n" + SLIP4 + "\n" + SLIP5 + "\n"`, copied from the one C1 uses for `.agent/live_review.md`, which DOES end with a newline, only terminated the existing last line instead of creating a blank-line separator. The reviewer confirmed it by measurement: the file's blank-line unit count stayed at 128 across an append of two slips where it should have reached 130, and the R3 slip, SLIP4 and SLIP5 now sit as three consecutive lines in a file whose other 118 dated slips are blank-separated. G3 as written is fully met — prefix and remainder are both byte-exact — so the worker applied the recipe correctly and the defect is the reviewer's, in exactly the class §3 item 34 names: the block ordered an append into a file it had not read for what that file already held, and the reviewer's own pre-emission script checked the terminal byte of `.agent/live_review.md` and never of `.agent/prose_slips.md`. The damage is cosmetic and confined to `.agent/`, so under operator amendment amend0827-process-diet rule 2 it is a dated line in `.agent/prose_slips.md` and spends NO R-id, and no correction round is opened: that file is append-only and never rewritten, nothing gates on it, and no load-bearing claim landed false. The counter-measure is in the round-7 block, which orders the terminal byte READ AND REPORTED before the append and gates the blank-line unit count to rise by exactly one. Its deviation 2 caught a stale line number for `_task_stream_dir` — the block said 3568, the `def` is at 3565 — and it re-grepped as ordered, so the right function was edited; deviation 3 records that it declined to reuse a pre-existing unrelated scratch directory as a worktree name and created nothing over it, which is the right instinct; and deviation 6 records that it built the absence guard as an AST REFERENCE reading rather than a substring search, alias-proof and immune to comments, which the reviewer verified is what makes `_jobs_dir` correctly invisible to it.
<<<END GATE_R6>>>

<<<BEGIN SLIP6>>>
2026-09-06 · F260 R6 (reviewer) · The round-6 block's C2 ordered an append to `.agent/prose_slips.md` as `"\n"` + SLIP4 + `"\n"` + SLIP5 + `"\n"`, the same byte recipe C1 uses for `.agent/live_review.md`. That recipe is correct only for a file that already ends with a newline. `.agent/live_review.md` does; `.agent/prose_slips.md` did not — at `3aaeb042` it was 89710 bytes ending `iet rule 2).` with no terminator — so the leading `"\n"` merely finished the previous line instead of opening a blank-line separator, and the two new slips landed fused to the R3 slip above them. Measured: the file's blank-line unit count stayed at 128 across an append of two slips, where every one of the other 118 dated slips in it is blank-separated. The worker measured the discrepancy, applied the slice byte for byte as constraint 1 required, and declared it; gate G3 as written was fully met, because prefix and remainder were both byte-exact and neither reading looks at separators. THE LESSON: §3 item 34 requires the reviewer to read every file a block orders a change against for what it ALREADY HOLDS, and a file's TERMINAL BYTE is part of what it holds — the reviewer's own pre-emission script checked that byte for `.agent/live_review.md` and never for `.agent/prose_slips.md`, then reused the arithmetic across both. An append recipe is a function of the target's last byte, so it is derived per target and never copied between them, and the gate that catches it is a STRUCTURAL count — blank-line units before and after — rather than the byte-prefix reading, which is satisfied by a malformed append and a well-formed one alike. The round-7 block orders the terminal byte read and reported before the append and gates the unit count to rise by exactly one. No correction round is opened and no landed byte is rewritten: this file is append-only, nothing gates on it, and no load-bearing claim landed false. Reviewer-authored recipe defect; the damage is cosmetic and confined to `.agent/`; nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP6>>>
