# Handback — F040 · SESSION 3 · round 15

> Written by the WORKER as the round's final commit, C6. `.agent/STOP` was
> re-read from disk before the first commit of this round and again
> immediately before this commit; it was ABSENT both times. Every number
> below that IS a measurement was taken from `subprocess.run(...).returncode`,
> `hashlib.sha256`, or a plain `open(...).read()` byte comparison inside the
> scripts under `.remedy-wt/g*.py`; not one was read through a pipe or from
> `$?`.

## Session

SESSION 3 of feature F040 · round 15 · rounds so far 15.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached.

## Range

Review of `e1050f8c..4eb957b7` (C0a through C5); this commit (C6) rewrites
this file on top of that range.

## Commits

### 7b18196b docs(f040): save the round 15 block verbatim (C0a)
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f040-r15.md` | 317/0 | new — verbatim copy of `.remedy-wt/f040-r15-block.md` via `shutil.copyfile` |

### dc9471eb docs(f040): mirror the round 15 block into last_block (C0b)
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 241/269 | whole-file rewrite — mirrors the round 15 block, replacing round 14's |

### ec087579 docs(f040): advance the plan to round 15 (C1)
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 10/10 | rewritten byte-for-byte from the PLAN15 slice |

### 4f405b74 docs(f040): append the R14 verdict to the ledger (C2)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | RECORD15 slice appended (R14 verdict) |

### 7bbec9a6 feat(f040): register job.digest in the command catalog (C3)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | 14/0 | one new `CommandEntry` for `job.digest`, inserted between `job.report` and `job.fences` per constraint 7 |

### 791bb4c1 feat(f040): add remedy job digest CLI parity (C4)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job.py` | 51/0 | new `_cmd_job_digest` function (placed immediately after `_cmd_job_report`) plus its `COMMAND_HANDLERS["job.digest"]` dispatch entry |

### 4eb957b7 test(f040): guard remedy job digest against the route's own envelope (C5)
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_job_digest_cli.py` | 166/0 | new — pytest guard, red-proved against all four G6 mutations |

### (this commit) docs(f040): write the round 15 handback (C6)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | not orderable here (§3 item 14) | this file |

All seven `+`/`-` figures above (317/0, 241/269, 10/10, 2/0, 14/0, 51/0, 166/0)
are taken verbatim from `git diff --numstat <commit>^..<commit>`, re-run
fresh for this table per G7's own instruction that this column comes from
that gate's output.

## External actions

- `git worktree add .remedy-wt/wt-r15-g3 HEAD --detach` (at `4f405b74`, after
  C2) — for G3's negative control.
- `git worktree remove .remedy-wt/wt-r15-g3 --force` — removed after G3.
- `git worktree add .remedy-wt/wt-r15-g6 HEAD --detach` (at `4eb957b7`, after
  C5) — for G6's four mutation red proofs. No `node_modules` symlink was
  needed: C5's guard is a pure pytest module exercising Python functions
  directly, so the worktree only ever needed `git`, not `npm`.
- `git worktree remove .remedy-wt/wt-r15-g6 --force` — removed after G6.
- `git push -u origin feature/f040-completion-digest` runs immediately after
  this commit, per the block's Handback instruction. No PR created, nothing
  merged, no force-push, no other branch touched.

## Verification

**G1 TRANSPORT, at C0b.** All three of `.remedy-wt/f040-r15-block.md`,
`.agent/authored/f040-r15.md` and `.agent/last_block.md` measured equal at
sha256 `1e55df4e2b1b3a8cc99565759055386a5c535e280481cce854395f322d1ec98d`,
23913 bytes. REAL (direct byte comparison via `hashlib.sha256`, no subprocess
involved). PASS.

**G2 THE PLAN, at C1.** `.agent/plan.md` byte-equal to the PLAN15 slice: True
(direct text comparison). 2210 bytes, 43 lines — **under 50**: True. Holds
`## Goal`, `## Next Steps` and `F040` (matches `\bF\d{3}\b`): True, True,
True. PASS.

**G3 THE RECORD APPEND, at C2, USING THE GENERALIZED READING (b) OF
CONSTRAINT 4.** Base re-measured via `git show 4f405b74^:.agent/live_review.md`:
1731700 bytes, ends WITH a trailing newline (last byte `\n`, preceded by the
period ending R14's own verdict paragraph — unlike prior rounds' bases, this
round's base already carried a trailing newline). Slice (RECORD15): 3885
bytes, also ends with a trailing newline. Committed: 1735586 bytes.

Reading (a): `base` is a byte prefix of `committed` → True;
`base + "\n" + slice == committed` → True.

Reading (b), literal application of this round's own "FINAL, GENERALIZED
FORM" (constraint 4): split the slice into N paragraphs on blank lines — N =
1 (RECORD15 is one dense paragraph, no internal blank line). Because the
base this round already ended with `\n`, adding the separator `\n` produces
TWO consecutive newlines before the slice — a genuine blank-line boundary,
not a fusion — so paragraph 1 lands as its OWN standalone blank-line unit in
the committed file rather than fused with the base's last paragraph. Checked
by the stated rule regardless ("paragraph 1 is ALWAYS checked by SUFFIX
match"): the committed file's blank-line units were computed by splitting on
`\n{2,}`, giving 765 units; unit index 764 (the last) both ENDS WITH
paragraph 1 AND equals it by raw equality (`committed_units[-1] ==
slice_bytes` → True), so the suffix check the rule specifies holds (True),
and the raw-equality bonus holds too since N = 1 has no paragraphs 2..N to
check separately. Reading (b) result: **True** — no gap this round, unlike
R14's own N=1 case. Negative control, inside a disposable worktree
(`.remedy-wt/wt-r15-g3`, scratch copy, removed after): one byte flipped
inside the appended slice (offset 1731801, absolute, well inside paragraph
1) → reading (a)'s reconstruction check goes **False**, reading (b)'s suffix
check goes **False** (`para1_hits: []`); restored → both return to **True**,
byte-equal to the unmutated committed content. `git worktree list` returned
to one line after removal. PASS.

**G4 THE LEDGER, at C2.** Computed by DIFFERENCE between `4f405b74^` (base)
and `4f405b74` (committed) `.agent/live_review.md`, never from the slice:
registered ids (`^- R-\d+ — `) ADDED `[]` REMOVED `[]`; resolved ids
(`^Done: R-\d+`) ADDED `[]` REMOVED `[]`; `DECISION F040 D\d+` ids ADDED `[]`
REMOVED `[]`; `^Gate: F040 R14 — ` lines: 0 before → 1 after. Open count
(registered minus resolved) 262 before → **262 after** (unchanged — this
round registers no new finding and resolves none). Distinct registered
317→317; distinct resolved 55→55. No id's resolved-status changed.

**G5 THE COMMAND'S SHAPE, at C3 and C4.** Over `apps/cli/command_catalog.py`:
one `CommandEntry(...)` block with `command_id="job.digest"` (count = 1);
its `args` tuple text is `args=(_JOB_ID, _JSON_OPT)` and `supports_json=True`
— both confirmed by direct import (`get_command("job.digest").args` resolves
to `(_JOB_ID, _JSON_OPT)`'s own `ArgDef` values, `supports_json` is `True`).

Over `apps/cli/commands/job.py` with comments stripped, `_cmd_job_digest`'s
own body (from its `def` line to the next top-level `def`, 1610 characters):

| Marker | Offset |
|---|---|
| `resolve_job_id(` | 508 |
| `load_job(` | 558 |
| `except JobNotFoundError` | 579 |
| `resolve_data_root(` | 916 |
| `load_run_events(` | 949 |
| `build_job_digest(` | 1080 |
| `_json.dumps(` (1st, inside the except branch) | 664 |
| `_json.dumps(` (2nd, inside the `if json_output:` success branch) | 1145 |

The six non-`_json.dumps` markers are strictly increasing (508 < 558 < 579 <
916 < 949 < 1080). The two `_json.dumps(` occurrences straddle that
sequence exactly as the error/success split requires: the first (664) falls
between `except JobNotFoundError` (579) and `resolve_data_root(` (916) —
the error branch necessarily resolves before the job's data can be loaded —
and the second (1145) falls after `build_job_digest(` (1080), inside the
success branch's own `if json_output:`. `build_job_digest(` occurs exactly
once; `_json.dumps(` occurs exactly twice in that span (both counted above);
`resolve_job_id(`, `load_job(`, `resolve_data_root(` and `load_run_events(`
each occur exactly once. Separately: the key `"job.digest"` occurs exactly
once in the `COMMAND_HANDLERS` dict, and its value's source text contains
both `_cmd_job_digest(` and `json_output=getattr(args, "json", False)`. All
computed by `.remedy-wt/g5_check.py`. PASS.

**G6 THE GUARD'S OWN RUN AND ITS RED PROOF, at C5.** First,
`python3 -m pytest tests/cli/test_job_digest_cli.py -q` in the primary
checkout: **REAL EXIT 0, 9 passed**. Second, THE RED PROOF, over a SCRATCH
COPY of `apps/cli/commands/job.py` inside the disposable worktree
`.remedy-wt/wt-r15-g6` (removed after), for each of the four ordered
mutations, anchor uniqueness asserted (within `_cmd_job_digest`'s own span)
before each replacement:

| Mutation | Anchor unique count | Real exit | Failed node id(s) | Restored byte-equal + re-green |
|---|---|---|---|---|
| (a) `if json_output:` → `if True:` (guarding (v)'s JSON print) | 1 | 1 | `TestBareModeIsNotJson::test_bare_output_does_not_parse_as_json` | True, 9 passed |
| (b) `print(_json.dumps(digest, indent=2))` → wraps in `{'digest': digest}` | 1 | 1 | `TestJsonModeMatchesTheEnvelopeExactly::test_the_json_payload_equals_build_job_digest_independently_computed`, `...::test_the_payload_is_not_wrapped_in_an_extra_key` | True, 9 passed |
| (c) delete the (ii) except branch's `if json_output:`/`else:` split | 1 | 1 | `TestUnknownJobId::test_json_mode_exits_1_with_a_json_payload_on_stdout` | True, 9 passed |
| (d) `job_id = resolve_job_id(job_id_str)` → `job_id = job_id_str` | 1 | 1 | `TestShortIdPrefixResolves::test_an_eight_character_prefix_matches_the_full_id_digest` | True, 9 passed |

Every one of the four mutations turned the guard red on the first version of
the guard. `git worktree list` returned to one line after removal. PASS.

**G7 THE SUITES AND THE TREE, at C5.**
- `python3 -m pytest tests/cli/ -q` → REAL EXIT 0, 1482 passed.
- `python3 -m pytest tests/ui_contracts/ -q` → REAL EXIT 0, 809 passed, 4 skipped.
- `python3 -m pytest tests/ui_server/ -q` → REAL EXIT 0, 515 passed.
- `python3 -m pytest tests/docs/ -q` → REAL EXIT 0, 295 passed.

`git status --porcelain`: `''` (empty). `git ls-files --others
--exclude-standard`: 0 untracked. `git worktree list`: one line, the primary
checkout only. `git diff --numstat` per commit C0a..C5:
- C0a `7b18196b` → `317	0	.agent/authored/f040-r15.md`
- C0b `dc9471eb` → `241	269	.agent/last_block.md`
- C1 `ec087579` → `10	10	.agent/plan.md`
- C2 `4f405b74` → `2	0	.agent/live_review.md`
- C3 `7bbec9a6` → `14	0	apps/cli/command_catalog.py`
- C4 `791bb4c1` → `51	0	apps/cli/commands/job.py`
- C5 `4eb957b7` → `166	0	tests/cli/test_job_digest_cli.py`

Every insertion figure in the Commits table above is copied from this list.
C6's own count is not orderable here and is not ordered (§3 item 14).

## Authored-text proofs

`.remedy-wt/f040-r15-block.md` → `.agent/authored/f040-r15.md` and
`.agent/last_block.md`: sha256-equal, byte-length-equal (see G1). PLAN15 and
RECORD15 slices applied byte-for-byte, verified structurally by G2 and G3.
No other reviewer-authored text was applied this round —
`apps/cli/command_catalog.py`'s new entry, `apps/cli/commands/job.py`'s new
function and dispatch line, and `tests/cli/test_job_digest_cli.py` are a
SPEC, not a slice, per constraint 1.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f040-r15.md` | done | G1 verifies |
| C0b mirror the block into `.agent/last_block.md` | done | G1 verifies |
| C1 rewrite `.agent/plan.md` from PLAN15 | done | G2 verifies; byte-equal, 43 lines, under 50 |
| C2 append RECORD15 to `.agent/live_review.md` | done | G3, G4 verify; open count 262→262 |
| C3 register `job.digest` in the catalog | done | G5 verifies; exactly one entry |
| C4 add `_cmd_job_digest` + its dispatch wiring | done | G5 verifies; markers in order, occurrence counts correct |
| C5 build `tests/cli/test_job_digest_cli.py` | done | G6 verifies, all four mutations red-proved first try |
| C6 rewrite `.agent/handoff.md` | done | this file |
| G1 transport | PASS | at C0b |
| G2 the plan | PASS | at C1 |
| G3 the record append | PASS | at C2 — no gap this round (see Verification) |
| G4 the ledger | PASS | at C2 |
| G5 the command's shape | PASS | at C3 and C4 |
| G6 the guard's own run and its red proof | PASS | at C5 — no repair needed |
| G7 the suites and the tree | PASS | at C5 |

## Deviations & assumptions

1. **Constraint 5(vi) says "five `print` lines" but explicitly enumerates
   SIX distinct pieces of content** (the job id; `state`; `headline`; the
   cost line; the decisions line; `primary_action.label`). I read the
   enumerated, item-by-item list as load-bearing (it names every field and
   its exact source) and the numeral "five" as a miscount, and implemented
   six `print` calls carrying exactly the six named pieces, in the stated
   order, on separate lines — matching `_cmd_job_report`'s own established
   convention of one line per field rather than combining the job id with
   another field. Nothing in G5 or G6 checks a literal print-statement
   count, so this reading affects no gate; the guard's own
   `test_bare_output_names_the_job_id_and_the_digest_state` test passes
   either way, since it only asserts substring presence. This is a
   non-blocking, damage-free numeral slip in the REVIEWER'S OWN block text
   (constraint 5(vi)), not a defect anywhere under `packages/`, `apps/`,
   `tests/` or `docs/` — declared here per the same "into this handback"
   route prior rounds have used for prose-precision findings in the block
   itself (amend0827 rule 2/4). `.agent/prose_slips.md` is outside this
   round's declared change set and was not touched.
2. **G5's own text lists the seven/eight offset markers in an order
   ("resolve_job_id, load_job, except, resolve_data_root, load_run_events,
   build_job_digest, first `_json.dumps(`, second `_json.dumps(`") that
   cannot itself be strictly increasing in source position**, because the
   error branch's own `_json.dumps(` call (guarding (ii)) necessarily
   executes, and therefore sits in source, BEFORE `resolve_data_root(`/
   `load_run_events(`/`build_job_digest(` — those three calls only run
   after a successful `load_job`, which is exactly what the except branch
   exists to short-circuit. I read this as G5's own "except... which
   straddle the `if json_output`/`else` branch" clause already anticipating
   this: the six non-`_json.dumps` markers are checked as strictly
   increasing among themselves, and the two `_json.dumps(` occurrences are
   reported separately with their true offsets (664 and 1145) rather than
   forced into the six-marker sequence. Same non-blocking classification as
   item 1: a reviewer-prose-ordering ambiguity, resolved by reporting the
   real, honestly-measured offsets rather than manufacturing an ordering
   the actual code cannot have while still satisfying constraint 5's own
   fixed call order.
3. **This round's own G3 base unexpectedly carried a trailing newline**
   (unlike every prior round's base, which lacked one) — see Verification's
   G3 section for the full mechanics. This is a fact about THIS round's
   bytes, not a wording defect, and reading (b) as literally stated handled
   it correctly (no gap, unlike R14's own N=1 case): because the join
   produced a genuine blank line rather than a fusion, paragraph 1 landed
   as its own standalone unit and satisfied both the suffix check and raw
   equality. No correction to the gate template's wording was needed this
   round; it is left as the "FINAL, GENERALIZED FORM" constraint 4 states.
4. No commit was reordered, dropped or added relative to the block's fixed
   C0a→C0b→C1→C2→C3→C4→C5→C6 sequence.

## Next

T003's remaining slice: the end-to-end (finish a fake job while the UI is
"away", reopen, hero shows the right CTA, dismiss, no re-show), then the
integration gate and closure. Wiring `onOpenDecisions`/`onPrimaryAction` for
real needs its own resolution design (DECISION F040 D5's "in-page action")
and is not yet scheduled.
