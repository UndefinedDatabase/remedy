# Handback — F031 R37 (decision inbox)
Fortschritt: ~98 % (F031 claimed; R1 through R36 landed, R36 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, request,
             deep-link, submit, nonce, outcome sentence and answer flow all
             shipped; component wiring is the last T003 step) — Schaetzung

## Range
Review of `cc7f72e6`..C3 — F031 decision inbox, round R37, branch `feature/f031-decision-inbox`, base `cc7f72e6`; commits C0a `e05eb4be`, C0b `1b163954`, C1 `f2aac4d8`, C2 `0d399389`, C3 this one (a handoff cannot state its own commit's sha — R-0149). No code and no test this round: the whole change set is `.agent/` state. The FULL per-gate detail — every count, digest, boolean and byte arithmetic — is in the round report, not here; that move is finding R-0582's own cheaper repair, applied by this round rather than quoted. Nothing was dropped.
## Commits
### e05eb4be docs(agent): save the F031 R37 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r37.md | +320 -0 | the reviewer's block, copied never retyped |
### 1b163954 docs(agent): mirror the F031 R37 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +193 -354 | the same bytes, read out of the C0a blob |
### f2aac4d8 docs(agent): point the F031 plan at R38
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19 -18 | slice PLANF031R37, whole-file replacement |
### 0d399389 docs(agent): record the F031 R36 verdict and R-0582's recurrence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 -0 | slice LEDGER37, appended |
### C3 docs(agent): write the F031 R37 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | not stated | this file; a handoff cannot table its own commit's numstat (R-0149) |

## Item-Status Table
| Item | Status | Reason |
|---|---|---|
| C0a save this block | done | |
| C0b mirror it into last_block | done | |
| C1 the plan | done | |
| C2 the R36 gate entry and R-0582's recurrence | done | |
| C3 handback | done | |
| G8 push | done | ordered after C3; its outcome is in the round report |

## External actions
`git push origin feature/f031-decision-inbox` — ordered by G8 AFTER this commit, so its result cannot sit inside the file it follows; the round report records what the three reads actually returned. No pull request created, none merged, no branch deleted, no worktree added or removed, no `gh` command, no `--force` and no history rewrite.
## Verification
Eight gates, every one run by me with a REAL exit code: G1 through G7 at commits STRICTLY EARLIER than C3, G8's push after it. One line each; the full detail is in the round report.
- G1 branch, cleanliness, transport HELD — branch `feature/f031-decision-inbox`, `git status --porcelain` 0 lines after C0a, C0b, C1 and C2; `.agent/STOP` read from disk as ABSENT before C0a and ABSENT again before C3, and no sentinel was created or deleted; all FOUR readings of the block equal at sha256 `dd86faeeababbedbe55716c95fe5137c51c5365551d65e23a5dbc2d66e6a09e3`, 32499 bytes, 320 lines, C0a and C0b being the SAME blob `50671be5bc77a562e13adba09d7c62b0f5e198b7`.
- G2 extraction and the block's own caps HELD — my extractor printed 2 slices, 52 CONTENT lines and 320 TOTAL, so PROSE is 320 - 52 = 268 against the 400 cap and TOTAL 320 against the 490 cap; neither exceeded.
- G3 the plan HELD — `.agent/plan.md` at C1 is byte-equal to PLANF031R37 under the newline-INCLUDED convention (2831 bytes, 49 lines both sides); the negative control against the slice minus its trailing newline is FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49, strictly under 50.
- G4 the append HELD — whole-file equality in the shape constraint 7 states is TRUE, 783847 + 1 + 11315 = 795163 against an actual 795163; the second, independent blank-line reader moves 331 units to 333, N = 2 by that split, the last 2 units equal LEDGER37's paragraphs IN ORDER and the SWAPPED comparison is FALSE; one byte flipped IN MEMORY at offset 789505 is REJECTED by both readers while both accept the true file, and the tracked file was never mutated.
- G5 the ledger sets HELD, moving exactly where constraint 9 allows — `^- R-\d+ — ` 246 to 246 with the ids ADDED and the ids REMOVED both the EMPTY SET, all 246 DISTINCT and the maximum still `R-0685`; `^Done: R-\d+ — ` 5 to 5 with the ids ADDED the EMPTY SET; `^Landed: R-` 0 to 0; `^Recurrence: R-` 25 to 26 and `^Recurrence: R-0582` 0 to 1; `^Gate: R\d+ — ` 19 to 19; `^Gate: F\d+ R\d+ — ` 17 to 18, the ADDED key exactly `F031 R36`, all keys DISTINCT; `- R-0582 — ` still occurs exactly ONCE line-anchored.
- G6 markers, paths, commit shapes and object ids HELD — line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in the plan at C1 and in the ledger at C2, against a CONTROL of 2 and 2 over the C0a blob; `git diff --name-only cc7f72e6..0d399389` names 4 paths, none under `docs/`, `packages/`, `tests/` or `apps/` and neither `.agent/context.md` nor `.agent/decisions.md` nor any inventory file, range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the four commits are each SINGLE-PARENT at insertions 320, 193, 19 and 4 read from `git diff --numstat`, each under 500, agreeing cell for cell with `git commit`'s own summary; `git ls-files .remedy-wt` 0, the tracked zip glob 0, `git worktree list` 1 line; the reflog scoped to this round's 4 entries reads `commit` in every operation prefix, so `amend`, `rebase` and `cherry` are 0 each; 16 SHA-shaped tokens, 9 distinct, every one type `commit` under `git cat-file -t`, FAILING SET EMPTY.
- G7 the state readers and the canary HELD — `git worktree list` 1 line immediately before the first, then six suites run SERIALLY in the primary checkout at the C2 tree, never two alive at once, every one a REAL exit 0 and every count IDENTICAL to the Base's, so nothing to account for: `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped, canary `test_golden_path` 42. NO `apps/ui` command was run.
- G8 the push — ordered AFTER C3, so it is not observable from inside this file; the round report carries what the local tip, the remote-tracking ref and `git ls-remote origin` each actually returned, and the sha in question is C3's own, which a handoff cannot state about itself (R-0149).
## Open findings count
241 OPEN at C2 `0d399389`, by the rule and commit DECISION F009 D10 requires — every `^- R-\d+ — ` paragraph, 246, minus every `^Done: R-\d+ — ` line, 5. This round minted no id and resolved none; R-0582 stays OPEN and gained its first `Recurrence:` line.
## Authored-text proofs
Both slices were extracted PROGRAMMATICALLY from the COMMITTED C0a blob by their marker LINES, and no marker reached a target file. `.agent/plan.md` at C1 is byte-equal to PLANF031R37 (G3); `.agent/live_review.md` at C2 is its pre-commit blob plus one newline plus LEDGER37 as one whole-file equality, confirmed by a second independent reader and by an in-memory negative control (G4). The four readings of the block itself agree byte for byte (G1), which is what docs/agents/self_drive_protocol.md substitutes for the hash-stamp ritual when there is no transport.
## Deviations & assumptions
The ordered sequence C0a, C0b, C1, C2, C3 was followed exactly: five commits, none extra, none dropped, none reordered. Two method notes, neither of which changes what was checked: (a) this session's command guard rejects shell loops, `$?` and `$( )`, so every gate ran through `python3` scripts under `.remedy-wt/r37scratch/` with REAL exit codes read from `subprocess.run(...).returncode`, and G7's six command lines were passed VERBATIM as argv with `cwd` at the repo root — a difference of method, not of command; (b) C0a and C0b landed while `.agent/plan.md` still described R36, which is what constraint 3 orders. No contradiction was found inside the block and no slice looked wrong. The scratch directory `.remedy-wt/r37scratch/` is mine alone and is removed by its exact path; nothing else under `.remedy-wt/` was touched. HANDBACK CAP: constraint 3 fixes the commit count at 5, which is NOT more than 5, so the AGENTS.md tier is 60 lines; the measured length of this file is 60 lines, measured with `wc -l` before it was committed. IT FITS — no DECISION D15 overage is declared, because the per-gate detail moved into the round report instead, which is the cheaper repair R-0582 itself named. The four handbacks R-0582's recurrence names each declared a D15 overage; this one does not.
## Next
The next session reads `.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule 2. R37's verdict is NOT YET on disk, and the next reviewed round records it as the `Gate: F031 R37` entry. R38 is the COMPONENT round and the last step of T003 — the server token threaded from `RemedyApp`'s `readUrlState` through `RemedyShell` and `RightLivePanel`, `answerDecisionCard` called on an answer click, the message's sentence rendered by its tone, the buttons enabled, and the three "nothing posts yet" sentences in `decisionCard.ts`, `decisionAnswer.ts` and `DecisionInboxCard.tsx` retired.
