# Handback — F040 · SESSION 4 · round 16

> Written by the WORKER as the round's final commit, C4. `.agent/STOP` was
> re-read from disk before the first commit of this round and again
> immediately before this commit; it was ABSENT both times. Every number
> below that IS a measurement was taken from `subprocess.run(...).returncode`,
> `hashlib.sha256`, or a plain `open(...).read()` byte comparison inside the
> scripts under `.remedy-wt/g*.py`; not one was read through a pipe or from
> `$?` (the sandbox's Bash tool denies `echo`/`$?`/command-substitution forms
> outright this session — see Deviations item 2).

## Session

SESSION 4 of feature F040 · round 16 · rounds so far 16.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached.

## Range

Review of `c32c02ff..a0d5cab7` (C0a through C3); this commit (C4) rewrites
this file on top of that range.

## Commits

### 2be8bc5e docs(f040): save the round 16 step block verbatim (C0a)
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f040-r16.md` | 317/0 | new — verbatim copy of `.remedy-wt/f040-r16-block.md` via `shutil.copyfile`, `cmp`-confirmed byte-identical |

### c9f2948d docs(f040): mirror the round 16 block to last_block.md (C0b)
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 244/244 | whole-file rewrite — mirrors the round 16 block, replacing round 15's; exempt from the churn cap (AGENTS.md single-`.agent/**`-state-file rewrite exemption, `last_block.md` named explicitly) |

### 4fe5443f docs(f040): update plan.md for round 16, session 4 (C1)
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 16/18 | rewritten byte-for-byte from the PLAN16 slice |

### e4ab5a14 docs(f040): append the R15 verdict to the ledger (C2)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | RECORD16 slice appended (R15 verdict) |

### a0d5cab7 test(f040): add the digest end-to-end vitest chaining T002 seams (C3)
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/digestEndToEnd.test.ts` | 118/0 | new — TESTFILE16 applied byte-for-byte, sha256- and length-confirmed against the marker's own stated values |

### (this commit) docs(f040): write the round 16 handback (C4)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | not orderable here (§3 item 14) | this file |

All five `+`/`-` figures above (317/0, 244/244, 16/18, 2/0, 118/0) are taken
verbatim from `git diff --numstat <commit>^..<commit>`, re-run fresh for this
table per G7's own instruction that this column comes from that gate's
output.

## External actions

- `git worktree add .remedy-wt/wt-r16-g3 HEAD --detach` (at `e4ab5a14`, after
  C2) — for G3's negative control.
- `git worktree remove .remedy-wt/wt-r16-g3` — removed after G3.
- `git worktree add .remedy-wt/wt-r16-g6 HEAD --detach` (at `a0d5cab7`, after
  C3, the fixed path constraint 7 names) — for G6's mutation red proof.
- `git worktree remove .remedy-wt/wt-r16-g6` — removed after G6.
- `git push -u origin feature/f040-completion-digest` runs immediately after
  this commit, per the block's Handback instruction. No PR created, nothing
  merged, no force-push, no other branch touched.

## Verification

**G1 TRANSPORT, at C0b.** All three of `.remedy-wt/f040-r16-block.md`,
`.agent/authored/f040-r16.md` and `.agent/last_block.md` measured equal at
sha256 `f98763c58b3ccf67af83e0c8303310cc98ccfe0175c24c05e79aa0fc73ab3a17`,
20507 bytes. REAL (direct byte comparison via `hashlib.sha256` /
`sha256sum`, no subprocess return code involved — this is a disk-to-disk
digest comparison, not a process). PASS.

**G2 THE PLAN, at C1.** `.agent/plan.md` byte-equal to the PLAN16 slice: True
(direct Python string comparison, 1992 bytes both sides). 41 lines — **under
50**: True. Holds `## Goal`, `## Next Steps` and `F040` (matches
`\bF\d{3}\b`): True, True, True. PASS.

**G3 THE RECORD APPEND, at C2.** Base re-measured directly (not taken from
the block's own claim): `.agent/live_review.md` at `e4ab5a14^` is 1735586
bytes and ends WITH a trailing newline (last byte `\n`). RECORD16 slice is a
single dense paragraph (N=1 under the blank-line split), 3190 characters /
3206 UTF-8 bytes, itself ending with a trailing newline. Committed file:
1738793 bytes.

Reading (a): `base` is a byte prefix of `committed` → True;
`base + b"\n" + slice_bytes == committed` → True (verified byte-for-byte via
`open(...,'rb').read()` slicing, `.remedy-wt/g4`-adjacent script).

Reading (b), per constraint 4's generalized form: split the slice on
blank lines → N = 1. Paragraph 1 (== the whole slice, since N=1) is checked
by asking whether SOME blank-line unit of the committed file ENDS WITH it:
True (the committed file's last blank-line unit ends with the slice).
Because N=1, no paragraphs 2..N exist to check by raw equality. Reading (b)
result: **True**.

Negative control, inside a disposable worktree (`.remedy-wt/wt-r16-g3`,
detached at `e4ab5a14`, removed after): one byte flipped in the middle of
the slice's first (only) paragraph → reading (a) goes **False** (prefix
check still True but reconstruction no longer equals committed), reading
(b) goes **False** (no committed blank-line unit ends with the flipped
text); with the unflipped bytes both readings return **True**. PASS.

**G4 THE LEDGER, at C2.** Computed by DIFFERENCE between `e4ab5a14^` (base)
and `e4ab5a14` (committed) `.agent/live_review.md`, never from the slice:
registered ids (`^- R-\d+ — `) ADDED `[]` REMOVED `[]`; resolved ids
(`^Done: R-\d+`) ADDED `[]` REMOVED `[]`; `DECISION F040 D\d+` ids ADDED `[]`
REMOVED `[]`; `^Gate: F040 R15 — ` lines: 0 before → 1 after. Open count
(registered minus resolved) 262 before → **262 after** (unchanged — this
round registers no new finding and resolves none). Distinct registered
317→317; distinct resolved 55→55. No id's resolved-status changed. PASS.

**G5 THE NEW FILE'S BYTES, at C3.** Committed
`apps/ui/src/api/digestEndToEnd.test.ts`: sha256
`77799c775ed9f10403a6efc248dc96120c4c7ddd1f17e5768733dd94da77b164`, 4788
bytes — both equal to TESTFILE16's own BEGIN-marker values, confirmed
independently via `git show a0d5cab7:apps/ui/src/api/digestEndToEnd.test.ts
| sha256sum` and `wc -c` on the working-tree copy. PASS. (Working note, not a
deviation: my own first extraction script stripped the file's own trailing
newline at the `\n<<<END TESTFILE16` boundary, producing 4787 bytes and a
mismatched hash; caught before committing anything, fixed by re-adding the
trailing newline, re-verified equal, then committed. No wrong bytes ever
reached a commit.)

**G6 THE TEST'S OWN RUN AND ITS RED PROOF, at C3.** First,
`python3 -m pytest tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes -q`
in the primary checkout: **REAL EXIT 0, 1 passed**. Second, THE RED PROOF:
worktree built at `.remedy-wt/wt-r16-g6`, detached at `a0d5cab7` (the commit
C3 creates). UNMUTATED CONTROL, run from the PRIMARY's `apps/ui` directory
against `--root .../wt-r16-g6/apps/ui src/api/`: **REAL EXIT 0, 705 passed,
35 files** — matches the block's own measured baseline exactly. Anchor
`activityMs > dismissedAtMs` asserted unique in the worktree's
`digestVisibility.ts` (count = 1) before mutating to
`activityMs >= dismissedAtMs`. Rerun of the SAME scoped command: **REAL EXIT
1**. Two tests turned red (not one — see Deviations item 1):
`src/api/digestVisibility.test.ts > digestVisibility and a dismissal >
holds a dismissal when the activity is EXACTLY the dismissal instant` (the
pre-existing boundary guard) and `src/api/digestEndToEnd.test.ts > the
completion digest, end to end (T5_F040 T003) > shows the right CTA on
reopen, holds through a dismissal, and re-arms on new activity` (this
round's own new test, failing at its `atTheBoundary` assertion, line 104) —
703 passed, 2 failed, 35 files. File restored from the pre-mutation backup;
`filecmp.cmp` confirmed byte-equal both to the pre-mutation worktree copy
and to `git show a0d5cab7:apps/ui/src/api/digestVisibility.ts`. Rerun of the
scoped command after restore: **REAL EXIT 0, 705 passed, 35 files** — same
as the first control run. `git worktree remove` run; `git worktree list`
returned to one line (the primary checkout only). PASS.

**G7 THE SUITES AND THE TREE, at C3.**
- `python3 -m pytest tests/ui_contracts/ -q` → REAL EXIT 0, 809 passed, 4 skipped.
- `python3 -m pytest tests/cli/test_golden_path.py -q` → REAL EXIT 0, 42 passed.

`git status --porcelain`: `''` (empty). `git ls-files --others
--exclude-standard`: 0 untracked. `git worktree list`: one line, the primary
checkout only. `git diff --numstat` per commit C0a..C3:
- C0a `2be8bc5e` → `317	0	.agent/authored/f040-r16.md`
- C0b `c9f2948d` → `244	244	.agent/last_block.md`
- C1 `4fe5443f` → `16	18	.agent/plan.md`
- C2 `e4ab5a14` → `2	0	.agent/live_review.md`
- C3 `a0d5cab7` → `118	0	apps/ui/src/api/digestEndToEnd.test.ts`

Every insertion figure in the Commits table above is copied from this list.
C4's own count is not orderable here and is not ordered (§3 item 14).

## Authored-text proofs

`.remedy-wt/f040-r16-block.md` → `.agent/authored/f040-r16.md` and
`.agent/last_block.md`: sha256-equal, byte-length-equal (see G1). PLAN16
slice applied byte-for-byte to `.agent/plan.md` (see G2). RECORD16 slice
appended byte-for-byte to `.agent/live_review.md` (see G3). TESTFILE16
applied byte-for-byte to `apps/ui/src/api/digestEndToEnd.test.ts` (see G5) —
per constraint 1 this file is a byte-exact SLICE this round, not a SPEC, and
it was applied and verified as such.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f040-r16.md` | done | G1 verifies |
| C0b mirror the block into `.agent/last_block.md` | done | G1 verifies |
| C1 rewrite `.agent/plan.md` from PLAN16 | done | G2 verifies; byte-equal, 41 lines, under 50 |
| C2 append RECORD16 to `.agent/live_review.md` | done | G3, G4 verify; open count 262→262 |
| C3 add `apps/ui/src/api/digestEndToEnd.test.ts` | done | G5 verifies byte-exact; G6 verifies it runs green and is itself a red-proof discriminator |
| C4 rewrite `.agent/handoff.md` | done | this file |
| G1 transport | PASS | at C0b |
| G2 the plan | PASS | at C1 |
| G3 the record append | PASS | at C2 |
| G4 the ledger | PASS | at C2 |
| G5 the new file's bytes | PASS | at C3 |
| G6 the test's own run and its red proof | PASS | at C3 |
| G7 the suites and the tree | PASS | at C3 |

## Deviations & assumptions

1. **G6's wording anticipates a singular "the failing test's name" under the
   mutation; two tests turned red, not one.** The mutation
   (`activityMs > dismissedAtMs` → `activityMs >= dismissedAtMs`) reddened
   both the pre-existing boundary guard in `digestVisibility.test.ts` AND
   this round's own new `digestEndToEnd.test.ts` (at its `atTheBoundary`
   assertion). I read this as strengthening rather than contradicting the
   gate's intent: the new end-to-end test is shown to be a genuine, live
   discriminator for the exact boundary condition it exercises, not a
   duplicate of coverage that already existed. Both failing node ids are
   reported in Verification/G6 rather than picking one. No production code
   or test file was touched to make this singular; the block's own fixed
   commands and mutation were applied exactly as specified.
2. **This session's Bash tool denies `echo`, bare `$?`, and command
   substitution (`$( )`) outright**, independent of any guard-pattern
   heuristic — plain single-line `grep -c` and multi-statement/multi-line
   compound commands were also denied at various points. Every gate's real
   exit code was instead captured via `subprocess.run(...).returncode`
   inside small scripts under `.remedy-wt/g*.py` and `.remedy-wt/run_g*.py`
   (kept as scratch, gitignored), which the block's own "Done when" preamble
   already names as the required source of a real exit code — so this
   tooling restriction changed HOW the numbers were captured, not WHAT was
   captured or verified. Every gate in Verification above was still executed
   for real, with a real returncode read directly from `subprocess.run`.
3. No commit was reordered, dropped or added relative to the block's fixed
   C0a→C0b→C1→C2→C3→C4 sequence. No file outside the six named paths (the
   five committed this round plus this handback) was touched;
   `packages/**`, `apps/cli/**`, and the four named
   `apps/ui/src/api/*.ts` production modules were read but never written.

## Next

The next round is the dedicated integration-gate round
(docs/agents/integration_gate.md); a regression there is a normal repair
round. After that, the closure sequence (STATUS_closure_protocol.md):
evidence job, a fresh review zip, the STATUS line, the PR. Wiring
`onOpenDecisions`/`onPrimaryAction` for real still needs its own resolution
design (DECISION F040 D5's "in-page action") and is not yet scheduled.
