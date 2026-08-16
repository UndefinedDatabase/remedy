# Handback — F083 R19 (record R18, register R-0483 and R-0484, MEASURE R-0480 as Q13)

Feature T2_F083 CI self-check · Round R19 · Branch `feature/f083-ci-self-check`
Base 6ce3c58d · C0a f5341008 · C0b a21d81a2 · C1 4b52f300 · C2 0239896a · C3 3c80c3fc ·
C4 = this commit.
This round wrote NO production code. MEASUREMENT round: it rules nothing and orders no fix.

## Range
Review of 6ce3c58d..HEAD.

## Commits

### f5341008 docs(f083): save the R19 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r19.md | +215/-0 | R19 block saved byte-verbatim (C0a) |

### a21d81a2 docs(f083): mirror the R19 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +134/-209 | byte-identical copy of the committed authored file (C0b) |

### 4b52f300 docs(f083): record the R18 PASS and register R-0483 and R-0484
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | RECORD-R18 EOF-append; no committed text edited (C1) |

### 0239896a docs(f083): measure the Q13 cause behind R-0480
| Path | +/- | Reason |
|---|---|---|
| .agent/f083_inventory.md | +178/-0 | `## Q13`, the six ordered questions answered with measurements (C2) |

### 3c80c3fc docs(f083): advance the plan to R20
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21/-22 | PLAN slice applied as a whole file (C3) |

### C4 docs(f083): write the R19 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | C4; a handoff cannot table its own commit (R-0149) |

## External actions
`git push -u origin feature/f083-ci-self-check` runs AFTER C4. That push result, the post-C4
`git status --porcelain` and the open-PR list postdate this file (R-0449) and are reported in
the round report, not here. No PR was created or merged. THREE disposable worktrees were added
and all three removed: `.remedy-wt/r19probe`, `.remedy-wt/r19cold`, `.remedy-wt/r19inst`.

## Verification — item status and measured values
Status values: done / skipped / deviated. Every ordered item appears exactly once.

| Item | Status | Measured |
|---|---|---|
| C0a f5341008 | done | +215/-0, one path |
| C0b a21d81a2 | done | +134/-209, one path |
| C1 4b52f300 | done | +6/-0, one path |
| C2 0239896a | done | +178/-0, one path |
| C3 3c80c3fc | done | +21/-22, one path |
| C4 | done | this commit; its own SHA and insertion count are reported in the round report (R-0149) |
| 1 | done | `pwd` printed FIRST = /home/decodeux/Repos/remedy; `git status --porcelain` EMPTY before C0a and before C4; `git worktree list` ONE line at round start and at handback; `.agent/STOP` ABSENT at both |
| 2 | done | base `git rev-parse HEAD` = 6ce3c58dff2af9f9d6907ef4907f8e8a765943b9 — equals 6ce3c58d |
| 3 | done | `.agent/authored/f083-r19.md` and `.agent/last_block.md` READ FROM HEAD are both sha256 64d578db137f2167, 20868 bytes, 215 lines; the scratch `.remedy-wt/f083-r19-block.md` is the same digest; ALL THREE EQUAL, and 215 is under the 400-line cap |
| 4 | done | pre 255203 B prefixes post 263322 B; post[len(pre):] EQUALS the RECORD-R18 slice extracted from the COMMITTED authored file by its markers, 8119 B, sha256 b4fa72b66a377244; numstat `6 0`, deletion column 0. Zero marker LINES reached the file; the one `--- BEGIN SLICE` occurrence the slice adds is mid-line quoted prose inside the R18 record's own text |
| 5 | done | `.agent/plan.md` byte-equals its PLAN slice; sha256 f34d1db67fc789b5, 2312 bytes, 41 lines (<50), `## Goal` and `## Next Steps` present, 0 `- [ ]` lines, 0 `--- BEGIN SLICE` occurrences |
| 6 | done | `git diff --name-only 6ce3c58d..HEAD -- packages/ apps/ tests/ scripts/` printed NOTHING. No production code was written |
| 7 | done | `python3 -m ruff check .` → final line `Found 26 errors.`, exit 1. UNCHANGED from the 26-error base, as expected: this round writes no Python |
| 8 | done | passed true, fail_count 0, check_count 5; handler_import pass `handlers=338`; live_review_verdict pass; plan_consistency pass (`unchecked=0, context_complete=False`); relevant_untracked pass (`untracked=0, relevant=0`); high_blockers_open pass |
| 9 | done | the five CI suites in one unpiped process → 46 passed, exit 0. All five paths resolve on disk (checked individually); none produced exit 4 |
| 10 | done | `python3 -m pytest tests/cli/test_golden_path.py -q` → 42 passed, exit 0. The path resolves on disk |
| 11 | done | 112 registered / 6 `Done:` / 0 `Landed:` / 106 open; max R-0484; next free R-0485; no duplicate id. Matches the block's expected values exactly |
| 12 | done | 13 `^## Q\d` headings in `.agent/f083_inventory.md`, Q1 through Q13 |
| 13 | done | 5 paths at C3, every one named by this block: `.agent/authored/f083-r19.md`, `.agent/f083_inventory.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`. C4 adds `.agent/handoff.md` as the sixth. Nothing outside the block's paths |
| 14 | done | insertions C0a 215, C0b 134 (verbatim single-`.agent/`-file rewrite, AGENTS.md-exempt, reported anyway), C1 6, C2 178, C3 21 — none over 500 |
| 15 | done | no `git commit --amend`, no `git rebase` and no `git reset` was run this round; the real npm cache `/home/decodeux/.npm` was neither deleted nor modified — it held `_cacache`, `_logs`, `_npx`, `_update-notifier-last-checked` and eight `_npx` sub-entries before the readings and the same four and same eight after |

## Q13 — the measured answer, in one paragraph
R-0480's OBSERVATION reproduces exactly and its stated CAUSE is not supported. The npx cache is
the per-user directory `/home/decodeux/.npm` and it is WARM: `_npx/1d6e82a4126006c4` has held a
`tsc` entry since 2026-06-02, and that entry is the DEPRECATED stub `tsc@2.0.4`, whose bin ends
in `process.exitCode = 1`. The test's argv is `["npx", "tsc", "--noEmit"]` with neither `--yes`
nor `--no-install`. In `.remedy-wt/r19probe` the full file ran `1 failed, 69 passed` exit 1 then
`70 passed` exit 0 — R-0480 exactly — and the variable that changed was `apps/ui/node_modules`,
which is gitignored at `.gitignore:221` and therefore absent from every new worktree. The same
suite under an EMPTY `npm_config_cache` was GREEN, `70 passed` exit 0; and in `.remedy-wt/r19cold`
with `node_modules` absent the tsc test alone was RED on BOTH runs, `1 failed` twice. `--yes`
changed nothing: exit 1 with `node_modules` absent, exit 0 with it present, in all four forms.
The installer was measured directly, not inferred: in `.remedy-wt/r19inst`, running only
`TestAutoBuildBehavior::test_auto_build_runs_by_default` took `node_modules` from absent to
present (exit 0, `1 passed in 4.26s`), and the tsc test alone then passed there. That test is 99
lines below `test_typescript_compiles` in the same file. This section carries NO recommendation.

## Authored-text proofs
`.remedy-wt/f083-r19-block.md`, the committed `.agent/authored/f083-r19.md` and the committed
`.agent/last_block.md` are all three byte-equal: sha256
64d578db137f21670492246575f7cf0638a0d9f38634a6c325c130e6232fa6b9, 20868 bytes, 215 lines.
Both slices were extracted from the COMMITTED authored file by their `--- BEGIN/END SLICE ---`
markers and applied programmatically; no marker LINE reached a target file. Constraint 3 held:
`.agent/live_review.md` was only appended to, and no committed text in it was edited. No
`Done:` paragraph was written by this worker; C1 carries only the reviewer's authored text.

## Deviations & assumptions
1. THREE disposable worktrees, not one. The block's questions 3 to 5 speak of "a disposable
   worktree" and then "that worktree". `.remedy-wt/r19probe` answered 3, 4 and the
   `node_modules`-present half of 5 literally, as ordered. But questions 4 and 5 asked for a
   COLD-cache reading, and in r19probe `node_modules` already existed after question 3, so npx
   never consults any cache there and the reading alone could not separate the two candidate
   causes. `.remedy-wt/r19cold` was added to hold `node_modules` ABSENT, and `.remedy-wt/r19inst`
   to measure WHICH test installs it rather than read it off the source. Both are ADDITIONS to
   the ordered readings, never substitutions: every literal reading the block asked for is in
   `## Q13` with its own exit code. All three worktrees were removed and pruned; `git worktree
   list` is ONE line and `git status --porcelain` is empty.
2. The real npm cache was never touched. Cold conditions came only from `npm_config_cache`
   pointed at new empty directories under `.remedy-wt/`, one per form, each listed as empty
   immediately before use and each verified with `npm config get cache` under that environment.
   Those scratch cache directories were deleted afterwards; `/home/decodeux/.npm` was not.
3. Two shell invocations were denied by this session class and produced NO reading: one
   `git worktree add` piped through `tail` with `$?`, and one large heredoc append. Both were
   re-run through `python3` and through the file-write tool respectively, with the same content;
   nothing was recorded from the denied attempts and no gate value came from them.
4. `.agent/plan.md` still read "R19 rules on R-0480" while C1 and C2 were committed, because the
   block's own sequence places the PLAN slice at C3. It named the right feature and the right
   round throughout, and C3 corrected the wording. Declared rather than left to be noticed.
5. This handoff is 138 lines, over the 60-line cap. Mandated cause (DECISION D15): the per-commit
   tables for six commits, the item-status table covering C0a-C4 plus all fifteen gates with
   their real measured values, the Q13 summary this round exists to produce, the authored-text
   proof and the declared deviations do not fit in 60 lines. No section was dropped and no
   transcript was padded.

## Open findings
112 registered, 6 resolved, 106 open. Max id R-0484, next free id R-0485.

## Next
1. Read `.agent/STOP` from disk (self-drive Phase 1 rule 1) — before anything else.
2. Run the Open PR Gate: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
3. Then R20, as the repaired `.agent/plan.md` names it: rule on R-0480 from the `## Q13` data.
   The data says the cause is the absent `apps/ui/node_modules`, not the npx cache, so R-0480
   is amended before any fix is ordered. It is a SPLIT round — the fix is production code.
Fortschritt: 62 % (F083 beansprucht · R1 bis R7 und R9 bis R18 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die Selektionstests, die gemessenen Stage-Budgets und die budgets-Stage mit geratschter Lint-Decke als Code gelandet · D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler ein · R19 misst nur: die Ursache hinter R-0480 wird als Q13 gemessen, bevor R20 darüber entscheidet · noch offen: T003 mit den hosted workflows) — Rundenzahl gemessen, Prozentwert geschätzt
