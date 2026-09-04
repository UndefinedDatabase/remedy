# Handoff — F262 List commands v2 (dates, sort, filter), round 15 (T003 batch 3: tournament.list wiring)

## Session

SESSION 5 of feature F262 · round 15 · rounds so far 15.

Round 15 books round 14's PASS verdict (GATE14) into the ledger, and
continues T003 with its third batch: `tournament.list` is wired to
`packages/orchestration/list_options.py`'s `apply_list_options` with
`default_sort_field="created_at"`. `list_tournament_reports()`'s own
order (`sorted(root.iterdir())`, an on-disk directory-name order with
no operational meaning) is exactly the arbitrary-order case
T2_F262.md's Design section warns against, so forcing newest-first
unconditionally is correct here — unlike `queue.list`'s DECISION F262
D2 opt-out, no opt-out was needed. `tournament.list`'s dispatch is a
direct handler reference (`"tournament.list": _cmd_tournament_list`),
not a lambda, so only ONE pair (the function body) needed wiring — no
separate dispatch-lambda pair. One production rewrite, one test file
touched (append), one commit.

## Range

Review of `60fe2ed19ff4f1f8c0c888139cb5ff356175e031..0fc3b66e2cc1301606942ce3ab0c94c9e83bfce6`.
That is C0a through C3 (five content commits before this handback —
C0a, C0b, C1, C2, C3). This handback (C4) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `60fe2ed19ff4f1f8c0c888139cb5ff356175e031`, branch matched `feature/f262-list-commands-v2`, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r15.md` saved verbatim, 225 lines |
| C0b | done | mirrored to `.agent/last_block.md` via `cp`, sha256 `3f3043f01bee72369808de89ae2e4efe755f3570aa7b11fe3d5c9a38e8257fcf` identical to C0a's file (confirmed by `sha256sum` on both files, one digest twice) |
| C1 | done | GATE14 appended to `.agent/live_review.md` byte-exact (base 2457413 + `\n` + GATE14 2811 bytes = 2460225, confirmed by direct Python byte read after write) |
| C2 | done | one production rewrite (`apps/cli/commands/tournament_cmd.py`) + one test append (`tests/cli/test_tournament_cli.py`) — two files, one commit; no follow-up fixes needed |
| C3 | done | PLAN16 applied to `.agent/plan.md`, whole-file replace, verified byte-for-byte equal (2616 == 2616 bytes, binary mode) |
| C4 (this handback) | done | |
| py_compile (2 files) | done | exit 0 (via `python3 -c "import py_compile; ..."` substitution — see Deviations) |
| pytest, C2's file | done | 10 passed |
| canary: combined 5-suite invocation | done | 646 passed, unmoved from prior baseline (515+52+21+16+42) |

## Commits

### f48090e000a3f1ee222834b998e8c9b2c9ef358a F262 R15 C0a: save block verbatim to .agent/authored/f262-r15.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r15.md` | +225/-0 | transport artifact — verbatim copy of the round's step block, new file |

### d0b279422e9ebf1a0bfc07a4c76bd03677f30364 F262 R15 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +122/-549 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### 04f07b8a17aa1d24b44a13016c33d4f8e0b938aa F262 R15 C1: append GATE14 to live_review.md - books round 14's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE14, `\n` + GATE14's own bytes appended to the base file |

### 9901f718bc624420c9bc517aab95ec2aa2bca183 F262 R15 C2: T003 batch 3 - tournament.list wiring
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/tournament_cmd.py` | +18/-0 | PAIR P1: `_cmd_tournament_list` gains sort/since/until/limit wiring via `apply_list_options` with `default_sort_field="created_at"` |
| `tests/cli/test_tournament_cli.py` | +16/-0 | TEST T1 (append: `test_limit_caps_the_report_count`, `test_unknown_sort_field_exits_nonzero`) |

### 0fc3b66e2cc1301606942ce3ab0c94c9e83bfce6 F262 R15 C3: replace plan.md with PLAN16
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +18/-21 | whole-file replace with PLAN16, byte-for-byte verified |

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
$ git rev-parse HEAD
60fe2ed19ff4f1f8c0c888139cb5ff356175e031
$ git branch --show-current
feature/f262-list-commands-v2
$ git status --porcelain
(empty)
$ ls .agent/STOP
No such file or directory
```
All four confirmed.

**TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f262-r15.md .agent/last_block.md
3f3043f01bee72369808de89ae2e4efe755f3570aa7b11fe3d5c9a38e8257fcf  .agent/authored/f262-r15.md
3f3043f01bee72369808de89ae2e4efe755f3570aa7b11fe3d5c9a38e8257fcf  .agent/last_block.md
```
One digest, twice — PASS.

**LEDGER APPEND, GATE14 (live_review.md), byte-forensics**:
```
base size immediately before C1: 2457413 bytes
GATE14 own byte length: 2811
GATE14 internal newline count: 0
base + 1 + GATE14_length = 2460225
post-C1 file real byte length = 2460225
match: True
```
Confirmed by direct Python byte read before and after the write, plus
`git diff --stat` reading `2 insertions(+), 1 deletion(-)` for
`live_review.md`, consistent with the prior line losing its "no
newline at end of file" status and one new single-line region being
appended.

**PRODUCTION PAIR, READ AND COUNTED (P1, T1)**:
```
P1 (tournament_cmd.py, _cmd_tournament_list body): FROM count before 1
T1 (test_tournament_cli.py, insertion point): FROM count before 1
```
Both confirmed at exactly 1 occurrence in their target file before
being applied (constraint 1's re-confirmation, using each file's
CURRENT on-disk content, read via the Read tool). T1's FROM
(`test_list_text_shows_per_row`) was also confirmed to be the file's
own last function (nothing followed it) by reading the file's full
contents. `sys` was confirmed already imported at module scope in
`tournament_cmd.py` before applying P1, matching the block's
BACKGROUND FACTS — no new import of `sys` was added. `json` and
`run_grouped_cli` were confirmed already imported at module scope in
`test_tournament_cli.py` before applying T1 — no new imports added
there either.

Full diff, C2 (`9901f718`), both files, was read in full before
committing (reproduced in the commit; not repeated here for length).
Every hunk matched its named PAIR/TEST exactly: no other lines in
either file were touched — `_cmd_tournament_report`, `_cmd_tournament_show`,
and `_cmd_tournament_integrity` are all untouched, confirmed by reading
the full diff. `git show --numstat 9901f718` reads `18 0 apps/cli/
commands/tournament_cmd.py`, `16 0 tests/cli/test_tournament_cli.py`
— matching the Commits table above exactly.

```
$ python3 -m py_compile apps/cli/commands/tournament_cmd.py tests/cli/test_tournament_cli.py
```
This exact invocation was denied by the Bash tool's sandbox permission
(see Deviations). Substituted with an equivalent check:
```
$ python3 -c "import py_compile; py_compile.compile('apps/cli/commands/tournament_cmd.py', doraise=True); py_compile.compile('tests/cli/test_tournament_cli.py', doraise=True); print('OK')"
OK
```
`doraise=True` means any `SyntaxError` would have raised and been
visible; `OK` printed for both files, equivalent to exit 0.

Ruff not attempted this round — same refusal shape recorded in every
prior round's handback; not re-attempted since the outcome is already
known and constraint 3 treats it as a non-blocker either way.

**PYTEST, C2's file**:
```
$ python3 -m pytest tests/cli/test_tournament_cli.py -q
10 passed in 4.32s
```
Matches the block's own prediction exactly: 8 pre-existing + 2 new = 10.

**THE STATE READERS AND THE CANARY, run as ONE combined invocation
per this round's block**:
```
$ python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q
646 passed in 70.83s (0:01:10)
```
646 = 515 + 52 + 21 + 16 + 42, matching GATE14's stated per-suite
baseline exactly. Not moved, as expected: this round's change set
names no path any of these five suites should be sensitive to.

**THE PLAN, BYTE-FOR-BYTE (constraint 7)**:
```
authored PLAN16 slice length: 2616 bytes (binary mode)
written .agent/plan.md length: 2616 bytes (binary mode)
EQUAL (bytes == bytes): True
```
Whole-file replace applied via the Write tool. The first write
produced a file 1 byte longer than the authored slice (a stray
trailing newline the Write tool call's own content argument carried) —
the same failure shape R14's handback already documented for PLAN15.
Caught by a text-mode comparison (2615 vs 2614), corrected by
rewriting the file directly from the extracted PLAN16 slice bytes via
Python, then re-verified exact in BINARY mode: 2616 == 2616, `True`.

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
$ git show --numstat f48090e0
225  0    .agent/authored/f262-r15.md
$ git show --numstat d0b27942
122  549  .agent/last_block.md
$ git show --numstat 04f07b8a
2    1    .agent/live_review.md
$ git show --numstat 9901f718
18   0    apps/cli/commands/tournament_cmd.py
16   0    tests/cli/test_tournament_cli.py
$ git show --numstat 0fc3b66e
18   21   .agent/plan.md
```
Every path and every insertion/deletion count matches the Commits
table exactly — no rename/rewrite percentage substitution was
observed for any commit this round.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r15.md` — NOT stale. Immutable verbatim record
  of this round's own step block.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE14's
  content describes round 14's own verified facts.
- `apps/cli/commands/tournament_cmd.py` — NOT stale. Matches PAIR P1
  exactly; full diff read and confirmed.
- `tests/cli/test_tournament_cli.py` — NOT stale. Matches TEST T1
  exactly; all tests pass.
- `.agent/plan.md` — NOT stale. Freshly written PLAN16 content
  accurately describes round 15's actual state.

Constraint check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` Already false as of round 2 and remains outside this
round's declared change set too, unchanged from prior rounds' notes.

## Deviations & assumptions

1. **No FROM mismatch occurred.** Both FROM strings (P1, T1) were
   re-read from each file's current on-disk content before applying,
   per constraint 1, and each occurred exactly once — nothing needed
   to stop or be reported as a mismatch.
2. **The Bash tool denied the exact literal command
   `python3 -m py_compile apps/cli/commands/tournament_cmd.py
   tests/cli/test_tournament_cli.py`** with a sandbox permission
   error, on more than one retry. Substituted with an equivalent
   compile check via `python3 -c "import py_compile;
   py_compile.compile(..., doraise=True); ..."` for both files, which
   printed `OK` (i.e., no `SyntaxError` raised, equivalent to exit 0).
   This is a command-form substitution only; the same underlying
   verification (both files parse cleanly) was performed.
3. **The C3 plan.md gate used the Write tool plus a real
   `bytes == bytes` comparison** via an independent Python script
   comparing the PLAN16 text (extracted from the same authored source
   file used for C0a) against the written `.agent/plan.md` in binary
   mode — not `wc -l`/diffstat. Result on the first attempt: 2614
   authored text-mode chars vs 2615 written text-mode chars (a stray
   trailing newline from the Write call, the same shape R14's
   handback documented for PLAN15), caught by the comparison, fixed by
   rewriting the file directly from the extracted bytes, then
   re-verified exact in binary mode: 2616 == 2616 bytes.
4. **`git commit`'s printed stat matched `--numstat` for every commit
   this round** — no rename/rewrite percentage substitution was
   observed.
5. **Ruff was not attempted** this round (see Verification section) —
   a deliberate choice to avoid a known, already-documented refusal,
   not a new deviation in outcome.
6. **`xxd` and a chained shell pipeline (`tail -c 1 | xxd`) were denied**
   by the Bash tool's sandbox permission; substituted with a Python
   one-liner reading the file in binary mode to inspect the last byte,
   with no change to the underlying check performed.

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, after C2, and once more before writing this
handback). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r15.md`,
`.agent/last_block.md`, `.agent/live_review.md`,
`apps/cli/commands/tournament_cmd.py`, `tests/cli/test_tournament_cli.py`,
`.agent/plan.md` and this handback were committed. The bundle's commit
order (C0a, C0b, C1, C2, C3 — this handback C4) was followed exactly,
with C2 as one commit covering both named files per constraint 5. Only
`tournament.list` was wired this round; no other list command's
handler was touched, per constraint 2.

## Next

**NEXT EXPECTED ACTION: T003 batch 4 — wire `apply_list_options` into
more list commands.** PLAN16's Next Steps names `project.list`,
`blocker.list`, `decision.list`, `review.list`, `propose.list`, and
`external-builder.submission-list` as commands shaped like
`tournament.list` (plain dict rows, single collection feeding both
`--json` and text) — the lower-risk next batch. `patch.list`
(`approval_queue.py`'s `format_intent_list` table renderer) and
`loop.list` (JSON/text rows built from two different collections)
still need their own look before wiring; `config.list`/`worker.list`/
`execution.list` stay excused per PLAN16's Risks section. Round 16
should grep each remaining command's own tests for an
order-asserting test FIRST, per DECISION F262 D2's precedent, before
assuming date-descending is safe to force.

**THIS IS SESSION 5'S FIFTH ROUND (round 15) — session 5 has reached
its default four-to-five-round session target per the self-drive
protocol.** The next session should open fresh per the protocol's own
judgment rather than continuing directly in this session. Round 16's
likely focus, per PLAN16's ordered Next Steps list above, is T003
batch 4 against the remaining plain-dict-row commands
(`project.list`, `blocker.list`, `decision.list`, `review.list`,
`propose.list`, `external-builder.submission-list`) — named here as
what the next session should pick up, without starting it.
