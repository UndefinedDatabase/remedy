# Handoff — F262 List commands v2 (dates, sort, filter), round 3 (T002 batch 1 ships)

## Session

SESSION 1 of feature F262 · round 3 · rounds so far 3.

Round 3 ships T002 batch 1: printed CREATED (and, where the model has
it, RESOLVED/UPDATED) dates on four list commands whose store already
records the timestamps and whose `--json` output already surfaces
them — only the TEXT rendering was missing them. No model or store
change, no `--json` change, no behavior change beyond the printed
line: `blocker.list`, `decision.list`, `approval.policy-list`,
`self-repair.proposal-list`. Two of the four (`blocker.list`,
`decision.list`) had no dedicated CLI test file before this round;
both now do.

## Range

Review of `c324929e8f0b97b34de30c6e4eb42bbca3357b61..41922f01aa656c4fd968a412cb9731de608c83a9`.
That is C0a through C3 (five content commits before this handback —
C0a, C0b, C1, C2, C3). This handback (C4) follows and is not part of
the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched, branch matched, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r3.md` saved verbatim, cmp exit 0 |
| C0b | done | mirrored to `.agent/last_block.md`, sha256 identical |
| C1 | done | GATE2 appended to `.agent/live_review.md` byte-exact |
| C2 | done | four printer PAIRs applied + two new test files, one commit |
| C3 | done | PLAN4 applied to `.agent/plan.md`, whole-file replace |
| C4 (this handback) | done | |
| G1 TRANSPORT | done | PASS — one digest, twice |
| G2 THE LEDGER APPEND | done | PASS — arithmetic matched, tail equal, negative control rejected |
| G3 THE FOUR PAIRS | done | PASS — all four FROM 1→0, TO 0→1, containment False, py_compile exit 0 ×6 |
| G4 THE TESTS, BEFORE AND AFTER | done | PASS — 68/12 unchanged before+after C2, new files 2/2 passed |
| G5 STATE READERS + CANARY | done | PASS — 515/52/21/16/42, unmoved from session baseline |
| G6 THE PLAN | done | PASS — cmp exit 0, 40 lines, both header counts 1 |
| G7 THE TREE, COMMITS, SWEEP | done | PASS — tree clean, `.remedy-wt` untracked, numstats match, staleness declared |

## Commits

### a262f041 F262 R3 C0a: save step block verbatim to .agent/authored/f262-r3.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r3.md` | +303/-0 | transport proof — verbatim `cp` of the reviewer's step block (`.remedy-wt/f262-r3-block.txt`), new file |

### be92b657 F262 R3 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +227/-225 | mirror of the round's authored block via `cp` (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### f5774a49 F262 R3 C1: append GATE2 to live_review.md, books round 2 PASS verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | byte-exact append of GATE2 (extracted from committed authored file by marker index), `\n` + GATE2's own bytes appended to the base file |

### e9589f54 F262 R3 C2: T002 batch 1 - print created/resolved dates on four list commands, with coverage
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/blocker.py` | +2/-1 | PAIR B — `_cmd_blocker_list` text row now prints `created=` and, when set, `resolved=` |
| `apps/cli/commands/decision.py` | +2/-1 | PAIR D — `_cmd_decision_list` text row now prints `created=` and, when set, `resolved=` |
| `apps/cli/commands/self_repair_cmd.py` | +2/-1 | PAIR S — `_cmd_proposal_list` text row now prints `created=`/`updated=` |
| `apps/cli/commands/worker_facade_cmd.py` | +2/-1 | PAIR P — `_cmd_approval_policy_list` text row now prints `created=`/`updated=` |
| `tests/cli/test_blocker_cmd.py` | +49/-0 | new — `TestBlockerListText`, 2 tests, follows `TestApprovalPolicyList`'s patching idiom |
| `tests/cli/test_decision_cmd.py` | +53/-0 | new — `TestDecisionListText`, 2 tests, same idiom, patches both `_load_job_events` and `list_decisions` |

### 41922f01 F262 R3 C3: replace plan.md with PLAN4 - round 4 continues T002 batch 2
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +21/-17 | whole-file replace with PLAN4 extracted from the committed authored file (per constraint 6) |

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
c324929e8f0b97b34de30c6e4eb42bbca3357b61
$ git branch --show-current
feature/f262-list-commands-v2
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
```
All four confirmed.

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f262-r3.md .agent/last_block.md
c8d93da08b41c7fe134ba3320f52f890d21a9998b300ffa8f19229c20313992b  .agent/authored/f262-r3.md
c8d93da08b41c7fe134ba3320f52f890d21a9998b300ffa8f19229c20313992b  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE LEDGER APPEND, FULL FORENSICS**:
```
base size immediately before C1: 2417095 bytes, trailing byte b'.' (no trailing newline)
GATE2 own byte length: 4209
GATE2 internal newline count: 0
base + 1 + GATE2_length = 2421305
post-C1 file real byte length = 2421305
match: True
tail slice (last 4209 bytes of post-C1 file) vs GATE2: equal True
  (cmp both directions, via scratch copies under .remedy-wt/: exit 0, no output, each direction)
negative control: flipped first byte of a COPY of GATE2 vs the real tail: rejected True
```
All readings PASS — matches the block's own stated expected sizes
(2417095 base, 2421305 post-append) exactly.

**G3 THE FOUR PAIRS, READ AND COUNTED**:
```
PAIR B (blocker.py):            FROM before 1, FROM after 0, TO after 1, FROM in TO: False
PAIR D (decision.py):           FROM before 1, FROM after 0, TO after 1, FROM in TO: False
PAIR P (worker_facade_cmd.py):  FROM before 1, FROM after 0, TO after 1, FROM in TO: False
PAIR S (self_repair_cmd.py):    FROM before 1, FROM after 0, TO after 1, FROM in TO: False
```
All four PASS — REWRITE confirmed, not APPEND, for all four (extracted
and applied via `.remedy-wt/apply_pairs.py`, never hand-retyped).

Full diff of all four production files, confirmed nothing beyond the
named pair changed in each:
```diff
--- a/apps/cli/commands/blocker.py
+++ b/apps/cli/commands/blocker.py
@@ -35,7 +35,8 @@ def _cmd_blocker_list(
             return
         for s in stops:
             status_mark = "[resolved]" if s.status == "resolved" else "[active]"
-            print(f"  {s.reason_code} {status_mark}  {s.safe_summary}  (id={s.id[:8]})")
+            resolved_str = f", resolved={s.resolved_at}" if s.resolved_at else ""
+            print(f"  {s.reason_code} {status_mark}  {s.safe_summary}  (id={s.id[:8]}, created={s.created_at}{resolved_str})")

--- a/apps/cli/commands/decision.py
+++ b/apps/cli/commands/decision.py
@@ -54,7 +54,8 @@ def _cmd_decision_list(job_id_str: str, *, json_output: bool = False) -> None:
             return
         for d in decisions:
             status_mark = "[open]" if d.status == "open" else "[resolved]"
-            print(f"  {d.type} {status_mark} ({d.severity}): {d.safe_summary}  (id={d.id})")
+            resolved_str = f", resolved={d.resolved_at}" if d.resolved_at else ""
+            print(f"  {d.type} {status_mark} ({d.severity}): {d.safe_summary}  (id={d.id}, created={d.created_at}{resolved_str})")

--- a/apps/cli/commands/self_repair_cmd.py
+++ b/apps/cli/commands/self_repair_cmd.py
@@ -90,7 +90,8 @@ def _cmd_proposal_list(args: argparse.Namespace) -> None:
         return

     for p in proposals:
-        print(f"  {p.get('proposal_id', '?'):20s}  {p.get('status', '?'):25s}  {p.get('title', '')[:50]}")
+        print(f"  {p.get('proposal_id', '?'):20s}  {p.get('status', '?'):25s}  {p.get('title', '')[:50]}"
+              f"  (created={p.get('created_at', '')}, updated={p.get('updated_at', '')})")

--- a/apps/cli/commands/worker_facade_cmd.py
+++ b/apps/cli/commands/worker_facade_cmd.py
@@ -662,7 +662,8 @@ def _cmd_approval_policy_list(ns: argparse.Namespace) -> None:
     print(f"Approval policies: {len(policies)}")
     for p in policies:
         status = "ENABLED" if p.get("enabled") else "disabled"
-        print(f"  [{status}] {p.get('policy_id', '?')}: {p.get('label', '')}")
+        print(f"  [{status}] {p.get('policy_id', '?')}: {p.get('label', '')}"
+              f"  (created={p.get('created_at', '')}, updated={p.get('updated_at', '')})")
```
Confirmed by direct reading: exactly one line replaced by two in each
file, nothing else touched.

```
$ python3 -m py_compile apps/cli/commands/blocker.py
(exit 0, no output)
$ python3 -m py_compile apps/cli/commands/decision.py
(exit 0, no output)
$ python3 -m py_compile apps/cli/commands/worker_facade_cmd.py
(exit 0, no output)
$ python3 -m py_compile apps/cli/commands/self_repair_cmd.py
(exit 0, no output)
$ python3 -m py_compile tests/cli/test_blocker_cmd.py
(exit 0, no output)
$ python3 -m py_compile tests/cli/test_decision_cmd.py
(exit 0, no output)
```
All six exit 0, reported individually — PASS.

Ruff attempted per constraint 4, exact refusal reproduced:
```
$ ruff check apps/cli/commands/blocker.py apps/cli/commands/decision.py apps/cli/commands/worker_facade_cmd.py apps/cli/commands/self_repair_cmd.py tests/cli/test_blocker_cmd.py tests/cli/test_decision_cmd.py
This command requires approval
```
Ruff is denied this session, exactly as the block warned.

**G4 THE TESTS, BEFORE AND AFTER**:
```
Before C2:
$ python3 -m pytest tests/cli/test_worker_facade_cmd.py -q
....................................................................     [100%]
68 passed in 0.32s
$ python3 -m pytest tests/cli/test_self_repair_cmd.py -q
............                                                             [100%]
12 passed in 2.43s

After C2:
$ python3 -m pytest tests/cli/test_worker_facade_cmd.py -q
....................................................................     [100%]
68 passed in 0.32s
$ python3 -m pytest tests/cli/test_self_repair_cmd.py -q
............                                                             [100%]
12 passed in 2.41s

New files, only after C2:
$ python3 -m pytest tests/cli/test_blocker_cmd.py -q
..                                                                        [100%]
2 passed in 0.19s
$ python3 -m pytest tests/cli/test_decision_cmd.py -q
..                                                                        [100%]
2 passed in 0.20s
```
Both pre-existing suites fully green, unchanged before and after
(68 and 12 both times) — additive printer change broke nothing. Both
new files show `2 passed` — PASS on all four readings.

**G5 THE STATE READERS AND THE CANARY**:
```
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.61s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.62s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.53s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.29s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 21.22s
```
515/52/21/16/42 — identical to this session's own prior readings.
Not moved, as expected: this round's change set names no path any of
these five suites should be sensitive to.

**G6 THE PLAN**:
```
$ (PLAN4 extracted from committed authored file, compared byte-for-byte in Python)
cmp equal: True
$ wc -l .agent/plan.md
40 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
cmp equal True (exit-0 equivalent), 40 lines (under 50), both header
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
$ git show --numstat a262f041
303  0    .agent/authored/f262-r3.md
$ git show --numstat be92b657
227  225  .agent/last_block.md
$ git show --numstat f5774a49
2    1    .agent/live_review.md
$ git show --numstat e9589f54
2    1    apps/cli/commands/blocker.py
2    1    apps/cli/commands/decision.py
2    1    apps/cli/commands/self_repair_cmd.py
2    1    apps/cli/commands/worker_facade_cmd.py
49   0    tests/cli/test_blocker_cmd.py
53   0    tests/cli/test_decision_cmd.py
$ git show --numstat 41922f01
21   17   .agent/plan.md
```
Every path and every insertion count matches the Commits table exactly
(303, 227, 2, 2+2+2+2+49+53=110 total for C2, 21).

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r3.md` — NOT stale. An immutable verbatim
  record of the round's own step block; nothing to go stale.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's
  block exactly, which is the file's whole purpose.
- `.agent/live_review.md` — NOT stale. Append-only ledger; GATE2's
  content describes round 2's own verified facts and is not asserted
  to describe anything after it.
- `apps/cli/commands/blocker.py` — NOT stale. Matches PAIR B exactly;
  no other line touched.
- `apps/cli/commands/decision.py` — NOT stale. Matches PAIR D exactly;
  no other line touched.
- `apps/cli/commands/worker_facade_cmd.py` — NOT stale. Matches PAIR P
  exactly; no other line touched.
- `apps/cli/commands/self_repair_cmd.py` — NOT stale. Matches PAIR S
  exactly; no other line touched.
- `tests/cli/test_blocker_cmd.py` — NOT stale. New file, matches the
  TEST SPEC's field names, patch target and both test cases.
- `tests/cli/test_decision_cmd.py` — NOT stale. New file, matches the
  TEST SPEC's field names, both patch targets and both test cases.
- `.agent/plan.md` — NOT stale. Freshly written PLAN4 content
  accurately describes round 3's actual state (T002 batch 1 shipped,
  round 4 = T002 batch 2 next).

Constraint 8 check (a sentence OUTSIDE the change set made stale by
this round): `docs/roadmap/features/T2_F262.md` line 5 still reads
`> REGISTRATION ONLY — nothing in this file has been implemented.`
This was already declared false as of round 2 (T001 shipped) and
remains outside the declared change set this round too; T002 batch 1
shipping this round makes the sentence even further from true, but it
is still not repaired, per Constraint 8 and consistent with round 2's
own handling of the same sentence.

No documentation elsewhere was found to quote an exact CLI output
line for any of the four touched commands (`grep` across `docs/` for
the four command ids found only conceptual references, no literal
printed-line quotes), so no other staleness was introduced by this
round's printer changes.

## Authored-text proofs

- `.agent/authored/f262-r3.md` written verbatim via `cp` from
  `.remedy-wt/f262-r3-block.txt` (the reviewer's original), confirmed
  byte-identical by `cmp` (exit 0) immediately after the copy — the
  transport proof required before building anything on top of it
  (C0a).
- `.agent/last_block.md` mirrors it via a second `cp`, likewise
  confirmed by matching sha256 (G1).
- GATE2 was extracted from the COMMITTED `.agent/authored/f262-r3.md`
  by a Python script reading the file in text mode, locating the
  `<<<BEGIN GATE2>>>`/`<<<END GATE2>>>` marker pair by string index,
  and taking the exact text strictly between them (marker lines
  excluded), stripping exactly the one trailing `\n` belonging to the
  marker line — never by hand-retyping (constraint 1). GATE2: 4209
  bytes, 0 internal newlines, no trailing newline of its own. Applied
  to `.agent/live_review.md` by appending `\n` + GATE2's bytes to the
  base file — reproduced byte-identical (G2).
- The four CODE PAIRS were extracted the same way, by their own
  `<<<BEGIN PAIR_*_FROM/TO>>>` marker pairs, and applied with
  `str.replace(FROM, TO, 1)` via `.remedy-wt/apply_pairs.py` — never by
  hand-retyping (constraint 2). Verified per-pair in G3 above.
- PLAN4 was extracted the same way, by the `<<<BEGIN PLAN4>>>`/
  `<<<END PLAN4>>>` marker pair, 1727 bytes, last byte `.` (no
  trailing newline). `.agent/plan.md` reproduces it byte-identical
  (G6).
- The two new test files (`tests/cli/test_blocker_cmd.py`,
  `tests/cli/test_decision_cmd.py`) were written by hand from the
  TEST SPEC, per constraint 3 — not a byte-transport slice. Verified
  against the spec field-by-field and test-by-test in G4 above.

## Deviations & assumptions

1. **`/tmp` denied; scratch redirected to `.remedy-wt/`.** The G2
   forensic scratch files (the extracted GATE2 copy and the tail
   slice used for the `cmp` double-check) could not be written to or
   read from `/tmp` — the sandbox blocked both `cp` and `cmp` against
   `/tmp` paths outright ("may only compare/copy files from the
   allowed working directories … `/home/decodeux/Repos/remedy`").
   Redone with the same Python extraction writing directly into
   `.remedy-wt/` (gitignored scratch, per this session's own
   Self-Drive Scratch Location convention), then `cmp`'d there; both
   scratch files were deleted immediately after use and `git ls-files
   .remedy-wt` confirms nothing under that directory was ever tracked.
   Same bytes, same comparisons, only the filesystem location of the
   throwaway copies changed.
2. **Bash tool chaining restriction.** Several attempted compound
   commands (`cmd1; cmd2`, `cmd && echo "..."`) were rejected by this
   session's Bash tool as "multiple operations" requiring separate
   approval. Re-expressed as single, unchained invocations per tool
   call — no change to intent or result, only to invocation shape.
   One consequence: several `py_compile` and `cmp` calls that the
   block's own prose implies could be one line are reported above as
   separate individual invocations instead; each was still run for
   real and its real (silent, exit-0) result recorded.
3. **`wc -l` undercounts a no-trailing-newline file by one line.**
   `.agent/plan.md` ends without a trailing newline (per constraint 6),
   so `wc -l`, which counts newline characters, reports 40 for a file
   whose content is 41 lines wide by any line-splitting count. Reported
   the raw `wc -l` reading (40) as the block's G6 literally asks for,
   which is still comfortably under the 50-line cap either way; not
   silently corrected to the alternate count.
4. **Constraint 8's stale sentence, re-declared not repaired.**
   `docs/roadmap/features/T2_F262.md` line 5 ("REGISTRATION ONLY —
   nothing in this file has been implemented") was already false as of
   round 2 and remains outside this round's declared change set, so it
   is left untouched again — see the Constraint 8 check under the
   staleness sweep above.

No other deviations. `.agent/STOP` was absent both times it was
checked (before C0a and immediately before C4, per constraint 9 of the
block). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r3.md`,
`.agent/last_block.md`, `.agent/live_review.md`,
`apps/cli/commands/blocker.py`, `apps/cli/commands/decision.py`,
`apps/cli/commands/worker_facade_cmd.py`,
`apps/cli/commands/self_repair_cmd.py`, `tests/cli/test_blocker_cmd.py`,
`tests/cli/test_decision_cmd.py`, `.agent/plan.md` and this handback
were committed. The bundle's commit order (C0a, C0b, C1, C2, C3 — this
handback C4) was followed exactly, with C2 as one commit covering all
six files per constraint 5.

## Next

**NEXT EXPECTED ACTION: Round 4 builds T002 batch 2.** Per PLAN4's Next
Steps: `memory.list` (add `updated_at` to its json dict, then text);
`tournament.list` and `external-builder.submission-list` (both DROP
their timestamp from the json shape today — restore it, then add
text). Round 5 continues with T002 batch 3
(`job.list`/`queue.list`/`project.list` need `--json` added before a
date can appear there; `loop.list`/`patch.list` have no timestamp on
their own model and need a design decision), and round 6+ covers the
remaining no-timestamp-concept commands per the plan's Risks section.
