# Handoff — F262 List commands v2 (dates, sort, filter), round 4 (T002 batch 2, memory.list)

## Session

SESSION 1 of feature F262 · round 4 · rounds so far 4.

Round 4 ships T002 batch 2: `memory.list` gains `updated_at` in its
`--json` output (the model already carries the field; the json branch
simply omitted it) and both `created=`/`updated=` in its text output.
Single production file (`apps/cli/commands/memory.py`), single test
file (`tests/test_grouped_cli.py`, two new methods in the existing
`TestMemoryCLIContract` class). No model or store change, no behavior
change beyond the printed/exported fields.

## Range

Review of `0d85f9fcc4381d0143c35f2e40bde6079e804789..a07c6cd2492c3dceea58d145f75df6746abbe81d`.
That is C0a through C3 (five content commits before this handback —
C0a, C0b, C1, C2, C3). This handback (C4) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched, branch matched, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r4.md` saved verbatim, cmp exit 0 |
| C0b | done | mirrored to `.agent/last_block.md`, sha256 identical |
| C1 | done | GATE3 appended to `.agent/live_review.md` byte-exact |
| C2 | done | PAIR M1 (append-shaped) + PAIR M2 (rewrite) applied to `memory.py`, two new test methods added, one commit |
| C3 | done | PLAN5 applied to `.agent/plan.md`, whole-file replace |
| C4 (this handback) | done | |
| G1 TRANSPORT | done | PASS — one digest, twice |
| G2 THE LEDGER APPEND | done | PASS — arithmetic matched, tail equal, negative control rejected |
| G3 THE TWO PAIRS | done | PASS — M1 FROM 1→1 (append-shaped, expected), TO 1; M2 FROM 1→0, TO 0→1; `_cmd_memory_recall` confirmed untouched; py_compile exit 0 ×2 |
| G4 THE TESTS, BEFORE AND AFTER | done | PASS — 511 before C2, 513 after (base + 2), fully green both times |
| G5 STATE READERS + CANARY | done | PASS — 515/52/21/16/42, unmoved from session baseline |
| G6 THE PLAN | done | PASS — cmp exit 0, 37 lines, both header counts 1 |
| G7 THE TREE, COMMITS, SWEEP | done | PASS — tree clean, `.remedy-wt` untracked, numstats match, staleness declared |

## Commits

### 831747fd F262 R4 C0a: save step block verbatim to .agent/authored/f262-r4.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r4.md` | +246/-0 | transport proof — verbatim `cp` of the reviewer's step block (`.remedy-wt/f262-r4-block.txt`), new file |

### dfe89e7e F262 R4 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +158/-215 | mirror of the round's authored block via `cp` (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### 2e1f7323 F262 R4 C1: append GATE3 to live_review.md - books round 3's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE3 (extracted from committed authored file by marker index), `\n` + GATE3's own bytes appended to the base file |

### 66d84b2e F262 R4 C2: memory.list gains updated_at in --json, created/updated in text output
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/memory.py` | +2/-1 | PAIR M1 (append-shaped: adds `"updated_at": e.updated_at,` after `"created_at": e.created_at,` in `_cmd_memory_list`'s json dict) and PAIR M2 (rewrite: extends the text-branch print with `created=`/`updated=`) |
| `tests/test_grouped_cli.py` | +25/-0 | two new test methods added by hand to the existing `TestMemoryCLIContract` class per the TEST SPEC: `test_list_json_has_updated_at_key`, `test_list_text_shows_created_and_updated` |

### a07c6cd2 F262 R4 C3: replace plan.md with PLAN5
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +18/-21 | whole-file replace with PLAN5 extracted from the committed authored file (per constraint 6) |

### (this handback commit, C4)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push origin feature/f262-list-commands-v2` — runs immediately
  after this commit, per the Bundle's C4 step; reported in the closing
  message, not here, since it happens after this file is committed. No
  `gh pr` command of any kind was run (forbidden this round: no PR, no
  merge, no Open PR Gate).

## Verification

Preconditions, checked before C0a:
```
$ git status --porcelain
(empty)
$ git rev-parse HEAD
0d85f9fcc4381d0143c35f2e40bde6079e804789
$ git branch --show-current
feature/f262-list-commands-v2
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
```
All four confirmed.

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f262-r4.md .agent/last_block.md
420f487092908823e0e1b43459f8860cd777ad884f2a95841049c09a1756e1df  .agent/authored/f262-r4.md
420f487092908823e0e1b43459f8860cd777ad884f2a95841049c09a1756e1df  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE LEDGER APPEND, FULL FORENSICS**:
```
base size immediately before C1: 2421305 bytes, no trailing newline (last byte '.')
GATE3 own byte length: 3680
GATE3 internal newline count: 0
base + 1 + GATE3_length = 2424986
post-C1 file real byte length = 2424986
match: True
tail slice (last 3680 bytes of post-C1 file) vs GATE3: equal True
  (cmp both directions, via scratch copies under .remedy-wt/: exit 0, no output, each direction)
negative control: flipped first byte of a COPY of GATE3 vs the real tail: rejected True
```
All readings PASS — matches the block's own stated expected sizes
(2421305 base, 2424986 post-append) exactly. Note: the character-count
extraction in Python text mode read GATE3 at 3670 (one em-dash "—"
character costs 3 UTF-8 bytes but 1 Python `str` character, and GATE3
contains several); every arithmetic and comparison step above was
redone and reported in raw BYTES (`rb`/`wb` file modes throughout),
which is what reconciles to the block's own byte totals.

**G3 THE TWO PAIRS, READ AND COUNTED, PER CONSTRAINT 2's SHAPES**:
```
PAIR M1 (append-shaped): FROM count before 1, TO contains FROM: True, FROM count after 1 (expected — TO literally contains FROM), TO count after 1
PAIR M2 (rewrite):       FROM count before 1, FROM count after 0, TO count after 1
```
Both PASS, matching Constraint 2's predicted shapes exactly (extracted
and applied via `.remedy-wt/apply_pairs.py`, never hand-retyped).

Full diff of `apps/cli/commands/memory.py`, confirmed nothing beyond
the two named insertions changed:
```diff
--- a/apps/cli/commands/memory.py
+++ b/apps/cli/commands/memory.py
@@ -93,6 +93,7 @@ def _cmd_memory_list(
                 "validity": e.validity, "review_status": e.review_status,
                 "scope": e.scope, "evidence_refs": e.evidence_refs,
                 "created_at": e.created_at,
+                "updated_at": e.updated_at,
             }
             for e in entries
         ]
@@ -105,7 +106,7 @@ def _cmd_memory_list(
         for e in entries:
             approved_mark = " [approved]" if e.approved else ""
             tags_str = f" tags={','.join(e.tags)}" if e.tags else ""
-            print(f"  {e.key}: {e.value}{approved_mark}{tags_str}  (id={str(e.id)[:8]})")
+            print(f"  {e.key}: {e.value}{approved_mark}{tags_str}  (id={str(e.id)[:8]}, created={e.created_at}, updated={e.updated_at})")
```
Confirmed by direct reading: exactly the two named lines changed in
`_cmd_memory_list`. `_cmd_memory_recall` (lines 37-74, the
near-identical function a few lines above with its own
`recall_memory` import and its own byte-identical-before-this-round
json-dict block) was read in full and is byte-for-byte untouched —
still ends its dict at `"created_at": e.created_at,` with no
`updated_at` key, and its print line is unchanged.

```
$ python3 -m py_compile apps/cli/commands/memory.py
(exit 0, no output)
$ python3 -m py_compile tests/test_grouped_cli.py
(exit 0, no output)
```
Both exit 0, reported individually — PASS.

Ruff attempted per constraint 4, exact refusal reproduced:
```
$ ruff check apps/cli/commands/memory.py tests/test_grouped_cli.py
This command requires approval
```
Ruff is denied this session, exactly as the block warned.

**G4 THE TESTS, BEFORE AND AFTER**:
```
Before C2:
$ python3 -m pytest tests/test_grouped_cli.py -q
511 passed in 48.57s

After C2:
$ python3 -m pytest tests/test_grouped_cli.py -q
513 passed in 48.58s
```
Base count 511, fully green; after C2, 513 (base + 2), fully green —
the two new tests plus every pre-existing test in this large shared
file, none of which this round should have touched, moved together
correctly.

**G5 THE STATE READERS AND THE CANARY**:
```
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.72s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.60s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.52s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.29s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.85s
```
515/52/21/16/42 — identical to this session's own prior readings.
Not moved, as expected: this round's change set names no path any of
these five suites should be sensitive to.

**G6 THE PLAN**:
```
$ (PLAN5 extracted from committed authored file, compared byte-for-byte in Python)
cmp equal: True
$ wc -l .agent/plan.md
37 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
cmp equal True (exit-0 equivalent), 37 lines (under 50), both header
counts 1 — PASS.

**G7 THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain   (immediately before C4 staged)
(empty)
$ git ls-files .remedy-wt
(no output)
```
Tree clean before C4, nothing under `.remedy-wt/` tracked.

Per-commit numstat cross-check (the '+' column) against this
handback's own Commits table:
```
$ git show --numstat 831747fd
246  0    .agent/authored/f262-r4.md
$ git show --numstat dfe89e7e
158  215  .agent/last_block.md
$ git show --numstat 2e1f7323
2    1    .agent/live_review.md
$ git show --numstat 66d84b2e
2    1    apps/cli/commands/memory.py
25   0    tests/test_grouped_cli.py
$ git show --numstat a07c6cd2
18   21   .agent/plan.md
```
Every path and every insertion count matches the Commits table exactly
(246, 158, 2, 2+25=27 total for C2, 18). Note: `git commit`'s own
printed post-commit summary differed from these `--numstat` readings
for C0b and C3 (it printed 246/303 for C0b and 38/41 for C3) — that
printed summary applies whole-file "rewrite %" accounting once a
file's dissimilarity crosses its own display threshold, whereas
`--numstat` reports the real line-level diff; this is the same
tooling substitution already declared in round 1's ledger entry
("`git show --numstat` used ... in place of `git commit`'s own
rewrite-detected stat line for whole-file rewrites"), not a new
finding, and this handback's table uses the `--numstat` reading
throughout per the block's own G7 instruction.

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r4.md` — NOT stale. An immutable verbatim
  record of the round's own step block; nothing to go stale.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly, which is the file's whole purpose.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE3's
  content describes round 3's own verified facts and is not asserted
  to describe anything after it.
- `apps/cli/commands/memory.py` — NOT stale. Matches PAIR M1 and
  PAIR M2 exactly; no other line touched; `_cmd_memory_recall`
  confirmed untouched.
- `tests/test_grouped_cli.py` — NOT stale. New methods match the
  TEST SPEC's names, placement and assertions exactly.
- `.agent/plan.md` — NOT stale. Freshly written PLAN5 content
  accurately describes round 4's actual state (T002 batch 2 shipped,
  round 5 = design the tournament.list/external-builder
  per-row text format next).

Constraint 8 check (a sentence OUTSIDE the change set made stale by
this round): `docs/roadmap/features/T2_F262.md` line 5 still reads
`> REGISTRATION ONLY — nothing in this file has been implemented.`
This was already declared false as of round 2 (T001 shipped) and
remains outside the declared change set this round too; T002 batch 2
shipping this round makes the sentence even further from true, but it
is still not repaired, per Constraint 8 and consistent with rounds 2
and 3's own handling of the same sentence.

No documentation elsewhere was found to quote an exact CLI output
line for `memory.list` (`grep` across `docs/` for `memory.list` found
only conceptual references, no literal printed-line quotes), so no
other staleness was introduced by this round's printer change.

## Authored-text proofs

- `.agent/authored/f262-r4.md` written verbatim via `cp` from
  `.remedy-wt/f262-r4-block.txt` (the reviewer's original), confirmed
  byte-identical by `cmp` (exit 0) immediately after the copy — the
  transport proof required before building anything on top of it
  (C0a).
- `.agent/last_block.md` mirrors it via a second `cp`, likewise
  confirmed by matching sha256 (G1).
- GATE3 was extracted from the COMMITTED `.agent/authored/f262-r4.md`
  by a Python script reading the file in BINARY mode, locating the
  `<<<BEGIN GATE3>>>`/`<<<END GATE3>>>` marker pair by byte index, and
  taking the exact bytes strictly between them (marker lines
  excluded) — never by hand-retyping (constraint 1). GATE3: 3680
  bytes, 0 internal newlines, no trailing newline of its own. Applied
  to `.agent/live_review.md` by appending `\n` + GATE3's bytes to the
  base file — reproduced byte-identical (G2).
- PAIR M1 and PAIR M2 were extracted the same way, by their own
  `<<<BEGIN PAIR_M1/M2_FROM/TO>>>` marker pairs, and applied with
  `str.replace(FROM, TO, 1)` via `.remedy-wt/apply_pairs.py` — never by
  hand-retyping (constraint 2). Verified per-pair in G3 above.
- PLAN5 was extracted the same way, by the `<<<BEGIN PLAN5>>>`/
  `<<<END PLAN5>>>` marker pair, 1536 bytes, last byte `.` (no
  trailing newline). `.agent/plan.md` reproduces it byte-identical
  (G6).
- The two new test methods (`test_list_json_has_updated_at_key`,
  `test_list_text_shows_created_and_updated`) were written by hand
  from the TEST SPEC, per constraint 3 — not a byte-transport slice.
  Verified against the spec field-by-field in G4 above.

## Deviations & assumptions

1. **`git commit`'s own printed rewrite-detected stat line disagreed
   with `git show --numstat` for C0b and C3.** For a whole-file
   rewrite that crosses git's own display dissimilarity threshold,
   the plain post-commit summary shows "full old file deleted, full
   new file inserted" counts (C0b: 246/303; C3: 38/41) rather than a
   real line-level diff. `--numstat` (used throughout this handback's
   Commits table, per the block's own G7 instruction) gives the real
   diff counts (C0b: 158/215; C3: 18/21). Both are internally
   consistent (each nets to the same net line-count delta) and this
   substitution is the same one already declared in round 1's own
   GATE1 ledger entry — not a new finding, no committed byte affected.
2. **GATE3's Python `str`-mode character count (3670) differs from its
   real byte length (3680).** The gate text contains several em-dash
   ("—", U+2014) characters, each 1 Python `str` character but 3 UTF-8
   bytes. All G2 arithmetic, extraction, and application in this round
   was done and reported in raw bytes (`rb`/`wb` file modes) to
   reconcile exactly with the block's own stated byte totals
   (2421305 base, 2424986 post-append) — the earlier text-mode
   character count was a scratch miscue, caught and discarded before
   any file was touched, never applied to a committed byte.
3. **Bash tool chaining restriction.** Several attempted compound
   commands (`cmd1; cmd2`, `cmd && echo "..."`) were rejected by this
   session's Bash tool as "multiple operations" requiring separate
   approval. Re-expressed as single, unchained invocations per tool
   call — no change to intent or result, only to invocation shape.
4. **Constraint 8's stale sentence, re-declared not repaired.**
   `docs/roadmap/features/T2_F262.md` line 5 ("REGISTRATION ONLY —
   nothing in this file has been implemented") was already false as of
   round 2 and remains outside this round's declared change set, so it
   is left untouched again — see the Constraint 8 check under the
   staleness sweep above.

No other deviations. `.agent/STOP` was absent both times it was
checked (before C0a and immediately before C4, per constraint 9 of the
block). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r4.md`,
`.agent/last_block.md`, `.agent/live_review.md`,
`apps/cli/commands/memory.py`, `tests/test_grouped_cli.py`,
`.agent/plan.md` and this handback were committed. The bundle's commit
order (C0a, C0b, C1, C2, C3 — this handback C4) was followed exactly,
with C2 as one commit covering both files per constraint 5.

## Next

**NEXT EXPECTED ACTION: Round 5 designs the tournament.list /
external-builder.submission-list per-row text format.** Both commands
print only a COUNT in text mode today — no per-row listing exists at
all — so adding dates there means designing a first per-row text
format before coding it, a bigger slice than a one-line edit, per
PLAN5's Next Steps. After that: `job.list`/`queue.list`/`project.list`
need `--json` added before a date can appear there;
`loop.list`/`patch.list` have no timestamp on their own model and need
a design decision (round 3's handback carries the full 28-command
audit). T003 (sort/filter/limit behavior) starts once date coverage is
far enough along to sort by.
