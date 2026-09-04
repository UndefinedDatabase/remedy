# Handoff — F114 Cost preview per command, round 8 (books R7's PASS; wires the real `confirm_cost_preview()` call into `job.run`)

## Session

SESSION 2 of feature F114 · round 8 · rounds so far 8.

This round books round 7's PASS verdict into the ledger (RECORD7) and
wires the real `confirm_cost_preview()` call into `_cmd_job_run_cycles`
(`apps/cli/commands/job.py`), gating BOTH the single-cycle short-circuit
and the full `run_cycles` path with one honest "estimate unavailable"
`CostBandEstimate(None, None, ESTIMATE_UNAVAILABLE, {})`. It also
repairs the existing `_cmd_job_run_cycles` call sites in
`tests/orchestration/test_long_run_executor.py` (four call sites) and
`tests/orchestration/test_escalation.py` (two call sites) that would
otherwise trip the new gate under pytest's non-tty stdin, and adds two
new tests directly covering the gate itself (decline path, and the
unavailable-estimate/`yes`-or-`unattended` path).

## Range

Review of `1f9797ab92bcbceea5c54450154edb5ffdb5d4ae..HEAD` (HEAD is
`bcf70fa4` before this handback commit).

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
| G4 THE TEN PAIRS | done | PASS |
| G5 COMPILE AND LINT | done | PASS (ruff denied, as expected) |
| G6 THE RED-PROOF | done | PASS (4 failed / 72 passed, then 76 passed restored) |
| G7 THE SUITES | done | PASS (all twelve measured) |
| G8 THE TREE, THE COMMITS AND THE SWEEP | done | PASS |

## Commits

### 296cf38e F114 R8 C0a: save step block verbatim to .agent/authored/f114-r8.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f114-r8.md` | +461/-0 | transport proof — verbatim `cp` of the supplied step block, new file |

### 76e8b85d F114 R8 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +365/-174 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 400704f0 F114 R8 C1: append RECORD7 to live_review.md, replace plan.md with PLAN8
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD7 (round 7's PASS verdict) — exactly one `\n` then RECORD7's 3698 bytes, no blank-line separator |
| `.agent/plan.md` | +27/-30 | whole-file replace with PLAN8 (first substantive commit, per constraint 2) |

### bcf70fa4 F114 R8 C2: wire confirm_cost_preview into job.run cycles, repair call sites, add gate tests
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job.py` | +19/-0 | SIG PAIR (adds `yes: bool = False` to `_cmd_job_run_cycles`'s signature), GATE PAIR (inserts the real `confirm_cost_preview()` call before `if resolved.max_cycles <= 1:`, gating both branches), HANDLER PAIR (`COMMAND_HANDLERS["job.run"]` now passes `yes=getattr(args, "yes", False)`) |
| `tests/orchestration/test_escalation.py` | +2/-2 | ESC1 (adds `yes=True` to the `cycles=3` call site in `test_without_the_flag_the_same_fixture_leaves_the_decision_open`), ESC2 (adds `yes=True` to the bare `"abc12345"` call site in `test_the_single_pass_is_silent_without_the_flag`) |
| `tests/orchestration/test_long_run_executor.py` | +35/-4 | TLRE1-4 (each adds `yes=True` to an existing `_cmd_job_run_cycles` call site testing capping/multi-cycle/config-cap behavior unrelated to the gate itself), NEWTESTS (appends two new methods to `TestJobRunCommand`: `test_declining_the_cost_preview_returns_without_running`, `test_the_gate_sees_an_unavailable_estimate_and_yes_or_unattended`) |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f114-cost-preview-per-command` → run after
  this handback commit (C3), pushing all five commits of the round.
- No `gh pr` command of any kind was run this round — no PR is created,
  edited or merged this round; constraint 14 states explicitly that the
  real confirm wiring landing does not by itself trigger the Open PR
  Gate, which waits for goldens, docs and the acceptance fixtures.
- One disposable git worktree, created and removed for G6's red-proof
  only, never the primary checkout:
  `git worktree add --detach .remedy-wt/g6-redproof-r8 bcf70fa4a0d84d108991a890cac6002d180f4dce`
  (created, detached HEAD at this round's own C2, `bcf70fa4`) then,
  after the red/green cycle, `git worktree remove --force
  .remedy-wt/g6-redproof-r8` (removed). `git worktree list` immediately
  after shows it gone — see G8.

## Verification

Preconditions, checked before C0a:

```
$ test -f .agent/STOP && echo EXISTS || echo ABSENT
ABSENT
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f114-cost-preview-per-command
$ git log --oneline -n 5
1f9797ab F114 R7 C3: rewrite .agent/handoff.md - round 7 handback
7c25fe18 F114 R7 C2: add --yes arg to job.run and its catalog test (T003 continued)
3d37b1b9 F114 R7 C1: append RECORD6 to live_review.md, replace plan.md with PLAN7
20a61359 F114 R7 C0b: mirror block to .agent/last_block.md
e83309b1 F114 R7 C0a: save step block verbatim to .agent/authored/f114-r7.md
```
Step block was read from `.remedy-wt/r5-review/f114-r8-draft.md`
(supplied path); `cp`'d verbatim, never retyped.

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f114-r8.md .agent/last_block.md
0cf4d30469d4f0510c2184d6f5fef916845d63f3427aa780b42e6a7a4162f960  .agent/authored/f114-r8.md
0cf4d30469d4f0510c2184d6f5fef916845d63f3427aa780b42e6a7a4162f960  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE LEDGER APPEND**:
```
Base size of .agent/live_review.md immediately before C1: 2371519 bytes
Base ends with trailing newline: False
RECORD7 own byte length (extracted from committed authored file): 3698 bytes, 0 internal newlines
base + 1 + len(RECORD7) = 2371519 + 1 + 3698 = 2375218
post-C1 file byte length: 2375218
Match: True (also matches the round instructions' own stated 2375218/2371519/3698 exactly)
```
Second, independent reader — sliced the post-C1 file's bytes from the
measured `base` offset (2371519) to end-of-file and compared against
`"\n" + RECORD7` directly:
```
tail (base..end) == "\n" + RECORD7: True
```
Negative control, scratch copy only (never the tracked file,
`.remedy-wt/scratch/live_review_scratch.md`) — one byte flipped (XOR
0xFF) inside a Python `bytearray` copy of the file at an offset inside
RECORD7's own text, then re-compared against the real `"\n" + RECORD7`:
```
second reader REJECTS the mutated copy: True (mutated tail != "\n" + RECORD7)
```
All PASS.

**G3 THE PLAN**:
```
$ cmp <PLAN8 extracted from committed authored file> .agent/plan.md
(no output — exit 0)
$ wc -l .agent/plan.md
46 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
`cmp` exit 0, `wc -l` 46 (under 50 — PASS), both grep counts 1 — PASS.

**G4 THE TEN PAIRS**:
```
Pre-C2 FROM counts (all measured immediately before C2, in constraint 6's order):
  SIG PAIR FROM (job.py): 1
  GATE PAIR FROM (job.py, re-counted after SIG applied): 1
  HANDLER PAIR FROM (job.py, re-counted after GATE applied): 1
  TLRE1 PAIR FROM (test_long_run_executor.py): 1
  TLRE2 PAIR FROM (re-counted after TLRE1 applied): 1
  TLRE3 PAIR FROM (re-counted after TLRE2 applied): 1
  TLRE4 PAIR FROM (re-counted after TLRE3 applied): 1
  NEWTESTS PAIR FROM (re-counted after TLRE4 applied): 1
  ESC1 PAIR FROM (test_escalation.py): 1
  ESC2 PAIR FROM (re-counted after ESC1 applied): 1
Containment (constraint 5 — NEWTESTS is the one append, the other nine are rewrites):
  SIG PAIR: TO contains FROM: false
  GATE PAIR: TO contains FROM: false
  HANDLER PAIR: TO contains FROM: false
  TLRE1 PAIR: TO contains FROM: false
  TLRE2 PAIR: TO contains FROM: false
  TLRE3 PAIR: TO contains FROM: false
  TLRE4 PAIR: TO contains FROM: false
  NEWTESTS PAIR: TO contains FROM: true
  ESC1 PAIR: TO contains FROM: false
  ESC2 PAIR: TO contains FROM: false
```
Then, extracting each slice from the committed authored file and
applying `str.replace(FROM, TO, 1)`, in constraint 6's order, to a
pre-C2 scratch copy of each target file (`git show HEAD~1:<path>` at
the C1 commit, before any pair was applied):
```
apps/cli/commands/job.py reconstructed matches actual: True
tests/orchestration/test_long_run_executor.py reconstructed matches actual: True
tests/orchestration/test_escalation.py reconstructed matches actual: True
```
All three `cmp` exit 0 — PASS.

**G5 COMPILE AND LINT**:
```
$ python3 -m py_compile apps/cli/commands/job.py tests/orchestration/test_long_run_executor.py tests/orchestration/test_escalation.py
(no output — exit 0)
$ ruff check apps/cli/commands/job.py
This command requires approval
```
`py_compile` exit 0 on all three files — PASS. `ruff check` produced
the session-level denial ("This command requires approval") — reported
verbatim per constraint 11, not assumed; `ruff` is denied to this
session, consistent with rounds 1-7's own notes.

**G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY**:
```
$ git worktree add --detach .remedy-wt/g6-redproof-r8 bcf70fa4a0d84d108991a890cac6002d180f4dce
Preparing worktree (detached HEAD bcf70fa4)
HEAD is now at bcf70fa4 F114 R8 C2: wire confirm_cost_preview into job.run cycles, repair call sites, add gate tests
```
Inside the worktree, GATE PAIR's own new `if not confirm_cost_preview(`
was inverted to `if confirm_cost_preview(` (one-word removal, flips
decline/approve):
```
$ python3 -m pytest tests/orchestration/test_long_run_executor.py -q
4 failed, 72 passed in 0.72s
FAILED tests/orchestration/test_long_run_executor.py::TestJobRunCommand::test_one_cycle_delegates_to_the_existing_single_pass
FAILED tests/orchestration/test_long_run_executor.py::TestJobRunCommand::test_multi_cycle_path_runs_the_loop_after_the_gate
FAILED tests/orchestration/test_long_run_executor.py::TestJobRunCommand::test_declining_the_cost_preview_returns_without_running
FAILED tests/orchestration/test_long_run_executor.py::TestJobRunCommand::test_the_gate_sees_an_unavailable_estimate_and_yes_or_unattended
```
4 failures (> 0) — exactly the two new NEWTESTS methods (their own
monkeypatched `confirm_cost_preview` result is now read backwards) plus
the two pre-existing tests whose call sites pass `yes=True` and rely on
the run actually proceeding (`test_one_cycle_delegates_to_the_existing_single_pass`,
`test_multi_cycle_path_runs_the_loop_after_the_gate` — with the
inversion, a real `yes=True` approval now reads as a decline and the
run never proceeds). The two capped-value tests
(`test_the_flag_is_capped_and_the_operator_is_told`,
`test_a_capped_config_value_names_the_config_key`) still pass because
the "capped to 8" message prints BEFORE the gate runs, unaffected by
the inversion — exactly as expected from GATE PAIR's own placement.
The edit was reverted inside that same worktree
(`if confirm_cost_preview(` back to `if not confirm_cost_preview(`),
then re-run:
```
$ python3 -m pytest tests/orchestration/test_long_run_executor.py -q
76 passed in 0.56s
```
Fully green again (the unmutated control) — 76 passed (74 pre-existing
+ 2 new), matching the primary checkout's own G7 reading for this
suite exactly. Worktree removed:
```
$ git worktree remove --force .remedy-wt/g6-redproof-r8
$ git worktree list
(no g6-redproof-r8 entry — confirmed gone)
```
PASS. The mutation was applied and tested exclusively inside
`.remedy-wt/g6-redproof-r8/`, never the primary checkout
(self_drive_protocol.md guardrail G5); the primary checkout's own
`job.py` was never touched by this gate.

**G7 THE SUITES, SERIALLY, PRIMARY CHECKOUT**:
```
$ python3 -m pytest tests/orchestration/test_long_run_executor.py -q
76 passed in 0.62s
$ python3 -m pytest tests/orchestration/test_escalation.py -q
68 passed in 0.58s
$ python3 -m pytest tests/orchestration/test_resume_kill.py tests/orchestration/test_resume_cli.py -q
42 passed in 1.82s
$ python3 -m pytest tests/test_no_interactive_guard.py -q
6 passed in 1.17s
$ python3 -m pytest tests/test_command_catalog.py tests/cli/test_command_catalog.py -q
45 passed in 0.73s
$ python3 -m pytest tests/docs/ -q
295 passed in 0.45s
$ python3 -m pytest tests/orchestration/test_roadmap_index.py -q
30 passed in 0.35s
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.59s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.58s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.48s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.31s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.75s
```
`test_long_run_executor.py` reads 76 passed — matches the gate's own
stated expectation exactly (74 existing + 2 new).
`test_escalation.py` reads 68 passed — matches the gate's own stated
expectation exactly (unchanged count, only `yes=True` added to two
call sites). `test_resume_kill.py` + `test_resume_cli.py` together read
42 passed — matches the gate's own stated expectation exactly
(unaffected, per constraint 10). `test_no_interactive_guard.py` reads 6
passed — matches the gate's own stated expectation exactly (`apps/cli`
stays outside its scan scope). `test_command_catalog.py` +
`tests/cli/test_command_catalog.py` (45 = 22 + 23),
`tests/docs/` (295), `test_roadmap_index.py` (30), `tests/ui_server/`
(515), `test_test_runner.py` (52), `test_resource_safety.py` (21),
`test_integrity_gate.py` (16) and `test_golden_path.py` (canary, 42)
are all IDENTICAL to round 7's own stated figures in RECORD7 — nothing
moved outside this round's own two new tests. These are the REAL,
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
/home/decodeux/Repos/remedy                                  bcf70fa4 [feature/f114-cost-preview-per-command]
(plus 8 pre-existing, unrelated .remedy-wt/job-* worktrees from other
job runs — none created or touched by this round's G6, confirmed by
name: none is "g6-redproof-r8")
```
Per-commit insertion cross-check (`git show --numstat`, `+` column
only) against this handback's own Commits table above — all cells
match:

| Commit | File | numstat `+` | Table `+` | Match |
|---|---|---|---|---|
| 296cf38e (C0a) | `.agent/authored/f114-r8.md` | 461 | 461 | yes |
| 76e8b85d (C0b) | `.agent/last_block.md` | 365 | 365 | yes |
| 400704f0 (C1) | `.agent/live_review.md` | 2 | 2 | yes |
| 400704f0 (C1) | `.agent/plan.md` | 27 | 27 | yes |
| bcf70fa4 (C2) | `apps/cli/commands/job.py` | 19 | 19 | yes |
| bcf70fa4 (C2) | `tests/orchestration/test_escalation.py` | 2 | 2 | yes |
| bcf70fa4 (C2) | `tests/orchestration/test_long_run_executor.py` | 35 | 35 | yes |

C3's own numbers go to neither this table nor a round report, per G8's
own instruction.

Staleness sweep, one entry per file this round touched:

| File | Stale? | Why |
|---|---|---|
| `.agent/authored/f114-r8.md` | NOT stale | immutable historical stamp of this round's instructions |
| `.agent/last_block.md` | NOT stale | current mirror of this round's block; accurate until round 9 overwrites it |
| `.agent/live_review.md` | NOT stale | RECORD7 books round 7's real PASS verdict, append-only ledger |
| `.agent/plan.md` | NOT stale | reflects F114 round 8's actual current step and real next steps |
| `apps/cli/commands/job.py` | NOT stale | `confirm_cost_preview()` is now a real, load-bearing call in `_cmd_job_run_cycles` — G6's red-proof proves it, not assumed |
| `tests/orchestration/test_long_run_executor.py` | NOT stale | four repaired call sites plus two new tests directly exercise the new gate |
| `tests/orchestration/test_escalation.py` | NOT stale | two repaired call sites remain accurate to the unattended/blocked behavior they test |
| `.agent/handoff.md` | N/A | this handback itself, written last, freshest by construction |

Outside the change set: no NEW stale sentence was found this round.
Rounds 2 and 3's own `.agent/context.md` declarations (lines 29 and 36)
stand and are not repeated here, per constraint 12's explicit
instruction. `docs/roadmap/features/T3_F114.md`'s line describing
"estimate unavailable" + confirm-above-threshold is a target-design
description that this round's wiring now REALIZES rather than
contradicts, so it is not stale. `docs/roadmap/STATUS.md`'s F114 line
(`- [~] F114`) is untouched and still correctly claimed (in progress).

## Authored-text proofs

- `.agent/authored/f114-r8.md` (copied via `cp` from
  `.remedy-wt/r5-review/f114-r8-draft.md`, never retyped) sha256
  `0cf4d30469d4f0510c2184d6f5fef916845d63f3427aa780b42e6a7a4162f960`,
  confirmed identical to the source via `sha256sum` before staging, and
  again matching `.agent/last_block.md` after C0b (G1).
- All twelve slices (RECORD7, PLAN8, and the ten pairs' FROM/TO) were
  extracted from the COMMITTED `.agent/authored/f114-r8.md` by a Python
  script reading delimiter indices (`<<<BEGIN ...>>>` /
  `<<<END ...>>>`), taking the exact substring strictly between each
  pair of markers — never by hand-retyping (constraint 1).
- Per constraint 4: RECORD7 and PLAN8 each had their one structural
  trailing `\n` (the byte separating the slice's last content line from
  its own `<<<END ...>>>` marker line) stripped before use, since that
  byte belongs to marker-line formatting, not the slice; all ten pairs'
  FROM/TO texts were used with that same separator byte RESTORED as
  their own trailing `\n` — the true last byte of the matched line
  group — per constraint 4's explicit statement that the pairs (unlike
  RECORD7/PLAN8) carry their own trailing newline.
- RECORD7: 3698 bytes, 0 internal newlines, matches the round
  instructions' own stated figure exactly; appended to
  `.agent/live_review.md` as exactly one `\n` + RECORD7 (G2, above).
- PLAN8: 2129 bytes, no trailing newline (matches `.agent/plan.md`'s own
  pre-round no-trailing-newline convention); `.agent/plan.md` reproduces
  it byte-identical (`cmp` exit 0).
- SIG PAIR FROM (156 bytes) / TO (179 bytes), GATE PAIR FROM (359
  bytes) / TO (887 bytes), HANDLER PAIR FROM (260 bytes) / TO (301
  bytes), TLRE1 FROM (48) / TO (58), TLRE2 FROM (60) / TO (70), TLRE3
  FROM (59) / TO (69), TLRE4 FROM (53) / TO (63), NEWTESTS FROM (95) /
  TO (1424), ESC1 FROM (67) / TO (77), ESC2 FROM (48) / TO (58) — all
  twenty texts include their own trailing `\n` as their real last byte,
  per constraint 4. Applied via `str.replace(FROM, TO, 1)` after
  confirming each FROM's count was exactly 1 in its target file
  immediately before use (re-counted after each preceding pair in the
  same file, per constraint 6). The reconstructed files (pre-C2 scratch
  copy + `str.replace` in constraint 6's order) are byte-identical to
  the real committed files (G4, above).

## Deviations & assumptions

None. Every one of the ten pairs' classification (nine rewrites, one
append — NEWTESTS) matched constraint 5's own stated classification
exactly, verified mechanically both before and after applying each
pair (FROM-in-TO containment checked with FROM and TO compared
correctly, not against themselves — the round 6 self-check typo this
block's own constraint 5 warns about did not recur here). The bundle's
commit order (C0a, C0b, C1, C2, C3) was followed exactly, and within
C2 the pairs were applied in constraint 6's stated order (SIG, GATE,
HANDLER for `job.py`; TLRE1-4, NEWTESTS for
`test_long_run_executor.py`; ESC1, ESC2 for `test_escalation.py`); the
change set touched exactly the eight declared paths and nothing else
(`apps/cli/command_catalog.py`, `packages/orchestration/cost_preview.py`,
`apps/cli/cost_preview_confirm.py`, `tests/orchestration/test_resume_kill.py`
and `tests/orchestration/test_resume_cli.py` were never opened for
writing, per constraint 10). No slice's content looked wrong, so
nothing needed declaring under constraint 1's "apply as written...
declare" clause. `.agent/STOP` was absent at both checkpoints (before
the first commit and again before C3). Every non-interactive `job.run`
call site in the two repaired test files now needs `--yes`, `yes=True`
or `unattended=True` or it exits via the gate's own decline path — this
is a real, by-design behavior change flagged in PLAN8's own Risks
section, not a defect.

## Next

T003 continuation (round 9 or later, no fixed round assigned yet):
goldens for the preview line and docs for `--yes` and the cost-preview
behavior on `job.run`; consider marking other expensive-sounding
commands ("rerunning subtrees", "long explanations") `is_expensive` —
only `job.run` carries it so far. Then acceptance fixtures, the
integration gate, then the closure sequence (PR, Open PR Gate) — no PR
exists yet and none is expected until T003 lands enough of the feature
to warrant one. Session note: round 8, session 2 — this is the 3rd
delegated round of session 2 (rounds 6, 7, 8), within the operator's
4-5 default; a new session should open before round 9 if this session's
context is running low.
