### STEP T002 — F257 Self-use track, round 4 (THE CONSUMPTION POINT)

Goal: book the round 3 verdict and its two findings, close the path-escape gap
R-0733 names in the module that is about to gain callers, and WIRE THE
CONSUMPTION POINT into `docs/roadmap/STATUS_closure_protocol.md` so exactly one
self-use item is consumed per feature close and the track cannot rot.

Base: `a12ba4ed`, the tip of `feature/f257-self-use-track` and the handback this
round starts from. Every reading stated below was taken there by the reviewer.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f257-r4.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 book the F257 R3 verdict AND register R-0733 and R-0734 into
  `.agent/live_review.md`, and append one reviewer-prose slip to
  `.agent/prose_slips.md`
- C3 the R-0733 containment fix in `packages/orchestration/self_use_job.py` and
  its tests
- C4 the closure-protocol wiring in `docs/roadmap/STATUS_closure_protocol.md`
- C5 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f257-r4.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/prose_slips.md`
- `packages/orchestration/self_use_job.py`
- `tests/orchestration/test_self_use_job.py`
- `docs/roadmap/STATUS_closure_protocol.md`
- `.agent/handoff.md`

`packages/orchestration/self_use_queue.py` and `scripts/self_use_queue.json` are
NOT edited: the loader stays read-only and no item is consumed by this round.
`tests/ui_server/test_command_channel.py` is NOT edited either — R-0734 is
REGISTERED here and repaired elsewhere, see the note under the finding slice.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — it was `[]` when this block was written, and if it is not `[]` now, STOP and
   hand back without committing. Report `git rev-parse HEAD`, which must equal
   `a12ba4ed6df6d0f842e5bb0958fb72cfc611f52a`, and `git branch --show-current`,
   which must be `feature/f257-self-use-track`. Create no branch and no pull
   request. Never force-push and never rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations; the record is repaired by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f257-r4.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under
   the gitignored `.remedy-wt/`. The primary checkout satisfies
   `git status --porcelain` empty at every commit.
6. Shell forms rejected by this session's guard are RE-EXPRESSED, never skipped
   and never weakened. Loops, `$( )`, `${arr[0]}`, `cp`, brace literals
   containing quotes, and every form of environment-variable assignment are
   rejected by FORM; route such work through a scratch script under
   `.remedy-wt/`, set variables in-process with `os.environ[...]`, and copy with
   `shutil.copyfile`. Capture real exit codes with
   `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess` — the tool does
   not surface a non-zero exit on its own. Report every re-expression.
7. THE GUARDS THAT SWEEP EVERY `packages/orchestration/*.py`, measured by the
   reviewer at `a12ba4ed`:
   `tests/test_data_paths.py::TestSingleReaderInvariant` forbids the literal
   `os.environ.get("REMEDY_DATA_DIR")` in any file under `packages/` but
   `data_paths.py`;
   `tests/test_path_utils.py::TestSingleImplementationInvariant` forbids the
   regex `[^a-zA-Z0-9_-]` and the name `_MAX_PATH_COMPONENT_LENGTH` outside
   `path_utils.py` — THIS ONE BINDS C3 DIRECTLY, so the fix below is stated as a
   containment check on RESOLVED PATHS and never as a character-class regex;
   `tests/regression/test_named_bugs.py::TestNoSilentSwallow` forbids a bare
   `except: pass`; and
   `tests/ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs`
   forbids a product module referencing `.agent/live_review.md`.
8. THE APPEND CONVENTION, and it governs every append this round. Each appended
   slice is separated from the text that precedes it by exactly ONE BLANK LINE,
   and the file ends with exactly one trailing newline: for a file whose last
   byte is already a newline, the bytes written are one newline, then the slice,
   then one newline. This constraint, not any arithmetic sentence in a gate
   below, is the authority on separators; if a gate's formula and this
   constraint disagree, follow this constraint and declare the disagreement.
9. THE OPEN SET IS COUNTED BY DISTINCT ID, never by line, as
   `len(set(registered ids) - set(resolved ids))`. It reads 251 at `a12ba4ed`,
   and this round REGISTERS TWO ids and resolves none, so it must read 253 at C2.
10. A PAIR IS APPLIED BY EXACT MATCH. Each FROM block below occurs EXACTLY ONCE
   in its target file at `a12ba4ed` — verify that count is 1 before replacing,
   and if it is not 1, STOP and hand back. Replace the FROM bytes with the TO
   bytes and change nothing else in the file.

### SPEC — the production code of C3, closing R-0733

Production code is DESCRIBED here, not sliced: write it in this repository's
idiom, with the one-line WHY comment above each definition that AGENTS.md's
discoverability conventions ask for.

S1. `write_self_use_job_file` in `packages/orchestration/self_use_job.py` MUST
REFUSE to write outside `dest_dir`. Today it interpolates `entry.id` straight
into a file name, and the reviewer ran it at `a12ba4ed` with an entry whose `id`
was `../../escaped`: it wrote to `<dest_dir>/../../escaped.md`, a path that
resolves OUTSIDE `dest_dir`. Add a containment check and raise
`SelfUseJobError` naming the offending id when it fails.

S2. THE CHECK IS ON RESOLVED PATHS, NOT ON THE CHARACTERS OF THE ID. After
computing the candidate path, require that its resolved PARENT equals the
resolved `dest_dir`. Express it with `Path.resolve()` on both sides and a plain
equality. Do NOT add a character-class regex and do NOT introduce a length
constant: constraint 7's `TestSingleImplementationInvariant` reserves both to
`packages/orchestration/path_utils.py`, and a resolved-parent comparison is the
stronger check anyway — it also catches an absolute id and a symlinked escape,
which a character filter would not.

S3. REFUSE, DO NOT SANITISE. Do not rewrite the id into a safe one. The
function's contract is that the file is named `<id>.md`, and a sanitiser would
quietly make the written name differ from the id the caller asked for — the
same class of silent divergence S4 of round 3 exists to prevent. Raising is
also what this module already does for its one other failure. State that reason
in the WHY comment.

S4. WHY THIS IS WORTH A GUARD WHEN THE LOADER ALREADY VALIDATES. Say it in the
comment, because the next reader will ask: `load_self_use_queue` refuses any id
but `^SU-\d{3}$`, so the SHIPPED path cannot reach this — but
`write_self_use_job_file` and `plan_self_use_item` are PUBLIC exports that take
a caller-built `SelfUseQueueEntry`, and that dataclass validates nothing. The
guard is what makes the public function safe on its own terms rather than only
as far as its current callers behave.

S5. `plan_self_use_item` and `plan_next_self_use_item` need no change: both
reach the file system only through `write_self_use_job_file`, so both inherit
the guard. Do not restate the check in either.

S6. Record the new refusal in the module docstring's existing `SelfUseJobError`
line so the Public API block stays true — it currently says the error means
only "asked to render or plan with no pending queue item", and after C3 it also
means "asked to write outside the destination directory".

S7. New tests in `tests/orchestration/test_self_use_job.py`, appended as their
own class, each its own test: an id of `../../escaped` raises `SelfUseJobError`;
an id that is an ABSOLUTE path raises it; the raised message names the offending
id; and NOTHING is written outside `dest_dir` when the refusal fires — assert
that by listing the parent of `dest_dir` before and after and comparing. Keep
every destination under `tmp_path`. Do not weaken or renumber the seven tests
already there; they must all still pass.

### The authored slices

<<<SLICE PLANF257R4
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
| render a queue item and plan it on the real job path | done | round 3, 7 tests |
| refuse a job file written outside its destination | done | this round, R-0733 |
| consume exactly one item per feature close | done | this round, precondition 6 |
| document the format where a reader looks | open | acceptance item 1 |

## Next Steps
1. Document the queue format and the job-file format where a reader would look,
   and register the page in `docs/README.md`.
2. Run the integration gate and build the closure package.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
- R-0734 is registered against `tests/ui_server/` and is deliberately NOT
  repaired on this branch; it is unrelated to F257's scope.
<<<END PLANF257R4

<<<SLICE GATEF257R3
Gate: F257 R3 — the JOB-PATH round, which shipped the renderer and the planner seam in a separate module, seven tests, and booked the round 2 verdict. THE ROUND PASSED. The reviewer re-ran every gate G1 through G8 independently at `a12ba4ed`, with its own scripts rather than the worker's, and every reading reproduced.

THE SHIPPED FUNCTIONS WERE EXECUTED, NOT READ. The reviewer called `plan_next_self_use_item` against the REAL shipped queue: it answered entry `SU-001`, wrote `SU-001.md`, and returned a `JobPlan` at status `planned` with an empty `error`, `job_title` `Document the Markdown job-file format`, and exactly one task `T001`. The rendered file's text equals `SU-001`'s `job_markdown` byte for byte at 1235 bytes, which is S4's whole claim. `scripts/self_use_queue.json` is byte-identical before and after two complete planning runs, so the read-only property DECISION F257 D2 turns on survives the job path and not merely the loader.

THE RED-PROOF REPRODUCED AND THEN SOME. In its own disposable worktree at `227246de`, control first: 7 passed at REAL exit 0 unmutated; appending a trailing line in the renderer gave exit 1 at 1 failed, 6 passed; returning `None` instead of raising on an exhausted queue gave exit 1 at 1 failed, 6 passed; and a THIRD mutation the block never ordered — naming the file `job.md` instead of `<id>.md` — gave exit 1 at 2 failed, 5 passed, so the suite pins the path contract as well as the two the block named. The module was restored byte-clean and the control returned to 7 passed at exit 0. The worktree was removed by exact path and the primary reads `git status --porcelain` empty with `git ls-files .remedy-wt` at 0.

THE FLAKE IN DEVIATION 3 DOES NOT BLOCK, AND THE WORKER WAS RIGHT TO REFUSE TO REPAIR IT. `tests/ui_server/` went red once on the worker's first pass at `test_wrong_bearer_is_403` and green on its re-run and at base. The reviewer re-ran all fourteen ordered suites serially, one pytest process at a time: ALL FOURTEEN EXIT 0, including `tests/ui_server/` at 497 passed. The round touches seven paths and none is under `apps/`, `packages/ui_server/` or `tests/ui_server/`, so the round cannot be the cause. The worker classified it, declared it untruncated and changed nothing to make it green, which is the required behaviour. The underlying race is real and was unregistered, so it is registered here as R-0734 rather than left to be rediscovered.

THE GATE ARITHMETIC ALL REPRODUCED. Transport: the committed authored blob and the reviewer's own original are EQUAL at sha256 `2863bad5…9b86d244`, 20399 bytes, and `.agent/last_block.md` shares one blob id with it. The plan at C1 is byte-equal to its slice including the trailing newline, at 34 lines. The record append reconstructs exactly, its negative control fails as it must, N is 5 paragraphs matching the last 5 units in order, and the pre-round blob is a byte prefix; the prose-slips append reconstructs too. The ledger is unmoved at 293 registered and 44 `Done:` lines over 42 distinct ids, the open set reads 251 at both revisions, and `Gate:` rises by exactly one. Both structural residues are empty, all five commits are single-parent and under 500 insertions, and the delimiter counts are 0 in all five targets beside a 3/3 control.
<<<END GATEF257R3

<<<SLICE FINDF257R4
- R-0733 — Low, A PUBLIC RENDERER WRITES OUTSIDE ITS DESTINATION DIRECTORY FOR AN ID IT DOES NOT VALIDATE. THE MEASUREMENT, taken by the reviewer at `a12ba4ed` by RUNNING the shipped function: `write_self_use_job_file` in `packages/orchestration/self_use_job.py` builds its destination as `dest_dir / f"{entry.id}.md"`, and called with an entry whose `id` is `../../escaped` it wrote to `<dest_dir>/../../escaped.md` — a path whose resolved parent is NOT `dest_dir`, confirmed True by the probe. WHY IT IS LOW AND NOT HIGHER: the shipped path cannot reach it, because `load_self_use_queue` refuses any id but `^SU-\d{3}$` at load time, and no caller in the repository constructs a `SelfUseQueueEntry` by hand — `git grep self_use_job` at `a12ba4ed` finds no importer outside the module's own tests. WHY IT IS STILL AN ID: `write_self_use_job_file` and `plan_self_use_item` are PUBLIC exports taking a caller-built entry, `SelfUseQueueEntry` is a frozen dataclass that validates nothing, and the module is one round away from gaining callers; a public function that escapes its stated destination is worth closing while it is four lines long. THE FAULT IS THE BLOCK AUTHOR'S, NOT THE WORKER'S: round 3's S3 ordered the destination as `dest_dir / f"{entry.id}.md"` in exactly those words and the worker implemented precisely that, so this spends no credit against the round, which PASSED. THE FIX is a containment check on RESOLVED paths — the candidate path's resolved parent must equal the resolved `dest_dir`, else raise `SelfUseJobError` naming the id — and never a character-class regex, which `tests/test_path_utils.py::TestSingleImplementationInvariant` reserves to `path_utils.py`. Resolved when that check is in the module, a test proves a traversal id raises rather than writes, and the seven existing tests still pass.

- R-0734 — Medium, A SERVER-START HELPER TREATS FILE EXISTENCE AS FILE READABILITY AND MAKES A 497-TEST SUITE INTERMITTENTLY RED. THE MEASUREMENT: `tests/ui_server/test_command_channel.py`, the `_start_server` helper, polls `if Path(info_file).exists()` and then immediately calls `json.loads(Path(info_file).read_text())` INSIDE that branch. The server thread creates the info file before it finishes writing it, so a poll that lands in that window reads zero bytes and `json.loads("")` raises `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` — which escapes the retry loop instead of being retried, so the fifty-attempt budget never gets its second chance. Observed at F257 R3 as `TestCommandChannelDoor::test_wrong_bearer_is_403`, `1 failed, 496 passed`, REAL exit 1, with the untruncated traceback in that round's handback; the suite was green on re-run, green at base `41505dea`, and green on the reviewer's own independent re-run at 497 passed, and the failing node alone ran 10/10 green. THIS IS THE R-0708 SERVER-START-BUDGET FAMILY and it is unregistered — a grep of the record for `info_file` and for `JSONDecodeError` at `a12ba4ed` returns nothing. WHY MEDIUM: nothing in the product is wrong, but every round's G7 runs this suite, and a gate that reddens for a reason unrelated to the change under review costs a round to classify each time it fires — which is exactly what it cost F257 R3. THE FIX is to treat "exists but not yet parseable" as "not started yet": parse inside the loop under `try`, catch the decode error and an empty read, and keep polling until the budget is spent, failing with `pytest.fail` only when it is. NOT REPAIRED ON THIS BRANCH: `tests/ui_server/` is outside F257's scope and AGENTS.md forbids mixing an unrelated fix into a feature branch. Resolved when the helper retries a partial read on a branch of its own.
<<<END FINDF257R4

<<<SLICE SLIPSF257R3
2026-08-29 · F257 R3 · The handback's G3 reported `.agent/plan.md` at C1 as 1591 bytes where the blob is 1593, and its G4 gave the first appended paragraph's span as 1378358..1378622 where the reviewer's script measures 1378358..1378625; both equality claims the two numbers decorate are correct and reproduced, so nothing on disk is wrong.
<<<END SLIPSF257R3

`PLANF257R4` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF257R3` and
`FINDF257R4` are TWO SEPARATE APPENDS to `.agent/live_review.md`, in that order,
each under constraint 8 — append `GATEF257R3` first, then `FINDF257R4`.
`SLIPSF257R3` is an APPEND to `.agent/prose_slips.md` under constraint 8. This
round registers R-0733 and R-0734 and resolves neither.

### The authored pairs for C4 — `docs/roadmap/STATUS_closure_protocol.md`

PAIR A — the new precondition. FROM (occurs exactly once):

<<<SLICE PAIRAFROM
5. Working tree clean, branch pushed, worker idle.
<<<END PAIRAFROM

TO:

<<<SLICE PAIRATO
5. Working tree clean, branch pushed, worker idle.
6. EXACTLY ONE SELF-USE ITEM IS CONSUMED BY THIS CLOSE (F257). The first
   pending item in `scripts/self_use_queue.json` — the one
   `packages.orchestration.self_use_queue.next_self_use_item` answers — has
   been planned through `packages.orchestration.self_use_job`, taken to the
   normal approval gate like any other job, and its `consumed_by` set to this
   feature's id in the closure commit. If the queue holds NO pending item the
   track is exhausted, not blocked: record `self-use NONE (queue exhausted)`
   in the handback and close normally, because an empty queue asks the
   operator to curate more rather than stopping a feature. Why this is a
   precondition and not an intention: "Remedy is used on Remedy" rots the
   moment it depends on someone remembering to do it, which is DECISION F257
   D2's CONSEQUENCE clause in as many words.
<<<END PAIRATO

PAIR B — the closure commit's path set. FROM (occurs exactly once):

<<<SLICE PAIRBFROM
   docs/roadmap/STATUS.md, README.md and the final .agent/ state
   (incl. handoff.md rewrite) — nothing else; the feature file's Built
   State is already current from an earlier commit (precondition 4).
<<<END PAIRBFROM

TO:

<<<SLICE PAIRBTO
   docs/roadmap/STATUS.md, README.md, scripts/self_use_queue.json (the one
   `consumed_by` edit precondition 6 requires) and the final .agent/ state
   (incl. handoff.md rewrite) — nothing else; the feature file's Built
   State is already current from an earlier commit (precondition 4).
<<<END PAIRBTO

Both pairs are applied to `docs/roadmap/STATUS_closure_protocol.md` in C4 and
nothing else in that file changes. No test reads this file's CONTENT — the
reviewer measured that at `a12ba4ed` with `git grep -l STATUS_closure_protocol`
over `tests/`, `packages/`, `scripts/`, `apps/` and `docs/README.md`, which
matched `docs/README.md` alone — so the file is already registered in the docs
index and C4 adds no index entry.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C3; report both answers. If it exists at either reading, finish the
commit in hand, write the handback and stop. Report constraint 0's three
readings and `git status --porcelain | wc -l` after each of C0a, C0b, C1, C2, C3
and C4.

G2 TRANSPORT. One digest comparison. Report sha256 and the byte length of the
committed blob `git show <C0a>:.agent/authored/f257-r4.md` and of the reviewer's
own original at `.remedy-wt/f257-r4-block.md`, and whether they are EQUAL. That
original was written before this worker existed, so the reading covers more than
self-consistency; it covers no emission, because this workflow has none — say
both in the handback. Then report that
`git rev-parse <C0b>:.agent/authored/f257-r4.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF257R4 including the
trailing newline — report `True` or `False`, with the byte length of each side.
Report `wc -l`, under 50, and the count of lines exactly `## Goal` and exactly
`## Next Steps`.

G4 THE RECORD APPENDS AT C2, over `.agent/live_review.md`. Reconstruct the C2
blob from the `a12ba4ed` blob plus GATEF257R3 plus FINDF257R4, applied IN THAT
ORDER each under constraint 8, and report `True` or `False` with all three
lengths. NEGATIVE CONTROL: flip one byte at an offset your script confirms lies
INSIDE the FIRST appended paragraph, recompute, and report the equality is now
`False`. Report that the pre-round blob is a byte PREFIX of the C2 blob, with
both lengths, and that the C2 blob ends in exactly ONE newline. Report
separately that `.agent/prose_slips.md` at C2 reconstructs from its `a12ba4ed`
blob plus SLIPSF257R3 under constraint 8.

G5 THE LEDGER AT C2, counted under constraint 9. Report over
`.agent/live_review.md` at `a12ba4ed` and again at C2: the count of lines
matching `^- R-\d+ — ` and whether all are DISTINCT; the count of
`^Done: R-\d+ — ` lines AND the count of DISTINCT ids among them, as two
separate numbers; the count of `^Landed: R-`; the count of
`^Gate: F\d+ R\d+ — `; and the OPEN SET as
`len(set(registered) - set(resolved))`. Expected: registered 293 → 295, the
`Done:` numbers and `Landed:` UNMOVED, `Gate:` 108 → 109, and the open set
251 → 253. Report the count of `^Gate: F257 R3 — ` at C2, which must be 1, and
the count of lines matching `^- R-0733 — ` and `^- R-0734 — `, each of which
must be 1.

G6 THE RED-PROOF AT C3, in a disposable worktree added at C3 under
`.remedy-wt/`, never in the primary checkout. Report the UNMUTATED CONTROL
FIRST, in that worktree — a colour with no baseline is not evidence — running
`python3 -B -m pytest tests/orchestration/test_self_use_job.py -q -p no:cacheprovider`
with its REAL exit code and passed count, and purge `__pycache__` before every
run. THE MUTATIONS, each applied alone and reverted before the next, each in
`packages/orchestration/self_use_job.py` inside the worktree, and each of which
must turn that file RED: (i) DELETE the containment check S1 adds, leaving the
path built exactly as it was at `a12ba4ed`; (ii) break S4 of round 3 by making
`write_self_use_job_file` append a trailing line instead of writing
`entry.job_markdown` verbatim. Report the exit code and the passed/failed counts
for every run, then the control again, green, with the module restored
byte-clean and the byte equality against the pristine bytes reported as `True`.
Report `git worktree list` and `git status --porcelain | wc -l` in the primary
after removing the worktree BY EXACT PATH.

G7 THE SUITES AT C4. One pytest process at a time, from the repository root, in
the PRIMARY checkout, each with its REAL exit code and its own passed/failed
line. CONFIRM FIRST that every path below resolves on disk and report the empty
list, because `pytest <missing path>` exits 4 and says almost nothing:
`tests/orchestration/test_self_use_job.py`;
`tests/orchestration/test_self_use_queue.py`; the guards constraint 7 names,
`tests/test_data_paths.py`, `tests/test_path_utils.py`,
`tests/regression/test_named_bugs.py` and
`tests/orchestration/test_development_artifact_boundary.py`; the job-path
neighbours `tests/orchestration/test_job_promote.py` and
`tests/orchestration/test_pingpong_cli.py`; the docs guards
`tests/docs/test_docs_consistency.py`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. If any is red, STOP
and write the handback with the full untruncated failure list.

G8 STRUCTURE, over `a12ba4ed..<C4>` — the range that ends BEFORE the handback
commit, because C5's own numbers cannot exist while C5 is being written. The
change set above lists `.agent/handoff.md`, which C5 writes, so compute the
changeset-minus-range residue over the change set WITHOUT that path and name the
path you excluded; the range-minus-changeset residue is computed against the
full change set and must be empty. Report each commit's insertions from
`git diff --numstat`, each under 500, and that each of C0a, C0b, C1, C2, C3 and
C4 is single-parent. Report, counted affirmatively over each file's C4 content,
the number of lines beginning `<<<SLICE ` and `<<<END ` in `.agent/plan.md`,
`.agent/live_review.md`, `.agent/prose_slips.md`,
`packages/orchestration/self_use_job.py`,
`tests/orchestration/test_self_use_job.py` and
`docs/roadmap/STATUS_closure_protocol.md` — each expected 0 — beside the same
counts over `.agent/authored/f257-r4.md` as the non-zero control. Report
`git ls-files .remedy-wt | wc -l`, expected 0. Report the `git diff --numstat`
line for `packages/orchestration/self_use_queue.py`,
`scripts/self_use_queue.json` and `tests/ui_server/test_command_channel.py` over
the range, all three expected ABSENT. Finally report, over the C4 blob of
`docs/roadmap/STATUS_closure_protocol.md`, the count of lines exactly
`5. Working tree clean, branch pushed, worker idle.` which must be 1, the count
of lines beginning `6. EXACTLY ONE SELF-USE ITEM` which must be 1, and the count
of occurrences of `scripts/self_use_queue.json` which must be 2.

### Handback

Rewrite `.agent/handoff.md` in C5 per docs/agents/handback_template.md. It
carries: `SESSION 2 of feature F257 · round 4`; the range `a12ba4ed..HEAD`; a
per-commit changed-files table whose `+/-` cells are taken from
`git diff --numstat` and compared cell by cell against the figures G8 reports;
ONE LINE PER GATE G1 through G8 with its real result; the deviations, including
every guard re-expression constraint 6 required; the item-status table with
every C-item and every gate appearing exactly once; the open-findings count,
which must be 253; and the next expected action.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — GATEF257R3
and FINDF257R4 are reviewer-authored text you apply verbatim, and any OTHER such
paragraph is a finding however hedged.

After C5: push with `git push origin feature/f257-self-use-track` and report the
outcome. Do NOT create a pull request and do NOT merge anything.
