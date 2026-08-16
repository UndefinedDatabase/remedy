# Handback — F083 R18 (the budgets stage, the R-0468 ruling, the determinism shape)

Feature T2_F083 CI self-check · Round R18 · Branch `feature/f083-ci-self-check`
Base ab1d2344 · C0a 2facdb97 · C0b 3d2c1310 · C1 56c463e1 · C2 03c2a5d7 · C3 26217cd4 ·
C4 75dda620 · C5 03fdd2bc · C6 ad01827b · C7 = this commit.
This round wrote PRODUCTION CODE. SPLIT round: nothing below is self-certified.

## Range
Review of ab1d2344..HEAD.

## Commits

### 2facdb97 docs(f083): save the R18 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r18.md | +290/-0 | R18 block saved byte-verbatim (C0a) |

### 3d2c1310 docs(f083): mirror the R18 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +270/-156 | byte-identical copy of the committed authored file (C0b) |

### 56c463e1 docs(f083): record the R17-REPAIR PASS and register R-0482
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | RECORD-R17 EOF-append; no committed text edited (C1) |

### 03c2a5d7 feat(f083): add the ratcheted lint ceiling and its checks
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ci_budgets.py | +86/-0 | BudgetCheck, LINT_ERROR_CEILING=26, parser, ceiling check (C2) |
| tests/orchestration/test_ci_budgets.py | +92/-0 | parse/ceiling cases plus the one live `subprocess` ratchet test (C2) |

### 26217cd4 docs(f083): record the Q12 budgets selection measurement
| Path | +/- | Reason |
|---|---|---|
| .agent/f083_inventory.md | +56/-0 | `## Q12`, three samples of the budgets selection (C3) |

### 75dda620 feat(f083): add the budgets stage and path-based stage selection
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ci_stages.py | +38/-5 | `test_paths` field, the `budgets` stage, argv append, D4 absence (C4) |
| tests/orchestration/test_ci_stage_selection.py | +33/-18 | union/overlap properties scoped to marker-selected stages (C4) |
| tests/orchestration/test_ci_stages.py | +32/-6 | name tuple, Q12 budget, both argv shapes, the path-resolves test (C4) |

### 03fdd2bc docs(f083): rule D4 and D5 and amend the feature file
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +62/-0 | DECISION F083 D4 and D5 in the file's existing entry shape (C5) |
| docs/roadmap/features/T2_F083.md | +19/-7 | Design stage list loses `determinism`, gains D4; T002 amended (C5) |

### ad01827b docs(f083): advance the plan to R19
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +24/-23 | PLAN slice applied as a whole file (C6) |

### C7 docs(f083): write the R18 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | C7; a handoff cannot table its own commit (R-0149) |

## External actions
`git push -u origin feature/f083-ci-self-check` runs AFTER C7. That push result, the post-C7
`git status --porcelain` and the open-PR list postdate this file (R-0449) and are reported in
the round report, not here. No PR was created or merged. ONE worktree was added and removed:
`.remedy-wt/redctl`, for gates 10 and 11 only.

## Verification — item status and measured values
Status values: done / skipped / deviated. Every ordered item appears exactly once.

| Item | Status | Measured |
|---|---|---|
| C0a 2facdb97 | done | +290/-0, one path |
| C0b 3d2c1310 | done | +270/-156, one path |
| C1 56c463e1 | done | +4/-0, one path |
| C2 03c2a5d7 | done | +86/-0 and +92/-0, two paths |
| C3 26217cd4 | done | +56/-0, one path |
| C4 75dda620 | done | +38/-5, +33/-18, +32/-6, three paths |
| C5 03fdd2bc | done | +62/-0 and +19/-7, two paths |
| C6 ad01827b | done | +24/-23, one path |
| C7 | done | this commit; its own SHA and insertion count are reported in the round report (R-0149) |
| 1 | done | `pwd` printed FIRST = /home/decodeux/Repos/remedy; `git status --porcelain` EMPTY before C0a and before C7; `git worktree list` ONE line at round start and at handback; `.agent/STOP` ABSENT at both |
| 2 | done | base `git rev-parse HEAD` = ab1d234436a1ffdab66cb395d3edb4b3fd6f2a5d — equals ab1d2344 |
| 3 | done | `.agent/authored/f083-r18.md` and `.agent/last_block.md` READ FROM HEAD are both sha256 272806846bd4e2048e3b610bed706b8b60a72024888a28bb6f398570a6833ca6, 23774 bytes, 290 lines; the scratch `.remedy-wt/f083-r18-block.md` is the same digest; ALL THREE EQUAL |
| 4 | done | pre 249551 B prefixes post 255203 B; post[len(pre):] EQUALS the RECORD-R17 slice extracted from the COMMITTED authored file by its markers, 5652 B, sha256 e5e9700351fb859ad306ec77c510efd98b93378900f6dfa6c7e95f8ad31f8f94; numstat `4 0`, deletion column 0. Zero marker LINES reached the file; the one `--- BEGIN SLICE` occurrence the slice adds is mid-line quoted prose inside the R17 record's own text |
| 5 | done | `.agent/plan.md` byte-equals its PLAN slice; sha256 2691f111be84108af0c46e57e6d137e773ec43617b26b1dc350b3e286549fa99, 2477 bytes, 42 lines (<50), `## Goal` and `## Next Steps` present, 0 `- [ ]` lines |
| 6 | done | `python3 -m ruff check .` → final line `Found 26 errors.`, exit 1. Taken TWICE with the same value: once BEFORE any pytest ran this round, and again at HEAD before every gate suite. EQUAL to the 26-error base — the four new/changed Python files add none |
| 7 | done | at HEAD: passed true, fail_count 0, check_count 5; handler_import pass `handlers=338`; live_review_verdict pass; plan_consistency pass (`unchecked=0, context_complete=False`); relevant_untracked pass (`untracked=0, relevant=0`); high_blockers_open pass |
| 8 | done | `python3 -m pytest tests/orchestration/test_ci_budgets.py -q` → 10 passed, exit 0 |
| 9 | done | the four suites in one unpiped process → 36 passed, exit 0. All four paths resolve on disk; none produced exit 4 |
| 10 | done | RED. In `.remedy-wt/redctl` only, `LINT_ERROR_CEILING` lowered to 0: pytest exit 1, COLOUR RED. Import path PROVEN — the probe printed `MODULE FILE: /home/decodeux/Repos/remedy/.remedy-wt/redctl/packages/orchestration/ci_budgets.py` and `CEILING SEEN: 0`. The live ratchet id `test_this_repository_really_is_at_or_below_the_lint_ceiling` fails on `26 ruff errors, ABOVE the ceiling of 0`; the two constant-pinning ids fail with it. Edit reverted, worktree removed, `git worktree list` ONE line |
| 11 | done | RED. In the same worktree, one `budgets` `test_paths` entry repointed to `tests/test_this_path_does_not_exist.py`: `test_every_test_path_a_stage_names_resolves_on_disk` fails with `AssertionError: ('budgets', 'tests/test_this_path_does_not_exist.py')`, exit 1, COLOUR RED. Edit reverted; worktree `git status --porcelain` empty before removal |
| 12 | done | `python3 -m pytest tests/docs/ -q` → 295 passed, exit 0 |
| 13 | done | the quartet plus the canary in one unpiped process → 148 passed, exit 0. `test_typescript_compiles` is in `tests/ui_server/test_dashboard_contract.py` and PASSED; the npx cache in the primary checkout is warm, so this run says nothing about R-0480 either way and no claim is made from it |
| 14 | done | 110 registered / 6 `Done:` / 0 `Landed:` / 104 open; max R-0482; next free R-0483; no duplicate id. Matches the block's expected values exactly |
| 15 | done | 12 paths at C6, every one named by this block: the six `.agent/` files, `docs/roadmap/features/T2_F083.md`, and the five Python files. C7 adds `.agent/handoff.md` as the thirteenth. Nothing outside the block's paths |
| 16 | done | insertions C0a 290, C0b 270 (verbatim single-`.agent/`-file rewrite, AGENTS.md-exempt, reported anyway), C1 4, C2 178, C3 56, C4 103, C6 24 — none over 500 |
| 17 | done | 12 `^## Q\d` headings in `.agent/f083_inventory.md`, Q1 through Q12 |
| 18 | done | no `git commit --amend`, no `git rebase` and no `git reset` was run this round (R-0477) |

## Authored-text proofs
`.remedy-wt/f083-r18-block.md`, the committed `.agent/authored/f083-r18.md` and the committed
`.agent/last_block.md` are all three byte-equal: sha256
272806846bd4e2048e3b610bed706b8b60a72024888a28bb6f398570a6833ca6, 23774 bytes, 290 lines.
Both slices were extracted from the COMMITTED authored file by their `--- BEGIN/END SLICE ---`
markers and applied programmatically; no marker LINE reached a target file. Constraint 2 held:
`.agent/live_review.md` was only appended to, and no committed text in it was edited. No
`Done:` paragraph was written by this worker; C1 carries only the reviewer's authored text.

## Deviations & assumptions
1. GATE ORDERING, declared because it cannot be met literally. Constraint 7 asks for the lint
   and integrity readings BEFORE any pytest command, but C3's measurement IS a pytest command
   and C4's `timeout_sec` is computed from it. Resolved by taking BOTH readings twice: once
   genuinely before any pytest ran (`Found 26 errors.` exit 1; integrity passed true), and once
   at HEAD after the last authoring commit and before every gate suite, with the SAME values.
   No reading was taken while a suite was running.
2. The FIRST integrity reading, taken before C2 was committed, was RED: `relevant_untracked`
   reported `2 relevant untracked: packages/orchestration/ci_budgets.py,
   tests/orchestration/test_ci_budgets.py`. That is the check working — the files were authored
   and not yet committed. It is recorded rather than hidden; committing C2 turned it green and
   the HEAD reading is the reported one.
3. C4 SCOPING, one clause implemented differently from the block's wording. The block orders
   four selection tests scoped to `runs_in_ci and not stage.test_paths`. Applied literally to
   `test_no_test_in_this_repository_escapes_all_five_stages` that also drops the `excluded`
   stage from the union, and the complement then reports every live-provider test as an
   escapee — the gate would go red for a reason the block did not intend. Implemented as
   `not stage.test_paths`: path-bearing stages are out, `excluded` stays in. The other three
   tests use `runs_in_ci and not stage.test_paths` exactly as ordered. The test was renamed to
   `test_no_test_in_this_repository_escapes_the_marker_selected_stages` and its docstring
   states both reasons.
4. A pre-commit run of the five CI suites (46 passed, exit 0) was made before C4 was committed,
   so that no untested code was committed. It is a pytest command and is declared here for the
   same ordering reason as deviation 1; the reported gate 8 and 9 values are from the later
   runs at HEAD.
5. Two shell invocations were denied by this session class and produced NO reading: one using
   output redirection with `$?`, and one `for`-loop probe. Nothing was recorded from either.
   Gate 6 was additionally run once with `--statistics` for a compact view; the ordered bare
   `python3 -m ruff check .` was then run at HEAD and THAT run is the reported value.
6. This handoff is 154 lines, over the 60-line cap. Mandated cause (DECISION D15): the
   per-commit tables
   for nine commits, the item-status table covering C0a-C7 plus all eighteen gates with their
   real measured values, the authored-text proof and the declared deviations do not fit in 60
   lines. No section was dropped and no transcript was padded.

## Open findings
110 registered, 6 resolved, 104 open. Max id R-0482, next free id R-0483.

## Next
1. Read `.agent/STOP` from disk (self-drive Phase 1 rule 1) — before anything else.
2. Run the Open PR Gate: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
3. Then R19, as the repaired `.agent/plan.md` names it: rule on R-0480 — the `ui` stage is RED
   on a clean checkout with a cold npx cache, so T2_F083's Acceptance line "clean checkout:
   green" is not met today. It is a SPLIT round.
Fortschritt: 58 % (F083 beansprucht · R1 bis R7 und R9 bis R17 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die Selektionstests und die gemessenen Stage-Budgets als Code gelandet · neu in R18: die budgets-Stage mit dokumentierter Lint-Decke, D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler auf einer Ratsche ein · noch offen: R-0480 (ui-Stage rot auf frischem Checkout mit kaltem npx-Cache) und T003 mit den hosted workflows) — Rundenzahl gemessen, Prozentwert geschätzt
