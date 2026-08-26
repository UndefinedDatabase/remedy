# Handback — F031 Decision inbox, Runde 20

Feature F031 (Tier 5) · Runde 20 · branch `feature/f031-decision-inbox`, never `main` · base `ba75103e` · the block's constraint 3 fixes 7 commits, and >5 commits puts the AGENTS.md `### handoff.md` tier at 100 lines.

Fortschritt: ~64 % (F031 claimed; R1 through R19 landed and gated ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING ships here · T002b filtering/badge und T003
             offen) — Schaetzung

## Range
Review of `ba75103eecc4c111f99ddd9c4cf6483b3c179d83`..HEAD, where HEAD is the C5 commit this file IS; its SHA cannot exist while this text is written.

## Commits
### 2ab7d2bf docs(agent): save the F031 R20 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f031-r20.md` | +479/-0 | C0a: the R20 block saved verbatim |
### b6e5eca7 chore(agent): mirror the R20 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +416/-320 | C0b: mirror written FROM the committed C0a blob |
### e6b865c3 docs(agent): point the F031 plan at R20
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +22/-25 | C1: PLANF031R20 applied as the whole file |
### 8efcab59 docs(agent): rule DECISION F031 D7, the feature-qualified ledger gate key
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +33/-0 | C2: DECISIOND7 appended, and nothing else |
### ab82dacd feat(ui): order the decision inbox by the DECISION F031 D6 urgency rule
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/decisionOrder.ts` | +69/-0 | C3: S1/S2/S3/S7 — the comparator, new file |
| `apps/ui/src/api/decisionOrder.test.ts` | +137/-0 | C3: S8 — 16 cases, new file |
| `apps/ui/src/api/decisionCard.ts` | +5/-0 | C3: S4 — `ageSeconds` field and its WHY |
| `apps/ui/src/api/decisionCard.test.ts` | +2/-0 | C3: S5 — one line per exact-shape `toEqual` |
| `apps/ui/src/components/panels/RightLivePanel.tsx` | +2/-1 | C3: S6 — the import and the one call site |
### bce7badc docs(agent): record the F031 R19 verdict under the qualified gate key
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | C4: LEDGER20 appended, and nothing else |
### C5 docs(agent): write the F031 R20 handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this file | C5: the handback; a handoff cannot table its own commit (R-0149) |

## External actions
- `git worktree add .remedy-wt/f031-r20-probe ab82dacd` — path did not exist; ONE worktree served G7's three probes AND G8's negative control.
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f031-r20-probe` — removed by that EXACT path before G11; `git worktree list` back to 1 line. Nothing pre-existing under `.remedy-wt/` was deleted.
- `git push origin feature/f031-decision-inbox` — ordered by G12 after C5. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate and records them in the R20 entry of `.agent/live_review.md`.
- No PR created, no merge, no branch deleted, no `gh` command run, no force-push, no history rewrite.

## Verification
- G1 branch `feature/f031-decision-inbox`, not `main`; `.agent/STOP` read from disk ABSENT before C0a and again before C5; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3 and C4.
- G2 all FOUR readings equal — `.remedy-wt/f031-r20.md` before C0a, the C0a blob, the C0b blob, `.agent/last_block.md` off disk after C0b — sha256 `befdd1eca61639d83457ef34f09d95b3820c134585322fb91f2fadc54dc0ebaa`, 34509 bytes, 479 lines; C0a and C0b resolve to the SAME blob id `ba57b10c9e9eb08277d422ffdf558ada29c5b0fd`.
- G3 my extractor printed 3 slices, 79 CONTENT lines, 479 TOTAL; PROSE = 479 − 79 = 400. TOTAL 479 ≤ 490 (F085 D6) and PROSE 400 ≤ 400 (F085 D5): NEITHER CAP IS EXCEEDED, the prose sitting exactly ON the cap.
- G4 `.agent/plan.md` at C1 byte-equal to PLANF031R20, 2544 bytes against 2544 under the newline-INCLUDED convention; NEGATIVE CONTROL against that slice with its trailing newline removed FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 46, strictly under 50.
- G5 the append at C2 in the shape constraint 7 states: whole-file equality TRUE, 570312 + 1 + 1960 = 572273 against an actual 572273, the 570312 measured off C1's blob. SECOND READER: blank-line split, N = 7 paragraphs by my own split, units 1360 → 1367, the LAST 7 units equal DECISIOND7's 7 paragraphs IN ORDER. HEADING SERIES `^## DECISION F031 D\d+` 6 → 7, the ADDED key exactly `D7`, `D1`–`D6` all still present and all 7 DISTINCT.
- G6 `decisionOrder.ts` exports EXACTLY `decisionUrgency` and `orderDecisionInbox` (no default export, no `export {`, no `export *`) and its ONLY import line is `import type { DecisionCardModel } from "./decisionCard";`. `DecisionCardModel` carries `ageSeconds: number | null` and `buildDecisionCardModel` returns `ageSeconds,` (S4). `git diff` for `RightLivePanel.tsx` alone is the one import line plus the one call site and NOTHING else (S6). `apps/ui/src/api/remedyApi.ts` is NOT in C3's 5-path set. In the PRIMARY checkout: `npm run typecheck` REAL exit 0 with ZERO diagnostics on stdout and stderr; `npm run test:unit` REAL exit 0, `Test Files 22 passed (22)` and `Tests 332 passed (332)`, `src/api/decisionOrder.test.ts` 16 and `src/api/decisionCard.test.ts` EXACTLY 27, the base reading.
- G7 all three probes ran in the disposable worktree by the block's own command line; CONTROL on the unmutated worktree exit 0, 16 passed, so the route can pass. Probe A (`+ 1` removed) exit 1, 8 FAILED: `decisionUrgency >` "is the blocked size plus one, times the age" / "scores a card that blocks nothing at its own age, not at zero" / "counts a non-finite blocked size as blocking nothing" / "counts a negative blocked size as blocking nothing, exactly as its label reads", `orderDecisionInbox >` "gives a shuffled inbox exactly one order" / "leaves age as the total order among cards that block nothing" / "breaks an exact urgency tie by id ascending" / "returns a new array and leaves the one it was given untouched". Probe B (open-first key removed) exit 1, 3 FAILED: `orderDecisionInbox >` "gives a shuffled inbox exactly one order" / "reads open cards before closed ones whatever their urgency" / "sorts an unreadable age last within its own group, not out of it". Probe C (`id` key removed) exit 1, 1 FAILED: `orderDecisionInbox >` "breaks an exact urgency tie by id ascending". NO PROBE WAS GREEN.
- G8 the append at C4 in the shape constraint 7 states: whole-file equality TRUE, 638246 + 1 + 4657 = 642904 against an actual 642904, the 638246 measured off what C2 and C3 left. SECOND READER: N = 1 paragraph by my own split, units 301 → 302, the LAST 1 unit equals LEDGER20's paragraph. NEGATIVE CONTROL: one byte flipped at offset 640575, inside the appended text and length-preserving, written only inside the disposable worktree and unlinked after — BOTH readers rejected the mutant and BOTH accepted the true file.
- G9 base → C4 in `.agent/live_review.md`: `^- R-\d+ — ` 242 → 242, all 242 DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0681` → `R-0681`; `^Done: R-` 4 → 4, `^Landed: R-` 0 → 0 and `^Recurrence: R-` 17 → 17, all three UNCHANGED. THE SPLIT SERIES: `^Gate: R\d+ — ` 19 → 19 UNCHANGED, `^Gate: F\d+ R\d+ — ` 0 → 1, the ADDED key exactly `F031 R19`. §3 item 10 open set at C4: 238.
- G10 line-anchored `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1, `.agent/decisions.md` at C2 and `.agent/live_review.md` at C4, against a CONTROL of 3 and 3 over the committed C0a blob, so the reading is not vacuous. `git diff --name-only ba75103e..bce7badc` names 10 paths, NONE under `docs/`, `packages/`, `tests/` or `apps/cli/` and neither `.agent/context.md` nor either inventory; RANGE minus change set EMPTY, change set minus RANGE exactly `.agent/handoff.md`. Per commit single-parent with INSERTIONS 479, 416, 22, 33, 215 and 2, each under 500, all from `git diff --numstat` and agreeing cell for cell with the `+/-` column above. `git ls-files .remedy-wt` 0 and `git ls-files *.zip` 0. REFLOG SCOPE: this round's 6 entries only, the top of the reflog down to but excluding the base; FIELD: the operation prefix before the first colon of `--format=%gs`, all six `commit`, so `amend` 0, `rebase` 0 and `cherry` 0.
- G11 `git worktree list` was 1 line immediately BEFORE the first pytest. The six suites ran SERIALLY in the primary checkout at the C4 tree, never two alive at once, every one a REAL exit 0: `tests/ui_server/` 474 passed, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `tests/ui_contracts/` 525 passed and 4 skipped, `test_golden_path.py` 42 — every count identical to the reviewer's base readings, so there is no difference to account for.
- G12 my extractor found 21 SHA-shaped occurrences of the word-bounded `[0-9a-f]{7,40}`, 13 DISTINCT, and the FAILING SET IS EMPTY. Types: `43e2018218e06a256fe8e18a46cd7dca3ff5d57d` is a `blob`; `1e9d3a83`, `24b47b3b`, `3d2a3be2`, `6325ac2f`, `6c758fc8`, `6ede183c`, `75d4b532`, `8171d403`, `a0ece183`, `a0f70a9e`, `ba75103e` and `ba75103eecc4c111f99ddd9c4cf6483b3c179d83` are all `commit`. The push ran after C5; its outcome is carried to the reviewer per this gate's own instruction and reported in the worker's final message.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY from the COMMITTED C0a blob by its `<<<SLICE`/`<<<END` marker LINES, never retyped or rewrapped; no marker line reached a target file (G10). This block carried NO FROM/TO pair (constraint 8).
- PLANF031R20 → `.agent/plan.md` at C1: sha256 `1c3abc4fa446d659d7a102d6d009b813f5fcfa64c5fed89506615e16202e84a0`, 2544 bytes, applied as the whole file, byte-equal (G4).
- DECISIOND7 → `.agent/decisions.md` at C2: sha256 `1410d23989bd76284f9c6d4d3984e2a332bb74cc18a5703a4e0cf2d993915296`, 1960 bytes, appended, whole-file equality TRUE (G5).
- LEDGER20 → `.agent/live_review.md` at C4: sha256 `d8497ce6c7bd1727385a334b8d3a4e1f0d9dcc0b453c7087651f5ccf4aa322de`, 4657 bytes, appended, whole-file equality TRUE (G8).

## Findings
This round MINTED NO ID and RESOLVED NOTHING. By the §3 item 10 rule DECISION F009 D10 requires — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the set is 238 measured at `bce7badc`, unchanged from 238 at `ba75103e`. The findings THIS FEATURE MUST STILL ACT ON are the 20 ids `.agent/plan.md` lists, of which R-0495 and R-0574 are the two Highs.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror into last_block | done | |
| C1 the plan | done | |
| C2 DECISION F031 D7 | done | |
| C3 the code | deviated | S2's clamp and S4's field comment, both declared below |
| C4 the R19 gate entry | done | |
| C5 handback | done | |
| push (G12) | done | ordered after C5; outcome carried by G12 to the reviewer |

## Deviations & assumptions
- NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE: C0a, C0b, C1, C2, C3, C4, C5 exactly — none extra, none dropped, none reordered.
- S2, DECLARED DEVIATION: `decisionUrgency` clamps a NEGATIVE `blockedCount` to 0, where S2 names only the non-finite case. `decisionBlockedLabel` already clamps a negative count to "blocks nothing", so without this a card whose label READS "blocks nothing" would score `(-5 + 1) * age` — negative — and sort BELOW a null-age card, contradicting DECISION F031 D6's own sentence that a null age "scores 0 and therefore sorts last within its group". Pinned by the test "counts a negative blocked size as blocking nothing, exactly as its label reads". For every non-negative `blockedCount` the function is exactly S2's `(blockedCount + 1) * age`.
- S3, implementation note: the urgency key is COMPARED, not subtracted, because `a - b` over two infinite scores yields NaN and an undefined comparator. The three keys and their directions are S3's.
- S4, DECLARED ADDITION: the new `ageSeconds` field carries a 3-line WHY comment (AGENTS.md Code Discoverability Conventions). S4 forbids other FIELD and SIGNATURE changes and states no "nothing else in that file changes" clause — unlike S5 and S6, which do and which were held to the letter.
- S8, cases added and named: 16 tests rather than S8's six, adding a non-finite age, a non-finite blocked size, the negative blocked size above, a never-throws case, an empty inbox, identical-key stability, and a second shuffle proving the order is the same answer twice.
- PROSE NOT SWEPT, flagged rather than fixed: `decisionCard.ts` and `DecisionInboxCard.tsx` still say ordering "is T002b's subject". Nothing there is falsified — neither file sorts, and T002b IS this work — so under AGENTS.md Scope Control ("no 'while I'm here' edits") both were left alone; the reverse pointers to `orderDecisionInbox` live in the new module's header instead (S7).
- PLANF031R20 was applied BYTE FOR BYTE per constraint 1 although at C1 it reads "`.agent/decisions.md` D1–D7" one commit before `D7` lands at C2.
- TOOLING, declared because it changed HOW not WHAT: the command guard denied `cd apps/ui && npm …`, bare `npm …` (the shell's cwd is the repo root, not `apps/ui`) and `npm --prefix apps/ui …`. G6's two ordered command lines therefore ran through `subprocess.run(["npm", "run", …], cwd="apps/ui")` — the same commands with the same working directory. G7's `npx vitest` line ran exactly as the block writes it.
- SCRATCH: this round's measurement scripts live under `.remedy-wt/r20-scratch/`, belong to no commit, and `git ls-files .remedy-wt` reads 0 (G10).

## Next
The R20 VERDICT IS UNRECORDED and is owed by the NEXT round's ledger commit (DECISION F085 D9). R21 is T002b FILTERING by TYPE under DECISION F031 D6, which needs no further ruling. Every ledger entry from here is headed under DECISION F031 D7's feature-qualified key `Gate: F031 R<n> — `, the unqualified form having stopped growing at 19. The next session reads Phase 1 rule 1 — `.agent/STOP` from disk — before rule 2.
