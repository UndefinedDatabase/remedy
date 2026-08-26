# Handback — F031 Decision inbox, round R29

Branch: `feature/f031-decision-inbox`. Base `26327a43`. Commits this round: 6
(C0a `ef3fbfb1`, C0b `9d05c933`, C1 `41f4e3dd`, C2 `16d0240e`, C3 `10c3b40c`, C4 this one).
Handoff line cap tier: 100 (AGENTS.md `### handoff.md`, the >5-commit table tier).

Fortschritt: ~94 % (F031 claimed; R1 through R28 landed, R28 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, deep-link
             and request seams shipped and now hardened, wiring open)
             — Schaetzung

## Range
Review of `26327a43`..HEAD.

## Commits
### ef3fbfb1 docs(agent): save the F031 R29 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r29.md | +451/-0 | the reviewer's R29 block, copied from `.remedy-wt/f031-r29.md`, never retyped |

### 9d05c933 docs(agent): mirror the F031 R29 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +228/-228 | R28's block replaced by R29's, byte-identical to the C0a blob |

### 41f4e3dd docs(agent): point the F031 plan at R29
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21/-20 | whole-file replacement by slice PLANF031R29 |

### 16d0240e docs(agent): record the F031 R28 verdict and register two findings
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | LEDGER29 appended: the F031 R28 gate entry plus R-0684 and R-0685 |

### 10c3b40c feat(ui): refuse a blank decision answer and name the send target
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionAnswer.ts | +30/-13 | S1 trim refusal and trimmed send; S3 header repair |
| apps/ui/src/api/decisionAnswer.test.ts | +17/-0 | S1 tests: blank refusal, trimming, inner spacing kept |
| apps/ui/src/api/decisionSend.ts | +31/-17 | S2 `DecisionSendTarget` object parameter; S3 header repair |
| apps/ui/src/api/decisionSend.test.ts | +42/-5 | call sites moved to the object; field-order and blank-answer tests |
| .agent/decisions.md | +44/-0 | S4 DECISION F031 D14 |

### C4 docs(agent): write the F031 R29 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | a handoff cannot table the commit that writes it (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| S1 | done | |
| S2 | done | |
| S3 | deviated | widened within the two named files: the builder DOCSTRINGS carried the same stale count and claim, so they were repaired too |
| S4 | done | |
| push | done | ordered after C4; outcome carried by G9 to the reviewer |

## External actions
- `git worktree add --detach .remedy-wt/r29-red-wt 10c3b40c` — created, path did not exist.
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r29-red-wt` — removed by that exact path; `git worktree list` 1 line after.
- `git push origin feature/f031-decision-inbox` — ordered after C4. That push's outcome is not a value of any file this round writes: the reviewer measures the pushed tips at the next gate and records them in the R29 entry of `.agent/live_review.md`.
- No PR created, no branch deleted, nothing merged, no force push, no history rewrite.

## Verification
- G1 PASS. `git branch --show-current` = `feature/f031-decision-inbox`. `.agent/STOP` absent from disk before C0a and again before C4. `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3. All FOUR readings equal: sha256 `6e361d0c24739e00b5cfcb29cdf8be47c4077c65357cc095542d3124be038609`, 41552 bytes, 451 lines. C0a and C0b blob id both `3e9206dd10a3a0445df9b7ca0581469cb890d984`.
- G2 PASS. Extractor over the committed C0a blob: 2 slices, 52 CONTENT lines, 451 TOTAL, PROSE = 451 − 52 = 399. Under both caps (490 TOTAL, 400 PROSE).
- G3 PASS. `.agent/plan.md` at C1 byte-equal to PLANF031R29: 2734 bytes, 47 lines, both sides; convention newline-INCLUDED. Negative control (slice minus trailing newline) FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 47 < 50.
- G4 PASS. Reader (a), constraint 8's shape: 717469 + 1 + 12046 = 729516 against actual 729516, EQUAL True. Reader (b), blank-line split, trailing newlines rstripped on BOTH sides: units 318 → 321, N = 3, last 3 units equal LEDGER29's 3 paragraphs IN ORDER. Negative control, one byte flipped in memory at offset 723493 inside the appended text: both readers reject the mutant, both accept the true file.
- G5 PASS. `^- R-\d+ — ` 244 → 246; ADDED exactly {R-0684, R-0685}; REMOVED empty; all 246 DISTINCT; maximum `R-0685`. `^Done: R-\d+ — ` 5 → 5, ids ADDED empty. `^Recurrence: R-` 22 → 22. `^Landed: R-` 0 → 0. `^Gate: R\d+ — ` 19 → 19. `^Gate: F\d+ R\d+ — ` 9 → 10, ADDED key exactly `F031 R28`, all keys DISTINCT. §3 item 10 open set at C2 = 241. `git diff --name-only 16d0240e..10c3b40c` does NOT name `.agent/live_review.md`.
- G6 PASS (red proved). Worktree `.remedy-wt/r29-red-wt` at `10c3b40c`. Unmutated: REAL exit 0, 23 files, 375 tests. Bytes about to change, occurrences of the refusal expression in that file: 1. Mutated (refusal reads the RAW answer text; the sent value stays trimmed): REAL exit 1, 2 failed / 373 passed, the failures being `buildDecisionResolveCommand > refuses a whitespace-only answer, which the server accepts and writes ONCE` and `buildDecisionSendRequest > propagates the blank-answer refusal, so no whitespace answer is sendable`. Restored byte-identically; that worktree's `git status --porcelain` 0; removed by its exact path; `git worktree list` 1 line after.
- G7 PASS. `decisionAnswer.ts` at C3: `.trim()` occurs 1, the refusal line reads `if (trimmedAnswer === "") {`, the raw-text comparison `answerText === ""` occurs 0, `fetch(` 0. `decisionSend.ts` at C3: signature is `buildDecisionSendRequest(target: DecisionSendTarget, model: DecisionCardModel, answerText: string, clientNonce: string): DecisionSendRequest | null`; `fetch(` 0, `Date.now` 0, `useState` 0. `four bodies` 0 across BOTH modules. `git worktree list` 1 line immediately before the suites; run SERIALLY. `npm run typecheck` REAL exit 0, zero diagnostics on stdout and stderr. `npm run test:unit` REAL exit 0, 26 files (unchanged) and 400 tests; `decisionCard.test.ts` 36, `decisionFilter.test.ts` 20, `decisionOrder.test.ts` 16, `decisionFocus.test.ts` 7 all unmoved; `decisionAnswer.test.ts` 17 → 20 (+3), `decisionSend.test.ts` 10 → 12 (+2). Python, all REAL exit 0: `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed 4 skipped, `test_golden_path` 42 — every count identical to the reviewer's base reading, no difference to account for.
- G8 PASS. Line-anchored `^<<<SLICE ` and `^<<<END ` 0/0 in the plan at C1, `live_review.md` at C2 and all five files C3 writes; CONTROL over the C0a blob 2/2. `git diff --name-only 26327a43..10c3b40c` names 9 paths, none under `docs/`, `packages/` or `tests/`, none of the forbidden named set, no inventory file; range MINUS change set EMPTY, change set MINUS range exactly `.agent/handoff.md`. Each of C0a..C3 single-parent, insertions 451, 228, 21, 6, 164, each under 500 (AGENTS.md DECISION F104 D1); those numbers agree cell for cell with the `+/-` column above, derived from `git diff --numstat`, not from `git commit`. `git ls-files .remedy-wt` 0; `git ls-files *.zip` 0. Reflog scoped to this round's 5 entries (C0a..C3), field = the operation prefix before the first colon of `git reflog --format=%gs`: all `commit`; `amend` 0, `rebase` 0, `cherry` 0. SHA-shaped tokens in the committed C0a blob (word-bounded 7–40 hex): 22 tokens, 10 distinct, 9 `commit` and 1 `blob`, FAILING SET EMPTY.
- G9 ordered after C4; see External actions.

## Authored-text proofs
Both slices were extracted programmatically from the COMMITTED C0a blob by marker line and applied without retyping. PLANF031R29 → `.agent/plan.md` at C1: disk-to-disk byte-equal, 2734 bytes both sides (G3). LEDGER29 → `.agent/live_review.md` at C2: whole-file equality plus an independent order-sensitive paragraph reading, both with a passing negative control (G4). The block itself: four readings equal at one sha256, one git blob id (G1).

## Deviations & assumptions
1. ORDERING: at C0a and C0b `.agent/plan.md` still described R28, so AGENTS.md's Commit Gate item 1 was met only from C1 onward. This is the block's own ordered sequence (constraint 4 makes C1 the first substantive commit because this round writes the finding ledger); no commit was added, dropped or reordered.
2. S3 WIDENED WITHIN THE TWO NAMED FILES. The spec names the module OPENING comments. The builder DOCSTRINGS carried the same defect — `decisionAnswer.ts` said "for exactly four reasons, each of them a body the server would refuse anyway" (a count AND the false mirror claim S3 orders retired) and `decisionSend.ts` said "the four bodies ... and for two more of its own". Both were repaired in the same modules; nothing outside the change set was touched. "State no numeral for either set" was also read conservatively wide: the count of `decisionSend.ts`'s OWN refusals went too, and both refused sets are now NAMED.
3. NAMING ASSUMPTION: S2 says "name the object for what it is — the addressed job and the credential that opens its door". The exported interface is `DecisionSendTarget`, matching the module's `DecisionSend*` family and AGENTS.md's 2–4-word rule, with its doc comment naming both halves and its fields `jobId` and `serverToken` carrying them. A name spelling out both nouns would have been longer than the rule allows.
4. `docs/` WAS NOT UPDATED although this round changes browser-visible behaviour. Constraint 11 forbids it; the plan routes it to the integration-gate round. Declared rather than silently skipped.
5. S2 COMPLETENESS: `buildDecisionSendRequest` has no caller outside `decisionSend.ts` and `decisionSend.test.ts` — grepped over `apps/**` for `.ts`/`.tsx`, 7 hits, all in those two files. No other caller was found, so `npm run typecheck` exit 0 IS the proof the signature change is complete.
6. G6's mutant fails TWO tests, not one: `decisionSend.test.ts` pins the composed refusal as well. The block states no number; both names are reported.
7. TOOLING: this sandbox's Bash guard rejects `$(...)`, `$?` and shell loops, so every measurement ran from a gitignored `.remedy-wt/r29-*.py` script via `subprocess` with real exit codes captured. No gate command was altered — G6's vitest line was run exactly as written. No contradiction was found in the block; every slice was applied byte for byte.

## Findings
Open findings by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — measured at C2 `16d0240e`: 241 (246 − 5). This round MINTED R-0684 and R-0685 and RESOLVED none. The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413, R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684 and R-0685; R-0495 and R-0574 are the two Highs.

## Next
1. The next session reads `.agent/STOP` from disk as Phase 1 rule 1, BEFORE the Open PR Gate as rule 2.
2. The R29 verdict is UNRECORDED and is owed by the next round's ledger commit (DECISION F085 D9).
3. Then T003's WIRING round, which owns the only `fetch` and the only component edits in this seam.
