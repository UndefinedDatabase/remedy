# Handback — F085 Sandbox hardening (stage 1), R53

Feature F085 · Round R53 · Branch `feature/f085-sandbox-hardening` · Base 3bafcc1e

## Range
Review of 3bafcc1e..HEAD. Eight commits: C0a C0b C1 C2 C3 C4 C5 C6.

## Commits
### 94e4da84 chore(f085): save the authored R53 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f085-r53.md` | +429/-0 | C0a — the R53 block, byte-verbatim from the reviewer's original |

### 8267fde9 chore(f085): mirror the R53 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +340/-284 | C0b — the COMMITTED blob copied over; single-state-file rewrite |

### 2e136a4e docs(f085): advance the plan to R53
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +9/-11 | C1 — PLAN7F→PLAN7T, the first substantive commit |

### d5fe684c docs(f085): record the R52 PASS and register R-0555 and R-0556
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +63/-0 | C2 — RECORD21 appended; R-0555 and R-0556 registered, nothing resolved |

### de4f2057 docs(f085): update the exec_guard coverage note for the dod-app seam
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/exec_guard.py` | +6/-5 | C3 — HDRF2→HDRT2; only C4 below makes that PARTIAL COVERAGE note false |

### bbd35e23 feat(f085): migrate the DoD app harness onto the guard seam
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/dod_runners.py` | +27/-7 | C4 — DOCF2→DOCT2, IMPF2→IMPT2, SITEF2→SITET2: docstring, import, `_run_app_once` call site |

### 85f5da00 test(f085): cover the dod-app seam at the harness call site
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_dod_runners.py` | +41/-0 | C5 — TESTSDOD2, one test |

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
G2 TRANSPORT — exit 0. The committed `.agent/authored/f085-r53.md`, the committed `.agent/last_block.md`, BOTH working copies and the reviewer's `.remedy-wt/f085-r53.md` are all five byte-EQUAL, disk-to-disk and not by digest fallback: sha256 58a4c90c25772d8c0083afd808474e69bf96cb3c27033eb652dca7cba28f1825, 28869 B, 429 lines, 24 marker lines — every figure measured on every copy.
G3 SHAPES — THE FIVE REWRITES, each measured separately over its own post-commit file, FROM 0x and TO exactly 1x in every case, each FROM 1x in its pre-commit blob: PLAN7F→PLAN7T at 2e136a4e numstat `9 11`; HDRF2→HDRT2 at de4f2057 numstat `6 5`; DOCF2→DOCT2, IMPF2→IMPT2 and SITEF2→SITET2 all at bbd35e23, that path's numstat `27 7`. THE PROSE APPEND, C2 / RECORD21 / `.agent/live_review.md` at d5fe684c: byte-exact PREFIX, remainder exactly one blank line plus the slice, exact SUFFIX, 0 marker LINES, and each of the 60 non-empty lines among its 62 slice lines occurring exactly once among the 63 lines that commit adds, numstat `63 0`. THE CODE APPEND, C5 / TESTSDOD2 at 85f5da00: `post == pre + slice` exactly — no byte between them and none appended after — prefix and suffix exact, the commit's added lines exactly the slice's 41 lines IN ORDER, 0 marker LINES, numstat `41 0`.
G4 LINT — `python3 -m ruff check packages/orchestration/exec_guard.py packages/orchestration/dod_runners.py tests/orchestration/test_dod_runners.py`: `All checks passed!`, exit 0.
G5 CODE SUITE — `python3 -m pytest tests/orchestration/test_dod_runners.py tests/orchestration/test_exec_guard.py tests/orchestration/test_product_smoke.py -q -rf`, primary checkout: `152 passed in 28.59s`, exit 0 — the base 151 plus the one test this round adds.
G6 STATE READERS — `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q`: `159 passed in 19.99s`, exit 0. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q`: `42 passed in 20.37s`, exit 0.
G7 PLAN CONTRACT — `.agent/plan.md` at 2e136a4e is 42 lines against the 50-line cap, the figure the block projected; contains `## Goal` true, contains `## Next Steps` true, matches `\bF\d{3}\b` true.
G8 ARITHMETIC — 169 registered / 27 done / 0 landed at 3bafcc1e and 171 / 27 / 0 at HEAD; 142 open at base and 144 at HEAD; max registered R-0554 then R-0556, max resolved R-0532 at both; the registered symmetric difference is exactly `R-0555` and `R-0556` while the done and landed symmetric differences are EMPTY; 0 duplicate ids and 0 resolutions naming an unregistered id at both SHAs; next free id R-0557.
G9 HYGIENE — measured BEFORE C6: `git diff --name-only 3bafcc1e..HEAD` holds exactly the seven ordered paths and nothing else, and does NOT hold `tests/orchestration/test_exec_guard.py`. Per-commit INSERTIONS 429, 340, 9, 63, 6, 27, 41 — none over 500, so the spent oversize allowance at d4473f85 stays untouched. Every commit has exactly one parent, the tree is clean and `git worktree list` is one line.
BLOCK SIZE, re-measured from the committed `.agent/authored/f085-r53.md`: TOTAL 429 against the 490 cap, PROSE 231 against 400 (429 minus the 198 slice-body lines, so marker lines count as prose), RECORD21 62 against 140 — all three agree with the figures constraint 9 states.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY by its marker pair out of the committed `.agent/authored/f085-r53.md` under that block's CONVENTION; none was retyped, reflowed or taken from the delegation prompt. All twelve were used — the five FROM texts each matched their target 1x, and the five TO texts, RECORD21 and TESTSDOD2 were written. The disk-to-disk comparison result is G2 above; 0 marker LINES reached any target file.

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a C0b C1 C2 C3 C4 C5 C6 ran in that order with no extra commit, no dropped commit and no reordering. NO ASSUMPTION WAS NEEDED this round: the block's CONVENTION states newline-inclusion explicitly, so `post == pre + slice` held byte-exactly for TESTSDOD2 with no joiner and no terminator added — the R-0556 counter-measure worked on its first use. The round's red control was deliberately NOT repeated; the reviewer executed it at 3bafcc1e under block constraint 10, so no worktree was created and none was removed. OBSERVED, not acted on: the block's Handback section says "seven commits" while its Bundle and its own item-status enumeration in the same sentence name eight ordered commits C0a..C6 — the R-0555 class recurring in the next block — and the >5-commit ≤100-line allowance applies identically either way. This file is 92 lines; no DECISION D15 stated-cause overage is claimed and no section was dropped.

## Fortschritt
Fortschritt: ~91 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R52 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c KOMPLETT in dieser Runde · T002d entsperrt durch
Amendment F085 D8, noch nicht gebaut · T003 offen) — Schätzung, gegen die Klassentabelle aus
Amendment F085 D1 gemessen.

## Next
ONE: the next expected action is the reviewer gating 3bafcc1e..HEAD and issuing R53's verdict; then R54, which implements T002d under the DECISION F085 D8 split — `runtime-server` takes no wall timeout and `runtime-build` keeps the one it already has — and which also extracts the guard-result translation the `test` and `dod-process` seams each carry, now that three uses show its shape. Then T003, the integration gate and closure.
TWO: R53's own verdict is NOT on disk as a gate entry, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, not a missing gate, and R54 must not open a repair round to close it; R53's verdict, when the reviewer issues it, is recorded by R54's OWN record slice.
THREE: 144 findings are open and R-0557 is the next free id.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk — the self-drive protocol requires every handoff that names the next session's first action to name that rule ahead of the Open PR Gate.
