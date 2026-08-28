### STEP T002 — F257 Self-use track, round 3 (THE JOB PATH)

Goal: book the round 2 verdict, and carry a curated queue item onto the REAL job
path — rendered to a job file on disk and planned through
`plan_job_from_file`, so the queue stops being data nobody runs.

Base: `41505dea`, the tip of `feature/f257-self-use-track`. Every reading stated
below was taken there by the reviewer.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f257-r3.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 book the F257 R2 verdict into `.agent/live_review.md` and append one
  reviewer-prose slip to `.agent/prose_slips.md`
- C3 the renderer and planner module and its tests
- C4 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f257-r3.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/prose_slips.md`
- `packages/orchestration/self_use_job.py`
- `tests/orchestration/test_self_use_job.py`
- `.agent/handoff.md`

`packages/orchestration/self_use_queue.py` and `scripts/self_use_queue.json` are
NOT edited. The loader's read-only property is the whole point of DECISION F257
D2, and this round adds a SEPARATE module rather than growing a writer into it.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — it was `[]` when this block was written, and if it is not `[]` now, STOP and
   hand back without committing. Report `git rev-parse HEAD`, which must equal
   `41505deafcf6ea3623661a9dc53dd44eec607855`, and `git branch --show-current`,
   which must be `feature/f257-self-use-track`. Create no branch and no pull
   request. Never force-push and never rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations; the record is repaired by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f257-r3.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under
   the gitignored `.remedy-wt/`. The primary checkout satisfies
   `git status --porcelain` empty at every commit.
6. Shell forms rejected by this session's guard are RE-EXPRESSED, never skipped
   and never weakened. Loops, `$( )`, `${arr[0]}`, `cp`, brace literals
   containing quotes, and every form of environment-variable assignment are
   rejected by FORM; route such work through `python3 - <<'PY'` or a scratch
   script under `.remedy-wt/`, set variables in-process with `os.environ[...]`,
   and copy with `shutil.copyfile`. Capture real exit codes with
   `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess` — the tool does
   not surface a non-zero exit on its own. Report every re-expression.
7. THE GUARDS THAT SWEEP EVERY NEW `packages/orchestration/*.py`, measured by
   the reviewer at `41505dea`:
   `tests/test_data_paths.py::TestSingleReaderInvariant` forbids the literal
   `os.environ.get("REMEDY_DATA_DIR")` in any file under `packages/` but
   `data_paths.py`;
   `tests/test_path_utils.py::TestSingleImplementationInvariant` forbids the
   regex `[^a-zA-Z0-9_-]` and the name `_MAX_PATH_COMPONENT_LENGTH` outside
   `path_utils.py`;
   `tests/regression/test_named_bugs.py::TestNoSilentSwallow` forbids a bare
   `except: pass`; and
   `tests/ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs`
   forbids a product module referencing `.agent/live_review.md`. The new module
   contains none of those.
8. THE APPEND CONVENTION, and it governs every append this round. Each appended
   slice is separated from the text that precedes it by exactly ONE BLANK LINE,
   and the file ends with exactly one trailing newline: for a file whose last
   byte is already a newline, the bytes written are one newline, then the slice,
   then one newline. This constraint, not any arithmetic sentence in a gate
   below, is the authority on separators; if a gate's formula and this
   constraint disagree, follow this constraint and declare the disagreement.
9. THE OPEN SET IS COUNTED BY DISTINCT ID, never by line. A finding legitimately
   carries more than one `Done:` paragraph — a resolution in part followed by
   its remainder — and `R-0721` and `R-0725` each do, measured at `41505dea`.
   So the open set is `len(set(registered ids) - set(resolved ids))`, which is
   251 there, and NOT the difference of the two line counts, which is 249.

### SPEC — the production code of C3

Production code is DESCRIBED here, not sliced: write it in this repository's
idiom, with the one-line WHY comment above each definition that AGENTS.md's
discoverability conventions ask for, and a module docstring carrying "Public
API" and "Deliberate absences" sections the way
`packages/orchestration/self_use_queue.py` does at `41505dea`.

S1. New module `packages/orchestration/self_use_job.py`. It imports
`SelfUseQueueEntry` and `next_self_use_item` from
`packages.orchestration.self_use_queue`, and `plan_job_from_file` from
`packages.orchestration.pingpong_job`. It adds NO writer to the queue.

S2. Export `SelfUseJobError(RuntimeError)` for the one failure this module owns:
being asked to render or plan when the queue has no pending item.

S3. Export `write_self_use_job_file(entry: SelfUseQueueEntry, dest_dir: Path) -> Path`.
It writes `entry.job_markdown` verbatim, UTF-8, to `dest_dir / f"{entry.id}.md"`,
creating `dest_dir` if absent, and returns that path. The destination is the
CALLER'S, never derived here: this module resolves no data root, which is what
keeps `tests/test_data_paths.py::TestSingleReaderInvariant` satisfied and the
function testable against `tmp_path`.

S4. THE RENDERED BYTES ARE THE CURATED BYTES. `write_self_use_job_file` performs
no templating, no substitution and no reformatting — the file's text equals
`entry.job_markdown` exactly. State the reason in the WHY comment: the queue
stores job-file TEXT precisely so the thing that runs is the thing an operator
curated and reviewed, and a renderer that edits it on the way out would make the
reviewed text and the executed text two different artifacts.

S5. Export `plan_self_use_item(entry: SelfUseQueueEntry, dest_dir: Path, repo_path: str = ".") -> tuple[Path, object]`.
It calls `write_self_use_job_file`, then `plan_job_from_file(str(path), repo_path)`,
and returns the path and the resulting `JobPlan`. It does NOT run the job:
planning is the read-only half, and running belongs to `do job-run` behind the
normal approval gate.

S6. Export `plan_next_self_use_item(dest_dir: Path, repo_path: str = ".", queue_path: Path | None = None) -> tuple[SelfUseQueueEntry, Path, object]`.
It takes the queue's next pending item via `next_self_use_item(queue_path)`, and
raises `SelfUseJobError` naming the queue path when that answers `None` —
because "the track is exhausted" is a state a caller must handle deliberately,
not a `None` that flows onward and fails later somewhere less obvious.

S7. DELIBERATE ABSENCES, recorded in the docstring where a reader will search
for them. This module deliberately does not RUN a job, does not promote one, and
does not mark a queue item consumed: consumption is the closure round's edit
under DECISION F257 D2, and promotion stays behind the `--approve` barrier in
`packages/orchestration/job_promote.py`.

S8. New file `tests/orchestration/test_self_use_job.py`, named after the module
it covers, pinning each of these as its own test: `write_self_use_job_file`
writes bytes EQUAL to `entry.job_markdown` and returns the `<id>.md` path;
it creates a missing `dest_dir`; `plan_self_use_item` returns a `JobPlan` whose
`job_title` is the H1's text with the `Job:` prefix stripped and whose `tasks`
are non-empty, with `error` empty — measured at `41505dea`, the SHIPPED item
`SU-001` plans to `job_title` `Document the Markdown job-file format`, exactly
one task, task id `T001`, and a non-empty `acceptance`; `plan_next_self_use_item`
returns the shipped pending item against the real queue; and it RAISES
`SelfUseJobError`, rather than returning `None` or an empty result, for a
fixture queue whose every item carries a non-empty `consumed_by`. Use `tmp_path`
for every destination directory so no test writes outside its own sandbox.

### The authored slices

<<<SLICE PLANF257R3
# Plan — F257 Self-use track

Branch: feature/f257-self-use-track, cut from `main` at the merge commit of pull
request #220. F257 was claimed by Rule A5 as the first unchecked line in
`docs/roadmap/STATUS.md` after F256.

## Goal
Remedy is used on Remedy on a schedule that cannot be skipped: a curated queue
of small maintenance jobs, exactly one consumed per feature close, run through
`do job-plan` and `do job-run` against this repository and taken to the normal
approval gate.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| claim F257 and retarget the state | done | round 1 |
| rule the queue format and the consumption point | done | DECISIONS F257 D1 and D2 |
| the queue file and its read-only loader | done | round 2, 18 tests |
| render a queue item and plan it on the real job path | done | this round |
| consume exactly one item per feature close | open | the closure-protocol edit |
| document the format where a reader looks | open | acceptance item 1 |

## Next Steps
1. Wire the consumption point into `docs/roadmap/STATUS_closure_protocol.md`, so
   exactly one item is consumed per feature close and the track cannot rot.
2. Document the queue format and the job-file format where a reader would look,
   and register the page in `docs/README.md`.
3. Run the integration gate and build the closure package.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
<<<END PLANF257R3

<<<SLICE GATEF257R2
Gate: F257 R2 — the QUEUE round, which shipped the curated queue, its read-only loader and eighteen tests, and booked the round 1 verdict. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran each one independently at `41505dea`.

THE LOADER WAS EXECUTED, NOT READ. The reviewer imported the shipped module and called it: `load_self_use_queue()` answers one entry `SU-001` with `is_pending` True, and the file's bytes are IDENTICAL before and after `load_self_use_queue`, `next_self_use_item` and `pending_self_use_items` together, which is the read-only property DECISION F257 D2 turns on. The module exports no writer — its public callables are `SelfUseQueueEntry`, `SelfUseQueueError`, `default_self_use_queue_path`, `load_self_use_queue`, `next_self_use_item` and `pending_self_use_items` — so a job cannot mark its own item consumed, for the reason `docs/roadmap/STATUS.md` sits in `scope_fences.BUILTIN_DENY`.

THE LOAD-BEARING INVARIANT HOLDS ON THE REAL PARSER. `SU-001`'s `job_markdown` was passed to `packages.orchestration.pingpong_job.parse_job_file`, which returned a `JobPlan` at status `planned` with an empty `error`, `job_title` `Document the Markdown job-file format` — the `Job:` prefix stripped as that parser does — and exactly one task `T001` carrying a 251-character acceptance. The queue therefore holds text the existing job path really accepts, rather than a second format that would have to be kept in step.

THE RED-PROOF WAS RE-RUN BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE, control first: 18 passed at REAL exit 0 unmutated; returning an empty tuple instead of raising on a missing file gave exit 1 at 2 failed; answering the first item regardless of `consumed_by` gave exit 1 at 2 failed; the module was restored byte-clean and the control returned to 18 passed at exit 0. The worktree was removed and the primary checkout reads `git status --porcelain` empty with `git ls-files .remedy-wt` at 0. Twelve suites re-ran green in the primary, including all four repo-wide guards a new `packages/orchestration/` module attracts.

THE ONE FLAGGED NUMBER IS THE BLOCK'S FAULT AND THE WORKER WAS RIGHT TO FLAG IT. G5 ordered the open set as "the registrations minus the resolutions", and the worker reported 249 where the round 1 handback's prose said 251. Both readings are UNMOVED across the round, which is what the gate protects, but 251 is the correct figure: `R-0721` and `R-0725` each carry TWO `Done:` paragraphs — a resolution in part at F037 R12 and R18, its remainder at R14 and R19 — so the record holds 44 `Done:` lines against 42 distinct ids, and a line-count subtraction under-reports the open set by exactly two. The open set is counted by DISTINCT ID from here, which the next block states as a constraint. Nothing on disk is wrong, so this spends no id.
<<<END GATEF257R2

<<<SLICE SLIPSF257R2
2026-08-28 · F257 R2 · The block's G5 ordered the open set as "the registrations minus the resolutions" without saying whether resolutions are counted by line or by distinct id; the two differ by two because `R-0721` and `R-0725` each carry a partial and a remainder `Done:` paragraph, so the worker honestly reported 249 where the correct figure is 251.
<<<END SLIPSF257R2

`PLANF257R3` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF257R2` is an
APPEND to `.agent/live_review.md` and `SLIPSF257R2` an APPEND to
`.agent/prose_slips.md`, each under constraint 8. This round mints no finding id
and resolves none.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C3; report both answers. If it exists at either reading, finish the
commit in hand, write the handback and stop. Report constraint 0's three
readings and `git status --porcelain | wc -l` after each of C0a, C0b, C1, C2
and C3.

G2 TRANSPORT. One digest comparison. Report sha256 and the byte length of the
committed blob `git show <C0a>:.agent/authored/f257-r3.md` and of the reviewer's
own original at `.remedy-wt/f257-r3-block.md`, and whether they are EQUAL. That
original was written before this worker existed, so the reading covers more than
self-consistency; it covers no emission, because this workflow has none — say
both in the handback. Then report that
`git rev-parse <C0b>:.agent/authored/f257-r3.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF257R3 including the
trailing newline — report `True` or `False`. Report `wc -l`, under 50, and the
count of lines exactly `## Goal` and exactly `## Next Steps`.

G4 THE RECORD APPEND AT C2, two readers, over `.agent/live_review.md`. (a)
Reconstruct the C2 blob from the `41505dea` blob and GATEF257R2 under constraint
8 and report `True` or `False`. NEGATIVE CONTROL: flip one byte at an offset
your script confirms lies INSIDE THE FIRST appended paragraph, recompute, and
report the equality is now `False`. (b) Split the C2 blob on blank lines; let N
be the number of paragraphs GATEF257R2 holds, COUNTED BY YOUR SCRIPT from the
slice and never taken from this block; report N and that the LAST N units match
those paragraphs IN ORDER. Report that the pre-round blob is a byte PREFIX, with
both lengths. Report separately that `.agent/prose_slips.md` at C2 reconstructs
from its `41505dea` blob and SLIPSF257R2 under constraint 8.

G5 THE LEDGER AT C2, counted under constraint 9. Report over
`.agent/live_review.md` at `41505dea` and again at C2: the count of lines
matching `^- R-\d+ — ` and whether all are DISTINCT; the count of
`^Done: R-\d+ — ` lines AND the count of DISTINCT ids among them, as two
separate numbers; the count of `^Landed: R-`; the count of
`^Gate: F\d+ R\d+ — `; and the OPEN SET as
`len(set(registered) - set(resolved))`. Everything but the `Gate:` count must be
UNMOVED, the open set must read 251 at both, and the `Gate:` count must rise by
exactly one. Report the count of `^Gate: F257 R2 — ` at C2, which must be 1.

G6 THE RED-PROOF AT C3, in a disposable worktree added at C3 under
`.remedy-wt/`, never in the primary checkout. Report the UNMUTATED CONTROL
FIRST, in that worktree — a colour with no baseline is not evidence — running
`python3 -m pytest tests/orchestration/test_self_use_job.py -q` with its REAL
exit code and passed count. THE MUTATIONS, each applied alone and reverted
before the next, each in `packages/orchestration/self_use_job.py` inside the
worktree, and each of which must turn that file RED: (i) break S4 by making
`write_self_use_job_file` append a trailing line to the rendered text instead of
writing `entry.job_markdown` verbatim; (ii) break S6 by making
`plan_next_self_use_item` return `None` instead of raising when the queue has no
pending item. Report the exit code and the passed/failed counts for every run,
then the control again, green, with the module restored byte-clean, and report
`git worktree list` and `git status --porcelain | wc -l` in the primary after
removal.

G7 THE SUITES AT C3. One pytest process at a time, from the repository root, in
the PRIMARY checkout, each with its REAL exit code and its own passed/failed
line: `tests/orchestration/test_self_use_job.py`;
`tests/orchestration/test_self_use_queue.py`; the guards constraint 7 names,
`tests/test_data_paths.py`, `tests/test_path_utils.py`,
`tests/regression/test_named_bugs.py` and
`tests/orchestration/test_development_artifact_boundary.py`; the job-path
neighbours `tests/orchestration/test_job_promote.py`,
`tests/orchestration/test_fences.py` and
`tests/orchestration/test_pingpong_cli.py`; the state readers
`tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
`tests/regression/test_resource_safety.py` and
`tests/orchestration/test_integrity_gate.py`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. If any is red, STOP
and write the handback with the full untruncated failure list.

G8 STRUCTURE, over `41505dea..<C3>` — the range that ends BEFORE the handback
commit, because C4's own numbers cannot exist while C4 is being written. The
change set above lists `.agent/handoff.md`, which C4 writes, so compute the
changeset-minus-range residue over the change set WITHOUT that path and name the
path you excluded; the range-minus-changeset residue is computed against the
full change set and must be empty. Report each commit's insertions from
`git diff --numstat`, each under 500, and that each of C0a, C0b, C1, C2 and C3
is single-parent. Report, counted affirmatively over each file's C3 content, the
number of lines beginning `<<<SLICE ` and `<<<END ` in `.agent/plan.md`,
`.agent/live_review.md`, `.agent/prose_slips.md`,
`packages/orchestration/self_use_job.py` and
`tests/orchestration/test_self_use_job.py` — each expected 0 — beside the same
counts over `.agent/authored/f257-r3.md` as the non-zero control. Report
`git ls-files .remedy-wt | wc -l`, expected 0. Report the `git diff --numstat`
line for `packages/orchestration/self_use_queue.py` and
`scripts/self_use_queue.json` over the range, both expected ABSENT.

### Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md. It
carries: `SESSION 1 of feature F257 · round 3`; the range `41505dea..HEAD`; a
per-commit changed-files table whose `+/-` cells are taken from
`git diff --numstat` and compared cell by cell against the figures G8 reports;
ONE LINE PER GATE G1 through G8 with its real result; the deviations, including
every guard re-expression constraint 6 required; the item-status table with
every C-item and every gate appearing exactly once; and the next expected
action.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — GATEF257R2 is
reviewer-authored text you apply verbatim, and any OTHER such paragraph is a
finding however hedged.

After C4: push with `git push origin feature/f257-self-use-track` and report the
outcome. Do NOT create a pull request and do NOT merge anything.
