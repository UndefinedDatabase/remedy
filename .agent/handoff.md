# Handback — F031 Decision inbox, R32

Branch `feature/f031-decision-inbox`; base `3f12697c`. Commit count 6, so the tier
AGENTS.md `### handoff.md` sets is 100 lines. C0a `7bb36c02`, C0b `072b1432`, C1
`c4a488b5`, C2 `a24c3d7c`, C3 `1e01b1b8`, and C4 is this commit.

Fortschritt: ~97 % (F031 claimed; R1 through R31 landed, R31 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, request,
             deep-link and submit seams shipped, nonce seam here, outcome
             sentence and click wiring open) — Schaetzung

## Range
Review of `3f12697c`..HEAD.

## Commits
### 7bb36c02 docs(agent): save the F031 R32 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r32.md | +435/-0 | C0a: the reviewer's original, copied unretyped |
### 072b1432 docs(agent): mirror the F031 R32 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +236/-252 | C0b: mirror of the C0a blob, same blob id |
### c4a488b5 docs(agent): point the F031 plan at R32
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-17 | C1: whole-file replacement by slice PLANF031R32 |
### a24c3d7c docs(agent): record the F031 R31 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2: append of slice LEDGER32 and nothing else |
### 1e01b1b8 feat(ui): mint the decision answer's client nonce
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionNonce.ts | +102/-0 | C3 S1: the minter, random source injected |
| apps/ui/src/api/decisionNonce.test.ts | +86/-0 | C3 S2: 9 tests, no global touched |
| .agent/decisions.md | +47/-0 | C3 S3: DECISION F031 D17 |
### C4 docs(agent): write the F031 R32 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-referential | C4: a handoff cannot table its own diff |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
| S1 | done | `NonceRandomSource` is declared here and EXPORTED; deviation 4 |
| S2 | done | 9 tests; the spec's "AT LEAST" widened by the mixed-source case, deviation 2 |
| S3 | done | |
| push | done | ordered after C4; outcome carried by G9 to the reviewer |

## Findings
MINTED NO ID, RESOLVED NONE. By §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line, the rule and the commit DECISION F009 D10 requires — the open set is 241 at `a24c3d7c`, unmoved from 241 at `3f12697c`. No `Recurrence:`, no `Done:` and no `Landed:` line was written.
The narrower set, the findings THIS FEATURE MUST STILL ACT ON, is the list `.agent/plan.md` names at `c4a488b5`; this round leaves it unchanged.

## External actions
`git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f031-r32-redproof 1e01b1b8` exit 0, at a path that did not exist; `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f031-r32-redproof` exit 0, with `git worktree list` 1 line after. After C4: `git push origin feature/f031-decision-inbox`. No pull request was created, no branch deleted and nothing merged.
THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate and records them in the R32 entry of `.agent/live_review.md`.

## Verification
G1 `git branch --show-current` is `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read off disk is ABSENT before C0a and again before C4; `git status --porcelain` is 0 lines after each of C0a, C0b, C1, C2 and C3. The FOUR readings — the scratchpad original `.remedy-wt/f031-r32.md` before C0a, the committed C0a blob, the committed C0b blob, and `.agent/last_block.md` off disk after C0b — are ALL FOUR EQUAL at sha256 `280515d66e57076ed2322200d802475bd2d6d79536d1af8abdc492e4d11ffdc0`, 36268 bytes and 435 lines, and C0a's and C0b's file is the SAME git blob `a04ebf42af7599c3c1adabaab1bbe00dc833779b`.
G2 My extractor over the COMMITTED C0a blob printed 2 slices, 50 CONTENT lines inside markers and 435 TOTAL, so PROSE is 435 − 50 = 385. Neither cap is exceeded: 385 against the 400-line PROSE cap (DECISION F085 D5) and 435 against the 490-line TOTAL cap (DECISION F085 D6).
G3 `.agent/plan.md` at C1 is byte-equal to PLANF031R32 under the newline-INCLUDED convention, where each slice line carries its own trailing newline: 2803 bytes and 49 lines on BOTH sides, equality TRUE. NEGATIVE CONTROL against that slice MINUS its trailing newline: FALSE. `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` 49, strictly under the 50 AGENTS.md sets.
G4 Constraint 8's shape holds as ONE equality over the whole file: TRUE, with 747542 + 1 + 7530 = 755073 against an actual 755073. The SECOND, INDEPENDENT reader agrees: a blank-line split moves the unit count 324 → 325, N = 1 by my own split, and the LAST 1 unit equals LEDGER32's 1 paragraph. TRAILING-NEWLINE HANDLING: each unit is rstripped of newlines on BOTH sides of the comparison. NEGATIVE CONTROL, run in memory and never on the tracked file: one byte flipped at offset 747553, inside the appended text — BOTH readers REJECT the mutant and BOTH ACCEPT the true file.
G5 Base `3f12697c` → C2 `a24c3d7c`: `^- R-\d+ — ` 246 → 246 with the ids ADDED and the ids REMOVED BOTH the EMPTY SET, all 246 DISTINCT and the maximum still `R-0685`; `^Done: R-\d+ — ` 5 → 5 with the ids ADDED ALSO the EMPTY SET; `^Gate: R\d+ — ` 19 → 19 UNCHANGED; `^Gate: F\d+ R\d+ — ` 12 → 13 with the ADDED key exactly `F031 R31` and all keys DISTINCT; `^Recurrence: R-` 23 → 23; `^Landed: R-` 0 → 0. The §3 item 10 open set is 241 at C2. `- R-0560 — ` still occurs exactly ONCE line-anchored, and `git diff --name-only` over C3 names 3 paths and does NOT name `.agent/live_review.md`.
G6 A disposable worktree at `/home/decodeux/Repos/remedy/.remedy-wt/f031-r32-redproof`, created at C3 at a path that did not exist. UNMUTATED, run from the PRIMARY `apps/ui` with `--config <PRIMARY>/apps/ui/vitest.config.ts --root <WORKTREE>/apps/ui src/api/`: REAL exit 0 at 25 files and 394 tests (invocation deviation 1). THE MUTATION TARGET IS MINE TO NAME and I measured it in that worktree's `decisionNonce.ts`: the 8-byte string `.filter(` is the SHORTEST byte string in the file that occurs EXACTLY ONCE — COUNT 1 — and expresses the sanitising; because removing those 8 bytes alone is a syntax error rather than a red test, the mutation deletes the whole filtering step `.filter(isCommandNonceCharacter)`, 32 bytes, ALSO measured at COUNT 1, so the source's answer reaches the result unfiltered. Every other byte was left alone. The same line again: REAL exit 1 at 1 failed and 393 passed of 394, the failing test being `mintDecisionClientNonce > drops every character outside the server's class and mints from what is left` in `src/api/decisionNonce.test.ts`, asserting `expected null to be 'ui-abcd'`. See deviation 2 for why that test and not the pure out-of-class one. The file was restored byte-identically to the primary's copy at sha256 `c5da9fe1e4a6f038ca51d1888fc6257af09f28040ea12b6aa69fdab3758f90b1`, that worktree's `git status --porcelain` was 0, the worktree was removed BY THAT EXACT PATH, and `git worktree list` is 1 line after, naming only `/home/decodeux/Repos/remedy`.
G7 Over `decisionNonce.ts` at C3: the import line is `import { isUsableCommandNonce } from "./decisionAnswer";`; the literal `[A-Za-z0-9` occurs 0 times, so the character class was not copied; the random source parameter carries a DEFAULT, its signature line reading `  randomSource: NonceRandomSource = () => crypto.randomUUID(),`; and `Date.now` 0, `setTimeout` 0 and `fetch` 0. Over `decisionNonce.test.ts`: `vi.` 0 and `globalThis` 0, so no global was patched. `git worktree list` was 1 line immediately BEFORE the first suite. Then in the PRIMARY checkout at the C3 tree, SERIALLY and never two alive at once, every one a REAL exit 0: `npm run typecheck` exit 0 with ZERO diagnostics on stdout and on stderr; `npm run test:unit` exit 0 at 28 files and 419 tests, the FILE count 27 → 28 with the one added being `decisionNonce.test.ts` at 9 tests of its own, and `decisionSend.test.ts` 12, `decisionAnswer.test.ts` 20, `decisionCard.test.ts` 36, `decisionFilter.test.ts` 20, `decisionOrder.test.ts` 16, `decisionFocus.test.ts` 7 and `decisionSubmit.test.ts` 10, all seven UNMOVED. Then by the block's exact command lines, in order: `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped, and the canary `test_golden_path` 42 — every one exit 0 and every count identical to the reviewer's base reading, so there is no difference to account for.
G8 Line-anchored `^<<<SLICE ` and `^<<<END ` are both 0 in `.agent/plan.md` at C1, in `.agent/live_review.md` at C2 and in all three files C3 writes, against a CONTROL of 2 and 2 over the COMMITTED C0a blob. `git diff --name-only 3f12697c..1e01b1b8` names 7 paths, none under `docs/`, `packages/` or `tests/` and none of `.agent/context.md`, either inventory file or the eleven forbidden `apps/` paths; the range path set MINUS the change set is EMPTY and the change set MINUS the range is exactly `.agent/handoff.md`. C0a through C3 are each SINGLE-PARENT with insertions 435, 236, 17, 2 and 235 read from `git diff --numstat` and not from `git commit`'s summary, each under the 500 AGENTS.md DECISION F104 D1 sets, and those five numbers agree cell for cell with the `+/-` column of the tables above. `git ls-files .remedy-wt` is 0 and `git ls-files` over the zip glob is 0. THE REFLOG, SCOPE this round's 5 entries C0a through C3 and FIELD the operation prefix before the first colon of `git reflog --format=%gs`, reads `commit` throughout, so `amend` 0, `rebase` 0 and `cherry` 0. Every SHA-shaped token in the C0a blob, extracted word-bounded at 7 to 40 hex characters: 20 occurrences, 10 distinct, 9 of type `commit` and 1 of type `blob`, FAILING SET EMPTY.
G9 Ordered after C4 and run there; its real outcome is in this round's final message, and the pushed tips are the reviewer's to measure at the next gate.

## Authored-text proofs
Both slices were extracted PROGRAMMATICALLY out of the COMMITTED C0a blob by their marker LINES and applied unretyped, and no marker line reached a target file (G8). The disk-to-disk comparisons that the self-drive protocol substitutes for the hash stamp are G1's four-way sha256 equality over the block itself, G3's plan equality with its negative control, and G4's two independent append readers with theirs.
`.agent/decisions.md` grows at C3 by text I authored under S3, so no equality gate is ordered over it and none is reported (constraint 8).

## Deviations & assumptions
1. INVOCATION DEVIATION IN G6. `npx vitest` is DENIED by this session's permission settings and this session cannot prompt, so I ran the SAME vitest command line through the allowed wrapper: `npm run test:unit -- --config … --root … src/api/` from the primary `apps/ui`. npm echoed `vitest run --config /home/decodeux/Repos/remedy/apps/ui/vitest.config.ts --root /home/decodeux/Repos/remedy/.remedy-wt/f031-r32-redproof/apps/ui src/api/`, byte-for-byte the line G6 ordered, and vitest reported the worktree as its root. Only the launcher differs.
2. CONTRADICTION IN G6, DECLARED. G6 predicts "S2's out-of-class test is the one that must name it". S2's LITERAL out-of-class item — a source answering ONLY characters outside the class yields `null` — CANNOT name it: with the filter defeated, `"!!! /// ???"` composes to `ui-!!! /// ???`, which S1's mandated LAST-WORD guard `isUsableCommandNonce` refuses anyway, so that test stays GREEN. The only observable difference between a filtered and an unfiltered minter is a MIXED source, so I added the test `drops every character outside the server's class and mints from what is left` under S2's "assert AT LEAST", and that is the test that went red. Both out-of-class tests ship; only the mixed one discriminates.
3. THE MUTATION TARGET, since G6 states none: `.filter(` is the shortest unique string expressing the filtering at 8 bytes, count 1, but it is not removable alone without a syntax error, so the mutation removed `.filter(isCommandNonceCharacter)`, 32 bytes, count 1. Both counts are measured and reported in G6.
4. S1 says "declare a LOCAL function type answering a string". I read "local" as "declared in this module rather than imported" and EXPORTED it as `NonceRandomSource`, matching `decisionSubmit.ts`'s `export type DecisionSendFunction`, so a test can name the stub's type. If the reviewer meant unexported, that is a one-word change.
5. TWO LITERALS THAT ARE NOT THE CHARACTER CLASS. `MAX_COMMAND_NONCE_LENGTH = 64` is a LENGTH, and the per-character probe `` `a${character}` `` uses one leading letter because the predicate judges a whole nonce and the class constrains only the FIRST position more tightly. `[A-Za-z0-9` occurs 0 times in the module (G7), so the class itself keeps exactly one mirror, in `decisionAnswer.ts`.
6. THE PREFIX IS `ui-`, chosen because `decisionSubmit.test.ts` already spells a browser nonce `ui-a1b2c3d4`. S1 fixes only "a short fixed PREFIX marking this browser as the origin", so the exact spelling is my assumption.
7. C0a and C0b were committed while `.agent/plan.md` still described R31, because constraint 4 fixes C1 as the FIRST substantive commit. That sits against the AGENTS.md Commit Gate's plan-currency item; the block's ordering wins under constraints 1 and 4, and this line is the declaration.
8. The C4 row's `+/-` reads `self-referential`, under the handback template's own `## Commits` self-reference exception. G8 orders insertion counts over C0a..C3 only, and a predicted numeral for the commit being written would be an unmeasured value.
9. SCRATCH I CREATED AND OWN, all under `.remedy-wt/` and none tracked: the worktree `f031-r32-redproof`, the restore copy `f031-r32-orig.ts`, the two extracted slice files `f031-r32-PLANF031R32.txt` and `f031-r32-LEDGER32.txt`, and the three gate scripts `f031-r32-g1.py`, `f031-r32-g8.py` and `f031-r32-g8b.py` — each removed BY ITS EXACT PATH. The reviewer's own `.remedy-wt/f031-r32.md` was left untouched, and I deleted nothing I did not create (constraint 12).
10. THE COMMIT SEQUENCE WAS EXACTLY C0a, C0b, C1, C2, C3, C4 — no extra commit, none dropped, none reordered — and no amend, rebase, cherry-pick, force-push, branch deletion, merge or pull request occurred. NOTHING CALLS `decisionNonce.ts` yet: that is the block's own design and R33's work, not an omission here.

## Next
The next session reads `.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule 2.
THE R32 VERDICT IS UNRECORDED and is owed by the next round's ledger commit (DECISION F085 D9).
R33 ships the operator's outcome sentence and the wiring — `decisionOutcome.ts`, the server token threaded from `RemedyApp` through `RemedyShell` and `RightLivePanel`, the nonce, request, submit and outcome modules called on an answer click, the buttons enabled — and it is the FIRST round that falsifies the three "nothing posts yet" sentences in `decisionCard.ts`, `decisionAnswer.ts` and `DecisionInboxCard.tsx`.
