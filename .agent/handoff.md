# Handback — F083 CI self-check, round R14

Branch: feature/f083-ci-self-check. BASE a677c3ba (gate 2: `git rev-parse HEAD`
before the first commit was a677c3bab027842f1fb8bb93d57748ca6b6bd230 — EQUALS
a677c3ba). Round start: `pwd` = /home/decodeux/Repos/remedy, `git status
--porcelain` EMPTY, `git worktree list` ONE line, `.agent/STOP` ABSENT. Before
C4: porcelain EMPTY, worktree ONE line, `.agent/STOP` ABSENT (gate 1).

## Range

Review of a677c3ba..HEAD.

## Commits

### 32b50bb3 docs(f083): save the R14 block verbatim (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r14.md | +301/-0 | the block, byte-verbatim |

### 3fc3e8ad docs(f083): mirror the R14 block into last_block (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +147/-127 | byte-identical mirror of C0a |

### e31972b1 docs(f083): record the R13 PASS and register R-0475 and R-0476 (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | RECORD-R13 appended at EOF |

### 23913f84 docs(f083): complete the three-sample serial reading of standard (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/f083_inventory.md | +76/-0 | the `## Q11` section appended |

### e52e2d06 docs(f083): point the plan at the R15 budget and timeout work (C3)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18/-17 | PLAN slice as a whole file |

C4 writes `.agent/handoff.md` and cannot table its own SHA or its own insertion
count (R-0371, R-0149); both are in the final message.

## External actions

`git push -u origin feature/f083-ci-self-check` after C4 — result in the final
message, it postdates this file (R-0449, R-0452). NO worktree added, NO PR
created, NO merge. Scratch `.remedy-wt/f083-r14/` did NOT exist before this round
created it (constraint 6); it is gitignored at `.gitignore:235`.

## Verification

1. pwd/porcelain/worktree/STOP — above. 2. BASE a677c3ba — EQUAL.
3. TRANSPORT: `.agent/authored/f083-r14.md` and `.agent/last_block.md` both
sha256 9ece6420fe5f8eba…9993e, 27455 bytes, 301 lines, EQUAL=True; each equals
its committed blob at C0a and C0b. Measured line count 301; cap 400; at-or-under
= True. No trailing-whitespace line.
4. C1: pre prefixes post True; tail == `b"\n" + RECORD-R13` extracted from the
COMMITTED authored file by its markers True; numstat `6 0` — deletions 0.
5. C2: pre prefixes post True; tail begins with exactly
`b"\n## Q11 — The three-sample serial cost of `standard`, completed at R14\n"`
True; numstat `76 0` — deletions 0.
6. C2 STRUCTURE: 11 `^## Q\d` lines, ordered Q1 Q2 Q3 Q4 Q5 Q6 Q7 Q8 Q9 Q10 Q11,
no number repeated; `## Q5 — Measured wall time and outcome per stage` = 1,
`## Q9 — Stage runtime, measured at R11` = 1, `## Q10 — Serial stage cost through
the production runner, measured at R13` = 1. `^## ` lines pre 11, post 12 — C2
added exactly 1.
7. C2 CONTENT: 3 SAMPLE rows — sample 1 taken at R13 (copied from the uncapped
probe in `## Q10`, not re-measured), samples 2 and 3 taken at R14. RED CONTROL
exit code 5, whole output `17045 deselected in 3.47s`, run FIRST. Samples: 1 —
927.72 s exit 0; 2 — 935.14 s exit 0; 3 — 916.36 s exit 0, each at
`REMEDY_PYTEST_TIMEOUT_SEC=5400`, named as an override. Provenance command
`git diff --name-only fb9ddf12..HEAD -- packages/ scripts/` printed NOTHING.
Precision convention as written: every wall second at exactly two decimals, every
derived value computed from the numbers AS PUBLISHED (min 916.36, max 935.14,
max−min 18.78 — and 935.14−916.36 = 18.78). `not measured` occurs 2×,
`not run` 2×. DECLARATION: `## Q11` contains no ceiling, no budget number and no
recommendation.
8. CI SUITES, each its own process, real exit code: test_ci_stages.py `7 passed`
exit 0; test_ci_stage_selection.py `9 passed` exit 0; test_ci_cmd.py `6 passed`
exit 0; test_ci_run.py `8 passed` exit 0. All four paths resolve on disk.
9. VERIFICATION, each separately: test_dashboard_contract.py `70 passed` exit 0;
test_resource_safety.py `21 passed` exit 0; test_integrity_gate.py `15 passed`
exit 0; canary test_golden_path.py `42 passed` exit 0. All four paths resolve.
10. C3 PLAN byte-equals its PLAN slice: True, sha256
fcacccfc3a49961f…776b, 40 lines (under 50), `## Goal` present, `## Next Steps`
present, 0 `- [ ]` lines, 1 numbered item under `## Next Steps`.
11. `git diff --name-only a677c3ba..HEAD -- packages/ apps/ tests/ scripts/
docs/` printed NOTHING (empty list). `git diff --name-only fb9ddf12..HEAD --
packages/ scripts/` printed NOTHING (empty list) — the provenance proof. Both run
from the repository root.
12. INTEGRITY (Python, `remedy` CLI denied — R-0408): passed True, fail_count 0,
check_count 5; handler_import pass `handlers=338` (BASE value, no handler added),
live_review_verdict pass, plan_consistency pass `unchecked=0,
context_complete=False`, relevant_untracked pass `untracked=0, relevant=0`,
high_blockers_open pass.
13. OPEN SET at HEAD, MEASURED: 104 registered, 6 `Done:`, 0 `Landed:`, open 98,
max R-0476, next free R-0477, no duplicate id — matches the reviewer's expected
104 / 6 / 0 / 98 / R-0476 / R-0477.
14. CHANGE SET at C3: `.agent/authored/f083-r14.md`, `.agent/f083_inventory.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` — count 5.
`.agent/handoff.md` is the sixth path, added by C4.
15. INSERTIONS: C0a +301, C0b +147 (verbatim single-`.agent/`-file rewrite,
AGENTS.md-exempt, reported anyway), C1 +6, C2 +76, C3 +18. None over 500. C4's
own count cannot exist inside C4 (R-0149) — final message.

## Authored-text proofs

RECORD-R13 and PLAN were both extracted from the COMMITTED
`.agent/authored/f083-r14.md` by their markers and applied byte-verbatim: gate 4
proves RECORD-R13 by byte equality of the append tail, gate 10 proves PLAN by
whole-file byte equality. The `## Q11` body is worker-authored from measurements,
so no byte-equality proof exists or was ordered for it (block SHAPES, gate 5).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this file; cannot table its own SHA |
| Gate 1 | done | clean at both readings |
| Gate 2 | done | BASE equals a677c3ba |
| Gate 3 | done | 301 lines, under the 400 cap |
| Gate 4 | done | byte-equal tail, deletions 0 |
| Gate 5 | done | prefix + first line, deletions 0 |
| Gate 6 | done | Q1–Q11, one `^## ` line added |
| Gate 7 | done | 3 samples, red control 5, no ceiling |
| Gate 8 | done | 7/9/6/8 passed, all exit 0 |
| Gate 9 | done | 70/21/15/42 passed, all exit 0 |
| Gate 10 | done | byte-equal, 40 lines |
| Gate 11 | done | both ranges empty |
| Gate 12 | done | passed True, handlers=338 |
| Gate 13 | done | 104 / 6 / 0, open 98 |
| Gate 14 | done | 5 paths |
| Gate 15 | done | max +301, none over 500 |

## Deviations & assumptions

Deviations, declared: this handback is 162 lines and exceeds BOTH caps that
bind it — the AGENTS.md ≤100-line cap for a >5-commit handback and the
docs/agents/handback_template.md ≤100-line cap in the same case (R-0462). The
cause is mandated content, not prose: fifteen ordered gate values, six
per-commit changed-files tables, and a 21-row item-status table covering every
C-item and every gate. No section was dropped and no gate value was trimmed.
Assumptions: none. No slice was repaired; no defect in reviewer text was found.

## Open findings

104 registered, 6 `Done:`, 0 `Landed:` — 98 open. Max R-0476, next free R-0477.
R-0475 is RESOLVED by C3 of this round; R-0476 is OPEN and its convention is
stated and obeyed by `## Q11`.

## Next

R15: carry a per-stage timeout in the stage table and write the budget stage from
the `## Q11` spread, rule on R-0468 from the 26-error ruff baseline `## Q10`
records, and settle the determinism stage's shape as a DECISION.

Fortschritt: 47 % (F083 beansprucht · R1 bis R7 und R9 bis R13 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht und die Selektionstests samt Live-Wächter als Code gelandet · R13 hat gemessen, dass `remedy ci` seine grösste Stage heute nach 600 Sekunden abschneidet, R14 vervollständigt die serielle Messung von `standard` auf drei Samples · noch keine Determinismus- oder Budget-Stage, kein Ceiling, kein Timeout-Fix, keine hosted workflows) — Rundenzahl gemessen, Prozentwert geschätzt
