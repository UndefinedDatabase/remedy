# Handback — F009 R18 (T003, the record round before round one of DECISION F009 D19)

Feature F009 "The single write channel", round 18, branch `feature/f009-single-write-channel`.
Round base SHA `6101ca205f06ecacf957d6880682437729c99922`. `.agent/STOP` absent before C0a and before C4.
Open findings at C2 by DECISION F009 D10's rule: 200. Max id R-0637. This round minted no id and resolved none.
This round wrote no production code and created no worktree, both measured by G9 rather than asserted.

Fortschritt: ~73 % (T001 gebaut · T002 gebaut · T003 begonnen: Extraktion,
             Publikations-Bound und das vollständige Vokabular stehen, der
             Dispatch ist geschnitten, aber noch nicht gebaut) — Schätzung

## Range

Review of 6101ca20..HEAD.

## Commits

### 92d2d425 docs(state): save the F009 R18 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f009-r18.md | 200/0 | C0a — the block saved byte for byte from the scratch copy |

### 9ff14cfd docs(state): mirror the F009 R18 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 97/219 | C0b — written from the committed C0a blob, not from scratch |

### b72c9aa4 docs(state): set the plan to the F009 R18 record round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 20/17 | C1 — whole-file replacement by slice PLANF009R18 |

### f5b7d497 docs(review): record the R17 verdict in the live review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — slice LEDGER18 appended, the R17 verdict |

### 63b51e52 docs(decisions): rule DECISION F009 D19 splitting the dispatch round
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 12/0 | C3 — slice DECISION19 appended |

### C4 docs(state): write the F009 R18 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | in the round report | C4 — this file; a handoff cannot table its own commit (R-0149, checklist item 14) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions

- `git push origin feature/f009-single-write-channel` after C4 → exit code and output in the round report.
- No worktree added or removed: no gate this round needed one, and `git worktree list` printed 1 line throughout.
- No PR created, no PR merged, no `gh` command run. F009 opens its PR at its own closure.

## Verification

One line per gate; the raw transcripts are in the round report (finding R-0582).

- G1 `.agent/STOP` absent at both checks; `git rev-parse --abbrev-ref HEAD` printed `feature/f009-single-write-channel`; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3; round base read at step 0 was `6101ca205f06ecacf957d6880682437729c99922`.
- G2 `.agent/authored/f009-r18.md` at C0a, `.agent/last_block.md` at C0b and the received block are all sha256 `767befc4ca5932b45c1e8dedefef8f9472ff5972866e0b5ebd577bbdb7370934`, 20867 bytes, 200 lines, and byte-equal to each other; C0b was written from the committed C0a blob.
- G3 the extractor read 3 slices out of the committed C0a blob by their marker lines; the count 3 and the aggregate 11848 bytes over 60 lines are what the script printed; per-slice digests in the round report.
- G4 `cmp .remedy-wt/r18gate/PLANF009R18 .agent/plan.md` exit 0, both sha256 `cc3780d5…`; negative control `cmp .remedy-wt/r18gate/PLANF009R18 .agent/last_block.md` exit 1; `wc -l` 48 against the 50-line cap; `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 both appends ACCEPTED by reader (a) prefix+remainder and reader (b) last-N-units: C2 over the round-base blob, remainder sha256 `9c46ec16…`, 5407 bytes, 2 lines, N=1 counted by the script, `.agent/live_review.md` 480991→486398 bytes and 1094→1096 lines; C3 over the C2 blob, remainder sha256 `9d00e7c2…`, 3612 bytes, 12 lines, N=6, `.agent/decisions.md` 454550→458162 bytes and 6845→6857 lines; flipping byte 0 of the FIRST appended paragraph at equal length (`G`→`!`, `#`→`!`) is REJECTED by both readers in both cases while both ACCEPT the true file.
- G6 line-anchored at line START over `.agent/live_review.md`, round base → C2: `^- R-\d+ — ` 203 → 203 with every captured id DISTINCT at each; `^Done: R-\d+ — ` 3 → 3; `^Landed: ` 0 → 0; `^Gate: R\d+ — ` 17 → 18 over that many DISTINCT keys; `^Gate: R18 — ` 0 → 1; `^- R-0638 — ` 0 → 0; max id R-0637 at both; open by D10's rule 200 at C2.
- G7 line-anchored at line START over `.agent/decisions.md`, round base → C3: `^## DECISION F009 D\d+ — ` 18 → 19 with every captured number DISTINCT at each; `^## DECISION ` 103 → 104; `^## DECISION F009 D19 — ` 0 → 1.
- G8 serially in the primary checkout, never two pytest processes at once and never in a worktree: `tests/cli/test_golden_path.py` exit 0 at 42 passed; the four-path group `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py` exit 0 at 507 passed.
- G9 the range base→C3 lists exactly the five declared paths other than `.agent/handoff.md`, with the set difference EMPTY in both directions and 0 paths beginning `packages/`, `apps/`, `tests/` or `docs/`, which is this round's no-production-code constraint as a measurement; five commits each with ONE parent; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the `## Commits` tables above, compared cell by cell — 200/0, 97/219, 20/17, 2/0 and 12/0; pre-handback insertions 200, 97, 20, 2 and 12, each under the 500 cap of AGENTS.md DECISION F104 D1; `^<<<SLICE ` and `^<<<END ` read 0 LINES in all three files a slice lands in; `git ls-files .remedy-wt` reads 0; this round's 5 reflog rows all classify as `commit` before the first `:`, with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; `git worktree list` printed 1 line throughout and no worktree was created.
- G10 every mandated section of docs/agents/handback_template.md is present in order, the item-status table carries exactly one row for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA is stated above, each gate is one line, the block's `Fortschritt:` line is repeated verbatim across all three of its lines, and this file's `wc -l` is reported in the round report.

## Authored-text proofs

All applied texts were extracted programmatically from the COMMITTED C0a blob by their marker lines and applied byte for byte; none was retyped, rewrapped, reflowed or reindented. `.agent/plan.md` = PLANF009R18 by `cmp` exit 0 with a negative control at exit 1 (G4). `.agent/live_review.md` and `.agent/decisions.md` carry LEDGER18 and DECISION19 as exact-prefix remainders under two independent readers each, with a rejecting equal-length flip control on the FIRST appended paragraph of each (G5). There is no FROM/TO pair in this round, so no replacement obligation arose.

## Deviations & assumptions

None. The ordered commit sequence C0a, C0b, C1, C2, C3, C4 was executed exactly as the block wrote it, with no extra commit, no dropped commit and no reordering. No slice was edited. No file outside the declared change set was touched, and nothing under `packages/`, `apps/`, `tests/` or `docs/` was written.

## Next

This was the LAST round of the session. The next session's FIRST action is Phase 1 rule 1 of docs/agents/self_drive_protocol.md — re-read `.agent/STOP` from disk — and its SECOND action is the AGENTS.md Open PR Gate. Then round one of DECISION F009 D19: `packages/orchestration/ui_server.py` dispatches `job.stop` to `safe_points.request_stop` under D18's ruled order of effect, audit line, publication, pays R-0636 by moving the replay token to `replayed`, and migrates every seam pin in `tests/ui_server/test_command_channel.py` that must move for the suite to stay green.
