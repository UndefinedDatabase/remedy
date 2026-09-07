# Handback — F272 One world completion, round 17

## Session

`SESSION 9 of feature F272 · round 17 · rounds so far 17`

F272's soft limit is 12 sessions and 40 rounds under operator amendment
amend0906-triage-throughput, so at session 9 / round 17 the feature is inside
its limit and NO scope report is owed. Context self-assessment (required by
amend0905-throughput): context is comfortable — this round spent most of it on
the six serial suites and the red-proof transcript rather than on reading, and
there is ample room for further rounds this session.

## Range

Review of `5964aa76`..`HEAD`.

## Commits

Six commits before this handback, every one single-parent, in exactly the
block's ordered sequence C0a, C0b, C1, C2, C3, C4. Every `+/-` cell below is
`git diff --numstat <parent> <commit>`, not a line count of any file, and each
matches G8's reading cell for cell.

### 0f198da0 f272: save the round 17 step block verbatim  (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f272-r17.md | +392 / -0 | the step block saved verbatim by `shutil.copyfile`, never retyped |

### 5277854d f272: mirror the round 17 block into the last-block slot  (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +374 / -288 | the same bytes mirrored by `shutil.copyfile`; the round 16 block it replaces is what the deletions are |

### d11d3415 f272: point the plan at the second T003 consumer  (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +26 / -21 | replaced with the PLANF272R17 slice, byte for byte |

### 7b3ff7a3 f272: book the round 16 verdict and the R-0822 resolution  (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 / -0 | the RECORDR17 slice appended as `pre + LF + slice`; no id minted |

### 7b9bf290 f272: move job context onto the unified record, across both stores  (C3)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job_context_cmd.py | +62 / -10 | the production change, written under the SPEC (S1-S8) rather than sliced |

### 335be882 f272: pin job context against a ping-pong created job  (C4)
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_context_cmd.py | +57 / -0 | the GUARDR17 slice appended; insertions only, no existing test touched |

### C5 — this handback (self-reference: a handoff cannot table the commit that writes it)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | (not counted) | rewritten per docs/agents/handback_template.md; the block excludes C5 from the insertion-count gate for exactly this reason |

Every insertion count above is under the DECISION F104 D1 cap of 500, which
counts INSERTIONS only; the largest is C0a at 392.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f272-r17.md` written by `shutil.copyfile` of the source block |
| C0b | done | `.agent/last_block.md` written by `shutil.copyfile` of the same source |
| C1  | done | `.agent/plan.md` replaced with the PLANF272R17 slice, byte-equal |
| C2  | done | RECORDR17 appended to `.agent/live_review.md` against a freshly read pre-image |
| C3  | deviated | SPEC S1-S8 all implemented as written; ONE sentence of the module docstring was additionally corrected — see Deviations 1 |
| C4  | done | GUARDR17 appended to `tests/cli/test_job_context_cmd.py`; pure append, 9 -> 12 tests |
| C5  | done | this file |

## Open findings

**57 open BY DISTINCT ID.** Arithmetic, measured over
`.agent/live_review.md` after C2: 306 distinct `^- R-\d{4} ` registrations
minus 249 distinct `^Done: R-\d{4} ` resolutions = 57. The round moved the
count 58 -> 57 by booking R-0822's resolution and minted ZERO ids; **R-0823
remains the next free id**, and the registration count is unchanged at 306,
which is the measurement that proves nothing was registered.

## Verification — one line per gate, every exit code REAL

| Gate | Real exit code | Result |
|---|---|---|
| G1 TRANSPORT | 0 | one sha256 `eea9a264…e835d6f`, one length 26723 bytes, one count 392 lines across the source block, `.agent/authored/f272-r17.md` and `.agent/last_block.md` |
| G2 THE RECORD | 0 | all four readers accept; see the breakdown below |
| G3 THE PLAN | 0 | `.agent/plan.md` 2167 bytes, 44 lines against the cap of 50, byte-equal to its slice, `## Goal` and `## Next Steps` both present |
| G4 THE MOVE IS REAL | 0 | the shipped handler answers for a unified job and keeps both exit-1 paths; see the breakdown below |
| G5 THE SUITES | 0, 0, 0, 0, 0, 0 | 1541 / 515 / 52 / 21 / 16 / 42 passed, six serial invocations |
| G6 RED-PROOF | 0, 1, 0 | control green 12 passed, reverted RED with two named failures and 10 passing, restored green 12 passed |
| G7 LINT AND INTEGRITY | 0, 0 | ruff `All checks passed!`; integrity `"passed": true`, `"fail_count": 0`, `"check_count": 5` |
| G8 THE TREE | 0 | `git status --porcelain` empty at all six commit boundaries and at the end |

### G1 TRANSPORT — one digest comparison

The source `.remedy-wt/f272-r17-block.md` was hashed ON ARRIVAL, before any
other work, and the figures reported back to the reviewer before the round
proceeded:

    sha256 = eea9a264fe7d48826689f97d9865d75114aea08cb0962adef0e97acc1e835d6f
    bytes  = 26723
    lines  = 392

All three artefacts carry those same three figures. C0a and C0b are both
`shutil.copyfile` of that source — a byte copy, never a retype.

### G2 THE RECORD — the four readers, each reported separately

(a) BYTE. Pre-image length 1157784, sha256
`e25c3ba53c763fb7e77892d807b9e1075e43b9c2742abf30960b671943da008b`, terminal
twelve bytes `b' next gate.\n'`, trailing-newline run 1. Post 1163718, sha256
`d84a6aac059295258da1d8d370a97c2828691879bf3aa63ba914c93be907c145`. Arithmetic
1157784 + 1 + 5933 = 1163718, matching disk. `pre` is a byte-exact PREFIX of
`post`: True. `post == pre + b"\n" + slice`: True. The pre-image was READ
immediately before the write, and was afterwards recovered INDEPENDENTLY from
git (`git show 7b3ff7a3^:.agent/live_review.md`) for the assertion-based
re-read, which reproduced every figure.

(b) STRUCTURAL. The file's SINGLE terminal newline is stripped BEFORE splitting
on blank lines — stated explicitly, because it is what decides the last unit.
N was COUNTED BY THE SCRIPT from the slice's own blank-line paragraphs and was
not taken from the block: **N = 2** (para 1 3965 bytes opening `Gate: F272 R16
— …`, para 2 1965 bytes opening `Done: R-0822 — RESOLVED …`). Units 715 ->
717, delta 2. The LAST 2 units equal the slice's 2 paragraphs IN ORDER: True.
Everything before them is unchanged: True.

(c) NEGATIVE CONTROL on the FIRST appended paragraph, IN MEMORY and never on
disk: byte at offset 1157806 flipped `b'e'` -> `b'E'`. Reader (a) rejects:
True. Reader (b) rejects: True. Both accept once restored: True. The on-disk
sha256 is `d84a6aac…907c145` both before and after the control — identical, so
the control never reached disk.

(d) COUNTS, before C2 -> after C2, every one measured. All seven reproduce the
block's figures exactly; there is NO difference to report.

    ^- R-\d{4} distinct        306 -> 306   (nothing registered; R-0823 stays free)
    ^Done: R-\d{4} distinct    248 -> 249
    open set BY DISTINCT ID     58 ->  57
    ^Gate:                      39 ->  40
    ^Gate: F272 R16              0 ->   1
    ^Done: R-0822                0 ->   1
    ^Landed: R-0822              1 ->   1

The last of those is the DECISION F272 D10 reading, and it holds: the `Landed:
R-0822` line SURVIVES beside the new `Done: R-0822` paragraph and was not
written over.

Constraint 2, line-anchored `^<<<(BEGIN|END) .*>>>$`, measured after C4: 0 in
`.agent/plan.md`, 0 in `.agent/live_review.md`, 0 in
`tests/cli/test_job_context_cmd.py`. `.agent/live_review.md` still holds 15
MID-LINE `<<<` substrings inside older records' prose, exactly the pre-existing
count the block predicted; `.agent/plan.md` holds 0 and the test file holds 0.

### G4 THE MOVE IS REAL — run against the shipped module

Provenance, printed FIRST:

    apps.cli.commands.job_context_cmd.__file__ =
      /home/decodeux/Repos/remedy/apps/cli/commands/job_context_cmd.py

With `REMEDY_DATA_DIR` set in-process (via `os.environ`, because env-var
assignment is denied in every shell form) to a scratch directory under
`.remedy-wt/`, a `JobPlan` carrying one `TaskEntry` and a real `repo_path` was
persisted to
`…/data/jobs/fc1da384f1e948e1/job.json`, and
`_cmd_job_context(job_id, task_ref="T001", json_output=True)` was called:

    exception raised = NONE
    job_id       = fc1da384f1e948e1   (== job.job_id)
    task_id      = T001
    task_label   = T001
    fenced_paths = ['alpha.py']

Then for ids in NEITHER store, real exit codes and real stderr:

    full uuid '3f2504e0-4f89-41d3-9a0c-0305e82c3301' -> exit 1
      stderr: "Job not found: 3f2504e0-4f89-41d3-9a0c-0305e82c3301"
    short hex '0123456789abcdef'                     -> exit 1
      stderr: "Error: no job matches prefix '0123456789abcdef'"

The second is `resolve_any_job_id`'s own exit path, byte-identical to what
`resolve_job_id` printed there before, as the SPEC's "what must not move" list
requires. CALL-form counts over `apps/cli/commands/job_context_cmd.py`:
`resolve_job_id(` = **0** (reviewer measured 1 at `5964aa76`), and
`resolve_any_job_id(` = **1** (reviewer measured 0). Both match the
expectation. The scratch directory was removed afterwards BY EXACT PATH.

### G5 THE SUITES — serial, each its own invocation, all in the PRIMARY checkout

    python3 -B -m pytest tests/cli/ -q -p no:randomly
      REAL_EXIT=0   1541 passed in 307.61s
    python3 -B -m pytest tests/ui_server/ -q -p no:randomly
      REAL_EXIT=0   515 passed in 37.48s
    python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly
      REAL_EXIT=0   52 passed in 6.42s
    python3 -B -m pytest tests/regression/test_resource_safety.py -q -p no:randomly
      REAL_EXIT=0   21 passed in 11.61s
    python3 -B -m pytest tests/orchestration/test_integrity_gate.py -q -p no:randomly
      REAL_EXIT=0   16 passed in 0.34s
    python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
      REAL_EXIT=0   42 passed in 21.14s

`tests/cli/` RECONCILED rather than asserted. `ast` counts the test functions
in `tests/cli/test_job_context_cmd.py` as **9 at the C3 commit** and **12 at
the C4 commit**, a delta of **+3** (the three new functions being
`test_a_ping_pong_created_job_compiles_context_like_a_classic_one`,
`test_a_ping_pong_job_without_a_repo_path_exits_two` and
`test_an_unknown_job_of_either_shape_still_exits_one`), and every one of the 9
pre-existing functions survives unchanged. The arithmetic is therefore
**1538 + 3 = 1541**, which is the number that ran. The other five readings —
515, 52, 21, 16, 42 — reproduce the reviewer's base readings exactly. NO
difference to report on any of the six.

### G6 RED-PROOF — only inside a disposable worktree

Worktree added detached at the C4 commit:
`git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f272-r17-redproof 335be882`
(REAL_EXIT=0). Every `__pycache__` under it was purged first (0 remaining) and
`python3 -B` was used throughout. Provenance probed BEFORE any edit:

    __file__ = /home/decodeux/Repos/remedy/.remedy-wt/f272-r17-redproof/apps/cli/commands/job_context_cmd.py

which resolves INSIDE the worktree, so no editable install shadowed it. The
ORDERED COLOUR, unmutated control FIRST, the command each time being
`python3 -B -m pytest tests/cli/test_job_context_cmd.py -q -p no:randomly`:

1. committed state — **REAL_EXIT=0**, `12 passed in 4.07s` (GREEN);
2. C3's file ALONE reverted via
   `git checkout 5964aa76 -- apps/cli/commands/job_context_cmd.py`, C4's tests
   left in place — **REAL_EXIT=1**, `2 failed, 10 passed in 3.82s` (RED);
3. restored — **REAL_EXIT=0**, `12 passed in 3.69s` (GREEN).

The two failures in the red run, BY NAME:

    FAILED tests/cli/test_job_context_cmd.py::test_a_ping_pong_created_job_compiles_context_like_a_classic_one
    FAILED tests/cli/test_job_context_cmd.py::test_a_ping_pong_job_without_a_repo_path_exits_two

and the assertion text the first carried — the shipped defect this round
repairs, in its own words:

    assert r.returncode == 0, r.stderr
    E  AssertionError: Error: no job matches prefix '579a9711620c46b7'
    E  assert 1 == 0

The second carried `assert 1 == 2`, again on
`stderr="Error: no job matches prefix '36d65626f4564234'\n"`. This matches the
reviewer's measurement of EXIT 1 with two named failures and ten passing
exactly. `test_an_unknown_job_of_either_shape_still_exits_one` PASSED in the
reverted run, as the block predicted: it is a regression pin on a contract both
the old and the new code satisfy and is deliberately not a discriminator. The
worktree was removed afterwards BY EXACT PATH (`git worktree remove
/home/decodeux/Repos/remedy/.remedy-wt/f272-r17-redproof`, REAL_EXIT=0, the
path confirmed gone), never by glob.

### G7 LINT AND INTEGRITY

    python3 -m ruff check apps/cli/commands/job_context_cmd.py tests/cli/test_job_context_cmd.py
      REAL_EXIT=0   All checks passed!
    python3 -m apps.cli.grouped integrity check --json
      REAL_EXIT=0   "passed": true, "fail_count": 0, "check_count": 5

All five checks pass: `handler_import` (handlers=342), `live_review_verdict`,
`plan_consistency` (unchecked=0), `relevant_untracked` (untracked=0) and
`high_blockers_open` (no open blocker/high findings). No finding was edited to
move any of them.

### G8 THE TREE

`git status --porcelain` was run at EVERY commit boundary and its real output
was EMPTY every time — after C0a, C0b, C1, C2, C3, C4 and at the end of the
round. `git ls-files .remedy-wt` is EMPTY. `git worktree list` shows thirteen
entries: the primary checkout plus the twelve pre-existing `remedy/job-*`
worktrees — the same thirteen as before the round, the red-proof worktree
having been added and removed inside it. Per-commit insertion counts against
the DECISION F104 D1 cap of 500 (INSERTIONS only), C5 excluded: 392, 374, 26,
4, 62, 57 — every one well under the cap.

`.agent/STOP` readings ordered by constraint 5, all three by
`os.path.exists`: **before C0a — False; before C3 — False; before C5 — False.**

## Authored-text proofs

Every slice was extracted PROGRAMMATICALLY from the committed
`.agent/authored/f272-r17.md`, between its `<<<BEGIN NAME>>>` and
`<<<END NAME>>>` lines, and applied byte for byte. None was retyped.

| Slice | Bytes | sha256 | Disk-to-disk result |
|---|---|---|---|
| PLANF272R17 | 2167 | `40a28d47…5743ad8` | `.agent/plan.md` byte-EQUALS the slice |
| RECORDR17 | 5933 | `a427b676…3700d90` | tail of `.agent/live_review.md` equals the slice; `post == pre + LF + slice` |
| GUARDR17 | 2266 | `ff2aff4e…3979765d` | tail of `tests/cli/test_job_context_cmd.py` equals the slice byte for byte |

The production change (C3) is DESCRIBED, not sliced: it was written by the
worker under the SPEC, so it has no authored-text proof by construction.

## Deviations & assumptions

There was NO departure from the block's ordered commit sequence: six commits,
C0a C0b C1 C2 C3 C4, in that order, one logical path each, plus C5.

**Deviation 1 — one sentence of the C3 module docstring corrected beyond the
literal S1-S8 list.** The module docstring of
`apps/cli/commands/job_context_cmd.py` stated "The fenced scope compiled here
is exactly the task's ``inputs["flight"]["files_hint"]``". S5 falsifies that
sentence for a `TaskEntry` in precisely the way S6 says S4 falsifies
`_task_label`'s docstring, but the SPEC named only the S6 clause. I corrected
it to name BOTH spellings and changed nothing else in the docstring. I take
AGENTS.md as the higher authority here — "Files must remain … consistent with
architecture, free of obvious bugs" and the Documentation Updates rule "an
existing behavior is changed" — and shipping a module whose own docstring
contradicts the function I just widened seemed the worse of the two readings.
It is +2 / -1 of the C3 diff. **I am declaring it rather than choosing
silently**, as the block instructs; if the reviewer reads the SPEC's
enumeration as exhaustive, this is the line to revert.

**Deviation 2 — the C3 numstat differs from the reviewer's dry run.** The block
measured 56 insertions and 15 deletions; I measure **62 insertions and 10
deletions**. Reported, and NOTHING was changed to make them agree. The
difference is prose and formatting, not behaviour: my three WHY comments run
two to four lines each, the S7 list comprehension is wrapped across three lines
rather than one, the S8 comment is five lines, and Deviation 1 adds a line —
which also converts what the reviewer counted as replaced lines into added
ones, explaining the lower deletion count. Every behavioural clause of the SPEC
is implemented, and the two independent measurements the block DID pin —
`resolve_job_id(` at 0 and `resolve_any_job_id(` at 1, and the file's suite
going 9 -> 12 — both reproduce exactly.

**Assumption 1 — the C4 separator.** The block states the append formula for C2
(`pre + b"\n" + slice`) but states none for C4. I derived it from the TARGET'S
OWN convention rather than inventing one: `tests/cli/test_job_context_cmd.py`
separates top-level definitions by exactly two blank lines and its pre-image
ends in a single newline, so C4 was applied as `pre + b"\n\n" + slice`. The
join region reads `b']\n\n\ndef '`. Two independent readers confirm it — the
diff is +57 / -0, insertions only, and `ruff check` exits 0 where E302 would
have caught a one-blank-line join.

**Assumption 2 — the Commit Gate at C0a and C0b.** At those two boundaries
`.agent/plan.md` still described round 16, because the block orders the plan
rewrite at C1. I took the conservative reading that the block's ordered
sequence governs and that a two-commit lag inside one round is what "Verify
`.agent/plan.md` matches the current work" tolerates, rather than reordering
the block. This is the same reading round 16 took.

**Assumption 3 — where `resolve_any_job_id` sits in C3.** S8 says to resolve
with `resolve_any_job_id` and to fall back "inside the existing `except
JobNotFoundError`". I placed the resolve call INSIDE the existing `try`, where
`resolve_job_id` already sat, so the diff is a substitution rather than a
restructure. This is behaviour-neutral: `resolve_any_job_id` raises
`SystemExit`, never `JobNotFoundError`, so the `except` clause cannot catch it
and its own exit-1 path is untouched — which G4 confirmed by running it.

**Not a deviation, recorded because a reader will look for it:** ZERO finding
ids were minted, as constraint 4 requires. R-0823 remains the next free id and
the registration count is unchanged at 306.

## External actions

| Action | Command | Outcome |
|---|---|---|
| worktree add | `git worktree add --detach .remedy-wt/f272-r17-redproof 335be882` | REAL_EXIT=0, detached at `335be882` |
| worktree remove | `git worktree remove .remedy-wt/f272-r17-redproof` | REAL_EXIT=0, path confirmed gone; 13 worktrees again |
| push | `git push -u origin feature/f272-one-world-completion` | run as the round's LAST action, immediately after the C5 commit this file is; a handback cannot record its own push outcome, so the branch tip at `origin` is the evidence |

NO PR was created. NOTHING was merged. NO force-push, no history rewrite, no
branch deletion. The G4 scratch directory under `.remedy-wt/` was removed by
exact path, never by glob.

## Next

The reviewer re-runs G1 through G8 itself at this branch tip and issues the
round 17 verdict. The single expected next action after that is T003's
remaining consumer surface — `packages/orchestration/ui_server.py` and its
`_JobPlanTaskAdapter` — whose boundary against F273 T001 (finding R-0804) must
be ruled before it is touched, per the plan's Next Steps. Phase 1 rule 1
(`.agent/STOP`) is checked before rule 2, as always.
