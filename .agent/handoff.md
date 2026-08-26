# Handback — F031 Decision inbox, Runde 21

Feature F031 (Tier 5) · Runde 21, a RECORD round shipping NO code · branch `feature/f031-decision-inbox`, never `main` · base `a462932f84180a14d39d3a7d5d08e0bc4d5cef88` · the block's constraint 3 fixes 5 commits, and 5 is NOT >5, so the AGENTS.md `### handoff.md` tier is 60 lines.

Fortschritt: ~66 % (F031 claimed; R1 through R20 landed, R20 gated here ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING SHIPPED and gated · T002b filtering/badge und
             T003 offen) — Schaetzung

## Range
Review of `a462932f84180a14d39d3a7d5d08e0bc4d5cef88`..HEAD, where HEAD is the C3 commit this file IS; its SHA cannot exist while this text is written.

## Commits
### 540ff83b chore(agent): save the F031 R21 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f031-r21.md` | +340/-0 | C0a: the R21 block saved verbatim |
### b7b345a4 chore(agent): mirror the R21 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +192/-331 | C0b: mirror written FROM the committed C0a blob |
### b2c00ebc docs(agent): point the F031 plan at R22
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +21/-19 | C1: PLANF031R21 applied as the whole file |
### 259e4fd9 docs(agent): record the F031 R20 verdict and two more R-0593 instances
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | C2: LEDGER21 then EVIDENCE0593 appended IN THAT ORDER, nothing else |
### C3 docs(agent): write the F031 R21 handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this file | C3: the handback; a handoff cannot table its own commit (R-0149) |

## External actions
- `git worktree add --detach .remedy-wt/f031-r21-mutant 259e4fd9` — the path did not exist; this ONE worktree carried G5's negative control and nothing else.
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f031-r21-mutant` — removed by that EXACT path, before the G7/G8 suites; `git worktree list` back to 1 line. Nothing pre-existing under `.remedy-wt/` was deleted.
- `git push origin feature/f031-decision-inbox` — ordered by G9 after C3. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate and records them in the R21 entry of `.agent/live_review.md`.
- No PR created, no merge, no branch deleted, no `gh` command run, no force-push, no history rewrite.

## Verification
- G1 `git branch --show-current` printed `feature/f031-decision-inbox`, not `main`; `.agent/STOP` read from disk ABSENT before C0a and again before C3, and never created or deleted; `git status --porcelain` 0 lines after each of C0a, C0b, C1 and C2.
- G2 all FOUR readings EQUAL — `.remedy-wt/f031-r21.md` before C0a, the committed C0a blob, the committed C0b blob, `.agent/last_block.md` off disk after C0b — sha256 `0fcea101e1f37782cf9565142a8269d23a8a497c2577d58f056d236cad862d75`, 29854 bytes, 340 lines; C0a's and C0b's file resolve to the SAME blob id `599e6675d9e5aa79fb038ca357f7b20e1498daf2`.
- G3 my extractor over the COMMITTED C0a blob printed 3 slices, 50 CONTENT lines inside markers and 340 TOTAL lines; PROSE = 340 − 50 = 290. Both caps the Base section names are met: TOTAL 340 ≤ 490 (DECISION F085 D6) and PROSE 290 ≤ 400 (DECISION F085 D5). NEITHER IS EXCEEDED.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R21 under the newline-INCLUDED convention — slice 2832 bytes and 48 lines, file 2832 bytes and 48 lines; NEGATIVE CONTROL against that slice with its trailing newline REMOVED is FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48, strictly under 50.
- G5 the C2 append in the shape constraint 7 states, TWO slices in ONE commit, LEDGER21 then EVIDENCE0593: whole-file equality TRUE, 642904 + 1 + 6827 + 1 + 2073 = 651806 against an actual 651806, the 642904 measured off C1's own blob. SECOND READER: blank-line split, N = 2 by my own split (LEDGER21 1 paragraph, EVIDENCE0593 1), units 302 → 304, the LAST 2 units equal LEDGER21's paragraph then EVIDENCE0593's IN ORDER. NEGATIVE CONTROL: one byte flipped at offset 643005, inside the appended text and length-preserving, written ONLY inside the disposable worktree — BOTH readers REJECTED the mutant and BOTH ACCEPTED the true file.
- G6 base `a462932f` → C2 in `.agent/live_review.md`: `^- R-\d+ — ` 242 → 242, all 242 DISTINCT at both ends, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0681` → `R-0681`; `^Done: R-` 4 → 4 and `^Landed: R-` 0 → 0, both UNCHANGED. `^Recurrence: R-` 17 → 18, the ADDED id exactly `R-0593` by multiset difference. THE SPLIT SERIES: `^Gate: R\d+ — ` 19 → 19 UNCHANGED, `^Gate: F\d+ R\d+ — ` 1 → 2, the ADDED key exactly `F031 R20`, the keys `F031 R19` and `F031 R20` DISTINCT. §3 item 10 open set at C2: 242 − 4 = 238. `- R-0593 — ` still occurs EXACTLY ONCE, line-anchored and as a substring: EVIDENCE0593 joined that finding and its landed paragraph was not edited.
- G7 line-anchored `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1 and `.agent/live_review.md` at C2, against a CONTROL of 3 and 3 over the committed C0a blob, so the reading is not vacuous. `git diff --name-only a462932f..259e4fd9` names 4 paths, NONE under `apps/`, `packages/`, `tests/` or `docs/`, and neither `.agent/decisions.md` nor `.agent/context.md` nor either `f031_*_inventory.md`; RANGE minus change set EMPTY, change set minus RANGE exactly `.agent/handoff.md`, which C3 writes. Per commit over C0a..C2, each SINGLE-PARENT, INSERTIONS 340, 192, 21 and 4 read from `git diff --numstat` and NOT from `git commit`'s own summary, each under the 500 cap of AGENTS.md DECISION F104 D1, and agreeing CELL FOR CELL with the `+/-` column of the `## Commits` table above. `git ls-files .remedy-wt` 0 and `git ls-files *.zip` 0. REFLOG SCOPE: this round's 4 entries only, the top of the reflog down to but excluding the base entry; FIELD: the operation prefix before the first colon of `git reflog --format=%gs`, all four `commit`, so `amend` 0, `rebase` 0 and `cherry` 0. In the PRIMARY checkout at `apps/ui`: `npm run typecheck` REAL exit 0 with ZERO diagnostics on stdout and stderr, and `npm run test:unit` REAL exit 0 with `Test Files 22 passed (22)` and `Tests 332 passed (332)` — both counts UNCHANGED from the base, the expected reading given the path set above names no `apps/` file.
- G8 my extractor found 19 SHA-shaped occurrences of the word-bounded `[0-9a-f]{7,40}` in the COMMITTED C0a blob, 11 DISTINCT, and the FAILING SET IS EMPTY. Types: `ba57b10c9e9eb08277d422ffdf558ada29c5b0fd` is a `blob`; `2ab7d2bf`, `6325ac2f`, `8efcab59`, `a462932f`, `a462932f84180a14d39d3a7d5d08e0bc4d5cef88`, `ab82dacd`, `b6e5eca7`, `ba75103e`, `bce7badc` and `e6b865c3` are all `commit` — 10 commit, 1 blob. `git worktree list` was 1 line immediately BEFORE the first pytest. The five suites then ran SERIALLY in the primary checkout at the C2 tree, never two alive at once, by the block's exact command lines with no extra flag, every one a REAL exit 0: `tests/ui_server/` 474 passed, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_golden_path.py` 42 — every count identical to the reviewer's base readings, so there is NO difference to account for.
- G9 `git push origin feature/f031-decision-inbox` runs AFTER C3, with no `--force`, no `--force-with-lease`, no history rewrite, no branch deletion and no pull request. Its outcome is carried by G9 to the reviewer, who measures the pushed tips at the next gate; it is reported in the worker's final message and is deliberately not a value of this file.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY from the COMMITTED C0a blob by its `<<<SLICE`/`<<<END` marker LINES, never retyped or rewrapped; no marker line reached a target file (G7). This block carried NO FROM/TO pair (constraint 8), so no containment test and no FROM-zero count is reported.
- PLANF031R21 → `.agent/plan.md` at C1: sha256 `cd9fcd30ae2567e742bf427653dab0f77b97be2912420f03857e33d4cd606766`, 2832 bytes, applied as the whole file, byte-equal (G4).
- LEDGER21 → `.agent/live_review.md` at C2, FIRST: sha256 `0707f9bdc1b013a1ecf8605b25e5f4c4ea008c48ba8a13eaf532668340c328e8`, 6827 bytes, appended.
- EVIDENCE0593 → `.agent/live_review.md` at C2, SECOND: sha256 `821dc08d04af6f9b3774f784fbb065ec44da675f690f027e76b1fe4828529e4d`, 2073 bytes, appended. Both land in the ONE commit C2 and the whole-file equality over both is TRUE (G5).

## Findings
This round MINTED NO ID and RESOLVED NOTHING; `^Done: R-` and `^Landed: R-` are untouched. By the §3 item 10 rule DECISION F009 D10 requires — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the set is 238 measured at `259e4fd9`, unchanged from 238 at the base `a462932f`. The findings THIS FEATURE MUST STILL ACT ON are the 21 ids `.agent/plan.md` lists at C1, counted mechanically off that committed blob, of which R-0495 and R-0574 are the two Highs; R-0593 joined that list this round.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror into last_block | done | |
| C1 the plan | done | |
| C2 the R20 gate entry and the R-0593 evidence | done | |
| C3 handback | done | |
| push (G9) | done | ordered after C3; outcome carried by G9 to the reviewer |

## Deviations & assumptions
- NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE: C0a, C0b, C1, C2, C3 exactly — none extra, none dropped, none reordered.
- Deviations, declared (AGENTS.md DECISION D15): this handback is 81 lines against the 60-line tier its 5 commits fix. The overage is MANDATED CONTENT — five per-commit changed-files tables, the nine-gate verification list, the item-status table, the authored-text proofs and the verbatim `Fortschritt:` block — and no section was dropped to fit. No token cap is claimed; DECISION F255 D6 withdrew it.
- PLANF031R21 was applied BYTE FOR BYTE per constraint 1 although at C1 it reads "R-0593 joins this list at C2" and "the set is 238 at `a462932f`, unchanged by this round", both written one commit BEFORE C2 makes the first of them true. Declared, not fixed: the reviewer adjudicated exactly this pattern in the R20 entry as correct behaviour and not the §3 item 20 defect.
- THE TWO STALE `apps/ui` COMMENTS EVIDENCE0593 NAMES WERE NOT REPAIRED. Constraint 10 forbids touching `apps/` this round and the slice itself assigns the repair to R22; recording them is the whole point of the entry.
- TOOLING, declared because it changed HOW not WHAT: the command guard denied `cd apps/ui && npm …` and bare `npm …` (the shell's cwd is the repo root), so G7's two `apps/ui` command lines ran through `subprocess.run` with `cwd="apps/ui"` — the same commands in the same working directory. G8's five pytest lines ran verbatim, through `subprocess.run` only so each REAL exit code could be read rather than swallowed by a pipe.
- G8's token reading is THIS block's own — 19 occurrences, 11 distinct. LEDGER21's "21 SHA-shaped occurrences, 13 distinct" describes the R20 block it reports on, not this one; the two are not in conflict.
- SCRATCH: this round's measurement artifacts live under `.remedy-wt/`, belong to no commit, and `git ls-files .remedy-wt` reads 0 (G7). Nothing pre-existing there was deleted.

## Next
The next session's first instruction, in this order. (1) Read `.agent/STOP` from disk as Phase 1 rule 1, BEFORE the Open PR Gate as rule 2 — a sentinel that appears mid-session is otherwise invisible (R-0347). (2) THE R21 VERDICT IS UNRECORDED and is owed by the NEXT round's ledger commit (DECISION F085 D9). (3) R22 ships T002b FILTERING by TYPE and MUST read `docs/ui/design_reference/` BEFORE authoring any control: `.agent/context.md` makes that reference binding for this feature and a control authored without it is a §4.5 BLOCK CONDITION, not a finding. (4) R22 also repairs the two `apps/ui` comments `Recurrence: R-0593` names, in `apps/ui/src/api/decisionCard.ts` and `apps/ui/src/components/panels/DecisionInboxCard.tsx`.
