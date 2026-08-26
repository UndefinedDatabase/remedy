# Handoff — F031 Decision inbox, round R30

Branch: feature/f031-decision-inbox · Base: def633e988f638efb2db2d816c720f419400b9bb (R29 handback, branch tip)
Fortschritt: ~95 % (F031 claimed; R1 through R29 landed, R29 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, request and
             deep-link seams shipped, deep link WIRED here, send open)
             — Schaetzung

## Range
Review of def633e9..HEAD

## Commits
### 3cdced7f docs(agent): save the F031 R30 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r30.md | +448 | C0a — the reviewer's original, copied, never retyped |
### a4a35350 docs(agent): mirror the F031 R30 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +261/-264 | C0b — mirror written from the C0a blob |
### 277d1f61 docs(agent): point the F031 plan at R30
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20/-19 | C1 — whole-file replacement by slice PLANF031R30 |
### eaf80e31 docs(agent): record the F031 R29 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 | C2 — append of slice LEDGER30, nothing else |
### 572f7298 feat(ui): jump from a decision card to its task's graph node
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/panels/RightLivePanel.tsx | +1/-1 | S1 — hands tasks and onSelectNode down |
| apps/ui/src/components/panels/DecisionInboxCard.tsx | +74/-31 | S2 — resolver call, jump control, labels, header |
| apps/ui/src/components/panels/RightLivePanel.module.css | +26 | S3 — .decisionJumpChip beside .decisionChip |
| .agent/decisions.md | +39 | S4 — DECISION F031 D15 |
### C4 (this commit) docs(agent): write the F031 R30 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — this file; a handoff cannot table its own SHA (R-0149) |

## External actions
- `git worktree add --detach .remedy-wt/r30-red 572f7298` — created; path did not exist before.
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r30-red` — removed BY THAT EXACT PATH; `git worktree list` 1 line after.
- `git push origin feature/f031-decision-inbox` — ordered after C4. That push's outcome is not a value of any file this round writes: the reviewer measures the pushed tips at the next gate and records them in the R30 entry of `.agent/live_review.md`.
- No PR created, no branch deleted, nothing merged, no force push.

## Verification
- G1 PASS. `git branch --show-current` = feature/f031-decision-inbox. `.agent/STOP` ABSENT before C0a and before C4. `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3. FOUR readings — scratch, C0a blob, C0b blob, last_block.md on disk — ALL EQUAL at sha256 350809178e8c5c50e14d709836d60b251aa294061816550bd2b173ee95fcb2c9, 36722 bytes, 448 lines; C0a and C0b resolve to the SAME blob id 537c08aa7b7a7d371d381570e40dfb72555b5bb5.
- G2 PASS. Extractor over the committed C0a blob: 2 slices (PLANF031R30, LEDGER30), 49 CONTENT lines, 448 TOTAL, so PROSE = 448 − 49 = 399. Caps met: TOTAL 448 ≤ 490 (F085 D6), PROSE 399 ≤ 400 (F085 D5).
- G3 PASS. Convention: newline-INCLUDED. `.agent/plan.md` at 277d1f61 byte-equal to PLANF031R30, slice 2774 bytes = file 2774 bytes. NEGATIVE CONTROL equal-to-slice-minus-trailing-newline: FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48, strictly under 50.
- G4 PASS. Reader A, the whole-file equality constraint 8 states: TRUE, 729516 + 1 + 7312 = 736829 against an actual 736829. Reader B, independent: blank-line split moves 321 → 322 units and the LAST 1 unit equals LEDGER30's 1 paragraph in order; trailing newlines rstripped on BOTH sides before splitting. NEGATIVE CONTROL, in memory only: one byte flipped at offset 729567, inside the appended text — BOTH readers reject the mutant, BOTH accept the true file. `git diff --name-only` over C3 does NOT name `.agent/live_review.md`.
- G5 PASS. `^- R-\d+ — ` 246 → 246, ids ADDED EMPTY and REMOVED EMPTY, all 246 DISTINCT, maximum still R-0685. `^Done: R-\d+ — ` 5 → 5, ids ADDED EMPTY. `^Landed: R-` 0 → 0. `^Recurrence: R-` 22 → 22. `^Gate: R\d+ — ` 19 → 19 UNCHANGED. `^Gate: F\d+ R\d+ — ` 10 → 11, ADDED key exactly `F031 R29`, all keys DISTINCT. §3 item 10 open set at eaf80e31: 241.
- G6 PASS, both controls REAL RED in one disposable worktree at 572f7298. (a) TYPE WIRING: target uniqueness — the naive attribute text ` onSelectNode={onSelectNode}` occurs 3 times in that file, so the unique target used was the whole `<DecisionInboxCard … />` element, occurrences 1, and the attribute was deleted inside it. Route (declared below): exit 2, single diagnostic `RightLivePanel.tsx(23,8): error TS2741: Property 'onSelectNode' is missing in type ... but required in type ...`. GREEN CONTROL on the unmutated worktree by the same route: exit 0, 0 diagnostics. (b) CSS CONTRACT: `--remedy-blue-strong` → `--remedy-focus` in S3's new rule (target occurrences 1); `python3 -m pytest tests/ui_contracts/test_design_drift.py -q` from that worktree exit 1, failing id `TestEveryCustomPropertyResolves::test_the_unresolved_set_has_not_grown`, message naming `--remedy-focus` in RightLivePanel.module.css. Each file restored byte-identically; worktree `git status --porcelain` 0 after each restore; worktree removed by exact path, `git worktree list` 1 line.
- G7 PASS. Structure at 572f7298: `nodeIdForDecisionCard` imported once — line 41 `import { nodeIdForDecisionCard } from "../../api/decisionFocus";` — and CALLED exactly once — line 139 `const jumpNodeId = nodeIdForDecisionCard(decision, tasks);`. Line 42 `import type { FocusableTask } from "../../api/feedFocus";`; local interface/type named FocusableTask: 0. `fetch(` 0; the answer button still carries a bare `disabled` (1). `never a value this file chose` 0. Tokens named by S3's new rule, all 6 DEFINED in tokens.css (1 definition each): --remedy-bg-2, --remedy-blue-strong, --remedy-ink, --remedy-line-strong, --remedy-muted, --remedy-radius-pill. Suites, PRIMARY checkout at the C3 tree, run SERIALLY, `git worktree list` 1 line immediately before the first: `npm run typecheck` exit 0, ZERO diagnostics on stdout and stderr; `npm run test:unit` exit 0 at 26 files and 400 tests, EXACTLY the Base reading. Python, exact command lines, all exit 0: tests/ui_server/ 480; test_test_runner 52; test_resource_safety 21; test_integrity_gate 16; tests/ui_contracts/ 525 passed 4 skipped; test_golden_path 42. Every count identical to the Base — no difference to account for.
- G8 PASS. Line-anchored `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and all four files C3 writes; CONTROL over the committed C0a blob 2 and 2. `git diff --name-only def633e9..572f7298` names 8 paths, NONE under docs/, packages/ or tests/, none an inventory file, none of the nine forbidden paths; range MINUS change set EMPTY, change set MINUS range exactly `.agent/handoff.md`. Commit shapes, insertions from `git diff --numstat` (not from `git commit`), each single-parent and under 500: 3cdced7f 448, a4a35350 261, 277d1f61 20, eaf80e31 2, 572f7298 140 — the same numbers fill the `+/-` column above, so the two agree cell for cell. `git ls-files .remedy-wt` 0; `git ls-files -- '*.zip'` 0. REFLOG scoped to THIS ROUND'S 5 entries (C0a..C3), field = the operation prefix before the first colon of `git reflog --format=%gs`: all 5 read `commit`; amend 0, rebase 0, cherry 0. SHA-shaped tokens in the C0a blob by `\b[0-9a-f]{7,40}\b`: 19 matched, 10 distinct, 9 `commit` and 1 `blob`, FAILING SET EMPTY.
- G9 — see `## External actions`; outcome reported to the reviewer, not written to a file.

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
| S1 | done | |
| S2 | deviated | two label constants, not one — see Deviations |
| S3 | done | |
| S4 | done | |
| push | done | ordered after C4; outcome carried by G9 to the reviewer |

## Authored-text proofs
Two slices, both extracted programmatically from the COMMITTED C0a blob by marker LINES and compared disk-to-disk: PLANF031R30 → `.agent/plan.md` byte-equal (G3); LEDGER30 → the C2 append, equal under both readers (G4). Block transport: four readings equal, one blob id (G1). No marker line reached any target (G8).

## Deviations & assumptions
1. S2(d)/(e) name ONE new constant; I wrote TWO — `DECISION_JUMP_LABEL` ("In graph", visible) and `DECISION_JUMP_TITLE` ("Show this decision's task in the graph", the `title`). (e) orders a header sentence saying the fixed affordance labels are declared as constants at the top; leaving the title inline would have made the sentence I was ordered to write FALSE, and `ANSWER_PENDING_TITLE` is this file's existing idiom for exactly a button `title`. Declared per constraint 2.
2. G6(a) orders the deleted byte count to be 1. The attribute text alone is NOT a unique target: ` onSelectNode={onSelectNode}` occurs 3 times in `RightLivePanel.tsx` (the DecisionInboxCard, ActivityFeedCard and TaskChecklistCard elements). I made the whole `<DecisionInboxCard … />` element the destructive target — occurrences 1 — and deleted the attribute inside it. The reported 1 is the target actually used.
3. G6(a) tsc route, NAMED because `npm run typecheck` cannot be pointed at a worktree: a fresh worktree has no `apps/ui/node_modules` and symlinking is denied, and `--project <worktree>/apps/ui/tsconfig.json` alone yields 816 diagnostics that are all missing-module noise. Route used: `npx tsc --noEmit --project .remedy-wt/r30-red-tsconfig.json`, run from the PRIMARY `apps/ui` so the primary's installed compiler and `node_modules` are used, where that gitignored scratch config carries the shipped compiler options, an `include` of the WORKTREE's `apps/ui/src`, and `baseUrl`/`paths`/`typeRoots` pointing at the primary's `node_modules`. It is not blind: the same route on the UNMUTATED worktree is exit 0 with 0 diagnostics. The config lives OUTSIDE the worktree, so the worktree's `git status --porcelain` stayed 0.
4. `DecisionInboxCard.tsx`'s map gained a block body, so the returned JSX was re-indented by two spaces — 39 whitespace-only lines inside C3's diff, no other content change there.
5. The props are REQUIRED, not optional. S2(a) says "typed as `ActivityFeedCard` types its own", and that component's EXPORTED props are optional while its inner `LiveFeed` types the same pair required. I took the required spelling, because G6(a) orders a dropped `onSelectNode` to go RED and an optional prop cannot.
6. `--remedy-focus` appears ONCE in S3's new rule, inside the COMMENT that records why it is not used. It appears in no `var()`; the ordered reading is the `var(--remedy-…)` set, which is the 6 names listed in G7.
7. Zip glob read as `git ls-files -- '*.zip'` (the block names no pattern). "The answer button still carries `disabled`" read as a bare `disabled` attribute line, count 1.
8. Scratch created under `.remedy-wt/` this round, all gitignored and belonging to no commit: `r30-extract/`, `r30-red-tsconfig.json`, `r30-g7-structure.py`, `r30-g8.py`. Nothing pre-existing there was deleted. `git ls-files .remedy-wt` 0.
9. Commit sequence C0a, C0b, C1, C2, C3, C4 followed EXACTLY — no extra commit, none dropped, no reordering. No amend, rebase, cherry-pick, force-push, branch deletion, merge or PR.
10. No finding id minted and none resolved, per constraint 10. `docs/` was not touched: constraint 11 forbids it, and the deep link's behaviour is documented nowhere under `docs/` that this round falsifies.

## Next
The next session reads `.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule 2. The R30 verdict is UNRECORDED and is owed by the next round's ledger commit (DECISION F085 D9). Then T003's SEND round, the last of the seam, which owns the only `fetch` in this feature.
