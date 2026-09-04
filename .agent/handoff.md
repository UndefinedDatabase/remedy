# Handoff — F114 Cost preview per command, round 9 (books R8's PASS; adds real acceptance tests for job.run's cost-preview behavior)

## Session

SESSION 2 of feature F114 · round 9 · rounds so far 9.

This round books round 8's PASS verdict into the ledger (RECORD8) and
adds `tests/cli/test_cost_preview.py` — the feature doc's own suggested
acceptance-test path (`docs/roadmap/features/T3_F114.md:66`), empty
until now. Unlike round 8's own gate tests (which mock
`confirm_cost_preview` itself to isolate the wiring), these five tests
exercise the REAL `confirm_cost_preview` end to end through `job.run`:
a non-tty pipe without `--yes` exits with code 2 and names `job.run` in
its hint, `--yes` and `--unattended` both proceed through the real gate
without a tty, and the printed line always carries its basis label. No
production code changes this round.

## Range

Review of `64de02a6..HEAD` (HEAD is `c18a416c` before this handback
commit).

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
| G4 THE NEW FILE | done | PASS |
| G5 COMPILE AND LINT | done | PASS (ruff denied, as expected) |
| G6 THE RED-PROOF | done | PASS (2 failed / 3 passed, then 5 passed restored) |
| G7 THE SUITES | done | PASS (all twelve measured) |
| G8 THE TREE, THE COMMITS AND THE SWEEP | done | PASS |

## Commits

### a871cd4f F114 R9 C0a: save step block verbatim to .agent/authored/f114-r9.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f114-r9.md` | +287/-0 | transport proof — verbatim `cp` of the supplied step block, new file |

### cab855b8 F114 R9 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +159/-333 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 947a1474 F114 R9 C1: append RECORD8 to live_review.md, replace plan.md with PLAN9
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD8 (round 8's PASS verdict) — exactly one `\n` then RECORD8's 3962 bytes, no blank-line separator |
| `.agent/plan.md` | +25/-25 | whole-file replace with PLAN9 (first substantive commit, per constraint 2) |

### c18a416c F114 R9 C2: add acceptance tests for job.run cost-preview behavior (T003 continued)
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_cost_preview.py` | +75/-0 | TESTMODULE, new file — five acceptance tests exercising the REAL `confirm_cost_preview` end to end through `job.run` (non-tty exit-2 + hint text, `--yes` proceeds, `--unattended` proceeds, basis label always printed) |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f114-cost-preview-per-command` → run after
  this handback commit (C3), pushing all five commits of the round.
- No `gh pr` command of any kind was run this round — no PR is created,
  edited or merged this round; constraint 10 states explicitly that a
  new acceptance-test file does not by itself trigger the Open PR Gate,
  which waits for docs and the remaining acceptance items.
- One disposable git worktree, created and removed for G6's red-proof
  only, never the primary checkout:
  `git worktree add .remedy-wt/r9-g6-redproof c18a416c68d6d2edabab9fba34f08cb7005e8f34`
  (created, detached HEAD at this round's own C2, `c18a416c`) then,
  after the red/green cycle, `git worktree remove --force
  .remedy-wt/r9-g6-redproof` (removed). `git worktree list` immediately
  after shows it gone — see G8.

## Verification

Preconditions, checked before C0a and again before C3:

```
$ test -f .agent/STOP && echo EXISTS || echo ABSENT
ABSENT (checked twice: before the first commit, and again before C3)
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f114-cost-preview-per-command
$ git log --oneline -n 5
64de02a6 F114 R8 C3: rewrite .agent/handoff.md - round 8 handback
bcf70fa4 F114 R8 C2: wire confirm_cost_preview into job.run cycles, repair call sites, add gate tests
400704f0 F114 R8 C1: append RECORD7 to live_review.md, replace plan.md with PLAN8
76e8b85d F114 R8 C0b: mirror block to .agent/last_block.md
296cf38e F114 R8 C0a: save step block verbatim to .agent/authored/f114-r8.md
```
Step block was read from `.remedy-wt/r5-review/f114-r9-draft.md`
(supplied path); `cp`'d verbatim, never retyped.

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f114-r9.md .agent/last_block.md
ce56e9ec686400c21b009c758a3309a813cd5f5705e768450332d530c56ab4a7  .agent/authored/f114-r9.md
ce56e9ec686400c21b009c758a3309a813cd5f5705e768450332d530c56ab4a7  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE LEDGER APPEND**:
```
Base size of .agent/live_review.md immediately before C1: 2375218 bytes
Base ends with trailing newline: False
RECORD8 own byte length (extracted from committed authored file): 3962 bytes, 0 internal newlines
base + 1 + len(RECORD8) = 2375218 + 1 + 3962 = 2379181
post-C1 file byte length: 2379181
Match: True (also matches the round instructions' own stated
2379181/2375218/3962 exactly)
```
Second, independent reader — sliced the post-C1 file's bytes from the
measured `base` offset (2375218) to end-of-file and compared against
`"\n" + RECORD8` directly:
```
tail (base..end) == "\n" + RECORD8: True
```
Negative control, scratch copy only (never the tracked file, a
`bytearray` held in memory, never written to `.agent/live_review.md`)
— one byte flipped (XOR 0xFF) at an offset inside RECORD8's own text
(50 bytes into the RECORD8 region), then re-compared against the real
`"\n" + RECORD8`:
```
second reader REJECTS the mutated copy: True (mutated tail != "\n" + RECORD8)
```
All PASS.

**G3 THE PLAN**:
```
$ cmp <PLAN9 extracted from committed authored file> .agent/plan.md
(no output — exit 0)
$ wc -l .agent/plan.md
46 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
`cmp` exit 0, `wc -l` 46 (under 50 — PASS), both grep counts 1 — PASS.

**G4 THE NEW FILE**:
```
$ cmp <TESTMODULE extracted from committed authored file> tests/cli/test_cost_preview.py
(no output — exit 0)
$ wc -c tests/cli/test_cost_preview.py
2965 tests/cli/test_cost_preview.py
```
`cmp` exit 0 (written with the Write tool as an exact byte copy, then
verified — a "copyfile", never a text-extraction-and-reflow, per
constraint 5), byte length 2965 — matches the round instructions' own
stated expectation exactly — PASS.

**G5 COMPILE AND LINT**:
```
$ python3 -m py_compile tests/cli/test_cost_preview.py
(no output — exit 0)
$ ruff check tests/cli/test_cost_preview.py
This command requires approval
```
`py_compile` exit 0 — PASS. `ruff check` produced the session-level
denial ("This command requires approval") — reported verbatim per
constraint 7, not assumed; `ruff` is denied to this session, consistent
with every prior round's own notes.

**G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY**:
```
$ git worktree add .remedy-wt/r9-g6-redproof c18a416c68d6d2edabab9fba34f08cb7005e8f34
Preparing worktree (detached HEAD c18a416c)
HEAD is now at c18a416c F114 R9 C2: add acceptance tests for job.run cost-preview behavior (T003 continued)
```
Inside the worktree, `_cmd_job_run_cycles`'s own existing
`if not confirm_cost_preview(` (landed in round 8, unmodified this
round) was inverted to `if confirm_cost_preview(` (one-word removal,
flips decline/approve — the same mutation round 8's own G6 used):
```
$ python3 -m pytest tests/cli/test_cost_preview.py -q
2 failed, 3 passed in 0.28s
FAILED tests/cli/test_cost_preview.py::TestJobRunCostPreviewAcceptance::test_yes_flag_proceeds_through_the_real_gate_without_a_tty
FAILED tests/cli/test_cost_preview.py::TestJobRunCostPreviewAcceptance::test_unattended_proceeds_through_the_real_gate_without_a_tty
```
2 failures (> 0) — exactly the two named in the round instructions:
`test_yes_flag_proceeds_through_the_real_gate_without_a_tty` and
`test_unattended_proceeds_through_the_real_gate_without_a_tty` (both
rely on the real gate letting the run proceed; with the inversion, a
real approval now reads as a decline). The other three tests
(non-tty-exit-2, non-tty-hint-text, basis-label) still pass because
they exercise the decline path or a `yes=True` call whose print
statement runs before the gate — unaffected by the inversion. The edit
was reverted inside that same worktree (`if confirm_cost_preview(`
back to `if not confirm_cost_preview(`; `git diff --stat` in the
worktree read empty, confirming an exact revert), then re-run:
```
$ python3 -m pytest tests/cli/test_cost_preview.py -q
5 passed in 0.22s
```
Fully green again (the unmutated control) — 5 passed, matching the
primary checkout's own G7 reading for this suite exactly. Worktree
removed:
```
$ git worktree remove --force .remedy-wt/r9-g6-redproof
$ git worktree list
(no r9-g6-redproof entry — confirmed gone)
```
PASS. The mutation was applied and tested exclusively inside
`.remedy-wt/r9-g6-redproof/`, never the primary checkout
(self_drive_protocol.md guardrail G5); the primary checkout's own
`job.py` was never touched by this gate.

**G7 THE SUITES, SERIALLY, PRIMARY CHECKOUT**:
```
$ python3 -m pytest tests/cli/test_cost_preview.py -q
5 passed in 0.23s
$ python3 -m pytest tests/orchestration/test_long_run_executor.py -q
76 passed in 0.54s
$ python3 -m pytest tests/orchestration/test_escalation.py -q
68 passed in 0.52s
$ python3 -m pytest tests/test_no_interactive_guard.py -q
6 passed in 1.19s
$ python3 -m pytest tests/test_command_catalog.py tests/cli/test_command_catalog.py -q
45 passed in 0.73s
$ python3 -m pytest tests/docs/ -q
295 passed in 0.45s
$ python3 -m pytest tests/orchestration/test_roadmap_index.py -q
30 passed in 0.36s
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.62s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.59s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.54s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.30s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.77s
```
`test_cost_preview.py` reads 5 passed — a brand new file, matches the
gate's own stated expectation exactly. All eleven remaining counts —
`test_long_run_executor.py` (76), `test_escalation.py` (68),
`test_no_interactive_guard.py` (6), `test_command_catalog.py` +
`tests/cli/test_command_catalog.py` (45), `tests/docs/` (295),
`test_roadmap_index.py` (30), `tests/ui_server/` (515),
`test_test_runner.py` (52), `test_resource_safety.py` (21),
`test_integrity_gate.py` (16) and `test_golden_path.py` (canary, 42) —
are all IDENTICAL to round 8's own stated figures in RECORD8, exactly
as expected since no production code changed this round. These are the
REAL, measured counts, not forced to any assumption.
`tests/ui_server/`, `test_test_runner.py`, `test_resource_safety.py`
and `test_integrity_gate.py` were run as all four named, not fewer, per
the gate's own instruction.

**G8 THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain
(empty — checked immediately before C3 staged)
$ git ls-files .remedy-wt
(no output — nothing under .remedy-wt/ is ever committed)
$ git worktree list
/home/decodeux/Repos/remedy                                  c18a416c [feature/f114-cost-preview-per-command]
(plus 8 pre-existing, unrelated .remedy-wt/job-* worktrees from other
job runs — none created or touched by this round's G6, confirmed by
name: none is "r9-g6-redproof")
```
Per-commit insertion cross-check (`git show --numstat`, `+` column
only) against this handback's own Commits table above — all cells
match:

| Commit | File | numstat `+` | Table `+` | Match |
|---|---|---|---|---|
| a871cd4f (C0a) | `.agent/authored/f114-r9.md` | 287 | 287 | yes |
| cab855b8 (C0b) | `.agent/last_block.md` | 159 | 159 | yes |
| 947a1474 (C1) | `.agent/live_review.md` | 2 | 2 | yes |
| 947a1474 (C1) | `.agent/plan.md` | 25 | 25 | yes |
| c18a416c (C2) | `tests/cli/test_cost_preview.py` | 75 | 75 | yes |

C3's own numbers go to neither this table nor a round report, per G8's
own instruction.

Staleness sweep, one entry per file this round touched:

| File | Stale? | Why |
|---|---|---|
| `.agent/authored/f114-r9.md` | NOT stale | immutable historical stamp of this round's instructions |
| `.agent/last_block.md` | NOT stale | current mirror of this round's block; accurate until round 10 overwrites it |
| `.agent/live_review.md` | NOT stale | RECORD8 books round 8's real PASS verdict, append-only ledger |
| `.agent/plan.md` | NOT stale | reflects F114 round 9's actual current step and real next steps |
| `tests/cli/test_cost_preview.py` | NOT stale | five real acceptance tests exercise the real `confirm_cost_preview` gate through `job.run` — G6's red-proof proves it, not assumed |
| `.agent/handoff.md` | N/A | this handback itself, written last, freshest by construction |

Outside the change set: no NEW stale sentence was found this round.
Rounds 2 and 3's own `.agent/context.md` declarations (lines 29 and 36)
stand and are not repeated here, per constraint 8's explicit
instruction. `docs/roadmap/features/T3_F114.md:66`'s line ("Suggested
tests: tests/cli/test_cost_preview.py.") is now REALIZED by this
round's new file rather than made stale by it — the suggestion is
fulfilled, not contradicted. `docs/roadmap/STATUS.md`'s F114 line
(`- [~] F114`) is untouched and still correctly claimed (in progress).

## Authored-text proofs

- `.agent/authored/f114-r9.md` (copied via `cp` from
  `.remedy-wt/r5-review/f114-r9-draft.md`, never retyped) sha256
  `ce56e9ec686400c21b009c758a3309a813cd5f5705e768450332d530c56ab4a7`,
  confirmed identical to the source via `sha256sum` before staging, and
  again matching `.agent/last_block.md` after C0b (G1).
- All three slices (RECORD8, PLAN9, TESTMODULE) were extracted from the
  COMMITTED `.agent/authored/f114-r9.md` by a Python script reading
  delimiter indices (`<<<BEGIN ...>>>` / `<<<END ...>>>`), taking the
  exact substring strictly between each pair of markers — never by
  hand-retyping (constraint 1).
- Per constraint 4: RECORD8 and PLAN9 each had their one structural
  trailing `\n` (the byte separating the slice's last content line from
  its own `<<<END ...>>>` marker line) stripped before use, since that
  byte belongs to marker-line formatting, not the slice. TESTMODULE's
  own trailing `\n` was KEPT as its true last byte — a real Python
  source file's own structural suffix, not marker-line formatting, per
  constraint 4's explicit statement.
- RECORD8: 3962 bytes, 0 internal newlines, matches the round
  instructions' own stated figure exactly; appended to
  `.agent/live_review.md` as exactly one `\n` + RECORD8 (G2, above).
- PLAN9: 2243 bytes, no trailing newline (matches `.agent/plan.md`'s own
  pre-round no-trailing-newline convention); `.agent/plan.md` reproduces
  it byte-identical (`cmp` exit 0).
- TESTMODULE: 2965 bytes, its own trailing `\n` kept as the true last
  byte, matches the round instructions' own stated figure exactly;
  written via the Write tool as a whole-file copy (never a
  text-extraction-and-reflow), then verified byte-identical against the
  extracted slice with `cmp` (G4, above).

## Deviations & assumptions

None. The slice extraction, the newline-convention handling (constraint
4), the whole-file copyfile-and-cmp for TESTMODULE (constraint 5), and
the G6 red-proof's isolation inside a disposable worktree
(self_drive_protocol.md guardrail G5) all matched the round
instructions exactly. No slice's content looked wrong, so nothing
needed declaring under constraint 1's "apply as written... declare"
clause. `.agent/STOP` was absent at both checkpoints (before the first
commit and again before C3). No production code file was opened for
writing this round — the six paths named in constraint 6
(`apps/cli/commands/job.py`, `packages/orchestration/cost_preview.py`,
`apps/cli/cost_preview_confirm.py`, `apps/cli/command_catalog.py`,
`tests/orchestration/test_long_run_executor.py`,
`tests/orchestration/test_escalation.py`) were never touched, confirmed
by the change set (only `.agent/authored/f114-r9.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`tests/cli/test_cost_preview.py` and this handback were written). The
bundle's commit order (C0a, C0b, C1, C2, C3) was followed exactly.

## Next

T003 continuation (round 10 or later, no fixed round assigned yet):
docs for `--yes` and the cost-preview behavior on `job.run` (no
dedicated CLI reference doc file exists yet for job commands — needs
its own investigation of `docs/README.md`'s structure rules before
writing anything); consider marking other expensive-sounding commands
("rerunning subtrees", "long explanations") `is_expensive` — only
`job.run` carries it so far; real cost bands for `job.run` still do not
exist and a future round needs real task-class data to replace the
unavailable estimate. Then acceptance fixtures continue, the
integration gate, then the closure sequence (PR, Open PR Gate) — no PR
exists yet and none is expected until enough of the feature lands to
warrant one. Session note: round 9, session 2 — this is the 4th
delegated round of session 2 (rounds 6, 7, 8, 9), at the operator's
4-5 default; a new session should open before round 10 if this
session's context is running low.
