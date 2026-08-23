# Handback — F022 Live cost ticker · Runde 12 (T003b-a)

Fortschritt: ~80 % (T001 fertig · T002 fertig · T003a fertig · T003b halb —
             diese Runde liefert die Server-Seite der Schluss-Zahl, repariert
             R-0670 und schreibt das R11-Urteil auf Platte) — Schaetzung

Branch `feature/f022-live-cost-ticker`. Round base `f6259860`.
Deviations, declared: this handback is 137 lines, over the 100-line cap, under
DECISION D15 — the cause is the mandated per-commit tables for 9 commits plus
the 14 one-line gate rows and the 9-row item-status table.

## Range

Review of `f6259860`..`HEAD` (C7 below).

## Commits

### f5508057 docs(state): save the F022 R12 step block as authored text (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f022-r12.md | +349/-0 | the block file copied byte-for-byte |

### 63987ec8 docs(state): mirror the F022 R12 block into last_block (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +241/-273 | same bytes; full-file state rewrite |

### fe6da915 docs(state): point the F022 plan at R12, the server final figure (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-18 | PLANF022R12 replaces the file whole |

### cbe4f643 docs(state): repair the F022 round map for R12 through R15 (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-3 | MAPFROM12 → MAPTO12, one replacement |

### d0d5e94b docs(state): record the F022 R11 verdict and two recurrences (C3)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | LEDGER12's three paragraphs appended |

### df8ae445 docs(comment): name the measured guard for the budget tick constant (C4)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +6/-3 | GUARDFROM → GUARDTO, R-0670's repair |

### 417d7136 feat(ui-server): serve the ledger final budget figure on the dashboard (C5)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +31/-0 | `_build_budget_final` + the `budget_final` key |
| tests/ui_server/test_budget_final_section.py | +185/-0 | NEW, 15 tests over the section |

### 11a379ee docs(state): resolve R-0670 by naming the measured guard (C6)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | DONE670 appended |

### C7 docs(state): hand back the F022 R12 server final-figure round
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file; a handoff cannot table its own commit |

## External actions

`git worktree add/remove .remedy-wt/g6 11a379ee --detach` → ok, both (G6
controls). `git worktree add/remove .remedy-wt/g8 417d7136 --detach` → ok, both
(G8 mutation). `gh pr list --state open --json number,headRefName` → `[]`.
`git push` → after C7. No PR created, nothing merged.

## Verification

One line per gate; transcripts stay in the round report (R-0582).

- G1 exit 0 — `.agent/STOP` absent before C0a and again before C7; branch `feature/f022-live-cost-ticker`; `git status --porcelain` 0 lines after each of C0a–C6.
- G2 exit 0 — five readings of the block are EQUAL: sha256 `1891867831bb…2ee8`, 31863 bytes, 349 lines (scratch `.remedy-wt/f022-r12.md`, C0a blob, C0b blob, `.agent/last_block.md` on disk, the delegation's digest); C0a and C0b are the same blob `31c21b07`.
- G3 exit 0 — extractor over the COMMITTED C0a blob printed 7 slices over 69 CONTENT lines; TOTAL 349, PROSE 280 — constraint 9's numerals reproduce exactly.
- G4 exit 0 — `.agent/plan.md` at `fe6da915` is 2559 bytes = PLANF022R12's 2558 + 1 newline; NEGATIVE CONTROL against the bare slice is FALSE; `^## Goal$` 1x, `^## Next Steps$` 1x, `wc -l` 45 ≤ 50.
- G5 exit 0 — both pairs printed `TO contains FROM: false`. `.agent/live_review.md` at `cbe4f643`: MAPFROM12 1→0, MAPTO12 0→1, byte delta 51 = 305 − 254, file == base with ONLY that replacement, `^## Steps$` 1x, and the `## Steps` paragraph's longest line is 80 chars (99 at base, R-0431's line). `packages/orchestration/ui_server.py` at `df8ae445`: GUARDFROM 1→0, GUARDTO 0→1, byte delta 255 = 520 − 265, file == base with ONLY that replacement.
- G6 exit 0 — C3: prefix byte-exact, remainder 8279 = 1 + LEDGER12's 8277 + 1, reader (b) N=3 paragraphs equal in order over 269→272 blank-line units. C6: remainder 1648 = 1 + DONE670's 1646 + 1, N=1, 272→273. NEGATIVE CONTROLS in `.remedy-wt/g6`: one BYTE flipped in the FIRST appended paragraph at offsets 551402 (`r paragraph whose tr` → `r paragrapH whose tr`) and 559681 (`measurement was a re` → `measuremenT was a re`) — both readers REJECT both mutants and ACCEPT both true files. Worktree removed.
- G7 exit 0 — `^- R-\d+ — ` records: 234 at base and 234 at C6, all DISTINCT at both, MAXIMUM `R-0673` at both; ids ADDED and ids REMOVED are both the EMPTY SET, so NO ID WAS MINTED. `^Done: R-` 1→2 gaining `R-0670` (ids `R-0653`, `R-0670`); `^Landed: ` 0→0; `^Recurrence: R-` 5→7 gaining `R-0431` and `R-0413`; `^Gate: R` 11→12 over 11→12 distinct keys, gaining `R11`. `^- R-0670 — `, `^- R-0431 — ` and `^- R-0413 — ` are each exactly 1 at both points. Every reference figure the block states for the base reproduced.
- G8 exit 0 (the gate's requirement met; the mutant run is RED by design) — in `.remedy-wt/g8` at C5, `BUDGET_TICK_EVENT` rewritten to `"budget.ticks"` and nothing else (1 file, +1/-1): `tests/ui_server/test_budget_tick_envelope.py` exit 1, 11 failed 5 passed — the newly named guard IS red; `tests/ui_contracts/test_humanize_catalog.py` exit 0, 9 passed — the previously named guard is blind, exactly as R-0670 measured. Unmutated control in the same worktree: both exit 0 (16 and 9 passed), and `ui_server.__file__` resolved to the worktree copy. Worktree removed.
- G9 exit 0 — `python3 -m pytest tests/ui_server/ -q` from the REPOSITORY ROOT: 470 passed. Base was 455; the +15 is exactly the 15 tests in the new `tests/ui_server/test_budget_final_section.py`.
- G10 exit 0 — `python3 -m pytest tests/ui_contracts/ -q` from the REPOSITORY ROOT (not from `apps/ui`): 518 passed, 4 skipped — identical to the base figures.
- G11 exit 0 — serially in the primary checkout at C6, never two pytest processes at once: `tests/ui_server/` 470, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 → 559 (base 544, +15 from G9); canary `tests/cli/test_golden_path.py` 42, matching base.
- G12 exit 0 — 8 commits before C7, every one single-parent; insertions 349, 241, 17, 4, 6, 6, 216, 2 — each under the 500 cap; the range path set is exactly the 6 declared non-handoff paths with the difference EMPTY in BOTH directions; `git show --numstat` agrees cell by cell with every `## Commits` row above; line-anchored `^<<<SLICE ` and `^<<<END ` count 0 in `.agent/plan.md` and 0 in `.agent/live_review.md`; `git ls-files .remedy-wt` 0; one worktree; the round's 8 reflog rows all carry the action `commit` — amend 0, rebase 0, cherry 0 (the single `amend` string in the last 40 rows is a PREVIOUS round's commit SUBJECT at `HEAD@{9}`, not an action).
- G13 exit 0 — `gh pr list --state open --json number,headRefName` printed `[]`. No PR created, nothing merged.
- G14 — CHECKED, every C1–C6 sentence stating a fact about a file re-measured at C6. Confirmed: branch and `c34ef32b` merge-base; `budget_final` added with no new endpoint; R-0672, R-0625, R-0495, R-0574, R-0622, R-0665 still open records and R-0670 now `Done:`; base line 53 = 99 chars and the repaired paragraph 80; `.agent/plan.md` at `7760e77d` = 2607 bytes; the R11 constraint-3 text LEDGER12 quotes is verbatim in `.agent/authored/f022-r11.md`. ONE RESIDUAL and two carried statements, all under Deviations — no slice was edited.

## Authored-text proofs

Seven slices extracted PROGRAMMATICALLY by marker line from the committed C0a
blob and applied byte-for-byte, never retyped: PLANF022R12 2558 B, MAPFROM12
254 / MAPTO12 305, GUARDFROM 265 / GUARDTO 520, LEDGER12 8277, DONE670 1646.
Disk-to-disk equality is G2, G4 (with the bare-slice control FALSE), G5 (both
pairs surgical) and G6 (both appends, two readers, byte-flip controls).

## Deviations & assumptions

- ORDERED COMMIT SEQUENCE: none. C0a, C0b, C1, C2, C3, C4, C5, C6, C7 landed
  exactly as constraint 3 fixes them — no extra commit, none dropped, no
  reordering. LEDGER12's three paragraphs landed in the ONE commit C3.
- RESIDUAL (G14, reported not repaired; per constraint 1 the slice was applied
  byte-for-byte anyway): DONE670 states "R8 through R11 held no Python path in
  their change sets". Measured at C6: R8's `68cf3c16` (+270) and R10's
  `48f63b1e` (+69) both changed `tests/ui_contracts/test_cost_metric_render.py`.
  The narrower routing claim the finding made IS true — no round R8–R11 touched
  `packages/orchestration/ui_server.py`.
- CARRIED, NOT RE-MEASURED: PLANF022R12's sentence that `npm run lint` in
  `apps/ui` is red at base — the block's "NOT A GATE" clause excludes it.
- NUANCE on GUARDTO (not a residual): `test_humanize_catalog.py` does name
  `ui_server.py` as a scanned module path (`UI_SERVER_MODULE`) but never reads
  this constant's VALUE — G8 confirms exit 0 under the rename.
- No measurement of mine differed from a reference numeral the block states for
  the base, so nothing needed reconciling.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save this block | done | |
| C0b mirror it into last_block | done | |
| C1 the plan | done | |
| C2 repair the round map | done | |
| C3 the R11 verdict and two recurrences | done | |
| C4 R-0670's comment repair | done | |
| C5 the final-figure section and its tests | done | |
| C6 resolve R-0670 | done | |
| C7 the handback | done | this commit |

## Next

1. Phase 1 rule 1 FIRST: re-read `.agent/STOP` from disk before anything else.
2. The Open PR Gate (`gh pr list --state open …`); it printed `[]` at G13.
3. R13, T003b's client half: read `budget_final` into the dashboard type and
   render the terminal reconciliation with its delta label, per DECISION F022 D7.
4. R12's own verdict is NOT on disk — R13's ledger commit owes it.
