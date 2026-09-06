── STEP T001 (part 3, REPAIR) — F272 ─────────────────────────
Goal:        Return the branch tip to green. Round 2's production change is
             CORRECT and stays; what was wrong is the reviewer's claim about how
             many tests observe it. Book that as finding R-0818, sweep the
             job-keyed run-log path out of every test that hand-spells it, and
             correct DECISION F272 D1's premise with DECISION F272 D2.
Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 register R-0818 ·
             C3 the test sweep · C4 DECISION F272 D2 · C5 the handback
(the rule line above is 61 copies of U+2500; the rule line below is the same 61)
─────────────────────────────────────────────────────────────

## Where this round starts

You are on `feature/f272-one-world-completion` at `b189a03f`, round 2's handback
and the branch tip. ROUND 2 FAILED ITS GATE and the tip is RED. The reviewer
re-ran the measurement independently at that tip: `python3 -m pytest -n auto -q
-p no:randomly` gives **207 failed, 19528 passed, 23 skipped**, and the canary
`tests/cli/test_golden_path.py` is exit 1 at `1 failed, 41 passed` where round 1
had 42. Nothing is reverted: rounds 2's C4 moved the run log to
`<data_root>/job_logs/<job_id>` and the ping-pong run store to
`<data_root>/runs/<run_id>`, both verified correct by the reviewer at gates G5
and G6, and all 74 reader and 35 writer call sites in `packages/` and `apps/`
still resolve through `data_paths.run_log_dir` exactly as DECISION F272 D1 said
they would. The defect is in the reviewer's own text, and this round repairs it.

Stay on that branch. Nothing is merged, no pull request is created.

## Change set — nothing outside this list

    .agent/authored/f272-r3.md                        (new, C0a)
    .agent/last_block.md                              (C0b)
    .agent/plan.md                                    (C1)
    .agent/live_review.md                             (C2)
    tests/cli/runtime_helpers.py                      (C3)
    tests/cli/test_golden_path.py                     (C3)
    tests/cli/test_job_rerun_manifest.py              (C3)
    tests/cli/test_teach_cmd.py                       (C3)
    tests/orchestration/test_budget_tick.py           (C3)
    tests/orchestration/test_event_persistence.py     (C3)
    tests/orchestration/test_event_replay.py          (C3)
    tests/orchestration/test_job_stop_integration.py  (C3)
    tests/orchestration/test_structured_planner_cli.py (C3)
    tests/orchestration/test_worker_execution.py      (C3)
    tests/orchestration/test_worktree_lifecycle.py    (C3)
    tests/orchestration/test_worktree_resume_cli.py   (C3)
    tests/test_agent_loop.py                          (C3)
    tests/test_agent_loop_execution.py                (C3)
    tests/test_brain_detail.py                        (C3)
    tests/test_brain_smoke.py                         (C3)
    tests/test_brain_viewer.py                        (C3)
    tests/test_context_coverage.py                    (C3)
    tests/test_patch_apply.py                         (C3)
    tests/test_patch_intent_approval.py               (C3)
    tests/test_project_brain.py                       (C3)
    tests/test_project_constitution.py                (C3)
    tests/test_project_context_coverage.py            (C3)
    tests/test_run_log_cli.py                         (C3)
    docs/roadmap/features/T2_F272.md                  (C4)
    .agent/handoff.md                                 (C5)

That is 24 files under C3, of which `tests/cli/runtime_helpers.py` is a shared
helper and the other 23 are test files. No file under `packages/` or `apps/` is
touched this round, and `tests/test_data_paths.py`, `tests/test_run_log.py` and
`tests/test_timeline.py` — swept in round 2 and green — are NOT touched again.

## The slices in this block

Each authored text sits between `<<<BEGIN name>>>` and `<<<END name>>>` on their
own lines. Extract by exact-position marker matching, asserting exactly one BEGIN
and one END per name. The whole-file text is PLANF272R3; the appended texts are
FIND0818 and DECISIOND2.

## C0a and C0b — save and mirror

This block is at `.remedy-wt/f272-r3-block.md`; the delegating prompt states its
sha256 as BLOCK_SHA. Verify the source against BLOCK_SHA BEFORE anything else,
then `shutil.copyfile` it to `.agent/authored/f272-r3.md` and commit it alone;
then `shutil.copyfile` the same bytes to `.agent/last_block.md` and commit that
alone.

## C1 — the plan

Write `.agent/plan.md` from the PLANF272R3 slice, byte for byte plus exactly one
trailing newline, and commit it alone. FIRST substantive commit (§3 item 23).

## C2 — register the finding, BEFORE any repair

APPEND the FIND0818 slice to `.agent/live_review.md` and commit it alone, before
a single test file is edited. §4 item 4: findings persist FIRST, in their own
commit, so nothing is lost if the session dies mid-repair. The recipe: read the
file's own terminal byte and confirm it is exactly one newline; then write, in
ONE write, the pre-image plus one newline plus the slice plus one newline.

This MINTS one id. R-0818 is the next free id — the reviewer recomputed the open
set from the record at `b189a03f` and found 301 distinct registrations against 3
distinct resolutions, so 298 open and R-0817 the maximum in use. After C2 the
open set is 299.

Do NOT write a `Done:` paragraph for it. R-0818 is repaired by C3 of this round,
but only reviewer-authored text sets `Done:` (§4 item 4). If you wish to record
that the fix landed, the line is `Landed: R-0818 — <one line: what changed, which
commit>` and nothing else — and it is NOT written this round, because the
reviewer will author the resolution at the next gate.

## C3 — the sweep

ONE commit. In each of the 24 files listed above, the job-keyed run-log directory
is spelled BY HAND as `<something> / "runs" / <job id>`. Round 2 moved that
directory to `<data_root>/job_logs/<job_id>`, so every one of those spellings now
names a directory nothing writes. Change the `"runs"` component to `"job_logs"`
at each such site, and nowhere else.

READ EACH SITE BEFORE CHANGING IT. This is not a blind substitution and a blind
one is wrong: `"runs"` is ALSO the correct spelling of the RUN store, which round
2 deliberately moved INTO `<data_root>/runs/<run_id>`. The test is what the path
is keyed BY. A path whose next component is a JOB id — `job.id`, `job_id`,
`job.job_id`, `jid`, `str(job.id)` — is the run log and changes. A path whose
next component is a RUN id, or which has no id component at all, does NOT change.

THE COMPLETE ENUMERATION, measured by the reviewer at `b189a03f` by listing every
`"runs" /` path component in all of `tests/`: 62 occurrences, of which 56 are
job-keyed and change, and SIX are not and must survive untouched —
`tests/orchestration/test_context_compiler.py:1451` (`"runs" /
CONTEXT_SIZE_FILENAME`, a file directly under the run store),
`tests/orchestration/test_failure_postmortem.py:412` (`"runs" / "r1"`, a RUN id),
`tests/orchestration/test_failure_wiring.py:903` and
`tests/orchestration/test_gauntlet_runner.py:490` (both `"runs" /
"postmortem.json"`), and `tests/test_data_paths.py` lines 396 and 430, which
assert `run_dir` and `pingpong_run_dir` against a RUN id and are the two
assertions that pin the new layout. Those figures are the reviewer's own count;
report YOURS rather than reproducing them.

Two of the 24 files whose tests fail — `tests/cli/test_propose_cli_runtime.py`
and `tests/cli/test_worker_cli_runtime.py` — hand-spell nothing themselves and
are absent from the change set: they reach the path through
`tests/cli/runtime_helpers.py`, which IS in the change set, and they must go
green without being edited. If either still fails after the sweep, report it
rather than editing it. Conversely
`tests/test_project_context_coverage.py` hand-spells the job-keyed path at three
lines and NONE of its tests currently fail; it is swept for correctness, not to
clear a red, and its own suite must still be green afterwards.

Where a local helper builds the path once for a whole module — `test_run_log_cli.py`
line 46 and `test_event_replay.py` line 10 are of that shape — fixing the helper
fixes every test beneath it, which is why 56 failures sit behind one line. Where
a docstring or comment beside a swept line describes the old layout as current,
correct it in the same commit.

## C4 — DECISION F272 D2

APPEND the DECISIOND2 slice to the END of
`docs/roadmap/features/T2_F272.md`, after its last existing line, by the same
read-the-terminal-byte recipe as C2, and commit it alone. DECISION F272 D1 IS NOT
EDITED: its ruling is correct and only its premise sentence is false, and this
repository corrects a landed decision by appending a correction rather than
rewriting it — the precedent is `DECISION F085 D6 — correction to the ruled
figure` in `.agent/decisions.md`.

## C5 — the handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md and commit it
last. Mandated sections, the item-status table covering C0a to C5 with every item
exactly once, one line per gate with REAL exit codes, and the SESSION NUMBER
line: **SESSION 1 of feature F272**, round 3. Do NOT state C5's own insertion
count (§3 items 14 and 31).

## Constraints

1. Every slice is applied BYTE FOR BYTE. If you believe one is wrong, apply it
   anyway and record the objection in the handback's deviations.
2. The change set is exhaustive. NOTHING under `packages/` or `apps/` is touched.
   Round 2's C4 is NOT reverted, in whole or in part.
3. Both appends this round are APPENDS, not FROM/TO pairs, so no containment
   reading and no FROM-zero count applies; the obligation is the ordered-equality
   reading of §4 item 9.
4. EXACTLY ONE id is minted: R-0818. None is resolved and none renumbered. The
   open set is 298 before C2 and 299 after it.
5. COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, each its own commit, each
   single-parent, nothing after C5. C2 precedes C3: the finding is on disk before
   the repair.
6. Every gate runs at a commit STRICTLY EARLIER than C5 (§3 item 31).
7. This session's shell guard refuses `python3 <script>` followed by
   `echo "EXIT=$?"`, refuses shell loops and refuses `$(...)`. Read exit codes
   from `subprocess.run(...).returncode` inside Python files under `.remedy-wt/`.
   Bare `ruff` is DENIED; the spelling that runs is `python3 -m ruff check`.
8. NOTHING destructive runs this round and no `git worktree` is needed: the round
   REMOVES a red rather than proving one, so its evidence is the before-and-after
   count on a known failing set, which G5 measures.
9. NOTHING IS MERGED and no pull request is created.
10. Read `.agent/STOP` with `os.path.exists` before C0a, before C3 and before C5,
    and report all three readings.
11. THIS BLOCK'S OWN SIZE, measured by the reviewer on these final bytes: PROSE
    276 lines against the 400-line cap of DECISION F105 D5, and TOTAL 355 lines
    against the 490-line budget of DECISION F085 D6. Re-measure BOTH from the
    committed `.agent/authored/f272-r3.md` and report both.

## Done when — the gates

**G1 TRANSPORT.** `.remedy-wt/f272-r3-block.md`, the committed
`.agent/authored/f272-r3.md` at C0a and `.agent/last_block.md` at C0b are
byte-identical: report the one sha256, the one byte length, and
`filecmp.cmp(shallow=False)` for source-vs-saved and source-vs-mirror. The digest
must equal BLOCK_SHA.

**G2 THE RECORD**, at C2. (a) BYTE: post equals pre plus one newline plus
FIND0818 plus one newline, EXACTLY; pre is a byte-exact PREFIX; report bytes
before and after and the delta; pre ended in exactly one newline, ASSERTED FROM
ITS OWN TERMINAL BYTE BEFORE WRITING, and post does too. (b) STRUCTURAL, computed
independently of (a): split the WHOLE image on `\n{2,}`, drop units empty after
stripping, strip each survivor of leading and trailing newlines; report the unit
count before and after and that the last N units equal the slice's paragraphs IN
ORDER, where N is a number YOUR SCRIPT COUNTS from the slice. (c) NEGATIVE
CONTROL, in memory on a `bytes` object and NEVER on disk: flip one byte inside
the FIRST appended paragraph, having ASSERTED by offset that it lies there;
report that reader (a) REJECTS and reader (b) REJECTS, then restore and report
both ACCEPT and the restored image equals the disk image. (d) COUNTS before →
after: distinct `^- R-\d{4} — ` ids 301 → 302; distinct `^Done: R-\d{4} — ` ids
3 → 3; open set BY DISTINCT ID 298 → 299, UP BY EXACTLY ONE, which is the
arithmetic of minting one id and resolving none; `^- R-0818 — ` 0 → 1; `^Gate: `
24 → 24; and ZERO lines matching `^Done:` or `^Landed:` in the appended region.

**G3 THE PLAN**, at C1. `.agent/plan.md` equals PLANF272R3 plus exactly one
trailing newline — report byte length and equality; line count under the
AGENTS.md cap of 50; carries `## Goal` and `## Next Steps`.

**G4 THE SWEEP IS COMPLETE AND SCOPED**, at C3. Report, as YOUR OWN measurement:
(i) the lines and files changed, from `git diff --numstat <C2> <C3>`, and that
`git diff --name-only` over C3 lists exactly the 24 paths of the change set and
nothing else. (ii) THE SURVIVOR INVENTORY, which is this gate's real content and
is an enumeration rather than a regex, because a regex over variable names misses
the sites spelled `jid` and would pass while the sweep was incomplete: list EVERY
line in ALL of `tests/` still holding a `"runs" /` path component after C3 — file,
line number and the line itself — and report the total. That list must be exactly
the SIX non-job-keyed sites named under C3 above, and its total must be 6. Any
seventh survivor is an unswept job-keyed site and the sweep is not done. (iii)
`git diff <C2> <C3> -- tests/test_data_paths.py tests/test_run_log.py
tests/test_timeline.py` is EMPTY, because round 2 already swept those three and
this round must not touch them again.

**G5 THE RED IS GONE**, at C3, and this is the round's whole point. In ONE pytest
invocation with `-p no:randomly`, run the 23 TEST files of the change set — every
C3 path except `tests/cli/runtime_helpers.py`, which is a helper and holds no
tests — plus `tests/cli/test_propose_cli_runtime.py` and
`tests/cli/test_worker_cli_runtime.py`, which are not edited and must go green
anyway: 25 files. Report the exit code, which must be 0, and the passed count. Then the
canary `python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly`, exit
0 at **42** passed — 41 is the red reading and 42 is round 1's. Then
`python3 -m apps.cli.grouped integrity check --json`, exit 0 with
`"passed": true` and `"fail_count": 0`. The reviewer runs the FULL suite itself
at the gate; do not run it here.

**G6 THE FEATURE FILE**, at C4. The pre-commit blob is a byte-exact PREFIX of the
post-commit file; the slice plus its leading and trailing newline is an exact
SUFFIX; and the lines C4's diff ADDS are exactly the slice's lines IN ORDER (§4
item 9). Report bytes before and after. Then, because the change set holds a
`docs/roadmap/**` path: `python3 -m pytest tests/docs/ -q -p no:randomly` exit 0
at 303 passed, and `python3 -m pytest tests/orchestration/test_roadmap_index.py
-q -p no:randomly` exit 0 at 30 passed.

**G7 LINT**, at C3. `python3 -m ruff check` over the 24 changed files —
pass them as arguments in one invocation — exits 0.

**G8 THE TREE.** `git status --porcelain` EMPTY and `git ls-files .remedy-wt`
empty, both read after C4 and before C5 is staged. Per commit and for C0a through
C4 ONLY, the `git diff --numstat <parent> <commit>` INSERTION count — the column
AGENTS.md DECISION F104 D1 caps at 500 — and that each commit is single-parent.
The count of lines beginning with the BEGIN or END marker prefix in
`.agent/plan.md`, `.agent/live_review.md`, `docs/roadmap/features/T2_F272.md` and
each of the 24 swept files; each must be 0.

<<<BEGIN PLANF272R3>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Round 1 PASSED. ROUND 2 FAILED its
gate: its production change is correct, but the reviewer's DECISION F272 D1
claimed only three test files observed it, and 24 do, so the tip went red at 207
tests. Round 3 is the repair.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

Round 3 returns the tip to green WITHOUT reverting round 2. It registers finding
R-0818 before touching anything, sweeps the job-keyed run-log path out of the 24
files that hand-spell it, and appends DECISION F272 D2 correcting D1's
premise — the sentence that called three files the only observers — while
leaving D1's ruling, which the gates proved right about production code, intact.

## Next Steps

1. The name collapse DECISION F272 D1 places next: `pingpong_runs_dir` and
   `pingpong_run_dir` are DELETED in favour of `runs_dir` and `run_dir` at every
   call site, with no alias and no attic, per AGENTS.md "Replacing is deleting".
2. The rest of the unified record: the eleven administrative fields and the
   Mission extension (T002).
3. The eleven consumers named under Design in `T2_F260.md`, one per commit where
   the diff allows (T003).

## Risks

- The sweep is not a blind substitution: `"runs"` is still the correct spelling
  of the RUN store, which round 2 moved INTO `<data_root>/runs/<run_id>`. Only a
  path keyed by a JOB id changes, and the gate counts the job-keyed spellings to
  zero rather than counting the word.
- A test that reaches the path through a shared helper is fixed by the helper and
  must not be edited; two such files are deliberately outside the change set and
  must go green untouched.
<<<END PLANF272R3>>>
<<<BEGIN FIND0818>>>
- R-0818 — Medium, A DECISION RULED FROM A THREE-FILE SEARCH ASSERTED A PROPERTY OF THE WHOLE TEST SUITE, AND THE BRANCH TIP WENT RED AT 207 TESTS. Raised by the reviewer against its own text at the F272 round 2 gate. DECISION F272 D1, committed at `43d91cda` in `docs/roadmap/features/T2_F272.md`, staged the run re-key and stated: "NO CALLER MOVES: all 109 sites resolve through `run_log_dir`, so the re-key is invisible to them, and the only code that observes the change is the three test files that hand-spell the layout." The first half is TRUE and the reviewer re-verified it at the gate — the 74 `load_run_events` readers and 35 `RunLogWriter` writers under `packages/` and `apps/` all resolve through `data_paths.run_log_dir` and not one of them moved. The second half is FALSE. Measured by the reviewer at `b189a03f` with `python3 -m pytest -n auto -q -p no:randomly`: **207 failed, 19528 passed, 23 skipped**, across **24 test files**, and the canary `tests/cli/test_golden_path.py` fell from 42 passed to `1 failed, 41 passed`. The job-keyed run-log directory is hand-spelled at **56 lines in 24 files**, counted by listing every `"runs" /` path component in all of `tests/` — 62 occurrences, of which six are legitimately run-keyed or name a file and must survive — and most of those lines sit inside one module-level helper per file, which is why 56 of the failures sit behind `tests/test_run_log_cli.py` line 46 alone and 18 behind `tests/orchestration/test_event_replay.py` line 10. The cause is precise and worth naming rather than generalising: the reviewer grepped THREE files — the three `docs/roadmap/features/T2_F272.md` T001 happens to name, `tests/test_timeline.py`, `tests/test_run_log.py` and `tests/test_data_paths.py` — and wrote the result as a property of the repository. That is the R-0419 class, "a block may state a repository-wide absence only after a repository-wide search, and the block names the search it ran", recurring in a DECISION rather than in a block, and it is also the R-0526 class, a slice asserting a universal over contents nobody measured. It is Medium rather than Low because the false half was LOAD-BEARING: it is the sentence that sized round 2's change set at three test files, and a round executed against it necessarily leaves the tip red. THE WORKER BEHAVED CORRECTLY AND THE ROUND COST NOTHING BEYOND THIS: it applied the block as written, measured the red itself, attributed it by demonstration rather than by assumption — the canary is exit 0 at 42 in a worktree at C4's parent `43d91cda` and exit 1 at 41 at C4 `1d24b4a7` — declined to widen the sweep on its own authority under self_drive_protocol.md G8, declined to revert C4 so the reviewer could reproduce the numbers, and reported the whole thing. THE FIX IS THE SWEEP, NOT A REVERT, because the production change is right: round 3 changes the `"runs"` component to `"job_logs"` at every job-keyed site in those 24 files and gates the surviving `"runs" /` components in all of `tests/` to exactly the six that are not job-keyed. DECISION F272 D2 records the corrected premise beside D1 rather than rewriting it. STANDING RULE, binding the reviewer from here and additional to R-0419's: when a block or a decision moves a PATH, the search that sizes the change is a search of the WHOLE repository for that path's spelling — `tests/` included and helpers first — and the count it returns is stated in the text as the measurement it is. A feature file naming three files is naming the files it knows about, never the files that exist. OPEN.
<<<END FIND0818>>>
<<<BEGIN DECISIOND2>>>
### DECISION F272 D2 (2026-09-06, F272 round 3) — correction to D1's premise: 24 test files observed the move, not three
DECISION F272 D1 is CORRECT IN ITS RULING and is not withdrawn: the run log keeps
its job key, the two directories move one function body each, the name collapse
follows in its own round, and the merge of the log into the per-run directory
stays deferred to T003. This decision corrects one FALSE SENTENCE in it, by
appending rather than by rewriting, which is how this repository corrects a
landed decision — the precedent is "DECISION F085 D6 — correction to the ruled
figure" in `.agent/decisions.md`.

THE FALSE SENTENCE. D1 says "the only code that observes the change is the three
test files that hand-spell the layout". Measured at `b189a03f`, after D1's move
had landed: `python3 -m pytest -n auto -q -p no:randomly` gives 207 failed,
19528 passed, 23 skipped, across 24 test files, and the job-keyed run-log
directory is hand-spelled at 56 lines in 24 files. The three files D1 named are
the three `docs/roadmap/features/T2_F272.md` T001 happens to list; they are the
files the reviewer searched, not the files that exist. Registered as finding
R-0818.

WHAT REMAINS TRUE, re-verified at the same commit: no production caller moved.
All 74 `timeline.load_run_events` readers and 35 `run_log.RunLogWriter` writers
resolve through `data_paths.run_log_dir`, and gates G5 and G6 of round 2 showed
the six shipped path functions returning exactly the layout D1 rules. The staging
D1 chose is therefore the right staging; only its estimate of the observer set
was wrong, and an estimate is what it should never have been.

CONSEQUENCE. The test-side spelling sweep that `docs/roadmap/features/T2_F272.md`
T001 inherits from DECISION F260 D6 is LARGER than that file's own sentence
suggests, and it is performed in full in round 3 rather than deferred: 24 files,
each read at the site rather than substituted blindly, because `"runs"` remains
the correct spelling of the RUN store that round 2 moved INTO `<data_root>/runs/`.
The gate is the job-keyed spelling counted to zero across all of `tests/`, never
the word counted anywhere.

REVERSE by deleting this section, at which point D1's premise sentence stands
uncorrected while the sweep it under-counted remains on disk.
<<<END DECISIOND2>>>
