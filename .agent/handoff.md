# Handoff — F262 List commands v2 (dates, sort, filter), round 17 (T003 batch 5: blocker.list/decision.list wiring)

## Session

SESSION 6 of feature F262 · round 17 · rounds so far 17.

Round 17 books round 16's PASS verdict (GATE16) into the ledger, and
continues T003 with its fifth batch: `blocker.list` and `decision.list`
are both wired to `packages/orchestration/list_options.py`'s
`apply_list_options` with `default_sort_field="created_at"`. Both are
job-scoped commands returning typed rows (`StopReason`/`HumanDecision`)
whose `created_at` is already a plain ISO string (no `.isoformat()`
call needed, unlike `project.list`'s datetime object). Neither store's
existing order carries operational meaning, and neither has an
order-asserting test in its own test file, so no D2-style opt-out was
needed for either. Both commands dispatch via a lambda
(`"blocker.list": lambda args: _cmd_blocker_list(...)`,
`"decision.list": lambda args: _cmd_decision_list(...)`), so — like
`project.list` in round 16 — BOTH the handler body and the dispatch
site needed a pair each: PAIR B1/B2 for blocker.py, PAIR D1/D2 for
decision.py. One production commit covering all four touched files
(two source files, two test files), one commit.

## Range

Review of `94eb67c91cb9c1f28c7f1285d4d6411a475c23e4..db7997ff84200e9b80eb6d4cd3004879288941ee`.
That is C0a through C3 (five content commits before this handback —
C0a, C0b, C1, C2, C3). This handback (C4) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `94eb67c91cb9c1f28c7f1285d4d6411a475c23e4`, branch matched `feature/f262-list-commands-v2`, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r17.md` saved verbatim, 288 lines, 19469 bytes |
| C0b | done | mirrored to `.agent/last_block.md` via `shutil.copyfile`, sha256 `1cc828a4f4b3e0a792406ae032bc30ca4c2847e0ef808ebd25dddec5031eb90b` identical to C0a's file (confirmed by `sha256sum` on both files, one digest twice) |
| C1 | done | GATE16 appended to `.agent/live_review.md` byte-exact (base 2462543 + `\n` + GATE16 2567 bytes = 2465111, confirmed by direct Python byte read before and after write) |
| C2 | done | PAIR B1 + PAIR B2 (`apps/cli/commands/blocker.py`), PAIR D1 + PAIR D2 (`apps/cli/commands/decision.py`), TEST T1 append (`tests/cli/test_blocker_cmd.py`), TEST T2 append (`tests/cli/test_decision_cmd.py`) — four files, one commit; no follow-up fixes needed |
| C3 | done | PLAN18 applied to `.agent/plan.md`, whole-file replace, verified byte-for-byte equal (2159 == 2159 bytes, binary mode) |
| C4 (this handback) | done | |
| G1 (py_compile, 4 files) | done | printed `OK` via the declared substitution (see Deviations) |
| G2 (pytest, C2's two test files) | done | 8 passed (4 pre-existing + 4 new) |
| G3 (canary: combined 5-suite invocation) | done | 646 passed, unmoved from prior baseline (515+52+21+16+42) |
| G4 (sha256sum transport) | done | one identical digest, twice |
| G5 (live_review.md byte forensics) | done | before 2462543, after 2465111, matching exactly |
| G6 (plan.md byte-for-byte) | done | 2159 bytes, byte-for-byte equal to PLAN18 |
| G7 (git status --porcelain, twice) | done | empty before C0a, empty immediately before C4 |
| G8 (git ls-files .remedy-wt) | done | empty output — nothing tracked under `.remedy-wt/` |

## Commits

### 138b543fb5c4bc2f28303514d3e107ec9a4aa295 F262 R17 C0a: save step block to .agent/authored/f262-r17.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r17.md` | +289/-0 | transport artifact — verbatim copy of the round's step block, new file |

### 741fcd513eab085206032e1520cbde4435a3bc49 F262 R17 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +197/-105 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### c43293f3dce520d8e2f48f52d47cd9a6a39159a4 F262 R17 C1: append GATE16 to live_review.md - books round 16's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE16, `\n` + GATE16's own bytes appended to the base file |

### b0c12ba5b8d668640a28c4948e3a7b9c1caea94e F262 R17 C2: T003 batch 5 - blocker.list/decision.list wiring
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/blocker.py` | +26/-0 | PAIR B1: `_cmd_blocker_list` gains sort/desc/since/until/limit params and `apply_list_options` wiring with `default_sort_field="created_at"`; PAIR B2: `"blocker.list"` dispatch lambda forwards the new flags via `getattr` |
| `apps/cli/commands/decision.py` | +31/-1 | PAIR D1: `_cmd_decision_list` gains sort/desc/since/until/limit params and `apply_list_options` wiring with `default_sort_field="created_at"`; PAIR D2: `"decision.list"` dispatch lambda forwards the new flags via `getattr` |
| `tests/cli/test_blocker_cmd.py` | +22/-0 | `import pytest` added; TEST T1 (append: `TestBlockerListOptions` with `test_limit_caps_returned_blockers`, `test_unknown_sort_field_exits_nonzero`) |
| `tests/cli/test_decision_cmd.py` | +26/-0 | `import pytest` added; TEST T2 (append: `TestDecisionListOptions` with `test_limit_caps_returned_decisions`, `test_unknown_sort_field_exits_nonzero`) |

### db7997ff84200e9b80eb6d4cd3004879288941ee F262 R17 C3: replace plan.md with PLAN18
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +19/-26 | whole-file replace with PLAN18, byte-for-byte verified |

### (this handback commit, C4)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once) — numbers not tabled here; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f262-list-commands-v2` — runs
  immediately after this commit; result reported in the closing
  message, not here, since it happens after this file is committed. No
  `gh pr` command of any kind was run (forbidden this round: no PR, no
  merge, no Open PR Gate, no `main` touched).

## Verification

Preconditions, checked before C0a:
```
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f262-list-commands-v2
$ git rev-parse HEAD
94eb67c91cb9c1f28c7f1285d4d6411a475c23e4
$ ls .agent/STOP
No such file or directory
```
All four confirmed.

**TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f262-r17.md .agent/last_block.md
1cc828a4f4b3e0a792406ae032bc30ca4c2847e0ef808ebd25dddec5031eb90b  .agent/authored/f262-r17.md
1cc828a4f4b3e0a792406ae032bc30ca4c2847e0ef808ebd25dddec5031eb90b  .agent/last_block.md
```
One digest, twice — PASS.

**LEDGER APPEND, GATE16 (live_review.md), byte-forensics**:
```
base size immediately before C1: 2462543 bytes
GATE16 own byte length: 2567
GATE16 internal newline count: 0
base + 1 + GATE16_length = 2465111
post-C1 file real byte length = 2465111
match: True
file still ends with no trailing newline: confirmed
```
Confirmed by direct Python byte read before and after the write
(`pathlib.Path.write_bytes`, not a shell append), plus `git show
--numstat c43293f3` reading `2  1  .agent/live_review.md`, consistent
with the prior line losing its "no newline at end of file" status and
one new single-line region being appended.

**PRODUCTION PAIRS, READ AND COUNTED (B1, B2, D1, D2)**:
```
B1 (blocker.py, _cmd_blocker_list signature+body): FROM count before 1
B2 (blocker.py, "blocker.list" dispatch lambda): FROM count before 1
D1 (decision.py, _cmd_decision_list signature+body): FROM count before 1
D2 (decision.py, "decision.list" dispatch lambda): FROM count before 1
```
All four confirmed at exactly 1 occurrence in their target file before
being applied (constraint 4's re-confirmation, using each file's
CURRENT on-disk content, read via the Read tool then re-counted with
`str.count` in Python). `sys` was confirmed already imported at module
scope in both `blocker.py` and `decision.py` (line 6, `import sys` in
each) before applying B1/D1 — no new import of `sys` was added in
either file. `StopReason.created_at`/`.status`/`.severity` and
`HumanDecision.created_at`/`.status`/`.severity` were confirmed to
exist on both dataclasses (`packages/orchestration/stop_reasons.py`,
`packages/orchestration/decision_queue.py`) before wiring the
`sort_fields` maps.

Full diff, C2 (`b0c12ba5`), all four files, was read in full before
writing this handback (`git show b0c12ba5 -- apps/cli/commands/blocker.py
apps/cli/commands/decision.py tests/cli/test_blocker_cmd.py
tests/cli/test_decision_cmd.py`). Every hunk matched its named
PAIR/TEST exactly: no other lines in any of the four files were
touched — every other handler in `blocker.py`
(`_cmd_blocker_show`, `_cmd_blocker_resolve`) and `decision.py`
(`_cmd_decision_show`, `_cmd_decision_resolve`, `_cmd_decision_explain`,
`parse_answer_options`, `_create_mission_for_job`, `AnswerParseError`)
and every other dispatch entry in both `COMMAND_HANDLERS` dicts are
untouched, confirmed by reading the full diff. `git show --numstat
b0c12ba5` reads `26  0  apps/cli/commands/blocker.py`, `31  1
apps/cli/commands/decision.py`, `22  0  tests/cli/test_blocker_cmd.py`,
`26  0  tests/cli/test_decision_cmd.py` — matching the Commits table
above exactly.

```
$ python3 -m py_compile apps/cli/commands/blocker.py apps/cli/commands/decision.py tests/cli/test_blocker_cmd.py tests/cli/test_decision_cmd.py
```
This exact multi-arg invocation form has been denied by the Bash
tool's sandbox permission in prior rounds (per the operator's declared
known quirk); not retried this round, substituted directly with the
declared equivalent:
```
$ python3 -c "import py_compile; py_compile.compile('apps/cli/commands/blocker.py', doraise=True); py_compile.compile('apps/cli/commands/decision.py', doraise=True); py_compile.compile('tests/cli/test_blocker_cmd.py', doraise=True); py_compile.compile('tests/cli/test_decision_cmd.py', doraise=True); print('OK')"
OK
```
`doraise=True` means any `SyntaxError` would have raised and been
visible; `OK` printed for all four files, equivalent to exit 0.

Ruff not attempted this round — same refusal shape recorded in every
prior round's handback; not re-attempted since the outcome is already
known and constraint 3 treats it as a non-blocker either way.

**PYTEST, C2's two files**:
```
$ python3 -m pytest tests/cli/test_blocker_cmd.py tests/cli/test_decision_cmd.py -q
........                                                                 [100%]
8 passed in 0.22s
```
Matches the block's own prediction exactly: 4 pre-existing + 4 new = 8.

**THE STATE READERS AND THE CANARY, run as ONE combined invocation
per this round's block**:
```
$ python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q
........................................................................ [ 11%]
........................................................................ [ 22%]
........................................................................ [ 33%]
........................................................................ [ 44%]
........................................................................ [ 55%]
........................................................................ [ 66%]
........................................................................ [ 78%]
........................................................................ [ 89%]
......................................................................   [100%]
646 passed in 70.54s (0:01:10)
```
646 = 515 + 52 + 21 + 16 + 42, matching GATE16's stated per-suite
baseline exactly. Not moved, as expected: this round's change set
names no path any of these five suites should be sensitive to.

**THE PLAN, BYTE-FOR-BYTE (constraint: byte-exact whole-file replace)**:
```
authored PLAN18 slice length: 2159 bytes (binary mode, no trailing newline)
written .agent/plan.md length: 2159 bytes (binary mode)
EQUAL (bytes == bytes): True
```
Whole-file replace applied via a direct binary write
(`pathlib.Path.write_bytes` from a Python-constructed byte buffer with
the trailing newline stripped from the source string before encoding),
then re-verified exact in BINARY mode: 2159 == 2159, `True`.

**AUTHORED-TEXT PROOFS** (GATE16 and PLAN18 as embedded in the
committed `.agent/authored/f262-r17.md`, compared disk-to-disk against
what was actually written):
```
gate16_from_authored length: 2567
gate16_in_live (last 2567 bytes of live_review.md) length: 2567
MATCH gate16: True

plan18_from_authored_block (stripped) length: 2159
plan.md length: 2159
MATCH plan18: True
```
Both reviewer-authored texts applied this round (GATE16 into
`live_review.md`, PLAN18 into `plan.md`) are byte-identical to the
text embedded in the committed `.agent/authored/f262-r17.md` slice —
the same file that was written directly from this prompt's own GATE16
and PLAN18 text, so the two are identical by construction, and were
re-verified byte-for-byte per the numbers above.

**THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain   (immediately before C4 staged)
(empty)
$ git ls-files .remedy-wt
(no output)
```
Tree clean before C4, nothing under `.remedy-wt/` tracked.

Per-commit numstat cross-check against this handback's own Commits
table:
```
$ git show --numstat 138b543f
289  0    .agent/authored/f262-r17.md
$ git show --numstat 741fcd51
197  105  .agent/last_block.md
$ git show --numstat c43293f3
2    1    .agent/live_review.md
$ git show --numstat b0c12ba5
26   0    apps/cli/commands/blocker.py
31   1    apps/cli/commands/decision.py
22   0    tests/cli/test_blocker_cmd.py
26   0    tests/cli/test_decision_cmd.py
$ git show --numstat db7997ff
19   26   .agent/plan.md
```
Every path and every insertion/deletion count matches the Commits
table exactly.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r17.md` — NOT stale. Immutable verbatim record
  of this round's own step block.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE16's
  content describes round 16's own verified facts.
- `apps/cli/commands/blocker.py` — NOT stale. Matches PAIR B1 and PAIR
  B2 exactly; full diff read and confirmed.
- `apps/cli/commands/decision.py` — NOT stale. Matches PAIR D1 and
  PAIR D2 exactly; full diff read and confirmed.
- `tests/cli/test_blocker_cmd.py` — NOT stale. Matches TEST T1
  exactly; all tests pass.
- `tests/cli/test_decision_cmd.py` — NOT stale. Matches TEST T2
  exactly; all tests pass.
- `.agent/plan.md` — NOT stale. Freshly written PLAN18 content
  accurately describes round 17's actual state.

Constraint check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` Already false as of round 2 and remains outside this
round's declared change set too, unchanged from prior rounds' notes.

## Authored-text proofs

For every reviewer-authored text applied this round — GATE16
(`.agent/live_review.md`) and PLAN18 (`.agent/plan.md`) — the
disk-to-disk comparison against the committed
`.agent/authored/f262-r17.md` slice is reported above under
Verification's "AUTHORED-TEXT PROOFS" heading: both matched
byte-for-byte (GATE16: 2567/2567 bytes equal; PLAN18: 2159/2159 bytes
equal).

## Deviations & assumptions

1. **No FROM mismatch occurred.** All four FROM strings (B1, B2, D1,
   D2) were re-read from each file's current on-disk content before
   applying, per constraint 4, and each occurred exactly once —
   nothing needed to stop or be reported as a mismatch.
2. **The literal command `python3 -m py_compile apps/cli/commands/blocker.py
   apps/cli/commands/decision.py tests/cli/test_blocker_cmd.py
   tests/cli/test_decision_cmd.py` was not attempted directly** — the
   operator's block flagged this exact form as previously denied by
   the Bash tool's sandbox permission in this repo, so the declared
   equivalent substitution (`python3 -c "import py_compile;
   py_compile.compile(..., doraise=True); ..."`) was used from the
   start, per constraint 9. It printed `OK` (i.e., no `SyntaxError`
   raised, equivalent to exit 0).
3. **The C3 plan.md gate used a direct binary write
   (`pathlib.Path.write_bytes`) plus a real `bytes == bytes`
   comparison**, with the trailing newline stripped from the source
   Python triple-quoted string before encoding (the known
   PLAN15/16/17-precedent failure shape of picking up one stray
   trailing byte was checked for and avoided from the start this
   round) — verified exact in binary mode: 2159 == 2159 bytes.
4. **Ruff was not attempted** this round (see Verification section) —
   a deliberate choice to avoid a known, already-documented refusal,
   not a new deviation in outcome.

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, and once more immediately before writing this
handback). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r17.md`,
`.agent/last_block.md`, `.agent/live_review.md`,
`apps/cli/commands/blocker.py`, `apps/cli/commands/decision.py`,
`tests/cli/test_blocker_cmd.py`, `tests/cli/test_decision_cmd.py`,
`.agent/plan.md` and this handback were committed. The bundle's commit
order (C0a, C0b, C1, C2, C3 — this handback C4) was followed exactly,
with C2 as one commit covering all four named files per constraint 5.
Only `blocker.list` and `decision.list` were wired this round; no
other list command's handler was touched, per constraint 1.
`apply_list_options` itself (`packages/orchestration/list_options.py`)
was not touched, per constraint 2.

## Next

**NEXT EXPECTED ACTION: T003 batch 6 — wire `apply_list_options` into
more list commands.** PLAN18's Next Steps names `review.list`,
`propose.list`, and `external-builder.submission-list` as the next
batch — same drill as batches 3-5 (`tournament.list`, `project.list`,
`blocker.list`/`decision.list`). `patch.list`
(`approval_queue.py`'s table renderer) and `loop.list` (two-collection
rows) still need their own look before wiring;
`config.list`/`worker.list`/`execution.list` stay excused per PLAN18's
Risks section. Round 18 should grep each remaining command's own
tests for an order-asserting test FIRST, per DECISION F262 D2's
precedent, before assuming date-descending is safe to force.
