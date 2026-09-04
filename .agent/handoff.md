# Handoff — F114 Cost preview per command, round 7 (books R6's PASS; continues T003 — job.run's `--yes` arg)

## Session

SESSION 2 of feature F114 · round 7 · rounds so far 7.

This round books round 6's PASS verdict into the ledger (RECORD6) and
continues T003: adds a `--yes` `ArgDef` to `job.run`'s own
`CommandEntry` (`apps/cli/command_catalog.py`), mirroring `loop.run`'s
own `--yes` shape, so the future `confirm_cost_preview()` call has a
real flag to skip its prompt. A catalog test confirms the arg exists
and is a flag. Wiring `confirm_cost_preview()` into
`_cmd_job_run_cycles` itself is NOT this round (constraint 6) — that is
round 8, once this round's `--yes` arg exists for it to read.

## Range

Review of `a886072b844566fb40757c036f8750e3a4f39090..HEAD` (HEAD is
`7c25fe18` before this handback commit).

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
| G4 THE TWO PAIRS | done | PASS |
| G5 COMPILE AND LINT | done | PASS (ruff denied, as expected) |
| G6 THE RED-PROOF | done | PASS (1 failed / 21 passed, then 22 passed restored) |
| G7 THE SUITES | done | PASS (all 10 measured) |
| G8 THE TREE, THE COMMITS AND THE SWEEP | done | PASS |

## Commits

### e83309b1 F114 R7 C0a: save step block verbatim to .agent/authored/f114-r7.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f114-r7.md` | +270/-0 | transport proof — verbatim `cp` of the supplied step block, new file |

### 20a61359 F114 R7 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +148/-211 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 3d37b1b9 F114 R7 C1: append RECORD6 to live_review.md, replace plan.md with PLAN7
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD6 (round 6's PASS verdict) — exactly one `\n` then RECORD6's 3735 bytes, no blank-line separator |
| `.agent/plan.md` | +29/-29 | whole-file replace with PLAN7 (first substantive commit, per constraint 2) |

### 7c25fe18 F114 R7 C2: add --yes arg to job.run and its catalog test (T003 continued)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | +4/-0 | YES_ARG PAIR — inserts a new `ArgDef("--yes", ...)` between the existing `--unattended` `ArgDef` and `_JSON_OPT` in `job.run`'s own args tuple |
| `tests/test_command_catalog.py` | +6/-0 | YES_TEST PAIR — new `test_job_run_has_a_yes_flag_to_skip_the_cost_confirmation` method inserted between `test_job_run_is_expensive` and `class TestCatalogSensitivity:` |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f114-cost-preview-per-command` → run after
  this handback commit (C3), pushing all five commits of the round.
- No `gh pr` command of any kind was run this round — no PR is created,
  edited or merged this round; constraint 10 states explicitly that a
  schema-only `--yes` arg does not by itself trigger the Open PR Gate.
- One disposable git worktree, created and removed for G6's red-proof
  only, never the primary checkout:
  `git worktree add .remedy-wt/r7-redproof HEAD` (created, detached HEAD
  at this round's own C2, `7c25fe18`) then, after the red/green cycle,
  `git worktree remove --force .remedy-wt/r7-redproof` (removed).
  `git worktree list` immediately after shows it gone — see G8.

## Verification

Preconditions, checked before C0a:

```
$ test -f .agent/STOP && echo EXISTS || echo absent
absent
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f114-cost-preview-per-command
$ git log --oneline -n 5
a886072b F114 R6 C3: rewrite .agent/handoff.md - round 6 handback
10c7b324 F114 R6 C2: mark is_expensive field and job.run (T003 first slice)
8f79f31b F114 R6 C1: append RECORD5 to live_review.md, replace plan.md with PLAN6
b025ca6e F114 R6 C0b: mirror block to .agent/last_block.md
6b415998 F114 R6 C0a: save step block verbatim to .agent/authored/f114-r6.md
```
Step block was read from `.remedy-wt/r5-review/f114-r7-draft.md`
(supplied path); `cp`'d verbatim, never retyped.

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f114-r7.md .agent/last_block.md
69c8767c2530932c17d8c432ff47487cc0868e13dade4c0986a2891ed3ff0b94  .agent/authored/f114-r7.md
69c8767c2530932c17d8c432ff47487cc0868e13dade4c0986a2891ed3ff0b94  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE LEDGER APPEND**:
```
Base size of .agent/live_review.md immediately before C1: 2367783 bytes
Base ends with trailing newline: False
RECORD6 own byte length (extracted from committed authored file): 3735 bytes, 0 internal newlines
base + 1 + len(RECORD6) = 2367783 + 1 + 3735 = 2371519
post-C1 file byte length: 2371519
Match: True (also matches the round instructions' own stated 2371519/2367783/3735 exactly)
```
Second, independent reader — sliced the post-C1 file's bytes from the
measured `base` offset (2367783) to end-of-file and compared against
`"\n" + RECORD6` directly:
```
tail (base..end) == "\n" + RECORD6: True
```
Negative control, scratch copy only (never the tracked file) — one byte
flipped (XOR 0xFF) inside a Python `bytearray` copy of the file at an
offset inside RECORD6's own text, then re-compared against the real
`"\n" + RECORD6`:
```
second reader REJECTS the mutated copy: True (mutated tail != "\n" + RECORD6)
```
All PASS.

**G3 THE PLAN**:
```
$ cmp <PLAN7 extracted from committed authored file> .agent/plan.md
(no output — exit 0)
$ wc -l .agent/plan.md
49 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
`cmp` exit 0, `wc -l` 49 (under 50 — PASS), both grep counts 1 — PASS.

**G4 THE TWO PAIRS**:
```
Pre-C2 FROM counts:
  YES_ARG PAIR FROM (command_catalog.py): 1
  YES_TEST PAIR FROM (test_command_catalog.py): 1
Containment (constraint 5 — both are rewrites):
  YES_ARG PAIR: TO contains FROM: false
  YES_TEST PAIR: TO contains FROM: false
```
Then, extracting each slice from the committed authored file and
applying `str.replace(FROM, TO, 1)` to a pre-C2 scratch copy
(`git show <C1-sha>:apps/cli/command_catalog.py` and
`git show <C1-sha>:tests/test_command_catalog.py`) of each target file:
```
command_catalog.py reconstructed matches actual: True
test_command_catalog.py reconstructed matches actual: True
```
Both `cmp` exit 0 — PASS. Direct read of the landed file confirms the
new `ArgDef("--yes", ...)` sits between `job.run`'s own `--unattended`
`ArgDef` and `_JSON_OPT`, and the new test method sits between
`test_job_run_is_expensive` and `class TestCatalogSensitivity:`.

**G5 COMPILE AND LINT**:
```
$ python3 -m py_compile apps/cli/command_catalog.py tests/test_command_catalog.py
(no output — exit 0)
$ ruff check apps/cli/command_catalog.py tests/test_command_catalog.py
This command requires approval
```
`py_compile` exit 0 on both files — PASS. `ruff check` produced the
session-level denial ("This command requires approval") — reported
verbatim per constraint 7, not assumed; `ruff` is denied to this
session, consistent with rounds 1-6's own notes.

**G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY**:
```
$ git worktree add .remedy-wt/r7-redproof HEAD
Preparing worktree (detached HEAD 7c25fe18)
HEAD is now at 7c25fe18 F114 R7 C2: add --yes arg to job.run and its catalog test (T003 continued)
```
Inside the worktree, the new `ArgDef("--yes", ...)` line group was
removed from `job.run`'s own args tuple via
`str.replace(YES_ARG_TO, YES_ARG_FROM, 1)` (reverting it to round 6's
shape):
```
$ python3 -m pytest tests/test_command_catalog.py -q
1 failed, 21 passed in 0.22s
FAILED tests/test_command_catalog.py::TestCatalogExpensive::test_job_run_has_a_yes_flag_to_skip_the_cost_confirmation
```
1 failure (> 0), exactly the test named in the gate's own expectation —
proving the `--yes` arg on `job.run` is real, reachable catalog data,
not dead code. The `ArgDef` was restored inside that same worktree via
`str.replace(YES_ARG_FROM, YES_ARG_TO, 1)`, then re-run:
```
$ python3 -m pytest tests/test_command_catalog.py -q
22 passed in 0.20s
```
Fully green again (the unmutated control) — 22 passed, matching the
primary checkout's own G7 reading for this suite. Worktree removed:
```
$ git worktree remove --force .remedy-wt/r7-redproof
$ git worktree list
(no r7-redproof entry — confirmed gone)
```
PASS. The mutation was applied and tested exclusively inside
`.remedy-wt/r7-redproof/`, never the primary checkout
(self_drive_protocol.md guardrail G5); the primary checkout's own
`command_catalog.py` was never touched by this gate.

**G7 THE SUITES, SERIALLY, PRIMARY CHECKOUT**:
```
$ python3 -m pytest tests/test_command_catalog.py -q
22 passed in 0.22s
$ python3 -m pytest tests/cli/test_command_catalog.py -q
23 passed in 0.73s
$ python3 -m pytest tests/orchestration/test_job_task_runner.py -q
214 passed in 78.33s
$ python3 -m pytest tests/docs/ -q
295 passed in 0.46s
$ python3 -m pytest tests/orchestration/test_roadmap_index.py -q
30 passed in 0.36s
$ python3 -m pytest tests/ui_server/ -q
515 passed in 33.60s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.71s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.47s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.30s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 21.05s
```
`test_command_catalog.py` reads 22 passed — matches the gate's own
stated expectation exactly (21 existing + 1 new). `tests/cli/test_command_catalog.py`
(23), `test_job_task_runner.py` (214), `tests/docs/` (295),
`test_roadmap_index.py` (30), `tests/ui_server/` (515),
`test_test_runner.py` (52), `test_resource_safety.py` (21),
`test_integrity_gate.py` (16) and `test_golden_path.py` (canary, 42)
are all IDENTICAL to round 6's own stated figures in RECORD6 — nothing
moved outside this round's own one new test. These are the REAL,
measured counts, not forced to any assumption. `tests/ui_server/`,
`test_test_runner.py`, `test_resource_safety.py` and
`test_integrity_gate.py` were run as all four named, not fewer, per the
gate's own instruction.

**G8 THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain
(empty — checked immediately before C3 staged)
$ git ls-files .remedy-wt
(no output — nothing under .remedy-wt/ is ever committed)
$ git worktree list
/home/decodeux/Repos/remedy                                  7c25fe18 [feature/f114-cost-preview-per-command]
(plus 8 pre-existing, unrelated .remedy-wt/job-* worktrees from other
job runs — none created or touched by this round's G6, confirmed by
name: none is "r7-redproof")
```
Per-commit insertion cross-check (`git show --numstat`, `+` column
only) against this handback's own Commits table above — all cells
match:

| Commit | File | numstat `+` | Table `+` | Match |
|---|---|---|---|---|
| e83309b1 (C0a) | `.agent/authored/f114-r7.md` | 270 | 270 | yes |
| 20a61359 (C0b) | `.agent/last_block.md` | 148 | 148 | yes |
| 3d37b1b9 (C1) | `.agent/live_review.md` | 2 | 2 | yes |
| 3d37b1b9 (C1) | `.agent/plan.md` | 29 | 29 | yes |
| 7c25fe18 (C2) | `apps/cli/command_catalog.py` | 4 | 4 | yes |
| 7c25fe18 (C2) | `tests/test_command_catalog.py` | 6 | 6 | yes |

C3's own numbers go to neither this table nor a round report, per G8's
own instruction.

Staleness sweep, one entry per file this round touched:

| File | Stale? | Why |
|---|---|---|
| `.agent/authored/f114-r7.md` | NOT stale | immutable historical stamp of this round's instructions |
| `.agent/last_block.md` | NOT stale | current mirror of this round's block; accurate until round 8 overwrites it |
| `.agent/live_review.md` | NOT stale | RECORD6 books round 6's real PASS verdict, append-only ledger |
| `.agent/plan.md` | NOT stale | reflects F114 round 7's actual current step and real next steps |
| `apps/cli/command_catalog.py` | NOT stale | `job.run`'s `--yes` arg is live and tested; zero real-caller reads yet, by design (constraint 6 — round 8 wires the confirm call) |
| `tests/test_command_catalog.py` | NOT stale | the new test directly covers the new `--yes` arg's existence and flag-ness, passing |
| `.agent/handoff.md` | N/A | this handback itself, written last, freshest by construction |

Outside the change set: no NEW stale sentence was found this round.
Rounds 2 and 3's own `.agent/context.md` declarations (lines 29 and 36)
stand and are not repeated here, per constraint 8's explicit
instruction. `docs/roadmap/features/T3_F114.md`'s T003 line still
describes a task-list item in progress, not a done/not-done claim, so
this round's further partial T003 progress does not make it stale.
`docs/roadmap/STATUS.md`'s F114 line (`- [~] F114`) is untouched and
still correctly claimed (in progress).

## Authored-text proofs

- `.agent/authored/f114-r7.md` (copied via `cp` from
  `.remedy-wt/r5-review/f114-r7-draft.md`, never retyped) sha256
  `69c8767c2530932c17d8c432ff47487cc0868e13dade4c0986a2891ed3ff0b94`,
  confirmed identical to the source via `cmp` before staging, and again
  matching `.agent/last_block.md` after C0b (G1).
- All six slices (RECORD6, PLAN7, YES_ARG PAIR FROM/TO, YES_TEST PAIR
  FROM/TO) were extracted from the COMMITTED `.agent/authored/f114-r7.md`
  by a Python script reading delimiter indices (`<<<BEGIN ...>>>` /
  `<<<END ...>>>`), taking the exact substring strictly between each
  pair of markers — never by hand-retyping (constraint 1).
- Per constraint 4: RECORD6 and PLAN7 each had their one structural
  trailing `\n` (the byte separating the slice's last content line from
  its own `<<<END ...>>>` marker line) stripped before use, since that
  byte belongs to marker-line formatting, not the slice; YES_ARG PAIR
  and YES_TEST PAIR (both FROM and TO) were used exactly as extracted,
  keeping their own trailing `\n` as the true last byte of the matched
  line group.
- RECORD6: 3735 bytes, 0 internal newlines, matches the round
  instructions' own stated figure exactly; appended to
  `.agent/live_review.md` as exactly one `\n` + RECORD6 (G2, above).
- PLAN7: 2475 bytes, no trailing newline (matches `.agent/plan.md`'s own
  pre-round no-trailing-newline convention); `.agent/plan.md` reproduces
  it byte-identical (`cmp` exit 0).
- YES_ARG PAIR FROM (380 bytes) / TO (672 bytes), YES_TEST PAIR FROM
  (140 bytes) / TO (501 bytes) — all four include their own trailing
  `\n` as their real last byte, per constraint 4. Applied via
  `str.replace(FROM, TO, 1)` after confirming each FROM's count was
  exactly 1 in its target file. The reconstructed files (pre-C2 scratch
  copy + `str.replace`) are byte-identical to the real committed files
  (G4, above).

## Deviations & assumptions

None. Constraint 4 stated each slice's newline convention explicitly
this round, and it reproduced every stated/measured number exactly
(RECORD6's 3735 bytes, the G2 arithmetic 2371519, both pairs' byte
lengths and containment results), so no ambiguity needed resolving or
declaring. The bundle's commit order (C0a, C0b, C1, C2, C3) was
followed exactly; the change set touched exactly the seven declared
paths and nothing else (`apps/cli/commands/job.py`,
`packages/orchestration/cost_preview.py`,
`apps/cli/cost_preview_confirm.py` were never opened for writing, per
constraint 6); no slice's content looked wrong, so nothing needed
declaring under constraint 1's "apply as written... declare" clause;
`.agent/STOP` was absent at both checkpoints (before the first commit
and again before C3). `job.run` now carries a `--yes` arg with zero
real-caller reads after this round, exactly as constraint 6 expects at
this stage — G6's red-proof is what proves the arg is real catalog data
despite that, not a "dead code" defect.

## Next

T003 continuation (round 8): import `confirm_cost_preview` and
`CostBandEstimate` into `apps/cli/commands/job.py`; call it once near
the top of `_cmd_job_run_cycles`, before either the single-cycle
short-circuit (`_cmd_run_next_task_local`) or the full `run_cycles`
path, with `basis="estimate_unavailable"` and
`yes=(yes_flag or unattended)` — `--unattended` maps to skip-prompt
because the feature doc requires unattended runs to never prompt and
rely on budgets instead (T3_F114.md's own explicit rule). Then goldens
for the preview line, docs, acceptance fixtures, the integration gate,
and the closure sequence (PR, Open PR Gate). No PR exists yet and none
is expected until T003 lands enough of the feature to warrant one.
