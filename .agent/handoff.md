# Handoff — F114 Cost preview per command, round 5 (books R4's PASS; completes T002 — cost_preview_confirm.py + tests)

## Session

SESSION 1 of feature F114 · round 5 · rounds so far 5.

Same loop session as rounds 1-4. This round books round 4's PASS verdict
into the ledger (RECORD4) and completes T002: ships the shared module
`apps/cli/cost_preview_confirm.py` (`render_estimate_line`,
`confirm_cost_preview`, `EXIT_USAGE`) and its 12 tests in
`tests/cli/test_cost_preview_confirm.py`. No real command calls it yet —
that is T003, a separate future round. Per PLAN5's own Next Steps note,
this is round 5 of the 4-5 default; a fresh session is a natural
consideration next, per amend0827 rule 6.

## Range

Review of `99157a070a2d7291332c16071246e8960cfffc34..HEAD` (HEAD is
`27c3acc4da827e52d23e618a8587cbfef0f8dc5f` before this handback commit).

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
| G4 THE TWO NEW FILES | done | PASS |
| G5 COMPILE AND LINT | done | PASS (ruff denied, as expected) |
| G6 THE RED-PROOF | done | PASS (6 failed / 12 green) |
| G7 THE SUITES | done | PASS (all 12 measured) |
| G8 THE TREE, THE COMMITS AND THE SWEEP | done | PASS |

## Commits

### 487a8ac8 F114 R5 C0a: save step block verbatim to .agent/authored/f114-r5.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f114-r5.md` | +393/-0 | transport proof — verbatim `cp` of the supplied step block, new file |

### 3f705774 F114 R5 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +282/-277 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 67a4a73c F114 R5 C1: append RECORD4 to live_review.md, replace plan.md with PLAN5
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD4 (round 4's PASS verdict) — exactly one `\n` then RECORD4's 3781 bytes, no blank-line separator |
| `.agent/plan.md` | +17/-19 | whole-file replace with PLAN5 (first substantive commit, per constraint 2) |

### 27c3acc4 F114 R5 C2: ship cost_preview_confirm.py (T002 complete) and its tests
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/cost_preview_confirm.py` | +72/-0 | new file, MODULE slice, whole-file `Write`-tool copy — `render_estimate_line`, `confirm_cost_preview`, `EXIT_USAGE` |
| `tests/cli/test_cost_preview_confirm.py` | +110/-0 | new file, TESTMODULE slice, whole-file `Write`-tool copy — 12 tests across 6 classes |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f114-cost-preview-per-command` → run after
  this handback commit (C3), pushing all five commits of the round.
- No `gh pr` command of any kind was run this round — no PR is created
  or touched this round; the block's Bundle/Constraints make no mention
  of PR creation, and constraint 11 states explicitly that T002
  completing does not by itself trigger the Open PR Gate.
- One disposable git worktree, created and removed for G6's red-proof
  only, never the primary checkout:
  `git worktree add --detach .remedy-wt/f114-r5-g6-mutation 27c3acc4`
  (created, detached HEAD at this round's own C2) then, after the
  red/green cycle, `git worktree remove --force
  .remedy-wt/f114-r5-g6-mutation` (removed). `git worktree list`
  immediately after shows it gone — see G8.

## Verification

Preconditions, checked before C0a:

```
$ git log --oneline -1
99157a07 F114 R4 C3: rewrite .agent/handoff.md - round 4 handback
$ git status --porcelain
(empty)
$ sha256sum .remedy-wt/f114_r5_block.txt
c029bef2dc53322be7602053545274fccf93df1905b0ba12bb496d4a461438a5  .remedy-wt/f114_r5_block.txt
$ wc -l .remedy-wt/f114_r5_block.txt; wc -c .remedy-wt/f114_r5_block.txt
392 .remedy-wt/f114_r5_block.txt
22188 .remedy-wt/f114_r5_block.txt
```
`wc -l` reads 392 (newline-terminated-line count) against the round
instructions' own stated "393 lines" — the file has 393 physical lines
with no trailing newline on the last one, so `wc -l` (which counts `\n`
bytes) reads one less; `wc -c` matches the stated 22188 bytes exactly,
and the sha256 matches the stated digest exactly — same pattern rounds
2-4 all hit. `.agent/STOP` checked absent both before the first commit
and again before C3 (`ls .agent/STOP` → "No such file or directory",
both times).

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f114-r5.md .agent/last_block.md
c029bef2dc53322be7602053545274fccf93df1905b0ba12bb496d4a461438a5  .agent/authored/f114-r5.md
c029bef2dc53322be7602053545274fccf93df1905b0ba12bb496d4a461438a5  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE LEDGER APPEND**:
```
Base size of .agent/live_review.md immediately before C1: 2360277 bytes
Base ends with trailing newline: False
RECORD4 own byte length (extracted from committed authored file): 3781 bytes, 0 internal newlines
base + 1 + len(RECORD4) = 2360277 + 1 + 3781 = 2364059
post-C1 file byte length: 2364059
Match: True (also matches the round instructions' own stated 2364059/2360277/3781 exactly)
```
Second, independent reader — sliced the post-C1 file's bytes from the
measured `base` offset (2360277) to end-of-file and compared against
`"\n" + RECORD4` directly:
```
tail (base..end) == "\n" + RECORD4: True
```
Negative control, scratch copy only (never the tracked file) — one byte
flipped inside a Python `bytearray` copy of the post-C1 file (offset 100
bytes into RECORD4's own text region, XORed with 0xFF), then
re-compared against the real `"\n" + RECORD4`:
```
second reader REJECTS the mutated copy: True (mutated tail != "\n" + RECORD4)
```
All PASS.

**G3 THE PLAN**:
```
$ cmp <PLAN5 extracted from committed authored file> .agent/plan.md
(no output — exit 0)
$ wc -l .agent/plan.md
37 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
`cmp` exit 0, `wc -l` 37 (under 50 — PASS), both grep counts 1 — PASS.

**G4 THE TWO NEW FILES**:
```
$ cmp <MODULE extracted from committed authored file> apps/cli/cost_preview_confirm.py
(no output — exit 0)
$ cmp <TESTMODULE extracted from committed authored file> tests/cli/test_cost_preview_confirm.py
(no output — exit 0)
$ wc -c apps/cli/cost_preview_confirm.py tests/cli/test_cost_preview_confirm.py
2541 apps/cli/cost_preview_confirm.py
4744 tests/cli/test_cost_preview_confirm.py
```
Both `cmp` exit 0 — PASS. Byte lengths 2541 and 4744, matching the round
instructions' own stated expectations exactly. Per constraint 4's
explicit statement, MODULE/TESTMODULE were extracted with their own
real trailing `\n` restored as a structural suffix (extraction script
at `.remedy-wt/extract_slices.py` joins marker-to-marker lines with
`\n` and then appends one more `\n` for these two slices only, never
for RECORD4/PLAN5) — confirmed byte-exact by `cmp` against the written
files, not assumed.

**G5 COMPILE AND LINT**:
```
$ python3 -m py_compile apps/cli/cost_preview_confirm.py
(no output — exit 0)
$ python3 -m py_compile tests/cli/test_cost_preview_confirm.py
(no output — exit 0)
$ ruff check apps/cli/cost_preview_confirm.py tests/cli/test_cost_preview_confirm.py
Permission to use Bash has been denied. IMPORTANT: You *may* attempt to
accomplish this action using other tools that might naturally be used
to accomplish this goal [...] If you believe this capability is
essential to complete the user's request, STOP and explain to the user
what you were trying to do and why you need this permission. Let the
user decide how to proceed.
```
`py_compile` exit 0 on both new files — PASS. `ruff check` produced the
exact session-level refusal text above (reported verbatim per
constraint 8, not assumed) — `ruff` is denied to this session,
consistent with rounds 1-4's own notes.

**G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY**:
```
$ git worktree add --detach .remedy-wt/f114-r5-g6-mutation 27c3acc4
Preparing worktree (detached HEAD 27c3acc4)
HEAD is now at 27c3acc4 F114 R5 C2: ...
```
Inside the worktree, `confirm_cost_preview`'s own
`estimate.band_usd_high > confirm_above_usd` line changed to use `<`
instead of `>` (a one-character edit):
```
$ python3 -m pytest tests/cli/test_cost_preview_confirm.py -q
6 failed, 6 passed in 0.23s
FAILED tests/cli/test_cost_preview_confirm.py::TestUnderThreshold::test_under_threshold_proceeds_without_any_prompt
FAILED tests/cli/test_cost_preview_confirm.py::TestUnderThreshold::test_under_threshold_never_touches_stdin
FAILED tests/cli/test_cost_preview_confirm.py::TestOverThresholdWithYes::test_yes_skips_the_prompt_and_proceeds
FAILED tests/cli/test_cost_preview_confirm.py::TestOverThresholdNonTty::test_non_tty_exits_with_usage_code_never_hangs
FAILED tests/cli/test_cost_preview_confirm.py::TestOverThresholdNonTty::test_non_tty_never_calls_input
FAILED tests/cli/test_cost_preview_confirm.py::TestOverThresholdTty::test_tty_declining_returns_false_without_raising
```
6 failures (> 0), spanning under-threshold, --yes, non-tty and tty
decline behaviour — the mutated `<` inverts which estimates count as
"expensive", so the under/over-threshold boundary and the tty-decline
path both flip, proving `is_expensive`'s comparison is real, reachable
code exercised by real tests. Edit reverted inside the same worktree:
```
$ python3 -m pytest tests/cli/test_cost_preview_confirm.py -q
12 passed in 0.19s
```
Fully green again (the unmutated control) — 12 passed, matching the
primary checkout's own G7 reading for this suite. Worktree removed:
```
$ git worktree remove --force .remedy-wt/f114-r5-g6-mutation
$ git worktree list
(no .remedy-wt/f114-r5-g6-mutation entry — confirmed gone)
```
PASS. The mutation was applied and tested exclusively inside
`.remedy-wt/f114-r5-g6-mutation/`, never the primary checkout
(self_drive_protocol.md guardrail G5); the primary checkout's own
`cost_preview_confirm.py` was never touched by this gate.

**G7 THE SUITES, SERIALLY, PRIMARY CHECKOUT**:
```
$ python3 -m pytest tests/cli/test_cost_preview_confirm.py -q
12 passed in 0.21s
$ python3 -m pytest tests/cli/test_loop_cmd.py -q
14 passed in 0.24s
$ python3 -m pytest tests/test_no_interactive_guard.py -q
6 passed in 1.22s
$ python3 -m pytest tests/orchestration/test_cost_preview.py -q
19 passed in 0.24s
$ python3 -m pytest tests/orchestration/test_config.py -q
81 passed in 0.31s
$ python3 -m pytest tests/docs/ -q
295 passed in 0.45s
$ python3 -m pytest tests/orchestration/test_roadmap_index.py -q
30 passed in 0.36s
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.42s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.66s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.41s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.29s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.66s
```
`test_cost_preview_confirm.py` reads 12 passed — a brand new file,
matching the gate's own stated expectation exactly. `test_loop_cmd.py`
reads 14 passed — this round's new module reuses its tty-mocking shape
but does not touch `loop_cmd.py` itself (constraint 7), so this is a
first-time baseline reading for this suite in F114's own G7 lists, not
a moved-count check. `test_no_interactive_guard.py` reads 6 passed —
IDENTICAL to every prior round's own reading; `apps/cli` is outside its
`_GUARDED_PACKAGES` scan scope (per the gate's own note), so the new
`cost_preview_confirm.py` file does not change this suite's count at
all, confirmed by direct measurement rather than assumed.
`test_cost_preview.py` (19), `test_config.py` (81), `tests/docs/`
(295), `test_roadmap_index.py` (30), `tests/ui_server/` (515),
`test_test_runner.py` (52), `test_resource_safety.py` (21),
`test_integrity_gate.py` (16) and `test_golden_path.py` (canary, 42)
are all IDENTICAL to round 4's own stated figures — nothing moved
outside this round's own six new tests (12 in the new file, plus
`test_loop_cmd.py`'s pre-existing 14 now also in scope). These are the
REAL, measured counts, not forced to any assumption. `tests/ui_server/`,
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
/home/decodeux/Repos/remedy                                  27c3acc4 [feature/f114-cost-preview-per-command]
(plus 8 pre-existing, unrelated .remedy-wt/job-* worktrees from other
job runs — none created or touched by this round's G6, confirmed by
name: none is "f114-r5-g6-mutation")
```
Per-commit insertion cross-check (`git show --numstat`, `+` column
only) against this handback's own Commits table above — all cells
match:

| Commit | File | numstat `+` | Table `+` | Match |
|---|---|---|---|---|
| 487a8ac8 (C0a) | `.agent/authored/f114-r5.md` | 393 | 393 | yes |
| 3f705774 (C0b) | `.agent/last_block.md` | 282 | 282 | yes |
| 67a4a73c (C1) | `.agent/live_review.md` | 2 | 2 | yes |
| 67a4a73c (C1) | `.agent/plan.md` | 17 | 17 | yes |
| 27c3acc4 (C2) | `apps/cli/cost_preview_confirm.py` | 72 | 72 | yes |
| 27c3acc4 (C2) | `tests/cli/test_cost_preview_confirm.py` | 110 | 110 | yes |

C3's own numbers go to neither this table nor a round report, per G8's
own instruction.

Staleness sweep, one entry per file this round touched:

| File | Stale? | Why |
|---|---|---|
| `.agent/authored/f114-r5.md` | NOT stale | immutable historical stamp of this round's instructions |
| `.agent/last_block.md` | NOT stale | current mirror of this round's block; accurate until round 6 overwrites it |
| `.agent/live_review.md` | NOT stale | RECORD4 books round 4's real PASS verdict, append-only ledger |
| `.agent/plan.md` | NOT stale | reflects F114 round 5's actual current step and real next steps |
| `apps/cli/cost_preview_confirm.py` | NOT stale | `render_estimate_line`/`confirm_cost_preview`/`EXIT_USAGE` are live and tested; no production caller yet, by design (T003 wires a real command, per constraint 6) |
| `tests/cli/test_cost_preview_confirm.py` | NOT stale | 12 new tests directly cover the new module, all passing |
| `.agent/handoff.md` | N/A | this handback itself, written last, freshest by construction |

Outside the change set: no NEW stale sentence was found this round.
`.agent/context.md` line 36 ("No `cost_preview.py` or
expensive-command registry exists today...") and line 29 (the
`budget_guard.py:482-484` reference) — round 2's and round 3's own
declared staleness — both stand unrepeated, per constraint 9's explicit
instruction not to repeat them. `docs/roadmap/features/T3_F114.md`
lines 43/45 describe T002/T003 as task-list items, not a done/not-done
claim, so T002 completing this round does not make that file stale.
`docs/roadmap/STATUS.md`'s F114 line (`- [~] F114`) is untouched and
still correctly claimed (in progress — T003 remains).

## Authored-text proofs

- `.agent/authored/f114-r5.md` (copied via `cp`, never retyped) sha256
  `c029bef2dc53322be7602053545274fccf93df1905b0ba12bb496d4a461438a5` at
  22188 bytes, 393 lines — matches the round instructions' own stamp
  exactly (verified before C0a and again after commit, via `sha256sum`
  against the scratch source at `.remedy-wt/f114_r5_block.txt`).
- `.agent/last_block.md` after C0b: same sha256 as above — confirmed
  equal (G1).
- All four slices (RECORD4, PLAN5, MODULE, TESTMODULE) were extracted
  from the COMMITTED `.agent/authored/f114-r5.md` by a Python script
  (`.remedy-wt/extract_slices.py`) reading delimiter indices
  (`<<<BEGIN ...>>>` / `<<<END ...>>>`), splitting the file on `\n`
  bytes and re-joining the lines strictly between each pair of markers
  — never by hand-retyping (constraint 1). Per constraint 4's explicit
  statement, RECORD4/PLAN5 were taken as the naive marker-to-marker
  join with no added trailing newline, while MODULE/TESTMODULE each had
  one `\n` appended back as their own real structural suffix — no
  ambiguity needed resolving this round.
- RECORD4: 3781 bytes, 0 internal newlines, matches the round
  instructions' own stated figure exactly; appended to
  `.agent/live_review.md` as exactly one `\n` + RECORD4 (G2, above).
- PLAN5: 1602 bytes, no trailing newline (matches `.agent/plan.md`'s own
  pre-round no-trailing-newline convention); `.agent/plan.md` reproduces
  it byte-identical (`cmp` exit 0).
- MODULE: 2541 bytes including its own trailing `\n`, matches the round
  instructions' own stated figure exactly; `apps/cli/cost_preview_confirm.py`
  (written via the `Write` tool with these exact bytes, then verified —
  a copyfile, not a text-extraction-and-reflow) reproduces it
  byte-identical (`cmp` exit 0).
- TESTMODULE: 4744 bytes including its own trailing `\n`, matches the
  round instructions' own stated figure exactly;
  `tests/cli/test_cost_preview_confirm.py` (same `Write`-tool copyfile
  method) reproduces it byte-identical (`cmp` exit 0).

## Deviations & assumptions

None. Constraint 4 stated each slice's newline convention explicitly
this round, and it reproduced every stated/measured number exactly
(RECORD4's 3781 bytes, the G2 arithmetic, MODULE's 2541 bytes,
TESTMODULE's 4744 bytes), so no ambiguity needed resolving or
declaring. The bundle's commit order (C0a, C0b, C1, C2, C3) was
followed exactly; the change set touched exactly the seven declared
paths and nothing else (`packages/orchestration/cost_preview.py`,
`packages/orchestration/config.py`, `apps/cli/commands/loop_cmd.py` and
`apps/cli/command_catalog.py` were never opened for writing, per
constraints 6/7); no slice's content looked wrong, so nothing needed
declaring under constraint 1's "apply as written... declare" clause;
`.agent/STOP` was absent at both checkpoints; the two new files have
zero production callers, exactly as constraint 6 expects at this stage
— G6's red-proof is what proves the code is real despite that, not a
"dead code" defect.

## Next

T003: mark expensive commands in `apps/cli/command_catalog.py`, wire
them to `confirm_cost_preview()`, goldens for the preview lines, docs —
the first round with a real production caller for either new module.
Then acceptance fixtures, the integration gate, and the closure
sequence (PR, Open PR Gate). No PR exists yet and none is expected
until T003 lands enough of the feature to warrant one.
