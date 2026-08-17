# Handback — F085 Sandbox hardening (stage 1), R51

Feature F085 · Round R51 · Branch `feature/f085-sandbox-hardening` · Base 3a64b65e

## Range
Review of 3a64b65e..HEAD. Nine commits: C0a C0b C1 C2 C3 C4 C5 C6 C7.

## Commits
### 44a1fbde chore(f085): save the authored R51 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f085-r51.md` | +489/-0 | C0a — the R51 block, byte-verbatim from the reviewer's original |

### aa38f8c7 chore(f085): mirror the R51 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +425/-270 | C0b — the COMMITTED blob copied over; single-state-file rewrite |

### 051b4082 docs(f085): advance the plan to R51
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +13/-11 | C1 — PLAN5F→PLAN5T, the first substantive commit |

### 73489620 docs(f085): record the R50 PASS
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +38/-0 | C2 — RECORD19 appended; nothing registered, nothing resolved |

### ff93b13a docs(f085): update the exec_guard coverage note for the dod-process seam
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/exec_guard.py` | +5/-3 | C3 — HDRF→HDRT, the PARTIAL COVERAGE note |

### fcfb2a0f feat(f085): add the dod-process seam to exec_guard
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/exec_guard.py` | +77/-0 | C4 — SEAM appended: allowlist, cap, policy, runner |

### 44460d56 feat(f085): migrate the DoD process check onto the guard seam
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/dod_runners.py` | +13/-6 | C5 — DOCF→DOCT, IMPF→IMPT, SITEF→SITET |

### 43cd292a test(f085): cover the dod-process seam and its policy
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_dod_runners.py` | +52/-0 | C6 — TESTSDOD, two tests |
| `tests/orchestration/test_exec_guard.py` | +22/-0 | C6 — TESTSGUARD, one test |

### C7 — self-reference, a handback cannot table the commit that writes it
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | in the round report | C7 — this file; its own insertions go to the operator |

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
| C6 | done | |
| C7 | done | this commit |

## External actions
`git push -u origin feature/f085-sandbox-hardening` after C7; outcome reported to the operator. No PR, no merge, no `gh` call, no worktree add and no worktree remove.

## Verification
G1 STATE — `.agent/STOP` absent before C0a and again before C7 (`ls` exit 2 at both points); `git status --porcelain` EMPTY at round start and after each of the eight commits preceding this one, whose own post-commit reading goes to the operator; `git worktree list` one line throughout.
G2 TRANSPORT — exit 0. The committed `.agent/authored/f085-r51.md`, the committed `.agent/last_block.md`, BOTH working copies and the reviewer's `.remedy-wt/f085-r51.md` are all five byte-EQUAL, disk-to-disk and not by digest fallback: sha256 12c6771bf04c38f94be460b4beb48ed93ea5b37709ce1f70711f89a093703abc, 29295 B, 489 lines, 28 marker lines — every figure measured on every copy.
G3 SHAPES — THE FIVE REWRITES, each measured on its own post-commit file, FROM 0x and TO 1x in each: PLAN5F→PLAN5T at 051b4082 numstat `13 11`, HDRF→HDRT at ff93b13a numstat `5 3`, and DOCF→DOCT, IMPF→IMPT and SITEF→SITET at 44460d56 numstat `13 6`; every pair reads `TO contains FROM: false`. THE PROSE APPEND, C2 / RECORD19 / `.agent/live_review.md`: the pre-commit blob is a byte-exact PREFIX, the remainder is exactly one blank line plus the slice, the slice is an exact SUFFIX, 0 marker LINES are in the post-commit file, and each of the 37 slice lines — 0 of them empty — occurs exactly once among the 38 lines that commit adds to that path, numstat `38 0`. THE THREE CODE APPENDS, each `pre + slice` with NO joiner byte, prefix and suffix exact, 0 marker LINES, and the added lines exactly the slice's lines IN ORDER: SEAM 77 lines at fcfb2a0f numstat `77 0`; TESTSDOD 52 lines numstat `52 0` and TESTSGUARD 22 lines numstat `22 0`, both at 43cd292a.
G4 LINT — `python3 -m ruff check packages/orchestration/exec_guard.py packages/orchestration/dod_runners.py tests/orchestration/test_dod_runners.py tests/orchestration/test_exec_guard.py`: `All checks passed!`, exit 0.
G5 CODE SUITE — `python3 -m pytest tests/orchestration/test_dod_runners.py tests/orchestration/test_exec_guard.py tests/orchestration/test_product_smoke.py -q -rf`, primary checkout: `150 passed in 28.17s`, exit 0 — the base 147 plus the three tests this round adds.
G6 STATE READERS — `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q`: `159 passed in 19.83s`, exit 0. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q`: `42 passed in 20.41s`, exit 0.
G7 PLAN CONTRACT — `.agent/plan.md` at 051b4082 is 43 lines against the 50-line cap; contains `## Goal` true, contains `## Next Steps` true, matches `\bF\d{3}\b` true.
G8 ARITHMETIC — 168 registered / 27 done / 0 landed at BOTH 3a64b65e and HEAD; 141 open at both; max registered R-0553, max resolved R-0532; the registered, done and landed symmetric differences are all EMPTY; 0 duplicate ids and 0 resolutions naming an unregistered id at both SHAs; next free id R-0554.
G9 HYGIENE — measured BEFORE C7: `git diff --name-only 3a64b65e..HEAD` holds exactly the eight ordered paths and nothing else. Per-commit INSERTIONS 489, 425, 13, 38, 5, 77, 13, 74 — none over 500. Every commit has exactly one parent, the tree is clean and `git worktree list` is one line.
BLOCK SIZE, re-measured from the committed `.agent/authored/f085-r51.md`: TOTAL 489 against the 490 cap, PROSE 226 against 400 (489 minus the 263 slice-body lines, so marker lines count as prose), RECORD19 37 against 140 — all three agree with the figures the block states.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY by its marker pair out of the committed `.agent/authored/f085-r51.md`; none was retyped, reflowed or taken from the delegation prompt. All fourteen were used — the five FROM texts PLAN5F, HDRF, DOCF, IMPF and SITEF matched their targets, and the nine texts PLAN5T, HDRT, DOCT, IMPT, SITET, SEAM, TESTSDOD, TESTSGUARD and RECORD19 were written. The disk-to-disk comparison result is G2 above; 0 marker LINES reached any target file.

## Deviations & assumptions
None. No departure from the block's ordered commit sequence: C0a C0b C1 C2 C3 C4 C5 C6 C7 ran in that order with no extra commit, no dropped commit and no reordering. The round's two red controls were deliberately NOT repeated — the reviewer had already executed them at 3a64b65e under block constraint 10 — so no worktree was created and none was removed. This file is 99 lines: more than five commits, so the ≤100-line allowance applies and no DECISION D15 stated-cause overage is claimed. No section was dropped to meet the cap.

## Fortschritt
Fortschritt: ~87 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R50 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c erste Hälfte in dieser Runde gebaut, `_run_app_once`
offen · T002d entsperrt durch Amendment F085 D8, noch nicht gebaut · T003 offen) — Schätzung,
gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Next
ONE: the next expected action is the reviewer gating 3a64b65e..HEAD and issuing R51's verdict; then R52, which implements T002c's second half — `_run_app_once` under the dod-app policy, taking the CHILD half alone through `plan_child_spawn`; T002d then follows under the D8 split, then T003, the integration gate and closure.
TWO: R51's own verdict is NOT on disk as a gate entry, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, not a missing gate, and R52 must not open a repair round to close it; R51's verdict, when the reviewer issues it, is recorded by R52's OWN record slice.
THREE: 141 findings are open and R-0554 is the next free id.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk — the self-drive protocol requires that rule to be named ahead of the Open PR Gate.
