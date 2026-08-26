# Handback — F031 Decision inbox, R31

Branch `feature/f031-decision-inbox`; base `5ee3024b`. Commit count 6, so the tier
AGENTS.md `### handoff.md` sets is 100 lines. C0a `34ed2495`, C0b `5310e3fb`, C1
`eb10e19d`, C2 `e54dc525`, C3 `f0254e78`, and C4 is this commit.

Fortschritt: ~96 % (F031 claimed; R1 through R30 landed, R30 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, request and
             deep-link seams shipped and wired, submit seam here, click
             handler open) — Schaetzung

## Range
Review of `5ee3024b`..HEAD.

## Commits
### 34ed2495 docs(agent): save the F031 R31 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r31.md | +451/-0 | C0a: the reviewer's original, copied unretyped |
### 5310e3fb docs(agent): mirror the F031 R31 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +261/-258 | C0b: mirror of the C0a blob, same blob id |
### eb10e19d docs(agent): point the F031 plan at R31
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +22/-21 | C1: whole-file replacement by slice PLANF031R31 |
### e54dc525 docs(agent): record the F031 R30 verdict and R-0560's recurrence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2: append of slice LEDGER31 and nothing else |
### f0254e78 feat(ui): send a decision answer and map the door's verdict
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionSubmit.ts | +83/-0 | C3 S1: the one network call, send injected |
| apps/ui/src/api/decisionSubmit.test.ts | +145/-0 | C3 S2: 10 tests, no global touched |
| .agent/decisions.md | +38/-0 | C3 S3: DECISION F031 D16 |
### C4 docs(agent): write the F031 R31 handback
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
| S1 | done | the default send is an inline arrow NAMING `fetch`; deviation 1 |
| S2 | done | 10 tests; the spec's "AT LEAST" widened by a 429 case, deviation 2 |
| S3 | done | |
| push | done | ordered after C4; outcome carried by G9 to the reviewer |

## Findings
MINTED NO ID, RESOLVED NONE. By §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line, the rule and the commit DECISION F009 D10 requires — the open set is 241 at `e54dc525`, unmoved from 241 at `5ee3024b`. ONE `Recurrence:` line was appended against R-0560, which stays OPEN.
The narrower set, the findings THIS FEATURE MUST STILL ACT ON, is the list `.agent/plan.md` names at `eb10e19d`; it is unchanged by this round except that R-0560 now sits in it.

## External actions
`git worktree add --detach .remedy-wt/f031-r31-red f0254e78` exit 0, at a path that did not exist; `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f031-r31-red` exit 0, with `git worktree list` 1 line after. After C4: `git push origin feature/f031-decision-inbox`. No pull request was created, no branch deleted and nothing merged.
THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate and records them in the R31 entry of `.agent/live_review.md`.

## Verification
G1 `git branch --show-current` is `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read off disk is ABSENT before C0a and again before C4; `git status --porcelain` is 0 lines after each of C0a, C0b, C1, C2 and C3. The FOUR readings — the scratchpad original `.remedy-wt/f031-r31.md` before C0a, the committed C0a blob, the committed C0b blob, and `.agent/last_block.md` off disk after C0b — are ALL FOUR EQUAL at sha256 `57f92a38820a7d1f9d192715f6cbcaf5fe67f5152cfc5f50d249b1c709b7d91b`, 40419 bytes and 451 lines, and C0a's and C0b's file is the SAME git blob `a87532620322c59bd7f0303c98da2b93ac3b8db9`.
G2 My extractor over the COMMITTED C0a blob printed 2 slices, 52 CONTENT lines inside markers and 451 TOTAL, so PROSE is 451 − 52 = 399. Neither cap is exceeded: 399 against the 400-line PROSE cap (DECISION F085 D5) and 451 against the 490-line TOTAL cap (DECISION F085 D6).
G3 `.agent/plan.md` at C1 is byte-equal to PLANF031R31 under the newline-INCLUDED convention, where each slice line carries its own trailing newline: 2823 bytes and 49 lines on BOTH sides, equality TRUE. NEGATIVE CONTROL against that slice MINUS its trailing newline: FALSE. `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` 49, strictly under the 50 AGENTS.md sets.
G4 Constraint 8's shape holds as ONE equality over the whole file: TRUE, with 736829 + 1 + 10712 = 747542 against an actual 747542. The SECOND, INDEPENDENT reader agrees: a blank-line split moves the unit count 322 → 324, N = 2 by my own split, and the LAST 2 units equal LEDGER31's 2 paragraphs IN ORDER. TRAILING-NEWLINE HANDLING: newlines are rstripped off the whole text before splitting and off each unit on BOTH sides of the comparison. NEGATIVE CONTROL, run in memory and never on the tracked file: one byte flipped at offset 742186, inside the appended text — BOTH readers REJECT the mutant and BOTH ACCEPT the true file.
G5 Base `5ee3024b` → C2 `e54dc525`: `^- R-\d+ — ` 246 → 246 with the ids ADDED and the ids REMOVED BOTH the EMPTY SET, all 246 DISTINCT and the maximum still `R-0685`; `^Done: R-\d+ — ` 5 → 5 with the ids ADDED ALSO the EMPTY SET; `^Gate: R\d+ — ` 19 → 19 UNCHANGED; `^Gate: F\d+ R\d+ — ` 11 → 12 with the ADDED key exactly `F031 R30` and all keys DISTINCT; `^Recurrence: R-` 22 → 23; `^Recurrence: R-0560` 0 → 1; `^Landed: R-` 0 → 0. The §3 item 10 open set is 241 at C2. `- R-0560 — ` still occurs exactly ONCE line-anchored, so its landed paragraph was not edited, and `git diff --name-only` over C3 names 3 paths and does NOT name `.agent/live_review.md`.
G6 A disposable worktree at `/home/decodeux/Repos/remedy/.remedy-wt/f031-r31-red`, created at C3 at a path that did not exist. UNMUTATED, the ordered line run from the PRIMARY `apps/ui` with `--config <PRIMARY>/apps/ui/vitest.config.ts --root <WORKTREE>/apps/ui src/api/`: REAL exit 0 at 24 files and 385 tests. THE MUTATION TARGET IS MINE TO NAME and I measured it in that file: the 11-byte string `: "refused"`, COUNT 1 — the SHORTEST byte string in `decisionSubmit.ts` that occurs exactly once and expresses the status mapping — replaced by `: "accepted"` so that EVERY answered request maps to the accepted outcome, every other byte left alone. The same line again: REAL exit 1 at 3 failed and 382 passed of 385, the three failing tests being `maps a 403 to refused CARRYING 403, which is how a card names a credential problem`, `maps a 409 to refused CARRYING 409, which is how a card names a decision already answered` and `maps a 429 to refused CARRYING 429, so the rate budget is not read as a credential problem`, all in `src/api/decisionSubmit.test.ts`. The file was restored byte-identical to the primary's copy, that worktree's `git status --porcelain` was 0, the worktree was removed BY THAT EXACT PATH, and `git worktree list` is 1 line after, naming only `/home/decodeux/Repos/remedy`.
G7 Over `decisionSubmit.ts` at C3: its ONLY import line is `import type { DecisionSendRequest } from "./decisionSend";`, so the request arrives as a TYPE; the send parameter's signature reads `send: DecisionSendFunction = (sent) =>` continuing onto `fetch(sent.path, { method: sent.method, headers: sent.headers, body: sent.body }),`, so the DEFAULT names the global `fetch`; `setTimeout` 0, `Date.now` 0 and `crypto` 0; and it reaches into no decision field, with `answerText` 0, `decision_id` 0, `client_nonce` 0, `taskId` 0 and `buildDecision` 0. Over `decisionSubmit.test.ts`: `vi.` 0 and `globalThis` 0, so no global was patched. `git worktree list` was 1 line immediately BEFORE the first suite. Then in the PRIMARY checkout at the C3 tree, SERIALLY and never two alive at once, every one a REAL exit 0: `npm run typecheck` exit 0 with ZERO diagnostics on stdout and on stderr; `npm run test:unit` exit 0 at 27 files and 410 tests, the FILE count 26 → 27 with the one added being `decisionSubmit.test.ts` at 10 tests of its own, and `decisionSend.test.ts` 12, `decisionAnswer.test.ts` 20, `decisionCard.test.ts` 36, `decisionFilter.test.ts` 20, `decisionOrder.test.ts` 16 and `decisionFocus.test.ts` 7, all six UNMOVED. Then by the block's exact command lines, in order: `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped, and the canary `test_golden_path` 42 — every one exit 0 and every count identical to the reviewer's base reading, so there is no difference to account for.
G8 Line-anchored `^<<<SLICE ` and `^<<<END ` are both 0 in `.agent/plan.md` at C1, in `.agent/live_review.md` at C2 and in all three files C3 writes, against a CONTROL of 2 and 2 over the COMMITTED C0a blob. `git diff --name-only 5ee3024b..f0254e78` names 7 paths, none under `docs/`, `packages/` or `tests/` and none of `.agent/context.md`, either inventory file or the nine forbidden `apps/` paths; the range path set MINUS the change set is EMPTY and the change set MINUS the range is exactly `.agent/handoff.md`. C0a through C3 are each SINGLE-PARENT with insertions 451, 261, 22, 4 and 266 read from `git diff --numstat` and not from `git commit`'s summary, each under the 500 AGENTS.md DECISION F104 D1 sets, and those five numbers agree cell for cell with the `+/-` column of the tables above. `git ls-files .remedy-wt` is 0 and `git ls-files` over the zip glob is 0. THE REFLOG, SCOPE this round's 5 entries C0a through C3 and FIELD the operation prefix before the first colon of `git reflog --format=%gs`, reads `commit` throughout, so `amend` 0, `rebase` 0 and `cherry` 0. Every SHA-shaped token in the C0a blob, extracted word-bounded at 7 to 40 hex characters: 21 occurrences, 10 distinct, 9 of type `commit` and 1 of type `blob`, FAILING SET EMPTY.
G9 Ordered after C4 and run there; its real outcome is in this round's final message, and the pushed tips are the reviewer's to measure at the next gate.

## Authored-text proofs
Both slices were extracted PROGRAMMATICALLY out of the COMMITTED C0a blob by their marker LINES and applied unretyped, and no marker line reached a target file (G8). The disk-to-disk comparisons that the self-drive protocol substitutes for the hash stamp are G1's four-way sha256 equality over the block itself, G3's plan equality with its negative control, and G4's two independent append readers with theirs.
`.agent/decisions.md` grows at C3 by text I authored under S3, so no equality gate is ordered over it and none is reported (constraint 8).

## Deviations & assumptions
1. S1 orders BOTH a NARROW local reply type rather than the DOM `Response` AND a default naming the global `fetch`. `fetch` itself is `(input, init) => Promise<Response>` and is not assignable to a one-parameter `DecisionSendFunction`, so the default is an inline arrow that NAMES `fetch` and passes the request's own four values through unchanged — no adapter object, no wrapper module. That is the conservative reading satisfying both clauses; G7 quotes the signature it produced.
2. S2 says "assert AT LEAST", so I added one property beyond its list: a 429 mapping to refused CARRYING 429, so a rate-budget refusal cannot be read as a credential problem. Ten tests in the file. A widening of an "at least", not a departure from the order.
3. G6 deliberately states no target. I chose `: "refused"` and report its measured count of 1 above. No SHORTER unique candidate exists: `"refused"` alone occurs 2 times, in the union type and in the mapping, and `"accepted"` likewise occurs 2 times.
4. C0a and C0b were committed while `.agent/plan.md` still described R30, because constraint 4 fixes C1 as the FIRST substantive commit. That sits against the AGENTS.md Commit Gate's plan-currency item; the block's ordering wins under constraints 1 and 4, and this line is the declaration.
5. The C4 row's `+/-` reads `self-referential`, under the handback template's own `## Commits` self-reference exception. G8 orders insertion counts over C0a..C3 only, and a predicted numeral for the commit being written would be an unmeasured value.
6. SCRATCH I CREATED AND OWN, both under `.remedy-wt/` and neither tracked: the worktree `.remedy-wt/f031-r31-red` and the extractor output directory `.remedy-wt/f031r31-extract/`, each removed BY ITS EXACT PATH. I deleted nothing I did not create (constraint 12).
7. NO CONTRADICTION FOUND in the block: every gate resolved against something real on disk and every ordered numeral reproduced. Nothing calls `decisionSubmit.ts` yet — that is the block's own design and R32's work, not an omission here.
8. THE COMMIT SEQUENCE WAS EXACTLY C0a, C0b, C1, C2, C3, C4 — no extra commit, none dropped, none reordered — and no amend, rebase, cherry-pick, force-push, branch deletion, merge or pull request occurred.

## Next
The next session reads `.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule 2.
THE R31 VERDICT IS UNRECORDED and is owed by the next round's ledger commit (DECISION F085 D9).
R32 is T003's LAST wiring round — the server token threaded to the card, the nonce minted, this module called on an answer click, the disabled buttons enabled — and it is the FIRST round that falsifies the three "nothing posts yet" sentences in `decisionCard.ts`, `decisionAnswer.ts` and `DecisionInboxCard.tsx`.
