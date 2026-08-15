# Handback — F083 CI self-check, R8 (worker)

BLOCKER: gate 8 (ruff) is RED — `I001` in `apps/cli/commands/ci_cmd.py`, the
authored CI-CMD slice. Applied BYTE-VERBATIM (constraint 2), NOT repaired.
Values in gate 8, cause in deviation 1. Per G8 the round stops after C7.

## Range
Review of 2d1c6d8d..HEAD (HEAD = C7, this commit).

## Commits

### b6b2c077 docs(f083): store the R8 block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r8.md | +400/-0 | C0a — byte copy of the R8 block (shutil.copyfile) |

### 9eef9599 chore(f083): mirror the R8 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +341/-148 | C0b — byte-identical mirror; AGENTS.md-exempt single-file rewrite |

### 73a7744b docs(f083): record the R7 PASS and register R-0461 and R-0462
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +5/-0 | C1 — RECORD-R7 appended at EOF after one blank line |

### 8d94e9c1 feat(f083): add the ci command handlers and summary table
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/ci_cmd.py | +76/-0 | C2 — NEW, whole file = CI-CMD slice |

### 97d24b65 feat(f083): register the ci group and ci run catalog entry
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +16/-0 | C3 — GROUP and ENTRY append-shaped pairs |

### ce4632c1 feat(f083): wire ci_cmd into collect_all_handlers
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/__init__.py | +2/-1 | C4 — IMPORT and TUPLE rewrite pairs |

### cffe65a6 test(f083): pin the ci CLI seam and a real runner subprocess
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_ci_cmd.py | +75/-0 | C5 — NEW, whole file = TEST-CI-CMD slice |

### be27374d docs(f083): point the plan at the landed CLI seam and R9
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +9/-11 | C6 — whole-file PLAN slice |

### C7 (this commit) — self-reference
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | n/a | C7 cannot table its own SHA or count (R-0371, R-0149); both are in the worker's final message |

## External actions
None during C0a..C7. `git push -u origin feature/f083-ci-self-check` runs AFTER
C7 and is reported in the final message (R-0449/R-0452). No PR created. No
worktree added — `git worktree list` was one line throughout.

## Verification
Every value below was RUN and measured. No gate is reported as a word.

1. `git status --porcelain` EMPTY before C0a and before C7 (both checked).
   `git worktree list` = 1 line. `.agent/STOP` ABSENT at start and at handback.
2. BASE `git rev-parse HEAD` = 2d1c6d8da96f73798af64978f5525d443434fb88 —
   EQUALS the block's 2d1c6d8d.
3. TRANSPORT: scratchpad, `.agent/authored/f083-r8.md` and `.agent/last_block.md`
   are three-way byte-EQUAL — sha256
   3b7d8cfb756bc950df49c605cdc99dc36971d9ea568ace4b9e70601afd129713,
   29275 bytes, 400 lines. Measured 400 EQUALS the block's declared footer 400.
4. C1 prefix over 73a7744b^..73a7744b: `post.startswith(pre)` True;
   `post[len(pre):]` == `b"\n" + RECORD-R7` True (7653 bytes, slice extracted BY
   MARKER from the committed authored file). numstat `5 0` — deletion column 0.
5. C2 `apps/cli/commands/ci_cmd.py` byte-equals CI-CMD: sha256
   c77954d808d19bea5a9581dfd7d883a6a33f496ce1b0883d6dbe95eb33f303e4, 76 lines.
   C5 `tests/cli/test_ci_cmd.py` byte-equals TEST-CI-CMD: sha256
   60f51da8f2c7102599a993a0280947822922fb04bdab7767d39442eedc29efc4, 75 lines.
   `git diff --name-only 8d94e9c1^..8d94e9c1` = `apps/cli/commands/ci_cmd.py` ALONE.
6. C3 append-shaped pairs on the committed blob, all eight:
   GROUP-FROM 1 before / 1 after; GROUP-TO 0 / 1; ENTRY-FROM 1 / 1; ENTRY-TO 0 / 1.
   At C3: `"ci": GroupDef` 1, `command_id="ci.run"` 1, `command_id="integrity.check"` 1.
   numstat `16 0`.
7. C4 rewrite pairs at ce4632c1: IMPORT-FROM 0, IMPORT-TO 1, TUPLE-FROM 0,
   TUPLE-TO 1. `ci_cmd` occurs 2, `bench_cmd` occurs 2. numstat `2 1`.
8. RUFF over the four files in ONE run — **RED**, REAL_EXIT=1, `Found 1 error.`
   The one error: `I001 Import block is un-sorted or un-formatted`,
   `apps/cli/commands/ci_cmd.py:15:1`, `help: Organize imports`.
   ISOLATED: the same command over the OTHER THREE files alone printed
   `All checks passed!` REAL_EXIT=0 — so the RED is the CI-CMD slice's own
   bytes, not the two edited files, whose BASE exit 0 the block declared.
9. `python3 -m pytest tests/cli/test_ci_cmd.py -q` → collected 6, `6 passed in
   0.44s`, REAL_EXIT=0. The subprocess test really ran and is the slowest:
   `--durations` shows `0.29s call test_a_stage_argv_really_reaches_the_pytest_runner`.
   It did NOT exceed any budget; nothing was trimmed.
10. All four paths confirmed on disk first (R-0438), then ONE run of
    `tests/test_command_catalog.py tests/cli/test_command_catalog.py
    tests/test_grouped_cli.py tests/cli/test_cli_ux.py -q` → `601 passed in
    40.44s`, REAL_EXIT=0. BASE declared 593; the +8 is MEASURED, not assumed —
    `--collect-only -q` piped to `grep -c` counts exactly 8 collected ids naming
    the new `ci` entry. I did not re-run this gate at BASE myself (no worktree
    permitted this round), so 593 stands as the block's number, not mine.
11. Each run separately, exit code from the process, all four paths confirmed on
    disk first: dashboard contract `70 passed` exit 0; resource safety
    `21 passed` exit 0; integrity-gate tests `15 passed` exit 0; canary
    `42 passed` exit 0. Every count equals the block's expectation.
12. `git diff --name-only 2d1c6d8d..HEAD -- packages/` printed NOTHING —
    measured empty list, REAL_EXIT=0. Stage table and runner untouched.
13. INTEGRITY GATE via python3 (the `remedy` CLI is denied here): `passed` true,
    `fail_count` 0, `check_count` 5. All five pass — handler_import,
    live_review_verdict, plan_consistency, relevant_untracked, high_blockers_open.
    `handler_import` message `handlers=338`, exactly 1 above the BASE 337.
14. OPEN SET at HEAD: registered 90, `Done:` 4, `Landed:` 0, open 86, max R-0462,
    next free R-0463, NO duplicate id, resolved ids exactly R-0456..R-0459.
    Matches the block's expected 90 / 4 / 0, max R-0462, open 86 on every value.
15. C6 `.agent/plan.md` byte-equals the PLAN slice: True. sha256
    2a4bfe4ed8c3ce9b12b69e9fd4022f2961f5e67a401f739f5f71dd776cceba17, 30 lines
    (cap 50), `## Goal` present, `## Next Steps` present, `- [ ]` lines 0,
    numbered items under `## Next Steps` = 1.
16. CHANGE SET measured BEFORE this commit, `git diff --name-only 2d1c6d8d..HEAD`
    = 8 paths: `.agent/authored/f083-r8.md`, `.agent/last_block.md`,
    `.agent/live_review.md`, `.agent/plan.md`, `apps/cli/command_catalog.py`,
    `apps/cli/commands/__init__.py`, `apps/cli/commands/ci_cmd.py`,
    `tests/cli/test_ci_cmd.py`. `.agent/handoff.md` is the ninth, added by C7.
17. Insertions (`+` column only): C0a 400, C0b 341, C1 5, C2 76, C3 16, C4 2,
    C5 75, C6 9. None over 500. C0b is the AGENTS.md-exempt verbatim rewrite of a
    single `.agent/` file, reported anyway. C7's own count cannot exist inside C7.

## Authored-text proofs
All eight authored units applied BYTE-VERBATIM, every body extracted BY MARKER
from the committed `.agent/authored/f083-r8.md` by script — nothing retyped.
RECORD-R7 by the gate-4 prefix identity; CI-CMD, TEST-CI-CMD and PLAN by whole-file
byte equality (sha256 above); GROUP/ENTRY by the append-shaped 8-value count set;
IMPORT/TUPLE by FROM 0x / TO 1x. Transport is three-way byte-equal (gate 3).

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | applied verbatim; its bytes are what gate 8 fails on |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | this commit |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | |
| Gate 5 | done | |
| Gate 6 | done | |
| Gate 7 | done | |
| Gate 8 | RED | I001 in the CI-CMD slice; the round's blocker |
| Gate 9 | done | |
| Gate 10 | done | 601, not the declared 593; +8 measured to the new entry |
| Gate 11 | done | |
| Gate 12 | done | |
| Gate 13 | done | |
| Gate 14 | done | |
| Gate 15 | done | |
| Gate 16 | done | |
| Gate 17 | done | |
| push / clean tree / PR list | deviated | postdate C7 (R-0449); in the final message |

## Deviations & assumptions
1. DECLARED DEFECT IN AUTHORED TEXT (constraint 2, not a silent repair). The
   CI-CMD slice fails this round's own ruff gate: one blank line between the
   import block and `def repo_root_for_ci` where ruff's `I` rules want two.
   Evidence: gate 8 above, plus `pyproject.toml:50`
   `select = ["E", "F", "W", "I", "UP"]`, with `I001` in neither `ignore` nor
   the `tests/**` per-file-ignores. The fix is one blank line; NOT applied,
   because repairing authored text is the conduct this repository forbids.
2. AGENTS.md "If Blocked" step 2 wants the blocker written into `.agent/plan.md`.
   Gate 15 orders `.agent/plan.md` to byte-equal the PLAN slice, which names no
   blocker. I obeyed the byte-equality and put the blocker here instead, at the
   top of this file. Assumption: authored-text fidelity outranks plan prose when
   a gate measures the bytes. Flagged so the reviewer can overrule it.
3. CAP OVERAGE, DECISION D15 stated cause, naming BOTH caps as R-0462 requires.
   This file is 200 lines against the ≤100 line cap for a >5-commit bundle, and
   it is over the "≤800 tokens" hard cap by a multiple under any ratio. Cause:
   the mandated content — 9 per-commit tables, a value for all 17 gates, and an
   item-status row per C-item and per gate. No section was dropped to fit.
4. `git worktree list` stayed at 1 line; no `packages/` path changed; no PR.
   Scratch scripts live in the gitignored `.remedy-wt/.cache/f083-r8/`, so the
   tree stayed clean throughout.

## Open findings
90 registered, 4 resolved, 86 open. Max R-0462, next free R-0463. R-0461 and
R-0462 were registered by C1 this round.

## Next
R9: repair the `I001` blocker in `apps/cli/commands/ci_cmd.py` (one blank line,
via an authored slice), re-run the ruff gate, then take its first item — promote
R-0460's rule into the §3 pre-emission checklist as item 11 (R-0461) — and add
the per-stage selection tests over a fixture tree.

Fortschritt: 32 % (F083 beansprucht · R1 bis R7 PASS · Stage-Tabelle, Stage-Runner und jetzt die `remedy ci` CLI-Naht als Code gelandet, mit einem Test der wirklich einen Stage-Argv durch den Runner startet · noch kein Summary in den hosted workflows, keine Determinismus- oder Budget-Stage) — gemessen, nicht geschätzt
