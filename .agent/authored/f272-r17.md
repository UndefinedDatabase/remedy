STEP T003 (consumer 2) — F272 One world completion — ROUND 17

EVERY RULE LINE IN THIS BLOCK IS EXACTLY SIX U+2500 CHARACTERS, so no run of
repeated characters in this frame has a length a reader has to recover by eye.

You are the WORKER for one round of docs/agents/self_drive_protocol.md.
AGENTS.md binds you in full: the self-review loop before EVERY commit, small
commits, `.agent/plan.md` current, a clean tree, a push at the end, and a
rewritten `.agent/handoff.md`. You write everything; the reviewer writes nothing
and will re-run every gate below itself before any verdict.

SESSION 9 of F272, round 17. The base of this round is `5964aa76`. F272's soft
limit is 12 sessions and 40 rounds under operator amendment
amend0906-triage-throughput, so the feature is inside it and no scope report is
owed.

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
`remedy job context <id>` searches the CLASSIC job store alone, so it answers
"no job matches prefix" for every job `remedy do job-run` created. Move it onto
the unified record — the second T003 consumer — and pin the move with tests
against a job built the ping-pong way.

Bundle, in this commit order
──────
C0a  save this block verbatim to `.agent/authored/f272-r17.md`
C0b  mirror the same bytes into `.agent/last_block.md`
C1   REPLACE `.agent/plan.md` with the PLANF272R17 slice
C2   APPEND the RECORDR17 slice to `.agent/live_review.md`
C3   the production change to `apps/cli/commands/job_context_cmd.py`, per the
     SPEC below — DESCRIBED, NOT SLICED
C4   APPEND the GUARDR17 slice to `tests/cli/test_job_context_cmd.py`
C5   rewrite `.agent/handoff.md`

Change set — these paths and nothing else
──────
  .agent/authored/f272-r17.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  apps/cli/commands/job_context_cmd.py
  tests/cli/test_job_context_cmd.py
  .agent/handoff.md

Constraints
──────
1. A SLICE IS APPLIED BYTE FOR BYTE. Extract each one PROGRAMMATICALLY from
   `.agent/authored/f272-r17.md`, between its `<<<BEGIN NAME>>>` and
   `<<<END NAME>>>` lines. Never retype, reflow, re-indent or "correct" a slice.
   If a slice looks wrong, apply it anyway and DECLARE it in the handback.
2. NO MARKER LINE REACHES A TARGET FILE. After C4, the line-anchored count of
   `^<<<(BEGIN|END) .*>>>$` is 0 in each of `.agent/plan.md`,
   `.agent/live_review.md` and `tests/cli/test_job_context_cmd.py`. Measured by
   the reviewer at `5964aa76`: that line-anchored count in
   `.agent/live_review.md` is already 0, while the file contains 15 MID-LINE
   `<<<` substrings inside older records' prose. Those are PRE-EXISTING, they
   are not marker lines, and the line-anchored reading is the one that binds —
   round 14's accepted deviation 2 established exactly this.
3. NO EXISTING TEST IS EDITED, DELETED OR WEAKENED. C4 is a pure append and its
   diff is insertions only.
4. ZERO finding ids are minted this round. The next free id is R-0823 and it
   stays free. C2 books a verdict and a resolution the reviewer has already
   authored; it registers nothing new.
5. READ `.agent/STOP` with `os.path.exists` at each of these points and report
   every reading: before C0a, before C3, and before C5. If it exists at any of
   them, finish the commit in flight, write the handoff, and stop.
6. THE PRODUCTION CHANGE IS DESCRIBED, NOT SLICED. Write the code yourself,
   under the SPEC below and AGENTS.md's self-review loop. The SPEC fixes
   behaviour, seam and public surface; the wording of the code is yours.
7. C2 IS APPENDED AS `pre + b"\n" + slice`, against a pre-image you READ
   immediately before the write rather than one you assume.

SPEC for C3 — apps/cli/commands/job_context_cmd.py
──────
The file today loads a job with `load_job(resolve_job_id(job_id_str))` inside
`_cmd_job_context`, and reads every field through the CLASSIC shapes: a core
`Job` with `.id` and `metadata["target_repo"]`, and core `Task` objects with
`.id` and an `inputs["flight"]` block. The unified record spells all four
differently — `JobPlan.job_id`, `JobPlan.repo_path`, `TaskEntry.task_id` and
`TaskEntry.files_hint` — and carries no flight block at all.

S1. ADD `_job_identity(job) -> str`. Returns `job_id` when the object has a
    truthy one, otherwise `id`, always as `str`. Carry one WHY line: the
    unified record spells it `job_id`, the classic Job spells it `id`.

S2. ADD `_job_target_repo(job) -> str`. Returns `repo_path` when truthy;
    otherwise `metadata["target_repo"]` when `metadata` is a dict; otherwise
    `""`. It must not raise for an object carrying neither. One WHY line naming
    both spellings.

S3. ADD `_task_identity(task) -> str`. Returns `task_id` when truthy, otherwise
    `id`, always as `str`. One WHY line: `TaskEntry` spells it `task_id`
    (`T001`), the classic Task spells it `id` (a UUID).

S4. WIDEN `_task_planned_id`. A truthy `task_id` attribute IS the planned id and
    wins; otherwise the existing flight-block read is unchanged.

S5. WIDEN `_task_files_hint`. A `files_hint` attribute that is a `list` wins;
    otherwise the existing flight-block read is unchanged. The existing
    "an absent hint is an EMPTY scope" behaviour does not move.

S6. `_task_label`'s fallback becomes `_task_identity(task)[:8]`. Its docstring
    says "the first 8 hex of its UUID", which this change falsifies — correct
    that clause to say the first 8 characters of its id, and change nothing
    else in that function.

S7. `resolve_task_for_context`'s PREFIX branch matches on
    `_task_identity(task).lower()` in place of `str(task.id)`. The `.lower()` is
    load-bearing rather than cosmetic: `ref` is already lowercased, a classic
    UUID is already lowercase so nothing about the classic path moves, and
    `T001` is not — without it a `TaskEntry` is not prefix-addressable at all.
    The planned-id branch above it is UNCHANGED and still runs first.

S8. `_cmd_job_context` resolves and loads across BOTH stores, in this order:
    resolve the argument with `resolve_any_job_id` rather than `resolve_job_id`,
    try `pingpong_job.load_job_plan(resolved)` FIRST, and fall back to
    `storage.load_job(resolved)` inside the existing `except JobNotFoundError`
    that prints `Job not found: {job_id_str}` and exits 1. `repo_str` then comes
    from `_job_target_repo(job)`, and the `result` dict's `"job_id"` and
    `"task_id"` come from `_job_identity(job)` and `_task_identity(task)`.
    Carry a comment naming WHY the unified record is read first: it is the same
    order `apps/cli/commands/job_stop_cmd.py::_load_job` already reads in.

WHAT MUST NOT MOVE, each of these being something a gate below measures:
  * the exit codes — 0 compiled, 1 unknown job, 2 no usable target repo,
    3 unresolvable task — and the stderr wording of each;
  * `resolve_any_job_id`'s own exit path: it prints
    `Error: no job matches prefix '<id>'` and exits 1 for an unknown short hex,
    byte-identical to what `resolve_job_id` printed there before;
  * `_repo_candidate_paths_with_source`, `list_repo_candidate_paths`,
    `_task_flight_inputs`, `_included_json`, `_print_text_view` and
    `COMMAND_HANDLERS` — none of them is touched;
  * DECISION F260 D5, which places the RESOLVER COLLAPSE in T004. This round
    ADDS a caller of `resolve_any_job_id`, which is exactly what that
    function's own docstring says callers reaching both stores do. It does not
    merge, rename or delete either resolver.

You may name the old function in a WHY comment if that is the honest way to say
what changed; no gate here counts that name to zero.

Measured by the reviewer at `5964aa76`, by applying this SPEC in a disposable
worktree and RUNNING it: `git diff --numstat` reads 56 insertions and 15
deletions for this file, `python3 -m ruff check` exits 0, and the file's own
suite goes from 9 tests to 12. Report the numbers YOU measure; where yours
differ, report the difference and change nothing to make them agree.

Slices
──────

<<<BEGIN PLANF272R17>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 16 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 and T002 are
COMPLETE. T003 is open: round 16 moved its first consumer, `job stop`, and this
round moves the second.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

T003's second consumer. `remedy job context` searched the CLASSIC store alone,
so it answered "no job matches prefix" for every job `remedy do job-run`
created. It now resolves across both stores and reads a `TaskEntry`'s own
`task_id` and `files_hint`, the way `job_stop_cmd._load_job` already reads
unified first and classic second.

## Next Steps

1. The remaining T003 consumer surface, re-grepped rather than taken from
   F260's 2026-09-05 list: `packages/orchestration/ui_server.py` and its
   `_JobPlanTaskAdapter`. That shim is finding R-0804's subject and the
   2026-09-06 triage routes R-0804 to F273 T001, so the boundary is ruled
   before it is touched. The `resolve_any_job_id` sites in
   `apps/cli/commands/teach_cmd.py` STAY: DECISION F260 D5 puts the resolver
   collapse in T004, with the store that makes it true.
2. Rule the Acceptance conflict as a DECISION, inside a round doing other
   work: this feature's Acceptance names tests.md ids that the 2026-09-06
   triage gave to F273 T001, and F272 cannot close while both claims stand.
3. T004, the classic runner and the resolver collapse, where `_CoreJobAdapter`
   dies with the classic store it exists to adapt.
4. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- F272's soft limit is 12 sessions and 40 rounds under operator amendment
  amend0906-triage-throughput. At session 9 and round 17 the feature is
  inside it and no scope report is owed.
<<<END PLANF272R17>>>

<<<BEGIN GUARDR17>>>
def _make_ping_pong_job(repo, *, files_hint=("alpha.py",), attach_repo=True):
    """Persist a real UNIFIED job record — the shape `remedy do job-run` writes.

    Its task carries no flight-plan block at all: a `TaskEntry` spells its
    planned id and its fenced scope as its OWN fields, which is exactly what
    this command must read to answer for a job of either store.
    """
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

    task = TaskEntry(task_id="T001", title="edit alpha", files_hint=list(files_hint))
    job = JobPlan(
        job_title="f272-context",
        repo_path=str(repo) if attach_repo else "",
        tasks=[task],
    )
    save_job_plan(job)
    return job, task


def test_a_ping_pong_created_job_compiles_context_like_a_classic_one(tmp_path, env):
    repo = _make_repo(tmp_path)
    job, _task = _make_ping_pong_job(repo)

    data = _run_json(env, job.job_id, "--task", "T001")

    assert data["job_id"] == job.job_id
    assert data["task_id"] == "T001"
    assert data["task_label"] == "T001"
    assert data["fenced_paths"] == ["alpha.py"]
    assert _entry(data["included"], "alpha.py")["tier"] == 1
    assert _entry(data["included"], "beta.py")["tier"] == 2
    assert data["candidate_count"] == 4


def test_a_ping_pong_job_without_a_repo_path_exits_two(tmp_path, env):
    """The unified record spells the target repo `repo_path`, so an empty one
    must reach the SAME exit 2 an unattached classic job reaches."""
    repo = _make_repo(tmp_path)
    job, _task = _make_ping_pong_job(repo, attach_repo=False)

    r = run_grouped_cli(["job", "context", job.job_id, "--task", "T001"], env)
    assert r.returncode == 2
    assert "target_repo" in r.stderr
    assert "Traceback" not in r.stderr


def test_an_unknown_job_of_either_shape_still_exits_one(tmp_path, env):
    """The exit-1 contract this module's docstring states, pinned across BOTH
    id shapes now that the lookup reaches both stores."""
    from uuid import uuid4

    for unknown in (str(uuid4()), "0123456789abcdef"):
        r = run_grouped_cli(["job", "context", unknown, "--task", "T001"], env)
        assert r.returncode == 1, f"{unknown}: {r.stdout}{r.stderr}"
        assert "Traceback" not in r.stderr
<<<END GUARDR17>>>

<<<BEGIN RECORDR17>>>
Gate: F272 R16 — the F272 round 16 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `d6e5f5e7`. Range `c80f32ce`..`d6e5f5e7`, nine commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, C7, with the change set exactly the eight ordered paths and nothing else, and `git status --porcelain` empty. G1 TRANSPORT IS A REAL CHAIN AND NOT MERELY SELF-CONSISTENT: the reviewer's own scratch original `.remedy-wt/f272-r16-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r16.md` and `.agent/last_block.md` are all 24740 bytes at 306 lines and all hash to `3ac45e7eeef9ed166ebd01b912423e45fdddc600e114bf4ed4dc02b8223c9c8b`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD: `.agent/live_review.md` 1149219 to 1157784 across TWO appends, each proved against its OWN pre-image, the pre-image a byte-exact prefix of the final image; all seven ordered counts reproduce exactly — registrations 305 to 306, resolutions 248 unchanged, open set BY DISTINCT ID 57 to 58, `^Gate: ` 38 to 39, `^Gate: F272 R15 ` 0 to 1, `^- R-0822 ` 0 to 1 and `^Landed: R-0822 ` 0 to 1 — and `^Done: R-0822 ` read 0, so the worker wrote the `Landed:` line and left the resolution to the reviewer, exactly as §4 item 4 requires. G3 THE PLAN is 1907 bytes byte-equal to its slice at 39 lines against the cap of 50. G4 THE FIX reproduces against the SHIPPED handler, RUN rather than read: with `_load_job` returning a completed `JobPlan`, `_cmd_job_stop(job_id, json_output=True)` raises SystemExit with code 1 and prints `"error": "job_not_stoppable"` with `"job_status": "completed"` as a plain string, and no AttributeError; `job.status` in that file is 0 occurrences and the external JSON key `"job_status"` is still 4, so the contract did not move while the Python field did. G5 THE RED-PROOF was re-run by the reviewer in its own disposable worktree at `1240a6c5`, provenance confirmed to resolve inside that worktree and the worktree removed afterwards by exact path: with C4 alone reverted the run is EXIT 1 with exactly `tests/cli/test_job_stop.py::TestItRefusesToLie::test_a_completed_job_says_so_in_json_too` failing and 26 passing, carrying the real `AttributeError: 'JobPlan' object has no attribute 'status'`, and with C4 restored it is EXIT 0 at 27 passed; the mutation is the SHIPPED DEFECT itself rather than an invented one, which is the strongest form this gate takes. G6 THE SUITES, re-run serially: `tests/cli/` EXIT 0 at 1538 passed, which is the base of 1537 plus exactly the one test C5 adds by an AST count taken at `ee17bb25` and at `d6e5f5e7`; `tests/ui_server/` EXIT 0 at 515; `tests/orchestration/test_test_runner.py` EXIT 0 at 52; `tests/regression/test_resource_safety.py` EXIT 0 at 21; `tests/orchestration/test_integrity_gate.py` EXIT 0 at 16; `tests/cli/test_golden_path.py` EXIT 0 at 42. G7 ruff EXIT 0 `All checks passed!` over both changed files, and integrity EXIT 0 with `"passed": true`, `"fail_count": 0` and `high_blockers_open` PASS despite the newly registered open Medium, which is the behaviour the block predicted. G8 THE TREE: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, and thirteen worktree entries being the primary plus the twelve pre-existing `remedy/job-*`. THE WORKER DECLARED NO DEVIATIONS AND NONE WAS OWED — the reviewer looked independently and found the block's arithmetic correct on every count. Its three stated ASSUMPTIONS are accepted AS assumptions: the C3 separator was read from the target's own convention and proved with both readers; the Commit Gate reading at C0a and C0b is the conservative one; and naming `RunState`'s real home, `packages.core.models`, is a correction the R-0822 registration text should have carried, and the reviewer used that same import when re-running G4.

Done: R-0822 — RESOLVED at F272 round 16, commits `ee17bb25` (the fix) and `1240a6c5` (the guard), verified by the reviewer at `d6e5f5e7` by running the shipped handler rather than by reading it. `apps/cli/commands/job_stop_cmd.py:167` read `job.status` inside the completed-job branch's JSON payload, an attribute neither object `_load_job` can return still carries — round 9 renamed the `JobPlan` field to `state` and round 14 retyped it onto `RunState`, and `_CoreJobAdapter.__slots__` never held `status` either — so `remedy job stop <completed-job> --json` raised `AttributeError` where it owed an error document. It now reads `job.state`, and `tests/cli/test_job_stop.py::TestItRefusesToLie::test_a_completed_job_says_so_in_json_too` exercises that exact path and asserts the `job_not_stoppable` payload. THE EXTERNAL CONTRACT DID NOT MOVE, and this is the half worth recording: the JSON key stays `"job_status"` at 4 occurrences in that file, and because `RunState` subclasses `str` the emitted value is still the plain string `"completed"` rather than an enum repr, which the reviewer confirmed from the real bytes the handler printed. THE RED-PROOF IS THE SHIPPED DEFECT ITSELF rather than an invented mutation: reverting the one-line fix alone in a disposable worktree gives EXIT 1 with exactly the one named test failing on the real `AttributeError`, and restoring it gives EXIT 0 at 27 passed. WHY NO GUARD SAW IT FOR SEVEN ROUNDS, which is the lesson rather than the fix: the neighbouring test covered the same refusal WITHOUT `--json`, and the plain-text branch never reads the attribute — a sibling test exercising one rendering of a branch is not coverage of the branch, and the JSON rendering of every refusal path is where this class of defect hides. The `Landed:` line above this paragraph SURVIVES beside it, per DECISION F272 D10: it records the commits that landed the fix, which this resolution would otherwise be the only carrier of.
<<<END RECORDR17>>>

Done when — every gate below is RUN, with its REAL exit code recorded
──────
Run G1 through G7 BEFORE C5, so the handback can quote them. G6 runs ONLY
inside a disposable `git worktree`, never in the primary checkout, which must
satisfy `git status --porcelain` == empty at every commit boundary.

G1 TRANSPORT — ONE digest comparison. `.remedy-wt/f272-r17-block.md`,
   `.agent/authored/f272-r17.md` and `.agent/last_block.md` share ONE sha256,
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
           ^Done: R-\d{4} distinct    248 -> 249
           open set BY DISTINCT ID     58 ->  57
           ^Gate:                      39 ->  40
           ^Gate: F272 R16              0 ->   1
           ^Done: R-0822                0 ->   1
           ^Landed: R-0822              1 ->   1
       The last of those is the DECISION F272 D10 reading: the `Landed:` line
       SURVIVES beside the `Done:` paragraph and is never written over. Where
       any measurement differs from these figures, REPORT THE DIFFERENCE and
       adjust nothing to make them agree.

G3 THE PLAN — `.agent/plan.md` byte-equals the PLANF272R17 slice; report its
   byte length and its line count against the AGENTS.md cap of 50, and that
   `## Goal` and `## Next Steps` are both present.

G4 THE MOVE IS REAL — against the SHIPPED module, RUN rather than read. Print
   `apps.cli.commands.job_context_cmd.__file__` FIRST as provenance. Then, with
   `REMEDY_DATA_DIR` set in-process to a scratch directory under `.remedy-wt/`,
   persist a `JobPlan` carrying one `TaskEntry` and a real `repo_path`, and call
   `_cmd_job_context(job_id, task_ref="T001", json_output=True)`. Report the
   parsed payload's `job_id`, `task_id`, `task_label` and `fenced_paths`, and
   that no exception was raised. Then call it for an id in NEITHER store and
   report the real exit code and the stderr text. Finally report, over that
   file, the occurrence counts of the two CALL forms `resolve_job_id(` and
   `resolve_any_job_id(` — the reviewer measured 1 and 0 at `5964aa76` and
   expects 0 and 1 after C3.

G5 THE SUITES — run SERIALLY, each its own invocation, each `-q -p no:randomly`,
   all in the PRIMARY checkout, and report the REAL exit code and the counted
   line of each:
       python3 -B -m pytest tests/cli/ -q -p no:randomly
       python3 -B -m pytest tests/ui_server/ -q -p no:randomly
       python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly
       python3 -B -m pytest tests/regression/test_resource_safety.py -q -p no:randomly
       python3 -B -m pytest tests/orchestration/test_integrity_gate.py -q -p no:randomly
       python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
   RECONCILE `tests/cli/` rather than asserting it: COUNT the test functions
   `ast` finds in `tests/cli/test_job_context_cmd.py` at the C3 commit and again
   at the C4 commit, add the difference to the base of 1538 the reviewer
   measured at `5964aa76`, and report your arithmetic beside the number that
   ran. The other readings the reviewer took at that same base are 515, 52, 21,
   16 and 42, in the order the commands are listed. Report any difference and
   change nothing.

G6 RED-PROOF — ONLY inside a disposable worktree added detached at the C4
   commit, removed afterwards BY EXACT PATH and never by glob. Purge every
   `__pycache__` under it first and use `python3 -B` throughout. Probe
   provenance BEFORE any edit: print
   `apps.cli.commands.job_context_cmd.__file__` and confirm it resolves INSIDE
   the worktree, so no editable install shadows it. Then report the ORDERED
   COLOUR, the unmutated control FIRST: with C3's file at its committed state
   the run is green; with C3's file ALONE reverted to its `5964aa76` blob —
   restore it with
   `git checkout 5964aa76 -- apps/cli/commands/job_context_cmd.py` inside that
   worktree, leaving C4's tests in place — the run is red; restored, green
   again. The command each time is
       python3 -B -m pytest tests/cli/test_job_context_cmd.py -q -p no:randomly
   Report the REAL exit code of all three runs and, for the red one, WHICH tests
   failed BY NAME and the assertion text one of them carried. The reviewer
   measured that reverted run as EXIT 1 with two named failures and ten passing.
   `test_an_unknown_job_of_either_shape_still_exits_one` is expected to PASS in
   the reverted run: it is a regression pin on a contract both the old and the
   new code satisfy, and it is deliberately NOT a discriminator. Report what you
   measure.

G7 LINT AND INTEGRITY — both with real exit codes:
       python3 -m ruff check apps/cli/commands/job_context_cmd.py tests/cli/test_job_context_cmd.py
       python3 -m apps.cli.grouped integrity check --json
   For the second, report `passed`, `fail_count` and `check_count`. Do not edit
   a finding to move any of them.

G8 THE TREE — run `git status --porcelain` at EVERY commit boundary and report
   its real output each time; it must be empty every time and empty at the end.
   Report `git ls-files .remedy-wt` (expected empty) and `git worktree list`.
   Then the per-commit insertion counts from
   `git diff --numstat <parent> <commit>`, C5 EXCLUDED because a handback cannot
   count its own insertions, each against the DECISION F104 D1 cap of 500 —
   which counts INSERTIONS only. Report the `.agent/STOP` readings constraint 5
   orders.

Handback
──────
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has NO
length cap. It must carry: the SESSION NUMBER (9) and the round (17); the range
and the branch; a per-commit changed-files table whose `+/-` column is taken
from `git diff --numstat` and NOT from any file's line counts, matching G8's
readings cell for cell; an item-status table holding every one of C0a, C0b, C1,
C2, C3, C4, C5 exactly once as done, skipped or deviated with a reason; the
open-findings count BY DISTINCT ID with the arithmetic that produced it; ONE
LINE PER GATE carrying its real exit code; every deviation and assumption; the
external actions you took; and one sentence of context self-assessment, which
operator amendment amend0905-throughput requires in the Session section.

DO NOT create a PR. DO NOT merge anything. DO NOT force-push. Push the branch
and stop.
