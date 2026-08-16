# Handback — F083 CI self-check, R15 (SPLIT round, production code)

## Range

Review of 54d83919..HEAD, branch feature/f083-ci-self-check.

## Commits

### 2c075cac docs(f083): save the R15 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r15.md | +400/-0 | the block, byte-verbatim |

### 3e3fe774 docs(f083): mirror the R15 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +368/-182 | byte-identical copy of the authored file |

### 52360496 docs(f083): record the R14-REC PASS and rule DECISION F083 D3
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | RECORD-R14REC EOF-append, nothing else |

### 2750f953 fix(f083): budget each CI stage and stop standard being killed at 600s
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ci_stages.py | +7/-0 | S1-S6: `timeout_sec` field + 5 budgets |
| packages/orchestration/ci_run.py | +18/-5 | S7-S12: budget reaches runner via env |
| tests/orchestration/test_ci_run.py | +33/-4 | S13-S18: widened stand-ins, 2 new guards |
| tests/orchestration/test_ci_stages.py | +37/-0 | S19-S20: 3 new budget guards |

### ef451892 docs(f083): point the plan at the R16 budget stage
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16/-26 | PLAN slice as a whole file |

### C4 docs(f083): write the R15 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | self-reference exception (R-0149) |

## External actions

- `git worktree add .remedy-wt/redctl-r15 HEAD --detach` — ok (red control, G5).
- `git worktree remove --force …` + `git worktree prune` — ok; list back to ONE line.
- Push, post-C4 clean tree and open-PR list postdate C3, so per R-0449 they are not
  recorded here; they are reported in the round's final message. No PR created.

## Verification

| # | Gate | Real value |
|---|---|---|
| 1 | pwd / tree / worktrees / STOP | `/home/decodeux/Repos/remedy`; `git status --porcelain` EMPTY before C0a and before C4; `git worktree list` ONE line at start and at handback; `.agent/STOP` ABSENT at both |
| 2 | BASE | `54d83919d641e3d89fd099b5de93a123237747ba` — equals 54d83919: YES |
| 3 | transport + size | authored `f083-r15.md` and `last_block.md` BOTH sha256 `ed21a4676a8fb162f0a89b73ce6b793175da8eb489a37e9b9347f7ff5e975887`, 23399 bytes, 400 lines; EQUAL: True. 400 is measured here; the block declared no count |
| 4 | C1 prefix property | pre prefixes post: True; `post[len(pre):]` EQUALS the RECORD-R14REC slice extracted from the COMMITTED authored file: True (3603 bytes both); numstat `4 0`, deletions 0 |
| 5 | inventory untouched | `git diff --name-only 54d83919..HEAD -- .agent/f083_inventory.md` printed NOTHING; `^## Q\d` count = 11 (Q1..Q11) |
| 6 | C2 change set | exactly the 4 code paths above; `scripts/remedy_pytest_runner.py` NOT among them |
| 7 | ruff, repo config, repo root | `Found 26 errors.` exit 1 — equals the `## Q10` baseline of 26; this round adds none |
| 8 | CI suites, own process each | test_ci_stages.py 10 passed exit 0; test_ci_stage_selection.py 9 passed exit 0; tests/cli/test_ci_cmd.py 6 passed exit 0; test_ci_run.py 10 passed exit 0 |
| 9 | verification quartet | ui_server/test_dashboard_contract.py 70 passed exit 0; regression/test_resource_safety.py 21 passed exit 0; orchestration/test_integrity_gate.py 15 passed exit 0; canary cli/test_golden_path.py 42 passed exit 0 |
| 10 | RED CONTROL, worktree only | `timeout_sec=2100`→`600` in `.remedy-wt/redctl-r15`: exit code 1, `2 failed, 8 passed`. FAILED ids: `test_each_budget_is_the_documented_multiple_of_the_measured_maximum` (assert 600 == 2100) and `test_the_standard_budget_clears_the_runners_default_that_killed_it` (assert 600 > 600). Worktree removed and pruned; list back to ONE line |
| 11 | C3 plan | byte-equals the PLAN slice: True; sha256 `890c56124e010f3152f50e1fd6cd5f57e4c492a35e74270cfc595a879cc7514b`; 33 lines (<50); `## Goal` and `## Next Steps` present; `- [ ]` lines: 0 |
| 12 | integrity gate | exit 0; `passed` True, `fail_count` 0, `check_count` 5; handler_import pass `handlers=338`; live_review_verdict pass; plan_consistency pass `unchecked=0, context_complete=False`; relevant_untracked pass `untracked=0, relevant=0`; high_blockers_open pass |
| 13 | open set at HEAD | registered 105 / `Done:` 6 / `Landed:` 0 → open 99; max R-0477; next free R-0478; duplicates: none. Unchanged — this block registered no finding |
| 14 | insertions | C0a 400, C0b 368 (verbatim single-`.agent/`-file rewrite, AGENTS.md-exempt), C1 4, C2 95, C3 16 — none over 500 |
| 15 | no amend | I ran no `git commit --amend`, no `git rebase` and no `git reset` this round |

## Authored-text proofs

- `.agent/authored/f083-r15.md` vs `.remedy-wt/f083-r15-block.md`: byte-identical,
  sha256 `ed21a467…5887`, 23399 bytes, 400 lines, bytes read in Python.
- All 22 named units (RECORD-R14REC, S1-S20, PLAN) were extracted from the
  COMMITTED authored file by their markers and applied programmatically. Every
  PAIR's FROM matched EXACTLY ONCE; after apply each REWRITE FROM count = 0 and
  each APPEND FROM count = 1. No marker, `FROM:` or `TO:` line reached any target.

## Deviations & assumptions

1. Gate 9 named four bare filenames; resolved on disk to `tests/ui_server/`,
   `tests/regression/`, `tests/orchestration/`, `tests/cli/`. Not assumed —
   `pytest tests/cli/test_dashboard_contract.py` was tried first and exited 4,
   "file or directory not found", the vacuous-gate trap R-0438; the paths were
   then globbed and re-run. No test content changed.
2. My slice applier aborted twice mid-apply on ITS OWN shape assertions (an
   over-strict `TO.startswith(FROM)` for APPEND; then a path parse that ate
   `EOF-APPEND to …`). No slice was repaired and no block text reinterpreted: the
   4 code files were restored from `HEAD` via `git show` — NOT `git reset` — to a
   tree verified EMPTY by `git status --porcelain`, then all 20 slices re-applied
   in one pass. Nothing partial was ever staged or committed.
3. Cap overage declared (DECISION D15): this file exceeds 100 lines. Cause is
   MANDATED content only — six per-commit tables (>5 commits), the block's fifteen
   ordered gates with real values, the transport and pair proofs, and an
   item-status table the block requires to cover every gate. No section dropped.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | all four code files in one commit |
| C3 | done | |
| C4 | done | this file |
| Gate 1 | done | clean tree, one worktree, no STOP |
| Gate 2 | done | base equals 54d83919 |
| Gate 3 | done | both files equal, 400 lines |
| Gate 4 | done | prefix holds, tail equals slice |
| Gate 5 | done | inventory untouched, 11 headings |
| Gate 6 | done | four code paths, runner absent |
| Gate 7 | done | 26 errors, baseline unchanged |
| Gate 8 | done | 10 / 9 / 6 / 10, all exit 0 |
| Gate 9 | done | 70 / 21 / 15 / 42, all exit 0 |
| Gate 10 | done | RED as ordered: exit 1, two named ids |
| Gate 11 | done | plan byte-equals slice, 33 lines |
| Gate 12 | done | passed true, 0 fails, handlers=338 |
| Gate 13 | done | 105 / 6 / 0, open 99, max R-0477 |
| Gate 14 | done | 400 / 368 / 4 / 95 / 16 |
| Gate 15 | done | no amend, rebase or reset |

## Next

Reviewer re-runs all fifteen gates at HEAD and issues the R15 verdict. Before
authoring R16, re-read `.agent/STOP` from disk — Phase 1 rule 1 before rule 2.

Fortschritt: 52 % (F083 beansprucht · R1 bis R7 und R9 bis R15 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht und die Selektionstests als Code gelandet · seit R15 trägt jede Stage ihr gemessenes Wall-Clock-Budget und `standard` wird nicht mehr nach 600 Sekunden abgeschnitten · noch keine budgets-Stage, keine Determinismus-Stage, kein Lint-Ceiling, keine hosted workflows) — Rundenzahl gemessen, Prozentwert geschätzt
