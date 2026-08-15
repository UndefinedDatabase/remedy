# Handback — F083 R4 (CI self-check · record R3, repair the round map, build the stage table)

Feature/Round: F083, R4 of 11. Branch: `feature/f083-ci-self-check`.
BASE 83d4a6496971064b9e7ac7059755862481bb5be0; `git rev-parse HEAD` taken before the
first commit is that same value — EQUAL to the declared 83d4a649 (gate 2, R-0428).
Open findings: 83 · max id R-0455 · next free R-0456 · 0 resolved. No PR exists for
this branch (Constraint 3); F083's PR is created at closure.

Fortschritt: 14 % (F083 beansprucht · R1 bis R3 PASS · Marker-Inventar gemessen · Stage-Set per DECISION F083 D2 entschieden · Stage-Tabelle als Code gelandet mit Struktur-Guards · noch kein Stage-Runner, keine CLI, keine hosted workflows) — gemessen, nicht geschätzt

## Range
Review of 83d4a6496971064b9e7ac7059755862481bb5be0..HEAD — seven commits: the six
tabled below plus the C5 commit that writes this file.

## Commits
### ef63c686 chore(f083): save the R4 block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r4.md | +396/-0 | C0a byte copy of the scratchpad original |

### 47313a95 chore(f083): mirror the R4 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +324/-158 | C0b mirror of the same 25711 bytes |

### d0ef752b docs(f083): record the R3 verdict and register R-0455
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C1 GATE-R3-BLOCK appended at EOF, deletions 0 |

### fa002acb docs(f083): repair the round map for the rounds that remain
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +12/-6 | C2 STEPS-FROM → STEPS-TO in place, R-0455's repair |

### 8ffc78cf feat(f083): add the CI stage table and its structural guards
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ci_stages.py | +98/-0 | C3 NEW, the D2 stage set as data |
| tests/orchestration/test_ci_stages.py | +67/-0 | C3 NEW, structural guards over that table |

### 513bbc6f chore(f083): point the plan at R4 and the rounds that follow
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-19 | C4 PLAN whole-file slice |

### (SHA cannot exist here) docs(f083): write the R4 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | whole-file rewrite | C5; a handoff cannot table its own SHA (R-0149, R-0371) |

## External actions
`git push -u origin feature/f083-ci-self-check` runs AFTER this commit; its result is in
the round's final message, as the block itself orders (R-0449, R-0452). No `gh pr create`
(Constraint 3). No worktree added (Constraint 4). The `remedy` CLI was not invoked — it is
denied in this session class, so gate 12 ran the integrity gate in Python (R-0408).

## Verification — real measured values, exit codes read from the process object
1. `git status --porcelain` EMPTY (0 lines) before C0a and again before this commit;
   the post-C5 reading is in the final message. `git worktree list` = 1 line throughout.
   `.agent/STOP` ABSENT at round start and again now (R-0347).
2. BASE: `git rev-parse HEAD` before the first commit =
   83d4a6496971064b9e7ac7059755862481bb5be0. EQUALS the declared 83d4a649.
3. TRANSPORT, bytes read in Python: `.remedy-wt/.cache/f083-r4/f083-r4.md`,
   `.agent/authored/f083-r4.md` and `.agent/last_block.md` are each sha256
   3ae4f3b405cf1f65080217f69f73fdc93392ebc893874a7db2d8d03292790ab9, 25711 bytes,
   396 lines; all three byte strings EQUAL = True; measured 396 == declared footer 396.
4. C1 PREFIX PROPERTY over d0ef752b^..d0ef752b, both blobs read from git: pre 150497 B,
   post 154993 B, `post.startswith(pre)` True, `post[len(pre):] == b"\n" + GATE-R3-BLOCK`
   True (slice 4495 B, 3 lines, extracted by marker from the COMMITTED authored file).
   numstat `4	0	.agent/live_review.md` — deletion column 0.
5. C2 REWRITE PAIR at fa002acb, both slices marker-extracted from the same committed
   authored file: over the WHOLE `.agent/live_review.md`, STEPS-FROM occurs 0x and
   STEPS-TO occurs 1x (before the edit: 1x and 0x). Inside the STEPS SECTION only —
   bytes between the line `## Steps` and the line `## Findings`, 1322 B — the literal
   `R3 T001` occurs 0x and `R4 T001 the stage definitions` occurs 1x.
   numstat `12	6	.agent/live_review.md`.
6. C3 NEW FILES, each read back from the commit with `git show HEAD:<path>` and compared
   with the marker-extracted slice: `packages/orchestration/ci_stages.py` byte-equals
   CI-STAGES True · sha256 6fb04d77bc4aae2e6f4ab5929c2577229da20213c2636b5e0fd5556f40e9f990
   · 3838 B · 98 lines. `tests/orchestration/test_ci_stages.py` byte-equals TEST-CI-STAGES
   True · sha256 d61b189366699ea65fae6e58937031cf6dedcf8e567e3ec4add6a71f68a14919 · 2355 B
   · 67 lines. Both ADDED: numstat `98	0` and `67	0`, deletion column 0 on both.
7. C3 RUNS GREEN, both paths confirmed to resolve on disk first, each command run
   separately with `subprocess.run(...).returncode` (R-0438):
   `python3 -m ruff check packages/orchestration/ci_stages.py tests/orchestration/test_ci_stages.py`
   → exit 0, stdout `All checks passed!`. `python3 -m pytest
   tests/orchestration/test_ci_stages.py -q` → 7 collected, 7 passed, exit 0. Both equal
   the reviewer's BASE-worktree readings. Repository-wide `ruff check` was NOT run (R-0364).
8. C4 PLAN byte-equals the PLAN slice as a whole file True · sha256
   cdaa06847f2b700548fab7baaccb8cd7a113b35fe0f0d2e8f44cf9b8f8ce13c5 · 2372 B · 41 lines
   (<50 True) · `## Goal` True · `## Next Steps` True · `- [ ]` lines 0.
9. CHANGE SET, `git diff --name-only 83d4a649..HEAD` measured BEFORE this file was
   written, 6 paths: .agent/authored/f083-r4.md · .agent/last_block.md ·
   .agent/live_review.md · .agent/plan.md · packages/orchestration/ci_stages.py ·
   tests/orchestration/test_ci_stages.py. Restricted to `apps/ scripts/ docs/`: EMPTY
   list, count 0. Restricted to `.agent/f083_inventory.md`: EMPTY list — not touched.
   `.agent/handoff.md` is the seventh and last path.
10. VERIFICATION, each run separately, exit code from the process object (R-0438); all
    four paths resolved on disk before running. `tests/ui_server/test_dashboard_contract.py`
    70 collected, 70 passed, exit 0 · `tests/regression/test_resource_safety.py` 21
    collected, 21 passed, exit 0 · `tests/orchestration/test_integrity_gate.py` 15
    collected, 15 passed, exit 0 · canary `tests/cli/test_golden_path.py` 42 collected,
    42 passed, exit 0. All four equal the reviewer's BASE readings. `tests/docs/` was not
    run: the change set holds no `docs/roadmap/**` path.
11. OPEN SET at HEAD: `^- R-\d+ — ` paragraphs 83 · `^Done: R-\d+ — ` lines 0 ·
    difference 83 · max id R-0455 · next free R-0456 · duplicate ids none. R3's recorded
    reading was 82 / max R-0454, so C1 added exactly the one ordered id.
12. INTEGRITY GATE in Python: `passed` true, `fail_count` 0, `check_count` 5 —
    handler_import pass (handlers=337) · live_review_verdict pass · plan_consistency pass
    (unchecked=0) · relevant_untracked pass (untracked=0) · high_blockers_open pass.
13. Insertions (`+` column only): C0a ef63c686 396 · C0b 47313a95 324 · C1 d0ef752b 4 ·
    C2 fa002acb 12 · C3 8ffc78cf 165 (98+67) · C4 513bbc6f 17. None over 500. C0b is a
    verbatim single-`.agent/`-file rewrite and is exempt by the AGENTS.md counting rule;
    its number is reported anyway. C5's own insertion count cannot exist inside C5
    (R-0149) — it is in the final message.

## Authored-text proofs
Every slice was extracted BY MARKER from the COMMITTED `.agent/authored/f083-r4.md` in
Python and applied byte-verbatim; none was retyped and neither new file received an added
header, a reflow or an import reorder. Equality is proved as byte equality plus sha256
rather than by `cmp`, whose availability varies in this session class (R-0408):
GATE-R3-BLOCK via gate 4, STEPS-FROM/STEPS-TO via gate 5, CI-STAGES and TEST-CI-STAGES
via gate 6, PLAN via gate 8. Every comparison True.

## Deviations & assumptions
1. No defect was found in this block's text. Nothing was repaired silently and nothing
   was interpreted: every gate subject and every gate path resolved on disk before it
   was measured.
2. Per the block's own closing paragraph, the push result, the post-C5
   `git status --porcelain`, the `gh pr list --state open` reading and C5's own insertion
   count are NOT written here — they postdate this commit (R-0449, R-0452). They are
   reported in the round's final message.
3. Handoff length: this file is 172 lines, over the 60-line cap, under DECISION D15's
   stated-cause rule — thirteen mandated gate readings, seven per-commit tables and a
   25-row item-status table do not fit. No section was dropped.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a authored copy | done | |
| C0b last_block mirror | done | |
| C1 live_review append | done | landed before C2 |
| C2 STEPS rewrite pair | done | |
| C3 two new files | done | one commit |
| C4 plan | done | |
| C5 handback | done | own SHA not tabled (R-0149) |
| Gate 1 clean tree, worktree, STOP | done | post-C5 status in final message |
| Gate 2 BASE | done | equal to 83d4a649 |
| Gate 3 transport | done | three files equal, 396 lines |
| Gate 4 C1 prefix property | done | numstat 4/0 |
| Gate 5 C2 rewrite pair | done | 0x / 1x, section 0 / 1 |
| Gate 6 C3 new files byte-equal | done | both added, deletions 0 |
| Gate 7 ruff and pytest on C3 | done | exit 0 · 7 passed exit 0 |
| Gate 8 C4 plan slice | done | 41 lines |
| Gate 9 change set | done | 6 paths, restricted lists empty |
| Gate 10 pytest, four targets | done | |
| Gate 11 open set | done | |
| Gate 12 integrity gate | done | |
| Gate 13 insertions per commit | done | C5's own count in final message |
| Constraint 1 change set | done | apps/ scripts/ docs/ empty, inventory untouched |
| Constraint 2 byte-verbatim slices | done | no block defect found, none repaired |
| Constraint 3 order and no PR | done | C1<C2<C3, push after C5 |
| Constraint 4 no worktree added | done | `git worktree list` 1 line |
| Constraint 5 no registration of the new files | done | no CLI catalog entry, no handler table row, no import from another module |

## Next
R5 wires the stage runner over the existing pytest subprocess runner
(`scripts/remedy_pytest_runner.py`), adds the `remedy ci` CLI seam Q8 names, and renders
the summary table, which states the accepted `standard`/`smoke` double-run. The next
session's first action is Phase 1 rule 1: re-read `.agent/STOP` from disk before anything
else.
