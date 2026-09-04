# Handoff — F262 List commands v2 (dates, sort, filter), round 18 (T003 batch 6: review.list/propose.list/external-builder.submission-list wiring)

## Session

SESSION 6 of feature F262 · round 18 · rounds so far 18.

Round 18 books round 17's PASS verdict (GATE17) into the ledger, and
closes out T003's plain single-collection-list batches: `review.list`,
`propose.list` and `external-builder.submission-list` are all wired to
`packages/orchestration/list_options.py`'s `apply_list_options` with
`default_sort_field="created_at"`. All three commands' dispatch
lambdas already forwarded `args` unchanged
(`"review.list": lambda args: _cmd_review_list(args)`,
`"propose.list": lambda args: _cmd_propose_list(args)`, and
`"external-builder.submission-list": _cmd_external_builder_submission_list`
as a direct function reference, no lambda at all), so — unlike
`project.list`/`blocker.list`/`decision.list` in rounds 16-17 — each
needed ONLY ONE pair (the handler body itself), no dispatch-site pair.
Row shapes vary across the three: `review.list`'s rows are plain
dicts (`r.get("created_at", "")`), `propose.list`'s rows are
`ProposedTask` pydantic models (`t.created_at.isoformat()`, matching
`project.list`'s datetime shape from round 16), and
`external-builder.submission-list`'s rows are dicts keyed
`received_at` mapped to the shared `created_at` sort-field name for
flag-name consistency across commands. No pre-existing test in any of
the three files asserted a meaningful non-date default order, so none
needed a D2-style opt-out. One production commit covers all six
touched files (three source files, three test files).

## Range

Review of `25ef619839597ff4ec9fdd9d6c626e4597ec9ea5..438bf3b0f543235caaf89bfa067d82479f121c39`.
That is C0a through C3 (five content commits before this handback —
C0a, C0b, C1, C2, C3). This handback (C4) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `25ef619839597ff4ec9fdd9d6c626e4597ec9ea5`, branch matched `feature/f262-list-commands-v2`, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r18.md` saved verbatim, 318 lines, 23305 bytes |
| C0b | done | mirrored to `.agent/last_block.md` via `shutil.copyfile`, sha256 `58f130673d6c8a3eb626e4f4593d64676e07f0c53202c3a0342e3d8067a53559` identical to C0a's file (confirmed by `sha256sum` on both files, one digest twice) |
| C1 | done | GATE17 appended to `.agent/live_review.md` byte-exact (base 2465111 + `\n` + GATE17 2420 bytes = 2467532, confirmed by direct Python byte read before and after write) |
| C2 | done | PAIR R1 (`apps/cli/commands/review_cmd.py`), PAIR PR1 (`apps/cli/commands/propose_cmd.py`), PAIR E1 (`apps/cli/commands/external_builder_cmd.py`), TEST T1 (`tests/cli/test_review_cmd.py`), TEST T2 (`tests/cli/test_propose_cli.py`), TEST T3 (`tests/cli/test_external_builder_cli.py`) — six files, one commit; no follow-up fixes needed |
| C3 | done | PLAN19 applied to `.agent/plan.md`, whole-file replace, verified byte-for-byte equal (2352 == 2352 bytes, binary mode) |
| C4 (this handback) | done | |
| G1 (py_compile, 6 files) | done | printed `OK` via the declared substitution (see Deviations) |
| G2 (pytest, C2's three test files) | done | 46 passed (40 pre-existing + 6 new) |
| G3 (canary: combined 5-suite invocation) | done | 646 passed, unmoved from prior baseline (515+52+21+16+42) |
| G4 (sha256sum transport) | done | one identical digest, twice |
| G5 (live_review.md byte forensics) | done | before 2465111, after 2467532, matching exactly |
| G6 (plan.md byte-for-byte) | done | 2352 bytes, byte-for-byte equal to PLAN19 |
| G7 (git status --porcelain, twice) | done | empty before C0a, empty immediately before C4 |
| G8 (git ls-files .remedy-wt) | done | empty output — nothing tracked under `.remedy-wt/` |

## Commits

### 94ced1a71d503690c800dbfed19ee00a9820053a F262 R18 C0a: save step block to .agent/authored/f262-r18.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r18.md` | +318/-0 | transport artifact — verbatim copy of the round's step block, new file |

### aa325b70e8b71f1d9ea444c4aeed246877da5ed2 F262 R18 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +217/-188 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### b3203e83dd6ebae8b4b2a93e84eee191cb373b8e F262 R18 C1: append GATE17 to live_review.md - books round 17's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE17, `\n` + GATE17's own bytes appended to the base file |

### 99876fa8873bccdb7b8d32ee1d3b0f0f584aa8d9 F262 R18 C2: T003 batch 6 - review.list/propose.list/external-builder.submission-list wiring
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/review_cmd.py` | +17/-0 | PAIR R1: `_cmd_review_list` gains `apply_list_options` wiring with `default_sort_field="created_at"`; no dispatch-site pair needed, `"review.list"` lambda already forwards `args` unchanged |
| `apps/cli/commands/propose_cmd.py` | +19/-0 | PAIR PR1: `_cmd_propose_list` gains `apply_list_options` wiring with `default_sort_field="created_at"`; no dispatch-site pair needed, `"propose.list"` lambda already forwards `args` unchanged |
| `apps/cli/commands/external_builder_cmd.py` | +17/-0 | PAIR E1: `_cmd_external_builder_submission_list` gains `apply_list_options` wiring with `default_sort_field="created_at"`; no dispatch-site pair needed, `COMMAND_HANDLERS` entry is a direct function reference (no lambda) |
| `tests/cli/test_review_cmd.py` | +32/-0 | `import pytest` added; TEST T1 (append: `test_limit_caps_returned_recommendations`, `test_unknown_sort_field_exits_nonzero`) |
| `tests/cli/test_propose_cli.py` | +17/-0 | TEST T2 (insert into `TestProposeListHandler`: `test_limit_caps_returned_tasks`, `test_unknown_sort_field_exits_nonzero_for_list`) |
| `tests/cli/test_external_builder_cli.py` | +23/-0 | TEST T3 (append: `test_submission_list_limit_caps_count`, `test_submission_list_unknown_sort_field_exits_nonzero`) |

### 438bf3b0f543235caaf89bfa067d82479f121c39 F262 R18 C3: replace plan.md with PLAN19
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +20/-17 | whole-file replace with PLAN19, byte-for-byte verified |

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
25ef619839597ff4ec9fdd9d6c626e4597ec9ea5
$ ls .agent/STOP
No such file or directory
```
All four confirmed.

**TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f262-r18.md .agent/last_block.md
58f130673d6c8a3eb626e4f4593d64676e07f0c53202c3a0342e3d8067a53559  .agent/authored/f262-r18.md
58f130673d6c8a3eb626e4f4593d64676e07f0c53202c3a0342e3d8067a53559  .agent/last_block.md
```
One digest, twice — PASS.

**LEDGER APPEND, GATE17 (live_review.md), byte-forensics**:
```
base size immediately before C1: 2465111 bytes
GATE17 own byte length: 2420
GATE17 internal newline count: 0
base + 1 + GATE17_length = 2467532
post-C1 file real byte length = 2467532
match: True
file still ends with no trailing newline: confirmed (last bytes "T IS PASS.")
```
Confirmed by direct Python byte read before and after the write
(`pathlib.Path.write_bytes`, not a shell append).

**PRODUCTION PAIRS, READ AND COUNTED (R1, PR1, E1)**:
```
R1 (review_cmd.py, _cmd_review_list body): FROM count before 1
PR1 (propose_cmd.py, _cmd_propose_list unreadable-store tail): FROM count before 1
E1 (external_builder_cmd.py, _cmd_external_builder_submission_list head): FROM count before 1
```
All three confirmed at exactly 1 occurrence in their target file
before being applied (constraint 4's re-confirmation, using each
file's CURRENT on-disk content, read via the Read tool then
re-counted with `str.count` in Python). `sys` and `json` were
confirmed already imported at module scope in all three files before
applying — no new import of either was added anywhere. No dispatch
site in any of the three `COMMAND_HANDLERS` dicts was touched, per
constraint 9 — confirmed by reading the full diff below.

Full diff, C2 (`99876fa8`), all three production files, was read in
full before writing this handback (`git show 99876fa8 --
apps/cli/commands/review_cmd.py apps/cli/commands/propose_cmd.py
apps/cli/commands/external_builder_cmd.py`). Every hunk matched its
named PAIR exactly: no other lines in any of the three files were
touched — every other handler in `review_cmd.py`
(`_cmd_review_run`, `_cmd_review_accept`, `_cmd_review_reject`,
`_cmd_review_bundle`), `propose_cmd.py` (`_cmd_propose_show`,
`_cmd_propose_evaluate`, `_cmd_propose_approve`, `_cmd_propose_reject`,
`_cmd_propose_defer`, `_cmd_propose_materialize`), and
`external_builder_cmd.py` (all other `_cmd_external_builder_*`
handlers), and every `COMMAND_HANDLERS` dict entry in all three files,
are untouched, confirmed by reading the full diff. `git show --numstat
99876fa8` reads `17  0  apps/cli/commands/external_builder_cmd.py`,
`19  0  apps/cli/commands/propose_cmd.py`, `17  0
apps/cli/commands/review_cmd.py`, `23  0
tests/cli/test_external_builder_cli.py`, `17  0
tests/cli/test_propose_cli.py`, `32  0  tests/cli/test_review_cmd.py`
— matching the Commits table above exactly.

```
$ python3 -m py_compile apps/cli/commands/review_cmd.py apps/cli/commands/propose_cmd.py apps/cli/commands/external_builder_cmd.py tests/cli/test_review_cmd.py tests/cli/test_propose_cli.py tests/cli/test_external_builder_cli.py
```
This exact multi-arg invocation form has been denied by the Bash
tool's sandbox permission in prior rounds (per the operator's declared
known quirk); not retried this round, substituted directly with the
declared equivalent:
```
$ python3 -c "import py_compile; py_compile.compile('apps/cli/commands/review_cmd.py', doraise=True); py_compile.compile('apps/cli/commands/propose_cmd.py', doraise=True); py_compile.compile('apps/cli/commands/external_builder_cmd.py', doraise=True); py_compile.compile('tests/cli/test_review_cmd.py', doraise=True); py_compile.compile('tests/cli/test_propose_cli.py', doraise=True); py_compile.compile('tests/cli/test_external_builder_cli.py', doraise=True); print('OK')"
OK
```
`doraise=True` means any `SyntaxError` would have raised and been
visible; `OK` printed for all six files, equivalent to exit 0.

Ruff not attempted this round — same refusal shape recorded in every
prior round's handback; not re-attempted since the outcome is already
known and constraint 3 treats it as a non-blocker either way.

**PYTEST, C2's three files**:
```
$ python3 -m pytest tests/cli/test_review_cmd.py tests/cli/test_propose_cli.py tests/cli/test_external_builder_cli.py -q
..............................................                           [100%]
46 passed in 6.26s
```
Matches the block's own prediction exactly: 40 pre-existing (2 + 29 +
9) + 6 new = 46.

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
646 passed in 70.38s (0:01:10)
```
646 = 515 + 52 + 21 + 16 + 42, matching GATE17's stated per-suite
baseline exactly. Not moved, as expected: this round's change set
names no path any of these five suites should be sensitive to.

**THE PLAN, BYTE-FOR-BYTE (constraint: byte-exact whole-file replace)**:
```
authored PLAN19 slice length: 2352 bytes (binary mode, no trailing newline)
written .agent/plan.md length: 2352 bytes (binary mode)
EQUAL (bytes == bytes): True
```
Whole-file replace applied via the Write tool, then re-verified exact
in BINARY mode against a slice extracted directly from the committed
`.agent/authored/f262-r18.md` (the delimiter between the PLAN19 text
and the following `CONSTRAINTS:` section): 2352 == 2352, `True`.

**AUTHORED-TEXT PROOFS** (GATE17 and PLAN19 as embedded in the
committed `.agent/authored/f262-r18.md`, compared disk-to-disk against
what was actually written):
```
gate17_from_authored length: 2420
gate17_in_live (last 2420 bytes of live_review.md) length: 2420
MATCH gate17: True (same construction — the file was written by
  appending base + \n + this exact 2420-byte string)

plan19_from_authored_block (stripped) length: 2352
plan.md length: 2352
MATCH plan19: True
```
Both reviewer-authored texts applied this round (GATE17 into
`live_review.md`, PLAN19 into `plan.md`) are byte-identical to the
text embedded in the committed `.agent/authored/f262-r18.md` slice —
the same file that was written directly from this prompt's own GATE17
and PLAN19 text, so the two are identical by construction, and were
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
$ git show --numstat 94ced1a7
318  0    .agent/authored/f262-r18.md
$ git show --numstat aa325b70
217  188  .agent/last_block.md
$ git show --numstat b3203e83
2    1    .agent/live_review.md
$ git show --numstat 99876fa8
17   0    apps/cli/commands/external_builder_cmd.py
19   0    apps/cli/commands/propose_cmd.py
17   0    apps/cli/commands/review_cmd.py
23   0    tests/cli/test_external_builder_cli.py
17   0    tests/cli/test_propose_cli.py
32   0    tests/cli/test_review_cmd.py
$ git show --numstat 438bf3b0
20   17   .agent/plan.md
```
Every path and every insertion/deletion count matches the Commits
table exactly.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r18.md` — NOT stale. Immutable verbatim record
  of this round's own step block.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE17's
  content describes round 17's own verified facts.
- `apps/cli/commands/review_cmd.py` — NOT stale. Matches PAIR R1
  exactly; full diff read and confirmed.
- `apps/cli/commands/propose_cmd.py` — NOT stale. Matches PAIR PR1
  exactly; full diff read and confirmed.
- `apps/cli/commands/external_builder_cmd.py` — NOT stale. Matches
  PAIR E1 exactly; full diff read and confirmed.
- `tests/cli/test_review_cmd.py` — NOT stale. Matches TEST T1 exactly;
  all tests pass.
- `tests/cli/test_propose_cli.py` — NOT stale. Matches TEST T2
  exactly; all tests pass.
- `tests/cli/test_external_builder_cli.py` — NOT stale. Matches TEST
  T3 exactly; all tests pass.
- `.agent/plan.md` — NOT stale. Freshly written PLAN19 content
  accurately describes round 18's actual state.

Constraint check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` Already false as of round 2 and remains outside this
round's declared change set too, unchanged from prior rounds' notes.

Also confirmed: `apps/cli/command_catalog.py`'s `_with_list_options`
helper (F262 T001, lines ~4905-4922) already auto-attaches
`--sort/--desc/--since/--until/--limit` `ArgDef`s to any catalog entry
whose `subcommand` is `"list"` or ends with `"-list"` — `review.list`,
`propose.list` (subcommand `"list"`) and
`external-builder.submission-list` (subcommand `"submission-list"`,
ends with `"-list"`) all already match this predicate, so no
`command_catalog.py` edit was needed this round for the flags to
reach the CLI parser; this was verified by reading the catalog file,
not assumed, before writing PAIR R1/PR1/E1.

## Authored-text proofs

For every reviewer-authored text applied this round — GATE17
(`.agent/live_review.md`) and PLAN19 (`.agent/plan.md`) — the
disk-to-disk comparison against the committed
`.agent/authored/f262-r18.md` slice is reported above under
Verification's "AUTHORED-TEXT PROOFS" heading: both matched
byte-for-byte (GATE17: 2420/2420 bytes equal; PLAN19: 2352/2352 bytes
equal).

## Deviations & assumptions

1. **No FROM mismatch occurred.** All three FROM strings (R1, PR1, E1)
   were re-read from each file's current on-disk content before
   applying, per constraint 4, and each occurred exactly once —
   nothing needed to stop or be reported as a mismatch.
2. **The literal command `python3 -m py_compile apps/cli/commands/review_cmd.py
   apps/cli/commands/propose_cmd.py apps/cli/commands/external_builder_cmd.py
   tests/cli/test_review_cmd.py tests/cli/test_propose_cli.py
   tests/cli/test_external_builder_cli.py` was not attempted directly**
   — the operator's block flagged this exact form as previously denied
   by the Bash tool's sandbox permission in this repo, so the declared
   equivalent substitution (`python3 -c "import py_compile;
   py_compile.compile(..., doraise=True); ..."`) was used from the
   start, per constraint 10. It printed `OK` (i.e., no `SyntaxError`
   raised, equivalent to exit 0).
3. **A `for`-loop plus `$(...)` command-substitution form
   (`for c in $(git log ...); do git show --numstat $c; done`) was
   denied by the Bash sandbox mid-round** while gathering commit
   numstats for this handback (matches the documented guard-rejects-
   loops-and-`$()`-by-form quirk). Worked around by issuing one plain
   `git show --numstat --format="" <sha>` per commit instead — a
   read-only verification step outside the declared change set, not a
   commit or a file write, so no constraint was affected.
4. **The C3 plan.md gate used the Write tool** plus a real
   `bytes == bytes` comparison against a slice extracted directly from
   the committed `.agent/authored/f262-r18.md` — verified exact in
   binary mode: 2352 == 2352 bytes, with no trailing-newline drift.
5. **Ruff was not attempted** this round (see Verification section) —
   a deliberate choice to avoid a known, already-documented refusal,
   not a new deviation in outcome.

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, and once more immediately before writing this
handback). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r18.md`,
`.agent/last_block.md`, `.agent/live_review.md`,
`apps/cli/commands/review_cmd.py`, `apps/cli/commands/propose_cmd.py`,
`apps/cli/commands/external_builder_cmd.py`,
`tests/cli/test_review_cmd.py`, `tests/cli/test_propose_cli.py`,
`tests/cli/test_external_builder_cli.py`, `.agent/plan.md` and this
handback were committed. The bundle's commit order (C0a, C0b, C1, C2,
C3 — this handback C4) was followed exactly, with C2 as one commit
covering all six named files per constraint 5. Only `review.list`,
`propose.list` and `external-builder.submission-list` were wired this
round; no other list command's handler was touched, per constraint 1.
`apply_list_options` itself (`packages/orchestration/list_options.py`)
was not touched, per constraint 2. No dispatch/`COMMAND_HANDLERS`
lambda was touched for any of the three commands, per constraint 9.

## Next

**NEXT EXPECTED ACTION: round 19 — investigate `patch.list` and
`loop.list`'s own shapes before deciding how/whether to wire them into
T003.** PLAN19's Next Steps names both as the last two candidates:
`patch.list` (`approval_queue.py`'s table renderer) and `loop.list`
(rows built from two different collections) are NOT plain
single-collection lists like every command wired in batches 3-6
(`tournament.list`, `project.list`, `blocker.list`/`decision.list`,
`review.list`/`propose.list`/`external-builder.submission-list`), so
round 19 should read each command's actual row-construction code and
existing tests FIRST (grepping for an order-asserting test per
DECISION F262 D2's precedent, same as every prior batch) before
deciding whether to wire, adapt, or excuse either one. This is the
LAST of the currently-known T003 batches, so round 19 may lead
straight into a T003 closure assessment once patch.list/loop.list are
resolved one way or the other.
