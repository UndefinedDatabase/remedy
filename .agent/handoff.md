# Handback — F085 Sandbox hardening (stage 1), R54

Feature F085 · Round R54 · Branch `feature/f085-sandbox-hardening` · Base 8ba3ad45

## Range
Review of 8ba3ad45..HEAD. Eight commits: C0a C0b C1 C2 C3 C4 C5 C6.

## Commits
### eb18ad04 docs(f085): save the authored R54 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f085-r54.md` | +490/-0 | C0a — the R54 block, byte-verbatim from the reviewer's original |

### 2067581f docs(f085): mirror the R54 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +417/-356 | C0b — the COMMITTED blob copied over; single-state-file rewrite |

### dbfb26af docs(f085): advance the plan to R54
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +8/-9 | C1 — PLAN8F→PLAN8T, the first substantive commit; 41 lines after |

### d48febf0 docs(f085): record the R53 PASS and register R-0557
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +53/-0 | C2 — RECORD22 appended; R-0557 registered, nothing resolved |

### 27279810 feat(f085): add the runtime-build seam and the shared guard-result translation
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/exec_guard.py` | +99/-0 | C3 — SEAM3: `_completed_process_from_guarded`, the policy and the wrapper |

### 1bfcaf0c refactor(f085): move the test and dod-process wrappers onto the shared translation
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/exec_guard.py` | +7/-26 | C4 — XLAT1F→XLAT1T, XLAT2F→XLAT2T, DOCXF→DOCXT; refactor kept out of C3 |

### a3d32124 test(f085): cover the runtime-build seam policy and its check knob
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_exec_guard.py` | +46/-0 | C5 — TESTSRB, four tests |

### C6 — self-reference, a handback cannot table the commit that writes it
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | in the round report | C6 — this file; its own insertions go to the operator |

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this commit |

## External actions
`git push -u origin feature/f085-sandbox-hardening` after C6; outcome reported to the operator. No PR, no merge, no `gh` call, no worktree add and no worktree remove.

## Verification
G1 STATE — `.agent/STOP` absent before C0a and again before C6 (`os.path.exists` false at both points); `git status --porcelain` EMPTY at round start and after each of the seven commits preceding this one, whose own post-commit reading goes to the operator; `git worktree list` one line throughout.
G2 TRANSPORT — exit 0. The committed `.agent/authored/f085-r54.md`, the committed `.agent/last_block.md`, BOTH working copies and the reviewer's `.remedy-wt/f085-r54.md` are all five byte-EQUAL, disk-to-disk and not by digest fallback: sha256 19497ed6660efbf34b3e2fbb246faa0c1ef0e0a75e7132c14e3757a6c3182959, 31279 B, 490 lines, 22 marker lines — every figure measured on every copy.
G3 SHAPES — THE FOUR REWRITES, each measured separately over its own post-commit file, FROM 0x and TO exactly 1x in every case, each FROM 1x in its pre-commit blob: PLAN8F→PLAN8T at dbfb26af numstat `8 9`; XLAT1F→XLAT1T, XLAT2F→XLAT2T and DOCXF→DOCXT all at 1bfcaf0c, that path's numstat `7 26`. THE PROSE APPEND, C2 / RECORD22 / `.agent/live_review.md` at d48febf0: byte-exact PREFIX, remainder exactly one blank line plus the slice, exact SUFFIX, 0 marker LINES, and each of the 51 non-empty lines among its 52 slice lines occurring exactly once among the 53 lines that commit adds, numstat `53 0`. THE CODE APPENDS under ORDERED EQUALITY, measured separately: C3 / SEAM3 at 27279810, `post == pre + slice` exactly — no byte between them and none appended after — prefix and suffix exact, the commit's added lines exactly the slice's 99 lines IN ORDER, 0 marker LINES, numstat `99 0`; C5 / TESTSRB at a3d32124, same four readings, added lines exactly the slice's 46 lines IN ORDER, 0 marker LINES, numstat `46 0`.
G4 LINT — `python3 -m ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py`, repository configuration and no `--isolated`: `All checks passed!`, exit 0.
G5 CODE SUITE — `python3 -m pytest tests/orchestration/test_exec_guard.py tests/orchestration/test_dod_runners.py tests/orchestration/test_product_smoke.py -q -rf`, primary checkout: `156 passed in 29.43s`, exit 0 — the base 152 plus the four tests TESTSRB adds. Under constraint 11 this is also the refactor's equality golden: no existing test for either migrated wrapper was rewritten, renamed or moved, and all still pass.
G6 STATE READERS — `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q`: `159 passed in 20.39s`, exit 0. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q`: `42 passed in 22.25s`, exit 0.
G7 PLAN CONTRACT — `.agent/plan.md` at dbfb26af is 41 lines against the 50-line cap, the figure the block projected in constraint 7; contains `## Goal` true, contains `## Next Steps` true, matches `\bF\d{3}\b` true.
G8 ARITHMETIC — 171 registered / 27 done / 0 landed at 8ba3ad45 and 172 / 27 / 0 at HEAD; 144 open at base and 145 at HEAD; max registered R-0556 then R-0557, max resolved R-0532 at both; the registered symmetric difference is exactly `R-0557` while the done and landed symmetric differences are EMPTY; 0 duplicate ids and 0 resolutions naming an unregistered id at both SHAs; next free id R-0558.
G9 HYGIENE — measured BEFORE C6: `git diff --name-only 8ba3ad45..HEAD` holds exactly the six ordered paths and nothing else, and does NOT hold `packages/orchestration/ui_server.py`. Per-commit INSERTIONS 490, 417, 8, 53, 99, 7, 46 — none over 500, so the spent oversize allowance at d4473f85 stays untouched. Every commit has exactly one parent, the tree is clean and `git worktree list` is one line.
BLOCK SIZE, re-measured from the committed `.agent/authored/f085-r54.md`: TOTAL 490 against the 490 cap ruled by DECISION F085 D6, PROSE 225 against 400 (490 minus the 265 slice-body lines, so marker lines count as prose), RECORD22 52 against 140 — all three agree with the figures constraint 9 states.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY by its marker pair out of the committed `.agent/authored/f085-r54.md` under that block's CONVENTION; none was retyped, reflowed or taken from the delegation prompt. All eleven were used — the four FROM texts each matched their target 1x, and the four TO texts, SEAM3, TESTSRB and RECORD22 were written. The disk-to-disk comparison result is G2 above; 0 marker LINES reached any target file.

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a C0b C1 C2 C3 C4 C5 C6 ran in that order with no extra commit, no dropped commit and no reordering. NO ASSUMPTION ABOUT SLICE SHAPE WAS NEEDED: the CONVENTION states newline-inclusion, so `post == pre + slice` held byte-exactly for both code appends with no joiner and no terminator added. DECLARED, since the change set says "nothing else": five throwaway helper scripts were written under the gitignored `.remedy-wt/` (`r54_slice.py`, `r54_apply.py`, `r54_arith.py`, `r54_gate.py`, `r54_proof.py`) to do the extraction, the application and the measuring; they are untracked, no commit contains them and `git status --porcelain` is empty. The round's red control was deliberately NOT repeated; the reviewer executed it at 8ba3ad45 under block constraint 10, so no worktree was created and none was removed. R-0557's counter-measure HELD: this block's Bundle states EIGHT ordered commits and its Handback section names the same eight, with no contradicting numeral. This file is 92 lines; no DECISION D15 stated-cause overage is claimed and no section was dropped.

## Fortschritt
Fortschritt: ~93 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R53 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c KOMPLETT · T002d zur Hälfte — Naht und Extraktion in
dieser Runde, Call-Sites offen · T003 offen) — Schätzung, gegen die Klassentabelle aus
Amendment F085 D1 gemessen.

## Next
ONE: the next round is R55, which migrates the two `runtime-build` call sites in `_auto_build_frontend` (`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with `check=True`, and rewrites the `exec_guard` PARTIAL COVERAGE note in that same round if and only if the migration makes it false. Then the three `runtime-server` sites, then T003, the integration gate and closure.
TWO: R54's own verdict is NOT on disk as a gate entry, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, and R55 must not open a repair round to close it; R54's verdict is recorded by R55's OWN record slice.
THREE: 145 findings are open and R-0558 is the next free id.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk — the self-drive protocol requires every handoff that names the next session's first action to put that rule ahead of the PR Gate.
