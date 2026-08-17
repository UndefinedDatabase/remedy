# Handback — F085 Sandbox hardening (stage 1), R52

Feature F085 · Round R52 · Branch `feature/f085-sandbox-hardening` · Base 67475107

## Range
Review of 67475107..HEAD. Seven commits: C0a C0b C1 C2 C3 C4 C5.

## Commits
### a7896384 chore(f085): save the authored R52 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f085-r52.md` | +373/-0 | C0a — the R52 block, byte-verbatim from the reviewer's original |

### 216fe178 chore(f085): mirror the R52 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +255/-371 | C0b — the COMMITTED blob copied over; single-state-file rewrite |

### 511736d6 docs(f085): advance the plan to R52
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +11/-10 | C1 — PLAN6F→PLAN6T, the first substantive commit |

### 23a7ec30 docs(f085): record the R51 PASS and register R-0554
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +56/-0 | C2 — RECORD20 appended; R-0554 registered, nothing resolved |

### d5b1c8f6 feat(f085): add the dod-app seam to exec_guard
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/exec_guard.py` | +50/-0 | C3 — SEAM2 appended: the allowlist and the policy, no runner and no call site |

### 610fd945 test(f085): cover the dod-app policy
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_exec_guard.py` | +30/-0 | C4 — TESTSGUARD2, one test |

### C5 — self-reference, a handback cannot table the commit that writes it
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | in the round report | C5 — this file; its own insertions go to the operator |

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

## External actions
`git push -u origin feature/f085-sandbox-hardening` after C5; outcome reported to the operator. No PR, no merge, no `gh` call, no worktree add and no worktree remove.

## Verification
G1 STATE — `.agent/STOP` absent before C0a and again before C5 (`ls` exit 2 at both points); `git status --porcelain` EMPTY at round start and after each of the six commits preceding this one, whose own post-commit reading goes to the operator; `git worktree list` one line throughout.
G2 TRANSPORT — exit 0. The committed `.agent/authored/f085-r52.md`, the committed `.agent/last_block.md`, BOTH working copies and the reviewer's `.remedy-wt/f085-r52.md` are all five byte-EQUAL, disk-to-disk and not by digest fallback: sha256 dbb09a909d14afe36d188f834eba2698f195ac502d2372f92e0f89d5bda554b8, 25680 B, 373 lines, 10 marker lines — every figure measured on every copy.
G3 SHAPES — THE ONE REWRITE, PLAN6F→PLAN6T at 511736d6: FROM 1x in the pre-commit blob, 0x in the post-commit file, TO exactly 1x, `TO contains FROM: false`, 0 marker LINES, numstat `11 10`. THE PROSE APPEND, C2 / RECORD20 / `.agent/live_review.md` at 23a7ec30: byte-exact PREFIX, remainder exactly one blank line plus the slice, exact SUFFIX, 0 marker LINES, and each of the 54 non-empty lines among its 55 slice lines occurring exactly once among the 56 lines that commit adds, numstat `56 0`. THE TWO CODE APPENDS, each `pre + slice` with NO joiner byte, prefix and suffix exact, 0 marker LINES, added lines exactly the slice's lines IN ORDER: SEAM2 50 lines at d5b1c8f6 numstat `50 0`; TESTSGUARD2 30 lines at 610fd945 numstat `30 0`.
G4 LINT — `python3 -m ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py`: `All checks passed!`, exit 0.
G5 CODE SUITE — `python3 -m pytest tests/orchestration/test_dod_runners.py tests/orchestration/test_exec_guard.py tests/orchestration/test_product_smoke.py -q -rf`, primary checkout: `151 passed in 28.19s`, exit 0 — the base 150 plus the one test this round adds.
G6 STATE READERS — `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q`: `159 passed in 20.18s`, exit 0. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q`: `42 passed in 22.23s`, exit 0.
G7 PLAN CONTRACT — `.agent/plan.md` at 511736d6 is 44 lines against the 50-line cap; contains `## Goal` true, contains `## Next Steps` true, matches `\bF\d{3}\b` true.
G8 ARITHMETIC — 168 registered / 27 done / 0 landed at 67475107 and 169 / 27 / 0 at HEAD; 141 open at base and 142 at HEAD; max registered R-0553 then R-0554, max resolved R-0532 at both; the registered symmetric difference is exactly `R-0554` while the done and landed symmetric differences are EMPTY; 0 duplicate ids and 0 resolutions naming an unregistered id at both SHAs; next free id R-0555.
G9 HYGIENE — measured BEFORE C5: `git diff --name-only 67475107..HEAD` holds exactly the six ordered paths and nothing else, and does NOT hold `packages/orchestration/dod_runners.py`. Per-commit INSERTIONS 373, 255, 11, 56, 50, 30 — none over 500. Every commit has exactly one parent, the tree is clean and `git worktree list` is one line.
BLOCK SIZE, re-measured from the committed `.agent/authored/f085-r52.md`: TOTAL 373 against the 490 cap, PROSE 205 against 400 (373 minus the 168 slice-body lines, so marker lines count as prose), RECORD20 55 against 140 — all three agree with the figures constraint 9 states.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY by its marker pair out of the committed `.agent/authored/f085-r52.md`; none was retyped, reflowed or taken from the delegation prompt. All five were used — the FROM text PLAN6F matched its target 1x, and PLAN6T, RECORD20, SEAM2 and TESTSGUARD2 were written. The disk-to-disk comparison result is G2 above; 0 marker LINES reached any target file.

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a C0b C1 C2 C3 C4 C5 ran in that order with no extra commit, no dropped commit and no reordering. ASSUMPTION, stated because it is an interpretation of G3's wording: for the two CODE APPENDS the post-commit file is `pre + slice` plus the file's own trailing LINE TERMINATOR. A terminator is not a joiner byte — the block's CONVENTION rules a trailing newline not an extra line — and the R51 appends were verified on disk to have the same shape (`post == pre + slice + "\n"` holds at fcfb2a0f, `post == pre + slice` does not). Taken byte-literally the two `.py` files would end without a newline and G4 would be red. The round's red control was deliberately NOT repeated — the reviewer executed it at 67475107 under block constraint 10 — so no worktree was created and none was removed. OBSERVED, not acted on: the block's Handback section says "Six commits" while its Bundle names seven ordered commits C0a..C5; the >5-commit ≤100-line allowance applies either way. This file is 86 lines; no DECISION D15 stated-cause overage is claimed and no section was dropped.

## Fortschritt
Fortschritt: ~88 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R51 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c erste Hälfte gebaut, Naht für die zweite in dieser Runde
gebaut, `_run_app_once` wird an R53 migriert · T002d entsperrt durch Amendment F085 D8, noch nicht
gebaut · T003 offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Next
ONE: the next expected action is the reviewer gating 67475107..HEAD and issuing R52's verdict; then R53, which migrates `_run_app_once` in `packages/orchestration/dod_runners.py` onto the seam this round adds, taking the CHILD half alone through `plan_child_spawn`, and rewrites the `exec_guard` PARTIAL COVERAGE note in the same round because that note only becomes false when the call site moves. T002d follows under the DECISION F085 D8 split, then T003, the integration gate and closure.
TWO: R52's own verdict is NOT on disk as a gate entry, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, not a missing gate, and R53 must not open a repair round to close it; R52's verdict, when the reviewer issues it, is recorded by R53's OWN record slice.
THREE: 142 findings are open and R-0555 is the next free id.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk — the self-drive protocol requires that rule to be named ahead of the Open PR Gate.
