# Handback — F256 Diff viewer completion, round 2

## Session

SESSION 1 of feature F256 · round 2 · rounds so far 2

## Range

Review of 7b23c46a..HEAD (branch `feature/f256-diff-viewer-completion`).

## Commits

### 8ba2684a chore(agent): save the F256 round 2 block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f256-r2.md` | +301 / -0 | C0a: the block copied byte for byte |

### 06ee19ea chore(agent): mirror the round 2 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +183 / -282 | C0b: the same bytes, one blob id |

### b45d9be2 chore(agent): advance the plan for the highlight composition
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +13 / -12 | C1: PLANF256R2, whole-file replacement |

### 5ae8b0af chore(agent): book the F256 R1 verdict and its slips
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +12 / -0 | C2: GATEF256R1 appended |
| `.agent/prose_slips.md` | +4 / -0 | C2: SLIPSF256R1 appended |

### 739d31e0 feat(diff-viewer): compose the token cut with the intraline cut
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/diffHighlight.ts` | +98 / -0 | C3: SPEC S1–S7, the composition |
| `apps/ui/src/api/diffHighlight.test.ts` | +229 / -1 | C3: SPEC S8, 6 further vitest tests |

### C4 (this commit) chore(agent): hand back F256 R2
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this file | C4: a handoff cannot table the commit that writes it |

Every `+/-` cell above was taken from `git diff --numstat <sha>^ <sha>` and
compared cell by cell against the figures G8 reports; the two agree for all five
commits in the range.

## External actions

| Command | Outcome |
|---|---|
| `gh pr list --state open --json number,headRefName` | `[]` — no open PR; none created, nothing merged |
| `git worktree add .remedy-wt/f256-r2-mut 739d31e0` | created, detached at C3 (G6) |
| `git worktree remove .remedy-wt/f256-r2-mut` | removed; `git worktree list` shows the primary only |
| `npx vite build` in `apps/ui` | exit 0, 1.6s — dist warmed before the G7 server suites; `dist/` is gitignored, tree stayed clean |
| `git push -u origin feature/f256-diff-viewer-completion` | see the push line below |

No pull request was created and nothing was merged.

## Verification

G1 HYGIENE — `.agent/STOP` read from disk with `os.path.exists`: **False** before
C0a and **False** before C3. `git rev-parse HEAD` before C0a =
`7b23c46a6f50de2304a5227cf00a8aa295b24c10`, equal to `7b23c46a` as required.
`git branch --show-current` = `feature/f256-diff-viewer-completion`.
`git status --porcelain | wc -l` after C0a = 0, after C0b = 0, after C1 = 0,
after C2 = 0, after C3 = 0.

G2 TRANSPORT — one digest comparison.
`git show 8ba2684a:.agent/authored/f256-r2.md` → sha256
`449a54ea4a2b799b8687a9c649133fc5bb87c6d463a066cf137cb0c7704f88ae`, 19466 bytes.
`.remedy-wt/f256-r2-block.md` → sha256
`449a54ea4a2b799b8687a9c649133fc5bb87c6d463a066cf137cb0c7704f88ae`, 19466 bytes.
Equal: **True**. That original was written before this worker existed and is not
this worker's output, so the reading covers transport and not merely the worker's
self-consistency. `git rev-parse 06ee19ea:.agent/authored/f256-r2.md` and
`git rev-parse 06ee19ea:.agent/last_block.md` both print
`9a042c5a1849b360018e530a9ee2e498d998c7f1` — ONE blob id.

G3 THE PLAN AT C1 — `.agent/plan.md` at C1 equals PLANF256R2 including the
trailing newline: **True** (1749 bytes on both sides). `wc -l` = **38**, under 50
as AGENTS.md requires. Lines exactly `## Goal` = **1**; lines exactly
`## Next Steps` = **1**.

G4 THE RECORD AT C2, two readers, each file separately.

`.agent/live_review.md` with GATEF256R1:
(a) `7b23c46a` blob + newline + slice == C2 blob: **True**. NEGATIVE CONTROL: the
first appended paragraph spans composed bytes [1335996, 1336225); flipping one bit
of the byte at offset 1336016 (character `e`, confirmed by the script to lie
inside that paragraph) makes the equality **False**.
(b) N, counted by the script from the slice itself with any empty trailing unit
ignored, = **6** paragraphs. The LAST 6 blank-line-separated units of the C2 blob
match those paragraphs IN ORDER, unit by unit: units 0–5 all True. The pre-round
blob is a byte PREFIX of the C2 blob: **True**; byte lengths 1335995 → 1339712.

`.agent/prose_slips.md` with SLIPSF256R1:
(a) `7b23c46a` blob + newline + slice == C2 blob: **True**. NEGATIVE CONTROL: the
first appended paragraph spans composed bytes [12777, 13551); flipping one bit of
the byte at offset 12797 (character `1`, confirmed by the script to lie inside
that paragraph) makes the equality **False**.
(b) N, counted by the script from the slice itself, = **1**. The slice's three
dated lines carry no blank line between them, so blank-line splitting sees ONE
unit; that unit matches the last unit of the C2 blob. The pre-round blob is a
byte PREFIX of the C2 blob: **True**; byte lengths 12776 → 13551.

G5 THE LEDGER AT C2 — the same six figures over both blobs.

| Figure | `7b23c46a` | C2 `5ae8b0af` |
|---|---|---|
| lines matching `^- R-\d+ — ` | 292 | 292 |
| all of those DISTINCT | True | True |
| lines matching `^Done: R-\d+ — ` | 43 | 43 |
| lines matching `^Landed: R-` | 11 | 11 |
| lines matching `^Gate: F\d+ R\d+ — ` | 97 | 98 |
| OPEN SET, computed as a set | 251 | 251 |

Every figure is UNMOVED except the gate-paragraph count, which rises by exactly
ONE, as the block requires of a round that registers and resolves nothing. The
literal `Gate: F256 R1` occurs exactly **1** time in the C2 blob.

G6 THE COMPOSITION RED-PROOF AT C3 — in the disposable worktree
`.remedy-wt/f256-r2-mut` at `739d31e0`, never in the primary checkout, driven from
`python3` with
`["npx","vitest","run","--root",WT+"/apps/ui","--config",PRIMARY+"/apps/ui/vitest.config.ts","src/api/","--reporter=basic"]`,
`cwd=PRIMARY+"/apps/ui"` (DECISION F037 D10; both flags load-bearing, run scoped
to `src/api/`).

| Run | Exit | Result |
|---|---|---|
| CONTROL, unmutated, FIRST | 0 | Test Files 30 passed (30) · Tests 601 passed (601) |
| MUTATION (i) S6(b) — every emitted run given `marked: false` | 1 | Test Files 1 failed \| 29 passed (30) · Tests 3 failed \| 598 passed (601) |
| MUTATION (ii) S6(c) — every emitted run given the kind `plain` | 1 | Test Files 1 failed \| 29 passed (30) · Tests 2 failed \| 599 passed (601) |
| MUTATION (iii) S7 — runs emitted unmerged, one per character | 1 | Test Files 1 failed \| 29 passed (30) · Tests 1 failed \| 600 passed (601) |
| CONTROL again, every file restored | 0 | Test Files 30 passed (30) · Tests 601 passed (601) |

Failures by name. (i): "gives every character the marked flag of the input
segment covering it", "merges adjacent runs that agree on both marked and kind",
"returns every run plain for an unknown language while the marked flags survive
unchanged". (ii): "gives every character the kind tokenizeDiffLine gives that
position for the same language", "merges adjacent runs that agree on both marked
and kind". (iii): "merges adjacent runs that agree on both marked and kind".
Each mutation was applied ALONE by an exact single-occurrence string replacement
(the script asserts the count is 1) and reverted before the next; after each
revert the worktree file was confirmed byte-identical to the C3 content, and the
worktree's `git status --porcelain` was empty at the end. The reviewer's own
measurement at `7b23c46a` was control 595; this round's control is 601, the same
595 plus the 6 tests C3 adds. After removal, `git worktree list` shows only
`/home/decodeux/Repos/remedy` and the primary's `git status --porcelain | wc -l`
= 0.

G7 THE SUITES AT C3 — one pytest process at a time, from the repository root, in
the PRIMARY checkout. All ten exit 0.

| Command | Exit | Result |
|---|---|---|
| `pytest tests/orchestration/test_test_runner.py -q` | 0 | 52 passed in 5.31s — wall clock 5.5s |
| `pytest tests/ui_server/ -q` | 0 | 495 passed in 28.63s |
| `pytest tests/regression/test_resource_safety.py -q` | 0 | 21 passed in 11.53s |
| `pytest tests/orchestration/test_integrity_gate.py -q` | 0 | 16 passed in 0.28s |
| `pytest tests/ui_contracts/test_brain_stream_ring.py -q` | 0 | 67 passed in 0.27s |
| `pytest tests/ui_contracts/test_cost_metric_render.py -q` | 0 | 30 passed in 0.32s |
| `pytest tests/ui_contracts/test_ux_quality.py -q` | 0 | 125 passed, 2 skipped in 1.51s |
| `pytest tests/ui_contracts/test_diff_view_model.py -q` | 0 | 8 passed in 0.20s |
| `pytest tests/ui_contracts/test_diff_view_render.py -q` | 0 | 19 passed in 0.20s |
| `pytest tests/cli/test_golden_path.py -q` | 0 | 42 passed in 20.67s |

G8 STRUCTURE, over `7b23c46a..739d31e0` — `git diff --name-only` returns exactly
seven paths: `.agent/authored/f256-r2.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
`apps/ui/src/api/diffHighlight.test.ts`, `apps/ui/src/api/diffHighlight.ts`.
With `.agent/handoff.md` set aside, as the block directs: residue range MINUS
change set `[]`, residue change set MINUS range `[]` — both empty.

| Commit | Insertions | Under 500 | Parents | Single-parent |
|---|---|---|---|---|
| C0a `8ba2684a` | 301 | True | 1 | True |
| C0b `06ee19ea` | 183 | True | 1 | True |
| C1 `b45d9be2` | 13 | True | 1 | True |
| C2 `5ae8b0af` | 16 | True | 1 | True |
| C3 `739d31e0` | 327 | True | 1 | True |

Marker lines counted affirmatively over each file's C3 content, `<<<SLICE ` and
`<<<END ` respectively: `.agent/plan.md` 0 / 0; `.agent/live_review.md` 0 / 0;
`.agent/prose_slips.md` 0 / 0; `apps/ui/src/api/diffHighlight.ts` 0 / 0;
`apps/ui/src/api/diffHighlight.test.ts` 0 / 0; and the non-zero control
`.agent/authored/f256-r2.md` 3 / 3. `git ls-files .remedy-wt | wc -l` = **0**.

Extra readings, not ordered gates, taken during the self-review loop before C3:
`npx tsc --noEmit` in `apps/ui` exited 0, and `npx vitest run
src/api/diffHighlight.test.ts` in the primary exited 0 with 13 tests passed.

## Authored-text proofs

| Slice | Target | Result |
|---|---|---|
| PLANF256R2 | `.agent/plan.md` | byte-equal including the trailing newline — True (G3) |
| GATEF256R1 | `.agent/live_review.md` | append reconstructed byte for byte, negative control False, last 6 units in order (G4) |
| SLIPSF256R1 | `.agent/prose_slips.md` | append reconstructed byte for byte, negative control False, last 1 unit matches (G4) |

Every slice was extracted from the COMMITTED blob
`git show 8ba2684a:.agent/authored/f256-r2.md`, never from the prompt text, by a
script that splits on the `<<<SLICE ` / `<<<END ` delimiter lines and keeps only
the bytes between them. No delimiter line reached any target file (G8). The C0a
file itself was produced by `cp` from `.remedy-wt/f256-r2-block.md`, copying bytes
rather than retyping them.

## Deviations & assumptions

1. THE ORDERED COMMIT SEQUENCE WAS FOLLOWED EXACTLY: C0a, C0b, C1, C2, C3, C4 —
   six commits, none added, none dropped, none reordered.
2. GUARD RE-EXPRESSIONS (constraint 6). Two shell forms were refused by this
   session's guard and were re-expressed, never skipped:
   (a) `cd .../apps/ui && npx vitest run ... | tail` was denied by form;
   re-expressed as `subprocess.run([...], cwd=".../apps/ui")` inside a
   `python3 - <<'PY'` heredoc. The same re-expression carries every `npx vitest`,
   `npx tsc` and `npx vite build` invocation of this round, and G6 is already
   ordered to be driven from `python3`.
   (b) The G8 script was denied by form inside a heredoc — it contained f-strings
   with brace literals holding quotes. Re-expressed by writing the identical
   script to `.remedy-wt/f256-r2-g8.py` (gitignored) without such literals and
   running it as `python3 .remedy-wt/f256-r2-g8.py`. No gate was weakened or
   dropped; both re-expressions run the same commands with the same arguments.
3. APPLIED AS WRITTEN, FLAGGED AS ASKED (constraint 1). PLANF256R2's
   `## Current Step` table reads `compose the token cut with the intraline cut |
   done | this round` at C1, where the slice lands; that row is false at C1 and
   becomes true at C3, within the same round. It is the same shape as the slip
   already recorded for PLANF256R1. The slice was applied byte for byte
   regardless, as constraint 1 requires.
4. G4 READER (b) OVER `.agent/prose_slips.md` COUNTS N = 1, NOT 3. The
   SLIPSF256R1 slice is three dated lines with no blank line between them, so the
   blank-line split the block orders sees ONE paragraph. The comparison still
   covers the whole appended region — reader (a) reconstructs it byte for byte —
   and the count was taken by the script from the slice itself, never from the
   block, exactly as ordered. Reported rather than rounded up to the line count.
5. THE FRONTEND DIST WAS REBUILT BEFORE G7, which the block does not order. C3
   makes `apps/ui/src` newer than `apps/ui/dist/index.html`, so
   `packages/orchestration/ui_server._frontend_is_stale()` answered True and the
   `tests/ui_server/` supervisors would have auto-built inside their start
   budget. `npx vite build` (exit 0, 1.6s) warmed it first; `_frontend_is_stale()`
   then answered False. `dist/` is gitignored, and `git status --porcelain` was
   empty before and after.
6. Three scratch files this round produced remain under the gitignored
   `.remedy-wt/`: `f256-r2-g8.py`, `f256-r2-control.txt` and the reviewer's own
   `f256-r2-block.md`. They are untracked (`git ls-files .remedy-wt` = 0), the
   primary tree is clean, and the first two are left in place deliberately as
   gate evidence for the review zip.
7. NO VERDICT PARAGRAPH OF THIS WORKER'S OWN was written anywhere, in any file.
   The verdict text booked into `.agent/live_review.md` at C2 is the
   reviewer-authored GATEF256R1 slice, applied byte for byte, and the same holds
   for SLIPSF256R1 in `.agent/prose_slips.md`.
8. ASSUMPTION, per SPEC S2 and constraint 9: `DiffMarkedSegment` is declared
   STRUCTURALLY in `diffHighlight.ts` and is asserted nowhere to stay identical to
   `DiffLineSegment` in `apps/ui/src/api/diffViewModel.ts`. The two shapes agree
   at `739d31e0` — both are `{ text: string; marked: boolean }` — but no gate this
   round pins them together, because pinning them would require the import that
   constraint 9 forbids. The wiring round that first passes real
   `splitLineIntoIntralineSegments` output into `composeHighlightedRuns` is where
   a type error would surface.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block verbatim | done | |
| C0b mirror into `.agent/last_block.md` | done | |
| C1 advance `.agent/plan.md` | done | |
| C2 append the R1 verdict and the slips | done | |
| C3 the composition and its vitest tests | done | |
| C4 rewrite `.agent/handoff.md` | done | this commit |
| G1 hygiene | done | STOP False twice; HEAD `7b23c46a`; porcelain 0 after all five |
| G2 transport | done | digests equal at 19466 bytes; one blob id |
| G3 the plan at C1 | done | byte-equal True; 38 lines; 1 and 1 |
| G4 the record at C2 | done | both True, both negative controls False, N=6 and N=1 in order |
| G5 the ledger at C2 | done | every figure unmoved, gate paragraphs 97 → 98, `Gate: F256 R1` once |
| G6 composition red-proof | done | control 0/601, all three mutations exit 1, control 0/601 |
| G7 the suites | done | ten commands, every one exit 0 |
| G8 structure | done | residues empty both ways; all under 500; all single-parent |

Open findings: unchanged this round — the C2 append registers no finding and
resolves none; the open set is 251 before and after.

## Next

The reviewer independently re-runs G1 through G8 over `7b23c46a..HEAD` and issues
the verdict for F256 R2. The work that verdict opens is Next Step 1 of
`.agent/plan.md`: ship the lazy per-language bundles and wire
`loadDiffLanguageBundle` into `DiffView`, rendering one element per composed run
with a palette derived from custom properties already defined under `apps/ui/src`.
Phase 1 rule 1 (`.agent/STOP`) is read before rule 2.
