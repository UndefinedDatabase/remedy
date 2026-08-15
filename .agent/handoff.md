# Handoff — F083 CI self-check, R6 (runner repairs)

Branch: feature/f083-ci-self-check. Worker round R6/13, delegated.

## Range

Review of 81af8a98..HEAD — the eight commits below plus the handoff commit.

## Commits

### 392e2078 docs(f083): save the R6 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r6.md | +346/-0 | C0a, byte copy of the scratchpad original |

### 0d887d30 docs(f083): mirror the R6 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +235/-271 | C0b, byte-identical mirror |

### 2a1c4263 docs(f083): record the R5 verdict in the live review
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C1, GATE-R5-BLOCK appended at EOF |

### 7e8c3a7b docs(f083): register R-0456 to R-0459 from the R5 review
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-0 | C2, FINDINGS appended at EOF |

### 7158c1ef docs(f083): repair the round map for the runner repair round
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +7/-6 | C3, STEPS-FROM to STEPS-TO in place |

### fb9ddf12 fix(f083): anchor the CI stage run and make an empty run red
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ci_run.py | +18/-6 | C4, RUNNER/INJECT/CALL/EXIT pairs |
| tests/orchestration/test_ci_run.py | +26/-4 | C4, ASSERT + LAMBDAS pairs, TESTS-APPEND |

### 5fbda7d2 docs(f083): mark R-0456 to R-0459 landed
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +5/-0 | C5, LANDED appended at EOF |

### 9bd7b584 docs(f083): point the plan at the runner repairs and one next round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +12/-15 | C6, PLAN whole-file replacement |

### C7 — this commit, self-reference
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C7 cannot table its own SHA or insertion count (R-0371, R-0149); both are in the worker's final message |

## External actions

None before C7. `git push -u origin feature/f083-ci-self-check` runs AFTER C7 per
the block's closing paragraph, so its result is reported in the final message and
not here. No PR created, no worktree added or removed.

## Verification

1. `git status --porcelain` empty before the first commit and before C7;
   `git worktree list` ONE line throughout; `.agent/STOP` absent at round start
   and at handback.
2. BASE `git rev-parse HEAD` = 81af8a98769e38a72c7b9cf0003d15e41d79c86b — EQUALS
   the declared 81af8a98.
3. TRANSPORT: scratchpad, `.agent/authored/f083-r6.md`, `.agent/last_block.md` all
   sha256 7c6acd4e1202d599bdcbff83b7e31c0e8e870f3e18a8a832ce60052450024540,
   30218 bytes, 346 lines, three-way byte-equal; 346 equals the declared footer.
4. C1 prefix property 158500 B to 161685 B, tail byte-equal `b"\n" + GATE-R5-BLOCK`,
   numstat `2 0`. C2 161685 B to 167607 B, tail byte-equal `b"\n" + FINDINGS`,
   numstat `8 0`. Deletion column 0 in both.
5. C3 whole file: STEPS-FROM 0x, STEPS-TO 1x. `repairs R-0456 to R-0458 and the
   cwd anchor` 1 · `R11 T003 the hosted workflow files` 1 · `R10 T003 the hosted
   workflow files` 0 · `Steps` occurs 25x. Numstat `7 6`.
6. C4 out of fb9ddf12: `ci_run.py` sha256 fa999c062b9f41e3…, 3908 B, 106 lines,
   numstat `18 6`; `test_ci_run.py` sha256 72cb197350dcd70b…, 3055 B, 103 lines,
   numstat `26 4`. In ci_run.py, measured 0 each: `check=False).returncode` ·
   `Callable[[list[str]], int]` · `stage, repo_root))` · `A skipped stage is not
   a pass` · `for r in results if r.ran`. Measured 1 each:
   `check=False, cwd=cwd).returncode` · `Callable[[list[str], Path], int]` ·
   `stage_command(stage, repo_root), repo_root)` · `ran = [result for result in
   results if result.ran]` · `cwd: Path) -> int:`. In test_ci_run.py, measured 0
   each: `"pytest" not in command[1:2]` · `lambda command:`. Measured 1 each:
   `command[1:3] != ["-m", "pytest"]`, and the two new test definitions
   `test_the_stage_run_is_anchored_at_the_repository_root` and
   `test_a_run_in_which_nothing_ran_is_not_green`. `lambda command, cwd:` = 3.
7. TESTS-APPEND: committed test file ENDS with the slice True; the two lines
   immediately before it are both empty True.
8. `ruff check packages/orchestration/ci_run.py tests/orchestration/test_ci_run.py`
   exit 0, "All checks passed!". `pytest tests/orchestration/test_ci_run.py -q`
   8 collected, 8 passed, exit 0 — the 6 at BASE plus the 2 TESTS-APPEND adds.
   `packages.orchestration.ci_run.__file__` =
   /home/decodeux/Repos/remedy/packages/orchestration/ci_run.py, PRIMARY checkout.
9. `pytest tests/orchestration/test_ci_stages.py -q` 7 collected, 7 passed,
   exit 0 — equals the reviewer's BASE reading; the stage table is untouched.
10. C6 plan sha256 ec12ddca9d07febd0dac3264725ff316bcc7a09d07fabc5a40b551220ea7ed23,
    byte-equal to the PLAN slice as a whole file, 32 lines (<50), `## Goal` and
    `## Next Steps` present, `- [ ]` count 0, numbered Next Steps items 1.
11. CHANGE SET `git diff --name-only 81af8a98..HEAD` before C7, count 6:
    .agent/authored/f083-r6.md · .agent/last_block.md · .agent/live_review.md ·
    .agent/plan.md · packages/orchestration/ci_run.py ·
    tests/orchestration/test_ci_run.py. Restricted to apps/, scripts/, docs/ the
    measured list is EMPTY; the measured list of ci_stages.py, test_ci_stages.py
    and .agent/f083_inventory.md entries is EMPTY.
12. `pytest tests/ui_server/test_dashboard_contract.py -q` 70 passed exit 0 [70/70,0];
    `tests/regression/test_resource_safety.py -q` 21 passed exit 0 [21,0];
    `tests/orchestration/test_integrity_gate.py -q` 15 passed exit 0 [15,0];
    canary `tests/cli/test_golden_path.py -q` 42 passed exit 0 [42/42,0].
13. OPEN SET at HEAD: 87 registered, 0 `Done:`, 4 `Landed:`; registered minus done
    87; max R-0459; next free R-0460; no duplicate id. Reviewer expected 87/0/4
    with max R-0459 — matched.
14. INTEGRITY GATE (Python; `remedy` CLI denied this session): passed true,
    fail_count 0, check_count 5 — handler_import pass (handlers=337),
    live_review_verdict pass, plan_consistency pass (unchecked=0),
    relevant_untracked pass (untracked=0), high_blockers_open pass.
15. Insertions: C0a 346 · C0b 235 · C1 2 · C2 8 · C3 7 · C4 44 · C5 5 · C6 12.
    None over 500. C0b is a verbatim single-`.agent/`-file rewrite and exempt by
    the AGENTS.md counting rule; reported anyway. C7's own count is in the final
    message, since it cannot exist inside C7.

## Authored-text proofs

Every slice was extracted BY MARKER from the COMMITTED
`.agent/authored/f083-r6.md` — never from the scratchpad, never retyped — and
compared byte-for-byte in Python. GATE-R5-BLOCK, FINDINGS, LANDED: appended tails
byte-equal `b"\n" + slice`. STEPS: FROM 1x before / 0x after, TO 0x before / 1x
after. RUNNER, INJECT, CALL, EXIT, ASSERT: each FROM occurred exactly 1x before
replacement. LAMBDAS: three separate lines, each exactly 1x, replaced one-for-one
in file order. TESTS-APPEND: committed file ends with the slice after two empty
lines. PLAN: `.agent/plan.md` byte-equals the slice as a whole file.

## Deviations & assumptions

1. DECLARED DEFECT IN THE BLOCK'S TEXT — not silently repaired, not routed
   around. The SLICE CONVENTION paragraph enumerates "five REWRITE pairs and one
   end-of-file append in the two code files", while the bundle's C4 line orders
   "all six repair pairs plus the test append". Six pairs exist on disk: RUNNER,
   INJECT, CALL, EXIT in `packages/orchestration/ci_run.py`; ASSERT, LAMBDAS in
   `tests/orchestration/test_ci_run.py`. The two clauses disagree with each
   other, and the disk agrees with the C4 line. That same paragraph also states
   "No numeral is stated for that list" while stating "two", "one" and "five"
   inside it. I applied SIX pairs, because gate 6 is satisfiable only with all
   six applied (`Callable[[list[str], Path], int]` must be 1 and
   `lambda command, cwd:` must be 3) and every ordered literal came out at its
   ordered value. No slice was altered. Reviewer to rule on the wording.
2. Stated-cause overage (DECISION D15): this handoff is 196 lines against the
   ≤100 cap for a >5-commit bundle. The cause is mandated content only — eight
   per-commit changed-files tables, the fifteen ordered gate values, and the
   item-status table carrying every C-item and every gate as its own row. No
   section was dropped and no prose was padded to reach that length.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | six pairs applied; see Deviations 1 |
| C5 | done | |
| C6 | done | |
| C7 | done | this commit |
| Gate 1 tree / worktree / STOP | done | |
| Gate 2 BASE SHA | done | equals 81af8a98 |
| Gate 3 TRANSPORT | done | |
| Gate 4 C1+C2 prefix property | done | |
| Gate 5 C3 rewrite pair | done | |
| Gate 6 C4 code literals | done | |
| Gate 7 TESTS-APPEND tail | done | |
| Gate 8 C4 runs green | done | |
| Gate 9 stage table still runs | done | |
| Gate 10 C6 plan | done | |
| Gate 11 change set | done | |
| Gate 12 verification suites | done | |
| Gate 13 open set | done | |
| Gate 14 integrity gate | done | |
| Gate 15 insertions | done | |

Open findings: 87 registered, 0 resolved. R-0456 to R-0459 are marked Landed this
round and await the reviewer's Done. Max id R-0459, next free id R-0460.

## Next

R7 builds the T001 CLI seam: the `remedy ci [--stage NAME] [--json]` catalog
group, its entry and a `COMMAND_HANDLERS` module, plus the summary table it
prints, which states the accepted `standard`/`smoke` double-run. The next
session's first action is Phase 1 rule 1 — re-read `.agent/STOP` from disk —
before the Open PR Gate.

Fortschritt: 22 % (F083 beansprucht · R1 bis R5 PASS · Marker-Inventar gemessen · Stage-Set per DECISION F083 D2 entschieden · Stage-Tabelle und Stage-Runner als Code gelandet · Runner-Defekte R-0456 bis R-0458 repariert · noch keine CLI, kein Summary, keine hosted workflows) — gemessen, nicht geschätzt
