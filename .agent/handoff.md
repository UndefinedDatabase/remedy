# Handback — F040 · SESSION 3 · round 13

> Written by the WORKER as the round's final commit, C5. `.agent/STOP` was
> re-read from disk before the first commit of this round and again
> immediately before this commit; it was ABSENT both times. Every number
> below that IS a measurement was taken from `subprocess.run(...).returncode`,
> `hashlib.sha256`, or a plain `open(...).read()` byte comparison inside the
> scripts under `.remedy-wt/f040-r13-*.py`; not one was read through a pipe
> or from `$?`.

## Session

SESSION 3 of feature F040 · round 13 · rounds so far 13.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached.

## Range

Review of `9da5d097..5d62f26b` (C0a through C4); this commit (C5) rewrites
this file on top of that range.

## Commits

### 726090a4 docs(f040): save the round 13 block verbatim (C0a)
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f040-r13.md` | 282/0 | new — verbatim copy of `.remedy-wt/f040-r13-block.md` via `shutil.copyfile` |

### 402a61f8 docs(f040): mirror the round 13 block into last_block (C0b)
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 200/277 | whole-file rewrite — mirrors the round 13 block, replacing round 12's |

### 12fa1e26 docs(f040): advance the plan to round 13 (C1)
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 14/28 | rewritten byte-for-byte from the PLAN13 slice — see Deviations item 1 for the 44/58 figure `git commit`'s own console line printed at commit time |

### 131c3096 docs(f040): append the R12 verdict to the ledger (C2)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | RECORD13 slice appended (R12 verdict) |

### 438172bb feat(f040): build the job digest fetch loader loadJobDigest (C3)
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/remedyApi.ts` | 45/0 | new section — `JobDigestFetcher`, `loadJobDigest`, paired with `jobDigestPath`/`decodeJobDigest`, following `loadDiffEnvelope`'s shape |

### 5d62f26b test(f040): cover the job digest fetch loader's decode and degrade paths (C4)
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/remedyApi.test.ts` | 48/1 | append — new `describe("the job digest door", ...)` block, 3 `it` cases, red-proved by G5 |

### (this commit) docs(f040): write the round 13 handback (C5)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | not orderable here (§3 item 14) | this file |

All six `+` figures above (282, 200, 14, 2, 45, 48) are taken verbatim from
`git diff --numstat <commit>^..<commit>`, re-run fresh for this table per
G7's own instruction that this column comes from that gate's output.

## External actions

- `git worktree add .remedy-wt/wt-r13 HEAD` (at `12fa1e26`, before C2) — for
  G3's negative control.
- `git worktree remove .remedy-wt/wt-r13 --force` — removed after G3.
- `git worktree add .remedy-wt/wt-r13-base 9da5d097` — for G6's base test
  count, `apps/ui/node_modules` symlinked from the primary checkout.
- `git worktree remove .remedy-wt/wt-r13-base --force` — removed after G6's
  base measurement.
- `git worktree add .remedy-wt/wt-r13 HEAD` (at `5d62f26b`, after C4) — for
  G5's mutation red proof, `apps/ui/node_modules` symlinked from the primary
  checkout the same way.
- `git worktree remove .remedy-wt/wt-r13 --force` — removed after G5.
- `git push -u origin feature/f040-completion-digest` runs immediately after
  this commit, per the block's Handback instruction. No PR created, nothing
  merged, no force-push, no other branch touched.

## Verification

**G1 TRANSPORT, at C0b.** All three of `.remedy-wt/f040-r13-block.md`,
`.agent/authored/f040-r13.md` and `.agent/last_block.md` measured equal at
sha256 `27cc654e61b299093106177bad44f8bcc1423294ffaba0be1448a79140c8f4e7`,
20074 bytes. REAL (direct byte comparison, no subprocess involved). PASS.

**G2 THE PLAN, at C1.** `.agent/plan.md` byte-equal to the PLAN13 slice
(with the delimiter's own trailing newline stripped, per the same convention
R12's own committed plan used): True. 2214 bytes, 44 lines — **under 50**:
True. Holds `## Goal`, `## Next Steps` and `F040` (matches `\bF\d{3}\b`):
True, True, True. PASS, with no objection needed this round.

**G3 THE RECORD APPEND, at C2.** Base re-measured from `git show
12fa1e26:.agent/live_review.md`: 1723955 bytes, confirming constraint 4's own
claim exactly. Slice (RECORD13, delimiter's own trailing newline stripped):
3384 bytes. Committed: 1727340 bytes. Reading (a): `base + "\n" + slice ==
committed` → True; base is a byte prefix of committed → True. Reading (b):
N=1 paragraph counted from the slice (it has no internal blank line); the
committed file's LAST blank-line unit does not equal the paragraph by raw
identity — it CONTAINS it as an exact trailing suffix, because constraint 4's
own single-newline join fuses the base's last existing paragraph with the
newly appended one rather than separating them by a blank line (verified:
`units[-1].endswith(paragraph)` is True). See Deviations item 3 for the full
reasoning and for a re-derivation showing R12's own G3 reading (b) had the
identical structural shape, undeclared at the time. Negative control, inside
a disposable worktree (`.remedy-wt/wt-r13`, scratch copy, removed after): one
byte flipped inside the appended paragraph → reading (a)'s reconstruction
check and reading (b)'s suffix check BOTH go False; restored → both return to
True, byte-equal to the unmutated committed content. `git worktree list`
returned to one line after removal. PASS (with the reading-(b) semantics
declared rather than assumed).

**G4 THE LEDGER, at C2.** Computed by DIFFERENCE between `12fa1e26` (base)
and `131c3096` (committed) `.agent/live_review.md`, never from the slice:
registered ids (`^- R-\d+ — `) ADDED `[]` REMOVED `[]`; resolved ids
(`^Done: R-\d+`) ADDED `[]` REMOVED `[]`; `DECISION F040 D\d+` ids ADDED `[]`
REMOVED `[]`; `^Gate: F040 R12 — ` lines: 0 before → 1 after. Open count
(registered minus resolved) 262 before → **262 after** (unchanged — this
round registers no new finding and resolves none). Distinct registered
317→317; distinct resolved 55→55. No id's resolved-status changed.

**G5 THE LOADER'S SHAPE, ITS GUARD AND ITS RED PROOF, at C4.**
Static scan over `remedyApi.ts`, comments stripped and quoted literals
blanked, `loadJobDigest`'s own brace span only: `Date.now` 0, `localStorage`
0. Exported names present: `loadJobDigest` True, `JobDigestFetcher` True.
Default second parameter is the file's own `fetchJson`: True. No `.py`
text-guard exists over this `.ts` pair (as the block states); colour comes
from vitest, reported under G6. THE RED PROOF, via a Python driver's
`subprocess.run` (never a bare `npx vitest` shell line, per constraint 12),
worktree `.remedy-wt/wt-r13` (built fresh at `5d62f26b`, after C4;
`apps/ui/node_modules` symlinked from the primary checkout — the F256 D6
route, declared per constraint's "either plumbing is acceptable" clause),
targeting `src/api/remedyApi.test.ts` alone:
- UNMUTATED CONTROL: REAL EXIT 0, 67/67 passed.
- (a) the `catch` block returns `undefined` instead of `null` (anchor
  `  } catch {\n    return null;\n  }\n}` — occurrences: 1; bytes differ:
  True; declaration differs after comment-strip: True): REAL EXIT 1, 1
  died — `the job digest door > degrades a rejected fetch to null rather
  than throwing`. Reverted, byte-equal to the original: True. Re-confirmed
  control: REAL EXIT 0, 67/67.
- (b) the fetcher is called with a literal path rather than
  `jobDigestPath(request)`'s result (anchor
  `const payload = await fetchPayload(jobDigestPath(request));` —
  occurrences: 1; bytes differ: True; declaration differs: True): REAL EXIT
  1, 1 died — `the job digest door > returns the decoded digest and reads
  its own path exactly once`. Reverted, byte-equal: True. Re-confirmed
  control: REAL EXIT 0, 67/67.

Worktree removed after; `git worktree list` back to one line; final
byte-equality of the worktree's mutated-then-restored file to the committed
primary file confirmed True.

**G6 VITEST, at C4.**
`python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs`
→ REAL EXIT 0, 4 passed; `test_vitest_passes` explicitly **PASSED** (verified
with `-v`, not merely inferred from the aggregate).
`python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs`
→ REAL EXIT 0, 1 passed, 73 deselected; `test_typescript_compiles` explicitly
**PASSED**.
Vitest test-file/test count, re-measured at this round's own base `9da5d097`
(not trusted from any earlier round's figure): a disposable worktree
`.remedy-wt/wt-r13-base` was built at `9da5d097`, its own `apps/ui/node_modules`
symlinked at the primary checkout's real one, and `npx vitest run` was run
unmodified, via `subprocess.run`, from that worktree's own `apps/ui` using
that revision's own real `vitest.config.ts` — REAL EXIT 0, **37 files, 726
tests**. Then measured again at HEAD (post C4) in the primary checkout: REAL
EXIT 0, **37 files, 729 tests**. File count rose by exactly 0: True (C4 is an
append to an EXISTING file, unlike R12's C5, which added a whole new file).
`remedyApi.test.ts`'s new `describe("the job digest door", ...)` block
declares 3 `it(` cases; test count rose by exactly 3: True.

**G7 THE SUITES, THE TOOLCHAIN AND THE TREE, at C4.**
- `python3 -m pytest tests/ui_contracts/ -q` → REAL EXIT 0, 783 passed, 4 skipped.
- `python3 -m pytest tests/ui_server/ -q` → REAL EXIT 0, 515 passed.
- `python3 -m pytest tests/docs/ -q` → REAL EXIT 0, 295 passed.
- `python3 -m pytest tests/cli/test_golden_path.py -q` → REAL EXIT 0, 42 passed.
- `python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs`
  → REAL EXIT 0, 1 passed, 73 deselected; explicitly **PASSED**, not SKIPPED.

`git status --porcelain`: `''` (empty). `git ls-files --others
--exclude-standard`: 0 untracked. `git worktree list`: one line, the primary
checkout only. `git diff --numstat` per commit C0a..C4:
- C0a `726090a4` → `282	0	.agent/authored/f040-r13.md`
- C0b `402a61f8` → `200	277	.agent/last_block.md`
- C1 `12fa1e26` → `14	28	.agent/plan.md`
- C2 `131c3096` → `2	1	.agent/live_review.md`
- C3 `438172bb` → `45	0	apps/ui/src/api/remedyApi.ts`
- C4 `5d62f26b` → `48	1	apps/ui/src/api/remedyApi.test.ts`

Every insertion figure in the Commits table above is copied from this list.
C5's own count is not orderable here and is not ordered (§3 item 14).

## Authored-text proofs

`.remedy-wt/f040-r13-block.md` → `.agent/authored/f040-r13.md` and
`.agent/last_block.md`: sha256-equal, byte-length-equal (see G1). PLAN13 and
RECORD13 slices applied byte-for-byte, verified structurally by G2 and G3. No
other reviewer-authored text was applied this round (`loadJobDigest` and its
tests are a SPEC, not a slice, per constraint 1).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f040-r13.md` | done | G1 verifies |
| C0b mirror the block into `.agent/last_block.md` | done | G1 verifies |
| C1 rewrite `.agent/plan.md` from PLAN13 | done | G2 verifies; byte-equal, 44 lines, under 50 |
| C2 append RECORD13 to `.agent/live_review.md` | done | G3, G4 verify; open count 262→262 |
| C3 build `loadJobDigest` in `remedyApi.ts` | done | G5 verifies |
| C4 build `remedyApi.test.ts`'s "the job digest door" tests | done | G5, G6 verify |
| C5 rewrite `.agent/handoff.md` | done | this file |
| G1 transport | PASS | at C0b |
| G2 the plan | PASS | at C1 |
| G3 the record append | PASS | at C2 — reading (b) semantics declared, see Deviations 3 |
| G4 the ledger | PASS | at C2 |
| G5 the loader's shape, guard and red proof | PASS | at C4 — both mutations die at the expected node ids |
| G6 vitest | PASS | at C4 |
| G7 the suites, the toolchain and the tree | PASS | at C4 |

## Deviations & assumptions

1. **`git commit`'s own console line for C1 disagreed with `git diff
   --numstat` for the same commit.** At commit time, `git commit` printed
   "1 file changed, 44 insertions(+), 58 deletions(-)" and "rewrite
   .agent/plan.md (60%)" for the `.agent/plan.md` rewrite. Re-querying the
   SAME two commits afterward with `git diff --numstat 402a61f8..12fa1e26`,
   `git diff --stat` and an independent Python `difflib.SequenceMatcher`
   line-level LCS computation all agree on **14 insertions, 28 deletions** —
   not 44/58. The 44/58 figures are exactly `len(new file)=44` and
   `len(old file)=58`: git's commit-time summary appears to have applied its
   complete-rewrite ("-B" break-detection) heuristic, which substitutes the
   full old/new line counts for a real diff once a file changes above its
   similarity threshold, rather than the actual line-level diff `--numstat`
   computes. G7 explicitly orders `git diff --numstat`'s own output for this
   table (matching R12's own precedent of sourcing its Commits table from
   `--numstat` rather than any other diffstat rendering), so **14/28** is
   what is reported and used above; this is a tooling-display anomaly, not a
   content defect — `.agent/plan.md` at HEAD is confirmed byte-equal to
   PLAN13 by G2 regardless of which line-count rendering is read.
2. **G5's mutation route used the F256 D6 worktree route with the primary's
   `apps/ui/node_modules` symlinked in**, declared per the block's own
   "either plumbing is acceptable, declare which" clause. The same route was
   used for G6's base-count worktree.
3. **G3 reading (b)'s literal wording does not hold by exact equality for
   the FIRST of the N last blank-line units**, because constraint 4 orders
   the append as a SINGLE newline (not a blank line) between the base's
   existing content and the new slice. A raw `\n\n`-split of the whole
   committed file therefore fuses the base's own last pre-existing paragraph
   with the newly appended first paragraph into one merged unit — there is
   no blank line at that join for `\n\n` to split on. What DOES hold, and is
   what is reported above and checked by the negative control, is that this
   merged unit ENDS WITH the paragraph as an exact suffix, in order, for
   each of the N paragraphs. Re-deriving this same check against R12's own
   committed `.agent/live_review.md` (`edd1a691`) shows the identical shape:
   its N=2 case's SECOND paragraph matched by raw equality (nothing preceded
   it but the join), but its FIRST paragraph's "last unit" was likewise
   merged with R11's own tail paragraph and only matched by suffix, not raw
   equality — R12's handback asserted plain equality for both without this
   distinction. This is declared here, per amend0827 rule 2, as a
   non-blocking, damage-free prose-precision gap in how a PASSED gate's
   reading was previously worded rather than a defect in the ledger's actual
   bytes; nothing on disk needs repair.
4. No commit was reordered, dropped or added relative to the block's fixed
   C0a→C0b→C1→C2→C3→C4→C5 sequence.

## Next

Mount the card into `RemedyShell.tsx`: `loadJobDigest` (built this round,
paired with `jobDigestPath`), `latestActivityMs` read from the brain
stream's `recent` ring buffer, a real `window`-bound instance of
`browserDigestVisibilityPort` (built R12), and the card mounted as a sibling
of the shell div (not inside `<main>`, which `test_main_layout_guard.py`
pins to exactly four children), with its own pytest text guard.
`onOpenDecisions` and `onPrimaryAction` stay inert that round too, per
PLAN13 step 2.
