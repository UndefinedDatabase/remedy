STEP T002/5 — F260 · ROUND 13 — ONE SPELLING FOR THE RUN-LOG STORE

Goal:        Give `<data_root>/runs/<job_id>/` ONE spelling in `data_paths`, as
             rounds 11 and 12 gave the ping-pong run store one, so DECISION F260
             D1's re-key of that directory by RUN id becomes a change to one
             function body instead of a sweep of every caller.

Base:        `4d13f5a02608a40081a7ebacf779124cc6318309` (round 12, reviewed PASS).

Bundle:      C0a  save this block verbatim to `.agent/authored/f260-r13.md`
             C0b  mirror the same bytes into `.agent/last_block.md`
             C1   rewrite `.agent/plan.md` from the PLAN slice
             C2   append GATE_R12 then FIND815 to `.agent/live_review.md`
             C3   append SLIP13 to `.agent/prose_slips.md`
             C4   SPEC (1) the `run_log_dir` accessor + SPEC (2) its tests
             C5   SPEC (3) the nine-site sweep across seven modules
             C6   rewrite `.agent/handoff.md` (the handback)

Change:      EXACTLY these fifteen paths, nothing else:
               .agent/authored/f260-r13.md
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/prose_slips.md
               .agent/handoff.md
               packages/orchestration/data_paths.py
               tests/test_data_paths.py
               packages/orchestration/timeline.py
               packages/orchestration/cockpit.py
               packages/orchestration/trust_report.py
               packages/orchestration/pingpong_job.py
               packages/orchestration/patch_apply.py
               packages/orchestration/patch_revert.py
               packages/orchestration/worker_queue.py

Constraints:
 1. A slice is applied byte for byte. If a slice looks wrong, apply it anyway
    and declare the problem in the handback; never edit a slice.
 2. `packages/orchestration/run_log.py` IS DELIBERATELY NOT IN THE CHANGE SET.
    `RunLogWriter.__init__` (run_log.py:114-115) joins `root / self._job_id`
    where `root` is already the runs BASE, so the accessor below — which takes a
    DATA root — does not fit its signature. That join is the one remaining
    writer-side spelling of this layout and it moves with D1's re-key, not here.
    Do not touch it, and do not change `RunLogWriter`'s signature.
 3. NO BEHAVIOUR CHANGE. Every edited site must build the IDENTICAL path it
    builds today. Measure that, per shape, before editing anything (G4).
 4. Import convention is decided PER FILE, following what that file already
    does, and no second convention is introduced. Measured at the base:
    `timeline.py`, `cockpit.py`, `trust_report.py` and `worker_queue.py` import
    their `packages.*` names at MODULE level, so the new import goes there, in
    isort order — `ruff check` enforces `I001` through this repository's own
    `pyproject.toml` and will reject a wrong position. `patch_apply.py`,
    `patch_revert.py` and `pingpong_job.py` import `data_paths` names
    FUNCTION-LOCALLY at the sites in question, so the new import goes beside the
    existing local import there.
 5. TWO NAME COLLISIONS EXIST AT THE BASE AND BOTH ARE YOURS TO RESOLVE.
    (a) `trust_report.py:373` already binds a LOCAL variable named
    `run_log_dir`. Rebinding that name in a function that also imports the
    accessor makes the name local for the whole function and raises
    `UnboundLocalError`. Rename the local — `run_log_path` is the suggested
    spelling — and leave the printed text unchanged.
    (b) `pingpong_job.py:3215` currently imports `runs_dir` for the single
    expression this round replaces. If that import becomes unused, remove it
    (ruff `F401`), and declare the removal in the handback the way round 12
    declared the `resolve_data_root` removal.
 6. `.agent/live_review.md` at the base ends with exactly ONE newline; append
    accordingly. `.agent/prose_slips.md` at the base ends with NO trailing
    newline. DERIVE EACH RECIPE FROM ITS OWN TARGET'S TERMINAL BYTE, measured
    at the base, and state both measurements in the handback.
 7. Gates run at C5. The handback is C6, so no gate reading may be taken after
    the handback exists (§3 item 31). C6's own insertion count is not reported
    by C6; the reviewer measures it at the next gate.
 8. Every destructive check runs in a disposable `git worktree` under
    `.remedy-wt/`, removed by EXACT PATH before the handback; the primary
    checkout satisfies `git status --porcelain` == empty at the handback.
 9. `cmp` is denied in this sandbox. Use `filecmp.cmp(shallow=False)` plus
    sha256. `remedy` is invoked as `python3 -m apps.cli.grouped`, `ruff` as
    `python3 -m ruff`. Purge `__pycache__` and run `python3 -B` for every
    mutation reading.

SPEC (1) — THE ACCESSOR

In `packages/orchestration/data_paths.py`, DIRECTLY BELOW the existing
`runs_dir` function (base line 71-73) and above `projects_dir`, add ONE new
public function plus the WHY comment above it, separated from its neighbours by
the file's existing two-blank-line convention.

The comment states, in this order: that this is the LIVE run-log store keyed by
JOB id as it is TODAY, `<data_root>/runs/<job_id>/`; that DECISION F260 D1
re-keys the directory by RUN id; and that giving it one spelling here turns that
re-key into a change to this function body instead of a sweep of every caller.
Write it in the voice of the `pingpong_runs_dir` comment block already in this
file (base lines 202-211) — that block is the model to follow, not to copy.

The function:

  - named `run_log_dir`
  - signature `(job_id: UUID | str, root: Path | None = None) -> Path`
    (`UUID` is already imported at data_paths.py:42; add no import)
  - one-line docstring naming what it returns TODAY
  - body exactly: `return runs_dir(root) / str(job_id)`

That body must be a single line and must occur EXACTLY ONCE in the file — G7
reverts by those bytes and constraint 25 of the reviewer's checklist requires
the revert target to be unique inside its named file. Verify the count is 1
before you commit C4 and report it.

Do NOT change `runs_dir`, `run_dir`, `jobs_dir` or any other existing function.
`run_dir(run_id, root)` is the TARGET spelling D1 introduces and is keyed by RUN
id; `run_log_dir` is the LIVE spelling keyed by JOB id. THEY ARE NOT THE SAME
FUNCTION AND MUST NOT BE MERGED THIS ROUND — that merge is D1's own work, and
performing it here would re-create the collision DECISION F260 D0 recorded.

SPEC (2) — TESTS FOR THE ACCESSOR

In `tests/test_data_paths.py`, add tests for `run_log_dir` beside the existing
`runs_dir` / `run_dir` tests (base lines 79, 102, 120, 375 show the house
style — follow it, including how the module imports the names under test).

Three readings, each its own test:
  (a) with an EXPLICIT root: `run_log_dir("j1", tmp_path)` equals
      `tmp_path / "runs" / "j1"`.
  (b) with NO root, under a monkeypatched `REMEDY_DATA_DIR`: the result equals
      `runs_dir() / "j1"`, so the accessor follows the process data root.
  (c) with a `UUID` job id: the result equals the same path built from
      `str(that_uuid)`, which is what pins the `str()` coercion in the body.

Each test asserts a PATH EQUALITY, never a string containment.

SPEC (3) — THE NINE-SITE SWEEP

Nine hand-spelled sites in seven modules move onto the two accessors. The line
numbers are measured at the base `4d13f5a0`; re-grep each before editing, and
report the count you re-measured (§3 item 9).

FOUR JOB-KEYED SITES move onto `run_log_dir`:
  timeline.py:75      `runs_dir = data_dir / "runs" / str(job_id)`
                      → the accessor, keeping the local name `runs_dir` if that
                        does not shadow an import you added; rename it if it does
  cockpit.py:380      `str(data_dir / "runs" / str(job.id))`
  trust_report.py:373 `run_log_dir = data_dir / "runs" / str(job.id)`
                      → see constraint 5(a): the LOCAL is renamed
  pingpong_job.py:3217 `job_runs = runs_dir() / job_id`
                      → `run_log_dir(job_id)`; see constraint 5(b)

FIVE BASE-ONLY SITES move onto `runs_dir`:
  timeline.py:64        `runs_root=Path(data_dir) / "runs"`
  patch_apply.py:526    `runs_root = (data_dir / "runs") if data_dir is not None else None`
  patch_apply.py:563    the SAME expression a second time — both move
  patch_revert.py:245   `runs_root = actual_data_dir / "runs"`
  worker_queue.py:488   `runs_root=root / "runs"`

`safe_points.py:671` and `pingpong_job.py:3178` already call `runs_dir()` and
are correct; they are NOT in the change set. The quoted token `"runs"` also
occurs across this repository as an ordinary JSON dict KEY (`"runs": [...]` in
verification payloads) — those are not paths and are NOT swept. Only the nine
sites listed above move.

DONE WHEN — EIGHT GATES

Every gate below is EXECUTED and its REAL exit code recorded, one line per gate
in the handback. "Green" as a word is a finding.

G1 TRANSPORT. `sha256sum .agent/authored/f260-r13.md .agent/last_block.md`;
   both equal the digest the delegation names. One comparison, not a chain.

G2 THE RECORD. After C2, prove `.agent/live_review.md` equals its pre-image plus
   exactly the two appended paragraphs, by TWO independent readers:
   (a) exact-image byte equality against the recipe you derived in constraint 6;
   (b) a STRUCTURAL reader that splits the whole file on `"\n\n"`, counts the
       units itself, and compares the LAST TWO units in order against GATE_R12
       and FIND815. N is counted by your script, never asserted by this block.
   (c) a negative control that flips one byte inside the FIRST appended
       paragraph (GATE_R12) and confirms BOTH readers reject it, and both accept
       after restore. Run it in memory, not by writing bad bytes to the file.
   (d) report `^Gate: ` count, registrations, `^Done: ` lines, and the open set
       BY DISTINCT ID after C2.

G3 THE PROSE FILES. `.agent/plan.md` disk bytes equal the PLAN slice plus one
   trailing newline; report its line count, which must be under 50.
   `.agent/prose_slips.md` equals its pre-image plus the recipe of constraint 6;
   report bytes before and after and the blank-line unit count before and after.

G4 THE ACCESSOR AND NO BEHAVIOUR CHANGE. At C4: `python3 -m pytest
   tests/test_data_paths.py -q -p no:randomly` exits 0 and its count is REPORTED.
   Additionally, BEFORE editing any consumer, run a scratch probe under
   `.remedy-wt/` that prints BOTH the hand-spelled and the accessor-built path
   for all THREE shapes this sweep uses — `root/"runs"`, `root/"runs"/str(jid)`,
   and `resolve_data_root()/"runs"/str(jid)` — and confirms each pair compares
   equal. Report the printed pairs, not a summary of them.

G5 THE SWEEP IS COMPLETE AND NON-VACUOUS. At C5, three readings:
   (a) enumerate `git ls-files` in PYTHON (a `tests/**/*.py` shell glob silently
       misses `tests/test_data_paths.py` — round 12 deviation 7), filter to `.py`
       under `packages/`, `apps/`, `tests/`, and report every line containing the
       quoted token `"runs"` that BUILDS A PATH, at the base and at C5, with the
       per-file counts. The nine swept sites must be absent at C5; JSON-key
       occurrences are expected to be unchanged and are reported as such.
   (b) per swept module, an AST reading counting calls to `run_log_dir` /
       `runs_dir`: EVERY module named in SPEC (3) is NON-ZERO at C5, and each
       file's base value is reported beside it.
   (c) `git diff --numstat <C5>^ <C5>` — exactly one row per module named in
       SPEC (3) and no row outside that list. Report the rows you measured
       rather than a count of them.

G6 THE SUITES, SERIALLY, each captured to a file under `.remedy-wt/` and read
   from the capture:
   (1) `python3 -m pytest tests/orchestration/ -q -p no:randomly`
   (2) `python3 -m pytest tests/cli/ -q -p no:randomly`
   (3) `python3 -m pytest tests/test_data_paths.py tests/test_timeline.py
       tests/test_cockpit.py tests/test_trust_report.py tests/test_patch_apply.py
       -q -p no:randomly`
   (4) `python3 -m apps.cli.grouped integrity check --json`
   The canary is inside (2); verify its presence with
   `python3 -m pytest tests/cli/test_golden_path.py --collect-only` and report
   the collected count. Report each suite's real numbers.

G7 MUTATION RED-PROOF — AND THIS ONE CAN GO RED, WHICH ROUND 12's COULD NOT.
   In a disposable worktree at C5, `python3 -B`, `__pycache__` enumerated as 0:
   (i)   CONTROL FIRST, unmutated, over the G6(3) selection: record exit code
         and count. Confirm module resolution by printing
         `data_paths.__file__` and the live BODY of `run_log_dir` from that
         worktree before trusting any colour.
   (ii)  Verify the bytes `    return runs_dir(root) / str(job_id)` occur
         EXACTLY ONCE in that worktree's `packages/orchestration/data_paths.py`,
         then replace that one line so `run_log_dir` appends `"_MUTATED"` to the
         job id. Re-print the live BODY to prove the mutation is loaded. Re-run
         the SAME selection. IT MUST GO RED. The tests still hand-spell
         `tmp_path / "runs" / <job id>`, so they are an INDEPENDENT OBSERVER of
         the accessor — which is exactly the property round 12's sweep had
         already destroyed for `pingpong_runs_dir`, and why that gate could not
         fail. Report the failure count and the failing files.
   (iii) Restore the original line, re-run the control, and show
         `git status --porcelain` and `git diff HEAD --stat` EMPTY in that
         worktree. Remove the worktree BY EXACT PATH and `git worktree prune`.
   If (ii) does NOT go red, STOP, do not reshape anything to make it red, and
   report the measurement — that would mean the sweep changed a path, which
   constraint 3 forbids.

G8 LINT AND CLEAN TREE. `python3 -m ruff check` over exactly the eight edited
   `.py` paths of the change set: `All checks passed!`. Then
   `git status --porcelain` and `git ls-files .remedy-wt`, both EMPTY.
   NOTE, measured at the base so you do not chase it: `ruff check` over ALL of
   `packages/orchestration/` reports two PRE-EXISTING errors, `UP035` at
   `dag_schedule.py:36` and `F821` at `gauntlet_injection.py:286`. Neither file
   is in this change set and neither is yours to fix. Scope the gate to the
   edited paths, as written above.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry the SESSION
             NUMBER (this is SESSION 4 of F260, round 13), the changed-files
             table with `+/-` from `git diff --numstat` and never re-derived by
             eye, one line per gate with its real exit code, the open-findings
             count BY DISTINCT ID, every deviation, and the item-status table.
             Push after the handback commit.

BEGIN PLAN
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 12 are reviewed and 2 to 12 PASSED. T001 is
CLOSED. T002 is open: the job record has MOVED, R-0814 is resolved, both
resolvers return `str`, and the ping-pong run store has one spelling on both the
production and the test side.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store, now `<data_root>/jobs/<16hex>/job.json`, become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

ONE SPELLING FOR THE RUN-LOG STORE. `<data_root>/runs/<job_id>/` is spelled by
hand at nine sites in seven modules. A new `data_paths.run_log_dir` names the
live job-keyed directory, five base-only sites move onto the existing
`runs_dir`, and the four job-keyed sites move onto the new accessor. This is the
run-log twin of what rounds 11 and 12 did for the ping-pong run store, and it is
what turns DECISION F260 D1's re-key into a change to one function body.

## Next Steps

- The TEST side of the run-log spelling: the hand-built `tmp_path / "runs" /
  <job id>` paths across the suite, which this round deliberately leaves standing
  because they are what makes its own red-proof able to fail.
- THE RE-KEY ITSELF: `run_log_dir` and `pingpong_run_dir` collapse onto
  `run_dir`, keyed by RUN id, and `<data_root>/runs/` stops being keyed by job
  id — DECISION F260 D0 measured that collision and D1 rules the target.
- The unified record's own fields, and the Mission extension (order, contract,
  mission plan, job refs), which is the rest of T002.
- Then T003 consumer by consumer; T004 the classic runner, the classic store and
  the resolver collapse together (DECISION F260 D5); T005 the reachability test
  and the cluster deletion.

## Risks

- `<data_root>/runs/` is keyed by JOB id today and D1 keys it by RUN id. Every
  reader of the old shape moves in the same commit as its writer.
- `RunLogWriter.__init__` still joins the job id onto a runs BASE it is handed,
  so the layout has one more writer-side spelling than `data_paths` shows.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
END PLAN

BEGIN GATE_R12
Gate: R12 — the F260 R12 entry. VERDICT PASS. Range `2ad2d1534ff53a202dc6965909391849b2dd2ca0`..`4d13f5a02608a40081a7ebacf779124cc6318309`, seven commits, all single-parent, in the Bundle's ordered sequence, pushed, no pull request. THE ROUND MOVED FOURTEEN HAND-SPELLED `"pingpong_runs"` PATH COMPONENTS IN SEVEN TEST FILES ONTO `data_paths.pingpong_run_dir` / `pingpong_runs_dir`, and the reviewer re-measured every gate independently rather than reading the handback's numbers. TRANSPORT: one digest `203cd3fc75b5c639947d1ace5a7a93197a8fe4ca18b60ab9296051e242d6410a` over `.agent/authored/f260-r12.md` and `.agent/last_block.md`, recomputed by the reviewer and equal to the digest the delegation carried. Per §3 item 37 that chain covers the SAVED COPY and its MIRROR and nothing wider: under self-drive the worker types the block into `.agent/authored/`, so no gate this workflow can run compares the EMITTED bytes, and this verdict claims no such comparison. THE SWEEP, RE-MEASURED: enumerating `git ls-files` in Python over 1030 tracked `.py` files under `packages/`, `apps/` and `tests/`, the quoted token `"pingpong_runs"` occurs at EXACTLY THREE sites at the round's head — `packages/orchestration/data_paths.py:216`, `tests/test_data_paths.py:406` and `tests/test_data_paths.py:407` — against SEVENTEEN sites in NINE files at the base, both readings taken by the reviewer from `git ls-tree` and `git show` rather than from the working tree. THE RECORD: `.agent/live_review.md` grew 918017 → 923356 bytes, its blank-line units 431 → 432, and the appended unit is the R11 entry; the open set stands at 296 BY DISTINCT ID, from 299 registrations over 299 distinct ids minus 3 distinct ids carrying a `Done:` line, recomputed mechanically from the record and not carried forward. `.agent/prose_slips.md` grew 108734 → 113984 with its blank-line units rising 139 → 143, a rise of exactly four, and the post-image begins with the pre-image byte for byte. `.agent/plan.md` is 2611 bytes and 49 lines, under the 50-line cap, and carries both `## Goal` and `## Next Steps`, so §4 item 11's contract readers stay green. LINT over exactly the seven swept files: `All checks passed!`. `tests/test_data_paths.py`: 48 passed. `integrity check --json`: passed, zero failures. SEVEN DEVIATIONS WERE DECLARED AND ALL SEVEN ARE ACCEPTED. THE ONE THAT NEEDED A VERDICT IS THE FIRST, AND THE WORKER WAS RIGHT: gate G7(ii) of the round-12 block ordered the swept test files to go RED under a mutation of `pingpong_runs_dir` and inferred that a file which stayed green "is still hand-spelling its path somewhere the token reading missed". THAT INFERENCE IS FALSE AND THE GATE COULD NOT FAIL. The reviewer reproduced the whole measurement in a disposable worktree at `326fe67abb62dbaaee7a3197dbab104d6db79f08`, `python3 -B`, `__pycache__` enumerated at 0, module resolution confirmed to the worktree's own `data_paths.py`: the unmutated control is exit 0 at 544 passed; with `pingpong_runs_dir` returning `"pingpong_runs_MUTATED"` and the mutation confirmed live in the same process, the run is STILL exit 0 at 544 passed and zero failed. The cause is the opposite of the one the gate named — round 11 had already moved PRODUCTION onto the same accessor, so mutating that one function moves the writer and the reader in lockstep and no observer inside the system can see it. THE WORKER'S P3 IS THE CORRECT PROOF AND THE REVIEWER REPRODUCED IT EXACTLY: the identical mutation, run against the same seven files checked out at their PRE-sweep bytes, is exit 1 at 30 failed and 514 passed. A one-spelling sweep is therefore proved by a PAIR — red before, green after — and never by demanding redness from the swept side. That is a defect of the reviewer's own gate text and not of anything on disk, so per operator amendment amend0827-process-diet rule 2 it is recorded as one dated line in `.agent/prose_slips.md` and spends no id, exactly as this feature's round 11 routed its own vacuous gate clause. THE REMAINING SIX DEVIATIONS ARE ACKNOWLEDGED AS CORRECT: `cmp` is denied in this sandbox and `filecmp.cmp(shallow=False)` plus sha256 is a full byte comparison, not a weaker one; the G2(c) negative control was run in memory rather than by writing corrupted bytes to the record, which is what self-drive guardrail G5 requires and is the stronger choice; `resolve_data_root` was dropped from an import line in `tests/orchestration/test_job_stop_integration.py` because the sweep left it unused and ruff `F401` would otherwise have gone red, which is inside the change set and behaviour-neutral; path equality was MEASURED for all five shapes before any file was edited rather than reasoned about; and the pathspec gotcha the worker recorded is real and is promoted into this round's own G5 — `tests/**/*.py` does not match `tests/test_data_paths.py`, so the reviewer's re-measurement above enumerates `git ls-files` in Python for exactly that reason. THE SECOND DEVIATION CARRIED A CANDIDATE AND IT IS REGISTERED THIS ROUND AS `R-0815`, immediately below: the guarded read at `tests/orchestration/test_job_stop_integration.py:248-251` skips its assertion instead of failing when the path is wrong. It predates round 12 and survives it unchanged, and the worker was right not to widen its change set to reach it.
END GATE_R12

BEGIN FIND815
- R-0815 — Low, A GUARDED READ IN `test_job_stop_integration.py` SILENTLY SKIPS ITS ASSERTION INSTEAD OF FAILING WHEN THE RUN FILE IS ABSENT. Offered as a CANDIDATE by the worker of F260 R12 in that round's deviation 2, and confirmed by the reviewer by reading the site at `4d13f5a02608a40081a7ebacf779124cc6318309`. In `tests/orchestration/test_job_stop_integration.py` the body of `TestStopDuringAProviderCall` reads the run record through `run = json.loads((pingpong_runs_dir() / f"{...run_id}.json").read_text()) if (pingpong_runs_dir() / f"{...run_id}.json").is_file() else None`, and the two assertions that follow sit under `if run is not None:`. When the path is wrong — which is precisely the state a regression in the run store would produce — `is_file()` returns False, `run` becomes None, and the test PASSES having asserted nothing about the run at all. PRODUCT EFFECT, which is why this spends an id rather than a `.agent/prose_slips.md` line under operator amendment amend0827-process-diet rule 2: the wrong state is on disk under `tests/`, and it is a gate over production code that is demonstrably blind — the reviewer measured that blindness directly while re-running round 12's red-proof, where mutating `pingpong_runs_dir` to return a different leaf left this file at ZERO failures while the file's own swept sites were the mutation's direct subject. LOW rather than Medium because the surrounding test still exercises the stop path and its other assertions — `stopped.status == JOB_STOPPED` and `stopped.tasks[0].status == TASK_PENDING` — do bind, so the defect costs coverage of the run record only, not of the behaviour the test is named for. ROOT CAUSE, stated so the class is visible: a conditional written to tolerate an OPTIONAL artefact is indistinguishable, once written, from one written to tolerate a BROKEN one, and nothing in the suite records which was meant — the same shape as reviewer-checklist item 27, arriving in a test instead of in a gate. SEARCHED BEFORE MINTING per §3 item 30: the open set was grepped for `is_file() else None`, for `silently skipped`, and for the file's own basename, and no open finding describes this defect; the nearest neighbours are the two-store findings this feature exists to close and neither names a guarded read. FIX: decide whether that run record is guaranteed present at that point, and if it is, drop the guard so a missing file FAILS; if it genuinely is not, assert the condition that IS guaranteed instead of wrapping the whole reading. Resolved when the assertions in that block are reachable unconditionally, or when the test asserts a property that holds whether or not the file exists.
END FIND815

BEGIN SLIP13
2026-09-06 · F260 R12 (reviewer) · Gate G7(ii) of the round-12 block ordered the seven swept test files to go RED under a mutation of `pingpong_runs_dir`, and told the worker that any file staying green "is still hand-spelling its path somewhere the token reading missed". Both halves are wrong, and the reviewer confirmed it by reproducing the entire measurement: the mutation leaves the swept selection at 544 passed and ZERO failed, while the same mutation against the same seven files at their pre-sweep bytes is 30 failed and 514 passed. THE LESSON is that a one-spelling sweep DESTROYS the very observer a mutation red-proof needs — once the writer and every reader route through one function, renaming that function's leaf moves them in lockstep and no test inside the system can see it — so the correct post-condition for such a round is a PAIR, red against the pre-sweep bytes and green against the swept ones, which is exactly what the worker's own P3 supplied. Checklist item 5 already says to order the PROBE instead of the colour when reachability is not obvious; the gap this instance exposes is that reachability had been DELETED by the round's own change, which is a case item 5's wording does not prompt anyone to look for. Reviewer-authored gate whose stated inference was false and whose colour was unreachable; the sweep itself is correct and independently re-measured, nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
END SLIP13
