STEP T002/5 — F260 · ROUND 9 · THE RECORD MOVE
(§3 item 37: every rule line below is exactly sixty-two U+2500 characters, and
no other line of this block's frame is a run of a repeated character.)

Goal:
  Move the ping-pong job record from `<data_root>/task_jobs/<16hex>/job.json` to
  `<data_root>/jobs/<16hex>/job.json`, so a job's record and its evidence finally
  share ONE root, and delete the three `task_job*` accessors with the store they
  named. This is the fix DECISION F260 D1 rules and the remaining fix condition
  of finding R-0814.

Base: `1523fde1b26892ee2c38166e2fad573f0569e397` (`1523fde1`). Every reading
quoted in this block was taken by the reviewer at that commit.

Bundle:
  C0a  Save this block verbatim as `.agent/authored/f260-r9.md`.
  C0b  Mirror it into `.agent/last_block.md`.
  C1   `.agent/plan.md` ← the PLAN slice, whole-file replacement.
  C2   `.agent/live_review.md` ← append the GATE_R8 slice.
  C3   `.agent/prose_slips.md` ← append the three SLIP lines.
  C4   THE MOVE, in ONE commit — see the SPEC below. It is one commit because a
       reader that does not move with the writer makes every ping-pong job
       unresolvable; see the measured probe under "Why C4 is atomic".
  C5   The two new tests, and the `Landed: R-0814` line.
  C6   Handback: rewrite `.agent/handoff.md`.

Change set — nothing outside these paths:
  .agent/authored/f260-r9.md            (new)
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/handoff.md
  packages/orchestration/data_paths.py
  packages/orchestration/pingpong_job.py
  packages/orchestration/job_evidence.py
  apps/cli/commands/teach_cmd.py
  tests/test_data_paths.py
  tests/orchestration/test_failure_wiring.py
  tests/orchestration/test_job_promote_consistency.py
  tests/orchestration/test_job_stop_integration.py
  tests/orchestration/test_job_worktree_handoff.py
  tests/orchestration/test_job_worktree_integration.py
  tests/orchestration/test_job_worktree_integrity.py
  tests/orchestration/test_pingpong_integration.py
  tests/orchestration/test_job_budgets.py
  tests/cli/test_teach_cmd.py

──────────────────────────────────────────────────────────────
WHY C4 IS ATOMIC — the reviewer measured this, do not re-derive it

At `1523fde1` the reviewer built a scratch data root holding all three shapes at
once and ran the two matchers over it. Readings:

  - `_classic_job_id_matches` globs `*.json` and returned `[]` for a 16-hex
    directory id, and the classic uuid for the classic id.
  - `_task_job_id_matches` re-pointed at `jobs_dir()` returned the 16-hex id for
    the ping-pong id and `[]` for the classic id.
  - A directory with no `job.json` matched neither.
  - The `resolve_any_job_id` union therefore has length 1 for both id kinds:
    one directory holding both shapes produces NO false ambiguity.
  - NEGATIVE CONTROL, and the reason C4 is one commit: `_task_job_id_matches`
    left pointing at `task_jobs/` returns `[]` for a record that has already
    moved. A writer that moves without its reader is exactly the
    `remedy teach narrate` regression of 2026-08-25.

──────────────────────────────────────────────────────────────
SPEC FOR C4 — described, not sliced; you write the code

(1) `packages/orchestration/data_paths.py`
    - DELETE `task_jobs_dir`, `task_job_dir` and `task_job_record_path`, and the
      comment block above `task_job_dir` that explains why the mirror pair
      existed. The "Remedy has TWO job stores" docstring paragraph is
      `task_jobs_dir`'s own docstring and goes with the function; F260 T004 still
      owns `resolve_any_job_id` itself and the shipped `TWO job stores` absence
      test, so do not add that test here.
    - `_task_job_id_matches`: glob `jobs_dir()` instead of `task_jobs_dir()`. Its
      docstring must say that `<data_root>/jobs/` now holds BOTH `<uuid>.json`
      FILES and `<16hex>/` DIRECTORIES, and that `is_dir()` plus the `job.json`
      check is what keeps the two populations apart.
    - `job_record_path`: its docstring currently opens "NOTHING WRITES HERE YET"
      and points at `task_jobs`. That is false after this commit. Rewrite it to
      say `pingpong_job._persist_job` writes here.
    - `resolve_any_job_id`'s docstring names `<data_root>/task_jobs/<16-hex>/
      job.json` as the second store. Correct it to `<data_root>/jobs/<16hex>/
      job.json` and say both stores now share the `jobs/` directory and are told
      apart by file-versus-directory.
    - Update the `Public API::` block at the top of the module: the three deleted
      names go, the survivors stay.

(2) `packages/orchestration/pingpong_job.py` — five call sites, measured at
    `1523fde1` at lines 382/384, 396/398, 1182/1184, 2675/2697 and 2853/2884.
    Replace `task_job_record_path` with `job_record_path` and `task_job_dir` with
    `job_dir`, import and call alike.
    HAZARD, and this is the one thing in C4 that is not mechanical: line 1184
    reads `job_dir = task_job_dir(job.job_id)` — a LOCAL VARIABLE already named
    `job_dir`, used again at lines 1203 and 1213. After the rename the local
    would shadow the imported function inside that scope. RENAME THE LOCAL to
    `job_root` at all three lines. Do not rely on the right-hand side being
    evaluated first.
    The docstring at line 2744 says the record is read from
    `task_jobs/<job-id>/`. Correct it.

(3) `packages/orchestration/job_evidence.py` — `task_job_dir` at lines 1149 and
    1160 becomes `job_dir`. The docstring at line 121 names
    `task_jobs/<id>/job.json`; correct it.

(4) `apps/cli/commands/teach_cmd.py` — the comments at lines 46 and 61 describe
    the second store as `task_jobs/<16-hex>/`. Correct them. No code changes.

(5) The tests that CALL the deleted accessors — replace `task_job_dir` with
    `job_dir`, import and call alike, in:
    `test_failure_wiring.py` (861, 867), `test_pingpong_integration.py` (15,
    147, 163, 179), `test_job_worktree_integrity.py` (25, 280),
    `test_job_promote_consistency.py` (351, 354), `test_job_worktree_handoff.py`
    (26, 154, 163, 171, 288, 403), `test_job_worktree_integration.py` (18, 180).
    In `test_job_worktree_handoff.py` line 288 the SAME local-shadowing hazard as
    (2) appears — `job_dir = task_job_dir(job.job_id)`, used at 291 and 292.
    Rename the local to `job_root`.

(6) The tests that hard-code the literal `"task_jobs"`. The reviewer resolved
    each site to its enclosing function at `1523fde1`; the six sites live in five
    enclosing functions, one of which is a shared helper, and through that helper
    seven tests depend on them:
      `tests/orchestration/test_job_budgets.py:1360`
        in `test_the_command_does_not_mutate_the_persisted_job`
      `tests/orchestration/test_job_stop_integration.py:527`, `:558`
        both in `test_a_three_task_job_stopped_after_task_one_exits_clean_with_no_leftovers`
      `tests/orchestration/test_job_stop_integration.py:860`
        in `test_a_planted_control_file_cannot_leak_a_secret_into_event_or_postmortem`
      `tests/cli/test_teach_cmd.py:207`
        in the helper `_write_task_job`, which three narrate tests call
      `tests/cli/test_teach_cmd.py:255`
        in `test_a_directory_without_a_job_file_is_not_a_job`
    Do NOT re-spell the layout by hand in these files. Import
    `data_paths.job_dir` (or `job_record_path`) and build the path from it, which
    is the same rule the D1 tests state: a test that rebuilds the path by hand
    pins its own copy and nothing else. The prose at
    `tests/cli/test_teach_cmd.py:198` names `task_jobs/`; correct it.

(7) `tests/test_data_paths.py`
    - DELETE `_task_layout`, `test_the_task_job_record_is_job_json_under_the_task_job_dir`
      and `test_the_root_override_is_honoured_by_both_task_job_helpers`, with the
      comment block above them (measured at lines 496-510), which predicted this
      collapse in as many words. The surviving D1 tests
      `test_the_record_is_named_job_json` and
      `test_the_root_override_is_honoured_by_all_four` already carry both
      readings. Confirm that before deleting; if either reading is NOT covered,
      keep it against the surviving names instead, and say so.
    - The comment above `_MIGRATED_OFF_JOBS_DIR_MODULES` (measured at lines
      291-296) says those modules "now spell it as `data_paths.task_job_dir` /
      `task_job_record_path`". Correct it to the surviving names.
    - The assertion messages of `test_pingpong_job_has_no_jobs_dir_attribute_at_all`
      (line 555) and `test_no_migrated_module_names_the_deleted_jobs_dir_helper`
      (line 583) both name `data_paths.task_job_dir`. Correct both.
    DO NOT TOUCH `_JOB_EVIDENCE_OWNING_MODULES`,
    `test_no_module_that_owns_job_evidence_spells_the_path_itself` or
    `test_the_classic_store_modules_still_call_jobs_dir`. The reviewer checked
    these against C4 at `1523fde1`: the first asserts ZERO AST references to the
    name `jobs_dir` in pingpong_job, job_evidence, repair_attest and do_cmd, and
    `job_dir` / `job_record_path` are DIFFERENT names under that reading, so C4
    does not trip it. The second requires `checkpoints` and `storage` to keep
    referencing `jobs_dir`; C4 touches neither module.

──────────────────────────────────────────────────────────────
SPEC FOR C5 — the two tests that make the round provable

Both go in `tests/test_data_paths.py`, inside `TestJobAndRunLayout`.

(A) `test_a_persisted_pingpong_job_writes_its_record_under_its_own_job_dir`
    Point `REMEDY_DATA_DIR` at `tmp_path`. Build the smallest `JobPlan`
    `pingpong_job` will persist, call `pingpong_job.save_job_plan`, and assert
    the returned path EQUALS `data_paths.job_record_path(job_id)`, that it is a
    real file on disk, and that `pingpong_job.job_evidence_dir(job_id).parent`
    EQUALS `data_paths.job_dir(job_id)` — the record and the evidence under ONE
    root, which is the remaining fix condition of R-0814. Assert the record is
    NOT under any path containing a `task_jobs` component.

(B) `test_a_pingpong_record_in_the_jobs_dir_is_still_resolvable_beside_a_classic_one`
    Point `REMEDY_DATA_DIR` at `tmp_path`. Write a classic `<uuid>.json` FILE and
    a ping-pong `<16hex>/job.json` DIRECTORY into the SAME `jobs_dir()`, plus a
    third directory with NO `job.json`. Assert `resolve_any_job_id` returns the
    ping-pong id for the ping-pong id and the classic id for the classic id —
    one match each, no ambiguity exit — and that the `job.json`-less directory
    resolves to nothing. This is the test the C4 atomicity argument rests on and
    the one gate G7(ii) mutates against.

Then, in the same commit, append to `.agent/live_review.md` ONE line of the shape
§4 item 4 fixes for a worker — `Landed: R-0814 — <what changed, which commit>` —
and nothing else. Do NOT write a `Done:` paragraph; the reviewer authors that at
the next gate. Report the byte length of the line you wrote: the block does not
name it, because the block did not write it.

──────────────────────────────────────────────────────────────
CONSTRAINTS

 1. Apply every authored slice BYTE FOR BYTE. If a slice looks wrong, apply it
    as given and declare the defect in the handback. Never repair a slice.
 2. Change-set discipline: no path outside the list above. The list bounds
    WRITES; it does not bound the reads, probes or worktrees you need.
 3. `.agent/plan.md` stays under 50 lines (AGENTS.md). The PLAN slice below was
    measured by the reviewer against that cap before emission.
 4. Both appends this round are to files that end with exactly ONE newline at
    `1523fde1`, measured: `.agent/live_review.md` at 898817 bytes and
    `.agent/prose_slips.md` at 97989 bytes. Derive each append recipe from its
    own target's terminal byte; do not copy one recipe to the other.
 5. Slice shapes, classified before emission: GATE_R8 is an APPEND to
    `.agent/live_review.md`, the three SLIPs an APPEND to
    `.agent/prose_slips.md`, PLAN a whole-file REWRITE of `.agent/plan.md`. NONE
    of them has a FROM, so no containment test applies and no FROM-zero count is
    ordered anywhere in this block.
 6. Commit order is fixed as the Bundle lists it. C1 before C2 is deliberate:
    this round touches the finding ledger, so §3 item 23 puts the plan first.
 7. `git status --porcelain` is EMPTY at the handback. Every destructive check
    runs in a disposable `git worktree`, never in the primary checkout
    (self-drive protocol G5).
 8. AGENTS.md throughout: self-review loop before every commit, 500-insertion
    cap per commit counting INSERTIONS only, push after committing, no force
    push, no work on `main`, no merge.

──────────────────────────────────────────────────────────────
DONE WHEN — eight gates, each RUN and its real exit code recorded

G1 TRANSPORT — one digest. `sha256sum .agent/authored/f260-r9.md` equals the
   digest in this block's BEGIN marker, and the same digest over
   `.agent/last_block.md`. One reading, not a chain. Per §3 item 37 this covers
   the saved copy and its mirror and is not a claim about the emitted bytes.

G2 THE RECORD — full byte forensics, both appends.
   (a) BYTE: at C2, `len(post) == 898817 + 1 + len(GATE_R8) + 1`, and the
       pre-image is a byte-exact PREFIX of the post-image. At C5, the second
       growth equals `1 + len(the Landed line) + 1` for the length YOU measured.
   (b) STRUCTURAL, independent of (a): split the post-image on `"\n\n"`; the
       LAST unit, with the file's own terminating newline STRIPPED, equals
       GATE_R8 exactly. Unit count runs 426 → 427 at C2 → 428 at C5.
   (c) NEGATIVE CONTROL: flip ONE byte inside the FIRST appended paragraph
       (§3 item 36) and confirm readings (a) and (b) BOTH reject it. Then
       restore and confirm both accept again.
   (d) POPULATIONS after C5: `^Gate: ` headers 18, all distinct;
       `^- R-\d{4} — ` registrations 299; `^Done: R-\d{4} — ` lines 4 over TWO
       distinct ids; `^Landed: R-0814 — ` exactly 1.

G3 THE SLIPS. `len(post) == 97989 + 1 + len(SLIP1) + 2 + len(SLIP2) + 2 +
   len(SLIP3) + 1`; the pre-image is a byte-exact PREFIX; blank-line units run
   131 → 134, a rise of exactly THREE, one per slip. If you measure 132 or 133
   the separators fused — that is the round-6 defect and the reason this gate
   states the rise rather than the total.

G4 THE PLAN. `.agent/plan.md` equals the PLAN slice plus exactly one trailing
   newline, byte for byte, and its line count is under 50.

G5 THE MOVE IS COMPLETE.
   (a) `hasattr(data_paths, n)` is False for `task_jobs_dir`, `task_job_dir` and
       `task_job_record_path`, and True for `jobs_dir`, `job_dir`,
       `job_record_path`, `job_evidence_dir` and `run_dir`. The second half is
       the non-vacuity control: it proves `hasattr` finds anything at all.
   (b) By AST over every `.py` file under `packages/`, `apps/` and `tests/`,
       references resolving to exactly `task_jobs_dir`, `task_job_dir` or
       `task_job_record_path` number ZERO. NON-VACUITY CONTROL: the same reading
       over `job_dir` is NON-ZERO. Both halves were run at the base by the
       reviewer: at `1523fde1` the three deleted names are NON-zero and
       `job_dir` is non-zero, so this gate can fail and its control can pass.
   (c) The literal substring `task_jobs` occurs ZERO times under `packages/`,
       `apps/` and `tests/`. Measured at `1523fde1` it occurs, so the gate is not
       vacuous. `docs/roadmap/features/` is deliberately OUT of scope: the
       feature files record the history and are not rewritten.
   (d) VALUE, with `REMEDY_DATA_DIR` at a scratch directory: `job_dir(j)` equals
       `jobs_dir() / j`; `job_record_path(j)` equals `job_dir(j) / "job.json"`;
       `job_evidence_dir(j)` equals `job_dir(j) / "evidence"`; and the `root`
       argument is honoured by all four against an env root set to a DIFFERENT
       directory, so a function that drops `root` cannot pass by coincidence.

G6 THE SUITES, run SERIALLY, each exit code recorded separately. The reviewer
   ran all three groups at `1523fde1` and every one was green, so any red is
   this round's:
     `pytest tests/test_data_paths.py tests/orchestration/test_mint_call_sites.py
      tests/cli/test_golden_path.py -q -p no:randomly`        (93 passed at base)
     `pytest tests/orchestration/test_job_worktree_handoff.py
      tests/orchestration/test_job_worktree_integration.py
      tests/orchestration/test_job_worktree_integrity.py
      tests/orchestration/test_job_promote_consistency.py
      tests/orchestration/test_failure_wiring.py
      tests/orchestration/test_pingpong_integration.py -q -p no:randomly`
                                                             (165 passed at base)
     `pytest tests/orchestration/test_job_stop_integration.py
      tests/orchestration/test_job_budgets.py
      tests/cli/test_teach_cmd.py -q -p no:randomly`          (186 passed at base)
   The first group carries the canary. Also run
   `python3 -m apps.cli.grouped integrity check --json` and record `passed`,
   `fail_count` and the check count.

G7 THE MUTATION RED-PROOF, in a disposable `git worktree` at the C5 commit,
   with `__pycache__` purged and `python3 -B`, and the module resolving from
   THAT worktree — confirm the resolution before trusting a colour.
   (i)   UNMUTATED CONTROL FIRST, in that worktree: run
         `tests/test_data_paths.py` and record exit code AND passed count. A
         colour with no baseline is not evidence (§3 item 33).
   (ii)  Point `_task_job_id_matches` back at a literal `task_jobs` directory.
         Test (B) must FAIL. Name the failing node id.
   (iii) Make `_persist_job` write to `jobs_dir() / job.job_id / "record.json"`
         instead of `job_record_path(job.job_id)`. Test (A) must FAIL. Name the
         failing node id.
   (iv)  Restore after EACH mutation and confirm the control is green again.
   Revert targets are named by PATH and the bytes are unique in that file at the
   commit you run at — verify that uniqueness before each edit (§3 item 25).

G8 LINT AND CLEAN TREE. `ruff check` over EXACTLY the change-set paths under
   `packages/`, `apps/` and `tests/` exits 0. Scoped to those files on purpose:
   `ruff check packages/` and `ruff check tests/orchestration/` are RED at the
   base with pre-existing errors that are not this feature's, so a
   directory-scoped gate could not pass, while the reviewer measured the
   file-scoped reading GREEN at `1523fde1` — this gate starts green and only this
   round can redden it. Then `git status --porcelain` and `git ls-files
   .remedy-wt` are both EMPTY.

──────────────────────────────────────────────────────────────
HANDBACK

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, `SESSION 3 of feature F260`, branch, commit SHAs, the changed-files table
with its `+/-` column read from `git diff --numstat` and never re-derived by eye
(§3 item 28), ONE LINE PER GATE with its real exit code, the open-findings count,
and the next expected action. No length cap applies (amend0827 rule 3). Declare
every deviation, including any place this block is wrong.

──────────────────────────────────────────────────────────────
AUTHORED SLICES

A slice is the bytes of the lines strictly BETWEEN its BEGIN and END marker
lines, joined by `"\n"`, carrying NO trailing newline. The marker lines are
never part of any slice and never reach any file.

<<<BEGIN GATE_R8>>>
Gate: R8 — the F260 R8 entry. R8 GAVE THE PING-PONG STORE ONE SPELLING AND DELETED THE MODULE-LOCAL `_jobs_dir`. VERDICT PASS. Range 072b54ed..607e2bec, seven commits, all single-parent, pushed to `origin/feature/f260-one-world`, no pull request created; largest insertion count 349 (a single `.agent/**` state write), largest code commit 257, both under the AGENTS.md 500-insertion cap. THE REVIEWER RE-RAN EVERY GATE ITSELF rather than reading the handback's numbers. TRANSPORT: one digest `f362c984379e56fb99a3d1d6f58fb62cff55d7f02ebef6d26f4d15bf56209ed1` across the reviewer's scratch original, the saved copy at `.agent/authored/f260-r8.md` and the mirror at `.agent/last_block.md`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into the prompt. THE RECORD: `.agent/live_review.md` 893805 to 898817 bytes, growth 5012 equal to a newline plus a 5010-byte slice plus a newline; the pre-image is a byte-exact PREFIX, the last blank-line unit with the file's terminating newline stripped equals the slice, and the two negative controls each reject in its OWN region and only there; blank-line units 425 to 426. THE SLIP FILE, with the round-8 counter-measure working: 94802 to 97989 bytes, the terminal byte before the append was a newline, and blank-line units rose 129 to 131 — a rise of exactly TWO, one per slip. The two-newline separator between the two slips was itself a correction the reviewer's pre-emission check caught before emission: with single newlines throughout the count reaches 130, which is the round-6 defect recurring one position over. THE DELETED NAME IS GONE, AND THE STORE DID NOT MOVE. `hasattr(pingpong_job, "_jobs_dir")` is False. By AST, references resolving to exactly `_jobs_dir` number 0 in `pingpong_job.py` (6 at the base `072b54ed`) and 0 in `job_evidence.py` (2 at that base). With `REMEDY_DATA_DIR` pointed at a scratch directory, `task_job_dir(j)` equals `task_jobs_dir() / j` and `task_job_record_path(j)` equals `task_jobs_dir() / j / "job.json"`, and the `root` override is honoured — the value-preservation property this round rests on. RUFF over exactly the eleven files C4 touched exits 0. It is scoped to those files on purpose: measured at `072b54ed`, `ruff check packages/` exits 1 with 2 errors and `ruff check tests/orchestration/` exits 1 with 11, all PRE-EXISTING and none of them this feature's, so a directory-scoped gate here could not pass. THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY, in a disposable worktree at `b92d096f` with the module resolving from that worktree. Unmutated control exit 0 at 46 passed. Ignoring `root` in `task_job_dir` fails `test_the_root_override_is_honoured_by_both_task_job_helpers`. Re-adding `_jobs_dir` as a `def` fails BOTH `test_pingpong_job_has_no_jobs_dir_attribute_at_all` AND `test_no_migrated_module_names_the_deleted_jobs_dir_helper[packages.orchestration.pingpong_job]` — which is the worker's guard fix working, and is the reading the reviewer's own block got wrong. Control green after each restore. THE LOAD-BEARING IMPORT PROOF ALSO REPRODUCES: deleting the single function-scoped import at `pingpong_job.py:2853` gives `NameError: name 'task_job_dir' is not defined` at `pingpong_job.py:2883`, failing exactly the two `tests/orchestration/test_job_worktree_handoff.py` tests the block predicted, and the suite is green again on restore. THE SUITES, re-run serially by the reviewer, all exit 0: 58, 34, 26, 26, 13, 24, 10, 46, 93, 178 and 42 — 550 tests — and `integrity check --json` returned `"passed": true` with `"fail_count": 0` over 5 checks. BOTH BLOCK DEFECTS THE WORKER DECLARED ARE UPHELD, and both were reproduced by the reviewer; they are two of the three `.agent/prose_slips.md` lines the round-9 block appends, and neither spends an R-id because both are reviewer-authored gate defects with nothing wrong on disk under `packages/`, `apps/`, `tests/` or `docs/`, which is what operator amendment amend0827-process-diet rule 2 routes there.
<<<END GATE_R8>>>

<<<BEGIN SLIP1>>>
2026-09-06 · F260 R8 (reviewer) · G4(b) of the round-8 block ordered, as its NON-VACUITY control, that `_jobs_dir` AST references be NON-ZERO in `packages/orchestration/storage.py`. Measured at `607e2bec` and at the base `072b54ed` alike: ZERO. `storage.py` names `_resolve_jobs_dir`, a different symbol that merely contains the same substring — which the block's own DO-NOT-TOUCH paragraph says in as many words, forty lines above the gate that contradicted it. The control could not pass in any round. THE LESSON: §3 item 12 and finding R-0364 require a gate to be RUN AT ITS BASE before it is ordered; the reviewer ran `ruff` at the base and never ran the AST reading it was about to gate on, so the one clause whose whole job was to prove the search could find anything was the one clause never executed. A non-vacuity control is a gate like any other and is measured before emission. Reviewer-authored vacuous gate clause; the gate's load-bearing half was correct and nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP1>>>

<<<BEGIN SLIP2>>>
2026-09-06 · F260 R8 (reviewer) · G6(iii) of the round-8 block ordered a revived `_jobs_dir` to fail BOTH the `hasattr` reading and "the same AST reference reading" the guard paragraph specified. A revived function is a `def`, so it parses to a `FunctionDef` node and produces no `ast.Name`, `ast.Attribute` or `ast.alias` at all — the reference reading round 7 built cannot see a definition, and the reviewer confirmed it independently on a two-line parse. The worker measured this at its first C4, added a `_names_of` helper covering the binding forms, left round 7's reference helper untouched because that one is correct for ITS property, and re-measured green. THE LESSON: §3 item 18 asks that a recipe and the property it must establish be read against each other, and two guards that sound alike — "no module CALLS this" and "no module DEFINES this" — need different AST readings. The block reused a reading by name instead of by what it matches. Reviewer-authored recipe/property mismatch, caught and repaired by the worker inside the round; nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP2>>>

<<<BEGIN SLIP3>>>
2026-09-06 · F260 R9 (reviewer) · The open-finding arithmetic §3 item 10 prescribes — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — DOUBLE-COUNTS a resolution that was written in two paragraphs, and the end-of-session-2 handoff reported 295 open findings through it. Measured at `1523fde1`: `.agent/live_review.md` holds 299 registration paragraphs carrying 299 DISTINCT ids, and 4 `Done:` lines carrying only TWO distinct ids — `R-0721`, resolved in part at F037 R12 and in remainder at R14, and `R-0725`, the same shape at F037 R18 and R19 — so the open set counted BY DISTINCT ID is 297 and not 295. The formula is right about the two populations it names and wrong to subtract one from the other, because a `Done:` LINE is not a resolved FINDING. THE LESSON is owed to the checklist and cannot be paid now: amend0827-process-diet rule 4 freezes §3 for the duration of an open feature, so it waits for F260's single consolidation pass, which may not lengthen the list — the merge target is item 10 itself, whose own text already asks for the set to be derived mechanically. Reviewer-prose arithmetic in a rewritten state file and never in the append-only record, whose gate entries state the two populations and never their difference; nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP3>>>

<<<BEGIN PLAN>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 8 are reviewed and 2 to 8 PASSED. T001 is
CLOSED. T002 is open, and this round is its centre: the ping-pong record moves
to the root DECISION F260 D1 rules.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

THE RECORD MOVE. `data_paths.task_job_dir` and `task_job_record_path` are
deleted and `pingpong_job._persist_job` writes through `job_record_path`, so
`<data_root>/task_jobs/<16hex>/job.json` becomes
`<data_root>/jobs/<16hex>/job.json` and a job's record and its evidence share
one root. `data_paths._task_job_id_matches` moves onto `jobs_dir()` in the SAME
commit, or every ping-pong job becomes unresolvable. Finding R-0814's remaining
fix conditions — one root, and a test asserting it — are discharged here.

## Next Steps

- The ONE resolver over the one store: `resolve_job_id` and `resolve_any_job_id`
  collapse into one `str`-returning function, which needs `storage.load_job`'s
  signature and its forty call sites across nine `apps/cli/commands/` modules
  (DECISION F260 D4). Finding R-0809 belongs to that step.
- Then `runs/<run_id>/` keyed by run id, replacing `pingpong_runs/`.
- Then T003 consumer by consumer, T004 the classic runner, T005 the
  reachability test and the cluster deletion.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer.
- `pingpong_job` imports `data_paths` only inside function bodies, so each call
  site carries its own import; one such site sits inside a compound boolean.
- `<data_root>/jobs/` now holds both `<uuid>.json` files and `<16hex>/`
  directories. The two matchers were measured not to see each other's entries,
  but any new reader of that directory must make the same distinction.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
<<<END PLAN>>>

──────────────────────────────────────────────────────────────
