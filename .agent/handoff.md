# Handoff — F262 List commands v2 (dates, sort, filter), round 16 (T003 batch 4: project.list wiring)

## Session

SESSION 6 of feature F262 · round 16 · rounds so far 16.

Round 16 books round 15's PASS verdict (GATE15) into the ledger, and
continues T003 with its fourth batch: `project.list` is wired to
`packages/orchestration/list_options.py`'s `apply_list_options` with
`default_sort_field="created_at"`. `_list_projects_readonly()` already
sorts newest-first (covered by `test_list_sorted_newest_first`), so
forcing the same default via the shared helper changes nothing
observable and needed no D2-style opt-out. `project.list`'s dispatch
is a lambda (`"project.list": lambda args: _cmd_list_projects(...)`),
unlike `tournament.list`'s direct handler reference, so BOTH the
handler body (PAIR P1) and the dispatch site (PAIR P2) needed wiring —
two pairs, not one. One production rewrite (two pairs in the same
file), one test file touched (append of two new tests), one commit.

## Range

Review of `095cd91ba42148e3d9773f1d48069f8aaeaeb83c..4c476063f51fae8e9ba3ca258f5fabe48a810bb3`.
That is C0a through C3 (five content commits before this handback —
C0a, C0b, C1, C2, C3). This handback (C4) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `095cd91ba42148e3d9773f1d48069f8aaeaeb83c`, branch matched `feature/f262-list-commands-v2`, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r16.md` saved verbatim, 197 lines, 16005 bytes |
| C0b | done | mirrored to `.agent/last_block.md` via `shutil.copyfile`, sha256 `ca1aaebf4e6024b0a7d98d1faefbc12001bdf0635dc1931c5d7c514213adcc3d` identical to C0a's file (confirmed by `sha256sum` on both files, one digest twice) |
| C1 | done | GATE15 appended to `.agent/live_review.md` byte-exact (base 2460225 + `\n` + GATE15 2317 bytes = 2462543, confirmed by direct Python byte read before and after write) |
| C2 | done | PAIR P1 + PAIR P2 rewrite (`apps/cli/commands/project.py`) + TEST T1 append (`tests/test_grouped_cli.py`) — two files, one commit; no follow-up fixes needed |
| C3 | done | PLAN17 applied to `.agent/plan.md`, whole-file replace, verified byte-for-byte equal (2530 == 2530 bytes, binary mode) |
| C4 (this handback) | done | |
| G1 (py_compile, 2 files) | done | printed `OK` via the declared substitution (see Deviations) |
| G2 (pytest, C2's test file) | done | 525 passed (523 pre-existing + 2 new) |
| G3 (canary: combined 5-suite invocation) | done | 646 passed, unmoved from prior baseline (515+52+21+16+42) |
| G4 (sha256sum transport) | done | one identical digest, twice |
| G5 (live_review.md byte forensics) | done | before 2460225, after 2462543, matching exactly |
| G6 (plan.md byte-for-byte) | done | 2530 bytes, byte-for-byte equal to PLAN17 |
| G7 (git status --porcelain, twice) | done | empty before C0a, empty immediately before C4 |
| G8 (git ls-files .remedy-wt) | done | empty output — nothing tracked under `.remedy-wt/` |

## Commits

### 2021dbff4ae3a429c33eb4779f154378172f427e F262 R16 C0a: save step block to .agent/authored/f262-r16.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r16.md` | +197/-0 | transport artifact — verbatim copy of the round's step block, new file |

### bb31aba53befe05436c575adfb86ac7107de1158 F262 R16 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +151/-179 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### 6ed533d38b1b083bc940525a7c9806069c15c5b4 F262 R16 C1: append GATE15 to live_review.md - books round 15's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE15, `\n` + GATE15's own bytes appended to the base file |

### f4b0ec8b8f733def806d6d3c39dd2fc7bdd39316 F262 R16 C2: T003 batch 4 - project.list wiring
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/project.py` | +32/-2 | PAIR P1: `_cmd_list_projects` gains sort/since/until/limit params and `apply_list_options` wiring with `default_sort_field="created_at"`; PAIR P2: `"project.list"` dispatch lambda forwards the new flags via `getattr` |
| `tests/test_grouped_cli.py` | +21/-0 | TEST T1 (append: `test_limit_caps_returned_projects`, `test_unknown_sort_field_exits_nonzero`) |

### 4c476063f51fae8e9ba3ca258f5fabe48a810bb3 F262 R16 C3: replace plan.md with PLAN17
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +17/-17 | whole-file replace with PLAN17, byte-for-byte verified |

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
095cd91ba42148e3d9773f1d48069f8aaeaeb83c
$ ls .agent/STOP
No such file or directory
```
All four confirmed.

**TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f262-r16.md .agent/last_block.md
ca1aaebf4e6024b0a7d98d1faefbc12001bdf0635dc1931c5d7c514213adcc3d  .agent/authored/f262-r16.md
ca1aaebf4e6024b0a7d98d1faefbc12001bdf0635dc1931c5d7c514213adcc3d  .agent/last_block.md
```
One digest, twice — PASS.

**LEDGER APPEND, GATE15 (live_review.md), byte-forensics**:
```
base size immediately before C1: 2460225 bytes
GATE15 own byte length: 2317
GATE15 internal newline count: 0
base + 1 + GATE15_length = 2462543
post-C1 file real byte length = 2462543
match: True
file still ends with no trailing newline: confirmed
```
Confirmed by direct Python byte read before and after the write
(`pathlib.Path.write_bytes`, not a shell append), plus `git show
--numstat 6ed533d3` reading `2  1  .agent/live_review.md`, consistent
with the prior line losing its "no newline at end of file" status and
one new single-line region being appended.

**PRODUCTION PAIRS, READ AND COUNTED (P1, P2, T1)**:
```
P1 (project.py, _cmd_list_projects signature+body): FROM count before 1
P2 (project.py, "project.list" dispatch lambda): FROM count before 1
T1 (test_grouped_cli.py, insertion point before class TestJobListCLI): FROM count before 1
```
All three confirmed at exactly 1 occurrence in their target file
before being applied (constraint 4's re-confirmation, using each
file's CURRENT on-disk content, read via the Read tool). `sys` was
confirmed already imported at module scope in `project.py` (line 6)
before applying P1 — no new import of `sys` was added. `json`,
`StringIO`, and `pytest` were confirmed already imported at module
scope in `test_grouped_cli.py` before applying T1 — no new imports
added there either.

Full diff, C2 (`f4b0ec8b`), both files, was read in full before
writing this handback (`git show f4b0ec8b -- apps/cli/commands/project.py
tests/test_grouped_cli.py`). Every hunk matched its named
PAIR/TEST exactly: no other lines in either file were touched — every
other handler in `project.py` (`_cmd_create_project`,
`_cmd_show_project`, `_cmd_attach_project_repo`,
`_cmd_attach_project_job`, `_cmd_project_context`,
`_cmd_project_brain`, `_cmd_project_summary`, `_cmd_project_current`,
`_cmd_project_attach_repo`, `_cmd_project_adopt`) and every other
dispatch entry are untouched, confirmed by reading the full diff.
`git show --numstat f4b0ec8b` reads `32  2  apps/cli/commands/
project.py`, `21  0  tests/test_grouped_cli.py` — matching the Commits
table above exactly.

```
$ python3 -m py_compile apps/cli/commands/project.py tests/test_grouped_cli.py
```
This exact invocation form has been denied by the Bash tool's sandbox
permission in prior rounds (per the operator's declared known quirk);
not retried this round, substituted directly with the declared
equivalent:
```
$ python3 -c "import py_compile; py_compile.compile('apps/cli/commands/project.py', doraise=True); py_compile.compile('tests/test_grouped_cli.py', doraise=True); print('OK')"
OK
```
`doraise=True` means any `SyntaxError` would have raised and been
visible; `OK` printed for both files, equivalent to exit 0.

Ruff not attempted this round — same refusal shape recorded in every
prior round's handback; not re-attempted since the outcome is already
known and constraint 3 treats it as a non-blocker either way.

**PYTEST, C2's file**:
```
$ python3 -m pytest tests/test_grouped_cli.py -q
........................................................................ [ 13%]
........................................................................ [ 27%]
........................................................................ [ 41%]
........................................................................ [ 54%]
........................................................................ [ 68%]
........................................................................ [ 82%]
........................................................................ [ 96%]
.....................                                                    [100%]
525 passed in 48.41s
```
Matches the block's own prediction exactly: 523 pre-existing + 2 new = 525.

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
646 passed in 70.26s (0:01:10)
```
646 = 515 + 52 + 21 + 16 + 42, matching GATE15's stated per-suite
baseline exactly. Not moved, as expected: this round's change set
names no path any of these five suites should be sensitive to.

**THE PLAN, BYTE-FOR-BYTE (constraint: byte-exact whole-file replace)**:
```
authored PLAN17 slice length: 2530 bytes (binary mode, no trailing newline)
written .agent/plan.md length: 2530 bytes (binary mode)
EQUAL (bytes == bytes): True
```
Whole-file replace applied via a direct binary write (`shutil.copyfile`
from a Python-constructed byte buffer), after first observing that a
plain triple-quoted Python string carried one stray trailing `\n`
beyond the target 2530 bytes (2531 vs 2530) — the same failure shape
R14/R15's handbacks documented for PLAN15/PLAN16 — caught by the byte
comparison, corrected by stripping the trailing newline to match
`.agent/plan.md`'s own no-trailing-newline convention, then
re-verified exact in BINARY mode: 2530 == 2530, `True`.

**AUTHORED-TEXT PROOFS** (GATE15 and PLAN17 as embedded in the
committed `.agent/authored/f262-r16.md`, compared disk-to-disk against
what was actually written):
```
gate15_from_authored length: 2317
gate15_in_live (last 2317 bytes of live_review.md) length: 2317
MATCH gate15: True

plan17_from_authored_block (stripped) length: 2530
plan.md length: 2530
MATCH plan17: True
```
Both reviewer-authored texts applied this round (GATE15 into
`live_review.md`, PLAN17 into `plan.md`) are byte-identical to the
text embedded in the committed `.agent/authored/f262-r16.md` slice.

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
$ git show --numstat 2021dbff
197  0    .agent/authored/f262-r16.md
$ git show --numstat bb31aba5
151  179  .agent/last_block.md
$ git show --numstat 6ed533d3
2    1    .agent/live_review.md
$ git show --numstat f4b0ec8b
32   2    apps/cli/commands/project.py
21   0    tests/test_grouped_cli.py
$ git show --numstat 4c476063
17   17   .agent/plan.md
```
Every path and every insertion/deletion count matches the Commits
table exactly. Note: `git commit`'s own printed summary for C0b showed
`197 insertions(+), 225 deletions(-)` with a `rewrite ... (90%)`
annotation — that is `git commit`'s break-rewrite heuristic treating
the file as a full delete+add (197 = new file's line count, 225 = old
file's line count) rather than a line-level diff; `git show --numstat`
without `-B` reports the line-level diff (151/179) used in the table
above, consistent with the convention R15's handback used for its own
C0b row.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r16.md` — NOT stale. Immutable verbatim record
  of this round's own step block.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE15's
  content describes round 15's own verified facts.
- `apps/cli/commands/project.py` — NOT stale. Matches PAIR P1 and PAIR
  P2 exactly; full diff read and confirmed.
- `tests/test_grouped_cli.py` — NOT stale. Matches TEST T1 exactly;
  all tests pass.
- `.agent/plan.md` — NOT stale. Freshly written PLAN17 content
  accurately describes round 16's actual state.

Constraint check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` Already false as of round 2 and remains outside this
round's declared change set too, unchanged from prior rounds' notes.

## Deviations & assumptions

1. **No FROM mismatch occurred.** All three FROM strings (P1, P2, T1)
   were re-read from each file's current on-disk content before
   applying, per constraint 4, and each occurred exactly once —
   nothing needed to stop or be reported as a mismatch.
2. **The literal command `python3 -m py_compile apps/cli/commands/project.py
   tests/test_grouped_cli.py` was not attempted directly** — the
   operator's block flagged this exact form as previously denied by
   the Bash tool's sandbox permission in this repo, so the declared
   equivalent substitution (`python3 -c "import py_compile;
   py_compile.compile(..., doraise=True); ..."`) was used from the
   start, per constraint 9. It printed `OK` (i.e., no `SyntaxError`
   raised, equivalent to exit 0).
3. **The C3 plan.md gate used a direct binary write (`shutil.copyfile`
   from a Python-constructed byte buffer) plus a real `bytes == bytes`
   comparison**, not the Write tool directly on the target path — a
   first construction via a Python triple-quoted string produced 2531
   bytes (one stray trailing newline) against the target 2530, caught
   before writing to `.agent/plan.md`, corrected by stripping the
   trailing newline, then verified exact in binary mode: 2530 == 2530
   bytes.
4. **One combined Bash tool-call denial occurred** when several
   inspection commands (`ls .agent/STOP`, `sha256sum`, `git ls-files
   .remedy-wt`, echoed section headers) were chained together in a
   single multi-line command with `&&`/`;` separators for the
   pre-C4 gate re-checks; the tool denied the combined call outright.
   Each check was then re-run as its own separate, simple Bash
   invocation, with no change to the underlying checks performed or
   their results.
5. **Ruff was not attempted** this round (see Verification section) —
   a deliberate choice to avoid a known, already-documented refusal,
   not a new deviation in outcome.
6. **`git commit`'s printed diffstat for C0b (bb31aba5) used a
   break-rewrite heuristic** (`197 insertions(+), 225 deletions(-)`,
   `rewrite ... (90%)`) that differs from `git show --numstat`'s
   line-level count (`151  179`) for the same commit; the Commits
   table above uses the `--numstat` line-level figures, consistent
   with R15's handback convention for its own C0b row. No content
   discrepancy — both commands describe the same commit; only the
   diff-stat heuristic differs.

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, and once more immediately before writing this
handback). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r16.md`,
`.agent/last_block.md`, `.agent/live_review.md`,
`apps/cli/commands/project.py`, `tests/test_grouped_cli.py`,
`.agent/plan.md` and this handback were committed. The bundle's commit
order (C0a, C0b, C1, C2, C3 — this handback C4) was followed exactly,
with C2 as one commit covering both named files per constraint 5. Only
`project.list` was wired this round; no other list command's handler
was touched, per constraint 1. `apply_list_options` itself
(`packages/orchestration/list_options.py`) was not touched, per
constraint 2. `_list_projects_readonly`'s own sort in
`project_registry.py` was not touched, per constraint 1.

## Next

**NEXT EXPECTED ACTION: T003 batch 5 — wire `apply_list_options` into
more list commands.** PLAN17's Next Steps names `blocker.list`,
`decision.list`, `review.list`, `propose.list`, and
`external-builder.submission-list` as commands shaped like
`project.list`/`tournament.list` (plain dict/model rows, single
collection feeding both `--json` and text) — the next batch.
`patch.list` (`approval_queue.py`'s `format_intent_list` table
renderer) and `loop.list` (JSON/text rows built from two different
collections) still need their own look before wiring;
`config.list`/`worker.list`/`execution.list` stay excused per PLAN17's
Risks section. Round 17 should grep each remaining command's own
tests for an order-asserting test FIRST, per DECISION F262 D2's
precedent, before assuming date-descending is safe to force.
