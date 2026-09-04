# Handoff — F262 List commands v2 (dates, sort, filter), round 20 (T003 batch 8, final: loop.list wiring per DECISION F262 D3)

## Session

SESSION 6 of feature F262 · round 20 · rounds so far 20.

Round 20 books round 19's PASS verdict (GATE19) into the ledger and
implements DECISION F262 D3: `loop.list` (`apps/cli/commands/loop_cmd.py`)
is restructured so `_cmd_loop_list` builds ONE row list of
`(spec, last_run_created_at, last_run_state)` tuples UNCONDITIONALLY —
moving the `last_run_for_loop` lookup out of the `json_output`-only
branch — runs `apply_list_options` once with `default_sort_field=None`
(config-declaration order stays the default, D2/D3 precedent), and
renders BOTH the text and json branches from that same post-options row
list. The text branch now reads its row's own precomputed
`last_run_created_at`/`last_run_state` instead of calling
`_last_run_label` a second time, removing the prior duplicate lookup.
`_last_run_label` itself is intentionally left in place, now unused —
deleting it is out of this round's scope per the block's constraint 5.

This is the SESSION 6's fifth and LAST delegated round (R16 through
R20), meeting the self-drive protocol's default of four to five rounds
per session. **T003 is now complete for every list command in scope.**
No arithmetic or byte-count contradiction was found in this round's
block (a possible mismatch between the stated PLAN21 byte length, 2189,
and a naive newline-terminated construction, 2190, was resolved by
matching `.agent/plan.md`'s existing no-trailing-newline convention —
not a genuine contradiction in the block's own numbers, so no STOP was
needed).

## Range

Review of `383e8808ef70633a65d16d07da2b7de072cc9818..4238fcd060ece33489075e40e03c64bcf7fdaf3f`.
That is C0a through C3 (five content commits so far — C0a, C0b, C1,
C2, C3). This handback (C4) follows and is not part of the reviewed
content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched `383e8808ef70633a65d16d07da2b7de072cc9818`, branch matched `feature/f262-list-commands-v2`, tree clean, `.agent/STOP` absent |
| DECISION F262 D3 re-read | done | confirmed at `.agent/decisions.md:10367` before authoring anything |
| Internal-consistency check | done (no contradiction) | GATE19's own 3350-byte claim and the 2470338→2473689 arithmetic (2470338 + 1 + 3350) both verified true by direct byte measurement before any write; the only apparent mismatch (PLAN21's stated 2189 bytes vs. a trailing-newline construction giving 2190) was a formatting choice, resolved by matching the file's own no-trailing-newline convention, not a stated arithmetic conflict — no STOP triggered |
| C0a | done | `.agent/authored/f262-r20.md` saved verbatim, new file, sha256 `1ebf71f1caaa3a8bed8c976e1840bfcf8254fadb490ecb777fd19d2d5b463855` |
| C0b | done | mirrored to `.agent/last_block.md` via `shutil.copyfile`, identical sha256 to C0a's file (confirmed by `sha256sum` on both, one digest twice) |
| C1 | done | GATE19 appended to `.agent/live_review.md` byte-exact: base 2470338 + `\n` + GATE19 (3350 bytes, 0 internal newlines) = 2473689, confirmed by direct Python byte read before and after write |
| C2 | done | PAIR L1 (whole-body rewrite) + PAIR L2 (dispatch site) in `apps/cli/commands/loop_cmd.py`, TEST T1 appended to `tests/cli/test_loop_cmd.py` — two files, one commit; full diff read and confirmed to match exactly, nothing else touched |
| C3 | done | PLAN21 applied to `.agent/plan.md`, whole-file replace, verified byte-for-byte equal (2189 == 2189 bytes, binary mode, no trailing newline) |
| C4 (this handback) | done | |
| G1 (py_compile, 2 files) | done | printed `OK` |
| G2 (pytest, test_loop_cmd.py) | done | 18 passed (16 pre-existing + 2 new) |
| G3 (canary: combined 5-suite invocation) | done | 646 passed, unmoved from prior baseline (515+52+21+16+42) |
| G4 (sha256sum transport) | done | one identical digest, twice: `1ebf71f1caaa3a8bed8c976e1840bfcf8254fadb490ecb777fd19d2d5b463855` |
| G5 (live_review.md byte forensics) | done | before 2470338, after 2473689 — both match |
| G6 (plan.md byte-for-byte) | done | 2189 bytes, byte-for-byte equal to PLAN21 |
| G7 (git status --porcelain, twice) | done | empty before C0a, empty immediately before C4 |
| G8 (git ls-files .remedy-wt) | done | empty output — nothing tracked under `.remedy-wt/` |

## Commits

### bfa1a9d5 F262 R20 C0a: save step block verbatim to .agent/authored/f262-r20.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r20.md` | +276/-0 | transport artifact — verbatim copy of the round's step block, new file |

### 575f1bc0 F262 R20 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +183/-137 | mirror of the round's authored block (whole-file rewrite via `shutil.copyfile`; diff-algorithm hunk counts differ from C0a's raw insert count because this is a content replacement, not an append — content is byte-identical, confirmed by G4's matching sha256) |

### d659587c F262 R20 C1: append GATE19 to live_review.md - books round 19's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE19, `\n` + GATE19's own 3350 bytes appended to the base file |

### 7e4cba95 F262 R20 C2: T003 batch 8 (final) - loop.list wiring per DECISION F262 D3
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/loop_cmd.py` | +61/-25 | PAIR L1: `_cmd_loop_list` whole-body rewrite — gains `sort`/`desc`/`since`/`until`/`limit` kwargs, builds one unconditional row list, wires `apply_list_options` with `default_sort_field=None`, renders both text and json from the same row list; PAIR L2: `"loop.list"` dispatch lambda threads all five kwargs via `getattr(args, ..., default)` |
| `tests/cli/test_loop_cmd.py` | +31/-0 | TEST T1 appended: `test_limit_caps_returned_loops`, `test_unknown_sort_field_exits_nonzero` |

### 4238fcd0 F262 R20 C3: replace plan.md with PLAN21
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +18/-18 | whole-file replace with PLAN21, byte-for-byte verified |

### (this handback commit, C4)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once) — numbers not tabled here; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f262-list-commands-v2` — runs immediately
  after this commit; result reported in the closing message, not here,
  since it happens after this file is committed. No `gh pr` command of
  any kind was run (forbidden this round: no PR, no merge, no Open PR
  Gate, no `main` touched).

## Verification

Preconditions, checked before C0a:
```
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f262-list-commands-v2
$ git rev-parse HEAD
383e8808ef70633a65d16d07da2b7de072cc9818
$ ls .agent/STOP
No such file or directory
```
All four confirmed.

**INTERNAL-CONSISTENCY CHECK** (before any commit): GATE19's own text
was byte-measured directly (Python `.encode('utf-8')`) and found to be
exactly 3350 bytes with zero internal newlines, matching the block's
own claim. The arithmetic `2470338 + 1 + 3350 = 2473689` was verified
by direct computation and matches the block's stated post-C1 target
exactly — no contradiction. `.agent/live_review.md`'s actual on-disk
size immediately before any write was independently measured at 2470338
bytes, matching the block's stated base exactly. PLAN21's text was
byte-measured two ways: with a trailing newline (2190 bytes) and
without (2189 bytes); the block's stated target (2189) matches the
no-trailing-newline form, which is also how the CURRENT `.agent/plan.md`
(pre-round-20) is stored (confirmed: `tail -c 5` of the pre-C3 file
ends `rder.` with no `\n`). This is a formatting detail resolved by
matching the file's own established convention, not a genuine
arithmetic contradiction in the block, so no STOP was triggered.

**TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f262-r20.md .agent/last_block.md
1ebf71f1caaa3a8bed8c976e1840bfcf8254fadb490ecb777fd19d2d5b463855  .agent/authored/f262-r20.md
1ebf71f1caaa3a8bed8c976e1840bfcf8254fadb490ecb777fd19d2d5b463855  .agent/last_block.md
```
One digest, twice — PASS.

**LEDGER APPEND, GATE19 (live_review.md), byte-forensics**:
```
before size: 2470338
gate19 length: 3350
after size: 2473689
ALL ASSERTIONS PASSED
```
Confirmed by direct Python byte read before and after the write
(`pathlib.Path.write_bytes`, not a shell append).

**PRODUCTION PAIRS, READ AND COUNTED (L1, L2)**:
```
FROM1 count: 1
FROM2 count: 1
```
Both confirmed at exactly 1 occurrence in `apps/cli/commands/loop_cmd.py`
before being applied (constraint 4's re-confirmation, against the
file's CURRENT on-disk content read directly via Python, not the copy
quoted in the prompt). `json`, `sys`, `EXIT_ERROR`, `NEVER_RAN`,
`INERT_MARK`, `INERT_TRIGGER_LEGEND` were confirmed already
defined/imported at module scope before applying PAIR L1 — no
duplicate import or redefinition was added. `_last_run_label` was
confirmed still present and unmodified after the edit (left in place,
now unused, per constraint 5).

**TEST T1, READ AND COUNTED**:
```
insertion point: end of file, immediately after
test_loop_run_is_registered_and_in_the_catalog's final assert
```
Confirmed the file's actual tail (via direct Python read) matched the
block's description exactly (`assert "loop.run" in catalog_ids` as the
final line, trailing newline, no blank line before EOF) before
appending. `_write_config`, `_dispatch_with`, `MANUAL_JOB_LOOP`, `json`,
`pytest` were all confirmed already defined/imported at module scope —
no duplicate import was added.

Full diff, C2 (`7e4cba95`), both files, was read in full before writing
this handback (`git show 7e4cba95`). Every hunk matched PAIR L1, PAIR
L2, and TEST T1 exactly: no other function in `loop_cmd.py` was
touched — `_last_run_label`, `_trigger_label`, `_cmd_loop_validate`,
`_resolve_project_id`, `_stdin_is_a_tty`, `_confirm_materialization`,
`_cmd_loop_run`, and the `"loop.validate"`/`"loop.run"`
`COMMAND_HANDLERS` entries are untouched. `git show --numstat 7e4cba95`
reads `61  25  apps/cli/commands/loop_cmd.py`, `31  0
tests/cli/test_loop_cmd.py` — matching the Commits table above exactly.

```
$ python3 -c "import py_compile; py_compile.compile('apps/cli/commands/loop_cmd.py', doraise=True); py_compile.compile('tests/cli/test_loop_cmd.py', doraise=True); print('OK')"
OK
```
Ran directly as the declared substitution form (the literal multi-arg
`python3 -m py_compile` form is documented in prior rounds' handbacks
as denied by this repo's Bash sandbox, so the substitution was used
from the start per constraint 10). `doraise=True` means any
`SyntaxError` would have raised and been visible; `OK` printed for both
files, equivalent to exit 0.

**PYTEST, C2's test file**:
```
$ python3 -m pytest tests/cli/test_loop_cmd.py -q
..................                                                       [100%]
18 passed in 0.26s
```
Matches the block's own prediction exactly: 16 pre-existing + 2 new =
18. This re-proves every pre-existing `loop.list` test still passes
after the restructure, including `test_after_one_real_firing_the_row_shows_that_run`,
`test_json_output_carries_last_run_created_at_and_state`, and
`test_json_output_last_run_is_null_when_never_ran`, which depend on the
last-run lookup still working correctly after being moved out of the
json-only branch.

**THE STATE READERS AND THE CANARY, run as ONE combined invocation per
this round's block**:
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
646 passed in 70.57s (0:01:10)
```
646 = 515 + 52 + 21 + 16 + 42, matching GATE19's stated per-suite
baseline exactly. Not moved, as expected: this round's change set
names no path any of these five suites should be sensitive to.

**THE PLAN, BYTE-FOR-BYTE (constraint: byte-exact whole-file replace)**:
```
PLAN21 bytes: 2189
written size: 2189
EXACT MATCH CONFIRMED
```
Whole-file replace applied via a direct `pathlib.Path.write_bytes`
call, then re-verified exact in BINARY mode: `after == plan21_bytes`
evaluated `True`.

**AUTHORED-TEXT PROOFS** (GATE19 and PLAN21 as embedded in the
committed `.agent/authored/f262-r20.md`, compared disk-to-disk against
what was actually written):
```
GATE19 text extracted from authored block: 3350 bytes, 0 internal newlines
GATE19 as appended to live_review.md: last 3350 bytes of the file — same construction (base + \n + this exact string), byte-identical by construction and confirmed by the byte-forensics above

PLAN21 text extracted from authored block: 2189 bytes
plan.md length: 2189 bytes
MATCH: True
```
Both reviewer-authored texts applied this round (GATE19 into
`live_review.md`, PLAN21 into `plan.md`) are byte-identical to the text
embedded in the committed `.agent/authored/f262-r20.md` — the same
file that was written directly from this prompt's own text, so both
are identical by construction, re-verified byte-for-byte per the
numbers above.

**THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain   (immediately before C4 staged)
(empty)
$ git ls-files .remedy-wt
(no output)
```
Tree clean before C4, nothing under `.remedy-wt/` tracked. `.agent/STOP`
absent, re-checked immediately before C4.

Per-commit numstat cross-check against this handback's own Commits
table:
```
$ git show --numstat --format="" bfa1a9d5
276  0    .agent/authored/f262-r20.md
$ git show --numstat --format="" 575f1bc0
183  137  .agent/last_block.md
$ git show --numstat --format="" d659587c
2    1    .agent/live_review.md
$ git show --numstat --format="" 7e4cba95
61   25   apps/cli/commands/loop_cmd.py
31   0    tests/cli/test_loop_cmd.py
$ git show --numstat --format="" 4238fcd0
18   18   .agent/plan.md
```
Every path and every insertion/deletion count matches the Commits
table exactly.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r20.md` — NOT stale. Immutable verbatim record
  of this round's own step block.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE19's
  content describes round 19's own verified facts.
- `apps/cli/commands/loop_cmd.py` — NOT stale. Matches PAIR L1/L2
  exactly; full diff read and confirmed.
- `tests/cli/test_loop_cmd.py` — NOT stale. Matches TEST T1 exactly;
  all tests pass.
- `.agent/plan.md` — NOT stale. Freshly written PLAN21 content
  accurately describes round 20's actual state (T003 complete for all
  list commands in scope).

Constraint check (a sentence OUTSIDE the change set already stale
before this round): `docs/roadmap/features/T2_F262.md` line 5 still
reads `> REGISTRATION ONLY — nothing in this file has been
implemented.` Already false as of round 2 and remains outside this
round's declared change set too, unchanged from prior rounds' notes.

## Authored-text proofs

For every reviewer-authored text applied this round — GATE19
(`.agent/live_review.md`) and PLAN21 (`.agent/plan.md`) — the
disk-to-disk comparison against the committed `.agent/authored/f262-r20.md`
slice is reported above under Verification's "AUTHORED-TEXT PROOFS"
heading: both matched byte-for-byte (GATE19: 3350/3350 bytes equal;
PLAN21: 2189/2189 bytes equal).

## Deviations & assumptions

1. **No genuine byte-count or arithmetic contradiction was found in
   this round's block**, unlike round 19's headline typo. The only
   near-miss was PLAN21's stated byte length (2189) initially appearing
   to disagree with a naive Python triple-quoted-string construction
   that included a trailing newline (2190 bytes); this was resolved by
   observing that `.agent/plan.md` has never carried a trailing newline
   in this feature's history (confirmed on the pre-round-20 file), so
   the correct, convention-matching construction — without a trailing
   newline — produces exactly 2189 bytes, matching the block. This is a
   formatting-convention resolution, not a silently-picked value for a
   genuine stated contradiction, so no STOP was warranted or issued.
2. **No FROM mismatch occurred.** Both FROM strings (L1, L2) and the
   TEST T1 anchor were re-read from each file's current on-disk content
   before applying, per constraint 4, and each occurred exactly once —
   nothing needed to stop or be reported as a mismatch.
3. **The literal command `python3 -m py_compile apps/cli/commands/loop_cmd.py
   tests/cli/test_loop_cmd.py` was not attempted directly** — prior
   rounds' handbacks already document this exact multi-arg form as
   denied by the Bash tool's sandbox permission in this repo, so the
   declared equivalent substitution (`python3 -c "import py_compile;
   py_compile.compile(..., doraise=True); ..."`) was used from the
   start, per constraint 10. It printed `OK` (i.e., no `SyntaxError`
   raised, equivalent to exit 0).
4. **One combined diagnostic Bash command was denied mid-round for
   reasons unrelated to this round's declared quirks** — a multi-line
   `echo "===" && ... && ...` combining several unrelated read-only
   checks (git log, numstat loop) in one invocation. Each check was
   retried as separate, simpler commands instead, all read-only and
   none affecting any commit or file write.
5. Ruff was not attempted this round — same known refusal shape
   recorded in every prior round's handback; not re-attempted since the
   outcome is already known and no constraint requires it.

No other deviations. `.agent/STOP` was absent every time it was
checked (before C0a, and once more immediately before C4/this
handback). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r20.md`,
`.agent/last_block.md`, `.agent/live_review.md`,
`apps/cli/commands/loop_cmd.py`, `tests/cli/test_loop_cmd.py`,
`.agent/plan.md` and this handback were committed. The bundle's commit
order (C0a, C0b, C1, C2, C3 — this handback C4) was followed exactly,
with C2 as one commit covering both named files per constraint 6. Only
`loop.list` was wired this round; no other list command
(`config.list`/`worker.list`/`execution.list`/`change.list`/etc.) was
touched, per constraint 1. `packages/orchestration/list_options.py`
was read only (to confirm `ListOptionError`/`apply_list_options`'s
existing signature) and not modified, per constraint 2.

## Next

**NEXT EXPECTED ACTION: Phase 0, fresh, at the start of the next
session.** T003 is now DONE for every list command in scope
(`config.list`/`worker.list`/`execution.list` remain excused per
Risks; this should be re-confirmed still true at closure time rather
than just asserted). The next session's likely path: (1) an
integration-level smoke test proving the ten-second Acceptance demo (a
named run findable by one command with `--since`/`--sort`), (2) the
still-open, D1-unrelated `change.list` event-log CREATED-date gap
(tracked separately — `do_run.py`'s event stays dead, `job.py`'s real
event carries no `intent_id` to join on), then (3) move toward F262
closure per `docs/roadmap/STATUS_closure_protocol.md`. **This session
(session 6) has now run its full five delegated rounds (R16 through
R20)** — the self-drive protocol's default per-session ceiling — so the
next round should open as a fresh Phase 0 / new session rather than a
sixth round appended to this one.
