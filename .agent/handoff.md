# Handback — F009 R28 (the route-walking 405 proof; T003 closes)

Branch `feature/f009-single-write-channel`. Round base `a164317b`, read at step 0.

Fortschritt: ~98 % (T001 gebaut · T002 gebaut · T003 gebaut: beide Kommandos
             dispatchen, melden sich auf dem SSE-Strom, sind import-seitig
             eingezäunt und jede andere mutierende Route ist begangen und
             beweisbar 405; offen bleiben nur Integrations-Gate und Closure) —
             Schätzung

## Range
Review of `a164317b`..`HEAD`.

## Commits
### f9f688d7 docs(state): save the F009 R28 block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r28.md | +431/-0 | C0a, the block byte-for-byte |
### 25d80e3a docs(state): mirror the F009 R28 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +273/-280 | C0b, written from the committed C0a blob |
### 3453b271 docs(state): set the plan to the F009 R28 route-walk round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +13/-13 | C1, PLANF009R28 |
### 72da8f6c docs(review): register R-0643 against the R27 block gate
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2, FINDING643, based on the round base |
### 4288bc91 docs(review): record the R27 verdict as PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C3, LEDGER28, based on **C2** |
### 51caddcb docs(decisions): rule F009 D25 on the derived route walk
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +14/-0 | C4, DECISION25, based on the round base |
### aa2b9048 test(ui-server): walk every served route and prove the 405 discipline
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_command_channel.py | +135/-0 | C5, the WALK pair |
### C6 docs(state): write the F009 R28 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-referential | C6 writes this file; its numstat is in the round report (item 14) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |

## External actions
`git worktree add .remedy-wt/r28wt aa2b9048 --detach` — created for G10. `git worktree remove --force` + `git worktree prune` — done before C6; `git worktree list` reads 1. `git push` after C6 — see the round report. No `gh` command, no PR created.

## Verification
- G1 — `.agent/STOP` ABSENT before C0a and before C6; branch `feature/f009-single-write-channel`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C4, C5. Base `a164317b3ff9a6476536a520d54fbc51a6c1c76c`.
- G2 — C0a, C0b and the received block are all sha256 `53523735…cd7500`, 35494 bytes, 431 lines; all three byte-equal. C0b written from the committed C0a blob.
- G3 — script-extracted from the C0a blob by marker line: aggregate 6 slices over 189 CONTENT lines; TOTAL 431, PROSE 242 — both re-measure to constraint 8's numerals, under D6's 490 and D5's 400.
- G4 — `cmp` plan vs PLANF009R28 EXIT 0, both sha256 `d8764adc…45ad29`; negative control vs `.agent/context.md` EXIT 1; `wc -l` 37 (cap 50); `^## Goal$` 1, `^## Next Steps$` 1.
- G5 — all three appends: reader (a) prefix+remainder and reader (b) last-N-paragraphs-in-order both ACCEPT the true file and both REJECT an equal-length printable-byte flip in the FIRST appended paragraph. N counted by script: FINDING643 1, LEDGER28 1, DECISION25 7. FINDING643 based on base, 544465→546975 bytes / 1124→1126 lines. LEDGER28 based on **C2**, 546975→552059 bytes / 1126→1128 lines. DECISION25 based on base, 480292→483709 bytes / 6939→6953 lines.
- G6 — line-anchored: base entries 208 all DISTINCT, `Done:` 3, `Landed: ` 0, `Gate: R` 27 over 27 DISTINCT, `Gate: R28` 0, `- R-0643` 0, max registered R-0642, open 205. C2: entries 209 DISTINCT, `- R-0643` 1, max R-0643, open 206. C3: `Gate: R` 28 over 28 DISTINCT, `Gate: R28` 1, open 206. Open = `^- R-\d+ — ` minus `^Done: R-\d+ — ` (DECISION F009 D10), measured at those three commits.
- G7 — WALK pair, whole-line and indent-agnostic AGREEING at every reading: base FROM 1 / TO 0; C5 FROM 1 / TO 1. Base read via `git show` into `.remedy-wt/`. My script printed `TO contains FROM: true`; no FROM-zero count ordered.
- G8 — ORDERED EQUALITY holds: the 135 lines C5's diff ADDS equal the applied slice's lines IN ORDER as a list compare, 0 removed. `git show --numstat` reads 135/0 — the reviewer's measurement reproduced, no difference to flag.
- G9 — serial, primary checkout: ruff EXIT 0 "All checks passed!"; `test_command_channel.py` EXIT 0, 100 passed; canary EXIT 0, 42 passed; four-path group EXIT 0, 527 passed.
- G10 — disposable worktree at C5; unmutated baseline EXIT 0 / 100 passed / 0 failures first. Each FROM reads 1 whole-line and 1 indent-agnostic; (a)'s second line alone reads 3, which is why its FROM spans two lines. Under `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf` with no `-k`: (a) 3 failed = the 3 ids ordered; (b) 1 failed = the id ordered; (c) 1 failed = `test_the_walk_knows_every_route_the_source_dispatches`. Every set EXACT, nothing to flag. Each reverted and byte-equal to its C5 blob. `git worktree list` 1 line before C6.
- G11 — range base→C5 lists exactly the declared paths, set difference EMPTY both directions, 0 paths beginning `packages/`, `apps/` or `docs/`. Every commit ONE parent; `git show --numstat` and `git diff --numstat` AGREE on every cell and every cell equals this file's `+/-` column. Insertions 431, 273, 13, 2, 2, 14, 135 — each under the 500 cap. Leading `<<<SLICE ` and `<<<END ` read 0 in all four slice targets; `git ls-files .remedy-wt` 0. This round's 7 reflog rows all classify `commit`; `amend`, `rebase`, `cherry` each 0; no total asserted over the whole reflog.
- G12 — this file; its `wc -l` is in the round report.

## Authored-text proofs
PLANF009R28: `.agent/plan.md` at C1 `cmp`-equal to the committed slice, EXIT 0, with a differing negative control. FINDING643, LEDGER28, DECISION25: applied as byte-exact appends, both readers ACCEPT, flip REJECTED. WALK_FROM/WALK_TO: the applied pair reproduces C5's added lines under ordered equality. Every slice was extracted from the committed C0a blob by a script keyed on its marker lines; no slice was hand-transcribed and no marker line reached a target file.

## Deviations & assumptions
None. The ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6 was followed exactly, with no extra commit, no dropped commit and no reordering.

## Next
Review this round; then the integration gate per docs/agents/integration_gate.md before F009 closure. The next session's first action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — before rule 2. Next free finding id R-0644.
