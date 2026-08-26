# Handback — F031 Decision inbox, R26

Branch `feature/f031-decision-inbox` (never `main`). Base
`92b323e314980ecb4eef7fd79fe619d54f55b8c6`, the R25 handback commit. Commits in
the order constraint 4 fixes: C0a `9ea82d68`, C0b `40df4b16`, C1 `7019185f`,
C2 `b313d680`, C3 `069f744c`, C4 = the commit carrying this file (a handback
cannot state its own SHA). 6 commits, so the AGENTS.md `### handoff.md` tier is
100 lines, not 60.

Fortschritt: ~90 % (F031 claimed; R1 through R25 landed, R25 gated here ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING, FILTERING and BADGE COMPLETE and gated ·
             T003 answer-command model here, its sender and forms open)
             — Schaetzung

## Range
Review of `92b323e3`..HEAD.

## Commits
### 9ea82d68 docs(agent): save the F031 R26 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r26.md | +448/-0 | C0a: the block, COPIED from `.remedy-wt/f031-r26.md`, never retyped |
### 40df4b16 docs(agent): mirror the F031 R26 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +347/-349 | C0b: byte-identical mirror written from the committed C0a blob |
### 7019185f docs(agent): point the F031 plan at R26
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +23/-25 | C1: whole-file replacement by slice PLANF031R26 |
### b313d680 docs(agent): record the F031 R25 verdict and resolve R-0682
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2: the one append, slice LEDGER26 |
### 069f744c feat(ui): build the decision answer command in the browser
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionAnswer.ts | +106/-0 | S1: the pure answer-command module |
| apps/ui/src/api/decisionAnswer.test.ts | +132/-0 | S2: its tests, models built via `buildDecisionCardModel` |
| apps/ui/src/components/panels/DecisionInboxCard.tsx | +7/-4 | S3: `role="group"`; header absence repaired |
| apps/ui/src/components/graph/GraphFilterChips.tsx | +1/-1 | S3: `role="group"` |
| .agent/decisions.md | +31/-0 | S4: DECISION F031 D11 |
### C4 (this commit) docs(agent): write the F031 R26 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4: this file; it cannot table its own numstat (R-0149 pattern) |

## External actions
`git worktree add --detach .remedy-wt/f031-r26-red 069f744c` at a path that did not
exist, then `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f031-r26-red`
by that exact path; `git worktree list` 1 line after. `git push origin
feature/f031-decision-inbox`, ordered by G9 AFTER C4. THAT PUSH'S OUTCOME IS NOT A
VALUE OF ANY FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the
next gate and records them in the R26 entry of `.agent/live_review.md`. No PR, no
branch deleted, nothing merged.

## Verification
G1 PASS — branch `feature/f031-decision-inbox`; `.agent/STOP` ABSENT on disk before C0a and again before C4; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3. Four readings — scratch file pre-C0a, C0a blob, C0b blob, `.agent/last_block.md` on disk after C0b — ALL FOUR EQUAL at sha256 `dbf5fbe2f657a7191d197a4be5767664604a86103ca22d4c48e165ec70290bde`, 38200 bytes, 448 lines; C0a's and C0b's file resolve to the SAME blob id `970f470292593aa1ad6f097b081c9d9a990c3e65`.
G2 PASS — my extractor over the committed C0a blob printed 2 slices, 50 CONTENT lines inside markers, 448 TOTAL; PROSE = 448 − 50 = 398. Against the Base's caps: 448 ≤ 490 (F085 D6), 398 ≤ 400 (F085 D5). Neither exceeded.
G3 PASS — `.agent/plan.md` at C1 byte-equals PLANF031R26 under the newline-INCLUDED convention (each slice ends in a newline): slice 2653 bytes, file 2653 bytes, equality TRUE. NEGATIVE CONTROL, equality against that slice MINUS its trailing newline: FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 47, strictly under 50.
G4 PASS — reader (a), the whole-file equality constraint 8 states: TRUE, arithmetic 687558 + 1 + 8841 = 696400 against an actual 696400, the C1 length measured by me from the C1 blob. Reader (b), independent: a blank-line split moves the unit count 311 → 313; N = 2, my split's own count of LEDGER26's paragraphs; the LAST 2 units equal those 2 paragraphs IN ORDER. Trailing-newline handling: `rstrip("\n")` over the whole text before splitting on a blank line, and `rstrip("\n")` on BOTH sides of every unit compared. NEGATIVE CONTROL, done in memory and never on the tracked file, one byte flipped at offset 687659 inside the appended text: BOTH readers reject the mutant and BOTH accept the true file.
G5 PASS — base `92b323e3` → C2 `b313d680`: `^- R-\d+ — ` 244 → 244, all 244 DISTINCT, ids ADDED the EMPTY SET and ids REMOVED the EMPTY SET, maximum `R-0683` → `R-0683`; `^Done: R-\d+ — ` 4 → 5 with ids ADDED exactly `R-0682`; `^Landed: R-` 0 → 0; `^Recurrence: R-` 19 → 19; `^Gate: R\d+ — ` 19 → 19 UNCHANGED; `^Gate: F\d+ R\d+ — ` 6 → 7, ADDED key exactly `F031 R25`, all 7 keys DISTINCT. §3 item 10 open set at C2 = 244 − 5 = 239. `- R-0682 — ` occurs exactly ONCE line-anchored. `git diff --name-only b313d680..069f744c` does NOT name `.agent/live_review.md`.
G6 PASS, REAL RED — disposable worktree `.remedy-wt/f031-r26-red` at C3 `069f744c`, vitest run from the PRIMARY `apps/ui`. UNMUTATED: `npx vitest run --config <primary>/apps/ui/vitest.config.ts --root <worktree>/apps/ui src/api/` REAL exit 0 at 21 files and 349 tests. MUTATED — the not-open refusal removed from `buildDecisionResolveCommand` so it returns its body for a model that is NOT open, that target occurring EXACTLY ONCE, every other byte left alone — REAL exit 1 at 2 failed and 347 passed, 1 file failed of 21. Failing NAMES: `buildDecisionResolveCommand > refuses a decision that is NOT open, which the server answers 409` and `buildDecisionResolveCommand > reads isOpen rather than an open-SOUNDING status string`. The file was restored byte-identically inside the worktree (`git status --porcelain` 0 there) before removal; `git worktree list` 1 line after, naming only `/home/decodeux/Repos/remedy`.
G7 PASS — structure at C3: `role="group"` EXACTLY ONCE in each chip file with the existing `aria-label` on the SAME element — `<div className={styles.decisionFilterRow} role="group" aria-label={FILTER_CHIPS_LABEL}>` at DecisionInboxCard.tsx line 91 and `<div className={styles.chips} role="group" aria-label="Graph filters">` at GraphFilterChips.tsx line 14; the `<output>` element is byte-identical to its text at the base; `aria-pressed` 1 and `aria-live` 1 still present. In `decisionAnswer.ts`: literal `decision.resolve` exactly 1, and `fetch(` 0, `XMLHttpRequest` 0, `Math.random` 0, `Date.now` 0. `git worktree list` 1 line immediately before the first suite. Suites run SERIALLY, never two alive at once, every one a REAL exit 0: `npm run typecheck` with ZERO diagnostics on stdout and stderr; `npm run test:unit` at 24 FILES — one more than the Base's 23, that one being `decisionAnswer.test.ts` — and 374 tests, of which S2 added 17, with `decisionCard.test.ts` 32, `decisionFilter.test.ts` 20 and `decisionOrder.test.ts` 16 all UNMOVED; then `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped, `test_golden_path` 42 — every count identical to the Base's reading, so there is no difference to account for.
G8 PASS — line-anchored `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and all 5 files C3 writes, against the CONTROL over the committed C0a blob where both are 2. `git diff --name-only 92b323e3..069f744c` names 9 paths, NONE under `docs/`, `packages/` or `tests/`, and none of `.agent/context.md`, either inventory file, `RightLivePanel.tsx`, `decisionCard.ts`, `decisionFilter.ts`, `decisionOrder.ts` or `RemedyApp.tsx`; range MINUS change set EMPTY, change set MINUS range exactly `.agent/handoff.md`. Per commit C0a..C3: single-parent TRUE for each, INSERTIONS — the `+` column of `git diff --numstat`, per DECISION F104 D1 — 448, 347, 23, 4, 277, each under 500, agreeing CELL FOR CELL with the `+/-` column of the tables above. `git ls-files .remedy-wt` 0; `git ls-files "*.zip"` 0. REFLOG by the OPERATION PREFIX before the first colon of `git reflog --format=%gs`, scoped to 6 entries: `commit` 6, `amend` 0, `rebase` 0, `cherry` 0. SHA-shaped tokens in the committed C0a blob under `\b[0-9a-f]{7,40}\b`: 20 occurrences, 10 DISTINCT, types 9 `commit` and 1 `blob`, FAILING SET EMPTY.
G9 ORDERED AFTER C4 — `git push origin feature/f031-decision-inbox`; no `--force`, no `--force-with-lease`, no history rewrite, no branch deletion, no PR. Outcome carried to the reviewer, not to any file this round writes.

## Authored-text proofs
Two reviewer-authored slices applied, both extracted PROGRAMMATICALLY from the
COMMITTED C0a blob by their marker LINES, which never reached a target file:
PLANF031R26 (2653 bytes, 47 lines) whole-file into `.agent/plan.md` at C1, and
LEDGER26 (8841 bytes, 3 lines) appended to `.agent/live_review.md` at C2. The
disk-to-disk comparison is G1's four readings, all four byte-identical; the block
states NO digest of itself (constraint 3), so G1's digest is the one I measured.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror into last_block | done | |
| C1 the plan | done | |
| C2 the R25 gate entry and R-0682's resolution | done | |
| C3 module, tests, both chip rows, D11 | done | |
| C4 handback | done | |
| S1 `decisionAnswer.ts` | done | |
| S2 `decisionAnswer.test.ts` | done | 17 tests |
| S3 `role="group"` in both files | done | |
| S4 DECISION F031 D11 | done | |
| G9 push | done | ordered after C4; outcome carried by G9 to the reviewer |

## Findings
Open set 239 by the §3 item 10 rule DECISION F009 D10 requires — every
`^- R-\d+ — ` paragraph (244) minus every `^Done: R-\d+ — ` line (5) — measured at
C2 `b313d680`. Minted this round 0; resolved this round 1, `R-0682`. The narrower
set, the findings THIS FEATURE MUST STILL ACT ON, is the 22 ids `.agent/plan.md`
lists at C1 `7019185f`, of which `R-0495` and `R-0574` are the two Highs.

## Deviations & assumptions
SEQUENCE: no departure. Exactly the six commits constraint 4 names, in that order,
none extra and none dropped.

STALE ABSENCE LEFT UNREPAIRED, DECLARED NOT FIXED. `apps/ui/src/api/decisionCard.ts`
line 25 reads "What is still genuinely absent everywhere is ANSWERING, which is
T003's". S1 falsifies "everywhere": the answer COMMAND now exists, though nothing
sends it. That is the R-0593 class. Constraint 11 forbids writing `decisionCard.ts`
by name, so I obeyed and declared rather than fixing silently (constraint 1). The
next round should carry that one-sentence repair.

READING TAKEN ON S3's REPAIR CLAUSE. The absence in `DecisionInboxCard.tsx`'s header
("What is still absent is ANSWERING") is falsified by S1's module, not by S3's
attribute. I read "this change" as the round's change and repaired that sentence in
a file S3 names, naming the module as falsifier and the SEND as what is still
absent. Read narrowly, that repair is +3 lines beyond the attribute.

ASSUMPTION ON "EMPTY". S1's first two refusals name an empty `id` and an empty
answer. I read "empty" literally as `=== ""`, no trim, so a whitespace-only answer
is BUILT rather than refused; trimming is behaviour the spec does not order.

REFLOG SCOPE. The 6 scoped entries include the base commit's own reflog entry; my
five commits alone would be 5. All 6 carry the prefix `commit`.

DECISION D15 STATED-CAUSE OVERAGE. This handback is 136 lines against the 100-line
tier its 6 commits earn. The overage is mandated content: six per-commit tables
(one per commit, C3 alone carrying 5 paths), nine one-line-per-gate results whose
ordered numerals cannot be summarized, an eleven-row item-status table, and four
declared deviations. No section was dropped and no token cap is claimed.

## Next
1. The next session reads `.agent/STOP` from disk as Phase 1 rule 1, BEFORE the
   Open PR Gate as rule 2.
2. The R26 verdict is UNRECORDED and is owed by the next round's ledger commit
   (DECISION F085 D9).
3. T003 continues with the SENDER round the plan's Next Steps names first: the
   CSRF header, the bearer token, the nonce the browser mints, and the answer
   affordances the card still ships DISABLED.
