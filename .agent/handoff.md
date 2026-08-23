# Handback — F031 Decision inbox, R5 (record R4, register R-0678, rule D1/D2/D3)

Branch: `feature/f031-decision-inbox` (never `main`). Base: `f4311bf6`, the R4 handback commit.

Fortschritt: ~4 % (F031 claimed; R1 through R4 landed and gated · the
             source inventory is on disk · R5 rules the three design
             questions · no T-slice started) — Schaetzung

Handback line cap, derived rather than quoted: constraint 3 fixes SEVEN commits (C0a, C0b, C1, C2, C3, C4, C5); seven is more than five, so the AGENTS.md `### handoff.md` tier that follows is ≤100 lines. No token cap is claimed: DECISION F255 D6 withdrew it.

## Range
Review of `f4311bf6`..`a8ec4e07` plus C5, the commit that writes this file — a commit cannot name its own SHA, so C5's id is in the round message (G13's counter-measure applied to self-reference).

## Commits
### af048031 docs(state): save the F031 R5 record and ruling block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r5.md | +488/-0 | C0a — the R5 block saved verbatim from `.remedy-wt/f031-r5.md` |
### d97c1d18 docs(state): mirror the F031 R5 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +358/-161 | C0b — mirror of the committed C0a blob, same blob id |
### cefcbbb4 docs(state): advance the plan to the F031 R5 ruling round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +27/-28 | C1 — slice PLANF031R5, whole-file |
### f05d00c5 docs(review): record the F031 R4 PASS and register finding R-0678
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2 — appended GATE4 then FIND678, in that order |
### b97e823e docs(decisions): rule the three F031 design questions as D1 D2 and D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +121/-0 | C3 — appended slice DEC031 |
### a8ec4e07 docs(roadmap): append the F031 design amendments for D1 D2 and D3
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T5_F031.md | +31/-0 | C4 — appended slice FEATAMEND |
### C5 docs(state): hand back the F031 R5 ruling round
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5 — this file; the R-0149 self-reference exception applies |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| the push (G13) | deviated | outcome deliberately withheld from disk by G13's own order; command and result go to the reviewer in the round message only |

## External actions
- `git worktree add --detach .remedy-wt/f031r5-neg f05d00c5` — created for the G5 negative control only.
- `git worktree remove --force .remedy-wt/f031r5-neg` — removed BY ITS EXACT PATH before the G12 suites; `git worktree list` back to 1 line. `.remedy-wt/dry` was not touched.
- `git push origin feature/f031-decision-inbox` — run after C5. Its OUTCOME is not recorded here, by G13.
- No pull request created, nothing merged, no `gh` command run, no amend/rebase/cherry-pick/force-push/branch deletion.

## Verification
G1 PASS — `git branch --show-current` printed `feature/f031-decision-inbox`, not `main`; `.agent/STOP` read from disk was ABSENT before C0a and again before C5; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3 and C4.
G2 PASS — all FOUR readings equal: sha256 `be41960e388ce8d3838aa44164dae902ce103d8b1b60188f02db28d64c763154`, 35476 bytes, 488 lines, for `.remedy-wt/f031-r5.md` before C0a, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk after C0b; C0a's and C0b's file are the SAME git blob `30bc5a779c1ab1dcaf201e7a5b07cbdbf1dc4df0`.
G3 PASS — my extractor over the COMMITTED C0a blob printed: 5 slices (PLANF031R5, GATE4, FIND678, DEC031, FEATAMEND), 200 CONTENT lines inside markers, 488 TOTAL lines.
G4 PASS — `.agent/plan.md` at `cefcbbb4` is byte-equal to PLANF031R5 under the newline-INCLUDED convention (every content line, last one included, ends in exactly one newline): slice 2816 bytes, file 2816 bytes. NEGATIVE CONTROL: equality against the slice with its trailing newline REMOVED is FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48, strictly under 50.
G5 PASS — at `f05d00c5` reader A: the base blob is a byte-exact PREFIX, 539793 → 546250 bytes, delta 6457 = 1 + 3974 (GATE4) + 1 + 2481 (FIND678), the two regions byte-equal at offsets 539794 and 543769. Reader B (independent, blank-line split): 277 → 279 units, the LAST TWO equal GATE4 then FIND678 IN ORDER. NEGATIVE CONTROL: one byte flipped at offset 539834, inside the FIRST appended paragraph, written to disk in the disposable worktree — BOTH readers rejected the mutant and BOTH accepted the true file.
G6 PASS — `.agent/live_review.md`, `f4311bf6` → `f05d00c5`: `^- R-\d+ — ` 238 → 239, all DISTINCT; ids ADDED exactly the one id `R-0678`; ids REMOVED the EMPTY SET; maximum `R-0677` → `R-0678`; `^Done: R-` 2 → 2; `^Recurrence: R-` 14 → 14 UNCHANGED; `^Gate: R\d+ — ` 4 → 5, gaining exactly the key `R4`, with `R19`, `R1`, `R2` and `R3` still present.
G7 PASS — `.agent/decisions.md` at `b97e823e`: base blob a byte-exact PREFIX, 552938 → 560571 bytes, delta 7633 = 1 + 7632 (DEC031), the appended region byte-equal to DEC031 at offset 552939. `^## DECISION F031 D` 0 at the base and 3 at C3; `^## DECISION F031 D1 `, `^## DECISION F031 D2 ` and `^## DECISION F031 D3 ` each exactly 1x at C3.
G8 PASS — `docs/roadmap/features/T5_F031.md` at `a8ec4e07`: base blob a byte-exact PREFIX, 4773 → 6705 bytes, delta 1932 = 1 + 1931 (FEATAMEND), the appended region byte-equal at offset 4774. `^## Design amendments ` 0 at the base and 1 at C4.
G9 PASS — `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, `.agent/decisions.md` at C3 and `docs/roadmap/features/T5_F031.md` at C4. `git diff --name-only f4311bf6..a8ec4e07` names 6 paths, NONE under `packages/`, `apps/` or `tests/`, NOT `README.md`, NEITHER `docs/roadmap/ROADMAP.md` NOR `docs/roadmap/STATUS.md`, and NOT `.agent/f031_inventory.md`.
G10 PASS — C0a..C4 each single-parent; INSERTIONS (the `+` column only, AGENTS.md DECISION F104 D1) 488, 358, 27, 4, 121 and 31, each under 500. Range path set MINUS the change set is EMPTY; change set MINUS the range is exactly `.agent/handoff.md`, which C5 writes. `git ls-files .remedy-wt` 0, `git ls-files *.zip` 0, `git worktree list` 1 line. REFLOG, scope and field stated in the reading: over THIS ROUND'S OWN 6 entries (C0a..C4 is six commits), read by the OPERATION PREFIX before the first colon of `git reflog --format=%gs`, every prefix is `commit`, so amend 0, rebase 0, cherry 0.
G11 PASS — word-bounded `[0-9a-f]{7,40}` over the COMMITTED C0a blob: 23 occurrences, 11 DISTINCT tokens. The set that FAILS `git cat-file -t` is exactly the one id `f26c5da5e5b60e8b7a3b2ba1a4b1a0e5c0ff5a0d` (exit 128, "could not get object info"), which FIND678 QUOTES — the gate's positive control, so the pattern demonstrably matched. Every other token exited 0: `302388e9` blob; `1d91b6d9`, `3ff12773`, `6325ac2f`, `9808ecbd`, `ef3653fe`, `f26c5da5`, `f26c5da5e5b6563b1b4fd8e71946344e8c3f6fac`, `f4311bf6`, `f4311bf6e711c6a1cc6ff17c3e14a6bb53803222` all commit.
G12 PASS — `git worktree list` 1 line immediately BEFORE the first pytest; seven suites run SERIALLY in the primary checkout at the C4 tree, never two pytest processes alive; every one REAL exit code 0 at 470, 52, 21, 16, 42, 295 and 30 passed. The first five reproduce the reviewer's 470, 52, 21, 16 and 42 cell for cell; the last two sum to 295 + 30 = 325, the reviewer's combined 325. No difference to account for.
G13 — `git push origin feature/f031-decision-inbox` runs AFTER C5, with no `--force`, no `--force-with-lease`, no history rewrite, no branch deletion and no pull request. Its OUTCOME is reported to the reviewer in the round message and is deliberately NOT a value of this or any file this round writes.

## Authored-text proofs
Five reviewer-authored slices applied, each extracted PROGRAMMATICALLY from the committed C0a blob `.agent/authored/f031-r5.md` by its marker LINES and applied BYTE FOR BYTE; no marker line reached any target file (G9). PLANF031R5 2816 bytes → `.agent/plan.md` at C1 (whole file, byte-equal). GATE4 3974 bytes and FIND678 2481 bytes → appended to `.agent/live_review.md` at C2, regions byte-equal (G5). DEC031 7632 bytes → appended to `.agent/decisions.md` at C3 (G7). FEATAMEND 1931 bytes → appended to `docs/roadmap/features/T5_F031.md` at C4 (G8).
Disk-to-disk: `.remedy-wt/f031-r5.md`, the committed `.agent/authored/f031-r5.md` blob, the committed `.agent/last_block.md` blob and `.agent/last_block.md` off disk are all one sha256 over 35476 bytes (G2).

## Deviations & assumptions
- Commit sequence: exactly C0a, C0b, C1, C2, C3, C4, C5 as constraint 3 orders — no extra commit, none dropped, no reordering. The push ran after C5.
- CONTRADICTION DECLARED, reconciled by neither side. `docs/agents/handback_template.md` requires "External actions" to carry every push as "command + outcome", while G13 of this block forbids the push's outcome from being a value of any file this round writes. This file therefore carries the push COMMAND and withholds its RESULT, and the item-status row for the push is marked `deviated` for that reason rather than for a failure. Both texts are followed as far as they can be simultaneously; nothing is invented to close the gap.
- ASSUMPTION, stated because the block does not fix it: "newline-INCLUDED" is read as every content line of a slice, the last one included, ending in exactly one newline, so each appended region ends the file in exactly one newline (constraint 7). Every append arithmetic above is computed under that reading and the G4 negative control tests it directly.
- ASSUMPTION: G5's "split the C2 file on blank lines" is implemented as a split on a newline, optional horizontal whitespace, and a newline, over the file with its single trailing newline removed. The base and C2 unit counts (277 and 279) are produced by that one reader applied to both.
- The G5 mutant lived only in the disposable worktree `.remedy-wt/f031r5-neg`, created at C2 and removed by its exact path before the G12 suites. The pre-existing `.remedy-wt/dry` was not touched. My own scratch scripts live under `.remedy-wt/`, which is gitignored — `git ls-files .remedy-wt` is 0.
- No disagreement with any slice: all five applied verbatim and none looked wrong.
- Findings, each with its rule and the commit it was measured at, per DECISION F009 D10: by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the open set is 237, measured at `f05d00c5`. It was 236 at `f4311bf6`; the single mover is `R-0678`, minted this round (constraint 8).
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it is and never called "open" unqualified — are R-0403, R-0413, R-0431, R-0445, R-0495, R-0533, R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677 and R-0678, of which R-0495 and R-0574 are the two Highs, inherited from F085 and F086.

## Next
1. Phase 1 rule 1: re-read `.agent/STOP` from disk before doing anything.
2. NO pull request exists for `feature/f031-decision-inbox`, and none should be created yet.
3. R6 records the R5 verdict — which by DECISION F085 D9 no artefact of THIS round can carry — and plans T001 against DECISION F031 D1, D2 and D3: the read endpoint over `list_decisions`, the blocked-size wiring from `blocked_downstream`, and a fixture per PRODUCING type.
