STEP T002/6 — F260 · ROUND 14 — ONE SPELLING FOR THE RUN-LOG JOIN

Goal:        Delete the LAST production hand-spelling of the job-keyed run-log
             layout. `RunLogWriter.__init__` still joins `root / self._job_id`
             onto a runs BASE it is handed; give it a DATA root instead and let
             `data_paths.run_log_dir` build the directory, so DECISION F260 D1's
             re-key of `<data_root>/runs/` by RUN id becomes a change to one
             function body plus the run-id plumbing, and to nothing else.

Base:        `4f265f91cbdf2f4c327e9dd303b8cd78c146618d` (round 13, reviewed PASS).

WHY THIS ROUND AND NOT THE TEST-SIDE SWEEP. Round 13's handback and
`.agent/plan.md` both name "the TEST side of the run-log spelling" as the next
step. The reviewer measured that step at `4f265f91` and is DECLINING it; the
measurement and the ruling are DECISION F260 D6, which C2 records. In short:
those tests supply a JOB id, D1 re-keys the directory by RUN id, so each needs a
SEMANTIC change at the re-key and not a spelling change — routing them through
`run_log_dir` first is churn the re-key undoes. The join below is the opposite:
deleted once, and it stays deleted.

Bundle:      C0a  save this block verbatim to `.agent/authored/f260-r14.md`
             C0b  mirror the same bytes into `.agent/last_block.md`
             C1   rewrite `.agent/plan.md` from the PLAN slice
             C2   append GATE_R13 to `.agent/live_review.md` AND DEC_D6 to
                  `.agent/decisions.md`, in that order, in ONE commit
             C3   append SLIP14, SLIP15, SLIP16, SLIP17 to `.agent/prose_slips.md`
             C4   SPEC (1) `RunLogWriter` takes a data root + SPEC (2) its tests
             C5   SPEC (3) the eight production call sites and the one comment
             C6   SPEC (4) the two other test files that pass `runs_root`
             C7   rewrite `.agent/handoff.md` (the handback)

Change:      EXACTLY these paths, nothing else:
               .agent/authored/f260-r14.md
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/decisions.md
               .agent/prose_slips.md
               .agent/handoff.md
               packages/orchestration/run_log.py
               tests/test_run_log.py
               packages/orchestration/timeline.py
               packages/orchestration/worker_queue.py
               packages/orchestration/patch_apply.py
               packages/orchestration/patch_revert.py
               packages/orchestration/safe_points.py
               packages/orchestration/pingpong_job.py
               packages/orchestration/prompt_trace.py
               tests/test_test_runner.py
               tests/cli/test_propose_cli.py

Constraints:
 1. A slice is applied byte for byte. If a slice looks wrong, apply it anyway
    and declare the problem in the handback; never edit a slice.
 2. NO LAYOUT CHANGE. `<data_root>/runs/<job_id>/<run_id>.jsonl` is exactly
    where a run log lives before this round and exactly where it lives after.
    This round moves WHO SPELLS the join, never the join's result. The re-key
    to `<run_id>` is D1's own work and is NOT performed here.
 3. THE RED-PROOF OBSERVER IS NAMED AND IS NOT SWEPT. Two tests in
    `tests/test_run_log.py` assert the writer's directory against a HAND-SPELLED
    right-hand side — `test_creates_job_directory` and
    `test_path_is_inside_job_directory`, at base lines 125 and 131. Their
    right-hand sides move from `tmp_path / str(job_id)` to
    `tmp_path / "runs" / str(job_id)` and STAY LITERAL. Do NOT route them
    through `run_log_dir`: they are what makes G6 able to fail, and round 12 of
    this feature is the record of what happens when a sweep consumes its own
    observer. The three `run_log_dir` tests in `tests/test_data_paths.py` are
    literal for the same reason and that file is NOT in the change set.
 4. SEARCH BY IDENTIFIER, NEVER BY SUBSTRING. Measured at the base: a SUBSTRING
    search for `runs_root` hits 17 files, because `job_evidence.py`,
    `pingpong_loop.py` and `worktree_resume.py` carry `pp_runs_root` locals and
    `local_candidate_generator.py` and `local_model_advisor.py` each define a
    `_runs_root(data_dir)` helper for their OWN run stores. A WORD-BOUNDED
    search (`\bruns_root\b`) hits 37 occurrences in 11 files, and those 11 are
    exactly the code files of the change set above. Use the word-bounded
    reading everywhere, and touch none of those five other modules — their
    stores are not this one. The same applies to `_runs_dir_default`:
    word-bounded it occurs TWICE, both in `run_log.py` (lines 34 and 114),
    while a substring search also hits `tests/test_data_paths.py:76`, which is
    a test NAMED `test_runs_dir_default` and is not the symbol.
 5. `scripts/` AND `tests/test_remedy_smoke_script.py` ARE NOT TOUCHED. That
    test pins the SHELL smoke script to `RUNS_ROOT=".data/runs"`. This round
    does not change that on-disk convention, so those guards stay green
    untouched. Checked at the base so you do not chase it.
 6. Every `RunLogWriter(job_id=...)` call that passes NO root is left alone.
    There are many and they already fall through to the module default;
    leaving them is what keeps this diff the size of its idea.
 7. IMPORT CONVENTION IS DECIDED PER FILE, following what that file already
    does, and no second convention is introduced. `ruff check` enforces `I001`
    through this repository's own `pyproject.toml`. `run_log.py` imports
    `data_paths` at MODULE level (line 34), so the new name goes there. In the
    consumer files this round mostly REMOVES a `runs_dir` call rather than
    adding one — if that leaves an import unused, remove it (`F401`) and
    declare the removal, per file.
 8. `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md`
    ALL THREE end with exactly ONE newline at the base — MEASURED at
    `4f265f91`, not recalled, because the round-13 block stated one of them
    wrongly and the round-12 block stated it wrongly in the opposite direction.
    Derive each recipe from its own target's terminal byte anyway, measured at
    the base, and state all three measurements in the handback.
 9. G4 IS A PRE-EDIT PROBE AND RUNS BEFORE C4; every other gate runs at C6.
    Stated as an ordering rather than as the word "before" because the two
    cannot both be met by one sentence: G4 measures the equality the edit
    depends on, so it can only be taken while `run_log.py` still holds the old
    join. The handback is C7, so no gate reading may be taken after the
    handback exists. C7's own insertion count is not reported by C7; the
    reviewer measures it at the next gate.
10. Every destructive check runs in a disposable `git worktree` under
    `.remedy-wt/`, removed by EXACT PATH before the handback; the primary
    checkout satisfies `git status --porcelain` == empty at the handback.
11. `cmp` is denied in this sandbox. Use `filecmp.cmp(shallow=False)` plus
    sha256. `remedy` is invoked as `python3 -m apps.cli.grouped`, `ruff` as
    `python3 -m ruff`. Purge `__pycache__` and run `python3 -B` for every
    mutation reading.

SPEC (1) — THE WRITER TAKES A DATA ROOT

In `packages/orchestration/run_log.py`:

  - line 34 reads
    `from packages.orchestration.data_paths import runs_dir as _runs_dir_default`.
    Replace the imported name with `run_log_dir`, keeping the module-level
    position and isort order. The aliased binding disappears with it; per
    constraint 4 nothing else in the repository uses that symbol.
  - `RunLogWriter.__init__`'s keyword-only parameter `runs_root: Path | None`
    becomes `data_root: Path | None`, same `None` default, same keyword-only
    position, same place in the signature.
  - the three lines that build the path (base lines 114-116)

        root = runs_root if runs_root is not None else _runs_dir_default()
        job_dir = root / self._job_id
        job_dir.mkdir(parents=True, exist_ok=True)

    become two:

        job_dir = run_log_dir(self._job_id, data_root)
        job_dir.mkdir(parents=True, exist_ok=True)

    `run_log_dir` resolves a `None` root through `runs_dir`, which is the same
    fallback `_runs_dir_default()` performed. THAT EQUALITY IS NOT ASSUMED: G4
    measures it before anything is edited.
  - the class docstring line 97 says
    `Creates <runs_root>/<job_id>/<run_id>.jsonl on first write`. It becomes
    `<data_root>/runs/<job_id>/<run_id>.jsonl` — the same directory, named by
    the root the caller now passes.
  - the module docstring line 5 already reads
    `<REMEDY_DATA_DIR>/runs/<job_id>/<run_id>.jsonl` and is CORRECT. Leave it.
    Recorded so you do not "fix" it.

Add a one-line WHY comment directly above `__init__`, in this file's voice,
saying the job-keyed join lives in `data_paths.run_log_dir` so DECISION F260 D1's
re-key changes one function body. Do NOT change `new_run_id`, the `path` and
`run_id` properties, `append`, or the event shape.

SPEC (2) — THE WRITER'S OWN TESTS

In `tests/test_run_log.py` every `RunLogWriter(...)` construction passes
`runs_root=tmp_path`. Measured at the base: TWENTY-ONE word-bounded occurrences
of `runs_root` in this file and none outside those constructions. Each becomes
`data_root=tmp_path`.

Because `tmp_path` was being used AS the runs base and is now the DATA root, the
writer's directory moves from `tmp_path/<job_id>/` to `tmp_path/runs/<job_id>/`
inside these tests. Two tests assert that directory and BOTH keep a literal
right-hand side, per constraint 3:

  - `test_creates_job_directory` — `job_dir = tmp_path / "runs" / str(job_id)`
  - `test_path_is_inside_job_directory` —
    `assert writer.path.parent == tmp_path / "runs" / str(job_id)`

Re-grep the file for any OTHER assertion naming a path relative to `tmp_path`
and REPORT WHAT YOU FOUND; the reviewer measured two, and the count you measure
is the one that binds.

Add ONE new test to `TestRunLogWriterConstruction`: with NO `data_root` argument
and a monkeypatched `REMEDY_DATA_DIR`, the writer's directory equals
`<that dir>/runs/<job_id>` — spelled LITERALLY, not through the accessor. This
pins the default path the deleted alias used to carry.

SPEC (3) — THE PRODUCTION CALL SITES AND THE ONE COMMENT

Eight constructions pass `runs_root`. Line numbers measured at the base
`4f265f91`; re-grep each before editing and report the count you re-measured.

  timeline.py:65        `RunLogWriter(jid, runs_root=runs_dir(Path(data_dir)))`
                        → `RunLogWriter(jid, data_root=Path(data_dir))`
  worker_queue.py:489   `runs_root=runs_dir(root)` → `data_root=root`
  patch_apply.py:527-528  `runs_root = runs_dir(data_dir) if data_dir is not None else None`
                        then `RunLogWriter(job_id=job.id, runs_root=runs_root)`
                        → the local goes away; pass `data_root=data_dir`
  patch_apply.py:565-566  the SAME pair a second time — both move
  patch_revert.py:245-246 `runs_root = runs_dir(actual_data_dir)` then the call
                        → the local goes away; pass `data_root=actual_data_dir`
  safe_points.py:675    `runs_root=runs_dir()` → DROP the argument entirely
  pingpong_job.py:3182  `runs_root=runs_dir()` → DROP the argument entirely

`patch_apply.py` passing `data_root=data_dir` when `data_dir` is `None` is
CORRECT and is the point of the change: `run_log_dir(job_id, None)` resolves the
process data root, which is exactly what `RunLogWriter` did with a `None`
`runs_root` before. State that in the handback; do not add a guard.

  prompt_trace.py:215   the comment ``RunLogWriter.path.parent`` is
                        ``<runs_root>/<job_id>/`` → ``<data_root>/runs/<job_id>/``.
                        COMMENT ONLY; no code in that file changes.

SPEC (4) — THE OTHER TWO TEST FILES

  tests/test_test_runner.py:344   `RunLogWriter(job_id=job.id, runs_root=tmp_path / "runs")`
                                  → `RunLogWriter(job_id=job.id, data_root=tmp_path)`
                                  The written path is unchanged by construction.
  tests/cli/test_propose_cli.py:339-340
                                  `runs_dir = tmp_path / "runs"` then
                                  `RunLogWriter(UUID(job_uuid), runs_root=runs_dir)`
                                  → `RunLogWriter(UUID(job_uuid), data_root=tmp_path)`.
                                  If the local `runs_dir` is then unused, delete
                                  that line too; report whether it was.

DONE WHEN — EIGHT GATES

Every gate is EXECUTED and its REAL exit code recorded, one line per gate in the
handback. "Green" as a word is a finding.

G1 TRANSPORT. `sha256sum .agent/authored/f260-r14.md .agent/last_block.md`;
   both equal the digest the delegation names. One comparison, not a chain.

G2 THE TWO RECORDS. After C2, prove EACH of `.agent/live_review.md` and
   `.agent/decisions.md` equals its own pre-image plus its own appended slice,
   by TWO independent readers per file:
   (a) exact-image byte equality against the recipe derived in constraint 8;
   (b) a STRUCTURAL reader that splits that whole file on `"\n\n"`, counts the
       units itself, and compares the LAST N units in order against that file's
       slice paragraphs. N is counted by your script, never asserted by this
       block, and the reading covers the WHOLE appended region.
   (c) a negative control per file, flipping one byte inside the FIRST appended
       paragraph, confirming BOTH readers reject it and both accept after
       restore. Run it in memory, not by writing bad bytes to either file.
   (d) report, for `.agent/live_review.md`, the `^Gate: ` count, registrations,
       `^Done: ` lines, and the open set BY DISTINCT ID after C2; and for
       `.agent/decisions.md`, the count of `^### DECISION F260 D` headings,
       which must be 1 for each of D5 and D6 and must not have changed for D5.

G3 THE PROSE FILES. `.agent/plan.md` disk bytes equal the PLAN slice plus one
   trailing newline; report its line count, which must be under 50.
   `.agent/prose_slips.md` equals its pre-image plus the constraint-8 recipe
   applied to the four slices IN ORDER; report bytes before and after and the
   blank-line unit count before and after.

G4 THE FALLBACK EQUALITY, MEASURED BEFORE ANYTHING IS EDITED. A scratch probe
   under `.remedy-wt/` prints BOTH sides of the equality this round rests on and
   confirms each pair equal, for three cases:
     - explicit root: `runs_dir(R) / str(J)` versus `run_log_dir(J, R)`
     - no root, under a monkeypatched `REMEDY_DATA_DIR`:
       `_runs_dir_default() / str(J)` versus `run_log_dir(J, None)`
     - `J` as a `UUID` and as its `str()` form, which must agree
   Report the printed pairs, not a summary. This is what makes "no layout
   change" a measurement rather than a claim.

G5 THE JOIN IS GONE AND ONE SPELLING SURVIVES. At C6, enumerating `git ls-files`
   IN PYTHON and filtering to `.py` under `packages/`, `apps/` and `tests/` (a
   `tests/**/*.py` shell glob silently misses `tests/test_data_paths.py`):
   (a) the bytes `root / self._job_id` occur ZERO times in `run_log.py` — base
       count 1 — and the WORD-BOUNDED identifier `_runs_dir_default` occurs
       ZERO times anywhere in that file set, against a base count of 2, both in
       `run_log.py`. Report both base and C6 readings.
   (b) an AST reading of `run_log.py` counts calls to `run_log_dir`: exactly 1
       at C6, 0 at the base.
   (c) the WORD-BOUNDED identifier `runs_root` occurs ZERO times in that file
       set, against a base count of 37 in 11 files. Report every surviving
       occurrence with its file and line; any survivor FAILS the gate.

G6 MUTATION RED-PROOF, AND IT MUST BE ABLE TO FAIL. In a disposable worktree at
   C6, `python3 -B`, `__pycache__` enumerated as 0:
   (i)   CONTROL FIRST, unmutated, over `tests/test_run_log.py
         tests/test_data_paths.py tests/test_timeline.py tests/test_patch_apply.py`:
         record exit code and count. Confirm module resolution by printing
         `data_paths.__file__` and the live BODY of `run_log_dir` from that
         worktree before trusting any colour.
   (ii)  Verify the bytes `    return runs_dir(root) / str(job_id)` occur EXACTLY
         ONCE in that worktree's `packages/orchestration/data_paths.py`, then
         replace that one line with
         `    return runs_dir(root) / (str(job_id) + "_MUTATED")` — note the
         PARENTHESES; without them the expression is a `Path + str` TypeError
         rather than a different path, and the run reddens for the wrong reason.
         Re-print the live BODY to prove the mutation is loaded. Re-run the SAME
         selection. IT MUST GO RED, and the two tests constraint 3 names must be
         AMONG the failures — report the failure count, the failing files, and
         whether those two are in the list.
   (iii) Restore the original line, re-run the control, and show
         `git status --porcelain` and `git diff HEAD --stat` EMPTY in that
         worktree. Remove the worktree BY EXACT PATH and `git worktree prune`.
   If (ii) does NOT go red, STOP, do not reshape anything to make it red, and
   report the measurement — that would mean the writer no longer routes through
   the accessor, which SPEC (1) forbids.

G7 THE SUITES, SERIALLY, each captured to a file under `.remedy-wt/` and read
   from the capture:
   (1) `python3 -m pytest tests/test_run_log.py tests/test_data_paths.py
       tests/test_timeline.py tests/test_patch_apply.py tests/test_test_runner.py
       -q -p no:randomly`
   (2) `python3 -m pytest tests/orchestration/ -q -p no:randomly`
   (3) `python3 -m pytest tests/cli/ -q -p no:randomly`
   (4) `python3 -m apps.cli.grouped integrity check --json`
   The canary is inside (3); verify its presence with
   `python3 -m pytest tests/cli/test_golden_path.py --collect-only` and report
   the collected count. Report each suite's real numbers.

G8 LINT AND CLEAN TREE. `python3 -m ruff check` over exactly the edited `.py`
   paths of the change set — COUNT THEM YOURSELF and report the number:
   `All checks passed!`. Then `git status --porcelain` and
   `git ls-files .remedy-wt`, both EMPTY.
   NOTE, measured at the base so you do not chase it: `ruff check` over ALL of
   `packages/orchestration/` reports two PRE-EXISTING errors, `UP035` at
   `dag_schedule.py:36` and `F821` at `gauntlet_injection.py:286`. Neither file
   is in this change set and neither is yours to fix.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry the SESSION
             NUMBER (this is SESSION 5 of F260, round 14), the changed-files
             table with `+/-` from `git diff --numstat` and never re-derived by
             eye, one line per gate with its real exit code, the open-findings
             count BY DISTINCT ID, every deviation, and the item-status table.
             Push after the handback commit.

BEGIN PLAN
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 13 are reviewed and 2 to 13 PASSED. T001 is
CLOSED. T002 is open: the job record has MOVED, R-0814 is resolved, both
resolvers return `str`, the ping-pong run store has one spelling on both sides,
and the run-log store has one spelling on the production READ side.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store, now `<data_root>/jobs/<16hex>/job.json`, become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

ONE SPELLING FOR THE RUN-LOG JOIN. `RunLogWriter.__init__` still joins
`root / self._job_id` onto a runs BASE it is handed — the last production
hand-spelling of the job-keyed layout. It takes a DATA root instead and builds
its directory with `data_paths.run_log_dir`. Eight production call sites and
three test files move with it.

## Next Steps

- THE RE-KEY ITSELF: `run_log_dir` and `pingpong_run_dir` collapse onto
  `run_dir`, keyed by RUN id — DECISION F260 D1. `RunLogWriter` already mints a
  run id, so the writer side is short; the READER side needs a job to name its
  runs, which makes the step below its prerequisite.
- `Job.run_refs`, the plural run list D1 names and nothing on disk carries yet:
  no reader can find a job's runs once `<data_root>/runs/` is keyed by run id.
- The rest of T002: the unified record's own administrative fields — measured at
  `4f265f91`, eight of D1's eleven have no counterpart in `JobPlan` — and the
  Mission extension.
- Then T003 consumer by consumer; T004 the classic runner, the classic store and
  the resolver collapse together (DECISION F260 D5); T005 the reachability test
  and the cluster deletion.

## Risks

- The test side of the run-log spelling is DECLINED, not forgotten: DECISION
  F260 D6 records why, and the re-key inherits those sites.
- The soft limit is 25 rounds or 7 sessions. This is round 14 of session 5 and
  the remaining scope is larger than the rounds left, so split-and-close is the
  likely endgame and each round leaves a self-consistent tree.
END PLAN

BEGIN GATE_R13
Gate: R13 — the F260 R13 entry. R13 GAVE THE LIVE JOB-KEYED RUN-LOG STORE ONE SPELLING IN `data_paths` AND MOVED NINE HAND-SPELLED SITES IN SEVEN MODULES ONTO IT. VERDICT PASS. Range `4d13f5a02608a40081a7ebacf779124cc6318309`..`4f265f91cbdf2f4c327e9dd303b8cd78c146618d`, eight commits, all single-parent, in exactly the Bundle's ordered sequence C0a to C6, pushed to `origin/feature/f260-one-world` — `origin` and the branch tip are the same object — and no pull request created. Largest insertion count 318, a single `.agent/**` state write exempt under AGENTS.md DECISION F104 D1; largest CODE commit 22. THE REVIEWER RE-RAN EVERY GATE ITSELF AND REPRODUCED EVERY NUMBER THE HANDBACK REPORTED. TRANSPORT: one digest `ba81fed15e2173bd73d969458cd033910ef7af510ae99d5c40f392a1402e3adb` over `.agent/authored/f260-r13.md` and `.agent/last_block.md`, recomputed by the reviewer. Per §3 item 37 that chain covers the SAVED COPY and its MIRROR and nothing wider; this session did not author the round-13 block, so the delegation digest is not independently recoverable and this verdict claims no comparison against emitted bytes. THE SLICES WERE VERIFIED DISK TO DISK, not against a retype: extracting each slice from the COMMITTED `.agent/authored/f260-r13.md` between its marker lines, `.agent/plan.md` equals the PLAN slice plus one newline exactly, `.agent/live_review.md` equals its pre-image plus `"\n"` plus GATE_R12 plus `"\n\n"` plus FIND815 plus `"\n"` exactly, and `.agent/prose_slips.md` equals its pre-image plus `"\n"` plus SLIP13 plus `"\n"` exactly. All eight marker lines occur once, at file lines 256, 306, 308, 310, 312, 314, 316 and 318, and NONE of the eight reached any of the three target files. THE RECORD: 923356 to 931365 bytes, blank-line units 432 to 434, the last two units GATE_R12 then FIND815 in that order, the post-image beginning with the pre-image byte for byte; `^Gate: ` 22, registrations 300 over 300 DISTINCT ids, `^Done: ` 5 lines over THREE distinct ids, open set 297 BY DISTINCT ID, `R-0815` present. A search of the appended region for unquoted `\bHEAD\b`, after deleting every backtick-quoted span, returns ZERO. THE SLIPS: 113984 to 115506 bytes, units 143 to 144. THE PLAN: 2664 bytes, 49 lines, under the 50-line cap, carrying `## Goal` and `## Next Steps`. THE SWEEP, RE-MEASURED BY THE REVIEWER over 1030 tracked `.py` files enumerated from `git ls-files` in Python: lines where the quoted token `"runs"` BUILDS A PATH now number 76, of which the production side under `packages/` and `apps/` is exactly ONE — the definition at `data_paths.py:73` — and the other 75 are tests; non-path JSON-key occurrences are 60 and unchanged. THAT READING IS ABOUT THE QUOTED TOKEN AND IS NOT A CLAIM THAT PRODUCTION HOLDS NO OTHER SPELLING OF THIS LAYOUT: `run_log.py:115` joins `root / self._job_id` onto a runs base and carries no quoted token at all, so the sweep cannot see it by construction. Round 13's constraint 2 deferred that join deliberately and correctly, and round 14 deletes it. THE AST READING reproduces the handback's table exactly — timeline 0/0 to 1/1, cockpit 0/0 to 1/0, trust_report 0/0 to 1/0, pingpong_job 0/2 to 1/1, patch_apply 0/0 to 0/2, patch_revert 0/0 to 0/1, worker_queue 0/0 to 0/1 — all seven modules non-zero at `8ccd9309` and six of the seven zero at the base. THE SUITES, re-run serially by the reviewer at the branch tip: `tests/orchestration/` exit 0 at 12805 passed and 10 skipped in 733.34 s with zero FAILED and zero ERROR lines, the five-file selection exit 0 at 344 passed, and `integrity check --json` `"passed": true` with `"fail_count": 0` over 5 checks. RUFF over the nine edited `.py` paths: `All checks passed!`. THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY in the reviewer's own disposable worktree at `8ccd9309`, `python3 -B`, `__pycache__` enumerated at 0, module resolution confirmed to that worktree's own `data_paths.py` and the revert target counted at 1 before anything was changed: the unmutated control is exit 0 at 344 passed; with `run_log_dir` appending `"_MUTATED"` to the job id and the mutation confirmed live in the same process, the run is exit 1 at 17 FAILED and 327 passed, the failures falling in `tests/test_timeline.py` 8, `tests/test_patch_apply.py` 6 and `tests/test_data_paths.py` 3 — the handback's split, digit for digit; after restore the control is exit 0 at 344 again, that worktree's `git status --porcelain` and `git diff HEAD --stat` are both empty, and the worktree was removed BY EXACT PATH and pruned, leaving only the eleven pre-existing `remedy/job-*` worktrees. THE ROUND'S CENTRAL CLAIM IS THEREFORE MEASURED AND TRUE: unlike round 12's, this red-proof COULD fail, because the tests still hand-spell `tmp_path / "runs" / <job id>` and remain an independent observer of the accessor. TEN DEVIATIONS WERE DECLARED AND ALL TEN ARE UPHELD. The three that needed a ruling are 1, 3 and 6, and in each the block's governing RULE was rightly followed over the block's own stated list: constraint 6 mis-stated `.agent/prose_slips.md` as ending with no trailing newline when it ends with exactly one — the reviewer confirmed both files end with exactly one newline at the base — constraint 4's import-convention list was wrong for `patch_revert.py`, which already imports `data_paths` at MODULE level, and for `worker_queue.py`, which has no module-level `packages.*` import at all, and G8 said "the eight edited `.py` paths" over a change set holding nine. All three are defects of the reviewer's own text that left nothing wrong on disk, so per operator amendment amend0827-process-diet rule 2 they are dated lines in `.agent/prose_slips.md` and spend no id. Deviation 7's absence is independently confirmed: `tests/test_cockpit.py` and `tests/test_trust_report.py` contribute zero failures because their assertions are substring tests against a LABEL, which no change to the path's leaf can disturb, and both modules measure at zero quoted-token occurrences and one `run_log_dir` call. The reviewer additionally read the second guarded read in `tests/orchestration/test_job_stop_integration.py`, at lines 527-529, and it is NOT a second instance of `R-0815`: that one sits in a polling loop whose `else` branch calls `pytest.fail`, so it cannot pass having asserted nothing.
END GATE_R13

BEGIN DEC_D6
### DECISION F260 D6 (2026-09-06, F260 round 14) — the test-side sweep of the job-keyed run-log paths is declined, and the re-key inherits those sites
Routed to planning under §4 item 7: the reviewer authored this ruling and proceeded under it rather than asking. `.agent/plan.md` at `4f265f91` and the round-13 handback both name "the TEST side of the run-log spelling" as the next step — the hand-built `tmp_path / "runs" / <job id>` paths across the suite — on the stated ground that it is what turns DECISION F260 D1's re-key into a change to one function body. MEASURED at `4f265f91` over 1030 tracked `.py` files enumerated from `git ls-files` in Python: 75 path-building occurrences of the quoted token `"runs"` survive under `tests/`, in 34 files, of which 6 are `tests/test_data_paths.py`'s own accessor contract tests and 65 of the remaining 69 supply a JOB id. THE STATED GROUND HOLDS FOR PRODUCTION AND NOT FOR TESTS. D1 re-keys `<data_root>/runs/` by RUN id, so a test asserting `tmp_path / "runs" / str(job.id)` does not merely spell that path differently after the re-key — it must supply a different id, obtained from somewhere it does not have today. Sweeping those 65 sites onto `run_log_dir(job.id, root)` therefore buys no reduction in the re-key's work and rewrites every one of them twice, against the AGENTS.md ruling that mass renames of existing code are forbidden as their own activity because churn is the enemy. CHOSEN: the sweep is declined; the re-key round touches those sites once, semantically, in the same commits as the writer whose layout they assert. Round 14 instead deletes the one remaining PRODUCTION hand-spelling, `RunLogWriter.__init__`'s join of `root / self._job_id`, which round 13's constraint 2 deferred on the ground that the accessor's signature did not fit — a blocker round 13's own work removed, since all eight call sites that pass a runs base now spell it `runs_dir(<data root>)` and can pass the data root directly. ALTERNATIVES CONSIDERED. Performing the sweep anyway for greppability — rejected: the re-key finds those sites by the same measured token search that found them here, and a symbol that is deleted one round later is not a reverse index. Sweeping only the 10 base-only test sites, which DO survive the re-key — rejected as too small to buy a round, and they are picked up free by any later round that touches their files. NOT CHANGED BY THIS RULING: D1's target layout, the re-key's scope, and the plan's remaining Next Steps. REVERSE by deleting this paragraph and restoring the test-side sweep as the plan's first Next Step, at which point the 69 sites measured above are its change set.
END DEC_D6

BEGIN SLIP14
2026-09-06 · F260 R13 (reviewer) · Constraint 6 of the round-13 block stated that `.agent/prose_slips.md` "at the base ends with NO trailing newline"; measured at `4d13f5a0` it ends with exactly one, as `.agent/live_review.md` does — the second consecutive round whose constraint 6 got this file's terminal byte wrong and in the opposite direction each time, and the worker followed the constraint's own derive-it-from-the-target rule instead, correctly; no id spent (amend0827-process-diet rule 2).
END SLIP14

BEGIN SLIP15
2026-09-06 · F260 R13 (reviewer) · Constraint 4 of the round-13 block listed `worker_queue.py` among the modules importing `packages.*` names at MODULE level and implied `patch_revert.py` imports `data_paths` function-locally; measured at the base both are wrong — `patch_revert.py:33` is a module-level `data_paths` import and `worker_queue.py` has no module-level `packages.*` import at all — and the worker followed the constraint's governing per-file rule over its list, which ruff `I001` then accepted; no id spent (amend0827-process-diet rule 2).
END SLIP15

BEGIN SLIP16
2026-09-06 · F260 R13 (reviewer) · Gate G8 of the round-13 block ordered `ruff check` over "exactly the eight edited `.py` paths of the change set" while that change set holds nine, so the numeral contradicted the list beside it — reviewer-checklist item 16's shape, a hand-counted number stated over a list the reader can count — and the worker linted all nine, which is the wider reading the gate's own words select; no id spent (amend0827-process-diet rule 2).
END SLIP16

BEGIN SLIP17
2026-09-06 · F260 R13 (reviewer) · The round-13 block's Bundle prose and constraint 5(b) named `pingpong_job.py:3215` for the import while SPEC (3) named `:3217` for the expression; both numbers are correct and they are different lines, but the block never said so, and the worker had to spend a declared deviation establishing that the two were not a contradiction; no id spent (amend0827-process-diet rule 2).
END SLIP17
