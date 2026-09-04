# Handoff — F262 List commands v2 (dates, sort, filter), round 14 (T003 batch 2: queue.list + memory.list wiring, DECISION F262 D2)

## Session

SESSION 5 of feature F262 · round 14 · rounds so far 14.

Round 14 books round 13's PASS verdict (GATE13) into the ledger, and
registers DECISION F262 D2: `queue.list`'s existing no-flag default
order is PRIORITY (load-bearing, a named passing test asserts it), not
date, so T003's newest-first-by-default principle must NOT silently
override it. `packages/orchestration/list_options.py`'s
`apply_list_options` is widened so `default_sort_field` may be `None`
— when both `sort` and `default_sort_field` are `None`, ordering is
skipped entirely, letting a caller with an existing meaningful order
opt out of the forced default. `queue.list` wires with
`default_sort_field=None` (keeps priority order); `memory.list` wires
with `default_sort_field="created_at"` (already sorted newest-first
internally, so the no-flag case is unchanged; `--sort`/`--since`/
`--until`/`--limit` are new capability on top). Three production
rewrites, three test files touched (all appends), one commit.

## Range

Review of `3459e7a818e7c7be1ffc6d0c0dfc8f5f8b3700c5..4eca056c8731849cafc3757671b12a8ee66c1e5d`.
That is C0a through C3 (five content commits before this handback —
C0a, C0b, C1, C2, C3). This handback (C4) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `3459e7a818e7c7be1ffc6d0c0dfc8f5f8b3700c5`, branch matched `feature/f262-list-commands-v2`, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r14.md` saved verbatim, 652 lines, sha256 `394dc28973984bb8d7803197196f575e0ec72d0893c78180574f2b619c95f51b` |
| C0b | done | mirrored to `.agent/last_block.md` via `cp`, sha256 identical to C0a's file (confirmed by `sha256sum` on both files, one digest twice) |
| C1 | done | GATE13 appended to `.agent/live_review.md` byte-exact (base 2455026 + `\n` + GATE13 2386 bytes = 2457413, confirmed by direct read after write) AND DECISION F262 D2 appended to `.agent/decisions.md` byte-exact (base 797530 + `\n` + DECISION 4891 bytes = 802422, confirmed the same way); tail-equality and negative-control byte-flip rejection both confirmed for both files |
| C2 | done | three production rewrites (`packages/orchestration/list_options.py`, `apps/cli/commands/queue_cmd.py`, `apps/cli/commands/memory.py`) + three test appends (`tests/orchestration/test_list_options.py`, `tests/cli/test_queue_cmd.py`, `tests/test_grouped_cli.py`) — six files, one commit; no follow-up fixes needed |
| C3 | done | PLAN15 applied to `.agent/plan.md`, whole-file replace, verified byte-for-byte equal (2880 == 2880) |
| C4 (this handback) | done | |
| py_compile (6 files) | done | exit 0, no output |
| regression check (constraint 9) | done | `tests/cli/test_queue_cmd.py::TestAdd::test_priority_is_recorded_and_orders_the_listing` — 1 passed, unmodified |
| pytest, C2's combined run | done | 562 passed |
| canary: combined 5-suite invocation | done | 646 passed, unmoved from prior baseline (515+52+21+16+42) |

## Commits

### aab15646427f902d6b51cd3a2b0785da65647855 F262 R14 C0a: save block verbatim to .agent/authored/f262-r14.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r14.md` | +652/-0 | transport artifact — verbatim copy of the round's step block, new file |

### 6315f8f885092b09c5ace01231c0e22ba2b316a7 F262 R14 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +430/-286 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### 06f35c1e315811e8458351cfaa2caca9e8be2e40 F262 R14 C1: append GATE13 to live_review.md and DECISION F262 D2 to decisions.md - books round 13's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14/-1 | byte-exact append of DECISION F262 D2, `\n` + the decision's own bytes appended to the base file |
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE13, `\n` + GATE13's own bytes appended to the base file |

### c65f83425f192160335f8588bfcdea07373869fc F262 R14 C2: T003 batch 2 - queue.list + memory.list wiring (DECISION F262 D2)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/memory.py` | +26/-0 | PAIR P4 (`_cmd_memory_list` gains sort/since/until/limit wiring via `apply_list_options` with `default_sort_field="created_at"`) + PAIR P5 (`memory.list` dispatch lambda passes the five new flags through) |
| `apps/cli/commands/queue_cmd.py` | +25/-1 | PAIR P2 (`_cmd_queue_list` gains sort/since/until/limit wiring via `apply_list_options` with `default_sort_field=None`, per DECISION F262 D2) + PAIR P3 (`queue.list` dispatch lambda passes the five new flags through) |
| `packages/orchestration/list_options.py` | +12/-9 | PAIR P1: `apply_list_options`'s `default_sort_field` widened to `str \| None = None`; ordering step skipped entirely when both `sort` and `default_sort_field` are `None` |
| `tests/cli/test_queue_cmd.py` | +20/-0 | TEST T2 (append: `test_sort_created_at_overrides_the_priority_default`, `test_unknown_sort_field_exits_nonzero_naming_valid_fields`) |
| `tests/orchestration/test_list_options.py` | +20/-0 | TEST T1 (append: `test_no_default_sort_field_keeps_original_order_when_sort_not_given`, `test_no_default_sort_field_still_honours_explicit_sort`) |
| `tests/test_grouped_cli.py` | +19/-0 | TEST T3 (append: `test_sort_by_key_orders_entries`, `test_unknown_sort_field_exits_nonzero`) |

### 4eca056c8731849cafc3757671b12a8ee66c1e5d F262 R14 C3: replace plan.md with PLAN15
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +24/-18 | whole-file replace with PLAN15, byte-for-byte verified |

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
3459e7a818e7c7be1ffc6d0c0dfc8f5f8b3700c5
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
$ sha256sum .agent/authored/f262-r14.md .agent/last_block.md
394dc28973984bb8d7803197196f575e0ec72d0893c78180574f2b619c95f51b  .agent/authored/f262-r14.md
394dc28973984bb8d7803197196f575e0ec72d0893c78180574f2b619c95f51b  .agent/last_block.md
```
One digest, twice — PASS.

**LEDGER APPENDS, GATE13 (live_review.md) and DECISION F262 D2 (decisions.md), full byte-forensics per constraint 8**:
```
base size immediately before C1 (live_review.md): 2455026 bytes
GATE13 own byte length: 2386
GATE13 internal newline count: 0
base + 1 + GATE13_length = 2457413
post-C1 file real byte length = 2457413
match: True
tail-equality (last 2386 bytes of file == gate13 slice): True
negative control (byte-flipped gate13 slice vs tail): False (correctly rejected)

base size immediately before C1 (decisions.md): 797530 bytes
DECISION F262 D2 own byte length: 4891
DECISION internal newline count: 12
base + 1 + DECISION_length = 802422
post-C1 file real byte length = 802422
match: True
tail-equality (last 4891 bytes of file == decision slice): True
negative control (byte-flipped decision slice vs tail): False (correctly rejected)
```
Confirmed by direct Python byte read before and after each file, plus
`git diff --stat` reading `2 insertions(+), 1 deletion(-)` for
`live_review.md` and `14 insertions(+), 1 deletion(-)` for
`decisions.md`, both consistent with the prior line losing its "no
newline at end of file" status and one new (possibly multi-line)
region being appended.

**PRODUCTION PAIR, READ AND COUNTED (P1-P5, T1-T3)**:
```
P1 (list_options.py, apply_list_options body): FROM count before 1
P2 (queue_cmd.py, _cmd_queue_list body): FROM count before 1
P3 (queue_cmd.py, queue.list dispatch lambda): FROM count before 1
P4 (memory.py, _cmd_memory_list body): FROM count before 1
P5 (memory.py, memory.list dispatch lambda): FROM count before 1
T1 (test_list_options.py, insertion point): FROM count before 1
T2 (test_queue_cmd.py, insertion point): FROM count before 1
T3 (test_grouped_cli.py, insertion point): FROM count before 1
```
All eight confirmed at exactly 1 occurrence in their target file
before being applied (constraint 1's re-confirmation, using each
file's CURRENT on-disk content, read via the Read tool and a Python
`str.count` check, not only the block's cited line numbers). T1's
FROM was also confirmed to be the file's own last function (nothing
followed it) by reading the file's tail directly. `sys` was confirmed
already imported at module scope in both `queue_cmd.py` and
`memory.py` before applying P2/P4, matching the block's BACKGROUND
FACTS — no new import of `sys` was added.

Full diff, C2 (`c65f8342`), all six files, was read in full before
committing (reproduced in the commit; not repeated here for length).
Every hunk matched its named PAIR/TEST exactly: no other lines in any
of the six files were touched. `git show --numstat c65f8342` reads
`26 0 apps/cli/commands/memory.py`, `25 1 apps/cli/commands/
queue_cmd.py`, `12 9 packages/orchestration/list_options.py`,
`20 0 tests/cli/test_queue_cmd.py`, `20 0 tests/orchestration/
test_list_options.py`, `19 0 tests/test_grouped_cli.py` — matching
the Commits table above exactly.

Also confirmed before applying P2/P3: `_with_list_options` in
`apps/cli/command_catalog.py` already attaches `--sort`/`--desc`/
`--since`/`--until`/`--limit` to every list-shaped catalog entry
(including `queue.list` and `memory.list`) automatically at catalog
build time — no `command_catalog.py` change was needed or made this
round, consistent with the block naming only six files for C2.

```
$ python3 -m py_compile packages/orchestration/list_options.py apps/cli/commands/queue_cmd.py apps/cli/commands/memory.py tests/orchestration/test_list_options.py tests/cli/test_queue_cmd.py tests/test_grouped_cli.py
(exit 0, no output)
```
Exit 0 confirmed for all six touched files, one combined invocation.

Ruff not attempted this round — same refusal shape recorded in every
prior round's handback; not re-attempted since the outcome is already
known and constraint 3 treats it as a non-blocker either way.

**REGRESSION CHECK, constraint 9, BEFORE the combined pytest run**:
```
$ python3 -m pytest tests/cli/test_queue_cmd.py::TestAdd::test_priority_is_recorded_and_orders_the_listing -q
1 passed in 0.83s
```
Note: this test lives under `TestAdd`, not `TestList`, in
`tests/cli/test_queue_cmd.py` (confirmed by `--collect-only -q` after
an initial node-id lookup under `TestList` returned "not found" —
the block's own text names the test by its unqualified method name
only and does not claim a class, so this is a correction to my own
first guess at the node id, not a mismatch with the block). Green,
unmodified — the regression DECISION F262 D2 exists to prevent did
not occur.

**PYTEST, C2's COMBINED RUN**:
```
$ python3 -m pytest tests/orchestration/test_list_options.py tests/cli/test_queue_cmd.py tests/test_grouped_cli.py -q
562 passed in 60.08s (0:01:00)
```
Matches the block's own prediction exactly: 556 pre-existing (9+26+521)
+ 6 new (2+2+2) = 562.

**THE STATE READERS AND THE CANARY, run as ONE combined invocation
per this round's block**:
```
$ python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q
646 passed in 70.28s (0:01:10)
```
646 = 515 + 52 + 21 + 16 + 42, matching GATE13's stated per-suite
baseline exactly. Not moved, as expected: this round's change set
names no path any of these five suites should be sensitive to.

**THE PLAN, BYTE-FOR-BYTE (constraint 7)**:
```
authored PLAN15 slice length: 2880 bytes
written .agent/plan.md length: 2880 bytes
EQUAL (bytes == bytes): True
```
Whole-file replace applied via the Write tool. The first write
produced a file 1 byte longer than the authored slice (a trailing
newline the Write tool call's own content argument carried); caught
by the binary comparison, corrected by stripping the single trailing
`\n` byte, and re-verified: `expected == written` read `True` on the
second check, no remaining gap.

**THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain   (immediately before C4 staged)
(empty)
$ git ls-files .remedy-wt
(no output)
```
Tree clean before C4, nothing under `.remedy-wt/` tracked (a
`.remedy-wt/` scratch directory was used transiently to hold extracted
GATE13/DECISION slice text for the byte-forensics math above; it was
never staged or committed).

Per-commit numstat cross-check against this handback's own Commits
table:
```
$ git show --numstat aab15646
652  0    .agent/authored/f262-r14.md
$ git show --numstat 6315f8f8
430  286  .agent/last_block.md
$ git show --numstat 06f35c1e
14   1    .agent/decisions.md
2    1    .agent/live_review.md
$ git show --numstat c65f8342
26   0    apps/cli/commands/memory.py
25   1    apps/cli/commands/queue_cmd.py
12   9    packages/orchestration/list_options.py
20   0    tests/cli/test_queue_cmd.py
20   0    tests/orchestration/test_list_options.py
19   0    tests/test_grouped_cli.py
$ git show --numstat 4eca056c
24   18   .agent/plan.md
```
Every path and every insertion/deletion count matches the Commits
table exactly — no rename/rewrite percentage substitution was
observed for any commit this round.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r14.md` — NOT stale. Immutable verbatim record
  of this round's own step block.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE13's
  content describes round 13's own verified facts.
- `.agent/decisions.md` — NOT stale. Append-only ledger; DECISION F262
  D2 describes this round's own measured facts about `queue.list`'s
  existing order and the widened `apply_list_options` contract.
- `apps/cli/commands/queue_cmd.py` — NOT stale. Matches PAIR P2 and
  PAIR P3 exactly; full diff read and confirmed.
- `apps/cli/commands/memory.py` — NOT stale. Matches PAIR P4 and PAIR
  P5 exactly; full diff read and confirmed.
- `packages/orchestration/list_options.py` — NOT stale. Matches PAIR
  P1 exactly.
- `tests/orchestration/test_list_options.py` — NOT stale. Matches
  TEST T1 exactly; all tests pass.
- `tests/cli/test_queue_cmd.py` — NOT stale. Matches TEST T2 exactly;
  all tests pass, including the unmodified priority regression test.
- `tests/test_grouped_cli.py` — NOT stale. Matches TEST T3 exactly;
  all tests pass.
- `.agent/plan.md` — NOT stale. Freshly written PLAN15 content
  accurately describes round 14's actual state.

Constraint check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` Already false as of round 2 and remains outside this
round's declared change set too, unchanged from prior rounds' notes.

## Deviations & assumptions

1. **No FROM mismatch occurred.** All eight FROM strings (P1-P5, T1-T3)
   were re-read from each file's current on-disk content before
   applying, per constraint 1, and each occurred exactly once —
   nothing needed to stop or be reported as a mismatch.
2. **The C3 plan.md gate used the Write tool plus a real
   `bytes == bytes` comparison** via an independent Python script
   comparing the PLAN15 text (extracted from the same authored source
   file used for C0a) against the written `.agent/plan.md` in binary
   mode — not `wc -l`/diffstat. Result on the first attempt: 2880
   authored bytes vs 2881 written bytes (a stray trailing newline from
   the Write call), caught by the comparison, fixed by trimming the
   one extra byte, then re-verified exact: 2880 == 2880.
3. **The C1 append to `.agent/decisions.md` got the same full
   byte-forensics treatment as `.agent/live_review.md`**, per
   constraint 8: base size + newline + slice length = post-commit
   size (both files), tail-equality (both files), and a negative-
   control byte-flip rejection (both files) — all six checks passed.
4. **`git commit`'s printed stat matched `--numstat` for every commit
   this round** — no rename/rewrite percentage substitution was
   observed.
5. **Ruff was not attempted** this round (see Verification section) —
   a deliberate choice to avoid a known, already-documented refusal,
   not a new deviation in outcome.
6. **The Bash tool rejected several chained/piped commands this
   round** (a combined `&&`-joined preconditions probe, a multi-line
   `grep -c` block, and a `grep -n ... -A 15 | head` pipe); each was
   re-run as a single standalone invocation (mostly small `python3`
   scripts doing string `.count()` checks in place of `grep -c`),
   with no change to the underlying verification performed —
   consistent with prior rounds' documented sandbox behavior.
7. **The constraint-9 regression test's actual class is `TestAdd`, not
   `TestList`**, in `tests/cli/test_queue_cmd.py` — the block names the
   test method (`test_priority_is_recorded_and_orders_the_listing`)
   without naming a class; my first node-id guess (`TestList::...`)
   returned "not found," corrected via `--collect-only -q`, then
   re-run and confirmed passing. This is a note about my own first
   guess, not a mismatch in the block or the codebase.

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, after C2, and once more before writing this
handback). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r14.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/decisions.md`,
`packages/orchestration/list_options.py`,
`apps/cli/commands/queue_cmd.py`, `apps/cli/commands/memory.py`,
`tests/orchestration/test_list_options.py`,
`tests/cli/test_queue_cmd.py`, `tests/test_grouped_cli.py`,
`.agent/plan.md` and this handback were committed. The bundle's commit
order (C0a, C0b, C1, C2, C3 — this handback C4) was followed exactly,
with C2 as one commit covering all six named files per constraint 5.
Only `queue.list` and `memory.list` were wired this round; no other
list command's handler was touched, per constraint 2.

## Next

**NEXT EXPECTED ACTION: T003 batch 3 — wire `apply_list_options` into
more list commands.** PLAN15's Next Steps names `patch.list`,
`loop.list`, `project.list`, `tournament.list`, `blocker.list`,
`decision.list`, `review.list`, `propose.list`, `test.list`,
`external-builder.submission-list`, and `config.list` as remaining
targets, each needing a check for a queue.list-shaped surprise (an
existing meaningful non-date order) before assuming date-descending is
safe. My one-sentence reasoning for round 15's likely focus:
`project.list` and `tournament.list` look like the next reasonable
batch since PLAN15 flags `patch.list` (needs a look at
`format_intent_list`'s table renderer first) and `loop.list` (needs its
two-collection JSON/text shape reconciled first) as both requiring
extra investigation before wiring, so a plain per-row handler without
either shape's complication is the lower-risk next step — round 15
should grep each remaining command's own tests for an order-asserting
test FIRST, per DECISION F262 D2's precedent, before wiring any of
them.

**THIS IS SESSION 5, ROUND 14** — the operator may continue directly
to round 15 in this same session or start a fresh session per the
self-drive protocol's own judgment; no session/round-limit threshold
has been reached.
