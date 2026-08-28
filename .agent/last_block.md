### STEP T002 — F257 Self-use track, round 5 (THE DOCUMENTED FORMAT)

Goal: book the round 4 verdict, close R-0735 — the guard the reviewer's own
mutation pass proved unpinned — and DOCUMENT the queue format, the job-file
format and the consumption rule where a reader will look, registered in the docs
index. This clears the last open acceptance item before the integration gate.

Base: `f594cf3b`, the tip of `feature/f257-self-use-track` and the handback this
round starts from. Every reading stated below was taken there by the reviewer.

Bundle, in commit order:

- C0a save this block verbatim to `.agent/authored/f257-r5.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1 advance `.agent/plan.md`
- C2 book the F257 R4 verdict AND register R-0735 into `.agent/live_review.md`,
  and append two reviewer-prose slips to `.agent/prose_slips.md`
- C3 the R-0735 single-component fix in `packages/orchestration/self_use_job.py`
  and its tests
- C4 the documentation page and its two index registrations
- C5 rewrite `.agent/handoff.md`

Change set — these paths and nothing else:

- `.agent/authored/f257-r5.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `.agent/prose_slips.md`
- `packages/orchestration/self_use_job.py`
- `tests/orchestration/test_self_use_job.py`
- `docs/system/self-use-track-v1.md`
- `docs/README.md`
- `.agent/handoff.md`

`packages/orchestration/self_use_queue.py`, `scripts/self_use_queue.json` and
`docs/roadmap/STATUS_closure_protocol.md` are NOT edited: the loader stays
read-only, no item is consumed by this round, and round 4 already wired the
consumption point. `tests/ui_server/test_command_channel.py` is NOT edited —
R-0734 stays registered and unrepaired on this branch, for the scope reason its
own entry states.

### Constraints

0. BEFORE ANYTHING: report `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
   — it was `[]` when this block was written, and if it is not `[]` now, STOP and
   hand back without committing. Report `git rev-parse HEAD`, which must equal
   `f594cf3b`'s full sha, and `git branch --show-current`, which must be
   `feature/f257-self-use-track`. Create no branch and no pull request. Never
   force-push and never rewrite history.
1. Apply every authored slice BYTE FOR BYTE — no reflow, rewording, retitling,
   correction or shortening. If a slice looks wrong, apply it as written and say
   so in the handback's deviations; the record is repaired by a later append.
2. The delimiter lines `<<<SLICE …` and `<<<END …` are transport only and never
   reach a target file.
3. Extract every slice from the COMMITTED blob with
   `git show <C0a>:.agent/authored/f257-r5.md`, never from this prompt's text.
4. AGENTS.md binds in full: the self-review loop before every commit, one
   logical step per commit, `.agent/plan.md` current before every commit, a
   clean tree, and the push.
5. Destructive verification runs ONLY inside a disposable `git worktree` under
   the gitignored `.remedy-wt/`, removed BY EXACT PATH. The primary checkout
   satisfies `git status --porcelain` empty at every commit.
6. Shell forms rejected by this session's guard are RE-EXPRESSED, never skipped
   and never weakened. Loops, `$( )`, `${arr[0]}`, `cp`, brace literals
   containing quotes, and every form of environment-variable assignment are
   rejected by FORM; route such work through a scratch script under
   `.remedy-wt/`, set variables in-process with `os.environ[...]`, and copy with
   `shutil.copyfile`. Capture real exit codes with
   `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess`. Note also that
   this Python is 3.10: an f-string expression may not contain a backslash, so
   hoist any regex out of an f-string into a named variable. Report every
   re-expression.
7. THE GUARDS THAT SWEEP EVERY `packages/orchestration/*.py`, measured by the
   reviewer at `f594cf3b`:
   `tests/test_data_paths.py::TestSingleReaderInvariant` forbids the literal
   `os.environ.get("REMEDY_DATA_DIR")` in any file under `packages/` but
   `data_paths.py`;
   `tests/test_path_utils.py::TestSingleImplementationInvariant` forbids the
   regex `[^a-zA-Z0-9_-]` and the name `_MAX_PATH_COMPONENT_LENGTH` outside
   `path_utils.py` — THIS ONE BINDS C3, so the fix below is stated as a
   path-component comparison and never as a character-class regex;
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
9. THE OPEN SET IS COUNTED BY DISTINCT ID, as
   `len(set(registered ids) - set(resolved ids))`. It reads 253 at `f594cf3b`,
   and this round REGISTERS ONE id and resolves none, so it must read 254 at C2.
10. A PAIR IS APPLIED BY EXACT MATCH. Each FROM block below occurs EXACTLY ONCE
   in its target file at `f594cf3b` — verify that count is 1 before replacing,
   and if it is not 1, STOP and hand back. Replace the FROM bytes with the TO
   bytes and change nothing else in the file.
11. `docs/system/self-use-track-v1.md` is a NEW file created whole from the
   DOCPAGE slice; it did not exist at `f594cf3b`. It is created in the SAME
   commit as the two `docs/README.md` registrations, because
   `tests/docs/test_docs_consistency.py::TestPrimaryDocLinksResolve` checks that
   every relative link in `docs/README.md` resolves, and a registration
   committed without its target would be red in that committed state.

### SPEC — the production code of C3, closing R-0735

Production code is DESCRIBED here, not sliced: write it in this repository's
idiom, with the one-line WHY comment above the definition.

S1. THE MEASURED DEFECT, so the fix is aimed at the real thing. At `f594cf3b`
`write_self_use_job_file` guards only `candidate.resolve().parent != dest_dir.resolve()`.
`Path.resolve()` NORMALISES `..` away, so an id of `x/../SU-001` passes the
guard — the resolved parent really is `dest_dir` — and then `write_text` fails
with a raw `FileNotFoundError` because `dest_dir/x` was never created. The
reviewer measured exactly that at `f594cf3b`. The module leaks a foreign
exception where it promises its own.

S2. THE FIX: REQUIRE THE ID TO BE A SINGLE PATH COMPONENT, checked BEFORE the
existing containment check. Require `Path(entry.id).name == entry.id`; when it
is not, raise `SelfUseJobError` naming the id. This one comparison refuses
`x/../SU-001`, `sub/dir`, `../../escaped`, an absolute id, and both `.` and `..`
— for `.` and `..` `Path(...).name` is the empty string, so they fail it too.
Do NOT add a character-class regex and do NOT introduce a length constant:
constraint 7 reserves both to `packages/orchestration/path_utils.py`.

S3. KEEP THE RESOLVED CONTAINMENT CHECK that is already there, after the new
one. It is the backstop for a destination reached through a symlink, which a
name comparison cannot see. Say in the WHY comment that the two checks answer
different questions — "is this id one file name?" and "does that file land
inside the caller's directory?" — so neither is redundant.

S4. THE TEST THAT DISCRIMINATES, and it is the point of this round. Add to
`tests/orchestration/test_self_use_job.py` a test that an id of `x/../SU-001`
raises `SelfUseJobError` — NOT `FileNotFoundError`, and assert the type
precisely, because the reviewer's mutation pass showed the eleven tests at
`f594cf3b` cannot tell the shipped guard from a materially different one.
Add tests that `.` and `..` are refused as well. Keep every destination under
`tmp_path`. Do not weaken or renumber the eleven tests already there; they must
all still pass.

S5. Update the `Raises:` line of `write_self_use_job_file`'s docstring so it
states both refusals, and leave the module docstring's Public API block correct.

### The authored slices

<<<SLICE PLANF257R5
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
| refuse a job file written outside its destination | done | round 4, R-0733 |
| consume exactly one item per feature close | done | round 4, precondition 6 |
| refuse an id that is not one file name | done | this round, R-0735 |
| document the format where a reader looks | done | this round |

## Next Steps
1. Run the integration gate — full suite, `pytest -n auto`, raw output — and
   build the closure package.
2. Close F257 through docs/roadmap/STATUS_closure_protocol.md, whose new
   precondition 6 this feature must itself satisfy.

## Risks
- A job must never mark its own queue item consumed; neither shipped module owns
  a queue writer, and DECISION F257 D2 rules the consumption point.
- `docs/roadmap/STATUS.md` is in `scope_fences.BUILTIN_DENY` and stays there.
- R-0734 is registered against `tests/ui_server/` and is deliberately NOT
  repaired on this branch; it is unrelated to F257's scope.
<<<END PLANF257R5

<<<SLICE GATEF257R4
Gate: F257 R4 — the CONSUMPTION-POINT round, which registered the round 3 findings, closed R-0733 and wired the self-use track into the closure protocol. THE ROUND PASSED. The reviewer re-ran every gate G1 through G8 independently at `f594cf3b` with its own scripts, and every reading reproduced: transport EQUAL at sha256 `c0e01bf7…fdb23ca0` over 27597 bytes with one blob id at C0b; the plan byte-equal at 1659 bytes and 35 lines; both record appends reconstructing to 1388216 bytes with the negative control failing as it must; the ledger moving 293 → 295 registered and 251 → 253 open with `Done:` and `Landed:` unmoved and `Gate:` 108 → 109; both structural residues empty; six single-parent commits all under 500 insertions; delimiters 0 in all six targets against an 8/8 control.

THE PAIRS TRANSPORTED PERFECTLY, AND THE PROOF IS STRONGER THAN A GATE. Before delegating, the reviewer applied both authored pairs to its own copy of `docs/roadmap/STATUS_closure_protocol.md` and kept the result. The C4 blob of that file is BYTE-IDENTICAL to that independently applied text. So the worker's two replacements are not merely well-formed, they are exactly the edit the block intended, with no reflow and no drift.

THE FIX WAS RUN, NOT READ. The reviewer called the shipped `write_self_use_job_file` with the exact input that produced R-0733 at `a12ba4ed`: an id of `../../escaped` now raises `SelfUseJobError` naming the id, nothing appears beside the destination directory, and a refused write creates no directory at all. Ids `../escaped`, an absolute `/tmp/absolute-escape` and `sub/dir` are refused too; a valid `SU-001` still writes into a destination that did not exist yet; and the shipped queue still plans end to end at `job_title` `Document the Markdown job-file format` with the queue file byte-unchanged after two full runs.

THE RED-PROOF REPRODUCED AND THEN EXPOSED A GAP. In its own worktree at `3c84e020`: control 11 passed at exit 0; deleting the containment guard gave exit 1 at 4 failed, 7 passed; breaking the verbatim-bytes rule gave exit 1 at 1 failed, 10 passed; and a fourth mutation refusing every id gave exit 1 at 6 failed, so the valid paths are pinned too. But a THIRD mutation — replacing the resolved comparison with an unresolved one — left the suite GREEN at 11 passed. That is a gate that cannot tell the shipped guard from a materially different one, and following it to a concrete consequence produced R-0735, registered below. All ten ordered suites re-ran green in the primary, `tests/docs/test_docs_consistency.py` at 295 passed among them.

THE WORKER'S THREE JUDGEMENT CALLS WERE ALL CORRECT AND ALL DECLARED. It changed S7's fourth test from `../../escaped` to `../escaped` because a listing of `dest_dir.parent` cannot observe a write two levels up and the assertion would have passed vacuously — that is the discriminator argument, made unprompted. It moved the containment check ahead of `mkdir` so a refusal creates nothing, declaring the reordering S1 did not order. And it applied two slices it believed wrong rather than correcting them, which is constraint 1 working as intended; both are booked as reviewer-prose slips, because both were the block author's error and neither touched anything on disk.
<<<END GATEF257R4

<<<SLICE FINDF257R5
- R-0735 — Low, A PATH GUARD NORMALISES AWAY THE CASE IT IS MEANT TO REFUSE, AND ELEVEN TESTS CANNOT SEE IT. THE MEASUREMENT, taken by the reviewer at `f594cf3b` by RUNNING the shipped function: `write_self_use_job_file` guards with `candidate.resolve().parent != dest_dir.resolve()`, and `Path.resolve()` normalises `..` segments away, so an id of `x/../SU-001` PASSES the guard — its resolved parent genuinely is `dest_dir` — and `write_text` then fails with `FileNotFoundError: [Errno 2] No such file or directory: '<dest_dir>/x/../SU-001.md'` because `<dest_dir>/x` was never created. The module promises `SelfUseJobError` for a destination it will not write and leaks a foreign exception instead. HOW IT WAS FOUND, and this is the part worth keeping: a reviewer mutation that replaced the resolved comparison with the unresolved `candidate.parent != dest_dir` left the suite GREEN at 11 passed, which says the tests pin the CONSEQUENCE of the guard but not the guard, and a formulation that differs in exactly the normalisation cases is invisible to them. WHY LOW: containment itself is NOT broken — the offending path resolves inside `dest_dir`, nothing escapes, and R-0733's contract holds; and the shipped path cannot reach it, because `load_self_use_queue` refuses any id but `^SU-\d{3}$` and no repository caller builds a `SelfUseQueueEntry` by hand. THE FAULT IS THE BLOCK AUTHOR'S AGAIN: round 4's S2 ordered the resolved-parent comparison in those words, and the worker implemented precisely that, so this spends no credit against round 4, which PASSED. THE FIX is to require the id to be ONE PATH COMPONENT — `Path(entry.id).name == entry.id`, which also refuses `.`, `..`, `sub/dir` and an absolute id — checked BEFORE the containment check, which stays as the symlink backstop. Resolved when that check is in the module and a test asserts `SelfUseJobError` PRECISELY, not merely that something raised, for an id of `x/../SU-001`.
<<<END FINDF257R5

<<<SLICE SLIPSF257R4
2026-08-29 · F257 R4 · The block's PLANF257R5 predecessor marked the consumption-point item `done` in the plan applied at C1, three commits before C4 made it true; the worker applied it verbatim under constraint 1 and declared it, which is the required behaviour.
2026-08-29 · F257 R4 · The block's FINDF257R4 called the R-0733 fix "four lines long" where the shipped guard is an `if` and a three-line `raise`; the estimate was written before the code existed and nothing on disk depended on it.
<<<END SLIPSF257R4

<<<SLICE DOCPAGE
# The self-use track (v1)

> **Status (2026-08-29):** built by F257. The queue, its loader, the job-path
> seam and the closure-protocol precondition are in place; consumption happens
> at feature close.

Remedy is used on Remedy on a schedule that cannot be skipped. This page is
where to look for the two file formats involved and for the rule that makes the
track run.

## Why it exists

"Dogfooding" rots the moment it depends on someone remembering to do it. The
self-use track replaces the intention with a mechanism: a curated queue of small
maintenance jobs, exactly ONE of which is consumed per feature close, planned
through the job path Remedy already has and taken to the normal approval gate.

## The queue file

`scripts/self_use_queue.json` — shipped, operator-curated INPUT, kept beside the
other shipped campaign data rather than under `docs/`, because a data file that
code reads is not a doc.

    {
      "schema_version": 1,
      "description": "<what this queue is for>",
      "items": [
        {
          "id": "SU-001",
          "title": "<one line>",
          "why": "<why this job is worth a feature close>",
          "job_markdown": "# Job: ...\n\n## Task 1\n...\n\nAcceptance:\n- ...\n",
          "consumed_by": ""
        }
      ]
    }

Rules the loader enforces, every one of them a refusal rather than a guess:

| Rule | Detail |
|------|--------|
| `schema_version` | must equal 1; a file from the future is refused, not half-read |
| item keys | exactly the five above — no more, no fewer |
| `id` | must match `^SU-\d{3}$`, and must be unique across the file |
| `title`, `why`, `job_markdown` | non-empty strings |
| `consumed_by` | a string; empty means the item is still PENDING |

An item is PENDING while `consumed_by` is blank. `next_self_use_item` answers
the FIRST pending item in file order, which is the curation order.

## The job-file format

`job_markdown` holds the LITERAL text of a job file in the format
`packages.orchestration.pingpong_job.parse_job_file` already accepts: a
`# Job: <title>` H1, then one or more `## Task N` headings, each carrying an
`Acceptance:` line. The queue deliberately stores job-file TEXT rather than a
richer schema of its own, so there is never a second task format to keep in step
with the first.

The rendered bytes are the curated bytes: `write_self_use_job_file` performs no
templating and no substitution, so the text an operator reviewed is exactly the
text that runs.

## The two modules

| Module | Role |
|--------|------|
| `packages/orchestration/self_use_queue.py` | the READ side — loads, validates, answers the next pending item. Owns no writer. |
| `packages/orchestration/self_use_job.py` | renders one item to `<dest_dir>/<id>.md` and plans it via `plan_job_from_file`. Plans only; never runs, never promotes. |

## Consumption — exactly one per feature close

Precondition 6 of the closure protocol
([STATUS_closure_protocol.md](../roadmap/STATUS_closure_protocol.md)) requires
that exactly one self-use item is consumed by each close: the first pending item
is planned, taken to the approval gate, and its `consumed_by` set to the
feature's id in the closure commit. An EXHAUSTED queue never blocks a feature —
the close records `self-use NONE (queue exhausted)` and proceeds, which is the
track asking for curation rather than stopping work.

## Deliberate absences

Remedy deliberately does not let a job mark its own queue item consumed. Neither
module owns a queue writer, and consumption is an edit the closure round makes.
A run that can check itself off is not a gate — the same reason
`docs/roadmap/STATUS.md` sits in `packages.orchestration.scope_fences`'s
built-in deny list.

Remedy deliberately does not discover, generate or infer queue items. The list
is operator-curated data; curation is where this feature's risk sits, and the
queue is exactly as useful as the human who wrote it.
<<<END DOCPAGE

`PLANF257R5` is a WHOLE-FILE replacement of `.agent/plan.md`. `GATEF257R4` and
`FINDF257R5` are TWO SEPARATE APPENDS to `.agent/live_review.md`, in that order,
each under constraint 8 — `GATEF257R4` first. `SLIPSF257R4` is an APPEND of TWO
LINES to `.agent/prose_slips.md` under constraint 8. `DOCPAGE` is the ENTIRE
content of the new file `docs/system/self-use-track-v1.md`. This round registers
R-0735 and resolves nothing.

### The authored pairs for C4 — `docs/README.md`

PAIR A — the quick-find row. FROM (occurs exactly once):

<<<SLICE PAIRAFROM
| self-drive | [self_drive_protocol.md](agents/self_drive_protocol.md) | agents |
<<<END PAIRAFROM

TO:

<<<SLICE PAIRATO
| self-drive | [self_drive_protocol.md](agents/self_drive_protocol.md) | agents |
| self-use track | [self-use-track-v1.md](system/self-use-track-v1.md) | system |
<<<END PAIRATO

PAIR B — the System Documentation table row, inserted in its alphabetical place.
FROM (occurs exactly once):

<<<SLICE PAIRBFROM
| [self-dogfood-v0.md](system/self-dogfood-v0.md) | Self-dogfood readiness + improvement planner |
<<<END PAIRBFROM

TO:

<<<SLICE PAIRBTO
| [self-dogfood-v0.md](system/self-dogfood-v0.md) | Self-dogfood readiness + improvement planner |
| [self-use-track-v1.md](system/self-use-track-v1.md) | Self-use track: the curated queue, the job-file format, one item consumed per feature close |
<<<END PAIRBTO

Both pairs are applied to `docs/README.md` in C4 and nothing else in that file
changes.

### Done when

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C3; report both answers. If it exists at either reading, finish the
commit in hand, write the handback and stop. Report constraint 0's three
readings and `git status --porcelain | wc -l` after each of C0a, C0b, C1, C2, C3
and C4.

G2 TRANSPORT. One digest comparison. Report sha256 and the byte length of the
committed blob `git show <C0a>:.agent/authored/f257-r5.md` and of the reviewer's
own original at `.remedy-wt/f257-r5-block.md`, and whether they are EQUAL. That
original was written before this worker existed, so the reading covers more than
self-consistency; it covers no emission, because this workflow has none — say
both in the handback. Then report that
`git rev-parse <C0b>:.agent/authored/f257-r5.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. `.agent/plan.md` at C1 equals PLANF257R5 including the
trailing newline — report `True` or `False`, with the byte length of each side.
Report `wc -l`, under 50, and the count of lines exactly `## Goal` and exactly
`## Next Steps`.

G4 THE RECORD APPENDS AT C2, over `.agent/live_review.md`. Reconstruct the C2
blob from the `f594cf3b` blob plus GATEF257R4 plus FINDF257R5, applied IN THAT
ORDER each under constraint 8, and report `True` or `False` with all three
lengths. NEGATIVE CONTROL: flip one byte at an offset your script confirms lies
INSIDE the FIRST appended paragraph, recompute, and report the equality is now
`False`. Report that the pre-round blob is a byte PREFIX of the C2 blob, with
both lengths, and that the C2 blob ends in exactly ONE newline. Report
separately that `.agent/prose_slips.md` at C2 reconstructs from its `f594cf3b`
blob plus SLIPSF257R4 under constraint 8, and that SLIPSF257R4 contributed
exactly TWO lines.

G5 THE LEDGER AT C2, counted under constraint 9. Report over
`.agent/live_review.md` at `f594cf3b` and again at C2: the count of lines
matching `^- R-\d+ — ` and whether all are DISTINCT; the count of
`^Done: R-\d+ — ` lines AND the count of DISTINCT ids among them, as two
separate numbers; the count of `^Landed: R-`; the count of
`^Gate: F\d+ R\d+ — `; and the OPEN SET as
`len(set(registered) - set(resolved))`. Expected: registered 295 → 296, the
`Done:` numbers and `Landed:` UNMOVED, `Gate:` 109 → 110, and the open set
253 → 254. Report the count of `^Gate: F257 R4 — ` at C2, which must be 1, and
the count of `^- R-0735 — `, which must be 1.

G6 THE RED-PROOF AT C3, in a disposable worktree added at C3 under
`.remedy-wt/`, never in the primary checkout. Report the UNMUTATED CONTROL
FIRST, in that worktree — a colour with no baseline is not evidence — running
`python3 -B -m pytest tests/orchestration/test_self_use_job.py -q -p no:cacheprovider`
with its REAL exit code and passed count, and purge `__pycache__` before every
run. THE MUTATIONS, each applied alone and reverted before the next, each in
`packages/orchestration/self_use_job.py` inside the worktree, and each of which
must turn that file RED: (i) DELETE the new single-component check, leaving the
`f594cf3b` guard alone — this is the R-0735 regression and it MUST redden, which
is the whole point of S4; (ii) DELETE the resolved containment check, keeping
the new single-component check; (iii) break the verbatim-bytes rule by making
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
`tests/orchestration/test_development_artifact_boundary.py`; the docs guards
`tests/docs/test_docs_consistency.py`; and the canary
`tests/cli/test_golden_path.py`. Every one must be exit 0. If any is red, STOP
and write the handback with the full untruncated failure list.

G8 STRUCTURE, over `f594cf3b..<C4>` — the range that ends BEFORE the handback
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
`tests/orchestration/test_self_use_job.py`, `docs/system/self-use-track-v1.md`
and `docs/README.md` — each expected 0 — beside the same counts over
`.agent/authored/f257-r5.md` as the non-zero control. Report
`git ls-files .remedy-wt | wc -l`, expected 0. Report the `git diff --numstat`
line for `packages/orchestration/self_use_queue.py`,
`scripts/self_use_queue.json` and `docs/roadmap/STATUS_closure_protocol.md` over
the range, all three expected ABSENT.
THEN THE DOC GATE, because the suite does not cover it:
`tests/docs/test_docs_consistency.py` checks relative links in FIVE primary docs
only — `README.md`, `AGENTS.md`, `docs/README.md`, `docs/roadmap/STATUS.md` and
`docs/roadmap/ROADMAP.md` — and `docs/system/self-use-track-v1.md` is NOT among
them. So resolve the new page's OWN relative markdown links yourself: extract
every `[text](target)` from its C4 blob, drop `http://`, `https://` and
`mailto:` targets, and report each remaining target with whether
`(docs/system/ / target)` exists. All must exist; the page carries at least the
link to `../roadmap/STATUS_closure_protocol.md`. Report also that
`docs/README.md` at C4 contains the string `system/self-use-track-v1.md` exactly
TWICE, and that `docs/system/self-use-track-v1.md` did NOT exist at `f594cf3b`
(`git cat-file -e` on that path at that revision fails).

### Handback

Rewrite `.agent/handoff.md` in C5 per docs/agents/handback_template.md. It
carries: `SESSION 2 of feature F257 · round 5`; the range `f594cf3b..HEAD`; a
per-commit changed-files table whose `+/-` cells are taken from
`git diff --numstat` and compared cell by cell against the figures G8 reports;
ONE LINE PER GATE G1 through G8 with its real result; the deviations, including
every guard re-expression constraint 6 required; the item-status table with
every C-item and every gate appearing exactly once; the open-findings count,
which must be 254; and the next expected action, which is the integration gate.

Do not write a `Done:` or `Gate:` paragraph of your own anywhere — GATEF257R4
and FINDF257R5 are reviewer-authored text you apply verbatim, and any OTHER such
paragraph is a finding however hedged.

After C5: push with `git push origin feature/f257-self-use-track` and report the
outcome. Do NOT create a pull request and do NOT merge anything.
