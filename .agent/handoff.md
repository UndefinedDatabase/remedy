# Handback — F031 Decision inbox, Runde 18

Feature F031 (Tier 5) · Runde 18 · branch `feature/f031-decision-inbox` · base `48124293` · the block's constraint 3 fixes 7 commits, and >5 commits puts the AGENTS.md `### handoff.md` tier at 100 lines.

Fortschritt: ~58 % (F031 claimed; R1 through R17 landed and gated ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             R-0681 repaired at R17, resolution owed · T002b
             ordering/filtering/badge und T003 offen) — Schaetzung

## Range
Review of `48124293`..HEAD, where HEAD is the C5 commit this file IS; its SHA cannot exist while this text is written.

## Commits
### 76ed9b66 chore(agent): save the F031 R18 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f031-r18.md` | +476/-0 | C0a: the R18 block saved verbatim |
### 9adced9a chore(agent): mirror the R18 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +310/-294 | C0b: mirror written FROM the committed C0a blob |
### a0565593 docs(agent): point the F031 plan at the R18 ruling round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +26/-26 | C1: PLANF031R18 applied as the whole file |
### 7107a563 docs(agent): record the F031 R17 verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | C2: LEDGER18 appended, and nothing else |
### 24b47b3b docs(agent): rule DECISION F031 D6 for the inbox ordering
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +56/-0 | C3: DECISIOND6 appended, and nothing else |
### 75d4b532 docs(roadmap): amend F031 with the D6 ordering ruling
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T5_F031.md` | +21/-0 | C4: AMEND18 appended, and nothing else |
### C5 docs(agent): write the F031 R18 handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | self-reference | C5: this file; a handoff cannot table the commit that writes it (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| push | done | ordered after C5; outcome carried by G12 to the reviewer |

## External actions
- `git worktree add --detach .remedy-wt/r18-neg 7107a563` → created for the G5 negative control; `git worktree remove --force .remedy-wt/r18-neg` → removed BY ITS EXACT PATH, before the G11 suites, as constraint 11 orders.
- `git push origin feature/f031-decision-inbox` — run AFTER C5. Its outcome is not a value of any file this round writes: the reviewer measures the pushed tips at the next gate and records them in the R18 entry of `.agent/live_review.md`.
- No `gh` command run; no pull request created, edited or merged; no branch created or deleted; no amend, rebase, cherry-pick or force-push.

## Verification
- G1 `git branch --show-current` printed `feature/f031-decision-inbox`, not `main`; `.agent/STOP` read from disk was ABSENT before C0a and ABSENT again before C5; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3 and C4.
- G2 All FOUR readings EQUAL: sha256 `32b2664d1827403c438ab4bd54327956a64f29779ddc82ed2da6f3a58fe31364`, 33873 bytes, 476 lines, for `.remedy-wt/f031-r18.md` before C0a, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk after C0b. C0a's and C0b's file resolve to the SAME git blob `c732ebf49afd964f5d2ccdc19a4f6da0482c548f`.
- G3 My extractor over the COMMITTED C0a blob printed: 4 slices (PLANF031R18, LEDGER18, DECISIOND6, AMEND18), 125 CONTENT lines inside markers, 476 TOTAL lines.
- G4 `.agent/plan.md` at C1 is byte-equal to PLANF031R18 under the newline-INCLUDED convention — slice 3024 bytes, file 3024 bytes. NEGATIVE CONTROL against that slice with its trailing newline REMOVED: FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49, strictly under 50.
- G5 C2 in the shape constraint 7 states: reader A TRUE, 624137 + 1 + 5060 = 629198 against an actual 629198, the parent being the base's 624137 unchanged by C1. Reader B, splitting the committed file on blank lines, measured N=1 paragraph in LEDGER18, units 298 → 299, and the last N units EQUAL the slice's paragraphs IN ORDER. NEGATIVE CONTROL, written only inside worktree `.remedy-wt/r18-neg`: one byte flipped at offset 624338 (`0x20` → `0x00`) inside the paragraph the append added, file length unchanged — BOTH readers REJECTED the mutant and BOTH ACCEPTED the true file.
- G6 Each append in the shape constraint 7 states, against the length measured at that commit's own parent. C3 `.agent/decisions.md`: TRUE, 566658 + 1 + 3653 = 570312 against an actual 570312, 7534 → 7590 lines, `^## DECISION F031 D\d+` 5 → 6 gaining EXACTLY `## DECISION F031 D6`, with D1 through D5 still present. C4 `docs/roadmap/features/T5_F031.md`: TRUE, 8485 + 1 + 1318 = 9804 against an actual 9804, 150 → 171 lines, `^## Design amendments ` 2 → 3 gaining EXACTLY `## Design amendments (F031 R18, 2026-08-26)`, with the R5 and R11 headings still present and all three DISTINCT.
- G7 base → C2 in `.agent/live_review.md`: `^- R-\d+ — ` 242 → 242, all 242 DISTINCT, ids ADDED the EMPTY SET and ids REMOVED the EMPTY SET, maximum `R-0681` → `R-0681`; `^Done: R-` 3 → 3, `^Landed: R-` 1 → 1 and `^Recurrence: R-` 16 → 16, all THREE UNCHANGED; `^Gate: R\d+ — ` 17 → 18, gaining EXACTLY the key `R17`, with `R19` and `R1` through `R16` still present and all 18 DISTINCT. The §3 item 10 open set at C2 is 242 − 3 = 239.
- G8 Line-anchored `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, `.agent/decisions.md` at C3 and `docs/roadmap/features/T5_F031.md` at C4; the same two patterns count 4 and 4 over the COMMITTED C0a blob as the CONTROL, so the reading is not vacuous. `git diff --name-only 48124293..75d4b532` names 6 paths: none under `packages/`, `apps/` or `tests/`, exactly one `docs/` path and it is the feature file above, and neither `.agent/context.md` nor either `f031_*_inventory.md`. Range MINUS change set is EMPTY; change set MINUS range is exactly `.agent/handoff.md`, which C5 writes. Every commit C0a..C4 is single-parent, with INSERTIONS — the `+` column only, per AGENTS.md DECISION F104 D1 — of 476, 310, 26, 2, 56 and 21, each under 500. The `## Commits` `+/-` column above is derived from `git diff --numstat`, not from `git commit`'s summary, and agrees with this gate cell for cell. `git ls-files .remedy-wt` 0 and `git ls-files '*.zip'` 0. Reflog SCOPE: this round's entries only, the 6 above the R17 handback entry; FIELD: the operation prefix before the first colon of `git reflog --format=%gs`, which is `commit` for all 6 — `amend` 0, `rebase` 0, `cherry` 0.
- G9 In the PRIMARY checkout: `npm run typecheck` in `apps/ui` REAL EXIT 0 with ZERO diagnostics on stdout and stderr; `npm run test:unit` REAL EXIT 0 at 21 files and 316 tests, both counts UNCHANGED from the base's 21 and 316. G8's reading that the range holds no `apps/` path is what makes those counts meaningful.
- G10 In the PRIMARY checkout at the C4 tree, SERIALLY, with the exact command lines ordered and no extra flag: `python3 -m pytest tests/docs/ -q` REAL EXIT 0, 295 passed; `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` REAL EXIT 0, 30 passed. Both equal the reviewer's base readings of 295 and 30, so there is no difference to account for — this round adds no feature FILENAME and no index row, only a section inside an existing feature file.
- G11 SHA-shaped tokens in the COMMITTED C0a blob under the word-bounded `[0-9a-f]{7,40}`: 22 occurrences, 8 DISTINCT, FAILING SET EMPTY. Types: `87dbf588669fe871237e703f21b0fc5bd175d7f1` → `blob`; `0faf773c`, `48124293`, `48124293e77c4fc2d9de558b0ab0f1d76fd421b0`, `6325ac2f`, `6ede183c`, `a48d1234` and `c7a0b099` → `commit`. `git worktree list` printed 1 line immediately BEFORE the first pytest command. The five Python suites, SERIALLY in the PRIMARY checkout at the C4 tree, never two alive at once, each with its REAL exit code: `tests/ui_server/` EXIT 0, 474 passed; `tests/orchestration/test_test_runner.py` EXIT 0, 52; `tests/regression/test_resource_safety.py` EXIT 0, 21; `tests/orchestration/test_integrity_gate.py` EXIT 0, 16; `tests/cli/test_golden_path.py` EXIT 0, 42. Every count equals the reviewer's base reading, so there is no difference to account for.
- G12 `git push origin feature/f031-decision-inbox`, run after C5, with no `--force`, no `--force-with-lease`, no history rewrite, no branch deletion and no pull request. Carrier as ordered: the reviewer measures the pushed tips at the next gate and records them in the R18 entry of `.agent/live_review.md`.

## Findings
The §3 item 10 open set — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line, the rule DECISION F009 D10 requires — is 239 at `7107a563`. The narrower set `.agent/plan.md` names "the findings this feature must still act on" is 21 distinct ids at `75d4b532`, counted mechanically off that bullet; it is not the open set and is never called "open" unqualified. This round minted no finding id and wrote no `Done:`, `Landed:` or `Recurrence:` line, exactly as constraint 8 orders.

## Authored-text proofs
- All four slices were extracted PROGRAMMATICALLY from the COMMITTED C0a blob by their `<<<SLICE`/`<<<END` marker LINES; nothing was retyped, rewrapped or hand-corrected, and no marker line reached a target file (G8).
- PLANF031R18 → `.agent/plan.md` at C1: byte-equal to the extracted slice, 3024 bytes both, with the trailing-newline-removed negative control FALSE (G4).
- LEDGER18 → `.agent/live_review.md` at C2: whole-file equality against the C1 blob plus one newline plus the slice, corroborated independently by the blank-line paragraph reader, and both readers proven able to reject a one-byte mutant (G5).
- DECISIOND6 → `.agent/decisions.md` at C3 and AMEND18 → `docs/roadmap/features/T5_F031.md` at C4: each proven by whole-file equality against that commit's PARENT blob plus one newline plus the slice (G6).

## Deviations & assumptions
- COMMIT SEQUENCE: C0a, C0b, C1, C2, C3, C4, C5 applied exactly as constraint 3 orders — no extra commit, none dropped, no reordering. No commit was made outside that sequence.
- NO PRODUCTION CODE MOVED, as constraint 9 orders: the range names no path under `packages/`, `apps/` or `tests/` (G8), and the two `apps/ui` counts are unchanged (G9).
- NO CONTRADICTION was found inside the block. Every reading it states about the base — the 624137 bytes and the five ledger set counts, the plan's 49 lines and 2892 bytes, the handoff's 95 lines, decisions.md's 566658 bytes and 7534 lines with five `## DECISION F031 D` headings, the feature file's 150 lines with two amendment headings, and the docs, npm and Python suite counts — reproduced exactly when measured here.
- TOOL DEVIATION, declared: this session's command guard rejected two shell forms mid-round — `$?` in a compound command, and a brace-with-quote set literal inside a `python3` heredoc. Both were measurement-only; each was re-run in an accepted form and the readings above are those re-runs. No committed byte was affected.
- SCRATCH, declared because it is a write outside the change set: this round created the worktree `.remedy-wt/r18-neg` and the directory `.remedy-wt/r18-slices/` holding the four extracted slice files. All were deleted BY EXACT PATH, never by glob; `git ls-files .remedy-wt` is 0 and `git worktree list` is 1 line. Nothing pre-existing under `.remedy-wt/`, the block file included, was touched or deleted.
- HANDBACK SIZE, per DECISION D15: this file measures 93 lines against the 100-line tier that 7 commits earn, so no overage is claimed and no token cap is asserted — that cap was withdrawn.

## Next
1. The R18 verdict is UNRECORDED and is owed by the NEXT round's ledger commit — by DECISION F085 D9 no artefact of this round can carry it.
2. R19 then RESOLVES R-0681 by replacing its `Landed:` line with authored `Done:` text, and builds T002b's ordering under DECISION F031 D6 — the two obligations `## Next Steps` items 1 and 2 of `.agent/plan.md` name.
