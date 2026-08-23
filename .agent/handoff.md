# Handback — F022 Live cost ticker, Runde 11 (the source ruling, no code)

Fortschritt: ~75 % (T001 fertig · T002 fertig · T003a fertig · T003b offen;
             diese Runde baut nichts, sie entscheidet die Quelle der
             Schluss-Zahl und schreibt das R10-Urteil auf Platte) — Schaetzung

Branch `feature/f022-live-cost-ticker`. Round base `3e1d3fae`.

## Range
Review of 3e1d3fae..ae58934d (C0a–C5) plus this handoff commit (C6).

## Commits
### 575336af docs(state): save the F022 R11 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f022-r11.md | +381/-0 | C0a, the block saved byte-for-byte |

### 5f6bbfb8 docs(state): mirror the F022 R11 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +269/-370 | C0b, same bytes, same git blob `410794db` |

### 7760e77d docs(state): point the F022 plan at R11 and the source ruling
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-19 | C1, slice PLANF022R11 whole-file |

### 60edc932 docs(state): repair the F022 round map for R11 through R14
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +5/-3 | C2, the MAPFROM11→MAPTO11 pair |

### 9933144c docs(state): record the F022 R10 verdict and the R-0625 recurrence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C3, LEDGER11's two paragraphs, appended |

### 5ca8c326 docs(state): rule DECISION F022 D7 on the ledger figure source
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +60/-0 | C4, slice DEC7, appended |

### ae58934d docs(roadmap): amend the F022 terminal reconciliation source
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T5_F022.md | +13/-4 | C5, the SPECFROM→SPECTO pair |

### C6 (this commit) — `.agent/handoff.md`, rewritten whole. A handoff cannot table the commit that writes it (R-0149).

## External actions
- `git worktree add .remedy-wt/g6ctl HEAD --detach` → G6 negative control; `git worktree remove .remedy-wt/g6ctl` → removed, `git worktree list` back to 1 line.
- `gh pr list --state open --json number,headRefName` → `[]` verbatim.
- `git push` → see Next. No PR created, nothing merged (G12).

## Verification
Every gate run by me; every exit code real. Transcripts are in the round report, not here (R-0582).
- G1 exit 0 — `.agent/STOP` absent, read from disk before C0a and again before C6; branch `feature/f022-live-cost-ticker`; `git status --porcelain` 0 lines after each of C0a..C5.
- G2 exit 0 — one sha256 `47a1a3db…5bbaa0e`, 31617 bytes, 381 lines across all FOUR readings (reviewer's `.remedy-wt/f022-r11.md`, the committed C0a blob, the committed C0b blob, `.agent/last_block.md` on disk); the delegation's digest is the fifth reading and agrees; C0a and C0b resolve to the SAME git blob `410794db`.
- G3 exit 0 — the extractor over the committed C0a blob found the slices by their marker LINES and printed 7 slices over 137 CONTENT lines, so TOTAL 381 and PROSE 244. Constraint 9's three numerals reproduce exactly; nothing to reconcile.
- G4 exit 0 — `.agent/plan.md` at C1 is 2607 bytes = PLANF022R11's 2606 + exactly one newline; the NEGATIVE CONTROL against the BARE 2606-byte slice is False; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 46 ≤ 50.
- G5 exit 0 — both pairs printed `TO contains FROM: false`, matching the convention block, one reading per pair. In `.agent/live_review.md` at C2: MAPFROM11 1 at base → 0, MAPTO11 0 → 1, bytes 542726 → 542903, delta 177 = len(MAPTO11) 423 − len(MAPFROM11) 246, `^## Steps$` 1. In `docs/roadmap/features/T5_F022.md` at C5: SPECFROM 1 → 0, SPECTO 0 → 1, bytes 4756 → 5303, delta 547 = 814 − 267. For BOTH, the committed file equals the base file with only that replacement applied and nothing else.
- G6 exit 0 — C3: the C2 blob is a byte-exact PREFIX and the remainder is 8047 = 1 + LEDGER11's 8045 + 1; reader (b) counted N=2 paragraphs in the slice and the file's last 2 of 269 units (267 at C2) equal them IN ORDER. C4: prefix byte-exact, remainder 3761 = 1 + DEC7's 3759 + 1; N=7, last 7 of 1310 units (1303 at C3) equal in order. NEGATIVE CONTROL in the disposable `.remedy-wt/g6ctl`: one byte flipped at BYTE offset 543025, inside LEDGER11's first appended paragraph which spans bytes 542904..545583 (`TOOL EVER BEING RUN ` → `TOOL EVER XEING RUN `), and at BYTE offset 544676 inside DEC7's first, spanning 544666..544747 (`## DECISION F022 D7 ` → `## DECISIOX F022 D7 `) — both readers REJECTED both mutants and ACCEPTED both true files. Worktree removed; `git worktree list` 1 line.
- G7 exit 0 — `.agent/live_review.md`, base vs C3: lines matching `^- R-\d+ — ` 234 → 234, all DISTINCT at both, MAXIMUM id `R-0673` at both; ids ADDED the EMPTY SET and ids REMOVED the EMPTY SET, so NO ID WAS MINTED. `^Done: R-` 1 → 1 over the single id `R-0653`; `^Landed: ` 0 → 0; `^Recurrence: R-` 4 → 5, gaining `R-0625` over ids R-0445, R-0644, R-0645, R-0672; `^Gate: R` 10 → 11 over 10 → 11 distinct keys, gaining `R10`. `^- R-0625 — ` is exactly 1 at both, so the recurrence APPENDED and rewrote nothing. Every base numeral the block quoted reproduced.
- G8 exit 0 — `^## DECISION F022 D7 ` in `.agent/decisions.md`: 1 in the C4 blob, 0 in the round-base blob.
- G9 exit 0 — from the REPOSITORY ROOT, serially: `python3 -m pytest tests/docs/ -q` 295 passed, `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` 30 passed. Both match the base reference of 295 and 30.
- G10 exit 0 — serially in the PRIMARY checkout at C5: `tests/ui_server/` 455, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 — 544 across the four; canary `tests/cli/test_golden_path.py` 42. Both match the base reference. No two pytest processes ran at once.
- G11 exit 0 — all 7 commits before C6 single-parent; insertions 381, 269, 17, 5, 4, 60, 13 (total 749), each under the 500 cap; the range path set matches the Change set with the difference EMPTY in BOTH directions (`.agent/handoff.md` excluded, it is C6's); `git show --numstat` agrees cell by cell with every `## Commits` row above; the LINE-ANCHORED `^<<<SLICE ` and `^<<<END ` count 0 in `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md` and `docs/roadmap/features/T5_F022.md`; `git ls-files .remedy-wt` 0; one worktree; the round's 8 reflog rows carry amend 0, rebase 0, cherry 0 measured on the reflog OPERATION field — an unanchored substring count returns amend 1, which is the word "amend" inside C5's own commit subject and not an operation (R-0608 class), and both readings are reported.
- G12 exit 0 — `gh pr list --state open --json number,headRefName` printed `[]`. No PR created, nothing merged.
- G13 exit 0 — checked, and ONE RESIDUAL. Every file-fact C1..C5 land re-measures TRUE at C5: `packages/orchestration/ui_server.py` contains the string `stats` 0 times and dispatches its job endpoints from one 13-key `handlers` dict plus `events-since`; `_build_token_usage` returns `"estimated": True` and `"source": "event_metadata"` and attributes to `context`, `memory`, `repair`, `planner`, `other`; `BUDGET_TICK_RUN_ID = "budget-ticks"` in `safe_points.py` and `_emit_budget_tick` writes through `RunLogWriter`; `_budget_tick_summary_payload` exists in `ui_server.py`; `measured_token_total` and `measured_cost_usd` are `BudgetCounters` fields in `budget_guard.py`; `git merge-base main HEAD` is `c34ef32b`; `72 problems` occurs exactly once in each of `.agent/authored/f022-r7.md`, `f022-r8.md`, `f022-r9.md` and `f022-r10.md`, as LEDGER11's recurrence states. THE RESIDUAL: MAPTO11's last line joins the sentence that followed MAPFROM11, leaving line 53 of `.agent/live_review.md` at 99 characters where that paragraph otherwise wraps at 72–80. Reported, not repaired — a slice is never edited to fix one.
- NOT A GATE and reported only because C1's risk sentence states it: `npm run lint` in `apps/ui` is RED at HEAD with 78 problems (76 errors, 2 warnings), identical to the reviewer's reading at `3e1d3fae` — no file under `apps/` is in this round's Change set. That sentence states no numeral, so it cannot have gone stale; LEDGER11's `R-0625` recurrence corrects the 72 the four earlier blocks carried.

## Authored-text proofs
Seven slices, all extracted PROGRAMMATICALLY by marker line from the committed C0a blob `575336af`, none retyped, rewrapped or reflowed:
- PLANF022R11 2606 bytes / 46 content lines → `.agent/plan.md` at C1, byte-equal plus one newline (G4).
- MAPFROM11 246 / 4 and MAPTO11 423 / 6 → the pair at C2, applied whole (G5).
- SPECFROM 267 / 5 and SPECTO 814 / 14 → the pair at C5, applied whole (G5).
- LEDGER11 8045 / 3 → appended at C3, both readers plus a byte-flip control (G6).
- DEC7 3759 / 59 → appended at C4, both readers plus a byte-flip control (G6).
`.agent/authored/f022-r11.md`, `.agent/last_block.md` and the reviewer's `.remedy-wt/f022-r11.md` are byte-identical (G2), so the disk-to-disk comparison the fidelity protocol asks for held in its strongest form.

## Deviations & assumptions
- DECISION D15 stated cause: this handback is 104 lines, over the 100 the block sets for this commit count. The overage is mandated content — 7 per-commit changed-files tables plus the C6 self-reference line, 13 one-line gate results several of which must carry base-vs-measured pairs and named byte offsets, the item-status table's 8 rows, and the authored-text proof list. No section was dropped and no transcript is included.
- NO DEPARTURE from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5, C6 were committed in exactly that order, none added, none dropped, none merged, none reordered.
- NO SLICE WAS EDITED. One tension inside the block, declared rather than resolved: constraint 3 says "Both pairs are applied before either append reads its file", while the same constraint fixes an order in which the SPECFROM/SPECTO pair (C5) lands AFTER the C3 and C4 appends. The ordered sequence governs and I followed it; the R-0639/R-0640 property it protects is per-file and holds, because the only pair over `.agent/live_review.md` is C2's and it precedes C3's append, while `docs/roadmap/features/T5_F022.md` carries no append.
- NO PRODUCTION CODE AND NO TESTS: nothing under `apps/`, `packages/` or `tests/` is in the range (constraint 4), and no open finding was repaired — R-0670 still waits for the next round that touches `packages/orchestration/ui_server.py` on its own account (constraint 5).
- `docs/roadmap/ROADMAP.md` was NOT touched; C5 edits only the feature detail file `docs/roadmap/features/T5_F022.md`, which AGENTS.md permits (constraint 6).

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a save this block | done | |
| C0b mirror it into last_block | done | |
| C1 the plan | done | |
| C2 repair the round map | done | |
| C3 the R10 verdict and the R-0625 recurrence | done | |
| C4 DECISION F022 D7 | done | |
| C5 the feature-file amendment | done | |
| C6 the handback | done | this commit |

## Next
1. Phase 1 rule 1 — re-read `.agent/STOP` from disk before anything else (R-0347).
2. The Open PR Gate: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`; it printed `[]` at C5.
3. R12 — T003b, built against DECISION F022 D7 and in its two halves: the SERVER's final-figure section, exposing the last `budget.tick` of the job's `budget-ticks` run log in the whitelisted shape `_budget_tick_summary_payload` already produces, and the CLIENT's terminal reconciliation rendering it in place of the live value with any delta labelled as a TRANSPORT statement. R12 touches `packages/orchestration/ui_server.py` on its own account, so it owes R-0670 its repair.
4. R11's own verdict is NOT yet on disk. R12's ledger commit owes it (DECISION F085 D9).
