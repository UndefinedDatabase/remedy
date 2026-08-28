# Handback — F256 Diff viewer completion, round 1

## Session

SESSION 1 of feature F256 · round 1 · rounds so far 1

## Range

Review of 0e8ab5b4..HEAD (branch `feature/f256-diff-viewer-completion`, cut from
`main` at `0e8ab5b4`).

## Commits

### 6f5916bb chore(agent): save F256 R1 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f256-r1.md` | +400 / -0 | C0a: the block saved byte for byte |

### 5b3c02a0 chore(agent): mirror F256 R1 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +379 / -265 | C0b: the same bytes, one blob id |

### 9c05aea3 chore(agent): retarget state onto F256 and record DECISION F256 D1
| Path | +/- | Reason |
|---|---|---|
| `.agent/context.md` | +25 / -35 | C1: CTXF256R1, whole-file replacement |
| `.agent/decisions.md` | +37 / -0 | C1: DECF256R1 appended |
| `.agent/plan.md` | +25 / -20 | C1: PLANF256R1, whole-file replacement |

### d4c00438 docs(status): claim F256 diff viewer completion
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1 / -1 | C2: the CLAIMFROM to CLAIMTO rewrite |

### 6581eec4 feat(ui): per-line diff highlight model with a closed token set
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/diffHighlight.ts` | +279 / -0 | C3: SPEC S1–S11, the model |
| `apps/ui/src/api/diffHighlight.test.ts` | +119 / -0 | C3: SPEC S12, 7 vitest tests |

### C4 (this commit) chore(agent): hand back F256 R1
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this file | C4: a handoff cannot table the commit that writes it |

Every `+/-` cell above was taken from `git diff --numstat <sha>~1..<sha>` and
compared cell by cell against the figures G8 reports; the two agree for all five
commits in the range.

## External actions

| Command | Outcome |
|---|---|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — Open PR Gate passes, continue normally |
| `git checkout -b feature/f256-diff-viewer-completion` | created at `0e8ab5b4` |
| `git worktree add .remedy-wt/f256-r1-mut 6581eec4 --detach` | created (G6) |
| `git worktree remove .remedy-wt/f256-r1-mut` | removed; `git worktree list` shows the primary only |
| `git push -u origin feature/f256-diff-viewer-completion` | see the push line below |

No pull request was created and nothing was merged.

## Verification

G1 HYGIENE — `.agent/STOP` read from disk with `os.path.exists`: **False** before
C0a and **False** before C3. `git rev-parse HEAD` before C0a =
`0e8ab5b4f780b5265a6aa604ee89067399046b1e`, equal to `0e8ab5b4` as required.
`git branch --show-current` = `feature/f256-diff-viewer-completion`.
`git status --porcelain | wc -l` after C0a = 0, after C0b = 0, after C1 = 0,
after C2 = 0, after C3 = 0.

G2 TRANSPORT — one digest comparison.
`git show 6f5916bb:.agent/authored/f256-r1.md` → sha256
`270fb5dade65ca8e2e7ace8888c6755205c4d25fbca0d80313efabb716ef68fc`, 21445 bytes.
`.remedy-wt/f256-r1-block.md` → sha256
`270fb5dade65ca8e2e7ace8888c6755205c4d25fbca0d80313efabb716ef68fc`, 21445 bytes.
Equal: **True**. That original was written before this worker existed and is not
this worker's output, so the reading covers transport and not only
self-consistency. `git rev-parse 5b3c02a0:.agent/authored/f256-r1.md` and
`git rev-parse 5b3c02a0:.agent/last_block.md` both print
`111985b6be139c8e3c7423bfbc8c1da618785d89` — ONE blob id.

G3 STATE SLICES AT C1 — `.agent/plan.md` at C1 equals PLANF256R1 including the
trailing newline: **True**. `.agent/context.md` at C1 equals CTXF256R1 including
it: **True**. `wc -l` of `.agent/plan.md` = **37**, under 50. Lines exactly
`## Goal` in `.agent/plan.md` = 1; lines exactly `## Next Steps` = 1; lines
exactly `## Active Branch` in `.agent/context.md` = 1.

G4 DECISIONS APPEND AT C1, two readers.
(a) `0e8ab5b4` blob of `.agent/decisions.md` + newline + DECF256R1 == C1 blob:
**True**. NEGATIVE CONTROL: the first appended paragraph spans composed bytes
[687669, 687822); flipping one bit of the byte at offset 687745 (character `t`,
confirmed by the script to lie inside that paragraph) makes the equality
**False**.
(b) N, counted by the script from the slice itself, = **7** paragraphs (the
seventh is the slice's trailing empty unit, which the slice really carries). The
LAST 7 blank-line-separated units of the C1 blob match those paragraphs IN ORDER,
unit by unit: units 1–7 all True. The pre-round blob is a byte PREFIX of the C1
blob: **True**; byte lengths 687668 → 689972.

G5 THE CLAIM AT C2, over `docs/roadmap/STATUS.md` at `d4c00438` — CLAIMFROM
count = **0**; CLAIMTO count = **1**; CLAIMTO present as a WHOLE LINE **1** time;
lines matching `^- \[~\] F\d{3} — ` = **1**, which is at most 1 as
`tests/docs/test_docs_consistency.py` requires; lines matching
`^- \[x\] F\d{3} — ` = **60** before C2 and **60** after C2 — unmoved.

G6 THE MODEL RED-PROOF AT C3 — in the disposable worktree
`.remedy-wt/f256-r1-mut` at `6581eec4`, never in the primary checkout, driven
from `python3` with
`["npx","vitest","run","--root",WT+"/apps/ui","--config",PRIMARY+"/apps/ui/vitest.config.ts","src/api/","--reporter=basic"]`,
`cwd=PRIMARY+"/apps/ui"` (DECISION F037 D10; both flags load-bearing, run scoped
to `src/api/`).

| Run | Exit | Result |
|---|---|---|
| CONTROL, unmutated, FIRST | 0 | Test Files 30 passed (30) · Tests 595 passed (595) |
| MUTATION (i) S7 — the scanner drops a character it consumed | 1 | Test Files 1 failed \| 29 passed (30) · Tests 6 failed \| 589 passed (595) |
| MUTATION (ii) S10 — adjacent `plain` segments returned unmerged | 1 | Test Files 1 failed \| 29 passed (30) · Tests 2 failed \| 593 passed (595) |
| CONTROL again, every file restored | 0 | Test Files 30 passed (30) · Tests 595 passed (595) |

Mutation (i) failed, by name: the two concatenation tests, "produces every token
kind the closed set names", the merge test, "ends an unterminated string at the
end of the line" and the totality test. Mutation (ii) failed, by name: the merge
test and the totality test. Each mutation was applied ALONE and reverted before
the next; after the second revert the worktree file was confirmed byte-identical
to the C3 blob and the worktree's `git status --porcelain` had 0 lines. The
reviewer's measurement at `0e8ab5b4` was control 588 passed; this round's control
is 595, the same 588 plus the 7 tests C3 adds. After removal,
`git worktree list` shows only `/home/decodeux/Repos/remedy` and the primary's
`git status --porcelain | wc -l` = 0.

G7 THE SUITES AT C3 — one pytest process at a time, from the repository root, in
the PRIMARY checkout. All twelve exit 0.

| Command | Exit | Result |
|---|---|---|
| `pytest tests/orchestration/test_test_runner.py -q` | 0 | 52 passed in 5.33s — wall clock 7.7s |
| `pytest tests/docs/ -q` | 0 | 295 passed in 0.60s |
| `pytest tests/orchestration/test_roadmap_index.py -q` | 0 | 30 passed in 0.35s |
| `pytest tests/ui_server/ -q` | 0 | 495 passed in 30.11s |
| `pytest tests/regression/test_resource_safety.py -q` | 0 | 21 passed in 11.69s |
| `pytest tests/orchestration/test_integrity_gate.py -q` | 0 | 16 passed in 0.26s |
| `pytest tests/ui_contracts/test_brain_stream_ring.py -q` | 0 | 67 passed in 0.27s |
| `pytest tests/ui_contracts/test_cost_metric_render.py -q` | 0 | 30 passed in 0.32s |
| `pytest tests/ui_contracts/test_ux_quality.py -q` | 0 | 125 passed, 2 skipped in 1.25s |
| `pytest tests/ui_contracts/test_diff_view_model.py -q` | 0 | 8 passed in 0.67s |
| `pytest tests/ui_contracts/test_diff_view_render.py -q` | 0 | 19 passed in 0.45s |
| `pytest tests/cli/test_golden_path.py -q` | 0 | 42 passed in 21.78s |

G8 STRUCTURE, over `0e8ab5b4..6581eec4` — `git diff --name-only` returns exactly
eight paths: `.agent/authored/f256-r1.md`, `.agent/context.md`,
`.agent/decisions.md`, `.agent/last_block.md`, `.agent/plan.md`,
`apps/ui/src/api/diffHighlight.test.ts`, `apps/ui/src/api/diffHighlight.ts`,
`docs/roadmap/STATUS.md`. Residue range MINUS change set: `[]`. Residue change
set MINUS range: `['.agent/handoff.md']`, which is C4's own path and therefore
cannot appear in a range ending at C3 — see the deviations. Residue change set
without `.agent/handoff.md` MINUS range: `[]`.

| Commit | Insertions | Under 500 | Parents | Single-parent |
|---|---|---|---|---|
| C0a `6f5916bb` | 400 | True | 1 | True |
| C0b `5b3c02a0` | 379 | True | 1 | True |
| C1 `9c05aea3` | 87 | True | 1 | True |
| C2 `d4c00438` | 1 | True | 1 | True |
| C3 `6581eec4` | 398 | True | 1 | True |

Marker lines counted affirmatively over each file's C3 content, `<<<SLICE ` and
`<<<END ` respectively: `.agent/plan.md` 0 / 0; `.agent/context.md` 0 / 0;
`.agent/decisions.md` 0 / 0; `docs/roadmap/STATUS.md` 0 / 0;
`apps/ui/src/api/diffHighlight.ts` 0 / 0;
`apps/ui/src/api/diffHighlight.test.ts` 0 / 0; and the non-zero control
`.agent/authored/f256-r1.md` 5 / 5. `git ls-files .remedy-wt | wc -l` = **0**.

Extra reading, not an ordered gate, taken during the self-review loop before C3:
`npx tsc --noEmit -p tsconfig.json` in `apps/ui` exited 0.

## Authored-text proofs

| Slice | Target | Result |
|---|---|---|
| PLANF256R1 | `.agent/plan.md` | byte-equal including the trailing newline — True (G3) |
| CTXF256R1 | `.agent/context.md` | byte-equal including the trailing newline — True (G3) |
| DECF256R1 | `.agent/decisions.md` | append reconstructed byte for byte with a negative control — True (G4) |
| CLAIMFROM / CLAIMTO | `docs/roadmap/STATUS.md` | FROM 0, TO 1, whole-line 1 (G5) |

Every slice was extracted from the COMMITTED blob
`git show 6f5916bb:.agent/authored/f256-r1.md`, never from the prompt text, by a
script that splits on the `<<<SLICE ` / `<<<END ` delimiter lines and keeps only
the bytes between them. No delimiter line reached any target file (G8).

## Deviations & assumptions

1. THE ORDERED COMMIT SEQUENCE WAS FOLLOWED EXACTLY: C0a, C0b, C1, C2, C3, C4 —
   six commits, none added, none dropped, none reordered.
2. GUARD RE-EXPRESSIONS (constraint 6). Two shell forms were refused by this
   session's guard and were re-expressed, never skipped:
   (a) `cd /home/decodeux/Repos/remedy/apps/ui && npx tsc ... | tail` was denied
   by form; re-expressed as `subprocess.run([...], cwd=".../apps/ui")` inside a
   `python3 - <<'PY'` heredoc. The same re-expression carried every `npx vitest`
   invocation of G6, which the block already orders driven from `python3`.
   (b) The first G8 script was denied by form — it contained brace literals
   holding quotes. Re-expressed by writing the same script to
   `.remedy-wt/g8_structure.py` (gitignored) with no such literal and running it
   as `python3 .remedy-wt/g8_structure.py`. No gate was weakened or dropped;
   both re-expressions run the same commands with the same arguments.
3. G8's change-set residue is EMPTY IN BOTH DIRECTIONS ONLY AFTER
   `.agent/handoff.md` is set aside. The block lists that path in the change set
   and also fixes G8's range to end at C3, so the path is measured before the
   commit that writes it exists. Both readings are reported above rather than the
   convenient one. This is a property of the block, not a departure from it.
4. APPLIED AS WRITTEN, FLAGGED AS ASKED (constraint 1). PLANF256R1's
   `## Current Step` table already reads `the per-line highlight model | done`,
   and that row is false at C1, where the slice lands, and only becomes true at
   C3. The slice was applied byte for byte regardless, as constraint 1 requires;
   the record is repaired by a later append if the reviewer wants it repaired.
5. Two scratch files this round produced remain under the gitignored
   `.remedy-wt/`: `g8_structure.py` and five `slice_*.txt` extractions. They are
   untracked (`git ls-files .remedy-wt` = 0), the primary tree is clean, and they
   are left in place deliberately as gate evidence for the review zip.
6. `.agent/live_review.md` was NOT edited, per the block: F037 R27 ended its
   branch, so §4 item 13 leaves nothing owed to the ledger this round. Neither
   of the two reviewer-only verdict paragraph forms was written anywhere by this
   worker, in any file — those are the reviewer's to author.
7. ASSUMPTION carried from the block and not independently re-derived: the
   grammar mapping's keys are the eleven distinct VALUES of
   `DIFF_SUPPORTED_LANGUAGES` in `apps/ui/src/api/diffViewModel.ts` read at
   `0e8ab5b4` — typescript, tsx, javascript, jsx, python, json, css, markdown,
   shell, yaml, toml. Nothing in `diffHighlight.ts` imports that constant, per
   SPEC S1, so no gate this round pins the two lists together.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block verbatim | done | |
| C0b mirror into `.agent/last_block.md` | done | |
| C1 retarget plan/context, append DECISION F256 D1 | done | |
| C2 the STATUS claim | done | |
| C3 the highlight model and its vitest suite | done | |
| C4 rewrite `.agent/handoff.md` | done | this commit |
| G1 hygiene | done | STOP False twice; HEAD `0e8ab5b4`; porcelain 0 after all five |
| G2 transport | done | digests equal; one blob id |
| G3 state slices | done | both True; plan 37 lines |
| G4 decisions append | done | True, negative control False, N=7 in order |
| G5 the claim | done | FROM 0, TO 1, tilde 1, x 60 → 60 |
| G6 model red-proof | done | control 0/595, both mutations exit 1, control 0/595 |
| G7 the suites | done | twelve commands, every one exit 0 |
| G8 structure | done | residues empty (see deviation 3); all under 500; all single-parent |

Open findings: unchanged this round — no finding was registered or resolved, and
`.agent/live_review.md` was not touched.

## Next

The reviewer independently re-runs G1 through G8 over `0e8ab5b4..HEAD` and issues
the verdict for F256 R1. The next round's first commit books that verdict into
`.agent/live_review.md`, and the work it opens is Next Step 1 of `.agent/plan.md`:
compose the token cut with the intraline cut in the model layer. Phase 1 rule 1
(`.agent/STOP`) is read before rule 2.
