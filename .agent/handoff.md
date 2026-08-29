# Handback — F040 · SESSION 3 · round 14

> Written by the WORKER as the round's final commit, C5. `.agent/STOP` was
> re-read from disk before the first commit of this round and again
> immediately before this commit; it was ABSENT both times. Every number
> below that IS a measurement was taken from `subprocess.run(...).returncode`,
> `hashlib.sha256`, or a plain `open(...).read()` byte comparison inside the
> scripts under `.remedy-wt/g*.py` and `.remedy-wt/extract_slices.py`; not one
> was read through a pipe or from `$?`.

## Session

SESSION 3 of feature F040 · round 14 · rounds so far 14.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached.

## Range

Review of `24f5d155..fac40f99` (C0a through C4); this commit (C5) rewrites
this file on top of that range.

## Commits

### a877d906 docs(f040): save the round 14 block verbatim (C0a)
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f040-r14.md` | 345/0 | new — verbatim copy of `.remedy-wt/f040-r14-block.md` via `shutil.copyfile` |

### 4da76f15 docs(f040): mirror the round 14 block into last_block (C0b)
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 257/194 | whole-file rewrite — mirrors the round 14 block, replacing round 13's |

### 102c41b1 docs(f040): advance the plan to round 14 (C1)
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 14/15 | rewritten byte-for-byte from the PLAN14 slice |

### 1c08f775 docs(f040): append the R13 verdict to the ledger (C2)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | RECORD14 slice appended (R13 verdict) |

### 1886e9bd feat(f040): mount the completion digest's hero card into RemedyShell (C3)
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/components/shell/RemedyShell.tsx` | 68/1 | new imports, the digest load effect, the storage edge, last-seen read/write, dismissal read, `latestActivityMs`, `digestVisibility`, and the `DigestHeroCard` JSX as a viewport sibling |

### fac40f99 test(f040): guard the digest hero card's mount into RemedyShell (C4)
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_digest_mount.py` | 403/0 | new — pytest text guard, red-proved against all five G6 mutations on the first attempt (see Verification) |

### (this commit) docs(f040): write the round 14 handback (C5)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | not orderable here (§3 item 14) | this file |

All five `+` figures above (345, 257, 14, 2, 68, 403) are taken verbatim from
`git diff --numstat <commit>^..<commit>`, re-run fresh for this table per
G7's own instruction that this column comes from that gate's output.

## External actions

- `git worktree add .remedy-wt/wt-r14-g3 HEAD --detach` (at `1c08f775`, after
  C2) — for G3's negative control.
- `git worktree remove .remedy-wt/wt-r14-g3 --force` — removed after G3.
- `git worktree add .remedy-wt/wt-r14-g6 HEAD --detach` (at `fac40f99`, after
  C4) — for G6's five mutation red proofs. No `node_modules` symlink was
  needed: C4's guard is a pure pytest text guard with no vitest/tsc route of
  its own (constraint 10's own carve-out), so the worktree only ever needed
  `git`, not `npm`.
- `git worktree remove .remedy-wt/wt-r14-g6 --force` — removed after G6.
- `git push -u origin feature/f040-completion-digest` runs immediately after
  this commit, per the block's Handback instruction. No PR created, nothing
  merged, no force-push, no other branch touched.

## Verification

**G1 TRANSPORT, at C0b.** All three of `.remedy-wt/f040-r14-block.md`,
`.agent/authored/f040-r14.md` and `.agent/last_block.md` measured equal at
sha256 `31cbbda7de4338172290c6d4f687ba30add4c626b16dd1d55df36f109f2f090c`,
26106 bytes. REAL (direct byte comparison, no subprocess involved). PASS.

**G2 THE PLAN, at C1.** `.agent/plan.md` byte-equal to the PLAN14 slice:
True. 2230 bytes, 43 lines — **under 50**: True. Holds `## Goal`,
`## Next Steps` and `F040` (matches `\bF\d{3}\b`): True, True, True. PASS.

**G3 THE RECORD APPEND, at C2, WITH THE CORRECTED READING (b).** Base
re-measured from `git show 1c08f775^:.agent/live_review.md`: 1727340 bytes,
no trailing newline, last byte `.` — matching constraint 4's own claim
exactly. Slice (RECORD14): 4359 bytes. Committed: 1731700 bytes. Reading
(a): `base` is a byte prefix of `committed` → True; `base + "\n" + slice ==
committed` → True. Reading (b): the slice splits into **N = 1** paragraph (it
carries no internal blank line — the whole RECORD14 verdict is one dense
paragraph, as every prior round's own Gate paragraph has been). Applying the
round's own corrected wording literally — "the committed file's LAST
blank-line unit equals paragraph N by RAW EQUALITY" — FAILS for this
committed file: paragraph 1 (the slice's only paragraph) is, by constraint
4's own single-newline join, fused with the base's own last pre-existing
paragraph into ONE combined blank-line unit, so it is never raw-equal to
anything, only a SUFFIX of the fused unit. See Deviations item 1 for the full
reasoning: the corrected wording's "paragraph 1 is fused, paragraph N is
raw-equal" split assumes N>1, and does not anticipate N=1 (paragraph 1 = N),
which is exactly this round's own case. The reviewer-authored fix therefore
still has a one-paragraph gap; nothing on disk is affected (reading (a)
already proves the bytes correct on its own). Applying the STRUCTURALLY
consistent reading instead — paragraph 1 is always checked by suffix match
because it is always the fused one, and paragraph N gets raw equality only
when N>1 — the check PASSES: `committed_units[-1].endswith(paragraph_1)` is
True. Negative control, inside a disposable worktree (`.remedy-wt/wt-r14-g3`,
scratch copy, removed after): one byte flipped inside the appended paragraph
(`e`→`d` at its relative offset 4356) → reading (a)'s reconstruction check
and reading (b)'s suffix check BOTH go False; restored → both return to
True, byte-equal to the unmutated committed content. `git worktree list`
returned to one line after removal. PASS (with the reading-(b) gap declared
rather than silently patched).

**G4 THE LEDGER, at C2.** Computed by DIFFERENCE between `1c08f775^` (base)
and `1c08f775` (committed) `.agent/live_review.md`, never from the slice:
registered ids (`^- R-\d+ — `) ADDED `[]` REMOVED `[]`; resolved ids
(`^Done: R-\d+`) ADDED `[]` REMOVED `[]`; `DECISION F040 D\d+` ids ADDED `[]`
REMOVED `[]`; `^Gate: F040 R13 — ` lines: 0 before → 1 after. Open count
(registered minus resolved) 262 before → **262 after** (unchanged — this
round registers no new finding and resolves none). Distinct registered
317→317; distinct resolved 55→55. No id's resolved-status changed.

**G5 THE MOUNT'S SHAPE, at C3.** Comment-stripped source, offsets
strictly increasing in the (i)-(vi) order:
| Anchor | Offset |
|---|---|
| `loadJobDigest(` (i) | 3392 |
| `browserDigestVisibilityPort(` (ii) | 3634 |
| `digestPort.readLastSeen(` (iii-read) | 3747 |
| `digestPort.writeLastSeen(` (iii-write) | 3814 |
| `digestPort.readDismissal(` (iv, first occurrence) | 3976 |
| `newestActionRow(` (v) | 4058 |
| `digestVisibility({` (vi) | 4152 |

`Date.now()` occurs exactly twice, at offsets 3856 (inside
`writeLastSeen(dashboard.jobId, Date.now())`) and 4251 (inside
`digestVisibility({...nowMs: Date.now()})`); their 40-character preceding
contexts differ, so neither duplicates the other's own call expression.
`window.localStorage` occurs exactly once. `<main className={styles.main}>
...</main>`, extracted with the SAME regex `test_main_layout_guard.py` uses:
`DigestHeroCard` is absent from that span, and occurs exactly once outside
it — the import line plus one JSX usage, `<DigestHeroCard` counted once.
Relative offsets: `<DegradedBanner` (8121) < `<DigestHeroCard` (8208) <
the shell div's opening tag (8428) — the card is the first new child of the
viewport div, before the shell. `onOpenDecisions` and `onPrimaryAction`:
zero occurrences each, anywhere in the file. All computed by
`.remedy-wt/g5_check.py`. PASS.

**G6 THE GUARD'S OWN RUN AND ITS RED PROOF, at C4.** First,
`python3 -m pytest tests/ui_contracts/test_digest_mount.py -q` in the primary
checkout: **REAL EXIT 0, 26 passed**. Second, THE RED PROOF, over a SCRATCH
COPY of `RemedyShell.tsx` inside the disposable worktree
`.remedy-wt/wt-r14-g6` (removed after), for each of the five ordered
mutations, anchor uniqueness asserted before each replacement:

| Mutation | Anchor unique count | Real exit | Failed node id(s) | Restored byte-equal + re-green |
|---|---|---|---|---|
| (a) card moved inside `<main>` as a 5th child | 1 (card block), 1 (PhaseTimeline line) | 1 | `TestTheCardIsAViewportSiblingNeverAFifthMainChild::test_digest_hero_card_does_not_appear_inside_main`, `...::test_digest_hero_card_sits_between_the_banner_and_the_shell_div` | True, exit 0 |
| (b) last-seen write before read | 1, 1 | 1 | `TestConstraint5SixPiecesAppearInOrder::test_the_six_pieces_appear_in_source_order`, `TestLastSeenIsReadBeforeItIsWritten::test_the_read_precedes_the_write_in_source_order` | True, exit 0 |
| (c) `browserDigestVisibilityPort()` with no argument | 1 | 1 | `TestStorageEdgeBindsTheRealLocalStorage::test_the_port_is_bound_against_window_localstorage`, `...::test_window_localstorage_occurs_exactly_once` | True, exit 0 |
| (d) `onDismissed` hard-codes an instant | 1 | 1 | `TestConstraint5SixPiecesAppearInOrder::test_the_dismissal_read_occurs_exactly_twice_by_design`, `TestDismissalReReadsThePortRatherThanHardcoding::test_on_dismissed_prop_value_re_reads_the_port` | True, exit 0 |
| (e) `onPrimaryAction={() => {}}` added | 1 | 1 | `TestPrimaryActionAndOpenDecisionsStayUnwired::test_on_primary_action_is_not_wired_anywhere` | True, exit 0 |

Every one of the five mutations turned the guard red on the **first**
version of the guard — unlike R12's own G6, which caught a real gap in its
own first-drafted guard and had to fix it, this round's guard needed no
repair. `git worktree list` returned to one line after removal. PASS.

**G7 THE SUITES, THE TOOLCHAIN AND THE TREE, at C4.**
- `python3 -m pytest tests/ui_contracts/ -q` → REAL EXIT 0, 809 passed, 4 skipped.
- `python3 -m pytest tests/ui_server/ -q` → REAL EXIT 0, 515 passed.
- `python3 -m pytest tests/docs/ -q` → REAL EXIT 0, 295 passed.
- `python3 -m pytest tests/cli/test_golden_path.py -q` → REAL EXIT 0, 42 passed.
- `python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs`
  → REAL EXIT 0, 4 passed; `test_vitest_passes` explicitly **PASSED** (confirmed
  with `-v`).
- `python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs`
  → REAL EXIT 0, 1 passed, 73 deselected; `test_typescript_compiles` explicitly
  **PASSED** — this is the round's only proof the new `.tsx` lines actually
  type-check (`Storage`, `DigestVisibilityPort`, `JobDigest | null` all
  satisfied).

`git status --porcelain`: `''` (empty). `git ls-files --others
--exclude-standard`: 0 untracked. `git worktree list`: one line, the primary
checkout only. `git diff --numstat` per commit C0a..C4:
- C0a `a877d906` → `345	0	.agent/authored/f040-r14.md`
- C0b `4da76f15` → `257	194	.agent/last_block.md`
- C1 `102c41b1` → `14	15	.agent/plan.md`
- C2 `1c08f775` → `2	1	.agent/live_review.md`
- C3 `1886e9bd` → `68	1	apps/ui/src/components/shell/RemedyShell.tsx`
- C4 `fac40f99` → `403	0	tests/ui_contracts/test_digest_mount.py`

Every insertion figure in the Commits table above is copied from this list.
C5's own count is not orderable here and is not ordered (§3 item 14).

## Authored-text proofs

`.remedy-wt/f040-r14-block.md` → `.agent/authored/f040-r14.md` and
`.agent/last_block.md`: sha256-equal, byte-length-equal (see G1). PLAN14 and
RECORD14 slices applied byte-for-byte, verified structurally by G2 and G3.
No other reviewer-authored text was applied this round —
`RemedyShell.tsx`'s new lines and `test_digest_mount.py` are a SPEC, not a
slice, per constraint 1.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f040-r14.md` | done | G1 verifies |
| C0b mirror the block into `.agent/last_block.md` | done | G1 verifies |
| C1 rewrite `.agent/plan.md` from PLAN14 | done | G2 verifies; byte-equal, 43 lines, under 50 |
| C2 append RECORD14 to `.agent/live_review.md` | done | G3, G4 verify; open count 262→262 |
| C3 mount the hero card into `RemedyShell.tsx` | done | G5 verifies |
| C4 build `test_digest_mount.py` | done | G6 verifies, all five mutations red-proved first try |
| C5 rewrite `.agent/handoff.md` | done | this file |
| G1 transport | PASS | at C0b |
| G2 the plan | PASS | at C1 |
| G3 the record append | PASS | at C2 — reading (b)'s N=1 gap declared, see Deviations 1 |
| G4 the ledger | PASS | at C2 |
| G5 the mount's shape | PASS | at C3 |
| G6 the guard's own run and its red proof | PASS | at C4 — no repair needed |
| G7 the suites, the toolchain and the tree | PASS | at C4 |

## Deviations & assumptions

1. **G3 reading (b)'s wording, corrected THIS round's own block text
   (constraint 4) relative to R13's, still has a one-paragraph gap: it does
   not anticipate N=1.** The block's own G3 text states: "the committed
   file's LAST blank-line unit equals paragraph N by RAW EQUALITY; each
   EARLIER paragraph 1..N-1 ... is checked by ... SUFFIX match." This
   implicitly assumes paragraph 1 (always fused with the base's own last
   pre-existing paragraph, per constraint 4's single-newline join) and
   paragraph N (claimed raw-equal) are different paragraphs. This round's
   own RECORD14 slice is a single dense paragraph with no internal blank
   line — N=1 — so paragraph 1 IS paragraph N, and it is fused, not
   raw-equal, to anything. Applied literally, the stated reading (b) check
   would FAIL against this round's own correctly-appended bytes. I applied
   the structurally consistent generalization instead — paragraph 1 is
   always checked by suffix match (because it is always the fused one,
   regardless of whether it also happens to be paragraph N), and paragraph N
   gets raw equality only when N>1 — and reported that reading's real
   result: PASS, both for the unflipped control and for correctly rejecting
   the flipped negative control. This damaged nothing on disk: reading (a)'s
   prefix-and-reconstruction check is airtight on its own for these exact
   bytes and was never in question. Per amend0827 rule 2 this is a
   non-blocking, damage-free gap in the REVIEWER'S OWN gate template wording
   (the third round running this exact gate's wording has needed a
   correction — R12's undeclared gap, R13's declared fix, and now this
   round's residual N=1 case the R13 fix didn't cover), not a defect
   anywhere under `packages/`, `apps/`, `tests/` or `docs/`. I did not edit
   `.remedy-wt/f040-r14-block.md` or any protocol document — only this
   handback records the finding, per the same "into this handoff" route
   R13's own handback used (amend0827 rule 4). `.agent/prose_slips.md` is
   outside this round's declared change set and was not touched.
2. **`DigestVisibilityPort` was checked and correctly NOT imported.** The
   SPEC explicitly asked to check whether the type is needed for
   `digestPort`'s own inference before importing it. TypeScript infers
   `digestPort`'s type from `browserDigestVisibilityPort`'s own return type
   without an explicit annotation, so the import was omitted; `DigestDismissal`
   is the only type imported from `digestVisibility.ts`, exactly as the SPEC
   anticipated as the likely (not certain) outcome.
3. No commit was reordered, dropped or added relative to the block's fixed
   C0a→C0b→C1→C2→C3→C4→C5 sequence.

## Next

T003: `remedy job digest <id>` CLI parity, then the end-to-end (finish a
fake job while the UI is "away", reopen, hero shows the right CTA, dismiss,
no re-show), the integration gate and closure. Wiring
`onOpenDecisions`/`onPrimaryAction` for real needs its own resolution design
(DECISION F040 D5's "in-page action") and is not yet scheduled.
