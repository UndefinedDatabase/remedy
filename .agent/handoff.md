# Handback — F031 R8 (record the R7 verdict, plan T002; state only)
Branch: feature/f031-decision-inbox · Base: 3f3d3e8f · no PR exists.
Fortschritt: ~25 % (F031 claimed; R1 through R7 landed and gated ·
             T001 SHIPPED — the derivation module, the read endpoint
             and 29 tests are on disk and green · T002 planned, its
             design gap named · T003 offen) — Schaetzung
(The `Fortschritt:` block above is carried verbatim; I counted 4 lines.)

## Range
Review of 3f3d3e8f..HEAD — 5 commits: C0a c0144d2c, C0b b23be552, C1 23522837, C2 3dbc1ba8, C3 this one.

## Commits
### c0144d2c docs(state): save the F031 R8 record step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r8.md | +293/-0 | C0a — block saved verbatim |
### b23be552 docs(state): mirror the F031 R8 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +157/-321 | C0b — byte-identical mirror of C0a |
### 23522837 docs(state): plan T002 against the measured design gap
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21/-21 | C1 — slice PLANF031R8 |
### 3dbc1ba8 docs(review): record the F031 R7 PASS with the pushed tips
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2 — slice GATE7 appended |
### C3 this commit (R-0149 self-reference exception)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C3 — this handback |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| push | deviated | ordered by G9 and run after C3, but its OUTCOME is deliberately not written here: it is not a value of any file this round writes. The reviewer measures the pushed tips and records them in the R8 entry of `.agent/live_review.md` (R-0679 fix clause) |

## External actions
`git push origin feature/f031-decision-inbox` — run after C3. This gate's outcome is not a value of any file this round writes; the reviewer measures the pushed tips at the next gate and records them in the R8 entry of `.agent/live_review.md`.
`git worktree add --detach .remedy-wt/r8-neg 3dbc1ba8` then `git worktree remove --force .remedy-wt/r8-neg` — the G5 mutant only, removed BY ITS EXACT PATH and before the G8 suites; `git worktree list` back to 1 line. `.remedy-wt/dry` and `.remedy-wt/rev-r7` were not created, read or deleted.
No `gh` command, no pull request, nothing merged, no history rewritten, no force-push.

## Verification
G1 PASS — branch `feature/f031-decision-inbox`, not `main`; `.agent/STOP` absent from disk before C0a and again before C3; `git status --porcelain` 0 lines after each of C0a, C0b, C1 and C2.
G2 PASS — `.remedy-wt/f031-r8.md` before C0a, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are ALL sha256 f3b569635c4e158e8569622372b0c1192799c7e17a5fa0901c59ca64c15728fc, 22462 bytes, 293 lines; C0a's and C0b's file are the SAME git blob ba2a3a9e16f127a3042f6edea319df7558268d12.
G3 PASS — my extractor over the committed C0a blob printed 2 slices, 50 CONTENT lines inside markers, 293 TOTAL lines (4 marker lines).
G4 PASS — `.agent/plan.md` at C1 byte-equal to PLANF031R8, 3017 bytes both, newline-INCLUDED convention; negative control against the slice with its trailing newline REMOVED is FALSE; `^## Goal$` 1, `^## Next Steps$` 1; `wc -l` 49, strictly under 50.
G5 PASS — reader A, ONE boolean over the whole file in the shape constraint 7 states (that paragraph, not restated here): True; 561117 → 566277 bytes, delta 5160 = 1 + 5159. Reader B, an independent blank-line split: 283 → 284 units, the LAST equal to GATE7. Control: the byte at offset 561218, inside the appended paragraph, flipped in the disposable worktree `.remedy-wt/r8-neg` — BOTH readers rejected the mutant and BOTH accepted the true file.
G6 PASS — `^- R-\d+ — ` 240 → 240, all DISTINCT; ids ADDED the EMPTY SET and ids REMOVED the EMPTY SET; maximum R-0679 → R-0679; `^Done: R-` 2 → 2; `^Recurrence: R-` 15 → 15 UNCHANGED; `^Gate: R\d+ — ` 7 → 8 gaining exactly the key R7, with R19, R1, R2, R3, R4, R5 and R6 still present.
G7 PASS — `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1 and `.agent/live_review.md` at C2; `git diff --name-only 3f3d3e8f..3dbc1ba8` names 4 paths, none under `packages/`, `apps/`, `tests/` or `docs/`, and neither `.agent/decisions.md` nor `.agent/f031_inventory.md`; range MINUS change set EMPTY; change set MINUS range exactly `.agent/handoff.md`; four single-parent commits with INSERTIONS 293, 157, 21 and 2, each under 500; `git ls-files .remedy-wt` 0; `*.zip` 0; `git worktree list` 1 line. Reflog scoped to THIS ROUND's 4 entries (every entry above base 3f3d3e8f), read by the OPERATION PREFIX before the first colon of `git reflog --format=%gs`: all 4 prefixes are `commit`, so amend 0, rebase 0, cherry 0.
G8 PASS — word-bounded `[0-9a-f]{7,40}` over the committed C0a blob: 9 occurrences, 6 distinct tokens, `git cat-file -t` exit 0 on every one — 98f6f251 is a blob, and 3f3d3e8f, 3f3d3e8f7f6032576db7ad0e5f672869b60f6dc2, 6325ac2f, 85daf94d and 8a0bdc18 are commits. THE FAILING SET IS EMPTY, exactly as this block predicted; the 64-char sha256 digests it also carries are not matched by the pattern. Suites: `git worktree list` 1 line immediately BEFORE the first pytest; five suites run SERIALLY in the primary checkout at the C2 tree, never two pytest processes alive, REAL exit code 0 for each at `tests/ui_server/` 474, test_test_runner 52, test_resource_safety 21, test_integrity_gate 16 and test_golden_path 42 — cell for cell the readings the reviewer took at 3f3d3e8f, so there is no difference to account for.
G9 — `git push origin feature/f031-decision-inbox`, run after C3. Its outcome is not a value of any file this round writes; the reviewer measures the pushed tips and records them in the R8 entry of the ledger. Reported in this round's final message.

## Authored-text proofs
2 slices applied, each extracted PROGRAMMATICALLY from the COMMITTED C0a blob by its marker LINES and never retyped: PLANF031R8 → `.agent/plan.md` (byte-equal, G4); GATE7 → `.agent/live_review.md` (one whole-file equality, G5). Disk-to-disk: `.agent/authored/f031-r8.md` equals the pre-C0a scratch original and equals `.agent/last_block.md`, all at sha256 f3b56963…c15728fc over 22462 bytes and 293 lines.

## Deviations & assumptions
The commit sequence C0a, C0b, C1, C2, C3 was followed exactly — no extra commit, none dropped, no reordering. No contradiction was found inside this block; constraint 7 states the append shape once and every gate names that paragraph rather than restating it.
DECLARED 1 — the `push` row of the item-status table records the status the block ORDERS, not a measured outcome: C3 writes this file BEFORE the push by construction (G9), and the block itself rules that the push's outcome has no carrier among this round's files. It is marked `deviated` for exactly that reason.
ASSUMPTION 1 — session scratch for slice extraction and the gate scripts lives directly under `.remedy-wt/` as `slice_PLANF031R8.txt`, `slice_GATE7.txt`, `f031-r8-g7.py`, `f031-r8-g8.py`, `f031-r8-reflog.py` and `f031-r8-suites.py`, all gitignored: `git ls-files .remedy-wt` is 0 (G7). Read as scratch, not as a write to the change set, which bounds tracked paths.
ASSUMPTION 2 — the newline-INCLUDED convention, declared at G4 as the block requires, is the convention used for every slice equality this round.
FINDINGS, with the rule and the commit DECISION F009 D10 requires: by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the open set is 238, measured at 3dbc1ba8. THIS ROUND MINTED NO ID and wrote no `Recurrence:` line (G6). The findings THIS FEATURE MUST STILL ACT ON, a narrower set never called "open", are R-0403, R-0413, R-0431, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679; R-0495 and R-0574 are the two Highs, from F085 and F086.
HANDBACK CAP, derived not quoted: constraint 3 fixes 5 commits, and 5 is NOT more than 5, so the AGENTS.md `### handoff.md` tier is 60 lines. DECISION D15 — Deviations, declared: this file measures 75 lines, over that tier. The mandated content behind the overage is the five per-commit changed-files tables (20 lines), the six-row item-status table (8 lines) and the one-line-per-gate verification block (9 lines), which G1–G9 and the block's Handback section both require. No section was dropped, and NO token cap is claimed — that cap was withdrawn by DECISION F255 D6.

## Next
1. Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
2. NO pull request exists for this branch, and none should be created yet.
3. R9 measures the UI inventory the inbox needs and rules the design gap the plan's Risks names: the canonical design reference carries NO inbox and NO decision component, so T002 has no visual authority until that ruling lands as a DECISION with alternatives and a reversal path.
4. R9's first commit also records the R8 verdict, which by DECISION F085 D9 no artefact of this round can carry.
