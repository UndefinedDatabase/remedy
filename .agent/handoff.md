# Handback — F083 CI self-check, round R10

Branch: feature/f083-ci-self-check. BASE 98900254 — gate 2 re-derived
`git rev-parse HEAD` before the first commit as 989002546d3de7417890d5040498c9f995fef82a, EQUAL to 98900254.

Deviations, declared: this handback is 184 lines against BOTH caps — the AGENTS.md
handoff cap (≤60, ≤100 with >5 commit tables) and the handback-template ≤800-token
cap. Cause is mandated content only: six per-commit tables, nineteen ordered gate
values, and a 26-row item-status table covering seven C-items and all nineteen
gates. No section was dropped and no prose was padded.

## Range

Review of 98900254..HEAD.

## Commits

### 6957b0ab C0a docs(f083): archive the R10 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f083-r10.md` | +399/-0 | byte copy of the scratchpad original |

### 91ccb7e8 C0b docs(f083): mirror the R10 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +310/-161 | byte-identical mirror of the authored file |

### 35b5e4fa C1 docs(f083): record the R9 PASS and register R-0465 to R-0467
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +7/-0 | RECORD-R9 appended at EOF, one body |

### 648671ee C2 test(f083): pin each CI stage selection against a fixture tree
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_ci_stage_selection.py` | +131/-0 | TESTFILE, new file whole |
| `tests/orchestration/test_ci_stages.py` | +1/-1 | DOCSTRING rewrite pair |

### c988d4cf C3 docs(f083): promote the dry-run rule to checklist item 12
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +21/-1 | OPENER rewrite + ITEM12 append |

### f7b04bff C4 docs(f083): point the plan at the R11 stage work
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +9/-10 | PLAN slice, whole file |

### C5 — this commit, `.agent/handoff.md`
A commit cannot table its own SHA or its own insertion count (R-0371, R-0149).
C5's SHA and `+` count are reported in the final message instead of invented here.

## External actions

- `git worktree add .remedy-wt/redproof-r10 HEAD --detach` — added at 648671ee (gate 8).
- `git worktree remove .remedy-wt/redproof-r10 --force` — removed inside the same
  gate; `git worktree list` is ONE line again.
- `git push -u origin feature/f083-ci-self-check` — runs AFTER C5, so it postdates
  this file (R-0449/R-0452); result in the final message. No PR created.

## Verification — every ordered gate, real values

1. `pwd` = /home/decodeux/Repos/remedy (printed first). `git status --porcelain`
   EMPTY before the first commit and before C5. `git worktree list` ONE line at
   round start and at handback. `.agent/STOP` ABSENT at both.
2. BASE 989002546d3de7417890d5040498c9f995fef82a = 98900254. Equal: YES.
3. TRANSPORT, read in Python: scratchpad, `.agent/authored/f083-r10.md` and
   `.agent/last_block.md` all sha256 ebfb3238fb9e18a3374805ba0adb3e9c2c51d22eb1e88566db69a2285f2d9880,
   31090 bytes, 399 lines. All three EQUAL: YES. Declared footer 399 lines: EQUAL.
4. C1 PREFIX over 35b5e4fa^..35b5e4fa: pre 188545 bytes, post 195613 bytes,
   `post.startswith(pre)` True, `post[len(pre):] == b"\n" + RECORD-R9` True
   (slice extracted by marker from the committed authored file). numstat 7 0 —
   deletion column 0.
5. C2: `tests/orchestration/test_ci_stage_selection.py` byte-equals TESTFILE,
   sha256 fbffda72e407c1a0ed12d99ee5a473beaccb64f9bd4fc000e556a987e7d9ce7e (EQUALS
   the declared digest), 6138 bytes, 131 lines. At C2 over the whole
   `test_ci_stages.py`: DOCSTRING-FROM 0x, DOCSTRING-TO 1x. numstat: 131 0 and 1 1.
6. `python3 -m ruff check tests/orchestration/test_ci_stage_selection.py` (repo
   root, no `--isolated`, no substituted flag) → `All checks passed!`, REAL_EXIT=0.
7. `python3 -m pytest tests/orchestration/test_ci_stage_selection.py -q` →
   `9 passed in 7.57s`, REAL_EXIT=0 — matches the reviewer's dry run.
8. RED CONTROL, in the disposable worktree only: the union test FAILED —
   `1 failed in 16.80s`, REAL_EXIT=1, `AssertionError: tests/cli/test_redproof_slow_only.py::test_case`
   / `1/17046 tests collected (17045 deselected)` / `assert 0 == 5`. COLOUR: RED.
   The primary checkout was never mutated (`git status --porcelain` empty
   throughout; no such file under the primary `tests/cli/`). After removal,
   `git worktree list` is ONE line.
9. C3 pairs over the whole file at c988d4cf: OPENER-FROM 0x, OPENER-TO 1x;
   ITEM12-FROM 1x BEFORE and 1x AFTER, ITEM12-TO 0x before and 1x after. Numerals
   at C3: `  12. **A dry run` 1, `  11. **A convention paragraph` 1, `  13. **` 0,
   `twelve checks mechanically` 1, `eleven checks mechanically` 0. numstat 21 1.
10. `python3 -m pytest tests/orchestration/test_ci_stages.py -q` → `7 passed`,
    REAL_EXIT=0 (BASE 7/7/0 — unmoved).
11. `python3 -m pytest tests/cli/test_ci_cmd.py -q` → `6 passed`, REAL_EXIT=0.
12. Four catalog paths confirmed on disk first, then ONE run →
    `601 passed in 39.59s`, REAL_EXIT=0. MEASURED 601, unmoved from BASE.
13. VERIFICATION, four separate runs, real exit from each process:
    dashboard_contract `70 passed` 0; resource_safety `21 passed` 0;
    integrity_gate `15 passed` 0; canary golden_path `42 passed` 0.
14. `git diff --name-only 98900254..HEAD -- packages/ apps/ docs/roadmap/` printed
    NOTHING (measured list: empty, `wc -l` = 0), run from /home/decodeux/Repos/remedy.
15. INTEGRITY GATE via Python: passed True, fail_count 0, check_count 5;
    handler_import pass `handlers=338`; live_review_verdict pass; plan_consistency
    pass `unchecked=0, context_complete=False`; relevant_untracked pass
    `untracked=0, relevant=0`; high_blockers_open pass.
16. OPEN SET at HEAD: registered 95, `Done:` 5, `Landed:` 0 → open 90; max R-0467,
    next free R-0468, no duplicate id. Matches the expected 95 / 5 / 0.
17. C4 `.agent/plan.md` byte-equals PLAN, sha256
    0518bf2d9cbde3f8e393b5e7f726235dfb4a40f4be0c89467dab083dd460b5dc, 29 lines
    (<50), `## Goal` and `## Next Steps` present, zero `- [ ]` lines, 1 numbered
    item under `## Next Steps`.
18. CHANGE SET at C4: 7 paths — `.agent/authored/f083-r10.md`,
    `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
    `docs/agents/planner_reviewer_prompt.md`,
    `tests/orchestration/test_ci_stage_selection.py`,
    `tests/orchestration/test_ci_stages.py`. `.agent/handoff.md` is the EIGHTH path,
    added by C5.
19. Insertions (`+` only): C0a 399, C0b 310 (verbatim single-`.agent/`-file
    rewrite, AGENTS.md-exempt, reported anyway), C1 7, C2 132, C3 21, C4 9. None
    over 500. C5's own count cannot exist inside C5 — final message.

## Authored-text proofs

All nine authored units were extracted BY MARKER with a Python script from the
COMMITTED `.agent/authored/f083-r10.md` and applied byte-verbatim; no retyping,
reflow or stripping, and no formatter was run. sha256 / bytes / lines:
RECORD-R9 ccd35335…bc43 7067 6; TESTFILE fbffda72…ce7e 6138 131; DOCSTRING-FROM
fb339e4e…36f8 80 1; DOCSTRING-TO 72c494c0…f37f 93 1; OPENER-FROM 4d09ad4c…04a0
82 1; OPENER-TO 63b7c487…b345 82 1; ITEM12-FROM f3a49657…7ce9 76 1; ITEM12-TO
8a530ad2…172e 1618 21; PLAN 0518bf2d…b5dc 1463 29. Whole-file slices proved by
byte equality on disk (TESTFILE, PLAN); pair slices proved by the counts in gates
5 and 9; RECORD-R9 proved by the C1 prefix property in gate 4.

## Deviations & assumptions

One, and it is the stated-cause cap overage declared at the top of this file
(184 lines; both caps named there). No block text was repaired: every gate ran,
every ordered value was reproduced, and no slice required a change. Cross-check: gate 8's collection total
17046 = 17036 (the reviewer's BASE reading in R-0467) + 9 tests added by C2 + the
1 red-control test, so the two independent measurements agree.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit; own SHA and `+` count deferred to the final message |
| Gate 1 | done | |
| Gate 2 | done | BASE equal to 98900254 |
| Gate 3 | done | three-way byte-equal, 399 lines = declared footer |
| Gate 4 | done | tail equals newline + RECORD-R9, deletions 0 |
| Gate 5 | done | digest equals the declared one |
| Gate 6 | done | exit 0 |
| Gate 7 | done | 9 passed, exit 0 |
| Gate 8 | done | RED reproduced, exit 1; worktree removed |
| Gate 9 | done | six pair readings + five numerals as ordered |
| Gate 10 | done | 7 passed, exit 0 |
| Gate 11 | done | 6 passed, exit 0 |
| Gate 12 | done | 601 passed, exit 0 |
| Gate 13 | done | 70 / 21 / 15 / 42 passed, each exit 0 |
| Gate 14 | done | empty, run from the repository root |
| Gate 15 | done | passed true, 0 failures, 5 checks, handlers=338 |
| Gate 16 | done | 95 / 5 / 0, open 90, max R-0467 |
| Gate 17 | done | byte-equal, 29 lines |
| Gate 18 | done | seven paths |
| Gate 19 | done | none over 500 |

## Open findings

95 registered, 5 resolved, open 90. Max id R-0467, next free id R-0468.
R-0465, R-0466 and R-0467 registered this round; R-0467 carries a `Done:` line
because C2 lands the live union guard that closes it.

Fortschritt: 38 % (F083 beansprucht · R1 bis R7 und R9 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner und die `remedy ci` CLI-Naht als Code gelandet, dazu die Selektionstests, die jede Marker-Expression gegen einen Fixture-Baum festnageln, plus ein Live-Wächter gegen Tests, die keine Stage erfasst · noch keine hosted workflows, keine Determinismus- oder Budget-Stage) — gemessen, nicht geschätzt

## Next

R11 adds the determinism and budget stages plus the guard-test wiring, and
measures `fast` under `-n auto` so a runtime budget can rest on data.
