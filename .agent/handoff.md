# Handback — F083 CI self-check, R5 (worker)

Branch: feature/f083-ci-self-check.

## Range
Review of 0e4526b0..<C5>. C5 is the commit that writes this file and cannot
carry its own SHA (R-0371, R-0149); none is invented. C5's insertion count, the
push result, the post-C5 clean-tree reading and the open-PR list all postdate
C5 and are reported in the worker's final message (R-0449, R-0452).

## Commits

### a220e903 chore(f083): save the R5 block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r5.md | +382/-0 | C0a — byte copy of the scratchpad original |

### eb94eb0d chore(f083): mirror the R5 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +291/-305 | C0b — same bytes as C0a |

### d9aa04d3 docs(f083): record the R4 verdict in the live review
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C1 — GATE-R4-BLOCK appended at EOF after one blank line |

### ff1aae12 docs(f083): split the map R5 clause into runner and CLI seam rounds
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-6 | C2 — STEPS-FROM to STEPS-TO, six whole lines in place |

### 8ab928aa feat(f083): add the CI stage runner and its wiring guards
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ci_run.py | +94/-0 | C3 — NEW, the stage runner |
| tests/orchestration/test_ci_run.py | +81/-0 | C3 — NEW, its wiring guards |

### e2c4bc8f docs(f083): point the plan at the runner round and the R6 CLI seam
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-23 | C4 — whole-file PLAN replacement |

### C5 — SHA unknowable inside itself
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | C5 — the handback, alone |

## External actions
None through C5: no push yet, no PR created, no gh command, no worktree added
or removed. `git push -u origin feature/f083-ci-self-check` runs after C5.

## Verification
Every gate below was RUN; none is reported as unrunnable. Exit codes were read
from the process object, never from a pipe (R-0438), and every path was
resolved on disk before it was used.

1. `git status --porcelain` EMPTY before the first commit and again before C5
   (both runs printed nothing). `git worktree list` ONE line both times:
   `/home/decodeux/Repos/remedy … [feature/f083-ci-self-check]`. `.agent/STOP`
   ABSENT at round start and at handback (`No such file or directory`).
2. BASE `git rev-parse HEAD` = 0e4526b05a5d940cb6d3cffc40fe6bd56e6f3342 —
   EQUAL to the declared 0e4526b0.
3. TRANSPORT, bytes read in Python: `.remedy-wt/.cache/f083-r5/f083-r5.md`,
   `.agent/authored/f083-r5.md` and `.agent/last_block.md` are each sha256
   54bd00a70d792420fe7ff66966dd284be2ddeb6a36848729bf29031aef4c8f04, 22102
   bytes, 382 lines; the three byte strings are EQUAL; the measured 382 equals
   the block's declared footer count of 382.
4. C1 PREFIX PROPERTY over d9aa04d3^..d9aa04d3, both blobs read from git: pre
   155450 B is a prefix of post 158478 B (True), and post[155450:] equals
   b"\n" + GATE-R4-BLOCK byte-for-byte (True), that slice extracted by its
   markers from the COMMITTED `.agent/authored/f083-r5.md`. numstat `2 0` —
   deletion column 0.
5. C2 REWRITE PAIR, both slices from that same committed file. Over the WHOLE
   `.agent/live_review.md` at ff1aae12: STEPS-FROM 0x, STEPS-TO 1x. The lines
   `## Steps` and `## Findings` each occur 1x, in that order; inside that
   section `R6 T001 the` = 1, `R11 the integration gate` = 1,
   `R10 the integration gate` = 0. The substring `Steps` still occurs (19x).
   numstat `6 6`.
6. C3 NEW FILES read back out of 8ab928aa and compared with the extracted
   slices: `packages/orchestration/ci_run.py` byte-equals CI-RUN — sha256
   1eab0b140529e05c90d124526165d4bf6c239ed2b1d09be033f3b4f580edd0c3, 3257 B,
   94 lines; `tests/orchestration/test_ci_run.py` byte-equals TEST-CI-RUN —
   sha256 cbe857b3afa99954e887569986750e395dffa2baafeb8aaf3608837779bacfa8,
   2517 B, 81 lines. numstat `94 0` and `81 0` — both ADDED, deletion column 0.
7. C3 RUNS GREEN, each command separately, both paths `is_file` True first.
   `python3 -m ruff check packages/orchestration/ci_run.py
   tests/orchestration/test_ci_run.py` → exit 0, "All checks passed!".
   `python3 -m pytest tests/orchestration/test_ci_run.py -q` → 6 collected,
   6 passed, exit 0. `python3 -c "import packages.orchestration.ci_run as m;
   print(m.__file__)"` → /home/decodeux/Repos/remedy/packages/orchestration/
   ci_run.py — inside the PRIMARY checkout, so the green is the committed
   code's (R-0337). Repo-wide `ruff check` was not run; it is not a gate here.
8. R4'S CODE, which this round imports:
   `python3 -m pytest tests/orchestration/test_ci_stages.py -q` → 7 collected,
   7 passed, exit 0.
9. C4 PLAN byte-equals the PLAN slice as a whole file — sha256
   8937d73f5badbdc1a6f43fd3c9c7263db004e413702221341bad6814dc8d9977, 2009 B,
   35 lines (under 50); `## Goal` and `## Next Steps` present; `- [ ]` lines: 0.
10. CHANGE SET `git diff --name-only 0e4526b0..HEAD`, measured BEFORE this file
   was written: `.agent/authored/f083-r5.md`, `.agent/last_block.md`,
   `.agent/live_review.md`, `.agent/plan.md`,
   `packages/orchestration/ci_run.py`, `tests/orchestration/test_ci_run.py` —
   count 6, with `.agent/handoff.md` the seventh and last. The same command
   restricted to `apps/ scripts/ docs/` printed NOTHING (0 paths); restricted
   to R4's two files and `.agent/f083_inventory.md` it printed NOTHING
   (0 paths).
11. VERIFICATION, each command run separately, measured value first, the
   reviewer's BASE reading in brackets:
   `tests/ui_server/test_dashboard_contract.py` → 70 passed, exit 0 [70/70, 0];
   `tests/regression/test_resource_safety.py` → 21 passed, exit 0 [21, 0];
   `tests/orchestration/test_integrity_gate.py` → 15 passed, exit 0 [15, 0];
   canary `tests/cli/test_golden_path.py` → 42 passed, exit 0 [42/42, 0].
12. OPEN SET at HEAD: `^- R-\d+ — ` paragraphs 83, `^Done: R-\d+ — ` lines 0,
   difference 83, max id R-0455, next free R-0456, duplicate ids none. No
   finding was registered this round; the measured triple equals the
   reviewer's BASE reading.
13. INTEGRITY GATE, in Python (the `remedy` CLI is denied in this session
   class, R-0408): passed true, fail_count 0, check_count 5 —
   handler_import pass (handlers=337), live_review_verdict pass,
   plan_consistency pass (unchecked=0, context_complete=False),
   relevant_untracked pass (untracked=0, relevant=0), high_blockers_open pass.
14. Insertions (`+` column only): C0a 382, C0b 291, C1 2, C2 6, C3 175, C4 17
   — none over 500. C0b is a verbatim single-`.agent/`-file rewrite and is
   exempt by the AGENTS.md counting rule; its number is reported anyway.

## Authored-text proofs
Every applied slice was extracted BY ITS MARKERS from the COMMITTED
`.agent/authored/f083-r5.md` (`git show <sha>:…`) and applied byte-verbatim;
nothing was retyped. Each equality is byte equality PLUS a sha256 computed in
Python — neither `cmp` nor `$?` was relied on (R-0408).

| Slice | Target | Proof |
|---|---|---|
| whole block | .agent/authored/f083-r5.md, .agent/last_block.md | three-way byte-equal with the scratchpad original, sha256 54bd00a7…4f04 |
| GATE-R4-BLOCK | .agent/live_review.md (C1) | post == pre + b"\n" + slice, True |
| STEPS-FROM / STEPS-TO | .agent/live_review.md (C2) | FROM 0x, TO 1x over the whole file at C2 |
| CI-RUN | packages/orchestration/ci_run.py | byte-equal out of 8ab928aa, sha256 1eab0b14…d0c3 |
| TEST-CI-RUN | tests/orchestration/test_ci_run.py | byte-equal out of 8ab928aa, sha256 cbe857b3…cfa8 |
| PLAN | .agent/plan.md | byte-equal whole file, sha256 8937d73f…9977 |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this file |
| Gate 1 clean tree / worktree / STOP | done | empty, one line, absent |
| Gate 2 BASE | done | equals 0e4526b0 |
| Gate 3 transport | done | three-way equal, 382 = 382 |
| Gate 4 C1 prefix | done | True, numstat 2 0 |
| Gate 5 C2 pair | done | 0x / 1x, 1 / 1 / 0 |
| Gate 6 C3 new files | done | both byte-equal, both added |
| Gate 7 C3 green | done | ruff 0, 6/6 exit 0, primary path |
| Gate 8 R4 code | done | 7/7, exit 0 |
| Gate 9 C4 plan | done | byte-equal, 35 lines |
| Gate 10 change set | done | 6 paths, both restrictions empty |
| Gate 11 verification | done | 70 / 21 / 15 / 42, all exit 0 |
| Gate 12 open set | done | 83 / 0 / R-0455 / R-0456 |
| Gate 13 integrity gate | done | passed true, 0 of 5 failed |
| Gate 14 insertions | done | max 382, none over 500 |

## Deviations & assumptions
1. STATED-CAUSE OVERAGE (AGENTS.md DECISION D15): this handoff is 200 lines,
   over the 100-line cap for a >5-commit round. The cause is mandated content
   only — seven per-commit changed-files tables, the fourteen gate transcripts
   the block ordered by number, the six-row authored-text proof table and the
   21-row item-status table. No section was dropped to meet the cap.
2. DECLARED, NOT REPAIRED (block constraint 2 — a defect in the block's text is
   declared, never silently fixed): the PLAN slice names TWO future rounds in
   its `## Next Steps` (item 1 R6, item 2 R7), while the map paragraph the same
   block leaves standing in `.agent/live_review.md` reads "Another file may name
   at most the NEXT round — `.agent/plan.md` must, because AGENTS.md mandates
   its Next Steps section". Disk evidence: the two numbered items in
   `.agent/plan.md` at e2c4bc8f, and that sentence inside the Steps section at
   ff1aae12. The plan at BASE had the same two-round shape (it named R5 and R6),
   so this round neither introduces nor widens the condition — it is reported
   because the block ordered the text verbatim and the rule it may cross sits in
   a file this same block rewrote. Applied as written; the reviewer rules.
3. Assumption, stated: C1's "exactly one blank line between the file's current
   last line and the first line of this slice" was applied as
   post = pre + b"\n" + slice, which is exactly what gate 4 orders byte-for-byte
   — the two readings of the instruction agree, and the file already ended in a
   newline (155450 B, ends `\n`).
4. Nothing outside the block's change set was touched: R4's `ci_stages.py` and
   `test_ci_stages.py` and `.agent/f083_inventory.md` are absent from the range
   diff (gate 10), no module registers the new code, no PR was created and no
   worktree was added.

Fortschritt: 20 % (F083 beansprucht · R1 bis R4 PASS · Marker-Inventar gemessen · Stage-Set per DECISION F083 D2 entschieden · Stage-Tabelle und Stage-Runner als Code gelandet · noch keine CLI, kein Summary, keine hosted workflows) — gemessen, nicht geschätzt

## Next
R6: the `remedy ci [--stage NAME] [--json]` CLI seam — catalog group, entry and
a `COMMAND_HANDLERS` module — plus the summary table it prints, which states the
accepted `standard`/`smoke` double-run, and one real stage invocation to prove
the subprocess seam end to end.
