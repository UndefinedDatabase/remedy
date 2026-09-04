# Handoff — F114 Cost preview per command, round 6 (books R5's PASS; starts T003's first slice — marking is_expensive)

## Session

SESSION 2 of feature F114 · round 6 · rounds so far 6.

First round of session 2 (session 1 closed at round 5 per amend0827 rule
6's 4-5 default). This round books round 5's PASS verdict into the
ledger (RECORD5) and starts T003's first slice: adds `is_expensive: bool
= False` to `CommandEntry` (`apps/cli/command_catalog.py`) and marks
`job.run` as the first and only expensive command so far. Catalog tests
in `tests/test_command_catalog.py` confirm the field's type and that
exactly `job.run` carries it. Wiring `confirm_cost_preview()` into a
real command's execution path, goldens, and docs are NOT this round
(constraint 6) — that needs task-count/class data `job.run` does not
gather yet, which is separate, larger work.

## Range

Review of `2e7e0090715562a7794b22a6b5ded313c3227c65..HEAD` (HEAD is
`10c7b3240e87920c470c9c45829d0ba6ec21265e` before this handback commit).

## Item Status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this handback |
| G1 TRANSPORT | done | PASS |
| G2 THE LEDGER APPEND | done | PASS |
| G3 THE PLAN | done | PASS |
| G4 THE THREE CATALOG PAIRS | done | PASS |
| G5 COMPILE AND LINT | done | PASS (ruff denied, as expected) |
| G6 THE RED-PROOF | done | PASS (2 failed / 21 green) |
| G7 THE SUITES | done | PASS (all 10 measured) |
| G8 THE TREE, THE COMMITS AND THE SWEEP | done | PASS |

## Commits

### 6b415998 F114 R6 C0a: save step block verbatim to .agent/authored/f114-r6.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f114-r6.md` | +333/-0 | transport proof — verbatim `cp` of the supplied step block, new file |

### b025ca6e F114 R6 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +229/-289 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 8f79f31b F114 R6 C1: append RECORD5 to live_review.md, replace plan.md with PLAN6
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD5 (round 5's PASS verdict) — exactly one `\n` then RECORD5's 3723 bytes, no blank-line separator |
| `.agent/plan.md` | +29/-17 | whole-file replace with PLAN6 (first substantive commit, per constraint 2) |

### 10c7b324 F114 R6 C2: mark is_expensive field and job.run (T003 first slice)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | +6/-0 | FIELD PAIR (adds `is_expensive: bool = False` to `CommandEntry`, between `may_execute_commands` and `related`) and MARK PAIR (marks `job.run`'s own entry `is_expensive=True`) — two separate `str.replace` calls, FIELD PAIR first per constraint 7 |
| `tests/test_command_catalog.py` | +19/-0 | TEST PAIR — new `TestCatalogExpensive` class (3 tests) inserted between `TestCatalogClassification` and `TestCatalogSensitivity` |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f114-cost-preview-per-command` → run after
  this handback commit (C3), pushing all five commits of the round.
- No `gh pr` command of any kind was run this round — no PR is created
  or touched this round; constraint 11 states explicitly that T003
  having only its first slice land does not by itself trigger the Open
  PR Gate.
- One disposable git worktree, created and removed for G6's red-proof
  only, never the primary checkout:
  `git worktree add /home/decodeux/Repos/remedy/.remedy-wt/f114-r6-redproof HEAD`
  (created, detached HEAD at this round's own C2, `10c7b324`) then, after
  the red/green cycle, `git worktree remove --force
  /home/decodeux/Repos/remedy/.remedy-wt/f114-r6-redproof` (removed).
  `git worktree list` immediately after shows it gone — see G8.

## Verification

Preconditions, checked before C0a:

```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f114-cost-preview-per-command
$ git log --oneline -n 5
2e7e0090 F114 R5 C3: rewrite .agent/handoff.md - round 5 handback
27c3acc4 F114 R5 C2: ship cost_preview_confirm.py (T002 complete) and its tests
67a4a73c F114 R5 C1: append RECORD4 to live_review.md, replace plan.md with PLAN5
3f705774 F114 R5 C0b: mirror block to .agent/last_block.md
487a8ac8 F114 R5 C0a: save step block verbatim to .agent/authored/f114-r5.md
```
Step block was read from `.remedy-wt/r5-review/f114-r6-draft.md`
(supplied path); `cp`'d verbatim, never retyped.

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f114-r6.md .agent/last_block.md
fabe2098d8505810ffc1cfbddbd9516acc284db32d0f76bd8db92e6fc87d318a  .agent/authored/f114-r6.md
fabe2098d8505810ffc1cfbddbd9516acc284db32d0f76bd8db92e6fc87d318a  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE LEDGER APPEND**:
```
Base size of .agent/live_review.md immediately before C1: 2364059 bytes
Base ends with trailing newline: False
RECORD5 own byte length (extracted from committed authored file): 3723 bytes, 0 internal newlines
base + 1 + len(RECORD5) = 2364059 + 1 + 3723 = 2367783
post-C1 file byte length: 2367783
Match: True (also matches the round instructions' own stated 2367783/2364059/3723 exactly)
```
Second, independent reader — sliced the post-C1 file's bytes from the
measured `base` offset (2364059) to end-of-file and compared against
`"\n" + RECORD5` directly:
```
tail (base..end) == "\n" + RECORD5: True
```
Negative control, scratch copy only (never the tracked file) — one byte
flipped (XOR 0xFF) inside a Python `bytearray` copy of RECORD5's own
first byte, then re-compared against the real `"\n" + RECORD5`:
```
second reader REJECTS the mutated copy: True (mutated tail != "\n" + RECORD5)
```
All PASS.

**G3 THE PLAN**:
```
$ cmp <PLAN6 extracted from committed authored file> .agent/plan.md
(no output — exit 0)
$ wc -l .agent/plan.md
49 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
`cmp` exit 0, `wc -l` 49 (under 50 — PASS), both grep counts 1 — PASS.

**G4 THE THREE CATALOG PAIRS**:
```
Pre-C2 FROM counts (command_catalog.py):
  FIELD PAIR FROM: 1
  MARK PAIR FROM (re-counted in the file AFTER FIELD PAIR applied, BEFORE MARK PAIR, per constraint 7): 1
Pre-C2 FROM count (test_command_catalog.py):
  TEST PAIR FROM: 1
Containment (constraint 5 — all three are rewrites):
  FIELD PAIR: TO contains FROM: false
  MARK PAIR: TO contains FROM: false
  TEST PAIR: TO contains FROM: false
```
Then, extracting each slice from the committed authored file and
applying `str.replace` in constraint-7 order (FIELD PAIR then MARK PAIR)
to a pre-C2 scratch copy (`git show <C1-sha>:apps/cli/command_catalog.py`)
of `command_catalog.py`, and TEST PAIR to a pre-C2 scratch copy of
`tests/test_command_catalog.py`:
```
command_catalog.py reconstructed matches actual: True
test_command_catalog.py reconstructed matches actual: True
```
Both `cmp`-equivalent (byte comparison) exit 0 — PASS. Direct read of
the landed file confirms `is_expensive=True` sits on `job.run`'s own
`CommandEntry` (not `job.run-next`'s), between `may_execute_commands=True,`
and `related=("job.run-next", "job.plan", "decision.list"),`.

**G5 COMPILE AND LINT**:
```
$ python3 -m py_compile apps/cli/command_catalog.py tests/test_command_catalog.py
(no output — exit 0)
$ ruff check apps/cli/command_catalog.py tests/test_command_catalog.py
This command requires approval
```
`py_compile` exit 0 on both files — PASS. `ruff check` produced the
session-level denial ("This command requires approval") — reported
verbatim per constraint 8, not assumed; `ruff` is denied to this
session, consistent with rounds 1-5's own notes.

**G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY**:
```
$ git worktree add /home/decodeux/Repos/remedy/.remedy-wt/f114-r6-redproof HEAD
Preparing worktree (detached HEAD 10c7b324)
HEAD is now at 10c7b324 F114 R6 C2: mark is_expensive field and job.run (T003 first slice)
```
Inside the worktree, the `is_expensive=True,` line was removed from
`job.run`'s own `CommandEntry` (reverting it to the field's default
`False` — a one-line removal):
```
$ python3 -m pytest tests/test_command_catalog.py -q
2 failed, 19 passed in 0.22s
FAILED tests/test_command_catalog.py::TestCatalogExpensive::test_exactly_job_run_is_marked_expensive_so_far
FAILED tests/test_command_catalog.py::TestCatalogExpensive::test_job_run_is_expensive
```
2 failures (> 0), exactly the two named in the gate's own expectation —
proving `is_expensive`'s mark on `job.run` is real, reachable data, not
dead code. The line was restored inside that same worktree (copied back
byte-identical from the primary checkout's own committed file, confirmed
by `cmp`), then re-run:
```
$ python3 -m pytest tests/test_command_catalog.py -q
21 passed in 0.19s
```
Fully green again (the unmutated control) — 21 passed, matching the
primary checkout's own G7 reading for this suite. Worktree removed:
```
$ git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f114-r6-redproof
$ git worktree list
(no f114-r6-redproof entry — confirmed gone)
```
PASS. The mutation was applied and tested exclusively inside
`.remedy-wt/f114-r6-redproof/`, never the primary checkout
(self_drive_protocol.md guardrail G5); the primary checkout's own
`command_catalog.py` was never touched by this gate.

**G7 THE SUITES, SERIALLY, PRIMARY CHECKOUT**:
```
$ python3 -m pytest tests/test_command_catalog.py -q
21 passed in 0.21s
$ python3 -m pytest tests/cli/test_command_catalog.py -q
23 passed in 0.71s
$ python3 -m pytest tests/orchestration/test_job_task_runner.py -q
214 passed in 63.29s
$ python3 -m pytest tests/docs/ -q
295 passed in 0.46s
$ python3 -m pytest tests/orchestration/test_roadmap_index.py -q
30 passed in 0.37s
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.75s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.57s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.54s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.30s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.73s
```
`test_command_catalog.py` reads 21 passed — matches the gate's own
stated expectation exactly (18 existing + 3 new `TestCatalogExpensive`
tests). `tests/cli/test_command_catalog.py` (23) and
`tests/orchestration/test_job_task_runner.py` (214) are IDENTICAL to
the reviewer's own stated base readings — moved-count checks, both
unmoved; this round touches only `CommandEntry`'s dataclass shape and
`job.run`'s own entry, and neither of those two suites asserts against
`is_expensive`. `tests/docs/` (295), `test_roadmap_index.py` (30),
`tests/ui_server/` (515), `test_test_runner.py` (52),
`test_resource_safety.py` (21), `test_integrity_gate.py` (16) and
`test_golden_path.py` (canary, 42) are all IDENTICAL to round 5's own
stated figures — nothing moved outside this round's own three new
tests. These are the REAL, measured counts, not forced to any
assumption. `tests/ui_server/`, `test_test_runner.py`,
`test_resource_safety.py` and `test_integrity_gate.py` were run as all
four named, not fewer, per the gate's own instruction.

**G8 THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain
(empty — checked immediately before C3 staged)
$ git ls-files .remedy-wt
(no output — nothing under .remedy-wt/ is ever committed)
$ git worktree list
/home/decodeux/Repos/remedy                                  10c7b324 [feature/f114-cost-preview-per-command]
(plus 8 pre-existing, unrelated .remedy-wt/job-* worktrees from other
job runs — none created or touched by this round's G6, confirmed by
name: none is "f114-r6-redproof")
```
Per-commit insertion cross-check (`git show --numstat`, `+` column
only) against this handback's own Commits table above — all cells
match:

| Commit | File | numstat `+` | Table `+` | Match |
|---|---|---|---|---|
| 6b415998 (C0a) | `.agent/authored/f114-r6.md` | 333 | 333 | yes |
| b025ca6e (C0b) | `.agent/last_block.md` | 229 | 229 | yes |
| 8f79f31b (C1) | `.agent/live_review.md` | 2 | 2 | yes |
| 8f79f31b (C1) | `.agent/plan.md` | 29 | 29 | yes |
| 10c7b324 (C2) | `apps/cli/command_catalog.py` | 6 | 6 | yes |
| 10c7b324 (C2) | `tests/test_command_catalog.py` | 19 | 19 | yes |

C3's own numbers go to neither this table nor a round report, per G8's
own instruction.

Staleness sweep, one entry per file this round touched:

| File | Stale? | Why |
|---|---|---|
| `.agent/authored/f114-r6.md` | NOT stale | immutable historical stamp of this round's instructions |
| `.agent/last_block.md` | NOT stale | current mirror of this round's block; accurate until round 7 overwrites it |
| `.agent/live_review.md` | NOT stale | RECORD5 books round 5's real PASS verdict, append-only ledger |
| `.agent/plan.md` | NOT stale | reflects F114 round 6's actual current step and real next steps |
| `apps/cli/command_catalog.py` | NOT stale | `is_expensive` field and `job.run`'s mark are live and tested; zero confirm-path callers yet, by design (constraint 6 — T003's next slice wires a real caller) |
| `tests/test_command_catalog.py` | NOT stale | 3 new `TestCatalogExpensive` tests directly cover the new field and mark, all passing |
| `.agent/handoff.md` | N/A | this handback itself, written last, freshest by construction |

Outside the change set: no NEW stale sentence was found this round.
`.agent/context.md` line 36 ("No `cost_preview.py` or
expensive-command registry exists today...") and line 29 (the
`budget_guard.py:482-484` reference) — round 2's and round 3's own
declared staleness — both stand unrepeated, per constraint 9's explicit
instruction not to repeat them. This round's own addition of
`is_expensive` to `command_catalog.py` arguably deepens line 36's
existing staleness (a per-command "expensive" mark on an existing file
now exists, closer to an "expensive-command registry" than round 3's
own reading), but it is the SAME already-declared line, not a new one,
so it is not re-declared here. `docs/roadmap/features/T3_F114.md` line
45 ("T003 marking the expensive commands...") describes a task-list
item still in progress, not a done/not-done claim, so this round's
partial T003 progress does not make it stale. `docs/roadmap/STATUS.md`'s
F114 line (`- [~] F114`) is untouched and still correctly claimed (in
progress — T003 remains, now partially started).

## Authored-text proofs

- `.agent/authored/f114-r6.md` (copied via `cp` from
  `.remedy-wt/r5-review/f114-r6-draft.md`, never retyped) sha256
  `fabe2098d8505810ffc1cfbddbd9516acc284db32d0f76bd8db92e6fc87d318a`,
  confirmed identical to the source via `cmp` before staging, and again
  matching `.agent/last_block.md` after C0b (G1).
- All six slices (RECORD5, PLAN6, FIELD PAIR FROM/TO, MARK PAIR FROM/TO,
  TEST PAIR FROM/TO) were extracted from the COMMITTED
  `.agent/authored/f114-r6.md` by a Python script
  (`.remedy-wt/r6-extract_slices.py`) reading delimiter indices
  (`<<<BEGIN ...>>>` / `<<<END ...>>>`), splitting the file on `\n`
  bytes and re-joining the lines strictly between each pair of markers
  — never by hand-retyping (constraint 1). Per constraint 4's explicit
  statement, RECORD5/PLAN6 were taken as the naive marker-to-marker join
  with no added trailing newline, while FIELD/MARK/TEST PAIR FROM and TO
  each had one `\n` appended back as their own real structural suffix —
  no ambiguity needed resolving this round.
- RECORD5: 3723 bytes, 0 internal newlines, matches the round
  instructions' own stated figure exactly; appended to
  `.agent/live_review.md` as exactly one `\n` + RECORD5 (G2, above).
- PLAN6: 2374 bytes, no trailing newline (matches `.agent/plan.md`'s own
  pre-round no-trailing-newline convention); `.agent/plan.md` reproduces
  it byte-identical (`cmp` exit 0).
- FIELD PAIR FROM (241 bytes) / TO (553 bytes), MARK PAIR FROM (133
  bytes) / TO (160 bytes), TEST PAIR FROM (433 bytes) / TO (1154 bytes)
  — all six include their own trailing `\n` as their real last byte,
  per constraint 4. Applied via `str.replace(FROM, TO, 1)` after
  confirming each FROM's count was exactly 1 in its target file
  (FIELD PAIR and MARK PAIR both against `command_catalog.py`, in that
  order per constraint 7; TEST PAIR against `test_command_catalog.py`).
  The reconstructed files (pre-C2 scratch copy + both `str.replace`
  calls) are byte-identical to the real committed files (G4, above).

## Deviations & assumptions

None. Constraint 4 stated each slice's newline convention explicitly
this round, and it reproduced every stated/measured number exactly
(RECORD5's 3723 bytes, the G2 arithmetic, all three pairs' byte
lengths), so no ambiguity needed resolving or declaring. The bundle's
commit order (C0a, C0b, C1, C2, C3) was followed exactly; the change
set touched exactly the seven declared paths and nothing else
(`apps/cli/commands/job.py`, `packages/orchestration/cost_preview.py`,
`apps/cli/cost_preview_confirm.py` were never opened for writing, and
`tests/cli/test_cost_preview.py` was never created, per constraint 6);
no slice's content looked wrong, so nothing needed declaring under
constraint 1's "apply as written... declare" clause; `.agent/STOP` was
absent at both checkpoints (before the first commit and again before
C3). `job.run` is marked `is_expensive` but still has zero confirm-path
callers after this round, exactly as constraint 6 expects at this stage
— G6's red-proof is what proves the flag is real despite that, not a
"dead code" defect.

## Next

T003 continuation: gather real task-count/class data for `job.run` (see
`packages/orchestration/token_economy.py`'s `TokenBand` classification
and `budget_guard.py`'s `predict_next_task_cost` for the existing
analogous consumer pattern), then wire `confirm_cost_preview()` into
`_cmd_job_run_cycles` (`apps/cli/commands/job.py`). Then goldens for the
preview line, docs, acceptance fixtures, the integration gate, and the
closure sequence (PR, Open PR Gate). No PR exists yet and none is
expected until T003 lands enough of the feature to warrant one.
