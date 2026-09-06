── STEP T001 (part 2) — F272 ─────────────────────────────────
Goal:        Free `<data_root>/runs/` for the RUN id. Rule the staging of the
             re-key as DECISION F272 D1 from the reviewer's measurement, move
             the job-keyed run log out of `runs/` and the ping-pong run store
             into it — the two function bodies F260 rounds 11 and 12 built for
             exactly this — and sweep the tests that hand-spell both paths.
Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 book the round 1
             verdict · C3 DECISION F272 D1 into the feature file · C4 the two
             directory bodies and the test sweep, together · C5 the handback
(the rule line above is 61 copies of U+2500; the rule line below is the same 61)
─────────────────────────────────────────────────────────────

## The branch

You are on `feature/f272-one-world-completion` at `69138a45`, which is round 1's
handback and the branch tip. Round 1 PASSED its gate; the reviewer re-ran every
one of its eight gates and reproduced every reading. Stay on that branch. Nothing
is merged, no pull request is created, and `main` is never touched.

## Change set — nothing outside this list

    .agent/authored/f272-r2.md              (new, C0a)
    .agent/last_block.md                    (C0b)
    .agent/plan.md                          (C1)
    .agent/live_review.md                   (C2)
    docs/roadmap/features/T2_F272.md        (C3)
    packages/orchestration/data_paths.py    (C4)
    tests/test_data_paths.py                (C4)
    tests/test_run_log.py                   (C4)
    tests/test_timeline.py                  (C4)
    .agent/handoff.md                       (C5)

Scratch goes under the gitignored `.remedy-wt/` only, and `git ls-files
.remedy-wt` must return nothing when you finish.

## The slices in this block

Each authored text sits between `<<<BEGIN name>>>` and `<<<END name>>>` on their
own lines. Extract by exact-position marker matching, asserting exactly one BEGIN
and one END per name; the marker lines never reach any file. The whole-file text
is PLANF272R2; the appended texts are GATEF272R1 and DECISIOND1.

## C0a — save this block

This block is on disk at `.remedy-wt/f272-r2-block.md`. The delegating prompt
states that file's sha256; call it BLOCK_SHA. VERIFY the source against BLOCK_SHA
BEFORE executing anything else. Then `shutil.copyfile` it to
`.agent/authored/f272-r2.md` — never a retype — and commit it alone.

## C0b — mirror

`shutil.copyfile` the same bytes to `.agent/last_block.md` and commit it alone.
One indivisible `.agent/**` state rewrite (AGENTS.md DECISION F104 D1 exemption).

## C1 — the plan

Write `.agent/plan.md` from the PLANF272R2 slice, byte for byte plus exactly one
trailing newline, and commit it alone. FIRST substantive commit, because this
round touches the finding ledger (planner_reviewer_prompt.md §3 item 23).

## C2 — book the round 1 verdict

APPEND the GATEF272R1 slice to `.agent/live_review.md` and commit it alone. The
recipe, and nothing else: read the file's own terminal byte first and confirm it
is exactly one newline; then write, in ONE write, the pre-image followed by a
single newline followed by the slice followed by a single newline.

The header is `Gate: F272 R1 — `, the FEATURE-FIRST form, and NOT
`Gate: R1 — the F272 R1 entry`. The reviewer compared the slice's header against
the headers already in that file at `69138a45`: `^Gate: R1 — ` ALREADY OCCURS
ONCE there, as F260's own round 1 entry, because F260's records rotate at the
NEXT closure and are still live. The second form would put two paragraphs under
one key (§3 item 26). `scripts/rotate_live_review.py` recognises both forms —
its `^Gate: F(\d{3}) R\d+` pattern is the one this slice matches — so the entry
still classifies to F272 and still rotates.

No finding is minted, resolved or renumbered.

## C3 — DECISION F272 D1

APPEND the DECISIOND1 slice to the END of `docs/roadmap/features/T2_F272.md`,
after its last existing line, by the same read-the-terminal-byte recipe as C2,
and commit it alone. Nothing already in that file changes by one byte.

## C4 — the two directory bodies and their observers, in ONE commit

The production halves and the test halves land TOGETHER: separating them would
leave the branch tip red at an intermediate commit, since the tests below are
what observe these paths. Declare that in the handback.

(a) `packages/orchestration/data_paths.py`. Add, beside the other
    "where does this live" answers:

        def job_logs_dir(root: Path | None = None) -> Path:
            """The job-keyed run-log area (<root>/job_logs)."""
            return (root if root is not None else resolve_data_root()) / "job_logs"

    Change `run_log_dir`'s BODY to `return job_logs_dir(root) / str(job_id)`. Its
    signature, its name and all 35 writer and 74 reader call sites are UNCHANGED
    — that is the whole point of the staging D1 rules, and you must not touch
    them.

    Change `pingpong_runs_dir`'s BODY to `return runs_dir(root)`, so the
    ping-pong run store now IS `<root>/runs/` keyed by run id.
    `pingpong_run_dir` already builds on it and needs no body change.

    Update the module docstring's Public API list and the two comment blocks that
    describe these directories AS THEY ARE TODAY, so no comment survives claiming
    a layout the code no longer has. Do not delete `pingpong_runs_dir` or
    `pingpong_run_dir`: DECISION F272 D1 places that collapse in the NEXT round,
    with the call-site sweep that makes it true.

(b) The observers. Sweep every hand-spelled occurrence of the two OLD layouts in
    `tests/test_data_paths.py`, `tests/test_run_log.py` and
    `tests/test_timeline.py`, and nothing else. The reviewer measured these at
    `69138a45`; re-grep before editing, because your own C4(a) does not move them
    but a careless edit can:
      - `tests/test_run_log.py` lines 128, 134 and 175 — `tmp_path / "runs" /
        str(job_id)` becomes `tmp_path / "job_logs" / str(job_id)`.
      - `tests/test_timeline.py` lines 66 and 255 — `data_dir / "runs" /
        str(job_id)` and `tmp_path / "runs" / str(job_id)` become `"job_logs"`.
      - `tests/test_data_paths.py` lines 126 and 138 — the `run_log_dir(...)`
        equalities become `"job_logs"`.
      - `tests/test_data_paths.py` lines 423 and 424 — the `pingpong_runs_dir` /
        `pingpong_run_dir` equalities become `arg_root / "runs"` and
        `arg_root / "runs" / rid`.
    LEAVE UNCHANGED, because `runs_dir` and `run_dir` themselves do not move:
    `tests/test_data_paths.py` lines 79, 102, 120 and 392. Where a docstring in
    those files describes the old layout as current, correct the docstring in the
    same commit; a test whose prose lies about the path it asserts is the defect
    this feature exists to remove.

## C5 — the handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md and commit it
last. Mandated sections, the item-status table covering C0a to C5 with every item
exactly once, one line per gate with REAL exit codes, and the SESSION NUMBER
line: **SESSION 1 of feature F272**, round 2. No length cap. Do NOT state C5's
own insertion count — the reviewer measures it at the gate (§3 items 14 and 31).

## Constraints

1. Every slice is applied BYTE FOR BYTE. If you believe one is wrong, apply it
   anyway and record the objection in the handback's deviations.
2. The change set above is exhaustive. In particular `README.md`,
   `docs/roadmap/STATUS.md`, `packages/orchestration/run_log.py`,
   `packages/orchestration/timeline.py` and every `apps/cli/commands/` module are
   NOT edited this round: the staging D1 rules exists precisely so that no caller
   moves.
3. Both appends this round are APPENDS, not pairs: GATEF272R1 into
   `.agent/live_review.md` and DECISIOND1 into
   `docs/roadmap/features/T2_F272.md`. Neither is a FROM/TO replacement, so no
   containment reading and no FROM-zero count applies to either; the obligation
   is the ordered-equality reading of §4 item 9, gated below.
4. NO FINDING ID IS MINTED, RESOLVED OR RENUMBERED. The open set is 298 BY
   DISTINCT ID at `69138a45` and must be 298 after C2. The next free id is
   R-0818; this round does not spend it.
5. COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, each its own commit, each
   single-parent, nothing after C5.
6. Every gate runs at a commit STRICTLY EARLIER than C5 (§3 item 31).
7. This session's shell guard refuses `python3 <script>` followed by
   `echo "EXIT=$?"`, refuses shell loops and refuses `$(...)`. Read exit codes
   from `subprocess.run(...).returncode` inside Python files under `.remedy-wt/`.
   Bare `ruff` is DENIED; the spelling that runs is `python3 -m ruff check`.
8. DESTRUCTIVE VERIFICATION — the G7 red proof only — runs in a DISPOSABLE
   `git worktree` and never in the primary checkout (self_drive_protocol.md G5).
   Remove and prune it before C5.
9. NOTHING IS MERGED and no pull request is created. `gh pr merge` and
   `gh pr create` are not run at all.
10. Read `.agent/STOP` with `os.path.exists` before C0a, before C4 and before
    C5, and report all three readings.
11. THIS BLOCK'S OWN SIZE, measured by the reviewer on these final bytes: PROSE
    274 lines against the 400-line cap of DECISION F105 D5, and TOTAL 379 lines
    against the 490-line budget of DECISION F085 D6. Re-measure BOTH from the
    committed `.agent/authored/f272-r2.md` and report both.

## Done when — the gates

Record every gate's REAL exit code and REAL output.

**G1 TRANSPORT.** `.remedy-wt/f272-r2-block.md`, the committed
`.agent/authored/f272-r2.md` at C0a and `.agent/last_block.md` at C0b are
byte-identical: report the one sha256, the one byte length, and
`filecmp.cmp(shallow=False)` for source-vs-saved and source-vs-mirror. The digest
must equal BLOCK_SHA.

**G2 THE RECORD**, at C2. (a) BYTE: the post-image equals the pre-image plus one
newline plus GATEF272R1 plus one newline, EXACTLY, and the pre-image is a
byte-exact PREFIX of it; report bytes before and after and the delta; report that
the pre-image ended in exactly one newline, ASSERTED FROM ITS OWN TERMINAL BYTE
BEFORE WRITING, and that the post-image does too. (b) STRUCTURAL, computed
independently of (a): split the WHOLE image on `\n{2,}`, drop units empty after
stripping, strip each survivor of leading and trailing newlines; report the unit
count before and after, and that the last N units equal the slice's paragraphs IN
ORDER, where N is a number YOUR SCRIPT COUNTS from the slice and never one this
block asserts. (c) NEGATIVE CONTROL, in memory on a `bytes` object and NEVER on
disk: flip one byte inside the FIRST appended paragraph, having first ASSERTED by
offset that the chosen byte lies inside it; report that reader (a) REJECTS and
reader (b) REJECTS, then restore and report that both ACCEPT and the restored
image equals the disk image. (d) COUNTS before → after: `^Gate: ` 23 → 24;
`^Gate: F272 R1 — ` 0 → 1; `^Gate: R1 — ` 1 → 1, UNCHANGED, which is the
duplicate-key reading; distinct `^- R-\d{4} — ` ids 301 → 301; distinct
`^Done: R-\d{4} — ` ids 3 → 3; open set BY DISTINCT ID 298 → 298.

**G3 THE PLAN**, at C1. `.agent/plan.md` equals PLANF272R2 plus exactly one
trailing newline — report the byte length and the equality; line count under the
AGENTS.md cap of 50; carries `## Goal` and `## Next Steps`.

**G4 THE FEATURE FILE**, at C3. The pre-commit blob is a byte-exact PREFIX of the
post-commit file; the slice plus its leading and trailing newline is an exact
SUFFIX of it; and the lines C3's diff ADDS are exactly the slice's lines IN ORDER
— the §4 item 9 ordered-equality reading for an append, not a per-line count.
Report bytes before and after. Then, because the change set holds a
`docs/roadmap/**` path: `python3 -m pytest tests/docs/ -q -p no:randomly` exit 0
(303 passed at the base) and `python3 -m pytest
tests/orchestration/test_roadmap_index.py -q -p no:randomly` exit 0 (30 passed at
the base).

**G5 THE CODE**, at C4. `python3 -m ruff check
packages/orchestration/data_paths.py tests/test_data_paths.py
tests/test_run_log.py tests/test_timeline.py` exits 0. Then read the SHIPPED
functions, not the source text, with an explicit root argument:
`job_logs_dir(R)` is `R/job_logs`; `run_log_dir("j1", R)` is `R/job_logs/j1`;
`runs_dir(R)` is `R/runs`; `run_dir("r1", R)` is `R/runs/r1`;
`pingpong_runs_dir(R)` is `R/runs`; `pingpong_run_dir("r1", R)` is `R/runs/r1`.
Report each of the six as the path it returned. Report also that the string
`pingpong_runs` occurs ZERO times in the RETURNED paths above — it may still
occur in the module's own identifiers, which this round deliberately keeps.

**G6 THE OBSERVERS AND THE NEIGHBOURS**, at C4, run SERIALLY: `python3 -m pytest
tests/test_data_paths.py tests/test_run_log.py tests/test_timeline.py -q
-p no:randomly` exit 0; then `python3 -m pytest tests/test_do_job_flow.py
tests/orchestration/test_job_run_refs.py -q -p no:randomly` exit 0 (178 and 4 at
the base); then `python3 -m pytest tests/ui_server/ -q -p no:randomly` exit 0
(515 at the base) and `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py -q -p no:randomly` exit 0 (89 at the
base). Report every passed count.

**G7 THE PRE-SWEEP RED PROOF**, ONLY inside a disposable worktree created at
C4's commit. This proves the swept tests really observe the paths C4(a) moved —
the pre-sweep half of the pair `docs/roadmap/features/T2_F272.md` T001 calls for.
Report in this order: (i) the CONTROL — `python3 -B -m pytest
tests/test_data_paths.py tests/test_run_log.py tests/test_timeline.py -q
-p no:randomly` inside that worktree, exit 0 with its passed count, and the
`__file__` of `packages.orchestration.data_paths` as imported there, which must
lie INSIDE the worktree; (ii) THE PRE-SWEEP — restore ONLY those three test files
to their C3 content with `git checkout <C3-sha> -- tests/test_data_paths.py
tests/test_run_log.py tests/test_timeline.py`, leaving `data_paths.py` at C4, and
re-run the same command; report the exit code, the failed count and the NAME of
every failing test. It must be non-zero, and the failures must name the run-log
and ping-pong path assertions. (iii) `git -C <worktree> diff --name-only` after
the restore. Then remove and prune the worktree and report `git worktree list`.
If the CONTROL is not exit 0, the proof is VOID: report that and mutate nothing.

**G8 THE CANARY, INTEGRITY AND THE TREE**, in the primary checkout after C4 and
BEFORE C5 is staged. `python3 -m pytest tests/cli/test_golden_path.py -q
-p no:randomly` exit 0 at 42 passed. `python3 -m apps.cli.grouped integrity check
--json` exit 0 with `"passed": true` and `"fail_count": 0`.
`git status --porcelain` EMPTY and `git ls-files .remedy-wt` empty. Per commit
and for C0a through C4 ONLY, the `git diff --numstat <parent> <commit>` INSERTION
count — the column AGENTS.md DECISION F104 D1 caps at 500 — and that each commit
is single-parent. The count of lines beginning with the BEGIN or END marker
prefix in each of `.agent/plan.md`, `.agent/live_review.md`,
`docs/roadmap/features/T2_F272.md`, `packages/orchestration/data_paths.py`,
`tests/test_data_paths.py`, `tests/test_run_log.py` and `tests/test_timeline.py`;
each must be 0.

<<<BEGIN PLANF272R2>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion, cut from `main` at
`b18fad576252f7f2739a5807b6408031da8fcde6`. Round 1 is reviewed and PASSED.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

Round 2 completes the FIRST move of the re-key. `<data_root>/runs/` is occupied
today by the job-keyed run log, so nothing can be keyed there by RUN id until
that log moves out. This round books round 1's verdict, records DECISION F272 D1
— which rules the staging from the reviewer's measurement of 74 reader and 35
writer call sites — moves the run log to `<data_root>/job_logs/<job_id>` and the
ping-pong run store to `<data_root>/runs/<run_id>`, each one function body, and
sweeps the three test files that hand-spell those paths.

## Next Steps

1. The name collapse DECISION F272 D1 places next: `pingpong_runs_dir` and
   `pingpong_run_dir` are DELETED in favour of `runs_dir` and `run_dir` at every
   call site, with no alias and no attic, per AGENTS.md "Replacing is deleting".
2. The rest of the unified record: the eleven administrative fields and the
   Mission extension (T002).
3. The eleven consumers named under Design in `T2_F260.md`, one per commit where
   the diff allows (T003).

## Risks

- The run log's directory moves while its API does not. Every one of the 74
  readers and 35 writers keeps working only because they all resolve through
  `data_paths.run_log_dir`; a caller that hand-spells the path instead would
  break silently, which is why the three test files that do exactly that are
  swept in the same commit and are the round's red proof.
- Old `.data` content becomes unreadable at this move. That is DECISION D-A
  working as ruled — no migration, no compatibility reader — not a regression.
<<<END PLANF272R2>>>
<<<BEGIN GATEF272R1>>>
Gate: F272 R1 — the F272 round 1 entry. R1 CLAIMED THE FEATURE AND GAVE THE JOB RECORD ITS PLURAL RUN LIST. VERDICT PASS. Range `b18fad57`..`69138a45`, eight commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6 with nothing added, dropped or reordered; insertion counts 488, 472, 57, 28, 1, 10, 122 and 296, each read from `git diff --numstat <parent> <commit>` and every one far under the AGENTS.md DECISION F104 D1 cap of 500, which counts INSERTIONS only. `git diff --name-only b18fad57..69138a45` lists exactly the nine paths of the change set and nothing more. THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT: the reviewer's scratch original `.remedy-wt/f272-r1-block.md`, the committed `.agent/authored/f272-r1.md` and the committed `.agent/last_block.md` are all 27393 bytes and all hash to `229900f50fc6cf7dfc85d54ab2e6631cc6e8ec5cf08be54db92bf13f627e0165`, the digest the delegation named before the round began; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. THE RECORD, at `5b14f469`: 955525 to 955908 bytes, and the reviewer reconstructed the post-image INDEPENDENTLY from the pre-image with only the two ordered replacements applied and found it byte-equal to the committed result; the carried region from the newline before `## Findings` to end of file is 953408 bytes hashing to `147ce009557d42bc81def2249853ed1a8fccd60676077a08e9532aea0bc0f8dc` BOTH before and after, so no finding record moved by one byte; registrations 301 to 301 and resolutions 3 to 3 BY DISTINCT ID, open set 298 to 298, zero ids minted, `^Gate: ` 23 to 23, and no `Gate: R24` paragraph exists anywhere, which is the F260 branch terminator being absent by construction rather than missing. THE PLAN AND THE CONTEXT, at `9b5312b2`: 2097 and 3366 bytes, each byte-equal to its slice plus exactly one trailing newline; the plan is 43 lines against the 50-line cap and carries `## Goal` and `## Next Steps`; the context carries `## Active Branch` with a `feature/` slug, a roadmap F-id and the substrings the four state readers assert. THE STATUS CLAIM, at `754bd14e`: `[~] F272` exactly 1, `[ ] F272` 0, accepted `[x]` still 74 and ledger lines still 272, file-wide `[~]` exactly 1 — the at-most-one-claim invariant `tests/docs/test_docs_consistency.py` pins — and that commit touches `docs/roadmap/STATUS.md` alone, `README.md` being byte-identical across the whole range. THE CODE, at `6955a197`, read from the SHIPPED dataclass rather than from the source text: `JobPlan().run_refs` is `[]` on two fresh instances and the two are NOT the same list object, so the `default_factory` is real; mutating one leaves the other empty; `_export_job` then `_import_job` preserves two ids IN ORDER; a record dict carrying no `run_refs` key imports as `[]` rather than raising; the string `run_refs` went 0 to 7 occurrences and `job.run_refs.append` occurs exactly once. THE TESTS, at `c16ad23d`: four tests, all four green in 0.74s. SUITES re-run by the reviewer, serially, in the primary checkout: `tests/orchestration/test_job_run_refs.py` exit 0 at 4, `tests/test_do_job_flow.py` and `tests/orchestration/test_job_budgets.py` exit 0 at 313 together — 178 and 135, both their base counts — `tests/docs/` and `tests/orchestration/test_roadmap_index.py` exit 0 at 333, `tests/ui_server/` exit 0 at 515, the three remaining state readers exit 0 at 89, the canary `tests/cli/test_golden_path.py` exit 0 at 42, `python3 -m ruff check` over both changed code paths exit 0, and `python3 -m apps.cli.grouped integrity check --json` exit 0 with `"passed": true` and `"fail_count": 0`. THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY in the reviewer's own disposable worktree at `c16ad23d`, with `packages.orchestration.pingpong_job` confirmed to resolve from INSIDE that worktree rather than from an editable install, `python3 -B` throughout and no `__pycache__` present: the unmutated control is a real exit 0 at 4 passed, deleting the two appending lines — verified to occur exactly once in that file before deletion — gives exit 1 with `1 failed, 3 passed` and the single failure is `tests/orchestration/test_job_run_refs.py::TestJobRunRefsEndToEnd::test_run_refs_names_every_task_run_in_order`, the end-to-end test, and the worktree diff names only `packages/orchestration/pingpong_job.py`; restoring the bytes returns the diff to empty and the worktree was removed and pruned. `git status --porcelain` EMPTY and `git ls-files .remedy-wt` empty at the gate, and zero marker lines reached any of the six written files. THE WORKER DECLARED FOUR DEVIATIONS AND ALL FOUR ARE UPHELD. The first is the reviewer's and is recorded here rather than charged to the round: G2(b) ordered the carried region "from and including the line `## Findings`" while the figure beside it, 953408 bytes, was measured from the NEWLINE BEFORE that line, so the worker's stricter reading of the block's words gave 953407 and a different digest; both readings are identical before and after C2, the reviewer re-measured both, and the load-bearing property — that no finding record changed — holds under either. The second declares that C0a and C0b precede the plan advance, which is not a deviation at all but the rule: §3 item 23 exempts exactly the two block-save commits, which write nothing but the block itself. The third and fourth record that no slice was edited, no commit reordered, no id spent, and that twelve pre-existing `remedy/job-*` worktrees under `.remedy-wt/` predate this round and were correctly left alone.
<<<END GATEF272R1>>>
<<<BEGIN DECISIOND1>>>
## DECISIONs

### DECISION F272 D1 (2026-09-06, F272 round 2) — the run re-key lands in two moves, and the run LOG keeps its job key
Ruled by the reviewer under docs/agents/planner_reviewer_prompt.md §4 item 7,
from a measurement taken at `b18fad576252f7f2739a5807b6408031da8fcde6` before
any line of this round was written. DECISION F260 D1 rules that a run lives at
`<data_root>/runs/<run_id>/` and adds that this directory "inherits what
`<data_root>/pingpong_runs/<run_id>/` holds today plus the run-log `.jsonl` that
today sits at `<data_root>/runs/<job_id>/`". The second half of that sentence was
written before anyone counted what reads the run log.

MEASURED, by grep over `packages/` and `apps/` at that commit:
`timeline.load_run_events(data_dir, job_id)` has **74 call sites** and
`run_log.RunLogWriter(job_id, ...)` has **35**, across 20 modules under
`packages/orchestration/` and 21 under `apps/cli/commands/`. Every one of them is
keyed by JOB id. Moving the run log under a RUN id therefore does not move a
directory; it changes what 109 call sites must know — each would first have to
resolve a job to its set of runs — and that is a whole-feature change standing
inside a T001 slice. The same measurement shows why the move cannot simply be
skipped either: `<data_root>/runs/` is OCCUPIED by that job-keyed log, so nothing
can be keyed there by run id while it stays.

CHOSEN — two moves, and the run log keeps its job key for now:

- **Move one, this round.** The job-keyed run log leaves `runs/` for
  `<data_root>/job_logs/<job_id>/`, and the ping-pong run store arrives at
  `<data_root>/runs/<run_id>/`. Both are ONE FUNCTION BODY each —
  `data_paths.run_log_dir` and `data_paths.pingpong_runs_dir` — which is exactly
  what F260 rounds 11 and 12 built those single spellings for. NO CALLER MOVES:
  all 109 sites resolve through `run_log_dir`, so the re-key is invisible to
  them, and the only code that observes the change is the three test files that
  hand-spell the layout. `<data_root>/runs/` is now keyed by RUN id and by
  nothing else, which is the property F260 D0 said had to be true before any
  directory moved.
- **Move two, the next round.** `pingpong_runs_dir` and `pingpong_run_dir` are
  DELETED in favour of `runs_dir` and `run_dir` at every call site — no alias, no
  attic, no compatibility reader, per AGENTS.md "Replacing is deleting" and
  DECISION D-A. They survive THIS round only because their bodies and their names
  must stop disagreeing in a commit whose diff a reviewer can read, and a
  nineteen-site rename mixed into a directory move is not that commit.
- **Whether the run log ultimately merges INTO the per-run directory is NOT
  decided here.** It is deferred to T003, where the eleven consumers move onto
  the unified model anyway and where a job can name its runs through
  `JobPlan.run_refs`, which round 1 built. Deciding it now would rule on 109 call
  sites from a measurement of none of them.

ALTERNATIVES CONSIDERED. Performing F260 D1's sentence literally in this task,
moving the log under the run id and teaching all 109 sites to resolve job to runs
— rejected on the count above: it is T003's work with T001's name on it, and no
500-insertion commit holds it. Leaving the log in `runs/` and keying the
ping-pong store there too — rejected as exactly the collision DECISION F260 D0
recorded, two directories under one root answering to different keys. Giving the
ping-pong store a third name and deferring `runs/` entirely — rejected because it
adds a spelling this feature exists to remove.

NOT CHANGED BY THIS RULING: the deliverable, the scope, and F260 D1's layout for
the JOB and the MISSION. Only the ORDER of the run log's move, and the task it
finally lands in, are settled here.

REVERSE by deleting this section, at which point F260 D1's sentence binds
unamended and the run log's move returns to this task as a required slice.
<<<END DECISIOND1>>>
