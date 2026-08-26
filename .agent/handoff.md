# Handback — F031 "Decision inbox", round R28

Branch `feature/f031-decision-inbox`; base `b6ae6f9955a72cc9dd91d4b7a8742028e82f2b3a`
(the R27 handback). Six commits, C0a–C4, exactly the sequence constraint 4 fixes.
Handback tier: 100 lines (AGENTS.md `### handoff.md`, >5 commits).

Fortschritt: ~93 % (F031 claimed; R1 through R27 landed, R27 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command and deep-link
             seam shipped, request seam here, wiring and forms open)
             — Schaetzung

## Range

Review of `b6ae6f9955a72cc9dd91d4b7a8742028e82f2b3a`..`HEAD`.

## Commits

### f211909b docs(agent): save the F031 R28 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r28.md | +451/-0 | C0a: the reviewer's original, copied not retyped |

### 5cbe934a docs(agent): mirror the F031 R28 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +243/-241 | C0b: written from the committed C0a BLOB |

### 29b4c13c docs(agent): point the F031 plan at R28
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19/-20 | C1: whole-file replacement by slice PLANF031R28 |

### 1598aa92 docs(agent): record the F031 R27 verdict and two recurrences
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | C2: LEDGER28 appended, nothing else |

### f22c95f5 feat(ui): build the decision answer's send request as a value
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionSend.ts | +82/-0 | S1: the pure request builder |
| apps/ui/src/api/decisionSend.test.ts | +114/-0 | S2: 10 tests pinning path, method, body, headers |
| .agent/decisions.md | +38/-0 | S3: DECISION F031 D13 |

### C4 docs(agent): write the F031 R28 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C4: this file; a handback cannot table its own commit |

## External actions

`git worktree add .remedy-wt/r28-red HEAD --detach` then
`git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r28-red` — G6 only, by that exact path.
`git push origin feature/f031-decision-inbox`, ordered after C4. THAT PUSH'S OUTCOME IS NOT A
VALUE OF ANY FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate and
records them in the R28 entry of `.agent/live_review.md`. No PR created, no branch deleted,
nothing merged.

## Verification

G1 PASS. `git branch --show-current` = `feature/f031-decision-inbox`. `.agent/STOP` ABSENT on
disk before C0a and again before C4. `git status --porcelain` = 0 lines after each of C0a, C0b,
C1, C2, C3. FOUR READINGS ALL EQUAL — `.remedy-wt/f031-r28.md` before C0a, the C0a blob, the C0b
blob, `.agent/last_block.md` off disk after C0b — each 42098 bytes, 451 lines, sha256
`2688e6ad3c9880d0122a4e69ae214a543be1a841894be2ebc8baae00c2d1120f`; C0a and C0b resolve to the
SAME blob id `1b854b72175b17bf72e9cd4db6803d3d8c72db9f`.

G2 PASS. My extractor over the committed C0a blob printed 2 slices (PLANF031R28, LEDGER28),
51 CONTENT lines, 451 TOTAL, so PROSE = 451 − 51 = 400. TOTAL 451 ≤ 490 (F085 D6); PROSE 400 is
AT the 400 cap (F085 D5), not over. No disagreement with the reviewer's 400.

G3 PASS. `.agent/plan.md` at 29b4c13c is byte-equal to PLANF031R28: slice 2799 bytes, file 2799
bytes, newline-INCLUDED convention (the slice ends in a newline). NEGATIVE CONTROL: equal to the
slice MINUS its trailing newline = FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 46 < 50.

G4 PASS. Reader (a), the whole-file equality constraint 8 states: TRUE; 705142 + 1 + 12326 =
717469 against an actual 717469. Reader (b), independent: blank-line split moves units 315 → 318;
N = 3, the number MY split measured; the last 3 units equal LEDGER28's 3 paragraphs IN ORDER,
with trailing newlines rstripped on BOTH sides. NEGATIVE CONTROL, in memory only, never on the
tracked file: one byte flipped at offset 711306 (inside the appended text) — both readers REJECT
the mutant, both ACCEPT the true file.

G5 PASS. Base `b6ae6f99` → C2 `1598aa92` in `.agent/live_review.md`: `^- R-\d+ — ` 244 → 244,
ids ADDED and ids REMOVED BOTH the EMPTY SET, all 244 DISTINCT, maximum still `R-0683`;
`^Done: R-\d+ — ` 5 → 5 with the ids ADDED the EMPTY SET; `^Landed: R-` 0 → 0;
`^Recurrence: R-` 20 → 22 with `^Recurrence: R-0419` 0 → 1 and `^Recurrence: R-0429` 0 → 1;
`^Gate: R\d+ — ` 19 → 19 UNCHANGED; `^Gate: F\d+ R\d+ — ` 8 → 9, ADDED key exactly `F031 R27`,
all keys DISTINCT. §3 item 10 open set at C2 = 244 − 5 = 239. `- R-0419 — ` and `- R-0429 — `
each still occur exactly ONCE line-anchored, so neither landed paragraph was edited.
`git diff --name-only HEAD~1..HEAD` over C3 names `.agent/decisions.md`, `decisionSend.ts`,
`decisionSend.test.ts` and NOT `.agent/live_review.md`.

G6 PASS (RED PROVEN). Worktree `.remedy-wt/r28-red` created at a path that did NOT exist, at C3,
vitest run from the PRIMARY `apps/ui` with `--config <PRIMARY>/apps/ui/vitest.config.ts --root
<WORKTREE>/apps/ui src/api/`. UNMUTATED: REAL exit 0, 23 files, 370 tests. Bytes to delete,
counted in that file first: the exact line `      "X-Remedy-CSRF": serverToken,` occurs exactly
1 time (36 bytes; 3925 → 3889). MUTATED: REAL exit 1, 2 failed / 368 passed — this block states
no failure number, and MY run measured 2: `carries the token in BOTH token headers, as ONE
secret per DECISION F009 D11` and `puts the Bearer scheme on the authorization header ONLY`.
Restored byte-identically (equal to the primary's blob), that worktree's `git status --porcelain`
0 lines, removed BY THE EXACT PATH `/home/decodeux/Repos/remedy/.remedy-wt/r28-red`, and
`git worktree list` is 1 line after, naming `/home/decodeux/Repos/remedy`.

G7 PASS. Structure at C3 over `decisionSend.ts`: `fetch(` 0, `XMLHttpRequest` 0, `Date.now` 0,
`Math.random` 0, `useState` 0; `Authorization` exactly 1 and `X-Remedy-CSRF` exactly 1; both
builders imported from `./decisionAnswer` by the line
`import { buildDecisionResolveCommand, jobCommandsPath } from "./decisionAnswer";`.
`git worktree list` 1 line immediately BEFORE the suites. Run SERIALLY, never two alive at once,
every one a REAL exit 0: `npm run typecheck` exit 0, ZERO diagnostics on stdout and stderr;
`npm run test:unit` exit 0 at 26 files (one more than the base's 25, that one being
`decisionSend.test.ts` at 10 tests) and 395 tests, with `decisionAnswer.test.ts` 17,
`decisionCard.test.ts` 36, `decisionFilter.test.ts` 20, `decisionOrder.test.ts` 16 and
`decisionFocus.test.ts` 7 — all five UNMOVED. Python, the six exact command lines: 480; 52; 21;
16; 525 passed with 4 skipped; 42 — every count identical to the reviewer's base reading, so
there is NO difference to account for.

G8 PASS. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0/0 in `.agent/plan.md` at C1,
`.agent/live_review.md` at C2 and all three files C3 writes, against the CONTROL over the C0a
blob at 2/2. `git diff --name-only <base>..C3` names 7 paths, NONE under `docs/`, `packages/` or
`tests/` and none of the forbidden set; range MINUS change set is EMPTY and change set MINUS
range is exactly `.agent/handoff.md`. Per commit, single-parent and INSERTIONS from
`git diff --numstat` (the `+` column only): f211909b 1/451, 5cbe934a 1/243, 29b4c13c 1/19,
1598aa92 1/6, f22c95f5 1/234 — each under 500, and those five numbers fill the `+/-` column of
`## Commits` above and AGREE cell for cell. `git ls-files .remedy-wt` 0; `git ls-files *.zip` 0.
REFLOG, SCOPE = this round's 5 entries so far (C0a–C3; C4 is later than every gate, §3 item 31),
FIELD = the operation prefix before the first colon of `git reflog --format=%gs`: `commit` five
times, so `amend` 0, `rebase` 0, `cherry` 0. SHA-shaped tokens in the committed C0a blob, pattern
`\b[0-9a-f]{7,40}\b`: 24 occurrences, 10 distinct, `git cat-file -t` gives 9 `commit` and 1
`blob`; FAILING SET EMPTY.

G9 ordered after C4; outcome carried to the reviewer per the section above and reported in the
worker's final message.

## Authored-text proofs

Two slices applied, both extracted PROGRAMMATICALLY from the COMMITTED C0a blob by their marker
LINES; no marker line reached a target file (G8). PLANF031R28 → `.agent/plan.md`, disk-to-disk
byte-equal (G3). LEDGER28 → `.agent/live_review.md`, whole-file equality plus an independent
ordered-paragraph reader, both with a negative control (G4). The block states no digest of
itself; the disk-to-disk comparison over four readings is the proof, and the digest I measured is
`2688e6ad3c9880d0122a4e69ae214a543be1a841894be2ebc8baae00c2d1120f`.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
| S1 | done | `decisionSend.ts`, 82 lines, pure |
| S2 | done | `decisionSend.test.ts`, 10 tests |
| S3 | done | DECISION F031 D13 |
| push | done | ordered after C4; outcome carried by G9 to the reviewer |

## Findings

Per §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line, the rule
DECISION F009 D10 requires — the open set is 239, measured at C2 `1598aa92`. This round MINTED
no id and RESOLVED none; R-0419 and R-0429 gained a recurrence each and stay OPEN. The narrower
set, the findings THIS FEATURE must still act on, is the 25 distinct ids `.agent/plan.md` lists
at C1, of which R-0495 and R-0574 are the two Highs.

## Deviations & assumptions

1. NO departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4 exactly, none extra,
   none dropped, none reordered. No amend, rebase, cherry-pick, force-push, branch deletion,
   merge or PR.
2. DECLARED OVERAGE (AGENTS.md DECISION D15): this handback is 198 lines against the 100-line
   tier its 6 commits earn. The mandated content behind it: six per-commit tables, nine gate
   entries carrying ordered numerals, the transport proof over four readings, the two-reader
   append proof, the item-status table and the finding counts. NO section was dropped to fit.
3. ASSUMPTION, reflog scope. G8's reflog reading is scoped to the 5 entries C0a–C3, because the
   block requires every gate to run at a commit STRICTLY EARLIER than C4. C4's own reflog entry
   is therefore outside the scope I report, and it is a plain `commit` like the rest.
4. ASSUMPTION, G6 failure count. The block states no expected number; my run measured 2 failing
   tests and I report the names rather than compare against a number that was not ordered.
5. ASSUMPTION, S1's null ORDER. The spec fixes WHICH inputs answer `null`, not the order the
   guards run in. I check the job id and the token BEFORE calling the body builder, so an
   unsendable request is refused without building a body that would be thrown away. Behaviour is
   identical either way.
6. SCRATCH, by exact path. I created `.remedy-wt/r28scratch/` (the extracted slices, the G6 file
   backup, this handback's draft) and the G6 worktree `.remedy-wt/r28-red`; the worktree was
   removed BY ITS EXACT PATH at G6 and the scratch files are removed BY THEIR EXACT PATHS at the
   close of the round. I deleted nothing I did not create; `git ls-files .remedy-wt` is 0.
7. NO CONTRADICTION FOUND in the block. Every clause I checked resolved: the header spellings
   match the server's own (`Authorization`, `X-Remedy-CSRF` in
   `packages/orchestration/ui_server.py`), and the Base's own readings — 705142 bytes / 1257
   lines, plan 2781 bytes / 47 lines, 244/5/20/0/19/8 — all reproduced before C0a.

## Next

1. The next session reads `.agent/STOP` from disk as Phase 1 rule 1, BEFORE the Open PR Gate as
   rule 2.
2. The R28 verdict is UNRECORDED and is owed by the next round's ledger commit (DECISION F085 D9).
3. T003's WIRING round is UNBLOCKED by DECISION F031 D13 — no design ruling is outstanding.
