# Handback — F021 Live activity feed, R11 (register-and-close). SESSION ENDS HERE.

Fortschritt: ~40 % (T001 fertig · T002 begonnen — die Projektion Frame→Zeile
             ist gebaut und verifiziert, Ring und Komponenten folgen; R11
             registriert einen Reviewer-Defekt und schliesst die Session)
             — Schaetzung

Round base (every "round base" below): `4f504337efac50667a346c3964b7b047728bcf1d`.
Branch `feature/f021-live-activity-feed`, unmerged and carrying no pull request by design.

## Range

Review of `4f504337efac50667a346c3964b7b047728bcf1d`..HEAD (C3, the commit that writes this file).

## Commits

### 8a03d8c6 docs(state): save the F021 R11 register-and-close block as authored text
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f021-r11.md` | +250 / -0 | C0a — the block saved verbatim as authored text (NEW) |

### b9a9f606 docs(state): mirror the F021 R11 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +116 / -110 | C0b — written FROM the committed C0a blob, not retyped |

### 54b23c4f docs(state): point the F021 plan at R11 and restore its terminating newline
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +10 / -10 | C1 — whole-file replacement by PLANF021R11 plus one terminating newline (R-0650's fix) |

### 17584638 docs(review): record the R10 verdict and register R-0650
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +6 / -0 | C2 — append of RECORD10: the R10 PASS entry and the new finding R-0650 |

### C3 — SHA not nameable here: this table is written BY that commit (R-0149 self-reference) — docs(state): hand back F021 R11 and close the self-drive session
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C3 — this handback; its own `git status --porcelain` and insertion count are ordered NOWHERE this round (§3 checklist item 31) |

## External actions

- `git push -u origin feature/f021-live-activity-feed` after C3 — see the push line at the end of Verification.
- `git worktree add --detach .remedy-wt/f021r11-g5 17584638` then `git worktree remove --force` + `git worktree prune` — G5's destructive half; `git worktree list` ends with the primary checkout alone.
- `gh pr list --state open --json number,headRefName` → exit 0, `[]`. No `gh pr create`, no `gh pr merge`, no merge of any kind.

## Verification

One line per gate; transcripts stay in the round report, not in this file (R-0582). All gates EXECUTED, real exit codes.
- G1 PASS — `.agent/STOP` ABSENT immediately before C0a and again immediately before C3; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2. C3's own reading is ordered nowhere.
- G2 PASS — TRANSPORT sha256 `d63a7e100cec48034b2946c4b034209d8474618d9ba912d6826abc7bc34310e3` over 21857 bytes and 250 lines, EQUAL across `.agent/authored/f021-r11.md` at C0a, `.agent/last_block.md` at C0b, the bytes received, and the reviewer's emitted copy at `.remedy-wt/f021-r11.md`.
- G3 PASS — the marker-line extractor printed 2 slices (PLANF021R11, RECORD10) over 53 CONTENT lines from the COMMITTED C0a blob; TOTAL 250 against D6's 490 and PROSE 197 against D5's 400, both equal to constraint 9.
- G4 PASS — `cmp .agent/plan.md` against PLANF021R11-plus-one-newline exit **0**; NEGATIVE CONTROL against the bare slice exit **1** ("EOF ... after byte 2783, in line 48"). The file's last byte IS a newline; `git diff HEAD -- .agent/plan.md` is empty and prints the no-newline marker 0 times. (`git show 54b23c4f` prints that marker once, on the REMOVED side — it describes the base file, i.e. the defect this round fixes.) `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48 ≤ 50.
- G5 PASS — reader (a): round-base blob is a byte-exact PREFIX of the C2 file; remainder sha256 `446ae09f36b6ae1c3670a838c356e99c01a029d0d34963e596a8e0958dafddee` over 5704 bytes and 6 lines = exactly one newline + RECORD10 + one newline; file 467847 B / 1092 L → 473551 B / 1098 L. Reader (b), terminator stripped from both blobs: units 227 → 230, RECORD10's own units **3** (= constraint 5's THREE), elementwise equal over the WHOLE list. NEGATIVE CONTROL in the disposable worktree `.remedy-wt/f021r11-g5`: byte offset **2**, inside the FIRST paragraph, `L` → `Q` at equal length — REJECTED by both readers while both ACCEPT the true file. Worktree removed and pruned.
- G6 PASS — ledger at round base → C2: `- R-` 212 → 213, DISTINCT at both; MAX id R-0649 → R-0650; `Done: R-` 0 → 0; `Landed: ` 0 → 0; `Gate: R` keys 10 → 11, DISTINCT at both; `Gate: R11` 0 → 1; `- R-0650 —` 0 → 1. Every value equals G6's prediction.
- G7 PASS — exit **0**, cwd `/home/decodeux/Repos/remedy` (repository root), **511** = 511 passed + 0 skipped. Checked against the `Change:` list first: all four non-handoff paths are under `.agent/`, 0 under `docs/`, so no docs gate is owed.
- G8 PASS — canary, run serially after G7, exit **0**, cwd `/home/decodeux/Repos/remedy`, **42** = 42 passed + 0 skipped.
- G9 PASS — `tests/ui_contracts/`, serially after G8, exit **0**, cwd `/home/decodeux/Repos/remedy`, **430** = 426 passed + 4 skipped.
- G10 PASS — base..C2 holds **0** paths beginning `apps/`, `packages/` or `tests/` (the four paths are all `.agent/`); `git ls-files .remedy-wt` reads **0**.
- G11 PASS — base..C2 path set equals this block's four non-handoff `Change:` paths with the set difference EMPTY in BOTH directions; all 4 commits single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with the `## Commits` table above (250/0, 116/110, 10/10, 6/0) and `git commit` produced no rewrite-detected summary, so there is no disagreement to report; insertions 250, 116, 10, 6 — each under the 500 cap; `<<<SLICE ` and `<<<END ` read **0 LINES** in `.agent/plan.md` and in `.agent/live_review.md`; all 4 of this round's reflog rows are `commit:` — amend 0, rebase 0, cherry 0.
- G12 PASS — `gh pr list --state open --json number,headRefName` exit 0, output `[]` (EMPTY). Neither `gh pr create` nor `gh pr merge` was run.
- G13 PASS — this file; `wc -l` reported under Deviations against the 60-line cap.
- Push: `git push -u origin feature/f021-live-activity-feed` after C3 — outcome recorded by the pushing command itself; the branch is remote-tracking and unmerged.

## Authored-text proofs

- `.agent/authored/f021-r11.md` (C0a) — disk-to-disk equal to the reviewer's emitted `.remedy-wt/f021-r11.md`: sha256 `d63a7e10…10e3`, 21857 bytes, 250 lines, byte-equality confirmed (G2).
- `.agent/last_block.md` (C0b) — written FROM the committed C0a blob; same digest, same byte and line counts (G2).
- PLANF021R11 → `.agent/plan.md` (C1) — `cmp` exit 0 against the slice extracted from the COMMITTED C0a blob plus one terminating newline, with the bare-slice negative control at exit 1 (G4).
- RECORD10 → `.agent/live_review.md` (C2) — remainder byte-exactly one newline + slice + one newline, under two independent readers plus a mutation control (G5).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a `.agent/authored/f021-r11.md` | done | |
| C0b `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` | done | terminating newline restored — R-0650's fix |
| C2 `.agent/live_review.md` | done | R10 PASS entry + R-0650 registered; nothing resolved |
| C3 `.agent/handoff.md` | done | this file |

## Deviations & assumptions

- **DECISION D15 stated-cause overage.** This handback is 97 lines against the 60-line cap. The mandated content that causes it: five per-commit changed-files tables (`## Commits`, one per commit including the self-referential C3 heading), the thirteen one-line gate results G1–G13 that `## Verification` requires with their real readings, the four authored-text proofs, the five-row item-status table, and the four items constraint 8 orders into `## Next`. No section was dropped and no transcript was inlined.
- Commit sequence: executed exactly as the block ordered — C0a, C0b, C1, C2, C3, no extra commit, none dropped, none reordered.
- No production file was created, modified or deleted; nothing under `apps/`, `packages/` or `tests/` was touched; no formatter or linter was run.
- Assumption, stated rather than assumed silently: G4's "`git diff` prints no no-newline marker for it" is read as a property of the file AS IT NOW STANDS — `git diff HEAD -- .agent/plan.md` prints it 0 times. `git show 54b23c4f` still prints it once, attached to the REMOVED side, because that is the base file's defect and history is not rewritten (G2 of the protocol).

## Next

The single expected next action: a new planner/reviewer session opens and reviews `4f504337..HEAD`. Before anything else it needs these four facts, which it cannot cheaply recompute:

1. **FIRST action is `docs/agents/self_drive_protocol.md` Phase 1 rule 1** — re-read `.agent/STOP` from disk — BEFORE rule 2's Open PR Gate. Phase 2 and finding R-0347 both require this ordering; the sentinel is absent as of C3 but that is a reading, not a guarantee.
2. **The Open PR Gate will find NO open pull request** (`gh pr list --state open` printed `[]` at G12), so Phase 1 rule 5 applies and F021 continues on `feature/f021-live-activity-feed`. Do not cut a new branch.
3. **The next build is the bounded ring DECISION F021 D5 rules**: `recent` on `BrainStreamState` and on `BrainStreamView`. Its append belongs INSIDE `receiveBrainFrame` in `apps/ui/src/api/brainStream.ts`, not in the runner's `dispatch`, because that function already drops a frame whose `seq` is not ahead of `lastSeq` — an append written anywhere else bypasses that guard and a reconnect replay duplicates rows. `feedRowOf` in `apps/ui/src/api/feedRow.ts` is the projection it feeds and is deliberately uncalled until then.
4. **Two handback commits are owed readings at the next reviewer's first gate.** Neither this round's C3 nor the R10 handback commit `4f504337` has ever had its own `git status --porcelain` reading or insertion count recorded, because §3 checklist item 31 orders them nowhere in the round that writes them. Both are owed that pair.
