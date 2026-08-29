# Handback — F040 · SESSION 3 · round 12

> Written by the WORKER as the round's final commit, C6. `.agent/STOP` was
> re-read from disk before the first commit of this round and again
> immediately before this commit; it was ABSENT both times. Every number
> below that IS a measurement was taken from `subprocess.run(...).returncode`,
> `hashlib.sha256`, or a plain `open(...).read()` byte comparison inside
> `.remedy-wt/f040-r12-gates.py`, whose full transcript is at
> `.remedy-wt/r12_gates_out.txt`; not one was read through a pipe or from `$?`.

## Session

SESSION 3 of feature F040 · round 12 · rounds so far 12.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached.

## Range

Review of `d649c330..0b4b3d20` (C0a through C5); this commit (C6) rewrites
this file on top of that range.

## Commits

### 32e86b76 docs(f040): save the round 12 block verbatim (C0a)
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f040-r12.md` | 359/0 | new — verbatim copy of `.remedy-wt/f040-r12-block.md` via `shutil.copyfile` |

### b652ed24 docs(f040): mirror the round 12 block into last_block (C0b)
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 290/303 | whole-file rewrite — mirrors the round 12 block, replacing round 11's |

### a28c176e docs(f040): advance the plan to round 12 (C1)
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 31/16 | rewritten byte-for-byte from the PLAN12 slice |

### edd1a691 docs(f040): append the R11 verdict and resolve R-0756 (C2)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 4/1 | RECORD12 slice appended (R11 verdict + `Done: R-0756`) |

### 3a9d375a feat(f040): extend the digest visibility port with last-seen methods (C3)
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/digestVisibility.ts` | 4/1 | `DigestVisibilityPort` gains `readLastSeen`/`writeLastSeen`; header comment gains one sentence |

### 278031e4 feat(f040): build the browser-local digest storage edge (C4)
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/browserDigestPort.ts` | 102/0 | new — the injectable storage-edge factory `browserDigestVisibilityPort` |

### 0b4b3d20 test(f040): pin the browser digest storage edge with a red-proved guard (C5)
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/browserDigestPort.test.ts` | 87/0 | new — 8 vitest cases, red-proved by G6 |

### (this commit) docs(f040): write the round 12 handback (C6)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | not orderable here (§3 item 14) | this file |

All seven `+` figures above (359, 290, 31, 4, 4, 102, 87) are taken verbatim
from G8's own `git diff --numstat` output, per the block's own instruction
that this table's `+/-` column comes from that gate's output.

## External actions

None yet — `git push -u origin feature/f040-completion-digest` runs
immediately after this commit, per the block's Handback instruction. No PR
created, nothing merged, no force-push, no other branch touched.

## Verification

**G1 TRANSPORT, at C0b.** All three of `.remedy-wt/f040-r12-block.md`,
`.agent/authored/f040-r12.md` and `.agent/last_block.md` measured equal at
sha256 `3f826f153d57113db1178b5f8e369d20819d0f46337e542dd21d011b47fe6882`,
27397 bytes. REAL (direct byte comparison, no subprocess involved). PASS.

**G2 THE PLAN, at C1.** `.agent/plan.md` byte-equal to the PLAN12 slice
(rstripped of the delimiter's own trailing newline): True. 3246 bytes, 58
lines, holds `## Goal`, `## Next Steps` and `F040`. **58 lines is NOT under
50** — see Deviations item 1; the slice was applied byte-for-byte per
constraint 1 and not repaired.

**G3 THE RECORD APPEND, at C2.** Base 1718984 bytes (re-measured from
`git show a28c176e:.agent/live_review.md`), committed 1723955 bytes, slice
4970 bytes. Reading (a): `base + "\n" + slice == committed` → True; base is a
byte prefix of committed → True. Reading (b): N=2 paragraphs counted from the
slice; the committed file's last 2 blank-line units match those 2 paragraphs
in order → True. Negative control, inside a disposable worktree
(`.remedy-wt/wt-r12`, removed after): one byte flipped at offset 1718990
inside the first appended paragraph → both readings REJECT it; restored →
both readings ACCEPT it. `git worktree list` returned to one line after
removal.

**G4 THE LEDGER, at C2**, computed by DIFFERENCE between `a28c176e` and
`edd1a691`, never from the slice: registered ids ADDED `[]` REMOVED `[]`;
resolved ids ADDED `['R-0756']` REMOVED `[]`; `DECISION F040` ids ADDED `[]`
REMOVED `[]`; one `^Gate: F040 R11 — ` line. Open count (registered minus
resolved) 263 before → **262 after**. `R-0756` present in registered both
before and after; absent from resolved before, present after. No other id's
resolved-status changed.

**G5 THE PORT INTERFACE'S SHAPE, at C3.** `DigestVisibilityPort` parses to
exactly four methods, in order: `readDismissal`, `writeDismissal`,
`readLastSeen`, `writeLastSeen`. `readLastSeen(jobId: string): number | null`
and `writeLastSeen(jobId: string, seenAtMs: number): void` both match modulo
whitespace. `digestVisibility()`'s own function body (its full brace span) is
byte-identical before (`3a9d375a^`) and after (`3a9d375a`). Exported types
before and after are identical: `DigestDismissal`, `DigestVisibility`,
`DigestVisibilityInput`, `DigestVisibilityPort`, `DigestVisibilityReason` —
no addition, no removal. `DigestVisibilityInput`, `DigestVisibility` and
`DigestVisibilityReason` are each unchanged (modulo comment-strip/whitespace)
against `3a9d375a^`.

**G6 THE STORAGE EDGE'S SHAPE, ITS GUARD AND ITS RED PROOF, at C5.**
Static scan over `browserDigestPort.ts`, comments stripped, quoted literals
blanked: `window` 0, `localStorage` 0, `Date.now` 0, `fetch` 0,
`XMLHttpRequest` 0 — each paired with a salted positive control that DID see
the token (all 5 controls True). Exported names: `['browserDigestVisibilityPort']`.
Pytest text-guard route: not applicable (no `.py` guard over this `.ts`
pair); colour comes from vitest, reported below. THE RED PROOF, via
`subprocess.run` from a Python driver (never a bare `npx vitest` line, per
constraint 14), worktree `.remedy-wt/wt-r12`, config
`.remedy-wt/r12_vitest.config.mjs` (root at the PRIMARY `apps/ui`, `include`
naming the worktree's mutated file by absolute path, `cacheDir` under
`.remedy-wt/`):
- UNMUTATED CONTROL: REAL EXIT 0, 8/8 passed.
- (a) `readDismissal` reads `LAST_SEEN_SEGMENT` instead of its own (anchor
  occurrences: 1; bytes differ: True; declaration differs after
  comment-strip: True): REAL EXIT 1, 4 died — `a numeric string round-trips
  through the same read path exactly (positive control)`, `a job's own
  dismissal and its own last-seen do not collide`, `a written dismissal
  reads back exactly, for one job`, `two different job ids' dismissals do
  not collide`. Reverted byte-equal: True. Re-confirmed control: REAL EXIT 0,
  8/8.
- (b) `writeDismissal` drops the job id, writing every job under one key
  (anchor occurrences: 1; bytes differ: True; declaration differs: True):
  REAL EXIT 1, 3 died — `a job's own dismissal and its own last-seen do not
  collide`, `a written dismissal reads back exactly, for one job`, `two
  different job ids' dismissals do not collide`. Reverted: True. Re-confirmed
  control: REAL EXIT 0, 8/8.
- (c) the finite-number guard removed, a corrupt string reads as `NaN`
  (anchor occurrences: 1; bytes differ: True; declaration differs: True):
  REAL EXIT 1, 1 died — `reading a key whose stored value does not parse to
  a finite number answers null`. Reverted: True. Re-confirmed control: REAL
  EXIT 0, 8/8.
- (d) `readLastSeen` reads `DISMISSAL_SEGMENT` instead of its own (anchor
  occurrences: 1; bytes differ: True; declaration differs: True): REAL EXIT
  1, 3 died — `a job's own dismissal and its own last-seen do not collide`,
  `two different job ids' last-seen instants do not collide`, `a written
  last-seen reads back exactly, for one job`. Reverted: True. Re-confirmed
  control: REAL EXIT 0, 8/8.

Worktree removed after; `git worktree list` back to one line.

**G7 VITEST AND THE TYPECHECK, at C5.**
`python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs`
→ REAL EXIT 0, 4 passed; `test_vitest_passes` explicitly **PASSED** (verified
with `-v`, not merely inferred from the aggregate).
`python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs`
→ REAL EXIT 0, 1 passed, 73 deselected; `test_typescript_compiles` explicitly
**PASSED**. Neither node reported a SKIP.
Vitest test-file/test count, re-measured at this round's own base `d649c330`
(not trusted from any earlier round's figure): a disposable worktree
`.remedy-wt/wt-r12-base` was built at `d649c330`; because a config with a
relocated `root` breaks resolution of `react/jsx-dev-runtime` for one file
(`promptTraceLens.test.ts`) whose bare-specifier lookup cannot walk out of
`.remedy-wt/` into `apps/ui/node_modules`, the worktree's own
`apps/ui/node_modules` was symlinked (disposable, removed with the worktree)
at the PRIMARY checkout's real one, and `npx vitest run` was run unmodified,
via `subprocess.run`, from that worktree's own `apps/ui` using that
revision's own real `vitest.config.ts` — REAL EXIT 0, **36 files, 718
tests**. Then measured again at HEAD (post C5) in the primary checkout: REAL
EXIT 0, **37 files, 726 tests**. File count rose by exactly 1: True.
`browserDigestPort.test.ts` declares 8 `it(` cases; test count rose by
exactly 8: True.

**G8 THE SUITES, THE TOOLCHAIN AND THE TREE, at C5.**
- `python3 -m pytest tests/ui_contracts/ -q` → REAL EXIT 0, 783 passed, 4 skipped.
- `python3 -m pytest tests/ui_server/ -q` → REAL EXIT 0, 515 passed.
- `python3 -m pytest tests/docs/ -q` → REAL EXIT 0, 295 passed.
- `python3 -m pytest tests/cli/test_golden_path.py -q` → REAL EXIT 0, 42 passed.

`git status --porcelain`: `''` (empty). `git ls-files --others
--exclude-standard`: 0 untracked. `git worktree list`: one line, the primary
checkout only. `git diff --numstat` per commit C0a..C5:
- C0a `32e86b76` → `359	0	.agent/authored/f040-r12.md`
- C0b `b652ed24` → `290	303	.agent/last_block.md`
- C1 `a28c176e` → `31	16	.agent/plan.md`
- C2 `edd1a691` → `4	1	.agent/live_review.md`
- C3 `3a9d375a` → `4	1	apps/ui/src/api/digestVisibility.ts`
- C4 `278031e4` → `102	0	apps/ui/src/api/browserDigestPort.ts`
- C5 `0b4b3d20` → `87	0	apps/ui/src/api/browserDigestPort.test.ts`

Every insertion figure in the Commits table above is copied from this list.
C6's own count is not orderable here and is not ordered (§3 item 14).

## Authored-text proofs

`.remedy-wt/f040-r12-block.md` → `.agent/authored/f040-r12.md` and
`.agent/last_block.md`: `cmp`-equivalent, sha256-equal (see G1). PLAN12 and
RECORD12 slices applied byte-for-byte, verified structurally by G2 and G3.
No other reviewer-authored text was applied this round (`browserDigestPort.ts`
and its test are SPECs, not slices, per constraint 1).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f040-r12.md` | done | G1 verifies |
| C0b mirror the block into `.agent/last_block.md` | done | G1 verifies |
| C1 rewrite `.agent/plan.md` from PLAN12 | done | G2 verifies; **58 lines exceeds the 50-line guideline — see Deviations 1** |
| C2 append RECORD12 to `.agent/live_review.md` | done | G3, G4 verify; open count 263→262 |
| C3 extend `DigestVisibilityPort` with `readLastSeen`/`writeLastSeen` | done | G5 verifies |
| C4 build `browserDigestPort.ts` | done | G6 verifies |
| C5 build `browserDigestPort.test.ts` | done | G6, G7 verify |
| C6 rewrite `.agent/handoff.md` | done | this file |
| G1 transport | PASS | at C0b |
| G2 the plan | PASS (with a noted objection) | at C1 — byte-equal but over the 50-line guideline |
| G3 the record append | PASS | at C2 |
| G4 the ledger | PASS | at C2 |
| G5 the port interface's shape | PASS | at C3 |
| G6 the storage edge's shape, guard and red proof | PASS | at C5 — all four mutations die |
| G7 vitest and the typecheck | PASS | at C5 |
| G8 the suites, the toolchain and the tree | PASS | at C5 |

## Deviations & assumptions

1. **G2's plan is 58 lines, not under 50.** Constraint 1 requires every
   authored slice to be applied byte-for-byte even when it looks wrong, and
   forbids repairing it; PLAN12 is such a slice. The applied `.agent/plan.md`
   is byte-equal to PLAN12 and holds all three required strings, but its own
   line count (58) exceeds AGENTS.md's "keep it short (<50 lines)" guideline
   and G2's own "report... that it is under 50" clause reads False. This is
   declared here rather than silently fixed, per constraint 1's own
   instruction to "DECLARE the objection in the handback."
2. **G7's base-count measurement needed a route not spelled out in the
   block.** The block's own G6-style scratch config (root relocated into the
   worktree, `include` an absolute path) works for a single named file but
   breaks when re-measuring the WHOLE suite's baseline count at `d649c330`:
   one unrelated file, `promptTraceLens.test.ts`, imports a `.tsx` component
   needing `react/jsx-dev-runtime`, and Vite's bare-specifier resolution
   cannot walk from a file under `.remedy-wt/` up into `apps/ui/node_modules`
   once `root` points inside the worktree. The route used instead — leave the
   worktree's own `apps/ui/vitest.config.ts` untouched and symlink
   `apps/ui/node_modules` at the primary's real one before running `npx
   vitest run` unmodified from the worktree's own `apps/ui`, via
   `subprocess.run`, disposed of with the worktree — is not itself ordered by
   the block; it is a plumbing choice made to satisfy G7's own requirement to
   re-measure rather than trust an earlier figure. Both worktrees used this
   round (`wt-r12` for G3/G6, `wt-r12-base` for G7) were removed before this
   commit; `git worktree list` shows one line throughout every gate's
   post-check.
3. No commit was reordered, dropped or added relative to the block's fixed
   C0a→C0b→C1→C2→C3→C4→C5→C6 sequence.

## Next

Mount the card into `RemedyShell.tsx`: `loadJobDigest` (paired with
`jobDigestPath`, following `loadDiffEnvelope`'s shape in `remedyApi.ts`),
`latestActivityMs` read from the brain stream's `recent` ring buffer via
`newestActionRow(...).receivedAtMs`, a real `window`-bound instance of this
round's `browserDigestVisibilityPort`, and the card mounted as a sibling of
the shell div (not inside `<main>`, which `test_main_layout_guard.py` pins to
exactly four children). `onOpenDecisions` and `onPrimaryAction` stay inert
that round too, per PLAN12 step 2.
