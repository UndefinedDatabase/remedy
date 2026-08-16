# Handback — F083 R20 (record R19, amend and fix R-0480, promote R-0483, resolve three)

Feature T2_F083 CI self-check · Round R20 · Branch `feature/f083-ci-self-check`
Base 59d7d341 · C0a 12423e57 · C0b 0f78cdc0 · C1 b83b02c1 · C2 f31f55c3 · C3 824bb6bb ·
C4 9ae4f8aa · C5 a6daec1e · C6 0e9c72ed · C7 = this commit.
SPLIT round: one test METHOD changed under `tests/`; `packages/`, `apps/` and `scripts/` untouched.

## Range
Review of 59d7d341..HEAD.

## Commits

### 12423e57 docs(f083): save the R20 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r20.md | +276/-0 | R20 block saved byte-verbatim (C0a) |

### 0f78cdc0 docs(f083): mirror the R20 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +202/-141 | byte-identical copy of the committed authored file (C0b) |

### b83b02c1 docs(f083): record the R19 PASS and amend the R-0480 cause
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | RECORD-R19 EOF-append; no committed text edited (C1) |

### f31f55c3 docs(agents): promote R-0483 as pre-emission checklist item 13
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +17/-0 | CHECKLIST pair, append-shaped, §3 item 13 (C2) |

### 824bb6bb fix(tests): resolve the local tsc or skip with an install hint
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_dashboard_contract.py | +9/-1 | `test_typescript_compiles` only; DECISION F083 D6 (C3) |

### 9ae4f8aa docs(f083): resolve R-0483 and R-0480
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | RESOLVE EOF-append; no committed text edited (C4) |

### a6daec1e docs(f083): rule DECISION F083 D6 and record the T003 install step
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +40/-0 | DECISION F083 D6 in the file's existing entry shape (C5) |
| docs/roadmap/features/T2_F083.md | +6/-1 | the A9 UI-toolchain bullet only; ROADMAP.md untouched (C5) |

### 0e9c72ed docs(f083): advance the plan to T003
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16/-18 | PLAN slice applied as a whole file (C6) |

### C7 docs(f083): write the R20 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | C7; a handoff cannot table its own commit (R-0149) |

## External actions
`git push -u origin feature/f083-ci-self-check` runs AFTER C7. That push result, the post-C7
`git status --porcelain` and the open-PR list postdate this file (R-0449) and are reported in the
round report, not here. No PR was created or merged. ONE disposable worktree was added and
removed: `.remedy-wt/r20probe` (gate 11).

## Verification — item status and measured values
Status values: done / skipped / deviated. Every ordered item appears exactly once.

| Item | Status | Measured |
|---|---|---|
| C0a 12423e57 | done | +276/-0, one path |
| C0b 0f78cdc0 | done | +202/-141, one path |
| C1 b83b02c1 | done | +6/-0, one path |
| C2 f31f55c3 | done | +17/-0, one path |
| C3 824bb6bb | done | +9/-1, one path, one method |
| C4 9ae4f8aa | done | +4/-0, one path |
| C5 a6daec1e | done | +40/-0 and +6/-1, two paths |
| C6 0e9c72ed | done | +16/-18, one path |
| C7 | done | this commit; its own SHA and insertion count are in the round report (R-0149) |
| 1 | done | `pwd` printed FIRST = /home/decodeux/Repos/remedy; `git status --porcelain` EMPTY before C0a and before C7; `git worktree list` ONE line at round start and at handback; `.agent/STOP` ABSENT at both |
| 2 | done | base `git rev-parse HEAD` = 59d7d341faef7f905ced4abed255dc54d02e45b0 — equals 59d7d341 |
| 3 | done | `.agent/authored/f083-r20.md` and `.agent/last_block.md` READ FROM HEAD are both sha256 8f77255a7c0328c8, 24374 bytes, 276 lines; the scratch `.remedy-wt/f083-r20-block.md` is the same digest; ALL THREE EQUAL |
| 4 | done | C1: pre 263322 B prefixes post 269472 B, tail 6150 B byte-EQUALS the RECORD-R19 slice extracted from the COMMITTED authored file by its markers, numstat `6 0`. C4: pre 269472 B prefixes post 271015 B, tail 1543 B byte-EQUALS the RESOLVE slice, numstat `4 0`. Deletion column 0 both times; no marker line and no FROM:/TO: label reached the file |
| 5 | done | the FROM string occurred exactly **1x** in `docs/agents/planner_reviewer_prompt.md` before C2 and was replaced once; all **17** TO-ONLY lines occur exactly **1x** each among the 17 lines C2's diff ADDS, and C2 adds no other line |
| 6 | done | `.agent/plan.md` byte-equals its PLAN slice; sha256 900ce257188f5781, 2149 bytes, **39 lines** (<50), `## Goal` and `## Next Steps` present, **0** `- [ ]` lines, 0 `--- BEGIN SLICE` occurrences |
| 7 | done | `git diff --name-only 59d7d341..HEAD -- packages/ apps/ scripts/` printed NOTHING (empty stdout, exit 0) |
| 8 | done | `python3 -m ruff check .` → final line `Found 26 errors.`, exit 1 — UNCHANGED, breakdown 20 I001 / 4 F401 / 1 F821 / 1 UP035. The edited test file alone: `All checks passed!`, exit 0. Taken at C3, before any pytest command ran this round |
| 9 | done | passed **true**, fail_count **0**, check_count **5**; exit 0. Taken at C3, before any pytest command ran this round |
| 10 | done | `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q` → **70 passed**, exit 0, zero skips. `test_typescript_compiles` **PASSED** — confirmed by name with `-v -k typescript_compiles`: `PASSED`, `1 passed, 69 deselected`, and `apps/ui/node_modules/.bin/tsc` is a file here |
| 11 | done | THE PROBE in `.remedy-wt/r20probe` at 824bb6bb, `apps/ui/node_modules` absent by construction: **SKIPPED**, exit **0**, summary `1 skipped, 69 deselected in 0.11s`, reason `UI toolchain absent: …/r20probe/apps/ui/node_modules is missing; run \`npm ci --prefix apps/ui\``. Not PASSED and not FAILED — the intended outcome. Worktree removed and pruned; `git worktree list` is ONE line |
| 12 | done | the five CI suites in one unpiped process → **46 passed**, exit 0 |
| 13 | done | `python3 -m pytest tests/docs/ -q` → **295 passed**, exit 0. Run TWICE: once before C5 and again AFTER C5, which is the commit that changes `docs/roadmap/**`; both readings are 295 passed, exit 0 |
| 14 | done | the verification set plus the canary → **78 passed**, exit 0. All three paths resolve on disk (checked individually); none produced exit 4 |
| 15 | done | **112** registered / **9** `Done:` / **0** `Landed:` / **103** open; max **R-0484**; next free **R-0485**; no duplicate id. Matches the block's expected values exactly. The new `Done:` ids are R-0483 and R-0480; the `Amended: R-0480` paragraph is correctly NOT counted as a registration |
| 16 | done | 8 paths at C6, every one named by this block: `.agent/authored/f083-r20.md`, `.agent/decisions.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md`, `docs/roadmap/features/T2_F083.md`, `tests/ui_server/test_dashboard_contract.py`. C7 adds `.agent/handoff.md` as the ninth. Nothing outside the block's paths |
| 17 | done | insertions 276, 202, 6, 17, 9, 4, 46, 16 for C0a…C6 — none over 500 |
| 18 | done | no `git commit --amend`, no `git rebase` and no `git reset` was run this round |

## Authored-text proofs
`.remedy-wt/f083-r20-block.md`, the committed `.agent/authored/f083-r20.md` and the committed
`.agent/last_block.md` are all three byte-equal: sha256
8f77255a7c0328c81bd31eb2f91397266215f805d2fb8f4ca3511c0bfe868402, 24374 bytes, 276 lines.
All four slices were extracted from the COMMITTED authored file by their `--- BEGIN/END SLICE ---`
markers and applied programmatically; no marker LINE and no `FROM:`/`TO:` label reached a target
file. Constraint 2 held: `.agent/live_review.md` was only appended to, at C1 and C4, and no
committed text in it was edited. No `Done:` or `Landed:` line was written by this worker — C1 and
C4 carry only the reviewer's authored text.

## Deviations & assumptions
1. **The WHY comment at C3 is TWO lines, not one.** The block orders "a one-line WHY comment"
   that names R-0480 AND DECISION F083 D6 AND states that `npx` resolves a cached `tsc@2.0.4`
   stub when no local TypeScript exists AND that the old form graded the stub's exit code. That
   content is ~148 characters; this repository's ruff `line-length` is 120 (`pyproject.toml:38`),
   so the mandated content cannot fit on one line without going red on the very lint gate the
   same block freezes at 26. Two lines is the fewest that carries all of it; both are ≤101
   characters and the file is ruff-clean. The comment sits directly above the `if not
   local_tsc.is_file():` guard, i.e. directly above the skip.
2. **Gate 13 was run twice**, before and after C5. The block lists it among gates whose order it
   does not fix, but its stated reason is "because C5 changes `docs/roadmap/**`", so a reading
   taken before C5 would not be a reading of the change it exists to gate. Both runs are 295
   passed, exit 0; the post-C5 run is the binding one. This is exactly the class of defect the
   checklist item 13 promoted at C2 describes, caught here rather than reported.
3. **Gates 8 and 9 were taken at C3, not at the base.** The prompt orders both readings before
   any pytest command runs this round, and the block additionally expects the ruff count to be
   unchanged BY the round — which only a reading that includes the edited test can show. C3 is
   the last commit that can change either value, and no pytest command had run at that point, so
   one reading satisfies both requirements. Naming the commit rather than relying on "before" is
   the item-13 rule applied to this round's own constraint.
4. **Every gate ran through `python3 -c`/`subprocess.run` rather than a bare shell line.** This
   session class denies `$?` and `echo "X=$?"` forms. Each gate is still its OWN unpiped process
   and every exit code reported above was read from THAT process's return code, never from a
   pipeline's tail.
5. This handoff is 148 lines, over the 60-line cap. Mandated cause (DECISION D15): per-commit
   tables for nine commits, the item-status table covering C0a-C7 plus all eighteen ordered
   gates with their real measured values, the transport and pair proofs, and the declared
   deviations do not fit in 60 lines. No section was dropped and no transcript was padded.

## Open findings
112 registered, 9 resolved, 103 open. Max id R-0484, next free id R-0485.

## Next
1. Read `.agent/STOP` from disk (self-drive Phase 1 rule 1) — before anything else.
2. Run the Open PR Gate: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
3. Then T003, the last slice: the hosted workflow files calling the same `remedy ci` entrypoint,
   the docs, and the runtime-budget documentation. Its first reviewed round also records THIS
   round's verdict, which lives only in the round report until it does. The workflow MUST run
   `npm ci --prefix apps/ui` before the `ui` stage — DECISION F083 D6 makes that step
   load-bearing.
Fortschritt: 78 % (F083 beansprucht · R1 bis R7 und R9 bis R19 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · T001 und T002 fertig: Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die Selektionstests, die gemessenen Stage-Budgets und die budgets-Stage mit geratschter Lint-Decke · D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler ein, D6 lässt den tsc-Check den LOKALEN Compiler auflösen statt einen gecachten tsc@2.0.4-Stub zu benoten · offen ist nur noch T003: hosted workflows, Docs und das Laufzeit-Budget, danach Integration Gate und Closure) — Rundenzahl gemessen, Prozentwert geschätzt
