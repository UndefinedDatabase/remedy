# Handback — F009 R29 (the integration gate; the R28 verdict, R-0644, the D25 correction)

Branch `feature/f009-single-write-channel`. Round base `986b40ee5784043a1f75c87d809892b641cb34d3`, read at step 0.

Fortschritt: ~98 % (T001 gebaut · T002 gebaut · T003 gebaut und verifiziert:
             beide Kommandos dispatchen, melden sich auf dem SSE-Strom, sind
             import-seitig eingezäunt und jede andere mutierende Route ist
             begangen und beweisbar 405; offen bleiben nur dieses
             Integrations-Gate und die zwei Closure-Runden) — Schätzung

## Range
Review of `986b40ee`..`HEAD`.

## Commits
### 0c9a5a5c docs(state): save the F009 R29 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r29.md | +271/-0 | C0a, the block byte-for-byte |
### 4c833e42 docs(state): mirror the R29 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +171/-331 | C0b, written from the committed C0a blob |
### d2671f7b docs(state): point the plan at the F009 integration gate
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +12/-10 | C1, PLANF009R29 |
### d86146c2 docs(review): register R-0644 against the R28 block inventory
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2, FINDING644, based on the round base |
### 5b497416 docs(review): record the R28 verdict as PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C3, LEDGER29, based on **C2** |
### 30203bb5 docs(decisions): correct the F009 D25 route inventory
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +6/-0 | C4, CORRECTD25, based on the round base |
### 62079678 docs(state): record the F009 R29 integration gate evidence
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f009_r29/attribution.txt | +22/-0 | C5, per-id attribution, both sets |
| .agent/gate_f009_r29/base_failed.txt | +6/-0 | C5, base FAILED list, sorted |
| .agent/gate_f009_r29/base_only.txt | +6/-0 | C5, the `comm -23` set |
| .agent/gate_f009_r29/branch_failed.txt | +0/-0 | C5, branch FAILED list, empty |
| .agent/gate_f009_r29/branch_only.txt | +0/-0 | C5, the `comm -13` set, empty |
| .agent/gate_f009_r29/summary.txt | +51/-0 | C5, both exit codes, wall times, tails, dist digests |
### C6 docs(state): write the F009 R29 handback
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
`git worktree add -b tmp/base-gate-f009r29 .remedy-wt/basegate ce49348b8f5b0374417f5b6c47d8c04966e7108e` EXIT 0 — ON A BRANCH, never detached, created for G8. `git worktree remove --force` EXIT 0, `git worktree prune` EXIT 0 and `git branch -D tmp/base-gate-f009r29` EXIT 0, all before C6; `git worktree list` then reads 1 line. `git push` after C6 — see the round report. No `gh` command. No PR created.

## Verification
- G1 — `.agent/STOP` ABSENT before C0a and again before C6; branch `feature/f009-single-write-channel`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C4 and C5. Round base `986b40ee5784043a1f75c87d809892b641cb34d3`. Scratch probe: `~/.cache/remedy-gate-f009-r29/` IS writable, so no substitution was needed.
- G2 — the C0a blob, the C0b blob, both on-disk copies and the reviewer's emitted original still on disk at `.remedy-wt/f009-r29.md` are all sha256 `f0df008b…b057d32`, 28469 bytes, 271 lines; all five byte-equal by a real disk-to-disk comparison, not by a recorded digest. C0b was written from the committed C0a blob.
- G3 — script-extracted from the COMMITTED C0a blob by marker line: aggregate 4 slices over 46 CONTENT lines. PLANF009R29 2180 B / 39 lines, FINDING644 3415 B / 1, LEDGER29 6177 B / 1, CORRECTD25 1320 B / 5. Constraint 8 re-measured from that blob: TOTAL 271 and PROSE 271 − 46 = 225, both agreeing with the block, under D6's 490 and D5's 400. Paragraphs counted by script: FINDING644 1, LEDGER29 1, CORRECTD25 3, so constraint 6 holds.
- G4 — `cmp` of the plan at C1 against PLANF009R29 EXIT 0, both sha256 `940d103c…26eefe`; negative control against `.agent/context.md` EXIT 1, differing at byte 3; `wc -l` 39 against the 50-line cap; `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 — all three appends under both readers: (a) the base blob is a byte-exact PREFIX and the remainder equals one newline plus the slice; (b) N counted BY THE SCRIPT, the last N blank-line units equal to the slice's paragraphs IN ORDER. FINDING644 at C2 on the ROUND BASE, 552059→555475 B / 1128→1130 lines, N 1. LEDGER29 at C3 on **C2**, its base blob reading 555475 B / 1130 lines — the reading a round-base comparison would have got wrong by a whole slice — going to 561653 B / 1132 lines, N 1. CORRECTD25 at C4 on the ROUND BASE, 483709→485030 B / 6953→6959 lines, N 3. In each, an equal-length printable-byte flip in the FIRST appended paragraph makes BOTH readers REJECT while both ACCEPT the true file.
- G6 — line-anchored at line START throughout. Round base: entries 209 all DISTINCT, `Done: R-` 3, `Landed: ` 0, `Gate: R` 28 over 28 DISTINCT keys, `Gate: R29` 0, `- R-0644` 0, max REGISTERED id R-0643, open 206 — every one of the reviewer's base readings reproduced. C2: entries 210 all DISTINCT, `- R-0644` 1, max R-0644, open 207. C3: `Gate: R` 29 over 29 DISTINCT, `Gate: R29` 1, entries 210, max R-0644, open 207. Open by DECISION F009 D10 = entries − `Done:` − `Landed: `.
- G7 — BRANCH RUN `python3 -m pytest -n auto -q` from the repo root: EXIT 0, wall 152.2 s, and the run itself printed `17572 passed, 20 skipped in 151.59s`, so 17592 collected, which is the reviewer's count. `branch_failed.txt` 0 lines. The raw log was written OUTSIDE the repo worktree at `~/.cache/remedy-gate-f009-r29/branch_raw.txt`, 249 lines, uncommitted.
- G8 — BASE RUN in the throwaway worktree at `ce49348b` ON branch `tmp/base-gate-f009r29`: EXIT 1, wall 126.7 s, the run printed `6 failed, 17406 passed, 20 skipped in 126.14s`, so 17432 collected. Parity restored by `shutil.copytree(src, dst, symlinks=True)` for `apps/ui/node_modules` and again for `apps/ui/dist`; all 23 `.bin` entries are real symlinks in the primary checkout and all 23 survived as symlinks in the base worktree. `REMEDY_UI_NO_AUTO_BUILD=1` was set. The recursive sha256 over `apps/ui/dist` reads `2139f2fe…501dc8` BEFORE and `2139f2fe…501dc8` AFTER — EQUAL, so the block's parity criterion is met; see Deviations for what that criterion cannot see. Raw log `~/.cache/remedy-gate-f009-r29/base_raw.txt`, 624 lines, uncommitted.
- G9 — `comm -13` branch-only 0 lines; `comm -23` base-only 6 lines. Branch-only flake-class count 0, and no BLOCKER candidate exists because the branch-only set is empty. All 6 base-only ids are attributed by direct evidence, unconditionally and not on the strength of the parity digests: each fails with `ERROR: React UI not built.` emitted at `packages/orchestration/ui_server.py:3016`, reached because `_frontend_is_stale()` reads True and `_auto_build_frontend()` returns None under `REMEDY_UI_NO_AUTO_BUILD=1`, after which `start_ui_server` calls `sys.exit(1)` and the test's server thread never binds. Missing artifact, per id: an `apps/ui/dist` newer than the throwaway worktree's freshly checked-out `apps/ui/src`. `copytree`/`copy2` PRESERVES the source mtime, measured at 1787375952.935 in both trees right after the copy, while `git worktree add` stamped `apps/ui/src` at 1787376060.806. Controlled proof at `ce49348b` inside that worktree: with `dist/index.html` set older than `src`, `test_server_starts_and_writes_info` FAILS with that exact error, EXIT 1; with the mtime restored and no byte of content changed, it PASSES, EXIT 0. All 6 ids re-run SERIALLY at `ce49348b` EXIT 0.
- G10 — C5 wrote `branch_failed.txt`, `base_failed.txt`, `branch_only.txt`, `base_only.txt`, `attribution.txt` and `summary.txt` into `.agent/gate_f009_r29/`, every one named `.txt` and every one copied AFTER both runs had exited. C5 insertions 85, under the 500-line cap, so no split was needed and no evidence file was truncated. The raw logs stay in the scratch directory and are not committed; their paths and line counts are in G7 and G8.
- G11 — CANARY `python3 -m pytest tests/cli/test_golden_path.py -q -rf` in the PRIMARY checkout, serially, with no other pytest process alive: EXIT 0, and the run printed `42 passed in 20.52s`.
- G12 — the range base→C5 lists exactly the 11 declared paths, the set difference EMPTY in both directions, and 0 paths beginning `packages/`, `apps/`, `docs/` or `tests/` — this round's measure-only constraint as a measurement. Every commit has ONE parent; `git show --numstat`, invoked with no `--` before the SHA, and `git diff --numstat` AGREE on every cell, and every cell equals this file's `+/-` column compared cell by cell. Pre-handback insertions 271, 171, 12, 2, 2, 6 and 85, each under the 500 cap. Leading `<<<SLICE ` and `<<<END ` read 0 LINES in `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md`; `git ls-files .remedy-wt` reads 0. This round's 7 reflog rows all classify as `commit`, with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog.
- G13 — this file; its `wc -l` and its own numstat are in the round report.

## Authored-text proofs
PLANF009R29: `.agent/plan.md` at C1 is `cmp`-equal to the committed slice, EXIT 0, with a differing negative control. FINDING644, LEDGER29 and CORRECTD25: applied as byte-exact appends of one newline plus the slice, both readers ACCEPTing the true file and both REJECTing an equal-length printable-byte flip in the first appended paragraph. Every slice was extracted from the COMMITTED C0a blob by a script keyed on its `<<<SLICE ` and `<<<END ` marker lines and applied programmatically; nothing was hand-transcribed and no marker line reached any target file.

## Deviations & assumptions
The ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6 was followed exactly — no extra commit, no dropped commit, no reordering. Two readings are handed to the reviewer to rule on. (1) `REMEDY_UI_NO_AUTO_BUILD=1` DID NOT HOLD. Every file under the base worktree's `apps/ui/dist` carries mtime 1787376153.535, about 81 s into a run that began at 1787376072, while the copy had left them at 1787375952.935. The tree was rewritten mid-run with byte-identical content, so the recursive CONTENT digest G8 orders comes back EQUAL and reports nothing — yet mtime is exactly the property `_frontend_is_stale()` reads, and it is what decided all 6 base-only ids. That is the R-0169 class recurring, and the ordered digest cannot see it. I minted no id for it: minting is the reviewer's. (2) Beyond the ordered evidence I re-ran the 6 base-only ids serially at `ce49348b` and ran one controlled mtime experiment there, both inside the disposable worktree; they strengthen the G9 attribution rather than replace it. No gate was weakened, no test changed, no ceiling raised, and no verdict is issued here.

## Next
Review this round and issue the integration-gate verdict, which is the reviewer's alone. Then closure per docs/roadmap/STATUS_closure_protocol.md in TWO rounds. The next session's first action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — before rule 2. Next free finding id R-0645.
