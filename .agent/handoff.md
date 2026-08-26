# Handback — F031 Decision inbox, Runde 19

Feature F031 (Tier 5) · Runde 19 · branch `feature/f031-decision-inbox` · base `6c758fc8` · the block's constraint 3 fixes 6 commits, and >5 commits puts the AGENTS.md `### handoff.md` tier at 100 lines.

Fortschritt: ~59 % (F031 claimed; R1 through R18 landed and gated ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             R-0681 resolved here · T002b ordering/filtering/badge
             und T003 offen) — Schaetzung

## Range
Review of `6c758fc8`..HEAD, where HEAD is the C4 commit this file IS; its SHA cannot exist while this text is written.

## Commits
### 8171d403 chore(agent): save the F031 R19 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f031-r19.md` | +383/-0 | C0a: the R19 block saved verbatim |
### a0f70a9e chore(agent): mirror the R19 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +263/-356 | C0b: mirror written FROM the committed C0a blob |
### 3d2a3be2 docs(agent): point the F031 plan at R19
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +27/-27 | C1: PLANF031R19 applied as the whole file |
### a0ece183 docs(agent): resolve R-0681 with the authored Done text
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +1/-1 | C2: LANDEDFROM replaced in place by DONE0681, and nothing else |
### 1e9d3a83 docs(agent): record the F031 R18 verdict and the R-0385 recurrence
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | C3: LEDGER19 appended, and nothing else |
### C4 docs(agent): write the F031 R19 handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this file | C4: the handback; a handoff cannot table its own commit (R-0149) |

## External actions
- `git worktree add --detach .remedy-wt/f031-r19-neg HEAD` — created for the G6 negative control only.
- `git worktree remove --force .remedy-wt/f031-r19-neg` — removed by that exact path; `git worktree list` back to 1 line.
- `git push origin feature/f031-decision-inbox` — ordered by G10 after C4. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate and records them in the R19 entry of `.agent/live_review.md`.
- No PR created, no merge, no branch deleted, no `gh` command run.

## Verification
- G1 branch `feature/f031-decision-inbox`, not `main`; `.agent/STOP` read from disk ABSENT before C0a and again before C4; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2 and C3.
- G2 all FOUR readings equal — scratchpad, C0a blob, C0b blob, `.agent/last_block.md` off disk — sha256 `922693ee69434f9e53449492ea94e790074a5c0f5be7b8f193fbca7b350ee54c`, 32110 bytes, 383 lines; C0a and C0b resolve to the SAME blob id `43e2018218e06a256fe8e18a46cd7dca3ff5d57d`.
- G3 my extractor printed 4 slices, 54 CONTENT lines, 383 TOTAL; PROSE = 383 − 54 = 329 (321 with the 8 marker lines excluded). TOTAL 383 ≤ 490 and PROSE 329 ≤ 400: NEITHER CAP IS EXCEEDED.
- G4 `.agent/plan.md` at C1 byte-equal to PLANF031R19, 3004 bytes against 3004, under the newline-INCLUDED convention; NEGATIVE CONTROL against the slice with its trailing newline removed FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49, strictly under 50.
- G5 the pair in the REWRITE shape constraint 8 measured: LANDEDFROM 1 before C2, 0 after; DONE0681 1 after. `git diff --numstat` for C2 names `.agent/live_review.md` alone at 1/1. Bytes 629198 → 631576, moving exactly +2378 = DONE0681's 2751 minus LANDEDFROM's 373, both taken from the extracted slices.
- G6 the append at C3 in the shape constraint 7 states: whole-file equality TRUE, 631576 + 1 + 6669 = 638246 against an actual 638246, the 631576 measured off what C2 left. SECOND READER: blank-line split, N = 2 paragraphs measured by my own split, units 299 → 301, and the LAST 2 units equal LEDGER19's 2 paragraphs IN ORDER. NEGATIVE CONTROL: one byte flipped at offset 631677, inside the FIRST added paragraph, `A` → `B`, written only inside the disposable worktree — BOTH readers rejected the mutant and BOTH accepted the true file.
- G7 base → C3 in `.agent/live_review.md`: `^- R-\d+ — ` 242 → 242, all 242 DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0681` → `R-0681`. `^Landed: R-` 1 → 0; `^Done: R-` 3 → 4, the ADDED id exactly `R-0681`. `^Recurrence: R-` 16 → 17, gaining exactly `R-0385`. `^Gate: R\d+ — ` 18 → 19, gaining exactly the key `R18`, `R19` and `R1`–`R17` all still present and all 19 DISTINCT. Open set at C3: 238.
- G8 line-anchored `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1 and in `.agent/live_review.md` at C3, against a CONTROL of 4 and 4 over the committed C0a blob, so the reading is not vacuous. `git diff --name-only 6c758fc8..C3` names 4 paths, NONE under `packages/`, `apps/`, `tests/` or `docs/` and none of `.agent/decisions.md`, `.agent/context.md` or either inventory; RANGE minus change set EMPTY, change set minus RANGE exactly `.agent/handoff.md`. Per commit single-parent with INSERTIONS 383, 263, 27, 1 and 4, each under 500, all from `git diff --numstat` and agreeing cell for cell with the `+/-` column above. `git ls-files .remedy-wt` 0 and `git ls-files "*.zip"` 0. REFLOG SCOPE: this round's 5 entries only, HEAD@{0}..HEAD@{4}, the base sitting at HEAD@{5}; FIELD: the operation prefix before the first colon of `%gs`, all five `commit`, so `amend` 0, `rebase` 0 and `cherry` 0. In the PRIMARY checkout `npm run typecheck` REAL exit 0 with ZERO diagnostics on stdout and stderr, and `npm run test:unit` REAL exit 0 at 21 files and 316 tests, both UNCHANGED from the base.
- G9 my extractor found 24 SHA-shaped occurrences, 11 DISTINCT, and the FAILING SET IS EMPTY. Types: `c732ebf49afd964f5d2ccdc19a4f6da0482c548f` is a `blob`; `24b47b3b`, `48124293`, `6325ac2f`, `6c758fc8`, `6c758fc84316cacc0162fb6fdf290b8d3034fe09`, `6ede183c`, `7107a563`, `75d4b532`, `8e4e55d6` and `a0565593` are all `commit`. `git worktree list` was 1 line immediately before the first pytest. The five suites ran SERIALLY in the primary checkout, never two alive at once, every one a REAL exit 0: `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `test_golden_path` 42 — identical to the reviewer's base readings, so there is no difference to account for.
- G10 `git push origin feature/f031-decision-inbox` run after C4; outcome carried to the reviewer per this gate's own instruction, and reported in the worker's final message.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY from the COMMITTED C0a blob by its `<<<SLICE`/`<<<END` marker lines, never retyped; that blob is `cmp`-equal to `.remedy-wt/f031-r19.md` (exit 0) and to `.agent/last_block.md`.
- PLANF031R19 → `.agent/plan.md` at C1: byte-equal, 3004 = 3004 (G4).
- LANDEDFROM → DONE0681 in `.agent/live_review.md` at C2: applied as a REWRITE in place, FROM 0 and TO 1 after the commit (G5).
- LEDGER19 → `.agent/live_review.md` at C3: parent blob + one newline + slice, whole-file equality TRUE under two independent readers (G6).

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror into last_block | done | |
| C1 the plan | done | |
| C2 the R-0681 resolution | done | |
| C3 the R18 gate entry and the R-0385 recurrence | done | |
| C4 handback | done | this file |
| the push (G10) | done | ordered after C4; outcome carried by G10 to the reviewer |

## Finding counts
Per §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the open set is 238, measured at C3 `1e9d3a83`, down from 239 at the base `6c758fc8`; R-0681 is the one that left, and this round MINTED NO ID. The narrower set the plan names as "the findings this feature must still act on" is 20 distinct ids at that same commit, R-0495 and R-0574 being the two Highs.

## Deviations & assumptions
NO DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE: C0a, C0b, C1, C2, C3, C4 were committed in that order, none extra, none dropped, none reordered.
- The command guard rejected two MEASUREMENT-ONLY shell forms — one using `$?` after `npm run typecheck`, one a python heredoc carrying a brace-with-quote set literal. Each was re-run in an accepted form (a `subprocess` call with `cwd` set to `apps/ui`, and `set()` built by `.add`); no committed byte is affected and no gate went unrun.
- Scratch created by me and removed BY EXACT PATH: the worktree `.remedy-wt/f031-r19-neg` and one build script under `.remedy-wt/`. One stray `.agent/.fort.tmp` was written by mistake and deleted by exact path before any commit; `git status --porcelain` was 0 after every commit. Nothing pre-existing under `.remedy-wt/` was touched.
- NO CONTRADICTION FOUND IN THE BLOCK. Every gate was met as written, and every value above is one I measured myself.

## Next
1. THE R19 VERDICT IS UNRECORDED and is owed by the NEXT round's ledger commit, which by DECISION F085 D9 no artefact of R19 can carry.
2. R20 is the T002b ORDERING round under DECISION F031 D6, which is already on disk at `24b47b3b` and mirrored at `75d4b532`, so it needs no further ruling.
3. R20's ledger entry is the FIRST that would collide with the inherited `Gate: R19` seed key, so R20's block must rule the feature-qualified key BEFORE writing it.
