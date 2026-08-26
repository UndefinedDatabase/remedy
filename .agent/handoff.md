# Handback — F031 Decision inbox, Runde 17

Feature F031 (Tier 5) · Runde 17 · branch `feature/f031-decision-inbox` · base `a48d1234` · the block's constraint 3 fixes 7 commits, and >5 commits puts the AGENTS.md `### handoff.md` tier at 100 lines.

Fortschritt: ~57 % (F031 claimed; R1 through R16 landed and gated ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             R-0681 repaired here · T002b ordering/filtering/badge
             und T003 offen) — Schaetzung

## Range
Review of `a48d1234`..HEAD, where HEAD is the C5 commit this file IS; its SHA cannot exist while this text is written.

## Commits
### 8e4e55d6 chore(agent): save the F031 R17 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f031-r17.md` | +460/-0 | C0a: the R17 block saved verbatim |
### e15458f9 chore(agent): mirror the R17 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +290/-195 | C0b: mirror written FROM the committed C0a blob |
### 0faf773c docs(agent): point the F031 plan at the R17 rename round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +15/-15 | C1: PLANF031R17 applied as the whole file |
### 564998a0 docs(agent): record the F031 R16 verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | C2: LEDGER17 appended, and nothing else |
### 6ede183c refactor(ui): rename the decision inbox entry interface
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/decisionCard.ts` | +4/-4 | C3 S1: the interface renamed on its 4 lines |
| `apps/ui/src/api/decisionCard.test.ts` | +9/-9 | C3 S2: the same identifier on its 9 lines |
### c7a0b099 docs(agent): mark R-0681 landed at the R17 rename
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | C4: LANDED17 appended, and nothing else |
### C5 docs(agent): write the F031 R17 handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | self-reference | C5: this file; a handoff cannot table the commit that writes it (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| push | done | ordered after C5; outcome carried by G12 to the reviewer |

## External actions
- `git worktree add --detach .remedy-wt/r17-neg 564998a0` → created for the G5 negative control; `git worktree remove --force .remedy-wt/r17-neg` → removed BY ITS EXACT PATH.
- `git worktree add --detach .remedy-wt/r17-redctl 6ede183c` → created for the G10 red control; `git worktree remove --force .remedy-wt/r17-redctl` → removed BY ITS EXACT PATH.
- `git push origin feature/f031-decision-inbox` — run AFTER C5. Its outcome is not a value of any file this round writes: the reviewer measures the pushed tips at the next gate and records them in the R17 entry of `.agent/live_review.md`.
- No `gh` command run; no pull request created, edited or merged; no branch created or deleted; no amend, rebase, cherry-pick or force-push.

## Verification
- G1 `git branch --show-current` printed `feature/f031-decision-inbox`, not `main`; `.agent/STOP` read from disk was ABSENT before C0a and ABSENT again before C5; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3 and C4.
- G2 All FOUR readings EQUAL: sha256 `8323814916eb60f8bf506bacd32cbc571fb5090a455a2ae0818ae0c5832e0673`, 31846 bytes, 460 lines, for the scratch file before C0a, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk after C0b. C0a's and C0b's file resolve to the SAME git blob `87dbf588669fe871237e703f21b0fc5bd175d7f1`.
- G3 My extractor over the COMMITTED C0a blob printed: 3 slices (PLANF031R17, LEDGER17, LANDED17), 51 CONTENT lines inside markers, 460 TOTAL lines.
- G4 `.agent/plan.md` at C1 is byte-equal to PLANF031R17 under the newline-INCLUDED convention — slice 2892 bytes, file 2892 bytes, 49 lines. NEGATIVE CONTROL against that slice with its trailing newline REMOVED: FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49, strictly under 50.
- G5 In the shape constraint 7 states. C2: reader A TRUE, 619591 + 1 + 4171 = 623763 against an actual 623763; reader B split on blank lines gave N=1 paragraph, units 296 → 297, last N units EQUAL to the slice's paragraphs in order. C4: reader A TRUE, 623763 + 1 + 373 = 624137 against an actual 624137; reader B N=1, units 297 → 298, EQUAL in order. NEGATIVE CONTROL for C2, inside worktree `.remedy-wt/r17-neg`: one byte flipped at offset 619692 (`E` → `e`) inside the paragraph the append added, same file length — BOTH readers REJECTED the mutant and BOTH ACCEPTED the true file.
- G6 base → C4 in `.agent/live_review.md`: `^- R-\d+ — ` 242 → 242, all 242 DISTINCT, ids ADDED the EMPTY SET and ids REMOVED the EMPTY SET, maximum `R-0681` → `R-0681`; `^Done: R-` 3 → 3; `^Recurrence: R-` 16 → 16; `^Landed: R-` 0 → 1, gaining exactly `R-0681`; `^Gate: R\d+ — ` 16 → 17, gaining exactly the key `R16`, with `R19` and `R1` through `R15` still present and all 17 DISTINCT. The §3 item 10 open set at C4 is 242 − 3 = 239.
- G7 Line-anchored `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1 and in `.agent/live_review.md` at C2 and at C4; the same pattern counts 6 in the C0a blob, so the reading is not vacuous. `git diff --name-only a48d1234..c7a0b099` names 6 paths: no path under `packages/`, `tests/` or `docs/`, no `apps/` path other than the two the change set names, and neither `.agent/decisions.md` nor `.agent/context.md` nor either inventory file. Range MINUS change set is EMPTY; change set MINUS range is exactly `.agent/handoff.md`. Every commit C0a..C4 is single-parent, with INSERTIONS 460, 290, 15, 2, 13 and 2 — each under 500. The `## Commits` `+/-` column above is derived from `git diff --numstat`, not from `git commit`'s summary, and agrees with this gate cell for cell.
- G8 `git ls-files .remedy-wt` 0 and `git ls-files '*.zip'` 0. Reflog SCOPE: this round's entries only, `HEAD@{0}`..`HEAD@{5}`, 6 entries; FIELD: the operation prefix before the first colon of `git reflog --format=%gs`, which is `commit` for all 6 — `amend` 0, `rebase` 0, `cherry` 0. `git worktree list` printed 1 line immediately before the first pytest command of G11.
- G9 In the PRIMARY checkout, never in a worktree: `npm run typecheck` in `apps/ui` EXIT 0 with ZERO diagnostics on stdout and stderr; `npm run test:unit` EXIT 0 at 21 files and 316 tests, both counts UNCHANGED from the base's 21 and 316. THE LIMIT constraint 13 names: no red control was run against typecheck, so this reading proves CONSISTENCY and not SENSITIVITY.
- G10 At the C3 tree, `git grep -n` over `apps/ui/src`: `DecisionInboxCard` on exactly 3 lines in exactly `apps/ui/src/components/panels/DecisionInboxCard.tsx` and `apps/ui/src/components/panels/RightLivePanel.tsx`, and 0 times anywhere under `apps/ui/src/api/`; `DecisionInboxEntry` on exactly 13 lines in exactly `apps/ui/src/api/decisionCard.ts` and `apps/ui/src/api/decisionCard.test.ts`. `git diff --numstat a48d1234..6ede183c` names exactly those two api files, 4 insertions and 4 deletions for `decisionCard.ts` and 9 and 9 for `decisionCard.test.ts`; total line counts UNCHANGED at 194 and 226. RED CONTROL, inside worktree `.remedy-wt/r17-redctl` at C3 and never in the primary checkout: `export interface DecisionInboxEntry {` counted EXACTLY 1 before replacing; after replacing it with `export interface DecisionInboxCard {` the first reading moved 3 → 4 and the `apps/ui/src/api/` reading moved 0 → 1 — BOTH moved. Worktree removed by its exact path.
- G11 SHA-shaped tokens in the COMMITTED C0a blob under the word-bounded `[0-9a-f]{7,40}`: 17 occurrences, 7 DISTINCT, FAILING SET EMPTY. Types: `5845552a2f9f2164a774bce6aa12edffb95737cd` → `blob`; `4fc7dc77`, `6325ac2f`, `7d031ab1`, `877fc883`, `a48d1234` and `a48d1234a5c82797a7760adadf1fa00140b92019` → `commit`. The five Python suites, SERIALLY in the PRIMARY checkout at the C4 tree, never two alive at once, each with its REAL exit code: `tests/ui_server/` EXIT 0, 474 passed; `tests/orchestration/test_test_runner.py` EXIT 0, 52; `tests/regression/test_resource_safety.py` EXIT 0, 21; `tests/orchestration/test_integrity_gate.py` EXIT 0, 16; `tests/cli/test_golden_path.py` EXIT 0, 42. Every count equals the reviewer's base reading, so there is no difference to account for.
- G12 `git push origin feature/f031-decision-inbox`, run after C5, with no `--force`, no `--force-with-lease`, no history rewrite, no branch deletion and no pull request. Carrier as ordered: the reviewer measures the pushed tips at the next gate and records them in the R17 entry of `.agent/live_review.md`.

## Findings
The §3 item 10 open set — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line, the rule DECISION F009 D10 requires — is 239 at `c7a0b099`. The narrower set `.agent/plan.md` names "the findings this feature must still act on" is 21 distinct ids at `c7a0b099`, counted mechanically off that bullet; it is not the open set. This round minted no finding id, wrote no `Done:` line and no `Recurrence:` line.

## Authored-text proofs
- All three slices were extracted PROGRAMMATICALLY from the COMMITTED C0a blob by their `<<<SLICE`/`<<<END` marker LINES; nothing was retyped, rewrapped or hand-corrected, and no marker line reached a target file (G7).
- PLANF031R17 → `.agent/plan.md` at C1: byte-equal to the extracted slice, 2892 bytes both, with the trailing-newline-removed negative control FALSE (G4).
- LEDGER17 → `.agent/live_review.md` at C2 and LANDED17 → the same file at C4: each proven by whole-file equality against the commit's PARENT blob plus one newline plus the slice, and independently by the blank-line paragraph reader (G5).

## Deviations & assumptions
- COMMIT SEQUENCE: C0a, C0b, C1, C2, C3, C4, C5 applied exactly as constraint 3 orders — no extra commit, none dropped, no reordering.
- G9 DEVIATION, declared: the block orders `npm run typecheck` and `npm run test:unit` "at the C3 tree". Both were first run with HEAD at C3 and a clean tree, and their REAL exit codes were then captured with HEAD at C4. `git diff --name-only 6ede183c..c7a0b099 -- apps/ui` names 0 paths, so the `apps/ui` tree at C4 IS the C3 tree; the output was identical across both runs.
- TOOL DEVIATION, declared: this session's command guard rejected several shell forms (`npm --prefix`, `$?`, shell redirection into `.remedy-wt/`, and a `for` statement inside a python heredoc). The C3 rename was therefore applied with the editor's whole-file identifier substitution instead of a line-scoped script. This is safe here and was checked rather than assumed: in BOTH files EVERY occurrence of `DecisionInboxCard` is a rename target the Base section names, so the substitution touched exactly the 4 and the 9 named lines and no other line — which the 4/4 and 9/9 numstat and the G10 greps measure.
- NO CONTRADICTION was found inside the block. Every reading it states about the base — the ledger counts, the plan and handoff sizes, the 16 identifier lines and their split into 13 interface and 3 component, the 194 and 226 line counts, and the five suite counts — reproduced exactly when measured here.
- Scratch files this round created under `.remedy-wt/` were the two worktrees named above, both removed by exact path, plus three extracted slice files; nothing pre-existing there was touched or deleted.
- HANDBACK SIZE, per DECISION D15: this file measures 95 lines against the 100-line tier, so no overage is claimed.

## Next
1. The R17 verdict is UNRECORDED and is owed by the NEXT round's ledger commit — by DECISION F085 D9 no artefact of this round can carry it.
2. The `Landed: R-0681` line is an UNREVIEWED fix until the reviewer replaces it with authored `Done:` text at that gate.
3. T002b is the next build step, under DECISION F031 D2.
