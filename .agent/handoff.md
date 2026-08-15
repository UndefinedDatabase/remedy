# Handback — F083 R2 (CI self-check · T001 marker inventory)

Feature/Round: F083, R2 of 8. Branch: `feature/f083-ci-self-check`.
BASE 928120aba07685c010ef159fded34554085796ee; `git rev-parse HEAD` taken before the
first commit is that same value — EQUAL to the declared 928120ab (gate 2, R-0428).
Open findings: 80 · max id R-0452 · next free R-0453 · 0 resolved. No PR exists for
this branch (Constraint 3); F083's PR is created at closure.

Fortschritt: 5 % (F083 beansprucht · R1 PASS · R-0451 und R-0452 registriert · T001-Marker-Inventar gemessen und geschrieben · noch kein Stage-Runner, kein Code) — gemessen, nicht geschätzt

## Range
Review of 928120aba07685c010ef159fded34554085796ee..HEAD — five commits: the four
tabled below plus the C3 commit that writes this file.

## Commits
### 3affaf9e chore(f083): save the R2 block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r2.md | +277/-0 | C0a byte copy of the scratchpad original |

### 2f0799a4 chore(f083): mirror the R2 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +212/-248 | C0b mirror of the same 23836 bytes |

### cadc73f2 docs(f083): record the R1 verdict and register R-0451 and R-0452
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | C1 GATE-R1-BLOCK appended at EOF, deletions 0 |

### d2282fca docs(f083): write the T001 marker inventory and rule the red-stage decision
| Path | +/- | Reason |
|---|---|---|
| .agent/f083_inventory.md | +334/-0 | C2 the worker-authored T001 inventory (NEW) |
| .agent/decisions.md | +22/-0 | C2 DEC-D1 appended at EOF |
| .agent/context.md | +3/-2 | C2 CTX-R2 rewrite pair |
| .agent/plan.md | +23/-22 | C2 PLAN whole-file slice |

### (SHA cannot exist here) docs(f083): write the R2 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | whole-file rewrite | C3; a handoff cannot table its own SHA (R-0149, R-0371) |

## External actions
`git push -u origin feature/f083-ci-self-check` runs AFTER this commit; its result is in
the round's final message, as the block itself orders (R-0449, R-0452). No `gh pr create`
(Constraint 3). No worktree added (Constraint 4). The `remedy` CLI was not invoked — it is
denied in this session class, so gate 11 ran the integrity gate in Python (R-0408).

## Verification — real measured values, exit codes read from the process object
1. `git status --porcelain` EMPTY (0 lines) before C0a and again before this commit;
   the post-C3 reading is in the final message. `git worktree list` = 1 line throughout.
   `.agent/STOP` ABSENT at round start and again now (R-0347).
2. BASE: `git rev-parse HEAD` before the first commit =
   928120aba07685c010ef159fded34554085796ee. EQUALS the declared 928120ab.
3. TRANSPORT, bytes read in Python: `.remedy-wt/.cache/f083-r2/f083-r2.md`,
   `.agent/authored/f083-r2.md` and `.agent/last_block.md` are each sha256
   6521fd1cbe019c44cb0093c5af9c62427c5c7179ce31eced251bed45cd41002a, 23836 bytes,
   277 lines; all three byte strings EQUAL = True; measured 277 == declared footer 277.
4. C1 PREFIX PROPERTY over cadc73f2^..cadc73f2: pre 138302 B, post 144333 B,
   `post.startswith(pre)` True, `post[len(pre):] == b"\n" + GATE-R1-BLOCK` True
   (slice sha256 9923bf5ac7cdbbe7d9b32c08c81c57cf04808f3b13d472f9ac203e8702ebbeda,
   6030 B, 5 lines, extracted by marker from the COMMITTED authored file).
   numstat `6	0	.agent/live_review.md` — deletion column 0.
5. C2 APPLIED TEXT at d2282fca, each against the marker-extracted slice:
   (a) `.agent/decisions.md` pre 340076 B, post 341347 B, prefix True,
       `post[len(pre):] == b"\n" + DEC-D1` True.
   (b) `.agent/context.md` FROM in pre 1 · FROM in post 0 · TO in post 1 ·
       `FROM in TO` False · `pre.replace(FROM,TO) == post` True.
   (c) `.agent/plan.md` byte-equals PLAN True · sha256
       9e1c41a287dfb427d576835b44d0c07c73a923f4823e200c18805a88d9c6fc75 · 41 lines
       (<50 True) · `## Goal` True · `## Next Steps` True · `- [ ]` lines 0.
6. THE INVENTORY: `.agent/f083_inventory.md` is 334 lines. Questions asked 8,
   questions answered 8. One-line summaries:
   Q1 nine markers declared in `pyproject.toml` `[tool.pytest.ini_options] markers`;
      `tests/conftest.py::pytest_collection_modifyitems` is the only automatic assigner
      (7 markers, via 5 filename sets and 3 path rules); `unit` and `slow` are
      never auto-assigned and reach tests only by decorator or module `pytestmark`.
   Q2 collected: unit 208 · integration 10961 · subprocess 1585 · smoke 23 · slow 7 ·
      real_ollama 79 · ui_contract 397 · safety 33 · architecture 71 · whole suite 17007.
   Q3 `integration`, `subprocess`, `smoke` exist; `ui-contract` and `live-provider` do
      NOT exist in any spelling on disk outside roadmap prose; `real_ollama` carries the
      live-provider role. The disagreement is recorded, not resolved.
   Q4 fast 3970 · standard 12546 · ui 397 · smoke 23 · excluded 79; union 17007 = whole
      suite, uncovered 0; NOT disjoint — one overlap, standard ∩ smoke = 8 node ids in
      `tests/cli/test_pytest_runner.py`, which sits in both SUBPROCESS_FILES and SMOKE_FILES.
   Q5 all six stage runs exit 0, 0 failed: fast 391.8 s (3963 passed, 7 skipped) ·
      ui 8.1 s · smoke 11.1 s · safety 19.4 s · architecture 4.8 s · standard `-n auto`
      134.1 s (12545 passed, 1 skipped). `excluded` NOT run, with its operator command.
   Q6 NO `ci` command exists — three greps empty plus a 1082-file path scan, 0 hits.
   Q7 NO hosted workflow files — the repository has no `.github` directory at all.
   Q8 reuse `scripts/remedy_pytest_runner.py::run` (+ `remedy_pytest.sh`'s flock), the
      `command_catalog.GROUPS`/`CATALOG` + `commands/__init__.collect_all_handlers` seam,
      and pytest-xdist 3.8.0; `packages/orchestration/test_runner.py::run_tests_local` is
      the target-repo runner and is NOT the same seam.
7. THE INVENTORY'S ARITHMETIC, RE-DERIVED AT HEAD d2282fca with a clean tree, by
   re-collecting all six selections rather than restating Q4: union size 17007,
   whole-suite collected 17007, uncovered count 0 (empty list), union minus suite 0,
   sum of the five sizes 17015 (17015 − 17007 = 8). Pairwise overlaps: standard ∩ smoke
   = 8; the other nine pairs are all 0. This reproduces Q4 exactly; nothing differs.
8. VERIFICATION, each run separately, exit code from the process object (R-0438); all
   four paths resolved on disk before running. `tests/docs/` 295 collected, 295 passed,
   exit 0 · `tests/regression/test_resource_safety.py` 21 collected, 21 passed, exit 0 ·
   `tests/orchestration/test_integrity_gate.py` 15 collected, 15 passed, exit 0 · canary
   `tests/cli/test_golden_path.py` 42 collected, 42 passed, exit 0. All four equal the
   reviewer's BASE readings.
9. CHANGE SET, `git diff --name-only 928120ab..HEAD` measured BEFORE this file was
   written, 7 paths: .agent/authored/f083-r2.md · .agent/context.md · .agent/decisions.md ·
   .agent/f083_inventory.md · .agent/last_block.md · .agent/live_review.md ·
   .agent/plan.md. Restricted to `packages/ apps/ scripts/ tests/ docs/`: EMPTY list,
   count 0. `.agent/handoff.md` is the eighth and last path.
10. OPEN SET at HEAD: `^- R-\d+ — ` paragraphs 80 · `^Done: R-\d+ — ` lines 0 ·
    difference 80 · max id R-0452 · next free R-0453 · duplicate ids none.
11. INTEGRITY GATE in Python: `passed` true, `fail_count` 0, `check_count` 5 —
    handler_import pass "handlers=337" · live_review_verdict pass "> Round-by-round review
    record for the F083 branch, reset at the feature claim." · plan_consistency pass
    "unchecked=0, context_complete=False" · relevant_untracked pass "untracked=0,
    relevant=0" · high_blockers_open pass "no open blocker/high findings".
12. Insertions (`+` column only): 3affaf9e 277 · 2f0799a4 212 · cadc73f2 6 ·
    d2282fca 382. None over 500. C0b is a verbatim single-`.agent/`-file rewrite and is
    exempt by the AGENTS.md counting rule; its number is reported anyway. C3's own
    insertion count cannot exist inside C3 (R-0149) — it is in the final message.

## Authored-text proofs
Every slice was extracted BY MARKER from the COMMITTED `.agent/authored/f083-r2.md` in
Python and applied byte-verbatim; none was retyped. Equality is proved as byte equality
plus sha256 rather than by `cmp`, whose availability varies in this session class
(R-0408): GATE-R1-BLOCK via gate 4, DEC-D1 via gate 5(a), CTX-R2 FROM/TO via gate 5(b),
PLAN via gate 5(c). Every comparison True. `.agent/f083_inventory.md` is NOT an authored
slice — it is worker prose from worker measurements, as the block prescribes.

## Deviations & assumptions
1. DEFECT IN THE BLOCK TEXT, declared and NOT repaired (Constraint 2). The PLAN slice's
   Risks section reads "Five of the six findings registered on this branch", while the
   same slice's opening paragraph reads "plus R-0448 to R-0452 registered on this branch"
   — five, not six. Gate 10 measures 80 open with max R-0452, which agrees with five.
   Applied byte-verbatim; the contradiction now sits on disk in `.agent/plan.md`.
2. DEFECT IN THE BLOCK TEXT, declared and NOT repaired. Q5 orders stage runs for
   `safety` and `architecture`, but Q4 defines only five selections and none of them is
   named safety or architecture, so the block ordered two runs whose selection it never
   states. Interpreted by analogy with the `ui` and `smoke` rows — `-m "safety and not
   real_ollama"` and `-m "architecture and not real_ollama"` — and both exact commands
   are recorded in the inventory's Q5 table so the reading is auditable.
3. DECISION F083 D1 was NOT exercised: every one of the six stage runs exited 0 with 0
   failures, so no red-stage data was recorded under it. The decision is ruled and on
   disk regardless, as ordered.
4. Per the block's own closing paragraph, the push result, the post-C3
   `git status --porcelain`, the `gh pr list --state open` reading and C3's own insertion
   count are NOT written here — they postdate this commit (R-0449, R-0452). They are
   reported in the round's final message.
5. Handoff length: this file is over the 60-line cap, under the DECISION D15 stated-cause
   rule — twelve mandated gate readings including eight per-question inventory summaries,
   five per-commit tables and a thirty-one-row item-status table do not fit. No section
   was dropped.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a authored copy | done | |
| C0b last_block mirror | done | |
| C1 live_review append | done | |
| C2 inventory, DEC-D1, CTX-R2, PLAN | done | |
| C3 handback | done | own SHA not tabled (R-0149) |
| Gate 1 clean tree, worktree, STOP | done | post-C3 status in final message |
| Gate 2 BASE | done | equal to 928120ab |
| Gate 3 transport | done | |
| Gate 4 C1 prefix property | done | |
| Gate 5 C2 applied text (a)(b)(c) | done | |
| Gate 6 inventory answers 8 of 8 | done | |
| Gate 7 arithmetic re-derived at HEAD | done | reproduces Q4 exactly |
| Gate 8 pytest, four targets | done | |
| Gate 9 change set | done | |
| Gate 10 open set | done | |
| Gate 11 integrity gate | done | |
| Gate 12 insertions per commit | done | C3's own count in final message |
| Q1 markers and assigners | done | |
| Q2 collected per marker | done | |
| Q3 feature-file names vs disk | done | |
| Q4 stage counts, cover, disjointness | done | |
| Q5 stage wall time and outcome | deviated | safety/architecture selections not stated by the block; see deviation 2 |
| Q6 existing `ci` command | done | absent |
| Q7 hosted workflow files | done | absent |
| Q8 what to reuse | done | |
| Constraint 1 change set | done | packages/ apps/ scripts/ tests/ docs/ all empty |
| Constraint 2 byte-verbatim slices | done | two block defects declared, not repaired |
| Constraint 3 C1 before C2, no PR | done | push after C3 |
| Constraint 4 no worktree added | done | `git worktree list` 1 line |
| Constraint 5 measure, never estimate | done | no `not-measured` value occurs |
| Constraint 6 red stage is data | done | not exercised; no stage was red |

## Next
The reviewer reviews 928120ab..HEAD and issues the R2 verdict; then R3 builds T001 — the
stage runner, the marker selections and the summary table — over the shape this
inventory settles. The next session's first action is Phase 1 rule 1: re-read
`.agent/STOP` from disk before anything else.
